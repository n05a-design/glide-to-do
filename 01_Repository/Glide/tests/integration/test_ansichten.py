"""FP-03/1: echte Filtereinstiege, Dialog, Persistenz, Altleser und Gegenprobe."""
import argparse
import copy
from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tests/integration'))
from test_schutzrunde import Lauf
from vorversion import einstellungsprobe_format25, finden
from historical_runtime import historical_app


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def criterion(identity='view', **extra):
    value = dict(id=identity, name='Projektansicht', query='', list_ids=[], label_ids=[],
                 status='all', importance='all', due='any', label_mode='any', source='all')
    value.update(extra)
    return value


def seed(run):
    app = run.app
    a = app.new_item('Passend', importance=3)
    a.update(planned_date=date.today().isoformat(), estimated_minutes=30)
    b = app.new_item('Zu lang', importance=3)
    b.update(planned_date=date.today().isoformat(), estimated_minutes=60)
    c = app.new_item('Andere Woche', importance=1)
    c.update(planned_date=(date.today()+timedelta(days=14)).isoformat(), estimated_minutes=15)
    source = app.new_list_object('Projekt', [a, b])
    other = app.new_list_object('Andere Liste', [c])
    app.lists.extend([source, other]);app.save_items()
    return source, other, a, b, c


def ids(app, value):
    return {row[4]['id'] for row in app.saved_filters.entries(value)}


def fall_bedingungen(run):
    app = run.app;source, other, a, b, c = seed(run)
    before = copy.deepcopy(app.lists)
    value = criterion(_view=dict(planned='today', effort='at_most', minutes=30, importance_min='2'))
    assert ids(app, value) == {a['id']}
    assert app.saved_filters.save(value);app.saved_filters.open('view');run.idle()
    explained = app.saved_filters.explain_item(source['id'], a['id'])
    assert {v['key'] for v in explained} == {'planned', 'effort', 'importance_min'}
    assert all(v['ok'] for v in explained)
    count, hidden, reasons = app.saved_filters.hidden_reasons()
    assert count == 1 and hidden >= 2 and reasons
    app.explain_saved_filter_item(source['id'], a['id'])
    assert any('30 Minuten' in str(v) for v in run.meldungen)
    assert app.lists == before
    a['blocked_by'] = [b['id']]
    assert ids(app, criterion(_view={'blocked':'yes'})) == {a['id']}
    b['done'] = True
    assert a['id'] in ids(app, criterion(_view={'blocked':'no'}))
    a['labels'] = ['wait']
    assert a['id'] not in ids(app, criterion(_view={'exclude_labels':['wait']}))
    return dict(treffer=count, erklaerte_bedingungen=len(explained))


def fall_oder(run):
    app=run.app;source, other, a, b, c=seed(run)
    value=criterion(list_ids=[source['id']], _view={'mode':'any','effort':'at_most','minutes':20})
    assert ids(app,value)=={a['id'],b['id'],c['id']}
    value['_view']['mode']='all';assert ids(app,value)==set()
    value['_view']={'mode':'any','future_rule':7}
    assert ids(app,value)==set()
    assert app.saved_filters.conditions(value,source,a)[-1]['key']=='view_invalid'
    return {'oder_ueber_listengrenzen':True,'unbekannt_auch_bei_oder_ungueltig':True}


