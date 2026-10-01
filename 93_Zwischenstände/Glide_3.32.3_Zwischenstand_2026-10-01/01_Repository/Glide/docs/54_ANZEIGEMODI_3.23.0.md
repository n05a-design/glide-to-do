# Anzeigemodi der Listenansicht – Glide 3.23.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · Einstellungen 2

## Das Problem

Bis 3.22 zeigte eine Listenzeile von einer Checkliste nur den Stand „☑ 2/5“ und
von Anhängen nur ihre Zahl. Wer wissen wollte, welche Schritte offen sind,
musste jeden Punkt einzeln öffnen.

Bei einem Dokument mit 42 Hauptpunkten und je fünf Schritten sind das 42
Dialoge – und genau das ist der Fall, der beim Weiterarbeiten an einer
umfangreichen KI-Antwort entsteht.

## Der Umschalter „Anzeige“

In der Filterzeile, neben „Nur offene Punkte“ – beide verändern die Sicht auf
denselben Bestand, nicht den Bestand.

| Modus | Was eine Zeile zeigt |
|---|---|
| **Kompakt** | Nur Titel, Termin und Labels. Keine Symbole für Beschreibung, Checkliste und Anhänge. |
| **Standard** | Die gewohnte Listenansicht mit diesen Symbolen. |
| **Checklisten** | Zusätzlich jeden Checklistenschritt als eigene Zeile – direkt abhakbar. |
| **Anhänge** | Zusätzlich jeden Anhang mit Namen und Größe. |
| **Erweitert** | Checklisten, Anhänge und den Anfang der Beschreibung. |

Die Wahl gilt für jede Ansicht, die Punkte als Zeilen zeigt – Liste, Ordner und
die abgeleiteten Übersichten. Die Tabelle hat eigene Spalten und braucht sie
nicht.

## Detailzeilen sind Darstellung, keine Daten

Eine Checklisten-, Anhang- oder Beschreibungszeile trägt ein eigenes
IID-Suffix (`::check0`, `::file1`, `::note0`) und gilt damit als synthetische
Zeile – wie die Fortsetzungszeilen eines Long-Tasks seit 3.4.

Daraus folgt:

- Sie zählt nicht als Punkt. `count_items` und jede Statistik bleiben
  unverändert.
- Sie erscheint nicht in der Auswahl für Punktaktionen, lässt sich nicht
  verschieben und nicht in eine Gruppe ziehen.
- Sie wandert nicht in Exporte, Backups oder den Änderungsverlauf.

**Eine Ausnahme:** Eine Checklistenzeile lässt sich abhaken. Ein Klick oder die
Leertaste schreibt dann in die Checkliste ihres Punkts, nicht in den Punkt
selbst – der bleibt offen. Das ist der Grund, warum die Schritte überhaupt in
der Liste stehen.

## Grenzen

- Höchstens **zwölf** Detailzeilen je Punkt. Ohne Grenze könnte eine Checkliste
  mit fünfzig Schritten eine Liste unbrauchbar machen; der Rest steht
  weiterhin in den Punktdetails.
- Die Beschreibung wird auf 160 Zeichen gekürzt; vollständig bleibt sie in den
  Punktdetails.
- Überschriften bekommen keine Detailzeilen: Sie tragen weder Checkliste noch
  Anhänge.
- Der gewählte Modus steht in den persönlichen Einstellungen (additiv,
  Einstellungsformat bleibt 2) und damit nicht im Aufgabenbackup.

## Umfangreiche Antworten weiterbearbeiten

Der Weg von einer langen KI-Antwort zu einer bearbeitbaren Glide-Struktur
sieht seit 3.23 so aus:

1. **Datei → Austauschformat anzeigen …** und den Text der Anfrage
   voranstellen.
2. Die Antwort als `.glideexchange` (oder als Markdown-Gliederung) sichern.
3. **Datei → KI-Ergebnis importieren …**, Vorschau prüfen, übernehmen.
4. **Anzeige: Checklisten** – jetzt stehen Hauptpunkte und ihre Schritte
   untereinander, und die Schritte lassen sich abhaken, ohne einen einzigen
   Dialog zu öffnen.

Die Hauptpunkte bleiben dabei Punkte mit eigener Nummer, Frist und Wichtigkeit;
die Schritte bleiben Schritte. Was entsteht, sieht nicht aus wie ein
unformatierter Datenimport, sondern wie eine gewachsene Liste.
