# Glide 3.32.3 – kompakte Übergabe an Claude Code

**Einmaliger Zwischenstand vom 01.10.2026 · Aufgabenformat 20.**

Diese Datei bündelt den aktuellen Stand und die Planung für eine externe Bearbeitung. **Sie wird künftig nicht aktualisiert, nicht synchronisiert und nicht in die laufende Dokumentationspflege aufgenommen.** Spätere Entscheidungen und Änderungen gehören in die aktive Projektablage. Die beigefügte Codebasis ist derselbe eingefrorene Stand. Die Planung beschreibt Reihenfolge und Grenzen; offene Empfehlungen sind keine zusätzlichen Implementierungsaufträge.

## 1. Projekt und Stand

Glide ist eine deutschsprachige, lokale Desktop-App für Aufgaben, Listen, Seiten, Notizen, Ordner, Bibliotheken, Notizbücher, Galerien, Pinnwände und Pixelzeichnungen. Kernfunktionen arbeiten ohne Internet, Konto oder Cloudservice. Nutzerdaten liegen außerhalb des Programmordners. Windows, macOS und Linux sind Zielplattformen; Mobile und Toolkit-Wechsel sind zurückgestellt.

Laufzeit: Python/Tk und Standardbibliothek, mitgelieferte Schriften sowie optionales `tkinterdnd2` für Drag-and-drop aus Finder/Explorer. Geprüft: Python 3.14.5, Tk 9.0.3 auf macOS. Keine neue Abhängigkeit ohne dokumentierte Entscheidung. Python 3.13/Tk 8.6 ist als eingeschränkt kompatibel beschrieben, bei dieser Übergabe nicht erneut getestet.

| Stand | Bereits umgesetzt |
|---|---|
| 3.30–3.32.0 | Pixel-Werkstatt, Seiten mit Bildern/Markdown, Startseite, Planung, Archiv, Etappe 1 mit Symbol-Export, Paletten, Platzhaltern und Tagesabschluss; Menü-/Bildseitenhänger korrigiert |
| 3.32.1 | Klappzustände, Label-Pfeilklick, verschachtelte Bibliothek; Pflichtprüfung über echte Bedienbindungen |
| 3.32.2 | Ziehen in bestehenden Seiten-/Notizbereichen; Schriftcache, gebündelte Formatleistenlayouts, gemeinsamer Hover |
| **3.32.3** | Unveränderte Bibliothekskarten und Aktionsleisten im selben lebenden Host erhalten; Archiv-Zurückholen aktualisiert einmal |

Bestehende Seitenaufgaben, Slash-Befehle, Datumshelfer, Suchfunktionen, PreviewCache und Zeiterfassung sind Ausgangspunkte. Einzelaufgaben **im Notiztext**, allgemeiner Datumseingabe-Parser und die weiteren unten genannten Ausbauten sind noch offen. Bereits vorhandene Funktionen zuerst im Code prüfen, bevor sie neu geplant werden.

## 2. Codebasis und Orientierung

Das ZIP enthält die vollständige aktuelle Python-Laufzeitbasis: acht unveränderte Dateien und alle benötigten `resources`/`vendor` einschließlich Lizenzen, insgesamt 139 abgeglichene Laufzeitdateien. Die Original-Hauptdatei heißt hier `app.pyw`; `glide_start.py` entspricht `Schnellstart.pyw` der Arbeitskopie. Archivfassungen, macOS-Bundle, Grafik-Master, komplette Testinfrastruktur und umfangreiche Dokumentationshistorie gehören zum größeren Projektpaket.

| Datei im Codepaket | Rolle |
|---|---|
| `app.pyw` | Hauptanwendung, Datenmodell, UI, Mutationen, Speicherung; rund 54.000 Zeilen |
| `drawing.py` | Pixelkern, Werkzeuge, Aktions-Undo, Paletten und PNG-Ausgabe |
| `drawing_image.py` | Zeichnungsvorschauen |
| `backdrop.py` | Hintergrundverläufe und PNG-Helfer |
| `page_markdown.py` | Markdown-Austausch |
| `image_preview.py` | Bildvorschauen und Konvertierungswege |
| `logo.py` | Logo, Akzentfarbe, Programmsymbole |
| `glide_start.py` | Start als Modul mit Bytecode-Cache außerhalb des Projekts |

Wichtige Einstiegspunkte in `app.pyw` – Zeilen gelten nur für diesen Snapshot:

| Bereich | Einstieg |
|---|---|
| Bibliothekskarten/Aktionen | `library_card_preview` 22166, `refresh_library_page` 22195, `refresh_page_actions` 22482 |
| Startseite/Layout | `refresh_home` 21040, `ButtonFlow` 1426, `app_font` 206 |
| Seitenbilder | `fit_read_width` 9117, `schedule_image_layout` 10009, `layout_images` 10023, `render_image` 10118, `place_images` 10197 |
| Speicherwege | `save_settings` 16465, zentrale `save_items` 37456 |
| Mutationsgrenzen | `item_change` 44190, `sidebar_change` 44252, `guarded_structural_change` 44410 |
| Dialoge/Menüs | `run_modal` 24319, `defer_window_menu_commands` 45 |

Die Datei enthält weitere Methoden gleichen Namens; Klasse und Aufrufer vor Änderungen abgleichen. Feste Kennungen erhalten: macOS `de.shaye.glide`, Windows `Shaye.Glide`.

## 3. Verbindliche Entscheidungen

| ID | Vorgabe |
|---|---|
| D01 | Allgemeines Datum wie „morgen“ setzt `planned_date` (Bearbeitungstag); ausdrücklich „fällig/bis“ setzt `due`. Erkannte Felder sichtbar und rücknehmbar machen; bestehende Slash-Semantik bewahren. |
| D02 | Aktionen bewirken die im sichtbaren Zielkontext erwartbare Änderung. Terminziel setzt das passende Feld; Zeitblock zusätzlich `planned_time`. Neutraler Listen-/Ordnerwechsel erhält Termine. Ein gemeinsamer Undo-Schritt. Eisenhower-Quadranten brauchen einen konkreten UI-Vertrag; keine pauschale Löschung von Fälligkeiten. |
| D03 | Desktop/Tk optimieren. Mobile und Toolkit-Probe zurückgestellt. |
| D04 | Bestehende Seitenleistenbereiche um Drag-and-drop erweitern; in 3.32.2 umgesetzt. |
| D05 | Einzelne echte Aufgaben in Notizen und Seiten unterstützen, Identität über IDs erhalten. Liste, Notiz und Seite bleiben getrennte Arten; keine allgemeine Konvertierungspflicht. |
| D06 | Hinweisgestaltung unverändert lassen. |
| D07 | Animations-Exportumfang offen: abspielbares GIF oder zuerst Frames/Vorschau/PNG-Spritesheet. Entscheidung erst bei Animation erforderlich. |
| D08 | Klappmechanismen über native Bedienung, Tastatur, verschachtelte Bereiche und Callbackfehler kontrollieren; Korrektur/Pflichtsuite seit 3.32.1. |

Git bleibt vertagt. Zusätzliche Feature-Richtung A–H und Bearbeitungstiefe sind offen. Inhaberangaben, Signatur/Store, Markenprüfung und Plattformabnahme bleiben eigene Entscheidungen.

## 4. Nächste beauftragte Arbeit: Performance

Die vorhandene Performance-Arbeit ist ausdrücklich fortgesetzt. Ein kleiner, gemessener Schnitt folgt auf den nächsten:

1. **Rest P03:** Startseitenkarten, einzelne Elemente geänderter Karten und viele tatsächlich sichtbare Karten untersuchen. Bibliothekswiederverwendung im selben Host ist abgeschlossen. Fokus, Scrollposition, Auswahl, Drag und Design bewahren.
2. **P04 / A-02:** Bildlayout dynamisch messen. Scrollen verwendet bereits `place_images`; nicht als neue Optimierung verkaufen. Aufrufe bei Resize, Text/Format, Auswahl und Ziehen zählen. Unveränderte effektive Lesespaltengeometrie ist ein Skip-Kandidat; Text/Anker, Faltungen, Schrift, Modi/Größe und fertig konvertierte Anhänge müssen invalidieren. Bestehenden PreviewCache verwenden.
3. **Rest P06 / A-03:** Doppelte Refresh-/Schreibanforderungen pro Aktion bestätigen. Archiv-Zurückholen ist bereits konsolidiert. 21 statische Kandidaten sind keine bewiesenen Fehler. Zuerst z. B. Kalender-Neuanlage und Seitenleisten-Umbenennen samt Undo zählen; auch fehlgeschlagenes Speichern, Dirty-Zustand, Warnung und Bestand prüfen, bevor ein Aufruf entfällt.

Begleitend: P01 um Verlaufvarianten, Speicherentwicklung und kalte/warme Serien ergänzen. P02 Schriftcache ist umgesetzt. Rest P05 betrifft gemeinsame UI-Texte nur bei gleicher Bedeutung. P07/FTS5 gehört zum Wissensausbau. Große Monolith-Aufteilung ist zurückgestellt. Dictionary-Schlüssel nicht pauschal durch Variablen ersetzen.

