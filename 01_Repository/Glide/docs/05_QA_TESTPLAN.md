# Prüfplan – Glide

Stand 05.10.2026 · Glide 3.33.8 · Aufgabenformat 20 · alle App-Tests mit isoliertem `GLIDE_DATA_DIR`

Wie Glide geprüft wird. Was tatsächlich geprüft wurde, steht im [QA-Bericht](07_QA_BERICHT.md). Am 03.10.2026 auf den gültigen Stand verdichtet; am 05.10.2026 um Nachweisregeln und Kontrollmatrix der Windows-Fassung ergänzt. Die Suitebeschreibungen je Einführungsversion trägt Git.

## Prüfstufen

| Stufe | Aufruf | Umfang | Wo |
|---|---|---|---|
| CI-Grundstufe | `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` | Syntax, Version, Dokumentation, Fixtures, Werkzeugtests, Unit-Tests, fünf Analysen, Startprobe, Lieferstand, Fremdcode, Datenschutz, Ablagegröße | GitHub Actions (Linux, Python 3.14, Tk 8.6, Xvfb) und lokal |
| Schnellprüfung | `python3 -B tests/tools/pruefen.py` | Syntax, Version, Dokumentation, Fixtures, Unit-Tests, Tk-Probe, Zeitzone, alle Integrationssuiten (3.33.8: 66), Showcase, fünf Analysen | Entwicklungsrechner |
| Vollprüfung | `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-<Version>/<Name> --timeout 900` | zusätzlich Reproduktion von Beispiel- und Releasedaten, Fensterfotos; zuletzt 84 automatische Schritte (3.33.8 unter Windows), je nach Rechner 15–60 Minuten | Referenz-Mac, Abnahme jeder Version (für 3.33.7/3.33.8 offen) |
| Windows | `tests/tools/windows_vollpruefung.cmd` | dieselbe Vollprüfung; verlangt Python 3.14 mit Tk 9 (sonst Exitcode 3) und prüft OneDrive-Platzhalter (Exitcode 4); Anleitung in der Prüfliste, B0 | Windows-PC des Inhabers |
| Manuell | [Manuelle Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md) | echte Bedienung, Plattformen, DPI, Screenreader | Inhaber |

Maßgeblich sind `SUITEN` und `ANALYSEN` in `tests/tools/pruefen.py`. Einzelsuite: `python3 -B tests/integration/<suite>.py`, unter macOS im Hintergrund mit `GLIDE_QA_HINTERGRUND=1 PYTHONPATH=tests/tools/hintergrund`. Unter Linux laufen die Integrationssuiten nur informativ; vier reine Linux-Abweichungen sind noch nicht kalibriert. Die Suiten sind auf den Referenz-Mac abgestimmt; Linux-Grundstufe und Windows-Lauf ersetzen keine Mac-Vollprüfung, und kein Windows-Nachweis wird aus einem Mac-Lauf abgeleitet. Laufzeit, Betriebssystem und tatsächlicher Umfang stehen in jedem `ergebnis.json`.

## Regeln

