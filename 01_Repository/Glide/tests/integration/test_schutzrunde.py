"""Schutzrunde WA-27 bis WA-30: Wächter, Laden, Editorübernahme, Datensperre.

Die Fälle stammen aus den Proben der Standanalyse vom 18.10.2026 (A32, A34,
A35, A36) und prüfen jetzt das richtige Verhalten: echte `ListApp` mit Tk,
künstliche Daten in einem temporären Datenordner (vor dem Import gesetzt),
gespeicherte Datei als Bytes. `--app` erlaubt die rote Gegenprobe gegen den
Stand vor der Korrektur, `--fall` einzelne Fälle.
"""
import argparse
import copy
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
FAELLE = ("waechter", "rueckweg", "laden", "flush", "editorwechsel", "sperre", "sperre_prozesse",
          "ausgaben", "editor_offen", "rueckweg_bytes", "sitzung", "speicherergebnis", "mehrfach",
          "struktur_ergebnis", "struktur_dialog", "struktur_editor")
FEHLERTITEL_OK = "Abgebrochen – keine Daten verloren"


class Lauf:
    def __init__(self, app_path, data):
        self.app_path = Path(app_path)
        os.environ["GLIDE_DATA_DIR"] = data
        os.environ["GLIDE_TEST_MODE"] = "1"
        sys.path.insert(0, str(self.app_path.parent))
        if self.app_path.parent.name == "Archiv":
            # Archivierte Hauptdatei: Begleitmodule liegen eine Ebene höher
            # (07_Python-Versionen/Archiv/README.md).
            sys.path.append(str(self.app_path.parent.parent))
        loader = importlib.machinery.SourceFileLoader("glide_schutz_" + str(abs(hash(str(app_path)))),
                                                      str(app_path))
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
        self.ende()
        self.start()

    def idle(self, runden=3):
        for _ in range(runden):
            self.root.update_idletasks()
            self.root.update()

    def ende(self):
        try:
            # Dieser Neustart ersetzt den gesamten Tcl-Interpreter. Vor dem
            # Testabbau die Instanzbindungen lösen, damit nachlaufende
            # Auswahl-/Configure-Ereignisse keine halb zerstörte Ansicht lesen.
            def unbind_tree(widget):
                for child in widget.winfo_children():
                    unbind_tree(child)
                for sequence in widget.bind():
                    widget.unbind(sequence)
            unbind_tree(self.root)
            for sequence in self.root.tk.splitlist(self.root.tk.call("bind", "all")):
                self.root.unbind_all(sequence)
            self.app.cancel_pending_callbacks()
            # Auch widgeteigene Jobs vor dem Abbau des Tcl-Interpreters
            # entfernen; sonst treffen sie den Interpreter des nächsten Falls.
            for job in self.root.tk.splitlist(self.root.tk.call("after", "info")):
                self.root.after_cancel(job)
            finish_session = getattr(self.app, "finish_recovery_session", None)
            if finish_session is not None:
                finish_session()
            self.app.release_data_lock()
            self.root.destroy()
        except Exception:
            pass

    def datei(self):
        return Path(self.mod.SAVE_FILE).read_bytes()

    def datei_ids(self):
        daten = json.loads(self.datei().decode("utf-8"))
        ids = set()
        for eintrag in daten.get("lists", []):
            ids |= self.mod.ListApp.collect_item_ids(eintrag.get("items", []))
        return ids

    def fehlertitel(self):
        return [meldung[1][0] for meldung in self.meldungen if meldung[0] == "show_error"]

    def grundbestand(self):
        app = self.app
        punkte = [app.new_item(name) for name in "ABCDEFGH"]
        liste = app.new_list_object("Arbeit", punkte)
        ziel = app.new_list_object("Ziel", [app.new_item("Schon da")])
        app.lists.extend([liste, ziel])
        assert app.save_items()
        app.set_active_list(liste["id"])
        self.idle()
        ids = {item["text"]: item["id"] for item in punkte}
        ids.update(liste=liste["id"], ziel=ziel["id"])
        return ids


def gleicher_ort(a, b):
    """Denselben Ort erkennen, auch wenn ihn zwei Schreibweisen bezeichnen.

    `change_data_folder` legt den neuen Datenordner über `os.path.realpath` ab.
    Liegt der Prüfordner hinter einem symbolischen Link oder unter Windows
    hinter einem 8.3-Kurznamen (GitHub-Runner: Benutzerordner `RUNNER~1`), ergibt
    das eine andere Zeichenkette für denselben Ordner. Ein reiner
    Zeichenkettenvergleich war dort rot, bei kurzen Benutzernamen grün.
    """
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


def volle_tiefe(app, tiefe):
    app.undo_stack[:] = [app.undo_state() for _ in range(tiefe)]
    return app.undo_stack[-1] if app.undo_stack else None


# ------------------------------------------------------------------ WA-27
def fall_waechter(lauf):
    """A32: Tiefe 0/19/20, direkter Schnappschuss und `item_change`; Datei bytegleich."""
    app = lauf.app
    lauf.grundbestand()
    rot = []  # alle Teilbefunde sammeln: Die Gegenprobe zeigt, welche Tiefe scheitert
    for tiefe in (0, 19, app.MAX_UNDO_STEPS):
        for variante in ("direkt", "rahmen"):
            oben = volle_tiefe(app, tiefe)
            vorher, ids_vorher = lauf.datei(), app.data_item_ids()
            lauf.meldungen.clear()
            with app.guarded_structural_change("Prüfverlust"):
                if variante == "direkt":
                    app.snapshot_undo()
                    app.items.pop()
                    app.save_items()
                else:
                    with app.item_change([], restore=False) as change:
                        app.items.pop()
                        change.mark()
            lauf.idle(1)
            fall = f"Tiefe {tiefe}/{variante}"
            if not app.data_item_ids() >= ids_vorher:
                rot.append(f"{fall}: Punkt fehlt nach dem Abbruch")
            if lauf.datei() != vorher:
                rot.append(f"{fall}: Datei nicht bytegleich")
            if len(app.undo_stack) != tiefe or (oben is not None and app.undo_stack[-1] is not oben):
                rot.append(f"{fall}: Rückgängig-Stapel {len(app.undo_stack)} statt {tiefe}")
            if lauf.fehlertitel() != [FEHLERTITEL_OK]:
                rot.append(f"{fall}: Meldung {lauf.fehlertitel()}")
            if app.dirty:
                rot.append(f"{fall}: ungespeicherte Änderung")
    assert not rot, rot
    # Ein gelungener Umbau bei vollem Stapel bleibt bei 20 Schritten.
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    lauf.meldungen.clear()
    with app.guarded_structural_change("Prüfumbau"):
        with app.item_change([app.items[0]["id"]]) as change:
            app.items.append(app.items.pop(0))
            change.mark()
    assert len(app.undo_stack) == app.MAX_UNDO_STEPS and not lauf.fehlertitel(), "Umbau bei vollem Stapel"
    ids = app.data_item_ids()
    lauf.neustart()
    assert ids <= lauf.app.data_item_ids() and ids <= lauf.datei_ids(), "Neustart: Bestand unvollständig"
    return "Tiefe 0/19/20 × Schnappschuss/Rahmen: Bestand, Datei bytegleich, Stapel, Meldung; Neustart"


