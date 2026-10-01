# Glide – Arbeitsvorbereitung: Modernisierung, Pinnwand-Board und Pixel-Werkstatt

Stand 25.09.2026 · Planungsstand · Glide 3.29.0 · Aufgabenformat 19 · Einstellungen 2

> **Status dieses Dokuments:** Arbeitsvorbereitung für den
> [Aufgabenkatalog](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md). Grundlage
> ist die [Wettbewerbsrecherche](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md).
> Nichts davon ist umgesetzt. Vor einer Etappe müssen die in Abschnitt 5
> genannten Entscheidungen der jeweiligen Pakete vorliegen.

## 1. Ziel und Leitbild

**Leitbild:** Glide ist der lokale Ort für Aufgaben, Notizen und Pixelbilder.
Die Oberfläche wird direkter bedienbar, zeigt mehr Bild statt Text und macht
die Pixelzeichnungen in der Organisation sichtbar.

**Erfolgskriterien für alle Etappen**

1. Jede Seite ist per Tastatur in höchstens drei Anschlägen plus Namensanfang
   erreichbar (MO-010).
2. Startseite und Pinnwand lassen sich dort anordnen, wo man sie sieht; der
   Dialog bleibt nur als zweiter Weg (ST-010, PW-010).
3. Umplanen gelingt durch Ziehen zwischen Spalten, ohne Maske (PW-010).
4. Beim Zeichnen braucht der Normalfall keinen Dialog: Farbe wechseln,
   Weiß auftragen und zoomen gehen direkt auf der Fläche (ZD-020, ZD-030).
5. Pixelbilder erscheinen außerhalb der Zeichnungsseite: als Kachel, als
   Übersichtsvorschau und als Seitensymbol (ST-030, AO-010, AO-050).
6. Kein Zusatzfenster, keine neue Laufzeitabhängigkeit, keine Datenverluste.

## 2. Verbindliche Rahmenbedingungen

Aus `AGENTS.md`, den Produktgrenzen und den Nutzerwünschen:

| Regel | Folge für diese Arbeit |
|---|---|
| Lokal, ohne Konto, Internet oder Telemetrie | Keine Netzfunktionen, keine KI-Dienste, keine Bildarchive aus dem Netz. |
| Python, Tk und Standardbibliothek | Nur Tk-8.6-Mittel (siehe Abschnitt 2.1). Neue Dateiformate nur, wenn sie mit der Standardbibliothek sauber lesbar sind. |
| **Eingebettet statt Zusatzfenster** | Neue Funktionen erscheinen in der Seitenanzeige, in Ordnern und Tagebüchern. Überlagerungen als eingebettete Frames wie `DropdownPopup`; nur kleine Bestätigungs- und Einstellungsdialoge über `run_modal`. |
| Änderungen an Punkten über `item_change`, an Listen und Ordnern über `sidebar_change` | Auch Ziehen im Spaltenboard, Anheften und Pfadsprünge laufen über diese Wege; Umbauten zusätzlich unter `guarded_structural_change`. |
| Zeichnungsänderungen über `apply_drawing_change` | Große Aktionen wie „Farbe ersetzen“ oder das Wiederherstellen eines Zwischenstands verwenden den markierten Vorher-Stand (`drawing_restore`). |
| Oberflächensymbole nur aus `ICONS` | Neue Glyphen in `ICONS` eintragen und gegen die Schriftabdeckung von DejaVu Sans prüfen. Pixelsymbole der Nutzer sind Inhalt, keine Oberflächensymbole; die Symbolprüfung braucht dafür eine dokumentierte Ausnahme. |
| Datenformat nur mit Migration, Vorsicherung und Tests | Siehe Abschnitt 3: möglichst additive Einstellungen, sonst ein gebündelter Formatsprung. |
| Deutsch, einsprachig | Alle Beschriftungen, Tooltips, Handbuch und Tastenkürzelübersicht auf Deutsch. |
| Überholte Dokumente zuerst archivieren | Gilt für jeden Vertrag, Index, Handoff und Changelog, der angefasst wird. |
| Tests nie mit echten Nutzerdaten | Immer `GLIDE_DATA_DIR` isolieren. |

