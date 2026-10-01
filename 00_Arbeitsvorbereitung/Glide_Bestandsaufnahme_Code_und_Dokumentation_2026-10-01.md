# Glide – Bestandsaufnahme Code und Dokumentation

Stand **01.10.2026** · Glide 3.32.3 (Aufgabenformat 20) · Teil 1 von 4 der Analyse vom 01.10.2026

Zugehörig:
- [Konkurrenz- und Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md)
- [Produktprinzipien und UX-Prüfung](Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)
- [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md)
- [Entscheidungsvorlage D09–D17](Glide_Entscheidungsvorlage_2026-10-01.md)
- [Nachweise: Messungen, Proben, Bilder](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/README.md)

## 1. Ergebnis in Kürze

1. **Die Dokumentation beschreibt den Funktionsstand weitgehend richtig.**
   - Alle 18 Einstiegspunkte der Claude-Übergabe stimmen zeilengenau mit dem Code überein.
   - Die Arbeits- und Featureplanung führt ihre Zeilenangaben ausdrücklich als Stand 3.32.0; sie sind um 36 bis 212 Zeilen verschoben, die Funktionen existieren alle.
   - `src/glide/app.pyw` ist bytegleich zur Hauptdatei in `07_Python-Versionen`.
2. **Es gibt 17 konkrete Abweichungen zwischen Dokumentation und Code bzw. Ablage** (Abschnitt 6).
   - Keine betrifft Datensicherheit.
   - Am wichtigsten: Die Produktgrenzen nennen für den Änderungsverlauf eine Obergrenze von 4000 Einträgen, der Code hält 15 Einträge und 15 Tage.
   - Die Produktgrenzen beschreiben JPEG/HEIC-Vorschau nur für macOS, der Code kann sie auch unter Windows.
   - Fünf Symbole tragen entgegen der eigenen Regel zwei Bedeutungen.
3. **Neuer, gemessener Leistungsbefund (T1):**
   - Jede Änderung prüft den *gesamten* Bestand dreimal auf Unterschiede (Änderungsverlauf, „zuletzt bearbeitet“, Aktivitätszählung) und legt einen vollständigen Rückgängig-Schnappschuss an.
   - Ein Abhaken kostet bei 10.000 Aufgaben **446 ms** (p95 502 ms) und bei 1.000 Aufgaben **56 ms** (Python 3.14, Linux-VM).
   - Bisher nicht Teil von P01–P07; Vorschlag **P08**.
4. **Das erste Speichern jeder Sitzung liest die Datendatei neunmal vollständig ein (T2).** Bei 10 MB rund 0,5 s zusätzlich. Kleine, risikoarme Korrektur.
5. **Linux läuft, aber eingeschränkt:**
   - Start mit Python 3.12/Tk 8.6 fehlerfrei.
   - Die Pixelschrift wird unter echtem Ubuntu-Tk registriert und ist sichtbar; das war bisher nur „mit nachgebildeter Bibliothek geprüft“.
   - Distributionen liefern meist Tk 8.6: keine Systemmitteilungen, kein SVG, keine JPEG-Vorschau.
6. **Die Ablage im Repository war nach dem Upload eine Ebene zu tief**, und die Git-Regeln hatten Dateien verändert bzw. ausgelassen.
   - Korrigiert: Struktur, 44 Linux-Bibliotheken, 123 CRLF-Dateien, Showcase-Sicherung.
   - Die Standprüfung des Projekts meldet danach statt 290 nur noch 4 Befunde (Abschnitt 4).
7. **Architektur:**
   - Die Datenschutz- und Integritätsmechanik ist eine echte Stärke.
   - Strukturell bleibt `ListApp` mit 41.063 Zeilen und 1.396 Methoden (76 % der Hauptdatei) der Engpass für Testbarkeit und Änderungsgeschwindigkeit; G27 „Aufteilen“ wartet auf die Versionsverwaltung.

## 2. Grundlage, Prüfumfang und Belegstufen

