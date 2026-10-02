"""3.33.3 (G01): deutsche Schnelleingabe mit Feldchips über echte Tasten-, Klick- und Dialogwege."""
import importlib.machinery
import importlib.util
import os
from datetime import date, timedelta
from pathlib import Path
import tempfile

repo = Path(__file__).resolve().parents[2]


def descendants(widget):
    result, stack = [], [widget]
    while stack:
        current = stack.pop()
        result.append(current)
        stack.extend(current.winfo_children())
    return result


with tempfile.TemporaryDirectory(prefix='glide-eingabe-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_eingabe3333', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    errors = []
    root = mod.tk.Tk()
    root.geometry('1280x900+20+20')
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    heute = date.today()

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def chips(frame):
        """Chiptexte: Beschriftungen mit einem × daneben; Hinweise zählen nicht."""
        return [w for w in descendants(frame) if isinstance(w, mod.tk.Label) and w.cget('text') != app.ICONS['remove']
                and any(isinstance(n, mod.tk.Label) and n.cget('text') == app.ICONS['remove']
                        for n in w.master.winfo_children())]

    def chip_texts(frame):
        return sorted(w.cget('text') for w in chips(frame))

    def remove_button(frame, prefix):
        label = next(w for w in chips(frame) if w.cget('text').startswith(prefix))
        return next(w for w in label.master.winfo_children() if w.cget('text') == app.ICONS['remove'])

    def type_into_entry(text):
        app.clear_entry_text()
        app.entry.focus_force()
        app.entry.insert(0, text)
        app.entry.icursor('end')
        app.entry.event_generate('<KeyRelease>', keysym='space')
        idle()

    try:
        idle()
        app.labels.append({'id': 'buero', 'name': 'Büro', 'color': 'clear'})
        liste = app.new_list_object('Eingang Test', [])
        app.lists.append(liste)
        app.save_items()
        app.set_active_list(liste['id'])
        idle()
        assert app.view_mode == 'list'

        # --- Abnahme aus dem Plan: drei Chips, einzeln rücknehmbar --------------
        type_into_entry('Angebot schicken morgen bis Freitag /wichtig')
        hint = app._capture_hint
        assert hint.winfo_ismapped()
        texts = chip_texts(hint)
        assert len(texts) == 3 and any(t.startswith('Bearbeitungstag') for t in texts), texts
        assert any(t.startswith('Fällig') for t in texts) and 'Wichtigkeit hoch' in texts, texts
        remove_button(hint, 'Fällig').event_generate('<Button-1>')
        idle()
        assert app.entry.get() == 'Angebot schicken morgen bis Freitag /wichtig', 'Text bleibt unverändert'
        assert not any(t.startswith('Fällig') for t in chip_texts(app._capture_hint)), chip_texts(app._capture_hint)
        app.entry.focus_force()
        app.entry.event_generate('<Return>')
        idle()
        item = liste['items'][-1]
        morgen = (heute + timedelta(days=1)).isoformat()
        assert item['text'] == 'Angebot schicken bis Freitag', item['text']
        assert item['planned_date'] == morgen and item['importance'] == 3 and not item['due'], item
        assert app.entry.get() in ('', app.entry_placeholder_text) and app.capture_ignored() == set()
        app.undo_last_change()
        idle()
        liste = next(entry for entry in app.lists if entry['id'] == liste['id'])
        assert not liste['items'], 'Rückgängig entfernt die neue Aufgabe'

        # --- Uhrzeit, Aufwand, Label; Anführungszeichen bleiben wörtlich -------
        type_into_entry('Exposé morgen 14:30, 45 Minuten #büro')
        app.add_item()
        idle()
        item = liste['items'][-1]
        assert (item['text'], item['planned_date'], item['planned_time'], item['estimated_minutes'], item['labels']) == \
            ('Exposé', morgen, '14:30', 45, ['buero']), item
        type_into_entry('Termin "morgen" absagen')
        assert not chips(app._capture_hint) if app._capture_hint.winfo_ismapped() else True
        app.add_item()
        idle()
        assert liste['items'][-1]['text'] == 'Termin "morgen" absagen' and not liste['items'][-1]['planned_date']
        # Nach dem Leeren gilt eine zurückgenommene Erkennung nicht mehr.
        type_into_entry('Steuer bis Freitag')
        assert any(t.startswith('Fällig') for t in chip_texts(app._capture_hint))
        app.entry.event_generate('<Escape>')
        idle()
        assert not app._capture_hint.winfo_ismapped()
        app.clear_entry_text()

        # --- 3.33.4: Wiederholung setzt die Fälligkeit (Entscheidung 02.10.2026) ---
        type_into_entry('Sport jeden Montag 18 Uhr')
        texts = chip_texts(app._capture_hint)
        assert len(texts) == 1 and texts[0].startswith('Wiederholung jeden Montag · fällig ab'), texts
        app.entry.focus_force()
        app.entry.event_generate('<Return>')
        idle()
        sport = liste['items'][-1]
        montag = heute + timedelta(days=(0 - heute.weekday()) % 7)
        assert sport['text'] == 'Sport' and sport['due'] == montag.isoformat() and sport['due_time'] == '18:00', sport
        assert sport['repeat'] and sport['repeat']['art'] == app.REPEAT_WEEKLY, sport['repeat']
        assert app.home_calendar_days().get(montag.isoformat(), 0) >= 1, 'steht im Kalender'
        assert app.toggle_item_done_anywhere(sport['id'])
        idle()
        offen = [p for p in liste['items'] if p['text'] == 'Sport' and not p.get('done')]
        assert offen and offen[0]['due'] == (montag + timedelta(days=7)).isoformat(), offen
        type_into_entry('Sport jeden Montag')
        remove_button(app._capture_hint, 'Wiederholung').event_generate('<Button-1>')
        idle()
        app.add_item()
        idle()
        assert liste['items'][-1]['text'] == 'Sport jeden Montag' and not liste['items'][-1]['repeat']

        # --- Schnellerfassung: dieselben Chips; Feld „Fällig“ hat Vorrang -------
        original_modal = app.run_modal

        def capture_modal(dialog, parent=None):
            idle()
            entries = [w for w in descendants(dialog) if isinstance(w, mod.tk.Entry)]
            # Reihenfolge im Baum ist nicht garantiert: Das Titelfeld steht oben, „Fällig“ darunter.
            title_entry, due_entry = sorted(entries, key=lambda e: e.winfo_rooty())[:2]
            title_entry.insert(0, 'Bericht morgen 14:30, 45 Minuten bis Montag')
            idle()
            frame = next(w for w in descendants(dialog) if isinstance(w, mod.tk.Frame)
                         and any(isinstance(c, mod.tk.Frame) for c in w.winfo_children())
                         and chips(w) and any(x.cget('text').startswith('Aufwand') for x in chips(w)))
            remove_button(frame, 'Aufwand').event_generate('<Button-1>')
            idle()
            assert not any(t.startswith('Aufwand') for t in chip_texts(frame))
            due_entry.insert(0, 'übermorgen')
            idle()
            assert any('Vorrang' in t for t in chip_texts(frame)), chip_texts(frame)
            button = next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton) and w.text == 'Erfassen')
            button.command()
        app.run_modal = capture_modal
        app.show_quick_capture()
        app.run_modal = original_modal
        idle()
        inbox = app.ensure_inbox_list()
        item = inbox['items'][-1]
        assert item['text'] == 'Bericht 45 Minuten', item['text']
        assert item['planned_date'] == morgen and item['planned_time'] == '14:30', item
        assert item['due'] == (heute + timedelta(days=2)).isoformat() and not item['estimated_minutes'], item

        # --- Hilfe nennt die neue Bedeutung ------------------------------------
        hilfe = repr(app.MANUAL_SECTIONS)
        assert 'setzen den Bearbeitungstag' in hilfe and '/bis Freitag' in hilfe
        assert 'setzen die Fälligkeit; /wichtig' not in hilfe, 'alte Bedeutung von /morgen'

        assert not errors, errors
        print('test_eingabe3333: OK; Chips, Wiederholung mit Fälligkeit und Folgetermin, Zurücknehmen per Klick, Return, Rückgängig, Uhrzeit/Aufwand/Label, '
              'Anführungszeichen, Escape, Schnellerfassung mit Vorrang des Fälligkeitsfelds')
    finally:
        root.destroy()
