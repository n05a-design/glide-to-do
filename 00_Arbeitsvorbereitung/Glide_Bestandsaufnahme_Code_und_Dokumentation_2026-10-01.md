# Glide – Bestandsaufnahme Code und Dokumentation

Stand **01.10.2026** · Codebasis **3.32.3** (Aufgabenformat 20) · Teil 1 von 4 der Analyse vom 01.10.2026

Zugehörig: [Konkurrenz- und Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md) · [Produktprinzipien und UX-Prüfung](Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md) · [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md) · [Entscheidungsvorlage](Glide_Entscheidungsvorlage_2026-10-01.md) · [Messungen und Werkzeuge](Analyse_2026-10-01/README.md)

## 1. Ergebnis in Kürze

1. **Die Dokumentation beschreibt den Funktionsstand weitgehend richtig.** Alle 18 Einstiegspunkte der Claude-Übergabe stimmen zeilengenau mit dem Code überein. Die Arbeits- und Featureplanung führt ihre Zeilenangaben ausdrücklich als historischen Stand 3.32.0; sie sind um 36 bis 212 Zeilen verschoben, die Funktionen existieren aber alle.
2. **Es gibt neun konkrete Abweichungen zwischen Doku und Code** (Abschnitt 5). Keine betrifft Datensicherheit. Am wichtigsten: Die Übergabe beschreibt Dateinamen und Messrohdaten, die im übergebenen Codepaket nicht enthalten sind, und mehrere Code-Kommentare sind sachlich überholt.
3. **Neuer, gemessener Leistungsbefund:** Jede Änderung prüft den *gesamten* Bestand dreimal auf Unterschiede (Änderungsverlauf, „zuletzt bearbeitet“, Aktivitätszählung) und legt einen vollständigen Rückgängig-Schnappschuss an. Das kostet bei 10.000 Aufgaben **rund 460 ms pro Abhaken** (Python 3.14), bei 1.000 Aufgaben rund 56 ms. Das ist bisher nicht Teil von P01–P07 und wird als **P08** vorgeschlagen.
4. **Das erste Speichern jeder Sitzung liest die Datendatei neunmal vollständig ein** (Schema-Sicherungen Format 12–20). Bei 10 MB kostet das rund 0,65 s zusätzlich. Kleine, risikoarme Korrektur.
5. **Linux läuft, aber mit deutlich eingeschränktem Erlebnis:** Start mit Python 3.12/Tk 8.6 fehlerfrei. Distributionen liefern aber meist noch Tk 8.6 (keine Systemmitteilungen, kein SVG). JPEG-Vorschauen gibt es unter Linux grundsätzlich nicht. Ohne Xft-fähiges Tk erscheinen die Symbole als `◷`.
6. **Architektur:** Die Datenschutz- und Integritätsmechanik ist ungewöhnlich gründlich und eine echte Stärke. Strukturell bleibt `ListApp` mit 41.063 Zeilen und 1.396 Methoden der Engpass für Testbarkeit und Änderungsgeschwindigkeit (76 % der Hauptdatei).
7. **Das Repository war bis zu dieser Analyse leer.** Testinfrastruktur, Verträge (`docs/`), Pflegewerkzeuge und CHANGELOG liegen nur im lokalen Projektpaket. Damit sind die meisten Doku-Verweise hier nicht auflösbar, und es gibt keine automatische Prüfung (Entscheidung E01).

## 2. Grundlage, Prüfumfang und Belegstufen

| Geprüft | Wie |
|---|---|
| Codepaket `07_Python-Versionen` (146 Dateien, 139 Laufzeitdateien) | Vollständig entpackt, SHA-256 aller Laufzeitdateien in [`sha256_07_Laufzeitdateien.txt`](Analyse_2026-10-01/ergebnisse/sha256_07_Laufzeitdateien.txt) |
| Hauptdatei `Glide-Aufgaben-und-Listen_v3.32.3.pyw` | AST-Analyse (Klassen, Methoden, Längen), gezieltes Lesen von Speicherweg, Änderungsrahmen, Undo, Verlauf, Menüs, Ansichten, Parser, Startseite, Dialogen |
| Module `drawing.py`, `image_preview.py`, `page_markdown.py`, `logo.py`, `backdrop.py`, `drawing_image.py`, `Schnellstart.pyw` | API-Überblick und Abgleich der Dokumentangaben |
| Dokumente | Claude-Übergabe 3.32.3, Sitzungsübergabe, Arbeits- und Featureplanung, Konkurrenzübersicht, `07_Python-Versionen/README.md` |
| Laufzeit | Linux-Container, Xvfb, **Python 3.12.3 + Tk 8.6.14 (Ubuntu, mit Xft)** und **Python 3.14.0rc2 + Tk 8.6.14 (python-build-standalone, ohne Xft)**; isolierter `GLIDE_DATA_DIR`, künstliche Daten |

