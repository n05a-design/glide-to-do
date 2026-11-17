# SPDX-License-Identifier: MPL-2.0
"""Vertragstest für `ListApp.run_modal` und `modal_over` mit echtem Grab (Shell-Paket 3).

Bevor der Modal-Weg aus `ListApp` herausgelöst wird, hält dieser Test fest,
was er heute garantiert. Jeder Fall öffnet echte `Toplevel`-Fenster am
echten Tk-Interpreter und ruft die unveränderten Methoden der App; nur
`grab_set` und `wait_window` werden in je einem Fall gezielt zum Scheitern
gebracht, weil ein fremder Grab bzw. ein Abbruch im Warten nicht künstlich
herzustellen ist. Geprüft werden Grab-Besitz, Freigabe, Rückgabe an das
aufrufende Fenster, Fokus, ein ansprechbarer Event-Loop während des Wartens,
aufgeschobene Menübefehle, wiederverwendbare Dialoge (`_glide_modal_finished`)
und der Abbau von Besitzer und Hauptfenster.

Ein Wächter (`faulthandler`) beendet den Prozess mit Stapelauszug, falls ein
Fall hängt; ein weicher Wächter am Event-Loop schließt offene Dialoge und
meldet den Fall als rot. Unter Windows und Linux belegt der Menüfall nur den
Aufschub über `after_idle`; die Menüverfolgung von macOS/Aqua braucht einen
nativen Mac-Lauf.

Seit 3.62.0 (Paket 3a) sind die `ListApp`-Methoden Fassaden für das
Shell-Modul `modal_session.py`; geprüft wird weiter über die Fassaden, also
über den Weg der App. Gegenproben (`--gegenproben`) legen `app.pyw` neben eine
Kopie von `modal_session.py`, in der je eine Schutzzeile entfernt ist, und
verlangen, dass der zuständige Fall rot wird. Findet eine Gegenprobe ihre Zeile
nicht mehr, ist der Modal-Weg umgebaut worden: Gegenproben und Vertrag
gemeinsam nachführen.

Aufruf: python3 -B tests/integration/test_modalvertrag.py [--fall NAME] [--gegenproben]
"""
import argparse
import faulthandler
import inspect
import importlib.machinery
import importlib.util
import os
import pathlib
import subprocess
import sys
import tempfile
import traceback

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
ZEITLIMIT = 60          # harter Wächter je Fall in Sekunden
WEICHES_LIMIT_MS = 15000
SCHRITT_MS = 40
WIEDERHOLUNGEN = 25


class Vertragsbruch(AssertionError):
    pass


def lade_app(temp_root):
    os.environ["GLIDE_DATA_DIR"] = temp_root
    loader = importlib.machinery.SourceFileLoader("glide_modalvertrag", str(SOURCE))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    assert pathlib.Path(mod.BASE_DIR).resolve() == pathlib.Path(temp_root).resolve()
    return mod