3.32.3 erhält Karten über `(Art, ID)` nur im selben lebenden Host. Anzeigedaten werden frisch berechnet; keine dauerhaften Aufgaben-/Terminzähler. Host-Zerstörung gibt Widgets und PhotoImages frei. Vollständige Invalidierung für Inhalt, Status, Termine/Tageswechsel, Pfad, Labels, Reihenfolge, Schrift, Design und Größe erhalten. Undo kann Python-Objekte ersetzen: Befehle lesen über IDs.

Messbeleg bei 1.000 synthetischen Aufgaben, warmer Median: unverändert **776,2 → 4,9 ms**, Status **785,3 → 388,3 ms**, Reihenfolge **795,1 → 85,8 ms**. Gemessen wurde erneutes Rendern derselben Bibliothek mit gleicher Kartenzahl; keine allgemeine Speicher-/Wechsellatenz und kein Nachweis für Tausende sichtbare Karten. Rohwerte für 100/1.000/10.000 Aufgaben liegen im Codepaket.

## 5. Anschließende Planung und offene Auswahl

Zielversionen sind Planungsreservierungen, keine Liefertermine oder Freigaben:

| Etappe | Geplante Inhalte |
|---|---|
| Planen · 3.33 | G01 deutsche Eingabe/Feldvorschau, G05 Fokus/Timer, G29 Aufgaben im Notiztext, G31 Seitenaufgabe über IDs in Liste schicken, Rest G32 Filter „aus Seiten“, G02 Eisenhower mit D02 |
| Wissen · 3.34 | G08/G30 gemeinsame Referenzschicht, G28 Live-Liste in Seite, G14 lokale Volltextsuche/SQLite FTS5 als erneuerbarer Cache, G09 Titelbild |
| Pixel · 3.35 | G19 Palettenbearbeitung/Undo, G17 Frames/Dauer/Vorschau; D07 und Migrationsvertrag klären |
| Austausch · danach | G24 Kontextdateien/Markdown/Felder/Änderungsdiff, G21 begrenzter Notion-/Todoist-Import mit Vorschau |

Referenzen und Löschverhalten vor G31/G28 klären. Textzeile entfernen darf nicht versehentlich die anderweitig verwendete Aufgabe löschen. Suchindex muss ersetzbar bleiben; Fehler dürfen Datenöffnung nicht verhindern. Neue inkompatible Inhalte können bereits vor Animation ein neues Datenformat erfordern.

Die zusätzliche Auswahl umfasst 24 Aufgaben; sie erweitert den Auftrag erst nach Auswahl:

| Richtung | Aufgaben |
|---|---|
| A Tempo | A-01 Bibliothekskarten abgeschlossen; A-02 Bildlayout; A-03 Doppelaufrufe teilweise erledigt |
| B Planen | B-01 Datumseingabe, B-02 Fokus, B-03 freie Zeitfenster bei Konflikten |
| C Textaufgaben | C-01 Notiztextaufgaben, C-02 Seitenaufgabe in Liste mit Verweis, C-03 Quellenfilter in „Mein Tag“ |
| D Wissen | D-01 Volltext/Fundstelle, D-02 Verweise/Rückverweise, D-03 Filterwirkung erklären |
| E Projektseiten | E-01 Live-Liste, E-02 Titelbild, E-03 gefüllte Vorlagenvorschau |
| F Austausch | F-01 KI-Kontext/Änderungsdiff, F-02 Import, F-03 Sicherungsvergleich |
| G Pixel | G-01 Palette/Undo, G-02 Animation, G-03 Symbolvorschau in 16/32/48 px |
| H Abnahme | H-01 Kontrollmatrix erweitern, H-02 Tastaturwege für Drag, H-03 Desktop-Paket mit eingebettetem Python |

Nach Performance sind C-01 oder B-01 empfohlen; diese Empfehlung ist keine zusätzliche Auswahlentscheidung.

## 6. Regeln für Änderungen und Abnahme

