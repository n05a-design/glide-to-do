"""Hintergrundverläufe (26.09.2026): Generator, Auswahl je Design, Einbau, Lesbarkeit.

Glide legt auf Wunsch einen Mesh-, Aurora- oder Pixelverlauf hinter die
Oberfläche – fünf Entwürfe je Design. Tk kennt keine Transparenz; der Verlauf
erscheint, weil jede Fläche in der Grundfarbe ihren Ausschnitt selbst zeichnet.
Die Suite prüft Generator und Einbau ohne Bildschirmaufnahme.
"""
import importlib.machinery
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import textwrap
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "src/glide"))
sys.dont_write_bytecode = True
import backdrop  # noqa: E402

# --- Generator ---------------------------------------------------------------
designs = ("light", "dark", "glass_light", "glass_dark", "minimal_light", "minimal_dark",
           "dopamine", "pixel", "contrast_light", "contrast_dark")
assert set(backdrop.PRESETS) == set(designs)
for design in designs:
    presets = backdrop.presets_for(design)
    assert len(presets) == 5, design
    assert len({preset.key for preset in presets}) == 5, design
    assert all(preset.key != backdrop.NONE_KEY and preset.name and preset.description for preset in presets)
eins = backdrop.render(backdrop.PRESETS["dark"][0], 40, 24, "#111113")
assert eins == backdrop.render(backdrop.PRESETS["dark"][0], 40, 24, "#111113"), "reproduzierbar"
assert backdrop.decode_png(backdrop.encode_png(eins, 40, 24)) == (eins, 40, 24)
rgb, breite, hoehe, faktor = backdrop.render_scaled(backdrop.find_preset("pixel", "plasma"), 320, 200, "#0D0D12")
assert faktor == 16 and breite == 20 and hoehe == 13, (faktor, breite, hoehe)
# Lesezone: Oben trägt die Schrift, darunter darf der Verlauf voll leuchten.
preset = backdrop.find_preset("glass_dark", "sonnenwind")
zone_staerke = backdrop.fit_intensity(preset, "#16181D", ["#F5F5F7", "#A1A1A6"], rows=(0.0, 0.2))
assert 0.0 <= zone_staerke <= preset.intensity
daten = backdrop.render(preset, 60, 40, "#16181D", zone=(0.2, zone_staerke, 0.1), seed=3)
for index in range(0, 60 * 8 * 3, 3):  # obere 20 %
    punkt = tuple(daten[index:index + 3])
    for delta in (preset.grain, -preset.grain):
        probe = tuple(max(0, min(255, kanal + delta)) for kanal in punkt)
        assert backdrop.contrast(backdrop.hex_rgb("#A1A1A6"), probe) >= 4.5 - 0.05, probe
assert backdrop.zone_intensity_at(0.1, 1.0, (0.2, 0.3, 0.1)) == 0.3
assert backdrop.zone_intensity_at(0.5, 1.0, (0.2, 0.3, 0.1)) == 1.0