class Umgebung:
    """Eine App-Hülle mit eigener Root, ohne Bestand, Autosave oder Lock."""

    def __init__(self, mod):
        self.mod = mod
        self.tk = mod.tk
        self.root = mod.tk.Tk()
        self.root.geometry("700x500+40+40")
        self.root.update()
        app = mod.ListApp.__new__(mod.ListApp)
        app.root = self.root
        app._after_ids = set()
        app.theme = mod.ListApp.THEMES["light"]
        self.protokoll = []
        app.log_error = self.protokoll.append
        self.app = app
        self.fehler = []

    # -- Hilfen ---------------------------------------------------------
    def dialog(self, master=None, titel="Prüfdialog"):
        fenster = self.tk.Toplevel(master or self.root)
        fenster.title(titel)
        fenster.geometry("320x160+120+120")
        self.tk.Entry(fenster, name="eingabe").pack(padx=12, pady=12)
        fenster.bind("<Escape>", lambda _e: fenster.destroy())
        return fenster

    def feld_im_hauptfenster(self):
        """Ein Eingabefeld im Hauptfenster, das vor dem Dialog den Fokus hat."""
        feld = self.tk.Entry(self.root, name="hauptfeld")
        feld.pack()
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        feld.focus_set()
        self.root.update()
        return feld

    def fokus(self):
        try:
            return self.root.focus_get()
        except (KeyError, self.tk.TclError):
            return None

    def pruefe_fokus(self, fenster, erwartet, wann):
        """Der Fokus liegt auf `erwartet`; ohne Systemfokus zählt, was das Fenster sich merkt."""
        self.root.update_idletasks()
        fokus = self.fokus()
        gemerkt = fenster.focus_lastfor()
        self.pruefe(gemerkt is erwartet, f"{wann}: Fenster merkt sich {gemerkt!r} statt {erwartet!r}")
        self.pruefe(fokus in (None, erwartet), f"{wann}: Fokus liegt auf {fokus!r} statt {erwartet!r}")

    def grab(self):
        try:
            return self.root.grab_current()
        except self.tk.TclError:
            return None

    def pruefe(self, bedingung, text):
        if not bedingung:
            raise Vertragsbruch(text)

    def ablauf(self, schritte):
        """Führt Schritte nacheinander im Event-Loop aus, auch über blockierende Schritte hinweg.

        Jeder Schritt plant seinen Nachfolger, bevor er läuft: Öffnet er einen
        verschachtelten Dialog, wartet er in `run_modal`, und der Nachfolger
        läuft trotzdem.
        """
        schritte = list(schritte)

        def fuehre(index):
            if index >= len(schritte) or self.fehler:
                return
            self.root.after(SCHRITT_MS, lambda: fuehre(index + 1))
            try:
                schritte[index]()
            except Exception:
                self.fehler.append(traceback.format_exc())
                self.notabbau()

        self.root.after(SCHRITT_MS, lambda: fuehre(0))

    def weicher_waechter(self):
        def abbrechen():
            self.fehler.append("Zeitlimit: Dialog wartete länger als %d ms" % WEICHES_LIMIT_MS)
            self.notabbau()
        return self.root.after(WEICHES_LIMIT_MS, abbrechen)

    def notabbau(self):
        for kind in list(self.root.winfo_children()):
            if isinstance(kind, self.tk.Toplevel):
                try:
                    kind.destroy()
                except self.tk.TclError:
                    pass

    def laufen(self, start):
        """Startet `start` (der `run_modal` aufruft) und meldet gesammelte Fehler."""
        waechter = self.weicher_waechter()
        try:
            start()
        finally:
            try:
                self.root.after_cancel(waechter)
            except self.tk.TclError:
                pass
        if self.fehler:
            raise Vertragsbruch("\n".join(self.fehler))

    def zerlegen(self):
        # Restliche Schritte der Kette abbrechen: Sonst laufen sie nach dem
        # Abbau im nächsten Interpreter an und melden „invalid command name“.
        try:
            for auftrag in self.root.tk.splitlist(self.root.tk.call("after", "info")):
                self.root.after_cancel(auftrag)
        except self.tk.TclError:
            pass
        try:
            self.root.destroy()
        except self.tk.TclError:
            pass


# -- Fälle -------------------------------------------------------------

def fall_grundvertrag(u):
    """Griff, Theme, Aktivmarke und Freigabe beim Schließen."""
    d = u.dialog()
    beobachtet = {}

    def waehrend():
        beobachtet["grab"] = u.grab()
        beobachtet["status"] = d.grab_status()
        beobachtet["aktiv"] = getattr(d, "_glide_modal_active", None)
        beobachtet["bg"] = d.cget("background")
        d.destroy()

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    u.pruefe(beobachtet.get("grab") is d, f"Griff während des Wartens: {beobachtet.get('grab')!r}")
    u.pruefe(beobachtet.get("status") == "local", f"Grabstatus: {beobachtet.get('status')!r}")
    u.pruefe(beobachtet.get("aktiv") is True, "_glide_modal_active fehlt während des Wartens")
    u.pruefe(beobachtet.get("bg") == u.app.theme["bg"], "Dialoghintergrund folgt nicht dem Theme")
    u.pruefe(u.grab() is None, f"Griff nach dem Schließen nicht frei: {u.grab()!r}")
    u.pruefe(getattr(d, "_glide_modal_active", None) is False, "_glide_modal_active bleibt gesetzt")
    u.pruefe(not u.protokoll, f"unerwarteter Protokolleintrag: {u.protokoll}")


