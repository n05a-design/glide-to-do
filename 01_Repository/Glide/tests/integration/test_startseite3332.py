"""3.33.2: Startseite „Ruhig“ (D12), eigene Auswahl, Zurücksetzen und Aufbaukosten über echte Wege."""
import importlib.machinery
import importlib.util
import os
import copy
import json
import sys
import time
from datetime import date, timedelta
from pathlib import Path
import tempfile
from unittest.mock import patch

repo = Path(__file__).resolve().parents[2]
# D12, seit B04 (15.10.2026) mit „Galeriebilder“ als achter Standardkachel.
D12 = ['mascot', 'today', 'week', 'recent', 'boardpreview', 'drawings', 'gallery', 'pinned']


def descendants(widget):
    result, stack = [], [widget]
    while stack:
        current = stack.pop()
        result.append(current)
        stack.extend(current.winfo_children())
    return result


def check_dashboard_lifetime(app, mod, idle):
    """WA-39: aktuelle Objekte, Archivgrenze und fehlerfester Renderkontext."""
    today = date.today()
    day = today.isoformat()
    tomorrow = (today + timedelta(days=1)).isoformat()
    source = app.new_list_object('Modellprüfung', list_id='home-model-active')
    child = app.new_item('Kind', item_id='home-model-child', due=tomorrow)
    first = app.new_item('Erster Gleichstand', item_id='home-model-first', due=day, planned_date=day)
    second = app.new_item('Zweiter Gleichstand', item_id='home-model-second', due=day, planned_date=day)
    source['items'] = [first, second, app.new_item('Struktur', kind=app.ITEM_KIND_GROUP, children=[child])]
    archived_folder = app.new_folder_object('Archiv', folder_id='home-model-archive', archived=True)
    archived = app.new_list_object('Im Archiv', list_id='home-model-hidden', folder_id=archived_folder['id'])
    archived['items'] = [app.new_item('Nicht mitzählen', due=day)]
    app.lists = [source, archived]
    app.folders = [archived_folder]
    app.labels = []
    app.items = source['items']
    app.active_list_id = source['id']
    app.settings['recent_lists'] = [{'id': archived['id'], 'edited_at': '2026-10-26T12:00:00'}]
    app.clear_render_cache()
    summary = app.home_summary()
    assert (summary['total'], summary['open'], summary['due_today'], summary['lists']) == (3, 3, 2, 2), summary
    assert summary['due_lists'] == [(source, 2)]
    assert summary['recent'][0][0] is archived
    assert app.home_focus_candidate()[0] is first
    assert app.next_scheduled_item()[0] is first
    assert app.home_summary(today + timedelta(days=1))['due_today'] == 1
    assert app.next_scheduled_item(today + timedelta(days=1))[0] is child
    assert app.home_week_overview(0) == []
    assert len(app.home_week_overview(14)) == 14

    app.set_active_list(source['id'])
    app.save_items()
    app.set_home_view()
    idle()
    # Die echte Erledigenaktion und Undo ersetzen Objekte: kein alter Dictcache.
    assert app.update_in_progress_item(first['id'], 'done', True) is not False
    idle()
    assert app.home_focus_candidate()[0]['id'] == second['id']
    app.undo_last_change()
    idle()
    current = app.home_focus_candidate()[0]
    assert current['id'] == first['id'] and current is not first
    assert app.next_scheduled_item()[0] is current
    assert app.home_summary()['due_today'] == 2

    # Sämtliche Bestandskacheln teilen genau einen Aufbau; kein Cache nach Rückkehr.
    visible = {'today', 'week', 'focus', 'labels', 'clock'}
    app.settings['home_tiles_hidden'] = [key for key in mod.glide_home.KEYS if key not in visible]
    app._home_signature = None
    with patch.object(mod.glide_home_dashboard, 'build', wraps=mod.glide_home_dashboard.build) as builds:
        app._refresh_home()
        assert builds.call_count == 1, builds.call_count
    assert app._home_dashboard_scope is None

    # Fehler nach Modellaufbau darf den Snapshot nicht in spätere Aufrufe tragen.
    original_summary = app.home_summary
    marker = RuntimeError('gezielter Renderabbruch')

    def failing_summary(*args, **kwargs):
        original_summary(*args, **kwargs)
        raise marker

    app._home_signature = None
    try:
        with patch.object(app, 'home_summary', side_effect=failing_summary):
            app._refresh_home()
    except RuntimeError as error:
        assert error is marker
    else:
        raise AssertionError('Renderabbruch nicht erreicht')
    current['done'] = True
    assert app.home_summary()['due_today'] == 1
    assert app.home_focus_candidate()[0]['id'] == second['id']
    # Auch reine Objektablösung mit gleicher ID/Revision muss frisch auflösen.
    source_index = next(index for index, entry in enumerate(app.lists) if entry['id'] == source['id'])
    replacement = copy.deepcopy(app.lists[source_index])
    replacement['items'][1]['text'] = 'Aktuelles Objekt nach Austausch'
    app.lists[source_index] = replacement
    app.items = replacement['items']
    app.clear_render_cache()
    assert app.home_focus_candidate()[0] is replacement['items'][1]
    app._home_signature = None
    app._refresh_home()
    idle()


