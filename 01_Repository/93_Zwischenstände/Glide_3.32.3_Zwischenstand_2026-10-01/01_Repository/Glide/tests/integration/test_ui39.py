"""3.9: reale Dropdown-Ereignisse, Dialoggeometrie, Aktionsparität und Persistenz."""
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import tempfile
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]

def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

with tempfile.TemporaryDirectory(prefix='glide-ui39-') as temp:
    os.environ['GLIDE_DATA_DIR'] = temp
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_ui39', str(REPO/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *error: errors.append(error)
    app = mod.ListApp(root)
    app.show_info = lambda *a, **kw: None
    root.geometry('1280x940+10+10')
    root.deiconify(); root.lift(); root.focus_force(); root.update()
    try:
        original = copy.deepcopy(app.lists)
        for theme in ('light', 'dark'):
            app.set_design(theme, apply_now=False); app.apply_theme(); root.update()
            app.settings['sidebar_visible'] = True; app._apply_sidebar_visibility(); root.update()
            before = app.content_frame.winfo_width()
            app.toggle_sidebar(); root.update()
            assert not app.sidebar_shell.winfo_ismapped()
            assert app.content_frame.winfo_width() > before + 200
            assert app.content_frame.winfo_rootx() == app.main_area.winfo_rootx()
            assert json.loads(Path(mod.SETTINGS_FILE).read_text())['sidebar_visible'] is False
            app.toggle_sidebar(); root.update()
            assert app.sidebar_shell.winfo_ismapped()
            assert app.content_frame.winfo_width() == before
            assert abs(app.notifications_button.winfo_rooty()-app.settings_button.winfo_rooty()) <= 1
            assert not app.reminder_status.winfo_ismapped()
            app.set_template_view(); root.update()
            for card, title, note, actions in app.template_rows:
                assert actions.winfo_y() >= 7
                assert card.winfo_height() - actions.winfo_y() - actions.winfo_height() >= 7
            owner = mod.tk.Toplevel(root)
            owner.geometry('620x600+20+20'); owner.update(); owner.grab_set()
            value = mod.tk.StringVar(value='Erste Option')
            values = ['Erste Option', 'Zweite Option'] + [f'Eintrag {i}' for i in range(40)]
            border, field = app._make_option_menu(owner, value, values, {'Zweite Option': 'confirm'})
            border.pack(fill='x', padx=20, pady=15)
            outside = mod.tk.Entry(owner)
            outside.pack(fill='x', padx=20, pady=20, before=border)
            # Stoppende Widgetbindungen dürfen die Schließlogik nicht verhindern.
            outside.bind('<ButtonPress-1>', lambda e: 'break')
            owner.lift(); owner.focus_force(); owner.update()
            top_count = sum(isinstance(w, mod.tk.Toplevel) for w in descendants(root))
            for index in range(15):
                owner.lift(); owner.focus_force(); owner.update_idletasks()
                field._open_popup(); owner.update()
                popup = field._popup
                assert isinstance(popup, mod.DropdownPopup)
                assert root.grab_current() is owner
                assert sum(isinstance(w, mod.tk.Toplevel) for w in descendants(root)) == top_count
                assert popup.winfo_rootx() >= owner.winfo_rootx()
                assert popup.winfo_rooty() + popup.winfo_height() <= owner.winfo_rooty() + owner.winfo_height()
                # Entry kann vom Popup verdeckt sein: Klick in den freien Außenrand.
                outside.event_generate('<ButtonPress-1>', x=2, y=2); owner.update()
                assert field._popup is None and value.get() == 'Erste Option'
                assert root.grab_current() is owner
                assert not any('GlideDropdown' in tag for tag in outside.bindtags())
            field._open_popup(); owner.update()
            field._choices.event_generate('<Down>'); owner.update()
            assert value.get() == 'Erste Option'
            field._choices.event_generate('<Return>'); owner.update()
            assert value.get() == 'Zweite Option' and field._popup is None
            field._open_popup(); owner.update()
            field._choices.event_generate('<Escape>'); owner.update()
            assert field._popup is None and owner.winfo_exists()
            field._open_popup(); owner.update()
            outside.configure(takefocus=False)
            field._choices.event_generate('<Tab>'); owner.update()
            assert field._popup is None and owner.winfo_exists()
            picker = mod.LabelDropdown(owner, app, app.labels, allow_create=True, dialog_parent=owner)
            picker.pack(fill='x', padx=20); owner.update()
            picker._open_popup(); owner.update()
            picker._popup.event_generate('<Tab>'); owner.update()
            assert picker._popup is None and owner.winfo_exists()
            picker._open_popup(); owner.update()
            assert isinstance(picker._popup, mod.DropdownPopup)
            assert root.grab_current() is owner
            picker._popup.event_generate('<space>'); owner.update()
            assert len(picker.read()) == 1
            picker._popup.event_generate('<Escape>'); owner.update()
            assert picker._popup is None and root.grab_current() is owner
            field._open_popup(); owner.update()
            with patch.object(app, 'current_focus_widget', return_value=None):
                field._popup._check_focus()
            assert field._popup is None
            field._open_popup(); owner.update()
            border.destroy(); owner.update()
            assert root.grab_current() is owner and not getattr(app, '_active_dropdown', None)
            picker._open_popup(); owner.update()
            owner.destroy(); root.update()
            assert root.grab_current() is None
            assert not getattr(app, '_active_dropdown', None)

            for screen_height in (720, 1400):
                def container(dialog, parent=None):
                    dialog.update()
                    widgets = list(descendants(dialog))
                    assert len([w for w in widgets if isinstance(w, mod.LabelDropdown)]) == 1
                    for widget in widgets:
                        if isinstance(widget, (mod.tk.Entry, mod.tk.Text)):
                            assert int(widget.cget('highlightthickness')) == 0
                            assert int(widget.cget('bd')) == 0
                            assert widget.winfo_rooty()+widget.winfo_height() < dialog.winfo_rooty()+dialog.winfo_height()-45
                    buttons = [w for w in widgets if isinstance(w, mod.RoundedButton)]
                    assert all(w.winfo_ismapped() for w in buttons)
                    assert dialog.winfo_height() <= int(screen_height*app.DIALOG_MAX_SCREEN_SHARE)
                    if screen_height == 720:
                        assert dialog.winfo_width() >= 860
                    dialog.destroy()
                with patch.object(mod.tk.Toplevel, 'winfo_screenheight', return_value=screen_height), patch.object(app, 'run_modal', container):
                    app.create_container_dialog()

            # Punkt 3 (3.23.0): eine Designauswahl statt Hell/Dunkel plus
            # Farbmodus plus Materialoptik-Häkchen.
            ziel_design = 'light' if theme == 'dark' else 'dark'
            def settings(dialog, parent=None):
                fields = [w for w in descendants(dialog) if isinstance(w, mod.AppOptionMenu)]
                design = next(w for w in fields
                              if w.options == [app.DESIGNS[k]['name'] for k in app.DESIGN_ORDER])
                design.variable.set(app.DESIGNS[ziel_design]['name'])
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton) and w.text == 'Speichern').command()
            with patch.object(app, 'run_modal', settings):
                app.show_settings_dialog()
            assert app.design_name() == ziel_design
            assert app.theme_name == ('light' if theme == 'dark' else 'dark')
            gespeichert = json.loads(Path(mod.SETTINGS_FILE).read_text())
            assert gespeichert['design'] == ziel_design
            assert gespeichert['theme'] == app.theme_name
            # Die abgeleiteten Werte bleiben für ältere Fassungen mitgeschrieben.
            assert gespeichert['color_mode'] == 'standard' and gespeichert['glass_mode'] is False

        entries = app.app_action_entries()
        assert len(entries) >= 50
        assert {'Datei','Bearbeiten','Ansicht','Hilfe'} == {a['category'] for a in entries}
        for label in ('Als CSV …','Komplettbackup laden …','Gruppe auflösen','Nach Wichtigkeit','Tastenkürzel anzeigen'):
            assert any(a['label'] == label for a in entries)
        text = mod.tk.Entry(root)
        text.pack(); text.insert(0,'Auswahl kopieren'); text.selection_range(0,7); text.focus_force(); root.update()
        app.invoke_app_action(next(a for a in entries if a['label']=='Kopieren'), text)
        assert root.clipboard_get() == 'Auswahl'
        text.destroy()
        # Seit 3.22 gliedert der Dialog die Aktionen in Gruppen. Überschriften
        # und Leerzeilen sind eigene Zeilen des Baums und zählen nicht mit.
        def aktionszeilen(tree):
            return [row for row in tree.get_children()
                    if not row.startswith((mod.ListApp.ACTION_GROUP_ROW_PREFIX,
                                           mod.ListApp.ACTION_SPACER_ROW_PREFIX))]

        def gruppenzeilen(tree):
            return [row for row in tree.get_children()
                    if row.startswith(mod.ListApp.ACTION_GROUP_ROW_PREFIX)]

        def actions(dialog, parent=None):
            dialog.update()
            tree = next(w for w in descendants(dialog) if w.winfo_name() == 'actions_tree')
            assert len(aktionszeilen(tree)) == len(entries)
            assert len(gruppenzeilen(tree)) >= 5
            # Vor jeder Gruppe außer der ersten steht genau eine Leerzeile.
            assert len([row for row in tree.get_children()
                        if row.startswith(mod.ListApp.ACTION_SPACER_ROW_PREFIX)]) == len(gruppenzeilen(tree)) - 1
            # Die Auswahl steht auf einer echten Aktion, nicht auf einer Überschrift.
            assert tree.selection() and tree.selection()[0] in aktionszeilen(tree)
            search = next(w for w in descendants(dialog) if w.winfo_name() == 'action_search')
            search.insert(0,'CSV'); dialog.update()
            # Seit 3.18 trägt auch der Import CSV im Namen; die Suche filtert
            # auf genau die Einträge, die den Begriff führen.
            csv_entries = [a for a in entries if 'csv' in a['label'].lower()]
            assert len(csv_entries) >= 2, csv_entries
            assert len(aktionszeilen(tree)) == len(csv_entries)
            dialog.destroy()
        with patch.object(app, 'run_modal', actions):
            app.show_actions_dialog()
        assert original == app.lists
        assert not errors, errors
        print('UI 3.9: OK (beide Themes, eingebettete Dropdowns, Außerklick, Tastatur, Grabs, Geometrie, Aktionen, Speicherung)')
    finally:
        app.cancel_pending_callbacks(); app.release_data_lock(); root.destroy()
