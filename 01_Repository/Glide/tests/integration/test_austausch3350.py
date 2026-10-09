"""Paket Austausch (3.35.0): G24 KI-Austausch Stufe 2 und F-03 Sicherungen vergleichen.

G24: „Für KI bereitstellen …“ schreibt mit Zweck „überarbeiten“ ein Kontextpaket der
ausgewählten Punkte (Verweise statt Kennungen, Ausgangsstand je Aufgabe). Ein
Änderungsvorschlag kommt über „KI-Ergebnis importieren …“ in eine eigene Prüfung:
jede Änderung Feld für Feld, Konflikte, Unbekanntes und Ungültiges benannt; übernommen
wird nur Anwendbares, nach einer Vorsicherung und als ein Rückgängig-Schritt.
F-03: Datei › Sicherung › „Sicherungen vergleichen …“ legt eine automatische
Sicherung neben den aktuellen Bestand und eine Sicherungsdatei neben sich selbst;
nichts wird geschrieben.

--app wählt den Quellstand; mit der unveränderten 3.34.0 muss die Suite rot sein
(Gegenprobe). Künstliche Daten in einem temporären GLIDE_DATA_DIR.
"""
import argparse
import copy
from datetime import date, timedelta
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def knopf(dialog, beschriftung):
    knoepfe = [w for w in descendants(dialog) if isinstance(getattr(w, "text", None), str)]
    treffer = [w for w in knoepfe if w.text == beschriftung]
    assert treffer, (beschriftung, [w.text for w in knoepfe])
    return treffer[0]


def dateistand(ordner):
    """{Pfad: (Größe, Änderungszeit)} aller Dateien – zum Nachweis, dass nichts geschrieben wurde."""
    stand = {}
    for wurzel, _ordner, dateien in os.walk(ordner):
        for name in dateien:
            pfad = os.path.join(wurzel, name)
            info = os.stat(pfad)
            stand[pfad] = (info.st_size, info.st_mtime_ns)
    return stand


