# Test-Fixtures

- `current_v11/reference_v11.json`: aktueller Format-11-Referenzbestand mit Wiederholungsregel.
- `current_v10/reference_v10.json`: historischer Referenzbestand des Datenformats 10. Erweitert den v9-Bestand um einen Papierkorbeintrag der Art `item`: ein gelöschter Punkt mit Unterpunkt, Beschreibung, Wichtigkeit und Fälligkeit, dazu seine Herkunft (Liste und Position). Weist nach, dass ein gelöschter Punkt Speichern, Laden und Wiederherstellen an dieselbe Stelle übersteht.
- `current_v9/reference_v9.json`: Sollstand des Datenformats 9. Erweitert den v8-Bestand um zwei Verschachtelungsebenen (`parent_id`), eine Liste im doppelt verschachtelten Ordner und einen Long-Task mit echten Zeilenumbrüchen.
- `current_v8/reference_v8.json`: Sollstand des historischen Datenformats 8. Erweitert den v7-Bestand um die beiden festen Labels (`system`), eine Zwischenüberschrift, zwei Long-Tasks – einer davon absichtlich ohne das feste Label, damit der Abgleich beim Laden nachweisbar ist – und einen Punkt mit unbekannter Art, der als gewöhnliche Aufgabe laden muss.
- `current_v7/reference_v7.json`: Sollstand des historischen Datenformats 7. Erweitert den v6-Bestand um zwei Labels mit eigener Farbe, um Labelzuweisungen an mehreren Punkten, um einen absichtlich ungültigen Verweis auf ein gelöschtes Label sowie um einen Papierkorb mit einer gelöschten Liste (inklusive Herkunftsordner) und einem gelöschten Ordner.
- `current_v6/reference_v6.json`: Referenzbestand des Datenformats 6. Enthält Eingang, Ordner, Listenfarbe, Beschreibungstexte, eine Gruppe mit verschachtelter Untergruppe, eine Aufgabe außerhalb jeder Gruppe sowie Fälligkeit, Wichtigkeit und erledigten Unterpunkt. Dient zusätzlich dem Nachweis, dass ein Bestand ohne `labels` und `trash` unverändert lädt.
- `current_v5/reference_v5.json`: Referenzbestand des Datenformats 5. Dient dem Nachweis, dass ein Bestand ohne Feld `kind` vollständig als Aufgaben lädt.
- `current_v4/reference_v4.json`: Referenzbestand des Datenformats 4 ohne Aufgabenfarbe.
- `legacy_v2/probelisten_5_listen_v2.json`: größerer Altbestand des Datenformats 2 für Migrationstests.

Alle neun Bestände werden vom Integrationstest durch die aktuelle Normalisierung geführt.

## Beispieldaten zum Einlesen

- `beispiele/Glide_Beispieldaten.glidebackup`: ausführlicher Beispielbestand zum
  Ausprobieren – kein Testbestand, sondern ein Komplettbackup, das sich über
  „Datei → Komplettbackup einlesen“ in eine leere Ablage importieren lässt.
  Zehn Listen in fünf teils verschachtelten Ordnern, rund 140 Punkte aus
  Exposé-Produktion, Kampagne, Vermarktungsstart, Baustellenkommunikation und
  einem Gestaltungsregelwerk, dazu neun Labels über alle sieben Palettenfarben,
  ein gefüllter Papierkorb und mehrzeilige Notizen als Long-Tasks.

  Erzeugt wird die Datei von `tests/tools/beispieldaten.py`; der Inhalt steht
  dort im Quelltext und ist damit nachvollziehbar und änderbar. Alle Fristen
  entstehen relativ zum Erzeugungstag. Der Integrationstest liest die Datei
  auf demselben Weg ein wie ein echter Import und prüft Umfang, Artenverteilung
  und Labelverweise – sie kann also nicht unbemerkt veralten.

## Releaseplanung 3.5.0

- `beispiele/glide_releaseplanung_3.5.0.glidebackup`: drei Arbeitslisten
  **Unterlagen & Assets**, **Vermarktungsstrategie**, **Feature-Übersicht**
  im Ordner **Releaseplanung 3.5.0**, zusätzlich ein geschützter leerer Eingang.
  119 Punkte: 82 Aufgaben, zehn Gruppen, elf Long-Tasks und 16 Überschriften;
  neun Labels. Keine Aufgabe ist abgehakt.
- Planungsstichtag: 05.09.2026. Code-/Redaktionsstand: 3.5.0 / Format 11.
  Webrecherche: 04.09.2026, Microsoft-Textvorgaben zusätzlich am 05.09.2026 geprüft.
- Erzeuger: `tests/tools/releasedaten.py`; `--stichtag 2026-09-05` reproduziert
  die Fristen. Zufalls-IDs und Exportzeitpunkte sind keine Inhaltsunterschiede.
- Alte Release-Fixtures 3.2.0, 3.3.0 und 3.4.0 liegen nur im `archiv/`.
- Windows-Vollprüfung einschließlich echtem Import und Inhaltsabgleich bestanden;
  Nachweis unter `tests/qa-3.5.0/abschluss/`.

**Import ersetzt den gesamten bisherigen Bestand.** Zuerst ein eigenes
Komplettbackup erstellen; zum Ausprobieren vorzugsweise eine separate Ablage
über `GLIDE_DATA_DIR` öffnen. Danach **Datei → Komplettbackup laden …** und
diese eine Datei auswählen. Es handelt sich nicht um drei nacheinander zu
ladende Backups. Die automatisch erzeugte Sicherung vor Import ist eine
zusätzliche Rückfallebene.

Der frühere README-Stand 3.2.0 vor dieser Ergänzung bleibt in
`archiv/README_3.2.0.md` erhalten. Grund: Fortschreibung um die recherchierte
Releaseplanung; die historischen Format-Fixtures bleiben an ihrem Platz.

Tests dürfen niemals echte Nutzerdaten ersetzen. Die Isolierung läuft über die Umgebungsvariable `GLIDE_DATA_DIR`; `APPDATA` allein wirkt nur unter Windows.
