# Werkzeuge

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10.

Hilfsprogramme rund um die Prüfung. Die Analysen und Generatoren liefern
Material; `pruefen.py` bündelt die automatisierten Prüfungen und meldet Fehler.
Die drei einzeln ausführbaren Suiten stehen in `tests/README.md`.

## pruefen.py

Ein Aufruf startet Syntaxprüfung aller aktuellen Python-Dateien, Versionsabgleich
(`VERSION`, `APP_VERSION`, Hauptsuite, oberster nummerierter Changelog-Eintrag),
Dokumentationsindex und lokale Markdown-Dateilinks, Fixture-Versionen, alle drei
Suiten und beide Analysewerkzeuge. Es setzt keine Version automatisch hoch und
führt weder Änderungen an Nutzerdaten noch Commits aus.

```
python tests/tools/pruefen.py --modus schnell
python tests/tools/pruefen.py --modus voll --protokoll PFAD_ZUM_QA_ORDNER
```

Der Vollmodus erzeugt die Beispiel- und Releasedaten zusätzlich in einem temporären Ordner
neu und vergleicht Inhalt, Verknüpfungen und relative Fristen mit dem vorhandenen
Fixture. Zufällige IDs und Erzeugungs-/Löschzeitstempel bleiben beim Vergleich
ausgenommen. Das vorhandene Fixture wird dabei nicht überschrieben. Eine
Abweichung fordert zur gezielten Neuerzeugung und Prüfung auf. Die eigentliche
Import- und Schemaprüfung übernimmt weiterhin die Hauptsuite. Für Releasedaten
liest der Lauf den Planungsstichtag aus dem Fixture und übergibt ihn dem
Erzeuger; dadurch bleiben auch Datumsangaben in den Beschreibungen identisch.

Im Vollmodus werden unter Linux/X11 zusätzlich Aufnahmen erzeugt. Unter Windows
ruft er `releasedaten.py --screenshot` auf, das den tatsächlich importierten
Releasebestand in Hell und Dunkel aufnimmt. Das ersetzt keine Aufnahmen aller
anderen Dialoge und Ansichten. Fehlen unter Linux
ImageMagick oder ein Bildziel, steht der Schritt mit Grund auf „übersprungen“.
`--screenshots PFAD` erlaubt einen eigenen Bildordner; sonst verwendet der Lauf
`PROTOKOLL/screenshots`. macOS benötigt eine separate Aufnahme.
Die Bildprüfung durch einen Menschen wird niemals automatisch als bestanden
ausgegeben. Ohne `DISPLAY` verwendet Linux vorhandenes `xvfb-run` selbstständig.

Das gewählte Python muss eine funktionierende Tk-Installation haben; `pruefen.py`
benutzt denselben Interpreter für alle Unterprozesse. `--timeout SEKUNDEN`
begrenzt einen einzelnen Schritt (Standard 300). `--protokoll` erhält die
vollständigen Ausgaben und `ergebnis.json`; neue Läufe sollten einen neuen
Protokollordner verwenden, wenn ältere Nachweise erhalten bleiben sollen.

Exitcodes: **0** automatisierte Pflichtprüfungen erfolgreich, **1** mindestens
ein Fehler, **2** Pflichtsuiten wegen fehlender Tk-/Anzeigeumgebung übersprungen.
Übersprungene optionale Bilder machen den Lauf nicht rot. Audit-Befunde werden
zusätzlich zur Exitcode-Prüfung aus der Zusammenfassung erkannt. Die Analysen
bleiben Hinweisgeber und werden nicht aufgrund ihrer Verdachtszahlen rot.

Dokumentationsprüfung bedeutet Indexabdeckung einschließlich Archiv und echte
lokale Markdown-Links der nicht archivierten Dokumente;
Aussagen im Fließtext, Funktionsnamen und historische Versionsnennungen brauchen
weiterhin fachliche Prüfung. Historische Formate bleiben erhalten.

Windows-Einstieg mit frei wählbarem Python:

```powershell
.\scripts\test\run_core_tests.ps1 -Modus voll -Python 'PFAD\python.exe' -Protokoll 'PFAD\QA'
```

## screenshots.py

Erzeugt Aufnahmen der wichtigsten Ansichten in hell und dunkel – Hauptfenster,
Kopfbereich mit und ohne Labels, Eingabemaske, aufgeklappte Labelauswahl und
Kalenderfenster.

```
xvfb-run -a --server-args="-screen 0 1400x1100x24" \
    python3.12 tests/tools/screenshots.py --out /tmp/shots
```

Benötigt ImageMagick (`import`). Unter Windows und macOS ist keine Aufnahme
vorgesehen; dort wird von Hand geprüft, siehe `Manuelle_Pruefung` in der
Arbeitsvorbereitung.