def fall_escape(u):
    """Abbruch über Escape und über das Schließen-Protokoll beendet das Warten."""
    for weg in ("escape", "protokoll"):
        d = u.dialog()
        if weg == "protokoll":
            d.protocol("WM_DELETE_WINDOW", d.destroy)

        def schliessen(d=d, weg=weg):
            if weg == "escape":
                # Tk leitet Tastenereignisse an den Fokus des Fensters um. Hat
                # der Prüfprozess keinen Systemfokus (anderes Programm vorn),
                # ginge Escape sonst verloren; der Fokus innerhalb des Dialogs
                # wird deshalb ausdrücklich gesetzt.
                eingabe = d.nametowidget("eingabe")
                eingabe.focus_set()
                eingabe.event_generate("<Escape>", when="now")
            else:
                d.tk.call(d.protocol("WM_DELETE_WINDOW"))

        u.ablauf([schliessen])
        u.laufen(lambda d=d: u.app.run_modal(d))
        u.pruefe(not d.winfo_exists(), f"{weg}: Dialog besteht noch")
        u.pruefe(u.grab() is None, f"{weg}: Griff nicht frei")


def fall_eventloop(u):
    """Während des Wartens laufen Zeitgeber und Leerlaufaufträge weiter."""
    d = u.dialog()
    zaehler = {"after": 0, "idle": 0}

    def tick(n=[0]):
        zaehler["after"] += 1
        n[0] += 1
        if n[0] < 5:
            u.root.after(10, tick)

    u.root.after(10, tick)
    u.root.after_idle(lambda: zaehler.__setitem__("idle", zaehler["idle"] + 1))
    u.ablauf([lambda: None, lambda: None, lambda: None, d.destroy])
    u.laufen(lambda: u.app.run_modal(d))
    u.pruefe(zaehler["after"] == 5, f"Zeitgeber liefen nicht durch: {zaehler}")
    u.pruefe(zaehler["idle"] == 1, f"Leerlaufauftrag lief nicht: {zaehler}")


def fall_verschachtelt(u):
    """Drei Ebenen ohne `parent=`: jeder Unterdialog gibt den Griff an seinen Vorgänger zurück."""
    a = u.dialog(titel="A")
    stand = {}

    def oeffne_b():
        b = u.dialog(master=a, titel="B")
        stand["b"] = b

        def oeffne_c():
            c = u.dialog(master=b, titel="C")
            stand["c"] = c
            u.app.run_modal(c)
            stand["nach_c"] = u.grab()

        u.root.after(SCHRITT_MS, oeffne_c)
        u.app.run_modal(b)
        stand["nach_b"] = u.grab()

    def schliesse_c():
        stand["waehrend_c"] = u.grab()
        stand["c"].destroy()

    def schliesse_b():
        stand["b"].destroy()

    def schliesse_a():
        a.destroy()

    u.ablauf([oeffne_b, lambda: None, lambda: None, schliesse_c, lambda: None, schliesse_b,
              lambda: None, schliesse_a])
    u.laufen(lambda: u.app.run_modal(a))
    u.pruefe(stand.get("waehrend_c") is stand.get("c"), f"C hielt den Griff nicht: {stand}")
    u.pruefe(stand.get("nach_c") is stand.get("b"), f"Griff nicht an B zurück: {stand}")
    u.pruefe(stand.get("nach_b") is a, f"Griff nicht an A zurück: {stand}")
    u.pruefe(u.grab() is None, "Griff nach A nicht frei")


