# Glide – weitere Aufgaben und Richtungsauswahl

Stand 01.10.2026 · Glide 3.33.1 · ursprüngliche Grundlage 3.32.2 · Aufgabenformat 20 · zusätzliche Auswahl noch offen

[Fortlaufende Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md): Bestehende Performance ist beauftragt; A-01 erledigt, A-03 teilweise. Vorschläge, Empfehlung und neue Featureauswahl bleiben getrennt.


**Fortschreibung 01.10.2026:** Glide 3.32.3 führt auf ausdrücklichen Weiterarbeitsauftrag das schon geplante P03/A-01 fort: unveränderte Bibliothekskarten und gemeinsame Aktionen erhalten. Teil A-03: Archiv-Zurückholen aktualisiert einmal. [Vertrag 71](../01_Repository/Glide/docs/71_KARTEN_PERFORMANCE_3.32.3.md); Vollprüfung (73 Schritte/58 Suiten) und Lieferung abgeschlossen, beide Startfassungen bytegleich. Die 24 Aufgaben bleiben nachvollziehbar, A-01 ist im beschriebenen Desktop-Schnitt umgesetzt und A-03 nur teilweise. Physische Plattformabnahme bleibt offen. Neue Feature-Richtungen und Bearbeitungstiefe bleiben offen.

Auftrag: weitere Aufgaben sammeln und den Inhaber entscheiden lassen, welche Richtungen recherchiert und umgesetzt werden. Diese Vorlage enthält **24 konkrete Aufgaben in acht Richtungen**. Sie führt bestehendes Backlog und neue Vorschläge zusammen. Die Einträge sind keine Behauptung, dass diese Funktionen bereits fehlen, vollständig untersucht oder zur Umsetzung ausgewählt sind.

Grundlage sind [Arbeitsplanung](Glide_Arbeits_und_Featureplanung_2026-09-30.md), [Sitzungsübergabe](Glide_Sitzungsuebergabe_2026-09-30.md), [Funktionsrecherche](Glide_Funktionsrecherche_Ausbau_2026-09-30.md), die abgeschlossene [QA 3.32.3](../01_Repository/Glide/docs/07_QA_BERICHT.md) und ein erneuter gezielter Codeabgleich. **Neu** bezeichnet einen zusätzlichen Vorschlag; alle anderen Einträge konkretisieren offene Arbeiten aus G01–G32 bzw. P01–P07. Die Buchstaben A–H gelten nur für diese Auswahl und ersetzen keine bisherigen Paketkennungen.

## 1. Schnell auswählen

| Richtung | Arbeitsziel | Sinnvoller erster Schnitt | Vorgehen zum Einstieg |
|---|---|---|---|
| **A – Tempo und Stabilität** | Weniger Neuaufbau und doppelte Aktualisierung | A-02/A-03: Bildlayout bzw. weitere Doppelaufrufe | A-01 in 3.32.3 umgesetzt; restliche Performance nach dynamischem Nachweis |
| **B – Planen und Fokus** | Schneller erfassen, Zeit bewusst verwenden | B-01: deutsche Eingabe mit Feldvorschau | Eingabe- und Kompatibilitätsvertrag konkretisieren, dann kleiner Parser-Schnitt |
| **C – Aufgaben im Text** | Beim Schreiben Aufgaben erzeugen und gezielt abarbeiten | C-01: einzelne Aufgaben im Notiztext | Aufgaben-IDs, Referenzen und Löschverhalten zuerst abgleichen |
| **D – Suchen und Wissen** | Inhalte schnell finden und sinnvoll verknüpfen | D-01: Volltextsuche mit Fundstelle | Kleine FTS-Probe und Rückfall prüfen, dann Suchoberfläche anbinden |
| **E – Projektseiten** | Projektwissen und Aufgaben an einem Ort | E-03: Vorschau einer gefüllten Vorlage | Bestehenden Erzeugungsweg erweitern; Live-Listen folgen nach Referenzschicht |
| **F – Austausch und Sicherungen** | Daten nachvollziehbar übernehmen und vergleichen | F-03: Sicherungsstände zunächst nur vergleichen | Identitäten, Vergleichsregeln und unterstützte Formate recherchieren |
| **G – Pixel-Werkstatt** | Farbvarianten und kleine Animationen | G-01: Paletteneinträge bearbeiten mit Undo | Palettenvertrag prüfen; Animation erst mit eigener Modellprobe |
| **H – Bedienkontrolle und Auslieferung** | Fehler über echte Bedienwege früher finden | H-01: Kontrollmatrix über Klappmechanismen hinaus | Bestehende QA erweitern; reale Plattformabnahme gesondert durchführen |

