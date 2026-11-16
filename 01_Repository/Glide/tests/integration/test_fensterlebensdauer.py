# SPDX-License-Identifier: MPL-2.0
"""Vertragstest für den Zeitgeberbesitz je Fenster oder Ansicht (Shell-Paket 3c).

Geprüft wird `src/glide/window_lifetime.py` allein, mit echtem Tk und ohne
Glide: Ein `AfterScope` führt seine Zeitgeber, vergisst gelaufene, bricht beim
Zerstören seines Widgets alle ab und nimmt danach keine mehr an. Das Zerstören
eines Kindes beendet den Bereich des Elternfensters nicht.

`--gegenproben` entfernt je eine Schutzzeile in einer Kopie des Moduls und
erwartet, dass der zuständige Fall rot wird.

Aufruf: python3 -B tests/integration/test_fensterlebensdauer.py [--fall NAME] [--gegenproben]
"""
import argparse
import faulthandler
import importlib.util
import pathlib
import subprocess
import sys
import tempfile
import tkinter as tk

REPO = pathlib.Path(__file__).resolve().parents[2]
MODUL = REPO / "src" / "glide" / "window_lifetime.py"
ZEITLIMIT = 60
NL = "\n"


def lade(quelle):
    spec = importlib.util.spec_from_file_location("window_lifetime_pruefling", quelle)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


def auftraege(root):
    return set(root.tk.splitlist(root.tk.call("after", "info")))


def pumpen(root, runden=6):
    for _ in range(runden):
        root.update_idletasks()
        root.update()


def warten(root, millisekunden):
    fertig = tk.BooleanVar(master=root, value=False)
    root.after(millisekunden, lambda: fertig.set(True))
    root.wait_variable(fertig)


def gleich(ist, soll, was):
    if ist != soll:
        raise AssertionError(f"{was}: {ist!r} statt {soll!r}")


def fall_laeuft_und_raeumt(shell, root):
    """Ein gelaufener Zeitgeber ruft zurück und verlässt den Bestand."""
    bereich = shell.AfterScope(root)
    gelaufen = []
    job = bereich.after(10, gelaufen.append, "zeit")
    leerlauf = bereich.after_idle(gelaufen.append, "leerlauf")
    gleich({job, leerlauf} <= bereich.jobs, True, "beide Aufträge im Bestand")
    gleich({job, leerlauf} <= auftraege(root), True, "beide Aufträge bei Tk angemeldet")
    warten(root, 80)
    gleich(sorted(gelaufen), ["leerlauf", "zeit"], "Rückrufe mit Argumenten")
    gleich(bereich.jobs, set(), "Bestand nach dem Lauf")


def fall_lesbarer_name(shell, root):
    """Der Auftrag heißt bei Tk wie die Funktion des Aufrufers."""
    bereich = shell.AfterScope(root)

    def abholen():
        pass

    job = bereich.after(5000, abholen)
    skript = str(root.tk.splitlist(root.tk.call("after", "info", job))[0])
    gleich(skript.split()[0].lstrip("0123456789"), "abholen", "Name in after info")
    bereich.cancel_all()


def fall_abbrechen(shell, root):
    """`cancel` und `cancel_all` verhindern den Rückruf; der Bereich bleibt benutzbar."""
    bereich = shell.AfterScope(root)
    gelaufen = []
    erster = bereich.after(20, gelaufen.append, 1)
    bereich.after(20, gelaufen.append, 2)
    bereich.after_idle(gelaufen.append, 3)
    bereich.cancel(erster)
    gleich(erster in auftraege(root), False, "abgebrochener Auftrag bei Tk")
    bereich.cancel(erster)
    bereich.cancel(None)
    bereich.cancel("after#gibtesnicht")
    bereich.cancel_all()
    gleich(bereich.jobs, set(), "Bestand nach cancel_all")
    gleich(bereich.closed, False, "Bereich nach cancel_all offen")
    spaeter = bereich.after(10, gelaufen.append, 4)
    gleich(spaeter is not None, True, "neuer Auftrag nach cancel_all")
    warten(root, 80)
    gleich(gelaufen, [4], "nur der neue Auftrag läuft")


