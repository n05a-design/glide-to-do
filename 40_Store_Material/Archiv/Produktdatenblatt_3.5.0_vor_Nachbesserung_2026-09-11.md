# Glide – Produktdatenblatt 3.5.0

Stand: 05.09.2026 · interner Vorabstand · Aufgabendatenformat 11

Glide ist eine lokale deutschsprachige Desktop-App für Aufgaben, Listen,
verschachtelte Ordner und kurze Notizen. Kernfunktionen benötigen kein Konto,
keinen Cloudservice und keinen Netzwerkzugriff. Laufzeitbasis: Python und Tkinter.

## Vorhandene Funktionen

- Aufgaben, Long-Tasks, Gruppen und Zwischenüberschriften; Unterpunkte,
  Beschreibungen, lokale Anhangskopien und eigene Farben.
- Listen und verschachtelte Ordner, Labels und Zuordnung in der Labelansicht.
- Fälligkeiten mit optionaler Uhrzeit, Kalender mit eigenen Fälligkeiten,
  Suche, Filter, Sortierung, Mehrfachauswahl und Rückgängig.
- Wiederholungen: täglich, alle N Tage, feste Wochentage, wöchentlich,
  monatlich oder jährlich, optional mit Enddatum. Beim Abhaken rückt derselbe
  Punkt weiter; Monats-/Jahresreihen rechnen vom Ursprungstermin.
- Persönliche Startseite mit Uhr, nächster eigener Fälligkeit, Tagesziel,
  lokalen Abschlusszahlen, zuletzt bearbeiteten Listen und drei wechselnden
  Angeboten aus zehn eingebauten Vorlagen.
- Gerätespezifische Einstellungen einschließlich Begrüßungsname, Textlogo,
  Logofarbe, Startansicht und Tagesziel; Hell-/Dunkelansicht und thematisierte Dialoge.
- Papierkorb für Punkte, Listen und Ordner, rotierende JSON-Sicherungen,
  portable Komplettbackups mit Anhängen sowie TXT-Import und TXT-/Markdown-/CSV-Export.

Nutzerdaten liegen standardmäßig im Benutzerordner, unter Windows in
`%APPDATA%/Glide`. `GLIDE_DATA_DIR` kann die Ablage überschreiben.
Die Aufgaben verwenden Format 11; ältere portable Backups werden ab Format 4
geprüft und additiv eingelesen. Ein Komplettimport ersetzt den geöffneten Bestand.
Persönliche Einstellungen und Tageszahlen sind nicht Teil des Aufgabenbackups.

## Prüfstand und Grenzen

Windows-Vollprüfung vom 05.09.2026 bestanden: Python 3.12.7 (64 Bit),
Tcl/Tk 8.6.13. Fünf Suiten, zwei Analysen, Fixtures und beide Daten-Reproduktionen.
Zusätzlich 14 Zustände der Wiederholungsmaske bei 700 Pixel Höhe geprüft.
Die Windows-Aufnahmen wurden angesehen; Symbolgrößen unterscheiden sich wegen
der tatsächlich verwendeten Schriftfamilien. Eine optische Vereinheitlichung
ist noch keine umgesetzte Änderung.

Offen bleiben echte Langzeitbedienung, weitere DPI/Monitore, macOS-/Linux-
Zielplattformabnahme, Uhrwechsel und historische Randfälle an Label-/Punkttiefengrenzen.
Windows und macOS sind Produktziele; ein Installer, eine Mindestbetriebssystem-
Zusage und eine Storefreigabe sind daraus nicht abzuleiten.

Nicht vorhanden: Cloud-Synchronisation, Mehrbenutzerbearbeitung, externe
Kalenderanbindung, Benachrichtigungen, Telemetrie, eigene Vorlagenverwaltung
oder ein Dialog zum Wechsel des Datenordners. Installer, Signierung, rechtliche
Anbieter-/Lizenzfreigaben und die Paketversion der ersten Einreichung bleiben offen.
Die Unterlagen enthalten keine abgeschlossene rechtliche oder Storeprüfung.

Quellen: [App-Quellcode](../01_Repository/Glide/src/glide/app.pyw),
[Wiederholungen](../01_Repository/Glide/docs/15_WIEDERHOLUNGEN_3.5.0.md),
[QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md),
[Release-Checkliste](../01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md).
Das ausführlichere Produktdatenblatt 3.3.0 bleibt historische Referenz.
