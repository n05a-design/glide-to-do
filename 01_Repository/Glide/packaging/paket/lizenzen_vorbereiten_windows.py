"""Lizenz-Prüfbestand passend zur tatsächlich installierten Windows-Baulaufzeit.

Läuft auf dem nativen Windows-Prüfstand (GitHub-Hosted-Runner) vor dem
Paketbau. Versionen kommen aus der geladenen Laufzeit, Lizenztexte aus der
Python-Installation, den Bauabhängigkeiten, dem Glide-Quellbestand und
versionsgenau aus den Herkunftsrepositorien. Für Glide selbst wird keine
Veröffentlichungslizenz gewählt; der vorhandene Statushinweis wird beigelegt.

Aufruf: python -B lizenzen_vorbereiten_windows.py --quelle src/glide --repo 01_Repository/Glide --ziel <Ordner>
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import ssl
import sys
import urllib.request

PIN = "6.22.3"
BUILD = ("pyinstaller", "pyinstaller-hooks-contrib", "altgraph", "packaging", "setuptools", "pefile", "pywin32-ctypes")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class Bestand:
    def __init__(self, ziel):
        self.ziel = Path(ziel)
        self.ziel.mkdir(parents=True, exist_ok=False)
        self.components, self.downloads = [], []

    def copy(self, source, name):
        target = self.ziel / name
        shutil.copy2(source, target)
        if not target.read_bytes().strip():
            raise ValueError("Leerer Lizenzbeleg: " + name)
        return target

    def write(self, name, data):
        target = self.ziel / name
        target.write_bytes(data)
        return target

    def fetch(self, url, name):
        with urllib.request.urlopen(url, timeout=60) as answer:
            data = answer.read()
        if not data.strip():
            raise ValueError("Leerer Lizenzbeleg: " + url)
        target = self.write(name, data)
        self.downloads.append(dict(source=url, file=name, sha256=sha(target)))
        return target

    def add(self, name, version, source, files):
        self.components.append(dict(name=name, version=version, source=source,
                                    files={Path(p).name: sha(p) for p in files}))


def comment_block(text, marker_words):
    block = text.split(b"*/", 1)[0] + b"*/\n"
    if not all(word in block for word in marker_words):
        raise ValueError("Lizenzkommentar nicht gefunden")
    return block


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--quelle", type=Path, required=True)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--ziel", type=Path, required=True)
    args = parser.parse_args()
    if sys.platform != "win32" or platform.machine().lower() not in ("amd64", "x86_64"):
        raise SystemExit("Nur auf dem nativen Windows-x64-Prüfstand.")
    if sys.version_info[:2] != (3, 14):
        raise SystemExit("Die gewählte Laufzeit braucht Python 3.14.")
    import tkinter
    import _tkinter
    tcl = str(tkinter.Tcl().call("info", "patchlevel"))
    if not tcl.startswith("9."):
        raise SystemExit("Python muss mit Tcl/Tk 9 verbunden sein.")
    b = Bestand(args.ziel)
    source, repo, base = args.quelle.resolve(), args.repo.resolve(), Path(sys.base_prefix)

    versions = {name: importlib.metadata.version(name) for name in BUILD}
    if versions["pyinstaller"] != PIN:
        raise SystemExit("Der Bau braucht PyInstaller " + PIN + ".")
    labels = {"pyinstaller": "PyInstaller", "pyinstaller-hooks-contrib": "PyInstaller-Hooks"}
    for distribution in BUILD:
        dist = importlib.metadata.distribution(distribution)
        files = []
        for entry in dist.files or ():
            name = Path(str(entry)).name
            if ".dist-info" not in str(entry) or not name.upper().startswith(("LICENSE", "COPYING", "NOTICE")):
                continue
            files.append(b.copy(dist.locate_file(entry), distribution + "-" + name))
        if not files:
            raise SystemExit("Lizenz der Bauabhängigkeit fehlt: " + distribution)
        b.add(labels.get(distribution, distribution), dist.version,
              "https://pypi.org/project/" + distribution + "/" + dist.version + "/", files)

    python_version = sys.version.split()[0]
    python_license = b.copy(base / "LICENSE.txt", "Python-LICENSE.txt")
    license_text = python_license.read_text(encoding="utf-8", errors="replace")
    b.add("Python", python_version, "https://github.com/python/cpython/tree/v" + python_version, [python_license])
    # Die Windows-Ausgabe von Python führt die Lizenzen ihrer mitgelieferten
    # Bibliotheken in LICENSE.txt; jede Zuordnung braucht ihren Abschnitt.
    for component, marker in (("libffi", "libffi"), ("libmpdec", "mpdecimal"), ("zlib", "zlib")):
        if marker.casefold() not in license_text.casefold():
            raise SystemExit("LICENSE.txt der Laufzeit enthält keinen Abschnitt für " + component)
        b.add(component, "mit Python " + python_version, "Python-LICENSE.txt (Windows-Ausgabe)", [python_license])
    if not list(base.glob("vcruntime140*.dll")):
        raise SystemExit("Microsoft-VC-Laufzeit fehlt in der Python-Installation.")
    if "microsoft distributable code" not in license_text.casefold():
        raise SystemExit("LICENSE.txt der Laufzeit nennt keine Weitergabebedingungen der Microsoft-Laufzeit.")
    b.add("Microsoft-VC-Runtime", "mit Python " + python_version,
          "Abschnitt „Microsoft Distributable Code“ in Python-LICENSE.txt (Windows-Ausgabe)", [python_license])
    # Versionen der mitgelieferten Fremdbibliotheken versionsgenau aus dem Bauskript des CPython-Tags.
    externals = b.fetch("https://raw.githubusercontent.com/python/cpython/v" + python_version + "/PCbuild/get_externals.bat",
                        "Python-get_externals.bat").read_text(encoding="utf-8", errors="replace")

    tag = "core-" + tcl.replace(".", "-")
    for name in ("Tcl", "Tk"):
        terms = b.fetch("https://raw.githubusercontent.com/tcltk/" + name.lower() + "/" + tag + "/license.terms",
                        name + "-LICENSE.txt")
        b.add(name, tcl, "https://github.com/tcltk/" + name.lower() + "/tree/" + tag, [terms])
    tommath = b.fetch("https://raw.githubusercontent.com/tcltk/tcl/" + tag + "/libtommath/LICENSE", "libtommath-LICENSE.txt")
    b.add("libtommath", "aus Tcl " + tcl, "https://github.com/tcltk/tcl/tree/" + tag + "/libtommath", [tommath])
    with urllib.request.urlopen("https://raw.githubusercontent.com/tcltk/tcl/" + tag + "/generic/regcustom.h", timeout=60) as answer:
        regex = b.write("Henry-Spencer-Regex-LICENSE.txt", comment_block(answer.read(), (b"Henry Spencer", b"Redistribution")))
    b.add("Henry-Spencer-Regex", "aus Tcl " + tcl, "https://github.com/tcltk/tcl/blob/" + tag + "/generic/regcustom.h", [regex])
    nano = []
    for header in ("nanosvg.h", "nanosvgrast.h"):
        with urllib.request.urlopen("https://raw.githubusercontent.com/tcltk/tk/" + tag + "/generic/" + header, timeout=60) as answer:
            nano.append(b.write(header + "-LICENSE.txt", comment_block(answer.read(), (b"Copyright", b"redistribute"))))
    b.add("NanoSVG", "aus Tk " + tcl, "https://github.com/tcltk/tk/tree/" + tag + "/generic", nano)

    openssl = ssl.OPENSSL_VERSION.split()[1]
    b.add("OpenSSL", openssl, "https://github.com/openssl/openssl/tree/openssl-" + openssl,
          [b.fetch("https://raw.githubusercontent.com/openssl/openssl/openssl-" + openssl + "/LICENSE.txt", "OpenSSL-LICENSE.txt")])
    import sqlite3
    b.add("SQLite", sqlite3.sqlite_version, "https://www.sqlite.org/copyright.html",
          [b.fetch("https://www.sqlite.org/copyright.html", "SQLite-Copyright.html")])
    import re
    found = re.findall(r"xz-(\d+\.\d+\.\d+)", externals)
    if len(set(found)) != 1:
        raise SystemExit("xz-Version im CPython-Bauskript nicht eindeutig: " + ", ".join(sorted(set(found))))
    xz = found[0]
    b.add("liblzma", xz, "https://github.com/tukaani-project/xz/tree/v" + xz,
          [b.fetch("https://raw.githubusercontent.com/tukaani-project/xz/v" + xz + "/COPYING", "XZ-COPYING.txt")])
    from compression import zstd as _zstd
    zstd = ".".join(str(part) for part in _zstd.zstd_version_info[:3])
    b.add("Zstandard", zstd, "https://github.com/facebook/zstd/tree/v" + zstd,
          [b.fetch("https://raw.githubusercontent.com/facebook/zstd/v" + zstd + "/LICENSE", "Zstandard-LICENSE.txt")])

    b.add("Glide", "Entwicklungsstand; öffentliche Lizenz offen", "LICENSE.md",
          [b.copy(repo / "LICENSE.md", "Glide-Lizenzstatus.md")])
    b.add("tkinterdnd2", "0.6.3", "https://pypi.org/project/tkinterdnd2/0.6.3/",
          [b.copy(source / "vendor/tkinterdnd2/LICENSE", "tkinterdnd2-LICENSE")])
    tkdnd = (source / "vendor/tkinterdnd2/tkdnd/win-x64-tcl9/tkdnd.tcl").read_bytes().split(b"package require Tk", 1)[0]
    if b"copyright" not in tkdnd or b"IN NO EVENT" not in tkdnd:
        raise SystemExit("tkdnd-Lizenzkommentar fehlt")
    b.add("tkdnd", "2.10.2", "https://pypi.org/project/tkinterdnd2/0.6.3/; unveränderter Kommentarblock aus tkdnd.tcl",
          [b.write("tkdnd-LICENSE.txt", tkdnd)])
    b.add("Glide-Schriften", "DejaVu 2.37 / Pixelify Sans 39df74a", "resources/fonts/provenance.json",
          [b.copy(source / "resources/fonts/LICENSE", "DejaVu-LICENSE"),
           b.copy(source / "resources/fonts/OFL-PixelifySans.txt", "PixelifySans-OFL.txt")])
    b.add("IANA-Zeitzonen", "2026e", "resources/timezones/provenance.json",
          [b.copy(source / "resources/timezones/LICENSE-iana.txt", "IANA-LICENSE.txt")])
    b.add("Unicode-CLDR", "48.2", "resources/timezones/provenance.json",
          [b.copy(source / "resources/timezones/LICENSE-CLDR.txt", "CLDR-LICENSE.txt")])

    runtime = dict(python=python_version, tcl=tcl, tk_compiled=_tkinter.TK_VERSION, platform="win32",
                   machine="x86_64", pyinstaller=PIN)
    manifest = dict(runtime=runtime, components=b.components, downloads=b.downloads, bauabhaengigkeiten=versions,
                    abnahme="Auf dem nativen Windows-Prüfstand aus der tatsächlichen Baulaufzeit erzeugt")
    (b.ziel / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(b.components), "Komponenten mit Lizenzbelegen für Python", python_version, "/ Tcl", tcl)


if __name__ == "__main__":
    main()
