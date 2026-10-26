"""FP-02/1: echte Masken, Vorrücken, Formatmigration und unveränderter Altleser."""
import argparse
import copy
from contextlib import nullcontext
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tests/integration'))
from test_schutzrunde import Lauf
from vorversion import finden
from historical_runtime import historical_app


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def seed(run, rule=None, due='2026-10-19'):
    app = run.app
    item = app.new_item('Wiederkehrender Test', due=due, due_time='09:00', repeat=rule)
    source = app.new_list_object('Rhythmen', [item])
    app.lists.append(source)
    assert app.save_items()
    app.set_active_list(source['id']); run.idle()
    return source, item


def choose(run, host, variable, value):
    control = next(w for w in descendants(host) if isinstance(w, run.mod.AppOptionMenu)
                   and str(w.variable) == str(variable))
    control.menu.invoke(control.options.index(value))


def click(widget):
    widget.event_generate('<ButtonPress-1>', x=10, y=10)
    widget.event_generate('<ButtonRelease-1>', x=10, y=10)


def fall_maske(run):
    app = run.app
    source, item = seed(run)
    original_modal = app.run_modal
    errors = []; sizes = []
    def modal(dialog, **kwargs):
        dialog.geometry('860x700+20+20')
        def act():
            try:
                menus = [w for w in descendants(dialog) if isinstance(w, run.mod.AppOptionMenu)]
                choice = next(w for w in menus if 'alle N Wochen an Wochentagen' in w.options)
                choice.menu.invoke(choice.options.index('n-ter Wochentag im Monat'))
                position = next(w for w in menus if 'letzter' in w.options)
                position.menu.invoke(position.options.index('2.'))
                weekday = next(w for w in menus if w.options == list(app.REPEAT_WEEKDAY_NAMES))
                weekday.menu.invoke(weekday.options.index('Di'))
                run.idle()
                labels = [str(w.cget('text')) for w in descendants(dialog) if isinstance(w,run.mod.tk.Label)]
                assert any('Nächste fünf Folgetermine' in v and '08.12.2026' in v for v in labels), labels[-20:]
                button = next(w for w in descendants(dialog) if isinstance(w,run.mod.RoundedButton) and w.text=='Speichern')
                sizes.append([dialog.winfo_width(),dialog.winfo_height()])
                assert sizes[-1][0]<=860 and sizes[-1][1]<=700,sizes
                assert button.winfo_ismapped() and button.winfo_rooty()+button.winfo_height()<=dialog.winfo_rooty()+dialog.winfo_height()
                click(button)
            except Exception:
                errors.append(traceback.format_exc()); dialog.destroy()
        dialog.after(100,act)
        return original_modal(dialog,**kwargs)
    with patch.object(app,'run_modal',side_effect=modal):
        details = app.item_form_dialog(mode='edit',item=item)
    assert not errors,errors
    assert details['repeat']['rrule']=='FREQ=MONTHLY;INTERVAL=2;BYDAY=2TU',details['repeat']
    assert app.apply_task_edit(item,details).saved is not False
    identity = item['id']; expected = copy.deepcopy(item['repeat'])
    run.neustart()
    assert run.app.find_item_in_lists(identity)[0]['repeat']==expected
    return dict(fenster=sizes,menue_und_speicherknopf=True,neustart=True)


def fall_maske_gross(run):
    run.app.settings['ui_font_size']='gross';run.app.apply_ui_font();run.idle()
    return fall_maske(run)


def fall_inspektor(run):
    app=run.app
    rule={'art':'serie','rrule':'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TH','start':'2026-10-19'}
    source,item=seed(run,rule)
    app.open_task_inspector(item['id']);run.idle()
    app.sync_detail_pane(force=True);run.idle()
    state=app._detail_state
    assert state['item_id']==item['id'],state['item_id']
    assert '02.11.2026' in state['repeat_preview'].cget('text')
    fields=state['fields']['repeat']
    choose(run,app.detail_pane,fields['art'],'letzter Werktag im Monat (Mo–Fr)')
    run.idle()
    current=app.find_item_in_lists(item['id'])[0]
    assert current['repeat']['rrule']=='FREQ=MONTHLY;INTERVAL=2;BYDAY=MO,TU,WE,TH,FR;BYSETPOS=-1',current
    assert not app._detail_commit_error
    assert '30.10.2026' in app._detail_state['repeat_preview'].cget('text')
    return dict(vorschau=True,echter_auswahlbefehl=True)