**Nicht geprüft:** macOS/Tk 9 (Referenzplattform des Inhabers), Windows, die 58 Integrationssuiten (nicht im Paket), echte Nutzerdaten, physische Bedienung. Online-/Linux-Ergebnisse ersetzen keine Abnahme auf macOS.

Belegstufen in diesem Dokument: **[gemessen]** in dieser Umgebung reproduziert · **[Code]** durch Quelltext belegt · **[Doku]** Aussage eines Dokuments · **[Einschätzung]** eigene Bewertung.

## 3. Code-Inventar

### 3.1 Dateien und Umfang [Code]

| Datei | Zeilen | Rolle |
|---|---:|---|
| `Glide-Aufgaben-und-Listen_v3.32.3.pyw` | 54.251 | Hauptanwendung: Datenmodell, Oberfläche, Mutationen, Speicherung (im Projekt `src/glide/app.pyw`) |
| `drawing.py` | 1.404 | Tk-freier Pixelkern: Zellmodell mit Palettenindizes, Werkzeuge, Aktions-Undo, PNG/ICO/SVG |
| `backdrop.py` | 455 | Hintergrundverläufe, PNG-Helfer |
| `page_markdown.py` | 380 | Markdown-Austausch für Seiten |
| `logo.py` | 314 | Logo, Akzentfarbe, Programmsymbole |
| `drawing_image.py` | 310 | Tk-Bildfunktionen für Zeichnungen |
| `image_preview.py` | 296 | Bildvorschau und Konvertierungswege je Plattform |
| `Schnellstart.pyw` | 57 | Start als Modul mit Bytecode-Cache (im Projekt `glide_start.py`) |

Abhängigkeiten zur Laufzeit: nur Standardbibliothek und tkinter; optional mitgeliefertes `tkinterdnd2` 0.6.3 mit tkdnd-Binärdateien für macOS, Windows und Linux. Schriften: DejaVu Sans 2.37, Pixelify Sans (OFL). Herkunft und Prüfsummen stehen in `vendor/provenance.json` und `resources/fonts/provenance.json`.

### 3.2 Struktur der Hauptdatei [Code]

| Kennzahl | Wert |
|---|---:|
| Klassen (oberste Ebene) | 36 |
| Funktionen und Methoden (einschließlich verschachtelter) | 2.471 |
| davon Methoden von `ListApp` | 1.396 |
| `ListApp`, Zeilen 12654–53716 | 41.063 Zeilen = 76 % |
| `ItemWorkspace` (Board/Reiter) | 4.539 Zeilen |
| `DrawingEditor` / `PageEditor` | 1.714 / 1.608 Zeilen |
| Median Methodenlänge / 90. Perzentil | 13 / 46 Zeilen |
| Methoden über 100 / über 200 Zeilen | 56 / 16 |
| Längste: `_refresh_home`, `item_form_dialog`, `create_ui` | 825 / 725 / 681 Zeilen |
| Kommentarzeilen + Docstringzeilen | ≈ 3.400 + ≈ 3.500 (≈ 13 %) |
| Modale Fenster (`tk.Toplevel`) | 37 Funktionen |
| `bind`-Aufrufe / `after`-Aufträge | 652 / 73 |

Zum Vergleich mit der Planung (3.32.0: „38 Klassen, 2.461 Funktionen“): Die Zählweise weicht leicht ab, die Größenordnung stimmt.

### 3.3 Datenmodell und Speicherung [Code]

