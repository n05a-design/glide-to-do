"""Begrenzte Bildkonversion ohne Tk: Dateicache, Abbruch und ein Worker (WA-26)."""
from collections import OrderedDict, deque
from dataclasses import dataclass, field
import hashlib
import base64
import os
import subprocess
import tempfile
import threading
import time

import preview_tools

MAX_CONVERTED = 1600


def stamp(path):
    try:
        info = os.stat(path)
    except OSError:
        return None
    return os.path.normcase(os.path.abspath(path)), info.st_mtime_ns, info.st_size


def windows_convert_command(source, target, max_kante=MAX_CONVERTED):
    # Ungeprüfte Pfade dürfen nicht Bestandteil von PowerShell-Quelltext sein.
    # UTF-8/Base64 transportiert Unicode und alle Anführungszeichen unverändert.
    def encoded(value):
        return base64.b64encode(os.fspath(value).encode('utf-8')).decode('ascii')
    script = (
        "$ErrorActionPreference='Stop';Add-Type -AssemblyName PresentationCore;"
        f"$src=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('{encoded(source)}'));"
        f"$dst=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('{encoded(target)}'));"
        "$s=[System.IO.File]::OpenRead($src);try{"
        "$d=[System.Windows.Media.Imaging.BitmapDecoder]::Create($s,"
        "[System.Windows.Media.Imaging.BitmapCreateOptions]::PreservePixelFormat,"
        "[System.Windows.Media.Imaging.BitmapCacheOption]::OnLoad);$f=$d.Frames[0];"
        f"$k=[Math]::Min(1.0,{int(max_kante)}/[Math]::Max($f.PixelWidth,$f.PixelHeight));"
        "$b=New-Object System.Windows.Media.Imaging.TransformedBitmap($f,"
        "(New-Object System.Windows.Media.ScaleTransform($k,$k)));"
        "$e=New-Object System.Windows.Media.Imaging.PngBitmapEncoder;"
        "$e.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($b));"
        "$o=[System.IO.File]::Create($dst);"
        "try{$e.Save($o)}finally{$o.Close()}}finally{$s.Close()}"
    )
    return ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", script]


def run_converter(command, cancel, timeout=45, **options):
    """Pipes abholen, Zeitlimit einhalten und abgebrochene Kinder sicher einsammeln."""
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **options) as process:
        deadline = time.monotonic() + timeout
        try:
            while not cancel.is_set() and time.monotonic() < deadline:
                try:
                    process.communicate(timeout=min(0.1, max(0.001, deadline-time.monotonic())))
                    return process.returncode == 0 and not cancel.is_set()
                except subprocess.TimeoutExpired:
                    pass
            return False
        finally:
            if process.poll() is None:
                process.kill()
            process.communicate()


def convert_file(path, cache_dir, platform, expected=None, cancel=None, runner=run_converter):
    """Nur vollständige Ergebnisse zum unveränderten Quellstand atomar veröffentlichen."""
    cancel = cancel or threading.Event()
    expected = expected or stamp(path)
    if expected is None or cancel.is_set() or stamp(path) != expected:
        return None
    base = os.path.join(cache_dir, hashlib.sha1(repr(expected).encode('utf-8')).hexdigest())
    for suffix in ('.png', '.ppm'):
        if os.path.isfile(base+suffix) and os.path.getsize(base+suffix) > 0:
            return base+suffix
    temporary = None
    try:
        os.makedirs(cache_dir, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix='glide-vorschau-', suffix='.png', dir=cache_dir)
        os.close(fd)
        options = {}
        suffix = '.png'
        if platform == 'darwin':
            command = ['sips', '-s', 'format', 'png', '-Z', str(MAX_CONVERTED), path, '--out', temporary]
        elif platform == 'nt':
            command = windows_convert_command(path, temporary)
            options['creationflags'] = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
        else:
            size = None
            if os.path.splitext(path)[1].lower() in preview_tools.JPEG:
                with open(path, 'rb') as source:
                    size = preview_tools.jpeg_size(source.read(256*1024))
            plan = preview_tools.linux_plan(path, temporary[:-4], size, MAX_CONVERTED)
            if plan is None:
                return None
            command, output = plan
            if output != temporary:
                os.unlink(temporary)
                temporary = output
            suffix = os.path.splitext(output)[1]
        if not runner(command, cancel, **options) or cancel.is_set() or stamp(path) != expected:
            return None
        if not os.path.isfile(temporary) or os.path.getsize(temporary) == 0:
            return None
        target = base+suffix
        os.replace(temporary, target)
        temporary = None
        return target
    except (OSError, subprocess.SubprocessError, ValueError):
        return None
    finally:
        if temporary:
            try:
                os.unlink(temporary)
            except OSError:
                pass


