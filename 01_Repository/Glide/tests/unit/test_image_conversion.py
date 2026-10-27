"""Konversion, Workergrenzen und Abbruch ohne Tk oder echte Nutzerdaten."""
from pathlib import Path
import ast
import base64
import os
import re
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
import image_conversion as conversion


def wait_for(predicate, timeout=4):
    deadline = time.monotonic()+timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(.005)
    raise AssertionError('Workerzustand nicht rechtzeitig erreicht')


class Files(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='glide-bildunit-')
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)/'quelle.jpg'
        self.source.write_bytes(b'Quelle')
        self.cache = Path(self.temp.name)/'cache'

    def convert(self, runner, **options):
        return conversion.convert_file(str(self.source), str(self.cache), 'darwin', runner=runner, **options)

    def test_atomic_success_and_reuse(self):
        calls = []
        def runner(command, cancel, **options):
            calls.append(command)
            Path(command[-1]).write_bytes(b'fertiges PNG')
            return True
        result = self.convert(runner)
        self.assertEqual(Path(result).read_bytes(), b'fertiges PNG')
        self.assertEqual(self.convert(runner), result)
        self.assertEqual(len(calls), 1)
        self.source.write_bytes(b'Neue Quelle mit anderer Groesse')
        self.assertNotEqual(self.convert(runner), result)

    def test_partial_output_is_not_published(self):
        def runner(command, cancel, **options):
            Path(command[-1]).write_bytes(b'unvollstaendig')
            return False
        self.assertIsNone(self.convert(runner))
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_source_change_discards_conversion(self):
        def runner(command, cancel, **options):
            Path(command[-1]).write_bytes(b'alt')
            self.source.write_bytes(b'Inzwischen geaendert')
            return True
        self.assertIsNone(self.convert(runner))
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_cancel_discards_conversion(self):
        cancel = threading.Event()
        def runner(command, event, **options):
            Path(command[-1]).write_bytes(b'alt')
            event.set()
            return True
        self.assertIsNone(self.convert(runner, cancel=cancel))
        self.assertEqual(list(self.cache.iterdir()), [])

    def test_missing_or_already_cancelled_does_not_start(self):
        cancel = threading.Event(); cancel.set()
        def unexpected(*args, **kwargs):
            self.fail('Konverter unnoetig gestartet')
        self.assertIsNone(self.convert(unexpected, cancel=cancel))
        self.source.unlink()
        self.assertIsNone(self.convert(unexpected))

    def test_actual_child_cancel_and_timeout(self):
        for cancelled in (False, True):
            cancel = threading.Event()
            timer = threading.Timer(.1, cancel.set) if cancelled else None
            if timer:
                timer.start()
            start = time.monotonic()
            self.assertFalse(conversion.run_converter([sys.executable, '-c', 'import time;time.sleep(60)'],
                                                     cancel, timeout=.2 if not cancelled else 10))
            self.assertLess(time.monotonic()-start, 5)
            if timer:
                timer.join()

    def test_nonzero_child_is_failure(self):
        self.assertFalse(conversion.run_converter([sys.executable, '-c', 'raise SystemExit(7)'], threading.Event()))

    def test_windows_paths_are_encoded_data_not_script_syntax(self):
        source = "C:/Bilder/‘ ’ ‚ ‛ “ ” „ $ ; O'Brian/Quelle.bmp"
        target = "C:/Cache/‘Neues’ Bild.png"
        script = conversion.windows_convert_command(source, target)[-1]
        encoded = re.findall(r"FromBase64String\('([^']+)'\)", script)
        self.assertEqual([base64.b64decode(v).decode('utf-8') for v in encoded], [source, target])
        self.assertNotIn(source, script)
        self.assertNotIn(target, script)

    @unittest.skipUnless(os.name == 'nt', 'Echte WIC-Wandlung braucht Windows')
    def test_native_windows_conversion_with_unusual_paths(self):
        folder = self.source.parent / "‘ ’ ‚ ‛ “ ” „ $ ; O'Brian"
        folder.mkdir()
        source, target = folder / 'Quelle.bmp', folder / 'Ergebnis.png'
        pixels = b'\xff\x00\x00' * 2 + b'\0\0'
        bitmap = (b'BM' + struct.pack('<IHHI', 70, 0, 0, 54)
                  + struct.pack('<IiiHHIIiiII', 40, 2, 2, 1, 24, 0, 16, 0, 0, 0, 0)
                  + pixels * 2)
        source.write_bytes(bitmap)
        self.assertTrue(conversion.run_converter(conversion.windows_convert_command(source, target),
                                                 threading.Event(), timeout=20,
                                                 creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)))
        self.assertEqual(target.read_bytes()[:8], b'\x89PNG\r\n\x1a\n')


