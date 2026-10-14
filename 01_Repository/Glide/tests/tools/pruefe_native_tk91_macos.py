"""Echte native NSAccessibility-Getter/Aktionen im eigenen Tk-Prüfprozess.

Kein Zugriff auf die Desktop-AX-Struktur oder fremde Prozesse. Ein grün
geprüfter Anbieter ist weiterhin keine tatsächliche VoiceOver-Abnahme.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import traceback


def run(library, report):
    with tempfile.TemporaryDirectory(prefix='glide-native-tk91-') as folder:
        os.environ['GLIDE_DATA_DIR'] = folder
        sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'src/glide'))
        import tkinter as tk
        from tkinter import ttk
        from accessibility import Attributes
        from accessibility_bindings import Binding, available
        from core_accessibility import entry_attributes
        from macos_native_accessibility import NativeAccessibility
        root = tk.Tk()
        root.title('Glide – künstliche native Zugangsprobe')
        root.geometry('500x360+20+20')
        checks, calls, callbacks, failures = [], [], [], []
        root.report_callback_exception = lambda *args: callbacks.append(''.join(traceback.format_exception(*args)))
        result = dict(exitcode=1, native_getter=True, nur_eigener_testprozess=True,
                      python=sys.version, tk=str(root.tk.call('package', 'provide', 'Tk')),
                      anbieter_sha256=hashlib.sha256(library.read_bytes()).hexdigest(),
                      voiceover_abnahme='offen; nativer Anbieter ersetzt keine Readerprobe',
                      checks=checks, failures=failures)
        def check(name, condition, detail):
            if condition:
                checks.append(name)
            else:
                failures.append({'pruefung':name, 'ist':detail})
        def pump():
            for _ in range(4):
                root.update_idletasks()
                root.update()
        try:
            supported = available(root.tk.call)
            result['vollstaendiger_backend_vertrag'] = supported
            check('Nativer Anbieter unterstützt den vollständigen Fokus-/Auswahlvertrag', supported, supported)
            # Zur unabhängigen Kalibrierung der übrigen nativen Verträge werden
            # diese eigenen Widgets auch bei einem fehlenden Fokuskommando
            # direkt registriert. Der fehlende Vertrag bleibt ein roter Fall.
            first = tk.Canvas(root, width=180, height=32, takefocus=True)
            first.pack()
            second = tk.Canvas(root, width=180, height=32, takefocus=True)
            second.pack()
            first_binding = Binding(first, lambda: Attributes('Button', 'Erste native Aktion', state=str(first.cget('state'))),
                                    action=lambda: calls.append('erste'), supported=True)
            Binding(second, lambda: Attributes('Button', 'Zweite native Aktion'), action=lambda: calls.append('zweite'), supported=True)
            entry = tk.Entry(root)
            entry.pack()
            text = '  Angebot prüfen 🏠'
            entry.insert(0, text)
            entry_binding = Binding(entry, lambda: entry_attributes(entry, 'Aufgabentitel'), supported=True)
            variable = tk.BooleanVar(value=False)
            checkbox = tk.Checkbutton(root, text='Unterlagen prüfen', variable=variable)
            checkbox.pack()
            Binding(checkbox, lambda: Attributes('Checkbutton', 'Unterlagen prüfen', value='1' if variable.get() else '0'),
                         action=lambda: variable.set(not variable.get()), supported=True)
            tree = ttk.Treeview(root, height=2)
            tree.insert('', 'end', iid='task', text='Angebot prüfen')
            tree.pack()
            selection = ['Angebot prüfen. Offen. Heute eingeplant.']
            tree_binding = Binding(tree, lambda: Attributes('Tree', 'Aufgaben', value=selection[0]), supported=True)
            pump()
            native = NativeAccessibility(root, library)
            values = {name: native.describe(widget) for name,widget in
                      (('button', first), ('entry', entry), ('checkbox', checkbox))}
            result['native_werte'] = values
            group = native.describe(tree)
            selection[0] = 'Unterlagen prüfen. Erledigt. Morgen eingeplant.'
            tree_binding.refresh(selection=True)
            pump()
            changed_group = native.describe(tree)
            result['native_auswahl'] = dict(vorher=group, nachher=changed_group)
            check('Native Aufgaben-Gruppe nennt ihren Bereich und die jeweils aktuelle Auswahl',
                  'Aufgaben' in group['label'] and 'Angebot prüfen' in group['label'] and
                  'Unterlagen prüfen' in changed_group['label'] and 'Erledigt' in changed_group['label'],
                  result['native_auswahl'])
            check('Native Rollen, deutscher Schaltflächentitel und unveränderter Unicode-Feldtext',
                  values['button']['role'] == 'AXButton' and values['button']['title'] == 'Erste native Aktion' and
                  values['entry']['role'] == 'AXTextField' and values['entry']['value'] == text and
                  values['checkbox']['role'] == 'AXCheckBox' and values['checkbox']['value'] == '0', values)
            check('Aktive native Bedienelemente melden sich als verfügbar',
                  all(value['enabled'] is True for value in values.values()), values)
            check('Native Kennung bleibt für dasselbe Widget stabil',
                  values['button']['identifier'] == native.describe(first)['identifier'], native.describe(first))
            entry.focus_force()
            pump()
            focused, unfocused = native.describe(entry), native.describe(first)
            result['nativer_fokus'] = dict(fokussiert=focused, nicht_fokussiert=unfocused)
            check('Nativer Fokus unterscheidet das aktuelle Feld von anderen Widgets',
                  focused['focused'] is True and unfocused['focused'] is False, result['nativer_fokus'])
            check('Native Bearbeitungshilfe ist über den offiziellen NSAccessibility-Getter erreichbar',
                  focused['help'] == entry_attributes(entry, 'Aufgabentitel').help, focused)
            pressed = native.press(checkbox)
            pump()
            checked = native.describe(checkbox)
            check('Echter Checkboxwert und AXPress', pressed and variable.get() and checked['value'] == '1', checked)
            first_pressed, second_pressed = native.press(first), native.press(second)
            pump()
            result['native_aktionen'] = list(calls)
            check('Zwei vor der Ereignisverarbeitung ausgelöste native Aktionen behalten jeweils ihr eigenes Ziel',
                  first_pressed and second_pressed and calls == ['erste', 'zweite'], list(calls))
            before = list(calls)
            first.configure(state='disabled')
            first_binding.refresh()
            pump()
            disabled_press = native.press(first)
            pump()
            check('Deaktivierte native Aktionen werden bereits vom Anbieter verweigert',
                  disabled_press is False and calls == before, dict(angenommen=disabled_press, aufrufe=list(calls)))
            removed = tk.Canvas(root, width=40, height=20)
            removed.pack()
            Binding(removed, lambda: Attributes('Button', 'Entfernte Aktion'),
                    action=lambda: calls.append('entfernt'), supported=True)
            pump()
            root.tk.createcommand('bgerror', lambda message: callbacks.append('Tcl: '+message))
            native.press(removed)
            removed.destroy()
            pump()
            check('Eine vorgemerkte Aktion eines entfernten Widgets bleibt ohne Aufruf und Tcl-Fehler',
                  calls == before and not callbacks, dict(aufrufe=list(calls), fehler=list(callbacks)))
            entry.configure(state='disabled')
            entry_binding.refresh()
            pump()
            disabled = native.describe(entry)
            result['schreibgeschuetztes_feld'] = disabled
            check('Schreibgeschützter Feldinhalt bleibt nativ lesbar und meldet sich als nicht bearbeitbar',
                  not disabled['ignored'] and disabled['enabled'] is False and disabled['value'] == text, disabled)
            result['callback_errors'] = callbacks
            result['exitcode'] = int(bool(failures or callbacks))
        except BaseException as error:
            result.update(fehler=str(error), traceback=traceback.format_exc(), callback_errors=callbacks)
        finally:
            root.destroy()
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        print('Native Tk-9.1-Anbieterprobe Exit', result['exitcode'])
        return result['exitcode']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bibliothek', type=Path, required=True)
    parser.add_argument('--bericht', type=Path, required=True)
    args = parser.parse_args()
    return run(args.bibliothek, args.bericht)


if __name__ == '__main__':
    raise SystemExit(main())
