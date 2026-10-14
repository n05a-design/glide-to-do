"""Tatsächliche NVDA-Sprache bei Tastaturbedienung der künstlichen Glide-App."""
import argparse
from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import traceback

from reader_nvda import Spy, prepare, require_hosted


def wait_value(path, condition, timeout=20):
    deadline = time.monotonic()+timeout
    last = None
    while time.monotonic() < deadline:
        if path.is_file():
            last = json.loads(path.read_text(encoding='utf-8'))
            if condition(last):
                return last
        time.sleep(.1)
    raise AssertionError('Reader-Probe wartet vergeblich auf ' + path.name + ': ' + str(last))


def run(destination, app_path):
    destination = require_hosted(destination)
    executable, profile = prepare(destination)
    result = dict(reader='NVDA 2026.2', nur_kuenstliche_daten=True, exitcode=1, speech=[],
                  menschliche_abnahme='offen; tatsächliche automatisierte Readerausgabe separat')
    child = None
    with (destination/'nvda-prozess.log').open('w', encoding='utf-8') as reader_log, \
            (destination/'glide-prozess.log').open('w', encoding='utf-8') as app_log:
        reader = subprocess.Popen([str(executable), '--minimal', '-c', str(profile),
                                   '--debug-logging', '--log-file', str(destination/'nvda.log')],
                                  stdout=reader_log, stderr=subprocess.STDOUT)
        try:
            spy = Spy(destination)
            spy.wait_ready()
            exchange = destination/'glide-diagnose'
            child = subprocess.Popen([sys.executable, '-B', str(Path(__file__).with_name('reader_app400.py')),
                                      '--app', str(app_path), '--diagnose', str(exchange)],
                                     stdout=app_log, stderr=subprocess.STDOUT,
                                     env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            ready = wait_value(exchange/'bereit.json', lambda value: value.get('tk') == '9.1.0')
            pid = ready['pid']
            assert pid == child.pid, 'Nur die gestartete Glide-Testinstanz darf bedient werden'

            def key(gesture):
                spy.key(pid, gesture)
                time.sleep(.1)

            def speak_focus():
                index = spy.next_speech()
                key('insert+tab')
                value = spy.speech(index)
                result['speech'].append(value)
                return value

            def focus_expected(text):
                value = speak_focus()
                assert text in value, (text, value)
                return value

            def find_by_tab(text, *, role=None):
                for _ in range(90):
                    key('tab')
                    spoken = speak_focus()
                    if text in spoken and (role is None or role in spoken.casefold()):
                        return spoken
                raise AssertionError('Per Tab und NVDA nicht erreichbar: ' + text)

            def type_text(text):
                for char in text:
                    assert char.isascii() and (char.isalpha() or char == ' ')
                    key('space' if char == ' ' else 'shift+'+char.lower() if char.isupper() else char)

            key('control+n')
            focus_expected('Neue Aufgabe')
            type_text('Angebot pruefen')
            key('enter')
            wait_value(exchange/'zustand.json', lambda value: len(value['tasks']) == 1)
            key('control+f')
            focus_expected('Aufgaben suchen')
            type_text('Angebot')
            key('escape')
            find_by_tab('Aufgaben', role='tree')
            key('home')
            focus_expected('Angebot pruefen')
            key('control+shift+p')
            key('home')
            focus_expected('Heute')
            key('enter')
            wait_value(exchange/'zustand.json', lambda value: value['tasks'][0].get('planned_date') == date.today().isoformat())
            find_by_tab('Arbeitsbereiche', role='tree')
            key('home')
            key('down')
            focus_expected('Heute')
            wait_value(exchange/'zustand.json', lambda value: value['view'] == ready['plan_day_view'])
            find_by_tab('Aufgaben', role='tree')
            key('home')
            focus_expected('Angebot pruefen')
            key('f2')
            focus_expected('Aufgabentitel')
            key('control+a')
            type_text('Angebot bearbeitet')
            key('control+s')
            wait_value(exchange/'zustand.json', lambda value: value['tasks'][0].get('text') == 'Angebot bearbeitet')
            find_by_tab('Bearbeitungstag')
            find_by_tab('Neuer Checklistenpunkt')
            type_text('Unterlagen pruefen')
            key('enter')
            wait_value(exchange/'zustand.json', lambda value: len(value['tasks'][0].get('checklist', [])) == 1)
            before = find_by_tab('Unterlagen pruefen')
            assert 'check box' in before.casefold(), before
            key('space')
            wait_value(exchange/'zustand.json', lambda value: value['tasks'][0]['checklist'][0]['done'])
            checked = focus_expected('Unterlagen pruefen')
            assert 'checked' in checked.casefold() and 'not checked' not in checked.casefold(), checked
            key('space')
            wait_value(exchange/'zustand.json', lambda value: not value['tasks'][0]['checklist'][0]['done'])
            key('control+z')
            final = wait_value(exchange/'zustand.json', lambda value: value['tasks'][0]['checklist'][0]['done'])
            assert not final['callback_errors'], final['callback_errors']
            assert not final['tasks'][0].get('due'), 'Einplanen darf keine Fälligkeit setzen'
            result.update(exitcode=0, version=ready['version'], tk=ready['tk'], checks=[
                'NVDA benennt Erfassung, Suche, Aufgabenliste und Inspektorfelder bei echter Tastaturbedienung',
                'Reader benennt ausgewählte Aufgabe und Heute-Menü; tatsächliche Heute-Ansicht erreicht, keine Fälligkeit; Titel gespeichert',
                'Checklistenpunkt per Tastatur hinzugefügt; NVDA meldet native Checkbox und Checked-Zustand',
                'Leertaste und ein Undo verändern den gespeicherten Datensatz; keine Callbackfehler'])
        except BaseException as error:
            result.update(fehler=str(error), traceback=traceback.format_exc())
        finally:
            state_path = destination/'glide-diagnose/zustand.json'
            if state_path.is_file():
                result['app_callback_errors'] = json.loads(state_path.read_text(encoding='utf-8'))['callback_errors']
            if child is not None and child.poll() is None:
                child.terminate()
                child.wait(timeout=15)
            subprocess.run([str(executable), '-q'], stdout=reader_log, stderr=subprocess.STDOUT, timeout=15)
            try:
                reader.wait(timeout=15)
            except subprocess.TimeoutExpired:
                reader.terminate()
                reader.wait(timeout=15)
    (destination/'reader-ergebnis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return result['exitcode']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ziel', type=Path, required=True)
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[2]/'src/glide/app.pyw')
    args = parser.parse_args()
    return run(args.ziel, args.app.resolve())


if __name__ == '__main__':
    raise SystemExit(main())
