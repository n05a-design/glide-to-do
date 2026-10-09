"""Etappe 1 der Funktionsrecherche (3.32.0, 30.09.2026): schnelle Gewinne.

- G16: Zeichnung als Symbol (ICO mit 16, 32, 48, 256 Pixeln), Grund wahlweise
  durchsichtig; Verkleinern ohne Mischfarben.
- G20: Paletten aus Aseprite-Dateien und Adobe-Farbfeldern (`.ase`); alles oder
  nichts wie bei Textpaletten.
- G11: Datums-Platzhalter in Vorlagen füllen sich selbst; abgefragt wird nur der
  Rest.
- G03: Tagesabschluss als dritter Modus der Startseite, mit Rückblick in die
  Tagesnotiz.

Alle App-Teile laufen mit einem temporären `GLIDE_DATA_DIR`.
"""
import copy
import importlib.machinery
import importlib.util
import os
import struct
import sys
import tempfile
import zlib
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.dont_write_bytecode = True
sys.path.insert(0, str(REPO / "src/glide"))
import drawing as glide_drawing  # noqa: E402

# --- G16: ICO ------------------------------------------------------------------
modell = glide_drawing.DrawingModel(size=16)
rot = modell.ensure_color("#E03030")
for index in range(16):
    modell.cells[index * 16 + index] = rot
ico = modell.to_ico()
reserviert, art, anzahl = struct.unpack_from("<HHH", ico, 0)
assert (reserviert, art, anzahl) == (0, 1, 4)
groessen = []
for nummer in range(anzahl):
    breite, hoehe, _farben, _r, ebenen, bits, laenge, versatz = struct.unpack_from("<BBBBHHII", ico, 6 + 16 * nummer)
    kante = breite or 256
    assert breite == hoehe and ebenen == 1 and bits == 32
    png = ico[versatz:versatz + laenge]
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert struct.unpack(">II", png[16:24]) == (kante, kante) and png[25] == 6, "RGBA-PNG"
    groessen.append(kante)
    if kante == 32:
        # IDAT entpacken: Grund durchsichtig, Diagonale rot, keine Mischfarben.
        idat_laenge = struct.unpack(">I", png[33:37])[0]
        roh = zlib.decompress(png[41:41 + idat_laenge])
        zeile = lambda y: roh[y * (1 + 32 * 4) + 1:(y + 1) * (1 + 32 * 4)]
        assert zeile(0)[:4] == bytes((0xE0, 0x30, 0x30, 255)), "Zelle (0,0) rot, 2× vergrößert"
        assert zeile(0)[8:12] == bytes((0xFF, 0xFF, 0xFF, 0)), "Grund durchsichtig"
        farben = {bytes(zeile(y)[x:x + 4]) for y in range(32) for x in range(0, 128, 4)}
        assert farben == {bytes((0xE0, 0x30, 0x30, 255)), bytes((0xFF, 0xFF, 0xFF, 0))}, farben
assert groessen == [16, 32, 48, 256]
weiss = modell.to_ico(transparent_background=False)
assert weiss != ico
assert glide_drawing.resample_cells(4, list(range(16)), 2) == [5, 7, 13, 15]
assert glide_drawing.resample_cells(2, [1, 2, 3, 4], 4) == [1, 1, 2, 2, 1, 1, 2, 2, 3, 3, 4, 4, 3, 3, 4, 4]
gross = glide_drawing.DrawingModel(size=128)
assert gross.to_ico(sizes=(48,))[:6] == struct.pack("<HHH", 0, 1, 1), "48 aus 128 ohne Fehler"


# --- G20: Binärpaletten -------------------------------------------------------------
def aseprite(chunks, frames=1):
    rahmen = b""
    for chunk_liste in [chunks] * frames:
        inhalt = b"".join(chunk_liste)
        rahmen += struct.pack("<IHHHH", 16 + len(inhalt), 0xF1FA, len(chunk_liste), 100, 0) \
            + struct.pack("<I", len(chunk_liste)) + inhalt
    return struct.pack("<IHHHHH", 128 + len(rahmen), 0xA5E0, frames, 16, 16, 32) + b"\0" * 114 + rahmen