def fall_vorruecken(run):
    app=run.app
    source,item=seed(run,{'art':'serie','rrule':'FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TH','start':'2026-10-19'})
    identity=item['id'];before=copy.deepcopy(item);depth=len(app.undo_stack)
    # Früh erledigen: genau ein Termin ab Fälligkeit, gleiche Uhrzeit.
    assert app.toggle_item_done_anywhere(identity)
    current=app.find_item_in_lists(identity)[0]
    assert current['due']=='2026-10-22' and not current['done'] and current['due_time']=='09:00',current
    assert len(app.undo_stack)==depth+1
    advanced=copy.deepcopy(current)
    app.undo_last_change();run.idle()
    assert app.find_item_in_lists(identity)[0]==before
    app.redo_last_change();run.idle()
    assert app.find_item_in_lists(identity)[0]==advanced
    depth=len(app.undo_stack)
    app.skip_repeat_occurrences([identity]);run.idle()
    current=app.find_item_in_lists(identity)[0]
    assert current['due']=='2026-11-02' and len(app.undo_stack)==depth+1,current
    app.undo_last_change();run.idle()
    assert app.find_item_in_lists(identity)[0]==advanced
    # Ein alter verpasster Rhythmus wird bis heute übersprungen.
    current=app.find_item_in_lists(identity)[0]
    with app.item_change([identity]) as change:
        current['due']='2026-01-01';current['repeat']['start']='2026-01-01';change.mark()
    app.skip_repeat_occurrences([identity],missed=True);run.idle()
    assert date.fromisoformat(app.find_item_in_lists(identity)[0]['due'])>=date.today()
    run.neustart();assert run.app.find_item_in_lists(identity)[0]['repeat']['art']=='serie'
    return dict(erledigen_ueberspringen_undo_redo_neustart=True)


CHILD = '''import importlib.machinery,importlib.util,json,sys
from pathlib import Path
from unittest.mock import patch
path=Path(sys.argv[1]);sys.path.insert(0,str(path.parent))
if path.parent.name=='Archiv':sys.path.append(str(path.parent.parent))  # archivierte Hauptdatei: Begleitmodule der Lieferung
loader=importlib.machinery.SourceFileLoader('fp02_reader',str(path))
m=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader));sys.modules[loader.name]=m;loader.exec_module(m)
m.ListApp.show_error=m.ListApp.show_warning=m.ListApp.show_info=lambda *a,**k:None
root=m.tk.Tk();disk=Path(m.SAVE_FILE);before=disk.read_bytes()
mode=sys.argv[2]
if mode=='kopierfehler':
 with patch.object(m.shutil,'copy2',side_effect=OSError('synthetisch gesperrte Vorsicherung')):
  app=m.ListApp(root);assert not app.save_items(show_error=False);assert disk.read_bytes()==before
 assert app.save_items(show_error=False)
else:app=m.ListApp(root)
if mode=='alt':
 assert app._data_read_only and app._read_only_reason=='newer_format'
 assert not app.save_items(show_error=False) and disk.read_bytes()==before
else:
 assert json.loads(disk.read_text(encoding='utf-8'))['version']==26
 backups=list(Path(m.BACKUP_DIR).glob('liste_vor_format26_*.json'))
 assert len(backups)==1 and backups[0].read_bytes()==before
 assert [v['repeat'] for v in json.loads(before)['lists'][-1]['items']]==[v['repeat'] for v in app.lists[-1]['items']]
app.cancel_pending_callbacks();app.release_data_lock();root.destroy()
print('OK',mode)
'''