def fall_persistenz(run):
    app=run.app;source, other, a, b, c=seed(run)
    value=criterion(_view={'planned':'today','effort':'none'})
    assert app.saved_filters.save(value)
    raw=json.loads(Path(run.mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    assert '_view' not in raw['saved_filters'][-1]
    assert raw['saved_view_conditions_v1']['view']==value['_view']
    payload=app.app_backup_payload()['app_backup']['settings']
    assert payload['saved_view_conditions_v1']==raw['saved_view_conditions_v1']
    assert app.pin_home_filter('view',True) is not False
    app.set_home_view();run.idle()
    backup=Path(run.data).parent/'ansicht.glideapp'
    app.write_complete_backup(str(backup),app.app_backup_payload())
    run.neustart();app=run.app
    assert app.saved_filters.definition(criterion())==value['_view']
    assert ids(app,criterion())==set()
    assert app.saved_filters.delete('view')
    assert 'view' not in app.settings['saved_view_conditions_v1']
    assert app.restore_app_backup(str(backup),sections={
        'tasks':True,'settings':True,'templates':True,'activity':True},show_success=False)
    assert app.saved_filters.definition(criterion())==value['_view']
    assert app.saved_filters.open('view');run.idle()
    assert app.view_mode=='saved_filter' and ids(app,criterion())==set()
    assert app.saved_filters.delete('view')
    run.neustart();assert 'view' not in run.app.settings['saved_view_conditions_v1']


def fall_fehler(run):
    app=run.app;seed(run)
    assert app.saved_filters.save(criterion(_view={'planned':'today'}))
    before=copy.deepcopy(app.settings)
    settings=Path(run.mod.SETTINGS_FILE);before_bytes=settings.read_bytes()
    with patch.object(app,'save_settings',return_value=False):
        assert not app.saved_filters.save(criterion(_view={'effort':'none'}))
        assert app.settings==before
        assert not app.saved_filters.delete('view')
        assert app.settings==before
    with patch.object(app,'write_json_atomic',side_effect=OSError('künstlicher Schreibfehler')):
        assert not app.saved_filters.save(criterion(_view={'effort':'none'}))
        assert app.settings==before and settings.read_bytes()==before_bytes
    app._data_read_only=True
    try:
        assert not app.saved_filters.save(criterion(_view={'effort':'none'}))
        assert app.settings==before and settings.read_bytes()==before_bytes
    finally:
        app._data_read_only=False
    assert not app.saved_filters.save(criterion(_view={'planned':'range','start':'bad','end':'2026-10-21'}))
    assert app.settings==before
    app.settings['saved_view_conditions_v1']['view']={'future':{'keep':True}}
    assert app.save_settings();run.neustart();app=run.app
    assert app.settings['saved_view_conditions_v1']['view']=={'future':{'keep':True}}
    assert ids(app,criterion())==set()


def fall_altleser(run):
    app=run.app;seed(run)
    value=criterion(_view={'planned':'this_week','exclude_labels':['wait']},
                    _layout=dict(display='table',group='list',columns=['title','source'],sort='title'))
    assert app.saved_filters.save(value)
    settings=Path(run.mod.SETTINGS_FILE)
    raw=json.loads(settings.read_text(encoding='utf-8'))
    run.ende()
    einstellungsprobe_format25(run.mod.SAVE_FILE)
    old=finden(REPO.parents[1],'3.43.1',REPO/'CHANGELOG.md');assert old is not None  # seit 3.44.0 im Archiv
    code='import sys;sys.path.insert(0,sys.argv[3]);from test_schutzrunde import Lauf\nr=Lauf(sys.argv[1],sys.argv[2]);assert r.app.save_settings();r.ende()'
    with historical_app(REPO.parents[1],old) as old_runtime:
        child=subprocess.run([sys.executable,'-B','-c',code,str(old_runtime),run.data,str(REPO/'tests/integration')],capture_output=True,text=True,timeout=90)
    assert child.returncode==0,(child.stdout+child.stderr)[-1200:]
    after=json.loads(settings.read_text(encoding='utf-8'))
    assert after['saved_view_conditions_v1']==raw['saved_view_conditions_v1']
    assert after['saved_view_layouts_v1']==raw['saved_view_layouts_v1']
    run.start();assert run.app.saved_filters.definition(criterion())==value['_view']
    return {'altleser_sha256':hashlib.sha256(old.read_bytes()).hexdigest(),'historische_begleitmodule':True}


def fall_altfilter(run):
    app=run.app;source,other,a,b,c=seed(run)
    a['due']=date.today().isoformat()
    b['due']=(date.today()+timedelta(days=1)).isoformat()
    c.update(done=True,due=(date.today()-timedelta(days=1)).isoformat())
    assert app.save_items()
    criteria=[criterion(status=status,due=due,importance=importance)
              for status in ('all','open','done')
              for due in ('any','none','today','tomorrow','overdue')
              for importance in ('all','3')]
    expected=[sorted(ids(app,value)) for value in criteria]
    request=Path(run.data).parent/'altfilter.json'
    request.write_text(json.dumps(criteria),encoding='utf-8')
    run.ende()
    einstellungsprobe_format25(run.mod.SAVE_FILE)
    old=finden(REPO.parents[1],'3.43.1',REPO/'CHANGELOG.md');assert old is not None  # seit 3.44.0 im Archiv
    code='''import sys,json;from pathlib import Path
sys.path.insert(0,sys.argv[3]);from test_schutzrunde import Lauf
r=Lauf(sys.argv[1],sys.argv[2]);values=json.loads(Path(sys.argv[4]).read_text(encoding="utf-8"))
print("ERGEBNIS "+json.dumps([sorted(row[4]["id"] for row in r.app.saved_filters.entries(v)) for v in values]));r.ende()
'''
    with historical_app(REPO.parents[1],old) as old_runtime:
        child=subprocess.run([sys.executable,'-B','-c',code,str(old_runtime),run.data,str(REPO/'tests/integration'),str(request)],capture_output=True,text=True,timeout=90)
    assert child.returncode==0,(child.stdout+child.stderr)[-1200:]
    actual=json.loads(next(line[9:] for line in child.stdout.splitlines() if line.startswith('ERGEBNIS ')))
    assert actual==expected,(actual,expected)
    run.start()
    return {'alte_kombinationen':len(criteria),'identisch_zum_ausgelieferten_leser':True,'historische_begleitmodule':True}


def fall_dialog(run):
    app=run.app;seed(run)
    failure=[]
    size=[]
    original_modal=app.run_modal
    def modal(dialog,**kwargs):
        dialog.geometry('780x570+30+30')
        def act():
            try:
                size.append([dialog.winfo_width(),dialog.winfo_height()])
                assert size[-1][0]<=860 and size[-1][1]<=700,size
                def button(text):
                    return next(w for w in descendants(dialog) if isinstance(w,run.mod.RoundedButton) and w.text==text)
                canvas=next(w for w in descendants(dialog) if isinstance(w,run.mod.tk.Canvas)
                            and any(w.type(item)=='window' for item in w.find_all()))
                canvas.yview_moveto(1);run.idle()
                def click(widget):
                    widget.event_generate('<ButtonPress-1>',x=10,y=10)
                    widget.event_generate('<ButtonRelease-1>',x=10,y=10)
                click(button('Weitere Bedingungen'));run.idle()
                choices=[w for w in descendants(dialog) if isinstance(w,run.mod.AppOptionMenu)]
                chosen=next(w for w in choices if w.cget('text')=='Jeder Bearbeitungstag')
                menu=chosen['menu']
                index=next(i for i in range(menu.index('end')+1) if menu.entrycget(i,'label')=='Heute')
                menu.invoke(index);run.idle()
                save=button('Speichern')
                assert save.winfo_ismapped() and save.winfo_rooty()+save.winfo_height()<=dialog.winfo_rooty()+dialog.winfo_height()
                assert not failure
                click(save)
            except Exception:
                failure.append(traceback.format_exc());dialog.destroy()
        dialog.after(150,act)
        return original_modal(dialog,**kwargs)
    with patch.object(app,'run_modal',side_effect=modal):
        value=app.saved_filters.edit_dialog()
    assert not failure,failure
    assert value and value['_view']['planned']=='today'
    assert app.saved_filters.save(value)
    assert len(app.saved_filters.entries(value))==2
    return {'scrollbarer_dialog_fester_fuss':True,'abmessungen':size,
            'schrift':app.settings.get('ui_font_size','mittel')}


def fall_dialog_gross(run):
    run.app.settings['ui_font_size']='gross'
    run.app.apply_ui_font();run.idle()
    return fall_dialog(run)


def fall_tempo(run):
    import view_definition as views
    definition={'planned':'today','effort':'at_most','minutes':30,'importance_min':'2','blocked':'no','exclude_labels':['wait']}
    facts=[dict(planned_date=date.today().isoformat(),estimated_minutes=20,importance=3,blocked=False,labels=[]) for _ in range(10000)]
    prepared=views.Prepared(definition,date.today())
    values=[]
    for _ in range(6):
        start=time.perf_counter()
        count=sum(prepared.matches(f) for f in facts)
        elapsed=(time.perf_counter()-start)*1000
        assert count==10000
        values.append(elapsed)
    median=statistics.median(values[1:])
    assert median<=100,values
    app=run.app
    tasks=[app.new_item('Aufgabe '+str(i),importance=3) for i in range(10000)]
    for task in tasks:
        task.update(planned_date=date.today().isoformat(),estimated_minutes=20)
    source=app.new_list_object('Messbestand',tasks)
    app.lists.append(source)
    assert app.save_items()
    criteria=criterion(_view=definition)
    real=[]
    before=copy.deepcopy(app.lists)
    for _ in range(3):
        start=time.perf_counter();entries=app.saved_filters.entries(criteria)
        real.append((time.perf_counter()-start)*1000)
        assert len(entries)==10000, dict(treffer=len(entries),
            listen=[(v['title'],len(v['items'])) for v in app.planning_lists()],
            punkte=len(source['items']),beispiel=app.saved_filters.conditions(criteria,source,tasks[0]))
    assert app.lists==before
    return {'punkte':10000,'reine_auswertung_ms':values[1:],'median_ms':median,'grenze_ms':100,
            'app_auswertung_ms':real,'app_quellen_unveraendert':True}


def fall_darstellung(run):
    app=run.app; source,other,a,b,c=seed(run)
    a['text']='Zweite'; b['text']='Erste'; c['text']='Dritte'
    a['labels']=['one','two']; b['labels']=['one']
    app.labels.extend([dict(id='one',name='Eins',color='blue'),dict(id='two',name='Zwei',color='green')])
    assert app.save_items()
    before=copy.deepcopy(app.lists)
    value=criterion(_layout=dict(display='table',group='list',sort='title',direction='asc',
                                columns=['title','source','importance'],widths={'title':450}))
    assert app.saved_filters.save(value);assert app.saved_filters.open('view');run.idle()
    assert app.is_saved_table_view()
    assert tuple(app.tree.cget('columns'))==('title','source','importance')
    assert [v[4]['id'] for v in app.saved_filters.entries()]==[c['id'],b['id'],a['id']]
    assert len(app.tree.get_children(''))==2
    # Echte Überschrift durchläuft aufsteigend, absteigend, Listenreihenfolge.
    command=app.tree.heading('title','command');app.tree.tk.call(command);run.idle()
    assert app.saved_filters.layout()['direction']=='desc'
    assert [v[4]['id'] for v in app.saved_filters.entries()]==[a['id'],b['id'],c['id']]
    assert app.saved_filters.change_display('list');run.idle()
    assert not app.workspace.visible and 'headings' not in str(app.tree.cget('show'))
    assert len(app.tree.get_children(''))==2
    assert app.saved_filters.update_layout(group='label');run.idle()
    rows=[row for row,source_id in app.in_progress_item_sources.items() if source_id[1]==a['id']]
    assert len(rows)==2 and len(set(rows))==2
    assert app.lists==before
    return dict(tabelle_liste_gruppen=True,echte_sortierueberschrift=True,label_mehrfachzeilen=True,originale_unveraendert=True)


def fall_darstellung_persistenz(run):
    app=run.app;source,other,a,b,c=seed(run)
    layout=dict(display='table',group='importance',sort='estimated_minutes',direction='desc',
                columns=['title','source','estimated_minutes'],widths={'title':480,'source':190},hide_empty=True)
    assert app.saved_filters.save(criterion(_layout=layout));assert app.saved_filters.open('view');run.idle()
    # Geänderte Breite über denselben Abschluss wie echtes Ziehen sichern.
    app.tree.column('title',width=510);app.remember_table_column_widths();run.idle()
    expected=copy.deepcopy(app.saved_filters.layout())
    assert expected['widths']['title']==510
    settings=Path(run.mod.SETTINGS_FILE)
    raw=json.loads(settings.read_text(encoding='utf-8'))
    assert '_layout' not in raw['saved_filters'][0]
    assert raw['saved_view_layouts_v1']['view']==expected
    backup=Path(run.data).parent/'darstellung.glideapp'
    app.write_complete_backup(str(backup),app.app_backup_payload())
    run.neustart();app=run.app;run.idle()
    assert app.view_mode=='saved_filter' and app.saved_filters.layout()==expected
    assert app.saved_filters.delete('view')
    assert 'view' not in app.settings['saved_view_layouts_v1']
    assert app.restore_app_backup(str(backup),sections={'tasks':True,'settings':True,'templates':True,'activity':True},show_success=False)
    assert app.saved_filters.open('view');run.idle()
    assert app.saved_filters.layout()==expected
    original=copy.deepcopy(app.settings)
    with patch.object(app,'save_settings',return_value=False):
        assert not app.saved_filters.update_layout(display='columns')
    assert app.settings==original and app.is_saved_table_view()
    unknown=dict(expected,future_layout=7)
    app.settings['saved_view_layouts_v1']['view']=unknown
    app.refresh_tree();run.idle()
    assert 'Darstellung ungültig' in app.saved_filters.summary(app.saved_filters.current())
    assert not app.saved_filters.update_layout(display='columns')
    assert app.settings['saved_view_layouts_v1']['view']==unknown
    return dict(neustart=True,app_sicherung=True,breiten_gesichert=True,schreibfehler_rueckweg=True,unbekannt_erhalten=True)


def fall_spaltenboard(run):
    app=run.app;source,other,a,b,c=seed(run)
    value=criterion(_layout=dict(display='columns',group='importance',sort='title',direction='asc'))
    assert app.saved_filters.save(value);app.saved_filters.open('view');run.idle()
    work=app.workspace
    assert work.visible and work.mode=='board' and work.board()['layout']=='columns'
    assert {item['id'] for _,item in work.column_entries()}=={a['id'],b['id'],c['id']}
    before=copy.deepcopy(app.lists);depth=len(app.undo_stack)
    assert work.move_to_column(a['id'],'3','1');run.idle()
    assert a['importance']==1 and b['importance']==3 and len(app.undo_stack)==depth+1
    app.undo_last_change();run.idle()
    assert app.lists==before
    app.redo_last_change();run.idle()
    assert app.find_item_in_lists(a['id'])[0]['importance']==1
    work.toggle_column('1');run.idle()
    assert '1' in app.saved_filters.layout()['collapsed']
    work.configure_board('hide_empty',True);run.idle()
    assert app.saved_filters.layout()['hide_empty']
    work.set_board_group_field('done');run.idle()
    work.configure_board('hide_empty',False);run.idle()
    # Tastaturalternative nutzt denselben Mutationsweg, mit sichtbarer Auswahl.
    work.selected_id=b['id'];work._selected_column='open'
    work.move_card_to_neighbour_column(1);run.idle()
    assert app.find_item_in_lists(b['id'])[0]['done'], dict(columns=getattr(work,'column_order',None),
        hits=getattr(work,'column_hits',None),selected=work.selected_id,selection=work.selection(),messages=run.meldungen)
    assert not any(key.startswith('view:') for key in app.settings['pinboards'])
    assert app.saved_filters.change_display('table');run.idle()
    assert not work.visible and app.is_saved_table_view()
    return dict(original_mutation_ein_undo_redo=True,alt_pfeil=True,gruppen_optionen=True,keine_pin_kopien=True)


def fall_ansicht_speichern(run):
    app=run.app;source,other,a,b,c=seed(run)
    app.set_active_list(source['id']);app.set_table_view();run.idle()
    app.settings['table_columns'][source['id']]=['title','due','importance']
    app.settings['table_sort'][source['id']]=dict(column='importance',direction='desc')
    app.set_list_group('importance');app.search_var.set('Passend');run.idle()
    with patch.object(app.saved_filters,'edit_dialog',side_effect=lambda value: value):
        app.saved_filters.capture_current()
    run.idle()
    assert app.view_mode=='saved_filter'
    current=app.saved_filters.current();first=current['id']
    assert current['query']=='passend' and current['list_ids']==[source['id']]
    assert app.saved_filters.layout()['columns']==['title','due','importance']
    assert app.saved_filters.layout()['sort']=='importance'
    assert app.saved_filters.layout()['group']=='importance'
    with patch.object(app.saved_filters,'edit_dialog',side_effect=lambda value: dict(value,name='Kopie')):
        app.saved_filters.capture_current()
    assert app.saved_filters.current()['id']!=first
    app.set_active_list(source['id']);app.workspace.set_mode('board')
    app.workspace.configure_board('layout','columns');app.workspace.set_board_group_field('done');run.idle()
    with patch.object(app.saved_filters,'edit_dialog',side_effect=lambda value: dict(value,name='Boardansicht')):
        app.saved_filters.capture_current()
    run.idle()
    assert app.saved_filters.layout()['display']=='columns' and app.saved_filters.layout()['group']=='done'
    return dict(tabelle_mit_suche_gruppe_sortierung=True,eigenstaendige_kopie=True,spaltenboard=True)


def fall_gruppenziehen(run):
    from types import SimpleNamespace
    app=run.app;source,other,a,b,c=seed(run)
    assert app.saved_filters.save(criterion(_layout=dict(group='importance',hide_empty=False)))
    app.saved_filters.open('view');run.idle()
    row=next(row for row,value in app.in_progress_item_sources.items() if value[1]==a['id'])
    target=next(row for row in app.tree.get_children('') if app.tree.item(row,'text').startswith('Niedrig'))
    # Die tatsächlichen Press-/Motion-/Release-Einstiege verwenden.
    app.tree.see(row);run.idle();x,y,w,h=app.tree.bbox(row)
    app.on_drag_start(SimpleNamespace(x=x+45,y=y+h//2,state=0))
    assert app.drag_start_id==row and app.drag_item_ids==[a['id']]
    depth=len(app.undo_stack)
    app.tree.see(target);run.idle();x,y,w,h=app.tree.bbox(target)
    event=SimpleNamespace(x=x+45,y=y+h//2,state=0,x_root=app.tree.winfo_rootx()+x+45,
                          y_root=app.tree.winfo_rooty()+y+h//2)
    app.on_drag_motion(event);app.on_drag_end(event);run.idle()
    assert a['importance']==1 and len(app.undo_stack)==depth+1
    app.undo_last_change();run.idle()
    assert app.find_item_in_lists(a['id'])[0]['importance']==3
    return dict(echte_zieheinstiege=True,eine_feldaenderung=True,ein_undo=True)


def fall_darstellung_ui(run):
    if not getattr(run,'ui_fresh',False):
        # Tk-Stile/Schriften aus den vorangehenden Interpreterwechseln gehören
        # nicht zum realen Einzelstart. Sichtnachweis deshalb separat starten.
        with tempfile.TemporaryDirectory(prefix='glide-ansicht-ui-') as temporary:
            report=Path(temporary)/'ui.json'
            command=[sys.executable,str(Path(__file__).resolve()),'--app',str(run.app_path),
                     '--fall','darstellung_ui','--ui-fresh','--report',str(report)]
            if getattr(run,'capture',None):command += ['--capture',str(run.capture)]
            child=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',timeout=120)
            assert child.returncode==0,(child.stdout+child.stderr)[-1800:]
            return json.loads(report.read_text(encoding='utf-8'))['faelle']['darstellung_ui']['messung']
    app=run.app;source,other,a,b,c=seed(run)
    a['text']='Langer deutscher Aufgabentitel für die gespeicherte Projektübersicht mit Kontext und Planung'
    value=criterion(name='Projektübersicht mit langfristiger Planung und deutschen Beschriftungen',
                    _layout=dict(display='list',group='list',sort='title'))
    assert app.saved_filters.save(value);app.saved_filters.open('view')
    configurations=[('hell_eng','light','860x700+20+20','gross',False),
                    ('dunkel_breit','dark','1280x800+20+20','mittel',True),
                    ('verlauf_eng','glass_dark','860x700+20+20','mittel',True),
                    ('verlauf_breit','glass_light','1280x800+20+20','gross',False)]
    checks=[]
    def screenshot(widget,name):
        if getattr(run,'capture',None):
            sys.path.insert(0,str(REPO/'tests/tools'))
            from releasedaten import save_windows_screenshot
            run.capture.mkdir(parents=True,exist_ok=True)
            save_windows_screenshot(widget,run.capture/(name+'.png'))
    for name,design,geometry,font,hints in configurations:
        app.settings['ui_font_size']=font;app.settings[run.mod.glide_interaction.HINTS_SETTING]=hints
        app.apply_ui_font();app.set_design(design)
        if design.startswith('glass'):
            preset=run.mod.glide_backdrop.presets_for(design)[0]
            app.set_backdrop_choice(preset.key)
        run.root.geometry(geometry);run.idle(3)
        for mode in ('list','table','columns'):
            assert app.saved_filters.change_display(mode);run.idle(3)
            assert not app.view_switch.winfo_ismapped(),(name,mode,'doppelter Ansichtsumschalter')
            if mode=='table':
                assert app.tree.column('title','width')>=app.TABLE_TITLE_MIN_VISIBLE,(name,app.tree.column('title','width'))
            if mode=='columns':
                choices=[w for w in descendants(app.workspace.body) if isinstance(w,run.mod.AppOptionMenu) and w.winfo_ismapped()]
                assert len(choices)==1,(name,[(str(w),w.winfo_ismapped(),w.cget('text')) for w in choices])
                choice=choices[0]
                assert choice.cget('text').startswith(app.workspace.group_choice.get()),(name,choice.cget('text'),choice.variable.get(),choice.winfo_width())
            buttons=[w for w in descendants(app.workspace.bar) if isinstance(w,run.mod.RoundedButton)]
            assert len(buttons)==4
            for button in buttons:
                assert button.winfo_ismapped(),(name,mode,button.text)
                assert button.winfo_rootx()+button.winfo_width()<=run.root.winfo_rootx()+run.root.winfo_width(),(name,mode,button.text)
                assert button.winfo_rooty()+button.winfo_height()<=run.root.winfo_rooty()+run.root.winfo_height(),(name,mode,button.text)
            screenshot(run.root,name+'_'+mode)
        def modal(dialog,**kwargs):
            dialog.geometry('780x570+30+30' if geometry.startswith('860') else '860x700+30+30')
            run.idle(3)
            options=[w for w in descendants(dialog) if isinstance(w,run.mod.AppOptionMenu)]
            # Reales Auswahlmenü; Darstellung nicht nur über die API setzen.
            menu=next(w for w in options if w.cget('text')=='Spaltenboard')['menu']
            menu.invoke(next(i for i in range(menu.index('end')+1) if menu.entrycget(i,'label')=='Tabelle'))
            canvas=next(w for w in descendants(dialog) if isinstance(w,run.mod.tk.Canvas)
                        and any(w.type(item)=='window' for item in w.find_all()))
            canvas.yview_moveto(1);run.idle(3)
            footer=[w for w in descendants(dialog) if isinstance(w,run.mod.RoundedButton) and w.text in ('Speichern','Abbrechen')]
            assert len(footer)==2 and all(w.winfo_ismapped() for w in footer)
            assert all(w.winfo_rooty()+w.winfo_height()<=dialog.winfo_rooty()+dialog.winfo_height() for w in footer)
            last=next(w for w in descendants(dialog) if isinstance(w,run.mod.tk.Checkbutton)
                      and w.cget('text')=='In der Darstellung nur offene Aufgaben')
            assert last.winfo_rooty()+last.winfo_height()<min(w.winfo_rooty() for w in footer)
            screenshot(dialog,name+'_dialog')
            button=next(w for w in footer if w.text=='Speichern')
            button.event_generate('<ButtonPress-1>',x=10,y=10)
            button.event_generate('<ButtonRelease-1>',x=10,y=10)
        with patch.object(app,'run_modal',side_effect=modal):
            result=app.saved_filters.edit_dialog(app.saved_filters.current())
        assert result and result['_layout']['display']=='table'
        checks.append(dict(konfiguration=name,darstellungen=3,dialog_fuss_und_ende_erreichbar=True))
    return dict(konfigurationen=checks,aufnahmen=16 if getattr(run,'capture',None) else 0,
                grenze='Eigene Windows-Testfenster; keine physische DPI-, Reader- oder Mehrplattformabnahme.')


CASES=('bedingungen','oder','persistenz','fehler','altleser','altfilter','dialog','dialog_gross','tempo',
       'darstellung','darstellung_persistenz','spaltenboard','ansicht_speichern','gruppenziehen')
CASES += ('darstellung_ui',)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report',type=Path);parser.add_argument('--fall',choices=CASES)
    parser.add_argument('--capture',type=Path)
    parser.add_argument('--ui-fresh',action='store_true',help=argparse.SUPPRESS)
    args=parser.parse_args();report={'app_sha256':hashlib.sha256(args.app.read_bytes()).hexdigest(),'faelle':{}}
    for name in ([args.fall] if args.fall else CASES):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-ansichten-') as directory:
            try:
                run=Lauf(args.app,str(Path(directory)/'daten'))
                run.capture=args.capture
                run.ui_fresh=args.ui_fresh
                evidence=globals()['fall_'+name](run)
                assert not run.errors,run.errors
                report['faelle'][name]={'ok':True,'messung':evidence};print('OK',name,evidence or '',flush=True)
            except Exception:
                error=traceback.format_exc().replace(str(Path.home()),'~').replace(str(Path.home()).replace('\\','\\\\'),'~')[-2500:]
                report['faelle'][name]={'ok':False,'fehler':error};print('ROT',name,error,flush=True)
            finally:
                if run is not None:run.app.previews.close();run.ende()
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(any(not v['ok'] for v in report['faelle'].values()))


if __name__=='__main__':raise SystemExit(main())