def fall_rueckweg(lauf):
    """A32: Verlust nach dem Speichern, scheiterndes Zurückschreiben, Gruppieren bei vollem Stapel."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    befunde = []

    # Verlust erst nach einem gelungenen Speichern im Wächter: Der Rückweg schreibt zurück.
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    lauf.meldungen.clear()
    with app.guarded_structural_change("Spätverlust"):
        with app.item_change([ids["A"]]) as change:
            app.find_item_in_lists(ids["A"])[0]["text"] = "A geändert"
            change.mark()
        app.items.pop()
    assert app.find_item_in_lists(ids["A"])[0]["text"] == "A", "Rückweg nimmt die Änderung nicht zurück"
    assert set(ids[k] for k in "ABCDEFGH") <= lauf.datei_ids(), "Datei ohne vollständigen Bestand"
    assert lauf.fehlertitel() == [FEHLERTITEL_OK], lauf.meldungen
    befunde.append("Verlust nach Speichern")

    # Das Zurückschreiben scheitert: keine Rettungsmeldung.
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    echt = app.write_json_atomic
    zaehler = {"n": 0}

    def schreiben(pfad, inhalt):
        if pfad == mod.SAVE_FILE:
            zaehler["n"] += 1
            if zaehler["n"] > 1:
                raise OSError("Datenträger voll (Prüfung)")
        return echt(pfad, inhalt)

    app.write_json_atomic = schreiben
    lauf.meldungen.clear()
    try:
        with app.guarded_structural_change("Spätverlust"):
            with app.item_change([ids["B"]]) as change:
                app.find_item_in_lists(ids["B"])[0]["text"] = "B geändert"
                change.mark()
            app.items.pop()
    finally:
        del app.write_json_atomic
    titel = lauf.fehlertitel()
    assert FEHLERTITEL_OK not in titel, f"Rettungsmeldung trotz gescheitertem Zurückschreiben: {titel}"
    assert "Abgebrochen – noch nicht gespeichert" in titel, titel
    assert set(ids[k] for k in "ABCDEFGH") <= app.data_item_ids() and app.dirty
    assert app.save_items() and set(ids[k] for k in "ABCDEFGH") <= lauf.datei_ids()
    befunde.append("Zurückschreiben gescheitert")

    # Selbst gemeldeter Verlust bei vollem Stapel.
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    vorher = lauf.datei()
    lauf.meldungen.clear()
    with app.guarded_structural_change("Prüfmeldung"):
        app.snapshot_undo()
        app.items.pop()
        raise mod.DataIntegrityError("Prüfung")
    assert set(ids[k] for k in "ABCDEFGH") <= app.data_item_ids() and lauf.datei() == vorher
    assert lauf.fehlertitel() == [FEHLERTITEL_OK] and "1 Punkt(e)" in lauf.meldungen[-1][1][1], lauf.meldungen
    befunde.append("DataIntegrityError")

    # Echtes Gruppieren, das einen Punkt verlöre, bei vollem Stapel.
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    vorher = lauf.datei()
    hinweise = []
    app.show_undo_toast = lambda *a, **k: hinweise.append(a)
    echt_new_item = app.new_item

    def verlierend(*args, **kw):
        if kw.get("kind") == app.ITEM_KIND_GROUP and kw.get("children"):
            kw["children"] = kw["children"][:-1]
        return echt_new_item(*args, **kw)

    app.new_item = verlierend
    lauf.meldungen.clear()
    try:
        auswahl = [app.items[0]["id"], app.items[1]["id"]]
        app.tree.selection_set(auswahl)
        app.tree.focus(auswahl[0])
        lauf.idle(1)
        app.group_selected_items()
        lauf.idle(1)
    finally:
        del app.new_item
        del app.show_undo_toast
    assert set(ids[k] for k in "ABCDEFGH") <= app.data_item_ids(), "Gruppieren verliert einen Punkt"
    assert lauf.datei() == vorher, "Gruppieren: Datei nicht bytegleich"
    assert not hinweise, f"Erfolgshinweis trotz Abbruch: {hinweise}"
    assert lauf.fehlertitel() == [FEHLERTITEL_OK], lauf.meldungen
    assert len(app.undo_stack) == app.MAX_UNDO_STEPS and not app.redo_available()
    befunde.append("Gruppieren")
    return ", ".join(befunde)


# ------------------------------------------------------------------ WA-28
def fall_laden(lauf):
    """A34: Darstellungsfehler nach gültigem Lesen; echte Lese- und Formatfehler wie bisher."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    sicherungen = Path(mod.BACKUP_DIR)

    def kopien():
        return set(sicherungen.glob("liste_unlesbar_*.json")) if sicherungen.is_dir() else set()

    for methode, fehler in (("refresh_tree", mod.tk.TclError("Prüffehler beim Zeichnen")),
                            ("update_sidebar_list", ValueError("Prüffehler in der Seitenleiste"))):
        vorher, vorher_kopien = lauf.datei(), kopien()
        def einmal(*a, _m=methode, _f=fehler, **k):
            # Nur der erste Aufbau scheitert; was danach zeichnet, läuft echt.
            app.__dict__.pop(_m, None)
            raise _f

        setattr(app, methode, einmal)
        lauf.meldungen.clear()
        try:
            app.load_items()
        finally:
            app.__dict__.pop(methode, None)
        texte = [meldung[1][1] for meldung in lauf.meldungen if meldung[0] == "show_error"]
        assert not any("beschädigt" in text for text in texte), f"{methode}: als beschädigte Datei gemeldet"
        assert texte and str(fehler) in texte[0], (methode, lauf.meldungen)
        assert kopien() == vorher_kopien, f"{methode}: unnötige Kopie liste_unlesbar_*"
        assert not getattr(app, "_data_read_only", False)
        assert set(ids[k] for k in "ABCDEFGH") <= app.data_item_ids(), f"{methode}: Bestand leer"
        assert lauf.datei() == vorher
        app.refresh_tree()
        assert app.save_items() and set(ids[k] for k in "ABCDEFGH") <= lauf.datei_ids(), \
            f"{methode}: späteres Speichern schreibt nicht den gelesenen Bestand"
        app.set_active_list(ids["liste"])
        lauf.idle(1)
    # Echter Lesefehler: wie bisher Kopie und leerer Start.
    vorher_kopien = kopien()
    Path(mod.SAVE_FILE).write_text("{kaputt", encoding="utf-8")
    lauf.meldungen.clear()
    app.load_items()
    assert any("beschädigt" in meldung[1][1] for meldung in lauf.meldungen if meldung[0] == "show_error")
    assert len(kopien() - vorher_kopien) == 1
    # Neueres Format: schreibgeschützt.
    Path(mod.SAVE_FILE).write_text(json.dumps({"version": 999, "lists": []}), encoding="utf-8")
    lauf.meldungen.clear()
    app.load_items()
    assert app._data_read_only and app._read_only_reason == "newer_format"
    return "TclError/ValueError in der Ansicht behalten den Bestand; JSON-Fehler und neueres Format wie bisher"


