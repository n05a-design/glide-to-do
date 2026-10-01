"""Eigene Testfenster und künstliche Daten für die 3.26-Sichtprüfung."""
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import json

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / 'tests/tools'))
from releasedaten import save_windows_screenshot

with tempfile.TemporaryDirectory(prefix='glide-sicht326-') as folder:
    os.environ['GLIDE_DATA_DIR'] = folder
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('sicht326', str(REPO / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    app.settings['animations_enabled'] = False
    app.set_design('dark')
    root.geometry('1180x900+10+10')
    errors = []
    root.report_callback_exception = lambda *exc: errors.append(exc)
    output = Path(__file__).parent / 'sichtpruefung'
    def settle(window):
        window.update()
        window.after(100, window.quit)
        window.mainloop()
        window.update_idletasks()
    def inspect(dialog, parent=None):
        for width in (1040, 620):
            dialog.geometry(f'{width}x850+10+10')
            settle(dialog)
            save_windows_screenshot(dialog, output / f'punktmaske_{width}.png')
        dialog.destroy()
    app.run_modal = inspect
    try:
        app.item_form_dialog('Neuer Punkt', allow_list_choice=True)
        note = app.new_list_object('Projektnotizen', [app.new_item(f'Nächster Schritt {i}') for i in range(1, 9)],
                                   list_kind='note', rich_note={'text': 'Planung\nEine lokale Notiz mit Formatierung.\nNächste Schritte gemeinsam festhalten.',
                                   'spans': [{'tag':'h1','start':0,'end':7}, {'tag':'bold','start':12,'end':25}], 'links':{}})
        app.lists.append(note)
        app.set_active_list(note['id'])
        settle(root)
        assert int(app.tree.cget('height')) == 6
        assert app.rich_note_editor.text.winfo_height() >= 200
        save_windows_screenshot(root, output / 'notiz.png')
        # Real atomic-save path: failed replacement preserves the old file and retries the draft.
        app.show_error = lambda *args, **kwargs: None
        app.save_items()
        old_bytes = Path(mod.SAVE_FILE).read_bytes()
        replace = mod.os.replace
        def deny_data_replace(source, destination):
            if Path(destination) == Path(mod.SAVE_FILE):
                raise PermissionError('Simulierter gesperrter Datenbestand')
            return replace(source, destination)
        mod.os.replace = deny_data_replace
        editor = app.rich_note_editor
        editor.text.insert('end-1c', '\nUnverlorener Entwurf')
        try:
            assert editor.flush() is False and app.dirty
            assert Path(mod.SAVE_FILE).read_bytes() == old_bytes
        finally:
            mod.os.replace = replace
        assert editor.flush() is True and not app.dirty
        saved = json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))
        assert 'Unverlorener Entwurf' in next(row for row in saved['lists'] if row['id'] == note['id'])['rich_note']['text']
        app._activate_system_view(app.HISTORY_VIEW)
        settle(root)
        save_windows_screenshot(root, output / 'verlauf.png')
        board_list = app.new_list_object('Pinnwandprüfung', [app.new_item(title) for title in
            ('Recherche zusammenfassen', 'Entwurf besprechen', 'Freigabe vorbereiten')])
        app.lists.append(board_list)
        app.set_active_list(board_list['id'])
        ws = app.workspace
        identities = [item['id'] for item in board_list['items']]
        ws.pin(identities);ws.set_mode('board')
        for identity, position in zip(identities, [(40,40),(380,80),(210,260)]):
            ws.store_position(identity, *position)
        ws.configure_board('connection_style','forward')
        ws.toggle_connection(identities[0], identities[1])
        ws.selected_ids = identities[:2]
        ws.configure_board('navigator', True)
        for zoom in (50, 100, 200):
            ws.configure_board('zoom', zoom)
            settle(root)
            save_windows_screenshot(root, output / f'pinnwand_{zoom}.png')
        preview = mod.BoardPreview(root, app.theme['card'], app.theme['input'], app.theme['muted'], app.theme['text'])
        preview_window = mod.tk.Toplevel(root)
        preview_window.geometry('450x190+10+10')
        preview.destroy()
        preview = mod.BoardPreview(preview_window, app.theme['card'], app.theme['input'], app.theme['muted'], app.theme['text'])
        preview.pack(fill='both', expand=True)
        app.settings['pinboards']['global'] = {'cards':[{'item_id':str(i),'x':(i%3)*316,'y':(i//3)*268} for i in range(205)], 'connections':[], 'layout':'free'}
        boxes, links, total = app.global_board_preview()
        preview.set_content(boxes, links)
        settle(preview_window)
        assert total == 205 and len(boxes) == 40
        save_windows_screenshot(preview_window, output / 'vorschau_205.png')
        preview_window.destroy()
        app.settings['home_tile_order'] = ['mascot', 'boardpreview', 'calendar']
        app._activate_system_view(app.HOME_VIEW)
        settle(root)
        def descendants(parent):
            for child in parent.winfo_children():
                yield child
                yield from descendants(child)
        def find_button(text):
            return next(widget for widget in descendants(app.home_content)
                        if isinstance(widget, mod.RoundedButton) and widget.text == text)
        mascot = next(widget for widget in descendants(app.home_content) if isinstance(widget, mod.MascotCanvas))
        find_button('Füttern').command()
        assert mascot.state_name == 'freut'
        assert any(isinstance(widget, mod.tk.Label) and widget.cget('text') == 'Danke für den kleinen Snack!'
                   for widget in descendants(app.home_content))
        save_windows_screenshot(root, output / 'startseite_gismo.png')
        find_button('Spielereien aus').command()
        settle(root)
        assert app.settings['mascot_playful'] is False
        assert not any(isinstance(widget, mod.RoundedButton) and widget.text == 'Füttern'
                       for widget in descendants(app.home_content))
        find_button('Spielereien an').command()
        settle(root)
        assert app.settings['mascot_playful'] is True
        assert not errors, errors
    finally:
        app.dirty = False
        app.on_close()
print(output)
