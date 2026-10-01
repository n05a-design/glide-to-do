"""Mindestgröße: jede Ansicht bei 860 × 700 ohne Überstand, Quetschung oder Anschnitt.

Anforderung vom 26.09.2026: „Wenn ich das Fenster komplett zusammendrücke,
möchte ich nur noch die wichtigsten Bestandteile und eine saubere Darstellung,
ohne Überschneidungen, Elemente, die zusammengequetscht wurden, oder
essentielle Bestandteile, die nicht mehr zu bedienen sind.“

Die Suite misst statt zu fotografieren – sie läuft damit auch ohne Bildschirm
(gesperrt, CI). Befunde je sichtbarem Widget:

- AUSSERHALB: ragt über den Fensterrand (unten abgeschnittene Aktionsreihen);
- ABGESCHNITTEN: ragt über den Rand seines Elternbereichs;
- GEQUETSCHT: eine Schaltfläche ist schmaler als ihre Beschriftung;
- TEXT ABGESCHNITTEN: ein einzeiliges Label ist schmaler als sein Text;
- SEITLICH: ein Element einer Scrollfläche ragt seitlich über sie hinaus.

Gegen den Stand vor der Korrektur fand dieselbe Messung 24 Befunde in
11 Ansichten; die Seitenleiste zeigte dort 2,2 statt heute 5 Zeilen.

Seit dem 26.09.2026 misst die Suite auch jeden Dialog aus der Menüleiste bei
seiner Mindestgröße, in mittlerer und großer Schrift. Der erste Lauf fand dort
Anschnitte im Kalender, einen gequetschten Kalenderknopf in der Punktmaske,
überstehende Aufklapppfeile und einen Absturz von „In Liste verschieben“.
"""
import importlib.machinery
import importlib.util
import os
import tempfile
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
BEISPIELE = REPO / "tests/fixtures/beispiele/glide_beispieldaten.glidebackup"


def nachfahren(widget):
    for kind in widget.winfo_children():
        yield kind
        yield from nachfahren(kind)