class Worker(unittest.TestCase):
    def setUp(self):
        self.service = conversion.ConversionService(capacity=1, history=4)
        self.addCleanup(self.service.close)

    def test_single_worker_deduplicates_and_bounds_queue(self):
        entered = threading.Event(); release = threading.Event(); calls = []
        self.addCleanup(release.set)
        def work(cancel):
            calls.append(threading.get_ident()); entered.set(); release.wait(3)
            return 'fertig'
        self.service.submit(('a',), work)
        self.assertTrue(entered.wait(2))
        self.assertEqual(self.service.submit(('a',), work), 'running')
        self.assertEqual(self.service.submit(('b',), lambda c:'b'), 'queued')
        self.assertEqual(self.service.submit(('c',), lambda c:'c'), 'busy')
        release.set()
        wait_for(lambda:self.service.state(('b',))[0]=='ready')
        self.assertEqual(len(calls), 1)
        self.assertNotEqual(calls[0], threading.get_ident())

    def test_failure_is_cached_until_retry(self):
        calls = []
        def fail(cancel):
            calls.append(1); return None
        self.service.submit(('a',), fail)
        wait_for(lambda:self.service.state(('a',))[0]=='failed')
        self.assertEqual(self.service.submit(('a',), fail), 'failed')
        self.assertEqual(len(calls), 1)
        self.service.submit(('a',), lambda c:'neu', retry=True)
        wait_for(lambda:self.service.state(('a',))==('ready','neu'))

    def test_queued_cancellation_does_not_run(self):
        entered=threading.Event(); release=threading.Event(); calls=[]
        self.addCleanup(release.set)
        self.service.submit(('a',),lambda c:(entered.set(), release.wait(3)))
        self.assertTrue(entered.wait(2))
        self.service.submit(('b',),lambda c:calls.append(1))
        self.service.cancel(('b',)); release.set()
        wait_for(lambda:self.service.state(('a',))[0]=='ready')
        self.assertEqual(calls,[])
        self.assertEqual(self.service.state(('b',))[0],'cancelled')

    def test_cancelled_old_task_cannot_replace_new_generation(self):
        entered=threading.Event(); release=threading.Event()
        self.addCleanup(release.set)
        def old(cancel):
            entered.set(); release.wait(3); return 'alt'
        self.service.submit(('a',),old); self.assertTrue(entered.wait(2))
        self.service.cancel(('a',))
        self.service.submit(('a',),lambda c:'neu'); release.set()
        wait_for(lambda:self.service.state(('a',))==('ready','neu'))

    def test_exceptions_do_not_kill_worker_and_history_is_bounded(self):
        def broken(cancel):
            raise ValueError('defektes Bild')
        self.service.submit(('a',),broken)
        wait_for(lambda:self.service.state(('a',))[0]=='failed')
        for i in range(8):
            self.service.submit((i,),lambda c:'ok')
            wait_for(lambda:self.service.state((i,))[0]=='ready')
        self.assertLessEqual(len(self.service._tasks),4)

    def test_close_cancels_active_and_rejects_new_tasks(self):
        entered=threading.Event(); stopped=threading.Event()
        def work(cancel):
            entered.set(); cancel.wait(3); stopped.set()
        self.service.submit(('a',),work); self.assertTrue(entered.wait(2))
        self.service.close(); self.assertTrue(stopped.wait(2))
        self.assertEqual(self.service.submit(('b',),lambda c:'b'),'closed')

    def test_diagnostics_are_bounded_and_do_not_contain_private_error_details(self):
        for number in range(19):
            exception = type(f'ConversionFailure{number}', (Exception,), {})

            def fail(cancel, exception=exception):
                raise exception('C:/Privat/Mein Bild.jpg: geheimer Inhalt')

            self.service.submit(('Privater Pfad', number), fail)
            wait_for(lambda:self.service.state(('Privater Pfad', number))[0]=='failed')
        diagnostics = self.service.diagnostics()
        self.assertEqual(len(diagnostics), 16)
        self.assertEqual(diagnostics[-1], ('ConversionFailure18', 1))
        self.assertNotIn('Privat', repr(diagnostics))
        self.assertNotIn('geheimer Inhalt', repr(diagnostics))
        self.service.submit(('nochmals',), fail)
        wait_for(lambda:self.service.state(('nochmals',))[0]=='failed')
        self.assertEqual(self.service.diagnostics()[-1], ('ConversionFailure18', 2))

    def test_expected_failure_and_cancelled_exception_do_not_add_diagnostics(self):
        self.service.submit(('negative',), lambda cancel: None)
        wait_for(lambda:self.service.state(('negative',))[0]=='failed')
        entered, release = threading.Event(), threading.Event()
        self.addCleanup(release.set)

        def cancelled(cancel):
            entered.set()
            release.wait(3)
            raise ValueError('abgebrochen')

        self.service.submit(('cancelled',), cancelled)
        self.assertTrue(entered.wait(2))
        self.service.cancel(('cancelled',))
        release.set()
        self.service.submit(('after',), lambda cancel: 'ok')
        wait_for(lambda:self.service.state(('after',))[0]=='ready')
        self.assertEqual(self.service.diagnostics(), ())

    def test_module_has_no_tk_import(self):
        tree=ast.parse(Path(conversion.__file__).read_text(encoding='utf-8'))
        imports=[n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        imports += [a.name for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names]
        self.assertFalse(any('tkinter' in str(x) for x in imports))


if __name__=='__main__':
    unittest.main()