# ------------------------------------------------------------------ WA-29
def fall_flush(lauf):
    """A35: Rückgabe für jede Editorkombination; Aufrufer mit `is False` halten an."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    seite = app.new_page_from_markdown("# Prüfseite\n\nText")
    lauf.idle()
    aufgabe = app.new_item("In der Seite")
    seite["items"].append(aufgabe)
    assert app.save_items()
    echt_editor = app.rich_note_editor
    try:
        for note, zeichnung in ((True, True), (False, True), (True, False), (False, False), (None, True)):
            app.rich_note_editor = SimpleNamespace(winfo_exists=lambda: True, flush=lambda n=note: n,
                                                   entry_id=seite["id"])
            app.flush_drawing_editor = lambda z=zeichnung: z
            erwartet = not (note is False or zeichnung is False)
            assert app.flush_rich_note() is erwartet, (note, zeichnung, app.flush_rich_note())
        app.rich_note_editor = None
        app.flush_drawing_editor = lambda: True
        assert app.flush_rich_note() is True, "ohne Editor"
        del app.flush_drawing_editor

        app.rich_note_editor = SimpleNamespace(winfo_exists=lambda: True, flush=lambda: False,
                                               entry_id=seite["id"])
        listen = len(app.lists)
        assert app.new_page_from_markdown("# Neu\n\nText") is None and len(app.lists) == listen, "Markdown"
        assert app.change_page_feature(seite["id"], "live_lists", [ids["ziel"]]) is False
        assert "live_lists" not in seite, "Seitenfunktion trotz gescheiterter Übernahme"
        app.confirm_template_preview = lambda *a, **k: True
        app.ask_template_fields = lambda *a, **k: {}
        assert app.create_list_from_template("daily") is None and len(app.lists) == listen, "Vorlage"
        assert app.apply_notion_selection(None, None, None, None, None) is False, "Notion"
        assert app.apply_page_restore(None, None, None) is False, "Seitenrestore"
        assert app.transfer_document_task(seite["id"], aufgabe["id"], ids["ziel"]) is False
        assert app.find_item_in_lists(aufgabe["id"])[3]["id"] == seite["id"], "Aufgabe trotzdem verlegt"
    finally:
        app.rich_note_editor = echt_editor
        for name in ("flush_drawing_editor", "confirm_template_preview", "ask_template_fields"):
            app.__dict__.pop(name, None)
    app._data_read_only = True
    try:
        assert app.flush_rich_note() is True, "unveränderter schreibgeschützter Editor meldet einen Fehler"
        assert app.page_markdown(seite["id"]) and app.build_page_print_html(seite["id"]), \
            "schreibgeschützter unveränderter Bestand darf nicht seine Ausgabewege verlieren"
    finally:
        app._data_read_only = False
    return ("fünf Kombinationen, kein Editor; Markdown, Seitenfunktion, Vorlage, Notion, Restore, Aufgabe verlegen; "
            "unverändert schreibgeschützt: Übernahme ohne Schreiben und Ausgabe erlaubt")


def fall_editorwechsel(lauf):
    """A35: Ein nicht übernommener Seitentext bleibt; Navigation, Anlegen und Beenden fragen."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    seite = app.new_page_from_markdown("# Prüfseite\n\nErster Absatz")
    lauf.idle()
    editor = app.rich_note_editor
    assert isinstance(editor, mod.PageEditor)
    grenze = mod.RichNoteEditor.MAX_TEXT
    befunde = []
    zerstoert = []
    try:
        mod.RichNoteEditor.MAX_TEXT = len(editor.text.get("1.0", "end-1c")) + 5
        editor.text.insert("end", "\nNachtrag über der Grenze")
        listen = len(app.lists)
        lauf.meldungen.clear()
        app.set_active_list(ids["ziel"])
        lauf.idle()
        assert app.active_list_id == seite["id"], "Wechsel trotz nicht übernommener Seite"
        assert app.rich_note_editor is editor and editor.winfo_exists(), "Editor abgebaut"
        assert "Nachtrag über der Grenze" in editor.text.get("1.0", "end-1c"), "Text verloren"
        assert any(m[0] == "show_warning" for m in lauf.meldungen), lauf.meldungen
        befunde.append("Navigation")
        app.create_new_page()
        lauf.idle()
        assert len(app.lists) == listen and app.active_list_id == seite["id"], "Neue Seite trotz offenem Text"
        befunde.append("Anlegen")
        gefragt = []
        app.ask_yes_no_cancel = lambda *a, **k: gefragt.append(a[0]) or None
        app.root.destroy = lambda: zerstoert.append(True)
        assert app._close_after_confirmation() is False and gefragt and not zerstoert, \
            f"Beenden ohne Rückfrage: {gefragt} {zerstoert}"
        befunde.append("Beenden fragt")
        app._data_read_only = True
        app.set_active_list(ids["ziel"])
        lauf.idle()
        assert app.active_list_id == ids["ziel"], "schreibgeschützt: Wechsel blockiert"
        app._data_read_only = False
        befunde.append("schreibgeschützt frei")
        # Schreibfehler: Der Text steht im Arbeitsspeicher, der Wechsel bleibt frei.
        mod.RichNoteEditor.MAX_TEXT = grenze
        app.set_active_list(seite["id"])
        lauf.idle()
        editor = app.rich_note_editor
        echt = app.write_json_atomic
        app.write_json_atomic = lambda p, d: (_ for _ in ()).throw(OSError("voll")) if p == mod.SAVE_FILE \
            else echt(p, d)
        try:
            editor.text.insert("end", "\nNachtrag im Speicher")
            app.set_active_list(ids["ziel"])
            lauf.idle()
        finally:
            del app.write_json_atomic
        assert app.active_list_id == ids["ziel"] and app.dirty
        assert "Nachtrag im Speicher" in seite["rich_note"]["text"]
        assert app.save_items()
        befunde.append("Schreibfehler frei")
    finally:
        mod.RichNoteEditor.MAX_TEXT = grenze
        app._data_read_only = False
        app.__dict__.pop("ask_yes_no_cancel", None)
        app.root.__dict__.pop("destroy", None)
    return ", ".join(befunde)


# ------------------------------------------------------------------ WA-30
def sperre_schreiben(pfad, **felder):
    jetzt = datetime.now().astimezone()
    inhalt = {"host": os.environ.get("COMPUTERNAME") or os.environ.get("HOSTNAME") or "unbekannt",
              "pid": 4, "token": "fremd", "started_at": jetzt.isoformat(), "refreshed_at": jetzt.isoformat()}
    inhalt.update(felder)
    Path(pfad).write_text(json.dumps(inhalt), encoding="utf-8")
    return inhalt


