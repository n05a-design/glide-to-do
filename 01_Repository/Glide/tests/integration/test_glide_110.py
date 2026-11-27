# SPDX-License-Identifier: MPL-2.0
"""Integrationsprüfung Glide 1.1.0 an der echten App (künstliche Daten, eigener GLIDE_DATA_DIR).

Abgedeckt:
1. Bento 0.2.0 auf der Startseite: Pilot „Zwei Spalten“ im Dreispaltenraster,
   Breakpoint-Wechsel, „Ganze Breite“ bleibt über dem Raster, Einstellung
   übersteht die Normalisierung, Editor zeigt den Schalter.
2. WA-52: Leerzustände Startseite (alle Kacheln aus), leere Liste, Heute,
   Seitenübersicht und Pinnwand mit Titel und Aktion.
3. L4: drei Referenzvorlagen DE und EN anwenden, Platzhalter, Datumsverschiebung,
   Beziehungen, Mehrfachanwendung, Undo und Persistenz nach erneutem Laden.
4. WA-53: Banner in „Verspätet“, „Heute einplanen“ ohne Friständerung,
   „Fristen neu setzen …“ ohne Serienaufgaben, je ein Undo-Schritt.

Aufruf aus `01_Repository/Glide`: python3 -B tests/integration/test_glide_110.py
"""
import importlib.machinery
import importlib.util
import json
import os
from datetime import date, timedelta
from pathlib import Path
import sys
import tempfile

repo = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(repo / "src/glide"))


def descendants(widget):
    result = []
    for child in widget.winfo_children():
        result.append(child)
        result.extend(descendants(child))
    return result