with tempfile.TemporaryDirectory(prefix="glide-austausch-") as ordner:
    daten = os.path.join(ordner, "daten")
    os.makedirs(daten)
    os.environ["GLIDE_DATA_DIR"] = daten
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_austausch_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    fehler, toasts, infos = [], [], []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: infos.append(a)
    original_toast = app.show_undo_toast
    app.show_undo_toast = lambda text, restore=None: (toasts.append(text), original_toast(text, restore))[1]
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()
            time.sleep(0.01)

    def tag(n):
        return (date.today() + timedelta(days=n)).isoformat()

    def aktuell(item):
        return app.find_item_in_lists(item["id"])[0]

    try:
        kunde = app.ensure_label_by_name("Kunde")
        a = app.new_item("Angebot schreiben", importance=1, due=tag(3))
        b = app.new_item("Rechnung prüfen", description="Beträge abgleichen")
        b["labels"] = [kunde["id"]]
        c = app.new_item("Pflanzen gießen", due=tag(0), repeat={"art": "tage", "abstand": 3})
        e = app.new_item("Termin vorbereiten", planned_date=tag(1))
        liste = app.new_list_object("Projekt", [a, b, c, e])
        anders = app.new_list_object("Anderes", [app.new_item("Nicht im Paket")])
        app.lists.extend([liste, anders])
        app.save_items()
        app.set_active_list(liste["id"])
        ruhe(0.3)

        # --- G24 (1): Kontextpaket der Auswahl über den echten Dialog -------------
        app.tree.selection_set([a["id"], b["id"], c["id"], e["id"]])
        app.tree.focus(e["id"])
        ruhe()
        gefunden = {}
        paketdatei = os.path.join(ordner, "kontext.glidecontext")
        mod.filedialog.asksaveasfilename = lambda **k: paketdatei

        def exportieren(dialog, *x, **k):
            for _ in range(5):
                dialog.update()
            menues = [w for w in descendants(dialog) if isinstance(w, mod.AppOptionMenu)]
            zweck = next(m for m in menues if any("Kontextpaket" in o for o in m.options))
            umfang = next(m for m in menues if any(o.startswith("Ausgewählte Punkte") for o in m.options))
            zweck.variable.set(next(o for o in zweck.options if "Kontextpaket" in o))
            umfang.variable.set("Ausgewählte Punkte (4)")
            dialog.update()
            gefunden["export"] = [(type(w).__name__, getattr(w, "text", None)) for w in descendants(dialog)
                                  if isinstance(w, mod.RoundedButton)]
            knopf(dialog, "Speichern").command()

        app.run_modal = exportieren
        app.show_exchange_export_dialog()
        ruhe()
        paket = json.loads(Path(paketdatei).read_text(encoding="utf-8"))
        assert paket["format"] == "glide.context" and paket["format_version"] == 2
        assert [eintrag["fields"]["title"] for eintrag in paket["items"]] == [
            "Angebot schreiben", "Rechnung prüfen", "Pflanzen gießen", "Termin vorbereiten"]
        roh = Path(paketdatei).read_text(encoding="utf-8")
        assert not any(item["id"] in roh for item in (a, b, c, e)) and liste["id"] not in roh
        assert paket["items"][1]["fields"]["labels"] == ["Kunde"]
        assert "Nicht im Paket" not in roh
        assert "Aufgabe(n) mit Ausgangsstand" in infos[-1][1]
        pruefungen.append("G24: Kontextpaket der Auswahl über „Für KI bereitstellen …“ – vier Aufgaben mit "
                          "Ausgangsstand, Verweise statt Kennungen, Labels mit Namen")

        # Zwischenzeitlich ändert jemand „Termin vorbereiten“ → Konflikt.
        with app.item_change([e["id"]]) as change:
            aktuell(e)["description"] = "inzwischen geändert"
            change.mark()
        ruhe()
        verweis = {eintrag["fields"]["title"]: eintrag for eintrag in paket["items"]}
        vorschlag = {"format": "glide.exchange", "format_version": 2, "mode": "patch", "changes": [
            {"ref": verweis["Angebot schreiben"]["ref"], "base": verweis["Angebot schreiben"]["base"],
             "set": {"importance": 3, "due": tag(5), "title": "Angebot  schreiben und senden"}},
            {"ref": verweis["Rechnung prüfen"]["ref"], "base": verweis["Rechnung prüfen"]["base"],
             "set": {"labels": ["Kunde", "Finanzen"], "estimated_minutes": 45}},
            {"ref": verweis["Pflanzen gießen"]["ref"], "base": verweis["Pflanzen gießen"]["base"],
             "set": {"done": True}},
            {"ref": verweis["Termin vorbereiten"]["ref"], "base": verweis["Termin vorbereiten"]["base"],
             "set": {"planned_date": None}},
            {"ref": "r-0000000000000000", "base": "x", "set": {"title": "Erfunden"}},
        ]}
        vorschlagsdatei = os.path.join(ordner, "vorschlag.json")
        Path(vorschlagsdatei).write_text(json.dumps(vorschlag, ensure_ascii=False), encoding="utf-8")
        vorher = copy.deepcopy(app.lists)
        tiefe = len(app.undo_stack)
        gelesen = {}

        def pruefen(antwort):
            def run_modal(dialog, *x, **k):
                for _ in range(5):
                    dialog.update()
                text = next(w for w in descendants(dialog) if isinstance(w, mod.tk.Text))
                gelesen["text"] = text.get("1.0", "end")
                gelesen["labels"] = [w.cget("text") for w in descendants(dialog) if isinstance(w, mod.tk.Label)]
                gelesen["knoepfe"] = [w.text for w in descendants(dialog) if isinstance(w, mod.RoundedButton)]
                knopf(dialog, antwort).command()
            return run_modal

        # Erst ansehen und abbrechen: nichts ändert sich.
        app.run_modal = pruefen("Abbrechen")
        app.show_exchange_import_dialog(path=vorschlagsdatei)
        ruhe()
        assert app.lists == vorher and len(app.undo_stack) == tiefe
        text = gelesen["text"]
        assert "✓  Angebot schreiben" in text and "Wichtigkeit: 1 → 3" in text, text
        assert "Titel: Angebot schreiben → Angebot schreiben und senden" in text, text
        assert "Labels: Kunde → Finanzen, Kunde" in text and "Aufwand: – → 45" in text, text
        assert "✗  Pflanzen gießen" in text and "Wiederkehrende Aufgabe" in text, text
        assert "⚠  Termin vorbereiten" in text and "seit dem Kontextpaket geändert" in text, text
        assert "?  Unbekannte Aufgabe" in text and "nicht gefunden" in text, text
        assert "2 anwendbar · 1 Konflikte · 1 nicht gefunden · 1 ungültig" in gelesen["labels"], gelesen["labels"]
        assert "2 übernehmen" in gelesen["knoepfe"], gelesen["knoepfe"]

        app.run_modal = pruefen("2 übernehmen")
        app.show_exchange_import_dialog(path=vorschlagsdatei)
        ruhe(0.3)
        assert aktuell(a)["importance"] == 3 and aktuell(a)["due"] == tag(5)
        assert aktuell(a)["text"] == "Angebot schreiben und senden"
        finanzen = next(label for label in app.labels if label.get("name") == "Finanzen")
        assert set(aktuell(b)["labels"]) == {kunde["id"], finanzen["id"]} and aktuell(b)["estimated_minutes"] == 45
        assert not aktuell(c).get("done") and aktuell(e)["planned_date"] == tag(1)
        assert aktuell(a)["id"] == a["id"] and len(app.undo_stack) == tiefe + 1
        assert toasts[-1] == "2 Aufgabe(n) nach Vorschlag geändert", toasts[-1]
        sicherungen = [name for name in os.listdir(mod.BACKUP_DIR) if name.startswith("vor_vorschlag_")]
        assert len(sicherungen) == 1 and sicherungen[0].endswith(".glidebackup"), sicherungen
        app.undo_last_change()
        ruhe(0.2)
        assert aktuell(a)["importance"] == 1 and aktuell(a)["text"] == "Angebot schreiben"
        assert aktuell(b)["labels"] == [kunde["id"]] and not aktuell(b).get("estimated_minutes")
        pruefungen.append("G24: Änderungsvorschlag über „KI-Ergebnis importieren …“ – Feldvergleich, Konflikt, "
                          "Wiederholung und Unbekanntes benannt, Abbrechen ändert nichts, Übernahme nur des "
                          "Anwendbaren nach Vorsicherung, ein Rückgängig-Schritt")

        # Version 1 kennt keinen Änderungsvorschlag: verständlich abgewiesen.
        alt = dict(vorschlag, format_version=1)
        Path(vorschlagsdatei).write_text(json.dumps(alt), encoding="utf-8")
        anzahl = len(fehler)
        app.show_exchange_import_dialog(path=vorschlagsdatei)
        assert len(fehler) == anzahl + 1 and "format_version 2" in fehler[-1], fehler[-1:]
        fehler.pop()
        beschreibung = app.exchange_prompt_text()
        assert '"mode": "patch"' in beschreibung and app.exchange_capabilities()["patch_mode"] == 1
        pruefungen.append("G24: Version 1 mit „patch“ abgewiesen; Formatbeschreibung nennt den Vorschlag")

        # --- F-03: Sicherungen vergleichen ------------------------------------------
        # Nach dem Rückgängig sind die Listen neue Objekte.
        liste = next(entry for entry in app.lists if entry["id"] == liste["id"])
        anders = next(entry for entry in app.lists if entry["id"] == anders["id"])
        app.save_items()
        for name in os.listdir(mod.BACKUP_DIR):
            if name.startswith("liste_backup_"):
                os.remove(os.path.join(mod.BACKUP_DIR, name))
        stempel = time.strftime("%Y%m%d_%H%M%S")
        automatisch = os.path.join(mod.BACKUP_DIR, f"liste_backup_{stempel}.json")
        Path(automatisch).write_bytes(Path(mod.SAVE_FILE).read_bytes())
        with app.item_change([a["id"], b["id"]]) as change:
            aktuell(a)["text"] = "Angebot verschickt"
            aktuell(a)["done"] = True
            change.mark()
        neu = app.new_item("Neu nach der Sicherung")
        liste["items"].append(neu)
        weg = next(i for i in liste["items"] if i["id"] == c["id"])
        liste["items"].remove(weg)
        verschoben = next(i for i in liste["items"] if i["id"] == e["id"])
        liste["items"].remove(verschoben)
        anders["items"].append(verschoben)
        app.save_items()
        ruhe()
        datei = os.path.join(ordner, "stand.glidebackup")
        app.write_complete_backup(datei, app.complete_backup_payload())
        aktion = next(eintrag for eintrag in app.app_action_entries() if eintrag["id"] == "show_backup_compare_dialog")
        assert aktion["path"].endswith("Sicherung"), aktion["path"]
        stand = dateistand(ordner)
        bestand = copy.deepcopy(app.lists)
        ergebnisse = []
        mod.filedialog.askopenfilename = lambda **k: datei

        def vergleichen(dialog, *x, **k):
            for _ in range(8):
                dialog.update()
            ergebnisse.append((copy.deepcopy(dialog._glide_compare),
                               next(w for w in descendants(dialog) if isinstance(w, mod.tk.Text)).get("1.0", "end"),
                               [w.cget("text") for w in descendants(dialog) if isinstance(w, mod.tk.Label)]))
            # Zweiter Vergleich: die gewählte Datei gegen sich selbst.
            for wahl in [w for w in descendants(dialog) if getattr(w, "text", None) == "Datei"]:
                wahl.command()
            knopf(dialog, "Vergleichen").command()
            dialog.update()
            ergebnisse.append((copy.deepcopy(dialog._glide_compare), "",
                               [w.cget("text") for w in descendants(dialog) if isinstance(w, mod.tk.Label)]))
            knopf(dialog, "Schließen").command()

        app.run_modal = vergleichen
        app.invoke_app_action(aktion)
        ruhe(0.3)
        ergebnis, text, beschriftungen = ergebnisse[0]
        assert [eintrag[0] for eintrag in ergebnis["items_added"]] == [neu["id"]]
        assert [eintrag[0] for eintrag in ergebnis["items_removed"]] == [c["id"]]
        assert [(eintrag[0], eintrag[2], eintrag[3]) for eintrag in ergebnis["items_moved"]] == [
            (e["id"], "Projekt", "Anderes")]
        geaendert = {eintrag[0]: eintrag[3] for eintrag in ergebnis["items_changed"]}
        assert ("Titel", "Angebot schreiben", "Angebot verschickt") in geaendert[a["id"]], geaendert
        assert ("Erledigt", "nein", "ja") in geaendert[a["id"]], geaendert
        assert "1 Aufgaben neu · 1 Aufgaben entfernt · 1 Aufgaben verschoben · 1 Aufgaben geändert" in beschriftungen
        assert "Aufgaben verschoben (1)" in text and "Projekt → Anderes" in text, text
        zweites = ergebnisse[1]
        assert "Keine Unterschiede bei Listen und Aufgaben" in zweites[2], zweites[2]
        assert dateistand(ordner) == stand and app.lists == bestand, "Vergleichen darf nichts schreiben"
        pruefungen.append("F-03: „Sicherungen vergleichen …“ – automatische Sicherung gegen den Bestand "
                          "(neu, entfernt, verschoben, geändert mit Feldern), Sicherungsdatei gegen sich selbst "
                          "ohne Unterschied; keine Datei geschrieben")

        ruhe(0.2)
        assert not fehler, fehler
        print("test_austausch3350: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
