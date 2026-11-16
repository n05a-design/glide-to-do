# SPDX-License-Identifier: MPL-2.0
"""Abbau-Vertragstest: was beim Schließen von Glide endet und was danach noch läuft (Shell-Paket 3b).

Bevor Fensterlebensdauer und Abbau in die Shell wandern, hält dieser Test fest,
was `ListApp.on_close` heute garantiert. Jeder Fall startet eine vollständige
App mit den künstlichen Beispieldaten in einem eigenen Prozess und eigener
Ablage, schließt sie über den normalen Weg und misst danach:

- ob das Hauptfenster abgebaut und die Datensperre freigegeben ist,
- welche Tcl-Zeitgeber (`after`) noch anstehen,
- ob in den folgenden 1,5 s Ereignisverarbeitung ein später Rückruf scheitert,
- ob ein Hintergrundfaden danach noch Tk berührt.

Vor dem Schließen nennt der Bericht die Zeitgeber, die nicht über
`_register_after` angemeldet sind. Glide verwirft beim Abbau der Wurzel alle
Tcl-Zeitgeber (`root_beendet` am `<Destroy>` des Hauptfensters); deshalb
überleben auch sie das Schließen nicht. Für einen Abbau von Ansichten ohne
das Hauptfenster (Shell-Paket 3, Fensterlebensdauer) ist diese Liste der
Aufräumbedarf.

Gegenproben (`--gegenproben`) entfernen je eine Schutzzeile in einer Kopie von
`app.pyw` und verlangen den zuständigen roten Fall.

Aufruf: python3 -B tests/integration/test_abbauvertrag.py [--fall NAME] [--gegenproben]
"""
import argparse
import faulthandler
import importlib.machinery
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import threading
import time
import traceback
import zipfile

REPO = pathlib.Path(__file__).resolve().parents[2]
SOURCE = REPO / "src" / "glide" / "app.pyw"
BESTAND = REPO / "tests" / "fixtures" / "beispiele" / "glide_beispieldaten.glidebackup"
ZEITLIMIT = 240          # je Fallprozess in Sekunden
NACHLAUF = 1.5           # Ereignisverarbeitung nach dem Schließen in Sekunden
FAELLE = ("ruhig", "verlauf_laeuft", "abbruch", "doppelt", "modal_offen")
# Seit Paket 3c gehören diese Zeitgeber einem Zeitgeberbereich (`window_lifetime`).
BESESSEN = ("_save_recent_pages", "abholen", "abgleichen", "collapse_emptied_frames", "draw_icons",
            "sync_backdrop_surfaces", "_paint_triangles")
NL = "\n"


def lade(quelle, ordner):
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(BESTAND) as archiv:
        pathlib.Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_abbauvertrag", str(quelle))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    return mod


def auftraege(root):
    return set(root.tk.splitlist(root.tk.call("after", "info")))


def benennen(root, kennungen):
    namen = []
    for kennung in sorted(kennungen):
        try:
            skript, art = root.tk.splitlist(root.tk.call("after", "info", kennung))
        except Exception:
            continue
        namen.append(f"{art}:{re.sub(r'^[0-9]+', '', str(skript).split()[0])}")
    return sorted(namen)