- **Isolation:** `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner. Nie echte Nutzerdaten; das Fehlerprotokoll des Inhabers nur mit Erlaubnis und nur Fehlereinträge.
- **Einfrieren:** Vor dem finalen Volllauf Quell- und Prüfstand per SHA-256 festhalten (`quellstand.json`) und danach abgleichen. Ändert sich danach ein ausführbarer Pfad oder eine Suite, betroffene Prüfungen und den Volllauf wiederholen.
- **Belege:** Vorhandene JSON-Ergebnisse nie auf neue Versionen umetikettieren; ein roter Vorlauf bleibt ein roter Vorlauf. Formal grüne Stand- und Linkprüfung durch einen semantischen Abgleich ergänzen: Funktionen, Datenformat, Aufgabenstatus, Entscheidungen und Grenzen gegen den Code. Für reine Dokumentpflege reichen Stand/Links, betroffene Werkzeugtests und der Nachweis unveränderter Laufzeit; keine künstliche App-Version.
- **Bestand bleibt aktiv:** Bestehende Integrationssuiten und Referenz-Fixtures laufen weiter, auch für alte Datenformate. Ergebnisse und Rohprotokolle entstehen lokal; in Git gehören nur bereinigte Zusammenfassungen (`ergebnis.json`, README).
- **Gegenprobe:** Eine neue Pflichtsuite muss mit der Vorversion rot sein. Bestehende grüne Tests sind keine Abnahme noch nicht gebauter Funktionen.
- **Echte Bedienwege** statt Setter: native Tk-Bindungen (Pfeilklick, Tastatur, Ziehen, Menü), Callbackfehler sammeln und scheitern lassen, Undo, Neustart und Reload prüfen.
- **Hintergrund unter macOS:** Prüffenster nehmen keine Maus an (`--vordergrund` schaltet das ab), die Prüf-App bleibt aber aktiv. Tastatureingaben während eines Laufs landen in Prüfdialogen; bei gesperrtem Bildschirm scheitern Suiten mit Tastenereignissen. Deshalb weder tippen noch sperren (`caffeinate -dims`), Suiten mit Tastenereignissen nicht parallel starten. Tk-Fokus im Hintergrund ist kein Nachweis des OS-Fokus. Unter Windows gibt es keinen Hintergrundmodus: Die Prüffenster kommen nach vorn, Maus und Tastatur bleiben während des Laufs unberührt.
- **Last:** UI-Messtests nicht parallel zur Vollprüfung; große Dateisynchronisierung (OneDrive) vorher ruhen lassen. Neue Dateien im Dokumentbestand erst nach dem Lauf anlegen – die Dokumentationsprüfung läuft zuerst.
- **Termine in Suiten liegen in der Zukunft:** Ein Punkt „heute 14:00“ mit relativer Erinnerung wurde mitten im Lauf ausgeliefert und veränderte den Bestand; zwei Suiten scheiterten dadurch tageszeitabhängig.
- **„Flaky“ ist keine Ursache:** Jeder rote Lauf wird nachgestellt und begründet; ein wiederholter Lauf zählt nur mit belegter Ursache für den ersten.
- **Messen** unprofiliert mit gleicher Fixture, Aufwärmlauf, Median und p95 (`scripts/pflege/messung_*.py`, `--measure` der Pflichtsuiten). Keine absoluten Zeitassertions in Bedienungstests. Kalte und warme Messungen trennen und Rohwerte festhalten; Profiling erklärt Ursachen, unprofilierte Werte belegen den Gewinn. Viele Aufgaben bei gleicher Kartenzahl belegen keine Skalierung auf viele Karten.
- **Sichtprüfung:** Aufnahmen und Fensterfotos sieht eine Person an; der Prüfstand meldet sie als übersprungen. Die Releaseplanung muss hell und dunkel verschieden aufgenommen sein.
- **Lieferung erst nach grüner Vollprüfung:** `scripts/pflege/abgleich_07.py`, `packaging/macos/baue_app.py`, SHA-256 von 07 und Bundle gegen `src/glide`, `codesign --verify --deep --strict`, `scripts/pflege/showcase_abgleich.py`.

## Schritte der Prüfung

- **Syntax, Versionskonsistenz** (VERSION, `APP_VERSION`, Hauptsuite, oberster CHANGELOG-Eintrag, Datenformat), **Dokumentation** (jedes `docs/**/*.md` im [Index](00_INDEX.md), lokale Links erreichbar), **Fixtures** (Format und Version der Beispielbackups).
- **Fachlogik-Unit-Tests** (`tests/unit`, Tk-frei nach D17): `schema_backups`, `sidebar_policy`, `svg_geometry`, `home_tiles`, `capture_parser`, `eisenhower`, `today_view`, `content_search`.
- **Tk-Probe** (`pruefe_tk.py`): unter macOS native Mausisolierung von Hauptfenster, Dialog und Tooltip; gibt die Tk-Version aus (`package provide Tk`). **Zeitzone:** Der Prüfstand setzt `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt, und misst den tatsächlich geltenden Versatz im Kindprozess – in einer Zone ohne Versatz ist jeder Zeitzonenfehler unsichtbar; Versatz null beendet mit Exitcode 2. Unter Windows gilt die Systemzone (kein `time.tzset()`), ein gesetztes `TZ` ist dort ein Befund.
- **Integrationssuiten** (3.33.8: 66) und **Showcase** (`pruefe_showcase.py`: ZIP und SHA-256, Teil-/App-Import, Anhänge, Remapping, alle Arten, Vorschauen, Klappzustand, Undo, Vorlagen, Neustart in eigenem Prozess).
- **Analysen:** `analyse_statisch.py`, `analyse_erreichbarkeit.py`, `standpruefung.py` (Stand, Formate, überholte Aussagen, Modullisten, Links; Regeln R1–R14), `attributpruefung.py` (Aufrufe ohne Ziel je Klasse, auch über Tk-Basen), `dublettenpruefung.py` (meldet Wiederholungen, bewertet nicht).
- **Nur Vollprüfung:** Beispieldaten und Releasedaten werden neu erzeugt und inhaltlich mit den Fixtures verglichen (Abweichungen erst auf Plattformabhängigkeit des Erzeugers prüfen); Fensterfotos aus `test_fenster330` unter macOS und Windows, unter Windows zusätzlich die Releaseplanung hell und dunkel (`release_hell*.png`). Versioniert werden nur `ergebnis.json` und README, keine Fensterbilder.
- **Nur CI:** Werkzeugtests (`tests/tools/test_*.py`), Startprobe unter Xvfb, Lieferstand (`src/glide` = `07_Python-Versionen`), Fremdcode (vendor/fonts unverändert), Datenschutz (keine Benutzerpfade, auch JSON-maskiert), Ablagegröße (`tests/tools/ablagegroesse.py`).

