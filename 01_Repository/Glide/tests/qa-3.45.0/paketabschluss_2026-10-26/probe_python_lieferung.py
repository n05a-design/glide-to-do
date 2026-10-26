"""Echte Start-/Speicher-/Undo-Probe der gelieferten Pythondateien aus 07."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile


repo = Path(__file__).resolve().parents[3]
delivery = repo.parents[1] / "07_Python-Versionen"
source = delivery / "Glide-Aufgaben-und-Listen_v3.45.0.pyw"
errors = []
with tempfile.TemporaryDirectory(prefix="glide-delivery345-") as data:
    os.environ.update(GLIDE_DATA_DIR=data, GLIDE_TEST_MODE="1")
    loader = importlib.machinery.SourceFileLoader("glide_delivery345", str(source))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.report_callback_exception = lambda *error: errors.append(str(error[1]))
    app = mod.ListApp(root)
    try:
        assert mod.APP_VERSION == "3.45.0" and app.DATA_SCHEMA_VERSION == 26
        assert Path(mod.glide_home_dashboard.__file__).resolve().parent == delivery.resolve()
        entry = app.ensure_inbox_list()
        app.set_active_list(entry["id"])
        task = app.new_item("Lieferprobe 3.45.0")
        entry["items"].append(task)
        assert app.save_items()
        app.update_in_progress_item(task["id"], "done", True)
        assert app.find_item_in_lists(task["id"])[0]["done"]
        app.undo_last_change()
        assert not app.find_item_in_lists(task["id"])[0]["done"]
        views = (app.set_home_view, app.set_today_view, app.set_table_view,
                 app.set_library_view, app.set_pages_view, lambda: app.set_active_list(entry["id"]))
        for view in views:
            view()
            root.update_idletasks()
            root.update()
        assert not errors, errors
        proof = dict(exitcode=0, version=mod.APP_VERSION, schema=app.DATA_SCHEMA_VERSION,
                     source="07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.45.0.pyw",
                     home_dashboard_from_delivery=True, views=len(views), save_complete=True,
                     done_undo=True, callback_errors=errors, data_isolated=True)
        (Path(__file__).parent / "python_lieferprobe.json").write_text(
            json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(proof, ensure_ascii=False))
    finally:
        preview = getattr(app, "_previews", None)
        if preview is not None:
            preview.close()
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
