"""Vergänglichen Windows-CI-Desktop auf die Größe der Geometrieprüfungen setzen.

Nur in GitHub Actions; verändert keine gespeicherte Bildschirmkonfiguration.
EnumDisplaySettingsW / ChangeDisplaySettingsW:
https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-enumdisplaysettingsw
https://learn.microsoft.com/windows/win32/api/winuser/nf-winuser-changedisplaysettingsw
Eine grüne Prüfung belegt weder menschliche Bedienung noch DPI/Mehrmonitor.
"""
import argparse
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import sys
import time


def prepare(width, height):
    if sys.platform != "win32" or os.environ.get("GITHUB_ACTIONS") != "true":
        raise RuntimeError("Nur für den vergänglichen Windows-Desktop in GitHub Actions")

    class DevMode(ctypes.Structure):
        _fields_ = [
            ("device", wintypes.WCHAR * 32),
            ("spec", wintypes.WORD), ("driver", wintypes.WORD),
            ("size", wintypes.WORD), ("extra", wintypes.WORD),
            ("fields", wintypes.DWORD),
            ("x", wintypes.LONG), ("y", wintypes.LONG),
            ("orientation", wintypes.DWORD), ("fixed_output", wintypes.DWORD),
            ("color", ctypes.c_short), ("duplex", ctypes.c_short),
            ("y_resolution", ctypes.c_short), ("tt_option", ctypes.c_short),
            ("collate", ctypes.c_short), ("form", wintypes.WCHAR * 32),
            ("log_pixels", wintypes.WORD), ("depth", wintypes.DWORD),
            ("width", wintypes.DWORD), ("height", wintypes.DWORD),
            ("flags", wintypes.DWORD), ("frequency", wintypes.DWORD),
            ("icm_method", wintypes.DWORD), ("icm_intent", wintypes.DWORD),
            ("media", wintypes.DWORD), ("dither", wintypes.DWORD),
            ("reserved1", wintypes.DWORD), ("reserved2", wintypes.DWORD),
            ("panning_width", wintypes.DWORD), ("panning_height", wintypes.DWORD),
        ]

    assert ctypes.sizeof(DevMode) == 220, ctypes.sizeof(DevMode)
    user32 = ctypes.WinDLL("user32", use_last_error=True)
    enumerate_mode = user32.EnumDisplaySettingsW
    enumerate_mode.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(DevMode)]
    enumerate_mode.restype = wintypes.BOOL
    change = user32.ChangeDisplaySettingsW
    change.argtypes = [ctypes.POINTER(DevMode), wintypes.DWORD]
    change.restype = wintypes.LONG

    def mode(number):
        value = DevMode()
        value.size = ctypes.sizeof(value)
        return value if enumerate_mode(None, number, ctypes.byref(value)) else None

    def geometry(value):
        return {"breite": value.width, "hoehe": value.height,
                "farbtiefe": value.depth, "frequenz": value.frequency}

    before = mode(0xFFFFFFFF)
    if before is None:
        raise RuntimeError("Aktueller Windows-Anzeigemodus nicht lesbar")
    supported, candidates, index = [], [], 0
    while (value := mode(index)) is not None:
        supported.append(geometry(value))
        if value.width == width and value.height == height and value.depth >= 24:
            candidates.append(value)
        index += 1
    report = {"vorher": geometry(before), "ziel": [width, height], "modi": supported}
    if (before.width, before.height) != (width, height):
        if not candidates:
            raise RuntimeError(f"Referenzgröße nicht unterstützt: {report}")
        target = max(candidates, key=lambda v: (v.depth, v.frequency))
        target.fields = 0x00040000 | 0x00080000 | 0x00100000  # depth, width, height
        # CDS_TEST prüft zuerst; 0 übernimmt nur für diese laufende Sitzung.
        tested = change(ctypes.byref(target), 2)
        if tested != 0:
            raise RuntimeError(f"Anzeigemodus abgelehnt: {tested}; {report}")
        applied = change(ctypes.byref(target), 0)
        if applied != 0:
            raise RuntimeError(f"Anzeigemodus nicht übernommen: {applied}; {report}")
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        after = mode(0xFFFFFFFF)
        if after and (after.width, after.height) == (width, height):
            break
        time.sleep(0.1)
    else:
        raise RuntimeError("Windows meldet nach Übernahme weiterhin eine andere Größe")
    # Derselbe Tk-Weg wie in den Suiten muss die neue Referenzgröße sehen.
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        root.update_idletasks()
        report["tk"] = {"breite": root.winfo_screenwidth(), "hoehe": root.winfo_screenheight(),
                        "skalierung": float(root.tk.call("tk", "scaling")),
                        "version": str(root.tk.call("package", "provide", "Tk"))}
        if (report["tk"]["breite"], report["tk"]["hoehe"]) != (width, height):
            raise RuntimeError(f"Tk sieht einen anderen Desktop: {report}")
    finally:
        root.destroy()
    report["nachher"] = geometry(after)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--breite", type=int, default=1920)
    parser.add_argument("--hoehe", type=int, default=1080)
    parser.add_argument("--protokoll", type=Path, required=True)
    args = parser.parse_args()
    try:
        report = prepare(args.breite, args.hoehe)
    except Exception as error:
        report = {"status": "fehlgeschlagen", "fehler": str(error)}
    else:
        report["status"] = "ausgeführt"
    args.protokoll.parent.mkdir(parents=True, exist_ok=True)
    args.protokoll.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "ausgeführt" else 1


if __name__ == "__main__":
    raise SystemExit(main())