## Integrationssuiten nach Bereich

Ausführbarer Vertrag zu [Funktionen](20_FUNKTIONEN.md). Pflichtsuiten der letzten Versionen zuerst.

| Bereich | Suiten |
|---|---|
| Editorlebensdauer beim Seitenwechsel (3.33.8) | `test_editor3338` |
| Inhaltssuche (3.33.7) | `test_suche3337` |
| Heute und Demnächst (3.33.6) | `test_heute3336` |
| Eisenhower (3.33.5) | `test_eisenhower3335` |
| Schnelleingabe, Wiederholungen (3.33.3/4) | `test_eingabe3333` |
| Startseite „Ruhig“ (3.33.2) | `test_startseite3332` |
| Vier Bereiche, Inhaltsgrenzen (3.33.1) | `test_bereiche3331` |
| Formatsicherung, Listenbreiten (3.33.0) | `test_fundament333` |
| Bibliothekskarten, Aktionsleisten (3.32.3) | `test_library_performance3323` |
| Ziehen in Bereichen, Layoutbündelung (3.32.2) | `test_drag_performance3322` |
| Klappmechanismen (3.32.1, D08) | `test_klappmechanismen3321` |
| Etappe 1: ICO, Paletten, Platzhalter, Tagesabschluss (3.32.0) | `test_etappe1_332` |
| Fenster über echte Wege, Fotos, Tempo (3.31) | `test_fenster330`, `test_tempo330`, `test_befunde330` |
| Modernisierung 3.30 | `test_features330`, `test_drawing330`, `test_seiten330`, `test_aufraeumen330`, `test_kompression330`, `test_bilder330`, `test_festlayout330`, `test_logo330`, `test_kartenfuss330`, `test_notizbereich330`, `test_rueckmeldung330`, `test_hintergrund330` |
| Mindestgröße, Kontrast, Paketierung | `test_mindestgroesse330` (jede Ansicht und jeder Dialog bei 860 × 700 in fünf Kombinationen), `test_kontrast330` (rund 13.700 Paare), `test_paketierung330` (baut unter macOS das Bundle und prüft die Signatur) |
| Belastung | `test_speicherlast330` (26.420 Punkte, Abbrüche, zwei Schreiber, Sperre, Startprüfung) |
| Zeichnung | `test_drawing`, `test_drawing_prototype`, `test_features329` |
| Funktionen 3.11–3.28 | `test_features311`–`test_features328` (Schnellerfassung, Heute, Tabelle, Planung, Kapazität, App-Backup, Druck, CSV, Verlauf, Kalenderausgabe, Kalenderimport, Checkliste, Designsystem, Pinnwand, Hierarchie, Notizbuch) |
| Grundbestand und Oberfläche | `test_glide`, `test_datenintegritaet` (130 Kombinationen), `audit_app`, `test_dialog_theme`, `test_ui_updates`, `test_glide_36`, `test_release36`, `test_ui_polish36`, `test_ui_followup36`, `test_release37`, `test_template_workflows`, `test_reminders`, `test_ui39`, `test_workspace310`, `test_vollpruefung325` (jede Ansicht, jedes Design, jede Menüaktion, jede Kachel) |

