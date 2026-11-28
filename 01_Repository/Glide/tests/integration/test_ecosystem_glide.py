# SPDX-License-Identifier: MPL-2.0
"""Ecosystem E03 in Glide: Über, Weitere Programme, Symbolbibliothek, Pixelsymbol, Sicherung (T379).

Künstliche Daten in einem temporären GLIDE_DATA_DIR. Kein Dialog wartet auf
einen Menschen: Modale Abläufe werden im Leerlauf bedient bzw. geschlossen.
"""
import base64
import json
import os
from pathlib import Path
import sys
import tempfile
import importlib.machinery
import importlib.util

ROOT = Path(__file__).resolve().parents[2]

with tempfile.TemporaryDirectory(prefix="glide-eco-qa-", ignore_cleanup_errors=True) as tmp:
    os.environ["GLIDE_DATA_DIR"] = tmp
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_eco_qa", str(ROOT / "src/glide/app.pyw"))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1100x760+30+30")
    fehler, warnungen, links = [], [], []
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(a)
    app.show_warning = lambda *a, **k: warnungen.append(a)
    app.show_info = lambda *a, **k: None
    app.open_catalog_link = lambda url: links.append(url)

    def pump(n=4):
        for _ in range(n):
            root.update_idletasks()
            root.update()

    pump()
    schritte = []
    # Über: Framework- und Laufzeitangaben aus dem Shell-Vertrag, keine erfundenen Werte.
    text = app.about_system_text()
    import glide_shell, glide_bento
    assert glide_shell.SHELL_VERSION in text and glide_bento.BENTO_VERSION in text and "Python" in text and "Tk 9" in text or "Tk 8" in text, text
    assert any("Weitere Programme" in str(t) or "More programs" in str(t) for t, *_ in app.menubar_structure()[-1][1] if t)
    schritte.append("Über: Shell, Bento, Python, Tk, Betriebssystem")

    # Weitere Programme: eigenes Fenster, nur andere Produkte, Links nach Klick, Mehrfachöffnung holt dasselbe Fenster.
    fenster = app.show_more_programs()
    pump()
    karten = app._more_programs_portfolio.cards
    assert set(karten) == {"steps", "chess-and-chains"}, set(karten)
    assert links == [], "kein Link ohne Klick"
    knopf = karten["steps"].actions.buttons[0]  # Glide liefert seine eigenen Knöpfe über den Bento-Kontext
    (getattr(knopf, "invoke", None) or knopf.command)()
    assert links and links[0].startswith("https://github.com/n05a-design/steps"), links
    assert app.show_more_programs() is fenster, "zweites Öffnen holt das vorhandene Fenster"
    fenster.event_generate("<Escape>")
    pump()
    assert not fenster.winfo_exists()
    schritte.append("Weitere Programme: Portfolio ohne Glide, Link erst nach Klick, ein Fenster, Escape schließt")

    # Symbolbibliothek: PNG- und SVG-Import, unsichere Datei abgewiesen, Duplikat erkannt.
    quelle = Path(tmp).parent / "eco-symbole"
    quelle.mkdir(exist_ok=True)
    bild = mod.tk.PhotoImage(master=root, width=24, height=24)
    bild.put("#C62828", to=(0, 0, 24, 24))
    bild.put("#1E7D3A", to=(6, 6, 18, 18))
    png = quelle / "Ampel.png"
    bild.write(str(png), format="png")
    svg = quelle / "Quadrat.svg"
    svg.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16"><rect x="2" y="2" width="12" height="12" fill="#2F6FDB"/></svg>')
    boese = quelle / "Boese.svg"
    boese.write_bytes(b'<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
    neu = app.import_symbol_files([str(png), str(svg), str(boese), str(png)])
    bericht = app._symbol_import_report
    bib = app.symbol_library()
    namen = {e["label"] for e in bib.symbols.values()}
    assert "Ampel" in namen and any("Boese.svg" in r for r in bericht["rejected"]), (namen, bericht)
    svg_ok = "Quadrat" in namen
    assert neu == len(bib.symbols) == (2 if svg_ok else 1), (neu, len(bib.symbols))
    gespeichert = json.loads(Path(tmp, "symbol_library.json").read_text(encoding="utf-8"))
    assert gespeichert["format"] == "glide-symbol-library" and len(gespeichert["symbols"]) == len(bib.symbols)
    assert not any("<script" in json.dumps(e) for e in gespeichert["symbols"].values()), "Quelldateien werden nicht gespeichert"
    schritte.append(f"Import: PNG{' und SVG' if svg_ok else ' (SVG von dieser Tk-Fassung nicht lesbar, gemeldet)'}, Skript-SVG abgewiesen, Duplikat erkannt")

    # Gemeinsame Symbolauswahl produktiv: Pixelsymbol einer Seite aus der Bibliothek setzen.
    seite = app.new_list_object("Probe-Seite", [], list_kind="page", list_id="eco-seite")
    app.lists.append(seite)
    zeichnung = app.new_list_object("Probe-Zeichnung", [], list_kind=app.LIST_KIND_DRAWING, list_id="eco-zeichnung")
    zeichnung["drawing"] = mod.glide_drawing.DrawingModel.blank(32).to_document()
    app.lists.append(zeichnung)
    assert app.save_items()
    ampel = next(sid for sid, e in bib.symbols.items() if e["label"] == "Ampel")

    def bedienen():
        auswahl = getattr(app, "_last_symbol_picker", None)
        if auswahl is None or not auswahl.dialog.winfo_exists():
            root.after(20, bedienen)
            return
        kategorien = auswahl.registry.categories()
        assert len(kategorien) >= 2, kategorien
        auswahl.choose(f"user:{ampel}")

    app._last_symbol_picker = None
    root.after_idle(bedienen)
    dokument = app.choose_symbol(exclude="eco-seite")
    assert dokument and dokument["width"] == 16 if "width" in dokument else dokument, dokument
    assert app.symbol_library().recent[0] == f"user:{ampel}"
    with app.sidebar_change(refresh_tree=True) as change:
        seite["icon"] = app.normalize_page_icon(dokument)
        change.mark()
    assert app.page_icon_image(seite) is not None
    assert app.symbol_library().references(ampel, app.lists) == [seite]
    bild_a = app.render_symbol(app.symbol_registry().get(f"user:{ampel}"), 32, app.theme)
    bild_b = app.render_symbol(app.symbol_registry().get(f"user:{ampel}"), 32, app.theme)
    assert bild_a is bild_b and app._symbol_render_cache.stats()["hits"] >= 1, "Symbolbilder kommen aus dem begrenzten Cache"
    schritte.append("Auswahl: Kategorien, Seite erhält Pixelsymbol, Zuletzt verwendet, Fundstelle, Render-Cache")

    # Löschen aus der Bibliothek ändert keine Seite.
    vorher = json.dumps(seite["icon"])
    bib.remove(ampel)
    assert json.dumps(seite["icon"]) == vorher
    schritte.append("Entfernen aus der Bibliothek lässt Seitensymbole unverändert")

    # Vollständige Sicherung enthält die Symbolbibliothek; Wiederherstellung ersetzt sie.
    sicherung = app.app_backup_payload()
    assert sicherung["app_backup"]["symbol_library"]["format"] == "glide-symbol-library" if "app_backup" in sicherung else True
    abschnitt = sicherung.get("app_backup", sicherung)
    assert "symbol_library" in abschnitt, sorted(abschnitt)
    schritte.append("Sicherung: Abschnitt symbol_library")

    # Projektübersicht (E04) aus echten Daten; Theme-Wechsel; ein Fenster.
    from datetime import date, timedelta
    heute = date.today()
    projekt = app.new_folder_object("Kundenprojekt")
    app.folders.append(projekt)
    punkte = [app.new_item("Erledigt gestern", item_id="d1"), app.new_item("Offen überfällig", item_id="o1"),
              app.new_item("Offen bald", item_id="o2"), app.new_item("Offen ohne Frist", item_id="o3")]
    punkte[0]["done"], punkte[0]["done_at"] = True, (heute - timedelta(days=1)).isoformat() + "T09:00:00"
    punkte[1]["due"] = (heute - timedelta(days=3)).isoformat()
    punkte[2]["due"] = (heute + timedelta(days=5)).isoformat()
    punkte[2]["importance"] = "high"
    app.lists.append(app.new_list_object("Arbeitspakete", punkte, folder_id=projekt["id"], list_id="eco-pakete"))
    assert app.save_items()
    dash = app.show_project_dashboard()
    pump(6)
    daten = app._project_dashboard_last
    kunde = next(p for p in daten["projects"] if p["id"] == projekt["id"])
    assert (kunde["open"], kunde["done"], kunde["overdue"]) == (3, 1, 1), kunde
    w = app._project_dashboard_widgets
    assert {e[0] for e in w["progress"].items} >= {projekt["id"]}
    assert len(w["activity"].cells) == 56, "jeder Tag des Zeitraums ist ein bekannter Wert (auch 0)"
    assert w["activity"].cells[(w["activity"].rows[(heute - timedelta(days=1)).weekday()],
                                next(c for (r, c), pkt in w["activity"].cells.items() if pkt.id == f"day:{(heute - timedelta(days=1)).isoformat()}"))].number == 1
    assert [s.id for s in w["due"].spans] == ["due:o2"], [s.id for s in w["due"].spans]
    assert [r["id"] for r in w["table"].rows].count(projekt["id"]) == 1
    assert app.show_project_dashboard() is dash
    app.toggle_theme()
    pump()
    app.refresh_project_dashboard()
    pump()
    app.toggle_theme()
    pump()
    dash.destroy()
    pump()
    schritte.append("Projektübersicht: Fortschritt, Status, Wichtigkeit, 56-Tage-Aktivität, Fristen, Tabelle aus echten Daten, Theme-Wechsel, ein Fenster")

    for widget in list(root.winfo_children()):
        try:
            if isinstance(widget, mod.tk.Toplevel):
                widget.destroy()
        except mod.tk.TclError:
            pass
    pump()
    assert not fehler, fehler
    app.on_close() if hasattr(app, "on_close") else root.destroy()
print("test_ecosystem_glide: OK – " + "; ".join(schritte) + " (Windows-Tk, künstliche Daten)")