| Geprüft | Wie |
|---|---|
| Quellbaum `01_Repository/Glide` (src, tests, docs, scripts, CHANGELOG, AGENTS) | Vollständig, Stand Upload 01.10.2026 |
| Hauptdatei `src/glide/app.pyw` (= `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.32.3.pyw`) | AST-Analyse; gezieltes Lesen von Speicherweg, Änderungsrahmen, Undo, Verlauf, Menüs, Ansichten, Parsern, Startseite, Dialogen, `ICONS` |
| Projektdokumentation | AGENTS.md, ARBEITSRICHTUNG, DOKUMENTENPFLEGE, 00_INDEX, 01_PRODUCT_CONSTRAINTS, 02_ARCHITECTURE, 06_DATA, 07_QA_BERICHT, Entscheidungen, Arbeitsvorbereitung (Übergaben, Planung, Funktionsrecherche, Aufgabenauswahl, Bestandsprüfung 27.09.) |
| Ablage | Struktur, `.gitignore`/`.gitattributes`, Byte-Abgleich `src/glide` ↔ `07_Python-Versionen` ↔ Übergabepaket, Projekt-Standprüfung `tests/tools/standpruefung.py` |
| Laufzeit | Linux-Container, Xvfb; **Python 3.12.3 + Tk 8.6.14 (Ubuntu, mit Xft)** und **Python 3.14.0rc2 + Tk 8.6.14 (python-build-standalone, ohne Xft)**; isolierter `GLIDE_DATA_DIR`, künstliche Daten |

**Nicht geprüft:**
- macOS/Tk 9 (Referenzplattform), Windows
- die 58 Integrationssuiten (laufen unter macOS; unter Linux nicht abgenommen)
- echte Nutzerdaten, physische Bedienung

Linux-Ergebnisse ersetzen keine Abnahme auf macOS.

Belegstufen: **[gemessen]** in dieser Umgebung reproduziert · **[Code]** durch Quelltext belegt · **[Doku]** Aussage eines Dokuments · **[Einschätzung]** eigene Bewertung.

## 3. Code-Inventar

### 3.1 Dateien und Umfang [Code]

| Datei (`src/glide/`) | Zeilen | Rolle |
|---|---:|---|
| `app.pyw` | 54.251 | Hauptanwendung: Datenmodell, Oberfläche, Mutationen, Speicherung |
| `drawing.py` | 1.404 | Tk-freier Pixelkern: Zellmodell mit Palettenindizes, Werkzeuge, Aktions-Undo, PNG/ICO/SVG |
| `backdrop.py` | 455 | Hintergrundverläufe, PNG-Helfer |
| `page_markdown.py` | 380 | Markdown-Austausch für Seiten |
| `logo.py` | 314 | Logo, Akzentfarbe, Programmsymbole |
| `drawing_image.py` | 310 | Tk-Bildfunktionen für Zeichnungen |
| `image_preview.py` | 296 | Bildvorschau und Konvertierungswege je Plattform |
| `glide_start.py` | 57 | Start als Modul mit Bytecode-Cache (in 07: `Schnellstart.pyw`) |

**Abhängigkeiten zur Laufzeit:**
- nur Standardbibliothek und tkinter;
- optional mitgeliefertes `tkinterdnd2` 0.6.3 mit tkdnd-Binärdateien für macOS, Windows und Linux;
- Schriften DejaVu Sans 2.37 und Pixelify Sans (OFL).

### 3.2 Struktur der Hauptdatei [Code]

| Kennzahl | Wert |
|---|---:|
| Klassen (oberste Ebene) | 36 |
| Funktionen und Methoden (einschließlich verschachtelter) | 2.471 |
| davon Methoden von `ListApp` | 1.396 |
| `ListApp` | 41.063 Zeilen = 76 % |
| `ItemWorkspace` (Board/Reiter) | 4.539 Zeilen |
| `DrawingEditor` / `PageEditor` | 1.714 / 1.608 Zeilen |
| Median Methodenlänge / 90. Perzentil | 13 / 46 Zeilen |
| Methoden über 100 / über 200 Zeilen | 56 / 16 |
| Längste: `_refresh_home`, `item_form_dialog`, `create_ui` | 825 / 725 / 681 Zeilen |
| Kommentarzeilen + Docstringzeilen | ≈ 3.400 + ≈ 3.500 (≈ 13 %) |
| Funktionen mit modalem Fenster (`tk.Toplevel`) | 37 |

### 3.3 Datenmodell und Speicherung [Code]

