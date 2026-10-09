"""Glide: Startseite, Einstellungen, Artwechsel, Textfarben und schmale Fenster.

Optional --screenshots ORDNER zeichnet ausschließlich eigene Testfenster auf Windows.
Alle Nutzdaten werden vor dem App-Import in einem temporären Ordner isoliert.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--screenshots', type=Path)
args = parser.parse_args()

def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)

with tempfile.TemporaryDirectory(prefix='glide-ui-updates-') as tmp:
    os.environ['GLIDE_DATA_DIR'] = tmp
    old_settings = {'theme': 'dark', 'title': 'Meine Liste', 'custom_setting': 'behalten'}
    (Path(tmp)/'settings.json').write_text(json.dumps(old_settings), encoding='utf-8')
    loader = importlib.machinery.SourceFileLoader('glide_ui_updates', str(REPO/'src/glide/app.pyw'))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    app = mod.ListApp(root)
    app.confirm_template_preview = lambda template: True
    root.geometry('1280x960+10+10')
    root.update()
    reported_errors=[]
    root.report_callback_exception = lambda *error: reported_errors.append(error)
    original_modal = app.run_modal

    def capture(widget, name):
        if args.screenshots and os.name == 'nt':
            sys.path.insert(0, str(REPO/'tests/tools'))
            from releasedaten import save_windows_screenshot
            widget.update()
            widget.tk.call('after', 100, 'set', '::capture_ready', '1')
            widget.tk.call('vwait', '::capture_ready')
            widget.update()
            save_windows_screenshot(widget, args.screenshots.resolve()/f'{name}.png')

    def inspect_dialog(check):
        def inspect(dialog, parent=None):
            dialog.update()
            try:
                check(dialog)
            finally:
                if dialog.winfo_exists():
                    dialog.destroy()
        app.run_modal = inspect

    def button(dialog, name):
        return next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton) and w.text == name)

    try:
        assert Path(mod.BASE_DIR).resolve() == Path(tmp).resolve()
        assert app.settings['profile_name'] == '' and not app.settings['start_on_home']
        assert app.settings['profile_logo'] == 'G'
        assert app.view_mode == 'list'
        assert app.save_settings()
        assert json.loads((Path(tmp)/'settings.before-v1.json').read_text()) == old_settings
        assert app.settings['custom_setting'] == 'behalten'

        inbox_id=app.active_list_id
        today=mod.date.today()
        done=app.new_item('Schon erledigt', done=True, due=today.isoformat())
        task=app.new_item('Konzept und Texte für den neuen Auftritt abstimmen', due=today.isoformat(), due_time='09:30', importance=3)
        old=app.new_item('Rückmeldung zum Entwurf', due=(today-mod.timedelta(days=1)).isoformat())
        group=app.new_item('Struktur', kind='heading')
        f1=app.new_folder_object('Projekte')
        f2=app.new_folder_object('Kommunikation und Gestaltung', parent_id=f1['id'])
        f3=app.new_folder_object('Laufende Kundenprojekte', parent_id=f2['id'])
        app.folders.extend([f1,f2,f3])
        entry=app.new_list_object('Neuer Auftritt und digitale Kommunikation', [group, task, done, old], folder_id=f3['id'])
        app.lists.append(entry)
        custom=app.new_label_object('Freigabe nötig', color='import')
        app.labels.append(custom)
        task['labels']=[custom['id']]
        app.set_active_list(entry['id'])
        app.save_items()
        summary=app.home_summary(today)
        assert (summary['total'],summary['open'],summary['done'],summary['due_today'],summary['overdue']) == (3,2,1,1,1)
        assert summary['due_lists'] == [(entry,1)]
        assert app.folder_task_count(f1['id']) == 3
        assert app.sidebar_listbox.set(f"folder:{f1['id']}", 'count') == '(3)'
        recent=copy.deepcopy(app.settings['recent_lists'])
        app.set_active_list(inbox_id)
        app.save_items()
        assert app.settings['recent_lists'] == recent, 'Navigation/Autosave ist keine Bearbeitung'

        for theme in ('dark','light'):
            # Seit das Design die einzige Quelle ist, wirkt eine Zuweisung an
            # theme_name nicht mehr; bis 08.10.2026 lief der Dunkelfall hier hell (W02).
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            assert (mod.relative_luminance(app.theme['bg']) < 0.2) == (theme == 'dark'), (theme, app.theme['bg'])
            app.set_active_list(entry['id'])
            for width in (1280,980,860):
                root.geometry(f'{width}x900+10+10')
                root.update()
                app.sync_task_tree_columns()
                text=app.tree.bbox(task['id'],'#0')
                if app.tree.column('due','width'):
                    due=app.tree.bbox(task['id'],'due')
                    assert due[0]-(text[0]+text[2]) == app.TASK_METADATA_GAP
                count_boxes=[app.sidebar_listbox.bbox(iid,'count') for iid in (f"folder:{f1['id']}",f"folder:{f3['id']}",f"list:{entry['id']}")]
                assert all(box for box in count_boxes)
                assert len({box[0]+box[2] for box in count_boxes}) == 1
                if width in (1280,860):
                    capture(root, f'liste-{theme}-{width}')
            root.geometry('1280x960+10+10')
            app.settings.update(profile_name='Tim',profile_logo='TV')
            app.set_home_tile_hidden('welcome', False)  # Seit D12 (3.33.2) nicht mehr im Standard: die geprüfte Kachel ausdrücklich einblenden.
            app.set_home_view()
            root.update()
            assert app.home_frame.winfo_ismapped() and not app.tree.winfo_ismapped()
            assert app.system_listbox.selection() == (app.HOME_ROW_ID,)
            assert app.home_content.cget('bg') == app.theme['bg']
            assert any('Tim' in str(w.cget('text')) for w in descendants(app.home_content) if isinstance(w,mod.tk.Label))
            capture(root,f'startseite-{theme}')
            app.set_active_list(entry['id'])
            root.update()
            assert app.tree.winfo_ismapped() and not app.home_frame.winfo_ismapped()

            def form_check(dialog):
                dropdown=next(w for w in descendants(dialog) if isinstance(w,mod.LabelDropdown))
                due=next(w for w in descendants(dialog) if isinstance(w,mod.DueField))
                options=[w for w in descendants(dialog) if isinstance(w,(mod.tk.OptionMenu,mod.MacOptionMenu))]
                kind_menu=next(w for w in options if w.cget('text') == 'Aufgabe')
                priority=next(w for w in options if w.cget('text') == app.importance_choice_text(3))
                color=next(w for w in options if w.cget('text') == 'Keine Farbe')
                assert priority.cget('fg') == app.theme['priority_high']
                for widget,choices,colors in (
                    (priority,[app.importance_choice_text(i) for i in range(4)], [app.importance_color_key(i) for i in range(4)]),
                    (color,['Keine Farbe']+[n for n,k in app.ITEM_COLOR_CHOICES],['text']+[k for n,k in app.ITEM_COLOR_CHOICES]),
                ):
                    for index,(choice,key) in enumerate(zip(choices,colors)):
                        widget['menu'].invoke(index)
                        widget.update()  # Menübefehle laufen seit 3.32.0 im nächsten Leerlauf
                        assert widget.cget('fg') == app.theme[key]
                        if index:
                            assert str(widget['menu'].entrycget(index,'foreground')) == app.theme[key], (choice,key,widget['menu'].entrycget(index,'foreground'),app.theme[key])
                title_entry=next(w for w in descendants(dialog) if isinstance(w,mod.tk.Entry) and w.get()==task['text'])
                long_label=app.get_system_label('long')
                heading_label=app.get_system_label('heading')
                assert long_label in dropdown.labels and heading_label in dropdown.labels
                dropdown.toggle_label(long_label['id'])
                assert kind_menu.cget('text') == 'Langtext'
                assert not title_entry.winfo_manager()
                long_text=next(w for w in descendants(dialog) if isinstance(w,mod.tk.Text) and w.get('1.0','end-1c')==task['text'])
                long_text.delete('1.0','end')
                long_text.insert('1.0','Erste Zeile\nZweite Zeile')
                dropdown.toggle_label(heading_label['id'])
                assert kind_menu.cget('text') == 'Zwischenüberschrift'
                assert heading_label['id'] in dropdown.read() and long_label['id'] not in dropdown.read()
                assert not due.master.winfo_manager()
                assert due.date_entry.get() == today.strftime('%d.%m.%Y')
                dropdown.toggle_label(long_label['id'])
                assert long_text.get('1.0','end-1c') == 'Erste Zeile\nZweite Zeile'
                assert due.master.winfo_manager() == 'grid'
                assert custom['id'] in dropdown.read()
                dropdown._open_popup()
                row=dropdown._rows[custom['id']]
                before=row['chip'].cget('bg')
                chip_fill=row['chip'].fill
                dropdown._paint_row(custom['id'],hover=True)
                assert before == app.theme['input']
                assert row['chip'].cget('bg') == app.theme['hover']
                assert row['chip'].fill == chip_fill
                assert row['frame'].cget('bg') == app.theme['hover']
                assert row['mark'].cget('bg') == app.theme['hover']
                assert isinstance(row['mark'], mod.LabelChip)
                assert row['mark'].fill == app.theme['selection']
                dropdown._close_popup()
                capture(dialog,f'eingabe-{theme}')
                button(dialog,'Speichern').command()
            inspect_dialog(form_check)
            result=app.item_form_dialog(mode='edit',item=task)
            assert result['kind']=='long' and result['text']=='Erste Zeile\nZweite Zeile'
            assert result['due_time']=='09:30' and custom['id'] in result['labels']

            def settings_check(dialog):
                assert dialog.cget('bg')==app.theme['bg']
                fields=[w for w in descendants(dialog) if isinstance(w,mod.tk.Entry)]
                fields[0].delete(0,'end'); fields[0].insert(0,'Tim')
                fields[1].delete(0,'end'); fields[1].insert(0,'TV')
                checks=[w for w in descendants(dialog) if isinstance(w,mod.tk.Checkbutton)]
                checks[0].select()
                startup = next(w for w in descendants(dialog) if isinstance(w,(mod.tk.OptionMenu,mod.MacOptionMenu))
                               and w.cget('text') in ('Letzte Ansicht','Startseite','Vorlagen'))
                startup['menu'].invoke(1)
                dialog.update()  # Menübefehle laufen seit 3.32.0 im nächsten Leerlauf
                capture(dialog,f'einstellungen-{theme}')
                button(dialog,'Speichern').command()
            inspect_dialog(settings_check)
            app.show_settings_dialog()
            assert app.settings['profile_name']=='Tim' and app.settings['start_on_home']
            inspect_dialog(lambda dialog: capture(dialog,f'tastenkuerzel-{theme}'))
            app.show_shortcuts_dialog()
            inspect_dialog(lambda dialog: capture(dialog,f'ueber-glide-{theme}'))
            app.show_about_dialog()
            inspect_dialog(lambda dialog: capture(dialog,f'rueckfrage-{theme}'))
            assert app.ask_yes_no('In den Papierkorb verschieben?', 'Diese Liste kann später wiederhergestellt werden.') is False

        app.run_modal=original_modal
        before_ids={value['id'] for value in app.lists}
        app.set_home_view()
        new=app.create_list_from_template('daily')
        assert new['id'] not in before_ids
        assert app.view_mode=='list' and app.active_list_id==new['id']
        assert all(item['due']==today.isoformat() for item in new['items'])
        app.undo_last_change()
        assert {value['id'] for value in app.lists}==before_ids and app.view_mode==app.HOME_VIEW
        app.set_active_list(entry['id'])
        # Alte und neue TXT-Marker bleiben verlustfrei lesbar.
        for marker in (app.GROUP_MARKER,app.LEGACY_GROUP_MARKER):
            assert app.parse_txt_items([f'1. {marker}Gruppe'])[0]['kind']=='group'
        for marker in (app.IMPORTANCE_MARKERS[3],'\U0001F6A9 '):
            assert app.parse_clipboard_items([marker+'Wichtig'][0])[0]['importance']==3
        for importance in (1,2,3):
            out=io.StringIO()
            app.write_items_to_txt(out,[app.new_item('Test',importance=importance)],[])
            assert app.parse_txt_items(out.getvalue().splitlines())[0]['importance']==importance
        app.settings.update(profile_name='Tim',profile_logo='TV',start_on_home=True)
        app.save_settings()
        assert app.save_items()
        assert not reported_errors, reported_errors
        app.cancel_pending_callbacks()
        root.destroy()
        root=mod.tk.Tk()
        app=mod.ListApp(root)
        root.update()
        assert app.view_mode==app.HOME_VIEW and app.home_frame.winfo_ismapped()
        assert app.settings['profile_name']=='Tim' and app.settings['profile_logo']=='TV'
        assert app.home_summary()['total']==3
        assert app.settings['recent_lists']
    finally:
        app.cancel_pending_callbacks()
        root.destroy()

print('UI-Erweiterungen: OK (Farben, Artwechsel, Abstände, Startseite, Vorlagen, Einstellungen und Neustart)')
