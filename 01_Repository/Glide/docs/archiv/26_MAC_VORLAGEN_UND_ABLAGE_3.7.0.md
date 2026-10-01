# Mac, Vorlagen und Ablage – Nachbesserung 11.09.2026

Glide 3.7.0 bleibt der nicht veröffentlichte Entwicklungsstand. Aufgabenformat 12,
Einstellungen 2, Vorlagenformat **2**. Dieser Nachtrag ersetzt für die sechs hier
behandelten Punkte die Beschreibungen und Prüfgrenzen vom 07.09.2026.

## Abgleich mit dem Auftrag

| Rückmeldung | Umsetzung | Nachweis |
|---|---|---|
| Startseite scrollt am Mac nicht | Gemeinsame Behandlung von MouseWheel und Tk-9-TouchpadScroll; kleine vertikale Bewegungen erhalten, horizontale Bewegungen nicht als vertikales Scrollen gewertet | `test_template_workflows.py`, `test_release37.py` |
| Vorlagenfenster im Light Mode fehlerhaft | Vollständig eingefärbter Dialoghintergrund; dieselben thematisierten Detailmasken wie bei Aufgaben, Listen und Ordnern | Echte Tk-Widgets in Hell/Dunkel automatisiert geprüft |
| Vorlagen ausführlich bearbeiten | Strukturbaum, Titel, Beschreibung, Farbe, Labels und Anhänge; vollständige Punktdetails; Listen, Unterordner, Punkte und Unterpunkte ergänzen, entfernen und innerhalb derselben Ebene umsortieren | Abbruch-, Struktur-, Detail- und Rundlaufprüfung |
| Vorlagendateien überarbeiten | 16 vollständige Vorlagen, konkrete Ergebnisse und Prüfkriterien; Immobilien, WordPress, WEG und Baukommunikation; Beispielanhänge; relative Termine | Reproduzierbarer Erzeuger und Importvalidator |
| Listenübersicht übersichtlicher | Typkennzeichnung, Ordnerpfad, Kennzahlen, Fortschritt, Labels; bis zu drei getrennte nächste Aufgaben, nach Termin und Wichtigkeit; gekürzte Vorschau mit vollständigem Tooltip | Responsive Kacheln und Navigation, 860/1280/1660 Pixel |
| Dokumentation und Dateien ordnen | Historische Arbeitsstände ins Archiv verschoben; aktive Einstiege, Katalog, Python-Arbeitskopie und Beispielbackups aktualisiert; keine endgültige Löschung | [Ablageprotokoll](../28_ABLAGEPRUEFUNG_2026-09-11.md) |

## Vorlagenbearbeitung

„Vorlagen → Bearbeiten“ schaltet die Katalogbearbeitung ein. Das Stiftsymbol öffnet
den Entwurf. „Vorlagendetails“ bietet die Eigenschaften der Stammliste bzw. des
Stammordners. Im Strukturbaum öffnet „Bearbeiten“ die passende Detailmaske:

- Liste/Ordner: Titel, Beschreibung, Farbe, Labels mit Neuanlage und Dateianhänge.
- Punkt: Aufgabe, Gruppe, Überschrift oder Long-Task, Wichtigkeit, Farbe, Datum,
  Uhrzeit, Wiederholung einschließlich Enddatum, Labels, Beschreibung und Anhänge.
- Unterpunkte bleiben beim Umbenennen und Umsortieren beim zugehörigen Objekt.
- Unterordner und darin enthaltene Listen bleiben erhalten; leere Unterordner ebenfalls.

„Übernehmen“ ändert den Katalog im Arbeitsspeicher. „Vorlagen speichern“ schreibt
die Datei. „Abbrechen“, Escape oder das Schließen des Entwurfs verwerfen dessen
Änderungen einschließlich neu angelegter Labels und temporärer Anhangskopien.
Die bestehenden Arbeitslisten werden durch das Bearbeiten einer Vorlage nicht verändert.
Die Wurzel selbst wird im Editor nicht entfernt; dafür gibt es „Vorlage löschen“
auf der Katalogseite. Umordnen erfolgt innerhalb derselben Ebene; der Editor
bietet keine Drag-and-Drop-Neuzuordnung zwischen Elternobjekten.

## Datenvertrag und Migration

Vorlagenformat 2 ergänzt das optionale ISO-Datum `schedule_anchor`.
Ist es vorhanden, verschiebt das Verwenden alle Fälligkeiten sowie `start` und
`ende` von Wiederholungen um `heute - Bezugsdatum`. Uhrzeiten und die gewählten
Wochentage einer Wiederholung bleiben gleich. Beispiel: Bezugsdatum 11.09.,
Aufgabe fällig 18.09.; beim Einsatz am 20.09. ist sie am 27.09. fällig.
Ohne Bezugsdatum bleiben absolute Termine unverändert.

Der Editor zeigt die Option „Termine relativ zum Einsatzdatum“; der Tooltip nennt
das Bezugsdatum. Vorgegebene Termine sind Planungshilfen und müssen zum Auftrag
passen. Sie sind weder rechtliche Fristen noch Benachrichtigungen.

