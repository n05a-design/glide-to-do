"""Aufnahmen aller Ansichten und Fenster für die Designprüfung (Linux/Xvfb, künstliche Showcase-Daten).

Zwei Prozesse je Konfiguration: `--prep` spielt den Showcase ein und setzt Schrift/Design/Hinweise,
der zweite Aufruf startet frisch und nimmt auf (eine Tk-Instanz je Prozess).

    xvfb-run -a -s "-screen 0 1920x1200x24" python3 -B aufnahmen.py --data <leer> --out <Ziel> --prep [Optionen]
    xvfb-run -a -s "-screen 0 1920x1200x24" python3 -B aufnahmen.py --data <dasselbe> --out <Ziel> [Optionen]

Optionen: --geo 1280x800, --design light|dark|glass_light …, --font klein|mittel|gross, --hints, --scope all|views|dialogs.
Benötigt ImageMagick (`import`). Bilder bleiben lokal (keine Fensterbilder versionieren).
"""
import faulthandler; faulthandler.dump_traceback_later(900, exit=True)
import argparse, json, re, subprocess, sys, tempfile, time, traceback, pathlib
from aufnahmen_basis import *
p = argparse.ArgumentParser()
p.add_argument('--geo', default='1280x800'); p.add_argument('--design', default='light')
p.add_argument('--font', default='mittel'); p.add_argument('--hints', action='store_true')
p.add_argument('--scope', default='all'); p.add_argument('--data', required=True); p.add_argument('--prep', action='store_true'); p.add_argument('--out', required=True); p.add_argument('--tag', default='')
a = p.parse_args()
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
log = {'config': vars(a), 'shots': [], 'errors': []}
tag = a.tag or f"{a.geo}_{a.design}_{a.font}{'_hinweise' if a.hints else ''}"
counter = [0]

