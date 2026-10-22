"""FP-01 Wiederholen nach Rückgängig: echte Tastenwege, Bytevergleich des Bestands.

Jeder Fall prüft eine Abnahme aus dem Entwicklungsplan (FP-01, Kriterien 1–5)
mit künstlichen Daten in einem temporären Datenordner. Rückgängig und
Wiederholen laufen über die tatsächlichen Tastenbindungen am Fenster; der
Bestand wird aus der gespeicherten Datei gelesen und als JSON-Bytes verglichen.
`--app` erlaubt die rote Gegenprobe gegen die Vorversion, `--fall` einzelne Fälle.
"""
import argparse
import importlib.machinery
import importlib.util
import json
import os
import sys
import tempfile
import traceback
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
FAELLE = ("matrix", "gueltigkeit", "schreibfehler", "fokusbuchung", "editoren", "pinnwand",
          "bedienwege", "verlauf", "messung")
HEUTE = date.today().isoformat()
MORGEN = (date.today() + timedelta(days=1)).isoformat()


class Lauf:
    def __init__(self, app_path, data):
        os.environ["GLIDE_DATA_DIR"] = data
        os.environ["GLIDE_TEST_MODE"] = "1"
        sys.path.insert(0, str(Path(app_path).parent))
        loader = importlib.machinery.SourceFileLoader("glide_redo_" + str(abs(hash(str(app_path)))), str(app_path))
        self.mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
        sys.modules[loader.name] = self.mod
        loader.exec_module(self.mod)
        self.data = data
        self.errors = []
        self.meldungen = []
        self.start()

    def start(self):
        self.root = self.mod.tk.Tk()
        self.root.geometry("1280x800+20+20")
        self.root.report_callback_exception = lambda *e: self.errors.append(
            "".join(traceback.format_exception(*e))[-600:])
        self.app = self.mod.ListApp(self.root)
        for name in ("show_info", "show_warning", "show_error"):
            setattr(self.app, name, lambda *a, _n=name, **k: self.meldungen.append((_n, a[:2])))
        self.app.ask_yes_no = lambda *a, **k: True
        self.app.themed_input_dialog = lambda *a, **k: "Gruppe"
        self.idle()

    def neustart(self):
        self.app.save_settings()
        self.root.destroy()
        self.start()

    def idle(self, runden=3):
        for _ in range(runden):
            self.root.update_idletasks()
            self.root.update()

    def ende(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    # ------------------------------------------------------------ Bestand
    def bestand(self):
        """Der gespeicherte Bestand als JSON-Bytes (Verlauf ausgenommen)."""
        with open(self.mod.SAVE_FILE, encoding="utf-8") as datei:
            daten = json.load(datei)
        teil = {key: daten.get(key) for key in ("folders", "labels", "lists", "trash")}
        return json.dumps(teil, sort_keys=True, ensure_ascii=False).encode("utf-8")

    def grundbestand(self, anzahl=0):
        """Eine Arbeitsliste mit benannten Aufgaben und eine Zielliste."""
        app = self.app
        rule = app.normalize_repeat({"art": "taeglich"}, default_start=HEUTE)
        punkte = [app.new_item(name) for name in "ABCDEFGH"]
        punkte.append(app.new_item("Wiederkehrend", due=HEUTE, repeat=rule))
        punkte.append(app.new_item("Heute geplant", planned_date=HEUTE, estimated_minutes=30))
        punkte.extend(app.new_item(f"Masse {n}") for n in range(anzahl))
        liste = app.new_list_object("Arbeit", punkte)
        ziel = app.new_list_object("Ziel", [app.new_item("Schon da")])
        app.lists.extend([liste, ziel])
        assert app.save_items()
        app.set_active_list(liste["id"])
        self.idle()
        ids = {item["text"]: item["id"] for item in punkte[:10]}
        ids.update(liste=liste["id"], ziel=ziel["id"])
        return ids

    def waehle(self, *item_ids):
        tree = self.app.tree
        tree.selection_set(item_ids)
        tree.focus(item_ids[-1])
        self.idle(1)

    def taste(self, sequenz, widget=None):
        """Echter Tastendruck am fokussierten Widget, Fensterbindung inklusive."""
        widget = widget or self.app.tree
        widget.focus_force()
        self.idle(2)
        widget.event_generate(sequenz)
        self.idle(2)

    def rueckgaengig(self, widget=None):
        self.taste("<Control-z>", widget)

    def wiederholen(self, windows_y=False, widget=None):
        self.taste("<Control-y>" if windows_y else "<Control-Shift-Z>", widget)


def abweichung(vor, ist, nach):
    """Teile des Bestands, die nach Rückgängig weder dem Vorher- noch dem Nachher-Stand gleichen."""
    alt, jetzt, danach = (json.loads(stand) for stand in (vor, ist, nach))
    return {key: ("wie nach der Aktion" if jetzt[key] == danach[key] else "abweichend")
            for key in alt if alt[key] != jetzt[key]}


def redo_offen(lauf):
    app = lauf.app
    return bool(getattr(app, "redo_available", lambda: False)())


# ---------------------------------------------------------------- Matrix
def anlegen(lauf, ids):
    app = lauf.app
    app.set_active_list(ids["liste"])
    lauf.idle(1)
    app.entry.delete(0, "end")
    app.entry_placeholder_active = False
    app.entry.insert(0, "Neu angelegt")
    app.add_item()


def loeschen(lauf, ids):
    lauf.waehle(ids["B"])
    lauf.app.delete_item()


def verschieben(lauf, ids):
    lauf.app.set_active_list(ids["liste"])
    lauf.idle(1)
    assert lauf.app.move_items_to_list([ids["C"]], ids["ziel"])


def einruecken(lauf, ids):
    lauf.waehle(ids["D"])
    lauf.app.indent_selected()


def gruppieren(lauf, ids):
    lauf.waehle(ids["E"], ids["F"])
    lauf.app.group_selected_items()


def abhaken_wiederholung(lauf, ids):
    lauf.waehle(ids["Wiederkehrend"])
    lauf.app.toggle_done()


def einplanen(lauf, ids):
    assert lauf.app.apply_quick_plan([ids["G"]], MORGEN, toast=False)


def entlasten(lauf, ids):
    plan = lauf.app.relief_plan([ids["Heute geplant"]], MORGEN)
    assert plan.moves, "Entlastungsvorschlag ohne Verschiebung"
    assert lauf.app.apply_day_relief(plan)


def importieren(lauf, ids):
    pfad = Path(lauf.data) / "import.txt"
    pfad.write_text("- Importiert eins\n- Importiert zwei\n", encoding="utf-8")
    lauf.mod.filedialog.askopenfilename = lambda **_k: str(pfad)
    lauf.app.set_active_list(ids["liste"])
    lauf.idle(1)
    lauf.app.import_from_txt()


MATRIX = (("anlegen", anlegen), ("löschen", loeschen), ("verschieben", verschieben),
          ("einrücken", einruecken), ("gruppieren", gruppieren),
          ("abhaken mit Wiederholung", abhaken_wiederholung), ("einplanen", einplanen),
          ("entlasten", entlasten), ("importieren", importieren))


def fall_matrix(lauf):
    """Kriterium 1: genau ein Wiederholen stellt den Stand vor Rückgängig her."""
    ids = lauf.grundbestand()
    geprueft = []
    for nummer, (name, aktion) in enumerate(MATRIX):
        vor = lauf.bestand()
        aktion(lauf, ids)
        lauf.idle()
        nach = lauf.bestand()
        assert nach != vor, f"{name}: Aktion ohne Wirkung"
        tiefe = len(lauf.app.undo_stack)
        lauf.rueckgaengig()
        zurueck = lauf.bestand()
        # Diagnose seit Lauf 03 der Vollprüfung 3.44.0 (einmal rot, einzeln
        # 13/13 grün): abweichende Teile und Meldungen nennen.
        assert zurueck == vor, (f"{name}: Rückgängig stellt nicht her", abweichung(vor, zurueck, nach),
                                len(lauf.app.undo_stack), lauf.meldungen[-3:])
        assert redo_offen(lauf), f"{name}: kein Wiederholen nach Rückgängig"
        # Unter Windows wechselt die Prüfung zwischen Strg+Y und Strg+Umschalt+Z.
        lauf.wiederholen(windows_y=lauf.mod.IS_WINDOWS and nummer % 2 == 1)
        assert lauf.bestand() == nach, f"{name}: Wiederholen weicht vom Stand vor Rückgängig ab"
        assert len(lauf.app.undo_stack) == tiefe, f"{name}: Rückgängig-Tiefe nach Wiederholen"
        assert not redo_offen(lauf), f"{name}: mehr als ein Wiederholen"
        geprueft.append(name)
    # Mehrere Schritte zurück und in umgekehrter Folge wieder vor.
    staende = [lauf.bestand()]
    for _ in range(3):
        lauf.rueckgaengig()
        staende.append(lauf.bestand())
    for erwartet in reversed(staende[:-1]):
        lauf.wiederholen()
        assert lauf.bestand() == erwartet, "Mehrschrittiges Wiederholen in falscher Folge"
    assert not [m for m in lauf.meldungen if m[0] == "show_error"], lauf.meldungen
    return f"{len(geprueft)} Aktionen bytegleich wiederholt, dazu drei Schritte in Folge"


# ----------------------------------------------------------- Gültigkeit
def nach_rueckgaengig(lauf, ids, name="F"):
    lauf.waehle(ids[name])
    lauf.app.delete_item()
    lauf.idle()
    lauf.rueckgaengig()
    assert redo_offen(lauf), "Vorbedingung: Wiederholen offen"


def fall_gueltigkeit(lauf):
    """Kriterium 2: neue Änderung, Laden, Wächterabbruch, Neustart leeren; Wirkungsloses nicht."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    befunde = []

    nach_rueckgaengig(lauf, ids)
    vor = lauf.bestand()
    lauf.waehle(ids["A"])
    app.outdent_selected()  # oberste Ebene: wirkungslos
    lauf.idle()
    assert lauf.bestand() == vor and redo_offen(lauf), "Wirkungslose Aktion verwirft Wiederholen"
    befunde.append("wirkungslos bleibt")

    app.autosave_tick()
    assert redo_offen(lauf), "Sicherheitspunkt ohne Änderung verwirft Wiederholen"
    app.dirty = True
    app.autosave_tick()
    assert not redo_offen(lauf), "Autospeichern einer ausstehenden Änderung lässt Wiederholen stehen"
    befunde.append("Autospeichern")

    nach_rueckgaengig(lauf, ids)
    anlegen(lauf, ids)
    lauf.idle()
    assert not redo_offen(lauf), "Neue Änderung lässt Wiederholen stehen"
    zahl = len(lauf.meldungen)
    vor = lauf.bestand()
    lauf.wiederholen()
    assert lauf.bestand() == vor and lauf.meldungen[zahl:][0][1][0] == "Wiederholen"
    befunde.append("neue Änderung")

    nach_rueckgaengig(lauf, ids)
    eintrag, _ = app.find_item_in_lists(ids["A"])[:2]
    with app.item_change([ids["A"]], background=True) as change:
        eintrag["description"] = "Zustellbeleg"
        change.mark()
    assert not redo_offen(lauf), "Hintergrundbeleg ohne Rückgängig-Punkt lässt Wiederholen stehen"
    befunde.append("Zustellbeleg")

    nach_rueckgaengig(lauf, ids)
    with app.guarded_structural_change("Prüfung"):
        app.snapshot_undo()
        raise mod.DataIntegrityError("Prüfung")
    assert not redo_offen(lauf), "Wächterabbruch lässt Wiederholen stehen"
    befunde.append("Wächterabbruch")

    nach_rueckgaengig(lauf, ids)
    lauf.neustart()
    assert not redo_offen(lauf) and not lauf.app.undo_stack, "Neustart behält Wiederholen"
    befunde.append("Neustart")

    app = lauf.app
    app.set_active_list(ids["liste"])
    lauf.idle()
    nach_rueckgaengig(lauf, ids, "G")
    anderer = Path(lauf.data).parent / (Path(lauf.data).name + "-zweit")
    app.change_data_folder(str(anderer))
    lauf.idle()
    assert not redo_offen(lauf), "Laden eines anderen Datenordners behält Wiederholen"
    befunde.append("Laden")
    return ", ".join(befunde)


# -------------------------------------------------------- Schreibfehler
def fall_schreibfehler(lauf):
    """Scheitert das Speichern, bleiben Bestand und beide Stapel unverändert; erneut gelingt es."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    vor = lauf.bestand()
    loeschen(lauf, ids)
    lauf.idle()
    nach = lauf.bestand()
    original = mod.ListApp.write_json_atomic
    zustand = {"fehler": 0}

    def scheitert(path, payload):
        if path == mod.SAVE_FILE and zustand["fehler"]:
            zustand["fehler"] -= 1
            raise OSError("Prüfung: Schreiben gesperrt")
        return original(path, payload)

    mod.ListApp.write_json_atomic = staticmethod(scheitert)
    try:
        tiefe, liste = len(app.undo_stack), json.dumps(app.lists, sort_keys=True)
        zustand["fehler"] = 1
        lauf.rueckgaengig()
        assert lauf.bestand() == nach and json.dumps(app.lists, sort_keys=True) == liste, \
            "Gescheitertes Rückgängig ändert den Bestand"
        assert len(app.undo_stack) == tiefe and not redo_offen(lauf), "Gescheitertes Rückgängig ändert die Stapel"
        assert any(m[0] == "show_error" for m in lauf.meldungen), "Fehler nicht gemeldet"
        lauf.rueckgaengig()
        assert lauf.bestand() == vor and redo_offen(lauf), "Erneutes Rückgängig gelingt nicht"
        zustand["fehler"] = 1
        lauf.wiederholen()
        assert lauf.bestand() == vor and json.dumps(app.lists, sort_keys=True) != liste, \
            "Gescheitertes Wiederholen ändert den Bestand"
        assert len(app.undo_stack) == tiefe - 1 and redo_offen(lauf), "Gescheitertes Wiederholen ändert die Stapel"
        lauf.wiederholen()
        assert lauf.bestand() == nach and not redo_offen(lauf), "Erneutes Wiederholen gelingt nicht"
    finally:
        mod.ListApp.write_json_atomic = staticmethod(original)
    return "Rückgängig und Wiederholen je einmal gescheitert und danach gelungen"


# ------------------------------------------------------- Fokusbuchung
def fall_fokusbuchung(lauf):
    """Eine offene Fokusbuchung sperrt Rückgängig und Wiederholen gleichermaßen."""
    app = lauf.app
    ids = lauf.grundbestand()
    nach_rueckgaengig(lauf, ids)
    vor, tiefe = lauf.bestand(), len(app.undo_stack)
    app.settings["time_booking"] = {"item_id": ids["A"], "start": "2026-10-17T08:00:00+02:00"}
    original = app.recover_time_booking
    app.recover_time_booking = lambda: False
    try:
        assert app.redo_last_change() == "break" and app.undo_last_change() == "break"
        assert lauf.bestand() == vor and len(app.undo_stack) == tiefe and redo_offen(lauf)
    finally:
        app.recover_time_booking = original
        app.settings.pop("time_booking", None)
    lauf.wiederholen()
    assert not redo_offen(lauf), "Nach der Buchung wirkt Wiederholen nicht"
    return "Sperre bei offener Buchung, danach wirksam"


# ------------------------------------------------------------ Editoren
def fall_editoren(lauf):
    """Kriterium 3: Textfelder und Zeichenfläche behalten ihre eigenen Stapel."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    nach_rueckgaengig(lauf, ids)
    vor = lauf.bestand()
    for sequenz in ("<Control-Shift-Z>",) + (("<Control-y>",) if mod.IS_WINDOWS else ()):
        lauf.taste(sequenz, widget=app.entry)
        assert lauf.bestand() == vor and redo_offen(lauf), f"{sequenz} im Textfeld wirkt global"
    flaeche = mod.tk.Canvas(app.root, width=20, height=20)
    flaeche.place(x=0, y=0)
    aufrufe = []

    class Editor:
        canvas = flaeche

        def redo(self):
            aufrufe.append("redo")
            return "break"

    original = app.current_drawing_editor
    app.current_drawing_editor = lambda: Editor()
    try:
        lauf.taste("<Control-Shift-Z>", widget=flaeche)
    finally:
        app.current_drawing_editor = original
        flaeche.destroy()
    assert aufrufe == ["redo"] and lauf.bestand() == vor and redo_offen(lauf), "Zeichenfläche wirkt global"
    return "Textfeld und Zeichenfläche ohne globale Wirkung"


# ------------------------------------------------------------ Pinnwand
def fall_pinnwand(lauf):
    """Stufe 2: Flächenänderungen der Pinnwand lassen sich wiederholen."""
    app = lauf.app
    ids = lauf.grundbestand()
    app.open_board_view()
    lauf.idle()
    flaeche = app.workspace
    scope = flaeche.context()

    def bereich(name):
        def change():
            board = app.settings["pinboards"].setdefault(scope, json.loads(json.dumps(flaeche.board(scope))))
            board.setdefault("areas", []).append({"id": name, "name": name, "color": "accent",
                                                   "x": 10, "y": 10, "w": 200, "h": 120})
        assert flaeche.board_view_change(change, f"Bereich „{name}“ angelegt")
        lauf.idle()

    # In der Pinnwand ist die Fläche fokussiert, nicht der verdeckte Aufgabenbaum.
    def zurueck():
        lauf.rueckgaengig(widget=app.workspace.canvas if app.workspace.mode == "board" else None)

    def vor():
        lauf.wiederholen(widget=app.workspace.canvas if app.workspace.mode == "board" else None)

    leer = json.dumps(app.settings["pinboards"].get(scope), sort_keys=True)
    bereich("eins")
    mit = json.dumps(app.settings["pinboards"].get(scope), sort_keys=True)
    zurueck()
    assert json.dumps(app.settings["pinboards"].get(scope), sort_keys=True) == leer, "Fläche nicht zurück"
    assert redo_offen(lauf), "Kein Wiederholen nach Flächen-Rückgängig"
    vor()
    assert json.dumps(app.settings["pinboards"].get(scope), sort_keys=True) == mit, "Fläche nicht wiederholt"
    zurueck()
    assert json.dumps(app.settings["pinboards"].get(scope), sort_keys=True) == leer, "Wiederholte Fläche nicht zurück"
    bereich("zwei")
    assert not redo_offen(lauf), "Neue Flächenänderung lässt Wiederholen stehen"
    # Gemischte Folge: Punktänderung, dann Fläche; zurück in umgekehrter Folge, vor in richtiger.
    app.workspace.set_mode("list")
    lauf.idle()
    anlegen(lauf, ids)
    lauf.idle()
    app.open_board_view()
    lauf.idle()
    bereich("drei")
    staende = [(lauf.bestand(), json.dumps(app.settings["pinboards"].get(scope), sort_keys=True))]
    for _ in range(2):
        zurueck()
        staende.append((lauf.bestand(), json.dumps(app.settings["pinboards"].get(scope), sort_keys=True)))
    assert staende[0][0] == staende[1][0] and staende[1][1] != staende[0][1], "Erst die Fläche zurück"
    assert staende[2][0] != staende[1][0], "Dann die Punktänderung zurück"
    for erwartet in reversed(staende[:-1]):
        vor()
        jetzt = (lauf.bestand(), json.dumps(app.settings["pinboards"].get(scope), sort_keys=True))
        assert jetzt == erwartet, "Gemischtes Wiederholen in falscher Folge"
    return "Fläche wiederholt, neue Fläche verwirft, gemischte Folge richtig"


# ---------------------------------------------------------- Bedienwege
def knopf_text(knopf):
    return str(getattr(knopf, "text", "") or "")


def fall_bedienwege(lauf):
    """Kriterium 5: Menü, Palette, Kürzel und Hinweis lösen dieselbe Kennung aus."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    eintraege = [e for e in app.app_action_entries() if e["id"] == "redo_last_change"]
    assert eintraege, "Bearbeiten › Wiederholen fehlt"
    menue = eintraege[0]
    assert menue["group"] == "Bearbeiten" and menue["shortcut"] == app.redo_accel(), menue
    erwartet = "Strg+Y" if mod.IS_WINDOWS else ("Cmd+Shift+Z" if mod.IS_MACOS else "Strg+Shift+Z")
    assert app.redo_accel() == erwartet, app.redo_accel()

    loeschen(lauf, ids)
    lauf.idle()
    nach = lauf.bestand()
    lauf.rueckgaengig()
    app.invoke_app_action({"id": "redo_last_change"})
    lauf.idle()
    assert lauf.bestand() == nach and not redo_offen(lauf), "Palette/Menü wiederholt nicht"

    # Hinweis: „Rückgängig“ im Hinweis, danach bietet derselbe Hinweis „Wiederholen“.
    lauf.waehle(ids["G"])
    app.delete_item()
    lauf.idle()
    nach = lauf.bestand()
    hinweis = getattr(app, "_undo_toast", None)
    assert hinweis and knopf_text(hinweis["button"]) == "Rückgängig", "Kein Rückgängig-Hinweis nach Löschen"
    hinweis["button"].command()
    lauf.idle()
    assert lauf.bestand() != nach and redo_offen(lauf)
    hinweis = getattr(app, "_undo_toast", None)
    assert hinweis and knopf_text(hinweis["button"]) == "Wiederholen", "Hinweis bietet kein Wiederholen"
    hinweis["button"].command()
    lauf.idle()
    assert lauf.bestand() == nach and not redo_offen(lauf), "Wiederholen im Hinweis wirkt nicht"

    # Überlaufmenü der Kopfzeile und Kürzelübersicht nennen Wiederholen.
    texte = []
    original = mod.tk.Menu.tk_popup
    mod.tk.Menu.tk_popup = lambda menu, *a, **k: texte.extend(
        menu.entrycget(i, "label") for i in range(menu.index("end") + 1) if menu.type(i) == "command")
    try:
        app.show_header_overflow_menu()
    finally:
        mod.tk.Menu.tk_popup = original
    assert "Wiederholen" in texte, texte
    return "Menü, Palette, Kürzel, Hinweis und Überlaufmenü über redo_last_change"


# --------------------------------------------------------------- Verlauf
def fall_verlauf(lauf):
    """Stufe 2: Der Änderungsverlauf verweist für ältere Stände auf „Sicherungen vergleichen“."""
    app, mod = lauf.app, lauf.mod
    lauf.grundbestand()
    app.open_history_view()
    lauf.idle()
    gefunden = []
    stapel = [app.home_content]
    while stapel:
        widget = stapel.pop()
        stapel.extend(widget.winfo_children())
        if isinstance(widget, mod.RoundedButton) and knopf_text(widget) == "Sicherungen vergleichen":
            gefunden.append(widget)
    assert gefunden, "Kein Verweis auf „Sicherungen vergleichen“ im Verlauf"
    aufrufe = []
    app.show_backup_compare_dialog = lambda *a, **k: aufrufe.append(1)
    gefunden[0].command()
    lauf.idle()
    assert aufrufe == [1], "Verweis öffnet den Sicherungsvergleich nicht"
    return "Knopf vorhanden und wirksam"


# --------------------------------------------------------------- Messung
def fall_messung(lauf):
    """Kriterium 4: Zusatzspeicher bei 10.000 Punkten und Grenze von 20 Schritten.

    Die Zeit des Abhakens bei 5.000 Punkten misst `scripts/pflege/messung_speicherweg.py`
    wie in §10 über `item_change`; Ergebnisse stehen im Nachweis.
    """
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand(anzahl=9990)
    masse = [item["id"] for item in app.current_list()["items"] if item["text"].startswith("Masse")]
    for item_id in masse[:mod.ListApp.MAX_UNDO_STEPS + 2]:
        punkt = app.find_item_in_lists(item_id)[0]
        with app.item_change([item_id]) as change:
            punkt["importance"] = 1
            change.mark()
    assert len(app.undo_stack) == mod.ListApp.MAX_UNDO_STEPS
    for _ in range(mod.ListApp.MAX_UNDO_STEPS):
        assert app.undo_last_change() == "break"
    lauf.idle()
    assert not app.undo_stack and len(app.redo_steps()) == mod.ListApp.MAX_UNDO_STEPS, "Grenze von 20 Schritten"
    eintrag = app.redo_steps().peek()
    zusatz = sum(len(v.data) for v in eintrag.values() if isinstance(v, mod.PackedState))
    bericht = {"punkte": sum(len(entry.get("items", [])) for entry in app.lists),
               "zusatz_je_schritt_bytes": zusatz, "zusatz_20_schritte_bytes": zusatz * mod.ListApp.MAX_UNDO_STEPS}
    print("MESSUNG " + json.dumps(bericht, ensure_ascii=False), flush=True)
    for _ in range(mod.ListApp.MAX_UNDO_STEPS):
        assert app.redo_last_change() == "break"
    assert len(app.undo_stack) == mod.ListApp.MAX_UNDO_STEPS and not app.redo_available()
    gesetzt = sum(1 for item_id in masse[:mod.ListApp.MAX_UNDO_STEPS + 2]
                  if app.find_item_in_lists(item_id)[0].get("importance") == 1)
    assert gesetzt == mod.ListApp.MAX_UNDO_STEPS + 2, "20 Schritte zurück und vor ergeben nicht den Stand davor"
    return (f"{bericht['punkte']} Punkte: Zusatz je Schritt {zusatz / 1024:.0f} KiB, "
            f"bei 20 Schritten {zusatz * 20 / 1024 / 1024:.1f} MiB; 20 zurück und 20 vor")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    ergebnis = {"app": str(args.app), "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix=f"glide-redo-{name}-") as daten:
            lauf = None
            try:
                lauf = Lauf(args.app, daten)
                text = globals()["fall_" + name](lauf)
                if lauf.errors:
                    raise AssertionError(("Rückruffehler", lauf.errors[:2]))
                ergebnis["faelle"][name] = {"ok": True, "befund": text}
                print(f"OK {name}: {text}", flush=True)
            except Exception as fehler:  # Bericht je Fall, Gesamtergebnis unten
                ergebnis["faelle"][name] = {"ok": False, "befund": repr(fehler)[:600]}
                ergebnis["fehler"].append(name)
                print(f"ROT {name}: {fehler!r}"[:700], flush=True)
            finally:
                if lauf is not None:
                    lauf.ende()
    if args.report:
        args.report.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"gruen": len(ergebnis["faelle"]) - len(ergebnis["fehler"]), "rot": ergebnis["fehler"]},
                     ensure_ascii=False))
    return 1 if ergebnis["fehler"] else 0


if __name__ == "__main__":
    sys.exit(main())
