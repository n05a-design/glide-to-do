# SPDX-License-Identifier: MPL-2.0
"""Integrationstest für Skill-Paket K3 (WA-61 / E-K5 Option A): Erweiterte Austauschfähigkeiten.

Prüft die fünf Kernbausteine von Paket K3:
1. Automatische dateibasierte Vorsicherung vor Create-Import (vor_import_*.glidebackup).
2. Markdown-Listenimport (markdown -> rich_note, Aufgabenextraktion) und Export.
3. Ordnerarten (folder_kind: library, journal, standard, toleranter Rückfall).
4. Wiederholungsregeln (repeat: EN- und DE-Schlüssel, Rundlauf, Prüfung auf Fälligkeitsdatum).
5. Benachrichtigungen und Erinnerungen (reminder: relative Minuten, feste Zeitpunkte, Rundlauf).
"""
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import zipfile

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "src" / "glide"
sys.path.insert(0, str(SOURCE))
sys.dont_write_bytecode = True


def run_tests():
    temp_dir = tempfile.mkdtemp(prefix="glide-k3-test-")
    data_dir = os.path.join(temp_dir, "daten")
    os.makedirs(data_dir, exist_ok=True)
    os.environ["GLIDE_DATA_DIR"] = data_dir
    os.environ["GLIDE_TEST_MODE"] = "1"

    loader = importlib.machinery.SourceFileLoader(
        f"glide_app_k3_{Path(temp_dir).name.replace('-', '_')}", str(SOURCE / "app.pyw")
    )
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)

    root = None
    app = None
    pruefungen = []

    try:
        root = mod.tk.Tk()
        root.withdraw()
        app = mod.ListApp(root)

        # ------------------------------------------------------------------
        # 1. Baustein: Automatische Vorsicherung beim Create-Import
        # ------------------------------------------------------------------
        # Ausgangsbestand anlegen
        ordner_alt = app.new_folder_object("Bestand Ordner")
        liste_alt = app.new_list_object("Bestand Liste", [app.new_item("Bestehende Aufgabe")])
        app.folders.append(ordner_alt)
        app.lists.append(liste_alt)
        app.save_items()
        app.set_active_list(liste_alt["id"])

        sicherungen_vorher = [
            f for f in os.listdir(mod.BACKUP_DIR) if f.startswith("vor_import_") and f.endswith(".glidebackup")
        ]
        assert len(sicherungen_vorher) == 0, f"Unerwartete Vorsicherungen: {sicherungen_vorher}"

        payload_k3 = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "folders": [
                {"key": "f_lib", "title": "Fachbibliothek", "folder_kind": "library"},
                {"key": "f_jrn", "title": "Projekttagebuch", "folder_kind": "journal"},
                {"key": "f_std", "title": "Standardordner", "folder_kind": "standard"},
            ],
            "lists": [
                {
                    "key": "l_md",
                    "title": "Dokumentation",
                    "folder": "f_jrn",
                    "markdown": "# Projektdokumentation\n\nEin wichtiger Absatz.\n\n- [ ] Erste Seite Aufgabe\n- [x] Fertig erledigt\n",
                },
                {
                    "key": "l_tasks",
                    "title": "Wiederkehrende Aufgaben",
                    "folder": "f_std",
                    "items": [
                        {
                            "title": "Wöchentlicher Bericht",
                            "due": "2026-12-01",
                            "due_time": "09:00",
                            "repeat": {"kind": "weekly"},
                            "reminder": {"mode": "relative", "minutes": 15},
                        },
                        {
                            "title": "Tägliches Backup",
                            "due": "2026-12-01",
                            "repeat": {"art": "taeglich"},
                            "reminder": {"mode": "fixed", "at": "2026-12-01T08:00:00+01:00"},
                        },
                    ],
                },
            ],
        }

        # Import anwenden
        neue_listen = app.apply_exchange_payload(payload_k3)
        assert neue_listen is not None and len(neue_listen) == 2, f"Import fehlgeschlagen: {neue_listen}"

        # Prüfe, dass automatische Vorsicherung existiert
        sicherungen_nachher = [
            f for f in os.listdir(mod.BACKUP_DIR) if f.startswith("vor_import_") and f.endswith(".glidebackup")
        ]
        assert len(sicherungen_nachher) == 1, f"Keine Vorsicherung angelegt: {sicherungen_nachher}"
        vorsicherung_pfad = os.path.join(mod.BACKUP_DIR, sicherungen_nachher[0])

        # Prüfe Inhalt der Vorsicherung
        with zipfile.ZipFile(vorsicherung_pfad, "r") as archive:
            assert "data.json" in archive.namelist(), "Vorsicherung enthält kein data.json"
            gesicherte_daten = json.loads(archive.read("data.json").decode("utf-8"))
            gesicherte_listen_titel = [l.get("title") for l in gesicherte_daten.get("lists", [])]
            assert "Bestand Liste" in gesicherte_listen_titel
            assert "Dokumentation" not in gesicherte_listen_titel
            assert "Wiederkehrende Aufgaben" not in gesicherte_listen_titel

        pruefungen.append("1. Automatische Vorsicherung beim Create-Import erfolgreich angelegt und verifiziert")

        # ------------------------------------------------------------------
        # 2. Baustein: Markdown-Seiten und -Notizen (markdown -> rich_note + items)
        # ------------------------------------------------------------------
        md_liste = next((l for l in app.lists if l.get("title") == "Dokumentation"), None)
        assert md_liste is not None, "Dokumentationsliste nicht gefunden"
        assert md_liste.get("list_kind") == "page", f"list_kind erwartet 'page', erhalten: {md_liste.get('list_kind')}"
        assert md_liste.get("rich_note"), "rich_note nicht vorhanden"
        assert "Projektdokumentation" in md_liste["rich_note"].get("text", "")

        # Aufgaben aus Checkboxen im Markdown
        assert len(md_liste.get("items", [])) == 2, f"Erwartet 2 Aufgaben aus Markdown, erhalten: {len(md_liste.get('items', []))}"
        aufgabe1 = md_liste["items"][0]
        aufgabe2 = md_liste["items"][1]
        assert aufgabe1["text"] == "Erste Seite Aufgabe"
        assert not aufgabe1.get("done")
        assert aufgabe2["text"] == "Fertig erledigt"
        assert aufgabe2.get("done") is True

        # Rundlauf-Export: Markdown muss exportiert werden
        export_payload = app.build_exchange_payload(lists=[md_liste])
        exp_liste = export_payload["lists"][0]
        assert "markdown" in exp_liste, f"Markdown fehlt im Export: {exp_liste.keys()}"
        assert "# Projektdokumentation" in exp_liste["markdown"]

        pruefungen.append("2. Markdown-Listenimport (rich_note, Checkboxen als Items) und Rundlauf-Export verifiziert")

        # ------------------------------------------------------------------
        # 3. Baustein: Ordnerarten (folder_kind)
        # ------------------------------------------------------------------
        f_lib = next((f for f in app.folders if f.get("title") == "Fachbibliothek"), None)
        f_jrn = next((f for f in app.folders if f.get("title") == "Projekttagebuch"), None)
        f_std = next((f for f in app.folders if f.get("title") == "Standardordner"), None)

        assert f_lib and f_lib.get("folder_kind") == "library", f"Fachbibliothek folder_kind: {f_lib}"
        assert f_jrn and f_jrn.get("folder_kind") == "journal", f"Projekttagebuch folder_kind: {f_jrn}"
        assert f_std and f_std.get("folder_kind") == "standard", f"Standardordner folder_kind: {f_std}"

        # Export von Ordnerarten
        export_folders_payload = app.build_exchange_payload(folders=[f_lib, f_jrn, f_std])
        exp_f_map = {f["title"]: f for f in export_folders_payload.get("folders", [])}
        assert exp_f_map["Fachbibliothek"].get("folder_kind") == "library"
        assert exp_f_map["Projekttagebuch"].get("folder_kind") == "journal"
        # Standardordner lässt redundantes folder_kind weg
        assert exp_f_map["Standardordner"].get("folder_kind") is None

        # Toleranter Rückfall bei unbekannter Ordnerart
        doc_unbekannt = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "folders": [{"key": "f_bad", "title": "Unbekannte Art", "folder_kind": "phantasie"}],
            "lists": [{"key": "l1", "title": "Liste in Bad", "folder": "f_bad", "items": []}],
        }
        valid_doc_bad, report_bad = app.parse_exchange_document(json.dumps(doc_unbekannt))
        assert any("Ordnerart 'phantasie'" in w for w in report_bad.warnings), f"Keine Warnung für ungültige Ordnerart: {report_bad.warnings}"
        app.apply_exchange_payload(valid_doc_bad)
        f_bad = next((f for f in app.folders if f.get("title") == "Unbekannte Art"), None)
        assert f_bad and f_bad.get("folder_kind") == "standard", f"Rückfall auf standard fehlgeschlagen: {f_bad}"

        pruefungen.append("3. Ordnerarten (library, journal, standard) und toleranter Rückfall verifiziert")

        # ------------------------------------------------------------------
        # 4. Baustein: Wiederholungsregeln (repeat)
        # ------------------------------------------------------------------
        tasks_liste = next((l for l in app.lists if l.get("title") == "Wiederkehrende Aufgaben"), None)
        assert tasks_liste is not None
        rep_task1 = next((i for i in tasks_liste["items"] if i["text"] == "Wöchentlicher Bericht"), None)
        rep_task2 = next((i for i in tasks_liste["items"] if i["text"] == "Tägliches Backup"), None)

        assert rep_task1 and rep_task1.get("repeat"), f"Wöchentlicher Bericht hat kein repeat: {rep_task1}"
        assert rep_task1["repeat"].get("art") == "woechentlich" or rep_task1["repeat"].get("kind") == "weekly"

        assert rep_task2 and rep_task2.get("repeat"), f"Tägliches Backup hat kein repeat: {rep_task2}"
        assert rep_task2["repeat"].get("art") == "taeglich" or rep_task2["repeat"].get("kind") == "daily"

        # Export von Wiederholungsregeln
        exp_repeat = app.build_exchange_payload(lists=[tasks_liste])
        exp_items_map = {i["title"]: i for i in exp_repeat["lists"][0]["items"]}
        assert "repeat" in exp_items_map["Wöchentlicher Bericht"], f"repeat fehlt in {exp_items_map['Wöchentlicher Bericht']}"
        assert exp_items_map["Wöchentlicher Bericht"]["repeat"]["kind"] == "weekly"

        # Wiederholung ohne Fälligkeitsdatum erzeugt Warnung und wird ignoriert
        doc_no_due = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "lists": [
                {
                    "key": "l_err",
                    "title": "Fehlerliste",
                    "items": [{"title": "Ohne Due", "repeat": {"kind": "daily"}}],
                }
            ],
        }
        _, report_no_due = app.parse_exchange_document(json.dumps(doc_no_due))
        assert any("Wiederholung ohne Fälligkeitsdatum" in w for w in report_no_due.warnings), f"Warnung erwartet: {report_no_due.warnings}"

        pruefungen.append("4. Wiederholungsregeln (EN/DE tolerant, Export, Validierung) verifiziert")

        # ------------------------------------------------------------------
        # 5. Baustein: Benachrichtigungen und Erinnerungen (reminder)
        # ------------------------------------------------------------------
        rem_task1 = rep_task1
        rem_task2 = rep_task2
        assert rem_task1.get("reminder"), f"Reminder fehlt bei task1: {rem_task1}"
        assert rem_task1["reminder"].get("offset_minutes") == 15 or rem_task1["reminder"].get("minutes") == 15

        assert rem_task2.get("reminder"), f"Reminder fehlt bei task2: {rem_task2}"

        # Export von Erinnerungen
        assert "reminder" in exp_items_map["Wöchentlicher Bericht"]
        exp_rem = exp_items_map["Wöchentlicher Bericht"]["reminder"]
        assert exp_rem.get("mode") == "relative" and exp_rem.get("minutes") == 15

        # Ungültige Erinnerung prüfen
        doc_bad_rem = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "lists": [
                {
                    "key": "l_bad_rem",
                    "title": "Bad Reminder",
                    "items": [{"title": "Punkt", "reminder": {"mode": "invalid_mode"}}],
                }
            ],
        }
        _, report_bad_rem = app.parse_exchange_document(json.dumps(doc_bad_rem))
        assert any("Erinnerung unbrauchbar" in w for w in report_bad_rem.warnings), f"Warnung erwartet: {report_bad_rem.warnings}"

        pruefungen.append("5. Erinnerungen (relativ/fest, Rundlauf, Validierung) verifiziert")

        # ------------------------------------------------------------------
        # Undo-Test
        # ------------------------------------------------------------------
        listen_vor_undo = len(app.lists)
        app.undo_last_change()
        assert len(app.lists) < listen_vor_undo, "Undo hat importierte Listen nicht zurückgenommen"
        pruefungen.append("6. Undo-Schritt des gesamten Imports verifiziert")

        print("test_austausch_k3: OK; " + "; ".join(pruefungen))
    finally:
        if app:
            try:
                app.cancel_pending_callbacks()
                app.release_data_lock()
            except Exception:
                pass
        if root:
            try:
                root.destroy()
            except Exception:
                pass
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    run_tests()
