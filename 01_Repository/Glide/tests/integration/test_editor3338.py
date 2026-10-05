"""Editorabbau: offene Timer enden, ungespeicherte Pixel überleben den Wechsel.

--app erlaubt eine Gegenprobe. Keine echten Nutzerdaten, kein globaler Timerabbau
zwischen den geprüften Seitenwechseln.
"""
import argparse
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
args = parser.parse_args()
sys.path.insert(0, str(REPO / 'src/glide'))

with tempfile.TemporaryDirectory(prefix='glide-editor3338-') as folder:
    os.environ['GLIDE_DATA_DIR'] = folder
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_editor_test', str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    errors = []
    root = mod.tk.Tk()
    root.geometry('860x700')
    root.report_callback_exception = lambda *error: errors.append(repr(error[1]))
    app = mod.ListApp(root)
    app.show_error = app.show_warning = lambda *a, **k: errors.append(repr(a))
    drawing = app.new_list_object(title='Timerprobe', list_kind='drawing')
    tasks = app.new_list_object(title='Aufgaben')
    app.lists.extend([drawing, tasks])
    app.save_items()
    try:
        for index in range(8):
            app.set_active_list(drawing['id'])
            root.update()
            editor = app.current_drawing_editor()
            assert editor is not None
            editor.model.set_cell(index, 0, '#123456')
            editor.mark_unsaved()
            editor.schedule_save()
            # Alle Editoraufträge deterministisch noch offen halten. Damit
            # hängt die Prüfung nicht davon ab, ob Windows schon 120 ms
            # für einen echten Layouttimer gebraucht hat.
            for name, callback in (('_context_rows_job', editor.reserve_context_rows),
                                   ('_fit_job', editor.fit_zoom),
                                   ('_preview_job', editor.render_full)):
                previous = getattr(editor, name, None)
                if previous is not None:
                    editor.after_cancel(previous)
                setattr(editor, name, editor.after(10_000, callback))
            jobs = {getattr(editor, name) for name in
                    ('_context_rows_job', '_fit_job', '_preview_job', '_save_job')}
            app.set_active_list(tasks['id'])
            assert not editor.winfo_exists()
            remaining = set(root.tk.call('after', 'info'))
            assert not jobs & remaining, f'Timer des abgebauten Editors: {jobs & remaining}'
            model = mod.glide_drawing.DrawingModel.from_document(drawing['drawing'])
            assert all(model.color_at(x, 0) == '#123456' for x in range(index + 1))
            root.update()
        assert not errors, errors
        # Nicht nur das Modell: auch der atomar gespeicherte Bestand enthält
        # den letzten Pinselstand vor dem Seitenwechsel.
        import json
        saved = json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))
        saved_drawing = next(entry for entry in saved['lists'] if entry['id'] == drawing['id'])
        assert saved_drawing['drawing'] == drawing['drawing']
        print('Editor 3.33.8: acht Wechsel, alle Editor-Timer beendet, Pixel gespeichert: OK')
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        for job in root.tk.call('after', 'info'):
            root.tk.call('after', 'cancel', job)
        root.destroy()