def fall_sperre(lauf):
    """A36 in einem Prozess: Probenfälle, Übernahme, Neuanlage, Verdrängung, Takt."""
    app, mod = lauf.app, lauf.mod
    lauf.grundbestand()
    probe = Path(lauf.data) / "sperrproben"
    probe.mkdir()
    jetzt = datetime.now().astimezone()
    alt = (jetzt - timedelta(hours=9)).isoformat()
    kind = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    befunde = []
    try:
        def lese(name, inhalt):
            pfad = probe / name
            pfad.write_text(inhalt, encoding="utf-8")
            return app.read_foreign_lock(str(pfad))

        assert lese("defekt.lock", "nicht json {"), "defekte Sperre gilt als frei"
        assert lese("liste.lock", "[1,2]"), "JSON-Liste gilt als frei"
        verzeichnis = probe / "verzeichnis.lock"
        verzeichnis.mkdir()
        assert app.read_foreign_lock(str(verzeichnis)), "unlesbarer Sperrpfad gilt als frei"
        assert lese("fremd.lock", json.dumps({"host": "ANDERER", "pid": 4, "token": "x",
                                              "started_at": jetzt.isoformat(), "refreshed_at": jetzt.isoformat()}))
        assert lese("alt.lock", json.dumps({"host": "ANDERER", "pid": 4, "token": "x",
                                            "started_at": alt, "refreshed_at": alt})) is None
        sperre_schreiben(probe / "lebend.lock", pid=kind.pid)
        assert app.read_foreign_lock(str(probe / "lebend.lock"))
        sperre_schreiben(probe / "tot.lock", pid=999999)
        assert app.read_foreign_lock(str(probe / "tot.lock")) is None
        befunde.append("Lesen")

        sperre = Path(mod.LOCK_FILE)
        # Dieser Fall simuliert eine regulär freigegebene Datensperre, keinen
        # Prozessabbruch. Den unabhängigen Sitzungsnachweis vorher abschließen;
        # echte ungeklärte Enden prüft test_wiederanlauf.fall_lockuebernahme.
        finish_session = getattr(app, "finish_recovery_session", None)
        if finish_session is not None:
            finish_session()
            assert json.loads(app._recovery_guard.marker_path.read_text(encoding="utf-8"))["state"] == "clean"
        app.release_data_lock()
        sperre.write_text("nicht json {", encoding="utf-8")
        info = app.acquire_data_lock()
        assert info and app._data_read_only, "defekte Sperre: Start schreibfähig"
        assert sperre.read_text(encoding="utf-8") == "nicht json {", "defekte Sperre überschrieben"
        assert app.save_items(show_error=False) is False
        assert app.take_over_data_lock() and not app._data_read_only
        assert json.loads(sperre.read_text(encoding="utf-8"))["token"] == app._lock_token["token"]
        befunde.append("defekt: schreibgeschützt, bewusste Übernahme")

        eigenes = dict(app._lock_token)
        app.mark_lock_read_only({"defective": True, "detail": "alte Warnung"})
        sperre_schreiben(sperre, pid=kind.pid, token="inzwischen-erworben")
        inzwischen = sperre.read_bytes()
        assert app.take_over_data_lock() is False and sperre.read_bytes() == inzwischen, \
            "Bestätigung einer alten Warnung verdrängt inzwischen gültige Sperre"
        sperre.write_text(json.dumps(eigenes), encoding="utf-8")
        app._data_read_only = False
        app._read_only_reason = "lock"
        befunde.append("Übernahme prüft erneut")

        sperre.unlink()
        assert app.save_items(show_error=False), "Speichern nach verschwundener Sperre"
        assert json.loads(sperre.read_text(encoding="utf-8"))["token"] == app._lock_token["token"], \
            "verschwundene Sperre nicht neu angelegt"
        befunde.append("Neuanlage")

        einstellungen = Path(mod.SETTINGS_FILE)
        app.save_settings()
        vorher = einstellungen.read_bytes()
        fenster = Path(mod.BASE_DIR) / "window.conf"
        fenster.write_text("100x100+0+0", encoding="utf-8")
        sperre_schreiben(sperre, pid=kind.pid, token="B")
        app.settings["glide_pruefwert"] = 7
        assert app.save_settings() is False, "verdrängte Instanz schreibt Einstellungen"
        assert einstellungen.read_bytes() == vorher and app._data_read_only
        app.save_window_geometry()
        assert fenster.read_text(encoding="utf-8") == "100x100+0+0", "verdrängte Instanz schreibt Fenstergröße"
        app.release_data_lock()
        assert json.loads(sperre.read_text(encoding="utf-8"))["token"] == "B", "fremde Sperre gelöscht"
        befunde.append("Verdrängung: Einstellungen, Fenster, Freigabe")
    finally:
        kind.kill()
        kind.wait(timeout=10)
    app.settings.pop("glide_pruefwert", None)
    app._data_read_only = False
    assert app.acquire_data_lock() is None and not app._data_read_only
    # Takt: Das Autospeichern erneuert den Zeitstempel auch ohne Änderung (L3).
    sperre = Path(mod.LOCK_FILE)
    inhalt = json.loads(sperre.read_text(encoding="utf-8"))
    inhalt["refreshed_at"] = alt
    sperre.write_text(json.dumps(inhalt), encoding="utf-8")
    app._lock_token = dict(app._lock_token, refreshed_at=alt)
    app.autosave_tick()
    erneuert = datetime.fromisoformat(json.loads(sperre.read_text(encoding="utf-8"))["refreshed_at"])
    assert (datetime.now().astimezone() - erneuert).total_seconds() < 120, "Autospeichern erneuert nicht"
    befunde.append("Takt")
    return ", ".join(befunde)


ERWERB = """
import importlib.machinery, importlib.util, json, sys, time
from pathlib import Path
loader = importlib.machinery.SourceFileLoader('glide_erwerb', sys.argv[1])
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(mod)
app = mod.ListApp.__new__(mod.ListApp)
gate = Path(sys.argv[2])
gate.with_name(gate.name + sys.argv[3]).touch()
deadline = time.monotonic() + 90
while not gate.exists():
    if time.monotonic() > deadline:
        raise TimeoutError('Startfreigabe fehlt')
    time.sleep(0.01)
app.acquire_data_lock()
print(json.dumps({"read_only": bool(app._data_read_only), "token": (app._lock_token or {}).get("token"),
                  "ready": True}), flush=True)
# Weiterlaufen, bis der andere Start sicher geprüft hat: Eine Sperre ohne
# lebenden Prozess darf übernommen werden.
while not gate.with_name(gate.name + '.ende').exists():
    if time.monotonic() > deadline:
        raise TimeoutError('Endfreigabe fehlt')
    time.sleep(0.01)
"""

ZWEITSTART = """
import importlib.machinery, importlib.util, json, sys
loader = importlib.machinery.SourceFileLoader('glide_zweit', sys.argv[1])
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
loader.exec_module(mod)
root = mod.tk.Tk()
app = mod.ListApp(root)
for _ in range(3):
    root.update()
zustand = {"read_only": bool(app._data_read_only), "timer": bool(app.running_timer())}
app.on_close()
try:
    zustand["closed"] = not root.winfo_exists()
except Exception:
    zustand["closed"] = True
print("ERGEBNIS " + json.dumps(zustand))
"""