def child(run,path,mode):
    import os
    env=dict(os.environ,GLIDE_DATA_DIR=run.data,GLIDE_TEST_MODE='1')
    runtime = historical_app(REPO.parents[1],path) if mode=='alt' else nullcontext(path)
    with runtime as child_app:
        result=subprocess.run([sys.executable,'-B','-c',CHILD,str(child_app),mode],env=env,capture_output=True,text=True,timeout=90)
    assert result.returncode==0,(result.stdout+result.stderr)[-1800:]


def fall_migration(run,copy_failure=False):
    source,item=seed(run,{'art':'monatlich','start':'2026-01-31'},'2026-02-28')
    run.app.previews.close();run.ende()
    disk=Path(run.mod.SAVE_FILE);value=json.loads(disk.read_text(encoding='utf-8'));value['version']=25
    disk.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')
    child(run,run.app_path,'kopierfehler' if copy_failure else 'migration')
    run.start()
    return dict(vorsicherung_bytegleich=True,alte_regel_unveraendert=True,schreibfehler_retry=copy_failure)


def fall_kopierfehler(run):
    return fall_migration(run,True)


def fall_altleser(run):
    seed(run,{'art':'serie','rrule':'FREQ=MONTHLY;INTERVAL=3'})
    disk=Path(run.mod.SAVE_FILE);before=disk.read_bytes()
    run.app.previews.close();run.ende()
    old=finden(REPO.parents[1],'3.43.1',REPO/'CHANGELOG.md')
    assert old is not None
    child(run,old,'alt')
    assert disk.read_bytes()==before
    run.start()
    assert run.app.lists[-1]['items'][0]['repeat']['art']=='serie'
    return dict(altleser_sha256=hashlib.sha256(old.read_bytes()).hexdigest(),datei_bytegleich=True,historische_begleitmodule=True)


def fall_altregeln(run):
    rules=[{'art':kind} for kind in ('taeglich','woechentlich','monatlich','jaehrlich')]
    rules += [{'art':'tage','abstand':3},{'art':'wochentage','tage':[0,3]}]
    # Der tatsächliche ausgelieferte Leser rechnet in einem eigenen Prozess.
    old=finden(REPO.parents[1],'3.43.1',REPO/'CHANGELOG.md');assert old is not None
    code='''import importlib.machinery,importlib.util,json,sys
from datetime import date
from pathlib import Path
p=Path(sys.argv[1]);sys.path.insert(0,str(p.parent))
if p.parent.name=='Archiv':sys.path.append(str(p.parent.parent))  # archivierte Hauptdatei: Begleitmodule der Lieferung
l=importlib.machinery.SourceFileLoader('oldrepeat',str(p));m=importlib.util.module_from_spec(importlib.util.spec_from_loader(l.name,l));sys.modules[l.name]=m;l.exec_module(m)
out=[]
for rule in json.loads(sys.argv[2]):
 anchor=current=date(2028,1,31);dates=[]
 for _ in range(24):
  current=m.ListApp.next_repeat_date(rule,current,anchor);dates.append(current.isoformat())
 out.append(dates)
print('ERGEBNIS '+json.dumps(out))
'''
    with historical_app(REPO.parents[1],old) as old_runtime:
        result=subprocess.run([sys.executable,'-B','-c',code,str(old_runtime),json.dumps(rules)],capture_output=True,text=True,timeout=90)
    assert result.returncode==0,result.stderr
    expected=json.loads(next(v[9:] for v in result.stdout.splitlines() if v.startswith('ERGEBNIS ')))
    for rule,dates in zip(rules,expected):
        current=anchor=date(2028,1,31);actual=[]
        for _ in range(24):
            current=run.app.next_repeat_date(rule,current,anchor);actual.append(current.isoformat())
        assert actual==dates,(rule,actual,dates)
    return dict(altregeln=6,termine=144,identisch=True)


