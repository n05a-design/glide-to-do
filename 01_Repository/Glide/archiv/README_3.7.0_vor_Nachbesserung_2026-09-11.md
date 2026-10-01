# Glide 3.7.0

Glide ist eine lokale deutschsprachige Desktop-App für Aufgaben, Listen,
verschachtelte Ordner und Notizen. Kernfunktionen benötigen kein Konto, keinen
Server und keine Internetverbindung.

## Aktueller Stand

- Kanonische App: [src/glide/app.pyw](src/glide/app.pyw).
- Aufgabenformat 12; Einstellungen 2; Vorlagen 1.
- Lokaler Entwicklungsstand mit Windows-Prüfung, kein signiertes Store-Release.
- [Vollständiger Funktionsabgleich](docs/25_FEATURE_ABGLEICH_3.7.0.md),
  [QA und Grenzen](docs/07_QA_BERICHT.md),
  [Historische Leistungsmessung 3.6](docs/21_LEISTUNGSBERICHT_3.6.0.md),
  [Material- und Glasbericht](docs/19_GLASS_SURFACE_3.6.0.md).

Der weitergeführte Funktionsumfang ergänzt und vervollständigt die Vorlagenseite mit geschützter Bearbeitung,
portable Listen-/Ordner-Teilbackups samt Anhängen, die Datenordnerwahl mit
Sperrhinweis und Schreibschutz, Mondphase, Jahresaktivität, private
Schrifteinbettung und erweiterte Einstellungen. Die Seitenleiste ist
zweispaltig ausgerichtet, Anlegemasken sind vollständig, Punktarten und Ziele
farbig, einzeilige Punkte direkt umbenennbar.

Die Materialoptik aus getönten Flächen und Glaskanten ist abschaltbar.
Echter selektiver Desktop-Blur durch die Tk-Seitenleiste gehört nicht zum
nachgewiesenen Funktionsumfang.

## Starten und Daten

```powershell
C:\Python312\python.exe src/glide/app.pyw
```

Vier TTF-Dateien und ihre Lizenz unter `src/glide/resources/fonts` mitführen.
Sie werden privat registriert. Unter Windows liegen die Standarddaten in
`%APPDATA%\Glide`. Datei → Datenordner zeigt die tatsächliche Ablage.
`GLIDE_DATA_DIR` hat Vorrang vor einer gespeicherten Datenordnerwahl.

Ein Komplettimport ersetzt den Aufgabenbestand. „Listen/Ordner hinzufügen“
ergänzt ihn. Aufgabenbackups enthalten Anhänge, aber keine persönlichen
Einstellungen oder den separaten Vorlagenkatalog. Für eine vollständige Ablage
alle Dateien des Datenordners bei geschlossener App sichern.

## Prüfung

```powershell
C:\Python312\python.exe tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.7.0/automatisch
```

Die Tests verwenden eigene isolierte Datenordner. Der Lauf enthält zehn Suiten,
zwei Analysen, Versions-/Dokumentationsprüfung, Fixture-Reproduktion und
Windows-Bilder. Der [QA-Bericht](docs/07_QA_BERICHT.md) nennt den tatsächlichen
Abschlussstatus und die manuellen Grenzen.

Alle Arbeitsunterlagen: [Dokumentationsindex](docs/00_INDEX.md).
Ältere Versionsbeschreibungen bleiben im [Änderungsverlauf](CHANGELOG.md) und
in den Archiven erhalten.

## Neu in 3.7.0

Kompakte Kacheln über die volle Breite, direktes Bearbeiten, zweispaltige Details mit Farben, Labels und Anhängen an Listen und Ordnern, korrigiertes Scrollen und Datumsanzeige im Jahresraster. [Änderungen, Migration und Prüfnachweis](docs/24_VERSION_3.7.0.md). Die zuvor genannten 3.6-Berichte bleiben historische Grundlagen.