**Fortgeschriebene Empfehlung:** A-01 ist als bestehende Performance-Arbeit in 3.32.3 umgesetzt; als nächster Performance-Schnitt A-02/A-03 prüfen. Als anschließende sichtbare Funktion C-01 oder B-01 wählen. H-01 begleitet jede Umsetzung als Kontrolle. Das ist eine Empfehlung; die Auswahl und Reihenfolge sind noch offen.

Antwortformat: `A-02/A-03 weiter umsetzen, C recherchieren, G später`. Einzelaufgaben lassen sich wählen, z. B. `A-03 umsetzen; B-03 nur prüfen`. Je Richtung bzw. Aufgabe sind **recherchieren**, **Umsetzung vorbereiten**, **kleinen Teil umsetzen**, **später** oder **nicht verfolgen** möglich. Bei „umsetzen“ gilt zunächst nur der beschriebene kleine Schnitt einschließlich seiner notwendigen Prüfungen und Auslieferung.

## 2. Die Aufgaben

„Abnahme“ nennt den Nachweis, den eine spätere Umsetzung liefern muss. Umfang und Aufwand werden nach der Auswahl konkretisiert; aus dem vorhandenen Baustein folgt noch keine belastbare Lieferzeit.

### A – Tempo und Stabilität

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| A-01 / P03 | **Umgesetzt 3.32.3:** Bibliothekskarten erhalten, statt bei jedem Refresh sämtliche Widgets neu anzulegen | Ausgangsbefund 3.32.2: vollständiger Neuaufbau. 3.32.3 erhält Widgets im lebenden Bibliothekshost; Startseite bleibt Folgeschnitt | Kartenidentität, Lebensdauer und vollständige Invalidierung festlegen; zunächst Wiederverwendung in derselben Ansicht | Weniger Neuerzeugungen, gemessener Gewinn; Fokus, Scrollen, Reihenfolge, Undo, Design und Tageswechsel stimmen |
| A-02 / P04 | Bildlayout von bloßer Bildplatzierung trennen | `layout_images`, `place_images` und PreviewCache vorhanden | Gründe für Geometrieänderung messen; beim Scrollen nur platzieren, soweit tatsächlich möglich | Gleiche Umflüsse/Bildgrößen; Resize, Auswahl, Ziehen und Rückkehr ohne Callbackfehler |
| A-03 / P06 | Gleiche Refresh-Anforderungen pro Aktion zusammenführen | `save_items` aktualisiert bereits die Seitenleiste; weitere Aufrufer können erneut aktualisieren | Requests pro Aktion zählen; nur nachgewiesene Doppelarbeit entfernen | Keine verzögerte ungesicherte Speicherung; atomarer Schreibweg, Backups, Sperre und Undo erhalten |

Begleitend P01 um Verlaufvarianten, Speicherentwicklung und kalte/warme Messungen ergänzen. Keine pauschale Ersetzung von Dictionary-Schlüsseln durch Variablen und kein allgemeines FPS-Versprechen.

### B – Planen und Fokus

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| B-01 / G01 | „Exposé morgen 14:30, 45 Minuten“ mit sichtbarer Feldvorschau erfassen | Deutsche Datumshelfer, Wiederholungsparser und Slash-Befehle vorhanden | Kleine eindeutige Grammatik; Bearbeitungstag, Uhrzeit und Schätzung zuerst; bestehende Slash-Semantik ausdrücklich behandeln | D01: allgemeines Datum setzt Bearbeitungstag, „fällig/bis“ die Fälligkeit; keine stille Uminterpretation vorhandener Eingabewege, Erkennung rücknehmbar |
| B-02 / G05 | Eingebetteter Fokusmodus mit Countdown und Pausen | Eine laufende Zeiterfassung und `time_spent_minutes` vorhanden | Timer- und Pausenregeln, Neustart/Ruhezustand prüfen; freie Dauer zuerst, feste Pomodoro-Zyklen optional | Eine Zeitbuchung; Pause/Wechsel/Neustart verdoppeln keine Minuten; Tastaturbedienung |
| B-03 / **Neu** | Bei Zeitkonflikten passende freie Zeitfenster vorschlagen | `time_blocks` erkennt Überschneidungen; Kapazitätsbilanz zeigt Überplanung bereits an | Vorschläge nur für ausdrücklich gewählte Aufgaben; Lücken, Dauer und Tagesgrenzen untersuchen | Vorschau nennt neue Planung; keine stille Terminänderung; Fälligkeit bleibt erhalten, eine Übernahme ist ein Undo-Schritt |

