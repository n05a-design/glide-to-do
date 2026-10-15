"""Echte native Setter und installierte Tcl-Klassenbindungen im eigenen Tk.

Readerstatus wird nur in diesem künstlichen Interpreter für den Scriptvertrag
simuliert. Dies ist ausdrücklich keine tatsächliche Screenreader-Abnahme.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import traceback


def run(report, script=None):
    result = dict(exitcode=1, nur_kuenstliche_daten=True, readerstatus='nur im eigenen Interpreter simuliert')
    with tempfile.TemporaryDirectory(prefix='glide-native-script-') as data:
        os.environ.update(GLIDE_DATA_DIR=data, GLIDE_TEST_MODE='1')
        import tkinter as tk
        from tkinter import ttk
        root = tk.Tk()
        root.withdraw()
        errors = []
        root.report_callback_exception = lambda *args: errors.append(''.join(traceback.format_exception(*args)))
        root.tk.createcommand('glide_script_bgerror', lambda message: errors.append(message))
        root.tk.call('proc', 'bgerror', 'message', 'glide_script_bgerror $message')
        try:
            result['tk'] = str(root.tk.call('package', 'present', 'Tk'))
            assert result['tk'] == '9.1.0'
            path = str(script) if script else str(root.tk.call('set', 'tk_library'))+'/accessibility.tcl'
            channel = root.tk.call('open', path, 'rb')
            try:
                original = root.tk.call('read', channel)
            finally:
                root.tk.call('close', channel)
            if isinstance(original, str):
                original = original.encode('utf-8')
            result['skript_sha256'] = hashlib.sha256(original).hexdigest()
            root.tk.call('rename', '::tk::accessible::check_screenreader', '::glide_saved_reader_check')
            root.tk.call('proc', '::tk::accessible::check_screenreader', '', 'return 1')
            root.tk.call('source', path)
            if root.tk.call('info', 'commands', '::tk::accessible::speak'):
                root.tk.call('proc', '::tk::accessible::speak', 'text', 'return')
            tree = ttk.Treeview(root, columns=('value',))
            identity = tree.insert('', 'end', text='Künstliche Prüfaufgabe', values=('Künstliche Prüfaufgabe',))
            tree.selection_set(identity)
            # Noch nicht gemappt: native Attributtabelle darf fehlen.
            try:
                root.tk.call('::tk::accessible::get_acc_role', str(tree))
            except tk.TclError:
                pass
            else:
                raise AssertionError('Gegenfixture braucht ein noch uninitialisiertes Widget.')
            root.tk.call('::tk::accessible::_updateselection', str(tree))
            plain = ttk.Treeview(root)
            plain.pack()
            tree.pack()
            root.deiconify()
            root.update_idletasks()
            root.update()
            root.tk.call('::tk::accessible::_updateselection', str(tree))
            assert root.tk.call('::tk::accessible::get_acc_role', str(plain))
            value = str(root.tk.call('::tk::accessible::get_acc_value', str(tree)))
            assert 'Künstliche Prüfaufgabe' in value, value
            path = str(tree)
            tree.destroy()
            root.tk.call('::tk::accessible::_updateselection', path)
            assert not errors, errors
            result.update(exitcode=0, checks=['Frühe Auswahl vor Map ohne Fehler',
                'Map initialisiert native Attribute und aktuelle Auswahl', 'Baum ohne Zusatzspalten initialisiert',
                'Entferntes Widget ohne verspäteten Setter'])
        except Exception as error:
            result.update(fehler=str(error), traceback=traceback.format_exc(), callback_errors=errors)
        finally:
            root.destroy()
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Native Tcl-Klassenbindung Exit', result['exitcode'])
    return result['exitcode']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bericht', type=Path, required=True)
    parser.add_argument('--skript', type=Path, help='Explizite eigene Baukopie; sonst tatsächlich installierte Scriptbytes')
    args = parser.parse_args()
    raise SystemExit(run(args.bericht, args.skript))