def fall_zerstoerung(shell, root):
    """Mit dem Widget enden seine Zeitgeber; danach wird nichts mehr angenommen."""
    fenster = tk.Toplevel(root)
    bereich = shell.scope_for(fenster)
    gelaufen = []
    jobs = {bereich.after(30, gelaufen.append, 1), bereich.after_idle(gelaufen.append, 2)}
    fenster.destroy()
    gleich(bereich.closed, True, "Bereich nach Zerstörung geschlossen")
    gleich(jobs & auftraege(root), set(), "Aufträge nach Zerstörung bei Tk")
    gleich(bereich.jobs, set(), "Bestand nach Zerstörung")
    gleich(bereich.after(10, gelaufen.append, 3), None, "after nach Zerstörung")
    gleich(bereich.after_idle(gelaufen.append, 4), None, "after_idle nach Zerstörung")
    warten(root, 100)
    gleich(gelaufen, [], "kein Rückruf nach Zerstörung")


def fall_kind_beendet_eltern_nicht(shell, root):
    """`<Destroy>` eines Kindes erreicht das Elternfenster; dessen Bereich bleibt offen."""
    fenster = tk.Toplevel(root)
    bereich = shell.scope_for(fenster)
    kind = tk.Frame(fenster)
    kind.pack()
    gelaufen = []
    bereich.after(20, gelaufen.append, "eltern")
    pumpen(root, 2)
    kind.destroy()
    gleich(bereich.closed, False, "Elternbereich nach Zerstörung des Kindes")
    warten(root, 80)
    gleich(gelaufen, ["eltern"], "Zeitgeber des Elternfensters läuft")
    fenster.destroy()


def fall_geschlossen_nimmt_nichts(shell, root):
    """`close` gilt auch ohne Zerstörung; ein bereits wartender Rückruf läuft nicht mehr."""
    bereich = shell.AfterScope(root, close_on_destroy=False)
    gelaufen = []
    bereich.after(10, gelaufen.append, 1)
    bereich.close()
    gleich(bereich.after(10, gelaufen.append, 2), None, "after nach close")
    gleich(bereich.adopt(None), None, "adopt ohne Auftrag")
    warten(root, 80)
    gleich(gelaufen, [], "kein Rückruf nach close")


def fall_ein_bereich_je_widget(shell, root):
    """`scope_for` liefert je Widget denselben Bereich und trennt Widgets."""
    a, b = tk.Frame(root), tk.Frame(root)
    gleich(shell.scope_for(a) is shell.scope_for(a), True, "gleicher Bereich je Widget")
    gleich(shell.scope_for(a) is shell.scope_for(b), False, "getrennte Bereiche")
    gleich(getattr(a, shell.SCOPE_ATTRIBUTE) is shell.scope_for(a), True, "Attribut am Widget")
    gelaufen = []
    shell.scope_for(a).after(20, gelaufen.append, "a")
    shell.scope_for(b).after(20, gelaufen.append, "b")
    a.destroy()
    warten(root, 80)
    gleich(gelaufen, ["b"], "nur der Zeitgeber des lebenden Widgets läuft")
    b.destroy()


def fall_uebernehmen(shell, root):
    """`adopt` führt fremd angelegte Aufträge und entfernt dabei gelaufene."""
    bereich = shell.AfterScope(root)
    kurz = bereich.adopt(root.after(10, lambda: None))
    warten(root, 60)
    lang = root.after(5000, lambda: None)
    gleich(bereich.adopt(lang), lang, "adopt gibt den Auftrag zurück")
    gleich(kurz in bereich.jobs, False, "gelaufener Auftrag fällt heraus")
    gleich(bereich.pending(), frozenset({lang}), "pending")
    gleich(lang in shell.pending_jobs(root), True, "pending_jobs über alle Bereiche")
    bereich.cancel_all()
    gleich(lang in auftraege(root), False, "übernommener Auftrag abgebrochen")


def fall_wurzel(shell, root):
    """Der Bereich der Wurzel endet mit ihr; späte Aufträge scheitern still."""
    wurzel = tk.Tk()
    wurzel.withdraw()
    bereich = shell.scope_for(wurzel)
    gelaufen = []
    bereich.after(20, gelaufen.append, 1)
    wurzel.destroy()
    gleich(bereich.closed, True, "Wurzelbereich geschlossen")
    gleich(bereich.after(10, gelaufen.append, 2), None, "after an toter Wurzel")
    gleich(bereich.pending(), frozenset(), "pending an toter Wurzel")
    bereich.cancel("after#1")
    warten(root, 80)
    gleich(gelaufen, [], "kein Rückruf der toten Wurzel")


