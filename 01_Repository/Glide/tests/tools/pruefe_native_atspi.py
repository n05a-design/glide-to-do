"""Externer AT-SPI-Verbraucher einer eigenen Linux-CI-Testinstanz.

Mit dem System-Python samt gi/Atspi starten, getrennt vom Python/Tk der App.
Es wird ausschließlich der ausdrücklich benannte Testprozess gelesen. Diese
OS-Schnittstellenprobe ist noch kein Nachweis tatsächlicher Orca-Sprachausgabe.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import time
import traceback


def text_values(text_interface, accessible):
    # Accessible.get_text() ist in PyGObject ein gleichnamiger Zugriff auf
    # das Interface. Die Methoden mit Offsets explizit auswählen.
    actual = text_interface.get_text(accessible, 0, -1)
    count = text_interface.get_character_count(accessible)
    caret = text_interface.get_caret_offset(accessible)
    prefix = text_interface.get_text(accessible, 0, min(2, count))
    return actual, count, caret, prefix


def run(pid, name, expected, report):
    if (sys.platform != 'linux' or os.environ.get('GITHUB_ACTIONS') != 'true'
            or os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'):
        raise RuntimeError('AT-SPI-Verbraucher nur im eigenen vergänglichen Linux-Hosted-CI-Prüfstand.')
    import gi
    gi.require_version('Atspi', '2.0')
    from gi.repository import Atspi, GLib
    result = dict(exitcode=1, pid=pid, eigener_testprozess=True, orca_abnahme='getrennt offen')
    try:
        desktop = Atspi.get_desktop(0)
        deadline = time.monotonic()+20
        application = None
        while time.monotonic() < deadline:
            for index in range(desktop.get_child_count()):
                child = desktop.get_child_at_index(index)
                if child is not None and child.get_process_id() == pid:
                    application = child
                    break
            if application is not None:
                break
            time.sleep(.1)
        assert application is not None, 'Eigene Tk-Instanz ist nicht im AT-SPI registriert'
        queue, seen, field = [application], set(), None
        while queue:
            node = queue.pop(0)
            if node is None or node in seen:
                continue
            seen.add(node)
            assert len(seen) <= 4096, 'Unerwartet großer Accessibility-Baum der kleinen Testfixture'
            assert node.get_process_id() == pid, 'Fremder Prozess darf nicht gelesen werden'
            if node.get_name() == name:
                field = node
                break
            queue.extend(node.get_child_at_index(index) for index in range(node.get_child_count()))
        assert field is not None, 'Feld nativ nicht auffindbar: ' + name
        text = field.get_text_iface()
        assert text is not None, 'Benanntes Eingabefeld bietet kein natives AtspiText'
        actual, count, caret, prefix = text_values(Atspi.Text, text)
        result.update(name=field.get_name(), role=field.get_role_name(), text=actual,
                      character_count=count, caret=caret, besuchte_eigene_knoten=len(seen))
        assert actual == expected, ('Native Textschnittstelle liefert einen anderen Inhalt', actual, expected)
        assert count == len(expected) and 0 <= caret <= count, (count, caret)
        assert prefix == expected[:2], 'AT-SPI-Zeichenoffsets müssen Unicode-Zeichen zählen'
        result['exitcode'] = 0
    except BaseException as error:
        result.update(fehler=str(error), traceback=traceback.format_exc())
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Externe native AT-SPI-Textprobe Exit', result['exitcode'])
    return result['exitcode']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--text', required=True)
    parser.add_argument('--bericht', type=Path, required=True)
    args = parser.parse_args()
    return run(args.pid, args.name, args.text, args.bericht)


if __name__ == '__main__':
    raise SystemExit(main())