- **Dateien:** `liste_speicher.json` mit `version` 20, `lists`, `folders`, `labels`, `trash`, `history`. Einstellungen in `settings.json`, Vorlagen in `vorlagen.json`, Anhänge in `attachments`.
- **Arten:**
  - Listenarten: Aufgaben, Notiz, Zeichnung, Seite, Galerie.
  - Ordnerarten: Ordner, Bibliothek, Notizbuch.
  - Punktarten: Aufgabe, Gruppe, Long-Task, Zwischenüberschrift.
- **Speichern** (`save_items`):
  - atomar über temporäre Datei, `fsync`, `os.replace` mit Wiederholung;
  - Sperrdatei mit Heartbeat;
  - Sicherungen nur bei geändertem Inhalt (max. 40, mind. 10, zusätzlich 14 Tagesstände);
  - Vorsicherung vor jedem Formatsprung;
  - neuere Dateien werden nur schreibgeschützt geöffnet.
- **Integrität:** `item_change`/`sidebar_change` bündeln Undo, Speichern und Neuzeichnen; `guarded_structural_change` vergleicht Punkt-IDs vor und nach Umbauten.
- **Undo:** bis 20 Schritte, jeder ein zlib-komprimierter JSON-Schnappschuss des *gesamten* Bestands (`PackedState`).
- **Änderungsverlauf:** entsteht beim Speichern aus dem Vergleich zweier vollständiger Vergleichsstände; höchstens 15 Einträge und 15 Tage (`MAX_HISTORY_ENTRIES`, `HISTORY_RETENTION_DAYS`).

### 3.4 Funktionsinventar (Kurzfassung) [Code]

Die Gegenüberstellung mit der Konkurrenz steht in der [Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md).

| Bereich | Vorhanden (Codebeleg) | Grenze laut Code |
|---|---|---|
| Erfassung | Eingabezeile, „Erweitert“-Maske, Schnellerfassung (`show_quick_capture`), `/`-Befehle (`SLASH_COMMANDS`), Datumshelfer `parse_capture_due` | Drei getrennte Datumsparser; `/morgen` setzt **Fälligkeit** |
| Planung | Mein Tag mit Tagesnavigation, Kapazität je Wochentag, Stundenraster/Zeitblöcke, In Bearbeitung, Verspätet, Nächste Aufgabe, Tagesbeginn, Tagesabschluss, Wochenrückblick, Kalender, Zeiterfassung, Abhängigkeiten | Kalender ist ein **modales Fenster**; kein Fokusmodus; keine Eisenhower-Ansicht |
| Organisation | Listen, Ordner, Bibliothek, Notizbuch, Labels, gespeicherte Filter, Archiv, Papierkorb, 16 Listen-/Ordnervorlagen + Notizbuch-/Seitenvorlagen, Reiter | Felder Glide-weit fest (bewusst) |
| Ansichten | Liste, Tabelle, Pinnwand (frei/Board, Verbindungen, Bereiche), globale Pinnwand, Galerie, Bibliothekskarten, Startseite mit 19 Kacheln (12 im Standard) | – |
| Seiten/Notizen | Block-Editor (13 Blockarten), 6 Inline-Formate, Bilder mit Umfluss, Markdown, Seitenaufgaben als echte Punkte, 16×16-Pixelsymbol | In Notizen keine Aufgabenzeilen (`NoteEditor.ALLOW_TASKS = False`); keine Seitenverweise |
| Pixel | 16–128 Zellen, Werkzeuge, Symmetrie, Muster, Kachelvorschau, Paletten (GPL/HEX/Aseprite/Adobe), PNG/ICO/SVG | Index 0 fest weiß; keine Animation |
| Suche | Schnellsuche über Titel, Ansichten, Filter, Punkttexte und Aktionen (`quick_open_results`) | Kein Inhalt von Seiten/Notizen/Beschreibungen; linear |
| Austausch | TXT, CSV, Markdown, ICS, Drucken/PDF, `.glidepage`, `.glideexchange`, Komplett- und App-Backup | Kein Notion-/Todoist-Import |
| Hinweise | Systemmitteilungen über `tk sysnotify` (Tk 9, laufende App), Dock-/Taskleistenhervorhebung | Stufe C (beendetes Programm) bewusst nicht |
| Darstellung | 10 Designs, Akzentfarbe, Schrift, Hintergrundverläufe, WCAG-Kontrastberechnung | Kein „wie System“ |
| Hilfe | Handbuch (F1), Tastenkürzel, Aktionssuche, Fußzeilen-Hinweise, Fehlerprotokoll; Probedaten „Rundgang“ und Showcase | Einstieg für neue Nutzer bewusst nicht gewählt (27.09.) |