def fall_sperre_prozesse(lauf):
    """A36 mit echten Prozessen: gleichzeitiger Erwerb; Zweitstart beendet sich bei laufendem Fokus."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    umgebung = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", GLIDE_TEST_MODE="1")
    besitzer = []
    for runde in range(6):
        ordner = Path(lauf.data).parent / f"{Path(lauf.data).name}-rennen{runde}"
        ordner.mkdir()
        if runde >= 3:
            sperre_schreiben(ordner / 'glide.lock', pid=999999, token='verwaist')
        gate = ordner / 'start'
        prozesse = [subprocess.Popen([sys.executable, "-B", "-c", ERWERB, str(lauf.app_path), str(gate), str(i)],
                                     env=dict(umgebung, GLIDE_DATA_DIR=str(ordner)), stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True, encoding="utf-8")
                    for i in range(2)]
        ergebnisse = []
        try:
            deadline = time.monotonic() + 90
            while not all(gate.with_name(gate.name + str(i)).exists() for i in range(2)):
                assert all(p.poll() is None for p in prozesse), 'Kind vor Startbereitschaft beendet'
                assert time.monotonic() < deadline, 'Startbereitschaft fehlt'
                time.sleep(0.02)
            gate.touch()
            # Beide bleiben am Leben, bis beide ihren Befund geliefert haben.
            for prozess in prozesse:
                ergebnisse.append(json.loads(prozess.stdout.readline()))
            gate.with_name(gate.name + '.ende').touch()
            for prozess in prozesse:
                ausgabe, fehler = prozess.communicate(timeout=30)
                assert prozess.returncode == 0, fehler[-800:]
        finally:
            for prozess in prozesse:
                if prozess.poll() is None:
                    prozess.kill()
                prozess.wait(timeout=10)
        frei = [eintrag for eintrag in ergebnisse if not eintrag["read_only"]]
        datei = json.loads((ordner / "glide.lock").read_text(encoding="utf-8"))
        besitzer.append(len(frei))
        assert len(frei) == 1 and frei[0]["token"] == datei["token"], f"Runde {runde}: {ergebnisse}"

    assert app.start_focus(ids["A"]), "Fokus startet nicht"
    einstellungen = Path(mod.SETTINGS_FILE).read_bytes()
    ergebnis = subprocess.run([sys.executable, "-B", "-c", ZWEITSTART, str(lauf.app_path)],
                              env=dict(umgebung, GLIDE_DATA_DIR=lauf.data), capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=180)
    zeile = next((z for z in ergebnis.stdout.splitlines() if z.startswith("ERGEBNIS ")), None)
    assert zeile, (ergebnis.returncode, ergebnis.stderr[-800:])
    zustand = json.loads(zeile[len("ERGEBNIS "):])
    assert zustand["read_only"] and zustand["timer"], zustand
    assert zustand["closed"], "schreibgeschützter Zweitstart lässt sich mit laufendem Fokus nicht beenden"
    assert Path(mod.SETTINGS_FILE).read_bytes() == einstellungen, "Zweitstart schreibt Einstellungen"
    app.stop_time_tracking()
    return (f"gleichzeitiger Erwerb mit Bereitschaftsschranke: fehlend/verwaist je 3 Runden {besitzer}; "
            "Zweitstart beendet sich, schreibt nichts")


def fall_ausgaben(lauf):
    """Keine Ausgabe darf einen fehlgeschlagenen Flush still übergehen."""
    app = lauf.app
    ids = lauf.grundbestand()
    seite = app.new_page_from_markdown("# Prüfseite\n\nText")
    lauf.idle()
    echt = app.rich_note_editor
    app.rich_note_editor = SimpleNamespace(winfo_exists=lambda: True, flush=lambda: False,
                                           entry_id=seite["id"])
    rot = []
    try:
        for name, args in (("partial_backup_payload", ([seite["id"]],)),
                           ("complete_backup_payload", ()), ("build_exchange_payload", ()),
                           ("page_markdown", (seite["id"],)), ("read_backup_for_compare", (None,))):
            try:
                getattr(app, name)(*args)
            except ValueError:
                pass
            else:
                rot.append(name + ": liefert veralteten Inhalt")
        if app.build_page_print_html(seite["id"]) is not None:
            rot.append("Druckseite liefert veralteten Inhalt")
        aufrufe = []
        echt_dialog = lauf.mod.filedialog.asksaveasfilename
        lauf.mod.filedialog.asksaveasfilename = lambda *a, **k: aufrufe.append(k.get("title")) or ""
        try:
            for name in ("export_as_txt", "export_as_markdown", "export_full_backup", "export_app_backup"):
                getattr(app, name)()
            app.export_page_markdown(seite["id"])
        finally:
            lauf.mod.filedialog.asksaveasfilename = echt_dialog
        if aufrufe:
            rot.append("Dateiauswahl trotz fehlender Übernahme: " + repr(aufrufe))
    finally:
        app.rich_note_editor = echt
    assert not rot, rot
    return "Teil-/Vollbackup, Austausch, Markdown, Vergleich, Drucken und fünf Exportwege halten an"


def fall_editor_offen(lauf):
    """Ein früherer Schreibfehler beweist nicht, dass neuer Text übernommen ist."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    seite = app.new_page_from_markdown("# Prüfseite\n\nText")
    lauf.idle()
    editor = app.rich_note_editor
    grenze = mod.RichNoteEditor.MAX_TEXT
    try:
        mod.RichNoteEditor.MAX_TEXT = len(editor.text.get("1.0", "end-1c")) + 3
        editor.text.insert("end", "\nNicht übernommener Nachtrag")
        app.dirty = True  # vorheriger, unabhängiger Schreibfehler
        app.set_active_list(ids["ziel"])
        assert app.active_list_id == seite["id"], "dirty=True lässt nicht übernommenen Text verschwinden"
        assert app.rich_note_editor is editor and editor.winfo_exists()
        assert "Nicht übernommener Nachtrag" in editor.text.get("1.0", "end-1c")
    finally:
        mod.RichNoteEditor.MAX_TEXT = grenze
    return "Navigation bewahrt nicht übernommenen Text auch bei vorheriger ungespeicherter Änderung"


def fall_rueckweg_bytes(lauf):
    """Auch ein später Abbruch nach erfolgreichem Zwischenspeichern bleibt bytegleich."""
    app = lauf.app
    ids = lauf.grundbestand()
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    vorher = lauf.datei()
    with app.guarded_structural_change("Später Abbruch"):
        with app.item_change([ids["A"]]) as change:
            app.find_item_in_lists(ids["A"])[0]["text"] = "Zwischenstand"
            change.mark()
        app.items.pop()
    assert lauf.datei() == vorher, "Rückweg erzeugt neue Datei statt des bytegleichen Vorzustands"
    assert app.find_item_in_lists(ids["A"])[0]["text"] == "A"
    return "Nach erfolgreichem Zwischenspeichern stellt der Abbruch die ursprünglichen Dateibytes her"