def fall_parent(u):
    """Ein ausdrücklicher `parent=` erhält seinen Griff, auch wenn Tk ihn nicht meldet."""
    a = u.dialog(titel="A")
    stand = {}

    def unter():
        b = u.dialog(master=a, titel="B")
        u.root.after(SCHRITT_MS, b.destroy)
        u.app.run_modal(b, parent=a)
        stand["nach_b"] = u.grab()
        a.destroy()

    u.ablauf([unter])
    u.laufen(lambda: u.app.run_modal(a))
    u.pruefe(stand.get("nach_b") is a, f"Griff nicht an parent zurück: {stand}")
    # Ein Hauptfenster als parent bekommt keinen Griff: es hatte keinen.
    b = u.dialog()
    u.root.after(SCHRITT_MS, b.destroy)
    u.laufen(lambda: u.app.run_modal(b, parent=u.root))
    u.pruefe(u.grab() is None, f"Hauptfenster erhielt einen Griff: {u.grab()!r}")


def fall_besitzer_weg(u):
    """Schließt sich der Besitzer während des Unterdialogs, bekommt niemand den Griff."""
    a = u.dialog(titel="A")
    stand = {}

    def unter():
        b = u.dialog(titel="B")  # nicht Kind von A, damit A allein verschwinden kann
        stand["b"] = b
        u.app.run_modal(b)
        stand["nach_b"] = u.grab()

    def a_weg():
        a.destroy()

    def b_zu():
        stand["b"].destroy()

    u.ablauf([unter, a_weg, lambda: None, b_zu])
    u.laufen(lambda: u.app.run_modal(a))
    u.pruefe("nach_b" in stand, "Unterdialog kehrte nicht zurück")
    u.pruefe(stand["nach_b"] is None, f"Griff an verschwundenes Fenster: {stand['nach_b']!r}")
    u.pruefe(u.grab() is None, "Griff nach dem Abbau nicht frei")


def fall_grab_fehlschlag(u):
    """Scheitert `grab_set`, wird protokolliert und trotzdem gewartet; kein Stillstand."""
    d = u.dialog()

    def scheitern():
        raise u.tk.TclError("grab failed: another application has grab")

    d.grab_set = scheitern
    beobachtet = {}

    def waehrend():
        beobachtet["aktiv"] = d._glide_modal_active
        d.destroy()

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    u.pruefe(beobachtet.get("aktiv") is True, "nach gescheitertem Griff wurde nicht gewartet")
    u.pruefe(len(u.protokoll) == 1 and "grab_set fehlgeschlagen" in u.protokoll[0],
             f"Protokoll: {u.protokoll}")
    u.protokoll.clear()


def fall_abbruch_im_warten(u):
    """Bricht das Warten mit einer Ausnahme ab, wird freigegeben und der Vorgänger erhält den Griff."""
    a = u.dialog(titel="A")
    stand = {}
    original = u.root.wait_window

    def unter():
        b = u.dialog(master=a, titel="B")

        def abbrechen(fenster=None):
            stand["griff_vorher"] = u.grab()
            raise KeyboardInterrupt("Abbruch im Warten")

        u.root.wait_window = abbrechen
        try:
            u.app.run_modal(b)
        except KeyboardInterrupt:
            stand["ausnahme"] = True
        finally:
            u.root.wait_window = original
        stand["b_status"] = b.grab_status() if b.winfo_exists() else "weg"
        stand["b_aktiv"] = b._glide_modal_active
        stand["nach"] = u.grab()
        b.destroy()

    u.ablauf([unter, lambda: None, a.destroy])
    u.laufen(lambda: u.app.run_modal(a))
    u.pruefe(stand.get("ausnahme"), f"Ausnahme kam nicht beim Aufrufer an: {stand}")
    u.pruefe(stand.get("griff_vorher") is not None and stand["griff_vorher"] is not a,
             f"B hielt vor dem Abbruch keinen Griff: {stand}")
    u.pruefe(stand.get("b_status") in ("", None), f"B behielt den Griff: {stand}")
    u.pruefe(stand.get("b_aktiv") is False, f"B blieb aktiv markiert: {stand}")
    u.pruefe(stand.get("nach") is a, f"Griff nicht an A zurück: {stand}")
    u.pruefe(u.grab() is None, "Griff nach A nicht frei")


