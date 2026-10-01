# Übergabe: Glide 3.6.0

Stand: 06.09.2026

Glide 3.6.0 baut auf dem Aufgabenformat 11 von 3.5.0 auf. Die gespeicherten
Listen, Ordner, Punkte, Labels, Wiederholungen und Papierkorbeinträge bleiben
kompatibel; die persönlichen Einstellungen und Vorlagen werden additiv
erweitert.

## Umgesetzt

- Die Startseite zeigt neben Uhr und Tagesfortschritt eine Mondphase mit Name
  und Beleuchtungsanteil. Unter dem Bestand liegt eine Jahresanzeige über 371
  Tage mit 53 Wochenfeldern, aktiven Tagen, Summe, bestem Tag und laufender
  Serie.
- Vorlagen liegen in `vorlagen.json` und sind über die eigene Vorlagenseite
  verfügbar. Es gibt zehn Listenvorlagen sowie Projekt- und
  Veranstaltungsordner. Vorlagen können als `.glidetemplates` exportiert,
  ergänzt, verwendet und aus Listen oder Ordnern erzeugt werden.
- Listen und Ordner lassen sich als verlustfreies `.glidebackup`-Teilformat
  ausgeben. „Listen/Ordner hinzufügen“ ergänzt einen bestehenden Bestand mit
  neuen IDs, statt ihn zu ersetzen.
- Der Datenordner kann über `%APPDATA%\\Glide\\datenordner.json` gerätebezogen
  gewählt werden. Beim Öffnen entsteht darin `glide.lock`; ein noch aktiver
  Fremdprozess wird mit Rechner und Startzeit gemeldet. Der Ordnerumzug kopiert
  Dateien und löscht den bisherigen Bestand nicht.
- Optionale TTF-/OTF-Dateien unter `src/glide/resources/fonts/` werden privat
  registriert. Ohne Datei bleibt die bisherige Tk-Schrift aktiv. Familie,
  Größe, Wochenbeginn, Sekundenzeiger, Mondphase und Jahresanzeige gehören zu
  den persönlichen Einstellungen.

## Daten und Grenzen

Der Datenordner bleibt lokal. Ein Cloud-Dienst, Konto, Hintergrundabgleich,
Konfliktzusammenführung und Mehrbenutzerbetrieb sind weiterhin ausgeschlossen.
Die Sperrdatei warnt vor gleichzeitigem Zugriff, verhindert ihn aber nicht.
Die Tageshistorie liegt in `settings.json` und ist gerätespezifisch; sie gehört
nicht zu einem Aufgabenbackup.

## Prüfung

Die automatisierten Suiten werden mit einer isolierten Ablage ausgeführt:

```text
GLIDE_DATA_DIR=<separater Ordner> python tests/tools/pruefen.py --modus schnell --protokoll tests/qa-3.6.0/abschluss
```

Zusätzlich prüft `tests/integration/test_glide_36.py` Mondphase,
Jahresstatistik, Einstellungsmigration und Vorlagenschema. Die Sichtprüfung
unter einer echten Windows-Skalierung und die vollständige macOS-Abnahme
bleiben manuelle Release-Schritte.