- **Eine Datei** `liste_speicher.json` mit `version` 20, `lists`, `folders`, `labels`, `trash`, `history`. Einstellungen getrennt in `settings.json`, Vorlagen in `vorlagen.json`, Anhänge im Ordner `attachments`.
- **Listenarten** (`LIST_KINDS`): Aufgaben, Notiz, Zeichnung, Seite, Galerie. **Ordnerarten:** Ordner, Bibliothek, Notizbuch. **Punktarten:** Aufgabe, Gruppe, Long-Task, Zwischenüberschrift.
- **Punktfelder (Format 20):** Text, erledigt/`done_at`, Wichtigkeit 0–3, `due`/`due_time`, `planned_date`/`planned_time`, `estimated_minutes`, `time_spent_minutes`, Wiederholung, Erinnerung, Labels, Farbe, Beschreibung, Anhänge, Checkliste (max. 50), `links`, `blocked_by` (max. 50 Verweise), Unterpunkte.
- **Speichern** (`save_items`, Z. 37456): atomar über temporäre Datei, `fsync`, `os.replace` mit Wiederholung unter Windows; Sperrdatei mit Heartbeat auch für fremde Rechner; automatische Sicherungen nur bei geändertem Inhalt (max. 40, mind. 10, zusätzlich 14 Tagesstände); Vorsicherung vor jedem Formatsprung; neuere Dateien werden nur schreibgeschützt geöffnet (`NewerDataError`).
- **Integrität:** `item_change`/`sidebar_change` (`ChangeRecord`) bündeln Undo, Speichern und Neuzeichnen; `guarded_structural_change` vergleicht Punkt-IDs vor und nach Umbauten und stellt bei Verlust den vorherigen Stand wieder her.
- **Undo:** bis 20 Schritte, jeder ein zlib-komprimierter JSON-Schnappschuss des *gesamten* Bestands (`PackedState`).
- **Änderungsverlauf (Format 15):** entsteht beim Speichern aus dem Vergleich zweier vollständiger Vergleichsstände (`history_snapshot` → `history_events`), max. 15 Einträge bzw. 15 Tage.

### 3.4 Funktionsinventar (Kurzfassung) [Code]

Die vollständige Gegenüberstellung mit der Konkurrenz steht in der [Featurematrix](Glide_Konkurrenz_und_Featurematrix_2026-10-01.md). Hier nur der Codebeleg je Bereich:

| Bereich | Vorhanden (Codebeleg) | Grenze laut Code |
|---|---|---|
| Erfassung | Eingabezeile, „Erweitert“-Maske, Schnellerfassung (`show_quick_capture`), `/`-Befehle (`SLASH_COMMANDS`: Wochentage, heute/morgen, Wichtigkeit, Labels, `/meintag`), Datumshelfer `parse_capture_due` | Drei getrennte Datumsparser (`parse_due_input`, `parse_capture_due`, `parse_slash_commands`); `/morgen` setzt **Fälligkeit** |
| Planung | Mein Tag mit Tagesnavigation, Kapazität je Wochentag, Stundenraster/Zeitblöcke, In Bearbeitung, Verspätet, Nächste Aufgabe, Tagesbeginn, Tagesabschluss, Wochenrückblick, Kalender (Monat/Woche), Zeiterfassung (`running_timer`), Abhängigkeiten | Kalender ist ein **modales Fenster**; kein Fokusmodus/Pomodoro; keine Eisenhower-Ansicht |
| Organisation | Listen, Ordner, Bibliothek, Notizbuch, Labels, gespeicherte Filter, Archiv, Papierkorb, Vorlagen (16 mitgeliefert), Reiter | Felder sind Glide-weit fest (bewusst) |
| Ansichten | Liste, Tabelle (Spaltenwahl), Pinnwand (frei/Board, Verbindungen, Bereiche), globale Pinnwand, Galerie, Bibliothekskarten, Startseite mit 19 Kacheln | – |
| Seiten/Notizen | Block-Editor (13 Blockarten inkl. Aufklapp- und Hinweisblock), 6 Inline-Formate, Bilder mit Größe/Lage, Markdown-Import/-Export, Seitenaufgaben als echte Punkte, Seitensymbol 16×16 Pixel | In Notizen keine Aufgabenzeilen (`NoteEditor.ALLOW_TASKS = False`); keine internen Seitenlinks |
| Pixel | 16/32/64/128 Zellen, Werkzeuge, Symmetrie, Muster, Kachelvorschau, Paletten (GPL/HEX/Aseprite/Adobe), Export PNG/ICO/SVG | Index 0 fest weiß; keine Animation |
| Suche | Schnellsuche über Titel von Listen/Ordnern, Ansichten, Filtern, Punkttexten und Aktionen (`quick_open_results`) | **Kein Inhalt** von Seiten/Notizen/Beschreibungen; lineare Suche |
| Austausch | TXT, CSV, Markdown, ICS (Import/Export), Drucken/PDF, Glide-Seiten, `.glideexchange` für KI, Komplett- und App-Backup | Kein Notion-/Todoist-Import |
| Hinweise | Systemmitteilungen über `tk sysnotify` (nur Tk 9, nur bei laufender App), Dock-/Taskleistenhervorhebung | Kein Hintergrunddienst |
| Darstellung | 10 Designs, Akzentfarbe, Schriftfamilie/-größe, Hintergrundverläufe, WCAG-Kontrastberechnung | **Kein „wie System“** (Hell/Dunkel folgt nicht dem Betriebssystem) |
| Hilfe | Handbuch (F1), Tastenkürzel, Aktionssuche, Fußzeilen-Hinweise je Ansicht, Fehlerprotokoll | Kein geführter Erststart |

