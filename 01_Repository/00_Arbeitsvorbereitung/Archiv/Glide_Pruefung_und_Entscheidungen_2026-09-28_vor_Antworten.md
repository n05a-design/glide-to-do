# Glide – Prüfung vom 28.09.2026: Entscheidungen und offene Punkte

Stand 28.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Entscheidungsvorlage, Antworten offen

Auftrag: abgelegte Aufgaben, Rückmeldungen, Dokumentation, Code,
Fehlerprüfungen sowie Ablage und Archivierung prüfen und daraus Entscheidungen
und offene Punkte für den Inhaber zusammenstellen.

Geprüft wurde am Windows-PC, nur lesend. Außer dieser Datei ist in der Ablage
nichts geändert. Im Glide-Datenordner des PCs wurden nur Dateinamen,
Formatnummer, Fehlerprotokoll und Prüfsummen angesehen, keine Inhalte.

**So antworten:** „Alle Empfehlungen“ reicht. Sonst je Nummer, etwa
„1 ja, 2 a und b, 6 später“. Die Antworten gehören in Abschnitt 7; erst danach
wird umgesetzt.

## 1. Ergebnis in Kürze

- **Code und automatische Prüfung sind in Ordnung.**
  - Der letzte Vollprüflauf `tests/qa-3.30.0/tk9_bilder_2026-09-27` (27.09.,
    19:55–20:16, macOS, Python 3.14.5, Tk 9.0.3) ist grün: 62 Schritte, zwei
    plattformbedingt übersprungen. Er deckt den letzten Code-Stand ab;
    `app.pyw` wurde zuletzt um 19:45 geändert.
  - Repository und `07_Python-Versionen` sind per SHA-256 bytegleich: alle
    sieben Code-Dateien, `vendor`, Schriften und aktuelle Vorlagen.
  - `tests/tools/standpruefung.py` lief am 28.09. unter Windows
    (Python 3.13.15) mit Exitcode 0.
  - Das Fehlerprotokoll des PCs hat nur einen Eintrag vom 19.09.
    (`tab_overview` in 3.25.0); der Fehler ist im heutigen Code behoben.
- **Neu gefunden:** zwei Datenrisiken (Punkte 1 und 2), dazu Befunde zu
  Prüfung, Ablage, Code und Doku.
- **63 % des Ablagevolumens sind Archivkopien:** 2.314 von 6.023 Dateien, 205
  von 324 MB (ohne `.venv`). In `docs/archiv` liegen 67 Kopien des
  QA-Berichts, 62 des Index, 54 der Übergabe und 25 des CHANGELOG. Eine
  Versionsverwaltung gibt es nicht, nur eine `.gitignore`.

## 2. Entscheidungen

Jede Entscheidung hat eine Empfehlung.

### Datensicherheit

#### 1. Automatische Sicherungen reichen nur etwa 50 Minuten zurück

- **Befund:** `autosave_tick` legt alle 5 Minuten eine Sicherung an, auch ohne
  Änderung (`src/glide/app.pyw`, Zeile 36572). `prune_backups` behält die 10
  neuesten und löscht ältere nach 30 Minuten (`MIN_BACKUPS`,
  `BACKUP_MAX_AGE_MINUTES`, Zeilen 12978–12979). Nach 50 Minuten ohne
  Änderung sind alle Sicherungen gleich, ältere Stände sind gelöscht.
- **Beleg:** Auf dem Windows-PC sind alle 10 Dateien `liste_backup_*.json` per
  SHA-256 gleich dem aktuellen Bestand.
- **Widerspruch:** `docs/decisions/PRODUCT_IDENTITY.md` nennt „letzte 40
  JSON-Stände“.
- **Empfehlung:** nur sichern, wenn sich der Inhalt seit der letzten Sicherung
  geändert hat, und zusätzlich je Tag den letzten Stand 14 Tage lang behalten.
  Mit Test und Doku.
- **Alternative:** so lassen und nur die Doku berichtigen.

#### 2. Alte Glide-Fassungen können den Bestand überschreiben – nicht nur 3.29

- **Befund:** Startbar liegen 55 Altstände bis 3.29 (`07_Python-Versionen/Archiv`:
  54 `.pyw` direkt, 3.29 im Unterordner), 12 Zwischenstände von 3.30 und 10
  alte `app_*.pyw` in `src/glide/archiv`.
