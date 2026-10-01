"""T2/W1: reale Speicher-/Ladewege, Fehler, Tabellen- und Listenbreiten."""
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

repo = Path(__file__).resolve().parents[2]
with tempfile.TemporaryDirectory(prefix='glide-fundament-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_fundament', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    errors, dialogs = [], []
    mod.ListApp.show_error = staticmethod(lambda *args: dialogs.append(args))
    root = mod.tk.Tk()
    root.geometry('1280x840+20+20')
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    try:
        root.update()
        item = app.new_item('Tabellentitel', due='2026-12-24', due_time='14:30')
        app.items.append(item)
        app.save_items()
        app.refresh_tree()
        root.update()
        expected = app.content_column_widths()
        assert expected and expected[0] > 0, expected
        with patch.object(mod.tkfont.Font, 'measure', side_effect=AssertionError('Tabellenmessung')):
            app.view_mode = app.TABLE_VIEW
            assert app.content_column_widths() is None
        app.view_mode = 'list'
        assert app.content_column_widths() == expected
        app.set_table_view()
        root.update()
        assert app.content_column_widths() is None
        app.set_active_list(app.active_list_id)
        root.update()
        assert app.content_column_widths() == expected

        source = Path(mod.SAVE_FILE)
        payload = app.data_payload()
        payload['version'] = 19
        original = json.dumps(payload, ensure_ascii=False).encode()
        source.write_bytes(original)
        app._schema20_backup_checked = False
        with patch.object(mod.shutil, 'copy2', side_effect=OSError('Sicherung gesperrt')):
            assert not app.save_items(show_error=False)
        assert app.dirty and source.read_bytes() == original
        assert not app._schema20_backup_checked
        assert app.save_items(show_error=False)
        assert not app.dirty
        assert any(p.read_bytes() == original for p in Path(mod.BACKUP_DIR).glob('liste_vor_format20_*.json'))

        # Reload liefert den Formatwert bereits: erster anschließender Save ohne JSON-Parse.
        app.load_items()
        root.update()
        original_load = mod.json.load
        def checked_load(file, *args, **kwargs):
            assert Path(file.name) != source, 'Zusatz-Parse der Datendatei'
            return original_load(file, *args, **kwargs)
        with patch.object(sys.modules['schema_backups'].json, 'load', side_effect=checked_load):
            assert app.save_items(show_error=False)
        assert not errors and not dialogs, (errors, dialogs)
        print('Formatsicherung, Fehler/Retry, Reload und Tabellen-/Listenbreiten: ok')
    finally:
        root.destroy()