FAELLE = {
    "laeuft_und_raeumt": fall_laeuft_und_raeumt,
    "lesbarer_name": fall_lesbarer_name,
    "abbrechen": fall_abbrechen,
    "zerstoerung": fall_zerstoerung,
    "kind_beendet_eltern_nicht": fall_kind_beendet_eltern_nicht,
    "geschlossen_nimmt_nichts": fall_geschlossen_nimmt_nichts,
    "ein_bereich_je_widget": fall_ein_bereich_je_widget,
    "uebernehmen": fall_uebernehmen,
    "wurzel": fall_wurzel,
}

# Name: (Funktion oder Methode im Modul, entfernte Schutzzeile, Ersatz, Fall, der rot werden muss)
GEGENPROBEN = {
    "ohne_abbau_am_destroy": ("_on_destroy", "self.close()", "pass", "zerstoerung"),
    "ohne_widgetpruefung": ("_on_destroy", "if getattr(event, \"widget\", None) is self.widget:", "if True:",
                            "kind_beendet_eltern_nicht"),
    "ohne_schliessen": ("close", "self.closed = True", "pass", "geschlossen_nimmt_nichts"),
    "ohne_abbruch": ("cancel", "self.widget.after_cancel(job)", "pass", "abbrechen"),
    "ohne_bestandspflege": ("run", "self.jobs.discard(holder[0])", "pass", "laeuft_und_raeumt"),
    "ohne_namen": ("_schedule", "run.__name__ = getattr(callback, \"__name__\", \"run\")", "pass", "lesbarer_name"),
}


def mutiere(text, funktion, alt, neu):
    anfang = text.index(f"def {funktion}(")
    zeilen = text[anfang:].split(NL)
    treffer = [i for i, zeile in enumerate(zeilen) if zeile.strip() == alt]
    if not treffer:
        raise AssertionError(f"Gegenprobe findet ihre Zeile in {funktion} nicht: {alt!r}")
    zeile = zeilen[treffer[0]]
    zeilen[treffer[0]] = zeile[:len(zeile) - len(zeile.lstrip())] + neu
    return text[:anfang] + NL.join(zeilen)


def faelle_ausfuehren(namen, quelle):
    shell = lade(quelle)
    root = tk.Tk()
    root.geometry("320x200+40+40")
    spaet = []
    root.report_callback_exception = lambda *a: spaet.append(repr(a[1]))
    rot = 0
    for name in namen:
        faulthandler.dump_traceback_later(ZEITLIMIT, exit=True)
        try:
            FAELLE[name](shell, root)
            pumpen(root)
            if spaet:
                raise AssertionError(f"Rückruffehler: {spaet[:2]}")
            print(f"  OK  {name}")
        except Exception as fehler:
            rot += 1
            spaet.clear()
            print(f"  ROT {name}: {fehler}")
        finally:
            faulthandler.cancel_dump_traceback_later()
    root.destroy()
    return rot


def gegenproben():
    text = MODUL.read_bytes().decode("utf-8")
    befunde = []
    with tempfile.TemporaryDirectory(prefix="glide-lebensdauer-gp-") as ordner:
        for name, (funktion, alt, neu, fall) in GEGENPROBEN.items():
            ziel = pathlib.Path(ordner) / f"{name}.py"
            ziel.write_bytes(mutiere(text, funktion, alt, neu).encode("utf-8"))
            lauf = subprocess.run([sys.executable, "-B", __file__, "--fall", fall, "--quelle", str(ziel)],
                                  capture_output=True, text=True, encoding="utf-8", errors="replace",
                                  timeout=ZEITLIMIT * 2)
            befunde.append((name, fall, lauf.returncode != 0))
    for name, fall, erkannt in befunde:
        print(f"  {'erkannt  ' if erkannt else 'ÜBERSEHEN'} {name} -> {fall}")
    uebersehen = [b for b in befunde if not b[2]]
    if uebersehen:
        print(f"Fensterlebensdauer-Gegenproben: {len(uebersehen)} von {len(befunde)} übersehen")
        return 1
    print(f"Fensterlebensdauer-Gegenproben: OK ({len(befunde)} Schutzzeilen, jede vom zuständigen Fall erkannt)")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fall", choices=sorted(FAELLE), action="append")
    parser.add_argument("--gegenproben", action="store_true")
    parser.add_argument("--quelle", type=pathlib.Path, default=MODUL, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.gegenproben:
        return gegenproben()
    namen = args.fall or list(FAELLE)
    rot = faelle_ausfuehren(namen, args.quelle.resolve())
    if rot:
        print(f"Fensterlebensdauer: {rot} von {len(namen)} Fällen rot")
        return 1
    print(f"Fensterlebensdauer: OK ({len(namen)} Fälle, echtes Tk {tk.TkVersion}, ohne Glide)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
