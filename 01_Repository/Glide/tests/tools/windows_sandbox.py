"""Windows-Vollprüfung in der Windows-Sandbox: Prüffenster auf dem zweiten Bildschirm (seit 23.10.2026).

Unter Windows holen sich die Prüffenster den Vordergrund, nehmen Tastatur und
Zwischenablage, und eine Eingabe in einem anderen Programm nimmt ihnen den
Fokus (Lauf 05 des Phasenabschlusses 3.44.0 brach deshalb ab). Ein zweiter
Bildschirm allein ändert daran nichts: Fokus und Tastatur gehören zur ganzen
Sitzung. Die Windows-Sandbox ist eine eigene Sitzung mit eigenem Fokus. Ihr
Fenster steht auf dem gewählten Bildschirm, gearbeitet wird auf dem anderen.

Ablauf:

1. Projektordner außerhalb der synchronisierten Ablage einfrieren – ohne
   `.git`, `__pycache__`, `build` und `.claude/worktrees`, wie bei den
   bisherigen eingefrorenen Läufen – und das Quellmanifest schreiben.
2. Sandbox-Konfiguration erzeugen: Kopie (schreibbar), die Python-Installation
   des Aufrufers (schreibgeschützt) und ein Ergebnisordner. Kein Netz, keine
   geteilte Zwischenablage, kein Mikrofon, keine Kamera, kein Drucker.
3. Sandbox starten und ihr Fenster ohne Aktivierung auf den Bildschirm legen.
   In der Sandbox läuft `pruefen.py --modus voll`; am Ende steht der
   Exitcode in `FERTIG.txt`.
4. Mit `--warten` auf das Ende warten und das Ergebnis zusammenfassen.

Aufruf unter Windows aus `01_Repository/Glide` mit dem Python, das geprüft
werden soll (keine Microsoft-Store-Fassung):

    py -3.14 -B tests/tools/windows_sandbox.py --warten
    py -3.14 -B tests/tools/windows_sandbox.py --bildschirm 2 --speicher 8192 --schliessen

`--nur-dateien` legt Kopie, Konfiguration und Startskript an, ohne die
Sandbox zu starten (auch zum Prüfen der Dateien auf anderen Systemen).

Voraussetzung: Windows Pro, Enterprise oder Education mit aktivierter
Windows-Sandbox (PowerShell als Administrator:
`Enable-WindowsOptionalFeature -Online -FeatureName Containers-DisposableClientVM -All`,
danach Neustart). Es läuft immer nur eine Sandbox. Das Sandbox-Fenster offen
lassen und nicht minimieren. Glide selbst bleibt unverändert; die Sandbox ist
ein Windows-Lauf derselben Windows-Fassung, aber ohne physische DPI-,
Screenreader- oder Menschenabnahme.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path, PureWindowsPath
from xml.sax.saxutils import escape

GLIDE = Path(__file__).resolve().parents[2]
PROJEKT = Path(__file__).resolve().parents[4]
SANDBOX_PROJEKT = r"C:\Glide"
SANDBOX_PYTHON = r"C:\Python"
SANDBOX_ERGEBNIS = r"C:\Ergebnis"
STARTSKRIPT = "start_pruefung.cmd"
FERTIG = "FERTIG.txt"
KONFIGURATION = "glide_pruefung.wsb"
STANDARD_SPEICHER = 6144
WARTEZEIT_START = 20
# Wie windows_vollpruefung.ps1: Zeitlimit je Suite und Mindeststand der Prüflaufzeit.
SUITEN_TIMEOUT = 900
MINDEST_PYTHON = (3, 14)
MINDEST_TK = 9
QA_LAUFZEIT = Path(".cache") / "glide-qa" / "python-3.14.8" / "runtime"
FEATURE = "Containers-DisposableClientVM"
AUSGESCHLOSSEN_NAMEN = frozenset({".git", "__pycache__", "build"})
AUSGESCHLOSSEN_FOLGEN = ((".claude", "worktrees"),)
AUSGESCHLOSSEN_ENDUNGEN = frozenset({".pyc", ".pyo"})


# --- Einfrieren -------------------------------------------------------------

def ausgeschlossen(teile):
    """Gehört ein relativer Pfad (als Teile) nicht in die eingefrorene Kopie?"""
    teile = tuple(teile)
    if any(teil in AUSGESCHLOSSEN_NAMEN for teil in teile):
        return True
    for folge in AUSGESCHLOSSEN_FOLGEN:
        laenge = len(folge)
        if any(teile[i:i + laenge] == folge for i in range(len(teile) - laenge + 1)):
            return True
    name = teile[-1] if teile else ""
    # Office-/OneDrive-Sperrdateien entstehen nur während des Bearbeitens.
    if name.startswith("~$") or name.startswith(".~lock."):
        return True
    return Path(name).suffix.lower() in AUSGESCHLOSSEN_ENDUNGEN


def dateiliste(quelle):
    """Alle einzufrierenden Dateien relativ zu `quelle`, sortiert."""
    quelle = Path(quelle)
    ergebnis = []
    for ordner, unterordner, dateien in os.walk(quelle):
        relativ = Path(ordner).relative_to(quelle)
        teile = relativ.parts
        unterordner[:] = sorted(u for u in unterordner if not ausgeschlossen(teile + (u,)))
        for datei in sorted(dateien):
            if not ausgeschlossen(teile + (datei,)):
                ergebnis.append(relativ / datei)
    return sorted(ergebnis, key=lambda pfad: pfad.as_posix())


def git_commit(projekt):
    """Commit des Arbeitsbaums aus `.git` gelesen, ohne Git aufzurufen (None, wenn unbekannt)."""
    gitpfad = Path(projekt) / ".git"
    try:
        if gitpfad.is_file():
            zeile = gitpfad.read_text(encoding="utf-8").strip()
            if not zeile.startswith("gitdir:"):
                return None
            gitpfad = (Path(projekt) / zeile.split(":", 1)[1].strip()).resolve()
        kopf = (gitpfad / "HEAD").read_text(encoding="utf-8").strip()
        if not kopf.startswith("ref:"):
            return kopf or None
        ref = kopf.split(":", 1)[1].strip()
        lose = gitpfad / ref
        if lose.is_file():
            return lose.read_text(encoding="utf-8").strip() or None
        gepackt = gitpfad / "packed-refs"
        if gepackt.is_file():
            for zeile in gepackt.read_text(encoding="utf-8").splitlines():
                teile = zeile.split()
                if len(teile) == 2 and teile[1] == ref:
                    return teile[0]
    except (OSError, UnicodeDecodeError):
        return None
    return None


def einfrieren(quelle, ziel, jetzt=None):
    """Projekt nach `ziel` kopieren und das Quellmanifest zurückgeben.

    Das Manifest folgt den bisherigen Läufen (`quellstand_*.json`): Zweck,
    Zeitpunkt, Commit, Version, App-SHA-256 und SHA-256 jeder Datei.
    """
    quelle, ziel = Path(quelle), Path(ziel)
    if ziel.exists() and any(ziel.iterdir()):
        raise FileExistsError(f"Zielordner ist nicht leer: {ziel}")
    hashes = {}
    for relativ in dateiliste(quelle):
        daten = (quelle / relativ).read_bytes()
        neu = ziel / relativ
        neu.parent.mkdir(parents=True, exist_ok=True)
        neu.write_bytes(daten)
        shutil.copystat(quelle / relativ, neu)
        hashes[relativ.as_posix()] = hashlib.sha256(daten).hexdigest()
    version_datei = quelle / "01_Repository" / "Glide" / "VERSION"
    app = "01_Repository/Glide/src/glide/app.pyw"
    return {
        "zweck": "Eingefrorener Quell- und Prüfstand einer Windows-Vollprüfung in der Windows-Sandbox "
                 "(Kopie außerhalb der synchronisierten Ablage, ohne .git, __pycache__, build und .claude/worktrees)",
        "erstellt": (jetzt or datetime.now().astimezone()).isoformat(timespec="seconds"),
        "git_commit": git_commit(quelle),
        "version": version_datei.read_text(encoding="utf-8").strip() if version_datei.is_file() else None,
        "app_sha256": hashes.get(app),
        "dateien": len(hashes),
        "sha256": hashes,
    }


# --- Ablage und Pfade -------------------------------------------------------

def onedrive_wurzeln(umgebung=None):
    """Synchronisierte Ordner aus den OneDrive-Umgebungsvariablen."""
    umgebung = os.environ if umgebung is None else umgebung
    return [umgebung[name] for name in ("OneDrive", "OneDriveConsumer", "OneDriveCommercial")
            if umgebung.get(name)]


def liegt_unter(pfad, wurzeln):
    """Liegt `pfad` in einer der Wurzeln? Windows-Schreibweise, Groß/Klein egal."""
    teile = tuple(teil.casefold() for teil in PureWindowsPath(str(pfad)).parts)
    for wurzel in wurzeln:
        basis = tuple(teil.casefold() for teil in PureWindowsPath(str(wurzel)).parts)
        if basis and teile[:len(basis)] == basis:
            return True
    return False


def standardziel(jetzt=None):
    stempel = (jetzt or datetime.now()).strftime("%Y%m%d-%H%M")
    return Path.home() / "GlidePruefung" / f"lauf_{stempel}"


# --- Sandbox-Dateien --------------------------------------------------------

def _xml(text):
    """XML-Text, Nicht-ASCII als Zeichenreferenz (Pfade mit Umlauten bleiben lesbar für den Parser)."""
    return escape(str(text)).encode("ascii", "xmlcharrefreplace").decode("ascii")


def wsb_xml(projekt, python, ergebnis, speicher=STANDARD_SPEICHER):
    """Inhalt der .wsb-Datei: drei Ordner, kein Netz, keine geteilte Zwischenablage."""
    ordner = ((projekt, SANDBOX_PROJEKT, False), (python, SANDBOX_PYTHON, True), (ergebnis, SANDBOX_ERGEBNIS, False))
    zeilen = ["<Configuration>",
              "  <Networking>Disable</Networking>",
              # Prüfungen kopieren und fügen ein; die Zwischenablage des Benutzers bleibt unberührt.
              "  <ClipboardRedirection>Disable</ClipboardRedirection>",
              "  <AudioInput>Disable</AudioInput>",
              "  <VideoInput>Disable</VideoInput>",
              "  <PrinterRedirection>Disable</PrinterRedirection>",
              f"  <MemoryInMB>{max(2048, int(speicher))}</MemoryInMB>",
              "  <MappedFolders>"]
    for host, sandbox, nur_lesen in ordner:
        zeilen += ["    <MappedFolder>",
                   f"      <HostFolder>{_xml(host)}</HostFolder>",
                   f"      <SandboxFolder>{_xml(sandbox)}</SandboxFolder>",
                   f"      <ReadOnly>{'true' if nur_lesen else 'false'}</ReadOnly>",
                   "    </MappedFolder>"]
    zeilen += ["  </MappedFolders>",
               "  <LogonCommand>",
               f"    <Command>cmd.exe /c {SANDBOX_ERGEBNIS}\\{STARTSKRIPT}</Command>",
               "  </LogonCommand>",
               "</Configuration>"]
    return "\r\n".join(zeilen) + "\r\n"


def startskript(schliessen=False, wartezeit=WARTEZEIT_START):
    """Startskript in der Sandbox: kurz warten, Vollprüfung, Exitcode nach FERTIG.txt."""
    glide = SANDBOX_PROJEKT + r"\01_Repository\Glide"
    protokoll = SANDBOX_ERGEBNIS + r"\protokoll"
    zeilen = ["@echo off",
              "rem Erzeugt von tests/tools/windows_sandbox.py: Glide-Vollprüfung in der Windows-Sandbox",
              "chcp 65001 >nul",
              # Die Anmeldung richtet den Desktop noch ein; Prüffenster erst danach öffnen.
              f'powershell -NoProfile -Command "Start-Sleep -Seconds {int(wartezeit)}"',
              "set PYTHONUTF8=1",
              "set PYTHONFAULTHANDLER=1",
              "set PYTHONDONTWRITEBYTECODE=1",
              f'cd /d "{glide}"',
              f'"{SANDBOX_PYTHON}\\python.exe" -B tests\\tools\\pruefen.py --modus voll --protokoll "{protokoll}"'
              f' --timeout {SUITEN_TIMEOUT} > "{SANDBOX_ERGEBNIS}\\konsole.txt" 2>&1',
              # Umleitung zuerst: „echo 1> Datei“ wäre eine Umleitung von Kanal 1.
              f'> "{SANDBOX_ERGEBNIS}\\{FERTIG}" echo %ERRORLEVEL%']
    if schliessen:
        zeilen.append("shutdown /s /t 60")
    return "\r\n".join(zeilen) + "\r\n"


# --- Bildschirme ------------------------------------------------------------

def monitore_ordnen(monitore):
    """Hauptbildschirm zuerst, dann von links nach rechts und oben nach unten."""
    return sorted(monitore, key=lambda m: (not m.get("haupt"), m["links"], m["oben"]))


def bildschirm_waehlen(monitore, nummer=None):
    """Bildschirm Nummer `nummer` (1 = Hauptbildschirm); ohne Angabe der zweite, sonst der erste."""
    geordnet = monitore_ordnen(monitore)
    if not geordnet:
        raise ValueError("Kein Bildschirm gefunden")
    if nummer is None:
        nummer = 2 if len(geordnet) > 1 else 1
    if not 1 <= int(nummer) <= len(geordnet):
        liste = ", ".join(f"{i}: {m['breite']}×{m['hoehe']} bei {m['links']},{m['oben']}"
                          + (" (Hauptbildschirm)" if m.get("haupt") else "")
                          for i, m in enumerate(geordnet, 1))
        raise ValueError(f"Bildschirm {nummer} gibt es nicht – vorhanden: {liste}")
    return geordnet[int(nummer) - 1]


# --- Ergebnis ---------------------------------------------------------------

def zusammenfassung(ergebnis):
    """Kurzfassung einer `ergebnis.json` von `pruefen.py`."""
    schritte = ergebnis.get("schritte") or []
    zaehler = {}
    for schritt in schritte:
        zaehler[schritt.get("status", "?")] = zaehler.get(schritt.get("status", "?"), 0) + 1
    teile = [f"{len(schritte)} Schritte"] + [f"{anzahl} {status}" for status, anzahl in sorted(zaehler.items())]
    zeilen = [", ".join(teile) + f"; Exitcode {ergebnis.get('exitcode')}"]
    rot = [s for s in schritte if s.get("status") == "fehlgeschlagen"]
    zeilen += [f"  rot: {s.get('schritt')} – {s.get('grund', '')}" for s in rot]
    return "\n".join(zeilen)


# --- Windows ----------------------------------------------------------------

def standard_python(heim=None, aufrufer=None):
    """Prüflaufzeit wie windows_vollpruefung.ps1: eigene QA-Laufzeit, sonst das aufrufende Python."""
    eigene = Path(heim or Path.home()) / QA_LAUFZEIT
    if (eigene / "python.exe").is_file():
        return eigene
    return Path(aufrufer or sys.base_prefix)


def laufzeit_geeignet(python_version, tk_version):
    """Python ≥ 3.14 und Tk ≥ 9 – dieselbe Grenze wie die bisherige Windows-Vollprüfung."""
    try:
        python = tuple(int(teil) for teil in str(python_version).split(".")[:2])
        tk = int(str(tk_version).split(".")[0])
    except ValueError:
        return False
    return python >= MINDEST_PYTHON and tk >= MINDEST_TK


def windows_python(ordner):
    """(Version, Tk-Patchlevel) eines Python-Ordners; Fehlermeldung als Ausnahme."""
    ordner = Path(ordner)
    if "WindowsApps" in ordner.parts:
        raise RuntimeError("Python aus dem Microsoft Store lässt sich nicht in die Sandbox einbinden; "
                           "bitte die Fassung von python.org verwenden (--python ORDNER).")
    programm = ordner / "python.exe"
    if not programm.is_file():
        raise RuntimeError(f"In {ordner} fehlt python.exe.")
    ausgabe = subprocess.run([str(programm), "-I", "-c",
                              "import sys, tkinter; print(sys.version.split()[0]); "
                              "print(tkinter.Tcl().eval('info patchlevel'))"],
                             capture_output=True, text=True, timeout=60, check=True).stdout.split()
    if not laufzeit_geeignet(ausgabe[0], ausgabe[1]):
        raise RuntimeError(f"Python {ausgabe[0]} mit Tk {ausgabe[1]}; nötig sind Python 3.14 und Tk 9 von python.org.")
    return ausgabe[0], ausgabe[1]


def sandbox_programm():
    gefunden = shutil.which("WindowsSandbox.exe")
    if gefunden:
        return Path(gefunden)
    kandidat = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "WindowsSandbox.exe"
    return kandidat if kandidat.is_file() else None


def _dpi_bewusst():
    """Koordinaten in echten Pixeln über alle Bildschirme (Fensterlage auf Bildschirmen mit eigener Skalierung)."""
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4))
    except (AttributeError, OSError):
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except (AttributeError, OSError):
            pass


def monitore_lesen():
    """Arbeitsflächen aller Bildschirme (ohne Taskleiste) über EnumDisplayMonitors."""
    import ctypes
    from ctypes import wintypes

    class MONITORINFO(ctypes.Structure):
        _fields_ = [("cbSize", wintypes.DWORD), ("rcMonitor", wintypes.RECT),
                    ("rcWork", wintypes.RECT), ("dwFlags", wintypes.DWORD)]

    user32 = ctypes.windll.user32
    liste = []
    rueckruf_typ = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HANDLE, wintypes.HDC,
                                      ctypes.POINTER(wintypes.RECT), wintypes.LPARAM)

    def rueckruf(monitor, _dc, _rechteck, _daten):
        info = MONITORINFO()
        info.cbSize = ctypes.sizeof(MONITORINFO)
        if user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            arbeit = info.rcWork
            liste.append({"links": arbeit.left, "oben": arbeit.top, "breite": arbeit.right - arbeit.left,
                          "hoehe": arbeit.bottom - arbeit.top, "haupt": bool(info.dwFlags & 1)})
        return True

    user32.EnumDisplayMonitors(None, None, rueckruf_typ(rueckruf), 0)
    return liste


def sandbox_fenster(timeout=120):
    """Größtes sichtbares Fenster eines Sandbox-Prozesses (Programmname enthält „Sandbox“) oder None."""
    import ctypes
    from ctypes import wintypes
    user32, kernel32 = ctypes.windll.user32, ctypes.windll.kernel32
    eigene = os.getpid()

    def programm(fenster):
        pid = wintypes.DWORD()
        user32.GetWindowThreadProcessId(fenster, ctypes.byref(pid))
        if pid.value == eigene:
            return ""
        prozess = kernel32.OpenProcess(0x1000, False, pid.value)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not prozess:
            return ""
        try:
            puffer = ctypes.create_unicode_buffer(1024)
            groesse = wintypes.DWORD(1024)
            if kernel32.QueryFullProcessImageNameW(prozess, 0, puffer, ctypes.byref(groesse)):
                return Path(puffer.value).name
        finally:
            kernel32.CloseHandle(prozess)
        return ""

    ende = time.monotonic() + timeout
    while time.monotonic() < ende:
        treffer = []
        aufzaehlen = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def pruefen(fenster, _daten):
            if user32.IsWindowVisible(fenster) and "sandbox" in programm(fenster).casefold():
                rechteck = wintypes.RECT()
                user32.GetWindowRect(fenster, ctypes.byref(rechteck))
                flaeche = (rechteck.right - rechteck.left) * (rechteck.bottom - rechteck.top)
                if flaeche > 200 * 200:
                    treffer.append((flaeche, fenster))
            return True

        user32.EnumWindows(aufzaehlen(pruefen), 0)
        if treffer:
            return max(treffer)[1]
        time.sleep(2)
    return None


def fenster_legen(fenster, bildschirm):
    """Fenster auf die Arbeitsfläche des Bildschirms legen, ohne es zu aktivieren."""
    import ctypes
    user32 = ctypes.windll.user32
    keine_reihenfolge, nicht_aktivieren = 0x0004, 0x0010
    user32.ShowWindow(fenster, 4)  # SW_SHOWNOACTIVATE: aus Vollbild/Maximierung lösen, ohne Fokus
    return bool(user32.SetWindowPos(fenster, None, bildschirm["links"], bildschirm["oben"], bildschirm["breite"],
                                    bildschirm["hoehe"], keine_reihenfolge | nicht_aktivieren))


# --- Ablauf -----------------------------------------------------------------

def main(argumente=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--ziel", type=Path, help="Neuer Ordner für Kopie und Ergebnis (Standard: ~/GlidePruefung/lauf_<Zeit>)")
    parser.add_argument("--quelle", type=Path, default=PROJEKT, help="Projektordner (Standard: dieser Baum)")
    parser.add_argument("--python", type=Path, default=None,
                        help="Ordner der Python-Installation für die Sandbox (Standard: eigene QA-Laufzeit "
                             "unter ~/.cache/glide-qa, sonst das aufrufende Python)")
    parser.add_argument("--bildschirm", type=int, help="1 = Hauptbildschirm; Standard: zweiter, falls vorhanden")
    parser.add_argument("--speicher", type=int, default=STANDARD_SPEICHER, help="Arbeitsspeicher der Sandbox in MB")
    parser.add_argument("--warten", action="store_true", help="Auf das Ende warten und das Ergebnis zusammenfassen")
    parser.add_argument("--max-stunden", type=float, default=6.0, help="Längste Wartezeit mit --warten")
    parser.add_argument("--schliessen", action="store_true", help="Sandbox nach der Prüfung herunterfahren")
    parser.add_argument("--nur-dateien", action="store_true", help="Nur Kopie, Konfiguration und Startskript anlegen")
    args = parser.parse_args(argumente)
    args.python = args.python or standard_python()
    windows = sys.platform == "win32"
    if not windows and not args.nur_dateien:
        print("Die Windows-Sandbox gibt es nur unter Windows; ohne Windows nur mit --nur-dateien.", file=sys.stderr)
        return 3

    ziel = (args.ziel or standardziel()).expanduser().resolve()
    quelle = args.quelle.expanduser().resolve()
    if liegt_unter(ziel, onedrive_wurzeln()) or liegt_unter(ziel, [quelle]):
        print(f"Zielordner {ziel} liegt in der synchronisierten Ablage oder im Projekt; bitte --ziel außerhalb wählen.",
              file=sys.stderr)
        return 3
    if ziel.exists() and any(ziel.iterdir()):
        print(f"Zielordner {ziel} ist nicht leer.", file=sys.stderr)
        return 3

    info = {"erstellt": datetime.now().astimezone().isoformat(timespec="seconds"),
            "werkzeug": "tests/tools/windows_sandbox.py", "speicher_mb": max(2048, args.speicher),
            "schliessen": bool(args.schliessen), "windows": platform.platform()}
    if windows:
        try:
            info["python"], info["tk"] = windows_python(args.python)
        except (RuntimeError, OSError, subprocess.SubprocessError, IndexError) as fehler:
            print(f"Python für die Sandbox ungeeignet: {fehler}", file=sys.stderr)
            return 3
        if not args.nur_dateien and sandbox_programm() is None:
            print("Windows-Sandbox nicht gefunden. Sie gibt es in Windows Pro, Enterprise und Education; aktivieren in "
                  "PowerShell als Administrator:\n"
                  f"  Enable-WindowsOptionalFeature -Online -FeatureName {FEATURE} -All\n"
                  "danach neu starten.", file=sys.stderr)
            return 3
        _dpi_bewusst()
        try:
            info["bildschirm"] = bildschirm_waehlen(monitore_lesen(), args.bildschirm)
        except ValueError as fehler:
            print(fehler, file=sys.stderr)
            return 3

    projekt, ergebnis = ziel / "projekt", ziel / "ergebnis"
    print(f"Friere {quelle} nach {projekt} ein …", flush=True)
    manifest = einfrieren(quelle, projekt)
    ergebnis.mkdir(parents=True, exist_ok=True)
    (ergebnis / "quellstand.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (ergebnis / STARTSKRIPT).write_bytes(startskript(args.schliessen).encode("utf-8"))
    wsb = ziel / KONFIGURATION
    wsb.write_bytes(wsb_xml(projekt, args.python.resolve(), ergebnis, args.speicher).encode("ascii"))
    info.update(app_sha256=manifest["app_sha256"], version=manifest["version"], dateien=manifest["dateien"],
                git_commit=manifest["git_commit"])
    (ergebnis / "sandbox.json").write_text(json.dumps(info, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{manifest['dateien']} Dateien eingefroren, App {str(manifest['app_sha256'])[:12]}…; Konfiguration {wsb}")
    if args.nur_dateien:
        return 0

    os.startfile(str(wsb))  # noqa: S606 – öffnet die .wsb mit der Windows-Sandbox
    fenster = sandbox_fenster()
    bildschirm = info["bildschirm"]
    if fenster:
        fenster_legen(fenster, bildschirm)
        # Nach der Anmeldung passt die Sandbox ihr Fenster einmal an; danach erneut legen.
        time.sleep(10)
        fenster_legen(fenster, bildschirm)
        print(f"Sandbox-Fenster auf Bildschirm {bildschirm['breite']}×{bildschirm['hoehe']} "
              f"bei {bildschirm['links']},{bildschirm['oben']} gelegt.")
    else:
        print("Sandbox-Fenster nicht gefunden; bitte von Hand auf den zweiten Bildschirm ziehen (nicht minimieren).")
    print(f"Ergebnis: {ergebnis} (FERTIG.txt, konsole.txt, protokoll\\ergebnis.json)")
    if not args.warten:
        return 0

    fertig = ergebnis / FERTIG
    ende = time.monotonic() + args.max_stunden * 3600
    while not fertig.is_file() and time.monotonic() < ende:
        time.sleep(30)
    if not fertig.is_file():
        print(f"Keine {FERTIG} nach {args.max_stunden} Stunden.", file=sys.stderr)
        return 2
    try:
        exitcode = int(fertig.read_text(encoding="utf-8", errors="replace").strip() or "2")
    except ValueError:
        exitcode = 2
    bericht = ergebnis / "protokoll" / "ergebnis.json"
    if bericht.is_file():
        print(zusammenfassung(json.loads(bericht.read_text(encoding="utf-8"))))
    return exitcode if exitcode in (0, 1, 2) else 1


if __name__ == "__main__":
    raise SystemExit(main())