def fall_wiederverwendbar(u):
    """Mit `_glide_modal_finished` endet das Warten ohne Zerstören; der Dialog bleibt nutzbar."""
    d = u.dialog()
    d._glide_modal_finished = u.tk.BooleanVar(master=d, value=False)
    for runde in (1, 2):
        d._glide_modal_finished.set(False)
        stand = {}

        def fertig(stand=stand):
            stand["grab"] = u.grab()
            stand["sichtbar"] = d.state()
            d.withdraw()
            d._glide_modal_finished.set(True)

        u.ablauf([fertig])
        u.laufen(lambda: u.app.run_modal(d))
        u.pruefe(stand.get("grab") is d, f"Runde {runde}: kein Griff während des Wartens")
        u.pruefe(d.winfo_exists(), f"Runde {runde}: Dialog wurde zerstört")
        u.pruefe(d.grab_status() in ("", None), f"Runde {runde}: Griff nicht freigegeben")
        u.pruefe(d._glide_modal_active is False, f"Runde {runde}: bleibt aktiv markiert")
        u.pruefe(u.grab() is None, f"Runde {runde}: Griff nicht frei")
        # bring_dialog_to_front holt den zurückgezogenen Dialog wieder hervor.
        u.pruefe(stand.get("sichtbar") == "normal", f"Runde {runde}: Dialog nicht sichtbar: {stand}")
    d.destroy()


def fall_wiederholt(u):
    """Wiederholtes Öffnen und Schließen hinterlässt weder Griff noch Zeitgeber."""
    def auftraege():
        return set(u.root.tk.splitlist(u.root.tk.call("after", "info")))

    vorher = auftraege()
    for runde in range(WIEDERHOLUNGEN):
        d = u.dialog(titel=f"Runde {runde}")
        u.root.after(5, d.destroy)
        u.laufen(lambda d=d: u.app.run_modal(d))
        u.pruefe(u.grab() is None, f"Runde {runde}: Griff nicht frei")
    u.root.update()
    rest = auftraege() - vorher
    u.pruefe(not rest, f"liegengebliebene Zeitgeber: {sorted(rest)}")
    u.pruefe(not [k for k in u.root.winfo_children() if isinstance(k, u.tk.Toplevel)],
             "liegengebliebene Toplevels")


def fall_fokus(u):
    """Der Dialog erhält den Fokus; nach dem Schließen kehrt er ins aufrufende Fenster zurück (D87).

    `run_modal` holt den Dialog nach vorn (`focus_force`). Seit 3.65.0 gibt
    die Shell den Fokus danach selbst zurück – auch wenn der Aufrufer vor
    `run_modal` schon ein Feld im Dialog fokussiert hat.
    """
    feld = u.feld_im_hauptfenster()
    d = u.dialog()
    d.nametowidget("eingabe").focus_set()
    stand = {}

    def waehrend():
        u.root.update_idletasks()
        stand["fokus"] = d.focus_get()
        d.destroy()

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    fokus = stand.get("fokus")
    u.pruefe(fokus is not None and str(fokus).startswith(str(d)),
             f"Fokus lag während des Wartens nicht im Dialog: {fokus!r}")
    u.pruefe_fokus(u.root, feld, "nach dem Schließen")


def fall_fokus_verschoben(u):
    """Verschiebt etwas den Fokus im Hauptfenster während des Wartens, gilt danach der Stand von vorher."""
    feld = u.feld_im_hauptfenster()
    knopf = u.tk.Button(u.root, text="anderes Ziel", name="anderes_ziel")
    knopf.pack()
    d = u.dialog()

    def waehrend():
        knopf.focus_set()
        u.root.update_idletasks()
        d.destroy()

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    u.pruefe_fokus(u.root, feld, "nach verschobenem Fokus")


def fall_fokus_verschachtelt(u):
    """Ein Unterdialog gibt den Fokus an das Feld der Maske zurück, nicht an das Hauptfenster."""
    u.feld_im_hauptfenster()
    a = u.dialog(titel="Maske")
    zweites = u.tk.Entry(a, name="zweites")
    zweites.pack()
    stand = {}

    def b_oeffnen():
        zweites.focus_set()
        u.root.update_idletasks()
        b = u.dialog(titel="Unterdialog")          # Master ist das Hauptfenster
        u.root.after(SCHRITT_MS, b.destroy)
        u.app.run_modal(b)
        u.root.update_idletasks()
        stand["fokus"] = u.fokus()
        stand["lastfor"] = a.focus_lastfor()
        a.destroy()

    u.ablauf([b_oeffnen])
    u.laufen(lambda: u.app.run_modal(a))
    u.pruefe(stand.get("lastfor") is zweites, f"Maske merkt sich nach dem Unterdialog {stand.get('lastfor')!r}")
    u.pruefe(stand.get("fokus") in (None, zweites), f"Fokus nach dem Unterdialog: {stand.get('fokus')!r}")