G02 Eisenhower-Matrix bleibt als eigenes bestehendes Feature offen. Erst den sichtbaren Terminkontext und die genaue Feldwirkung definieren; B-03 ersetzt diese Ansicht nicht. Gewohnheiten bleiben Vorrat und werden durch diese Auswahl nicht automatisch vorgezogen.

### C – Aufgaben im Text

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| C-01 / G29 | Einzelne echte Aufgaben im Notiztext unterstützen | Gemeinsamer Editor; `NoteEditor.ALLOW_TASKS = False`, Aufgabenbereich oberhalb vorhanden | ID-basierte Aufgabenwege für Notizen öffnen; bloßes Umschalten des Flags reicht nicht | Text und Aufgabenbereich zeigen dieselben Punkte; Abhaken, Bearbeiten, Löschen, Undo und Laden konsistent |
| C-02 / G31 | Eine Seitenaufgabe in eine passende Aufgabenliste schicken und einen Verweis behalten | Verschieben vorhanden, `move_items_to_list` hängt heute an Baumzeilen | Verschieben anhand IDs von sichtbarer Baum-Auswahl entkoppeln; Quellreferenz und Eigentümerschaft klären | Keine doppelte Aufgabe; Referenz, Details, Planung, Papierkorb und Undo funktionieren aus beiden Ansichten |
| C-03 / G32 | In „Mein Tag“ gezielt Aufgaben aus Seiten und Notizen finden | Herkunft/Listenart und vorhandene Kopfzähler nutzbar | Bestehenden Filterweg erweitern; Zähler wiederverwenden | Filter trifft dieselben Originalpunkte und aktualisiert nach Verschieben/Undo; kein zweiter Aufgabenbestand |

D05 bleibt verbindlich: Liste, Notiz und Seite behalten ihren Zweck und Typ. Aus diesen Aufgaben folgt keine allgemeine Formatkonvertierung.

### D – Suchen und Wissen

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| D-01 / G14, P07 | Volltext über Seiten-/Notiztext und Aufgaben mit Ausschnitt und Fundstelle | Bestehende Suche und `quick_open_results`; kein FTS-Index im geprüften Anwendungscode | SQLite-FTS5-Probe, Indexaktualisierung und Rückfall; Anhangnamen zuerst, Anhanginhalt eigener späterer Umfang | Treffer führen zum tatsächlichen Inhalt; Cache jederzeit neu aufbaubar, Datenöffnung funktioniert ohne FTS5 |
| D-02 / G08, G30 | Seiten, Listen und Aufgaben im Text verknüpfen; Rückverweise anzeigen | Aufgabenverknüpfungen und `item_backlinks` vorhanden | Gemeinsame Referenzschicht mit stabilen IDs; Normalisierung/Altleser vor neuem Dokumentinhalt prüfen | Umbenennen, Import, Löschen, Wiederherstellen und fehlende Ziele verlieren keine Verweise |
| D-03 / **Neu** | Aktive Filter erklären: warum ein Punkt erscheint oder ausgeblendet ist | Gespeicherte Filter und Status-/Label-/Suchprüfung vorhanden | Dieselbe Filterauswertung mit nachvollziehbaren Gründen ergänzen; keine zweite Filterlogik | Erklärung entspricht dem Ergebnis; kombinierte Filter und leere Treffer verständlich, per Tastatur erreichbar |

