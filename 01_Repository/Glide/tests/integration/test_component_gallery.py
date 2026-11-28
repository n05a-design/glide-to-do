# SPDX-License-Identifier: MPL-2.0
"""Komponenten-Galerie in Glide (D105, Master-Serie Teil 02) über den echten Einstieg.

Geprüft wird an der laufenden App mit künstlichen Daten in einem temporären
GLIDE_DATA_DIR:

- Erreichbarkeit: Hilfe › „Komponenten-Galerie …“ ruft `show_component_gallery`.
- Vollständigkeit: jede erwartete Shell- und Bento-Komponente ist gebaut, keine
  Vorführung schlägt fehl.
- Echte Implementierung: die Widgets sind Instanzen der Klassen aus
  `glide_shell.custom_controls` bzw. `glide_bento` – keine Kopien.
- Interaktion: Hover und Leertaste an einem GlideCheckbutton, Auswahl im
  GlideListbox, Regler bewegt.
- Design: Wechsel Aktiv/Hell/Dunkel baut neu auf, die Bento-Karte trägt die
  Kartenfarbe der gewählten Tabelle.
- Breite: schmal/breit ändert die Spaltenzahl des echten BentoGrid.
- Abbau: Schließen gibt den Zustand frei; Daten-, Einstellungs- und
  Vorlagendateien bleiben bytegleich.

--app wählt den Quellstand (Gegenprobe gegen einen Stand ohne Galerie).
"""
import argparse
import hashlib
import importlib.machinery
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import time
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser()
parser.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
args = parser.parse_args()
sys.path.insert(0, str(args.app.parent))
sys.dont_write_bytecode = True


def hashes(ordner):
    ergebnis = {}
    for pfad in sorted(Path(ordner).rglob("*")):
        if pfad.is_file() and pfad.suffix in (".json", ".glidetemplates") and "backup" not in pfad.name.lower():
            ergebnis[str(pfad.relative_to(ordner))] = hashlib.sha256(pfad.read_bytes()).hexdigest()
    return ergebnis


