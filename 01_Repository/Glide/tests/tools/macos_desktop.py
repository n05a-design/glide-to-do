# SPDX-License-Identifier: MPL-2.0
"""Native QA im passenden Bildschirmmodus eines vergänglichen Mac-CI-Runners.

Der aufrufende Prozess bleibt während der Kindprüfung am Leben: Laut Apple
gilt CGDisplaySetDisplayMode nur für seine Lebensdauer. Persönliche Macs sind
ausgeschlossen. Quelle: developer.apple.com/documentation/coregraphics/
cgdisplaysetdisplaymode(_:_:_:). Keine Änderung an Glides Fenstervertrag.
"""
import argparse
import ctypes
import ctypes.util
import json
import os
from pathlib import Path
import subprocess
import sys


def select_mode(modes, width, height):
    available = [m for m in modes if m["usable"] and m["width"] >= width and m["height"] >= height]
    if not available:
        raise RuntimeError(f"Kein nativer Bildschirmmodus für {width}x{height}: {modes}")
    return min(available, key=lambda m: (m["width"] * m["height"], m["pixel_width"] * m["pixel_height"]))


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
