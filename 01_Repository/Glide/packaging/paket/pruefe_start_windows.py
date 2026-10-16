"""Echte native Startprobe: ACL-Sperre ausschließlich auf einem Hosted-CI-Runner.

Vor jeder Sperre werden die ACLs gesichert, im finally-Zweig exakt restauriert
und das externe Python erneut gestartet. Inhaberinstallationen sind durch den
Tk-freien Grenzvertrag ausdrücklich ausgeschlossen.
"""
import argparse
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from windows_isolation import access_denied, acl_rules, acl_snapshot, normalize_environment, plan, isolation_probe


def run(package,report,forbidden,*,timeout=150):
    if sys.platform!='win32':raise RuntimeError('Native Windows-Probe erforderlich.')
    # Reale Pfade vor der reinen Prüfung auflösen; keine Junction darf eine
    # Quelle außerhalb des zulässigen vergänglichen Prüfbereichs verstecken.
    environment=normalize_environment(os.environ)
    for key in ('RUNNER_TEMP','RUNNER_TOOL_CACHE','GITHUB_WORKSPACE','SYSTEMROOT'):
        if key in environment:environment[key]=str(Path(environment[key]).resolve())
    boundary=plan(environment,str(Path(package).resolve()),str(Path(report).resolve()),
                  [str(Path(path).resolve())for path in forbidden])
    package,report=Path(boundary['package']),Path(boundary['report'])
    sources=[Path(path)for path in boundary['forbidden']]
    executable=package/'Glide.exe'
    if not executable.is_file()or report.exists():raise ValueError('Paket und unbenutzter Berichtspfad erforderlich.')
    if not any(Path(sys.executable).resolve().is_relative_to(path)for path in sources):
        raise ValueError('Die tatsächliche externe Prüflaufzeit muss gesperrt werden.')
    report.parent.mkdir(parents=True,exist_ok=True)
    smoke=report.with_name(report.stem+'-paket.json')
    if smoke.exists():raise ValueError('Neuer Paketbericht erforderlich.')
    system=Path(environment['SYSTEMROOT'])/'System32'
    def command(args,**kwargs):
        # Projekt und externes Python werden gesperrt. Systembefehle und
        # Gegenproben müssen weiterhin aus einem ungesperrten Ordner starten.
        kwargs.setdefault('cwd', str(package.parent))
        return subprocess.run([str(value)for value in args],capture_output=True,text=True,
                              encoding='utf-8',errors='replace',timeout=timeout,**kwargs)
    who=command([system/'whoami.exe','/user','/fo','csv','/nh'])
    if who.returncode:raise RuntimeError('CI-Benutzerkennung nicht ermittelbar.')
    sid=next(csv.reader(io.StringIO(who.stdout)))[1]
    if not sid.startswith('S-1-'):raise ValueError('Ungültige Windows-SID.')
    assert command([system/'cmd.exe','/d','/c','exit','0']).returncode==0
    assert command([sys.executable,'-B','-c','raise SystemExit(0)']).returncode==0
    result={'plattform':'Windows x64','nur_vergaenglicher_hosted_ci_runner':True,
            'inhaber_installationen_unveraendert':True,'exitcode':1}
    saved=[];restored=[];unlocked=[];verified=[];rules_verified=[];restore_details=[];failure=None
    probes=[]
    for path in sources:
        probe=isolation_probe(path)
        if probe is None:raise ValueError('Externe Quelle braucht eine tatsächlich lesbare Prüfdatei.')
        with probe.open('rb') as stream:stream.read(1)
        probes.append(probe)
    # ctypes und alle API-Definitionen vor der externen Python-Sperre laden.
    from windows_acl import OriginalAclRestorer
    exact_restorer=OriginalAclRestorer(environment,package,report,sources)
    exact_codes=[]
    with tempfile.TemporaryDirectory(prefix='glide-acl-',dir=environment['RUNNER_TEMP'])as backup:
        try:
            for number,path in enumerate(sources):
                if not path.is_dir():raise ValueError('Externe CI-Quelle fehlt.')
                acl=Path(backup)/f'acl-{number}.txt'
                # /L: Ohne den Schalter sichert icacls für einen Symlink die
                # DACL des Ziels und /restore schreibt durch den Link hindurch.
                save=command([system/'icacls.exe',path,'/save',acl,'/T','/L','/Q'])
                if save.returncode:raise RuntimeError('Original-ACL konnte nicht vollständig gesichert werden.')
                original=acl_snapshot(acl.read_bytes())
                saved.append((path,acl,original))
                # OI/CI vererbt die Sperre. /T würde nach dem Sperren des
                # Elternordners erneut hineingehen und an sich selbst scheitern.
                # Nur Dateiinhalt/Verzeichnisliste und Ausführung sperren.
                # READ_CONTROL/WRITE_DAC bleiben für die Restaurierung verfügbar.
                deny=command([system/'icacls.exe',path,'/deny','*'+sid+':(OI)(CI)(RD,X)','/Q'])
                if deny.returncode:
                    result['acl_sperrfehler']=deny.stdout+deny.stderr
                    raise RuntimeError('Externe Laufzeit nicht vollständig gesperrt.')
            denied=[]
            for probe in probes:
                try:
                    with probe.open('rb') as stream:stream.read(1)
                except OSError as exc:
                    if not access_denied(exc):raise
                    denied.append(True)
                else:
                    raise RuntimeError('Gegenprobe fehlgeschlagen: externe Quelldatei noch lesbar.')
            result['externe_quellen_lesegegenproben']=denied
            try:
                blocked=command([sys.executable,'-B','-c','raise SystemExit(0)'])
                code=blocked.returncode
            except OSError as exc:
                if not access_denied(exc):raise
                code='OS-Zugriff verweigert: '+str(getattr(exc,'winerror',None) or exc.errno)
            if code==0:raise RuntimeError('Gegenprobe fehlgeschlagen: externes Python noch ausführbar.')
            child_env=dict(environment,PATH=str(system),PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1')
            for key in ('PYTHONHOME','PYTHONPATH','TCL_LIBRARY','TK_LIBRARY'):child_env.pop(key,None)
            # Arbeitsverzeichnis neben dem Paket: die Projektquelle ist gesperrt.
            child=command([executable,'--paket-pruefen',smoke],env=child_env,cwd=str(package.parent))
            result.update(externes_python_gegenprobe=code,paketprozess_exitcode=child.returncode,
                          ausgabe=child.stdout+child.stderr)
            if smoke.exists():result['paket']=json.loads(smoke.read_text(encoding='utf-8'))
            if child.returncode==0 and result.get('paket',{}).get('exitcode')==0:result['exitcode']=0
        except BaseException as exc:
            # traceback kann Module nachladen. Während der Sperre nur die
            # Ausnahme merken; erst nach der Restaurierung formatieren.
            failure=exc
            result.update(fehler=str(exc),exitcode=1)
        finally:
            def cleanup(args):
                try:
                    child=command(args)
                    return child.returncode,child.stdout+child.stderr
                except BaseException as exc:
                    return 1,str(exc)
            for path,acl,original in reversed(saved):
                # Jeden Restaurierungsschritt auch dann versuchen, wenn der
                # vorherige Systembefehl selbst abgebrochen ist.
                unlock,unlock_output=cleanup([system/'icacls.exe',path,'/remove:d','*'+sid,'/Q'])
                unlocked.append(unlock)
                restore,restore_output=cleanup([system/'icacls.exe',path.parent,'/restore',acl,'/L','/Q'])
                restored.append(restore)
                try:
                    exact=exact_restorer.restore(path,original)
                except BaseException as exc:
                    exact={'exitcode':1,'fehler':str(exc)}
                exact_codes.append(exact['exitcode'])
                after=acl.with_name(acl.stem+'-nachher.txt')
                check,check_output=cleanup([system/'icacls.exe',path,'/save',after,'/T','/L','/Q'])
                difference={}
                try:
                    actual=acl_snapshot(after.read_bytes()) if check==0 else {}
                    verified.append(check==0 and actual==original)
                    rules_verified.append(check==0 and acl_rules(actual)==acl_rules(original))
                    if actual!=original:
                        changed=[name for name in original.keys() & actual.keys() if original[name]!=actual[name]]
                        difference={'vorher':len(original),'nachher':len(actual),
                                    'fehlend':len(original.keys()-actual.keys()),
                                    'neu':len(actual.keys()-original.keys()),'geaendert':len(changed),
                                    'fehlende_beispiele':sorted(original.keys()-actual.keys())[:3],
                                    'neue_beispiele':sorted(actual.keys()-original.keys())[:3],
                                    'beispiele':[{'datei':name,'vorher':original[name],'nachher':actual[name]}
                                                 for name in sorted(changed)[:3]]}
                except BaseException as exc:
                    verified.append(False)
                    rules_verified.append(False)
                    check_output+='\n'+str(exc)
                restore_details.append({'entsperren':unlock_output,'restaurieren':restore_output,
                                        'native_originalrestaurierung':exact,
                                        'nachpruefen':check_output,'acl_vergleich':difference})
            result['acl_entsperrung_exitcodes']=unlocked
            result['acl_restaurierung_exitcodes']=restored
            result['acl_native_restaurierung_exitcodes']=exact_codes
            result['acl_originale_wiederhergestellt']=verified
            result['acl_zugriffsregeln_wiederhergestellt']=rules_verified
            result['acl_modellmarker_ai_abweichend_zulaessig']=True
            result['acl_restaurierung_details']=restore_details
            if (len(restored)!=len(saved) or any(restored) or
                    len(unlocked)!=len(saved) or any(unlocked) or any(exact_codes) or not all(rules_verified)):
                result['exitcode']=1
    if failure is not None:
        try:
            result['traceback']=''.join(traceback.format_exception(failure))
        except Exception as error:
            result['traceback']='Fehlerformatierung nach Restaurierung fehlgeschlagen: '+type(error).__name__
    try:
        code=command([sys.executable,'-B','-c','raise SystemExit(0)']).returncode
    except OSError:
        code=1
    result['externes_python_nach_restaurierung_exitcode']=code
    if code:result['exitcode']=1
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Native isolierte Windows-Paketprobe Exit',result['exitcode'])
    return result['exitcode']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paket',type=Path,required=True)
    parser.add_argument('--bericht',type=Path,required=True)
    parser.add_argument('--sperren',type=Path,action='append',required=True)
    args=parser.parse_args();raise SystemExit(run(args.paket,args.bericht,args.sperren))
