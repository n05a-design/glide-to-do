"""Gepinntes NVDA-Testwerkzeug ausschließlich im vergänglichen Hosted-Runner.

Die unveränderten offiziellen Spy-Dateien erfassen NVDA-generierte Sprache.
Glide-Pakete enthalten weder NVDA noch Spy/Robot. Kein Zugriff auf Inhaber-
Installationen, Profile oder echte Glide-Daten. Menschliche Abnahme separat.
"""
import argparse
import ctypes
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import urllib.request
import xmlrpc.client


SPEECH_SPY_MODULE = 'speechSpySynthDriver'


def profile_configuration():
    return '''schemaVersion = 24
[general]
language = en
saveConfigurationOnExit = False
askToExit = False
showWelcomeDialogAtStartup = False
playStartAndExitSounds = False
[update]
askedAllowUsageStats = True
autoCheck = False
startupNotification = False
allowUsageStats = False
[speech]
synth = '''+SPEECH_SPY_MODULE+'''
[development]
enableScratchpadDir = True
'''


def require_hosted(destination):
    if (sys.platform != 'win32' or os.environ.get('GITHUB_ACTIONS') != 'true'
            or os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'):
        raise RuntimeError('Reader-Testwerkzeug nur auf vergänglichem Windows-Hosted-CI-Runner.')
    temporary = Path(os.environ['RUNNER_TEMP']).resolve()
    destination = Path(destination).resolve()
    if destination == temporary or not destination.is_relative_to(temporary):
        raise ValueError('Eigener Reader-Ordner muss unter RUNNER_TEMP liegen.')
    return destination


def download(record, destination):
    with urllib.request.urlopen(record['source'], timeout=120) as response:
        data = response.read()
    if hashlib.sha256(data).hexdigest() != record['sha256']:
        raise ValueError('Reader-Testquelle weicht vom Originalpin ab: ' + record['file'])
    destination.write_bytes(data)


def prepare(destination):
    destination = require_hosted(destination)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Reader-Test braucht einen neuen leeren Ordner.')
    lock = json.loads(Path(__file__).with_name('reader_nvda_lock.json').read_text(encoding='utf-8'))
    originals = destination / 'originale'
    originals.mkdir()
    for record in [lock['installer'], *lock['files']]:
        download(record, originals / record['file'])
    portable = destination / 'portable'
    with (destination / 'portable-erzeugung.log').open('w', encoding='utf-8') as log:
        result = subprocess.run([str(originals / lock['installer']['file']), '--create-portable-silent',
                                 '--portable-path', str(portable), '--minimal'],
                                stdout=log, stderr=subprocess.STDOUT, timeout=240)
    if result.returncode or not (portable / 'nvda.exe').is_file():
        raise RuntimeError('Portable NVDA-Testkopie nicht erfolgreich erzeugt.')
    profile = destination / 'profil'
    plugin = profile / 'scratchpad/globalPlugins/speechSpyGlobalPlugin'
    libraries = plugin / 'libs'
    synths = profile / 'scratchpad/synthDrivers'
    libraries.mkdir(parents=True)
    synths.mkdir(parents=True)
    shutil.copy2(originals / 'speechSpyGlobalPlugin.py', plugin / '__init__.py')
    shutil.copy2(originals / 'blockUntilConditionMet.py', plugin / 'blockUntilConditionMet.py')
    shutil.copy2(originals / 'robotremoteserver.py', libraries / 'robotremoteserver.py')
    for name in ('RobotRemoteServer-LICENSE.txt', 'RobotRemoteServer-COPYRIGHT.txt'):
        shutil.copy2(originals / name, libraries / name)
    shutil.copy2(originals / 'copying.txt', profile / 'NVDA-COPYING.txt')
    shutil.copy2(originals / 'speechSpySynthDriver.py', synths / 'speechSpySynthDriver.py')
    (profile / 'nvda.ini').write_text(profile_configuration(), encoding='utf-8')
    (destination / 'herkunft.json').write_text(json.dumps(lock, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return portable / 'nvda.exe', profile


class Spy:
    def __init__(self, destination):
        self.destination = require_hosted(destination)
        self.remote = xmlrpc.client.ServerProxy('http://127.0.0.1:8270', allow_none=True)

    def call(self, name, *arguments):
        result = self.remote.run_keyword(name, list(arguments), {})
        if result.get('status') != 'PASS':
            raise RuntimeError('NVDA-Testwerkzeug: ' + result.get('error', 'Unbekannter Remote-Fehler'))
        return result.get('return')

    def wait_ready(self):
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            try:
                self.remote.get_keyword_names()
                self.call('wait_for_NVDA_startup_to_complete')
                return
            except (OSError, xmlrpc.client.Error):
                time.sleep(.2)
        raise RuntimeError('Offizielles NVDA-Sprachtestwerkzeug nicht erreichbar.')

    @staticmethod
    def foreground_pid():
        user32 = ctypes.WinDLL('user32', use_last_error=True)
        user32.GetForegroundWindow.argtypes = []
        user32.GetForegroundWindow.restype = ctypes.c_void_p
        user32.GetWindowThreadProcessId.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_ulong)]
        user32.GetWindowThreadProcessId.restype = ctypes.c_ulong
        pid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), ctypes.byref(pid))
        return pid.value

    def key(self, pid, gesture):
        if self.foreground_pid() != pid:
            raise RuntimeError('Kein Tastendruck: Die eigene Glide-Testinstanz hat nicht den Vordergrund.')
        aliases = {'up':'upArrow', 'down':'downArrow', 'left':'leftArrow', 'right':'rightArrow'}
        gesture = '+'.join(aliases.get(part, part) for part in gesture.split('+'))
        return self.call('emulateKeyPress', gesture)

    def next_speech(self):
        return int(self.call('get_next_speech_index'))

    def speech(self, start):
        self.call('wait_for_speech_to_finish', 10, start, None)
        result = self.call('get_speech_at_index_until_now', start)
        if not isinstance(result, str) or not result.strip():
            raise AssertionError('NVDA-Testprofil hat keine tatsächliche Sprachausgabe erfasst; Synthesizer und Readerprotokoll prüfen.')
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ziel', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.ziel)
    print('Originaltreue portable NVDA-Testkopie und isoliertes Profil vorbereitet; Readerprobe noch offen.')


if __name__ == '__main__':
    main()
