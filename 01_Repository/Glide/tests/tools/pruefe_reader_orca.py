"""Tatsächliche Orca-Sprache und Tastatur im eigenen vergänglichen Linux-CI.

Nur SPEECH OUTPUT aus dem Orca-Prozess zählt; Tk/spd-say-Ausgabe zählt nicht.
Keine Inhaberprofile, keine systemweiten Änderungen außerhalb des Hosted-CI.
"""
import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import traceback


def require_hosted(destination):
    if (sys.platform != 'linux' or os.environ.get('GITHUB_ACTIONS') != 'true' or
            os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'):
        raise RuntimeError('Orca-Probe ausschließlich im vergänglichen Linux-Hosted-CI.')
    temporary = Path(os.environ['RUNNER_TEMP']).resolve()
    destination = destination.resolve()
    if destination == temporary or not destination.is_relative_to(temporary):
        raise ValueError('Eigener Orca-Prüfordner muss unter RUNNER_TEMP liegen.')
    return destination


def wait_value(path, predicate, timeout=20):
    deadline = time.monotonic()+timeout
    while time.monotonic() < deadline:
        if path.is_file():
            value = json.loads(path.read_text(encoding='utf-8'))
            if predicate(value):
                return value
        time.sleep(.1)
    raise AssertionError('Reader-Probe wartet vergeblich auf '+path.name)


def profile():
    return dict(general=dict(firstStart=False, enableSpeech=True, enableBraille=False,
        keyboardLayout=1, speechServerFactory='speechdispatcherfactory',
        startingProfile=['Default','default'], activeProfile=['Default','default']),
        profiles={'default':dict(profile=['Default','default'],pronunciations={},keybindings={})},
        pronunciations={}, keybindings={})


def speech_fragments(data):
    # Die Fixturetexte enthalten keine Apostrophe. Die Stimme/ACSS-Metadaten
    # hinter dem gesprochenen Text werden nicht als Readerinhalt gewertet.
    return re.findall(r"SPEECH OUTPUT: '([^']*)'", data)


class Actor:
    def __init__(self, pid, log, environment):
        self.pid, self.log, self.environment = pid, log, environment
        self.spoken = []

    def assert_focus(self):
        value = subprocess.check_output(['xdotool','getwindowfocus','getwindowpid'],
                                        env=self.environment,text=True).strip()
        if int(value) != self.pid:
            raise RuntimeError('Kein Tastendruck: eigene Glide-Testinstanz hat nicht den Vordergrund.')

    def key(self, gesture):
        self.assert_focus()
        names={'control':'ctrl','enter':'Return','escape':'Escape','tab':'Tab','home':'Home',
               'end':'End','up':'Up','down':'Down','insert':'Insert','f2':'F2'}
        keys='+'.join(names.get(part,part) for part in gesture.split('+'))
        subprocess.run(['xdotool','key','--clearmodifiers',keys],env=self.environment,check=True)
        time.sleep(.15)

    def type(self, text):
        self.assert_focus()
        assert text.isascii() and all(char.isalpha() or char==' ' for char in text)
        subprocess.run(['xdotool','type','--clearmodifiers','--delay','5',text],
                       env=self.environment,check=True)
        time.sleep(.15)

    def where(self):
        offset=len(self.log.read_text(encoding='utf-8',errors='replace'))
        self.key('KP_Enter')
        deadline=time.monotonic()+4
        values=[]
        changed=time.monotonic()
        previous=''
        while time.monotonic()<deadline:
            data=self.log.read_text(encoding='utf-8',errors='replace')[offset:]
            values=speech_fragments(data)
            if data!=previous:
                changed=time.monotonic();previous=data
            if values and time.monotonic()-changed>=.5:
                break
            time.sleep(.1)
        value=' '.join(values)
        self.spoken.append(value)
        if not value:
            raise AssertionError('Orca erzeugt beim eigenen Fokus keine Sprachausgabe.')
        return value

    def focus(self, expected):
        value=self.where()
        assert expected in value,(expected,value)
        return value

    def find(self, expected, *, role=None):
        for _ in range(90):
            self.key('tab')
            value=self.where()
            if expected in value and (role is None or role in value.casefold()):
                return value
        raise AssertionError('Mit Tab/Orca nicht erreichbar: '+expected)


def run(destination, app):
    destination=require_hosted(destination)
    destination.mkdir(parents=True,exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Orca-Probe benötigt einen neuen leeren Ordner.')
    for command in ('orca','xdotool','pulseaudio','pactl'):
        if shutil.which(command) is None:
            raise RuntimeError('Native Reader-Bauvoraussetzung fehlt: '+command)
    if subprocess.run(['pgrep','-x','orca'],capture_output=True).returncode==0:
        raise RuntimeError('Vorhandene fremde Orca-Instanz im Prüfstand; keine Übernahme.')
    env=dict(os.environ,LANG='C.UTF-8',LC_ALL='C.UTF-8',PYTHONDONTWRITEBYTECODE='1')
    for key,folder in (('XDG_CONFIG_HOME','config'),('XDG_CACHE_HOME','cache'),
                       ('XDG_DATA_HOME','data'),('XDG_RUNTIME_DIR','runtime')):
        path=destination/folder;path.mkdir(mode=0o700);env[key]=str(path)
    reader_env=dict(env);reader_env.pop('PYTHONPATH',None)
    preferences=destination/'profil';preferences.mkdir()
    (preferences/'user-settings.conf').write_text(json.dumps(profile()),encoding='utf-8')
    debug=destination/'orca-debug.log'
    source=Path('/usr/lib/python3/dist-packages/orca/speech.py')
    if not source.is_file() or 'SPEECH OUTPUT:' not in source.read_text(encoding='utf-8'):
        raise RuntimeError('Installierter Orca-Sprechpfad nicht für diese Debugprobe geprüft.')
    result=dict(exitcode=1,reader=subprocess.check_output(['orca','--version'],env=reader_env,text=True).strip(),
        orca_speech_source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
        nur_kuenstliche_daten=True,tk_spd_say_zaehlt_nicht=True,menschliche_abnahme='getrennt offen')
    reader=child=None
    with (destination/'prozesse.log').open('w',encoding='utf-8') as log:
        try:
            subprocess.run(['pulseaudio','--start','--exit-idle-time=-1'],env=reader_env,
                           stdout=log,stderr=log,timeout=20,check=True)
            subprocess.run(['pactl','load-module','module-null-sink','sink_name=glideqa'],env=reader_env,
                           stdout=log,stderr=log,timeout=10,check=True)
            subprocess.run(['pactl','set-default-sink','glideqa'],env=reader_env,
                           stdout=log,stderr=log,timeout=10,check=True)
            reader=subprocess.Popen(['orca','--user-prefs',str(preferences),'--debug-file',str(debug)],
                                    env=reader_env,stdout=log,stderr=log)
            deadline=time.monotonic()+30
            while time.monotonic()<deadline:
                if reader.poll() is not None:raise RuntimeError('Orca vorzeitig beendet.')
                if debug.is_file() and 'SPEECH: Using speech server factory:' in debug.read_text(errors='replace'):break
                time.sleep(.2)
            else:raise RuntimeError('Orca-Speechserver nicht tatsächlich initialisiert.')
            exchange=destination/'glide-diagnose'
            child=subprocess.Popen([sys.executable,'-B',str(Path(__file__).with_name('reader_app400.py')),
                '--app',str(app),'--diagnose',str(exchange)],env=env,stdout=log,stderr=log)
            ready=wait_value(exchange/'bereit.json',lambda value:value.get('tk')=='9.1.0')
            assert ready['pid']==child.pid
            actor=Actor(child.pid,debug,env);result['speech']=actor.spoken
            state=lambda condition:wait_value(exchange/'zustand.json',condition)
            actor.key('control+n');actor.focus('Neue Aufgabe')
            actor.type('Angebot pruefen');actor.key('enter')
            state(lambda value:len(value['tasks'])==1)
            actor.key('control+f');actor.focus('Aufgaben suchen')
            actor.type('Angebot');actor.key('escape')
            actor.find('Aufgaben',role='tree');actor.key('home');actor.focus('Angebot pruefen')
            actor.key('control+shift+p');actor.key('home');actor.focus('Heute');actor.key('enter')
            state(lambda value:value['tasks'][0].get('planned_date')==date.today().isoformat())
            actor.find('Arbeitsbereiche',role='tree');actor.key('home');actor.key('down');actor.focus('Heute')
            state(lambda value:value['view']==ready['plan_day_view'])
            actor.find('Aufgaben',role='tree');actor.key('home');actor.focus('Angebot pruefen')
            actor.key('f2');actor.focus('Aufgabentitel')
            actor.key('control+a');actor.type('Angebot bearbeitet');actor.key('control+s')
            state(lambda value:value['tasks'][0].get('text')=='Angebot bearbeitet')
            actor.find('Bearbeitungstag');actor.find('Neuer Checklistenpunkt')
            actor.type('Unterlagen pruefen');actor.key('enter')
            state(lambda value:len(value['tasks'][0].get('checklist',[]))==1)
            before=actor.find('Unterlagen pruefen');assert 'check box' in before.casefold(),before
            actor.key('space');state(lambda value:value['tasks'][0]['checklist'][0]['done'])
            checked=actor.focus('Unterlagen pruefen')
            assert 'checked' in checked.casefold() and 'not checked' not in checked.casefold(),checked
            actor.key('space');state(lambda value:not value['tasks'][0]['checklist'][0]['done'])
            actor.key('control+z');final=state(lambda value:value['tasks'][0]['checklist'][0]['done'])
            assert not final['callback_errors'] and not final['tasks'][0].get('due'),final['callback_errors']
            result.update(exitcode=0,version=ready['version'],tk=ready['tk'],checks=[
                'Orca-generierte Sprache bei echter Erfassung/Suche/Heute-Planung/Inspektor',
                'Ausgewählte Aufgabe und Heute-Menü gesprochen; Heute-Ansicht erreicht; benannte Felder, Checkbox/Checked, Titel, ein Undo, keine Callbackfehler'])
        except Exception as error:
            result.update(fehler=str(error),traceback=traceback.format_exc())
        finally:
            if child is not None:
                path=destination/'glide-diagnose/zustand.json'
                if path.is_file():result['app_callback_errors']=json.loads(path.read_text())['callback_errors']
            for process in (child,reader):
                if process is not None and process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=10)
                    except subprocess.TimeoutExpired:process.kill();process.wait(timeout=10)
            subprocess.run(['pulseaudio','--kill'],env=reader_env,stdout=log,stderr=log,timeout=10)
    (destination/'reader-ergebnis.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return result['exitcode']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ziel',type=Path,required=True)
    parser.add_argument('--app',type=Path,default=Path(__file__).resolve().parents[2]/'src/glide/app.pyw')
    args=parser.parse_args();raise SystemExit(run(args.ziel,args.app.resolve()))
