"""Geprüfte 07-Fassung mit künstlichen Daten starten und neue Aktionswege prüfen."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import date, timedelta

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
DELIVERY = ROOT/'07_Python-Versionen'
result = {'version':'3.46.0', 'schema':26, 'data_isolated':True, 'callback_errors':[]}
with tempfile.TemporaryDirectory(prefix='glide-346-lieferung-') as folder:
    os.environ['GLIDE_DATA_DIR'] = folder
    os.environ['GLIDE_TEST_MODE'] = '1'
    sys.path.insert(0, str(DELIVERY))
    loader = importlib.machinery.SourceFileLoader('glide_delivery346', str(DELIVERY/'Glide-Aufgaben-und-Listen_v3.46.0.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry('1280x800+20+20')
    root.report_callback_exception = lambda *exc: result['callback_errors'].append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *args: result['callback_errors'].append(str(args))
    app.show_info = app.show_warning = lambda *args: None

    def idle():
        root.update_idletasks()
        root.update()

    try:
        assert mod.APP_VERSION == '3.46.0' and mod.ListApp.DATA_SCHEMA_VERSION == 26
        assert Path(mod.glide_task_tiles.__file__).resolve().parent == DELIVERY.resolve()
        assert Path(mod.glide_side_view.__file__).resolve().parent == DELIVERY.resolve()
        source = app.new_list_object('Lieferprobe 3.46')
        item = app.new_item('Straße prüfen', due=date.today().isoformat(), planned_date=date.today().isoformat())
        source['items'] = [item]
        identity, source_id = item['id'], source['id']
        app.lists, app.items, app.active_list_id = [source], source['items'], source_id
        assert app.save_items()
        app.set_home_view()
        idle()
        app.undo_stack.clear()
        app.choose_home_plan('tomorrow', (identity,))
        assert app.find_item_in_lists(identity)[0]['planned_date'] == (date.today()+timedelta(days=1)).isoformat()
        assert app.find_item_in_lists(identity)[0]['due'] == date.today().isoformat()
        assert len(app.undo_stack) == 1
        app.undo_last_change()
        idle()
        assert app.find_item_in_lists(identity)[0]['planned_date'] == date.today().isoformat()
        app.complete_home_task(identity)
        assert app.find_item_in_lists(identity)[0]['done']
        app.undo_last_change()
        idle()
        assert not app.find_item_in_lists(identity)[0]['done']
        assert app.open_side_view(source_id)
        app.open_side_search()
        before = Path(mod.SAVE_FILE).read_bytes()
        app._side_search_entry.insert(0, 'STRASSE')
        idle()
        assert len(app._side_search_matches) == 1
        assert Path(mod.SAVE_FILE).read_bytes() == before
        app.close_side_view()
        views = ('set_home_view','set_today_view','set_table_view','set_library_view','set_pages_view','set_notes_view')
        for name in views:
            getattr(app, name)()
            idle()
        assert app.save_items()
        assert not result['callback_errors']
        result.update(exitcode=0, runtime_modules_from_delivery=True, plan_undo=True,
                      done_undo=True, side_search=True, views=len(views))
    finally:
        app.cancel_pending_callbacks()
        for job in root.tk.splitlist(root.tk.call('after','info')):
            root.after_cancel(job)
        app.release_data_lock()
        try:
            root.destroy()
        except mod.tk.TclError:
            # Wie im vorhandenen Harness: Tcl-Kommandos können schon vom
            # Appabbau entfernt worden sein; Interpreterfenster sicher schließen.
            if root.winfo_exists():
                root.tk.call('destroy', '.')
(HERE/'python_lieferprobe.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False))
