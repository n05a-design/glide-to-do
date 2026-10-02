"""3.33.6 (D14): „Heute“ und „Demnächst“ – Abschnitte, nächste Aufgabe, Tageswechsel, Modi, Wege."""
import importlib.machinery
import importlib.util
import json
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


with tempfile.TemporaryDirectory(prefix='glide-heute-') as directory:
    os.environ['GLIDE_DATA_DIR'] = directory
    os.environ['GLIDE_TEST_MODE'] = '1'
    loader = importlib.machinery.SourceFileLoader('glide_heute3336', str(repo / 'src/glide/app.pyw'))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    errors = []
    root = mod.tk.Tk()
    root.geometry('1400x900+20+20')
    root.report_callback_exception = lambda *exc: errors.append(str(exc[1]))
    app = mod.ListApp(root)
    heute = date.today()
    tag = lambda delta: (heute + timedelta(days=delta)).isoformat()

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def menu_labels(menu):
        labels = []
        for index in range(menu.index('end') + 1):
            try:
                labels.append(menu.entrycget(index, 'label'))
            except mod.tk.TclError:
                pass
        return labels

    try:
        idle()
        plan_a = app.new_item('Plan A', planned_date=tag(0))
        plan_wichtig = app.new_item('Plan wichtig', planned_date=tag(0), importance=3)
        verspaetet = app.new_item('Verspätet', due=tag(-2))
        liegen = app.new_item('Liegen', planned_date=tag(-3))
        faellig = app.new_item('Heute fällig', due=tag(0))
        morgen = app.new_item('Morgen fällig', due=tag(1))
        erledigt = app.new_item('Erledigt alt', due=tag(-5))
        erledigt['done'] = True
        liste = app.new_list_object('Arbeit', [plan_a, plan_wichtig, verspaetet, liegen, faellig, morgen, erledigt])
        app.lists.append(liste)
        eingang = next(entry for entry in app.lists if app.is_inbox_list(entry))
        eingang_frei = app.new_item('Eingang frei')
        eingang_faellig = app.new_item('Eingang fällig', due=tag(0))
        eingang['items'].extend([eingang_frei, eingang_faellig])
        app.save_items()
        idle()

        def zeile(item, quelle=liste):
            return f"in-progress:{quelle['id']}:{item['id']}"

        # --- „Heute“ über die Seitenleiste ------------------------------------
        app.set_home_view()
        idle()
        assert app.system_listbox.exists(app.PLAN_DAY_ROW_ID)
        sidebar_text = app.system_listbox.item(app.PLAN_DAY_ROW_ID, 'text')
        assert 'Heute' in sidebar_text and 'Mein Tag' not in sidebar_text, sidebar_text
        # Zahl: zwei geplant, verspätet, liegen geblieben, zwei heute fällig (eine im Eingang).
        assert app.count_today_view() == 6, app.count_today_view()
        app.system_listbox.selection_set(app.PLAN_DAY_ROW_ID)
        app.system_listbox.focus(app.PLAN_DAY_ROW_ID)
        app.system_listbox.event_generate('<<TreeviewSelect>>')
        idle()
        assert app.view_mode == app.PLAN_DAY_VIEW, app.view_mode
        assert app.get_display_title().startswith('Heute · '), app.get_display_title()

        oben = list(app.tree.get_children(''))
        erwartet = [app.NEXT_TASK_SECTION_ROW_ID, app.OVERDUE_SECTION_ROW_ID, app.LEFTOVER_SECTION_ROW_ID,
                    app.DAYPLAN_SECTION_ROW_ID, app.DUE_TODAY_SECTION_ROW_ID, app.UPCOMING_LINK_ROW_ID,
                    app.PLAN_INBOX_HEADING_ROW_ID]
        assert oben == erwartet, oben
        # Die nächste Aufgabe ist dieselbe wie auf der Startseite.
        fokus, fokus_liste = app.home_focus_candidate()
        assert fokus['id'] == plan_wichtig['id']
        assert app.tree.get_children(app.NEXT_TASK_SECTION_ROW_ID) == (zeile(plan_wichtig),)
        assert app.tree.get_children(app.OVERDUE_SECTION_ROW_ID) == (zeile(verspaetet),)
        assert app.tree.get_children(app.LEFTOVER_SECTION_ROW_ID) == (zeile(liegen),)
        assert app.tree.get_children(app.DAYPLAN_SECTION_ROW_ID) == (zeile(plan_a),)
        assert set(app.tree.get_children(app.DUE_TODAY_SECTION_ROW_ID)) == {zeile(faellig), zeile(eingang_faellig, eingang)}
        assert app.tree.get_children(app.PLAN_INBOX_HEADING_ROW_ID) == (zeile(eingang_frei, eingang),)
        assert 'Heute fällig · 2' in app.tree.item(app.DUE_TODAY_SECTION_ROW_ID, 'text')
        assert 'Tagesplan · 1' in app.tree.item(app.DAYPLAN_SECTION_ROW_ID, 'text')
        # Künftiges und Erledigtes gehört nicht nach „Heute“.
        alle = [kind for kopf in oben for kind in app.tree.get_children(kopf)]
        assert zeile(morgen) not in alle and zeile(erledigt) not in alle
        assert len(alle) == len(set(alle)) == 7

        # Der Verweis am Ende führt nach „Demnächst“, das keine Seitenleistenzeile hat.
        assert 'Demnächst · 1 weitere Fälligkeit' in app.tree.item(app.UPCOMING_LINK_ROW_ID, 'text')
        app.tree.focus(app.UPCOMING_LINK_ROW_ID)
        assert app.open_in_progress_source_item() == 'break'
        assert app.view_mode == 'in_progress'
        app.set_today_view()
        idle()
        # Doppelklick auf eine neue Überschrift klappt nur und bleibt in der Ansicht.
        app.tree.focus(app.DUE_TODAY_SECTION_ROW_ID)
        assert app.open_in_progress_source_item() == 'break'
        assert app.view_mode == app.PLAN_DAY_VIEW
        # Zuklappen übersteht Neuladen; eine alte, entfallene Kennung nicht.
        app.set_overview_section_open(app.LEFTOVER_SECTION_ROW_ID, False)
        app.settings['overview_sections_closed'].append('planinprogress:heading')
        app.save_settings()
        geladen = app.load_settings()
        assert app.LEFTOVER_SECTION_ROW_ID in geladen['overview_sections_closed']
        assert 'planinprogress:heading' not in geladen['overview_sections_closed']
        app.set_overview_section_open(app.LEFTOVER_SECTION_ROW_ID, True)

        # --- Tagesbeginn und Tagesabschluss als Modi von „Heute“ ---------------
        knopf = app.plan_day_mode_button
        assert knopf.winfo_ismapped(), 'Tag … fehlt in der Filterzeile'
        assert app.show_plan_day_mode_menu() == 'break'
        idle()
        panel = getattr(app, '_active_dropdown', None)
        assert isinstance(panel, mod.DropdownPopup)
        beginn = next(w for w in descendants(panel) if 'text' in w.keys() and w.cget('text') == 'Tagesbeginn …')
        beginn.event_generate('<ButtonRelease-1>')
        idle()
        assert app.view_mode == app.HOME_VIEW and getattr(app, '_day_review', None) is not None
        app.set_today_view()
        idle()
        smart = menu_labels(app.build_smart_view_menu(app.PLAN_DAY_VIEW))
        assert 'Tagesbeginn …' in smart and 'Tagesabschluss …' in smart, smart
        assert smart[0].startswith('Heute · ') and smart[0].endswith('(6)'), smart[0]

        # --- Ein anderer Tag ------------------------------------------------------
        app.plan_day_forward()
        idle()
        assert app.get_display_title().startswith('Tagesplan · '), app.get_display_title()
        oben = list(app.tree.get_children(''))
        assert app.NEXT_TASK_SECTION_ROW_ID not in oben and app.OVERDUE_SECTION_ROW_ID not in oben, oben
        assert app.tree.get_children(app.DUE_TODAY_SECTION_ROW_ID) == (zeile(morgen),)
        assert 'An diesem Tag fällig · 1' in app.tree.item(app.DUE_TODAY_SECTION_ROW_ID, 'text')
        assert app.EMPTY_ROW_ID in oben

        # --- „Demnächst“: chronologisch, ohne nächste Aufgabe ---------------------
        app.set_in_progress_view()
        idle()
        assert app.get_display_title() == 'Demnächst'
        oben = list(app.tree.get_children(''))
        assert app.NEXT_TASK_SECTION_ROW_ID not in oben, oben
        assert oben[0] == app.OVERDUE_SECTION_ROW_ID
        offen = app.tree.get_children(app.IN_PROGRESS_SECTION_ROW_ID)
        assert zeile(morgen) in offen
        faelligkeiten = [app.in_progress_item_sources[z] for z in offen]
        assert faelligkeiten.index((liste['id'], morgen['id'])) == len(faelligkeiten) - 1

        # --- Nächste Aufgabe aus jeder Ansicht ------------------------------------
        app.set_home_view()
        idle()
        assert app.open_next_task() == 'break'
        idle()
        assert app.view_mode == app.PLAN_DAY_VIEW and app.plan_day() == tag(0)
        assert app.tree.focus() == zeile(plan_wichtig)

        # --- Wege und Texte -----------------------------------------------------
        aktionen = [text for gruppe in app.ACTION_GROUPS.values() for text in gruppe]
        for text in ('Heute', 'Demnächst', 'Heute: Tag zurück', 'Heute: Tag vor', 'Heute: Stundenraster ein/aus'):
            assert text in aktionen, text
        assert not any('Mein Tag' in text or 'In Bearbeitung' in text for text in aktionen)
        assert [name for name, _symbol, _befehl in app.quick_open_views()][1:3] == ['Heute', 'Demnächst']
        assert dict((k, n) for k, n, _h in app.STARTUP_VIEW_CHOICES)['in_progress'] == 'Demnächst'
        handbuch = json.dumps(app.MANUAL_SECTIONS, ensure_ascii=False)
        assert '"Heute"' in handbuch and '"Demnächst"' in handbuch
        assert 'Mein Tag' not in handbuch and 'In Bearbeitung“ mit' not in handbuch
        # Kontextmenü einer Liste: Einplanen heißt jetzt „Für heute einplanen“.
        app.set_active_list(liste['id'])
        idle()
        app.tree.selection_set(morgen['id'])
        app.tree.focus(morgen['id'])
        assert 'Für heute einplanen' in menu_labels(app.build_item_context_menu())
        assert not errors, errors
        print('test_heute3336: OK; Abschnitte von Heute, nächste Aufgabe wie Startseite, keine Dubletten, '
              'anderer Tag, Demnächst chronologisch, Tag … mit Tagesbeginn, Wege und Texte')
    finally:
        root.destroy()