## 4. Laufzeitbefunde unter Linux

| Befund | Beleg | Bewertung |
|---|---|---|
| Start mit Python 3.12.3/Tk 8.6.14 (Ubuntu) ohne Fehler, leeres Fehlerprotokoll, 151 Widgets, Aufbau 0,34–0,70 s | [gemessen] [`startprobe_py3.12…json`](Analyse_2026-10-01/ergebnisse/startprobe_py3.12_tk8.6_xft.json), [Bild](Analyse_2026-10-01/bilder/start_leer_tk86_mit_xft.png) | Python 3.12 ist nirgends als kompatibel dokumentiert, funktioniert aber für den Grundaufbau |
| Mit Tk ohne Xft (python-build-standalone) erscheinen alle Symbole als `◷`, `⎙` … | [gemessen] [Bild](Analyse_2026-10-01/bilder/start_leer_tk86_ohne_xft.png) | Umgebungseffekt, kein Fehler im üblichen Distributions-Tk. Wichtig für ein späteres Paket mit eingebettetem Python (H-03): Tk **mit** Xft/Fontconfig bündeln |
| Ansichtswechsel mit Beispieldaten: Liste 37 ms, Startseite 348 ms, Mein Tag 77 ms, Tabelle 62 ms, Bibliothek 148 ms, Seitenübersicht 66 ms, neue Seite 150 ms, Pinnwand 127 ms | [gemessen] [`ansichten_probe_py3.12.json`](Analyse_2026-10-01/ergebnisse/ansichten_probe_py3.12.json), Einzelmessung inkl. `update()` | Nur Größenordnung; die Startseite ist die teuerste Ansicht (passt zu Rest P03) |
| Bildvorschauen unter Linux nur PNG, GIF, SVG; JPEG/HEIC/WebP zeigen nur die Endung | [Code] Docstring `image_preview.py` | Für Seiten und Galerie ein spürbarer Plattformunterschied, nirgends in Nutzerdoku genannt |
| Tk 8.6: keine Systemmitteilungen, kein SVG, Logo als gezeichnete Fläche | [Code] `system_notification_backend`, [Doku] 07-README | Ubuntu 24.04 liefert Tk 8.6 – Linux-Nutzer erhalten standardmäßig den eingeschränkten Modus |
| Der modale Kalender blockiert die Probe bis zum Schließen | [gemessen] | Bestätigt das modale Verhalten (UX-Befund U11) |

## 5. Abgleich Dokumentation ↔ Code