## 4. Ablage im Repository (Upload 01.10.2026)

Das GitHub-Repository enthielt bis 01.10.2026 nur ein leeres README. Dieser Abschnitt hält den Upload-Befund und die Korrekturen fest.

| Befund | Wirkung | Korrektur | Beleg |
|---|---|---|---|
| Alle Projektordner lagen unter `01_Repository/` (eine Ebene zu tief). Alle Dokumente verweisen auf die Projektstruktur mit `00_Arbeitsvorbereitung`, `07_Python-Versionen` usw. neben `01_Repository/Glide` (AGENTS.md: `../../00_Arbeitsvorbereitung`) | Standprüfung des Projekts: **290 Befunde**, davon 288 tote Links | Projektordner in die Wurzel; `01_Repository/Glide` bleibt. Danach 41 Befunde | `standpruefung.py` vor/nach |
| Root-`.gitignore` (Python-Vorlage) schloss `*.so` aus | 44 tkdnd-Bibliotheken für Linux fehlten in 11 vendor-Kopien, auch im kanonischen `src/glide/vendor` | Wiederhergestellt; SHA-256 stimmen mit `SHA256SUMS.txt`/`abgleich.json` des Projekts überein; Ausnahme `!**/vendor/tkinterdnd2/**/*.so` | [`ergebnis.json`](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/ergebnis.json) |
| `Glide/.gitattributes` mit `* text=auto` wandelte CRLF in LF | 41 Drittdateien (tkdnd-Windows-Skripte, OFL-Lizenz) nicht mehr bytegleich zu 07 (123 Dateien inkl. Prüfkopien) | `**/vendor/** -text`, `**/resources/fonts/** -text`; Bytes aus 07 wiederhergestellt. `src/glide` = 07 bis auf README | wie oben |
| `Glide/.gitignore` schließt `*.glidebackup` außer `tests/fixtures/beispiele/*.glidebackup` aus | `tests/fixtures/showcase/Glide-Showcase.glidebackup` fehlte (im Manifest verlangt); Archivkopie `beispiele/archiv/glide_beispieldaten_3.32.3_vor_Showcase_…` fehlt | Showcase-Sicherung aus `05_Probelisten_Testdaten/Showcase` wiederhergestellt (SHA-256 laut `manifest.json`), Ausnahmen ergänzt. Die Archivkopie muss der Inhaber nachliefern | wie oben |
| `Glide/.gitignore` schließt `*.log` aus (bewusste Projektregel) | Prüfprotokolle fehlen; Arbeitsplanung verlinkt 3 Logs | Nicht geändert; Entscheidung D09 | Standprüfung R11 |
| Links mit `archiv/`, obwohl die Ordner `Archiv/` heißen (bzw. umgekehrt) | macOS ignoriert Groß-/Kleinschreibung, Linux/GitHub nicht: 37 tote Links im Dokumentationsindex | Im Index korrigiert | Standprüfung |
| 27 `.DS_Store`-Dateien | Rauschen | Entfernt, in `.gitignore` | – |
| `93_Zwischenstände/…` (1.931 Dateien, 286 MB) dupliziert den Stand vom 01.10. | Doppelte Wahrheit im Repository, große Checkouts | Unverändert (Beleg nach DOKUMENTENPFLEGE). Mit Git sind Zwischenstandsabbilder entbehrlich; Entscheidung D09 | – |
| Keine echten Nutzerdaten, keine persönlichen Fehlerprotokolle, keine Schlüssel gefunden | – | – | Dateisuche nach `liste_speicher.json`, `fehlerprotokoll`, Schlüsselmustern |

## 5. Laufzeitbefunde unter Linux

