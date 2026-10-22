"""FP-04: Originale, Flächen-Undo, alte ausgelieferte Fassung und Bedienwege."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import statistics
import subprocess
import sys
import tempfile
import time
import traceback
from types import SimpleNamespace
from unittest.mock import patch

REPO=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(REPO/'tests/integration'))
from test_schutzrunde import Lauf
from vorversion import einstellungsprobe_format25


def seed(run):
    app=run.app
    item=app.new_item('Aufgabe')
    entry=app.new_list_object('Projekt',[item])
    page=app.new_list_object('Wissensseite',[app.new_item('Offen'),app.new_item('Fertig')],list_kind='page')
    page['items'][1]['done']=True
    page['rich_note']={'text':'Erster Absatz mit Kontext.','spans':[],'links':{}}
    note=app.new_list_object('Notiz',[],list_kind='note')
    note['rich_note']={'text':'Notizinhalt.','spans':[],'links':{}}
    app.lists.extend([entry,page,note]);assert app.save_items()
    app.set_active_list(entry['id']);run.idle()
    return entry,page,note,item


def fall_inhalt_undo(run):
    app=run.app;entry,page,note,item=seed(run);view=app.workspace
    identity='page:'+page['id']
    app.pin_page_on_board(page['id']);run.idle()
    assert identity in view.card_ids
    assert view.view_undo_pending()
    app.undo_last_change();run.idle();assert identity not in view.card_ids
    app.redo_last_change();run.idle();assert identity in view.card_ids
    blocks,_=view.page_card_blocks(page,300)
    assert any('1 offene Aufgaben' in b.get('text','') for b in blocks)
    assert any('Erster Absatz' in b.get('text','') for b in blocks)
    with app.sidebar_change(refresh_tree=True) as change:
        page['title']='Neuer Titel';page['rich_note']['text']='Geänderter Kontext';change.mark()
    assert any('Neuer Titel' in b.get('text','') for b in view.page_card_blocks(page,300)[0])
    view.selected_id=identity;view.selected_ids=[identity]
    before=copy.deepcopy(view.board());view.move_card(1,0);assert view.board()!=before
    app.undo_last_change();assert view.board()==before
    view.pin([item['id']]);view.toggle_connection(identity,item['id'])
    assert view.connections();app.undo_last_change();assert not view.connections()
    app.redo_last_change();assert view.connections()
    view.selected_id=identity;view.selected_ids=[identity];view.unpin();run.idle()
    assert identity not in view.card_ids
    app.undo_last_change();run.idle();assert identity in view.card_ids and view.connections()
    view.open_page_card(identity);run.idle();assert app.active_list_id==page['id']
    return {'offene_aufgaben':1,'auszug_max':160}


def fall_archiv_loeschen(run):
    app=run.app;entry,page,note,item=seed(run);view=app.workspace
    app.pin_page_on_board(page['id']);identity='page:'+page['id'];run.idle()
    assert app.set_archived('list',page['id'],True);run.idle();assert identity not in view.valid_pages()
    assert identity not in str(view.board())
    app.undo_last_change();run.idle();assert identity in view.valid_pages() and identity in str(view.board())
    app.ask_yes_no=lambda *a,**k:True
    app.delete_list_by_id(page['id']);run.idle();assert identity not in view.valid_pages()
    app.undo_last_change();run.idle();assert identity in view.valid_pages() and identity in str(view.board())


def fall_auswahl_ziehen(run):
    app=run.app;entry,page,note,item=seed(run);view=app.workspace
    selected='page:'+note['id']
    def choose(dialog):
        widgets=[dialog];tree=None
        while widgets:
            widget=widgets.pop();widgets.extend(widget.winfo_children())
            if isinstance(widget,run.mod.ttk.Treeview):tree=widget
        assert tree is not None and selected in tree.get_children()
        tree.selection_set(selected)
        widgets=[dialog]
        while widgets:
            widget=widgets.pop();widgets.extend(widget.winfo_children())
            if isinstance(widget,run.mod.RoundedButton) and widget.text=='Anheften':
                widget.command();break
        run.idle()
        assert not dialog.winfo_exists(),'Auswahl wurde nicht übernommen'
    with patch.object(app,'run_modal',side_effect=choose):view.choose_cards()
    run.idle();assert selected in view.card_ids
    iid=app.find_sidebar_iid(('list',page['id']));assert iid
    tree=app.get_sidebar_tree_for_iid(iid);tree.see(iid);run.idle()
    box=tree.bbox(iid);assert box
    x,y=box[0]+40,box[1]+box[3]//2
    root_x,root_y=view.canvas.winfo_rootx()+30,view.canvas.winfo_rooty()+30
    tree.event_generate('<ButtonPress-1>',x=x,y=y,rootx=tree.winfo_rootx()+x,rooty=tree.winfo_rooty()+y,time=10000)
    run.idle()
    assert view.visible and view.mode=='board','Mausdruck baut die Zielpinnwand vor dem Ziehen ab'
    tree.event_generate('<B1-Motion>',x=root_x-tree.winfo_rootx(),y=root_y-tree.winfo_rooty(),rootx=root_x,rooty=root_y,state=0x0100,time=10100)
    run.idle()
    tree.event_generate('<ButtonRelease-1>',x=root_x-tree.winfo_rootx(),y=root_y-tree.winfo_rooty(),rootx=root_x,rooty=root_y,time=10200)
    run.idle();assert 'page:'+page['id'] in view.card_ids
    # Ein gewöhnlicher Klick auf dieselbe Seitenzeile öffnet weiterhin das Original.
    iid=app.find_sidebar_iid(('list',page['id']));tree=app.get_sidebar_tree_for_iid(iid)
    box=tree.bbox(iid);assert box
    x,y=box[0]+40,box[1]+box[3]//2
    tree.event_generate('<ButtonPress-1>',x=x,y=y,state=0,time=11000)
    run.idle();tree.event_generate('<ButtonRelease-1>',x=x,y=y,state=0,time=11100);run.idle()
    assert app.active_list_id==page['id']


def fall_altleser_backup(run):
    app=run.app;entry,page,note,item=seed(run);view=app.workspace
    app.pin_page_on_board(page['id']);view.pin([item['id']]);view.toggle_connection('page:'+page['id'],item['id']);run.idle()
    assert app.save_settings();before=copy.deepcopy(view.board())
    raw=json.loads(Path(run.mod.SETTINGS_FILE).read_text(encoding='utf-8'))
    assert 'page_pinboards_v1' in raw
    assert 'page:'+page['id'] not in str(raw['pinboards'])
    payload=app.app_backup_payload()
    assert 'page_pinboards_v1' in payload['app_backup']['settings']
    app_path=Path(run.mod.__file__);data=run.data;run.ende()
    einstellungsprobe_format25(run.mod.SAVE_FILE)
    old=REPO.parents[1]/'07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.43.1.pyw'
    code="""import sys;sys.path.insert(0,sys.argv[3]);from test_schutzrunde import Lauf