| Nr. | Fundstelle | Aussage | Befund im Code/Paket | Bewertung | Empfehlung |
|---|---|---|---|---|---|
| A1 | Claude-Übergabe §2 | „Die Original-Hauptdatei heißt hier `app.pyw`; `glide_start.py` entspricht `Schnellstart.pyw`.“ | Das ZIP enthält `Glide-Aufgaben-und-Listen_v3.32.3.pyw` und `Schnellstart.pyw`, kein `app.pyw`/`glide_start.py` | **widersprüchlich** | In lebenden Dokumenten beide Namen nennen (Projekt ↔ 07). Die Übergabe selbst bleibt laut eigener Regel unverändert; Korrektur hier und im [Repository-README](../README.md) |
| A2 | Claude-Übergabe §4 | „Rohwerte für 100/1.000/10.000 Aufgaben liegen im Codepaket.“ | Im ZIP liegen keine Messdateien | **fehlt** | Rohwerte aus `tests/qa-3.32.2/…` ins Repository übernehmen (E01) |
| A3 | Arbeitsplanung §3, §5 | Zeilenangaben 3.32.0 (z. B. `parse_due_input` 36214, `quick_open_results` 52256) | Jetzt 36390 bzw. 52457; alle genannten Funktionen existieren (`time_spent_minutes` ist ein Feld, keine Funktion) | veraltet, aber als historisch gekennzeichnet | In lebenden Dokumenten Funktionsnamen statt Zeilen verwenden; Zeilen nur in datierten Verträgen |
| A4 | `07_Python-Versionen/README.md` | Gliederung „Neu in 3.30 (Auszug)“, 3.31/3.32 fehlen bis auf eine Schlusszeile | – | veraltet | Beim nächsten Versionswechsel mit `versionswechsel.py` nachführen; die Datei gehört zum bytegleichen Paket und wurde deshalb hier **nicht** geändert |
| A5 | `Schnellstart.pyw`, Docstring | „rund 48.000 Zeilen“ | 54.251 Zeilen | veraltet | Beim nächsten Produktionsschnitt korrigieren (Zahl weglassen) |
| A6 | Code-Kommentar bei `LIST_KIND_PAGE` (Z. 13751) | „Format 20 ist noch unveröffentlicht“ | Format 20 ist seit 3.30 ausgeliefert | veraltet | Kommentar kürzen |
| A7 | Code-Kommentar Wiederholungen (Z. 13864) | „Benachrichtigungen … bleiben ein Nicht-Ziel, weil sie einen Hintergrunddienst bräuchten“ | Systemmitteilungen existieren seit 3.30 (`tk sysnotify`), nur ohne Hintergrunddienst | teilweise überholt | Auf „kein Hintergrunddienst“ präzisieren |
| A8 | Code-Kommentar `write_json_atomic` | „`dumps` in einem Stück … der C-Kodierer statt der Python-Schleife“ | Mit `indent=4` nutzt Python **bis 3.13** den reinen Python-Kodierer; erst 3.14 kodiert eingerückt in C. Gemessen 10.000 Punkte: 153 ms (3.12) gegenüber 29 ms (3.14) | nur für 3.14 richtig | Kommentar ergänzen; für das als kompatibel beschriebene 3.13 ist das Speichern spürbar langsamer |
| A9 | Kompatibilitätsangaben (Übergabe, 07-README) | „Python 3.14/Tk 9; 3.13/Tk 8.6 eingeschränkt“ | Es gibt keine Versionsprüfung im Code; 3.12/Tk 8.6 startet; Syntax ist ab 3.10 gültig | unvollständig | Mindestversion festlegen und beim Start prüfen (freundliche Meldung statt Folgefehler) |
| A10 | Konkurrenzübersicht §8.4 | Kombination aus Seiten, Aufgaben, Pinnwand und lokalen Daten „liegt selten im Mittelpunkt“ | AFFiNE und AppFlowy (beide quelloffen, lokal, je ~70.000 GitHub-Sterne) fehlen im Vergleich | unvollständig | Positionierung schärfen, siehe Featurematrix §6 |
| A11 | D01 vs. Code | D01: „morgen“ setzt den Bearbeitungstag; Slash-Semantik bewahren | `/morgen` setzt `due` (`SLASH_COMMANDS`: „fällig morgen“) | **Konzeptkonflikt** | Kein Doku-Fehler. Zwei Bedeutungen desselben Worts verwirren; Entscheidung **E02** |
| A12 | Sitzungsübergabe §3 „Git vorerst nicht“ | Git vertagt | Das GitHub-Repository `glide-to-do` existiert und enthält jetzt den Stand | überholt durch Tatsachen | Entscheidung **E01** |
| A13 | Begriffe im Code | `ITEM_KIND_LABELS` „Zwischenüberschrift“, `ITEM_KIND_NAMES` „Überschrift“; „Long-Task“; „Punkt“/„Listenpunkt“/„Aufgabe“ gemischt | – | uneinheitlich | Glossar festlegen (UX-Befund U16) |