### 2.1 Technische Grenzen und Möglichkeiten von Tk 8.6

| Thema | Befund | Konsequenz |
|---|---|---|
| PNG | `tk.PhotoImage` liest und schreibt PNG ohne Zusatz. | PNG-Export (ZD-120) und Miniaturen sind ohne neue Abhängigkeit machbar. |
| Bilder in der Seitenleiste | `ttk.Treeview` zeigt je Zeile ein Bild. | Pixelsymbole in der Seitenleiste (AO-050) sind machbar; Bildobjekte müssen referenziert bleiben. |
| Scharfe Vergrößerung | `PhotoImage.zoom` und `subsample` skalieren ganzzahlig ohne Glättung. | Miniaturen nur in ganzzahligen Faktoren; Cache nach Zeichnungs-Prüfsumme. |
| Transparenz | Keine echte Deckkraft je Widget. | Deckkraft der Referenz (ZD-150) als vorberechnete Mischfarbe, wie heute „blass“. |
| Gesten | Kein Trackpad-Zusammenziehen in Tk 8.6. | Zoom über Strg/Cmd+Mausrad; Scrollen über Mausrad und Umschalt+Mausrad. |
| Maustasten | Unter macOS ist `<Button-2>` der Rechtsklick und `<Button-3>` die mittlere Taste; unter Windows und Linux umgekehrt. | Rechtsklick-Malen (ZD-020) und Verschieben mit der mittleren Taste (ZD-030) plattformabhängig binden; Glide nutzt die mittlere Taste bereits (3.28). |
| Mausrad | Windows/macOS `<MouseWheel>`, Linux `<Button-4/5>`. | Eine gemeinsame Hilfsfunktion, getestet auf allen drei Wegen. |
| Tastenkürzel | Belegt sind unter anderem Strg/Cmd+E (TXT-Export), +K (Kalender), +P (Druck), +H (Verlauf). Frei sind Strg/Cmd+O und +J. | Vorschlag für die Seitensuche: Strg/Cmd+O (E-03). |

## 3. Datenwirkung und Formatstrategie

Jedes Paket ist einer von vier Datenklassen zugeordnet. Die Klasse bestimmt
Aufwand, Test und Risiko.

| Klasse | Bedeutung | Pakete |
|---|---|---|
| **D0 – keine Daten** | Reine Darstellung oder Eingabe | MO-020, MO-040, MO-050, ZD-010, ZD-030, ZD-040, ZD-060, ZD-100, ZD-110, ZD-120, ZD-130, PW-040, AO-060 |
| **D1 – Einstellungen additiv** | Neue Schlüssel in `settings.json`, Einstellungsformat bleibt 2, fehlende Werte bedeuten das heutige Verhalten | ST-010, ST-020, ST-030, ST-040, ST-050, MO-010, MO-030, MO-060, ZD-020, ZD-050, ZD-090, ZD-150, AO-010, AO-020, AO-030, AO-040 |
| **D2 – Pinnwandabschnitt additiv** | Neue Felder im `pinboards`-Abschnitt; Transport und Neuzuordnung im Backup wie seit 3.24 | PW-010, PW-020, PW-030, PW-050, PW-060, PW-070 |
| **D3 – Aufgabenformat 20** | Neues Feld im Bestand, Migration mit Vorsicherung | ZD-140, AO-050, MO-070; je nach Entscheidung ZD-080 und ein Statusfeld (E-07) |

Die P3-Pakete MO-080, AO-070, ZD-160 und ZD-170 werden erst bei ihrer
Konkretisierung einer Klasse zugeordnet.

**Regeln für D1 und D2**

