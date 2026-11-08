# SPDX-License-Identifier: MPL-2.0
"""Native QA im passenden Bildschirmmodus eines vergänglichen Mac-CI-Runners.

Der aufrufende Prozess bleibt während der Kindprüfung am Leben: Laut Apple
gilt CGDisplaySetDisplayMode nur für seine Lebensdauer. Persönliche Macs sind
ausgeschlossen. Quelle: developer.apple.com/documentation/coregraphics/
cgdisplaysetdisplaymode(_:_:_:). Keine Änderung an Glides Fenstervertrag.
"""
import argparse
from contextlib import contextmanager
import ctypes
import ctypes.util
import json
import os
import plistlib
from pathlib import Path
import subprocess
import sys
import time


def select_mode(modes, width, height):
    available = [m for m in modes if m["usable"] and m["width"] >= width and m["height"] >= height]
    if not available:
        raise RuntimeError(f"Kein nativer Bildschirmmodus für {width}x{height}: {modes}")
    return min(available, key=lambda m: (m["width"] * m["height"], m["pixel_width"] * m["pixel_height"]))


@contextmanager
def dock_workarea(evidence):
    """Nur den Dock-Autohide-Wert im vergänglichen CI-Desktop ändern/zurücksetzen.

    1920x1080 allein ergab nativ nur 954 px Fensterhöhe. Die Prüfungen
    brauchen unverändert 960 px. Menüleiste und App-Fenster bleiben normal.
    Apple: support.apple.com/guide/mac-help/mchlp1119/mac.
    """
    exported = subprocess.run(["defaults", "export", "com.apple.dock", "-"],
                              check=True, capture_output=True).stdout
    preferences = plistlib.loads(exported)
    original = preferences.get("autohide")
    if original is not None and not isinstance(original, bool):
        raise RuntimeError("Unerwarteter Typ der Dock-Autohide-Einstellung")
    evidence["dock_autohide_original"] = original
    changed = original is not True
    try:
        if changed:
            subprocess.run(["defaults", "write", "com.apple.dock", "autohide", "-bool", "true"], check=True)
            subprocess.run(["killall", "Dock"], check=True)
        yield
    finally:
        if changed:
            restore = (["defaults", "delete", "com.apple.dock", "autohide"] if original is None else
                       ["defaults", "write", "com.apple.dock", "autohide", "-bool", "false"])
            subprocess.run(restore, check=True)
            subprocess.run(["killall", "Dock"], check=True)
        evidence["dock_autohide_restored"] = True


def verify_workarea():
    """Auf echte Arbeitsfläche warten; jeder Versuch öffnet einen neuen Tk-Prozess.

    Der Dock startet asynchron. Tk 9.1 übernimmt NSScreen.visibleFrame beim
    Öffnen des Displays in ext_data (tkMacOSXXStubs.c:TkMacOSXDisplayChanged).
    Ein sofort gestarteter Interpreter kann damit alte Grenzen behalten.
    Keine Maxsize-/Fenster-/Testgrenze wird künstlich vergrößert.
    """
    script = """
import json, time, tkinter as tk
root = tk.Tk()
try:
    root.geometry('1720x960+0+0')
    deadline = time.monotonic() + .5
    while True:
        root.update_idletasks(); root.update()
        actual = [root.winfo_width(), root.winfo_height()]
        if actual == [1720, 960] or time.monotonic() >= deadline:
            break
        time.sleep(.05)
    print(json.dumps(dict(requested=[1720,960], actual=actual, maxsize=list(root.maxsize()),
                         screen=[root.winfo_screenwidth(),root.winfo_screenheight()],
                         tk=root.tk.call('info', 'patchlevel'))))
finally:
    root.destroy()
"""
    attempts = []
    for index in range(10):
        result = subprocess.run([sys.executable, "-B", "-c", script], check=True,
                                capture_output=True, text=True, timeout=5)
        proof = json.loads(result.stdout)
        if result.stderr:
            raise RuntimeError("Tk-Arbeitsflächenprobe meldet Fehler: " + result.stderr)
        attempts.append(proof)
        if proof["actual"] == [1720, 960]:
            break
        if index < 9:
            time.sleep(.25)
    return dict(proof, attempts=attempts)