def check_task_tile_actions(app, mod, idle, errors):
    """Offene Vorschau, echte Kästchen, aktuelle IDs, Undo/Redo und B15."""
    sys.path.insert(0, str(repo / 'tests/integration'))
    from test_uiux_paket import knopf_befunde
    root = app.root
    today = date.today().isoformat()
    source = app.new_list_object('Tagesaufgaben', list_id='home-actions')
    for number in range(13):
        item = app.new_item(f'{"A erledigt" if number < 6 else "B offen"} {number:02}',
                            item_id=f'home-action-{number}', planned_date=today)
        item['done'] = number < 6
        source['items'].append(item)
    app.lists = [source]
    app.folders, app.labels, app.trash = [], [], []
    app.items, app.active_list_id = source['items'], source['id']
    app.settings['home_tile_order'] = ['today', 'focus']
    app.settings['home_tiles_hidden'] = [key for key in app.HOME_TILE_KEYS if key not in ('today', 'focus')]
    app.settings['release_notes_seen'] = mod.APP_VERSION
    app.settings['daily_goal'] = 0
    app.clear_render_cache()
    assert app.save_items()
    app.undo_stack.clear()
    app.set_home_view()
    idle()

    def checks():
        return [w for w in descendants(app.home_content) if isinstance(w, mod.RoundedButton)
                and getattr(w, '_home_task_id', None) and w.text == app.ICONS['task_open']]

    def check(identity):
        return next(w for w in checks() if w._home_task_id == identity)

    def click(widget):
        widget.event_generate('<ButtonPress-1>', x=6, y=6)
        widget.event_generate('<ButtonRelease-1>', x=6, y=6)
        idle()

    assert {w._home_task_id for w in checks()} == {f'home-action-{n}' for n in range(6, 11)}
    retained = check('home-action-6')
    for _ in range(3):
        app._home_signature = None
        app.refresh_home()
        idle()
        assert check('home-action-6') is retained, 'Renderer verliert die bestehenden Knöpfe'
    original = app.find_item_in_lists('home-action-6')[0]
    old_command = check(original['id']).command
    click(check(original['id']))
    assert app.view_mode == app.HOME_VIEW and len(app.undo_stack) == 1
    assert app.find_item_in_lists(original['id'])[0]['done']
    saved = json.loads(Path(mod.SAVE_FILE).read_text(encoding='utf-8'))
    assert next(item for item in saved['lists'][0]['items'] if item['id'] == original['id'])['done']
    assert {w._home_task_id for w in checks()} == {f'home-action-{n}' for n in range(7, 12)}
    old_command()
    idle()
    assert len(app.undo_stack) == 1, 'Zweiter veralteter Klick öffnet den Punkt wieder'
    app.undo_last_change()
    idle()
    current = app.find_item_in_lists(original['id'])[0]
    assert not current['done'] and current is not original
    app.redo_last_change()
    idle()
    assert app.find_item_in_lists(original['id'])[0]['done']
    app.undo_last_change()
    idle()
    old_command()
    idle()
    assert app.find_item_in_lists(original['id'])[0]['done'], 'Callback hält das Objekt vor Undo'
    app.undo_last_change()
    idle()

    # Derselbe stabile-ID-Weg öffnet weiterhin die Originalaufgabe.
    title = next(w for w in descendants(app.home_content) if isinstance(w, mod.RoundedButton)
                 and getattr(w, '_home_task_id', None) == original['id'] and w.text != app.ICONS['task_open'])
    click(title)
    assert app.active_list_id == source['id'] and original['id'] in app.tree.selection()
    app.set_home_view()
    idle()
    callback = check('home-action-7').command
    before, depth = copy.deepcopy(app.lists), len(app.undo_stack)
    with patch.object(app, 'refresh_data_lock', return_value=False):
        callback()
    assert app.lists == before and len(app.undo_stack) == depth
    app._data_read_only = True
    with patch.object(app, 'refresh_data_lock', return_value=True):
        callback()
        app.refresh_home()
        idle()
        assert not checks()
        assert not any(w.text.endswith('Erledigt') for w in descendants(app.home_content)
                       if isinstance(w, mod.RoundedButton))
        assert app.lists == before and len(app.undo_stack) == depth
    app._data_read_only = False
    app.refresh_home()
    idle()

    # Der echte neue Knopf unter Schreibfehler: Originaldatei und ein Undo bleiben.
    data_before = Path(mod.SAVE_FILE).read_bytes()
    writer = app.write_json_atomic

    def fail_data(path, payload):
        if str(path) == str(mod.SAVE_FILE):
            raise OSError('Startseiten-Schreibprobe')
        return writer(path, payload)

    with patch.object(app, 'write_json_atomic', side_effect=fail_data), \
            patch.object(app, 'show_error'), patch.object(app, 'show_undo_toast') as toast:
        click(check('home-action-7'))
        assert app.dirty and Path(mod.SAVE_FILE).read_bytes() == data_before
        assert len(app.undo_stack) == depth + 1 and not toast.called
    assert app.save_items()
    app.undo_last_change()
    idle()

    # Geometrie der ruhenden Ansicht: vorhandene zeitlich begrenzte
    # Erledigungsfahnen natürlich auslaufen lassen und den Undo-Hinweis schließen.
    app.hide_undo_toast()
    deadline = time.monotonic() + 1.1
    while time.monotonic() < deadline:
        idle()
        time.sleep(.02)
    configurations = [('light', '860x700', 'mittel', False), ('dark', '1280x800', 'gross', False),
                      ('glass_light', '860x700', 'gross', False), ('light', '480x560', 'gross', True)]
    count, evidence = 0, []
    for design, geometry, font, compact in configurations:
        app.settings['ui_font_size'] = font
        app.apply_ui_font()
        app.set_design(design)
        if design.startswith('glass'):
            app.set_backdrop_choice(mod.glide_backdrop.presets_for(design)[0].key)
        if compact:
            app.enter_compact_mode()
        root.geometry(geometry + '+20+20')
        app._home_signature = None
        app.refresh_home()
        idle()
        for position in (0, 0.5, 1):
            app.home_canvas.yview_moveto(position)
            idle()
            tested, findings = knopf_befunde(root, mod, f'Heute-Aktionen {design} {geometry} {position}')
            count += tested
            assert not findings, findings[:5]
        evidence.append(dict(design=design, geometry=geometry, font=font, compact=compact))
        if os.environ.get('GLIDE_HOME_CAPTURE'):
            sys.path.insert(0, str(repo / 'tests/tools'))
            from releasedaten import save_windows_screenshot
            app.home_canvas.yview_moveto(0)
            idle()
            target = Path(os.environ['GLIDE_HOME_CAPTURE']) / f'{design}-{geometry}.png'
            target.parent.mkdir(parents=True, exist_ok=True)
            save_windows_screenshot(root, target)
        if compact:
            app.leave_compact_mode()
    assert not errors, errors
    return dict(open_preview=5, undo_redo=True, stale_callback=True, write_failure=True,
                read_only=True, configurations=evidence, button_checks=count)