- Die Normalisierung entfernt unbekannte Werte und setzt Vorgaben; ein älteres
  Glide überschreibt die neuen Schlüssel beim nächsten Speichern ohne Fehler.
  Das ist für Ansichtszustand akzeptabel und wird im jeweiligen Vertrag
  genannt.
- Eine neue Pinnwandanordnung wie `columns` fällt in älteren Fassungen auf
  `free` zurück (Normalisierung `layout`). Kartenpositionen bleiben erhalten.

**Empfehlung für D3: ein gebündeltes Formatpaket 20.** Alle
bestandsändernden Pakete werden in **einer** Etappe umgesetzt, statt mehrere
Formatsprünge hintereinander zu machen. Der Ablauf folgt dem Übergang auf
Format 19:

1. Zentrale Registrierung der neuen Felder mit Validierung.
2. Unveränderte Vorsicherung `liste_vor_format20_<Zeitstempel>.json` vor dem
   ersten Schreiben; scheitert sie, bricht der Start sichtbar ab.
3. Ältere Glide-Fassungen lehnen Format 20 sichtbar ab.
4. Duplizieren, Papierkorb, Vorlagen, Teil-, Komplett- und App-Backup,
   Austauschformat und additiver Import mit neuen Kennungen prüfen.
5. Neues Referenz-Fixture `current_v20`, Fixture-Zuordnung 19 für Fassungen
   bis 3.29 in `pruefen.py`.

## 4. Einstiegspunkte im Code

Zeilennummern beziehen sich auf `src/glide/app.pyw` 3.29.0 und sind
ungefähre Orientierung.

| Bereich | Einstiegspunkte | Hinweis |
|---|---|---|
| Startseite | `HOME_TILE_DEFINITIONS` (~10358), Normalisierung `home_tile_order`/`home_tiles_hidden` (~9690), Aufbau der Startseite, Dialog „Startseite einrichten“, `BoardPreview`, `MascotCanvas` | Kein Vollneuaufbau je Mausbewegung; Lehre aus [Flackern 3.28](../01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md). Neue Kacheln sind für bestehende Startseiten zunächst aus. |
| Übersicht | `refresh_library_page` (~11693), `library_entries` | Die Kartenabstände prüft `test_ui_followup36.py`; Messung bis zum stabilen Layout. |
| Seitenleiste | `sidebar_listbox` als `ttk.Treeview` (~17520), `on_sidebar_drag_*` (~20404), Kontextmenüs | Hover-Schaltflächen als eingebettete Frames an der Zeilen-Bbox. |
| Kopfzeile und Pfad | `update_header_title` (~21966), `get_display_title` (~12699), `folder_path_titles` (~15988), `list_path_title` (~16000) | Titelkürzung bleibt; der Pfad bekommt eine eigene Zeile. |
| Aktionen und Suche | `show_actions_dialog` (~36235), `ACTION_GROUPS`, `MANUAL_SECTIONS`, Tastenbindungen (~8840–8920) | Die Gruppe „Weitere Aktionen“ muss leer bleiben (Regression 3.22). |
| Rückmeldung und Undo | `feedback()`, `ACTION_FEEDBACK_TEXTS`, `undo_last_change`, `snapshot_undo` | Rückgängig im Hinweis nur, solange der Snapshot der gemeldeten Aktion oben liegt. |
| Pinnwand | Normalisierung `layout` (~3619) und Vorgaben (~3742), Anordnungsauswahl (~4645), Kartenaufbau (~5361), Ziehen (~5908), Kontextmenü (~4749) | Spaltenboard als dritte Anordnung; Karten bleiben Verweise auf Punkte. |
| Zeichnung | `DrawingEditor` (~6376): `TOOLS`, `ZOOM_LEVELS`, `_build`, Bindungen (~6512–6544); `ListApp.apply_drawing_change`, `drawing_view_state`, `show_drawing_menu`, `drawing_color_dialog`, `drawing_export` | Modell, Treffer, Füllung und Undo-Ring in `drawing.py`; Bildfunktionen in `drawing_image.py` (`model_to_photo`). |
| Designs | `DESIGNS`, `THEMES`, `CONTRAST_THEMES`, `MINIMAL_THEMES` (~7157–7415) | Kontrastregeln aus dem [Designsystem](../01_Repository/Glide/docs/50_DESIGNSYSTEM_3.23.0.md). |

