"""3.33.2: Startseite „Ruhig“ (D12), eigene Auswahl, Zurücksetzen und Aufbaukosten über echte Wege."""
import importlib.machinery
import importlib.util
import os
from datetime import date
from pathlib import Path
import tempfile

repo = Path(__file__).resolve().parents[2]
D12 = ['mascot', 'today', 'week', 'recent', 'boardpreview', 'drawings', 'pinned']


def descendants(widget):
    result, stack = [], [widget]
    while stack:
        current = stack.pop()
        result.append(current)
        stack.extend(current.winfo_children())
    return result


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
        # --- Neuer Bestand: Standard „Ruhig“ mit sieben Kacheln (D12) -------
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
        assert not errors, errors
        print('test_startseite3332: OK; D12-Standard, zusammengeführte Kachel Heute, eigene Auswahl nach Neustart, '
              'Zurücksetzen, Größenfilter Hauptfenster, gebündeltes Zeichnen, Designwechsel')
    finally:
        root.destroy()
