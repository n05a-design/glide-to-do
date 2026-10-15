"""Aufgaben-Kernablauf mit künstlichen Daten und echten Tk-Widgets.

Attribut- und Tastaturprüfungen sind keine Screenreader-Abnahme. --nativ
verlangt zusätzlich die eigene Tk-9.1-Laufzeit und deren tatsächliche Kommandos.
OS-Anbieter und Reader-Ausgaben werden in getrennten Proben geprüft.
"""
import argparse
import copy
from datetime import date, timedelta
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import traceback


def run(app_path, report=None, *, native=False):
    checks, callbacks, expected_errors = [], [], []
    with tempfile.TemporaryDirectory(prefix='glide-zugang400-') as folder:
        os.environ.update(GLIDE_DATA_DIR=folder, GLIDE_TEST_MODE='1')
        sys.path.insert(0, str(app_path.parent))
        loader = importlib.machinery.SourceFileLoader('glide_zugang400', str(app_path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        core = getattr(mod, 'glide_core_accessibility', None)
        assert core is not None, 'Semantik des Aufgaben-Kernablaufs fehlt'
        root = mod.tk.Tk()
        root.geometry('1280x800+20+20')
        root.report_callback_exception = lambda *args: callbacks.append(''.join(traceback.format_exception(*args)))
        app = mod.ListApp(root)
        app.show_info = app.show_warning = lambda *args, **kwargs: None
        app.show_error = lambda *args, **kwargs: expected_errors.append(args)

        def pump():
            for _ in range(4):
                root.update_idletasks()
                root.update()
                time.sleep(.01)

        def attributes(widget):
            binding = widget._glide_accessibility
            result = binding.attributes()
            assert result is not None
            return result

        def fresh():
            return app.find_item_in_lists(identity)[0]

        def step():
            return next(widget for widget in app.iter_descendants(app.detail_pane)
                        if getattr(widget, '_accessible_step_index', None) == 0)

        try:
            pump()
            runtime = str(root.tk.call('package', 'provide', 'Tk'))
            supported = bool(app.tree._glide_accessibility.supported)
            if native:
                assert runtime == '9.1.0', ('Eigene Tk-9.1.0-Laufzeit erforderlich', runtime)
                assert supported, 'Kein natives Accessibility-Backend; gleichnamige Stubs genügen nicht'
            assert attributes(app.entry).name == 'Neue Aufgabe'
            assert attributes(app.search_entry).name == 'Aufgaben suchen'
            source = app.new_list_object('Zugangsprobe', [])
            app.lists.append(source)
            app.save_items()
            app.update_sidebar_list()
            app.set_active_list(source['id'])
            pump()
            app.entry.focus_force()
            app.entry.delete(0, 'end')
            app.entry.insert(0, 'Angebot prüfen')
            app.entry_placeholder_active = False
            app.entry.event_generate('<Return>')
            pump()
            assert len(source['items']) == 1, 'Enter muss genau eine Aufgabe erfassen'
            identity = source['items'][0]['id']
            assert fresh()['text'] == 'Angebot prüfen'
            checks.append('Echte Erfassung mit Enter: genau eine Aufgabe; Eingabe und Suche eindeutig benannt')

            app.search_entry.focus_force()
            app.search_entry.delete(0, 'end')
            app.search_entry.insert(0, 'Angebot')
            app.search_placeholder_active = False
            app.search_entry.event_generate('<KeyRelease>')
            pump()
            assert 'Angebot' in attributes(app.search_entry).value
            assert any(app.tree.item(row, 'text') or app.tree.item(row, 'values') for row in app.tree.get_children())
            app.search_entry.event_generate('<Escape>')
            pump()
            app.set_active_list(source['id'])
            app.tree.selection_set(identity)
            app.tree.focus(identity)
            app.tree.focus_force()
            pump()
            value = attributes(app.tree).value
            assert 'Angebot prüfen' in value and 'Offen' in value
            assert 'Nicht eingeplant' in value and 'Ohne Fälligkeit' in value
            checks.append('Suche und echte Zeilenauswahl: aktueller Aufgabentext, Status und getrennte Datumsarten')
            before, depth = copy.deepcopy(fresh()), len(app.undo_stack)
            for tree in (app.tree, app.sidebar_listbox):
                tree.focus_force()
                pump()
                tree.event_generate('<Control-Tab>')
                pump()
                current = root.focus_get()
                assert current is not None and current is not tree, 'Strg+Tab bleibt im Baum hängen'
                current.event_generate('<Control-Shift-Tab>')
                pump()
                assert root.focus_get() is tree, 'Rückwärtiger Bereichswechsel verliert den Baum'
            assert fresh() == before and len(app.undo_stack) == depth
            checks.append('Strg+Tab verlässt Aufgaben-/Listenbaum vorwärts und zurück ohne Daten-/Undoänderung; Tab-Einrücken bleibt erhalten')

            menu = app.build_quick_plan_menu(item_ids=(identity,))
            try:
                today = next(index for index in range(menu.index('end')+1)
                             if menu.type(index) == 'command' and menu.entrycget(index, 'label').startswith('Heute'))
                menu.invoke(today)
                pump()
            finally:
                menu.destroy()
            assert fresh()['planned_date'] == date.today().isoformat() and not fresh().get('due')
            app.set_today_view()
            pump()
            assert app.open_task_inspector(identity)
            pump()
            fields = app._detail_state['fields']
            assert attributes(fields['text']).name == 'Aufgabentitel'
            assert attributes(fields['description']).name == 'Beschreibung'
            assert attributes(fields['planned'].date_entry).name == 'Bearbeitungstag'
            assert attributes(fields['due'].date_entry).name == 'Fälligkeit'
            assert fresh()['planned_date'] == date.today().isoformat()
            fields['due'].date_entry.delete(0, 'end')
            fields['due'].date_entry.insert(0, (date.today()+timedelta(days=2)).strftime('%d.%m.%Y'))
            fields['description'].delete('1.0', 'end')
            fields['description'].insert('1.0', 'Erste Zeile\n\n  Zweite Zeile 🏠')
            assert app.commit_detail_pane()
            pump()
            assert fresh()['description'] == 'Erste Zeile\n\n  Zweite Zeile 🏠'
            assert fresh()['due'] == (date.today()+timedelta(days=2)).isoformat()
            assert fresh()['planned_date'] == date.today().isoformat()
            checks.append('Heute-Planungsaktion und gemeinsamer Inspektor: Fälligkeit getrennt, Unicode/Absätze gespeichert')

            app.add_detail_pane_step(identity, 'Unterlagen prüfen')
            pump()
            checkbox = step()
            assert isinstance(checkbox, mod.tk.Checkbutton)
            assert checkbox.cget('variable') and attributes(checkbox).value == '0'
            assert not checkbox._accessible_variable.get()
            depth = len(app.undo_stack)
            checkbox.focus_force()
            checkbox.event_generate('<space>')
            pump()
            assert fresh()['checklist'][0]['done'] and len(app.undo_stack) == depth+1
            assert step()._accessible_variable.get() and attributes(step()).value == '1'
            app.undo_last_change()
            pump()
            assert not fresh()['checklist'][0]['done'] and not step()._accessible_variable.get(), {
                'modell': fresh()['checklist'], 'variable': step()._accessible_variable.get(),
                'undo': len(app.undo_stack), 'vorher': depth}
            checks.append('Echte Checkbox per Leertaste: kanonische 0/1-Variable, ein Undo, frische Objekte nach Undo')

            disk = Path(mod.SAVE_FILE).read_bytes()
            before = copy.deepcopy(fresh())
            depth = len(app.undo_stack)
            original = app.write_json_atomic
            def fail_save(path, payload):
                if str(path) == str(mod.SAVE_FILE):
                    raise OSError('Absichtlicher Schreibfehler in synthetischen Daten')
                return original(path, payload)
            app.write_json_atomic = fail_save
            try:
                step().invoke()  # Der native Tk-Mausweg toggelt die Variable vor command.
                pump()
                assert fresh() == before and Path(mod.SAVE_FILE).read_bytes() == disk
                assert len(app.undo_stack) == depth and not step()._accessible_variable.get()
            finally:
                app.write_json_atomic = original
            assert expected_errors
            app._detail_commit_error = None
            app._data_read_only = True
            try:
                step().invoke()
                pump()
                assert fresh() == before and not step()._accessible_variable.get()
                assert attributes(step()).state == 'disabled'
            finally:
                app._data_read_only = False
            checks.append('Echter Dateischreibfehler und nachträglicher Schreibschutz: Modell, Datei, Undo und Haken unverändert')

            fixture = Path(folder)/'Angebot.txt'
            fixture.write_text('Künstlicher Anhang der Zugangsprobe.', encoding='utf-8')
            attachments = app._store_pending_attachments([{'name':fixture.name, 'pending_path':str(fixture)}])
            assert attachments
            details = app.item_details_snapshot(fresh())
            details['attachments'] = attachments
            app.apply_task_edit(fresh(), details)
            app.sync_detail_pane(force=True)
            pump()
            attachment = next(widget for widget in app.iter_descendants(app.detail_pane)
                if isinstance(widget, mod.tk.Label) and hasattr(widget, '_glide_accessibility') and
                   attributes(widget).name == 'Anhang öffnen: Angebot.txt')
            opened = []
            app.open_external_path = lambda path: opened.append(str(path))
            attachment.focus_force()
            attachment.event_generate('<Return>')
            pump()
            attachment.event_generate('<space>')
            pump()
            expected = str(app.resolve_attachment_path(attachments[0]))
            assert opened == [expected, expected]
            binding = attachment._glide_accessibility
            app._detail_state['fields']['attachments'].clear()
            binding.invoke()
            assert opened == [expected, expected], 'Entfernter Anhang darf keine Aktion mehr auslösen'
            checks.append('Eigener Anhang mit Enter/Leertaste erreichbar; aktueller Dateiname und entfernte Zielprüfung ohne externes Öffnen')

            app.reload_task_inspector()
            pump()
            choice = next(widget for widget in app.iter_descendants(app.detail_pane)
                          if isinstance(widget, mod.AppOptionMenu) and attributes(widget).name == 'Wichtigkeit')
            labels = app._detail_state['fields']['labels']
            before = copy.deepcopy(fresh())
            depth = len(app.undo_stack)
            choice.focus_force()
            choice.event_generate('<Return>')
            pump()
            assert choice._popup is not None
            app._data_read_only = True
            choice._choices.event_generate('<Down>')
            choice._choices.event_generate('<Return>')
            pump()
            assert choice._popup is None and fresh() == before
            choice.event_generate('<space>')
            pump()
            assert choice._popup is None and attributes(choice).state == 'disabled'
            app._data_read_only = False
            labels.summary_label.focus_force()
            labels.summary_label.event_generate('<Return>')
            pump()
            assert labels._popup is not None
            selected = list(labels.selected_ids)
            app._data_read_only = True
            labels._popup.event_generate('<space>')
            pump()
            assert labels.selected_ids == selected
            labels._close_popup()
            labels.summary_label.event_generate('<Return>')
            pump()
            assert labels._popup is None and attributes(labels.summary_label).state == 'disabled'
            app.sync_detail_pane(force=True)
            pump()
            readonly = [widget for widget in app.iter_descendants(app.detail_pane)
                        if isinstance(widget, mod.AppOptionMenu)]
            assert readonly and all(str(widget.cget('state')) == 'disabled' for widget in readonly)
            assert fresh() == before and len(app.undo_stack) == depth
            app._data_read_only = False
            app.reload_task_inspector()
            pump()
            checks.append('Schreibschutz auch während offener Auswahl: Wichtigkeit/Labels verweigern Tastatur- und native Aktionen ohne Modell-/Undoänderung')

            old = step()._glide_accessibility
            command = old.command
            app.close_task_inspector(discard=True)
            pump()
            if supported:
                before = copy.deepcopy(fresh())
                old.invoke()
                assert not old.widget.winfo_ismapped() and fresh() == before
                assert app.open_task_inspector(identity)
                pump()
                assert old.closed and old.job is None and old.command is None
                assert not root.tk.call('info', 'commands', command)
            checks.append('Ausgeblendeter Inspektor verweigert Aktionen; Neuaufbau gibt alte Bindungen, Aufträge und Tcl-Kommandos frei')
            app.close_task_inspector(discard=True)
            app.settings['ui_font_size'] = 'gross'
            app.apply_ui_font()
            root.geometry('860x700+20+20')
            pump()
            assert app.open_task_inspector(identity)
            pump()
            canvas = app._detail_state['canvas']
            controller = canvas._glide_inspector_focus
            app._detail_state['fields']['text'].focus_force()
            pump()
            before, depth = copy.deepcopy(fresh()), len(app.undo_stack)
            reached = False
            for _ in range(65):
                focused = root.focus_get()
                assert focused is not None, 'Tastaturfokus verloren'
                if str(focused).startswith(str(canvas)+'.'):
                    top = focused.winfo_rooty()-canvas.winfo_rooty()
                    height = focused.winfo_height()
                    assert top >= 0 and (height > canvas.winfo_height()-16 or top+height <= canvas.winfo_height()), (
                        'Fokussiertes Inspektorfeld außerhalb der sichtbaren Fläche', focused.winfo_class(),
                        top, height, canvas.winfo_height())
                if getattr(focused, '_accessible_step_index', None) == 0:
                    reached = True
                    break
                focused.event_generate('<Control-Tab>')
                pump()
            assert reached, 'Checkliste per Bereichswechsel nicht erreichbar'
            title = app._detail_state['fields']['text']
            for _ in range(65):
                focused = root.focus_get()
                if focused is title:
                    break
                focused.event_generate('<Control-Shift-Tab>')
                pump()
            assert root.focus_get() is title
            assert 0 <= title.winfo_rooty()-canvas.winfo_rooty() <= canvas.winfo_height()-title.winfo_height()
            assert fresh() == before and len(app.undo_stack) == depth, 'Bereichswechsel darf Inhalte nicht verändern'
            app.sync_detail_pane(force=True)
            pump()
            assert controller.closed and controller.job is None and controller.canvas is None
            checks.append('860×700/große Schrift: Strg+Tab vor/zurück hält fokussierte Inspektorfelder sichtbar; Modell/Undo unverändert, alter Scrollauftrag freigegeben')
            assert not callbacks, callbacks
            result = dict(exitcode=0, version=mod.APP_VERSION, tk=runtime, native_backend=supported,
                          checks=checks, callback_errors=callbacks,
                          app_sha256=hashlib.sha256(app_path.read_bytes()).hexdigest(),
                          reader_abnahme='offen; Attribut-/Tastaturprüfung ersetzt keine tatsächliche Readerausgabe')
            if report:
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            print(json.dumps(result, ensure_ascii=False))
        except Exception as error:
            if report:
                report.parent.mkdir(parents=True, exist_ok=True)
                report.write_text(json.dumps(dict(exitcode=1, checks=checks, fehler=str(error) or type(error).__name__,
                    ort=f'{Path(traceback.extract_tb(error.__traceback__)[-1].filename).name}:{traceback.extract_tb(error.__traceback__)[-1].lineno}',
                    callback_errors=callbacks, app_sha256=hashlib.sha256(app_path.read_bytes()).hexdigest()),
                    ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            raise
        finally:
            try:
                if root.winfo_exists():
                    app.close_daily_planning()
                app.cancel_pending_callbacks()
                app.release_data_lock()
            finally:
                if root.winfo_exists():
                    root.destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[2] / 'src/glide/app.pyw')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--nativ', action='store_true')
    args = parser.parse_args()
    run(args.app.resolve(), args.report, native=args.nativ)


if __name__ == '__main__':
    main()
