"""Gehaltene native AT-SPI-Referenzen über künstliche Widgetwechsel prüfen."""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import traceback


def run(pid, exchange):
    temporary=Path(os.environ['RUNNER_TEMP']).resolve();exchange=exchange.resolve()
    if (sys.platform!='linux' or os.environ.get('GITHUB_ACTIONS')!='true' or
            os.environ.get('RUNNER_ENVIRONMENT')!='github-hosted' or exchange==temporary or
            not exchange.is_relative_to(temporary)):
        raise RuntimeError('Lebensdauerprobe nur in eigener Hosted-CI-Fixture.')
    import gi
    gi.require_version('Atspi','2.0')
    from gi.repository import Atspi,GLib
    result=dict(exitcode=1,nur_eigene_fixture=True,reader_abnahme='getrennt offen')
    try:
        desktop=Atspi.get_desktop(0)
        application=next((desktop.get_child_at_index(i) for i in range(desktop.get_child_count())
                          if desktop.get_child_at_index(i).get_process_id()==pid),None)
        assert application is not None
        def find(name):
            queue=[application];seen=set()
            while queue:
                node=queue.pop(0)
                if node is None or node in seen:continue
                seen.add(node);assert len(seen)<256 and node.get_process_id()==pid
                if node.get_name()==name:return node
                queue.extend(node.get_child_at_index(i) for i in range(node.get_child_count()))
            raise AssertionError('Eigenes Feld fehlt: '+name)
        def phase(value):
            (exchange/'phase.txt').write_text(str(value))
            deadline=time.monotonic()+12
            while time.monotonic()<deadline:
                path=exchange/'phase.json'
                if path.exists():
                    state=json.loads(path.read_text())
                    if state==dict(pid=pid,phase=value):return
                time.sleep(.1)
            raise TimeoutError('Eigene native Fixturephase fehlt: '+str(value))
        original=find('AT-SPI-Prüffeld')
        text=Atspi.Text.get_text(original.get_text_iface(),0,-1)
        phase(1)
        assert original.get_name()=='AT-SPI-Prüffeld' and Atspi.Text.get_text(original.get_text_iface(),0,-1)==text
        phase(2)
        replacement=find('Ersatz-Prüffeld')
        assert replacement!=original and Atspi.Text.get_text(replacement.get_text_iface(),0,-1)=='Neuer Inhalt'
        try:
            closed=original.get_state_set().contains(Atspi.StateType.DEFUNCT)
        except GLib.Error:
            closed=True
        assert closed,'Gehaltenes entferntes Objekt muss DEFUNCT oder nicht mehr erreichbar sein.'
        (exchange/'phase.txt').write_text('3')
        result.update(exitcode=0,checks=[
            'Gehaltenes eigenes AT-SPI-Feld nach dynamischen Nachbarn unverändert',
            'Registrierte Nachbarn ohne Absturz zerstört',
            'Entferntes Feld geschlossen; neuer Inhalt am selben Widgetpfad getrennt erreichbar'])
    except Exception as error:
        result.update(fehler=str(error),traceback=traceback.format_exc())
    (exchange/'atspi-lifetime.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Native AT-SPI-Lebensdauerprobe Exit',result['exitcode'])
    return result['exitcode']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--pid',type=int,required=True);parser.add_argument('--austausch',type=Path,required=True)
    args=parser.parse_args();raise SystemExit(run(args.pid,args.austausch))
