"""Eigene vergängliche Glide-Instanz für tatsächliche Reader-Proben.

Nur die Anfangsfixture wird vorbereitet. Danach bedient der Reader-Prüfplatz
die echte Oberfläche; kein Steuerkanal führt Appbefehle aus. Diagnose und
Modellschnappschuss stammen ausschließlich aus dieser künstlichen Instanz.
"""
import argparse
import faulthandler
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback


def diagnostic_state(app, pid, callbacks):
    return dict(pid=pid, view=app.view_mode,
        tasks=[item for entry in app.lists for item in app.walk_items(entry.get('items', []))],
        inspector=getattr(app, '_detail_state', {}).get('item_id'), callback_errors=list(callbacks))


def run(app_path, exchange):
    exchange = exchange.resolve()
    exchange.mkdir(parents=True, exist_ok=True)
    if any(exchange.iterdir()):
        raise ValueError('Für die Reader-App einen eigenen neuen Diagnoseordner verwenden.')
    with tempfile.TemporaryDirectory(prefix='glide-reader400-') as data:
        os.environ.update(GLIDE_DATA_DIR=data, GLIDE_TEST_MODE='1')
        faulthandler.enable()
        sys.path.insert(0, str(app_path.parent))
        loader = importlib.machinery.SourceFileLoader('glide_reader400', str(app_path))
        mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = mod
        loader.exec_module(mod)
        root = mod.tk.Tk()
        root.geometry('1280x800+20+20')
        callbacks = []
        def record_error(message):
            callbacks.append(message)
            temporary = exchange/'callback-fehler.tmp'
            temporary.write_text(json.dumps(callbacks, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            temporary.replace(exchange/'callback-fehler.json')
        root.report_callback_exception = lambda *args: record_error(''.join(traceback.format_exception(*args)))
        # Auch native Tcl-Klassenbindungen des aktiven Readers können Fehler
        # auslösen. Im Prüfling protokollieren statt einen blockierenden
        # Fehlerdialog zu öffnen; jeder Eintrag lässt die Readerprobe scheitern.
        root.tk.createcommand('glide_reader_bgerror', lambda message:
            record_error('Tcl: '+message+'\n'+str(root.tk.call('set', '::errorInfo'))))
        root.tk.call('proc', 'bgerror', 'message', 'glide_reader_bgerror $message')
        app = mod.ListApp(root)
        if str(root.tk.call('package', 'provide', 'Tk')) != '9.1.0' or not app.tree._glide_accessibility.supported:
            root.destroy()
            raise RuntimeError('Reader-App braucht die eigene Tk-9.1-Laufzeit mit nativem Backend.')
        source = app.new_list_object('Reader-Prüfliste', [])
        app.lists.append(source)
        app.save_items()
        app.update_sidebar_list()
        app.set_active_list(source['id'])

        def write(name, value):
            temporary = exchange / (name + '.tmp')
            temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
            temporary.replace(exchange / (name + '.json'))

        def snapshot():
            if not root.winfo_exists():
                return
            value = diagnostic_state(app, os.getpid(), callbacks)
            focused = root.focus_get()
            value['tk_fokus'] = dict(pfad=str(focused), klasse=focused.winfo_class()) if focused else None
            write('zustand', value)
            root.after(150, snapshot)

        def ready():
            app.focus_entry()
            root.focus_force()
            app.entry.focus_set()
            write('bereit', dict(pid=os.getpid(), tk=str(root.tk.call('package', 'provide', 'Tk')),
                                  version=mod.APP_VERSION, plan_day_view=app.PLAN_DAY_VIEW, daten='ausschließlich temporäre künstliche Daten'))
            snapshot()

        root.after(500, ready)
        root.after(600_000, root.destroy)
        try:
            root.mainloop()
        finally:
            # on_close ist für die physische Reader-Probe vorhanden; ein
            # Prüfzeitlimit darf keine echten Nutzerfenster schließen.
            try:
                exists = bool(root.winfo_exists())
            except mod.tk.TclError:
                exists = False
            if exists:
                app.close_daily_planning()
                root.destroy()
            app.release_data_lock()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[2] / 'src/glide/app.pyw')
    parser.add_argument('--diagnose', type=Path, required=True)
    args = parser.parse_args()
    run(args.app.resolve(), args.diagnose)


if __name__ == '__main__':
    main()
