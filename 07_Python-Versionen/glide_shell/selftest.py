# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 11: Selbsttest einer übernommenen Glide Shell auf dem Zielrechner.

Start: `python -m glide_shell.selftest` mit dem Ordner über `glide_shell` im
Suchpfad. Der Test öffnet ein kleines, sofort wieder geschlossenes Tk-Fenster
und prüft jeden Baustein mit echtem Tk: Paketversion, Geometrie, Systemmodus,
Wiederholen-Stapel, Zeitgeberbereich, Übergang, Menüleiste, Bedienelement,
Textkürzung mit echter Schrift, Aktionsauswahl, Pfadauflösung ohne
Seiteneffekt und modalen Dialog mit Griff und Freigabe. Ausgabe je Prüfung `ok` oder `FAIL`,
Die Prüfungen greifen auch unter
`python -O`. Exitcode 0 nur, wenn alles bestanden ist; 2, wenn kein Tk-Fenster möglich ist
(etwa ohne Anzeige). Meldungen sind Englisch (D96). Vertrag:
`tests/integration/test_shell_selbsttest.py`.
"""

import os
import sys
import tempfile
import time
import tkinter as tk
import tkinter.font as tkfont

from glide_shell import SHELL_VERSION
from glide_shell import (action_picker, custom_controls, desktop_adapter, modal_session, motion, redo_history,
                         runtime_paths, system_appearance, text_fit, window_geometry, window_lifetime)


def expect(condition, detail):
    """Prüft auch unter `python -O`, wo `assert` entfällt."""
    if not condition:
        raise AssertionError(detail)


def check_version(_root):
    parts = SHELL_VERSION.split(".")
    expect(len(parts) == 3 and all(p.isdigit() for p in parts), SHELL_VERSION)
    return SHELL_VERSION


def check_geometry(root):
    text = window_geometry.format_geometry(420, 240, -40, 40)
    expect(window_geometry.parse(text) == (420, 240, -40, 40), text)
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    placed = window_geometry.clamp(9000, 9000, 99999, 99999, width, height, (200, 120))
    expect(placed[0] <= max(200, width) and placed[2] < width, placed)
    return f"screen {width}x{height}"


def check_appearance(root):
    answer = None
    if root.tk.call("tk", "windowingsystem") == "aqua":
        try:
            answer = root.tk.call("tk::unsupported::MacWindowStyle", "isdark", root)
        except tk.TclError:
            answer = None
    dark = system_appearance.tk_is_dark(answer) if answer is not None else None
    expect(system_appearance.resolve({"light": "a", "dark": "b"}, dark, "a") in ("a", "b"), "resolve returned no pair value")
    return {True: "system dark", False: "system light", None: "system mode not reported"}[dark]


def check_redo(_root):
    history, undo = redo_history.RedoHistory(2), ["step"]
    history.push("redo", undo)
    expect(history.validate(undo) and history.peek() == "redo", "redo entry not available")
    history.note_write()
    expect(not history.validate(undo), "a write must invalidate redo")
    return "valid until the next write"


def pump(root, done, timeout=2.0):
    end = time.monotonic() + timeout
    while not done() and time.monotonic() < end:
        root.update()
        time.sleep(0.005)
    return done()


def check_scope_and_motion(root):
    frame = tk.Frame(root)
    scope = window_lifetime.scope_for(frame)
    fired = []
    scope.after(1, lambda: fired.append("timer"))
    transitions = motion.Transitions(scope.after, scope.cancel)
    values = []
    transitions.start("probe", values.append, duration_ms=40)
    finished = pump(root, lambda: fired and not transitions.active)
    expect(finished, (fired, transitions.active))
    expect(values[-1] == 1.0, values)
    scope.after(10000, lambda: None)
    frame.destroy()
    expect(scope.closed and not scope.jobs, scope.jobs)
    return f"{len(values)} transition steps, scope closed with widget"


def check_controls(root):
    actions = []
    menus = []
    bar = desktop_adapter.build_menu_tree(root, [("File", [("Run", lambda: actions.append("run"), "", "run")])],
                                          menus_out=menus)
    ids = {action for menu in menus for action in menu._glide_action_ids.values()}
    expect("run" in ids, ids)
    value = tk.BooleanVar(root, value=False)
    box = custom_controls.GlideCheckbutton(root, text="Probe", variable=value, command=lambda: actions.append("box"))
    box.invoke()
    expect(value.get() and "box" in actions, (value.get(), actions))
    box.destroy()
    bar.destroy()
    return f"platform {desktop_adapter.platform_name()}"


def check_modal(root):
    dialog = modal_session.create_dialog(root, "Self-test", withdrawn=True, resizable=(False, False))
    seen = {}

    def inside():
        seen["grab"] = root.grab_current() is dialog
        dialog.destroy()

    dialog.deiconify()
    root.after(100, inside)
    modal_session.run_modal(root, dialog)
    expect(seen.get("grab") is True, seen)
    expect(root.grab_current() is None, "grab not released")
    return "grab held and released"


def check_text_fit(root):
    font = tkfont.nametofont("TkDefaultFont", root=root)
    text = "Self-test with a label that is far too long for its column"
    width = font.measure(text) // 2
    short = text_fit.fit(text, font.measure, width)
    expect(short.endswith("…") and font.measure(short) <= width, (short, width))
    expect(text_fit.clip(text, 10) == "Self-te...", text_fit.clip(text, 10))
    marks = text_fit.aligned_markers(("✓", "□"), font.measure)
    gap = abs(font.measure(marks["✓"]) - font.measure(marks["□"]))
    expect(gap <= font.measure(text_fit.HAIR_SPACE) + 1, marks)
    return f"fitted to {width} px, markers within {gap} px"


def check_action_picker(_root):
    rows = [((0,), "Open", (), True, 0, "command"), ((1,), "✓ Wrap lines", (), True, 0, "command"),
            ((2, 0), "Rename", ("Edit",), False, 1, "command"), ((3,), "None", (), False, 1, "command")]
    found = action_picker.entries(rows, ("File",), placeholders=("None",), reason=lambda label, path: "busy")
    expect([e.label for e in found] == ["Open", "Wrap lines", "Rename"], found)
    expect(found[1].checked and found[2].reason == "busy" and found[2].section == "Edit", found)
    expect([e.label for e in action_picker.search(found, "wr")] == ["Wrap lines"], "search")
    expect(action_picker.counts(found) == (2, 3), action_picker.counts(found))
    return f"{len(found)} entries in {len(action_picker.grouped(found))} sections"


def check_runtime_paths(_root):
    with tempfile.TemporaryDirectory(prefix="glide-shell-selftest-") as folder:
        default = os.path.join(folder, "default")
        pointer = os.path.join(folder, "pointer.json")
        with open(pointer, "w", encoding="utf-8-sig") as handle:
            handle.write('{"path": "%s"}' % os.path.join(folder, "chosen").replace("\\", "/"))
        chosen, overridden = runtime_paths.resolve_base(None, {}, "APP_DATA_DIR_PROBE", default, pointer)
        expect(os.path.basename(chosen) == "chosen" and not overridden, chosen)
        forced = runtime_paths.resolve_base(None, {"APP_DATA_DIR_PROBE": folder}, "APP_DATA_DIR_PROBE", default, pointer)
        expect(forced == (os.path.abspath(folder), True), forced)
        expect(not os.path.exists(default) and not os.path.exists(chosen), "resolution must not create folders")
    data = runtime_paths.platform_data_dir("Probe")
    expect(os.path.isabs(data) and os.path.basename(data) == "Probe", data)
    return "pointer, override and platform folder resolved without side effects"


CHECKS = (("version", check_version), ("window_geometry", check_geometry),
          ("system_appearance", check_appearance), ("redo_history", check_redo),
          ("window_lifetime+motion", check_scope_and_motion), ("desktop_adapter+custom_controls", check_controls),
          ("text_fit", check_text_fit), ("action_picker", check_action_picker),
          ("runtime_paths", check_runtime_paths), ("modal_session", check_modal))


def run(out=sys.stdout):
    try:
        root = tk.Tk()
    except tk.TclError as error:
        print(f"FAIL tk: no Tk window possible ({error})", file=out)
        return 2
    root.withdraw()
    failed = 0
    try:
        for name, check in CHECKS:
            try:
                print(f"ok   {name}: {check(root)}", file=out)
            except Exception as error:  # pylint: disable=broad-except
                failed += 1
                print(f"FAIL {name}: {type(error).__name__}: {error}", file=out)
    finally:
        root.destroy()
    print(f"Glide Shell {SHELL_VERSION}: {len(CHECKS) - failed}/{len(CHECKS)} checks passed", file=out)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(run())
