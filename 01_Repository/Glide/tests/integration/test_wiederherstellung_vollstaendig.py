# SPDX-License-Identifier: MPL-2.0
"""Teil 05B (DS-06): Vollständige Wiederherstellungsprobe mit künstlichen Daten.

Drei getrennte Prozesse, weil der Datenordner beim Import feststeht:
1. Aufbau in Ordner A: repräsentativer Bestand (Referenz Format 27 mit
   Kapitelankern, Kapitelverweis, Navigationsort, Beziehungen, Zeichnung mit
   Bildfolge, Notizbuch, Archiv) plus verschachtelte Ordner, ein Anhang, der
   von Liste und Aufgabe gemeinsam genutzt wird, Papierkorb, Vorlage und
   Einstellung. Vollständige App-Sicherung über den Produktweg.
2. Wiederherstellung in einen leeren Ordner B über `restore_app_backup`.
3. Neustart von B, erneutes Speichern.
Verglichen werden Objekte, Kennungen, Inhalte, Hierarchie, Verweise, Anker,
Navigationsorte, Anhangsbytes, Vorlagen und Einstellungen.
"""
import argparse
import copy
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
parser.add_argument("--phase", default=None)
parser.add_argument("--ordner", type=Path, default=None)
parser.add_argument("--archiv", type=Path, default=None)
parser.add_argument("--bericht", type=Path, default=None)
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))
FLUECHTIG = {"updated_at", "exported_at", "history", "app_version", "refreshed_at"}


