"""Regressionen aus den 14 UI-Rückmeldungen; ausschließlich isolierte Daten.

Prüft echte Widgetgeometrie, Theme-Wechsel, Hover, Navigation und Hauptphasen.
Optional --screenshots ORDNER erfasst nur die eigenen Windows-Testfenster.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from datetime import date, datetime, timedelta, timezone

ROOT = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--screenshots', type=Path)
args = parser.parse_args()

def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

with tempfile.TemporaryDirectory(prefix='glide-ui-polish36-') as tmp:
    os.environ['GLIDE_DATA_DIR'] = tmp
    loader = importlib.machinery.SourceFileLoader('glide_ui_polish', str(ROOT/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    errors = []
    root.report_callback_exception = lambda *error: errors.append(error)
    app = mod.ListApp(root)
    app.show_info = lambda *a, **kw: None
    app.ask_yes_no = lambda *a, **kw: True
    root.geometry('1280x960+10+10')
    root.deiconify()
    root.update()

    def capture(widget, name):
        if args.screenshots and os.name == 'nt':
            sys.path.insert(0, str(ROOT/'tests/tools'))
            from releasedaten import save_windows_screenshot
            widget.update()
            save_windows_screenshot(widget, args.screenshots.resolve()/f'{name}.png')

    def button_text_fits(scope):
        for widget in descendants(scope):
            if isinstance(widget, mod.RoundedButton) and widget.winfo_ismapped():
                for item in widget.find_all():
                    if widget.type(item) != 'text':
                        continue
                    bounds = widget.bbox(item)
                    assert bounds[0] >= 3 and bounds[2] <= widget.winfo_width()-3, (widget.text, bounds, widget.winfo_width())
                    assert bounds[1] >= 1 and bounds[3] <= widget.winfo_height()-1, (widget.text, bounds, widget.winfo_height())

    try:
        # Auswahlen folgen jeder Akzentfarbe; gespeicherte Farbnamen bleiben stabil.
        for name in ('light', 'dark'):
            app.set_design(name, apply_now=False)
            for accent in app.LIST_COLOR_KEYS:
                app.settings['accent_color'] = accent
                theme = app.active_theme()
                # Punkt 19 (3.23.0): Die Auswahl trägt die gewählte
                # Akzentfarbe, wird aber so weit nachgezogen, dass ihre
                # Schrift messbar lesbar bleibt. Geprüft wird deshalb der
                # Kontrast, nicht mehr die pixelgenaue Gleichheit.
                assert theme['selection'] == mod.ensure_contrast(theme[accent], theme['selection_text'])
                assert mod.contrast_ratio(theme['selection_text'], theme['selection']) >= 4.5
                assert theme['accent'] == app.THEMES[name]['accent']
                assert app.theme_name == name
                kinds = [app.ITEM_KIND_TASK, app.ITEM_KIND_GROUP, app.ITEM_KIND_LONG, app.ITEM_KIND_HEADING]
                assert len({theme[app.kind_color_key(kind)] for kind in kinds}) == 4
        app.settings['accent_color'] = 'accent'
        app.settings['profile_logo'] = 'TvT'
        app.settings['activity_history'] = {date.today().isoformat(): 7}
        entry = app.new_list_object('Lange Beispiel-Liste für vollständig sichtbare Startseitenaktionen und Zeilenumbrüche',
                                    [app.new_item('Heute prüfen', due=date.today().isoformat())])
        app.lists.append(entry)
        app.set_active_list(entry['id'])
        app.templates[0]['note'] = 'Diese ausführliche Beschreibung bleibt auch bei einem schmalen Fenster vollständig und linksbündig lesbar.'
        app._templates_editing = True
        for name in ('dark', 'light'):
            app.set_design(name, apply_now=False)
            app.apply_theme()
            app.set_template_view()
            for width in (860, 1280):
                root.geometry(f'{width}x960+10+10')
                root.update()
                app.home_canvas.yview_moveto(0)
                button_text_fits(app.template_actions)
                assert app.template_actions.winfo_ismapped()
                assert app.template_actions.winfo_rooty()+app.template_actions.winfo_height() < root.winfo_rooty()+root.winfo_height()
                for surface in (app.home_frame, app.home_canvas, app.home_content):
                    assert surface.cget('bg') == app.theme['bg']
                for card, title, note, actions in app.template_rows:
                    assert title.cget('anchor') == note.cget('anchor') == 'w'
                    assert note.cget('justify') == 'left'
                    assert actions.winfo_x()+actions.winfo_width() <= card.winfo_width()
                    assert title.winfo_x()+title.winfo_width() <= actions.winfo_x()
                    for button in descendants(actions):
                        if isinstance(button, mod.RoundedButton):
                            assert button.bg_color == card.cget('bg')
                    button_text_fits(actions)
                capture(root, f'vorlagen-{name}-{width}')
            # Wechsel ohne Zwischenbesuch auf der Startseite reproduziert den alten schwarzen Hintergrund.
            # Gegenstück über das Design wählen (W02): theme_name allein wirkt nicht.
            app.set_design('light' if name == 'dark' else 'dark', apply_now=False)
            app.apply_theme()
            assert (mod.relative_luminance(app.theme['bg']) < 0.2) == (name != 'dark'), app.theme['bg']
            root.update()
            assert app.home_canvas.cget('bg') == app.theme['bg']
            app.set_design(name, apply_now=False)
            app.apply_theme()
            app.set_home_tile_hidden('welcome', False)  # Seit D12 (3.33.2) nicht mehr im Standard: die geprüfte Kachel ausdrücklich einblenden.
            app.set_home_tile_hidden('stats', False)
            app.set_home_view()
            for width in (860, 1280):
                root.geometry(f'{width}x960+10+10')
                root.update()
                app.home_canvas.yview_moveto(0)
                visible = [key for button, key in app.home_quick_actions.entries if button.winfo_ismapped()]
                # Seit 3.22 führt eine Zeile zum Tag; dafür kam „Startseite
                # einrichten“ in den Schnellzugriff.
                # Punkt 12 (3.24.0): Der Schnellzugriff führt zusätzlich auf
                # die globale Pinnwand.
                # Punkt 3 (4. Startseite, 3.25.0): Vier Wege stehen als Fläche
                # da, alles Weitere hinter „Weitere …“. Bei 860 bleibt der
                # Eingang und die Sammelfläche.
                assert visible == (['today', 'more'] if width == 860 else
                                   ['today', 'progress', 'inbox', 'board', 'more']), visible
                button_text_fits(app.home_content)
                assert not any(isinstance(w, mod.tk.Button) for w in descendants(app.home_content))
                assert app._home_summary['due_lists']
                capture(root, f'startseite-{name}-{width}')
            app.home_canvas.yview_moveto(1)
            root.update()
            heatmap = next(w for w in descendants(root) if isinstance(w, mod.YearHeatmap))
            assert heatmap.bbox('all')[3] < heatmap.winfo_height(), (heatmap.bbox('all'), heatmap.winfo_height())
            capture(root, f'jahresanzeige-{name}')

            def settings_check(dialog, parent=None):
                dialog.update()
                entries = [w for w in descendants(dialog) if isinstance(w, mod.tk.Entry)]
                assert entries[-1].winfo_rootx() > entries[0].winfo_rootx()+300
                button_text_fits(dialog)
                capture(dialog, f'einstellungen-{name}')
                dialog.destroy()
            app.run_modal = settings_check
            app.show_settings_dialog()

            def labels_check(dialog, parent=None):
                # Die Auswahl schließt sich bei Fokusverlust – das ist gewollt
                # und wird über root.focus_get() entschieden. Im
                # automatisierten Lauf hat das Fenster unter Windows aber
                # keinen Systemfokus, weil die Konsole im Vordergrund steht;
                # focus_get() liefert dann None, und die Auswahl klappte
                # zwischen Öffnen und Prüfen wieder zu. Ohne erzwungenen Fokus
                # prüft dieser Abschnitt nicht die Auswahl, sondern die
                # Fensterverwaltung der Prüfmaschine.
                dialog.focus_force()
                dialog.update()
                dropdown = next(w for w in descendants(dialog) if isinstance(w, mod.LabelDropdown))
                dropdown._open_popup()
                dialog.update()
                popup = dropdown._popup
                assert popup is not None, (
                    'Labelauswahl hat sich sofort wieder geschlossen; '
                    f'Fokus liegt auf {app.current_focus_widget()!r}')
                buttons = [w for w in descendants(popup) if isinstance(w, mod.RoundedButton)]
                assert {w.text for w in buttons} == {'Fertig', '+ Neues Label'}
                first_row = next(iter(dropdown._rows.values()))
                for button in buttons:
                    assert button.winfo_rooty() > first_row['frame'].winfo_rooty()+first_row['frame'].winfo_height()
                key = next(iter(dropdown._rows))
                dropdown._paint_row(key, hover=True)
                assert first_row['frame'].cget('bg') == app.theme['hover']
                fill = first_row['chip'].fill
                dropdown.toggle_label(key)
                assert first_row['chip'].fill == fill
                assert first_row['mark'].fill == app.theme['selection']
                button_text_fits(popup)
                capture(popup, f'labels-{name}')
                dropdown._close_popup()
                dialog.destroy()
            app.run_modal = labels_check
            app.item_form_dialog(mode='add')

        # Kompakte Symbolspalte bleibt bedienbar, inklusive Auswahl und Hover.
        app.set_home_view()
        root.update()
        tree = app.system_listbox
        target = next(i for i in tree.get_children() if tree.set(i, 'title').strip() == 'Vorlagen')
        x, y, width, height = tree.bbox(target, 'icon')
        tree.icon_canvas.event_generate('<ButtonPress-1>', x=10, y=y+height//2)
        tree.icon_canvas.event_generate('<ButtonRelease-1>', x=10, y=y+height//2)
        root.update()
        assert app.view_mode == app.TEMPLATE_VIEW
        drawn = [item for item in tree.icon_canvas.find_all() if tree.icon_canvas.type(item) == 'text']
        # Startseite, Mein Tag, Labels, Vorlagen, Papierkorb – seit dem
        # 26.09.2026: „In Bearbeitung“ ist ein Abschnitt in „Mein Tag“, der
        # Verlauf ein Knopf in der Kopfzeile; seit dem 27.09.2026 hat „Seiten“
        # einen eigenen Bereich über den Listen.
        assert len(drawn) == 5
        # Das Symbol der angeklickten Zeile sitzt auf deren Zeilenmitte; der
        # Index folgt der Baumreihenfolge, damit eine Umsortierung der
        # Navigation den Test nicht zufällig richtig oder falsch macht.
        stelle = tree.get_children().index(target)
        assert tree.icon_canvas.coords(drawn[stelle])[1] == y+height/2-2
        sample = next(w for w in descendants(app.template_actions) if isinstance(w, mod.RoundedButton))
        sample.event_generate('<Enter>')
        root.update()
        assert sample.is_hovered and sample.itemcget(sample.find_all()[0], 'fill') == sample.hover_fill
        capture(root, 'vorlagen-hover')
        sample.event_generate('<Leave>')

        # Unabhängige 50 USNO-Referenzereignisse, offline lesbares Original-JSON.
        reference = json.loads((ROOT/'tests/fixtures/mondphasen-usno-2026.json').read_text(encoding='utf-8'))
        computed = mod.calendar_moon_phases(date(2026,1,1), date(2026,12,31), timezone.utc)
        assert len(computed) == reference['data']['numphases'] == 50
        differences = []
        for phase in reference['data']['phasedata']:
            day = date(phase['year'], phase['month'], phase['day'])
            instant = datetime.fromisoformat(f"{day}T{phase['time']}:00+00:00")
            actual = computed[day]
            difference = abs((actual['utc']-instant).total_seconds())/60
            differences.append(difference)
            assert difference < 20, (day, difference)
        shifted = mod.calendar_moon_phases(date(2026,6,29), date(2026,6,30), timezone(timedelta(hours=2)))
        assert date(2026,6,30) in shifted and shifted[date(2026,6,30)]['name'] == 'Vollmond'

        app._calendar_mode = 'month'
        app.open_calendar_view()
        for _ in range(3):
            root.update_idletasks(); root.update()
        assert app.home_mode() == 'calendar' and root.grab_current() is None
        markers = [w for w in descendants(app.home_content) if hasattr(w, 'moon_day')]
        assert markers
        for marker in markers:
            cell = marker.master
            assert marker.winfo_y() >= cell.winfo_height()-marker.winfo_height()-8
        button_text_fits(app.home_content)
        capture(root, 'kalender-hauptphasen')
        assert not errors, errors
        print(f'UI-Nachbesserung: OK; Hell/Dunkel, 860/1280, Vorlagenaktionen, Hover, Einstellungen, Auswahlfarben, Symbolnavigation. 50 USNO-Phasen: max. {max(differences):.1f} Minuten Abweichung.')
    finally:
        app.release_data_lock()
        root.destroy()