def fall_schreibfehler(run):
    app=run.app;source,item=seed(run,{'art':'monatlich'})
    before=copy.deepcopy(item);disk=run.datei();depth=len(app.undo_stack)
    details=app.item_details_snapshot(item)
    details['repeat']={'art':'serie','rrule':'FREQ=MONTHLY;INTERVAL=3','start':item['due']}
    with patch.object(app,'write_json_atomic',side_effect=OSError('synthetischer Schreibfehler')):
        assert app.apply_task_edit(item,details).saved is False
    assert item==before and run.datei()==disk and len(app.undo_stack)==depth
    assert app.apply_task_edit(item,details).saved is not False
    value=json.loads(run.datei())
    value['version']=25
    try:app.normalize_lists_data(value)
    except ValueError as error:assert 'Datenformat 26' in str(error)
    else:raise AssertionError('Neue Serie unter altem Formattor akzeptiert')
    try:app.normalize_lists_data([{'text':'Unversioniert','repeat':details['repeat']}])
    except ValueError as error:assert 'Datenformat 26' in str(error)
    else:raise AssertionError('Neue Serie in unversionierter Altliste akzeptiert')
    return dict(modell_datei_undo_bei_schreibfehler_erhalten=True,erneuter_versuch=True,formattor=True)


def fall_austausch(run):
    app=run.app
    source,item=seed(run,{'art':'serie','rrule':'FREQ=MONTHLY;INTERVAL=3','start':'2026-10-19'})
    expected=copy.deepcopy(item['repeat']);identity=item['id']
    lines=app.ics_event_lines(item,source)
    assert 'RRULE:FREQ=MONTHLY;INTERVAL=3' in lines
    restored=app.ics_repeat_from_rule(app.ics_repeat_rule(item),start=item['due'])
    assert restored['rrule']==expected['rrule']
    assert app.parse_repeat_text(app.describe_repeat(expected))['rrule']==expected['rrule']
    path=Path(run.data).parent/'serie.glideapp'
    app.write_complete_backup(str(path),app.app_backup_payload())
    details=app.item_details_snapshot(item);details['repeat']=None
    assert app.apply_task_edit(item,details).saved is not False
    assert app.restore_app_backup(str(path),sections={'tasks':True,'settings':True,'templates':True,'activity':True},show_success=False)
    run.neustart()
    assert run.app.find_item_in_lists(identity)[0]['repeat']==expected
    return dict(txt_regel_erhalten=True,kalender_rundweg=True,vollbackup_neustart=True)


def fall_steuerung(run):
    app=run.app
    source,item=seed(run,{'art':'tage','abstand':3},(date.today()+timedelta(days=10)).isoformat())
    identity=item['id'];app.open_task_inspector(identity);run.idle()
    options=lambda:app._detail_state['fields']['repeat']['options']
    choose(run,app.detail_pane,options()['basis'],'Ab Erledigung');run.idle()
    entry=options()['entry'];entry.delete(0,'end');entry.insert(0,'3');entry.event_generate('<FocusOut>');run.idle()
    pause=next(w for w in descendants(app.detail_pane) if isinstance(w,run.mod.tk.Checkbutton)
               and str(w.cget('variable'))==str(options()['paused']))
    pause.invoke();run.idle()
    current=app.find_item_in_lists(identity)[0]
    assert current['repeat']['bezug']=='erledigt' and current['repeat']['rest']==3 and current['repeat']['pausiert'],current
    assert 'pausiert' in app._detail_state['repeat_preview'].cget('text')
    saved=copy.deepcopy(current['repeat']);run.neustart();app=run.app
    current=app.find_item_in_lists(identity)[0];assert current['repeat']==saved
    app.toggle_item_done_anywhere(identity);run.idle()
    assert app.find_item_in_lists(identity)[0]['done'] and app.find_item_in_lists(identity)[0]['repeat']['rest']==3
    app.undo_last_change();run.idle()
    current=app.find_item_in_lists(identity)[0]
    details=app.item_details_snapshot(current);details['repeat'].pop('pausiert')
    assert app.apply_task_edit(current,details).saved is not False
    app.toggle_item_done_anywhere(identity);run.idle()
    current=app.find_item_in_lists(identity)[0]
    assert current['due']==(date.today()+timedelta(days=3)).isoformat() and current['repeat']['rest']==2,current
    app.undo_last_change();run.idle();assert app.find_item_in_lists(identity)[0]['repeat']['rest']==3
    app.redo_last_change();run.idle();assert app.find_item_in_lists(identity)[0]['repeat']['rest']==2
    app.toggle_item_done_anywhere(identity);app.toggle_item_done_anywhere(identity);run.idle()
    current=app.find_item_in_lists(identity)[0]
    assert current['done'] and current['repeat'] is None,current
    return dict(inspektor_alle_drei_steuerungen=True,pause_ohne_verbrauch=True,erledigungsbezug=True,
                endliche_serie_stoppt=True,undo_redo_neustart=True)