Format-1-Kataloge bleiben lesbar. Vor dem ersten Schreiben als Format 2 entsteht
unter `backups/vorlagen_vor_format2_<Zeitstempel>.json` eine unveränderte Kopie.
Scheitert diese Sicherung, wird die alte Datei nicht überschrieben. Ältere Apps
können Format 2 nicht lesen; für eine Rückkehr die gesicherte Format-1-Datei verwenden.
Das Aufgabenformat wird durch diese Änderung nicht angehoben.

Ein vollständig unveränderter ursprünglicher Katalog wird beim Laden auf alle 16 Praxisvorlagen aktualisiert. In bearbeiteten Katalogen werden nur noch unveränderte mitgelieferte Vorlagen inhaltlich aktualisiert.
Eigene Änderungen werden erkannt und bleiben erhalten. Gelöschte Vorlagen werden
nicht ungefragt wiederhergestellt; ein absichtlich leerer Katalog bleibt leer.
Neue zusätzliche Vorlagen lassen sich aus dem ausgelieferten Katalog ergänzen.

## Architektur

`TemplateDraft` verwendet die bestehenden ListApp-Detailmasken mit eigenen
Objektlisten, Labels und einer temporären Dateiablage. Es startet keine zweite App,
keine Autospeicherung und keine Datenordnersperre. Erst `export_record` baut ein
validiertes Teilpayload mit eingebetteten Anhangsbytes. `create_list_from_template`
verwendet den bestehenden transaktionalen Import mit neuen IDs. Erfolgreiche
Vorlagenanlage benötigt keinen zusätzlichen „Import erfolgreich“-Dialog.

Der Katalog liegt unter `src/glide/resources/templates/glide_vorlagen.glidetemplates`.
`tests/tools/vorlagendaten.py` erzeugt ihn deterministisch. Beim Verpacken oder
Kopieren der Python-Datei immer den vollständigen Ordner `resources` mitführen.

Die Scrollumstellung folgt der lokalen Tk-9-Implementierung und
[Tk TIP 684](https://core.tcl-lang.org/tips/doc/main/tip/684.md).
Tk 8 kennt das zusätzliche Ereignis nicht; die optionale Bindung wird dort
übersprungen, während das bisherige Mausrad weiterarbeitet.

## Prüfung und Grenzen

Alle elf Testsuiten und der vollständige automatische Prüflauf sind erfolgreich.
Einzelheiten stehen im [QA-Bericht](../07_QA_BERICHT.md).
Die Ausgangsprüfung fand einen bereits vorhandenen Mac-Fehler im Testlader:
`.pyw` wurde nicht als Python-Modul erkannt. Der explizite SourceFileLoader
beseitigt diesen Fehler. Nutzdaten aller Tests liegen unter `GLIDE_DATA_DIR` in
temporären Ordnern. Ein manuell ausgeführter physischer Trackpad-Test und eine
vollständige native Sichtabnahme dürfen daraus nicht abgeleitet werden.

## Zweiter UI-Nachtrag vom 11.09.2026

Die Rückmeldung mit den Bildern von 08:23/08:24 zeigte zwei vom bisherigen
Test nicht erfasste Darstellungsfehler: Der Strukturbaum des Vorlageneditors
verwendete den Standard-Treeview ohne App-Stil und native Scrollleisten.
Die Mac-OptionMenus zeichneten ihre grauen Systemflächen trotz gesetzter Farben.

Der Vorlagenbaum erbt jetzt den bestehenden `App.Treeview`-Stil in einer
gerundeten Kartenfläche. Schrift, Auswahl, Hover, Hierarchiezeichen und Scrollleiste
folgen den normalen Listen. Native Tabellenköpfe entfallen. Metadatenspalten passen
sich der Breite an; Fälligkeiten sind deutsch formatiert und berücksichtigen die
Uhrzeit. Untere Aktionen erhalten ihren Platz vor dem wachsenden Inhaltsbereich.
Der Titel nutzt den gemeinsamen Feldrahmen. Geschlossene Zweige bleiben beim
Auffrischen geschlossen; F2/Enter und Doppelklick öffnen die vorhandenen Details.

`MacOptionMenu` wird ausschließlich bei `IS_MACOS` verwendet. Feld und aufklappbare,
scrollbare Auswahl übernehmen die Themefarben. StringVar und Menüaktionen
bleiben der bestehende Auswahlvertrag; Windows und Linux verwenden weiterhin
`tk.OptionMenu` mit den bisherigen Einstellungen. Pfeiltasten, Home/End,
Anfangsbuchstaben, Enter, Escape und Tab sind vorgesehen. Navigation übernimmt
erst nach Bestätigung. Schließen, Außenklick und Zerstören geben den Grab an
einen weiterhin bestehenden modalen Aufrufer zurück. Popupkoordinaten
berücksichtigen auch außerhalb des Hauptbildschirms liegende Elternfenster.

Die Regression in `test_template_workflows` umfasst beide Auswahlfeldpfade,
Farben in Hell/Dunkel, Auswahl/Abbruch, lange Auswahlmenüs, Grab- und Trace-Cleanup,
Baumfarben, erhaltene Zweigzustände und erreichbare Aktionen bei 800×640,
1050×780 und 1500×950. Die bestehenden Detail- und Einstellungsdurchläufe
prüfen weiterhin Farbwechsel und Art-/Labelkopplung. Es gibt keine Datenmigration
und keine neue Laufzeitabhängigkeit. Native Windows-Sichtabnahme und mehrere
physische Monitore bleiben gesondert zu prüfen.