def laden(directory):
    os.environ["GLIDE_DATA_DIR"] = str(directory)
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader(f"glide_wh_{args.phase}", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    return mod


def oeffnen(mod, fehler):
    root = mod.tk.Tk()
    root.geometry("1000x700+40+40")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    app.show_warning = lambda *a, **k: fehler.append(repr(a))
    app.show_info = lambda *a, **k: None
    app.ask_yes_no = lambda *a, **k: True
    for _ in range(15):
        root.update()
        time.sleep(0.02)
    return root, app


def ohne_fluechtiges(wert):
    if isinstance(wert, dict):
        return {k: ohne_fluechtiges(v) for k, v in wert.items() if k not in FLUECHTIG}
    if isinstance(wert, list):
        return [ohne_fluechtiges(v) for v in wert]
    return wert


def bericht(app, directory):
    daten = ohne_fluechtiges(copy.deepcopy(app.data_payload()))
    anhaenge = {}
    for pfad in sorted((Path(directory) / "attachments").rglob("*")):
        if pfad.is_file():
            anhaenge[pfad.relative_to(directory).as_posix()] = hashlib.sha256(pfad.read_bytes()).hexdigest()
    return {"daten": daten, "anhaenge": anhaenge,
            "vorlagen": sorted(t.get("name", "") for t in app.templates),
            "einstellung": app.settings.get("daily_capacity_minutes"),
            "seite_kapitel": [k.key for k in app.chapter_outline(app.page_entry("fixture-notion-page"))],
            # E01: KI-Arbeitsbereich (Begleitdatei) gehört zur vollständigen Wiederherstellung.
            "ki": ohne_fluechtiges(app.ai_workspace().to_payload())}


def aufbau(directory):
    ref = json.loads((REPO / "tests/fixtures/current_v27/reference_v27.json").read_text(encoding="utf-8"))
    (directory / "liste_speicher.json").write_text(json.dumps(ref, ensure_ascii=False), encoding="utf-8")
    mod = laden(directory)
    fehler = []
    root, app = oeffnen(mod, fehler)
    oben = app.new_folder_object("Projekte")
    unten = app.new_folder_object("Teilprojekt", parent_id=oben["id"])
    app.folders.extend([oben, unten])
    quelle = directory.parent / "probe-anhang.bin"
    quelle.write_bytes(bytes(range(256)) * 64)
    gespeichert = app.store_attachment(str(quelle), "probe-anhang.bin")
    liste = app.new_list_object("Mit Anhang", [], folder_id=unten["id"], attachments=[gespeichert])
    app.lists.append(liste)
    aufgaben = app.current_list() and None
    tasks = next(e for e in app.lists if e["id"] == "fixture-tasks")
    tasks["items"][0].setdefault("attachments", []).append(copy.deepcopy(gespeichert))
    weg = app.new_list_object("Kommt in den Papierkorb", [])
    app.lists.append(weg)
    assert app.save_items()
    app.delete_list_by_id(weg["id"])
    app.settings["daily_capacity_minutes"] = 333
    app.save_settings() if hasattr(app, "save_settings") else None
    vorlage = app.capture_template(list_id="fixture-tasks")
    vorlage["name"] = "Probevorlage"
    app.templates.append(vorlage)
    app.save_templates()
    assert app.save_items()
    assert app.trash, "Papierkorb leer"
    # KI-Arbeitsbereich: Projekt, Anweisung, Agent, Baustein, Paket, Prompt mit Version,
    # Dokument mit zwei Versionen, Bericht, Folgeauftrag.
    ws = app.ai_workspace()
    ws.project(oben["id"])["description"] = "Probe"
    anweisung = ws.set_instruction(oben["id"], "Regel", "Erste Fassung")
    ws.set_instruction(oben["id"], "Regel", "Zweite Fassung", anweisung)
    agent = ws.add_agent("Probe-Agent", provider="lokal")
    baustein = ws.add_block("Architektur", "Shell-First")
    paket = ws.add_pack("Paket", [{"kind": "block", "id": baustein}])
    prompt = app.ai_create_prompt(title="Probe-Prompt", body="Freitext", folder_id=oben["id"],
                                  fields={"basics": {"goal": "Ziel"}})
    ws.prompt(prompt)["agent"] = agent
    ws.prompt(prompt)["context"] += [{"kind": "pack", "id": paket}, {"kind": "instruction", "id": anweisung}]
    dok_quelle = directory.parent / "dokument.md"
    dok_quelle.write_text("# Dokument v1", encoding="utf-8")
    dok = app.ai_import_documents(paths=[str(dok_quelle)])[0]
    dok_quelle.write_text("# Dokument v2", encoding="utf-8")
    app.ai_import_documents(paths=[str(dok_quelle)], add_version_to=dok)
    ws.prompt(prompt)["context"].append({"kind": "doc", "id": dok})
    md, info = ws.render(prompt, "Probe-Prompt", "Freitext")
    ws.create_version(prompt, md, "Freitext", info, "übergeben")
    ws.add_report(prompt, "Bericht", "Ergebnis")
    folge = app.ai_create_prompt(title="Folgeauftrag", source=(prompt, "follow_up"))
    assert app.save_ai_workspace() and folge
    archiv = directory.parent / "probe.glideapp"
    app.write_complete_backup(str(archiv), app.app_backup_payload())
    args.bericht.write_text(json.dumps(bericht(app, directory), ensure_ascii=False), encoding="utf-8")
    app.on_close()
    assert not fehler, fehler


def wiederherstellen(directory):
    mod = laden(directory)
    fehler = []
    root, app = oeffnen(mod, fehler)
    sektionen = {name: True for name in app.APP_BACKUP_SECTIONS}
    assert app.restore_app_backup(path=str(args.archiv), sections=sektionen, show_success=False), fehler
    for _ in range(10):
        root.update()
    assert app.save_items()
    args.bericht.write_text(json.dumps(bericht(app, directory), ensure_ascii=False), encoding="utf-8")
    app.on_close()
    assert not fehler, fehler


def neustart(directory):
    mod = laden(directory)
    fehler = []
    root, app = oeffnen(mod, fehler)
    assert not app._data_read_only, app._read_only_reason
    assert app.save_items()
    args.bericht.write_text(json.dumps(bericht(app, directory), ensure_ascii=False), encoding="utf-8")
    app.on_close()
    assert not fehler, fehler


def lauf(phase, ordner, archiv, bericht_pfad):
    ergebnis = subprocess.run([sys.executable, "-B", __file__, "--app", str(args.app), "--phase", phase,
                               "--ordner", str(ordner), "--archiv", str(archiv), "--bericht", str(bericht_pfad)],
                              capture_output=True, text=True, timeout=600)
    assert ergebnis.returncode == 0, (phase, ergebnis.stdout[-1500:], ergebnis.stderr[-3000:])
    return json.loads(bericht_pfad.read_text(encoding="utf-8"))


def unterschiede(a, b, pfad=""):
    if type(a) is not type(b):
        return [f"{pfad}: {type(a).__name__} ≠ {type(b).__name__}"]
    if isinstance(a, dict):
        aus = []
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                aus.append(f"{pfad}/{k}: nur {'B' if k not in a else 'A'}")
            else:
                aus += unterschiede(a[k], b[k], f"{pfad}/{k}")
        return aus
    if isinstance(a, list):
        if len(a) != len(b):
            return [f"{pfad}: Länge {len(a)} ≠ {len(b)}"]
        aus = []
        for i, (x, y) in enumerate(zip(a, b)):
            aus += unterschiede(x, y, f"{pfad}[{i}]")
        return aus
    return [] if a == b else [f"{pfad}: {a!r} ≠ {b!r}"]


def haupt():
    with tempfile.TemporaryDirectory(prefix="glide-wh-", ignore_cleanup_errors=True) as tmp:
        tmp = Path(tmp)
        a, b = tmp / "a", tmp / "b"
        a.mkdir()
        b.mkdir()
        archiv = tmp / "probe.glideapp"
        vorher = lauf("aufbau", a, archiv, tmp / "bericht_a.json")
        assert archiv.is_file()
        nachher = lauf("wiederherstellen", b, archiv, tmp / "bericht_b.json")
        neu = lauf("neustart", b, archiv, tmp / "bericht_c.json")
        for name, stand in (("Wiederherstellung", nachher), ("Neustart", neu)):
            diff = unterschiede(vorher, stand)
            assert not diff, (name, diff[:25])
        daten = vorher["daten"]
        assert len(vorher["anhaenge"]) >= 1 and vorher["anhaenge"] == neu["anhaenge"]
        assert vorher["seite_kapitel"] and vorher["seite_kapitel"] == neu["seite_kapitel"]
        assert any(e.get("nav_parent_id") for e in daten["lists"])
        assert daten["trash"], "Papierkorb nicht gesichert"
        ki = vorher["ki"]
        assert len(ki["prompts"]) == 2 and len(ki["documents"]) == 1 and ki["reports"] and ki["packs"] and ki["agents"]
        assert len(next(iter(ki["documents"].values()))["versions"]) == 2
        assert vorher["ki"] == neu["ki"], "KI-Arbeitsbereich nach Neustart verändert"
        print(f"test_wiederherstellung_vollstaendig: OK ({len(daten['lists'])} Listen, {len(daten['folders'])} Ordner, "
              f"{len(vorher['anhaenge'])} Anhangsdateien, {len(daten['trash'])} Papierkorbeinträge, "
              f"KI-Arbeitsbereich mit {len(ki['prompts'])} Prompts und {len(ki['documents'])} Dokument; Windows-Tk, künstliche Daten)")


if args.phase == "aufbau":
    aufbau(args.ordner)
elif args.phase == "wiederherstellen":
    wiederherstellen(args.ordner)
elif args.phase == "neustart":
    neustart(args.ordner)
else:
    haupt()
