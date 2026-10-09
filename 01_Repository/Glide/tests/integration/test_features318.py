"""CSV-Import: Erkennung, Zuordnung, Werteregeln, Verschachtelung, Ziele, Dialog."""
import copy
import csv
import importlib.machinery
import importlib.util
import io
import os
import tempfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


def schreibe_csv(pfad, zeilen, delimiter=";", encoding="utf-8"):
    puffer = io.StringIO()
    csv.writer(puffer, delimiter=delimiter, lineterminator="\n").writerows(zeilen)
    Path(pfad).write_bytes(puffer.getvalue().encode(encoding))
    return pfad


def texte(items):
    """Baum als (Text, Ebene)-Folge in Lesereihenfolge."""
    ergebnis = []

    def gehe(liste, ebene):
        for punkt in liste:
            ergebnis.append((punkt.get("text"), ebene))
            gehe(punkt.get("children", []), ebene + 1)
    gehe(items, 1)
    return ergebnis


with tempfile.TemporaryDirectory(prefix="glide-features318-") as folder:
    os.environ["GLIDE_DATA_DIR"] = folder
    os.environ["GLIDE_TEST_MODE"] = "1"
    loader = importlib.machinery.SourceFileLoader("glide_features318", str(REPO / "src/glide/app.pyw"))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    root = mod.tk.Tk()
    root.withdraw()
    callbacks = []
    root.report_callback_exception = lambda *args: callbacks.append(args)
    app = mod.ListApp(root)
    meldungen = []
    app.show_warning = app.show_error = lambda *args, **kwargs: meldungen.append(args)
    infos = []
    app.show_info = lambda *args, **kwargs: infos.append(args)
    app.ask_yes_no = lambda *args, **kwargs: True
    A = mod.ListApp
    try:
        heute = date.today().isoformat()
        assert A.MAX_CSV_IMPORT_ROWS == 5000 and A.MAX_CSV_IMPORT_COLUMNS == 64
        assert [key for key, _text in A.CSV_FIELD_LABELS][:3] == ["text", "description", "done"]

        # --- 1. Rundlauf über eine echte Exportdatei -------------------------
        quelle = app.new_list_object("Umzug & Übergabe", [])
        haupt = app.new_item('Schlüssel "Hof" übergeben', due=heute, due_time="09:30",
                             planned_date=heute, estimated_minutes=45, importance=3)
        haupt["description"] = "Beim Verwalter melden"
        fertig = app.new_item("Kartons zählen")
        fertig["done"] = True
        gruppe = app.new_item("Keller", kind=A.ITEM_KIND_GROUP)
        unter = app.new_item("Regale abbauen", estimated_minutes=90)
        tiefer = app.new_item("Schrauben sortieren")
        unter["children"] = [tiefer]
        gruppe["children"] = [unter]
        ueberschrift = app.new_item("Danach", kind=A.ITEM_KIND_HEADING)
        mehrzeilig = app.new_item("Zeile eins\nZeile zwei", kind=A.ITEM_KIND_LONG)
        quelle["items"] = [haupt, fertig, gruppe, ueberschrift, mehrzeilig]
        app.lists.append(quelle)
        app.set_active_list(quelle["id"])
        etikett = app.ensure_label_by_name("Vor Ort")
        haupt["labels"] = list(haupt.get("labels") or []) + [etikett["id"]]
        assert app.save_items()

        export_pfad = os.path.join(folder, "export.csv")
        mod.filedialog.asksaveasfilename = lambda *args, **kwargs: export_pfad
        app.export_as_csv()
        assert os.path.isfile(export_pfad)

        tabelle = app.read_csv_table(export_pfad)
        assert tabelle["has_header"] and tabelle["delimiter"] == ";"
        assert tabelle["encoding"] == "utf-8-sig", tabelle["encoding"]
        zuordnung = app.csv_auto_mapping(tabelle)
        for feld in ("text", "description", "done", "importance", "due", "due_time",
                     "kind", "labels", "planned_date", "estimated_minutes", "level", "number"):
            assert isinstance(zuordnung[feld], int), (feld, zuordnung)
        ziel, bericht = app.import_csv_table(tabelle, zuordnung)
        assert bericht["skipped"] == 0 and bericht["cells"] == 0, bericht
        assert texte(ziel["items"]) == texte(quelle["items"]), texte(ziel["items"])
        neu_haupt = ziel["items"][0]
        assert neu_haupt["due"] == heute and neu_haupt["due_time"] == "09:30"
        assert neu_haupt["planned_date"] == heute and neu_haupt["estimated_minutes"] == 45
        assert neu_haupt["importance"] == 3 and not neu_haupt["done"]
        assert neu_haupt["description"] == "Beim Verwalter melden"
        assert app.format_item_label_names(neu_haupt) == app.format_item_label_names(haupt)
        assert ziel["items"][1]["done"] and app.item_kind(ziel["items"][2]) == A.ITEM_KIND_GROUP
        assert app.item_kind(ziel["items"][3]) == A.ITEM_KIND_HEADING
        assert app.item_kind(ziel["items"][4]) == A.ITEM_KIND_LONG
        assert ziel["items"][4]["text"] == "Zeile eins\nZeile zwei"
        # Der Rundlauf legt keine zweiten Labels an.
        assert len([eintrag for eintrag in app.labels if eintrag.get("name") == "Vor Ort"]) == 1

        # --- 2. Trennzeichen und Kodierungen --------------------------------
        for nummer, trenner in enumerate((";", ",", "\t", "|"), start=1):
            pfad = schreibe_csv(os.path.join(folder, f"trenn{nummer}.csv"),
                                [["Aufgabe", "Fällig"], ["Fenster putzen", "01.10.2026"]],
                                delimiter=trenner)
            erkannt = app.read_csv_table(pfad)
            assert erkannt["delimiter"] == trenner, (trenner, erkannt["delimiter"])
            assert erkannt["rows"][0][0] == "Fenster putzen"
        # Die Handwahl überstimmt die Erkennung.
        gemischt = schreibe_csv(os.path.join(folder, "gemischt.csv"),
                                [["Aufgabe;Zusatz"], ["Tür,ölen;links"]], delimiter="|")
        mit_komma = app.read_csv_table(gemischt, delimiter=",")
        assert mit_komma["delimiter"] == "," and len(mit_komma["columns"]) == 2

        for kodierung, erwartet in (("utf-8", "utf-8"), ("utf-8-sig", "utf-8-sig"),
                                    ("cp1252", "cp1252"), ("utf-16", "utf-16")):
            pfad = schreibe_csv(os.path.join(folder, f"kod_{kodierung}.csv"),
                                [["Aufgabe"], ["Küche für Ärzte prüfen"]], encoding=kodierung)
            gelesen = app.read_csv_table(pfad)
            assert gelesen["encoding"] == erwartet, (kodierung, gelesen["encoding"])
            assert gelesen["rows"][0][0] == "Küche für Ärzte prüfen", gelesen["rows"]
        # Falsche Handwahl meldet sich, statt Zeichenmüll zu erzeugen.
        try:
            app.read_csv_table(os.path.join(folder, "kod_utf-16.csv"), encoding="utf-8")
        except ValueError as fehler:
            assert "Kodierung" in str(fehler)
        else:
            raise AssertionError("UTF-16 wurde als UTF-8 angenommen")

        # --- 3. Ohne Kopfzeile ----------------------------------------------
        ohne_kopf = schreibe_csv(os.path.join(folder, "ohnekopf.csv"),
                                 [["Müll rausbringen", "1"], ["Post holen", "2"]])
        rohe = app.read_csv_table(ohne_kopf)
        assert rohe["has_header"] is False, rohe
        assert rohe["columns"] == ["Spalte 1", "Spalte 2"] and len(rohe["rows"]) == 2
        assert all(wert is None for wert in app.csv_auto_mapping(rohe).values())
        hand = {key: None for key, _text in A.CSV_FIELD_LABELS}
        hand["text"] = 0
        punkte, hand_bericht = app.csv_rows_to_items(rohe, hand)
        assert [punkt["text"] for punkt in punkte] == ["Müll rausbringen", "Post holen"]
        assert hand_bericht["items"] == 2 and hand_bericht["skipped"] == 0
        # Erzwungene Kopfzeile nimmt die erste Datenzeile als Namen.
        erzwungen = app.read_csv_table(ohne_kopf, has_header=True)
        assert erzwungen["columns"][0] == "Müll rausbringen" and len(erzwungen["rows"]) == 1

        # --- 4. Spaltenerkennung über Synonyme -------------------------------
        fremd = schreibe_csv(os.path.join(folder, "fremd.csv"), [
            ["Title", "Notes", "Status", "Priority", "Due Date", "Tags", "Duration", "Level"],
            ["Angebot schreiben", "mit Anlagen", "done", "high", "2026-10-02", "Büro|Kunde", "1:30", "1"],
        ])
        fremd_tabelle = app.read_csv_table(fremd)
        fremd_zuordnung = app.csv_auto_mapping(fremd_tabelle)
        assert fremd_zuordnung["text"] == 0 and fremd_zuordnung["description"] == 1
        assert fremd_zuordnung["done"] == 2 and fremd_zuordnung["importance"] == 3
        assert fremd_zuordnung["due"] == 4 and fremd_zuordnung["labels"] == 5
        assert fremd_zuordnung["estimated_minutes"] == 6 and fremd_zuordnung["level"] == 7
        fremd_punkte, _bericht = app.csv_rows_to_items(fremd_tabelle, fremd_zuordnung)
        einer = fremd_punkte[0]
        assert einer["done"] and einer["importance"] == 3 and einer["due"] == "2026-10-02"
        assert einer["estimated_minutes"] == 90 and len(einer["labels"]) == 2
        assert "Büro" in app.format_item_label_names(einer)

        # --- 5. Werteregeln einzeln -----------------------------------------
        for wert, erwartet in (("ja", True), ("x", True), ("1", True), ("WAHR", True),
                               ("erledigt", True), ("done", True), ("nein", False),
                               ("0", False), ("offen", False), ("-", False), ("", None),
                               ("vielleicht", None)):
            assert A.parse_csv_flag(wert) is erwartet, wert
        for wert, erwartet in (("keine", 0), ("niedrig", 1), ("mittel", 2), ("hoch", 3),
                               ("low", 1), ("HIGH", 3), ("2", 2), ("", None), ("später", None)):
            assert A.parse_csv_importance(wert) == erwartet, wert
        for wert, erwartet in (("45", 45), ("45 min", 45), ("1:30", 90), ("1,5 h", 90),
                               ("2h", 120), ("", None), ("bald", None), ("0", None),
                               (str(A.MAX_ESTIMATED_MINUTES + 1), None)):
            assert A.parse_csv_minutes(wert) == erwartet, wert
        for wert, erwartet in (("Aufgabe", A.ITEM_KIND_TASK), ("Gruppe", A.ITEM_KIND_GROUP),
                               ("Langtext", A.ITEM_KIND_LONG), ("Zwischenüberschrift", A.ITEM_KIND_HEADING),
                               ("Zwischenüberschrift", A.ITEM_KIND_HEADING), ("heading", A.ITEM_KIND_HEADING),
                               ("", None), ("Epic", None)):
            assert A.parse_csv_kind(wert) == erwartet, wert
        assert A.csv_labels_from_cell("Büro | Kunde") == ["Büro", "Kunde"]
        assert A.csv_labels_from_cell("Büro, Kunde, Büro") == ["Büro", "Kunde"]
        assert A.csv_labels_from_cell("") == []
        assert A.clean_csv_cell("'=1+1") == "=1+1", "Formelschutz wird beim Lesen entfernt."
        assert A.normalize_csv_header("Aufwand (Minuten)") == "aufwand"

        fehlerhaft = schreibe_csv(os.path.join(folder, "fehler.csv"), [
            ["Aufgabe", "Fällig", "Uhrzeit", "Bearbeitungstag", "Aufwand", "Art", "Erledigt", "Wichtigkeit"],
            ["Gültig", "03.10.2026", "08:15", "02.10.2026", "30", "Aufgabe", "ja", "hoch"],
            ["Krumme Werte", "irgendwann", "25:99", "nächste Woche", "viel", "Epic", "vielleicht", "später"],
            ["", "03.10.2026", "", "", "", "", "", ""],
        ])
        fehler_tabelle = app.read_csv_table(fehlerhaft)
        fehler_punkte, fehler_bericht = app.csv_rows_to_items(fehler_tabelle,
                                                              app.csv_auto_mapping(fehler_tabelle))
        assert [punkt["text"] for punkt in fehler_punkte] == ["Gültig", "Krumme Werte"]
        assert fehler_bericht["skipped"] == 1 and fehler_bericht["items"] == 2
        # Art, Erledigt, Wichtigkeit, Fällig, Uhrzeit, Bearbeitungstag, Aufwand.
        assert fehler_bericht["cells"] == 7, fehler_bericht
        assert fehler_bericht["notes"] and len(fehler_bericht["notes"]) == 3
        assert all(note.startswith("Zeile ") for note in fehler_bericht["notes"])
        krumm = fehler_punkte[1]
        assert krumm["due"] is None and krumm["due_time"] is None
        assert krumm["planned_date"] is None and krumm["estimated_minutes"] is None
        assert not krumm["done"] and krumm["importance"] == 0
        # Gruppen und Überschriften verwerfen Status- und Fristangaben.
        strukturell = schreibe_csv(os.path.join(folder, "struktur.csv"), [
            ["Aufgabe", "Art", "Erledigt", "Fällig", "Wichtigkeit", "Aufwand"],
            ["Abschnitt", "Gruppe", "ja", "03.10.2026", "hoch", "30"],
        ])
        st_tabelle = app.read_csv_table(strukturell)
        st_punkte, _st_bericht = app.csv_rows_to_items(st_tabelle, app.csv_auto_mapping(st_tabelle))
        assert app.item_kind(st_punkte[0]) == A.ITEM_KIND_GROUP
        assert not st_punkte[0]["done"] and st_punkte[0]["due"] is None
        assert st_punkte[0]["importance"] == 0 and st_punkte[0]["estimated_minutes"] is None

        # --- 6. Verschachtelung ---------------------------------------------
        assert A.parse_csv_level("3", "") == 3 and A.parse_csv_level("", "2.1.3") == 3
        assert A.parse_csv_level("", "4.") == 1 and A.parse_csv_level("", "") == 1
        assert A.parse_csv_level("2", "1.1.1") == 2, "Die Ebene entscheidet vor der Nummer."
        ebenen = schreibe_csv(os.path.join(folder, "ebenen.csv"), [
            ["Aufgabe", "Ebene"],
            ["Oben", "1"], ["Darunter", "2"], ["Noch tiefer", "3"],
            ["Sprung", "7"], ["Wieder oben", "1"], ["Waise", "4"],
        ])
        eb_tabelle = app.read_csv_table(ebenen)
        eb_zuordnung = app.csv_auto_mapping(eb_tabelle)
        eb_punkte, _b = app.csv_rows_to_items(eb_tabelle, eb_zuordnung)
        assert texte(eb_punkte) == [("Oben", 1), ("Darunter", 2), ("Noch tiefer", 3),
                                    ("Sprung", 4), ("Wieder oben", 1), ("Waise", 2)], texte(eb_punkte)
        flach, _b = app.csv_rows_to_items(eb_tabelle, eb_zuordnung, nest=False)
        assert [ebene for _text, ebene in texte(flach)] == [1] * 6
        nummern = schreibe_csv(os.path.join(folder, "nummern.csv"), [
            ["Nummer", "Aufgabe"],
            ["1", "Erstes"], ["1.1", "Unterpunkt"], ["1.1.1", "Tiefster"], ["2", "Zweites"],
        ])
        nr_tabelle = app.read_csv_table(nummern)
        nr_punkte, _b = app.csv_rows_to_items(nr_tabelle, app.csv_auto_mapping(nr_tabelle))
        assert texte(nr_punkte) == [("Erstes", 1), ("Unterpunkt", 2), ("Tiefster", 3), ("Zweites", 1)]
        # Eine Überschrift gliedert, wird aber nicht Elternpunkt.
        mit_ueberschrift = schreibe_csv(os.path.join(folder, "ueberschrift.csv"), [
            ["Aufgabe", "Art", "Ebene"],
            ["Kapitel", "Überschrift", "1"], ["Darunter", "Aufgabe", "2"],
        ])
        ue_tabelle = app.read_csv_table(mit_ueberschrift)
        ue_punkte, _b = app.csv_rows_to_items(ue_tabelle, app.csv_auto_mapping(ue_tabelle))
        assert texte(ue_punkte) == [("Kapitel", 1), ("Darunter", 1)], texte(ue_punkte)

        # --- 7. Importziele --------------------------------------------------
        ziel_datei = schreibe_csv(os.path.join(folder, "Neue Aufgaben.csv"),
                                  [["Aufgabe"], ["Erster Punkt"], ["Zweiter Punkt"]])
        ziel_tabelle = app.read_csv_table(ziel_datei)
        ziel_zuordnung = app.csv_auto_mapping(ziel_tabelle)
        anzahl_vorher = len(app.lists)
        neue_liste, _b = app.import_csv_table(ziel_tabelle, ziel_zuordnung)
        assert len(app.lists) == anzahl_vorher + 1
        assert neue_liste["title"] == "Neue Aufgaben", neue_liste["title"]
        assert app.active_list_id == neue_liste["id"] and neue_liste["folder_id"] is None
        app.set_active_list(quelle["id"])
        punkte_vorher = app.count_items(app.items, include_groups=True)
        gleiche, _b = app.import_csv_table(ziel_tabelle, ziel_zuordnung, append_to_current=True)
        assert gleiche["id"] == quelle["id"]
        assert app.count_items(app.items, include_groups=True) == punkte_vorher + 2
        assert app.items[-1]["text"] == "Zweiter Punkt"
        ordner = app.new_folder_object("Projekte", color="accent")
        app.folders.append(ordner)
        assert app.save_items()
        app.set_active_folder(ordner["id"])
        im_ordner, _b = app.import_csv_table(ziel_tabelle, ziel_zuordnung)
        assert im_ordner["folder_id"] == ordner["id"]
        app.set_active_list(quelle["id"])
        # Ohne zugeordneten Aufgabentext passiert nichts.
        leer_zuordnung = {key: None for key, _text in A.CSV_FIELD_LABELS}
        try:
            app.import_csv_table(ziel_tabelle, leer_zuordnung)
        except ValueError:
            pass
        else:
            raise AssertionError("Import ohne Textspalte wurde angenommen")

        # --- 8. Grenzen ------------------------------------------------------
        zu_viele_zeilen = schreibe_csv(os.path.join(folder, "viele.csv"),
                                       [["Aufgabe"]] + [[f"Punkt {nummer}"]
                                                        for nummer in range(A.MAX_CSV_IMPORT_ROWS + 5)])
        try:
            app.read_csv_table(zu_viele_zeilen)
        except ValueError as fehler:
            assert str(A.MAX_CSV_IMPORT_ROWS) in str(fehler)
        else:
            raise AssertionError("Zeilengrenze wirkte nicht")
        zu_viele_spalten = schreibe_csv(os.path.join(folder, "breit.csv"),
                                        [[f"S{nummer}" for nummer in range(A.MAX_CSV_IMPORT_COLUMNS + 2)],
                                         ["x"] * (A.MAX_CSV_IMPORT_COLUMNS + 2)])
        try:
            app.read_csv_table(zu_viele_spalten)
        except ValueError as fehler:
            assert "Spalten" in str(fehler)
        else:
            raise AssertionError("Spaltengrenze wirkte nicht")
        gross = os.path.join(folder, "gross.csv")
        with open(gross, "wb") as datei:
            datei.write(b"Aufgabe\n" + b"x" * (A.MAX_CSV_IMPORT_BYTES + 1))
        try:
            app.read_csv_table(gross)
        except ValueError as fehler:
            assert "MB" in str(fehler)
        else:
            raise AssertionError("Größengrenze wirkte nicht")
        os.remove(gross)
        leere_datei = os.path.join(folder, "leer.csv")
        Path(leere_datei).write_text("\n\n", encoding="utf-8")
        try:
            app.read_csv_table(leere_datei)
        except ValueError:
            pass
        else:
            raise AssertionError("Leere Datei wurde angenommen")

        # --- 9. Bericht und Rückgängig ---------------------------------------
        with_labels = schreibe_csv(os.path.join(folder, "labels.csv"), [
            ["Aufgabe", "Labels"],
            ["Mit neuem Label", "Frisch aus CSV"],
            ["", "Zeile ohne Aufgabentext"],
        ])
        lbl_tabelle = app.read_csv_table(with_labels)
        labels_vorher = copy.deepcopy(app.labels)
        def ohne_verlauf(payload):
            """Vergleich ohne das Protokoll: Rückgängig nimmt Bestand zurück,
            nicht den Änderungsverlauf – der bleibt als Aufzeichnung stehen."""
            return {key: wert for key, wert in payload.items() if key != "history"}

        bestand_vorher = ohne_verlauf(copy.deepcopy(app.data_payload()))
        lbl_ziel, lbl_bericht = app.import_csv_table(lbl_tabelle, app.csv_auto_mapping(lbl_tabelle))
        assert app.get_label_by_name("Frisch aus CSV") is not None
        zusammenfassung = app.csv_import_summary(lbl_bericht, lbl_ziel)
        assert "1 Punkt übernommen" in zusammenfassung and "übersprungen" in zusammenfassung
        assert "Zeile 3" in zusammenfassung, zusammenfassung
        app.undo_last_change()
        assert app.get_label_by_name("Frisch aus CSV") is None, "Rückgängig nimmt neue Labels mit."
        assert len(app.labels) == len(labels_vorher)
        assert ohne_verlauf(app.data_payload()) == bestand_vorher, "Rückgängig stellt den Bestand her."

        # --- 10. Dialog in Hell und Dunkel -----------------------------------
        dialog_datei = schreibe_csv(os.path.join(folder, "Dialogprobe.csv"), [
            ["Aufgabe", "Ebene", "Fällig"],
            ["Dialogpunkt", "1", "05.10.2026"],
            ["Unterpunkt", "2", ""],
        ])
        root.deiconify()
        root.geometry("1100x780+10+10")
        for theme in ("light", "dark"):
            app.set_design(theme, apply_now=False)
            app.apply_theme()
            app.set_active_list(quelle["id"])
            vorher = app.count_items(app.items, include_groups=True)
            listenzahl = len(app.lists)
            infos.clear()

            def importieren(dialog, parent=None):
                dialog.geometry("780x640")
                dialog.update()
                widgets = list(descendants(dialog))
                haken = {name: next(w for w in widgets if w.winfo_name() == name)
                         for name in ("csv_header", "csv_nest", "csv_append")}
                assert all(str(w.cget("state")) != "disabled" for w in haken.values())
                vorschau = next(w for w in widgets if w.winfo_name() == "csv_preview")
                text = vorschau.get("1.0", "end")
                assert "Dialogpunkt" in text and "Unterpunkt" in text, text
                assert "05.10.2026" in text, text
                haken["csv_append"].invoke()  # in die geöffnete Liste
                knopf = next(w for w in widgets if isinstance(w, mod.RoundedButton)
                             and w.text == "Importieren")
                assert knopf.winfo_ismapped()
                assert (knopf.winfo_rooty() + knopf.winfo_height()
                        <= dialog.winfo_rooty() + dialog.winfo_height())
                knopf.command()
            app.run_modal = importieren
            assert app.show_csv_import_dialog(path=dialog_datei) == "break"
            assert len(app.lists) == listenzahl, "Anhängen legt keine neue Liste an."
            assert app.count_items(app.items, include_groups=True) == vorher + 2
            assert app.items[-1]["text"] == "Dialogpunkt"
            assert app.items[-1]["children"][0]["text"] == "Unterpunkt"
            assert infos and "übernommen" in infos[-1][1], infos

            def abbrechen(dialog, parent=None):
                dialog.update()
                next(w for w in descendants(dialog) if isinstance(w, mod.RoundedButton)
                     and w.text == "Abbrechen").command()
            app.run_modal = abbrechen
            zustand = copy.deepcopy(app.data_payload())
            app.show_csv_import_dialog(path=dialog_datei)
            assert app.data_payload() == zustand, "Abbrechen ändert nichts."
            assert ohne_verlauf(app.data_payload()) == ohne_verlauf(zustand)
        assert not callbacks, callbacks
    finally:
        app.cancel_pending_callbacks()
        app.release_data_lock()
        root.destroy()

print("OK: CSV-Import mit Erkennung, Zuordnung, Werteregeln, Verschachtelung, Zielen, Grenzen und Dialog")