def chunk(art, inhalt):
    return struct.pack("<IH", 6 + len(inhalt), art) + inhalt


neu = chunk(0x2019, struct.pack("<III", 3, 0, 2) + b"\0" * 8
            + struct.pack("<HBBBB", 0, 255, 0, 0, 255)
            + struct.pack("<HBBBB", 1, 0, 128, 0, 255) + struct.pack("<H", 4) + b"Gras"
            + struct.pack("<HBBBB", 0, 9, 9, 9, 0))
assert glide_drawing.parse_binary_palette(aseprite([neu]), "Figur") == ("Figur", ["#FF0000", "#008000"])
alt = chunk(0x0004, struct.pack("<H", 1) + bytes((0, 2)) + bytes((1, 2, 3, 250, 251, 252)))
assert glide_drawing.parse_binary_palette(aseprite([alt]))[1] == ["#010203", "#FAFBFC"]
alt63 = chunk(0x0011, struct.pack("<H", 1) + bytes((0, 1)) + bytes((63, 0, 63)))
assert glide_drawing.parse_binary_palette(aseprite([alt63]))[1] == ["#FF00FF"]


def swatch(name, modell_name, werte):
    text = (name + "\0").encode("utf-16-be")
    inhalt = struct.pack(">H", len(text) // 2) + text + modell_name + werte + struct.pack(">H", 2)
    return struct.pack(">HI", 1, len(inhalt)) + inhalt


gruppe = struct.pack(">HI", 0xC001, 4) + b"\0\0\0\0"
adobe = b"ASEF" + struct.pack(">HHI", 1, 0, 4) + gruppe \
    + swatch("Blau", b"RGB ", struct.pack(">fff", 0, 0, 1)) \
    + swatch("Grau", b"Gray", struct.pack(">f", 0.5)) \
    + swatch("Schwarz", b"CMYK", struct.pack(">ffff", 0, 0, 0, 1))
assert glide_drawing.parse_binary_palette(adobe, "Adobe")[1] == ["#0000FF", "#808080", "#000000"]
for kaputt, grund in ((b"GIF89a" + b"\0" * 200, "fremde Datei"),
                      (b"ASEF" + struct.pack(">HHI", 1, 0, 1) + swatch("Lab", b"LAB ", struct.pack(">fff", 50, 0, 0)), "Lab"),
                      (aseprite([neu])[:150], "abgeschnitten")):
    try:
        glide_drawing.parse_binary_palette(kaputt)
    except glide_drawing.DrawingFormatError:
        pass
    else:
        raise AssertionError(f"muss abgelehnt werden: {grund}")

# --- App-Teile -------------------------------------------------------------------------------
with tempfile.TemporaryDirectory(prefix="glide-etappe1-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_etappe1", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.geometry("1300x900+20+20")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)

    def ruhe(runden=6):
        for _ in range(runden):
            root.update_idletasks()
            root.update()

    app = mod.ListApp(root)
    app.confirm_template_preview = lambda template: True
    try:
        ruhe()
        # G16/G20 in der Zeichnung: Menüeinträge, Export und Import über die Oberfläche.
        eintrag = app.create_new_drawing(size=16)
        app.set_active_list(eintrag if isinstance(eintrag, str) else eintrag["id"])
        ruhe()
        editor = app.drawing_editor
        editor.model.cells[0] = editor.model.ensure_color("#123456")
        editor.flush()
        ziel = os.path.join(ordner, "symbol.ico")
        mod.filedialog.asksaveasfilename = lambda **kwargs: ziel
        # Seit 3.35.0 (G-03) steht vor dem Speichern die Symbolvorschau; ihr Knopf führt weiter.
        def symbolvorschau(dialog, *args, **kwargs):
            dialog.update()
            stapel, knoepfe = [dialog], []
            while stapel:
                widget = stapel.pop()
                stapel.extend(widget.winfo_children())
                if isinstance(widget, mod.RoundedButton) and widget.text == "Exportieren":
                    knoepfe.append(widget)
            knoepfe[0].command()
        original_modal = app.run_modal
        app.run_modal = symbolvorschau
        try:
            app.drawing_export_ico(editor, True)
        finally:
            app.run_modal = original_modal
        daten = Path(ziel).read_bytes()
        assert daten[:6] == struct.pack("<HHH", 0, 1, 4), "ICO geschrieben"
        palette = os.path.join(ordner, "figur.aseprite")
        Path(palette).write_bytes(aseprite([neu]))
        mod.filedialog.askopenfilename = lambda **kwargs: palette
        app.drawing_import_palette(editor)
        paletten = app.drawing_tool_settings()["palettes"]
        assert any(p.get("name") == "figur" and p.get("colors") == ["#FF0000", "#008000"] for p in paletten), paletten
        menues = []
        original_popup = mod.tk.Menu.tk_popup
        mod.tk.Menu.tk_popup = lambda self, *args: menues.append(self)
        try:
            editor.show_more_menu()
            editor.show_palette_menu()
        finally:
            mod.tk.Menu.tk_popup = original_popup

        def alle(menu):
            for i in range(menu.index("end") + 1):
                if menu.type(i) in ("command", "cascade"):
                    yield menu.entrycget(i, "label")
                if menu.type(i) == "cascade":
                    yield from alle(root.nametowidget(menu.entrycget(i, "menu")))
        beschriftungen = list(alle(menues[-2]))
        assert "Als Symbol exportieren (ICO)" in beschriftungen, beschriftungen
        assert "Palette importieren (.gpl, .hex, .ase) …" in list(alle(menues[-1]))

        # G11: selbstfüllende Platzhalter
        heute = date.today()
        assert app.template_auto_value("Wochentag") == app.WOCHENTAGE[heute.weekday()]
        assert app.template_auto_value("KW") == str(heute.isocalendar()[1])
        assert app.template_auto_value("Morgen") == (heute + timedelta(days=1)).strftime("%d.%m.%Y")
        assert app.template_auto_value("Projektname") is None
        basis = next(t for t in app.templates if "payload" in t and t.get("kind") == "list")
        vorlage = copy.deepcopy(basis)
        vorlage["id"] = "test-platzhalter"
        vorlage["title"] = "Protokoll {{Wochentag}} KW {{KW}} – {{Projekt}}"
        app.templates.append(vorlage)
        gefragt = []
        app.ask_template_fields = lambda felder, titel="": (gefragt.append(list(felder)), {"Projekt": "Alpha"})[1]
        vorher = {entry["id"] for entry in app.lists}
        app.create_list_from_template("test-platzhalter")
        ruhe()
        neue = [entry for entry in app.lists if entry["id"] not in vorher]
        assert gefragt == [["Projekt"]], gefragt
        assert neue and neue[0]["title"] == (f"Protokoll {app.WOCHENTAGE[heute.weekday()]} KW "
                                             f"{heute.isocalendar()[1]} – Alpha"), neue[0]["title"]
        gefragt.clear()
        vorlage2 = copy.deepcopy(basis)
        vorlage2["id"] = "test-nur-datum"
        vorlage2["title"] = "Tag {{Datum}}"
        app.templates.append(vorlage2)
        app.create_list_from_template("test-nur-datum")
        assert gefragt == [], "Nur Datumsfelder: kein Dialog"

        # G03: Tagesabschluss
        liste = app.new_list_object("Abschluss", [])
        app.lists.append(liste)
        heute_iso = heute.isoformat()
        punkte = []
        for titel, geplant, erledigt in (("Bericht schreiben", heute_iso, False), ("Anruf", heute_iso, True),
                                         ("Später", None, False)):
            punkt = app.new_item(titel)
            punkt["planned_date"] = geplant
            punkt["done"] = erledigt
            if erledigt:
                punkt["done_at"] = f"{heute_iso}T17:00:00+02:00"
            punkte.append(punkt)
        liste["items"] = punkte
        app.save_items()
        schlange = app.day_close_queue()
        assert [s["item_id"] for s in schlange if s["list_id"] == liste["id"]] == [punkte[0]["id"]], schlange
        assert [punkt["text"] for punkt, eintrag in app.done_today_items() if eintrag is liste] == ["Anruf"]
        app.start_day_close()
        # Nur unsere Liste entscheiden: die Schlange auf sie begrenzen.
        app._day_review["queue"] = [s for s in app._day_review["queue"] if s["list_id"] == liste["id"]]
        ruhe()
        assert app.home_mode() == "day_close" and app.get_display_title() == "Tagesabschluss"
        app.day_review_decide("tomorrow")
        ruhe()
        assert punkte[0]["planned_date"] == (heute + timedelta(days=1)).isoformat()
        assert app._day_review["moved"] == ["Bericht schreiben"]
        notiz = app.write_day_close_note()
        ruhe()
        text = notiz["rich_note"]["text"]
        assert "Tagesabschluss" in text and "Anruf" in text and "Weitergegeben (1): Bericht schreiben" in text, text
        assert (notiz.get("journal") or {}).get("moment_date") == heute_iso
        laenge = len(text)
        app.start_day_close()
        app.write_day_close_note()
        assert len(notiz["rich_note"]["text"]) > laenge, "zweiter Abschluss hängt an dieselbe Notiz an"
        tagesnotizen = [e.get("title") for e in app.lists if e.get("list_kind") == "note"
                        and (e.get("journal") or {}).get("moment_date") == heute_iso]
        assert len(tagesnotizen) == 1, tagesnotizen
        # Hänger vom 30.09.2026: Seite mit Bildern öffnen, wechseln, Größe
        # ändern, scrollen – die Bildplatzierung darf sich nicht verschachteln.
        import traceback
        tiefe = [0]
        original_origin = mod.PageEditor.place_origin

        def messend(self):
            tiefe[0] = max(tiefe[0], len(traceback.extract_stack()))
            return original_origin(self)
        mod.PageEditor.place_origin = messend
        mod.PageEditor._padding_counts = None
        try:
            png = next((REPO / "src/glide/resources/logo").rglob("*.png"))
            bildseite = app.new_page_from_markdown("# Bilder\n\nEins\nZwei\n\nDrei\n\nVier\nFünf\n")
            ruhe()
            app.set_active_list(bildseite["id"])
            ruhe()
            seiteneditor = app.rich_note_editor
            erstes = seiteneditor.insert_images([str(png)], "3.0")[0]
            zweites = seiteneditor.insert_images([str(png)], "end")[0]
            seiteneditor.set_image_mode(zweites, "center")
            ruhe()
            for runde in range(4):
                app.set_active_list(liste["id"])
                ruhe(3)
                app.set_active_list(bildseite["id"])
                ruhe(3)
                root.geometry(f"{1150 + 70 * (runde % 3)}x{800 + 30 * (runde % 2)}")
                ruhe(3)
                app.rich_note_editor.text.yview_scroll(3, "units")
                ruhe(2)
        finally:
            mod.PageEditor.place_origin = original_origin
        assert 0 < tiefe[0] < 80, f"Bildplatzierung verschachtelt sich: Stapeltiefe {tiefe[0]}"
        assert not fehler, fehler[:1]
    finally:
        try:
            root.destroy()
        except Exception:
            pass

print("test_etappe1_332: OK; Symbol-Export (ICO 16/32/48/256, durchsichtig), Aseprite- und Adobe-Paletten, "
      "selbstfüllende Platzhalter und Tagesabschluss geprüft.")