- Kleine notwendige Änderungen; bestehende Architektur, Funktionen, IDs, Bindungen, Auswahl, Undo und Bedienwege erhalten. Keine pauschale Neuimplementierung.
- Punkte über `item_change`, Listen/Ordner über `sidebar_change`, Strukturumbauten zusätzlich über `guarded_structural_change`; Dialoge über `run_modal`.
- Atomare Speicherung, `fsync`, Sperren, Backups, Migrationen und Fehleranzeige bewahren. Keine verzögerte ungesicherte Speicherung. Ältere Fassungen wie 3.29 nicht mit umgestellten Format-20-Daten starten.
- Neue inkompatible Listen-/Ordnerart oder Datenfelder: Migration, Vorsicherung, Formatversion und Tests planen; ältere Versionen müssen den neueren Bestand geschützt behandeln.
- Keine verschachtelten `update()`/`update_idletasks()` in selbstauslösenden Rückrufen. Ersetzte Bindungen/`after`-Aufträge freigeben. Synchrone Höhenleser brauchen vorher ein fertiges Layout.
- Menübefehl erst nach Schließen des Menüs über `defer_window_menu_commands`; Tests nach `menu.invoke()` kontrolliert `update()` ausführen.
- UI auf Deutsch, Tastatur/Fokus und kleine Fenster beachten. Symbole aus `ICONS`, Logo-Ausnahme aus `resources/logo`. Farben über `BUTTON_ROLE_RULES`: Rot Löschen, Grün Bestätigen, Lila Hinzufügen, Gelb Hinweise. Hinweise gemäß D06 erhalten.
- Keine Originaldaten, persönlichen Fehlerprotokolle oder Ganzbildschirmfotos verwenden. Tests/Messungen mit temporärem `GLIDE_DATA_DIR` **vor Import** isolieren; nur eigene App-Fenster erfassen.
- Bestehende Projektdateien nicht löschen; Überholtes mit `_Z` kennzeichnen. Vor Dokumentüberschreiben im aktiven Projekt benachbart archivieren. Diese Kurzfassung bleibt unverändert.
- Vor Produktionsänderungen passende Baseline, danach Bedienweg/Fehlerfall und vergleichbare Messung mit Aufwärmen/Rohwerten/Median/p95 prüfen. In der aktiven Ablage Version, CHANGELOG, Planung und QA nachführen. Erst nach Abgleich von `07_Python-Versionen` und macOS-Bundle per SHA-256 gilt ein Produktionsschnitt als geliefert.

Vorhandener Volltest: **73 Schritte, 58 Integrationssuiten, fünf Analysen, Exitcode 0**. Dokumentations-/Prüfwerkzeugnachlauf vom 01.10.2026 separat abgeschlossen; App und Integrationssuiten unverändert. Keine erneute Laufzeitvollprüfung für diese Zusammenstellung. Offen: physische macOS-Bedienung/OS-Fokus, Windows/Linux, DPI/Mehrmonitor, Screenreader und Releaseabnahme. Originalfoto-Befunde ohne reproduzierbaren Ablauf nicht pauschal als behoben markieren.

Im vollständigen Repository lautet der Vollaufruf:

```sh
python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.32.3/<neuer-Lauf> --timeout 900
```

Die vollständige Testinfrastruktur liegt im großen Projektpaket, nicht im kleinen Laufzeit-ZIP. Eine Online-Umgebung ohne Tk/Anzeige kann die Desktop-Bedienung nicht abnehmen; dort erfolgte Syntax-/Codeprüfung entsprechend kennzeichnen. Das vorhandene macOS-Bundle ist ad hoc signiert, benötigt separat installiertes Python und ist kein öffentlich freigegebenes Release.

## 7. Start bei Claude Code

Zuerst diese Datei lesen, dann die passende Codestelle und ihre Aufrufer. Als Anschlussauftrag verwenden:

> Arbeite mit dem beigefügten Glide-Stand 3.32.3. Untersuche zunächst Rest P03, P04/A-02 und Rest P06/A-03. Wähle den kleinsten belegbaren Performance-Schnitt, beschreibe Ursache, konkrete Änderung, Risiken und sinnvolle Abnahme. Setze nur den tatsächlich beauftragten Schnitt um. Bereits erledigte Bibliothekswiederverwendung nicht nochmals planen. D01–D08, Daten-/Undo-/Fokusregeln und die Grenzen der Online-Testumgebung beachten. Die offene Feature-Auswahl nicht eigenständig entscheiden. Diese historische Übergabe nicht fortschreiben.

Herkunft in der ursprünglichen Ablage: Sitzungsübergabe, Arbeits-/Featureplanung und Aufgabenauswahl unter `00_Arbeitsvorbereitung`; `01_Repository/Glide/AGENTS.md`; `docs/ARBEITSRICHTUNG.md`, Architektur, Produktgrenzen, QA-Bericht und Verträge 69/70/71. Der Originalcode ist maßgeblich für vorhandene Funktionen; die aktuelle aktive Projektablage ist maßgeblich für spätere Entscheidungen.