with tempfile.TemporaryDirectory(prefix="glide-mindestgroesse-") as ordner:
    os.environ["GLIDE_DATA_DIR"] = ordner
    os.environ["GLIDE_TEST_MODE"] = "1"
    with zipfile.ZipFile(BEISPIELE) as archiv:
        Path(ordner, "liste_speicher.json").write_bytes(archiv.read("data.json"))
    loader = importlib.machinery.SourceFileLoader("glide_mindestgroesse", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)

    root = mod.tk.Tk()
    root.geometry("860x700+0+30")
    fehler = []
    root.report_callback_exception = lambda *args: fehler.append(args)
    app = mod.ListApp(root)
    app.show_info = app.show_warning = app.show_error = lambda *args, **kwargs: None

    def ruhe():
        for _ in range(4):
            root.update_idletasks()
            root.update()

    def groesse(breite, hoehe):
        root.geometry(f"{breite}x{hoehe}+0+30")
        ruhe()
        assert (root.winfo_width(), root.winfo_height()) == (breite, hoehe), "Fenstergröße nicht übernommen"

    def schrift(stufe, design=None):
        if design:
            app.set_design(design, apply_now=False)
        app.settings["ui_font_size"] = stufe
        for attr in ("_ui_font_family", "_font_families", "_sidebar_row_font", "_system_row_font",
                     "_task_row_font", "_label_column_width", "_due_column_width"):
            setattr(app, attr, None)
        app.apply_ui_font()
        app.apply_theme()
        app.update_header_title()
        app.refresh_tree()
        ruhe()

    def scrollflaeche(widget):
        eltern = widget.master
        while eltern is not None:
            if isinstance(eltern, mod.tk.Canvas) and not isinstance(eltern, mod.RoundedButton):
                return eltern
            eltern = eltern.master
        return None

    def befunde(fenster=None):
        fenster = fenster or root
        breite, hoehe = fenster.winfo_width(), fenster.winfo_height()
        rx, ry = fenster.winfo_rootx(), fenster.winfo_rooty()
        gefunden = []
        for w in nachfahren(fenster):
            try:
                if not w.winfo_ismapped() or w.winfo_toplevel() is not fenster:
                    continue
                x, y = w.winfo_rootx() - rx, w.winfo_rooty() - ry
                ww, hh = w.winfo_width(), w.winfo_height()
            except mod.tk.TclError:
                continue
            if ww <= 2 or hh <= 2:
                continue
            knopf = isinstance(w, mod.RoundedButton)
            if knopf and not w.wrap_text and ww < w.text_width() + 12:
                gefunden.append(f"GEQUETSCHT „{w.text}“ {ww}px < Text {w.text_width()}px")
            flaeche = scrollflaeche(w)
            if flaeche is not None:
                fx = flaeche.winfo_rootx() - rx
                if x + ww > fx + flaeche.winfo_width() + 1:
                    gefunden.append(f"SEITLICH {w.winfo_class()} ragt über die Scrollfläche")
                continue
            art = w.winfo_class()
            text = w.text if knopf else ""
            if isinstance(w, mod.CanvasLabel):
                text = str(w.cget("text"))
                if text.strip() and not int(float(str(w.cget("wraplength")) or 0)) and w.text_size()[0] > ww + 2:
                    gefunden.append(f"TEXT ABGESCHNITTEN „{text[:40]}“ {ww}px < {w.text_size()[0]}px")
            if art == "Label":
                text = str(w.cget("text"))
                umbruch = int(float(str(w.cget("wraplength")) or 0))
                if text.strip() and not umbruch and not str(w.cget("image")) and w.winfo_reqwidth() > ww + 2:
                    gefunden.append(f"TEXT ABGESCHNITTEN „{text[:40]}“ {ww}px < {w.winfo_reqwidth()}px")
            if y + hh > hoehe + 1 or x + ww > breite + 1:
                gefunden.append(f"AUSSERHALB {art} „{text[:30]}“ y={y}..{y + hh}")
            eltern = w.master
            if eltern is not None and eltern is not fenster and not isinstance(eltern, mod.tk.Canvas):
                px, py = eltern.winfo_rootx() - rx, eltern.winfo_rooty() - ry
                if (y + hh > py + eltern.winfo_height() + 1 or x + ww > px + eltern.winfo_width() + 1) \
                        and (text or art in ("Treeview", "Entry", "Text")):
                    gefunden.append(f"ABGESCHNITTEN {art} „{text[:30]}“")
        return sorted(set(gefunden))

    def zeilen(baum):
        hoehe_zeile = int(mod.ttk.Style().lookup(baum.cget("style") or "Treeview", "rowheight") or 20)
        return baum.winfo_height() / max(1, hoehe_zeile)

    normal = next(entry for entry in app.lists
                  if entry.get("list_kind") in (None, "", "list", "tasks") and len(entry.get("items", [])) > 5)
    standard = next(folder for folder in app.folders if folder.get("folder_kind") != "journal")
    zeichnung = next((entry for entry in app.lists if app.is_drawing_list(entry)), None)
    ansichten = [
        ("Startseite", app.set_home_view),
        ("Mein Tag", app.set_plan_day_view),
        ("In Bearbeitung", app.set_in_progress_view),
        ("Verspätet", app.set_overdue_view),
        ("Labels", app.set_labels_view),
        ("Listen und Ordner", app.set_library_view),
        ("Vorlagen", app.set_template_view),
        ("Papierkorb", app.set_trash_view),
        ("Globale Pinnwand", app.open_global_board),
        ("Liste", lambda: app.set_active_list(normal["id"])),
        ("Tabelle", app.set_table_view),
        ("Pinnwand", lambda: (app.set_active_list(normal["id"]), app.workspace.set_mode("board"))),
        ("Liste nach Pinnwand", lambda: app.workspace.set_mode("list")),
        ("Ordner", lambda: app.set_active_folder(standard["id"])),
    ]
    if zeichnung is not None:
        ansichten.append(("Zeichnung", lambda: app.set_active_list(zeichnung["id"])))

    try:
        gesamt = 0
        for design, stufe, breite, hoehe in ((None, "mittel", 860, 700), (None, "gross", 860, 700),
                                             ("pixel", "gross", 860, 700), ("glass_dark", "mittel", 860, 700),
                                             ("dark", "mittel", 1400, 700)):
            schrift(stufe, design)
            for name, oeffnen in ansichten:
                oeffnen()
                groesse(breite, hoehe)
                liste = befunde()
                assert not liste, (design, stufe, breite, hoehe, name, liste[:6])
                gesamt += 1
        assert not fehler, fehler[:1]

        # Was bei Mindesthöhe bleibt und was weicht.
        schrift("mittel", "light")
        app.set_active_list(normal["id"])
        groesse(860, 700)
        assert app.height_density() == "minimal"
        # Auswahlleiste: bei Mindestbreite nur Wichtigkeit, Fällig, Löschen.
        app.tree.selection_set(next(iid for iid in app.tree.get_children("") if app.find_item(iid)))
        ruhe()
        assert app.selection_bar.winfo_ismapped()
        sichtbar = [knopf for knopf in app.selection_buttons if knopf.winfo_ismapped()]
        assert app.delete_button in sichtbar and app.flag_button in sichtbar
        for knopf in sichtbar:
            assert knopf.winfo_width() >= knopf.text_width() + 12, (knopf.text, knopf.winfo_width())
        app.tree.selection_set(())
        ruhe()
        assert not app.selection_bar.winfo_ismapped()
        assert zeilen(app.tree) >= 6.5 and zeilen(app.sidebar_listbox) >= 4.5, (
            zeilen(app.tree), zeilen(app.sidebar_listbox))
        # Ausgeblendete Aktionen bleiben erreichbar: Überlaufmenü der Kopfzeile.
        assert app.header_overflow_button.winfo_ismapped()
        # Die Kennzahlen unter dem Titel zeigen nur ganze Chips.
        zeile = app.page_chip_row
        for chip in zeile.winfo_children():
            if chip.winfo_ismapped():
                assert chip.winfo_x() + chip.winfo_width() <= zeile.winfo_width() + 1
        # Tabelle: Der Titel behält Platz, ganze Spalten weichen.
        app.set_table_view()
        groesse(860, 700)
        sichtbar = [str(spalte) for spalte in app.tree.cget("displaycolumns")]
        assert sichtbar[0] == "title" or "title" in sichtbar
        assert int(app.tree.column("title", "width")) >= app.TABLE_TITLE_MIN_VISIBLE - 1
        assert "type" not in sichtbar, "Die Art weicht zuerst"
        assert app.board_button.winfo_width() >= app.board_button.text_width() + 12
        # Groß genug: alles wieder da.
        app.set_active_list(normal["id"])
        groesse(1280, 1000)
        assert app.height_density() == "full"
        app.tree.selection_set(next(iid for iid in app.tree.get_children("") if app.find_item(iid)))
        ruhe()
        assert all(knopf.winfo_ismapped() for knopf in app.selection_buttons)
        app.tree.selection_set(())
        app.set_table_view()
        groesse(1500, 1000)
        breit = [str(spalte) for spalte in app.tree.cget("displaycolumns")]
        assert len(breit) > len(sichtbar), (breit, sichtbar)
        assert not fehler, fehler[:1]

        # Jeder Dialog aus der Menüleiste bei seiner Mindestgröße, in mittlerer
        # und großer Schrift. `run_modal` misst statt zu warten; davor läuft
        # dieselbe Absicherung der Mindestbreite wie im Betrieb.
        mod.filedialog.askopenfilename = lambda *args, **kwargs: ""
        mod.filedialog.askopenfilenames = lambda *args, **kwargs: ()
        mod.filedialog.asksaveasfilename = lambda *args, **kwargs: ""
        mod.filedialog.askdirectory = lambda *args, **kwargs: ""
        mod.tk.Menu.tk_popup = lambda self, *args, **kwargs: None
        app.ask_yes_no = lambda *args, **kwargs: False
        app.ask_yes_no_cancel = lambda *args, **kwargs: None
        app.open_external_path = lambda pfad: None
        dialoge = []

        def messen(self, dialog, parent=None):
            try:
                self.ensure_dialog_min_width(dialog)
                mindest_b, mindest_h = dialog.minsize()
                if mindest_b <= 1 or mindest_h <= 1:
                    mindest_b, mindest_h = dialog.winfo_reqwidth(), dialog.winfo_reqheight()
                dialog.geometry(f"{mindest_b}x{mindest_h}+40+60")
                for _ in range(4):
                    dialog.update_idletasks()
                    dialog.update()
                dialoge.append((dialog.title(), befunde(dialog)))
            finally:
                if dialog.winfo_exists():
                    dialog.destroy()

        mod.ListApp.run_modal = messen
        groesse(1280, 860)
        for stufe in ("mittel", "gross"):
            schrift(stufe, "light")
            for eintrag in app.app_action_entries():
                if eintrag["label"] in ("Beenden", "Papierkorb leeren", "Aktive Liste löschen"):
                    continue
                app.set_active_list(normal["id"])
                ruhe()
                erster = next(iid for iid in app.iter_tree_ids()
                              if app.find_item(iid) and not app.is_structural_item(app.find_item(iid)[0]))
                app.tree.selection_set(erster)
                app.tree.focus(erster)
                eintrag["menu"].invoke(eintrag["index"])
                ruhe()
                assert not fehler, (stufe, eintrag["label"], fehler[:1])
        assert len(dialoge) >= 40, len(dialoge)
        mit_befund = [(titel, liste[:4]) for titel, liste in dialoge if liste]
        assert not mit_befund, mit_befund[:3]
    finally:
        root.destroy()

print(f"test_mindestgroesse330: OK; {gesamt} Ansichten in fünf Design-, Größen- und Schriftstufen und "
      f"{len(dialoge)} Dialogaufrufe bei Mindestgröße ohne Befund, Höhenstufen und Tabellenspalten geprüft.")
