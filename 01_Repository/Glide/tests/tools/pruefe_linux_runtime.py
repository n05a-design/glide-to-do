"""Künstliche Tk-9.1-Fixture und externer AT-SPI-Verbraucher im Hosted-CI."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


def child(exchange):
    # Der Elternprozess besitzt und entfernt diesen neuen Datenordner.
    if not os.environ.get('GLIDE_DATA_DIR'):
        raise ValueError('Temporärer Testdatenordner fehlt.')
    import tkinter as tk
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src/glide'))
    from core_accessibility import bind_entry
    root = tk.Tk()
    root.title('Glide – künstliche AT-SPI-Textprobe')
    root.geometry('500x200')
    text = '  Angebot prüfen 🏠\nZweite Zeile'
    field = tk.Text(root, height=4)
    field.insert('1.0', text)
    field.pack()
    bind_entry(field, 'AT-SPI-Prüffeld', text=True)
    field.mark_set('insert', '1.3')
    field.focus_force()
    def ready():
        (exchange / 'bereit.json').write_text(json.dumps(dict(pid=os.getpid(), text=text,
            name='AT-SPI-Prüffeld', caret=3, tk=str(root.tk.call('package', 'provide', 'Tk')),
            native_backend=field._glide_accessibility.supported)), encoding='utf-8')
    root.after(300, ready)
    root.after(90_000, root.destroy)
    try:
        root.mainloop()
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass


def run(runtime, destination):
    temporary = Path(os.environ['RUNNER_TEMP']).resolve()
    destination = destination.resolve()
    if (sys.platform != 'linux' or os.environ.get('GITHUB_ACTIONS') != 'true' or
            os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted' or
            destination == temporary or not destination.is_relative_to(temporary)):
        raise ValueError('Nur eigener vergänglicher Linux-CI-Prüfstand unter RUNNER_TEMP.')
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Native Textprobe benötigt einen neuen leeren Diagnoseordner.')
    result = dict(exitcode=1, nur_kuenstliche_daten=True, orca_sprachausgabe='getrennt offen')
    with tempfile.TemporaryDirectory(prefix='glide-native-atspi-', dir=temporary) as data:
        env = dict(os.environ, GLIDE_DATA_DIR=data, PYTHONPATH=str(runtime / 'python-extension'))
        with (destination / 'tk-prozess.log').open('w', encoding='utf-8') as log:
            process = subprocess.Popen([sys.executable, '-B', str(Path(__file__).resolve()),
                '--kind', str(destination)], env=env, stdout=log, stderr=subprocess.STDOUT)
            try:
                deadline = time.monotonic()+30
                ready_path = destination / 'bereit.json'
                while not ready_path.is_file() and process.poll() is None and time.monotonic() < deadline:
                    time.sleep(.1)
                if not ready_path.is_file():
                    raise RuntimeError('Native Tk-Fixture nicht gestartet; Prozesscode '+str(process.poll()))
                ready = json.loads(ready_path.read_text(encoding='utf-8'))
                if ready['pid'] != process.pid or ready['tk'] != '9.1.0' or not ready['native_backend']:
                    raise RuntimeError('Eigene native Tk-9.1-Fixture nicht belegt.')
                report = destination / 'atspi-text.json'
                consumer = subprocess.run(['/usr/bin/python3', '-B', str(Path(__file__).with_name('pruefe_native_atspi.py')),
                    '--pid', str(process.pid), '--name', ready['name'], '--text', ready['text'],
                    '--caret', str(ready['caret']), '--bericht', str(report)],
                    env=env, timeout=45)
                result.update(exitcode=consumer.returncode, tk=ready['tk'], native_backend=True)
            except Exception as error:
                result['fehler'] = str(error)
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait(timeout=10)
    (destination / 'ergebnis.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))
    return result['exitcode']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--runtime', type=Path)
    parser.add_argument('--ziel', type=Path)
    parser.add_argument('--kind', type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.kind:
        child(args.kind)
    else:
        if args.runtime is None or args.ziel is None:
            parser.error('--runtime und --ziel sind erforderlich')
        raise SystemExit(run(args.runtime.resolve(), args.ziel))