## 5. Offene Produktentscheidungen

Diese Fragen entscheidet der Inhaber. Die Spalte „Empfehlung“ ist ein
Vorschlag, keine Festlegung.

| Kennung | Frage | Empfehlung | Betrifft |
|---|---|---|---|
| E-01 | In welcher Reihenfolge werden die Etappen umgesetzt? | Etappe A zuerst, dann nach Nutzen B oder D (Abschnitt 6) | alle |
| E-02 | Werden alle bestandsändernden Pakete in einem Formatpaket 20 gebündelt? | Ja | ZD-140, AO-050, ZD-080, MO-070, E-07 |
| E-03 | Welches Tastenkürzel öffnet die Seiten- und Befehlssuche? | Strg/Cmd+O („Öffnen …“); Strg/Cmd+K bleibt Kalender | MO-010 |
| E-04 | Soll ein eingebetteter Detailbereich die Punktmaske als Standard ersetzen? | Nein, zunächst zuschaltbar; unter 980 px bleibt die Maske | MO-030 |
| E-05 | Visuelle Richtung nach dem Inspirationsbild: eigenes Design „Pixel“ oder Akzente in allen Designs? Pixelschrift? | Eigenes Design „Pixel“; Pixelschrift nur nach Lizenzprüfung als Ressource | MO-060 |
| E-06 | Wird zusätzlich zum Papierkorb „Archivieren“ gebraucht? | Erst nach Nutzungsbeobachtung | MO-070 |
| E-07 | Bekommt eine Aufgabe ein Statusfeld (Offen, In Arbeit, Wartet, Erledigt) für das Spaltenboard? | Etappe C ohne neues Feld; Status erst im Formatpaket 20, falls Bedarf | PW-010 |
| E-08 | Legt Strg/Cmd+Enter auf der Pinnwand eine Karte nur mit Titel an, entgegen der 3.24-Regel „volle Maske“? | Ja, Titel direkt auf der Karte; Doppelklick öffnet weiter die volle Maske | PW-050 |
| E-09 | Wird ein Pixelsymbol als eigene 16-×-16-Zeichnung im Listen- beziehungsweise Ordnerobjekt gespeichert oder als Verweis auf eine Zeichnungsseite? | Eigene kleine Zeichnung im Objekt | AO-050 |
| E-10 | Werden Linie, Rechteck und Ellipse freigegeben? V1 hat sie am 24.09.2026 ausgeschlossen. | Ja, zusammen mit E-11 | ZD-060 |
| E-11 | Gilt Rückgängig künftig je Aktion statt je Zelle (heute 20 Zelländerungen, Entscheidung vom 24.09.2026)? | Ja; ein breiter Pinseltupfer hat bis zu 64 Zellen und sprengt den Zellring | ZD-070, ZD-050, ZD-060, ZD-100 |
| E-12 | Wo liegen benannte Zwischenstände: im Bestand (Format 20) oder als Anhänge? | Als Anhänge; jede Kopie im Bestand vergrößert jedes Autosave | ZD-080 |
| E-13 | Wird PNG-Export vorgezogen? Er war am 24.09.2026 als nachrangig eingestuft. | Ja, geringer Aufwand, großer Nutzen | ZD-120 |
| E-14 | Gibt es neben 128 × 128 die Größen 16, 32 und 64? | Ja; Kern der Pixel-Nische und Voraussetzung für Pixelsymbole | ZD-140, AO-050 |
| E-15 | Liefert Glide fremde Paletten (etwa PICO-8, Endesga) mit oder nur eigene? | Nur eigene Glide-Palette; Fremdpaletten per Import | ZD-090 |
| E-16 | Welche Punkte zeigt das Spaltenboard: alle Punkte des Bereichs oder nur angeheftete Karten? | Alle Punkte des Bereichs, filterbar; die freie Pinnwand behält ihre angehefteten Karten | PW-010 |

