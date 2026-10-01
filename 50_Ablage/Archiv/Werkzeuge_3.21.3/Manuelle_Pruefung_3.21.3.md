# Manuelle Prüfung – Glide 3.21.3

Stand: 14.09.2026 · Glide 3.21.3 · interner Entwicklungsstand · Aufgabenformat 15

3.21.3 ändert keinen Anwendungscode. Zu prüfen ist, ob die Dokumentation jetzt
lückenlos den tatsächlichen Stand wiedergibt, ob die Archivierung stimmt und ob
die eine inhaltliche Korrektur im Beispielbestand sichtbar ist. Der
automatisierte Teil steckt in `tests/tools/standpruefung.py`; diese Liste prüft,
was eine Maschine nicht prüfen kann.

## Vor der Prüfung

- [ ] Eigenen Datenordner sichern oder `GLIDE_DATA_DIR` auf einen leeren Ordner
      setzen. Das Wiederherstellen eines App-Backups **ersetzt** den Bestand.
- [ ] `05_Probelisten_Testdaten/Glide-Funktionsvorschau_3.21.3.glidebackup` über
      „Listen/Ordner hinzufügen …" einlesen.

## Standprüfung

- [ ] `python3 tests/tools/standpruefung.py` im Repository: Exitcode 0, keine
      Befunde. Die Ausgabe nennt die Zahl der fortgeschriebenen und
      festgeschriebenen Dokumente – beide Zahlen sollten plausibel sein
      (rund 50 fortgeschrieben, rund 40 festgeschrieben).
- [ ] Gegenprobe, dass die Prüfung wirklich greift: In einer **Kopie** eines
      READMEs die Version auf 3.21.0 setzen und die Prüfung erneut laufen
      lassen. Sie muss die Datei mit Regelnummer melden. Danach die Kopie
      entfernen.
- [ ] `grep -rIlF "3.21.2" --include="*.md" .` – die Treffer dürfen nur
      Belegstellen sein: Archivnamen (`_vor_3.21.2`), der Werkzeugordner, der
      Prüfbeleg `tests/qa-3.21.2/abschluss` und die Abschnitte zu 3.21.2 in
      Änderungsverlauf, QA-Bericht und Weitergabe.

## Dokumentation

- [ ] Wurzel-README, `01_Repository/Glide/README.md`, `docs/00_INDEX.md`,
      `10_Dokumentation/README.md` und das Produktdatenblatt nennen **3.21.3**.
- [ ] `01_Repository/Glide/README.md` hat einen Aufmacher zu 3.21 statt zu 3.15.
- [ ] `docs/08_CODE_BEFUND.md`, `11_BESTANDSANALYSE.md`,
      `12_ABSCHLUSSBERICHT.md`, `25_FEATURE_ABGLEICH_3.7.0.md`,
      `28_ABLAGEPRUEFUNG_2026-09-11.md` und
      `30_DOKUMENTATIONSABGLEICH_2026-09-12.md` tragen **kein** Banner
      „Aktueller Entwicklungsstand" mehr, sondern einen Verweis ohne Nummer.
- [ ] `docs/09_PROJECT_HANDOFF.md`: genau **eine** Stelle sagt „das zuletzt
      umgesetzte Funktionspaket". Die Ideenzeile nennt nur Offenes – kein
      Änderungsverlauf, kein CSV-Import.
- [ ] Der Satz über die durchgehende Grundlage steht wortgleich in Wurzel-README,
      Repository-README, Weitergabe und Produktdatenblatt-Umfeld.
- [ ] Im Dokumentationsindex trägt kein Linktext eines fortgeschriebenen
      Dokuments eine Versionsnummer („QA-Bericht", nicht „QA-Bericht 3.21.0").
- [ ] Genau **eine** aktive Weitergabedatei in `00_Arbeitsvorbereitung`.

## Archivierung

- [ ] `07_Python-Versionen` enthält aktiv nur
      `Glide-Aufgaben-und-Listen_v3.21.3.pyw`, den README, `resources/` und
      `Archiv/`. Die Fassungen 3.14.0 bis 3.21.2 liegen im Archiv.
- [ ] Die startbare Fassung 3.21.3 startet und zeigt in „Über Glide" die
      Version 3.21.3.
- [ ] `Claude outputs` ist leer; die drei ZIP-Pakete liegen unter
      `50_Ablage/Archiv/Uebertragungspakete`.
- [ ] `05_Probelisten_Testdaten` enthält aktiv nur die drei 3.21.3-Dateien und
      den README; alle älteren Fassungen liegen in `Archiv/`.
- [ ] `00_Arbeitsvorbereitung/Notizen`, `Checklisten` und `Entscheidungen`
      enthalten je nur die 3.21.3-Fassung; die 3.21.2-Fassungen liegen im
      jeweiligen `Archiv/`.
- [ ] `tests/fixtures/beispiele` enthält weiterhin **alle** versionierten
      Releaseplanungen von 3.5.0 bis 3.21.3. Sie gehören dorthin und dürfen
      nicht archiviert werden.

## Beispielbestand

- [ ] Die Liste „Kalender, Erinnerungen und Tagesplanung" im Ordner
      „Website-Betrieb" hat jetzt eine **Farbe** (Braun). Bis 3.21.2 hatte sie
      keine, weil der Erzeuger einen unbekannten Farbwert setzte.
- [ ] „Ablage & Ideen" bleibt die einzige Liste ohne Farbe – das ist gewollt.
- [ ] Ansicht → Tagesplanung, heutiger Tag: **sechs** Punkte, Summe **270
      Minuten**; morgen **ein** Punkt mit 120 Minuten.
- [ ] Beide Erinnerungsarten stehen an „Rückruf Bauträger" (relativ, 30 Minuten)
      und „Angebotsfrist Parkquartier" (fest, Vortag 8 Uhr).
- [ ] Alle sechs Wiederholungsarten sind vertreten; die Wochentagsserie
      Mo/Mi trägt ein Enddatum.

## Kalenderrundlauf (unverändert gegenüber 3.21.2, hier als Rückfallprüfung)

- [ ] Kalenderausgabe als ICS für die Liste, Datei im Texteditor ansehen:
      `UNTIL` steht **ohne „Z"** und beim Ganztagstermin als reines Datum.
- [ ] Dieselbe Datei importieren: alle Termine als Duplikate übersprungen.
- [ ] Gegentest mit ersetzten `UID:`-Zeilen: Aufgaben entstehen, das Serienende
      bleibt der 140. Tag – auch nach einem Wechsel der Systemzeitzone.

## Prüflauf

- [ ] `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.21.3/abschluss`
      auf dem Mac: Exitcode 0, **neununddreißig** Schritte, davon
      siebenunddreißig ausgeführt; übersprungen bleiben allein die
      plattformgebundene Screenshot-Erzeugung und die Sichtprüfung.

## Offen und nicht Teil dieser Prüfung

Native Sichtabnahme unter Windows, DPI- und Mehrmonitorprofile, Screenreader,
Langzeitbetrieb, Installer und Signierung.