Neue Klappflächen gehören in `test_klappmechanismen3321`, neue Fenster in `test_fenster330`, neue Ansichten in `test_mindestgroesse330` und `test_kontrast330`. Jede neue Funktion bekommt ein Beispiel im Showcase oder eine ausführbare Bedienprüfung.

## Was nur manuell geht

Echte Maus-, Trackpad- und Tastaturbedienung, Windows- und Linux-Desktop, DPI und mehrere Monitore, Screenreader, Schlafen/Aufwachen und Langzeitbetrieb, Druck im Browser, Signatur/Notarisierung/Installer. Die automatischen Prüfungen ersetzen diese Abnahme nicht und werden nie als solche ausgegeben. Einzelpunkte je Gerät: [Manuelle Prüfung](../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md).

**Kontrollmatrix:** Jede Zeile bleibt offen, bis ein tatsächlicher Geräteversuch dokumentiert ist.

| Bereich | Zu prüfen |
|---|---|
| Vier Seitenleistenbereiche | Sichtbarkeit, Neu/Verschieben, gemischte Altordner, Notizbuchzeichnungen, Klappen, Zustand nach Neustart |
| Tastatur und Fokus | Tab-Reihenfolge, Kürzel, Esc/Return, OS-App-Wechsel, modale Dialoge und Rückkehr zum richtigen Feld |
| Ziehen | Maus/Trackpad, Bereichs-/Ordnerziele, Gruppenmitte/Rand, Termine/IDs/Undo |
| Aktualisierung | Auswahl, Fokus und Scrollposition; Tageswechsel, neue/gelöschte/archivierte Elemente |
| Zeichnung | Strich/Undo, Werkzeugwechsel, Zoom/Raster, Referenz/Nachzeichnung, Autosavefehler, Neustart, Export in externen Programmen |
| Seiten/Notizen/Bilder | Text, Formatspannen, Unicode, Umfluss, Größeziehen, Anhänge, Finder/Explorer, Galerie |
| Startseite | Eigene Kacheln, sieben Standards, Wiederherstellen, Neustart, Vorschauen, nächste Aufgabe |
| Planung und Ansichten | Tagesbeginn/-abschluss, Aufwand, Zeitblöcke, Kalender, Board-Spalten, abgeleitete Filter |
| Darstellung | Alle Fenster/Dialoge, zehn Designs, Kontrast, 860 × 700, Schriftgrößen, DPI/Mehrmonitor, Hochkontrast und RDP |
| Barrierefreiheit | Nur Tastatur, Screenreader, Canvas-Beschriftung und nachvollziehbare Statusmeldungen |
| Speichern/Backups | Unlesbar/neueres Format, Vorsicherungsfehler, Schreibschutz, Fremdbelegung, Restore/Additivimport, Cloudordner nacheinander |
| Systemmitteilungen | Laufende App, verpasste Hinweise, Aufschub, Ruhezustand/Aufwachen, feste Plattformkennungen |
| Dauerbetrieb und Release | Dauerlauf, Clean Machine, Installer/Update/Deinstallation, Druck/PDF, Signatur/Notarisierung |