def fall_fokus_ziel_weg(u):
    """Verschwindet das gemerkte Widget, erhält sein Fenster den Fokus – ohne Fehler."""
    feld = u.feld_im_hauptfenster()
    d = u.dialog()

    def waehrend():
        feld.destroy()
        d.destroy()

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    fokus = u.fokus()
    u.pruefe(fokus is None or fokus.winfo_toplevel() is u.root, f"Fokus nach verschwundenem Ziel: {fokus!r}")
    u.pruefe(not u.protokoll, f"unerwarteter Protokolleintrag: {u.protokoll}")


def fall_fokus_drittes_fenster(u):
    """Öffnet der Dialog ein drittes Fenster und schließt dann, behält dieses den Fokus."""
    feld = u.feld_im_hauptfenster()
    d = u.dialog()
    stand = {}

    def waehrend():
        drittes = u.tk.Toplevel(u.root)
        drittes.geometry("240x100+200+200")
        eingabe = u.tk.Entry(drittes)
        eingabe.pack()
        drittes.deiconify()
        drittes.lift()
        drittes.update()
        try:
            d.grab_release()
        except u.tk.TclError:
            pass
        drittes.focus_force()
        eingabe.focus_force()
        drittes.update()
        stand["drittes"] = drittes
        stand["vorher"] = u.fokus()
        d.destroy()

    def im_dritten(widget):
        # Windows legt den Fokus nach focus_force zunächst auf das Toplevel
        # selbst, macOS und X11 auf das Feld; der Vertrag gilt fensterweit.
        try:
            return widget is not None and widget.winfo_toplevel() is stand.get("drittes")
        except (KeyError, u.tk.TclError):
            return False

    u.ablauf([waehrend])
    u.laufen(lambda: u.app.run_modal(d))
    u.root.update_idletasks()
    fokus = u.fokus()
    u.pruefe(im_dritten(stand.get("vorher")), f"Vorbedingung: drittes Fenster hatte keinen Fokus ({stand.get('vorher')!r})")
    u.pruefe(im_dritten(fokus), f"drittes Fenster verlor den Fokus an {fokus!r}")
    u.pruefe(u.root.focus_lastfor() is feld, "der gemerkte Fokus des Hauptfensters ging verloren")


def fall_menue(u):
    """Ein Menübefehl kehrt sofort zurück; seine Arbeit öffnet im Leerlauf einen Unterdialog."""
    a = u.dialog(titel="A")
    menue = u.tk.Menu(u.root, tearoff=0)
    stand = {"lauf": 0}

    def befehl():
        stand["lauf"] += 1
        b = u.dialog(master=a, titel="aus dem Menü")
        u.root.after(SCHRITT_MS, b.destroy)
        u.app.run_modal(b)
        stand["nach_b"] = u.grab()

    menue.add_command(label="Unterdialog", command=befehl)

    def ausloesen():
        menue.invoke(0)
        stand["sofort"] = stand["lauf"]

    u.ablauf([ausloesen, lambda: None, lambda: None, lambda: None, a.destroy])
    u.laufen(lambda: u.app.run_modal(a))
    menue.destroy()
    u.pruefe(stand.get("sofort") == 0, f"Menübefehl lief noch im Aufruf: {stand}")
    u.pruefe(stand["lauf"] == 1, f"Menübefehl lief nicht genau einmal: {stand}")
    u.pruefe(stand.get("nach_b") is a, f"Griff nach dem Menüdialog nicht bei A: {stand}")