### E – Projektseiten

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| E-01 / G28 | Bestehende Aufgabenliste live in einer Projektseite anzeigen | Aufgabenmodell und Seitenblöcke vorhanden; Live-Einbettung noch offen | D-02/Referenzvertrag zuerst; zunächst eine begrenzte Listenansicht statt vollständigem Board | Abhaken ändert Originalaufgabe; keine Kopien, klare Löschwirkung, keine Einbettungszyklen |
| E-02 / G09 | Lokales Titelbild oder Pixelzeichnung zur Wiedererkennung verwenden | Bilder, Bibliothekskarten und Galerie vorhanden | Cover-Speicherung/Altleser prüfen; bestehende Karten ergänzen | Vorschau, Änderung, Import und Backup korrekt; große Bilder bremsen den Kartenaufbau nicht unkontrolliert |
| E-03 / **Neu** | Gefüllte Vorlage vor dem Anlegen vollständig prüfen | Listen-/Ordnervorlagen und gemeinsame Platzhalterabfrage existieren bereits | Vorschau an `create_list_from_template` anschließen; erste Stufe zeigt Struktur und aufgelöste Texte, zukünftige Verweise danach | Abbrechen legt nichts an; Vorschau entspricht Erzeugung; Fehlstellen erkennbar, Anlage einmal rücknehmbar |

Eine Vorlage für ein ganzes Ordnerpaket ist bereits möglich. E-03 erfindet diese Funktion nicht neu, sondern erweitert die Vorschau und später die Referenzprüfung.

### F – Austausch und Sicherungen

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| F-01 / G24 | Kontextdateien und nachvollziehbare Änderungsvorschläge für KI-Austausch | `.glideexchange`, Markdown und bestätigte Importvorschau vorhanden | Exportierte Basisversion und ID-Zuordnung, Feldvergleich und veraltete Vorschläge untersuchen; erst danach Patch-Übernahme | Auswahl zeigt konkrete Feldänderungen und Konflikte; nichts wird still überschrieben; keine direkte Nachrichten- oder Cloudanbindung |
| F-02 / G21 | Notion-Markdown/ZIP oder Todoist-CSV zuverlässig übernehmen | Markdown-, CSV- und Backup-Import als Bausteine vorhanden | Zuerst **ein** Quellformat wählen; aktuelle Exportstruktur, Links, Anhänge und Verluste mit künstlichen Beispielen prüfen | Vorschau und Verlustbericht; keine unbeabsichtigten Dubletten; ursprüngliche Datei unverändert |
| F-03 / **Neu** | Zwei Sicherungsstände lesbar vergleichen | Vollständige Sicherungen und Mengen-/Inhaltsvorschau vorhanden | Zunächst reiner Vergleich von Titeln, Text, Status und Terminen bei stabilen IDs; kein Merge | Änderungen/Neu/Entfernt nachvollziehbar; kein Schreibzugriff, keine Wiederherstellung; unabhängige Imports nicht allein am Titel gleichsetzen |

### G – Pixel-Werkstatt

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| G-01 / G19 | Paletteneintrag ändern und alle zugehörigen Pixel umfärben, mit Undo | `DrawingModel.cells` ist bereits indiziert; Palettenimport/-export vorhanden | Editor für Einträge und Transaktions-/Undo-Vertrag; Index 0 und Transparenz ausdrücklich prüfen | Farbvariante rücknehmbar; Speichern/Laden/PNG erhalten Indizes; heutige Weiß-Regel nicht still umdeuten |
| G-02 / G17 | Frames, Dauer und Animationsvorschau hinzufügen | Einzelbildmodell; Aseprite-Import liest bisher Paletten, keine Animation | Begrenzte Modellprobe mit mehreren Frames; Migration/Altleser und Dateigrenzen zuerst | Alle Frames/Dauern über Backup und Undo stabil; Vorschau und Spritesheet reproduzierbar; GIF nur im entschiedenen Umfang |
| G-03 / **Neu** | Symbol vor Export in realen 16/32/48-Pixel-Größen beurteilen | PNG- und ICO-Export bereits umgesetzt | Vorschau und Rand-/Transparenzprüfung am bestehenden Exportweg | Vorschau stimmt mit Datei überein; Pixelkanten bleiben scharf; kein neuer paralleler Exporter |

**D07 bleibt offen:** Bei Auswahl von G-02 entscheiden, ob die erste Etappe ein abspielbares GIF enthalten soll oder Frames/Vorschau/Spritesheet genügen. Ein Spritesheet ist eine PNG mit mehreren Frames, keine selbst abspielende Animation.

