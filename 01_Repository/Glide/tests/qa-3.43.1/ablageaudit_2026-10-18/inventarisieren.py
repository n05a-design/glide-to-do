"""Vollständige Metadateninventur, ohne Dateiinhalte zu laden oder zu löschen."""
import argparse
from collections import Counter, defaultdict
import ctypes
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess

REDIRECT_TAGS = {0xA0000003, 0xA000000C}


def git_paths(root, *args):
    p = subprocess.run(["git", "-C", str(root), "ls-files", "-z", *args],
                       capture_output=True, check=True)
    return {x.decode("utf-8", "surrogateescape") for x in p.stdout.split(b"\0") if x}


def kind(relative):
    parts = relative.split("/")
    if parts[0] == ".git":
        return "Git-Verwaltung und Historie"
    if relative.startswith(".claude/worktrees/"):
        return "separate Arbeitskopie: " + parts[2]
    if relative.startswith("00_Arbeitsvorbereitung/Featurepaket_UI_UX/bilder/"):
        return "geschützte Nutzerreferenz"
    if "__pycache__" in parts or parts[-1] == ".DS_Store":
        return "erzeugter Cache"
    if "build" in parts:
        return "Paket und Bauartefakt"
    if "qa-" in relative and "tests" in parts:
        return "QA-Nachweis"
    if "fixtures" in parts:
        return "Prüffixture und Migrationsreferenz"
    if relative.startswith("07_Python-Versionen/"):
        return "Python-Lieferstand"
    if relative.startswith("20_Grafik_Master/"):
        return "Grafikquelle und Master"
    if relative.startswith("05_Probelisten_Testdaten/"):
        return "Showcase und Probedaten"
    if relative.lower().endswith((".md", ".txt", ".rst")):
        return "Dokumentation oder Textressource"
    return "Code, Ressource oder Projektverwaltung"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    tracked = git_paths(root, "--cached")
    ignored = git_paths(root, "--others", "--ignored", "--exclude-standard")
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    size = kernel.GetCompressedFileSizeW
    size.argtypes = [ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_ulong)]
    size.restype = ctypes.c_ulong
    errors, files, directories, links = [], [], [], []
    pending = [root]
    while pending:
        directory = pending.pop()
        try:
            entries = list(os.scandir(directory))
        except OSError as exc:
            errors.append({"pfad": directory.relative_to(root).as_posix(), "fehler": str(exc)})
            continue
        for entry in entries:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            try:
                st = entry.stat(follow_symlinks=False)
                tag = getattr(st, "st_reparse_tag", 0)
                attrs = getattr(st, "st_file_attributes", 0)
                if stat.S_ISLNK(st.st_mode) or tag in REDIRECT_TAGS:
                    links.append({"pfad": relative, "tag": tag, "ziel": os.readlink(path)})
                    continue
                if entry.is_dir(follow_symlinks=False):
                    directories.append({"pfad": relative, "attribute": attrs, "tag": tag})
                    pending.append(path)
                    continue
                high = ctypes.c_ulong()
                ctypes.set_last_error(0)
                low = size("\\\\?\\" + str(path), ctypes.byref(high))
                error = ctypes.get_last_error()
                disk = None if low == 0xFFFFFFFF and error else (high.value << 32) | low
                if disk is None:
                    errors.append({"pfad": relative, "fehler": "Belegung nicht ermittelbar", "winerror": error})
                files.append({"pfad": relative, "bytes": st.st_size, "belegt_bytes": disk,
                              "mtime_ns": st.st_mtime_ns, "attribute": attrs, "tag": tag,
                              "inhalt_nicht_vollstaendig_lokal": bool(attrs & (0x1000 | 0x400000)),
                              "versioniert": relative in tracked, "ignoriert": relative in ignored,
                              "bereich": kind(relative), "identitaet": [st.st_dev, st.st_ino]})
            except OSError as exc:
                errors.append({"pfad": relative, "fehler": str(exc)})
    groups = defaultdict(lambda: {"dateien": 0, "bytes": 0, "belegt_bytes": 0})
    by_folder = defaultdict(lambda: {"dateien": 0, "bytes": 0, "belegt_bytes": 0})
    seen = set()
    unique_disk = 0
    for row in files:
        for group in (groups[row["bereich"]], by_folder["/".join(row["pfad"].split("/")[:4])]):
            group["dateien"] += 1
            group["bytes"] += row["bytes"]
            group["belegt_bytes"] += row["belegt_bytes"] or 0
        # OneDrive meldet hier teilweise (0, 0); das ist keine Dateiidentität.
        identity = tuple(row["identitaet"]) if all(row["identitaet"]) else (row["pfad"],)
        if identity not in seen:
            seen.add(identity)
            unique_disk += row["belegt_bytes"] or 0
    report = {"datum": datetime.now(timezone.utc).isoformat(), "wurzel": "Projektablage",
              "dateien": sorted(files, key=lambda x: x["pfad"]), "ordner": directories,
              "verknuepfungen": links, "fehler": errors, "bereiche": dict(groups),
              "unterordner": dict(by_folder), "belegt_bytes_dateipfade": unique_disk,
              "laufwerk_frei_bytes": shutil.disk_usage(root).free,
              "grenzen": ["Metadateninventur, keine Inhaltsfreigabe allein aufgrund eines Dateinamens",
                          "Cloud-Platzhalter werden nicht durch Inhaltslesen nachgeladen",
                          "Verknüpfungen werden erfasst, aber nicht verfolgt; NTFS-Verwaltungsdaten sind nicht eingerechnet",
                          "Ohne gültige Dateiidentität werden Pfade gezählt; mögliche Hardlinks sind dann nicht dedupliziert"]}
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"dateien": len(files), "ordner": len(directories), "links": len(links),
                      "fehler": len(errors), "bereiche": dict(groups),
                      "groesste_ordner": sorted(by_folder.items(), key=lambda x: x[1]["bytes"], reverse=True)[:18]},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
