"""Gezielte, isolierte Diagnose des unveraenderten Glide-Quellstands."""
import ast
import copy
import difflib
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
REPO = BASE / '01_Repository/Glide'
SOURCE = REPO / 'src/glide/app.pyw'
ARCHIVE = REPO / 'src/glide/archiv/app_3.25.0_vor_3.26.0.pyw'
results = {'source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
old = ARCHIVE.read_text(encoding='utf-8-sig')
new = SOURCE.read_text(encoding='utf-8-sig')
def methods(source):
    return {c.name+'.'+m.name: m for c in ast.parse(source).body
            if isinstance(c, ast.ClassDef) for m in c.body if isinstance(m, ast.FunctionDef)}
a, b = methods(old), methods(new)
results['changed_methods'] = sorted(n for n in a.keys() & b.keys() if ast.dump(a[n]) != ast.dump(b[n]))
results['new_methods'] = sorted(b.keys()-a.keys())
(OUT/'quellvergleich.diff').write_text('\n'.join(difflib.unified_diff(old.splitlines(), new.splitlines(), fromfile=str(ARCHIVE), tofile=str(SOURCE))), encoding='utf-8')

with tempfile.TemporaryDirectory(prefix='glide-audit326-') as folder:
    os.environ['GLIDE_DATA_DIR'] = folder
    os.environ['GLIDE_TEST_MODE'] = '1'
    os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_audit326', str(SOURCE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    root.geometry('1300x850+0+0')
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None
    errors = []
    root.report_callback_exception = lambda *args: errors.append(str(args[1]))
    try:
        results['version'] = mod.APP_VERSION
        results['schema'] = app.DATA_SCHEMA_VERSION
        results['mascot_default'] = app.mascot_name()
        inbox = app.ensure_inbox_list()
        inbox['items'].append(app.new_item('Audit-Eingang'))
        app.save_items()
        app.set_today_view()
        root.update()
        row = app.PLAN_INBOX_HEADING_ROW_ID
        results['inbox_row'] = {'text': app.tree.item(row, 'text'), 'children': len(app.tree.get_children(row)),
                                'open': bool(app.tree.item(row, 'open'))}
        app.tree.item(row, open=False)
        results['inbox_collapsed_text'] = app.tree.item(row, 'text')

        # Two populated branches and an unrelated list: explicit folder scoping.
        app.folders = [{'id':'audit-folder','title':'Audit'}, {'id':'audit-child','title':'Child','parent_id':'audit-folder'}, {'id':'audit-other','title':'Other'}]
        one = app.new_list_object('Inside', [app.new_item('A'), app.new_item('B')])
        one['folder_id'] = 'audit-folder'
        child = app.new_list_object('Child', [app.new_item('C')]); child['folder_id'] = 'audit-child'
        other = app.new_list_object('Outside', [app.new_item('D')]); other['folder_id'] = 'audit-other'
        app.lists.extend([one,child,other])
        ws = app.workspace
        results['folder_scope'] = [x['title'] for x in ws.eligible_lists('folder:audit-folder')]
        app.set_active_folder('audit-folder')
        original_form = app.new_item_dialog
        form_call = {}
        def outside_choice(*args, **kwargs):
            form_call.update(kwargs)
            return {'text':'Outside via folder board', 'list_id':other['id'], 'kind':app.ITEM_KIND_TASK}
        app.new_item_dialog = outside_choice
        before_count = len(other['items'])
        ws.create_card_item(24,24)
        results['folder_creation_scope'] = {'allows_list_choice':form_call.get('allow_list_choice'), 'created_in_outside_list':len(other['items']) > before_count, 'outside_in_valid_items':other['items'][-1]['id'] in ws.valid_items('folder:audit-folder')}
        app.new_item_dialog = original_form
        app.set_active_list(one['id'])
        ws.pin([x['id'] for x in one['items']])
        first, second = [x['id'] for x in one['items']]
        ws.configure_board('connection_style', 'line')
        ws.toggle_connection(first, second)
        before = copy.deepcopy(ws.connections())
        ws.configure_board('connection_style', 'forward')
        results['connection_style_change'] = {'before':before, 'after': ws.connections(), 'default_after':ws.connection_style()}

        ws.open_tab(first)
        seen = {}
        original_choice = app.themed_choice_dialog
        def choose(title, prompt, choices, **kwargs):
            seen['choices'] = choices
            return choices[0][0]
        app.themed_choice_dialog = choose
        ws.tab_overview()
        results['tab_selection'] = {'valid_pairs': all(isinstance(x,tuple) and len(x)==2 for x in seen['choices']), 'opened_expected': ws.mode == first}
        app.themed_choice_dialog = original_choice

        # Tall geometry reproduces the thin-strip preview without private task data.
        cards = [{'list_id':one['id'], 'item_id':f'card-{i}', 'x':16, 'y':16+i*260, 'scale':'normal'} for i in range(205)]
        app.settings['pinboards']['global'] = {'cards':cards, 'connections':[{'from':'card-100','to':'card-101','style':'forward'}], 'width':300, 'layout':'grid'}
        boxes, links, count = app.global_board_preview()
        preview = mod.BoardPreview(root, bg_color='#1e1e1e', card_color='#2b2b2b', line_color='#999999', border_color='#333333')
        preview._boxes = boxes
        fit = preview._fitted(425,132)
        results['preview'] = {'cards_total':count,'cards_in_preview':len(boxes),'connections_total':1,'connections_reported':len(links), 'first_card_width':fit[0][2], 'first_card_height_before_minimum':fit[0][3], 'honors_grid_layout':False}
        preview.destroy()
        old_entries = [{'id':str(i),'at':'2020-01-01T12:00:00','kind':'item','action':'created','target':'Audit'} for i in range(20)]
        results['history'] = {'max_entries':app.MAX_HISTORY_ENTRIES, 'old_entries_retained':len(app.normalize_history_entries(old_entries))}
        results['callback_errors'] = errors
    finally:
        app.release_data_lock()
        root.destroy()

# Read only geometry from the actual data directory; never import/start against it.
default = Path(os.environ['APPDATA'])/'Glide'
pointer = default/'datenordner.json'
data_dir = Path(json.loads(pointer.read_text(encoding='utf-8-sig'))['path']) if pointer.exists() else default
settings = data_dir/'settings.json'
if settings.exists():
    data = json.loads(settings.read_text(encoding='utf-8-sig'))
    board = data.get('pinboards',{}).get('global',{})
    cards = board.get('cards',[])
    results['actual_preview_geometry_read_only'] = {'cards':len(cards), 'connections':len(board.get('connections',[])), 'layout':board.get('layout'), 'first40_distinct_x':len({x.get('x') for x in cards[:40]}), 'first40_y_min':min((x.get('y',0) for x in cards[:40]),default=0), 'first40_y_max':max((x.get('y',0) for x in cards[:40]),default=0), 'width':board.get('width')}
    factors = {'normal':1,'large':1.3,'small':.78}
    boxes = [(c.get('x',0),c.get('y',0),board.get('width',300)*factors.get(c.get('scale'),1)) for c in cards[:40]]
    if boxes:
        width = max(x+w for x,y,w in boxes)-min(x for x,y,w in boxes)
        height = max(y+w*.42 for x,y,w in boxes)-min(y for x,y,w in boxes)
        scale = min(409/width,116/height)
        results['actual_preview_geometry_read_only'].update({'assumed_preview_pixels':[425,132], 'logical_extent':[width,height], 'fitted_extent':[width*scale,height*scale], 'first_card_size_before_minimum':[boxes[0][2]*scale,boxes[0][2]*.42*scale]})

(OUT/'sonden-ergebnis.json').write_text(json.dumps(results,ensure_ascii=False,indent=2), encoding='utf-8')
print(json.dumps(results,ensure_ascii=False,indent=2))