### H – Bedienkontrolle und Auslieferung

| Nr. / Bezug | Aufgabe und Nutzen | Aktuelle Grundlage | Recherche bzw. erster Schnitt | Abnahme |
|---|---|---|---|---|
| H-01 / D08 erweitert, **Neu** | Echte Bedienwege auch für Menüs, schwebende Werkzeuge und Drag-Aktionen systematisch absichern | 58 Suiten; Klapp- und Drag-Pflichtsuiten prüfen native Ereignisse/Callbackfehler | Kontrollmatrix aus Vertrag 69 auf kritische Aktionsfolgen erweitern; vorhandene Suiten wiederverwenden | Pro Aktion konkrete Vor-/Nachbedingung, Undo, Fokus/Scrollen, Neustart und Callbackfehler geprüft; keine bloßen Setter-Proben |
| H-02 / **Neu** | Zum Ziehen passende Tastaturwege mit sichtbarem Ziel herstellen | Verschiebemenüs, Tastaturbindungen und Zielauswahl vorhanden | Bedienparität je Aktion erfassen; nur nachgewiesene Lücken schließen, bestehende Dialoge verwenden | Seiten/Notizen/Ordner ohne Maus bewegen; zulässiges Ziel und erwartete Wirkung erkennbar, ein Undo-Schritt |
| H-03 / G26 | Desktop-Paket mit eingebettetem Python reproduzierbar vorbereiten | Entwicklungsbundle nutzt installiertes Python und Ad-hoc-Signatur | Build-Probe für gewählte Zielplattform, Tk-/tkDnD-Mitnahme und Clean-Machine-Prüfung; Signatur/Store separat | Nachweis auf Gerät ohne Entwicklungs-Python; feste Versionen/Lizenzen, Daten außerhalb des Pakets, aktueller SHA-Abgleich |

H-01 ergänzt D08, ohne die abgeschlossene Klappkorrektur erneut als offen zu führen. Physische Maus/Trackpad, Windows/Linux, DPI und Screenreader bleiben eigene Plattformnachweise.

## 3. Erneuter Codeabgleich

Der [Anwendungscode](../01_Repository/Glide/src/glide/app.pyw) blieb unverändert: SHA-256 `c51b811fdd0d804834f727f4a55ce2b16e770654adfb597245f4503d61b1c7e6`. Zeilen sind Orientierung im Stand 3.32.2; dieser Abgleich ist gezielte statische Untersuchung, keine neue Vollprüfung.

| Bereich | Gelesene Anker in `app.pyw` | Konsequenz |
|---|---|---|
| Eingabe | `parse_capture_due` 3492; `parse_slash_commands` 3543 | `/morgen` setzt bisher `due`; den neuen Bearbeitungstag-Vertrag mit Altbedienung ausdrücklich vereinbaren |
| Planung | `time_blocks` 17154; `apply_time_plan` 17222; `planning_summary` 17630 | Kapazitätsanzeige und Überschneidungen sind vorhanden; B-03 ergänzt Vorschläge |
| Performance | `_refresh_home` 21044; `refresh_library_page` 22166; `save_items` 37388 | Widget-Neuaufbau und Refresh-Konsolidierung bleiben konkrete Arbeitsziele |
| Editor | `RichNoteEditor.normalize` 8583; `NoteEditor` 10543; `layout_images` 10023; `place_images` 10197 | Daten-/Altleservertrag vor Referenzen; Bilder brauchen keinen zweiten Cache |
| Vorlagen | `capture_template` 22624; `template_fields` 22749; `create_list_from_template` 22911 | Ordnerpakete und Feldabfrage existieren; Vorschau gezielt ergänzen |
| Bewegen | `move_list_to_folder_dialog` 31235; `move_sidebar_selection` 32364; `move_items_to_list` 47082 | Tastatur-/Textaufgabenwege an vorhandene Aktionen anschließen |
| Fokus/Suche | `start_time_tracking` 46322; `stop_time_tracking` 46336; `quick_open_results` 52389 | Zeiterfassung und Befehlssuche erweitern; kein zweiter Timer und keine zweite Befehlspalette |
| Austausch | `build_exchange_payload` 48284; `show_exchange_import_dialog` 48863; `format_app_backup_preview` 51110 | Importvorschau/Mengenvorschau existieren; Feld-Diff und Sicherungsvergleich separat untersuchen |