# --- Einbau in Glide ---------------------------------------------------------
with tempfile.TemporaryDirectory(prefix="glide-hintergrund-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_hintergrund", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1280x800+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    try:
        normal = next(entry for entry in app.lists
                      if entry.get("list_kind") in (None, "", "list", "tasks") and len(entry.get("items", [])) > 5)
        app.set_active_list(normal["id"])
        ruhe()
        # Ohne Wahl: kein Verlauf, keine Flächen.
        assert app.backdrop_choice() == backdrop.NONE_KEY and not getattr(app, "_backdrop", None)
        assert not getattr(app, "_backdrop_surfaces", set())

        for design, wahl in (("glass_dark", "sonnenwind"), ("light", "herbstlicht"), ("pixel", "abendrot")):
            app.set_design(design)
            roh_karte = app._compose_theme()["card"]
            app.set_backdrop_choice(wahl)
            verlauf = app.wait_for_backdrop(60)
            ruhe()
            app.sync_backdrop_surfaces()
            ruhe()
            assert verlauf and verlauf["design"] == design, design
            assert app.settings["backdrops"][design] == wahl
            cache = Path(ordner, "cache", "hintergrund")
            assert any(cache.glob("*.png")), "Zwischenspeicher im Testordner, nicht im System-Cache"
            flaechen = app._backdrop_surfaces
            # Das Hauptfenster zeigt den Verlauf in seinem Rand – als Stücke nur
            # dort, wo kein Kind liegt (26.09.2026: sichtbare Teile statt ganzer
            # Ausschnitte, auf der Startseite vorher rund siebenfach übereinander).
            sichtbar = [e for e in app.root._backdrop_labels if e.winfo_ismapped()]
            assert app.root in flaechen and sichtbar, "Rand des Hauptfensters"
            assert app.title_label in flaechen and app.title_label.find_withtag("backdrop")
            knoepfe = [w for w in flaechen if isinstance(w, mod.RoundedButton)]
            assert knoepfe and all(w.find_withtag("backdrop") for w in knoepfe)
            # Jedes Stück eines Rahmens liegt innerhalb des Rahmens (bis auf die
            # Rundung auf ganze Rechenpunkte), und die Summe bleibt klein.
            faktor = verlauf["factor"]
            flaeche = 0
            for rahmen in (w for w in flaechen if isinstance(w, mod.tk.Frame)):
                for etikett in rahmen._backdrop_labels:
                    if not etikett.winfo_ismapped():
                        continue
                    info = etikett.place_info()
                    foto = etikett.cget("image")
                    breite = int(root.tk.call("image", "width", foto))
                    hoehe = int(root.tk.call("image", "height", foto))
                    flaeche += breite * hoehe
                    assert int(info["x"]) > -faktor and int(info["x"]) + breite <= rahmen.winfo_width() + faktor, rahmen
                    # Hintergrundbilder reichen nur Mausereignisse weiter – mit dem
                    # Bindtag des Rahmens bekam der Rahmen auch deren <Configure>.
                    assert etikett.bindtags() == (app.BACKDROP_BINDTAG,), rahmen
            assert flaeche < root.winfo_width() * root.winfo_height(), ("Überzeichnung", flaeche)
            # Das Bild liegt nur in Rechenauflösung im Speicher.
            assert verlauf["image"].width() * faktor >= root.winfo_screenwidth() - faktor
            assert verlauf["image"].width() <= root.winfo_screenwidth()
            # Schrift auf dem Verlauf bleibt lesbar: zuerst weicht die Schrift
            # im eigenen Farbton aus, die Pille ist nur der letzte Ausweg.
            for beschriftung in (w for w in flaechen if isinstance(w, mod.CanvasLabel)):
                x = beschriftung.winfo_rootx() - root.winfo_rootx()
                y = beschriftung.winfo_rooty() - root.winfo_rooty()
                punkte = app.backdrop_extremes(beschriftung, x, y, verlauf)
                if beschriftung._halo:
                    assert mod.contrast_ratio(beschriftung.cget("fg"), beschriftung._halo) >= 4.5
                    continue
                schrift = beschriftung._fg_override or beschriftung.cget("fg")
                assert all(mod.contrast_ratio(schrift, punkt) >= 4.5 - 0.05 for punkt in punkte), \
                    (design, str(beschriftung), schrift, punkte)
            # Milchglas je Kachel: Karte, Liste und Beschriftungen tragen dieselbe
            # Tönung, und die Schrift hält darauf 4,5:1.
            if design != "contrast_dark":
                karte = app.list_frame_outer
                assert karte in app._frosted_cards and karte.fill_color == karte._frost, design
                assert karte._frost.lower() != app.theme["card"].lower(), "Tönung erwartet"
                for rolle in ("text", "muted"):
                    assert mod.contrast_ratio(app.theme[rolle], karte._frost) >= 4.5, (design, rolle)
                assert str(app.tree.cget("style")).startswith("Frost"), app.tree.cget("style")
                assert app.style.lookup(app.tree.cget("style"), "background").lower() == karte._frost.lower()
                reste = []
                stapel = [karte.inner]
                while stapel:
                    w = stapel.pop()
                    stapel.extend(k for k in w.winfo_children() if not isinstance(k, mod.RoundedContainer))
                    try:
                        if str(w.cget("bg")).lower() == app.theme["card"].lower():
                            reste.append(str(w))
                    except mod.tk.TclError:
                        pass
                assert not reste, ("ungetönte Flächen in der Karte", reste[:3])
            # Der Glanz der Glas-Kacheln bleibt im oberen Innenrand.
            if design.startswith("glass"):
                for kachel in app.rounded_containers:
                    for element in kachel.find_withtag("surface"):
                        if kachel.type(element) == "rectangle":
                            assert kachel.coords(element)[3] <= kachel.inner_pad_y + 3, str(kachel)
            if design.startswith("glass"):
                assert app.theme["card"] != roh_karte, "Glas nimmt die Verlaufsfarbe auf"
            assert not fehler, (design, fehler[:1])

        # Fenster haben einen statischen, zum Verlauf passenden Grund: Das Design
        # nimmt dessen Farbe auf; nachträglich umgefärbt wird nichts (das ließ
        # Tk im Punktdialog endlos neu anordnen).
        roh = app._compose_theme()
        assert app.theme["bg"].lower() != roh["bg"].lower(), "Grund folgt dem Verlauf"
        assert mod.contrast_ratio(app.theme["text"], app.theme["bg"]) >= 4.5
        assert not hasattr(app, "frost_window")

        # Menü: sechs Einträge, gewählter mit Häkchen, in der Aktionssuche richtig eingeordnet.
        eintraege = [app.backdrop_menu.entrycget(i, "label") for i in range(app.backdrop_menu.index("end") + 1)]
        assert len(eintraege) == 6 and eintraege[0] == "Hintergrund: aus", eintraege
        assert app.backdrop_menu.entrycget(eintraege.index("Hintergrund: 8-Bit-Abend"), "accelerator") == "✓"
        aktionen = [a for a in app.app_action_entries() if a["label"].startswith("Hintergrund: ")]
        assert len(aktionen) == 6 and all(a["group"] == "Ansichtseinstellungen" for a in aktionen)
        # Wieder aufgebaut kommt das Bild aus dem Zwischenspeicher – ohne Rechnen.
        app._backdrop_key = None
        app._backdrop = None
        app.refresh_backdrop()
        assert app._backdrop and app._backdrop["key"] == app._backdrop_key, "sofort aus dem Zwischenspeicher"
        # Abschalten räumt alles ab.
        app.set_backdrop_choice(backdrop.NONE_KEY)
        ruhe()
        app.sync_backdrop_surfaces()
        ruhe()
        assert not app._backdrop and not app._backdrop_surfaces
        assert not app._frosted_cards and app.list_frame_outer.fill_color == app.theme["card"]
        assert not str(app.tree.cget("style")).startswith("Frost")
        assert not [e for e in (getattr(app.root, "_backdrop_labels", None) or []) if e.winfo_exists()]
        assert not app.title_label.find_withtag("backdrop")
        assert "pixel" not in app.settings["backdrops"]
        # Unbekannte Werte fallen beim Laden weg.
        bereinigt = app.normalize_personal_settings({"backdrops": {"dark": "aurora", "light": "gibtsnicht",
                                                                   "fremd": "aurora", "pixel": 3}})
        assert bereinigt["backdrops"] == {"dark": "aurora"}, bereinigt["backdrops"]
        # Die Auswahl in den Einstellungen: „Aus“ und fünf Vorschauen je Design.
        gesehen = {}

        original_modal = app.run_modal
        def messen(self, dialog, parent=None):
            def zaehlen():
                try:
                    rahmen = self._backdrop_choice_frame
                    gesehen["kacheln"] = sum(1 for zelle in rahmen.winfo_children() for kind in zelle.winfo_children()
                                             if isinstance(kind, mod.tk.Canvas))
                finally:
                    dialog.destroy()
            def sichtbar_machen():
                try:
                    rahmen = self._backdrop_choice_frame
                    canvas = rahmen.master
                    while not isinstance(canvas, mod.tk.Canvas):
                        canvas = canvas.master
                    bbox = canvas.bbox("all")
                    top = rahmen.winfo_rooty() - canvas.winfo_rooty() + canvas.canvasy(0)
                    canvas.yview_moveto(max(0, (top - 12) / (bbox[3] - bbox[1])))
                    # Der Abschnitt muss wie bei echter Bedienung sichtbar
                    # werden; die ursprünglichen sechs Vorschauen bleiben Pflicht.
                    root.after(30, zaehlen)
                except Exception:
                    dialog.destroy()
                    raise
            root.after(30, sichtbar_machen)
            return original_modal(dialog, parent)

        mod.ListApp.run_modal = messen
        app.show_settings_dialog()
        assert gesehen.get("kacheln") == 6, gesehen
        assert not fehler, fehler[:1]
    finally:
        root.destroy()

# --- Absturz vom 26.09.2026 --------------------------------------------------
# Start im schmalen Fenster (860 × 1042) auf der Startseite mit Verlauf: Tk
# stürzte ab, weil die Hintergrundbilder das Bindtag ihres Rahmens trugen.
# Ein nativer Absturz lässt sich nur in einem eigenen Prozess beobachten.
with tempfile.TemporaryDirectory(prefix="glide-hintergrund-start-") as ordner:
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    Path(ordner, "settings.json").write_text(json.dumps({
        "settings_version": 2, "design": "glass_light", "view_mode": "home",
        "backdrops": {"glass_light": "iris"}}), encoding="utf-8")
    Path(ordner, "window.conf").write_text("860x1042+0+38", encoding="utf-8")
    skript = textwrap.dedent(f"""
        import importlib.machinery, importlib.util, sys
        sys.dont_write_bytecode = True
        loader = importlib.machinery.SourceFileLoader("glide_start", {str(REPO / "src/glide/app.pyw")!r})
        spec = importlib.util.spec_from_loader(loader.name, loader)
        mod = importlib.util.module_from_spec(spec)
        loader.exec_module(mod)
        root = mod.tk.Tk()
        app = mod.ListApp(root)
        root.after(5000, root.destroy)
        root.mainloop()
        print("gestartet")
    """)
    umgebung = dict(os.environ, GLIDE_DATA_DIR=ordner)
    umgebung.pop("GLIDE_TEST_MODE", None)
    lauf = subprocess.run([sys.executable, "-c", skript], env=umgebung, capture_output=True, text=True, timeout=180)
    assert lauf.returncode == 0 and "gestartet" in lauf.stdout, (lauf.returncode, lauf.stderr[-1500:])

print("test_hintergrund330: OK; 50 Entwürfe, Lesezone, Einbau in drei Designs, Schrift statt Pille, "
      "Milchglas für Kacheln, Listen und Fenster, Menü, Zwischenspeicher, Abschalten, Auswahl in den "
      "Einstellungen und Start im schmalen Fenster ohne Absturz geprüft.")