@dataclass
class Task:
    key: tuple
    work: object
    cancel: threading.Event = field(default_factory=threading.Event)
    status: str = 'queued'
    result: object = None


class ConversionService:
    """Ein lazily gestarteter Daemon, begrenzte Warteschlange und negative Ergebnisse.

    Keine UI-Rückrufe im Worker. Der Hauptthread fragt status/result ab. Ein
    abgebrochener alter Auftrag darf einen neueren derselben Kennung nicht ersetzen.
    """
    def __init__(self, capacity=32, history=256):
        self.capacity = capacity
        self.history = max(capacity+1, history)
        self._condition = threading.Condition()
        self._queue = deque()
        self._tasks = OrderedDict()
        self._thread = None
        self._closed = False
        self._diagnostics = OrderedDict()

    def diagnostics(self):
        """Höchstens 16 Fehlerklassen mit Anzahl, ohne Pfad, Schlüssel oder Fehlertext.

        Abfrage im Hauptthread möglich; keine UI-Rückrufe aus dem Worker.
        Erwartete negative Konvertierungsergebnisse erzeugen keinen Eintrag.
        """
        with self._condition:
            return tuple(self._diagnostics.items())

    def submit(self, key, work, retry=False):
        with self._condition:
            if self._closed:
                return 'closed'
            task = self._tasks.get(key)
            if task and task.status != 'cancelled' and not (retry and task.status == 'failed'):
                self._tasks.move_to_end(key)
                return task.status
            if len(self._queue) >= self.capacity:
                return 'busy'
            task = Task(key, work)
            self._tasks[key] = task
            self._queue.append(task)
            if self._thread is None:
                self._thread = threading.Thread(target=self._run, name='glide-bildkonversion', daemon=True)
                self._thread.start()
            self._condition.notify()
            return task.status

    def state(self, key):
        with self._condition:
            task = self._tasks.get(key)
            return (task.status, task.result) if task else ('missing', None)

    def cancel(self, key):
        with self._condition:
            task = self._tasks.get(key)
            if task and task.status in ('queued', 'running'):
                task.cancel.set()
                task.status = 'cancelled'
                self._queue = deque(t for t in self._queue if t is not task)

    def forget(self, key=None):
        with self._condition:
            for candidate in list(self._tasks):
                if (key is None or candidate == key) and self._tasks[candidate].status not in ('queued', 'running'):
                    del self._tasks[candidate]

    def close(self):
        with self._condition:
            self._closed = True
            for task in self._tasks.values():
                if task.status in ('queued', 'running'):
                    task.cancel.set()
                    task.status = 'cancelled'
            self._queue.clear()
            self._condition.notify_all()

    def _run(self):
        while True:
            with self._condition:
                while not self._queue and not self._closed:
                    self._condition.wait()
                if self._closed:
                    return
                task = self._queue.popleft()
                task.status = 'running'
            error_kind = None
            try:
                result = task.work(task.cancel)
            except Exception as exc:
                # Ein defektes Bild beendet nicht den gemeinsamen Worker.
                # Nur der Klassenname, niemals Dateinamen oder private Meldungen.
                error_kind = type(exc).__name__[:80]
                result = None
            with self._condition:
                if self._tasks.get(task.key) is task and not task.cancel.is_set():
                    if error_kind:
                        count = self._diagnostics.pop(error_kind, 0)
                        self._diagnostics[error_kind] = min(count + 1, 1000000)
                        while len(self._diagnostics) > 16:
                            self._diagnostics.popitem(last=False)
                    task.result = result
                    task.status = 'ready' if result else 'failed'
                for key in list(self._tasks):
                    if len(self._tasks) <= self.history:
                        break
                    if self._tasks[key].status not in ('queued', 'running'):
                        del self._tasks[key]