| Befund | Beleg | Bewertung |
|---|---|---|
| Start mit Python 3.12.3/Tk 8.6.14 (Ubuntu) ohne Fehler, leeres Fehlerprotokoll, 151 Widgets, Aufbau 0,34–0,70 s | [gemessen] [Startprobe](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/ergebnisse/startprobe_py3.12_tk8.6_xft.json), [Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/start_leer_tk86_mit_xft.png) | Python 3.12 ist nirgends als kompatibel dokumentiert, startet aber |
| `register_private_fonts` registriert DejaVu und Pixelify Sans über Fontconfig; „Pixelify Sans“ erscheint in `font families` | [gemessen] | Schließt den offenen Punkt „Pixelschrift auf echtem Linux“ der Bestandsprüfung vom 27.09. für Registrierung und Verfügbarkeit; Sichtprüfung offen |
| Mit Tk ohne Xft erscheinen alle Symbole als `◷` … | [gemessen] [Bild](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/bilder/start_leer_tk86_ohne_xft.png) | Umgebungseffekt. Für ein späteres Paket mit eingebettetem Python (G26/H-03): Tk **mit** Xft bündeln |
| Ansichtswechsel mit Beispieldaten: Liste 37 ms, Startseite 348 ms, Mein Tag 77 ms, Tabelle 62 ms, Bibliothek 148 ms, Seiten 66 ms, neue Seite 150 ms, Pinnwand 127 ms | [gemessen] Einzelmessung inkl. `update()` | Nur Größenordnung; Startseite ist die teuerste Ansicht (passt zu Rest P03) |
| Bildvorschau unter Linux nur PNG/GIF/SVG | [Code] `image_preview.py` | Plattformunterschied; in Produktgrenzen nur indirekt erwähnt |
| Der modale Kalender blockiert die Probe bis zum Schließen | [gemessen] | Bestätigt das modale Verhalten (U11) |

## 6. Abgleich Dokumentation ↔ Code

Kennungen AB01–AB17 (Abweichung). Die Claude-Übergabe ist laut eigener Regel eingefroren und bleibt unverändert; die übrigen Dokumente erhalten Korrektur oder Nachtrag mit Vorsicherung.