def fall_sitzung(lauf):
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    own = dict(app._lock_token)
    old = (datetime.now().astimezone() - timedelta(hours=9)).isoformat()
    lock = Path(mod.LOCK_FILE)
    lock.write_text(json.dumps(dict(own, started_at=old, refreshed_at=old)), encoding='utf-8')
    app._lock_token = dict(own, refreshed_at=old)
    script = (
        'import importlib.machinery,importlib.util,json,sys\n'
        'from pathlib import Path\n'
        'sys.path.insert(0,str(Path(sys.argv[1]).parent))\n'
        "loader=importlib.machinery.SourceFileLoader('lock_competitor',sys.argv[1])\n"
        'mod=importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name,loader))\n'
        'sys.modules[loader.name]=mod;loader.exec_module(mod)\n'
        'app=mod.ListApp.__new__(mod.ListApp);app.acquire_data_lock()\n'
        "print(json.dumps({'read_only':app._data_read_only,'token':app._lock_token}),flush=True)\n"
        'app.release_data_lock()\n')
    result = subprocess.run([sys.executable, '-B', '-c', script, str(lauf.app_path)],
                            capture_output=True, text=True, encoding='utf-8', timeout=30)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)['read_only'], 'lebende Sitzung nach Zeitablauf verdrängt'
    assert json.loads(lock.read_text(encoding='utf-8'))['token'] == own['token']
    assert app.save_items(show_error=False)

    before = lauf.datei(); writer = app.write_json_atomic
    def fail_renew(path, payload):
        if os.path.abspath(path) == os.path.abspath(mod.LOCK_FILE):
            raise OSError('Erneuerung gesperrt')
        return writer(path, payload)
    app._lock_token['refreshed_at'] = old
    with patch.object(app, 'write_json_atomic', side_effect=fail_renew):
        assert app.save_items(show_error=False) is False
        assert lauf.datei() == before and app.dirty
        assert app._last_save_result.lock_verified is False
        assert app.create_list_from_template('fehlt') is None, 'direkter Caller ignoriert Erneuerungsfehler'
    assert app.save_items(show_error=False)

    stale = dict(app._lock_token)
    app.release_data_lock()
    successor = mod.ListApp.__new__(mod.ListApp)
    try:
        successor.acquire_data_lock()
        assert not successor._data_read_only
        current = lock.read_bytes()
        app._data_read_only = False
        assert app.save_items(show_error=False) is False, 'freigegebene Sitzung ohne Token schreibt erneut'
        assert lock.read_bytes() == current
        app._lock_token = stale; app._data_read_only = False
        assert app.check_data_lock(True) is False
        app.release_data_lock()
        assert lock.read_bytes() == current, 'alter Besitzer löscht/erneuert neue Sitzung'
    finally:
        successor.release_data_lock()
        app.acquire_data_lock()
    origin = Path(mod.BASE_DIR)
    target = Path(lauf.data).parent / 'ordnerwechsel'
    assert app.change_data_folder(str(target), move_existing=True)
    assert app.verify_data_lock() is True and app._lock_session.held
    assert gleicher_ort(app._lock_session.path, target / 'glide.lock'), (app._lock_session.path, str(target))
    assert not (origin / 'glide.lock').exists() and app.find_item_in_lists(ids['A'])
    assert app.change_data_folder(str(origin))
    assert app.verify_data_lock() is True
    assert gleicher_ort(app._lock_session.path, origin / 'glide.lock'), (app._lock_session.path, str(origin))
    assert not (target / 'glide.lock').exists()
    return 'Lebender Besitzer geschützt; Erneuerung/Freigabe strikt, alte Tokens wirkungslos; Kopieren/Ordnerwechsel/Rückwechsel mit neuem Erwerb'


def fall_speicherergebnis(lauf):
    app = lauf.app; ids = lauf.grundbestand()
    before = lauf.datei(); writer = app.write_json_atomic
    app.find_item(ids['A'])[0]['text'] = 'Offene Änderung'
    def fail_main(path, payload):
        if os.path.abspath(path) == os.path.abspath(lauf.mod.SAVE_FILE): raise OSError('Datei gesperrt')
        return writer(path, payload)
    with patch.object(app, 'write_json_atomic', side_effect=fail_main):
        assert app.save_items(show_error=False) is False
    result = app._last_save_result
    assert not result.data_written and result.lock_verified and result.error
    assert lauf.datei() == before and app.dirty
    with patch.object(app, 'write_backup_copy', return_value='Sicherung nicht erreichbar'):
        assert app.save_items(show_error=False) is True
        result = app._last_save_result
        assert result.data_written and result.backup_warning and result.history_updated
    with patch.object(app, 'update_sidebar_list', side_effect=RuntimeError('Anzeigeprobe')):
        assert app.save_items(show_error=False) is True
        assert app._last_save_result.data_written and app._last_save_result.followup_errors
    with patch.object(app, 'write_backup_copy', return_value='Sicherung voll'), \
            patch.object(app, 'show_warning', side_effect=lauf.mod.tk.TclError('Fenster geschlossen')):
        assert app.save_items() is True, 'Meldungsfehler verwirft bereits gespeicherte Daten'
        assert app._last_save_result.data_written and app._last_save_result.followup_errors
    assert not app.dirty
    depth = len(app.undo_stack)
    with app.item_change([ids['A']], local=True) as no_change:
        pass
    assert len(app.undo_stack) == depth and no_change.saved is None
    with app.item_change([ids['A']], local=True) as changed:
        app.find_item(ids['A'])[0]['importance'] = 2; changed.mark(ids['A'])
    assert changed.saved is True and changed.save_result.data_written
    assert changed.changed_ids == {ids['A']} and changed.changed_lists == {ids['liste']}
    assert changed.save_result.settings_pending is False
    save_settings = app.save_settings
    def failed_settings(**options):
        return save_settings(**options) if options.get('defer') else False
    with patch.object(app, 'save_settings', side_effect=failed_settings):
        with app.item_change([ids['A']], local=True) as partial:
            app.find_item(ids['A'])[0]['importance'] = 3; partial.mark(ids['A'])
            app.settings['glide_pruefwert'] = 'offene Einstellung'
            app.save_settings(defer=True)
        assert partial.saved is True and partial.save_result.data_written
        assert partial.save_result.settings_saved is False and partial.save_result.followup_errors
    with patch.object(app, 'save_items', return_value=False):
        with app.item_change([ids['A']], local=True) as failed:
            app.find_item(ids['A'])[0]['importance'] = 1; failed.mark()
        assert failed.saved is False and failed.save_result is None, 'veraltetes Speicherergebnis weitergegeben'
    return 'Hauptdatei/Backup/Folgefehler/aufgeschobene Einstellungen unterschieden; ein Mutationsvertrag, Bool kompatibel'


def fall_mehrfach(lauf):
    app = lauf.app
    tasks = [app.new_item('Aufgabe ' + str(i)) for i in range(1000)]
    source = app.new_list_object('Mehrfachauswahl', tasks)
    app.lists.append(source); assert app.save_items(); app.set_active_list(source['id']); lauf.idle()
    selected = [item['id'] for item in tasks[-100:]]
    app.tree.selection_set(selected)
    before = len(app.undo_stack)
    calls = 0; depth = 0; original = app.find_item
    def count(*args, **kwargs):
        nonlocal calls, depth
        if not depth: calls += 1
        depth += 1
        try: return original(*args, **kwargs)
        finally: depth -= 1
    with patch.object(app, 'find_item', side_effect=count):
        app.toggle_done()
    assert all(app.find_item(identity)[0]['done'] for identity in selected)
    assert len(app.undo_stack) == before + 1
    assert calls < 50, ('wiederholte rekursive Suche bei Mehrfachaktion', calls)
    app.undo_last_change(); lauf.idle()
    assert all(not app.find_item(identity)[0]['done'] for identity in selected)
    app.redo_last_change(); lauf.idle()
    assert all(app.find_item(identity)[0]['done'] for identity in selected)
    app.undo_last_change(); lauf.idle()
    # Die Bestätigung tauscht Objekte bei gleichen IDs aus. Der Mutationskörper
    # muss danach aktuelle Referenzen verwenden, nicht die vor dem Dialog.
    def replace_during_confirm(_items):
        app.items = copy.deepcopy(app.items)
        app.sync_current_list_reference()
        return True
    app.tree.selection_set(selected)
    with patch.object(app, 'confirm_complete_blocked', side_effect=replace_during_confirm):
        app.toggle_done()
    assert all(app.find_item(identity)[0]['done'] for identity in selected)
    # Wiederholungsfehler bleibt eine offene, rücknehmbare Mutation.
    app.tree.selection_set(selected)
    disk = lauf.datei()
    with patch.object(app, 'save_items', return_value=False):
        app.toggle_done()
    assert lauf.datei() == disk
    return f'100 von 1.000 Aufgaben: {calls} einzelne Suchstarts, ein Undo/Redo; neue Objekte nach Bestätigung aufgelöst'


