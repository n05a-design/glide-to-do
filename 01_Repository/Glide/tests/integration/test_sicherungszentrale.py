"""Sicherungsübersicht, sichere Dateiauswahl und vorhandene Restorewege über echte Tk-Dialoge."""
import argparse
import copy
import gc
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import traceback
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tests/integration'))
from test_uiux_paket import Lauf, knoepfe, knopf_befunde


def button(dialog, mod, text):
    label = mod.RoundedButton.action_text(text)
    return next(b for b in knoepfe(dialog, mod.RoundedButton) if b.text == label)


def visit(lauf, title, open_dialog, action):
    visited, failures = [], []

    def interact():
        dialog = next((w for w in lauf.root.winfo_children()
                       if isinstance(w, lauf.mod.tk.Toplevel) and w.title() == title), None)
        try:
            assert dialog is not None, title
            lauf.idle()
            action(dialog)
            visited.append(True)
        except Exception:
            failures.append(traceback.format_exc().replace(str(Path.home()), '~'))
        finally:
            if dialog is not None and dialog.winfo_exists():
                dialog.destroy()

    lauf.root.after(80, interact)
    result = open_dialog()
    lauf.idle()
    assert visited and not failures, failures
    return result


def backup(lauf, name='liste_backup_test.json', text='Alter Stand'):
    app, mod = lauf.app, lauf.mod
    item = app.new_item(text)
    data = app.data_payload()
    data['lists'] = [{'id': 'sicherung-liste', 'title': 'Sicherungsprobe', 'items': [item]}]
    path = Path(mod.BACKUP_DIR) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    return path, data


def fall_uebersicht(lauf):
    app, mod = lauf.app, lauf.mod
    path, _ = backup(lauf)
    before = path.read_bytes()

    def action(dialog):
        assert any(a['id'] == 'show_backup_catalog' for a in app.app_action_entries())
        tree = next(iter(knoepfe(dialog, mod.ttk.Treeview)))
        entry = next(iter(knoepfe(dialog, mod.tk.Entry)))
        assert len(tree.get_children()) >= 1
        entry.insert(0, 'TEST Aufgaben')
        lauf.idle()
        assert len(tree.get_children()) == 1
        button(dialog, mod, 'Lesen').command()
        lauf.idle()
        detail = next(w for w in knoepfe(dialog, mod.tk.Label) if w.winfo_name() == 'backup_detail')
        assert '1 Listen · 1 Punkte' in detail.cget('text'), detail.cget('text')
        assert 'Speicherstufe 26' in detail.cget('text')
        entry.delete(0, 'end')
        entry.insert(0, 'KEIN TREFFER')
        lauf.idle()
        assert not tree.get_children()
        assert button(dialog, mod, 'Wiederherstellen …').cget('state') == 'disabled'

    visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog, action)
    assert path.read_bytes() == before
    return 'Echter Menü-/Katalogeintrag, Filter, Metadaten, lesende Inhaltsprüfung und Leerzustand'


def fall_datei_fehler(lauf):
    app, mod = lauf.app, lauf.mod
    path = Path(lauf.data) / 'extern' / 'defekt.glideapp'
    path.parent.mkdir()
    path.write_bytes(b'Kein ZIP und kein JSON')
    before = path.read_bytes()

    def action(dialog):
        with patch.object(mod.filedialog, 'askopenfilename', return_value=str(path)):
            button(dialog, mod, 'Datei …').command()
        lauf.idle()
        state = dialog._glide_backup_catalog
        assert any(row.path == str(path) for row in state['rows'].values())
        button(dialog, mod, 'Lesen').command()
        detail = next(w for w in knoepfe(dialog, mod.tk.Label) if w.winfo_name() == 'backup_detail')
        assert 'Lesen fehlgeschlagen' in detail.cget('text')

    visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog, action)
    assert path.read_bytes() == before
    return 'Externe Datei ausdrücklich aufgenommen, defekten Inhalt sichtbar gemeldet und unverändert erhalten'


def fall_vergleichen(lauf):
    app, mod = lauf.app, lauf.mod
    path, data = backup(lauf)
    second = Path(lauf.data) / 'anderer-ordner' / path.name
    second.parent.mkdir()
    changed = copy.deepcopy(data)
    changed['lists'][0]['items'][0]['text'] = 'Neuer Stand'
    second.write_text(json.dumps(changed), encoding='utf-8')

    def action(dialog):
        assert len(dialog._glide_compare['items_changed']) == 1

    visit(lauf, 'Sicherungen vergleichen',
          lambda: app.show_backup_compare_dialog(older_path=str(path), newer_path=str(second)), action)
    calls = []
    with patch.object(app, 'show_backup_compare_dialog', side_effect=lambda **kw: calls.append(kw)):
        visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog,
              lambda dialog: button(dialog, mod, 'Vergleichen').command())
    assert calls == [{'older_path': str(path)}], calls
    return 'Auswahl direkt zum Vergleich; gleichnamige Dateien aus verschiedenen Ordnern bleiben getrennt'


