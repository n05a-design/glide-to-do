"""3.33.5 (G02, D13): Eisenhower als Gruppierung im Board und in der Liste – echte Auswahl, Ablegen, Undo."""
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


with tempfile.TemporaryDirectory(prefix='glide-eisenhower-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_eisenhower3335', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    errors, infos, toasts = [], [], []
    root = mod.tk.Tk()
    root.geometry('1400x900+20+20')
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    app.show_info = lambda *args, **kwargs: infos.append(args)
    original_toast = app.show_undo_toast
    app.show_undo_toast = lambda text, restore=None: (toasts.append(text), original_toast(text, restore))[1]
    heute = date.today()

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    try:
        idle()
        a = app.new_item('Angebot', importance=3, due=heute.isoformat())
        b = app.new_item('Strategie', importance=2)
        c = app.new_item('Anruf', planned_date=heute.isoformat())
        d = app.new_item('Ablage')
        e = app.new_item('Abgabe', importance=2, due=(heute + timedelta(days=1)).isoformat())
        liste = app.new_list_object('Matrix', [a, b, c, d, e])
        app.lists.append(liste)
        app.save_items()
        app.set_active_list(liste['id'])
        idle()

        # --- Gruppierung über die echte Auswahl der Board-Optionen --------------
        ws = app.workspace
        ws.set_mode('board')
        ws.configure_board('layout', 'columns')
        idle()
        menue = next(w for w in descendants(ws.body) if isinstance(w, mod.AppOptionMenu)
                     and any('Dringlichkeit' in str(option) for option in w.options))
        menue.variable.set('Gruppieren: Dringlichkeit × Wichtigkeit')
        idle()
        assert ws.board()['group_by'] == 'eisenhower'
        assert [spalte['key'] for spalte in ws.column_order] == ['q1', 'q2', 'q3', 'q4']
        assert ws.column_order[0]['title'].startswith('Sofort')

        def spalte(item):
            return sorted(key for _box, identity, key, _tag in ws.column_hits if identity == item['id'])
        assert [spalte(x) for x in (a, b, c, d, e)] == [['q1'], ['q2'], ['q3'], ['q4'], ['q1']]

        def aktuell(item):
            return app.find_item_in_lists(item['id'])[0]

        # --- Ablegen ändert nur, was der Quadrant verlangt ------------------------
        assert ws.move_to_column(d['id'], 'q4', 'q2')
        assert aktuell(d)['importance'] == 2 and not aktuell(d)['planned_date']
        assert toasts and toasts[-1] == 'Eingeordnet · Wichtigkeit mittel', toasts
        assert ws.move_to_column(b['id'], 'q2', 'q1')
        assert aktuell(b)['planned_date'] == heute.isoformat() and aktuell(b)['importance'] == 2
        # Eine nahe Fälligkeit bleibt; das Ablegen wird erklärt abgelehnt.
        vorher = dict(aktuell(e))
        assert ws.move_to_column(e['id'], 'q1', 'q2') is False
        assert infos and 'Fälligkeit' in str(infos[-1]), infos
        assert aktuell(e)['due'] == vorher['due'] and aktuell(e)['importance'] == vorher['importance']
        # Nicht dringend: Bearbeitungstag auf den ersten Tag nach dem Fenster; Undo stellt ihn zurück.
        assert ws.move_to_column(c['id'], 'q3', 'q4')
        assert aktuell(c)['planned_date'] == (heute + timedelta(days=3)).isoformat()
        app.undo_last_change()
        idle()
        assert aktuell(c)['planned_date'] == heute.isoformat()
        ws._signature = None
        ws.refresh()
        idle()
        assert spalte(c) == ['q3'] and spalte(d) == ['q2']
        # Tastatur: Alt+Rechts in den nächsten Quadranten.
        ws.selected_id = d['id']
        ws._selected_column = 'q2'
        ws.move_card_to_neighbour_column(1)
        idle()
        assert aktuell(d)['importance'] == 1 and aktuell(d)['planned_date'] == heute.isoformat()

        # --- Dieselbe Gruppierung in der Listenansicht ---------------------------
        ws.set_mode('list')
        app.set_list_group('eisenhower')
        idle()
        assert app.list_group_field() == 'eisenhower'
        abschnitte = [iid for iid in app.tree.get_children('') if app.is_group_section_row(iid)]
        # Leere Abschnitte blendet die Liste wie bei jeder Gruppierung aus; die Reihenfolge bleibt.
        assert [app.group_section_key(iid) for iid in abschnitte] == ['q1', 'q3'], abschnitte
        kinder = {app.group_section_key(iid): set(app.tree.get_children(iid)) for iid in abschnitte}
        assert kinder == {'q1': {a['id'], b['id'], e['id']}, 'q3': {c['id'], d['id']}}, kinder
        # Einstellungen bleiben nach dem Neuladen gültig.
        app.settings = app.load_settings()
        assert app.settings['list_group_by'].get(liste['id']) == 'eisenhower'
        assert not errors, errors
        print('test_eisenhower3335: OK; Auswahl im Board, vier Quadranten, Ablegen nach D13, Fälligkeit bleibt, '
              'Undo, Alt+Rechts, Listengruppierung, Neuladen')
    finally:
        root.destroy()