Zusätzlich [Zeichenkern](../01_Repository/Glide/src/glide/drawing.py) und [Markdown-Austausch](../01_Repository/Glide/src/glide/page_markdown.py) als bestehende Fachmodule berücksichtigen. Neue interne Dokumentinhalte können eine Schemaerhöhung verlangen; Format 21 ist nicht exklusiv für Animation reserviert.

## 4. Marktimpulse: geprüft, daraus abgeleitet

Kurzer Quellencheck am 30.09.2026; keine vollständige Marktstudie oder neue Preisbewertung. Die Glide-Aufgaben sind unsere Ableitung, keine zugesagte Herstellerkompatibilität.

- Todoist dokumentiert die Erfassung von Datum, Deadline und weiteren Feldern sowie rücknehmbare Datumerkennung. Das stützt die sichtbare Vorschau in B-01; Glides D01 bleibt maßgeblich. [Offizielle Quick-Add-Dokumentation](https://www.todoist.com/help/todoist/features/use-task-quick-add-in-todoist-va4Lhpzz).
- Obsidian erklärt Suchoperatoren, Suchkontext und die Funktion „Explain search term“. Daraus leite ich D-03 für die bereits bestehenden Glide-Filter ab. [Offizielle Suchdokumentation](https://obsidian.md/help/Plugins/Search).
- Notion beschreibt verknüpfte Datenquellen: Ansichten können eigene Filter haben, Änderungen an den Inhalten wirken auf die ursprüngliche Quelle. Das ist ein Vorbild für E-01 mit Originalaufgaben. [Offizielle Dokumentation](https://www.notion.com/help/data-sources-and-linked-databases).
- Aseprite dokumentiert Frames, Vorschau, Frame-Dauer und Zwiebelhaut. Das stützt eine begrenzte, eigenständige Animationsetappe G-02; es belegt keine GIF-Exportfähigkeit von Tk. [Offizielle Animationsdokumentation](https://www.aseprite.org/docs/animation/).

## 5. Entscheidungen und anschließender Ablauf

| Entscheidung | Stand |
|---|---|
| Erste Richtung und ggf. zweite Priorität | offen; Empfehlung A, anschließend C oder B |
| Bearbeitungstiefe | offen: Recherche/Plan, kleiner Umsetzungsschnitt oder nur Sammlung |
| G-02: erster Animations-Exportumfang | D07 weiterhin offen; nur bei Animation relevant |
| F-02: erste Importquelle | erst bei Auswahl: Notion-Markdown/ZIP oder Todoist-CSV |
| Neue Zusatzaufgaben | B-03, D-03, E-03, F-03, G-03, H-01/H-02 als Vorschläge, nicht automatisch beauftragt |

D01–D06 bleiben entschieden. Mobile/Toolkit-Wechsel, Cloud/Mehrbenutzerbetrieb, allgemeine Formatkonvertierung und Gestaltungsänderungen an Hinweisblöcken werden durch diese Auswahl nicht wieder eröffnet; einklappbare Hinweiszeilen sind mit D11 beschlossen. Keine neuen Laufzeitabhängigkeiten ohne dokumentierte Entscheidung; Nach D09 ist das GitHub-Repository die maßgebliche Ablage; D17 fordert Tk-freie Fachmodule.

Nach der Auswahl: ein kleines Ergebnis definieren → notwendige Recherche/Modellprobe → Code- und Datenvertrag → konkrete Aufgaben mit Abnahme → passende Baseline und Implementierung → gezielte und erforderliche vollständige QA → dokumentierter Versions-/Auslieferungsabgleich. Bei reiner Recherche endet der Schnitt mit Befunden und einer konkreten Entscheidungsvorlage. Bestehende grüne Tests werden nicht als Abnahme noch nicht implementierter Features ausgegeben.

Antworten des Inhabers werden hier und in der Arbeitsplanung nachgeführt; bis dahin ist keine Auswahl eingetragen. Die [Performance-Abschlussaufgabe](Glide_Arbeits_und_Featureplanung_2026-09-30.md#9-abschlussaufgabe--ausdrücklich-aufnehmen) bleibt Bestandteil der Arbeitsplanung.