| Nr. | Fundstelle | Aussage | Befund | Bewertung | Umgang |
|---|---|---|---|---|---|
| AB01 | Claude-Übergabe §2 | Hauptdatei `app.pyw`, Starter `glide_start.py`, Rohwerte im Codepaket | Stimmt für das vorgesehene Paket `Glide_3.32.3_Python_Codebasis.zip` (`Archiv/Glide_3.32.3_Claude_Code_2026-10-01`). In dieser Sitzung wurde stattdessen `07_Python-Versionen.zip` übergeben; Laufzeitdateien bytegleich, Rohwerte nur im vorgesehenen Paket | Übergabefehler, kein Dokumentfehler | Hinweis in der Sitzungsübergabe |
| AB02 | Arbeitsplanung §3, §5 | Zeilenangaben 3.32.0 | Um 36–212 Zeilen verschoben; Funktionen vorhanden | als historisch gekennzeichnet | Lebende Dokumente: Funktionsnamen statt Zeilen |
| AB03 | `07_Python-Versionen/README.md` | Gliederung „Neu in 3.30 (Auszug)“ | 3.31/3.32 nur in einer Schlusszeile | veraltet | Beim nächsten Versionswechsel nachführen (bytegleicher Lieferordner, hier nicht geändert) |
| AB04 | `glide_start.py`, Docstring | „rund 48.000 Zeilen“ | 54.251 | veraltet | Nächster Produktionsschnitt |
| AB05 | Code-Kommentar bei `LIST_KIND_PAGE` | „Format 20 ist noch unveröffentlicht“ | seit 3.30 ausgeliefert | veraltet | Nächster Produktionsschnitt |
| AB06 | Code-Kommentar Wiederholungen | „Benachrichtigungen … Nicht-Ziel“ | Systemmitteilungen existieren; nur Hintergrunddienst fehlt | teilweise überholt | Nächster Produktionsschnitt |
| AB07 | Code-Kommentar `write_json_atomic` | „C-Kodierer statt Python-Schleife“ | Mit `indent=4` erst ab Python 3.14 in C. 10.000 Punkte: 176 ms (3.12) gegenüber 32 ms (3.14) | nur für 3.14 richtig | Kommentar ergänzen |
| AB08 | Kompatibilitätsangaben | „3.14/Tk 9; 3.13/Tk 8.6 eingeschränkt“ | Keine Versionsprüfung im Code; 3.12/Tk 8.6 startet | unvollständig | Mindestversion festlegen und prüfen |
| AB09 | Konkurrenzübersicht §8.4 | Kombination „liegt selten im Mittelpunkt“ | AFFiNE und AppFlowy fehlen | unvollständig | [Featurematrix §6](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md) |
| AB10 | D01 vs. Code | „morgen“ = Bearbeitungstag; Slash-Semantik bewahren | `/morgen` setzt `due` | Konzeptkonflikt | Entscheidung **D10** |
| AB11 | ARBEITSRICHTUNG, Sitzungsübergabe | „Git bleibt vertagt“ | Repository `glide-to-do` enthält das Projekt | durch Tatsachen überholt | Entscheidung **D09** |
| AB12 | Begriffe im Code | „Zwischenüberschrift“/„Überschrift“ für dieselbe Art; „Long-Task“; „Punkt“/„Listenpunkt“/„Aufgabe“ | – | uneinheitlich | UX-Befund U16 |
| AB13 | 01_PRODUCT_CONSTRAINTS (Abschnitt 3.19) | Änderungsverlauf „Obergrenze 4000 Einträge“ | `MAX_HISTORY_ENTRIES = 15`, `HISTORY_RETENTION_DAYS = 15` (CHANGELOG: „höchstens 15 Einträge und höchstens 15 Tage“) | **veraltet** | In den Produktgrenzen korrigiert |
| AB14 | 01_PRODUCT_CONSTRAINTS (Galerie) | JPEG/HEIC „nur unter macOS über `sips`“ | `image_preview.py` wandelt unter Windows über WIC/PowerShell; Linux nur PNG/GIF/SVG | **veraltet** | In den Produktgrenzen korrigiert |
| AB15 | 01_PRODUCT_CONSTRAINTS „Form folgt Funktion“ | „Farbe trägt Bedeutung: Grün bestätigt, Rot löscht, sonst neutral grau“ | `BUTTON_ROLE_RULES` kennt zusätzlich Lila = Hinzufügen (seit 29.09.) | veraltet | In den Produktgrenzen korrigiert |
| AB16 | 01_PRODUCT_CONSTRAINTS „Kein Symbol trägt zwei Bedeutungen“ | Regel | `ICONS`: ▲ = nach oben/verspätet/aufsteigend, ▼ = nach unten/Eingang/absteigend, ◷ = Verlauf/Zeiterfassung, ≡ = Details/Beschreibung, ◐ = In Bearbeitung/Mondviertel | Code verletzt Regel | UX-Befund U24 |
| AB17 | 01_PRODUCT_CONSTRAINTS „Bedienelemente ohne Wirkung … ausgeblendet“ | Regel | „Suche löschen“ steht auch bei leerer Suche | Code verletzt Regel | UX-Befund U03 |

## 7. Technische Befunde und Optimierungspotenziale

Grundsatz: Funktionierende Bereiche nicht umbauen, nur gemessene oder klar belegte Kosten angehen.

### T1 – Speicherweg skaliert mit dem Gesamtbestand (neu, gemessen)

Ein einziges Abhaken über `item_change` führt aus:

1. `snapshot_undo`: kompletter Bestand → JSON → zlib.
2. `save_items` → `update_history` → `history_snapshot` (alle Punkte, alle 19 Vergleichsfelder, SHA-256 jeder Beschreibung und Zeichnung) und `history_events`.
3. `write_json_atomic` des Gesamtbestands mit `fsync`.
4. `record_recent_list_edits`: JSON + SHA-256 **jeder Liste** und **jedes planbaren Punkts**; ggf. `save_settings`.
5. `refresh_reminder_status`, `update_sidebar_list`, `refresh_tree`.

**Messung** mit dem neuen Pflegewerkzeug [`messung_speicherweg.py`](../01_Repository/Glide/scripts/pflege/messung_speicherweg.py):
- Linux-VM, Xeon 2,1 GHz, künstliche Daten
- je ein Aufwärmlauf, dann 9 warme Läufe, Median / p95
- [Rohwerte](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/messung_speicherweg/)