## 6. Etappenplan (Empfehlung)

Die Versionsnummern sind Vorschläge. Innerhalb einer Etappe gilt die Reihenfolge
des Katalogs.

| Etappe | Titel | Pakete | Daten | Vorbedingung |
|---|---|---|---|---|
| **A** | Schneller Zugriff und Zeichenkomfort | MO-020, MO-040, MO-010, ZD-010, ZD-020, ZD-030, ZD-040, ZD-120, ST-030 | D0/D1 | E-03, E-13 |
| **B** | Startseite und Übersichten | ST-010, ST-020, ST-040, ST-050, AO-010 mit Rest von ZF-120, AO-020 | D1 | – |
| **C** | Pinnwand als Board | PW-010 und AO-040 (gemeinsame Gruppierung), PW-020, ZF-100, PW-030, PW-040, PW-050, PW-060, PW-070, Anlageoption „Pinnwand“ | D0/D1/D2 | E-07, E-08, E-16 |
| **D** | Pixel-Werkstatt | ZD-070, ZD-050, ZD-060, ZD-100, ZD-110, ZD-130, ZD-150, ZD-090 mit ZF-210 | D0/D1 | E-10, E-11, E-15 |
| **E** | Formatpaket 20 | ZD-140, AO-050, ZD-080, MO-070, gegebenenfalls Statusfeld | D3 | E-02, E-06, E-09, E-12, E-14 |
| später | Ergänzungen | MO-030, MO-050, MO-060, AO-030, AO-060, AO-070, MO-080, ZD-160, ZD-170 | je Paket | E-04, E-05 |

**Alternative Reihenfolge für die Nische:** Soll das Pixelprofil zuerst
wachsen, folgen auf A direkt D und E; B und C schließen sich an. Etappe A
bleibt in jedem Fall der Anfang, weil sie ohne Formatänderung sofort spürbar
ist und Grundlagen legt: Miniaturcache, Seitensuche und Kontextleiste.

## 7. Arbeitsweise je Paket

**Bereit zur Umsetzung, wenn**

1. die Entscheidungen des Pakets (Abschnitt 5) vorliegen,
2. Abnahmekriterien und Datenklasse im Katalog stehen,
3. die Einstiegspunkte gelesen und bestehende Tests des Bereichs bekannt sind.

**Fertig, wenn**

1. Syntaxprüfung und die neue Suite `tests/integration/test_features3XX.py`
   grün sind und die Suite in `tests/tools/pruefen.py` registriert ist,
2. `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-<Version>/<Ordner> --timeout 900`
   mit Exitcode 0 endet, Dokumentations- und Standprüfung eingeschlossen,
3. `VERSION`, `APP_VERSION`, gegebenenfalls `DATA_SCHEMA_VERSION`,
   Releasedaten und Fixtures konsistent sind,
4. Vertrag `docs/66_…` (fortlaufend), `CHANGELOG.md`, Dokumentationsindex,
   Projektübergabe, QA-Bericht, `tests/qa-verlauf.md` und dieser Katalog
   (Statusspalte) nachgeführt und alle geänderten Dokumente vorher archiviert
   sind,
5. Handbuch (`MANUAL_SECTIONS`), Tastenkürzelübersicht und App-Aktionen die
   neue Funktion nennen,
6. die startbare Kopie in `07_Python-Versionen` bytegleich synchronisiert ist,
7. eine manuelle Prüfliste `Checklisten/Manuelle_Pruefung_<Version>.md`
   Plattform, DPI, Screenreader und echte Maus-/Trackpadbedienung nennt.

## 8. Prüfstrategie