- Die Listenarten „Seite“ (26.09.) und „Galerie“ (27.09.) kamen ohne neue
  Formatnummer dazu. 10 der 12 Zwischenstände kennen mindestens eine davon
  nicht:

| Zwischenstand in `07_Python-Versionen/Archiv` | kennt „Seite“ | kennt „Galerie“ | Kopie vor Leerstart |
|---|---|---|---|
| `…_vor_Ausbau_2026-09-25` | nein | nein | **nein** |
| `…_vor_Ausbau2` bis `…_vor_Seiten` (8 Stände) | nein | nein | ja |
| `…_vor_Aufraeumen_2026-09-27` | ja | nein | ja |
| `…_vor_Kompression`, `…_vor_Tk9_und_Bildern` | ja | ja | ja |

- **Wirkung:** `check_list_kind` lehnt eine unbekannte Listenart ab, und
  `load_items` behandelt das als unlesbare Datei (`handle_unreadable_save_file`,
  Zeile 35651). Der Schutz „neueres Format → nur lesen“ greift nur bei einer
  höheren Formatnummer. Folge: eine Kopie `liste_unlesbar_*` (beim Stand vom
  25.09. nicht einmal das), ein leerer Bestand, und die erste Eingabe
  überschreibt die Datei. Der heutige Code verhält sich bei einer künftigen
  unbekannten Listenart genauso.
- **Empfehlung:**
  - a) alle Altstände je Version in ZIP-Dateien packen, damit keiner
    versehentlich startet (umkehrbar);
  - b) im Code eine unbekannte Listenart wie ein neueres Format behandeln: nur
    lesen statt leer starten;
  - c) neue Listenarten künftig nur mit neuer Formatnummer.
- **Alternative:** nur a).

#### 3. Der Windows-Bestand ist noch nicht umgestellt

- **Befund:** `%APPDATA%\Glide\liste_speicher.json` trägt Format 17, zuletzt
  geändert am 21.09.2026. Glide 3.30 lief am 28.09. um 19:59–20:00 mit
  Python 3.13 aus `07_Python-Versionen`, ohne Eingabe. Die erste Eingabe
  stellt um (mit Vorsicherung `liste_vor_format20_*`).
- **Frage:** Ist dieser Bestand noch wichtig, oder ist der Mac-Bestand
  führend? Sollen beide zusammengeführt werden?
- **Empfehlung:** vor der ersten Eingabe eine Vollsicherung (`.glidebackup`)
  anlegen.

### Prüfung

#### 4. Windows-Vollprüfung vorbereiten

- **Befund:** Auf dem PC ist nur Python 3.13.15 mit Tk 8.6.15 installiert;
  Grundlage ist laut E-03 Python 3.14 mit Tk 9. Rund 1.400 Dateien der Ablage
  liegen nur online, dann bricht `windows_vollpruefung.ps1` mit Exitcode 4 ab.
  Der letzte grüne Windows-Gesamtlauf war 3.26 am 21.09.; der Lauf 3.28 am
  23.09. scheiterte an OneDrive-Platzhaltern.
- **Empfehlung:** Python 3.14 installieren, den Ordner „Glide ToDo“ auf „Immer
  auf diesem Gerät behalten“ stellen, dann
  `01_Repository/Glide/tests/tools/windows_vollpruefung.cmd` starten (15–25
  Minuten).
- **Alternative:** mit Python 3.13 prüfen; das deckt nur den Tk-8.6-Weg ab.

#### 5. Ein nicht nachgestellter Datenbefund

- **Befund:** Laut QA-Bericht (Ausbau-Nachprüfung vom 26.09.) scheiterte
  `test_ui_followup36` unter doppelter Last einmal am Datenvergleich nach
  Speichern und Laden. Das ließ sich nicht nachstellen und ist als offene
  Beobachtung notiert. Dazu kommt der einmalige Befund in `test_glide` vom
  27.09. (E-12, Prüfung gehärtet).
- **Empfehlung:** ein gezielter Belastungstest für Speichern und Laden:
  paralleles Speichern, große Bestände, Abbruch mitten im Schreiben.

### Ablage und Archiv

