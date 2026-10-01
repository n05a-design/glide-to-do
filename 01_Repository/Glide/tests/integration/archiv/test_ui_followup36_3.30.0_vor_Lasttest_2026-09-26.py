"""Vorlagenbreite, Jahreswerte und die Bestandsübersicht mit isolierten Daten."""
import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import date, timedelta

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--screenshots', type=Path)
parser.add_argument('--layout-report', type=Path)
args = parser.parse_args()


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix='glide-ui-followup36-') as tmp:
    os.environ['GLIDE_DATA_DIR'] = tmp
    loader = importlib.machinery.SourceFileLoader('glide_followup', str(ROOT/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    if os.name == 'nt':
        root.attributes('-alpha', 0.0)  # Eigene Testfenster stören die laufende Arbeit nicht.
        root.attributes('-toolwindow', True)
    errors = []
    root.report_callback_exception = lambda *error: errors.append(error)
    app = mod.ListApp(root)
    app.show_info = lambda *a, **kw: None
    root.geometry('1280x960+10+10')
    root.deiconify()
    root.update()

    def settle():
        # Windows liefert Mapping und Größenänderungen asynchron. Erst den
        # stabilen Canvas-Inhalt prüfen, nicht eine gerade umgepackte Leiste.
        if root.state() != 'normal':
            root.deiconify()
        for _ in range(4):
            root.update()
            root.after(80, root.quit)
            root.mainloop()
        root.update()
        root.update_idletasks()

    def capture(name):
        if args.screenshots and os.name == 'nt':
            sys.path.insert(0, str(ROOT/'tests/tools'))
            from releasedaten import save_windows_screenshot
            save_windows_screenshot(root, args.screenshots.resolve()/f'{name}.png')

    def resize(width):
        for _ in range(5):
            root.deiconify()
            root.update()
            root.geometry(f'{width}x960+10+10')
            settle()
            if (root.state() == 'normal' and root.winfo_width() == width
                    and app.home_content.winfo_width() == app.home_canvas.winfo_width()
                    and bool(app.home_scrollbar.winfo_manager()) == bool(app.home_scrollbar.winfo_ismapped())):
                return
        raise AssertionError(('Fenstergröße nicht stabil', width, root.geometry(), root.state()))

    def button_text_fits(scope):
        for button in descendants(scope):
            if isinstance(button, mod.RoundedButton) and button.winfo_ismapped():
                for item in button.find_all():
                    if button.type(item) == 'text':
                        box = button.bbox(item)
                        assert 2 <= box[0] and box[2] <= button.winfo_width()-2, (button.text, box, button.winfo_width())

    layout_snapshots = []
    def check_library_cards(expected_columns=None):
        cards = app.library_cards
        for card in cards:
            # Tk aktualisiert eingebettete Frames erst beim Sichtbarwerden.
            # Deshalb echte sichtbare Inhalte prüfen, auch nach einem Resize.
            offset = card.winfo_rooty() - app.home_canvas.winfo_rooty() + app.home_canvas.canvasy(0)
            app.home_canvas.yview_moveto(offset / max(1, app.home_content.winfo_reqheight()))
            inner = card.inner
            # Nach Schriftwechsel und Resize ordnet Tk unter Last mitunter
            # mehrere Durchläufe nach. Gemessen wird der stabile Endzustand;
            # die Anforderung an die Abstände bleibt unverändert streng.
            # Seit 3.30 wartet derselbe Durchlauf auch auf die Sichtbarkeit der
            # Schaltflächen: Unter Last meldete eine frisch gescrollte Karte
            # „Liste öffnen“ einmal als noch nicht eingeblendet.
            kartenknoepfe = [w for w in descendants(card) if isinstance(w, mod.RoundedButton)]
            for _attempt in range(6):
                settle()
                x, y = card.winfo_rootx(), card.winfo_rooty()
                width, height = card.winfo_width(), card.winfo_height()
                insets = (inner.winfo_rootx() - x, inner.winfo_rooty() - y,
                          x + width - inner.winfo_rootx() - inner.winfo_width(),
                          y + height - inner.winfo_rooty() - inner.winfo_reqheight())
                if min(insets) >= 12 and max(insets) - min(insets) <= 2 and \
                        all(knopf.winfo_ismapped() for knopf in kartenknoepfe):
                    break
            assert x >= app.home_content.winfo_rootx()
            assert x + width <= app.home_content.winfo_rootx() + app.home_content.winfo_width()
            assert min(insets) >= 12 and max(insets) - min(insets) <= 2, ('Innenabstände', insets, (x, y, width, height))
            labels = [w.cget('text') for w in descendants(card) if isinstance(w, mod.tk.Label)]
            assert 'LISTE' not in labels and 'ORDNER' not in labels
            buttons = [w for w in descendants(card) if isinstance(w, mod.RoundedButton)]
            assert len(buttons) == 2
            for button in buttons:
                assert button.winfo_ismapped(), button.text
                assert button.winfo_rootx() >= x + insets[0]
                assert button.winfo_rootx()+button.winfo_width() <= x + width - insets[2]
                assert button.winfo_rooty()+button.winfo_height() <= y + height - insets[3]
            bottom = max(button.winfo_rooty()+button.winfo_height() for button in buttons)
            assert abs(y + height - bottom - insets[0]) <= 2, ('CTA-Abstand unten', insets, y+height-bottom)
            button_text_fits(card)
        app.home_canvas.yview_moveto(0)
        settle()
        columns = {}
        boxes = []
        for card in cards:
            x, y = card.winfo_rootx(), card.winfo_rooty()
            columns.setdefault(x, []).append(card)
            boxes.append((x, y, card.winfo_width(), card.winfo_height()))
        if expected_columns is not None:
            assert len(columns) == expected_columns, (root.winfo_width(), columns.keys())
        assert len({box[3] for box in boxes}) > 1, 'Unterschiedliche Inhalte benötigen unterschiedliche Höhen'
        for column in columns.values():
            ordered = sorted(column, key=lambda card: card.winfo_rooty())
            gaps = [after.winfo_rooty() - before.winfo_rooty() - before.winfo_height()
                    for before, after in zip(ordered, ordered[1:])]
            assert all(8 <= gap <= 20 for gap in gaps), ('Lücken in der Spalte', gaps)
            assert not gaps or max(gaps) - min(gaps) <= 1, gaps
        for index, (x, y, width, height) in enumerate(boxes):
            for other_x, other_y, other_width, other_height in boxes[index+1:]:
                assert (x+width <= other_x or other_x+other_width <= x
                        or y+height <= other_y or other_y+other_height <= y), 'Kacheln überlappen'
        # Auch ein per Tastatur erreichter CTA unterhalb des sichtbaren
        # Bereichs muss vollständig in den Ausschnitt gescrollt werden.
        last_card = max(cards, key=lambda card: card.winfo_rooty()+card.winfo_height())
        last_button = [w for w in descendants(last_card) if isinstance(w, mod.RoundedButton)][-1]
        last_button.event_generate('<FocusIn>')
        settle()
        assert last_button.winfo_rooty() >= app.home_canvas.winfo_rooty()
        assert last_button.winfo_rooty()+last_button.winfo_height() <= app.home_canvas.winfo_rooty()+app.home_canvas.winfo_height()
        app.home_canvas.yview_moveto(0)
        settle()
        layout_snapshots.append({'theme':app.theme_name, 'font':app.settings.get('ui_font_size'),
                                 'window_width':root.winfo_width(), 'columns':len(columns), 'cards':boxes})

    try:
        # Alte Erledigungen verschwanden nach der ersten neuen Bearbeitung.
        today = date.today()
        older = (today-timedelta(days=2)).isoformat()
        yesterday = (today-timedelta(days=1)).isoformat()
        histories = {'completion_history': {older: 2, yesterday: 1}, 'activity_history': {today.isoformat(): 4}}
        app.settings.update(copy.deepcopy(histories))
        assert app.yearly_activity_history() == {older: 2, yesterday: 1, today.isoformat(): 4}
        assert mod.YearHeatmap.statistics(app.yearly_activity_history())['total'] == 7
        app.settings['activity_history'][yesterday] = 3
        assert app.yearly_activity_history()[yesterday] == 3  # keine Addition derselben Erledigung
        app.settings['completion_history'][yesterday] = 5
        assert app.yearly_activity_history()[yesterday] == 5  # ältere Mindestzahl bleibt erhalten
        app.settings.update(copy.deepcopy(histories))
        app.save_settings()
        app.settings = app.load_settings()
        assert all(app.settings[key] == values for key, values in histories.items())
        assert app.yearly_activity_history()[older] == 2

        for theme in ('dark', 'light'):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            for editing in (False, True):
                app._templates_editing = editing
                app.set_template_view()
                for width in (860, 1280, 1660):
                    resize(width)
                    assert root.state() == 'normal', root.state()
                    assert root.winfo_width() == width, (root.geometry(), width)
                    assert app.home_frame.winfo_width() == app.content_frame.winfo_width()
                    assert not any(isinstance(w, mod.tk.Label) for w in app.home_content.winfo_children())
                    if not app.home_scrollbar.winfo_manager():
                        assert app.template_cards[0].winfo_width() == app.content_frame.winfo_width(), (theme, editing, width, app.template_cards[0].winfo_width(), app.content_frame.winfo_width(), app.home_canvas.winfo_width(), app.home_canvas.yview(), app.home_scrollbar.winfo_manager())
                    for card, row in zip(app.template_cards, app.template_rows):
                        assert isinstance(card, mod.RoundedContainer) and card.radius == app.HOME_CARD_RADIUS
                        panel, title, note, actions = row
                        assert actions.winfo_x()+actions.winfo_width() <= panel.winfo_width()
                        if int(note.grid_info()['row']) == 0:
                            assert note.winfo_x() < 290, note.winfo_x()
                            assert 0 <= note.winfo_x() - title.winfo_x() - title.winfo_width() <= 20
                    assert len(app.template_action_groups) == 2
                    for group in app.template_action_groups:
                        assert isinstance(group, mod.RoundedContainer)
                        assert group.fill_color == app.theme['card'] and group.radius == 16
                        assert len([w for w in group.inner.winfo_children() if isinstance(w, mod.RoundedButton)]) == 2
                        assert group.winfo_rootx()+group.winfo_width() <= app.content_frame.winfo_rootx()+app.content_frame.winfo_width(), (theme, editing, width, root.geometry(), group.winfo_x(), group.winfo_width(), app.content_frame.winfo_width(), root.state())
                    button_text_fits(app.home_content)
                    button_text_fits(app.template_actions)
                    capture(f'vorlagen-{theme}-{width}-' + ('bearbeiten' if editing else 'ansehen'))

            app.set_home_view()
            for width in (860, 1280, 1660):
                resize(width)
                app.home_canvas.yview_moveto(1)
                root.update()
                heatmap = next(w for w in descendants(app.home_content) if isinstance(w, mod.YearHeatmap))
                chart = next(w for w in descendants(app.home_content) if isinstance(w, mod.CompletionChart))
                assert heatmap.winfo_width() == chart.winfo_width()
                cells = heatmap.find_withtag('day')
                line = next(item for item in chart.find_all() if chart.type(item) == 'line')
                plot = chart.coords(line)
                assert abs(min(heatmap.coords(item)[0] for item in cells)-plot[0]) <= 1
                assert abs(max(heatmap.coords(item)[2] for item in cells)-plot[2]) <= 1
                for item in heatmap.find_all():
                    if heatmap.type(item) != 'text':
                        continue
                    weekday = {'Mo': 0, 'Do': 3, 'So': 6}[heatmap.itemcget(item, 'text')]
                    matching = next(cell for cell in cells if date.fromisoformat(heatmap.gettags(cell)[1]).weekday() == weekday)
                    box = heatmap.coords(matching)
                    assert abs(heatmap.coords(item)[1]-(box[1]+box[3])/2) <= 1
                assert heatmap.bbox('all')[3] < heatmap.winfo_height()
                for day in (older, yesterday, today.isoformat()):
                    assert heatmap.find_withtag(day)
                    assert heatmap.itemcget(heatmap.find_withtag(day)[0], 'fill') != heatmap.empty_color
                capture(f'jahresanzeige-{theme}-{width}')

        # Grenzfall: Die Scrollleiste macht das Raster schmaler und damit
        # niedriger. Ein Pixel Überlauf darf kein endloses Umräumen auslösen.
        app.set_home_view()
        resize(1280)
        for widget in app.home_content.winfo_children():
            widget.destroy()
        spacer = mod.tk.Frame(app.home_content, height=1)
        spacer.pack(fill='x')
        boundary_heatmap = mod.YearHeatmap(app.home_content, {})
        boundary_heatmap.pack(fill='x')
        settle()
        changes = []
        def observe_resize(event):
            changes.append(event.width)
            if len(changes) > 20:
                spacer.configure(height=1)  # Test bricht eine Regression kontrolliert ab.
        binding = app.home_canvas.bind('<Configure>', observe_resize, add='+')
        spacer.configure(height=app.home_canvas.winfo_height()-boundary_heatmap.winfo_reqheight()+1)
        settle()
        app.home_canvas.unbind('<Configure>', binding)
        assert len(changes) <= 20, ('Scrollleiste pendelt zwischen zwei Breiten', changes)
        app.refresh_home()

        # Ohne normale Listen/Ordner darf der Hinweis an den Spaltengrenzen
        # weder beschnitten werden noch die unteren Aktionen verdecken.
        saved_lists, saved_folders = app.lists, app.folders
        app.lists = [entry for entry in app.lists if app.is_inbox_list(entry)]
        app.folders = []
        app.set_library_view()
        for width in (860, 1050, 1280, 1660):
            resize(width)
            assert not app.library_cards
            hint = next(w for w in descendants(app.home_content)
                        if isinstance(w, mod.tk.Label) and w.cget('text').startswith('Noch keine Listen'))
            assert hint.winfo_ismapped()
            assert hint.winfo_reqheight() <= hint.winfo_height()
            assert int(hint.cget('wraplength')) <= hint.winfo_width()
            assert hint.winfo_rootx()+hint.winfo_width() <= app.home_content.winfo_rootx()+app.home_content.winfo_width()
            assert app.template_actions.winfo_ismapped()
        app.lists, app.folders = saved_lists, saved_folders

        # Ein gemeinsamer Bestand mit Wurzellisten, verschachtelten und leeren Ordnern.
        folder = app.new_folder_object('Projekte', color='clear')
        nested = app.new_folder_object('Redesign und Branding', color='accent', parent_id=folder['id'])
        empty = app.new_folder_object('Ideen für später', color='import')
        app.folders.extend((folder, nested, empty))
        titles = ('Planung', 'Recherche', 'Gestaltung', 'Freigabe', 'Veröffentlichung', 'Rückblick',
                  'Haushalt', 'Einkauf', 'Reiseplanung', 'Wochenplanung')
        for index, title in enumerate(titles):
            tasks = [app.new_item('Nächste Schritte festlegen'), app.new_item('Informationen zusammenstellen'),
                     app.new_item('Erstes Ergebnis prüfen', done=True)]
            app.lists.append(app.new_list_object(title, tasks,
                folder_id=nested['id'] if index < 3 else folder['id'] if index < 6 else None,
                color=app.LIST_COLOR_KEYS[index % len(app.LIST_COLOR_KEYS)],
                note='Ein gemeinsamer Platz für Aufgaben, Notizen und nächste Schritte.'))
        app.lists.append(app.new_list_object('Kurz', []))
        long_label = app.new_label_object('Freigabe mit Eigentümer abstimmen', None, 'accent')
        app.labels.append(long_label)
        app.lists.append(app.new_list_object(
            'Immobilienvermarktung – umfangreiche Unterlagen, Bildauswahl und Freigaben für mehrere Beteiligte',
            [app.new_item('Vollständige Bildauswahl und Beschreibung mit dem Eigentümer abstimmen',
                          due=(today+timedelta(days=3)).isoformat()),
             app.new_item('Veröffentlichung auf den vereinbarten Kanälen vorbereiten'),
             app.new_item('Ansprechpartner und nächste Schritte für Rückfragen dokumentieren')],
            note='Alle benötigten Unterlagen zusammenstellen und vor der Veröffentlichung prüfen. ' * 3,
            labels=[long_label['id']]))
        app.save_items()
        expected = {('folder', entry['id']) for entry in app.folders}
        expected |= {('list', entry['id']) for entry in app.lists if not app.is_inbox_list(entry)}
        data_before = copy.deepcopy((app.lists, app.folders))
        for theme in ('dark', 'light'):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            app.sidebar_title.event_generate('<Button-1>')
            root.update()
            assert app.view_mode == app.LIBRARY_VIEW
            assert app.get_active_page() is None
            assert not app.require_list_view(message=False)
            assert not app.system_listbox.selection() and not app.sidebar_listbox.selection()
            assert app.sidebar_heading_icon.cget('text') == app.ICONS['list']
            assert app.sidebar_title.cget('bg') == app.theme['selection']
            assert set(app.library_open_buttons) == expected
            assert len(app.library_cards) == len(expected)
            assert ('folder', nested['id']) in [(kind, entry['id']) for kind, entry in app.library_entries()]
            for width, expected_columns in ((860, 1), (1280, 2), (1660, 3)):
                resize(width)
                check_library_cards(expected_columns)
                button_text_fits(app.template_actions)
                capture(f'listen-ordner-{theme}-{width}')
                app.home_canvas.yview_moveto(1)
                root.update()
                assert app.home_canvas.yview()[0] > 0
                assert app.template_actions.winfo_ismapped()
                assert app.template_actions.winfo_rooty()+app.template_actions.winfo_height() < root.winfo_rooty()+root.winfo_height()
                app.home_canvas.yview_moveto(0)
            old_font_size = app.settings.get('ui_font_size', 'mittel')
            for font_size in ('klein', 'gross'):
                app.settings['ui_font_size'] = font_size
                app.apply_ui_font()
                app.refresh_library_page()
                for width in (860, 1380, 1660):
                    resize(width)
                    check_library_cards()
            app.settings['ui_font_size'] = old_font_size
            app.apply_ui_font()
            app.refresh_library_page()
            assert (app.lists, app.folders) == data_before

        # Kachelziele und Rückkehr wechseln nur die Ansicht, nie den Bestand.
        for kind, entry in app.library_entries():
            app.set_library_view()
            app.library_open_buttons[(kind, entry['id'])].command()
            root.update()
            assert app.view_mode == kind
            assert (app.active_folder_id if kind == 'folder' else app.active_list_id) == entry['id']
        app.set_active_folder(folder['id'])
        app.save_items()  # Aufgabenablage merkt den Ordner, Einstellungen danach die Übersicht.
        app.set_library_view()
        app.settings['startup_view'] = 'last'
        app.save_settings()
        app.load_items()
        root.update()
        assert app.view_mode == app.LIBRARY_VIEW
        assert (app.lists, app.folders) == data_before
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()
        root = mod.tk.Tk()
        root.withdraw()
        if os.name == 'nt':
            root.attributes('-alpha', 0.0)
            root.attributes('-toolwindow', True)
        root.report_callback_exception = lambda *error: errors.append(error)
        app = mod.ListApp(root)
        root.deiconify()
        settle()
        assert app.view_mode == app.LIBRARY_VIEW
        assert set(app.library_open_buttons) == expected
        assert (app.lists, app.folders) == data_before
        assert not errors, errors
        if args.layout_report:
            args.layout_report.parent.mkdir(parents=True, exist_ok=True)
            args.layout_report.write_text(json.dumps(layout_snapshots, ensure_ascii=False, indent=2)+'\n')
        print('UI-Nachtrag: OK; Vorlagen in 2 Modi/2 Themes/3 Breiten; Tageshistorien erhalten, keine Doppelzählung; Diagrammachsen und Breiten; alle Ordner/Listen, Kachelziele, Scrollen, Rückkehr, Daten unverändert.')
    finally:
        if errors:
            print('Tk-Fehler:', errors)
        app.cancel_pending_callbacks()
        app.release_data_lock()
        if root.winfo_exists():
            root.destroy()
