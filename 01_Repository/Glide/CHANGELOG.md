# Änderungsverlauf

Stand 14.11.2026: Die Versionen 3.51.0 bis 3.33.18 sind am 14.11.2026 nach der Regel „sieben neueste ausführlich“ auf je eine Tabellenzeile gekürzt; ausführliche Einträge und die Nachträge vom 08./09.11.2026 trägt Git.

## 3.61.0 – 14.11.2026

- **Überlastungsgründe sichtbar (D81):** „Tag entlasten“ nennt unter der Vorher/Nachher-Bilanz je überplantem Tag die Gründe; ein entlasteter Tag zeigt die Gründe davor und „nachher nicht mehr überplant“. Die Einzahl lautet jetzt „1 Aufgabe ohne Aufwandsschätzung kann …“. [Handbuch](docs/20_FUNKTIONEN.md#tageskapazität-und-entlastung-seit-3550).
- **Datenordner nicht erreichbar (D82):** Statt still abzubrechen nennt Glide Pfad und Quelle (`datenordner.json` oder `GLIDE_DATA_DIR`) in einem Systemdialog und beendet sich, ohne etwas anzulegen. Ein Zeiger mit Byte-Order-Mark ist wieder gültig. [Datenvertrag](docs/06_DATA_BACKUP_MIGRATION.md#ablage).
- **Suche:** Zerlegt gespeicherte Umlaute und Akzente (NFD, etwa aus macOS-Dateinamen) werden gefunden und an der richtigen Stelle markiert.
- **Neuerungskarte:** Einträge für 3.61.0 und die sichtbaren Änderungen von 3.60.0; der Eintrag zu 3.55.0 verspricht keine Überlastungsgründe mehr.
- **Design Richtlinien:** neu geordnet mit Grundsätzen P1–P6, den sechs verbindlichen Lehren aus der Marktanalyse (D83) und einem Gestaltungsregister aller gestaltungsrelevanten Entscheidungen, Fachentscheidungen und Inhaberzitate.
- **Dokumentation:** Übergabe auf den aktuellen Stand gekürzt, Arbeitsvorrat im Entwicklungsplan, Marktbericht §16 mit den Bewegungen bis 14.11.2026, Prüfplan und Faktenkorrekturen aus der Dokumentationsprüfung; dieses CHANGELOG auf sieben ausführliche Versionen gekürzt.
- Glide-System V1.24; Datenformat 26 unverändert. Prüfumfang und Grenzen im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3610-14112026).

## Dokumentationspflege – 14.11.2026

- **Tagesbilanz:** Das [Handbuch](docs/20_FUNKTIONEN.md#tageskapazität-und-entlastung-seit-3550) beschreibt die tatsächliche Anzeige. Die mit 3.55.0 angekündigten Überlastungsgründe werden berechnet, aber noch nicht angezeigt; der Eintrag zu 3.55.0 bleibt als Verlauf stehen.
- **WA-49:** 3.55.0 brachte den ersten Schnitt, die Tk-freie Pfadauflösung. Erst seit 3.60.0 legt der Import keine Ordner mehr an; Menüaufschub und Zeigerlesen beim Import bleiben offen.
- **Datenordnerzeiger:** Der [Datenvertrag](docs/06_DATA_BACKUP_MIGRATION.md#ablage) nennt das Verhalten bei unerreichbarem Ziel und bei BOM als offenen Befund.
- **Prüfstand 3.55.0:** Nachtrag zu Version, Laufzeit und Quellhash der Messdateien im [QA-Bericht](docs/07_QA_BERICHT.md#prüfstand-3550-11112026).
- **Markt, Plan, Übergabe, Index:** Featurematrix auf 3.60.0 ergänzt und eine verschobene Tabellenzeile repariert. Planeinstieg, Statusverweise, Register WA-12/WA-49 und Risiko R1 auf den Code ausgerichtet. Befunde in der [Analyse §13.36](../../00_Arbeitsvorbereitung/Glide_Analyse.md#1336-gesamtaudit-gegen-code-und-dokumentation-14112026), Rest im [Plan §21.91](../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2191-dokumentationskorrekturen-aus-dem-gesamtaudit-14112026).
- App 3.60.0, Datenformat 26 und Glide-System V1.23.1 unverändert.

## 3.60.0 – 13.11.2026

- **Marke und Projektseite:** Neues Glide-App-Symbol und zweifarbiges In-App-Logo. Die Fläche folgt der Themenfarbe, der Schatten bleibt eigenständig sichtbar. Der Showcase „Werkhaus West“ liefert einen bearbeitbaren Projektstand und 15 verschiedene Windows-Aufnahmen.
- **Showcase auf Linux:** Dieselben vier Studio-Motive liegen in den Demo-Sicherungen und Vorlagen als PNG vor. Galerie und Seitenbilder laden auch ohne externen JPEG-Decoder.
- **Seitenleiste:** Bei mehreren angehefteten Seiten passt Glide die Baumhöhen nach dem Layout an. Der Bereich „Zeichnungen“ bleibt dadurch auch bei eingeschränkter Fensterhöhe erreichbar.

- **Einstellungen mit „Kreativ“ in kleiner Schrift:** Der Einstellungsdialog öffnet auch mit DM Serif Display und der Schriftgröße „klein“ sofort. Vorher kreisten Umbruch und Spaltenbreite vor dem ersten Anzeigen endlos über drei Werte (gemessen unter macOS mit Tk 9.0.3). Die Tk-freie Regel `ui_design.settled_wrap_width` beendet die Runde bei einer wiederkehrenden Breite; das Ergebnis der übrigen Schriftkombinationen ist unverändert.
- **Fensterlage beim Start:** Die Lageregel der Normalansicht rechnet Tk-frei in `compact_mode.keep_visible`; `ListApp.clamp_geometry` bleibt die Fassade. Verhalten unverändert.
- **Import ohne Ordneranlage (WA-49):** Der Import von `app.pyw` legt auch mit `GLIDE_DATA_DIR` keine Ordner mehr an; das übernimmt der App-Start.
- **Prüfungen:** `test_startwege.py` hält als Teil von `SUITEN` Direktstart, Schnellstart und nachgestellten Paketstarter gegen vier künstliche Ablagen fest. `test_runtime_config.py` hält die drei Auflösungen des Bytecode-Ordners gleich. `test_arbeitsmodi.py` berücksichtigt zwei Eigenschaften von Tk 9.0 unter macOS.
- Glide-System V1.23.1; Datenformat 26 unverändert. Prüfumfang und Grenzen im [QA-Bericht](docs/07_QA_BERICHT.md#technische-vollprüfung-3600-auf-pc02-14112026).

## Dokumentationspflege – 13.11.2026

- Contributing-Einstieg und README-Navigation für Mitarbeit, Roadmap, Funktionen, Architektur, Entwicklungsablauf und Qualität ergänzt.
- Führende Dokumente und Änderungsfolgen in der [Pflegematrix](docs/DOKUMENTENPFLEGE.md#zuständigkeiten-und-änderungsbezüge) zusammengeführt; Arbeitsregeln, Einstiege und Fachquellen darauf ausgerichtet.
- Shell-Konzept auf Zielarchitektur konzentriert, doppelte Modulaufzählungen ins bestehende Systemregister zurückgeführt und geplante Schnittstellen von vorhandenen Bausteinen abgegrenzt; Beschreibung von `RedoHistory` und den verbleibenden App-Kopplungen berichtigt.
- Glide-Systemkatalog als Dokumentationskorrektur auf V1.17.3 fortgeschrieben; App 3.55.1 und Datenformat 26 unverändert. Prüfumfang und Grenzen im [Nachweis](tests/qa-3.55.1/dokumentation_2026-11-13/README.md).

## 3.55.1 – 12.11.2026

- **Windows-Paketstart (lokaler Nachlauf, 13.11.2026):** Der Paketstart beschränkt den DLL-Suchpfad auf Anwendung, Paket und Windows-Systemverzeichnis. Die native Startprobe löst Pfadumleitungen vor dem Vergleich auf. Ein regulärer Paketneubau mit diesem Startskript steht aus.

- **Dateinamen unter macOS:** Die Speicherdialoge für JSON Canvas und App-Sicherung schlagen den Namen mit einfacher Dateiendung vor. Bestehende Sicherungen bleiben lesbar.

- **JSON-Canvas-Export:** Die aktive Pinnwand liefert ihre sichtbaren Karten, Positionen und Verbindungen. Der Export schreibt eine nutzbare Datei und zeigt die Formatgrenzen im Verlustbericht. Der Dateidialog und der Schutz der internen Daten sind über den App-Einstieg geprüft.

- **Tag entlasten:** Zielwahl und Rückmeldung stehen im festen Dialogfuß. Glide zeigt die Bilanz automatisch nach der Zielwahl. „Umplanen“ ist erst bei einer wirksamen Auswahl verfügbar. Fälligkeiten und gemeinsames Rückgängig bleiben erhalten.

## 3.55.0 – 11.11.2026

- **Neuerungskarte:** Die Startseite zeigt nach dem Update „Neu in Glide 3.55.0“ mit der Tagesbilanz und dem Fälligkeitserhalt. Nach „Gelesen“ bleibt der Eintrag unter Hilfe › Über Glide › Neuerungen verfügbar.

- **Tagesplanung & Kapazität (WA-12 / D57):** Transparente und handlungsorientierte Kapazitätsübersicht im Tagesentlastungs- und Planungsbereich (`planning.py`, `day_relief.py`, `app.pyw`). Exakte Berechnung von geplantem Aufgabenaufwand, belegter Kalenderzeit und verfügbarer Netto-Kapazität. Ungeschätzte Aufgaben werden transparent gesondert ausgewiesen und niemals heimlich als 0 Minuten gewertet. Konkrete Überlastungsgründe werden benannt. Im Entlastungsdialog wird die Fälligkeit von Aufgaben explizit als erhalten ausgewiesen (`Fälligkeit (bleibt)`), unterstützt von dynamischer Spaltenbreitenanpassung und atomarem Undo.
- **Architekturentkopplung & Initialisierung (WA-49):** Das Tk-freie Modul [`runtime_config.py`](src/glide/runtime_config.py) löst die Anwendungs-, Cache- und Logpfade auf. Die Pfadauflösung legt keine Verzeichnisse an. Windows verwendet für bestehende Daten weiterhin `%APPDATA%/Glide` und für den Cache standardmäßig `%LOCALAPPDATA%/Glide/Cache`.
- **Glide Shell Framework Vorbereitung:** Ausarbeitung des umfassenden Architektur- und Entkopplungskonzepts in [`docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md`](docs/GLIDE_SHELL_FRAMEWORK_KONZEPT.md) mit klarer Abgrenzung zwischen wiederverwendbarem Desktop-Fundament (Lifecycle, Window-Manager, Appearance, Widgets, Modal-Runner) und Glide-spezifischer Domäne sowie Entkopplung über Ports & Adapters.
- **System- und Testpflege:** Glide-Systemkatalog auf `V1.17` fortgeschrieben (`M095` `runtime_config.py`, `T313` `test_day_capacity.py`, `T314` `test_runtime_config.py`), 95 Quell- und 314 Testdateien, CI-Grundstufe 19/19 grün, Aufgabenformat 26 unverändert beibehalten.

## 3.54.0 – 10.11.2026

- Vollständige Fundortübersicht („Fundorte anzeigen …“, WA-21): listet für jede Aufgabe, Seite, Notiz, Liste und Zeichnung alle Verwendungen im Bestand auf (Heimatcontainer, Objektverweise, Textlinks, Aufgabenzeilen in Seiten/Notizen, Live-Listen, Aufgabenbeziehungen, Pinnwandkarten/-verbindungen und unverknüpfte Titelerwähnungen) samt Zielzustand, Öffnen im Haupt- oder Nebenbereich und direktem Verknüpfen unverknüpfter Erwähnungen.
- Pinnwand-Export als JSON Canvas 1.0 (`.canvas`, WA-07 / FP-07 Stufe 2): exportiert Bereiche als `group`-Knoten, Aufgaben-, Seiten-, Notiz- und Zeichnungskarten als `text`-Knoten mit stabilen Kennungen, Koordinaten, Maßen und Farben sowie Verbindungen als `edges`, begleitet von einem ausdrücklichen Verlustbericht über nicht abbildbare Glide-Metadaten.
- Klassischen Tk-Restbestand vollständig abgelöst (`Sperrklinke = 0`, UI-Feinschliff §21.76): alle 28 `Checkbutton`-, 2 `Radiobutton`-, 4 `Listbox`- und 1 `Scale`-Instanzen durch themengerechte Eigenzeichnungen (`GlideCheckbutton`, `GlideRadiobutton`, `GlideListbox`, `GlideScale`) ersetzt und in `altbestandteile.py` dauerhaft gesperrt.

## 3.53.0 – 10.11.2026

- Schrift- und Symbolprüfungen erweitert: alle vier auswählbaren Schriftfamilien werden mit sämtlichen UI-Symbolen in normalem und fettem Tk-Gewicht auf die tatsächlich verwendete Glyphenfamilie geprüft.
- `symbolpruefung.py` untersucht die vier Schriftstile statt nur der aktuell gewählten Familie; die lokale QA-Zuordnung benennt direkte Tests, indirekte Geometrieprüfungen sowie native und menschliche Abnahmegrenzen.
- Versionswechsel von 3.52.0 auf 3.53.0. Die plattformübergreifende Vollmatrix und menschliche Abnahme sind weiterhin Freigabetore.

## 3.52.0 – 10.11.2026

- Schriftstile: Modern Rubik, Technisch DM Mono, Kreativ DM Serif Display und Klassisch Charis SIL. Frühere gespeicherte Familien bleiben der passenden Stilklasse zugeordnet.
- DM Mono nutzt für „Kräftig“ Medium 500; DM Serif Display besitzt keinen statischen Bold-Schnitt. Schriftgewicht und Größe bleiben getrennt.
- OFL-Texte und SHA-256-Provenienz der ausgewählten Originaldateien sind mitgeführt. DejaVu Sans bleibt als Symbolbegleiter erforderlich, da die neuen Schriften nicht alle UI-Symbole abdecken.
- Das Schriftgewicht lässt sich unabhängig von der Größe wählen. Kreativ und Klassisch erscheinen automatisch im kräftigeren Bold-Schnitt.
- Das Kopflogo rückt 2 px nach rechts und wächst proportional nach oben. Die Unterkante bleibt an der Unterzeile, der Titel behält seine Position.
- Hinzufügen und weitere bisher lila Oberflächenakzente folgen der Themenfarbe. Löschen bleibt rot, Bestätigen grün.


## Frühere Versionen (verdichtet)

Vollständig beschrieben sind die sieben neuesten Versionen; ältere stehen verdichtet in der Tabelle darunter. Ihre ausführlichen Einträge, Verträge und Nachweise trägt Git (3.33.13–3.33.16 im Commit `6098877`, ältere im Stand vor dem 03.10.2026). Das aktuelle Verhalten beschreiben die [Funktionen](docs/20_FUNKTIONEN.md).

Datenformate und ihre Felder: [Daten und Migration](docs/06_DATA_BACKUP_MIGRATION.md#formatstufen).

| Version | Datum | Kern |
|---|---|---|
| 3.51.0 | 09.11.2026 | Die vier Plus-Knöpfe in der Seitenleiste erscheinen im Ruhezustand ohne Kontur. |
| 3.50.7 | 08.11.2026 | Produktkommunikation, MPL-2.0 und Validierung |
| 3.50.6 | 07.11.2026 | Menschliche Abnahme am Mac (D66–D71) |
| 3.50.5 | 05.11.2026 | Abnahmekorrekturen und Suchfelder |
| 3.50.4 | 05.11.2026 | Neuer Stand für die fortgesetzte menschliche Abnahme |
| 3.50.3 | 05.11.2026 | Korrekturen aus der menschlichen Abnahme |
| 3.50.2 | 03.11.2026 | Versions- und Ablageabgleich |
| 3.50.1 | 03.11.2026 | Themenflächen und lesbarere Schriftstile |
| 3.50.0 | 02.11.2026 | Erster öffentlicher Stand |
| 3.49.0 | 28.10.2026 | Tagesplanung, Verweise und geschützter Wiederanlauf |
| 3.48.0 | 27.10.2026 | Tagesnavigation, Mehrfachfelder und Verweise |
| 3.47.0 | 27.10.2026 | Mehrfachplanung und Nebenansichtsverlauf |
| 3.46.0 | 27.10.2026 | Tagessteuerung und Nachschlagen |
| 3.45.0 | 25.10.2026 | Sicherungsübersicht, Arbeitsmodi und Speicherstatus |
| 3.44.0 | 22.10.2026 | Wiederholen, eigene Rhythmen, Ansichten, Seitenkarten, Erwähnungen, KI-Aufträge und Markdown-Export |
| 3.43.1 | 16.10.2026 | Kürzel in Listen unter Linux/Tk 9.1 |
| 3.43.0 | 16.10.2026 | UI-/UX-Paket aus Nutzerbeobachtungen |
| 4.0.0 (Vorbereitung, keine Lieferung) | ab 15.10.2026 | Barrierefreiheit: eigene Tk-9.1-Laufzeit mit Patches, Reader- und Zustandsgegenproben; Stand im Entwicklungsplan (Paket 8) |
| 3.42.0 | 13.10.2026 | Eigenständige Entwicklungspakete |
| 3.41.0 | 13.10.2026 | Notion-Import und Seitenwiederherstellung |
| 3.40.0 | 13.10.2026 | Pixelanimation |
| 3.39.1 | 13.10.2026 | Wiederholungen richtig erfassen und austauschen |
| 3.39.0 | 12.10.2026 | Tagesplanung mit belegter Zeit |
| 3.38.0 | 11.10.2026 | Aufgaben unmittelbar bearbeiten |
| 3.37.0 | 10.10.2026 | Logo und Symbole |
| 3.36.0 | 10.10.2026 | Fundament und Tempo |
| 3.35.0 | 09.10.2026 | Pixel und Austausch |
| 3.34.0 | 09.10.2026 | Wissen und Seiten |
| 3.33.21 | 09.10.2026 | Ruhige Oberfläche |
| 3.33.20 | 09.10.2026 | Komfort im Alltag |
| 3.33.19 | 09.10.2026 | Tempo |
| 3.33.18 | 08.10.2026 | Seiten im Alltag (G28/G09/U08): Live-Listen zeigen Originalaufgaben samt Unteraufgaben direkt in Seiten. |
| 3.33.17 | 07.10.2026 | Wissen und Woche: eingebetteter Kalender, Kapazität/Zeitfenster, lokale Objektverweise und Rückverweise; Format 22 |
| 3.33.16 | 07.10.2026 | Bedienkomfort: eine Palette für Inhalte und Aktionen, höchstens vier Kopfknöpfe, einklappbare Hinweise, Bibliothekswege, Bearbeitungstag in der Datumsspalte, eindeutige Symbole (U01/U02/U13/U14/U16/U22/U24) |
| 3.33.15 | 07.10.2026 | Aufgaben im Wissen: echte Aufgaben im Notiztext, Übernahme in Listen mit erhaltenen IDs, „Aus Seiten“ (G29/G31/G32); Format 21 |
| 3.33.14 | 07.10.2026 | Tagesvorschlag „Was passt heute?“, geführter Tagesbeginn, Zeitblöcke per Tastatur, Fokus mit genau einmal gebuchter Zeit (AU01/AU03/H-02/G05) |
| 3.33.13 | 07.10.2026 | Gemeinsames Menü „Einplanen“ und verfügbare Zeit in allen Planungswegen (KO01/AU02, `planning.py`) |
| 3.33.12 | 06.10.2026 | Titel vor Kennzahlen, Herkunft rechts in Heute (U10/U19), erste Gestaltungsskala (OB01); ausführlicher Stand in Git |
| 3.33.11 | 06.10.2026 | Gezielter Speichervergleich (P08b), stabile Aktionskennungen, U03/U07; ausführlicher Stand in Git |
| 3.33.10 | 06.10.2026 | Kennzahlen und Messwerte je Aufbau wiederverwenden (P09b); ausführlicher Stand in Git |
| 3.33.9 | 05.10.2026 | Gemeinsamer Speichervergleich (P08a); ausführlicher Stand in Git |
| – | 05.10.2026 | Windows-Prüfung und Befunde festgehalten, App unverändert; ausführlicher Stand in Git |
| 3.33.8 | 05.10.2026 | Windows-Layout, Prüflaufzeit, Formatsicherung mit Inhaltsvergleich; ausführlicher Stand in Git |
| 3.33.7 | 05.10.2026 | Inhaltssuche in der Palette (G14 erste Stufe); ausführlicher Stand in Git |
| – | 03.10.2026 | Aufräumen der Ablage, App unverändert; ausführlicher Stand in Git |
| 3.33.6 | 02.10.2026 | Heute/Demnächst und Tagesmodi (D14); ursprüngliche Mac-Abnahme im festen Git-Stand |
| 3.33.5 | 02.10.2026 | Eisenhower-Gruppierung mit erhaltener Fälligkeit (D13); ausführlicher Stand in Git |
| 3.33.4 | 02.10.2026 | Wiederholungen in der Schnelleingabe mit erstem Termin und Feldchip; ausführlicher Stand in Git |
| 3.33.3 | 02.10.2026 | Deutsche Schnelleingabe mit Feldchips (G01, D10); ausführlicher Stand in Git |
| 3.33.2 | 02.10.2026 | Startseite Ruhig und beschleunigter Aufbau; ausführlicher Stand in Git |
| 3.33.1 | 01.10.2026 | Vier Seitenleistenbereiche, Fensterbedienung, Logo und Schaltflächen nachgezogen; ausführlicher Stand in Git |
| 3.33.0 | 01.10.2026 | Tk-freies Fundament: gemeinsame Formatsicherung, Bereichsregeln, SVG-Geometrie und Startseitenkacheln |
| 3.32.3 | 01.10.2026 | Bibliothek und Aktionsleiste behalten unveränderte Karten (Refresh bei 1.000 Aufgaben 776 → 5 ms); aktiver Showcase „Parkquartier“; Beschlüsse D09–D17 |
| 3.32.2 | 30.09.2026 | Drag-and-drop in allen Seitenleistenbereichen (D04); Schriftwerte je Tk-Interpreter zwischengespeichert |
| 3.32.1 | 30.09.2026 | Klappzustände von Labelgruppen, Fächern und Bereichen bleiben erhalten; Klapppfeile per Tastatur; D01–D06 übernommen |
| 3.32.0 | 30.09.2026 | ICO-Export, Aseprite-/ASE-Paletten, selbstfüllende Platzhalter, Tagesabschluss; Hänger bei Menübefehlen und Bildseiten behoben; Pflegewerkzeuge |
| 3.31.0 | 30.09.2026 | Rückmeldungen R1–R11: Menüdialoge öffnen wieder, Editor mit Blockaktionen, Farben nach Bedeutung, schnellere Übersicht |
| 3.30.0 | 25.–29.09.2026 | Modernisierung: Pixel-Werkstatt, Startseite zum Anpassen, Pinnwand als Board, Notizbuch, Seiten mit Bildern, Galerien, Tk 9, Ziehen aus Finder/Explorer, Systemmitteilungen, zehn Designs, Logo; **Format 20** |
| 3.29.0 | 24.09.2026 | Zeichnung als eigene Listenart mit Referenzbild; **Format 19** |
| 3.28.0 | 23.09.2026 | Ordnertypen und Tagebuch (später Notizbuch); **Format 18** |
| 3.26.0 | 21.09.2026 | Notizen als Listenart, Begleiter Gismo, Lizenzentwurf; **Format 17** |
| 3.25.0 | 19.09.2026 | „Form follows function“: Übersicht und Hierarchie, Startseite mit Kacheln und gezeichneter Figur |
| 3.24.0 | 19.09.2026 | Kürzere Navigation; Pinnwand mit Mehrfachauswahl und gerichteten Verbindungen |
| 3.23.0 | 18.09.2026 | Zusammenhalt vorhandener Funktionen (46 Punkte) |
| 3.22.0 | 17.09.2026 | Checkliste je Aufgabe; **Format 16** |
| 3.21.0–3.21.4 | 14.09.2026 | Kalenderimport aus ICS, Serienende ohne UTC-Versatz, Beispielbestand testbar, Standprüfung |
| 3.20.0 | 14.09.2026 | Kalenderausgabe als ICS |
| 3.19.0 | 13.09.2026 | Dauerhafter Änderungsverlauf; **Format 15** |
| 3.18.0 | 13.09.2026 | CSV-Import mit Spaltenzuordnung |
| 3.17.0 | 13.09.2026 | Druck- und PDF-Ausgabe |
| 3.16.0 | 13.09.2026 | Vollständiges App-Backup (`.glideapp`) |
| 3.15.0 | 13.09.2026 | Tagesplanung und Tageskapazität |
| 3.14.0 | 13.09.2026 | Bearbeitungstag und geschätzter Aufwand; **Format 14** |
| 3.13.0 | 13.09.2026 | Tabellenansicht |
| 3.12.0 | 13.09.2026 | „Mein Tag“ (seit 3.33.6 „Heute“) |
| 3.11.0 | 13.09.2026 | Schnellerfassung und gespeicherte Filter |
| 3.10.0 | 13.09.2026 | Reiter und Pinnwand |
| 3.9.0 | 12.09.2026 | Einheitliche Oberfläche, Einstellungen, Hell/Dunkel |
| 3.8.0 | 12.09.2026 | Lokale Erinnerungen, Aufmerksamkeit in Taskleiste und Dock; **Format 13** |
| 3.7.0 | 07.–12.09.2026 | Kompakte Kacheln, Anhänge an Listen und Ordnern, dynamische Übersicht; **Format 12** |
| 3.6.0 | 06.09.2026 | Kachelübersicht der Listen, Jahresanzeige |
| 3.5.0 | 05.09.2026 | Wiederkehrende Aufgaben; **Format 11** |
| 3.4.0 | 05.09.2026 | Startseite neu: Uhr, Tagesziel, Schnellzugriffe, Bestand, Listenfarben |
| 3.3.0 | 04.09.2026 | Ansicht „Labels“ |
| 3.2.0 | 04.09.2026 | Keine Übernahme aus Altordnern; zentrale Textzeichen |
| 3.1.0 | 04.09.2026 | Aufräumversion ohne neue Funktion |
| 3.0.0–3.0.2 | 03.09.2026 | Neue Oberfläche (Inhalt nach oben, kein Schwarz im Hellmodus); Gruppen benutzbar, Mehrmonitor-Dialoge |
| 2.12.0 | 03.09.2026 | Ruhigere Eingabemaske |
| 2.11.0 | 03.09.2026 | Papierkorb auch für Punkte, Mehrfachauswahl, Uhrzeit; **Format 10** |
| 2.10.0 | 03.09.2026 | Label-Chips, verlustfreier TXT-Rundlauf |
| 2.9.0 | 03.09.2026 | Verschachtelte Ordner, Long-Task-Details |
| 2.8.0 | 02.09.2026 | Verspätet, Long-Task, Zwischenüberschrift, Anlage-Dialog |
| 2.7.0–2.7.2 | 02.09.2026 | Papierkorb für Listen und Ordner, Labels; **Format 7** |
| 2.6.0 | 01.09.2026 | Gruppen; **Format 6** |
| 2.5.1–2.5.5 | 31.08.–02.09.2026 | Ordneransicht, fester Eingang, Kontextmenü, „In Bearbeitung“, Anhangspfade; **Format 5** |
| 2.5.0, 2.4.1 | vor 31.08.2026 | Zwischenstand und Ausgangsstand |