def fall_hauptfenster_abbau(u):
    """Wird das Hauptfenster während eines Dialogs abgebaut, kehrt `run_modal` ohne Ausnahme zurück."""
    a = u.dialog(titel="A")
    stand = {}

    def unter():
        b = u.dialog(master=a, titel="B")
        try:
            u.app.run_modal(b)
            stand["b"] = "zurück"
        except Exception:
            stand["b"] = traceback.format_exc()

    u.ablauf([unter, lambda: None, u.root.destroy])
    try:
        u.app.run_modal(a)
        stand["a"] = "zurück"
    except Exception:
        stand["a"] = traceback.format_exc()
    u.pruefe(stand.get("b") == "zurück", f"Unterdialog: {stand.get('b')}")
    u.pruefe(stand.get("a") == "zurück", f"Dialog: {stand.get('a')}")
    try:
        lebt = bool(u.root.winfo_exists())
    except u.tk.TclError:
        lebt = False
    u.pruefe(not lebt, "Hauptfenster besteht noch")


FAELLE = {
    "grundvertrag": fall_grundvertrag,
    "escape": fall_escape,
    "eventloop": fall_eventloop,
    "verschachtelt": fall_verschachtelt,
    "parent": fall_parent,
    "besitzer_weg": fall_besitzer_weg,
    "grab_fehlschlag": fall_grab_fehlschlag,
    "abbruch_im_warten": fall_abbruch_im_warten,
    "wiederverwendbar": fall_wiederverwendbar,
    "wiederholt": fall_wiederholt,
    "fokus": fall_fokus,
    "fokus_verschoben": fall_fokus_verschoben,
    "fokus_verschachtelt": fall_fokus_verschachtelt,
    "fokus_ziel_weg": fall_fokus_ziel_weg,
    "fokus_drittes_fenster": fall_fokus_drittes_fenster,
    "menue": fall_menue,
    "hauptfenster_abbau": fall_hauptfenster_abbau,
}


# Name: (Funktion in modal_session.py, entfernte Schutzzeile, Ersatz, Fall, der rot werden muss)
NL = "\n"
SHELL_MODUL = "modal_session.py"
GEGENPROBEN = {
    "ohne_griff": ("wait_modal", "dialog.grab_set()", "pass", "grundvertrag"),
    "ohne_freigabe": ("wait_modal", "dialog.grab_release()", "pass", "wiederverwendbar"),
    "ohne_aktivmarke_ende": ("wait_modal", "setattr(dialog, ACTIVE_ATTRIBUTE, False)", "pass", "grundvertrag"),
    "ohne_grabschutz": ("wait_modal", r'log_error(f"grab_set fehlgeschlagen: {fehler}\n")', "raise",
                        "grab_fehlschlag"),
    "ohne_wartevariable": ("wait_modal", "finished = getattr(dialog, FINISHED_ATTRIBUTE, None)",
                           "finished = None", "wiederverwendbar"),
    "ohne_rueckgabe": ("modal_over", "owner.grab_set()", "pass", "verschachtelt"),
    "ohne_fokusrueckgabe": ("return_focus", "target.focus_set()", "pass", "fokus_verschoben"),
    "ohne_fokusmerken": ("remember_focus", "widget = window.focus_lastfor()", "widget = None",
                         "fokus_verschoben"),
    "ohne_fremdfensterschutz": ("return_focus", "return False  # ein drittes Fenster behält den Fokus",
                                "pass", "fokus_drittes_fenster"),
}


def mutiere(text, funktion, alt, neu):
    """Ersetzt genau eine ganze Zeile `alt` (ohne Einrückung) im Körper der Modulfunktion `funktion`."""
    anfang = text.index(f"{NL}def {funktion}(")
    folgen = [i for i in (text.find(NL + "def ", anfang + 1), text.find(NL + "@", anfang + 1)) if i != -1]
    ende = min(folgen) if folgen else len(text)
    zeilen = text[anfang:ende].split(NL)
    treffer = [i for i, zeile in enumerate(zeilen) if zeile.strip() == alt]
    if len(treffer) != 1:
        raise Vertragsbruch(f"Gegenprobe findet ihre Zeile in {funktion} nicht genau einmal: {alt!r}")
    zeile = zeilen[treffer[0]]
    zeilen[treffer[0]] = zeile[:len(zeile) - len(zeile.lstrip())] + neu
    return text[:anfang] + NL.join(zeilen) + text[ende:]