with tempfile.TemporaryDirectory(prefix="glide-galerie-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_galerie_test", str(args.app))
    mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    sys.modules[loader.name] = mod
    loader.exec_module(mod)
    mod.ListApp.system_is_dark = lambda self: False
    import glide_bento
    from glide_shell import custom_controls

    fehler = []
    root = mod.tk.Tk()
    root.geometry("1280x840+20+20")
    root.report_callback_exception = lambda *exc: fehler.append(repr(exc[1]))
    app = mod.ListApp(root)
    app.show_error = lambda *a, **k: fehler.append(repr(a))
    pruefungen = []

    def ruhe(sekunden=0.15):
        ende = time.perf_counter() + sekunden
        while time.perf_counter() < ende:
            root.update()

    def finde(widget, klasse):
        if isinstance(widget, klasse):
            return widget
        for kind in widget.winfo_children():
            treffer = finde(kind, klasse)
            if treffer is not None:
                return treffer
        return None

    try:
        ruhe(0.3)
        app.save_items()
        vorher = hashes(ordner)
        assert vorher, "keine Datendateien zum Vergleich"

        hilfe = [eintrag for titel, eintraege in app.menubar_structure() if titel == mod.glide_i18n.t("menu.help", "Hilfe")
                 for eintrag in eintraege if eintrag]
        assert any(e[1] == app.show_component_gallery for e in hilfe), "Hilfe-Menü ohne Komponenten-Galerie"
        pruefungen.append("Hilfe-Menü führt zur Galerie")

        def in_galerie(dialog, *a, **k):
            zustand = app._component_gallery
            assert zustand and zustand["dialog"] is dialog
            # E05: schrittweiser Aufbau – beim Öffnen steht nur der erste Stapel, der Rest folgt im Leerlauf.
            gesamt = len(zustand["expected"])
            assert 0 < len(zustand["widgets"]) <= app.COMPONENT_GALLERY_FIRST_BATCH < gesamt, (len(zustand["widgets"]), gesamt)
            dialog.geometry("1100x800+30+30")
            ruhe(0.4)
            assert app.finish_component_gallery() == gesamt
            erwartet = mod.glide_component_gallery.expected_components()
            assert set(zustand["widgets"]) == set(erwartet), set(erwartet) - set(zustand["widgets"])
            assert not zustand["failures"], zustand["failures"]
            assert not mod.glide_component_gallery.registry_problems(zustand["registry"])
            pruefungen.append(f"{len(erwartet)} Komponenten gebaut, keine Vorführung fehlgeschlagen")

            w = zustand["widgets"]
            assert isinstance(w["shell.canvas_label"], custom_controls.CanvasLabel)
            assert isinstance(w["shell.listbox"], custom_controls.GlideListbox)
            assert isinstance(w["shell.scale"], custom_controls.GlideScale)
            assert finde(w["shell.auto_scrollbar"], custom_controls.ThemedAutoScrollbar) is not None
            assert isinstance(w["bento.card"], glide_bento.BentoCard)
            assert isinstance(w["bento.metric"], glide_bento.BentoMetric)
            assert isinstance(w["bento.empty_state"], glide_bento.BentoEmptyState)
            assert isinstance(w["bento.grid"], glide_bento.BentoGrid)
            pruefungen.append("Widgets sind Instanzen der echten Shell-/Bento-Klassen")

            knopf = finde(w["shell.checkbutton"], custom_controls.GlideCheckbutton)
            wert = knopf._showcase_variable.get()
            knopf.event_generate("<Enter>")
            ruhe(0.05)
            assert knopf._hovered, "Hover nicht erkannt"
            knopf.focus_force()
            ruhe(0.05)
            knopf.event_generate("<space>")
            ruhe(0.05)
            assert knopf._showcase_variable.get() != wert, "Leertaste schaltet nicht"
            w["shell.listbox"].selection_clear(0, "end")
            w["shell.listbox"].selection_set(3)
            assert w["shell.listbox"].curselection() == (3,)
            w["shell.scale"]._showcase_variable.set(75)
            ruhe(0.05)
            assert w["shell.scale"].get() == 75
            pruefungen.append("Hover, Leertaste, Listenauswahl und Regler reagieren")

            karten = {}
            for wahl in ("light", "dark"):
                zustand["theme"].set(wahl)
                app.render_component_gallery()
                app.finish_component_gallery()
                ruhe(0.2)
                karte = zustand["widgets"]["bento.card"]
                karten[wahl] = karte.context.resolve_color("card_bg")
                assert karten[wahl] == app.component_gallery_palette(wahl)["card"], wahl
            assert karten["light"] != karten["dark"], karten
            zustand["theme"].set("current")
            app.render_component_gallery()
            pruefungen.append(f"Designwechsel baut neu auf (Karte hell {karten['light']}, dunkel {karten['dark']})")

            spalten = {}
            for breite in ("narrow", "wide"):
                zustand["width"].set(breite)
                app.render_component_gallery()
                app.finish_component_gallery()
                ruhe(0.4)
                spalten[breite] = zustand["widgets"]["bento.grid"].current_columns
            assert spalten["narrow"] < spalten["wide"], spalten
            pruefungen.append(f"Breite steuert das echte Raster ({spalten['narrow']} → {spalten['wide']} Spalten)")
            # Suche und Kategorie (E04): Filter über die Kompositionsbibliothek, ohne Treffer ein Hinweis.
            zustand["search"].set("heatmap")
            zustand["search"].flush()
            app.finish_component_gallery()
            assert set(zustand["widgets"]) == {"bento.viz.heatmap", "bento.viz.calendar", "bento.viz.calendar-sparse"}, set(zustand["widgets"])
            zustand["search"].set("")
            zustand["search"].flush()
            zustand["category_display"].set("Time")
            app.finish_component_gallery()
            assert {e for e in zustand["widgets"]} == {"bento.viz.timeline", "bento.viz.milestones", "bento.viz.gantt", "bento.viz.sequence"}
            zustand["search"].set("gibt-es-nicht")
            zustand["search"].flush()
            assert zustand["expected"] == [] and not zustand["widgets"]
            pruefungen.append("Suche und Kategorie filtern die Kompositionsbibliothek")
            dialog.destroy()

        with patch.object(app, "run_modal", side_effect=in_galerie):
            app.show_component_gallery()
        ruhe(0.3)
        assert getattr(app, "_component_gallery", None) is None, "Galeriezustand nach dem Schließen nicht freigegeben"
        app.save_items()
        nachher = hashes(ordner)
        assert nachher == vorher, {k for k in set(vorher) | set(nachher) if vorher.get(k) != nachher.get(k)}
        pruefungen.append("Schließen gibt frei; Daten-, Einstellungs- und Vorlagendateien unverändert")
        assert not fehler, fehler
        print("test_component_gallery: OK; " + "; ".join(pruefungen))
    finally:
        try:
            app.cancel_pending_callbacks()
            getattr(app, "finish_recovery_session", lambda: None)()
            app.release_data_lock()
        except Exception:
            pass
        try:
            root.destroy()
        except mod.tk.TclError:
            pass