| Bestand | Datei | Abhaken (3.14) | `save_items` (3.14) | Abhaken (3.12) | Erstes Speichern (3.14) |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 1,0 MB | **56 / 69 ms** | 39 / 48 ms | 73 / 101 ms | 86 ms |
| 5.000 | 5,0 MB | **218 / 257 ms** | 161 / 199 ms | – | 384 ms |
| 10.000 | 10,1 MB | **446 / 502 ms** | 356 / 491 ms | 613 / 722 ms | 844 ms |

**Aufschlüsselung** eines Abhakens bei 10.000 Punkten (cProfile, 3.14, [Profil](../01_Repository/Glide/tests/qa-3.32.3/analyse_planung_2026-10-01/messung_speicherweg/profil_abhaken_py3.14rc2_10000.txt)):
- **Anteile an `save_items`:** Änderungsverlauf ≈ 53 %, „zuletzt bearbeitet“/Aktivität ≈ 25 %, alle Dateischreibvorgänge inkl. `fsync` ≈ 9 %.
- **Außerhalb von `save_items`:** Undo-Paket ≈ 10 % dieser Zeit, dazu Seitenleiste, Erinnerungen und Baum.

**Einordnung [Einschätzung]:**
- Bei typischen persönlichen Beständen (1.000–3.000 Punkte) unkritisch.
- Ab etwa 5.000 Punkten wird jede Aktion spürbar träge, weil die Kosten pro Aktion linear wachsen, auch wenn nur ein Punkt geändert wurde.
- Auf einem aktuellen Mac sind die Absolutwerte kleiner, die Proportionen bleiben.
- Der 26.420-Punkte-Lasttest belegt Speichern/Laden, nicht die Bedienlatenz.

**Vorschlag P08:**
- **P08a – ein Durchlauf statt drei:**
  - Verlauf, „zuletzt bearbeitet“ und Aktivitätszählung aus *einer* gemeinsamen Pro-Liste-/Pro-Punkt-Signatur speisen.
  - Signaturen je Liste zwischenspeichern und nur für geänderte Listen neu berechnen.
  - Erwartung: etwa Halbierung bei gleicher Semantik.
- **P08b – gezielte Invalidierung:**
  - `item_change`/`sidebar_change` markieren betroffene Listen; nur diese werden verglichen.
  - Der Fünf-Minuten-Autosave vergleicht weiterhin vollständig. So bleibt die gewollte Vollständigkeit „jeder Weg läuft über `save_items`“ erhalten.
  - Abnahme mit Differenztest alt/neu.
- **Undo-Schnappschuss pro Liste:** größerer dritter Schritt, erst nach erneuter Messung.

### T2 – Neun vollständige Leseläufe beim ersten Speichern (neu, gemessen)

- **Befund:** `ensure_schema12_backup` … `ensure_schema20_backup` sind neun fast identische Methoden. Jede parst beim ersten Speichern der Sitzung `liste_speicher.json`, nur um `version` zu lesen.
- **Messung (10.000 Punkte, 3.14):** erstes Speichern 844 ms gegenüber 356 ms im Folgespeichern.
- **Korrektur:** eine Methode, die die Version einmal liest und die passende Vorsicherung anlegt; Dateinamen und Verhalten unverändert; etwa 120 Zeilen weniger. Unter einem halben Tag inkl. Test für alle Formatstufen.

### T3 – Monolith und Testbarkeit

- `ListApp` vereint Datenmodell, Persistenz, Fachlogik und Oberfläche. Fachlogik lässt sich nur mit Tk-Fenster testen; die 58 Suiten laufen rund 25 Minuten.
- G27 („Aufteilen von `app.pyw`“) wartet laut Funktionsrecherche auf die Versionsverwaltung.
- **Empfehlung D17 (Strangler):** Jede neue oder angefasste Fachlogik als Tk-freies Modul neben `drawing.py`, mit schnellen Unit-Tests. Reihenfolge: Datumsparser (G01), Wiederholung, Verlaufs-Diff (P08), Suchindex (G14), Referenzschicht (G08/G30).

### T4 – Automatische Prüfung im Repository

