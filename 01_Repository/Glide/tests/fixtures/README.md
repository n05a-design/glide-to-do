# Referenzdaten und Beispiele

Aktueller Aufgabenstand: **Glide 3.33.8 / Format 20**. `current_v20` enthält
die feste Referenz für aktuelle Daten.

- Enthalten sind die Tagebuchseiten aus Format 19, dazu Punkte mit
  Verknüpfung, „wartet auf“, Uhrzeit, erfasster Zeit und Erledigt-Zeitpunkt.
- Dazu kommen Pixelsymbole an Liste und Ordner, eine archivierte Liste und
  eine 32er-Zeichnung (Dokumentversion 2).
- Die Datei ist ein Fixpunkt der Normalisierung; `test_features330.py` prüft
  das.
- `current_v19` bleibt die Referenz für Format 19. Historische Formatordner bleiben für
Migrationen erhalten; sie werden nicht auf den aktuellen App-Stand
umetikettiert.

Unter `beispiele` liegen `glide_beispieldaten.glidebackup`, `glide_rundgang.glidebackup` und die Releaseplanungen. Beispieldaten und die Releaseplanung der aktuellen Version werden im Vollmodus mit den aktuellen Erzeugern reproduziert und verglichen.

`glide_rundgang.glidebackup` ist ein Teilbackup mit dem Ordner „Rundgang“ – je eine Liste, Notiz, Seite und Zeichnung. Die Seite erklärt die Funktionen mit fünf Aufnahmen des Glide-Fensters; diese Bilder liegen unter `rundgang/` und zeigen nur künstliche Beispieldaten. Erzeuger: `tests/tools/rundgang.py`; `test_bilder330` liest die Datei ein. Der Rundgang wird nicht im Vollmodus neu erzeugt, weil die Seitenbilder über den sichtbaren Seiteneditor eingesetzt werden.

`showcase/` enthält den Showcase (Teil-, App-Backup, Vorlagen, Starter, Manifest) und unter `bilder/` die sechs Originalmotive; `quellen.json` belegt sie per SHA-256. Erzeuger `tests/tools/showcase.py`, Prüfung `tests/tools/pruefe_showcase.py`, Auslieferung nach `05_Probelisten_Testdaten/Showcase` mit `scripts/pflege/showcase_abgleich.py`.

## Releaseplanungen

Die Fixtureprüfung liest jede `glide_releaseplanung_<Version>.glidebackup` und erwartet genau die Version aus dem Namen und das zugehörige Datenformat. Seit 03.10.2026 bleiben (Regel „Archivalter“ der Ablageprüfung):

- die Releaseplanungen der sieben neuesten Versionen;
- je älterer Formatstufe ab Format 11 die letzte Releaseplanung als Lesbarkeitsbeleg (3.6.0, 3.7.0, 3.13.0, 3.18.0, 3.21.4, 3.25.0, 3.26.0, 3.28.0, 3.29.0);
- 3.30.0, die `test_tempo330` als feste Messgrundlage liest.

Ältere Fassungen trägt Git. Vorfassungen der unversionierten Bestände (`glide_beispieldaten`, `glide_rundgang`, Showcase) ebenfalls; Archivkopien weist die CI-Grundstufe zurück.

## Umgang mit den Beispielen

Ein Komplettimport ersetzt den Bestand. Beispiele deshalb in isolierter Ablage
öffnen oder bewusst über „Listen/Ordner hinzufügen“ ergänzen.

Der Vollprüflauf vergleicht Struktur, Inhalte, Verknüpfungen und relative
Fristen; zufällige IDs, Erzeugungszeit und die Zeitpunkte des Änderungsverlaufs
(`history[].at`) sind ausgenommen – sie entstehen beim Speichern und könnten
zwischen zwei Erzeugungen nie gleich sein. Die Tabellenansicht, „Mein Tag“,
Filter und Reiter/Pinnwand bleiben Einstellungen der App und werden nicht in
ein Aufgabenbackup geschrieben.