def fall_struktur_ergebnis(lauf):
    """Echte Strukturaufrufer: kein Erfolgsfeedback bei Hauptdateifehlern."""
    app, mod = lauf.app, lauf.mod
    ids = lauf.grundbestand()
    app.tree.selection_set((ids['A'], ids['B']))
    volle_tiefe(app, app.MAX_UNDO_STEPS)
    vorher = lauf.datei()
    # Gruppieren erneuert vor der Änderung die Datensperre, höchstens einmal
    # pro Sekunde. Die pauschale Fehlerinjektion traf an einer Sekundengrenze
    # schon diese Sperrdatei (GitHub #156) und verhinderte die beabsichtigte
    # Mutation. Nur die Hauptdatei sperren; die Erneuerung immer erzwingen.
    writer = app.write_json_atomic
    writes = []
    def fail_main(path, payload):
        writes.append(path)
        if gleicher_ort(path, mod.SAVE_FILE):
            raise OSError('Hauptdatei gesperrt')
        return writer(path, payload)
    app._lock_token = dict(app._lock_token, refreshed_at='')
    with patch.object(app, 'write_json_atomic', side_effect=fail_main), \
            patch.object(app, 'show_undo_toast') as toast, patch.object(app, 'feedback') as feedback:
        app.group_selected_items()
    assert any(gleicher_ort(path, mod.LOCK_FILE) for path in writes), 'Sperrerneuerung nicht geprüft'
    assert any(gleicher_ort(path, mod.SAVE_FILE) for path in writes), 'Hauptdateifehler nicht erreicht'
    assert not toast.called and not feedback.called, 'Gruppieren meldet Erfolg trotz Schreibfehler'
    assert lauf.datei() == vorher and app.dirty, 'Hauptdatei muss erhalten und Mutation offen bleiben'
    assert len(app.undo_stack) == app.MAX_UNDO_STEPS
    group = next(item for item in app.items if app.is_group_item(item))
    assert {item['id'] for item in group['children']} == {ids['A'], ids['B']}
    assert app._last_save_result.data_written is False
    app.undo_last_change(); lauf.idle()
    assert app.find_item(ids['A']) and app.find_item(ids['B'])

    # Ein UI-Folgefehler nach dem Hauptdateischreiben ist kein Dateimisserfolg.
    app.tree.selection_set((ids['A'], ids['B']))
    with patch.object(app, 'update_sidebar_list', side_effect=RuntimeError('Anzeige')), \
            patch.object(app, 'show_undo_toast') as toast:
        app.group_selected_items()
    assert toast.called and app._last_save_result.data_written
    assert app._last_save_result.followup_errors
    group = next(item for item in app.items if app.is_group_item(item))
    group_id = group['id']
    assert group_id in lauf.datei_ids()
    app.tree.selection_set(group_id)
    depth = len(app.undo_stack)
    with patch.object(app, 'refresh_tree', side_effect=RuntimeError('Inhaltsansicht')), \
            patch.object(app, 'show_warning', side_effect=RuntimeError('Warnungsfenster')):
        app.dissolve_selected_group()
    lauf.idle()
    assert not app.find_item(group_id) and app.find_item(ids['A'])
    assert group_id not in lauf.datei_ids(), 'UI-Folgefehler rollt geschriebenen Bestand zurück'
    assert app._last_save_result.data_written and app._last_save_result.followup_errors
    assert any('Fehlermeldung:' in detail for detail in app._last_save_result.followup_errors)
    assert len(app.undo_stack) == min(depth + 1, app.MAX_UNDO_STEPS)
    app.undo_last_change(); lauf.idle()
    assert app.find_item(group_id)
    app.redo_last_change(); lauf.idle()
    assert not app.find_item(group_id)

    folder = app.new_folder_object('Rahmenordner')
    app.folders.append(folder)
    app.lists.append(app.new_list_object('Im Ordner', [app.new_item('Erhalten')], folder_id=folder['id']))
    assert app.save_items()
    color = next(key for key in app.LIST_COLOR_KEYS if key)
    snapshot = app.snapshot_undo
    def neue_farbreferenzen(*args, **kwargs):
        snapshot(*args, **kwargs)
        app.folders = copy.deepcopy(app.folders)
    with patch.object(app, 'snapshot_undo', side_effect=neue_farbreferenzen):
        app.set_folder_color(folder['id'], color)
    assert app.get_folder(folder['id'])['color'] == color
    assert app._last_save_result.data_written
    stable = list(app.undo_stack)
    app.set_folder_color(folder['id'], color)
    assert app.undo_stack == stable, 'Gleiche Farbe verbraucht Undo'
    app.trash_folder(folder['id']); lauf.idle()
    trash = next(entry for entry in app.trash if entry['kind'] == app.TRASH_KIND_FOLDER)
    disk = lauf.datei()
    # Dasselbe auch für den Restore-Aufrufer (früher GitHub #141, Windows).
    writes.clear()
    app._lock_token = dict(app._lock_token, refreshed_at='')
    with patch.object(app, 'write_json_atomic', side_effect=fail_main):
        assert app.restore_trash_entry(trash['id']) is False, 'Restore meldet ungespeicherten Erfolg'
    assert any(gleicher_ort(path, mod.LOCK_FILE) for path in writes), 'Restore ohne Sperrerneuerung'
    assert any(gleicher_ort(path, mod.SAVE_FILE) for path in writes), 'Restore ohne Hauptdateifehler'
    assert lauf.datei() == disk and app.dirty
    assert app.get_folder(folder['id']), 'Fehlgeschlagene Änderung bleibt offen und rücknehmbar'
    assert app._last_save_result.data_written is False
    app.undo_last_change(); lauf.idle()
    assert not app.get_folder(folder['id']) and app.get_trash_entry(trash['id'])
    assert app.restore_trash_entry(trash['id']) is True
    app.empty_trash(); lauf.idle()
    assert not app.trash
    app.empty_trash()
    app.set_folder_color('fehlt', 'red')
    assert len(app.undo_stack) <= app.MAX_UNDO_STEPS
    lauf.neustart()
    assert app is not lauf.app and lauf.app.get_folder(folder['id'])
    assert lauf.app.find_item_in_lists(ids['A'])
    return 'Gruppieren/Auflösen, Farbe, Ordnerpapierkorb, Restore/Leeren: ehrliche Ergebnisse, ein Undo/Redo, No-op, voller Stapel und Neustart'