- Der Prüfstand liegt jetzt im Repository (`tests/tools/pruefen.py`, Standprüfung, 58 Suiten), läuft aber nur lokal unter macOS.
- **Vorschlag (mit D09):** schnelle CI-Stufe unter Linux/Xvfb:
  - Standprüfung, Syntax, Startprobe;
  - Tk-freie Unit-Tests (T3);
  - SHA-256-Abgleich `src/glide` ↔ `07_Python-Versionen`.
- Ersetzt **nicht** die Vollprüfung.

### T5 – Plattformen und Verteilung

- **Linux:** siehe Abschnitt 5. JPEG-Vorschau ließe sich ohne neue Python-Abhängigkeit über Systemwerkzeuge (`gdk-pixbuf`-Thumbnailer, ImageMagick) mit Rückfall lösen – analog zu `sips`/WIC.
- **Verteilung:** Der python.org-Installer für macOS liefert seit 3.14.5 Tk 9.0.3. Ein Paket mit eingebettetem Python 3.14 + Tk 9 (G26/H-03) beseitigt die Plattformunterschiede am wirksamsten (D15).

### T6 – Barrierefreiheit

- Tk 9.1 bringt mit `tk accessible` Screenreader-Unterstützung für Kern- und ttk-Widgets (ATK, MSAA, NSAccessibility). 9.1a1 erschien am 04.03.2026, stabile Freigabe war für September 2026 geplant ([TIP 733](https://core.tcl-lang.org/tips/doc/main/tip/733.md), [Tcl 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html)); Freigabestand am 01.10.2026 nicht verifiziert.
- **Risiko:** Glides selbstgezeichnete Canvas-Bedienelemente (`RoundedButton`, `CanvasLabel`, `OptionRows`, `LabelChip`) erhalten nicht automatisch Rollen und Namen.

### T7 – Weitere Beobachtungen (niedrige Priorität)

- **Drei Datumsparser und zwei Aktionssuchen:** Zusammenführung mit G01 bzw. U01.
- **Zwei vollständige Punkt-Editoren:** Detailbereich und Maske `item_form_dialog`, siehe U12.
- **Historische Erzählung in Kommentaren:** DOKUMENTENPFLEGE verlangt bereits „Entwicklungserzählungen gehören in Changelog bzw. Archiv“. Neue Kommentare danach ausrichten, bestehende nicht pauschal umschreiben.
- **Ausnahmebehandlung:** 46 × `except Exception`, 295 × `except tk.TclError`; durch Fehlerprotokoll abgefedert.

## 8. Stärken, die erhalten bleiben müssen

- **Datensicherheit:** atomares Schreiben, Vorsicherungen je Formatstufe, Tagesstände, Bestandswächter, schreibgeschützter Modus, Sperrdatei mit Heartbeat.
- **Rückgängig:** für alles, auch Strukturumbauten.
- **Tk-Fallstricke systematisch gelöst:** Menübefehle aufgeschoben, `pythonw`-Ströme, Größenereignisse, WCAG-Kontrast.
- **Mess- und Dokumentationskultur:** Vorher/Nachher, Median/p95, nummerierte Entscheidungen, Verträge, maschinelle Standprüfung.

## 9. Konsequenzen für die Planung

| Befund | Klasse | Übernahme |
|---|---|---|
| T1 Speicherweg | notwendig ab ca. 5.000 Punkten, sonst sinnvoll | P08a/P08b in Stufe 0 nach Rest P03/P04/P06 |
| T2 Schema-Sicherung | notwendig (klein) | Stufe 0 |
| AB03–AB08 Kommentare/Lieferordner | notwendig (klein) | Nächster Produktionsschnitt |
| AB13–AB15 Produktgrenzen | notwendig | In diesem Nachlauf korrigiert |
| AB16/AB17 Regelverstöße im Code | sinnvoll | UX-Bereinigung 1 |
| T3 Strangler-Module | sinnvoll | Mit jeder Feature-Etappe (D17) |
| T4 CI-Grundstufe | sinnvoll | Stufe 0, abhängig von D09 |
| T5 Linux/Verteilung | sinnvoll | Stufe 4 (D15); JPEG-Rückfall Linux klein in Stufe 1 |
| T6 Barrierefreiheit | Zukunft | Nach stabiler Tk-9.1-Freigabe und Paketentscheidung |
