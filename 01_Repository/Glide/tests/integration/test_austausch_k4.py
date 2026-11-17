# SPDX-License-Identifier: MPL-2.0
"""Integrationstest für Skill-Paket K4 (WA-61): Bilder, Dateianhänge und ZIP-Container.

Prüft die Kernbausteine von Paket K4:
1. Sicherheitsprüfung von Austausch-ZIP-Containern (inspect_exchange_archive, Schutz gegen Zip-Slip).
2. Import von .glideexchange-ZIP-Containern mit Anhängen (Ordner, Listen, Aufgaben).
3. Galerie-Listen mit Dateianhängen (list_kind: gallery).
4. Seiten-Cover (cover: attachments/...) und Markdown-Seiten mit eingebetteten Bildern (![...](attachments/...)).
5. Export von Austauschpaketen (write_exchange_package, build_exchange_payload mit Anhängen & Cover).
6. Sauberes Rollback: Aufräumen physisch erzeugter Anhangsdateien bei fehlgeschlagenem Import.
"""
import copy
import importlib.machinery
import importlib.util
import io
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
    temp_dir = tempfile.mkdtemp(prefix="glide-k4-test-")
    data_dir = os.path.join(temp_dir, "daten")
    os.makedirs(data_dir, exist_ok=True)
    os.environ["GLIDE_DATA_DIR"] = data_dir
    os.environ["GLIDE_TEST_MODE"] = "1"

    loader = importlib.machinery.SourceFileLoader(
        f"glide_app_k4_{Path(temp_dir).name.replace('-', '_')}", str(SOURCE / "app.pyw")
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
        # 1. Baustein: Sicherheitsprüfung (Zip-Slip, Pfadvalidierung)
        # ------------------------------------------------------------------
        boeses_zip_pfad = os.path.join(temp_dir, "evil.zip")
        with zipfile.ZipFile(boeses_zip_pfad, "w") as zf:
            zf.writestr("../boese.txt", "schadcode")
            zf.writestr("exchange.json", json.dumps({"format": "glide.exchange", "format_version": 2, "lists": []}))

        with zipfile.ZipFile(boeses_zip_pfad, "r") as zf:
            try:
                app.inspect_exchange_archive(zf)
                assert False, "Zip-Slip mit '../' hätte abgewiesen werden müssen"
            except ValueError:
                pruefungen.append("1.1 Zip-Slip-Abweisung erfolgreich")

        boeses_zip_pfad2 = os.path.join(temp_dir, "evil_folder.zip")
        with zipfile.ZipFile(boeses_zip_pfad2, "w") as zf:
            zf.writestr("unbekannter_ordner/datei.txt", "daten")
            zf.writestr("exchange.json", json.dumps({"format": "glide.exchange", "format_version": 2, "lists": []}))

        with zipfile.ZipFile(boeses_zip_pfad2, "r") as zf:
            try:
                app.inspect_exchange_archive(zf)
                assert False, "Nicht erlaubter Ordner im Paket hätte abgewiesen werden müssen"
            except ValueError:
                pruefungen.append("1.2 Unbekannte Ordner im Paket abgewiesen")

        # ------------------------------------------------------------------
        # 2. Baustein: Erstellung und Import eines vollständigen Austauschpakets
        # ------------------------------------------------------------------
        paket_pfad = os.path.join(temp_dir, "gueltig.glideexchange")
        nutzlast = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "folders": [
                {
                    "key": "o1",
                    "title": "Projektordner",
                    "attachments": [{"name": "ordner_doku.txt", "file": "attachments/ordner_doku.txt"}],
                }
            ],
            "lists": [
                {
                    "key": "l1",
                    "title": "Aufgaben mit Anhang",
                    "folder": "o1",
                    "list_kind": "tasks",
                    "items": [
                        {
                            "title": "Aufgabe 1",
                            "attachments": [{"name": "spezifikation.pdf", "file": "attachments/spezifikation.pdf"}],
                        }
                    ],
                },
                {
                    "key": "l2",
                    "title": "Fotogalerie",
                    "folder": "o1",
                    "list_kind": "gallery",
                    "attachments": [
                        {"name": "landschaft.png", "file": "attachments/landschaft.png", "title": "Berge"}
                    ],
                },
                {
                    "key": "l3",
                    "title": "Dokumentation",
                    "folder": "o1",
                    "list_kind": "page",
                    "cover": "attachments/cover.png",
                    "markdown": "# Projekthandbuch\n\nEinleitungstext.\n\n![Architektur](attachments/architektur.png)\n\n- [ ] Prüfen\n- [x] Abstimmen",
                },
            ],
        }

        # Erstelle echtes PNG-Dummy-Bild
        transparent_png = (
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
            b"\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc`\x00\x00\x00"
            b"\x02\x00\x01H\xaf\xa4q\x00\x00\x00\x00IEND\xaeB`\x82"
        )

        with zipfile.ZipFile(paket_pfad, "w") as zf:
            zf.writestr("exchange.json", json.dumps(nutzlast, ensure_ascii=False, indent=2))
            zf.writestr("attachments/ordner_doku.txt", "Ordner Dokumentation Inhalt")
            zf.writestr("attachments/spezifikation.pdf", "%PDF-1.4 Spezifikation Inhalt")
            zf.writestr("attachments/landschaft.png", transparent_png)
            zf.writestr("attachments/cover.png", transparent_png)
            zf.writestr("attachments/architektur.png", transparent_png)

        # Import über read_exchange_file und apply_exchange_payload
        json_inhalt = app.read_exchange_file(paket_pfad)
        gelesen_doc, bericht = app.parse_exchange_document(json_inhalt)
        assert gelesen_doc is not None, f"Parsing fehlgeschlagen: {bericht.errors}"

        listen = app.apply_exchange_payload(gelesen_doc, attachment_source=paket_pfad)
        assert listen is not None and len(listen) == 3, f"Erwartet 3 Listen, erhalten: {len(listen) if listen else 0}"
        pruefungen.append("2.1 Paket-Import erfolgreich ausgeführt")

        # ------------------------------------------------------------------
        # 3. Baustein: Verifikation der übernommenen Objekte & Dateien
        # ------------------------------------------------------------------
        # Prüfe Ordner
        ordner = next((o for o in app.folders if o["title"] == "Projektordner"), None)
        assert ordner is not None, "Ordner nicht angelegt"
        assert len(ordner.get("attachments") or []) == 1, "Ordner-Anhang fehlt"
        ordner_anhang = ordner["attachments"][0]
        assert ordner_anhang["name"] == "ordner_doku.txt"
        ordner_anhang_pfad = app.resolve_attachment_path(ordner_anhang)
        assert ordner_anhang_pfad and os.path.isfile(ordner_anhang_pfad), "Physische Ordner-Anhangdatei fehlt"
        pruefungen.append("3.1 Ordner-Anhang physisch in ATTACHMENTS_DIR vorhanden")

        # Prüfe Aufgabenliste mit Anhang
        liste_tasks = next((l for l in listen if l["title"] == "Aufgaben mit Anhang"), None)
        assert liste_tasks is not None, "Aufgabenliste fehlt"
        aufgabe = liste_tasks["items"][0]
        assert len(aufgabe.get("attachments") or []) == 1, "Aufgaben-Anhang fehlt"
        aufgabe_anhang = aufgabe["attachments"][0]
        assert aufgabe_anhang["name"] == "spezifikation.pdf"
        aufgabe_anhang_pfad = app.resolve_attachment_path(aufgabe_anhang)
        assert aufgabe_anhang_pfad and os.path.isfile(aufgabe_anhang_pfad), "Physische Aufgaben-Anhangdatei fehlt"
        pruefungen.append("3.2 Aufgaben-Anhang physisch in ATTACHMENTS_DIR vorhanden")

        # Prüfe Galerie-Liste
        liste_galerie = next((l for l in listen if l["title"] == "Fotogalerie"), None)
        assert liste_galerie is not None, "Galerie fehlt"
        assert liste_galerie.get("list_kind") == "gallery", f"Erwartet gallery, erhalten: {liste_galerie.get('list_kind')}"
        assert len(liste_galerie.get("attachments") or []) == 1, "Galerie-Bild fehlt"
        bild_anhang = liste_galerie["attachments"][0]
        assert bild_anhang.get("title") == "Berge", "Galerie-Bildtitel fehlt"
        bild_pfad = app.resolve_attachment_path(bild_anhang)
        assert bild_pfad and os.path.isfile(bild_pfad), "Physisches Galeriebild fehlt"
        pruefungen.append("3.3 Galerie-Liste samt Anhang & Titel übernommen")

        # Prüfe Seite mit Cover und eingebettetem Markdown-Bild
        liste_seite = next((l for l in listen if l["title"] == "Dokumentation"), None)
        assert liste_seite is not None, "Seite fehlt"
        assert liste_seite.get("list_kind") == "page", f"Erwartet page, erhalten: {liste_seite.get('list_kind')}"
        assert liste_seite.get("cover") is not None, "Seiten-Cover fehlt"
        assert liste_seite["cover"].get("kind") == "image", "Seiten-Cover hat falsche Art"
        cover_att_id = liste_seite["cover"].get("attachment")
        assert any(a.get("id") == cover_att_id for a in (liste_seite.get("attachments") or [])), "Cover-Anhang nicht in Listen-Anhängen"

        rich_note = liste_seite.get("rich_note") or {}
        assert "\ufffc" in rich_note.get("text", ""), "Bild-Anker fehlt im Seitentext"
        assert bool(rich_note.get("images")), "images-Dict fehlt im rich_note"
        assert len(liste_seite.get("items") or []) == 2, "Checkbox-Aufgaben aus Markdown fehlen"
        pruefungen.append("3.4 Seiten-Cover und Markdown-Bild erfolgreich eingebettet")

        # ------------------------------------------------------------------
        # 4. Baustein: Export von Austauschpaket (write_exchange_package)
        # ------------------------------------------------------------------
        export_zip = os.path.join(temp_dir, "exportiert.glideexchange")
        export_payload = app.build_exchange_payload(lists=[liste_tasks, liste_galerie, liste_seite], folders=[ordner])
        app.write_exchange_package(
            export_zip,
            export_payload,
            attachments=[ordner_anhang, aufgabe_anhang, bild_anhang],
        )
        assert os.path.isfile(export_zip), "Exportierte ZIP-Datei existiert nicht"
        with zipfile.ZipFile(export_zip, "r") as zf:
            export_infolist = zf.namelist()
            assert "exchange.json" in export_infolist, "exchange.json fehlt im exportierten Paket"
            assert any(n.startswith("attachments/") for n in export_infolist), "Anhänge fehlen im exportierten Paket"
        pruefungen.append("4.1 write_exchange_package und build_exchange_payload erfolgreich")

        # ------------------------------------------------------------------
        # 5. Baustein: Rollback bei fehlerhaftem Import räumt neue Dateien auf
        # ------------------------------------------------------------------
        vorher_dateien = set(os.listdir(app.paths.attachments_dir))
        schlechtes_paket = os.path.join(temp_dir, "schlecht.glideexchange")
        schlechte_nutzlast = {
            "format": "glide.exchange",
            "format_version": 2,
            "mode": "create",
            "lists": [
                {
                    "title": "Gute Liste",
                    "attachments": [{"name": "datei_roll.txt", "file": "attachments/datei_roll.txt"}],
                },
                {
                    # Liste ohne Titel wird zwar übersprungen, aber wenn keine Liste übrig bleibt oder Fehler fliegt:
                    "title": "Ungültig",
                    "list_kind": "drawing",
                    "items": [{"title": "Punkte in Zeichnung verboten"}],
                },
            ],
        }
        with zipfile.ZipFile(schlechtes_paket, "w") as zf:
            zf.writestr("exchange.json", json.dumps(schlechte_nutzlast))
            zf.writestr("attachments/datei_roll.txt", "Wird wieder aufgeräumt")

        # Parsing weist verbotene Punkte in Zeichnung ab
        roh_schlecht = app.read_exchange_file(schlechtes_paket)
        _, schlecht_bericht = app.parse_exchange_document(roh_schlecht)
        assert bool(schlecht_bericht.errors), "Ungültige Zeichnung mit Punkten hätte Fehler melden müssen"

        # Simuliere Importabbruch / Fehler mitten in apply_exchange_payload:
        try:
            app.apply_exchange_payload(
                {"format": "glide.exchange", "format_version": 2, "lists": [
                    {"title": "Abbruch", "list_kind": "drawing", "items": [{"title": "Verboten"}],
                     "attachments": [{"name": "roll.txt", "file": "attachments/datei_roll.txt"}]}
                ]},
                attachment_source=schlechtes_paket
            )
        except Exception:
            pass

        nachher_dateien = set(os.listdir(app.paths.attachments_dir))
        assert nachher_dateien == vorher_dateien, f"Dateien wurden bei Rollback nicht aufgeräumt: {nachher_dateien - vorher_dateien}"
        pruefungen.append("5.1 Rollback räumt neu erzeugte Anhangsdateien vollständig auf")

        print(f"Integrationstest K4 erfolgreich: {len(pruefungen)} Prüfungen bestanden.")
        for p in pruefungen:
            print(f"  ✓ {p}")

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