Die Übergabe selbst ist laut eigener Regel ein eingefrorener Stand und bleibt unverändert. Die übrigen Dokumente erhalten einen datierten Nachtrag mit Verweis auf diese Analyse; Vorfassungen liegen in [`Archiv/`](Archiv/).

## 6. Technische Befunde und Optimierungspotenziale

Grundsatz: Funktionierende Bereiche nicht umbauen, nur gemessene oder klar belegte Kosten angehen.

### T1 – Speicherweg skaliert mit dem Gesamtbestand (neu, gemessen)

Ein einziges Abhaken über `item_change` führt aus:

1. `snapshot_undo`: kompletter Bestand → JSON → zlib.
2. `save_items` → `update_history` → `history_snapshot` (alle Punkte, alle 19 Vergleichsfelder, SHA-256 jeder Beschreibung und jeder Zeichnung) und `history_events` (Vergleich vorher/nachher).
3. `write_json_atomic` des Gesamtbestands mit `fsync`.
4. `record_recent_list_edits`: JSON + SHA-256 **jeder Liste** (`list_edit_signatures`) und zusätzlich **jedes planbaren Punkts**; anschließend ggf. `save_settings`.
5. `refresh_reminder_status`, `update_sidebar_list`, `refresh_tree`.

**Messung** (Linux-VM, Xeon 2,1 GHz, künstliche Daten, Median warm, [Rohdaten](Analyse_2026-10-01/ergebnisse/)):

| Bestand | Datei | Abhaken gesamt (3.14) | `save_items` (3.14) | Abhaken (3.12) | Erstes Speichern (3.14) |
|---:|---:|---:|---:|---:|---:|
| 1.000 | 1,0 MB | **56 ms** | 37 ms | 80 ms | 88 ms |
| 5.000 | 5,0 MB | **232 ms** | 179 ms | – | 456 ms |
| 10.000 | 10,1 MB | **458 ms** | 357 ms | 685 ms | 1.018 ms |

Aufschlüsselung eines Abhakens bei 10.000 Punkten (cProfile, 3.14, [Profil](Analyse_2026-10-01/ergebnisse/profil_abhaken_py3.14rc2_10000.txt)): Änderungsverlauf **≈ 51 %** von `save_items`, „zuletzt bearbeitet“/Aktivität **≈ 28 %**, alle Dateischreibvorgänge inkl. `fsync` **≈ 8 %**. Zusätzlich vor dem Speichern das Undo-Paket (≈ 75 ms) sowie Seitenleiste, Erinnerungen und Baum.

**Einordnung [Einschätzung]:** Bei typischen persönlichen Beständen (1.000–3.000 Punkte) ist das unkritisch. Ab etwa 5.000 Punkten wird jede Aktion spürbar träge, weil die Kosten pro Aktion linear wachsen, auch wenn nur ein Punkt geändert wurde. Auf einem aktuellen Mac sind die Absolutwerte kleiner, die Proportionen bleiben. Ein 26.420-Punkte-Lasttest existiert laut Planung nur für Speichern/Laden, nicht für Bedienlatenz.