if True:
    t = a.data
    mod = load(t)
    for n in ('showinfo', 'showwarning', 'showerror'):
        setattr(mod.messagebox, n, lambda *x, **k: None)
    mod.messagebox.askyesno = lambda *x, **k: False
    import tkinter.filedialog as _fd
    for _n in ('askdirectory','askopenfilename','askopenfilenames','asksaveasfilename'):
        setattr(_fd, _n, lambda *x, **k: '')
        if hasattr(mod, 'filedialog'): setattr(mod.filedialog, _n, lambda *x, **k: '')
    def start():
        root = mod.tk.Tk(); root.geometry(a.geo + '+0+0')
        root.report_callback_exception = lambda *e: log['errors'].append(''.join(traceback.format_exception(*e))[-500:])
        app = mod.ListApp(root)
        app.show_info = app.show_warning = lambda *x, **k: None
        return root, app
    G = {}
    def settle(n=6):
        for _ in range(n):
            G['root'].update_idletasks(); G['root'].update()
    if a.prep:
      root, app = start(); G['root'] = root
      settle()
      app.restore_app_backup(str(SHOWCASE), sections={'tasks': True, 'settings': True, 'templates': True, 'activity': True}, show_success=False)
      settle()
      app.settings['ui_font_size'] = a.font
      app.settings['show_hints'] = bool(a.hints)
      app.set_design(a.design, apply_now=True)
      app.save_settings()
    # Neustart, damit Schrift/Design wie beim Nutzer aus den Einstellungen kommen
    def ende():
        root, app = G['root'], G['app']
        def unbind_tree(widget):
            for child in widget.winfo_children(): unbind_tree(child)
            for seq in widget.bind(): widget.unbind(seq)
        unbind_tree(root)
        for seq in root.tk.splitlist(root.tk.call('bind', 'all')): root.unbind_all(seq)
        pv = getattr(app, '_previews', None)
        if pv is not None:
            pv.close()
            th = getattr(getattr(pv, '_conversions', None), '_thread', None)
            if th is not None: th.join(30)
        app.cancel_pending_callbacks()
        for job in root.tk.splitlist(root.tk.call('after', 'info')): root.after_cancel(job)
        if hasattr(app, 'finish_recovery_session'): app.finish_recovery_session()
        app.release_data_lock()
        try: root.destroy()
        except mod.tk.TclError: pass
    if a.prep:
        G['app'] = app
        ende(); print('vorbereitet'); sys.exit(0)
    root, app = start(); G['root'] = root; G['app'] = app; settle(10)
    print('Listen nach Neustart:', len(app.lists), 'Schrift', app.settings.get('ui_font_size'), 'Design', app.settings.get('design'))
    root.geometry(a.geo + '+0+0'); settle(10)

    def shot(widget, name):
        settle(6)
        counter[0] += 1
        safe = re.sub(r'[^A-Za-z0-9ÄÖÜäöüß_-]+', '_', name)[:60]
        f = out / f"{tag}__{counter[0]:03d}_{safe}.png"
        x, y, w, h = widget.winfo_rootx(), widget.winfo_rooty(), widget.winfo_width(), widget.winfo_height()
        r = subprocess.run(['import', '-window', 'root', '-crop', f'{w}x{h}+{x}+{y}', '+repage', str(f)], capture_output=True)
        log['shots'].append({'file': f.name, 'name': name, 'geom': [x, y, w, h], 'ok': f.exists()})

    def modal(dialog, parent=None):
        try:
            dialog.configure(bg=app.theme['bg']); app.ensure_dialog_min_width(dialog); app.bring_dialog_to_front(dialog)
        except Exception as e: log['errors'].append(f'modal-prep: {e}')
        settle(8)
        title = ''
        try: title = dialog.title()
        except Exception: pass
        shot(dialog, 'Dialog_' + (title or type(dialog).__name__))
        try: dialog.destroy()
        except Exception: pass
    app.run_modal = modal

    def view(name, fn):
        try:
            fn(); settle(10)
            shot(root, name)
        except Exception as e:
            log['errors'].append(f'{name}: {e!r} ' + traceback.format_exc()[-400:])

    def dialog(name, fn):
        print('>>', name, flush=True)
        before = {str(w) for w in root.winfo_children()}
        try:
            fn(); settle(8)
        except Exception as e:
            log['errors'].append(f'{name}: {e!r} ' + traceback.format_exc()[-400:])
        for w in list(root.winfo_children()):
            if str(w) not in before and isinstance(w, mod.tk.Toplevel) and w.winfo_exists():
                try:
                    if w.winfo_ismapped() and w.winfo_width() > 20:
                        shot(w, 'Fenster_' + (w.title() or name))
                    w.destroy()
                except Exception as e: log['errors'].append(f'{name} toplevel: {e}')
        settle(4)

    L = {e['title']: e for e in app.lists}
    def lid(prefix):
        return next(e['id'] for e in app.lists if e['title'].startswith(prefix))
    liste = lid('Vermarktung'); seite = lid('Parkquartier'); notiz = lid('Abstimmung'); galerie = lid('Bildwelt')
    zeichnung = lid('Quartier'); leer = lid('Eingang'); rhythmus = lid('Wiedervorlagen')
    folder = app.folders[0]['id']

    views = [
        ('Startseite', app.set_home_view), ('Heute', app.set_today_view),
        ('Tagesplan', app.set_plan_day_view), ('Überfällig', app.set_overdue_view),
        ('Labels', app.set_labels_view), ('Vorlagen', app.set_template_view),
        ('Papierkorb', app.set_trash_view), ('Bibliothek', app.set_library_view),
        ('Seitenübersicht', app.set_pages_view), ('Notizübersicht', app.set_notes_view),
        ('Zeichnungsübersicht', app.set_drawings_view),
        ('Liste', lambda: app.set_active_list(liste)),
        ('Liste_Tabelle', lambda: (app.set_active_list(liste), app.set_table_view())),
        ('Liste_Pinnwand', lambda: (app.set_active_list(liste), app.open_board_view())),
        ('Liste_Listenansicht_zurück', lambda: (app.set_active_list(liste), app.open_list_view())),
        ('Liste_Kalender', lambda: (app.set_active_list(liste), app.open_calendar_view())),
        ('Liste_Rhythmus', lambda: app.set_active_list(rhythmus)),
        ('Liste_leer_Eingang', lambda: app.set_active_list(leer)),
        ('Seite', lambda: app.set_active_list(seite)),
        ('Notiz', lambda: app.set_active_list(notiz)),
        ('Galerie', lambda: app.set_active_list(galerie)),
        ('Zeichnung', lambda: app.set_active_list(zeichnung)),
        ('Ordner', lambda: app.set_active_folder(folder)),
        ('Verlauf', app.open_history_view),
    ]
    if a.scope in ('all', 'views'):
        for n, f in views: view(n, f)
        # Inspektor und Nebenansicht
        def inspector():
            app.set_active_list(liste); settle(4)
            it = next(i for i in app.items if i.get('text'))
            app.themed_item_details_dialog(it)
        view('Liste_Inspektor', inspector)
        try: app.close_task_inspector()
        except Exception: pass
        def side():
            app.set_active_list(liste); settle(4)
            app.open_side_view(seite)
        view('Liste_mit_Nebenansicht_Seite', side)
        try: app.close_side_view()
        except Exception as e: log['errors'].append(f'close_side_view: {e}')
        # Kompaktmodus
        def compact():
            app.set_active_list(liste); app.toggle_compact_mode()
        view('Kompaktmodus_Liste', compact)
        view('Kompaktmodus_Seite', lambda: app.set_active_list(seite))
        view('Kompaktmodus_Heute', app.set_today_view)
        try: app.toggle_compact_mode()
        except Exception: pass
        view('Seitenleiste_schmal', lambda: (app.set_active_list(liste), app.toggle_sidebar_narrow()))
        try: app.toggle_sidebar_narrow()
        except Exception: pass
        view('Seitenleiste_aus', lambda: (app.set_active_list(seite), app.toggle_sidebar()))
        try: app.toggle_sidebar()
        except Exception: pass
    if a.scope in ('all', 'dialogs'):
        app.set_active_list(liste); settle(4)
        for n in ('show_about_dialog', 'show_release_notes_dialog', 'open_error_log', 'show_shortcuts_dialog',
                  'show_settings_dialog', 'show_manual_dialog', 'show_home_tiles_dialog', 'show_storage_status',
                  'show_backup_catalog', 'show_quick_capture', 'open_label_manager', 'create_new_list',
                  'create_new_folder', 'show_busy_calendar_dialog', 'show_exchange_export_dialog',
                  'show_print_dialog', 'show_table_columns_dialog',
                  'show_calendar_export_dialog', 'show_exchange_spec_dialog', 'open_calendar_dialog',
                  'show_journal_filter_dialog'):
            fn = getattr(app, n, None)
            if fn: dialog(n, fn)
        dialog('Fälligkeit', lambda: app.themed_due_dialog('2026-11-03', '09:30'))
        def palette(name, opener):
            print('>>', name, flush=True)
            def grab():
                try:
                    settle(6); shot(root, name)
                finally:
                    try:
                        w = root.focus_get() or root
                        w.event_generate('<Escape>')
                    except Exception as e: log['errors'].append(f'{name} esc: {e}')
            job = root.after(900, grab)
            try:
                opener()
                ende_t = time.time() + 1.6
                while time.time() < ende_t:
                    root.update_idletasks(); root.update(); time.sleep(0.02)
            except Exception as e:
                log['errors'].append(f'{name}: {e!r}')
        palette('Aktionsauswahl_Liste', app.show_actions_dialog)
        app.set_active_list(seite); settle(4)
        palette('Aktionsauswahl_Seite', app.show_actions_dialog)
    try: ende()
    except Exception as e: log['errors'].append(f'ende: {e}')
(out / f'{tag}__log.json').write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(log['shots']), 'Aufnahmen,', len(log['errors']), 'Fehler')
for e in log['errors'][:30]: print(' -', e[:300].replace('\n', ' | '))