def fall_schnelleingabe(run):
    app=run.app;source,item=seed(run)
    for text,expected in (
        ('Team alle 2 Wochen montags und donnerstags','FREQ=WEEKLY;INTERVAL=2;BYDAY=MO,TH'),
        ('Termin jeden zweiten Dienstag im Monat','FREQ=MONTHLY;INTERVAL=1;BYDAY=2TU'),
        ('Filter drei Tage nach Erledigung insgesamt 3 Termine',None)):
        app.clear_entry_placeholder();app.entry.delete(0,'end');app.entry.insert(0,text)
        app.update_slash_hint();run.idle()
        chips=[w for w in descendants(app._capture_hint) if isinstance(w,run.mod.tk.Label)]
        assert any('Wiederholung' in str(w.cget('text')) for w in chips)
        app.add_item();run.idle();value=app.items[-1]
        assert value['text'] in ('Team','Termin','Filter'),value
        if expected:assert value['repeat']['rrule']==expected,value
        else:assert value['repeat']['bezug']=='erledigt' and value['repeat']['rest']==3,value
        identity=value['id'];app.undo_last_change();run.idle();assert not app.find_item_in_lists(identity)
        app.redo_last_change();run.idle();assert app.find_item_in_lists(identity)
    # Den erkannten Chip über sein wirkliches Rücknahmeelement deaktivieren.
    text='Wartung alle 3 Monate am 15.'
    app.clear_entry_placeholder();app.entry.delete(0,'end');app.entry.insert(0,text);app.update_slash_hint();run.idle()
    reverse=next(w for w in descendants(app._capture_hint) if isinstance(w,run.mod.tk.Label) and w.cget('text')==app.ICONS['remove'])
    reverse.event_generate('<Button-1>');run.idle();app.add_item();run.idle()
    assert app.items[-1]['text']==text and not app.items[-1]['repeat'],app.items[-1]
    return dict(echte_chips=3,undo_redo=True,chipruecknahme=True)


CASES=('maske','maske_gross','inspektor','vorruecken','migration','kopierfehler','altleser','altregeln','schreibfehler','austausch','steuerung','schnelleingabe')


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report',type=Path);parser.add_argument('--fall',choices=CASES)
    args=parser.parse_args();report=dict(app_sha256=hashlib.sha256(args.app.read_bytes()).hexdigest(),faelle={})
    for name in ([args.fall] if args.fall else CASES):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-serien-') as directory:
            try:
                run=Lauf(args.app,str(Path(directory)/'daten'))
                evidence=globals()['fall_'+name](run)
                assert not run.errors,run.errors
                report['faelle'][name]=dict(ok=True,messung=evidence);print('OK',name,flush=True)
            except Exception:
                error=traceback.format_exc().replace(str(Path.home()),'~').replace(str(Path.home()).replace('\\','\\\\'),'~')[-2500:]
                report['faelle'][name]=dict(ok=False,fehler=error);print('ROT',name,error,flush=True)
            finally:
                if run is not None:run.app.previews.close();run.ende()
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(any(not v['ok'] for v in report['faelle'].values()))


if __name__=='__main__':raise SystemExit(main())