**Vorschlag P08 (zwei Stufen):**
- **P08a – ein Durchlauf statt drei:** Verlauf, „zuletzt bearbeitet“ und Aktivitätszählung aus *einer* gemeinsamen Pro-Liste-/Pro-Punkt-Signatur speisen. Die Signaturen je Liste werden zwischengespeichert und nur für Listen neu berechnet, die sich seit dem letzten Speichern geändert haben. Erwartung: etwa Halbierung bei unveränderter Semantik.
- **P08b – gezielte Invalidierung:** `item_change`/`sidebar_change` kennen die betroffenen IDs. Sie markieren die betroffenen Listen als „schmutzig“, und nur diese werden verglichen. Zur Absicherung vergleicht der Fünf-Minuten-Autosave weiterhin vollständig. So bleibt die bewusst gewählte Vollständigkeit „jeder Weg läuft über `save_items`“ erhalten.
- Undo-Schnappschuss pro Liste statt Gesamtbestand ist ein dritter, größerer Schritt. Erst nach P08a/b und neuer Messung entscheiden.

### T2 – Neun vollständige Leseläufe beim ersten Speichern (neu, gemessen)

`ensure_schema12_backup` … `ensure_schema20_backup` sind neun fast identische Methoden. Jede öffnet beim ersten Speichern der Sitzung `liste_speicher.json` und parst sie komplett, nur um `version` zu lesen. Erstes Speichern bei 10.000 Punkten: 1.018 ms gegenüber 357 ms im Folgespeichern (3.14).

**Korrektur:** Eine Methode `ensure_schema_backup()`, die die Version einmal liest und die passende Vorsicherung anlegt. Verhalten und Dateinamen bleiben gleich. Das spart etwa 120 Zeilen doppelten Code („keine Funktion doppelt“ auch im Code). Aufwand: unter einem halben Tag inklusive Test für alle Formatstufen. Risiko: gering, aber Datenpfad – Vorsicherungstest verpflichtend.

### T3 – Monolith und Testbarkeit

- `ListApp` vereint Datenmodell, Persistenz, Fachlogik (Termine, Wiederholung, Verlauf, Suche) und Oberfläche. Fachlogik lässt sich deshalb nur mit Tk-Fenster testen; die 58 Suiten laufen rund 25 Minuten.
- Die Entscheidung „große Monolith-Aufteilung zurückgestellt“ ist richtig. Ein Umbau in einem Schritt wäre bei 41.000 Zeilen ohne Typprüfung riskant.
- **Empfehlung (Strangler-Prinzip, E10):** Jede neue oder angefasste Fachlogik als Tk-freies Modul neben `drawing.py` ablegen, mit eigenen schnellen Unit-Tests. Kandidaten in Reihenfolge des Nutzens: Datums-/Eingabeparser (G01), Wiederholungsregeln, Verlaufs-Diff (P08), Suchindex (G14), Referenzschicht (G08/G30). `ListApp` ruft diese Module nur noch auf. So schrumpft der Monolith nebenbei, ohne eigenes Umbauprojekt.

### T4 – Keine automatische Prüfung im Repository

- Die Vollprüfung existiert nur lokal (macOS, 25 Minuten).
- Vorschlag: eine schnelle CI-Stufe (Linux, Xvfb, Python 3.12 und 3.14, Tk 8.6) mit Startprobe, Syntaxprüfung, den künftigen Tk-freien Unit-Tests und dem SHA-256-Abgleich des Laufzeitordners. Die Werkzeuge in [`Analyse_2026-10-01/werkzeuge`](Analyse_2026-10-01/werkzeuge/) sind dafür ein Startpunkt.
- Ersetzt **nicht** die macOS-Vollprüfung, fängt aber Syntax-, Import- und Startfehler sowie versehentliche Paketänderungen vor jeder Lieferung ab.

### T5 – Plattformen und Verteilung