def fall_ausfuehren(name, quelle):
    """Läuft im Kindprozess; gibt ein JSON-Ergebnis auf stdout aus."""
    faulthandler.dump_traceback_later(ZEITLIMIT - 20, exit=True)
    ergebnis = {"fall": name, "fehler": []}
    # Unter Windows hält eine nicht geschlossene App ihre Dateien offen; das
    # Aufräumen darf den Befund dann nicht verdecken.
    with tempfile.TemporaryDirectory(prefix="glide-abbau-", ignore_cleanup_errors=True) as ordner:
        mod = lade(quelle, ordner)
        root = mod.tk.Tk()
        root.geometry("1280x800+0+30")
        spaet = []
        root.report_callback_exception = lambda *a: spaet.append("".join(traceback.format_exception(*a))[-500:])
        app = mod.ListApp(root)
        app.show_info = app.show_warning = app.show_error = lambda *a, **k: None
        for _ in range(8):
            root.update_idletasks()
            root.update()
        sperre = pathlib.Path(mod.LOCK_FILE)
        ergebnis["sperre_vorher"] = sperre.exists()
        faeden_vorher = set(threading.enumerate())

        if name == "verlauf_laeuft":
            import backdrop
            app.set_design("dark")
            app.set_backdrop_choice(backdrop.presets_for("dark")[0].key)
        if name == "abbruch":
            # Ungespeicherte Änderung und „Abbrechen“ in der Rückfrage: Glide bleibt offen.
            app.dirty = True
            app.flush_rich_note = lambda *a, **k: True
            app.ask_yes_no_cancel = lambda *a, **k: None
            angemeldet = set(app._after_ids) & auftraege(root)
            ergebnis["abbruch_rueckgabe"] = app.on_close()
            ergebnis["abbruch_lebt"] = bool(root.winfo_exists())
            ergebnis["abbruch_closing"] = getattr(app, "_closing", None)
            ergebnis["abbruch_angemeldet_bleibt"] = angemeldet <= auftraege(root)
            ergebnis["abbruch_sperre"] = sperre.exists()
            app.dirty = False
            app.ask_yes_no_cancel = lambda *a, **k: False
            for _ in range(3):
                root.update()

        if name == "modal_offen":
            # Schließen, während eine Rückfrage modal wartet: Der Dialog geht mit
            # dem Hauptfenster, der Aufrufer bekommt eine Antwort statt eines Fehlers.
            app.ask_yes_no = type(app).ask_yes_no.__get__(app)
            offen = {}

            def schliessen():
                offen["dialoge"] = sum(isinstance(k, mod.tk.Toplevel) for k in root.winfo_children())
                offen["griff"] = bool(root.grab_current())
                app.on_close()

            root.after(400, schliessen)
            try:
                ergebnis["modal_antwort"] = repr(app.ask_yes_no("Abbauvertrag", "Rückfrage bleibt offen."))
            except Exception:
                ergebnis["modal_antwort"] = "Fehler: " + traceback.format_exc()[-400:]
            ergebnis["modal_dialoge"] = offen.get("dialoge")
            ergebnis["modal_griff"] = offen.get("griff")

        vorher = auftraege(root) if name != "modal_offen" else set()
        registriert = set()
        if name != "modal_offen":
            registriert = set(app._after_ids) | set(mod.glide_window_lifetime.pending_jobs(root))
        ergebnis["besessen_vor_schliessen"] = benennen(root, registriert & vorher)
        ergebnis["frei_vor_schliessen"] = benennen(root, vorher - registriert)
        ergebnis["registriert_vor_schliessen"] = len(registriert & vorher)
        if name != "modal_offen":
            app.on_close()
        if name == "doppelt":
            try:
                app.on_close()
                ergebnis["zweiter_aufruf"] = "ruhig"
            except Exception:
                ergebnis["zweiter_aufruf"] = traceback.format_exc()[-400:]
        try:
            ergebnis["wurzel_lebt"] = bool(root.winfo_exists())
        except mod.tk.TclError:
            ergebnis["wurzel_lebt"] = False
        ergebnis["after_ids"] = len(getattr(app, "_after_ids", ()) or ())
        ergebnis["offen_nach_schliessen"] = benennen(root, auftraege(root))
        ergebnis["sperre_nachher"] = sperre.exists()
        neue = [f for f in threading.enumerate() if f not in faeden_vorher]
        for faden in neue:
            faden.join(timeout=60)
        ergebnis["faeden_haengen"] = [f.name for f in neue if f.is_alive()]
        ende = time.monotonic() + NACHLAUF
        while time.monotonic() < ende:
            try:
                root.tk.dooneevent(2)  # nicht blockierend
            except Exception as fehler:
                spaet.append(f"dooneevent: {fehler}")
                break
            time.sleep(0.01)
        ergebnis["spaete_fehler"] = spaet
        ergebnis["offen_nach_nachlauf"] = benennen(root, auftraege(root))
    faulthandler.cancel_dump_traceback_later()
    print("ERGEBNIS " + json.dumps(ergebnis, ensure_ascii=False))


