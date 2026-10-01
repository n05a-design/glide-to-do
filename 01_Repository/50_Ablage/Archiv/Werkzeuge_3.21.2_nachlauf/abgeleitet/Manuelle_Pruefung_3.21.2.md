# Manuelle Prüfung – Glide 3.21.2

Stand: 14.09.2026 · interner Entwicklungsstand · Aufgabenformat 15

3.21.2 ändert keinen Anwendungscode. Zu prüfen ist, ob der erweiterte
Beispielbestand hält, was er verspricht – und ob die Ablage stimmt.

## Vor der Prüfung

- [ ] Eigenen Datenordner sichern oder `GLIDE_DATA_DIR` auf einen leeren Ordner
      setzen. Das Wiederherstellen eines App-Backups **ersetzt** den Bestand.
- [ ] Systemzeitzone notieren. Für die Kalenderschritte ist eine Zone **mit**
      Versatz nötig; in UTC zeigen sich Zeitzonenfehler grundsätzlich nicht.
- [ ] `05_Probelisten_Testdaten/Glide-Funktionsvorschau_3.21.2.glidebackup` über
      „Listen/Ordner hinzufügen …" einlesen.

## Beispielbestand

- [ ] Der Ordner „Website-Betrieb" enthält die Liste „Kalender, Erinnerungen und
      Tagesplanung".
- [ ] Die Liste hat einen Anhang („Kalenderpruefung.txt"), lesbar über die
      Listendetails.
- [ ] Der Long-Task mit der Rundlaufanleitung steht vollständig in der Liste,
      vier Schritte, ohne Abschneiden.

## Tagesplanung und Tageskapazität

- [ ] Ansicht → Tagesplanung, heutiger Tag: **sechs** Punkte, Summe **270
      Minuten**.
- [ ] „Angebot ohne Schätzung" wird getrennt als Punkt ohne Aufwand ausgewiesen,
      nicht mit 0 Minuten mitgerechnet.
- [ ] „Exposé gegenlesen" ist erledigt und bleibt in der Summe – so ist die Regel
      aus 3.15 festgelegt.
- [ ] In den Einstellungen eine Tageskapazität von 240 Minuten setzen: Die
      Tagesplanung muss die Überschreitung sichtbar machen.
- [ ] Auf morgen umschalten: **ein** Punkt, 120 Minuten.

## Erinnerungen

- [ ] „Rückruf Bauträger": relative Erinnerung, 30 Minuten vor dem Termin.
- [ ] „Angebotsfrist Parkquartier": feste Erinnerung, Vortag 8 Uhr, in Ortszeit
      angezeigt.
- [ ] Bei einem fälligen Hinweis hebt Glide Dock beziehungsweise Taskleiste
      hervor. Systemzustellung bei beendetem Programm gibt es nicht.

## Wiederholungen

- [ ] Alle sechs Arten sind vertreten: täglich („Backup der Arbeitsdateien"),
      alle 14 Tage mit Ende („Freigaben nachhalten"), Wochentage Mo/Mi mit Ende
      („Baustellenbegehung"), wöchentlich („Kontaktformular"), monatlich
      („Monatsabschluss"), jährlich („Jahresabgleich Bildrechte").
- [ ] „Baustellenbegehung Mo und Mi" abhaken: Der Punkt rückt auf den nächsten
      Montag oder Mittwoch vor, es entsteht **kein** neuer Punkt.

## Kalenderrundlauf

- [ ] Liste öffnen, Datei → Kalenderausgabe als ICS, Umfang „Aktuelle Liste",
      alle Optionen an.
- [ ] Datei im Texteditor: Ganztags- (`VALUE=DATE`) und Zeittermine, `FREQ=DAILY`,
      `FREQ=WEEKLY;BYDAY=MO,WE`, `FREQ=MONTHLY`, `FREQ=YEARLY`, zwei `VALARM`.
- [ ] `UNTIL` steht **ohne „Z"** und – beim Ganztagstermin – als reines Datum.
- [ ] Dieselbe Datei importieren: Der Bericht überspringt **alle** Termine als
      Duplikate.
- [ ] Gegentest: `UID:`-Zeilen ersetzen, erneut importieren. Aufgaben entstehen,
      das Enddatum der Wochentagsserie bleibt der 140. Tag.
- [ ] Systemzeitzone auf eine westliche (Amerika/New York) und eine östliche
      (Pacific/Kiritimati) Zone stellen, Rundlauf wiederholen: Enddatum
      unverändert. Danach die eigene Zone wiederherstellen.
- [ ] Rückgängig nimmt den Import samt neu angelegter Labels vollständig zurück.

## Änderungsverlauf

- [ ] Ansicht → „Änderungsverlauf …" oder Strg/Cmd+H: Der Import steht als
      Sammeleintrag darin.
- [ ] Rückgängig nimmt den Bestand zurück, **nicht** das Protokoll – so ist es
      festgelegt.

## Ablage und Dokumentation

- [ ] `05_Probelisten_Testdaten` enthält aktiv nur die drei 3.21.2-Dateien und
      den README; alle älteren Fassungen liegen in `Archiv/`.
- [ ] Der Ordner-README nennt 3.21.2 und Aufgabenformat 15 und beschreibt die
      Funktionstabelle zutreffend.
- [ ] Wurzel-README, `01_Repository/Glide/README.md` und `10_Dokumentation/README.md`
      nennen 3.21.2.
- [ ] Genau **eine** aktive Weitergabedatei in `00_Arbeitsvorbereitung`.

## Offen und nicht Teil dieser Prüfung

Native Sichtabnahme unter Windows, DPI- und Mehrmonitorprofile, Screenreader,
Langzeitbetrieb, Installer und Signierung.