with tempfile.TemporaryDirectory(prefix='glide-startseite-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_startseite3332', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    # Größenmeldungen des Hauptfensters zählen, bevor die App sie bindet.
    original_density = mod.ListApp.sync_height_density
    density_calls = []

    def counted_density(self, event=None):
        density_calls.append(None if event is None else (event.widget, event.height))
        return original_density(self, event)
    mod.ListApp.sync_height_density = counted_density
    errors = []
    root = mod.tk.Tk()
    root.geometry('1400x950+20+20')
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def click(widget):
        widget.event_generate('<ButtonPress-1>', x=6, y=6)
        widget.event_generate('<ButtonRelease-1>', x=6, y=6)
        idle()

    def visible():
        return [key for key in app.home_tile_order() if app.home_tile_visible(key)]

    def home_texts():
        texts = []
        for widget in descendants(app.home_content):
            try:
                texts.append(str(widget.cget('text')) if isinstance(widget, mod.tk.Label) else getattr(widget, 'text', ''))
            except mod.tk.TclError:
                pass
        return texts

    def button(text):
        return next(w for w in descendants(app.home_content)
                    if isinstance(w, mod.RoundedButton) and w.text == text)

    try:
        idle()
        # --- Neuer Bestand: Standard „Ruhig“ mit acht Kacheln (D12, B04) ----
        assert visible() == D12, visible()
        assert app.settings['home_tile_order'] == []
        liste = app.lists[0] if not app.is_inbox_list(app.lists[0]) else app.ensure_inbox_list()
        app.set_active_list(liste['id'])
        heute = date.today().isoformat()
        app.items.append(app.new_item('Angebot schreiben', planned_date=heute, due=heute))
        app.items.append(app.new_item('Unterlagen sortieren', planned_date=heute))
        app.settings['daily_goal'] = 3
        assert app.save_items()
        app.set_home_view()
        idle()
        texts = home_texts()
        # „Heute“ trägt Tagesziel und nächste Aufgabe, weil deren eigene Kacheln aus sind.
        assert sum(t.startswith('Heute geschafft: 0 von 3') for t in texts) == 1, texts
        assert 'Als Nächstes' in texts and 'Angebot schreiben' in texts, texts
        assert not any(t.startswith('Hallo') or t.startswith('Guten') for t in texts)

        # --- Einblenden im Bearbeitungsmodus ist eine eigene Auswahl ----------
        app.toggle_home_editing()
        idle()
        for key in ('welcome', 'focus', 'clock'):
            title = dict((k, t) for k, t, _g, _b, _s in app.HOME_TILE_DEFINITIONS)[key]
            click(button(f'+ {title}'))
        click(button('Fertig'))
        assert app.settings['home_tile_order'], 'Auswahl wurde nicht als eigene gespeichert'
        assert {'welcome', 'focus', 'clock'} <= set(visible())
        texts = home_texts()
        # Keine Angabe doppelt: Tagesziel steht jetzt in der Begrüßung, die
        # nächste Aufgabe in ihrer eigenen Kachel.
        assert sum(t.startswith('Heute geschafft: 0 von 3') for t in texts) == 1, texts
        assert 'Als Nächstes' not in texts, texts
        # Neustart der Einstellungen: Die Auswahl bleibt (bis 3.33.1 fiel sie zurück).
        app.settings = app.load_settings()
        assert {'welcome', 'focus', 'clock'} <= set(visible()), visible()

        # --- Zurücksetzen im Dialog „Startseite einrichten“ -------------------
        original_modal = app.run_modal

        def reset_modal(dialog, parent=None):
            idle()
            buttons = [w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)]
            next(w for w in buttons if w.text == 'Standard wiederherstellen').command()
            listbox = next(w for w in descendants(dialog) if isinstance(w, mod.tk.Listbox))
            assert listbox.size() == len(app.HOME_TILE_KEYS)
            next(w for w in buttons if w.text == 'Speichern').command()
        app.run_modal = reset_modal
        app.show_home_tiles_dialog()
        app.run_modal = original_modal
        idle()
        assert app.settings['home_tile_order'] == [] and visible() == D12, (app.settings['home_tile_order'], visible())
        app.settings = app.load_settings()
        assert visible() == D12

        # --- Größenmeldungen: Python sieht nur das Hauptfenster ---------------
        density_calls.clear()
        app.home_content.event_generate('<Configure>')
        app.home_canvas.event_generate('<Configure>')
        idle()
        assert density_calls == [], density_calls
        root.geometry('1400x900+20+20')
        idle()
        assert density_calls and all(widget is root for widget, _h in density_calls), density_calls
        assert density_calls[-1][1] == root.winfo_height()

        # --- Gerundete Flächen zeichnen einmal je Leerlauf ---------------------
        box = mod.RoundedContainer(app.home_content, app.theme['bg'], app.theme['card'], width=200, height=80)
        box.pack()
        idle()
        drawn = []
        original_draw = box._draw
        box._draw = lambda: (drawn.append((box.winfo_width(), box.winfo_height())), original_draw())
        for _ in range(5):
            box._on_configure()
        assert drawn == [] and box._draw_pending is not None
        root.update_idletasks()
        assert len(drawn) == 1 and box._draw_pending is None, drawn
        box._on_configure()
        box.destroy()
        idle()
        knopf = mod.RoundedButton(app.home_content, 'Probe', lambda: None, app.theme['line'],
                                  app.theme['hover'], app.theme['text'])
        knopf.pack()
        knopf._schedule_draw()
        knopf.destroy()
        idle()

        # --- Designwechsel: Farben werden weiterhin übernommen ----------------
        for design in ('dark', 'light'):
            app.set_design(design, apply_now=False)
            app.apply_theme()
            app.set_home_view()
            idle()
            assert app.home_canvas.cget('bg') == app.theme['bg'] == app.home_content.cget('bg')
            assert app.home_scrollbar.bg_color == app.theme['bg']
        check_dashboard_lifetime(app, mod, idle)
        actions = check_task_tile_actions(app, mod, idle, errors)
        if os.environ.get('GLIDE_HOME_ACTION_REPORT'):
            Path(os.environ['GLIDE_HOME_ACTION_REPORT']).write_text(
                json.dumps(actions, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        assert not errors, errors
        print('test_startseite3332: OK; D12-Standard, zusammengeführte Kachel Heute, eigene Auswahl nach Neustart, '
              'Zurücksetzen, Größenfilter Hauptfenster, gebündeltes Zeichnen, Designwechsel; '
              'Startseitenmodell: Archiv, Datum, Gleichstände, Erledigen/Undo, Objektwechsel, Renderabbruch')
    finally:
        root.destroy()