def run(command, width, height, report):
    if sys.platform != "darwin" or os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("Nur für den vergänglichen macOS-Desktop in GitHub Actions")
    cg = ctypes.CDLL(ctypes.util.find_library("CoreGraphics"))
    cf = ctypes.CDLL(ctypes.util.find_library("CoreFoundation"))

    def signature(lib, name, result, *arguments):
        function = getattr(lib, name)
        function.restype, function.argtypes = result, list(arguments)
        return function

    ptr = ctypes.c_void_p
    display = signature(cg, "CGMainDisplayID", ctypes.c_uint32)()
    copy_modes = signature(cg, "CGDisplayCopyAllDisplayModes", ptr, ctypes.c_uint32, ptr)
    copy_current = signature(cg, "CGDisplayCopyDisplayMode", ptr, ctypes.c_uint32)
    set_mode = signature(cg, "CGDisplaySetDisplayMode", ctypes.c_int32, ctypes.c_uint32, ptr, ptr)
    count = signature(cf, "CFArrayGetCount", ctypes.c_long, ptr)
    entry = signature(cf, "CFArrayGetValueAtIndex", ptr, ptr, ctypes.c_long)
    release = signature(cf, "CFRelease", None, ptr)
    fields = {key: signature(cg, name, ctypes.c_size_t, ptr) for key, name in (
        ("width", "CGDisplayModeGetWidth"), ("height", "CGDisplayModeGetHeight"),
        ("pixel_width", "CGDisplayModeGetPixelWidth"), ("pixel_height", "CGDisplayModeGetPixelHeight"))}
    usable = signature(cg, "CGDisplayModeIsUsableForDesktopGUI", ctypes.c_bool, ptr)
    modes, original = copy_modes(display, None), copy_current(display)
    evidence = {"requested": [width, height], "modes": [], "exitcode": None}
    report.parent.mkdir(parents=True, exist_ok=True)

    def save():
        report.write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    changed = False
    try:
        if not modes or not original:
            raise RuntimeError("CoreGraphics liefert keinen aktiven Bildschirmbestand")
        pointers = {}
        for index in range(count(modes)):
            mode = entry(modes, index)
            row = {key: getter(mode) for key, getter in fields.items()}
            row.update(usable=bool(usable(mode)), index=index)
            evidence["modes"].append(row)
            pointers[index] = mode
        evidence["original"] = {key: getter(original) for key, getter in fields.items()}
        save()
        selected = select_mode(evidence["modes"], width, height)
        code = set_mode(display, pointers[selected["index"]], None)
        if code:
            raise RuntimeError(f"CoreGraphics-Moduswechsel fehlgeschlagen: {code}")
        changed = True
        evidence["selected"] = selected
        save()
        print("Nativer Mac-Prüfdesktop:", selected, flush=True)
        with dock_workarea(evidence):
            evidence["workarea"] = verify_workarea()
            save()
            if evidence["workarea"]["actual"] != [1720, 960]:
                raise RuntimeError(f"Native QA-Arbeitsfläche zu klein: {evidence['workarea']}")
            evidence["exitcode"] = subprocess.run(command, check=False).returncode
        return evidence["exitcode"]
    except Exception as error:
        evidence["error"] = str(error)
        raise
    finally:
        if changed:
            evidence["restore_code"] = set_mode(display, original, None)
        if original:
            release(original)
        if modes:
            release(modes)
        save()
        if evidence.get("restore_code"):
            raise RuntimeError(f"Mac-Prüfdesktop nicht zurückgesetzt: {evidence['restore_code']}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--breite", type=int, default=1920)
    parser.add_argument("--hoehe", type=int, default=1080)
    parser.add_argument("--protokoll", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command or args.breite < 1 or args.hoehe < 1:
        parser.error("Positive Maße und ein Prüfkommando nach -- erforderlich")
    return run(command, args.breite, args.hoehe, args.protokoll)


if __name__ == "__main__":
    raise SystemExit(main())