def bewerten(ergebnis):
    """Vertragsbrüche eines Fallergebnisses als Liste von Texten."""
    brueche = []
    name = ergebnis["fall"]
    if not ergebnis.get("sperre_vorher"):
        brueche.append("Datensperre fehlte schon vor dem Schließen")
    if ergebnis.get("wurzel_lebt"):
        brueche.append("Hauptfenster besteht nach dem Schließen")
    if ergebnis.get("after_ids"):
        brueche.append(f"_after_ids nicht geleert: {ergebnis['after_ids']}")
    if ergebnis.get("offen_nach_schliessen"):
        brueche.append(f"Zeitgeber überleben das Schließen: {ergebnis['offen_nach_schliessen']}")
    if ergebnis.get("offen_nach_nachlauf"):
        brueche.append(f"Zeitgeber nach dem Nachlauf: {ergebnis['offen_nach_nachlauf']}")
    if ergebnis.get("sperre_nachher"):
        brueche.append("Datensperre nach dem Schließen nicht freigegeben")
    if ergebnis.get("spaete_fehler"):
        brueche.append(f"späte Rückrufe scheitern: {ergebnis['spaete_fehler'][:3]}")
    if ergebnis.get("faeden_haengen"):
        brueche.append(f"Hintergrundfäden laufen weiter: {ergebnis['faeden_haengen']}")
    unbesessen = [e for e in ergebnis.get("frei_vor_schliessen", []) if e.split(":", 1)[-1] in BESESSEN]
    if unbesessen:
        brueche.append(f"Zeitgeber ohne Zeitgeberbereich: {unbesessen}")
    if name == "modal_offen":
        if not ergebnis.get("modal_dialoge") or not ergebnis.get("modal_griff"):
            brueche.append("Rückfrage stand beim Schließen nicht modal offen – Fall prüft nichts")
        if ergebnis.get("modal_antwort") not in ("True", "False", "None"):
            brueche.append(f"Rückfrage endet nicht sauber: {ergebnis.get('modal_antwort')}")
    if name == "verlauf_laeuft" and "timer:abholen" not in ergebnis.get("besessen_vor_schliessen", []):
        brueche.append("Abholtimer des Hintergrundverlaufs stand vor dem Schließen nicht an – Fall prüft nichts")
    if name == "abbruch":
        if ergebnis.get("abbruch_rueckgabe") is not None and ergebnis.get("abbruch_lebt") is not True:
            brueche.append("Abbruch hat das Fenster trotzdem geschlossen")
        if not ergebnis.get("abbruch_lebt"):
            brueche.append("Hauptfenster nach Abbruch nicht mehr da")
        if ergebnis.get("abbruch_closing") is not False:
            brueche.append(f"_closing nach Abbruch: {ergebnis.get('abbruch_closing')!r}")
        if not ergebnis.get("abbruch_angemeldet_bleibt"):
            brueche.append("Abbruch hat angemeldete Zeitgeber verworfen")
        if not ergebnis.get("abbruch_sperre"):
            brueche.append("Abbruch hat die Datensperre freigegeben")
    if name == "doppelt" and ergebnis.get("zweiter_aufruf") != "ruhig":
        brueche.append(f"zweiter Schließaufruf: {ergebnis.get('zweiter_aufruf')}")
    return brueche


def starte(name, quelle, umgebung=None):
    env = dict(os.environ if umgebung is None else umgebung, PYTHONIOENCODING="utf-8")
    try:
        lauf = subprocess.run([sys.executable, "-B", __file__, "--intern", name, "--quelle", str(quelle)],
                              capture_output=True, text=True, encoding="utf-8", errors="replace",
                              env=env, timeout=ZEITLIMIT)
    except subprocess.TimeoutExpired:
        return None, ["Zeitlimit des Fallprozesses"]
    zeile = next((z for z in lauf.stdout.splitlines() if z.startswith("ERGEBNIS ")), None)
    if lauf.returncode != 0 or zeile is None:
        return None, [f"Prozess endete mit {lauf.returncode}: {(lauf.stderr or lauf.stdout)[-600:]}"]
    ergebnis = json.loads(zeile[len("ERGEBNIS "):])
    return ergebnis, bewerten(ergebnis)