def fall_struktur_dialog(lauf):
    """Objekte und Reihenfolge dürfen sich während eines modalen Dialogs ändern."""
    app = lauf.app
    ids = lauf.grundbestand()
    app.tree.selection_set((ids['A'], ids['B']))

    def austausch(*_args, **_kwargs):
        app.items = copy.deepcopy(app.items)
        app.items.insert(0, app.items.pop())
        app.sync_current_list_reference()
        return 'Frische Gruppe'

    with patch.object(app, 'themed_input_dialog', side_effect=austausch):
        app.group_selected_items()
    group = next((item for item in app.items if item.get('text') == 'Frische Gruppe'), None)
    assert group and app.items.index(group) == 1, 'Gruppieren hält alte Geschwister/Position über den Dialog'
    assert [item['id'] for item in group['children']] == [ids['A'], ids['B']]
    app.undo_last_change(); lauf.idle()
    assert [item['text'] for item in app.items[:3]] == ['H', 'A', 'B']
    app.tree.selection_set((ids['A'], ids['B']))

    def andere_ebene(*_args, **_kwargs):
        first = app.find_item(ids['A'])[0]
        second = app.remove_item_by_id(ids['B'])
        first['children'].append(second)
        return 'Veraltet'

    depth = len(app.undo_stack)
    with patch.object(app, 'themed_input_dialog', side_effect=andere_ebene):
        app.group_selected_items()
    assert not any(item.get('text') == 'Veraltet' for item in app.items)
    assert len(app.undo_stack) == depth, 'Veränderte Ebene darf keinen Undo-Schritt verbrauchen'
    folder = app.new_folder_object('Alt')
    app.folders.append(folder)
    assert app.save_items()

    def neuer_ordner(*_args, **_kwargs):
        app.folders = copy.deepcopy(app.folders)
        app.get_folder(folder['id'])['title'] = 'Frischer Titel'
        return True

    with patch.object(app, 'ask_yes_no', side_effect=neuer_ordner):
        app.delete_folder(folder['id'])
    trashed = next(entry['folder'] for entry in app.trash if entry['kind'] == app.TRASH_KIND_FOLDER)
    assert trashed['title'] == 'Frischer Titel', 'Ordnerauflösen archiviert veraltetes Dialogobjekt'
    # Ein voller Papierkorb verdrängt regulär den ältesten Eintrag. Der neue
    # Strukturwächter darf deshalb keine gültige Ordnerauflösung zurücknehmen.
    app.trash = [app.new_trash_entry(app.TRASH_KIND_ITEM, app.new_item('Alte Ablage ' + str(i)))
                 for i in range(app.MAX_TRASH_ENTRIES)]
    oldest = app.trash[-1]['item']['id']
    full_folder = app.new_folder_object('Bei vollem Papierkorb')
    app.folders.append(full_folder)
    child_list = app.new_list_object('Bleibt', [app.new_item('Bleibt auch')], folder_id=full_folder['id'])
    app.lists.append(child_list)
    assert app.save_items()
    with patch.object(app, 'refresh_tree', side_effect=RuntimeError('Inhaltsansicht')):
        app.delete_folder(full_folder['id'])
    assert not app.get_folder(full_folder['id']), 'Voller Papierkorb verhindert reguläre Ordnerauflösung'
    assert child_list['folder_id'] is None and child_list['items'][0]['id'] in lauf.datei_ids()
    assert len(app.trash) == app.MAX_TRASH_ENTRIES and oldest not in app.data_item_ids()
    app.undo_last_change(); lauf.idle()
    assert app.get_folder(full_folder['id']) and oldest in app.data_item_ids()
    return 'Gruppieren löst IDs/Geschwister/Position nach Dialog neu auf; geänderte Ebene bricht ohne Undo ab; Ordner verwendet frisches Objekt'


def fall_struktur_editor(lauf):
    """Ordnerpapierkorb übernimmt Seitentext, bevor der Container verschwindet."""
    app, mod = lauf.app, lauf.mod
    lauf.grundbestand()
    folder = app.new_folder_object('Offene Seite')
    app.folders.append(folder)
    page = app.new_page_from_markdown('# Prüfseite\n\nAusgangstext', folder_id=folder['id'])
    lauf.idle()
    editor = app.rich_note_editor
    limit = mod.RichNoteEditor.MAX_TEXT
    disk = lauf.datei()
    undo = list(app.undo_stack)
    try:
        mod.RichNoteEditor.MAX_TEXT = len(editor.text.get('1.0', 'end-1c')) + 3
        editor.text.insert('end', '\nNicht übernommener Nachtrag')
        app.trash_folder(folder['id'])
        assert app.get_folder(folder['id']), 'Ordner entfernt, bevor offener Text übernommen ist'
        assert app.active_list_id == page['id'] and app.rich_note_editor is editor
        assert lauf.datei() == disk and app.undo_stack == undo
        assert 'Nicht übernommener Nachtrag' in editor.text.get('1.0', 'end-1c')
    finally:
        mod.RichNoteEditor.MAX_TEXT = limit
    app.trash_folder(folder['id']); lauf.idle()
    assert not app.get_folder(folder['id'])
    trashed = next(entry['list'] for entry in app.trash if entry['kind'] == app.TRASH_KIND_LIST
                   and entry['list']['id'] == page['id'])
    assert 'Nicht übernommener Nachtrag' in json.dumps(trashed, ensure_ascii=False)
    app.undo_last_change(); lauf.idle()
    assert app.get_folder(folder['id'])
    assert 'Nicht übernommener Nachtrag' in app.page_markdown(page['id'])
    readonly = copy.deepcopy(app.folders)
    with patch.object(app, 'refresh_data_lock', return_value=False):
        app.trash_folder(folder['id'])
        app.delete_folder(folder['id'])
        app.set_folder_color(folder['id'], 'red')
    assert app.folders == readonly
    return 'Nicht übernommener Text hält Ordnerpapierkorb an; erfolgreicher Flush bewahrt Text im Papierkorb und Undo; Sperrfehler verhindert Mutation'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    parser.add_argument("--fall", choices=FAELLE + ("alle",), default="alle")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    args.app = args.app.resolve()
    import hashlib
    ergebnis = {"app": "app.pyw", "app_sha256": hashlib.sha256(args.app.read_bytes()).hexdigest(),
                "faelle": {}, "fehler": []}
    for name in (FAELLE if args.fall == "alle" else (args.fall,)):
        with tempfile.TemporaryDirectory(prefix=f"glide-schutz-{name}-") as daten:
            lauf = None
            try:
                lauf = Lauf(args.app, str(Path(daten) / "daten"))
                text = globals()["fall_" + name](lauf)
                if lauf.errors:
                    raise AssertionError(("Rückruffehler", lauf.errors[:2]))
                ergebnis["faelle"][name] = {"ok": True, "befund": text}
                print(f"OK {name}: {text}", flush=True)
            except Exception as fehler:  # Bericht je Fall, Gesamtergebnis unten
                # Eine nackte Assertion meldet sonst nur „AssertionError()“; im
                # CI-Protokoll wäre die Stelle ohne Zeilennummer nicht auffindbar.
                eigene = [f for f in traceback.extract_tb(fehler.__traceback__)
                          if Path(f.filename).resolve() == Path(__file__).resolve()]
                ort = f" (Zeile {eigene[-1].lineno})" if eigene else ""
                detail = repr(fehler).replace(str(Path.home()).replace("\\", "\\\\"), "~")
                detail = detail.replace(str(Path.home()), "~")
                ergebnis["faelle"][name] = {"ok": False, "befund": (ort.strip(" ()") + ": " if ort else "") + detail[:600]}
                ergebnis["fehler"].append(name)
                print(f"ROT {name}{ort}: {detail}"[:700], flush=True)
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