#### 6. Versionsverwaltung (Git) statt Archivkopien

- **Befund:** Regel 10 in `AGENTS.md` kopiert vor jeder Änderung ganze
  Dokumente ins Archiv; eine Änderungsrunde erzeugt 20 bis 60 Kopien.
- **Empfehlung:** Git lokal für `01_Repository/Glide` einrichten und Regel 10
  danach auf Versionsstände beschränken. Solange die Ablage in OneDrive liegt,
  nur an einem Rechner gleichzeitig arbeiten.
- **Alternative:** ein privates GitHub-Repository mit Arbeitskopien außerhalb
  von OneDrive, oder alles wie bisher.

#### 7. Archiv verdichten

- **Befund:** `50_Ablage/QA/Dokumentation` belegt 121 MB in 464 Dateien, vor
  allem Renderläufe alter Word-Berichte 2.5.x; laut README sind fünf
  praktisch identisch. Dazu kommen die alten QA-Läufe und die Doku-Kopien.
- **Empfehlung:** je Version eine ZIP-Datei, das SHA-256-Manifest neu
  erzeugen, nichts endgültig löschen.
- **Alternative:** alles lassen.

#### 8. Kleinkram (einzeln abwählbar)

- `.venv` löschen: eine leere Python-3.13-Umgebung vom 20.09. mit 894 Dateien,
  nur `pip`; Glide braucht sie nicht.
- `Glide-Logo.af` und `Inspiration für Glide.png` nach `20_Grafik_Master`
  verschieben. Dessen README beschreibt Unterordner (`Illustrator/`,
  `Photoshop/`, `Arbeitsdateien/`, `Branding/`), die es nicht gibt.
- Das Vorlagen-Archiv in `07_Python-Versionen/resources/templates/archiv` mit
  dem Repository abgleichen: Gleiche Dateien tragen andere Namen, und
  `glide_vorlagen_3.26.0_vor_3.28.0` liegt nur in der Kopie.
- `01_Repository/Glide/build/macos/Glide.app` stammt vom 27.09., 12:00, und
  ist veraltet: `app.pyw` und `page_markdown.py` weichen ab, `image_preview.py`
  und `vendor` fehlen. Vor der Mac-Prüfung neu bauen, sonst lassen sich die
  Systemmitteilungen nicht prüfen.
- **Empfehlung:** alles ja.

### Code

#### 9. Kein Bytecode im OneDrive-Ordner

- **Befund:** Beim direkten Start einer `.pyw` legt Python `__pycache__` neben
  die Module, am 28.09. in `07_Python-Versionen/__pycache__` (fünf Dateien
  `cpython-313.pyc`). Nur `glide_start.py` (Schnellstart) leitet den Bytecode
  in den Systemcache um. Auch die Windows-Verknüpfung
  (`packaging/windows/verknuepfung_anlegen.ps1`) startet `app.pyw` direkt.
- **Empfehlung:** `app.pyw` setzt `sys.pycache_prefix` beim Start selbst, wie
  `glide_start.py`. Den vorhandenen `__pycache__`-Ordner löschen.

#### 10. Die Hauptdatei aufteilen?

- **Befund:** `app.pyw` hat 52.146 Zeilen (2,6 MB), die Klasse `ListApp`
  allein rund 39.700. `docs/02_ARCHITECTURE.md` hält den Monolithen bewusst
  fest.
- **Empfehlung:** noch nicht. Erst nach Git (6) und der Windows-Prüfung (4),
  dann schrittweise auslagern, wie schon bei `drawing.py`, `backdrop.py`,
  `page_markdown.py` und `image_preview.py`.

### Doku

#### 11. Veraltete Aussagen berichtigen

`standpruefung.py` prüft nur Versionsnummern und findet diese Widersprüche
nicht:

| Ort | Veraltete Aussage | Richtig |
|---|---|---|
| `README.md` (Wurzel) | Link „Warum es keine Systembenachrichtigung gibt“; „zwei aktuelle Beispielbackups“ | Systemmitteilungen gibt es seit 27.09. als Option; drei Backups einschließlich „Rundgang“ |
| `docs/66_MODERNISIERUNG_3.30.0.md` §11, „Galerie“ | Ziehen aus Finder/Explorer bräuchte eine Erweiterung; JPEG-Vorschau nur unter macOS | seit 27.09. tkinterdnd2; unter Windows WIC (ungeprüft) |
| `Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md` §6 | Systembenachrichtigungen fehlen; Galerie-Vorschau bräuchte eine Bildbibliothek; Architekturen offen | am 27.09. umgesetzt bzw. entschieden |
| Aufgabenkatalog §2, Aufgabensammlung Zeichenfläche | ZF-200: Systembenachrichtigungen offen; MO-020 „umgesetzt“ | Systemmitteilungen umgesetzt; MO-020 seit 27.09. entfallen (Vertrag 66 §8.13) |
| `docs/decisions/PRODUCT_IDENTITY.md` | „Prüflaufzeit Windows / Python 3.13.15“; „letzte 40 JSON-Stände“ | maßgeblich ist macOS / Python 3.14.5; zu den Sicherungen siehe Punkt 1 |
| `40_Store_Material/Produktdatenblatt_3.30.0_Entwurf.md` | Kennungen und Architektur offen; Laufzeit nur Standardbibliothek | am 26./27.09. entschieden; tkinterdnd2 wird mitgeliefert |
| `30_Release_Exports/README.md` | nur `drawing.py` und `drawing_image.py` als Module; „Gebaute Bundles liegen nicht in dieser Ablage“ | sechs Module plus `vendor`; `build/macos` liegt in der Ablage |
| `07_Python-Versionen/README.md` | Schnellstart nennt nur den macOS-Cachepfad | unter Windows `%LOCALAPPDATA%\Glide\Cache\bytecode` |
| `docs/06_DATA_BACKUP_MIGRATION.md` | Listenarten „Seite“ und „Galerie“ fehlen; Rückfallwarnung nur „3.29 und älter“ | im Vertrag 66 §3 beschrieben; Zwischenstände von 3.30 siehe Punkt 2 |

- **Empfehlung:** in einem Durchgang berichtigen, zusammen mit den
  Entscheidungen oben.

## 3. Nur durch den Inhaber

- Inhaberangaben bestätigen:
  [Vorschläge](../40_Store_Material/Inhaberangaben_Vorschlaege_2026-09-27.md)
  für Copyright, Datenschutz-URL, Sicherheitskontakt und Inno-AppId.
- Lizenzbedingungen veröffentlichen (Entwurf: kostenlos für private,
  nicht kommerzielle Nutzung).
- Logo als PNG 1024 × 1024 aus `Glide-Logo.af` exportieren.
- Apple-Developer-Konto und Windows-Code-Signing-Zertifikat besorgen.
- Markenprüfung „Glide“ durch einen Fachanwalt für Markenrecht.
- Python 3.14.7 auf dem Mac installieren (braucht das Passwort).
- Manuelle Prüfung: 159 offene Punkte (3.30), 23 (3.29), 14 (3.28) und 5
  (Windows), zusammen 201.

## 4. Offene Produktfragen (seit 27.09. unentschieden)

- Seiten: Titelbild und Unterseiten? Bis zu 5 Ebenen? Lesebreite
  umschaltbar? Bibliothek zusätzlich als Galerie?
- Tempo: Startseite auf einer Fläche, lange Listen nur mit sichtbaren Zeilen?
- Import aus Notion und Todoist, Export als Markdown?
- Fokusansicht: eine Aufgabe groß, Zeiterfassung läuft?

## 5. Rückfrage zur Rückmeldung vom 26.09.

Verschwinden beim Scrollen noch Knöpfe? Laut QA-Bericht ließ sich das nicht
nachstellen; der Punkt ist offen.

## 6. Windows-PC am 28.09.2026 (für Folgesitzungen an anderen Rechnern)

- Python 3.13.15 mit Tk 8.6.15; kein Python 3.14, kein Tk 9.
- Echter Bestand noch nicht umgestellt (siehe Punkt 3); die zehn
  automatischen Sicherungen sind bytegleich mit ihm.
- Rund 1.400 Dateien der Ablage nur online (OneDrive).
- Keine Startmenü-Verknüpfung angelegt; git ist installiert.

## 7. Antworten des Inhabers

Offen.

| Nr. | Antwort | Umsetzung |
|---|---|---|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |
| 11 | | |