# Name: (Methode in app.pyw, entfernte Schutzzeile, Ersatz, Fall, der rot werden muss)
GEGENPROBEN = {
    "ohne_tcl_abbruch": ("install_empty_frame_guard", 'self.root.tk.call("after", "cancel", job)', "pass",
                         "verlauf_laeuft"),
    # Die Sperre wird doppelt freigegeben: beim Schließen und am <Destroy> der
    # Wurzel. Die Gegenprobe trifft deshalb die Freigabe selbst.
    "ohne_sperrfreigabe": ("release_data_lock", "os.remove(LOCK_FILE)", "pass", "ruhig"),
    "ohne_abbruchgrenze": ("on_close", "self._closing = False", "pass", "abbruch"),
    # Paket 3c: ein Zeitgeber am Zeitgeberbereich vorbei muss auffallen.
    "ohne_zeitgeberbereich": ("schedule_backdrop_sync",
                              "if self.after_scope().after_idle(self.sync_backdrop_surfaces) is None:",
                              "if self.root.after_idle(self.sync_backdrop_surfaces) is None:", "verlauf_laeuft"),
}


def mutiere(text, methode, alt, neu):
    anfang = text.index(f"    def {methode}(")
    ende = text.index(NL + "    def ", anfang + 1)
    zeilen = text[anfang:ende].split(NL)
    treffer = [i for i, zeile in enumerate(zeilen) if zeile.strip() == alt]
    if len(treffer) != 1:
        raise AssertionError(f"Gegenprobe findet ihre Zeile in {methode} nicht genau einmal: {alt!r}")
    zeile = zeilen[treffer[0]]
    zeilen[treffer[0]] = zeile[:len(zeile) - len(zeile.lstrip())] + neu
    return text[:anfang] + NL.join(zeilen) + text[ende:]


def gegenproben():
    text = SOURCE.read_bytes().decode("utf-8")
    umgebung = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [str(SOURCE.parent)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])))
    befunde = []
    with tempfile.TemporaryDirectory(prefix="glide-abbau-gp-") as ordner:
        for name, (methode, alt, neu, fall) in GEGENPROBEN.items():
            ziel = pathlib.Path(ordner) / name / "app.pyw"
            ziel.parent.mkdir()
            ziel.write_bytes(mutiere(text, methode, alt, neu).encode("utf-8"))
            _ergebnis, brueche = starte(fall, ziel, umgebung)
            befunde.append((name, fall, bool(brueche), brueche[:1]))
    for name, fall, erkannt, hinweis in befunde:
        print(f"  {'erkannt  ' if erkannt else 'ÜBERSEHEN'} {name} -> {fall}: {' '.join(hinweis)[:160]}")
    uebersehen = [b for b in befunde if not b[2]]
    if uebersehen:
        print(f"Abbauvertrag-Gegenproben: {len(uebersehen)} von {len(befunde)} übersehen")
        return 1
    print(f"Abbauvertrag-Gegenproben: OK ({len(befunde)} Schutzzeilen, jede vom zuständigen Fall erkannt)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fall", choices=FAELLE, action="append")
    parser.add_argument("--gegenproben", action="store_true")
    parser.add_argument("--intern", choices=FAELLE, help=argparse.SUPPRESS)
    parser.add_argument("--quelle", type=pathlib.Path, default=SOURCE, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.intern:
        fall_ausfuehren(args.intern, args.quelle.resolve())
        return 0
    if args.gegenproben:
        return gegenproben()
    rot = 0
    for name in args.fall or FAELLE:
        ergebnis, brueche = starte(name, SOURCE)
        frei = ", ".join(ergebnis.get("frei_vor_schliessen", [])) if ergebnis else "–"
        print(f"  {'OK ' if not brueche else 'ROT'} {name}  (frei vor dem Schließen: {frei or 'keine'})")
        for bruch in brueche:
            print(f"      {bruch}")
        rot += bool(brueche)
    if rot:
        print(f"Abbauvertrag: {rot} von {len(args.fall or FAELLE)} Fällen rot")
        return 1
    print(f"Abbauvertrag: OK ({len(args.fall or FAELLE)} Fälle, vollständige App, künstliche Daten)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