with tempfile.TemporaryDirectory(prefix="glide-110-") as directory:
    os.environ["GLIDE_DATA_DIR"] = directory
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_110", str(repo / "src/glide/app.pyw"))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    import glide_bento
    import i18n
    import empty_states

    errors = []
    root = mod.tk.Tk()
    root.geometry("1500x950+20+20")
    root.report_callback_exception = lambda *exc: errors.append(f"{exc[0].__name__}: {exc[1]}")
    app = mod.ListApp(root)
    checks = []

    def idle():
        for _ in range(3):
            root.update_idletasks()
            root.update()

    def check(name, condition, detail=""):
        checks.append((name, bool(condition)))
        assert condition, f"{name}: {detail}"

    try:
        idle()
        heute = date.today()

        # ---------------- 1. Startseite Multi-Span ----------------
        app.settings["home_columns"] = "3"
        app.settings["home_tile_order"] = ["clock", "welcome", "calendar", "today", "impulse", "week", "recent"]
        app.settings["home_tiles_hidden"] = [k for k in app.HOME_TILE_KEYS if k not in app.settings["home_tile_order"]]
        app.set_home_tile_span("calendar", "double")
        normalized = app.settings.get("home_tile_span")
        app.set_home_view()
        idle()
        plan = app._home_layout_plan
        split = [b for b in plan.bands if b.kind == "split"]
        check("1a Bandmodell mit Zweispaltenkarte", split and split[0].lanes[0].cards[0].key == "calendar"
              and split[0].lanes[0].span == 2, [b.kind for b in plan.bands])
        check("1b Ganze Breite bleibt über dem Raster",
              not any(c.key in ("clock", "welcome") for b in plan.bands for c in b.cards if b.kind != "full"))
        check("1c Einstellung double bleibt", normalized.get("calendar") == "double", normalized)
        loaded = app.normalized_settings(dict(app.settings)) if hasattr(app, "normalized_settings") else None
        app.settings["home_columns"] = "2"
        app.refresh_home()
        idle()
        kinds2 = [(b.kind, [c.key for c in b.cards]) for b in app._home_layout_plan.bands]
        check("1d Zwei Spalten: Karte über volle Breite an ihrer Stelle",
              ("full", ["calendar"]) in kinds2 and app._home_layout_plan.column_count == 2, kinds2)
        app.settings["home_columns"] = "1"
        app.refresh_home()
        idle()
        check("1e Eine Spalte: kein Split", all(b.kind != "split" for b in app._home_layout_plan.bands))
        app.settings["home_columns"] = "auto"
        app.toggle_home_editing()
        idle()
        texte = [getattr(w, "text", "") for w in descendants(app.home_content)]
        check("1f Editor bietet Zwei Spalten / Eine Spalte",
              any(t in ("Zwei Spalten", "Eine Spalte") for t in texte), texte[:20])
        app.toggle_home_editing()
        idle()

        # ---------------- 2. Leerzustände ----------------
        app.settings["home_tiles_hidden"] = list(app.HOME_TILE_KEYS)
        app.refresh_home()
        idle()
        leer = getattr(app, "_home_empty_state", None)
        check("2a Startseite: BentoEmptyState mit zwei Aktionen", leer is not None and leer.winfo_exists()
              and leer.action_button is not None and leer.secondary_button is not None)
        leer.secondary_button.command()
        idle()
        check("2b Standard wiederherstellen blendet Kacheln ein",
              any(app.home_tile_visible(k) for k in app.HOME_TILE_KEYS))

        liste = app.new_list_object("Leere Testliste", [])
        app.lists.append(liste)
        app.set_active_list(liste["id"])
        idle()
        zeile = app.tree.item(app.EMPTY_ROW_ID, "text")
        check("2c Leere Liste: Titel und Erklärung", zeile == app.empty_state_for("list").text, zeile)
        check("2d U20: kein zweiter Anlegeknopf bei sichtbarer Eingabezeile",
              app.empty_state_action() is None or app.entry_line_visible() is False)

        app.set_plan_day_view() if hasattr(app, "set_plan_day_view") else app._activate_system_view(app.PLAN_DAY_VIEW)
        idle()
        aktion = app.empty_state_action()
        check("2e Heute: Hauptaktion vorhanden", aktion is not None and aktion[0] in (
            empty_states.empty_state("today")[0] if False else "Arbeitstag planen …", "Erste Aufgabe anlegen"), aktion)

        app._activate_system_view(app.PAGES_VIEW)
        idle()
        seiten = getattr(app, "_pages_empty_state", None)
        if not app.page_entries():
            check("2f Seitenübersicht ohne Seiten: Leerzustand", seiten is not None and seiten.winfo_exists())
            vorher = len(app.page_entries())
            seiten.action_button.command()
            idle()
            check("2g Erste Seite erstellen legt eine Seite an", len(app.page_entries()) == vorher + 1)
        else:
            checks.append(("2f/2g Seitenübersicht (Bestand hat Seiten, übersprungen)", True))

        # ---------------- 3. Vorlagen L4 DE/EN ----------------
        app.confirm_template_preview = lambda template: True
        meldungen = []
        app.show_error = lambda title, message, **o: meldungen.append(f"{title}: {message}")
        app.ask_template_fields = lambda fields, title="": {name: "Muster GmbH" for name in fields}
        for sprache in ("de", "en"):
            i18n.set_language(sprache)
            app.templates = app.default_template_records(sprache)
            for vid in ("client-project", "design-project", "weekly-review"):
                vorlage = app.template_by_id(vid)
                check(f"3a {sprache}/{vid} im Katalog", vorlage is not None and "payload" in vorlage)
                listen_vorher = {e["id"] for e in app.lists}
                ordner_vorher = {f["id"] for f in app.folders}
                tiefe = len(app.undo_stack)
                ergebnis = app.create_list_from_template(vid)
                idle()
                check(f"3b {sprache}/{vid} angewendet", ergebnis is not None, (errors[-3:], meldungen[-3:]))
                neu = [e for e in app.lists if e["id"] not in listen_vorher]
                punkte = [i for e in neu for i in app.walk_items(e.get("items", []))]
                ids = {i["id"] for i in punkte}
                check(f"3c {sprache}/{vid} Punkte und Beziehungen", punkte and all(
                    ref in ids for i in punkte for ref in i.get("blocked_by", [])), len(punkte))
                texte = " ".join(i["text"] for i in punkte)
                check(f"3d {sprache}/{vid} Platzhalter ersetzt", "{{" not in texte and "}}" not in texte, texte[:200])
                daten = sorted(d for i in punkte for d in (i.get("due"), i.get("planned_date")) if d)
                check(f"3e {sprache}/{vid} Daten relativ ab heute", daten and daten[0] >= heute.isoformat(), daten[:3])
                # Mehrfachanwendung: neue Kennungen
                zweit = app.create_list_from_template(vid)
                idle()
                neu2 = [e for e in app.lists if e["id"] not in listen_vorher and e not in neu]
                ids2 = {i["id"] for e in neu2 for i in app.walk_items(e.get("items", []))}
                check(f"3f {sprache}/{vid} zweite Anwendung mit eigenen Kennungen", zweit is not None and ids2
                      and not (ids & ids2))
                # Undo nimmt die zweite Anwendung zurück
                app.undo_last_change()
                idle()
                check(f"3g {sprache}/{vid} Undo", not any(e["id"] in {x["id"] for x in neu2} for e in app.lists))
                if sprache == "en":
                    check(f"3h en/{vid} englische Texte", not any(ch in texte for ch in "äöüß"), texte[:120])
        i18n.set_language("de")
        app.save_items()
        gespeichert = json.loads(Path(mod.SAVE_FILE).read_text(encoding="utf-8")) if Path(mod.SAVE_FILE).is_file() else {}
        titel = {e.get("title") for e in gespeichert.get("lists", [])}
        check("3i Persistenz in der Speicherdatei", {"Phasen und Meilensteine", "Persönliche Wochenplanung"} <= titel,
              sorted(titel)[:12])

        # ---------------- 4. WA-53 ----------------
        ziel = app.new_list_object("Fristen", [])
        alt = (heute - timedelta(days=9)).isoformat()
        ziel["items"] = [app.new_item("Verstrichen A", due=alt), app.new_item("Verstrichen B", due=(heute - timedelta(days=2)).isoformat()),
                         app.new_item("Serie", due=alt, repeat={"art": "woechentlich", "start": alt, "ende": None}),
                         app.new_item("Zukunft", due=(heute + timedelta(days=3)).isoformat())]
        app.lists.append(ziel)
        app.save_items()
        app.set_overdue_view()
        idle()
        banner = getattr(app, "overdue_banner", None)
        check("4a Banner in Verspätet", banner is not None and banner.winfo_manager() == "pack"
              and "verstrichener Frist" in app.overdue_banner_text.cget("text"), app.overdue_banner_text.cget("text") if banner else None)
        faellig_vorher = {i["id"]: i["due"] for i in ziel["items"]}
        app.plan_overdue_today()
        idle()
        items = {i["text"]: i for i in app.find_list(ziel["id"])["items"]} if hasattr(app, "find_list") else \
            {i["text"]: i for i in next(e for e in app.lists if e["id"] == ziel["id"])["items"]}
        check("4b Heute einplanen setzt nur Bearbeitungstag",
              all(items[n].get("planned_date") == heute.isoformat() for n in ("Verstrichen A", "Verstrichen B", "Serie"))
              and items["Zukunft"].get("planned_date") is None
              and {i["id"]: i["due"] for i in items.values()} == faellig_vorher)
        app.undo_last_change()
        idle()
        items = {i["text"]: i for i in next(e for e in app.lists if e["id"] == ziel["id"])["items"]}
        check("4c Undo nimmt Einplanen in einem Schritt zurück",
              all(not items[n].get("planned_date") for n in ("Verstrichen A", "Verstrichen B", "Serie")))
        neu_frist = (heute + timedelta(days=1)).isoformat()
        app.themed_due_dialog = lambda *a, **k: (neu_frist, None)
        fragen = []
        app.ask_yes_no = lambda title, message, **o: fragen.append(message) or True
        app.shift_overdue_dues()
        idle()
        items = {i["text"]: i for i in next(e for e in app.lists if e["id"] == ziel["id"])["items"]}
        check("4d Fristen neu setzen nach Rückfrage, Serie unverändert",
              fragen and items["Verstrichen A"]["due"] == neu_frist and items["Verstrichen B"]["due"] == neu_frist
              and items["Serie"]["due"] == alt and "Serienaufgaben" in fragen[0], fragen)
        app.undo_last_change()
        idle()
        items = {i["text"]: i for i in next(e for e in app.lists if e["id"] == ziel["id"])["items"]}
        check("4e Undo stellt Fristen exakt wieder her", {i["id"]: i["due"] for i in items.values()} == faellig_vorher)
        app.ask_yes_no = lambda title, message, **o: False
        app.shift_overdue_dues()
        idle()
        items = {i["text"]: i for i in next(e for e in app.lists if e["id"] == ziel["id"])["items"]}
        check("4f Abbruch ändert nichts", {i["id"]: i["due"] for i in items.values()} == faellig_vorher)
        app.set_active_list(ziel["id"])
        idle()
        check("4g Banner nur in Verspätet", banner.winfo_manager() == "")

        check("Keine Tk-Rückruffehler", not errors, errors)
        print(f"test_glide_110: OK; {len(checks)} Prüfungen bestanden "
              "(Startseite Multi-Span, Leerzustände, Vorlagen DE/EN, verstrichene Fristen)")
    finally:
        root.destroy()