- **Geometrie statt Bildschirmaufnahme.** In der Agentenumgebung sind keine
  Aufnahmen möglich. Lage, Größe und Sichtbarkeit werden über Widgetgeometrie
  geprüft, jeweils bis zum stabilen Layout gemessen (Lehre aus
  `test_ui_followup36.py`).
- **Ziehen und Rechtsklick** werden über `event_generate` mit
  plattformgerechten Tasten geprüft. Jede Ziehaktion bekommt einen Tastaturweg
  und einen eigenen Test dafür.
- **Leistung.** In `leistungspruefung.py` messen:
  - Startseite mit 40 Zeichnungen, Miniaturen aus dem Cache;
  - Spaltenboard mit 500 Karten in sechs Spalten;
  - Übersicht mit 200 Karten.

  Grenzwerte vor der Umsetzung festlegen und im Vertrag nennen.
- **Daten.** Jedes D1-, D2- und D3-Paket bekommt einen Rundlauf über Neustart,
  App-Backup und, wo zutreffend, Komplettbackup, Teilbackup und additiven
  Import mit neuen Kennungen.
- **Zeichnung.** Deterministische Tests für Symmetrie, Formen, pixel-perfekte
  Linie und Farbersetzung auf Zellebene; PNG-Rücklesen über `PhotoImage`.
- **Manuell** bleiben Windows/macOS, hohe DPI, zweiter Monitor, VoiceOver und
  Sprachausgabe, echte Trackpads sowie die Sichtprüfung aller Designs.

## 9. Risiken

| Risiko | Gegenmaßnahme |
|---|---|
| Direktes Anordnen der Startseite flackert oder baut bei jeder Bewegung neu auf | Platzhalter verschieben, Neuaufbau erst beim Loslassen; Messung im Dopamin-Design |
| Spaltenboard verändert Felder überraschend (Wiederholung, Uhrzeit, Mehrfachlabels) | Regeln je Gruppierungsfeld vorab im Vertrag festlegen und testen; nicht setzbare Spalten nehmen nichts an |
| Zwei Board-Formen verwirren | Begriffe trennen: „Pinnwand – frei“, „Pinnwand – Spalten“; im Index und Handbuch abgrenzen |
| Aktions-Undo bricht den bestätigten Zellvertrag | Entscheidung E-11 vorher; Vertrag 65 fortschreiben; bestehende Undo-Tests bewusst ersetzen |
| Miniaturen kosten Speicher und Zeit | Cache nach Prüfsumme, ganzzahlige Faktoren, Obergrenze je Ansicht |
| Pixelsymbole verletzen die ICONS-Regel | Nutzerinhalt ausdrücklich von Oberflächensymbolen trennen; Symbolprüfung um dokumentierte Ausnahme ergänzen |
| Rechtsklick unter macOS falsch belegt | Plattformtabelle aus 2.1 als Hilfsfunktion; Test für beide Belegungen |
| Mehrere Formatsprünge in kurzer Folge | Formatpaket 20 bündeln (E-02) |
| Neues Design verfehlt Kontrastregeln | Messung jeder Schrift auf jeder Fläche wie bei „Minimal“; Muster für Farbfehlsichtige |
| Fremdpaletten mit unklarer Lizenz | Nur eigene Palette mitliefern; Import durch Nutzer (E-15) |

## 10. Dokumentationspflichten

Nach jeder Etappe:

- neuer Vertrag unter `docs/` mit Nummer 66 folgende;
- `CHANGELOG.md`, Dokumentationsindex (Begriffe und Einstieg), Projektübergabe,
  QA-Bericht, Produktgrenzen bei neuen Grenzen;
- Statusspalte im Katalog, README dieses Ordners;
- die Begriffe im Index um „Pinnwand – Spalten“, „Angeheftet“ und
  „Pixelsymbol“ erweitern, sobald sie existieren;
- alle geänderten Dokumente vorher nach `archiv/` beziehungsweise `Archiv/`
  kopieren.