r=Lauf(sys.argv[1],sys.argv[2]);r.app.workspace.prune();assert r.app.save_settings();r.ende()
"""
    child=subprocess.run([sys.executable,'-B','-c',code,str(old),data,str(REPO/'tests/integration')],capture_output=True,text=True,timeout=90)
    assert child.returncode==0,(child.stdout+child.stderr)[-1800:]
    assert json.loads(Path(run.mod.SETTINGS_FILE).read_text(encoding='utf-8'))['page_pinboards_v1']==raw['page_pinboards_v1']
    run.start();run.app.set_active_list(entry['id']);run.app.workspace.set_mode('board');run.idle()
    after=run.app.workspace.board()
    assert after['cards']==before['cards'] and after['connections']==before['connections'],(before,after)
    return {'altleser_app_sha256':hashlib.sha256(old.read_bytes()).hexdigest()}


def fall_titelbild_praesentation_sicherung(run):
    app=run.app;entry,page,note,item=seed(run)
    app.set_home_view();run.idle()
    menu=app.build_list_menu(page['id'])
    indices=[i for i in range(menu.index('end')+1) if menu.type(i)=='command'
             and menu.entrycget(i,'label')=='Auf Pinnwand anheften']
    assert len(indices)==1
    menu.invoke(indices[0]);run.idle()
    view=app.workspace;identity='page:'+page['id']
    assert view.context()==view.GLOBAL_SCOPE and identity in view.card_ids
    png=run.mod.tk.PhotoImage(master=run.root,width=24,height=16)
    png.put('#1185e1',to=(0,0,24,16))
    source=Path(run.data).parent/'titelbild.png';png.write(str(source),format='png')
    app.choose_page_cover(page['id'],path=str(source));run.idle()
    page=next(p for p in app.lists if p['id']==page['id'])
    blocks,_=view.page_card_blocks(page,300)
    assert any(b['art']=='bild' for b in blocks)
    assert 'data:image/png;base64,' in view.build_board_print_html()
    def area():
        app.settings['pinboards'][view.context()]['areas']=[{
            'id':'bereich','name':'Kontextbereich','x':0,'y':0,'w':1200,'h':900,'color':'accent'}]
    assert view.board_view_change(area,'Bereich angelegt')
    view.start_presentation();run.idle();assert view.presentation_active()
    html=view.build_presentation_print_html()
    assert page['title'] in html and 'Erster Absatz' in html
    view.end_presentation();run.idle()
    backup=Path(run.data).parent/'probe.glideapp'
    app.write_complete_backup(str(backup),app.app_backup_payload())
    view.selected_id=identity;view.selected_ids=[identity];view.unpin();run.idle()
    assert identity not in view.card_ids
    assert app.restore_app_backup(str(backup),sections={
        'tasks':True,'settings':True,'templates':True,'activity':True},show_success=False)
    app.open_global_board();run.idle();view=app.workspace
    assert identity in view.card_ids and view.connections()==[]
    view.selected_id=identity;view.selected_ids=[identity]
    view.canvas.focus_force();run.idle();view.canvas.event_generate('<Return>');run.idle()
    assert app.active_list_id==page['id'],'Tastatur öffnet nicht das Original'
    return {'titelbild':True,'praesentation':True,'app_sicherung':True,'tastatur':True}


def fall_druck_tempo(run):
    app=run.app;entry,page,note,item=seed(run);view=app.workspace
    # Derselbe Aufbau mit 200 Aufgabenkarten, dann 150 Aufgaben/50 Seiten.
    entry['items'][:]=[app.new_item('Karte '+str(i)) for i in range(200)]
    app.save_items();app.set_active_list(entry['id']);view.pin([i['id'] for i in entry['items']]);run.idle()
    baseline_board=copy.deepcopy(view.board())
    mixed_board=copy.deepcopy(baseline_board)
    for i,card in enumerate(mixed_board['cards'][-50:]):
        p=app.new_list_object('Seite '+str(i),[],list_kind='page');p['rich_note']={'text':'Kurzer Kontext.','spans':[],'links':{}}
        app.lists.append(p);card['item_id']='page:'+p['id'];card['list_id']=p['id']
    app.save_items()
    scope=view.context()
    def measure(board):
        app.settings['pinboards'][scope]=copy.deepcopy(board)
        start=time.perf_counter();view.draw_board()
        return (time.perf_counter()-start)*1000
    # Beide Darstellungen vorwärmen und abwechselnd messen. Die Reihenfolge
    # kehrt je Paar um, damit ein langsamerer Rechnerzustand nicht einseitig
    # nur die zweite Messreihe belastet. Grenze unverändert: maximal +10 %.
    for _ in range(2):measure(baseline_board);measure(mixed_board)
    baseline=[];current=[]
    for i in range(5):
        if i%2:
            current.append(measure(mixed_board));baseline.append(measure(baseline_board))
        else:
            baseline.append(measure(baseline_board));current.append(measure(mixed_board))
    app.settings['pinboards'][scope]=mixed_board;app.save_settings();view.draw_board()
    assert len(view.card_ids)==200 and sum(v.startswith('page:') for v in view.card_ids)==50,(len(view.card_ids),len(view.board()['cards']))
    assert statistics.median(current)<=statistics.median(baseline)*1.10,(baseline,current)
    html=view.build_board_print_html()
    assert 'Kurzer Kontext' in html and 'offene Aufgaben' in html and 'Seite 49' in html
    return {'aufgaben_ms':baseline,'gemischt_ms':current,'verhaeltnis':statistics.median(current)/statistics.median(baseline)}


CASES=('inhalt_undo','archiv_loeschen','auswahl_ziehen','altleser_backup','titelbild_praesentation_sicherung','druck_tempo')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--app',type=Path,default=REPO/'src/glide/app.pyw')
    parser.add_argument('--report',type=Path);parser.add_argument('--fall',choices=CASES)
    args=parser.parse_args();report={'app_sha256':hashlib.sha256(args.app.read_bytes()).hexdigest(),'faelle':{}}
    for name in ([args.fall] if args.fall else CASES):
        run=None
        with tempfile.TemporaryDirectory(prefix='glide-fp04-') as directory:
            try:
                run=Lauf(args.app,str(Path(directory)/'daten'))
                evidence=globals()['fall_'+name](run)
                assert not run.errors,run.errors
                report['faelle'][name]={'ok':True,'messung':evidence};print('OK',name,evidence or '',flush=True)
            except Exception:
                error=traceback.format_exc().replace(str(Path.home()),'~')[-3000:]
                report['faelle'][name]={'ok':False,'fehler':error};print('ROT',name,error,flush=True)
            finally:
                if run is not None:run.app.previews.close();run.ende()
    if args.report:args.report.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return int(any(not v['ok'] for v in report['faelle'].values()))


if __name__=='__main__':raise SystemExit(main())