- Linux: siehe Abschnitt 4. JPEG-Vorschau ließe sich ohne neue Python-Abhängigkeit über vorhandene Systemwerkzeuge (`gdk-pixbuf`-Thumbnailer, ImageMagick) mit Fallback lösen – analog zum bestehenden PowerShell-/`sips`-Weg.
- Verteilung: Glide braucht ein separat installiertes Python. Der python.org-Installer für macOS liefert seit 3.14.5 Tcl/Tk 9.0.3 mit ([Quelle](https://discuss.python.org/t/python-org-macos-installer-users-of-tkinter-python-3-14-with-tcl-tk-9-0-3-instead-of-8-6-17/107206)). Unter Windows und Linux ist Tk 9 nicht selbstverständlich. Ein Paket mit eingebettetem Python 3.14 und Tk 9 (H-03/G26) würde die Plattformunterschiede am wirksamsten beseitigen (E07).

### T6 – Barrierefreiheit

- Tk 9.1 bringt mit `tk accessible` erstmals Screenreader-Unterstützung für Kern- und ttk-Widgets (ATK, MSAA, NSAccessibility). Version 9.1a1 erschien am 04.03.2026, stabile Freigabe ist für September 2026 geplant ([TIP 733](https://core.tcl-lang.org/tips/doc/main/tip/733.md), [Tcl 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html)). Ob 9.1 am 01.10.2026 bereits final ist, wurde nicht verifiziert.
- **Risiko [Einschätzung]:** Glide zeichnet zentrale Bedienelemente selbst auf `tk.Canvas` (`RoundedButton`, `CanvasLabel`, `OptionRows`, `LabelChip` …). Diese erhalten nicht automatisch Rollen und Namen und brauchen eine explizite Beschriftung über die neue API. Das ist bei einer späteren Barrierefreiheitsetappe einzuplanen.

### T7 – Weitere Beobachtungen (niedrige Priorität)

- **Drei Datumsparser** (`parse_due_input`, `parse_capture_due`, `parse_slash_commands`) und **zwei Aktionssuchen** (Schnellsuche und Aktionsdialog) – Zusammenführung gehört zu G01 bzw. U01.
- **Zwei vollständige Punkt-Editoren:** Detailbereich (`render_detail_pane`, „alle Felder außer Anhängen“) und Maske (`item_form_dialog`, 725 Zeilen) – siehe U12.
- **Historische Erzählung in Kommentaren** („Bis 27.09.2026 stand hier …“) macht den Code nachvollziehbar, vergrößert aber das Rauschen. Neue Kommentare sollten den heutigen Grund nennen; die Historie gehört in CHANGELOG/Verträge. Bestehende Kommentare nicht pauschal umschreiben.
- Ausnahmebehandlung: 46 × `except Exception`, 295 × `except tk.TclError`. Für Tk üblich und durch Fehlerprotokoll und `report_callback_exception` abgefedert; kein Handlungsbedarf.

## 7. Stärken, die erhalten bleiben müssen

- **Datensicherheit auf hohem Niveau:** atomares Schreiben mit `fsync`, Vorsicherungen je Formatstufe, Tagesstände, Bestandswächter, schreibgeschützter Modus für neuere Formate, Sperrdatei mit Heartbeat auch für synchronisierte Ordner.
- **Rückgängig für alles**, auch Strukturumbauten, und ein konsistenter Änderungsrahmen.
- **Tk-Fallstricke systematisch gelöst:** Menübefehle unter macOS aufgeschoben, `pythonw`-Ströme abgesichert, Größenereignisse gefiltert, Kontrast nach WCAG berechnet.
- **Messkultur:** Performance-Arbeit mit Vorher/Nachher, Median/p95 und Grenzen der Aussage.
- **Dokumentationskultur:** Entscheidungen nummeriert und datiert, Verträge je Version, Belegstufen.

## 8. Konsequenzen für die Planung

| Befund | Klasse | Übernahme in den Plan |
|---|---|---|
| T1 Speicherweg | notwendig ab ca. 5.000 Punkten, sonst sinnvoll | P08a/P08b in Stufe 0 nach Rest P03/P04/P06 |
| T2 Schema-Sicherung | notwendig (klein, risikoarm) | Stufe 0 |
| A1–A9 Doku-/Kommentarkorrekturen | notwendig (klein) | Mit dem nächsten Produktionsschnitt bzw. sofort in lebenden Dokumenten |
| T3 Strangler-Module | sinnvoll | Mit jeder Feature-Etappe, beginnend mit G01 |
| T4 CI-Grundstufe | sinnvoll | Stufe 0/1, abhängig von E01 |
| T5 Linux/Verteilung | sinnvoll | Stufe 4 (E07); JPEG-Fallback Linux klein in Stufe 1 |
| T6 Barrierefreiheit | Zukunft | Nach stabiler Tk-9.1-Freigabe und Paketentscheidung |

Details, Aufwand und Reihenfolge: [Entwicklungsplan](Glide_Entwicklungsplan_3.33ff_2026-10-01.md).