Das Werkzeug baut seine Beispielablage selbst auf und setzt `GLIDE_DATA_DIR`
vor dem Import auf ein temporäres Verzeichnis. Echte Nutzerdaten werden dabei
nie berührt.

Warum es hier liegt und nicht in einem Arbeitsordner: Beim Übergang von 2.11.0
auf 2.12.0 gingen genau solche Werkzeuge verloren, weil sie nur außerhalb des
Repositorys existierten. Aufnahmen, deren Erzeuger fehlt, lassen sich später
nicht wiederholen.

## analyse_statisch.py

Liest den Syntaxbaum und fragt: Was ist definiert, wie groß, wie tief
verschachtelt, wie oft wörtlich wiederholt? Meldet nie genannte Namen, lange
Funktionen, doppelte Blöcke und verdächtige Muster.

```
python3.12 tests/tools/analyse_statisch.py [--quelle PFAD] [--grenze N]
```

## analyse_erreichbarkeit.py

Der zweite, unabhängige Weg: geht vom Programmstart aus und fragt, was von dort
erreichbar ist, welche Methoden denselben Aufbau haben und welche Attribute
geschrieben, aber nie gelesen werden.

```
python3.12 tests/tools/analyse_erreichbarkeit.py [--quelle PFAD]
```

**Beide Werkzeuge erzeugen Falsch-Positive.** Sie kennen keine Bindungen, die Tk
zur Laufzeit herstellt, und keine Aufrufe über Zeichenketten. Jeder Fund ist ein
Verdacht, kein Befund – vor dem Löschen immer den echten Aufrufer im Quelltext
suchen. In der Vergangenheit wurden `LabelChip.set_colors`, `format_file_size`,
`_store_pending_attachments` und `refresh_scrollbar_state` fälschlich als
unerreichbar gemeldet; alle vier sind in Benutzung.

## beispieldaten.py

Erzeugt `tests/fixtures/beispiele/Glide_Beispieldaten.glidebackup` – einen
ausführlichen Beispielbestand zum Einlesen über „Datei → Komplettbackup laden“.
Der Inhalt steht im Quelltext des Werkzeugs.

```
xvfb-run -a python3.12 tests/tools/beispieldaten.py [--ziel PFAD]
```

Nach jeder Änderung am Werkzeug muss die Datei neu erzeugt werden: Der
Integrationstest prüft Umfang, Artenverteilung, Labelverweise und
Palettenabdeckung. `pruefen.py --modus voll` deckt zusätzlich Abweichungen
zwischen Erzeuger und vorhandener Datei auf.

## releasedaten.py

Erzeugt `tests/fixtures/beispiele/glide_releaseplanung_3.3.0.glidebackup` mit
den drei Arbeitslisten für Unterlagen und Assets, Vermarktungsstrategie und
Feature-Übersicht. Quellen und Abrufdatum stehen in den Punktbeschreibungen;
offene Inhaberentscheidungen bleiben als solche markiert.

```
python tests/tools/releasedaten.py [--ziel PFAD] [--stichtag YYYY-MM-DD] [--screenshot PFAD.png]
```

Der Stichtag steuert die relativen Planungsfristen. Das Werkzeug importiert
`app.pyw` erst nach Setzen von `GLIDE_DATA_DIR`; der echte Nutzerdatenbestand
bleibt unangetastet. Die Datei enthält alle drei Inhalte gemeinsam, weil ein
Komplettbackup beim Laden den gesamten Bestand ersetzt. Die Hauptsuite prüft
das erzeugte Fixture. `--screenshot` benötigt Windows und erzeugt zusätzlich
`PFAD_dunkel.png`; die Aufnahme verwendet nur die Standardbibliothek und Win32.
`pruefen.py --modus voll` prüft außerdem die Reproduktion zum ursprünglichen
Planungsstichtag.

## Archiv

`archiv/README_3.2.0_vor_bestandsanalyse.md` bewahrt die vorherige Beschreibung
der vier Werkzeuge. Sie wurde am 04.09.2026 kopiert, bevor der gemeinsame
Prüfprozess und das Release-Werkzeug ergänzt wurden. Die ursprüngliche README
war bereits vollständig für die vier vorhandenen Werkzeuge; der Arbeitsauftrag
beschrieb hier einen älteren Zwischenstand.

## symbolpruefung.py

Nennt für jedes Zeichen aus `ICONS` die Schriftfamilie, aus der Tk es auf
diesem Rechner tatsächlich zeichnet, und markiert jede Ersatzschrift. Damit
lässt sich belegen, warum dieselbe Oberfläche unter Windows und unter Linux
verschieden aussieht, bevor an der Symbolauswahl etwas geändert wird.

    python tests/tools/symbolpruefung.py

Braucht eine Anzeige und ausschließlich die Standardbibliothek. Setzt
`GLIDE_DATA_DIR` selbst auf einen Testordner und rührt keine Nutzerdaten an.
