# Manuelle Prüfung – Glide 3.21.1

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15

3.21.1 behebt Zeitzonenfehler. Die automatisierten Suiten deckenden Rundlauf ab; von Hand
zu prüfen bleibt, was nur ein fremdes Kalenderprogramm zeigen kann.

## Vor der Prüfung

- [ ] Eigenen Datenordner sichern oder `GLIDE_DATA_DIR` auf einen leeren Ordner setzen.
      Nie mit echten Nutzdaten prüfen.
- [ ] Systemzeitzone notieren. Für die Prüfung ist eine Zone **mit** Versatz nötig –
      in UTC zeigt sich der behobene Fehler grundsätzlich nicht.

## Rundlauf mit Enddatum

- [ ] Aufgabe mit Uhrzeit anlegen, Wiederholung „an Wochentagen" mit **Enddatum
      31.01.2027**. Über Datei → Kalenderausgabe als `.ics` schreiben.
- [ ] Datei in einem Texteditor öffnen: Die `RRULE` muss auf `UNTIL=20270131T235959`
      enden – **ohne** „Z".
- [ ] Dieselbe Datei über Datei → „Kalenderdatei (ICS) importieren …" einlesen. Das
      Enddatum der Wiederholung muss wieder **31.01.2027** lauten, nicht der 01.02.
- [ ] Denselben Rundlauf mit einer ganztägigen Aufgabe: Die `RRULE` muss auf
      `UNTIL=20270131` enden, ohne Uhrzeit.

## Fremde Kalender

- [ ] Wiederkehrenden Termin mit Enddatum in Apple Kalender, Outlook oder Google Kalender
      anlegen und als `.ics` exportieren. Diese Programme schreiben das Tagesende
      üblicherweise als `…T235959Z`.
- [ ] Datei in Glide importieren: Das Enddatum muss dem im fremden Programm angezeigten
      Tag entsprechen, nicht dem Folgetag.
- [ ] Eine mit 3.21.1 geschriebene Datei in dasselbe fremde Programm einlesen: Die Reihe
      muss am 31.01.2027 enden und der letzte Termin an diesem Tag noch erscheinen.

## Zeitzonenwechsel

- [ ] Systemzeitzone auf eine Zone **westlich** von Greenwich stellen (etwa
      Amerika/New York), Glide neu starten, Rundlauf wiederholen. Enddatum muss gleich
      bleiben.
- [ ] Zone auf eine weit **östliche** stellen (etwa Pacific/Kiritimati, UTC+14),
      wiederholen. Enddatum muss gleich bleiben.
- [ ] Ursprüngliche Zone wiederherstellen.

## Sichtprüfung

- [ ] Der Importdialog bei 780 × 640 in Hell und Dunkel vollständig erreichbar,
      Vorschau lesbar, Schaltflächen nicht abgeschnitten.
- [ ] Abschlussmeldung nennt angelegte Punkte, übersprungene Termine mit Grund und nicht
      lesbare Felder.

## Bestand

- [ ] Rückgängig nimmt einen Import samt neu angelegter Labels vollständig zurück.
- [ ] Abbrechen und Escape lassen den Bestand unverändert.
- [ ] Ein Bestand aus 3.21.0 öffnet unverändert; kein Formatsprung, keine Sicherung nötig.

## Offen und nicht Teil dieser Prüfung

Native Sichtabnahme unter Windows, DPI- und Mehrmonitorprofile, Screenreader,
Langzeitbetrieb, Installer und Signierung.
