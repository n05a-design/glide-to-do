# Werkzeuge

Hilfsprogramme rund um die Prüfung. Kein Bestandteil der Testsuiten: Sie
liefern kein Ja/Nein, sondern Material zum Hinsehen.

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
Palettenabdeckung.
