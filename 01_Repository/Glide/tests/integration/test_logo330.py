"""Logo, Lupe und Programmsymbol (Auftrag vom 29.09.2026).

- Das Logo kommt aus den SVG-Mastern in `resources/logo` und trägt die
  Akzentfarbe der Oberfläche; ohne SVG (Tk 8.6) wird es als Fläche gezeichnet.
- In der Kopfzeile steht es ab der ersten Breitenstufe links neben Titel und
  Unterzeile und rückt beide nach rechts; bei schmalem Fenster weicht es.
- Es steht in jeder Ansicht an derselben Stelle, „Über Glide“ zeigt es groß.
- Fenster, Dock und Taskleiste tragen das App-Symbol.
- Die Lupe in der Kopfzeile öffnet die Suche über Seiten, Punkte und Aktionen.
"""
import importlib.machinery
import importlib.util
import os
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True

with tempfile.TemporaryDirectory(prefix="glide-logo-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup") as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_logo_test", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    logo = mod.glide_logo

    # --- Modul: Master, Geometrie, Einfärben -------------------------------
    for name in (logo.LOGO_FILE, logo.ICON_FILE, logo.LOGO_PNG, logo.ICON_PNG):
        assert Path(logo.resource_dir(), name).is_file(), name
    svg = logo.read_svg()
    assert logo.MASTER_FILL in svg, "Der Logo-Master ist einfarbig in Glide-Blau"
    tinted_svg = logo.tinted(svg, "#123456")
    assert logo.MASTER_FILL not in tinted_svg and ('fill="#123456"' in tinted_svg or "fill: #123456" in tinted_svg)
    for falsch in ("rot", "#12345", "", None):
        try:
            logo.tinted(svg, falsch)
        except ValueError:
            pass
        else:
            raise AssertionError(f"ungültige Farbe angenommen: {falsch!r}")
    x, y, breite, hoehe = logo.bounding_box()
    assert 220 < x < 240 and 100 < y < 120 and 390 < breite < 420 and 600 < hoehe < 630, (x, y, breite, hoehe)
    assert 0.6 < logo.aspect() < 0.7
    assert 'viewBox="' in logo.cropped_svg(svg, (x, y, breite, hoehe))
    assert logo.icon_margin("darwin") > 0 and logo.icon_margin("win32") == 0 and logo.icon_margin("linux") == 0
    # Kein Master darf Entitäten mitbringen.
    logo.read_svg.cache_clear()
    logo.outline.cache_clear()
    echt = logo.read_svg
    logo.read_svg = lambda name=logo.LOGO_FILE: '<!DOCTYPE svg [<!ENTITY a "x">]><svg/>'
    try:
        logo.outline("probe.svg")
    except ValueError:
        pass
    else:
        raise AssertionError("Entitäten im SVG angenommen")
    finally:
        logo.read_svg = echt
    # Relative Pfadbefehle und H/V gehören zum Leser, auch wenn die Master sie nicht nutzen.
    teile = logo.subpaths("M10 10 h5 v5 l-5 0 Z m20 0 L30 30 c1 1 2 2 3 3 z")
    assert teile[0][:4] == [(10, 10), (15, 10), (15, 15), (10, 15)] and teile[1][0] == (30, 10), teile

    root = mod.tk.Tk()
    root.geometry("1280x860+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe(runden=10):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    def lage(widget):
        if not widget.winfo_ismapped():
            return None
        return (widget.winfo_rootx() - root.winfo_rootx(), widget.winfo_rooty() - root.winfo_rooty(),
                widget.winfo_width(), widget.winfo_height())

    def logo_farbe(leinwand):
        """Farbe eines deckenden Pixels mitten im Zeichen – aus dem Bild oder dem Polygon."""
        bild = getattr(leinwand, "_logo_image", None)
        if bild is not None:
            for yy in range(bild.height() // 4, bild.height() // 2):
                xx = bild.width() // 2
                if not bild.transparency_get(xx, yy):
                    return "#%02X%02X%02X" % bild.get(xx, yy)
            raise AssertionError("kein deckendes Pixel im Logo")
        return leinwand.itemcget(leinwand.find_withtag("logo")[0], "fill").upper()

    def nahe(farbe, soll, toleranz=3):
        a = [int(farbe[i:i + 2], 16) for i in (1, 3, 5)]
        b = [int(soll[i:i + 2], 16) for i in (1, 3, 5)]
        return all(abs(p - q) <= toleranz for p, q in zip(a, b))

    try:
        ruhe()
        svg_da = logo.has_svg(root)
        if svg_da:
            rendered = logo.logo_photo(root, 80, "#123456")
            # The new g has a transparent inner opening; its center must stay empty.
            bx, by, _bw, bh = logo.bounding_box()
            assert rendered.transparency_get(round((410 - bx) * 80 / bh), round((280 - by) * 80 / bh))
        # --- Programmsymbol ---------------------------------------------------
        assert getattr(root, "_glide_icons", None), "Fenster trägt das App-Symbol"
        assert [bild.width() for bild in root._glide_icons] == [256, 64, 32, 16] or not svg_da
        klein = app.app_icon_photo(16)
        assert klein.width() == 16 and klein.height() == 16

        # --- Kopfzeile bei breitem Fenster ------------------------------------
        app.set_home_view()
        ruhe(14)
        assert app.header_density() != "minimal"
        zeichen, titel = lage(app.header_logo), lage(app.title_label)
        assert zeichen and titel, (zeichen, titel)
        assert zeichen[0] == lage(app.sidebar_shell)[0], "Logo auf der Flucht der Seitenleiste"
        assert zeichen[0] + zeichen[2] + app.HEADER_LOGO_GAP <= titel[0], "Titel rückt nach rechts"
        assert zeichen[3] == app.header_logo_height() and zeichen[3] >= 40, zeichen
        assert zeichen[1] + zeichen[3] <= lage(app.header_frame)[1] + app.header_frame.winfo_height(), \
            "Logo bleibt in der Kopfzeile"
        assert nahe(logo_farbe(app.header_logo), app.header_logo_color()), (logo_farbe(app.header_logo),
                                                                           app.header_logo_color())
        assert mod.contrast_ratio(app.header_logo_color(), app.theme["bg"]) >= 3.0

        # Fest in jeder Ansicht.
        normal = max((eintrag for eintrag in app.lists if eintrag.get("list_kind", "tasks") == "tasks"
                      and not app.is_inbox_list(eintrag)), key=lambda eintrag: len(eintrag.get("items", [])))
        seite = app.new_page_from_markdown("# Bericht\n\nText")
        zeichnung = app.new_list_object("Zeichnung", [], list_kind="drawing")
        app.lists.append(zeichnung)
        app.save_items()
        for oeffnen in (lambda: app.set_active_list(normal["id"]), app.open_board_view, app.open_list_view,
                        lambda: app.set_active_list(seite["id"]), lambda: app.set_active_list(zeichnung["id"]),
                        app.set_today_view, app.set_trash_view, app.set_home_view):
            oeffnen()
            ruhe()
            assert lage(app.header_logo) == zeichen, ("Logo verschoben", lage(app.header_logo), zeichen)

        # Akzentfarbe wechseln: das Logo folgt.
        vorher = app.header_logo_color()
        for schluessel in ("green", "orange", "muted"):
            if schluessel == app.settings.get("accent_color"):
                continue
            app.settings["accent_color"] = schluessel
            app.apply_theme()
            ruhe()
            if app.header_logo_color() != vorher:
                break
        assert app.header_logo_color() != vorher, "andere Akzentfarbe"
        assert nahe(logo_farbe(app.header_logo), app.header_logo_color())

        # Designs: Logo überall lesbar (3:1) und in der Akzentfarbe.
        for design in ("light", "glass_dark", "contrast_dark", "minimal_light", "pixel"):
            if design not in app.DESIGNS:
                continue
            app.set_design(design)
            ruhe()
            assert mod.contrast_ratio(app.header_logo_color(), app.theme["bg"]) >= 3.0, design
            assert nahe(logo_farbe(app.header_logo), app.header_logo_color()), design

        # --- Schmales Fenster: Logo weicht, Titel an den Rand --------------------
        root.geometry("940x800+0+30")
        ruhe(16)
        assert app.header_density() == "minimal"
        assert not app.header_logo.winfo_ismapped()
        assert lage(app.title_label)[0] == lage(app.sidebar_shell)[0], "Titel wieder am Rand"
        assert app.search_button.winfo_ismapped(), "Die Lupe bleibt auch schmal"
        root.geometry("860x700+0+30")
        ruhe(16)
        assert not app.header_logo.winfo_ismapped() and app.search_button.winfo_ismapped()
        root.geometry("1280x860+0+30")
        ruhe(16)
        assert app.header_logo.winfo_ismapped() and lage(app.header_logo)[0] == zeichen[0]

        # --- Rückfall ohne SVG (Tk 8.6): gezeichnete Fläche --------------------
        leinwand = mod.tk.Canvas(root)
        echt_svg = logo.has_svg
        logo.has_svg = lambda master: False
        try:
            assert logo.logo_photo(leinwand, 40) is None
            breite = app.draw_logo(leinwand, 50, "#AB12CD")
            flaechen = leinwand.find_withtag("logo")
            assert flaechen and leinwand.type(flaechen[0]) == "polygon", flaechen
            assert leinwand.itemcget(flaechen[0], "fill").upper() == "#AB12CD"
            box = leinwand.bbox("logo")
            assert abs((box[3] - box[1]) - 50) <= 2 and abs((box[2] - box[0]) - breite) <= 2, (box, breite)
            png_symbole = logo.icon_photos(root, (32,))
            assert png_symbole and png_symbole[0].width() <= 40, "App-Symbol aus dem PNG"
        finally:
            logo.has_svg = echt_svg
            leinwand.destroy()

        # --- „Über Glide“ mit Logo --------------------------------------------
        gesehen = {}

        def pruefen(dialog, *args, **kwargs):
            dialog.update_idletasks()
            zeichen_dialog = None
            for kind in dialog.winfo_children():
                stapel = [kind]
                while stapel:
                    widget = stapel.pop()
                    stapel.extend(widget.winfo_children())
                    if widget.winfo_name() == "about_logo":
                        zeichen_dialog = widget
            gesehen["logo"] = zeichen_dialog
            gesehen["farbe"] = logo_farbe(zeichen_dialog) if zeichen_dialog is not None else None
            dialog.destroy()

        echt_modal = app.run_modal
        app.run_modal = pruefen
        try:
            app.show_about_dialog()
        finally:
            app.run_modal = echt_modal
        assert gesehen.get("logo") is not None, "Logo in „Über Glide“"
        assert nahe(gesehen["farbe"], app.header_logo_color())

        # Klick auf das Logo öffnet „Über Glide“.
        geoeffnet = []
        echt_about = app.show_about_dialog
        app.show_about_dialog = lambda: geoeffnet.append(True)
        try:
            app.header_logo.event_generate("<Button-1>", x=5, y=5)
            ruhe()
        finally:
            app.show_about_dialog = echt_about
        assert geoeffnet, "Klick auf das Logo"

        # --- Lupe: globale Suche ----------------------------------------------
        assert app.ICONS["search"] == "⌕" and app.search_button.text == app.ICONS["search"]
        reihe = [str(knopf) for knopf in app.header_controls.pack_slaves()]
        assert reihe.index(str(app.search_button)) == reihe.index(str(app.actions_button)) + 1, \
            "Lupe links neben ⌘"
        app.search_button.command()
        ruhe()
        assert getattr(app, "_quick_open", None) is not None, "Lupe öffnet die Suche"
        app.search_button.command()
        ruhe()
        assert getattr(app, "_quick_open", None) is None, "zweiter Klick schließt sie"
        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("test_logo330: OK; Logo-Master einfarbig und einfärbbar, Logo links neben Titel ab der ersten "
      "Breitenstufe, fest in acht Ansichten, Akzentfarbe in fünf Designs, Rückfall ohne SVG, "
      "„Über Glide“, Programmsymbol und Lupe.")
