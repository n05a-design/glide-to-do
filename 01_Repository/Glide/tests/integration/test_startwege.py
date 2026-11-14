# SPDX-License-Identifier: MPL-2.0
"""Start-Baseline der drei Startwege mit künstlichen Ablagen (WA-49, erster Shell-Schnitt 2a).

Jede Zelle startet einen echten Prozess über seinen unveränderten Einstieg –
`app.pyw` direkt, `glide_start.py` und den Paketstarter `start_glide.py` – gegen
eine leere, vorhandene, fremd gesperrte, beschädigte oder nicht anlegbare Ablage
(statt `backups/` liegt dort eine Datei). Festgehalten
werden Exit-Code, Diagnosebeleg, geschlossene Dialoge und alle entstandenen
Pfade. Die Tabelle ist die Vergleichsgrundlage für Änderungen an Start, Pfaden
und Importzustand; sie ändert kein Produktverhalten. Der Fall
`import_ohne_ordner` lädt die App nur als Modul: Auch mit `GLIDE_DATA_DIR`
entstehen dabei weder Ordner noch Fenster.

Der Paketstarter läuft hier aus den Quellen in einer nachgestellten
Staging-Ebene (`glide_app.py` neben `start_glide.py`). Das belegt seinen
Kontrollfluss, nicht das gebaute Paket (dafür `test_paketierung330.py`).

Isolation: `GLIDE_DATA_DIR` und der Profilordner (HOME, APPDATA …) zeigen in
eine kurze Prüfablage. Ein Begleiter in `sitecustomize` beendet den Prozess
sofort, falls der Profilordner nicht dort liegt (Fall `schutz_profil`), und
schließt danach Dialoge und Hauptfenster über deren Schließen-Protokoll – wie
ein Klick auf das Schließfeld.

Aufruf: python3 -B tests/integration/test_startwege.py [--fall NAME] [--tabelle DATEI]
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src" / "glide"
PAKETSTARTER = REPO / "packaging" / "paket" / "start_glide.py"
HINTERGRUND = REPO / "tests" / "tools" / "hintergrund" / "sitecustomize.py"
EINSTIEGE = ("direkt", "schnellstart", "paket_quelle")
ZUSTAENDE = ("leer", "vorhanden", "gesperrt", "fehlerhaft", "unerreichbar")
SCHUTZ = "schutz_profil"
IMPORT = "import_ohne_ordner"
FAELLE = tuple(f"{einstieg}_{zustand}" for einstieg in EINSTIEGE for zustand in ZUSTAENDE) + (SCHUTZ, IMPORT)
ZEITLIMIT = 120
FREMDE_SPERRE = {"host": "anderer-arbeitsplatz", "pid": 4242, "token": "0" * 32}
BESCHAEDIGT = '{"version": 26, "lists": ['
SPERRDATEI = "Datei statt Ordner"

IMPORTPROBE = r'''
import importlib.machinery, importlib.util, json, os, sys, tkinter
quelle, ziel = sys.argv[1], os.environ["GLIDE_DATA_DIR"]
lader = importlib.machinery.SourceFileLoader("glide_app", quelle)
modul = importlib.util.module_from_spec(importlib.util.spec_from_loader(lader.name, lader))
sys.modules[lader.name] = modul
lader.exec_module(modul)
print(json.dumps({"basis_gleich": os.path.realpath(modul.BASE_DIR) == os.path.realpath(ziel),
                  "ordner_vorhanden": os.path.exists(ziel),
                  "tk_fenster": tkinter._default_root is not None,
                  "menue_aufschub": bool(getattr(tkinter.Menu, "_glide_defers_windows", False))}))
'''

BEGLEITER = r'''
import json, os, sys, time
_protokoll = os.environ.get("GLIDE_STARTWEGE_PROTOKOLL")
_wurzel = os.environ.get("GLIDE_STARTWEGE_WURZEL")
if _protokoll and _wurzel:
    _wurzel = os.path.realpath(_wurzel) + os.sep
    for _pfad in (os.path.expanduser("~"), os.environ.get("GLIDE_DATA_DIR") or os.sep):
        if not (os.path.realpath(_pfad) + os.sep).startswith(_wurzel):
            os._exit(97)
    import tkinter

    def _melden(**eintrag):
        with open(_protokoll, "a", encoding="utf-8") as datei:
            datei.write(json.dumps(eintrag, ensure_ascii=False) + "\n")

    def _fenster(widget):
        for kind in widget.winfo_children():
            if isinstance(kind, tkinter.Toplevel) and kind.winfo_viewable() and not kind.overrideredirect():
                yield kind
            yield from _fenster(kind)

    _stand = {"schleife": None, "geschlossen": False}
    _alt_init, _alt_schleife = tkinter.Tk.__init__, tkinter.Misc.mainloop

    def _init(self, *args, **kwargs):
        _alt_init(self, *args, **kwargs)

        def bedienen():
            try:
                # Zuerst neu einplanen: Ein Schließen kann eine Rückfrage öffnen,
                # deren Warteschleife sonst niemand mehr bediente.
                self.after(300, bedienen)
                offen = list(_fenster(self))
                if offen:
                    dialog = offen[-1]
                    _melden(dialog=str(dialog.title()))
                    befehl = dialog.protocol("WM_DELETE_WINDOW")
                    self.tk.call(befehl) if befehl else dialog.destroy()
                elif (not _stand["geschlossen"] and _stand["schleife"] is not None
                        and time.monotonic() - _stand["schleife"] >= 1.0):
                    _stand["geschlossen"] = True
                    befehl = self.protocol("WM_DELETE_WINDOW")
                    _melden(hauptfenster="protokoll" if befehl else "destroy")
                    self.tk.call(befehl) if befehl else self.destroy()
            except tkinter.TclError:
                pass

        self.after(300, bedienen)

    def _schleife(self, *args, **kwargs):
        _stand["schleife"] = time.monotonic()
        return _alt_schleife(self, *args, **kwargs)

    tkinter.Tk.__init__, tkinter.Misc.mainloop = _init, _schleife
    import tkinter.messagebox as _meldungen

    def _fehlermeldung(title=None, message=None, **_optionen):
        # Systemdialoge vor dem App-Fenster (etwa ein nicht erreichbarer
        # Datenordner) sind keine Tk-Fenster; ihr Titel wird festgehalten.
        _melden(meldung=str(title))
        return "ok"

    _meldungen.showerror = _fehlermeldung
    _hintergrund = os.environ.get("GLIDE_STARTWEGE_HINTERGRUND")
    if _hintergrund and os.environ.get("GLIDE_QA_HINTERGRUND"):
        with open(_hintergrund, encoding="utf-8") as _quelle:
            exec(compile(_quelle.read(), _hintergrund, "exec"), {"__name__": "glide_hintergrund"})
'''


def staging(ziel):
    """Oberste Paketebene aus den Quellen nachstellen: `glide_app.py` und der Starter als Dateien."""
    ziel.mkdir(parents=True)
    for eintrag in sorted(SRC.iterdir()):
        if eintrag.name in ("__pycache__", "drawing_prototype.pyw"):
            continue
        name = "glide_app.py" if eintrag.name == "app.pyw" else eintrag.name
        if eintrag.is_dir():
            try:
                os.symlink(eintrag, ziel / name, target_is_directory=True)
            except OSError:
                shutil.copytree(eintrag, ziel / name)
        else:
            shutil.copy2(eintrag, ziel / name)
    # Als Datei, nicht als Verweis: Der Starter ruft sich über seinen aufgelösten Pfad erneut auf.
    shutil.copy2(PAKETSTARTER, ziel / PAKETSTARTER.name)
    return ziel / PAKETSTARTER.name


def umgebung(wurzel, daten, profil, protokoll, begleiter):
    env = {name: wert for name, wert in os.environ.items()
           if not name.startswith(("XDG_", "GLIDE_")) and name not in ("PYTHONPYCACHEPREFIX", "PYTHONDONTWRITEBYTECODE")}
    if sys.platform.startswith("linux") and "XAUTHORITY" not in env:
        # X11 sucht seinen Schlüssel im echten Profilordner; nur dieser eine Pfad bleibt dort.
        berechtigung = Path.home() / ".Xauthority"
        if berechtigung.is_file():
            env["XAUTHORITY"] = str(berechtigung)
    temp = wurzel / "t"
    temp.mkdir(exist_ok=True)
    env.update(HOME=str(profil), USERPROFILE=str(profil), APPDATA=str(profil / "AppData" / "Roaming"),
               LOCALAPPDATA=str(profil / "AppData" / "Local"), TMPDIR=str(temp), TEMP=str(temp), TMP=str(temp),
               GLIDE_DATA_DIR=str(daten), GLIDE_TEST_MODE="1", PYTHONPATH=str(begleiter),
               GLIDE_STARTWEGE_PROTOKOLL=str(protokoll), GLIDE_STARTWEGE_WURZEL=str(wurzel),
               GLIDE_STARTWEGE_HINTERGRUND=str(HINTERGRUND))
    if os.environ.get("GLIDE_QA_HINTERGRUND"):
        env["GLIDE_QA_HINTERGRUND"] = os.environ["GLIDE_QA_HINTERGRUND"]
    return env


def beenden(prozess):
    """Zeitlimit: die ganze Prozessgruppe beenden, auch das Kind eines Starters."""
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(prozess.pid), "/T", "/F"], capture_output=True)
        else:
            os.killpg(prozess.pid, signal.SIGKILL)
    except (OSError, ProcessLookupError):
        pass


def starten(befehl, env):
    optionen = dict(creationflags=subprocess.CREATE_NEW_PROCESS_GROUP) if os.name == "nt" else dict(start_new_session=True)
    prozess = subprocess.Popen(befehl, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               stdin=subprocess.DEVNULL, **optionen)
    try:
        ausgabe = prozess.communicate(timeout=ZEITLIMIT)[0]
        return prozess.returncode, "regulär", ausgabe.decode("utf-8", "replace")
    except subprocess.TimeoutExpired:
        beenden(prozess)
        ausgabe = prozess.communicate()[0]
        return prozess.returncode, "Zeitlimit", ausgabe.decode("utf-8", "replace")


def abbild(ordner):
    if not ordner.is_dir():
        return {}
    return {pfad.relative_to(ordner).as_posix(): hashlib.sha256(pfad.read_bytes()).hexdigest()
            for pfad in sorted(ordner.rglob("*")) if pfad.is_file() and not pfad.is_symlink()}


def neutral(name):
    """Sitzungskennungen, Zeitstempel und Bytecode-Inhalte aus Pfadnamen nehmen."""
    for marke in ("/bytecode/", "/__pycache__/"):
        if marke in "/" + name:
            return ("/" + name).split(marke)[0].lstrip("/") + marke + "*"
    return re.sub(r"\d{2,}", "#", re.sub(r"[0-9a-f]{16,}", "<id>", name))


def veraenderung(vorher, nachher):
    zeilen = set()
    for name in set(vorher) | set(nachher):
        art = ("neu" if name not in vorher else "weg" if name not in nachher
               else "gleich" if vorher[name] == nachher[name] else "anders")
        zeilen.add(f"{art} {neutral(name)}")
    return sorted(zeilen)


def belege(daten, vorher):
    """Diagnosebelege dieser Sitzung: neu oder verändert gegenüber dem Stand davor."""
    ergebnis = []
    for name, summe in abbild(daten / "diagnostics").items():
        if vorher.get("diagnostics/" + name) == summe or not name.endswith(".json"):
            continue
        try:
            stand = json.loads((daten / "diagnostics" / name).read_text(encoding="utf-8"))
        except (OSError, ValueError):
            ergebnis.append({"unlesbar": True})
            continue
        ergebnis.append({feld: stand.get(feld) for feld in
                         ("supervised", "last_completed_phase", "completed", "exit_code", "start_error")})
    return sorted(ergebnis, key=lambda eintrag: json.dumps(eintrag, sort_keys=True))


def ablage_herrichten(daten, zustand, vorlage):
    if zustand == "leer":
        daten.mkdir(parents=True)
        return
    shutil.copytree(vorlage, daten)
    if zustand == "gesperrt":
        jetzt = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        jetzt = jetzt[:-2] + ":" + jetzt[-2:]
        (daten / "glide.lock").write_text(json.dumps(dict(FREMDE_SPERRE, started_at=jetzt, refreshed_at=jetzt)),
                                          encoding="utf-8")
    elif zustand == "fehlerhaft":
        (daten / "liste_speicher.json").write_text(BESCHAEDIGT, encoding="utf-8")
    elif zustand == "unerreichbar":
        sperre = daten / "backups"
        shutil.rmtree(sperre, ignore_errors=True)
        sperre.write_text(SPERRDATEI, encoding="utf-8")


def zelle(einstieg, zustand, befehle, vorlage, wurzel, begleiter):
    platz = Path(tempfile.mkdtemp(prefix="z-", dir=wurzel))
    daten, profil, protokoll = platz / "daten", platz / "profil", platz / "begleiter.jsonl"
    profil.mkdir()
    ablage_herrichten(daten, zustand, vorlage)
    vorher, temp_vorher = abbild(daten), abbild(wurzel / "t")
    code, ende, ausgabe = starten(befehle[einstieg], umgebung(wurzel, daten, profil, protokoll, begleiter))
    schritte = []
    if protokoll.is_file():
        for zeile in protokoll.read_text(encoding="utf-8").splitlines():
            eintrag = json.loads(zeile)
            schritte.append("Dialog: " + eintrag["dialog"] if "dialog" in eintrag
                            else "Meldung: " + eintrag["meldung"] if "meldung" in eintrag
                            else "Hauptfenster: " + eintrag["hauptfenster"])
    ergebnis = dict(exit=code, ende=ende, schritte=schritte, belege=belege(daten, vorher),
                    daten=veraenderung(vorher, abbild(daten)),
                    profil=sorted({"neu " + neutral(name) for name in abbild(profil)}),
                    temp=[zeile for zeile in veraenderung(temp_vorher, abbild(wurzel / "t")) if not zeile.startswith("gleich ")],
                    ausgabe=bool(ausgabe.strip()))
    if ausgabe.strip():
        ergebnis["ausgabe_ende"] = ausgabe.strip().replace(str(wurzel), "<ablage>").replace(str(REPO), "<repo>")[-600:]
    shutil.rmtree(platz, ignore_errors=True)
    return ergebnis


def schutzprobe(wurzel, begleiter):
    """Der Begleiter beendet einen Prozess, dessen Profilordner nicht in der Prüfablage liegt."""
    fremd = Path(tempfile.mkdtemp(prefix="glide-fremd-", dir=wurzel.parent))
    try:
        env = umgebung(wurzel, wurzel / "schutz-daten", fremd, wurzel / "schutz.jsonl", begleiter)
        code, ende, ausgabe = starten([sys.executable, "-c", "print('lief')"], env)
    finally:
        shutil.rmtree(fremd, ignore_errors=True)
    return dict(exit=code, ende=ende, ausgabe=bool(ausgabe.strip()))


def importprobe(wurzel, begleiter):
    """Der bloße Import der App legt auch mit `GLIDE_DATA_DIR` weder Ordner noch Fenster an (WA-49)."""
    platz = Path(tempfile.mkdtemp(prefix="i-", dir=wurzel))
    daten, profil = platz / "daten", platz / "profil"
    profil.mkdir()
    env = umgebung(wurzel, daten, profil, platz / "begleiter.jsonl", begleiter)
    # Ein direkt geladenes Modul legte seinen Bytecode sonst neben die Quelle, bevor es den Cache umlenkt.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code, ende, ausgabe = starten([sys.executable, "-c", IMPORTPROBE, str(SRC / "app.pyw")], env)
    try:
        zustand = json.loads(ausgabe.strip().splitlines()[-1])
    except (ValueError, IndexError):
        zustand = {"unlesbar": ausgabe.strip().replace(str(wurzel), "<ablage>").replace(str(REPO), "<repo>")[-600:]}
    ergebnis = dict(exit=code, ende=ende, zustand=zustand, daten=veraenderung({}, abbild(daten)),
                    profil=sorted({"neu " + neutral(name) for name in abbild(profil)}))
    shutil.rmtree(platz, ignore_errors=True)
    return ergebnis


def quellbaum_bytecode():
    return sorted(pfad.relative_to(REPO).as_posix() for ordner in (SRC, PAKETSTARTER.parent, Path(__file__).parent)
                  for pfad in ordner.glob("__pycache__"))


def befunde(name, ergebnis):
    """Plattformunabhängiger Vertrag jeder Zelle; alles Weitere hält die Tabelle nur fest."""
    if name == SCHUTZ:
        return [] if ergebnis == dict(exit=97, ende="regulär", ausgabe=False) else [f"Schutz griff nicht: {ergebnis}"]
    if name == IMPORT:
        zustand = ergebnis["zustand"]
        regeln = [
            (ergebnis["ende"] == "regulär" and ergebnis["exit"] == 0, f"Ende {ergebnis['ende']} mit Exit {ergebnis['exit']}: {zustand}"),
            (zustand.get("basis_gleich") is True, "Pfadkonstanten folgen GLIDE_DATA_DIR nicht"),
            (zustand.get("ordner_vorhanden") is False and not ergebnis["daten"], "der Import hat den Datenordner angelegt"),
            (zustand.get("tk_fenster") is False, "der Import hat ein Tk-Fenster erzeugt"),
        ]
        return [text for erfuellt, text in regeln if not erfuellt]
    einstieg, zustand = name.rsplit("_", 1)
    daten = set(ergebnis["daten"])
    if zustand == "unerreichbar":
        belege = ergebnis["belege"]
        regeln = [
            (ergebnis["ende"] == "regulär" and ergebnis["exit"] == 1, f"Ende {ergebnis['ende']} mit Exit {ergebnis['exit']}"),
            (ergebnis["schritte"] == ["Meldung: Datenordner nicht erreichbar"], f"Meldeweg {ergebnis['schritte']}"),
            (len(belege) == 1 and belege[0].get("exit_code") == 1 and belege[0].get("completed") is True,
             f"Diagnosebeleg {belege}"),
            (not ergebnis["ausgabe"], "Ausgabe auf der Konsole: " + ergebnis.get("ausgabe_ende", "")),
            (not ergebnis["temp"], f"Reste im Temp-Ordner: {ergebnis['temp']}"),
            ({"gleich liste_speicher.json", "gleich backups"} <= daten
             and not any(zeile.startswith(("neu ", "anders ")) and "diagnostics/" not in zeile for zeile in daten),
             f"Ablage verändert: {sorted(daten)}"),
        ]
        return [text for erfuellt, text in regeln if not erfuellt]
    erwartet_beleg = dict(supervised=einstieg != "direkt", last_completed_phase="closed", completed=True,
                          exit_code=0, start_error=None)
    regeln = [
        (ergebnis["ende"] == "regulär" and ergebnis["exit"] == 0, f"Ende {ergebnis['ende']} mit Exit {ergebnis['exit']}"),
        (ergebnis["belege"] == [erwartet_beleg], f"Diagnosebeleg {ergebnis['belege']}"),
        (ergebnis["schritte"][-1:] == ["Hauptfenster: protokoll"], f"Schließweg {ergebnis['schritte']}"),
        (not ergebnis["ausgabe"], "Ausgabe auf der Konsole: " + ergebnis.get("ausgabe_ende", "")),
        (not ergebnis["temp"], f"Reste im Temp-Ordner: {ergebnis['temp']}"),
        # Die `.acquire`-Datei bleibt als Träger der Betriebssystemsperre liegen; der eigene Eintrag verschwindet.
        (zustand == "gesperrt" or not any(zeile.endswith(" glide.lock") for zeile in daten),
         "eigener Sperreintrag nach dem Ende nicht entfernt"),
    ]
    if zustand == "leer":
        regeln.append(("neu liste_speicher.json" in daten, "leere Ablage ohne neue Bestandsdatei"))
    if zustand == "vorhanden":
        regeln.append(("gleich liste_speicher.json" in daten, "unbearbeiteter Bestand wurde verändert"))
    if zustand == "gesperrt":
        regeln.append(({"gleich liste_speicher.json", "gleich glide.lock"} <= daten,
                       "fremd gesperrte Ablage wurde verändert"))
    if zustand == "fehlerhaft":
        regeln.append(("neu backups/liste_unlesbar_#_#_#.json" in daten, "beschädigte Bestandsdatei ohne Sicherungskopie"))
        regeln.append(("gleich liste_speicher.json" in daten, "beschädigte Bestandsdatei wurde ersetzt"))
        regeln.append((any(schritt.startswith("Dialog: ") for schritt in ergebnis["schritte"]),
                       "beschädigte Bestandsdatei ohne Meldung"))
    return [text for erfuellt, text in regeln if not erfuellt]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--tabelle", type=Path, help="Tabelle aller Zellen als JSON")
    args = parser.parse_args()
    namen = FAELLE if args.fall == "alle" else (args.fall,)
    tabelle, rot = {}, []
    with tempfile.TemporaryDirectory(prefix="glide-start-") as ordner:
        wurzel = Path(ordner).resolve()
        begleiter = wurzel / "begleiter"
        begleiter.mkdir()
        (begleiter / "sitecustomize.py").write_text(BEGLEITER, encoding="utf-8")
        befehle = {"direkt": [sys.executable, str(SRC / "app.pyw")],
                   "schnellstart": [sys.executable, str(SRC / "glide_start.py")],
                   "paket_quelle": [sys.executable, str(staging(wurzel / "stufe"))]}
        # Die vorhandene Ablage entsteht aus einem echten ersten Start über den Direkteinstieg.
        vorlage = wurzel / "vorlage"
        profil = wurzel / "vorlage-profil"
        profil.mkdir()
        code, ende, ausgabe = starten(befehle["direkt"], umgebung(wurzel, vorlage, profil, wurzel / "vorlage.jsonl", begleiter))
        if code != 0 or ende != "regulär" or not (vorlage / "liste_speicher.json").is_file():
            print("ROT vorlage", code, ende, ausgabe[-600:], flush=True)
            return 1
        for name in namen:
            if name == SCHUTZ:
                ergebnis = schutzprobe(wurzel, begleiter)
            elif name == IMPORT:
                ergebnis = importprobe(wurzel, begleiter)
            else:
                einstieg, zustand = name.rsplit("_", 1)
                ergebnis = zelle(einstieg, zustand, befehle, vorlage, wurzel, begleiter)
            tabelle[name] = ergebnis
            fehler = befunde(name, ergebnis)
            if fehler:
                rot.append(name)
            print("ROT" if fehler else "OK", name, "; ".join(fehler) if fehler else
                  f"Exit {ergebnis['exit']}" + (", Import ohne Ordner und ohne Fenster" if name == IMPORT else
                                                f", {len(ergebnis['daten'])} Datenpfade, {len(ergebnis['profil'])} Profilpfade"
                                                if "daten" in ergebnis else ", Start ohne umgelenktes Profil abgewiesen"),
                  flush=True)
        bytecode = quellbaum_bytecode()
        if bytecode:
            rot.append("quellbaum")
            print("ROT quellbaum Bytecode neben den Quellen:", bytecode, flush=True)
    if args.tabelle:
        args.tabelle.parent.mkdir(parents=True, exist_ok=True)
        args.tabelle.write_text(json.dumps(tabelle, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"gruen": len(namen) - len([name for name in rot if name in namen]), "rot": rot}, ensure_ascii=False))
    return int(bool(rot))


if __name__ == "__main__":
    sys.exit(main())