def gegenproben():
    modul = (SOURCE.parent / SHELL_MODUL).read_bytes().decode("utf-8")
    app = SOURCE.read_bytes()
    umgebung = dict(os.environ, PYTHONPATH=os.pathsep.join(
        [str(SOURCE.parent)] + ([os.environ["PYTHONPATH"]] if os.environ.get("PYTHONPATH") else [])),
        PYTHONIOENCODING="utf-8")
    befunde = []
    with tempfile.TemporaryDirectory(prefix="glide-modal-gp-") as ordner:
        for name, (funktion, alt, neu, fall) in GEGENPROBEN.items():
            # app.pyw stellt seinen eigenen Ordner vorn in den Suchpfad: Die
            # veränderte Modulkopie daneben gewinnt, alle übrigen Module kommen
            # über PYTHONPATH aus der Quelle.
            ziel = pathlib.Path(ordner) / name
            ziel.mkdir()
            (ziel / "app.pyw").write_bytes(app)
            (ziel / SHELL_MODUL).write_bytes(mutiere(modul, funktion, alt, neu).encode("utf-8"))
            try:
                lauf = subprocess.run([sys.executable, "-B", __file__, "--quelle", str(ziel / "app.pyw"),
                                       "--fall", fall],
                                      capture_output=True, text=True, encoding="utf-8", errors="replace",
                                      env=umgebung, timeout=ZEITLIMIT + 30)
                erkannt = lauf.returncode != 0 and f"ROT {fall}" in lauf.stdout
                hinweis = lauf.stdout.strip().splitlines()[-1:] if lauf.stdout.strip() else [lauf.stderr[-300:]]
            except subprocess.TimeoutExpired:
                erkannt, hinweis = False, ["Zeitlimit"]
            befunde.append((name, fall, erkannt, hinweis))
    for name, fall, erkannt, hinweis in befunde:
        print(f"  {'erkannt  ' if erkannt else 'ÜBERSEHEN'} {name} -> {fall}: {' '.join(hinweis)}")
    uebersehen = [name for name, _fall, erkannt, _h in befunde if not erkannt]
    if uebersehen:
        print(f"Modalvertrag-Gegenproben: {len(uebersehen)} von {len(befunde)} übersehen")
        return 1
    print(f"Modalvertrag-Gegenproben: OK ({len(befunde)} Schutzzeilen, jede vom zuständigen Fall erkannt)")
    return 0


def main():
    global SOURCE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--fall", choices=sorted(FAELLE), action="append")
    parser.add_argument("--gegenproben", action="store_true", help="Schutzzeilen entfernen und Erkennung prüfen")
    parser.add_argument("--quelle", type=pathlib.Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.quelle:
        SOURCE = args.quelle.resolve()
    if args.gegenproben:
        return gegenproben()
    namen = args.fall or list(FAELLE)
    ergebnisse = []
    with tempfile.TemporaryDirectory(prefix="glide-modal-") as temp_root:
        mod = lade_app(temp_root)
        for name in namen:
            faulthandler.dump_traceback_later(ZEITLIMIT, exit=True)
            u = Umgebung(mod)
            try:
                FAELLE[name](u)
                ergebnisse.append((name, None))
            except Exception:
                ergebnisse.append((name, traceback.format_exc()))
            finally:
                faulthandler.cancel_dump_traceback_later()
                u.zerlegen()
    rot = [(name, text) for name, text in ergebnisse if text]
    for name, text in ergebnisse:
        print(f"  {'OK ' if not text else 'ROT'} {name}")
    for name, text in rot:
        print(f"\n--- {name} ---\n{text}", file=sys.stderr)
    if rot:
        print(f"Modalvertrag: {len(rot)} von {len(ergebnisse)} Fällen rot")
        return 1
    print(f"Modalvertrag: OK ({len(ergebnisse)} Fälle, echter Grab, Tk {mod.tk.TkVersion})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