def fall_wiederherstellen(lauf):
    app, mod = lauf.app, lauf.mod
    path, _ = backup(lauf)
    app.save_items()
    before = Path(mod.SAVE_FILE).read_bytes()
    ids = [entry['id'] for entry in app.lists]
    with patch.object(app, 'ask_yes_no', return_value=False), patch.object(
            app, 'import_full_backup', wraps=app.import_full_backup) as restore:
        visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog,
              lambda dialog: button(dialog, mod, 'Wiederherstellen …').command())
    restore.assert_called_once_with(path=str(path))
    assert [entry['id'] for entry in app.lists] == ids
    assert Path(mod.SAVE_FILE).read_bytes() == before
    return 'Bestehender Importweg mit Bestätigung; Ablehnen erhält Listen und Hauptdatei unverändert'


def fall_anhaenge(lauf):
    app, mod = lauf.app, lauf.mod
    path = Path(lauf.data) / 'Probe.cmd'
    path.write_text('rem Wird niemals ausgeführt', encoding='utf-8')
    with patch.object(mod.os, 'startfile', create=True) as win, patch.object(mod.subprocess, 'Popen') as unix:
        with patch.object(app, 'ask_yes_no', return_value=False) as ask:
            assert app.open_external_path(str(path)) is False
            assert ask.call_args.kwargs['default'] == 'no'
            assert 'Sicherung oder Vorlage' in ask.call_args.args[1]
        win.assert_not_called()
        unix.assert_not_called()
        with patch.object(app, 'ask_yes_no', return_value=True):
            assert app.open_external_path(str(path)) is True
        assert win.call_count + unix.call_count == 1
    # Echter Anhangseditor: ausstehender, lokal gewählter Anhang nimmt denselben Weg.
    dialog = mod.tk.Toplevel(lauf.root)
    attachments = [{'name': path.name, 'pending_path': str(path)}]
    listing = app._make_attachment_editor(dialog, dialog, attachments)
    listing.selection_set(0)
    try:
        with patch.object(app, 'ask_yes_no', return_value=False) as ask, patch.object(
                mod.os, 'startfile', create=True) as win, patch.object(mod.subprocess, 'Popen') as unix:
            button(dialog, mod, 'Öffnen').command()
            ask.assert_called_once()
            win.assert_not_called()
            unix.assert_not_called()
    finally:
        dialog.destroy()
    # Die tatsächliche Rückfrage erlaubt auch mit Enter keine Ausführung.
    def decline_with_enter(dialog):
        dialog.focus_force()
        lauf.idle()
        dialog.event_generate('<Return>')

    with patch.object(mod.os, 'startfile', create=True) as win, patch.object(mod.subprocess, 'Popen') as unix:
        assert visit(lauf, 'Ausführbaren Anhang öffnen?',
                     lambda: app.open_external_path(str(path)), decline_with_enter) is False
        win.assert_not_called()
        unix.assert_not_called()
    return 'Abbruch verhindert OS-Aufruf, Zustimmung einmalig; echter Anhangseditor führt durch die Typregel'


def fall_layout(lauf):
    app, mod = lauf.app, lauf.mod
    backup(lauf, 'liste_backup_' + 'Langer-Dateiname-' * 8 + '.json')
    count = 0
    for font in ('mittel', 'gross'):
        app.settings['ui_font_size'] = font
        lauf.neustart()
        app = lauf.app

        def action(dialog):
            nonlocal count
            for geometry in ('600x480', '800x600'):
                dialog.geometry(geometry)
                lauf.idle(6)
                n, errors = knopf_befunde(dialog, mod, f'Sicherungen {font} {geometry}')
                assert not errors, errors
                count += n

        visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog, action)
    return f'{count} Knopfprüfungen bei 600x480/800x600 und mittlerer/großer Schrift'


def fall_lebensdauer(lauf):
    app, mod = lauf.app, lauf.mod
    variables = []

    def action(dialog):
        entry = next(iter(knoepfe(dialog, mod.tk.Entry)))
        name = str(entry.cget('textvariable'))
        assert 'render' in str(lauf.root.tk.call('trace', 'info', 'variable', name))
        variables.append(name)

    for _ in range(5):
        visit(lauf, 'Sicherungsübersicht', app.show_backup_catalog, action)
        gc.collect()
    retained = [name for name in variables if 'render' in str(
        lauf.root.tk.call('trace', 'info', 'variable', name))]
    assert not retained, f'Geschlossene Dialoge behalten {len(retained)} Suchrückrufe'
    return 'Fünfmal öffnen/schließen: keine Suchrückrufe an zerstörten Dialogen erhalten'


FAELLE = ('uebersicht', 'datei_fehler', 'vergleichen', 'wiederherstellen', 'anhaenge', 'layout', 'lebensdauer')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=REPO / 'src/glide/app.pyw')
    parser.add_argument('--fall', choices=FAELLE + ('alle',), default='alle')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = {'app_sha256': hashlib.sha256(args.app.read_bytes()).hexdigest(), 'faelle': {}, 'fehler': []}
    for name in (FAELLE if args.fall == 'alle' else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix='glide-sicherungen-') as data:
            lauf = None
            try:
                lauf = Lauf(args.app, data)
                detail = globals()['fall_' + name](lauf)
                assert not lauf.errors, lauf.errors
                result['faelle'][name] = {'ok': True, 'befund': detail}
                print('OK', name, detail, flush=True)
            except Exception:
                detail = traceback.format_exc().replace(str(Path.home()), '~')[-2000:]
                result['faelle'][name] = {'ok': False, 'befund': detail}
                result['fehler'].append(name)
                print('ROT', name, detail, flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return int(bool(result['fehler']))


if __name__ == '__main__':
    sys.exit(main())
