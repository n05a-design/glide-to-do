# Referenzdaten und Beispiele

Aktueller Aufgabenstand: **Glide 3.25.0 / Format 16**. `current_v16` enthält
die feste Referenz für aktuelle Daten. Historische Formatordner bleiben für
Migrationen erhalten; sie werden nicht auf den aktuellen App-Stand
umetikettiert.

Unter `beispiele` liegen `glide_beispieldaten.glidebackup` und
`glide_releaseplanung_3.22.0.glidebackup`. Beide werden im Vollmodus mit den
aktuellen Erzeugern reproduziert und verglichen.

## Warum hier einundzwanzig Releaseplanungen aktiv liegen

`glide_releaseplanung_3.5.0` bis `glide_releaseplanung_3.21.4` liegen
**absichtlich** alle im aktiven Ordner und gehören **nicht** ins Archiv. Die
Fixtureprüfung liest jede `*.glidebackup` und erwartet bei einem
versionierten Dateinamen genau die Version aus dem Namen – ohne Namen die
aktuelle. Diese Reihe ist damit der Nachweis, dass jede Formatstufe weiterhin
lesbar ist. Wer sie aufräumt, nimmt dem Prüfstand seine Migrationsbelege.

Vorfassungen der **unversionierten** Bestände sind dagegen zu archivieren:
`glide_beispieldaten.glidebackup` wird bei jedem Stand ersetzt, seine
Vorfassung liegt als `glide_beispieldaten_<alt>_vor_<neu>.glidebackup` in
`beispiele/archiv/`.

## Umgang mit den Beispielen

Ein Komplettimport ersetzt den Bestand. Beispiele deshalb in isolierter Ablage
öffnen oder bewusst über „Listen/Ordner hinzufügen“ ergänzen.

Der Vollprüflauf vergleicht Struktur, Inhalte, Verknüpfungen und relative
Fristen; zufällige IDs, Erzeugungszeit und die Zeitpunkte des Änderungsverlaufs
(`history[].at`) sind ausgenommen – sie entstehen beim Speichern und könnten
zwischen zwei Erzeugungen nie gleich sein. Die Tabellenansicht, „Mein Tag“,
Filter und Reiter/Pinnwand bleiben Einstellungen der App und werden nicht in
ein Aufgabenbackup geschrieben.
