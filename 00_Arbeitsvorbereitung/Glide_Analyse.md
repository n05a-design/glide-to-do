# Glide – Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung

**Einordnung nach Integration am 18.10.2026:** Die folgende Gesamtanalyse bewahrt den untersuchten Vorzustand `c0252ba` / App-Hash `ed2b7eb…` sowie die damalige Upstream-Probe. FP-01 und WA-27–WA-30 sind inzwischen im lokalen Prüfkandidaten integriert. Aktuelle Quell-, Prüf- und Lieferstände stehen im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), Aufgaben nur im [Plan](Glide_Entwicklungsplan.md). Die vollständige Ablagenachprüfung steht im [Nachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Historische Befunde und Messergebnisse werden hier nicht umgedeutet.

Stand 18.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · lokale Quelle `c0252ba`, davon getrennter Upstream-Kandidat `9ec474b` · Analyse und Planung, keine Produktionsrunde

Diese Fassung führt die Analysen vom 08.–15.10.2026 zusammen und ersetzt deren überholte aktive Bewertungen. Die Vorfassungen bleiben in Git. **Glide besitzt bereits einen breiten lokalen Arbeitsumfang; sein offener Kern ist inzwischen die sichere Integration und Auslieferung zusammenhängender Abläufe.** Der jetzige Auftrag umfasst Analyse, Recherche, Dokumentationspflege und Planung. Produktionslogik, Datenformat, echte Nutzerdaten und ausgelieferte Pakete bleiben unverändert.

Navigation: [tatsächlicher Stand §9](#9-gesamtanalyse-vom-18102026) · [Szenarien §10](#10-nutzungsszenarien-und-bereichsübergänge) · [Code §11](#11-systematische-codeanalyse) · [Abdeckung §12](#12-abdeckung-und-abschlussabgleich) · [Quellen und Rekonstruktion §12.2](#122-quellen-und-rekonstruktionsbilanz-der-gegenprüfung). Aufgaben und Umsetzungsreihenfolge stehen allein im [Entwicklungsplan](Glide_Entwicklungsplan.md); Herstellerrecherche allein in [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md); bestätigte Entscheidungen allein in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md).

**Belegarten:** **Auftrag** = direkte Beauftragung; **Entscheidung** = dokumentierter Inhaberwortlaut, D49 ausdrücklich eine Auslegung; **Code** = untersuchte Datei/Commit; **Probe** = hier tatsächlich ausgeführter Versuch mit künstlichen Daten; **QA** = bestimmter historischer oder neuer Lauf, dessen Umfang und Ergebnis benannt werden; **Lieferung** = vorhandene Datei und Hash/Manifest; **Primärquelle** = aktuelle Herstellerdokumentation; **Einschätzung** = daraus abgeleitete Empfehlung. Keine dieser Stufen ersetzt eine andere. „Implementiert“ bedeutet nicht automatisch geprüft oder ausgeliefert. Eine technische Fehlerinjektion beweist den Fehlerpfad, keine Häufigkeit im normalen Alltag. Es liegen keine Nutzungsstudien und keine Telemetrie vor.

## 1. Untersuchter Bestand

| Bereich | Aktuell untersuchte Abgrenzung | Ergebnis und Beleggrenze |
|---|---|---|
| Maßgeblicher Projektordner | `Github/glide-to-do`, Quellbaum `01_Repository/Glide`; Windows-Arbeitskopie | Keine Vermischung mit der älteren OneDrive-Glide-Ablage; relative Pfade beziehen sich auf diese Wurzel |
| Git | lokaler Zweig `claude/tag3390-sichtbarkeit`, HEAD `c0252bad69780c86b853f2653d5396e5256c0b32`, zu Beginn sauber | Upstream und weitere lokale Planungsstände lesend abgeglichen, keine Git-Integration (§9) |
| Eigene Laufzeit | 67 Dateien einschließlich `app.pyw`, davon 62 ohne Tk-Import; zusätzlich isolierte Bedienprobe `drawing_prototype.pyw` | Strukturelle Abdeckung aller Dateien und gezielte Vertiefung in §11; „ohne Tk-Import“ beweist allein keine vollständige fachliche Entkopplung |
| Zentraler UI-/Adaptercode | `app.pyw` 61.256 Zeilen, `ListApp` 46.929 Zeilen mit 1.634 direkten Methoden | Größe und Kopplung sind Wartbarkeitsbefunde, keine Laufzeitmessung |
| Prüfbestand | lokale Liste `SUITEN` mit 92 Integrationssuiten; Fachlogik und Werkzeugtests zusätzlich | Ausgeführte aktuelle Grundstufe und gezielte Fehlerproben im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md); kein neuer vollständiger Integrationslauf |
| Dokumente | maschinelles Inventar einschließlich lokaler ausgeschlossener Dateien, 48 aktive Markdown-Dokumente außerhalb historischer QA-/Fixturebelege und erzeugter Paket-/Vendorbestände | Zweck, Zuständigkeit und Behandlung §7; keine Inhalte echter Nutzerdaten oder privater Fehlerprotokolle gelesen |
| Lieferung | 67 Code- und 146 Ressourcen-/Vendordateien in `07_Python-Versionen`, sechs Showcase-Dateien | Neu per SHA-256 bytegleich; eigenständige Pakete separat (§9) |
| Originalreferenzen | UI-/UX-Originalauftrag, Prompt, Bildzuordnung und 28 lokale Originalbilder | Größen und SHA-256 aller 28 stimmen; Bilder bleiben vom Git-Upload ausgeschlossen. Keine neue visuelle Produktprüfung dieser Bilder behauptet |
| Plattform hier | Windows 11, Python 3.14.7, Tcl/Tk 9.0.4 | Native Mac-/Linux-Ausführung, eigene Tk-9.1-Runtime und echte Screenreader wurden in dieser Runde nicht betrieben |

Die Dateiinventur erfasst Metadaten einschließlich ignorierter Hauptcheckout-Dateien. `.git`, separate Arbeitskopien, lokale heruntergeladene CI-Rohartefakte und echte Arbeitsdaten sind eigene Klassen; sie werden nicht pauschal geöffnet oder gelöscht. Windows-Langpfade wurden über den erweiterten Dateipfad erneut erfasst, nachdem der normale Zugriff an einem langen Inspirationsbild scheiterte. Das endgültige Metadateninventar hat keine Lese-/Statfehler.

## 2. Funktionsanalyse

Maßgeblicher Verhaltensvertrag ist [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md). Das vollständige Kennungsregister mit Verbindlichkeit, Ist-/Restumfang, Modulen, Prüfstand und Paketzuordnung steht im [Entwicklungsplan §18](Glide_Entwicklungsplan.md#18-konsolidiertes-funktions--und-aufgabeninventar). Diese Übersicht erklärt die Zusammenhänge und bildet kein zweites Backlog.

| Bereich | Heutiger lokaler Umfang | Tatsächliche Lücke / Trennung |
|---|---|---|
| Erfassen und Organisation | Eingabe mit bestätigten Feldchips, mehrzeiliges Einfügen, Eingang, Aufgaben/Langtext/Gruppen/Überschriften, Unterpunkte, Checklisten, Labels, Ordner, Archiv/Papierkorb | Erweiterte Wiederholungen bleiben Text mit Hinweis statt falscher Teilerkennung; neue Serie benötigt FP-02, keine zweite Eingabemaske |
| Tages- und Wochenplanung | Bearbeitungstag und Fälligkeit getrennt; Aufwand, Kapazität, Zeitblöcke, Vorschläge, Fokus, Routinen, Tagesbeginn/-abschluss, Hinweise, lokale ICS-Belegzeiten, Tag entlasten | Keine automatische Kalender-Synchronisierung; zusätzliche Wochenrituale und Zeitberichte sind getrennte Vorschläge. Kapazität ist eine Entscheidungshilfe, keine Garantie gegen jede Terminüberlappung |
| Wiederholungen | sechs Regelarten, Enddatum/Anker, Termin auslassen, verpasste Termine überspringen; Monatsende-/Zeitzonenfehler in 3.39.1 behoben | Intervall-/Wochentag-/Ausnahme-/Erledigungsanker benötigen gemeinsame Semantik zwischen Erfassen, Aufgabe und ICS; FP-02 darf nicht nur einen Dialog erweitern |
| Liste, Tabelle, Pinnwand | gemeinsame Originalaufgaben, Inspektor und direkte Felder; freie/geordnete/Spaltenansicht, Verbindungen/Präsentation | gespeicherte Filter speichern noch keine vollständige Ansicht; Seiten-/Notizkarten fehlen lokal. Objektidentität muss über Undo/Import erhalten bleiben |
| Seiten und Wissen | Blockeditor, lokale Bilder/Titelbilder, echte Aufgaben mit Original-ID, Live-Listen, Verweise/Rückverweise, Notizen/Notizbücher/Galerien | unverknüpfte Erwähnungen und lesende Nebenansicht sind Ergänzungen; Unterseiten, Datenbank-Baukasten und allgemeiner Editorneubau bleiben außerhalb der bestehenden Entscheidungen |
| Suche und Großbestand | gemeinsame Inhalts-/Aktionspalette, Trefferstellen, erklärte Filter, stabile Aktions-IDs | historische 66,6 ms bei 10.000 Punkten gelten nur für die damalige Messung; aktuelle Render-/Import-/Bildkosten nicht daraus ableiten |
| Undo und Fehler | global 20 komprimierte Bestandsschritte; eigene Text-/Zeichenhistorien | globales Redo fehlt lokal, ist aber in `origin/main` als FP-01-Kandidat implementiert. A32/A34/A35 zeigen zusätzliche Fehlergrenzen, die ein neuer Redo-Stapel allein nicht schließt |
| Kreatives Arbeiten | Pixelzeichnungen 16–128, Paletten, PNG/ICO/SVG/JSON und seit 3.40.0 Bildfolgen mit Dauern, Vorschau, Spritesheet/Einzelbildern | kein GIF-Auftrag und kein vollständiges Ebenen-/Vektorprogramm; Transfer in Symbole, Seiten und Pinnwand ist der konkrete Produktbezug |
| Import, KI und Portabilität | CSV/Markdown/ICS, `.glidepage`, Aufgaben-/App-Sicherung, Vergleich, dateibasierter KI-Kontext und geprüfte Vorschläge; Notion-Import/Wiedererkennung und Seitenrestore seit 3.41.0 | offener Gesamtexport mit Manifest ist FP-07; App-Sicherung, lesbarer Austausch und verlustfreie Wiederherstellung sind unterschiedliche Leistungsversprechen |
| Oberfläche | zehn Designs, berechnete Kontraste, Rollenfarben, schmale Seitenleiste, Hinweisschalter, B01–B20, Mindestgröße 860 × 700 | E-U1–E-U3 sind konkrete offene Auswahlen. Historisch bestandene Geometrieprüfungen ersetzen keine persönliche Sicht-/DPI-Abnahme |
| Zugänglichkeit und Betrieb | additive semantische Adapter im lokalen Quellbaum, eigenständige 3.42.0-Pakete vorhanden, Start-/Format-/Sperr-/Backupschutz | Paket 8 ist trotz vorhandener Adapter noch nicht abgenommen/geliefert. Hier vorhandenes Mac-Bundle ist unvollständig; Reader-, Mac- und Release-Tore bleiben getrennt |

**Produktfolgerung [Einschätzung]:** Der nächste Nutzen entsteht vor allem durch konsistente Übergänge: eine Aufgabe im Text, in Heute und auf einer Pinnwand bleibt dieselbe; eine Planung ändert das ausdrücklich genannte Feld; eine fehlgeschlagene Speicherung stoppt die Folgeaktion; ein Export benennt Verluste. Zusätzliche Hauptbereiche würden diese Integrationsarbeit vergrößern. Notion ist ein belegtes Vorbild des Inhabers, kein Auftrag zum Nachbau aller Notion-Datenbankfunktionen.

## 3. Abgleich Dokumentation ↔ Implementierung

Die Kennungen A01–A30 bleiben auffindbar; ausführliche damalige Beobachtungen stehen in Git und den bezeichneten QA-Belegen. Die folgenden konsolidierten Status ersetzen widersprüchliche aktive Zwischenstände.

| Kennung | Gegenstand und heutiger Befund | Einordnung / zuständiger Verweis |
|---|---|---|
| A01–A06 | fehlender Dokumentationsabgleich, falsche Kopf-/Paket-/Format-/Modulzahlen und N01/I7-Abhängigkeit aus 08.10. | damalige Korrekturen erhalten; diese Runde erneut semantisch abgeglichen (§7). Kein Beleg einer neuen Produktentscheidung |
| A07–A11 | Retention-Verknüpfungen, Fokuskommentar, Python-Annahme, native Mac-Standangabe, OneDrive-Ausgabestrom | historische Werkzeug-/Dokumentbefunde; aktuelle Plattform-/Ausführungsgrenzen stehen in §9 und QA. Frühere Mac-Prüfung bestätigt kein heutiges vollständiges Bundle |
| A12/A13/A15 | überholte Marktlücken, Tempoangaben und 07-Lieferabsatz | Markt konsolidiert, Messwerte datiert; 07 aktuell hashgleich. Kein ungeprüfter Transfer alter Zeiten auf 3.43.1 |
| A14 | Symbolfallbacks systemübergreifend uneinheitlich | später D28/D29/B10 präzisiert und umgesetzt; physische Glyphen-/DPI-Sichtabnahme getrennt offen |
| A16/A17 | vollständige Erfassung schlecht erreichbar; Erledigen im Überblick ohne reguläre Wiederholungsfolgen | seit 3.33.20 behoben; echte gemeinsame Mutation bleibt Regel |
| A18/A19 | Altleser-Proben durch Retention und Sperrzeitstempel an Sekundengrenze | historische Prüfwerkzeugkorrekturen; ausgelassene Altleserprobe außerhalb Retention ausdrücklich als ausgelassen führen |
| A20/A21/A22/A23 | Einrücken, Suchkosten, überlappende/fehlende Seitenbilder, Dreifachklick beim Umfärben | in 3.34.0/3.35.0 geliefert; die damaligen Mess-/UI-Belege bleiben historisch |
| A24/A25 | Plattformstände, Inspektor/OB02/OB03 und Animation in Architektur/Markt veraltet | aktuelle Quellen korrigiert; Lieferung/Abnahme heute differenziert |
| A26 | Aufgaben- und ICS-Wiederholungsrechner getrennt | weiterhin Wartungs-/Integrationsbefund; gemeinsame Verträge für FP-02 statt unkontrollierter Zusammenlegung |
| A27 | bekannte verschachtelte Einstellungsstrukturen verwerfen Unbekanntes beim Normalisieren/Prunen | WA-09 als Vorarbeit vor FP-04; Containerformat 2 allein garantiert keinen Schutz neuer verschachtelter Felder (§11) |
| A28/A29/A30 | Monatsende-/Schaltjahrserien im ICS-Austausch, Teilerkennung von Serienangaben, Zeitzonen im Aufgabenimport | in 3.39.1 gezielt korrigiert und geliefert; kein erneuter offener Fehlerauftrag. FP-02 muss diese Gegenproben bewahren |
| A31–A35 | Bildkonversion, Guard-/Undo-/Lade-/Flush-Fehlergrenzen | neue technische Belege in §11, Aufgaben ausschließlich im Plan |

Die frühere pauschale Aussage „kein Datenintegritätsrisiko“ wird nicht fortgeschrieben. Sie war durch die damalige Stichprobe nicht ausreichend gestützt und widerspricht den jetzt nachgewiesenen Schutzfehlerpfaden. Ebenso entfallen nicht belegte Behauptungen wie „jedes Vergleichsprodukt bietet Redo“ und „ohne Gegenstück“. Vergleichbar sind konkret dokumentierte Abläufe mit ihren Grenzen.

## 4. Oberflächenanalyse

Untersucht wurden der bestehende Layout-/Interaktionscode, Nutzeraufträge, Designrichtlinien und historische Pflicht-/Gegenproben des UI-/UX-Pakets. **Diese Runde enthält keinen neuen vollständigen visuellen Produktaudit.** Nutzerbilder wurden nach Manifest geprüft, nicht als frisch getestete Oberfläche behandelt. Menschen-, Eingabe-, DPI- und Readerabnahmen stehen weiterhin in der [manuellen Prüfliste](Glide_Manuelle_Pruefung.md).

Die drei festen Zonen Seitenleiste/Kopf/Inhalt und der gemeinsame Inspektor sind tragfähige vorhandene Strukturen. B01–B20 korrigieren beobachtete Reibung im bestehenden Aufbau; daraus folgt keine Freigabe für kleinere Fenster, zwei bearbeitbare Inhalte oder einen neuen Editor. E-U1 betrifft einen ausdrücklich reduzierten Kompaktkopf, E-U2 die Anzahl aktiver Ansichten, E-U3 konkrete Notion-Muster. Diese Änderungen unterscheiden sich erheblich in Kopplung und Prüfaufwand. Eine allgemeine Mindestgrößensenkung ist nicht durch die bisherigen 860-×-700-Prüfungen gedeckt.

| Beobachtung / früherer Befund | Heutiger Zusammenhang | Konsequenz |
|---|---|---|
| O01–O04: dichte Zeilen, Seiten-/Zeilenhierarchie, dauerhafte Aktionen | N05/KO04/OB02/OB03 und B11–B14 bereits implementiert; Titel und Metadaten hängen vom Kontext ab | neue Funktion in vorhandene Feld-/Aktionswege integrieren, kein zweiter Editor |
| O05–O07: Systemzeichen, Kopfaktionen, Startseitenfülle | Symbolpolitik, Lupe/Fallback, optische Glyphenregel und acht Standardkacheln dokumentiert | alte „sieben Kacheln“/„Su immer“/„Kopfdatum“ sind keine aktuellen Verträge |
| O08–O11: Eingabe, Pinnwandwerkzeugleiste, Bilder, Seitenleiste | überwiegend seit 3.33.20–3.34.0 geliefert; Bildscrollen B16 später korrigiert | kalte Bildkonversion A31 ist ein anderer Fehlerpfad als der schon korrigierte Scrollsprung |
| Aufgabenkontext über mehrere Bereiche | Original-ID vorhanden, aber aktiver Host/Fokus/Editorzustand zentral | lesende Nebenansicht ist kleiner als zwei schreibende Hosts, benötigt trotzdem Flush-/ID-/Schließtests |
| Fehler- und Erfolgsrückmeldung | A32/A33/A35 zeigen Widerspruch zwischen tatsächlichem Ergebnis und gemeldeter Wirkung | Erfolgstexte an tatsächliche persistierte Wirkung binden; fachliche Meldung vor weiterer Aktion |

## 5. Entscheidungsanalyse

Bestätigt sind D01–D48 und D50 sowie die aus dem getrennten Planungszweig rekonstruierte **D51 vom 17.10.2026**. D49 bleibt als damalige Auslegung mit Korrekturvorbehalt kenntlich. Neue Entscheidungen beginnen bei **D52**. Die im getrennten Zweig enthaltenen E-P1–E-P5 und WA-19–WA-25 sind Vorschläge mit bereits vergebenen Kennungen und müssen erhalten werden; ihre bloße Existenz ist keine Zustimmung. Das vollständige aktuelle Entscheidungsregister mit Antwortoptionen steht im [Entwicklungsplan §20](Glide_Entwicklungsplan.md#20-vollständiges-entscheidungsregister).

| Themenfamilie | Bestehende Festlegung | Bedeutung für diese Runde |
|---|---|---|
| Planung | D01/D02/D10/D13/D14: Bearbeitungstag ≠ Fälligkeit, sichtbare Feldsemantik, zwei Hauptansichten | Serien, Kalender und Vorschläge dürfen die Felder nicht still gleichsetzen |
| Technik | D03/D15/D16/D17: Desktop/Tk, Python/Tk-Basis, JSON-Hauptspeicher, neue Fachlogik Tk-frei | gezielte Entkopplung möglich; anderer Toolkit-/Speicheransatz bleibt gesonderte Richtungswahl |
| KI/Datenschutz | Q2/Q3 und Produktgrenzen: lokale Kernfunktionen, keine neuen plattformeigenen Laufzeitabhängigkeiten, externer KI-Dateiaustausch | FP-06 verbessert Auftrag/Prüfung; keine Endpunkt-/Cloud-/MCP-Integration aus dieser Recherche ableiten |
| Lieferung/Abnahme | D42/D43: native und menschliche Tore sowie Veröffentlichung separat | CI-Grün ist keine Lizenz-, Signatur-, Mac- oder Menschenfreigabe |
| Paketfolge | D44/D49, D50 UI-/UX-Vorrang, Abschlussauftrag 15.10. | neue Phasenfolge muss diese Vorgeschichte explizit auflösen; E-P2 bleibt Auswahl, keine automatisch genehmigte Parallelisierung von Paket 8 |
| Prüftakt | D51: mehrere Pakete je Phase, gezielte Prüfungen während der Arbeit, Vollprüfung und Lieferung am Phasenende | größere fachliche Pakete mit einem eingefrorenen Abschluss; Schutzfehler rechtfertigen eine gesonderte Korrekturrunde |
| Aktueller Auftrag 18.10. | Analyse, Recherche, Dokumentationspflege, theoretische Planung | keine Produktionsumsetzung und kein neuer Versions-/Lieferstand in dieser Runde |

Bewusst ausgeschlossene und zurückgestellte Ideen bleiben mit Gründen erhalten (Planregister). Ein grundlegender Toolkitwechsel, Cloud-/Teammodell oder relationaler Baukasten würde die Produktausrichtung verändern. Der neue Codebefund rechtfertigt gezielte Schutz- und Adapterverbesserung, noch keine solche Grundsatzänderung.

## 6. Erkenntnisgewinn gegenüber früheren Analysen

| Frühere Untersuchung / Grenze | Was weiter gilt | Was neu geklärt oder vertieft wurde |
|---|---|---|
| 03./08.10.: Marktbreite, Funktionslücken, Tagesabläufe; keine Nutzungsstudie | Vorbilder und konkrete Nutzeraufträge als Bedarf; keine Behauptung gemessener persönlicher Eignung | aktuelle Primärquellen, Offline-/Konten-/Exportmodelle getrennt, Szenarien und Paketbedingungen statt bloßer Featurehaken |
| 08./09.10.: Stand 3.33.18–3.35.0, O-/A-Befunde, Sprint | historische Messungen und behobene Fehler behalten ihre Belegfunktion | keine aktuellen Modul-/Suite-/Lieferzahlen aus dieser Baseline übernommen |
| 13.10.: 3.39.0, FP-00 und FP-01–FP-07, A26–A30 | Serien-/Einstellungsrisiken, alltagsbezogene Lücken | Animation/Import/Pakete inzwischen vorhanden; FP-01 upstream Kandidat; A31–A35 und Modul-/Callerabdeckung neu |
| 15.10.: UI-/UX-Originale, Paketvollständigkeit, lokale Bundlegrenze | unveränderte Quellen/28 Referenzen und getrennte Menschenabnahme | alle 28 Hashes und heutige Manifestdateien neu geprüft; historische „vollständig geliefert“-Formulierung nicht auf aktuelle Mac-Kopie übertragen |
| 17.10.: getrenntes Phasenprogramm, D51/E-P/WAs | weniger wiederholte Gesamtprüfung, größere Nutzpakete | gültige Entscheidung über Zweige rekonstruiert; Vorschläge in einen Plan zurückgeführt; ID-Kollision verhindert |
| Frühere Sicherheitsbewertung aus Stichprobe | atomare Dateien, Vorsicherungen und Formattore vorhanden | konkrete Fehlergrenzen bei vollem Undo, UI-Ladefehler und verworfenem Flush-Ergebnis; kein pauschaler Integritätsschluss mehr |
| Bisherige Marktmatrix | Konto-/Offline-/Portabilitätsfragen relevant | z.B. Notion-Export ≠ Workspace-Restore, Joplin-Whiteboard als JSONCanvas, Sicherungs- und Austauschqualität getrennt; Quellen im Marktdokument |

## 7. Dokumentenpflege und Zuständigkeit

Alle aktiven Dokumente wurden nach Zweck/Verbindlichkeit, aktuellen Standangaben, Verweisen, Überschneidung und benötigter Belegfunktion eingeordnet; Inhaltsvertiefung erfolgte am jeweiligen Gegenstand, nicht durch Umbenennen des Datums. Der Bericht zu jedem aktiven Dokument folgt unten aus dem Inventar. Historische QA-JSONs und Originalaufträge bleiben unverändert.

**Zusammengeführt:** alte aktive Analyse-/Marktzwischenstände in ihren vorhandenen Dokumenten; überholte Statusaussagen im Plan; D51 und eindeutige Vorschlagskennungen aus Commit `7527e87` in die kanonische Dokumentstruktur, ohne Branchmerge. Die Originalquelle ist in Git weiterhin separat abrufbar. **Gelöscht in dieser Runde: keine Datei.** Die Inventur findet keine aktive OneDrive-Konfliktkopie und kein sicher entbehrliches zweites aktuelles Themendokument. Die einzige bytegleiche aktive Markdown-Paarung ist `LICENSE.md`/`packaging/paket/lizenzen/macos/Glide-Lizenzstatus.md`: die zweite Datei ist eine erforderliche Paketlizenzkopie und bleibt.

**Begründet erhalten:** sieben QA-/Archivversionen 3.39.0, 3.39.1, 3.40.0, 3.41.0, 3.42.0, 3.43.0, 3.43.1; QA-Bildgrenze betrifft nur die drei jüngsten Versionen, die lokale Metadatenprüfung findet keine abgelaufenen QA-Bilder. Format-/Migrationsfixtures, aktuelle Showcase-Originale, D45-Abnahmetafeln und die 28 Nutzerreferenzen sind andere Klassen. Separate Worktrees und zwei Stashes bleiben eigenständige Arbeitsstände. Der alte Affinity-Stand ist eine vorhandene binäre Quelle mit historisch blockiertem Löschversuch vom 15.10.; seine aktuelle Entfernung wird nicht durch einen anderen Mechanismus erzwungen. Die damals blockierten beiden `.pyc`-Dateien sind heute nicht mehr vorhanden. Der alte historische Bereinigungsbericht wird nicht nachträglich umgeschrieben.

Der frühere Bestandsprüfungsbericht vom 15.10. benennt in seiner `ergebnis.json` noch eine laufende Abschlussprüfung. Er ist kein aktueller grüner Abschlussbeleg; die jetzige Runde erzeugt ihren eigenen datierten Nachweis bei unveränderter App-Version. Ein kleiner Nachweisordner ist Prüfprovenienz und keine parallele Analyse oder Aufgabenliste.

| Aktives Dokument | Behandlung | Zweck / konkreter Abgleich |
|---|---|---|
| [CLAUDE.md](../CLAUDE.md) | aktualisiert | Agentenspezifischer Einstieg; D51/D52. Der zwischenzeitlich eingetragene Auftragsumfang vom 18.10. wurde in der Gegenprüfung wieder entfernt: Sitzungsstand gehört in die Übergabe, nicht in Regeldateien |
| [README.md](../README.md) | aktualisiert | Projektauftritt und Startwege; lokale Lieferung, Upstream und Release getrennt |
| [SECURITY.md](../SECURITY.md) | begründet beibehalten | Repository-Sicherheitsmeldungen; eigener Gegenstand gegenüber App-Schutzregeln |
| [.claude/skills/design-richtlinien/SKILL.md](../.claude/skills/design-richtlinien/SKILL.md) | begründet beibehalten | Aktiver neutraler Design-Einstieg; Regeln nur in Design Richtlinien |
| [.claude/skills/design-richtlinien/referenzen/bewegung-material-typografie.md](../.claude/skills/design-richtlinien/referenzen/bewegung-material-typografie.md) | begründet beibehalten | Fremdreferenz mit MIT-Lizenz, keine eigenständige Glide-Regel |
| [00_Arbeitsvorbereitung/Glide_Analyse.md](Glide_Analyse.md) | aktualisiert | Einzige aktuelle Analyse; Stand, Dokumentregister, Szenarien, Code und Abdeckung |
| [00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md](Glide_Entwicklungsplan.md) | aktualisiert | Einziger Backlog mit vollständigem Inventar, Paket- und Entscheidungsregister |
| [00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md](Glide_Manuelle_Pruefung.md) | begründet beibehalten | Offene echte Bedien-/Plattform-/Readerabnahmen; kein neuer Ergebniswert erfunden |
| [00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md](Glide_Markt_und_Vorbilder.md) | aktualisiert | Einzige aktuelle Wettbewerbsrecherche; historische Code-/Bildbezüge gekennzeichnet |
| [00_Arbeitsvorbereitung/Glide_Uebergabe.md](Glide_Uebergabe.md) | aktualisiert | Kompakter Einstieg und tatsächlicher Fortsetzungspunkt |
| [00_Arbeitsvorbereitung/README.md](README.md) | aktualisiert | Navigation zur aktuellen Analyse, Planung und Entscheidungen |
| [00_Arbeitsvorbereitung/Featurepaket_UI_UX/AUFTRAG.md](Featurepaket_UI_UX/AUFTRAG.md) | begründet beibehalten | Unveränderter Originalauftrag vom 15.10.; eigenständiger Eingangsbeleg |
| [00_Arbeitsvorbereitung/Featurepaket_UI_UX/BILDREFERENZEN.md](Featurepaket_UI_UX/BILDREFERENZEN.md) | begründet beibehalten | Zuordnung der 28 Originalbilder; Manifest frisch gehasht, Originale erhalten |
| [00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md](Featurepaket_UI_UX/PROMPT.md) | begründet beibehalten | Ausführbare Anforderungen/Referenzen des UI-/UX-Pakets; Status nur im Plan |
| [01_Repository/Glide/AGENTS.md](../01_Repository/Glide/AGENTS.md) | aktualisiert | Verbindliche Arbeitsregeln; D51. Die zwischenzeitlich eingetragene Auftragsgrenze vom 18.10. wurde in der Gegenprüfung wieder entfernt |
| [01_Repository/Glide/CHANGELOG.md](../01_Repository/Glide/CHANGELOG.md) | begründet beibehalten | Produktionsverlauf bleibt unverändert, da keine App-Änderung |
| [01_Repository/Glide/LICENSE.md](../01_Repository/Glide/LICENSE.md) | begründet beibehalten | Aktueller Projektlizenzstatus; keine neue Lizenz durch Analyse |
| [01_Repository/Glide/README.md](../01_Repository/Glide/README.md) | begründet beibehalten | Projektauftritt und Startwege; lokale Lieferung, Upstream und Release getrennt |
| [01_Repository/Glide/SECURITY.md](../01_Repository/Glide/SECURITY.md) | begründet beibehalten | Appbezogene Schutz-/Datenregeln; eigener Gegenstand gegenüber Repository-Meldeweg |
| [01_Repository/Glide/assets/README.md](../01_Repository/Glide/assets/README.md) | begründet beibehalten | Projektauftritt und Startwege; lokale Lieferung, Upstream und Release getrennt |
| [01_Repository/Glide/docs/00_INDEX.md](../01_Repository/Glide/docs/00_INDEX.md) | aktualisiert | Aktuelle Navigation, Zuständigkeiten, D51 und berichteter Prüfstand |
| [01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) | aktualisiert | Bestehende Grenzen; Hinweisschalter nach D50 präzisiert |
| [01_Repository/Glide/docs/02_ARCHITECTURE.md](../01_Repository/Glide/docs/02_ARCHITECTURE.md) | aktualisiert | Module, tatsächliche Start-/Mutationswege und belegte Fehlergrenzen |
| [01_Repository/Glide/docs/05_QA_TESTPLAN.md](../01_Repository/Glide/docs/05_QA_TESTPLAN.md) | aktualisiert | Prüfregeln nach D51; lokale 92 Suiten / 714 Units von historischen Zahlen getrennt |
| [01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) | aktualisiert | Datenvertrag und aktuelle tatsächliche Fehlergrenzen; Formate nicht geändert |
| [01_Repository/Glide/docs/07_QA_BERICHT.md](../01_Repository/Glide/docs/07_QA_BERICHT.md) | aktualisiert | Einziger Ergebnisbericht; neue Proben, roter Vorlauf, abschließende Prüfungen getrennt |
| [01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) | aktualisiert | Aktueller lesender GitHub-Abgleich; historische Tabelle und offene Release-Tore erhalten |
| [01_Repository/Glide/docs/20_FUNKTIONEN.md](../01_Repository/Glide/docs/20_FUNKTIONEN.md) | aktualisiert | Verhaltensvertrag mit ausgewiesenen aktuellen Fehlerabweichungen |
| [01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md](../01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) | begründet beibehalten | Eigenständige Praxisbeispiele; kein neuer Vorlagen-/Datenauftrag |
| [01_Repository/Glide/docs/ARBEITSRICHTUNG.md](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) | aktualisiert | D51 aus getrenntem Quellstand konsolidiert, Empfehlungen nicht beschlossen |
| [01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) | begründet beibehalten | Zentrale Gestaltungsvorgaben; kein neuer Gestaltungsbeschluss |
| [01_Repository/Glide/docs/DOKUMENTENPFLEGE.md](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) | aktualisiert | Zuständigkeit und Aufbewahrung; Originale/Fixtures/Lieferkopien unterscheiden |
| [01_Repository/Glide/docs/decisions/ABHAENGIGKEIT_TKDND.md](../01_Repository/Glide/docs/decisions/ABHAENGIGKEIT_TKDND.md) | begründet beibehalten | Entschiedene Ausnahme; Herkunft 116Dateien neu gegen Original geprüft |
| [01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md](../01_Repository/Glide/docs/decisions/ARBEITSBEGLEITER.md) | aktualisiert | Aktuelle B03-Kachelregel statt entfallenem Spielereien-Schalter |
| [01_Repository/Glide/docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md](../01_Repository/Glide/docs/decisions/GRUPPE_ORDNER_UEBERSCHRIFT.md) | begründet beibehalten | Eigenständige Strukturbegriffe/Entscheidung; keine Umwandlung beauftragt |
| [01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md) | begründet beibehalten | Identitäts- und Grenzwerte; offene Inhaberwerte bleiben offen |
| [01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md) | begründet beibehalten | Eigener Betriebsvertrag; Zustellung bei geschlossener App nicht gewählt |
| [01_Repository/Glide/packaging/README.md](../01_Repository/Glide/packaging/README.md) | aktualisiert | Paketbau/Startwege; heutige unvollständige Mac-Kopie präzisiert |
| [01_Repository/Glide/packaging/paket/lizenzen/macos/Glide-Lizenzstatus.md](../01_Repository/Glide/packaging/paket/lizenzen/macos/Glide-Lizenzstatus.md) | begründet beibehalten | Erforderliche bytegleiche Mac-Paketlizenzkopie, keine entbehrliche Themendublette |
| [01_Repository/Glide/packaging/runtime/README.md](../01_Repository/Glide/packaging/runtime/README.md) | aktualisiert | Runtimeherkunft und P8-Vorbereitung; historische und lokale Suitezahlen getrennt |
| [01_Repository/Glide/scripts/pflege/README.md](../01_Repository/Glide/scripts/pflege/README.md) | begründet beibehalten | Projektauftritt und Startwege; lokale Lieferung, Upstream und Release getrennt |
| [01_Repository/Glide/src/glide/README.md](../01_Repository/Glide/src/glide/README.md) | begründet beibehalten | Modulübersicht des lokalen Lieferstands; kein Upstream-Modul hineinerfunden |
| [01_Repository/Glide/tests/README.md](../01_Repository/Glide/tests/README.md) | aktualisiert | Lokale 92Suiten/Format 25 korrigiert; Ausführungsregeln referenzierenQA |
| [01_Repository/Glide/tests/tools/README.md](../01_Repository/Glide/tests/tools/README.md) | begründet beibehalten | Werkzeugzuständigkeiten und Isolation; aktuelle Ergebnisse ausschließlich inQA |
| [05_Probelisten_Testdaten/README.md](../05_Probelisten_Testdaten/README.md) | begründet beibehalten | Showcase-/Testdatenanleitung; sechs Lieferkopien bytegleich, keine Bearbeitung echter Daten |
| [05_Probelisten_Testdaten/Showcase/README.md](../05_Probelisten_Testdaten/Showcase/README.md) | begründet beibehalten | Showcase-/Testdatenanleitung; sechs Lieferkopien bytegleich, keine Bearbeitung echter Daten |
| [07_Python-Versionen/README.md](../07_Python-Versionen/README.md) | begründet beibehalten | Startbare Lieferung und Modulaufzählung stimmen; Lieferdokument unverändert erhalten |
| [20_Grafik_Master/README.md](../20_Grafik_Master/README.md) | begründet beibehalten | Master-/Laufzeitkopien und D45-Herkunft; alte binäre Quelle mit historischem Löschblock erhalten |

## 8. Bestandsaufnahme und Gap-Analyse (13.10.2026)

Dieser Anker bleibt für bestehende Verweise erhalten. Die damalige Baseline war `c38d960`, 3.39.0/Format 23, Apphash `7995ecbc…`; die frühere Ausarbeitung liegt in Git. Ihre aktuelle Fortschreibung steht in §§1–7 und §9–§11.

### 8.1 Funktionsinventar

Das aktuelle zweiachsige Gesamtregister liegt ausschließlich im [Entwicklungsplan §18](Glide_Entwicklungsplan.md#18-konsolidiertes-funktions--und-aufgabeninventar); die Einordnung nach Nutzerabläufen oben in §2. Die einst offenen G17/G21/G26 sind inzwischen im gewählten Rahmen geliefert. FP-01 ist inzwischen upstream implementiert und gezielt geprüft, lokal aber nicht geliefert. Eine historische „nicht vorhanden“-Zelle darf weder diesen Kandidaten noch die weiterhin fehlende lokale Lieferung verdecken.

### 8.2 Technische Einschränkungen

JSON-Hauptspeicher, komprimierte Vollschnappschüsse, zentraler Tk-Adapter und verschachtelte Einstellungen bleiben relevante Grenzen; die aktuellen Belege und Alternativen stehen in §11. Historische Performancewerte und Dateizeilen aus 3.39.0 werden nicht als heutige Messung fortgeschrieben.

### 8.3 Gap-Analyse

Die fachliche Lücke besteht überwiegend in erweiterten Rhythmen, Ansichten, Wissenskontext und offenen Ausgaben (FP-02–FP-07). Vor diesen Erweiterungen liegen bestätigte Schutzfehler und getrennte Liefer-/Abnahmetore. „Aufgaben im Wissen mit Original-ID“ ist ein vorhandener Zusammenhang; seine bessere persönliche Eignung gegenüber anderen Produkten bleibt eine Hypothese für einen Vergleich anhand derselben Szenarien.

## 9. Gesamtanalyse vom 18.10.2026

### 9.1 Arbeitsstruktur und belegte Stände

Die zu Beginn angelegte Arbeitsstruktur wurde in getrennten Strängen ausgeführt: Root für Bestands-/Liefer-/Dokumentabgleich, Markt für aktuelle Primärquellen, Planung für Kennungen/Pakete/Entscheidungen, Code für vollständige Modulübersicht und kritische Datenflüsse. Schreibzuständigkeiten waren getrennt; Integration und zweiter Abgleich werden anschließend gemeinsam abgeschlossen. Abhängigkeit: tatsächlicher Stand → Funktionslücken/Code → Szenarien/Markt → Pakete/Entscheidungen → Dokument-/Abschlussprüfungen.

| Stand | Identität und tatsächlicher Inhalt | Prüfung | Lieferung / Konsequenz |
|---|---|---|---|
| Lokaler Quellbaum | `c0252ba`, `VERSION=APP_VERSION=3.43.1`, Format 25, App-SHA `ed2b7eb6…`; 66 Begleitdateien | aktueller Grundstufenlauf plus Fehlerproben; historische Gesamtmatrix bei `eb5658c` separat | 67 Code- und 146 Ressourcendateien in `07_Python-Versionen` sowie sechs Showcase-Dateien neu als bytegleich bestätigt. Kein FP-01 im lokalen Baum |
| `origin/main` | live `9ec474b9dcbd502efce8cb221e53e24c322f9a78`, Nachfahre von lokal, sechs zusätzliche Commits; ebenfalls Versionsstring 3.43.1 | enthält Werkzeugnachlauf PR #35 und FP-01-Kandidat PR #36; Belege zum Kandidaten im Plan; abschließend Lauf 39075284901 grün: Grundstufe, Linux-/Windows-Vollprüfung mit eigener Tk 9.1 und Windows-Paketjob; spezielle Readerjobs ausgelassen | kein Versionswechsel/07-Abgleich dieses FP-01-Kandidaten belegt. Keine Übernahme in dieser Runde. Gegenprobe am selben Tag: A33 dort behoben, A32/A34/A35/A27 unverändert ([§11.4](#114-neue-konkrete-befunde-und-gegenprüfungen)) |
| Lokaler `main` | `eb5658c`, frühere native Linux-/Windows-Gesamtmatrix grün | historischer [Lauf 38979558948](https://github.com/n05a-design/glide-to-do/actions/runs/38979558948) | kein Beleg für beliebige neuere Kandidaten desselben Versionsstrings |
| Planungszweig `claude/ausbauprogramm-phasen` | `19c7df5`, darin Commit `7527e87`: D51, E-P1–E-P5, WA-19–WA-25, TK9-RAD und PS-01/PS-02 | Dokumentplanung, keine neue App-Version; gültiger Wortlaut D51 separat rekonstruiert | eindeutige Inhalte kanonisch konsolidiert; Vorschlagsfolge bleibt offen |
| Separater FP-01-Arbeitsstand | `4c15d71` auf `claude/fp01-wiederholen`, Worktree `glide-weiterarbeiten-618cb4` | gezielte Suite 9/9, Gegenprobe 9/9 rot, zusätzliche Units und betroffene Suiten; genaue Grenzen im Plan | implementierter Kandidat, kein lokaler Lieferabschluss |
| P8-/4.0-Vorbereitung | additive Adapter bereits im lokalen 3.43.1-Baum; zugehörige Runtime-/Readerproben unter QA 3.42.0 | historische native Vorläufe; vollständige Reader-/Menschen-/4.0-Abnahme offen | keine eigene gelieferte 4.0.0. Nicht als exklusiver Inhalt eines beliebigen anderen Worktrees bezeichnen |
| Windows-Paket | `build/windows/Glide-3.42.0`, Version 3.42.0 | 102/102 Manifestdateien heute hashgleich; heutiger Paketstart nicht ausgeführt | unsigniertes Entwicklungsartefakt; enthält keine 3.43.x- oder FP-01-Lieferung |
| Mac-Bundle | `build/macos/Glide.app`, historische 3.42.0-Lieferung | 327/330 heutige Manifestdateien vorhanden und hashgleich; es fehlen drei Dateien in `Python.framework/Versions/3.14`: das Python-Programm selbst, dessen `Resources/Info.plist` und `_CodeSignature/CodeResources` – ohne das Programm ist diese Kopie nicht startfähig | lokale Kopie unvollständig; vor Mac-Lieferung nativer Neubau/Reparatur, Start und Signaturprüfung |
| Öffentlicher Release | GitHub-Releases bei lesender API-Abfrage leer; `git ls-remote --tags origin` ohne Eintrag | keine Veröffentlichung oder Signatur durch diese Runde | D43/I-Tore offen. Sichtbarer Repository-Code ist keine freigegebene Endnutzerveröffentlichung |

Vollständige Hashes, Refstände und Manifestabweichungen: [Ausgangsstand](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/ausgangsstand.json). Aktuelle Prüfungen und Grenzen: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Eine Versionsnummer oder Dateizeit ist hier ausdrücklich kein hinreichender Gleichheitsbeleg. Keine Commits, Pushes, Merges, Checkouts, Installationen oder Veröffentlichungen wurden ausgeführt.

### 9.2 Betriebs- und Datenfolgen

Die wesentlichen Risiken liegen an Transaktionsgrenzen: vor einer Strukturänderung muss ein konkret adressierbarer Wiederherstellungsstand existieren; ein UI-Fehler nach erfolgreichem JSON-Lesen ist kein defekter Datensatz; ein fehlgeschlagener Editorflush muss den anschließenden Import/Restore stoppen. Atomare Dateiumbenennung schützt nur gegen teilweise geschriebene Bytes, nicht gegen fachlich leeren oder falschen Inhalt. Ebenso ersetzt eine vorhandene Sicherung nicht eine korrekte Erfolgsmeldung und verhindert nicht jeden Verlust jüngster Änderungen.

A32/A34/A35 sind mit abgegrenzten künstlichen Proben beziehungsweise direktem Caller-/Rückgabefluss belegt. Ihre natürliche Auslöserhäufigkeit, vollständige UI-Fehlerkette und tatsächlicher produktiver Datenverlust wurden nicht gemessen. Das genügt für prioritäre Schutzkorrekturen mit Gegenproben; es genügt nicht für eine Behauptung, echte Bestände seien beschädigt. Echte Daten wurden nicht geöffnet.

## 10. Nutzungsszenarien und Bereichsübergänge

Die folgenden Abläufe sind aus Code, Verträgen und Aufträgen hergeleitet, soweit keine konkrete Probe genannt wird. Konkurrenzabläufe sind offiziell dokumentiert und wurden in dieser Runde nicht selbst bedient. Primärquellen und Varianten stehen im [Marktdokument](Glide_Markt_und_Vorbilder.md); Kennungen und Paketdetails ausschließlich im Plan. Wo eine Aktion speichert, muss der Erfolg über die echten UI- und Mutationseinstiege sowie anschließendes Neuladen und Rückgängigmachen geprüft werden. Die folgenden Kriterien beschreiben diese künftige Abnahme; sie sind keine Behauptung, dass alle Szenarien in dieser Runde praktisch ausgeführt wurden.

| ID / Ausgangslage und Ziel | Heute in Glide / Reibung | Verbesserung, Konkurrenzbezug und Voraussetzung | Nachteil / überprüfbares Erfolgskriterium |
|---|---|---|---|
| S01 Gedanken schnell erfassen und später einordnen | Eingang, Mehrzeileneingabe und Feldchips sind vorhanden; nicht abbildbare Serien bleiben Text. Beim Verschieben vom Eingang ins Projekt müssen die Kennungen erhalten bleiben. | Vorhandene Eingabe, erklärtes Verschieben und zuletzt benutzte Ziele konsequent verwenden. Todoist und Things dienen als Vergleich für den Erfassungsablauf; ein zusätzlicher Eingang ist unnötig. | Mehr Parserintelligenz erhöht das Risiko einer Fehlzuordnung. Test: zehn gemischte Zeilen, keine unbeabsichtigten Termine, jede Aufgabe genau einmal; Verschieben, Undo und Neuladen prüfen. |
| S02 Den Tag realistisch planen | Heute führt über Tagesbeginn und Vorschlag zu Kapazität und Raster; eine lokale ICS-Datei kann externe Belegzeiten zeigen. | Gemeinsame Kapazitäts- und Vorschlagsbasis bewahren. Super Productivity und Sunsama dienen als Vergleich für Planung und Reflexion. Vor dem Wochenritual WA-20 den vorhandenen Tagesabschluss wiederverwenden. | Zusätzliche Rituale können Pflege erzwingen. Test: Bei festen Aufgaben und Belegzeiten ist die Restzeit in Vorschlag, Kopf und Entlastungsdialog identisch; Überspringen verändert keine Daten. |
| S03 Fälligkeit, Bearbeitungstag und freie Zeit unterscheiden | Getrennte Felder und direkte Bearbeitungswege sind vorhanden; unterschiedliche Kalenderrollen können Erwartungen vermischen. | FP-02 und FP-03 müssen Bearbeitung, Frist und Belegzeit getrennt erklären. Things mit Startdatum/Deadline und Taskwarriors Datumsrollen liefern Vergleichsmuster. | Mehr Felder können überfordern. Test: Einplanen ändert nur `planned_date` und die zugehörige Planungszeit; die Frist bleibt erhalten. Eine Friständerung verändert keine Belegdatei. Jede Aktion bildet einen Undo-Schritt. |
| S04 Liegen gebliebene Aufgaben neu einplanen | Hinweise auf Überfälliges, Einplanen und „Tag entlasten“ mit Mehrfachvorschau sind vorhanden; andere Fundorte können noch den alten Kontext zeigen. | Die Vorschau nennt Ziele, Kapazität und Ursprung. WA-21 kann Fundorte zeigen, ohne eine zweite Aufgabe anzulegen. Todoist und Planify dienen als Vergleich für bewusstes Aufschieben. | Automatische Vorschläge können verbindlich wirken. Test: Alt und Neu werden vollständig gezeigt; Abbruch schreibt nichts, überlastete Zieltage bleiben sichtbar und die Fälligkeit ändert sich nicht unbemerkt. |
| S05 Wiederkehrende Verpflichtungen verlässlich führen | Sechs Regelarten, Überspringen und Monatsendregeln sind vorhanden; komplexere Rhythmen und Einzelausnahmen fehlen. | FP-02 gemeinsam mit WA-23/WA-24 und gegebenenfalls WA-14 betrachten. Todoist, Things und Super Productivity unterscheiden Kalenderanker und Wiederholung ab Erledigung. Gemeinsame Semantik, Formattor und Altleserprüfung sind nötig. | Serienhistorie und Ausnahmen vergrößern das Modell. Test: Monatsende, 29. Februar, Sommerzeitwechsel, n-ter Wochentag, Zweiwochenrhythmus, Ausnahme, Pause/Fortsetzen, Erledigung und ICS-Rundlauf ergeben den vereinbarten Verlauf. |
| S06 Eine Aufgabe aus Seite oder Notiz bearbeiten | Heimat- und Verweiszeile, Inspektor und Live-Liste verwenden die echte Aufgabenkennung; vorgelagert muss der Text gespeichert werden. | Zuerst A35 schließen, danach vorhandene Verweise und Inspektor verbessern. Notions Aufgaben im Seitenkontext und Joplins Notizaufgaben liefern unterschiedliche Vergleichsmodelle. | Lokale Editorhistorie und globales Undo brauchen klare Zuständigkeiten. Test: Titel und Status stimmen in Seite und Liste überein; das Löschen eines Verweises entfernt keine Heimataufgabe, und ein Schreibfehler stoppt die Folgeaktion. |
| S07 Informationen wiederfinden und sinnvoll verknüpfen | Globale Suche, markierte Trefferstellen und Rückverweise sind vorhanden; unverknüpfte Erwähnungen werden nicht angeboten. | FP-05 mit lokalen Kandidaten und ausdrücklich bestätigter Verknüpfung; Obsidian und Joplin als Vergleich. Fehlende oder archivierte Ziele und doppelte Titel berücksichtigen. | Falsche Treffer und Kosten proportional zu Bestand und Titelzahl sind möglich. Test: kein automatischer Link, eindeutiges Vorschauziel; Umbenennen, Undo und Archivieren verwerfen veraltete Kandidaten. Mit großem Bestand messen. |
| S08 Zwischen Liste, Heute, Kalender, Seite und Pinnwand wechseln | Ansichten zeigen dieselbe Aufgabe, verwenden aber einen zentralen Host; gespeicherte Ansichten sind begrenzt. | FP-03 speichert Filter und Darstellung, FP-04 ergänzt Dokumentkarten. E-U2 sollte zunächst lesenden Kontext bieten. AFFiNE, Obsidian und Vikunja zeigen unterschiedliche Ansichtsmodelle. | Unklarer Fokus, falscher Undo-Stapel oder veraltete Objekte sind Risiken. Test: stabile Kennung, getrennte Scrollposition und aktueller Status; kein verlorener Editorinhalt, eindeutiges Verhalten beim Schließen und Aktivwechsel. |
| S09 Einen großen Bestand übersichtlich halten | Filter, Gruppierung, Suche, Archiv und einklappbare Bereiche sind vorhanden; ältere Messungen gelten für bestimmte Mengen und Ansichten. | FP-03 erweitert Bedingungen um Bearbeitungstag, Aufwand und Ausschlüsse sowie die gespeicherte Darstellung. Große Kartenbestände zusätzlich messen. Kein FTS5 ohne aktuellen Engpass. | Komplexe Filter werden schwer erklärbar. Test: Ergebnis und Erklärung stimmen überein; Verschachtelung und Archiv werden richtig behandelt. 1.000 und 10.000 Punkte sowie viele tatsächlich gezeichnete Karten getrennt prüfen. |
| S10 Ausschließlich mit Tastatur arbeiten | Palette, Menüs, Kontextaktionen und Treeview-Wege sind vorhanden; Tk 9.1 löste zusätzlich unerwünschte Emacs-Navigation aus. | Die Korrektur aus 3.43.1 bewahren. Neue Kompakt-, Block- und Nebenansichten über Tastatur und semantische Anbindung anbieten, nicht nur beim Überfahren mit der Maus. Things und Obsidian dienen als dokumentierte Referenzen. | Kürzelkonflikte und falscher Editorfokus sind Risiken. Test: Erfassen, Einplanen, Seitenwechsel und Undo vollständig ohne Maus; Kopieren/Einfügen bleibt im Text, und Dialogabbruch stellt den ursprünglichen Fokus wieder her. |
| S11 Fehler verstehen und rückgängig machen | Globales Undo mit 20 Schritten, lokale Editorhistorien und Sicherungen sind vorhanden; A32–A35 zeigen Grenzen der Schutzwirkung. A33 betrifft die Erfolgsmeldung. | Schutzkorrekturen vor dem Ausbau; den FP-01-Kandidaten kontrolliert abschließen. Redo-Konventionen nur für konkret nachgewiesene Vergleichsprodukte anführen. | Vollschnappschüsse kosten Speicher; Undo ersetzt kein Backup. Test: Stapellängen 0/19/20, fehlgeschlagenes Speichern, Guardfehler, neue Mutation nach Undo und Fokusziel. Die Meldung muss dem persistierten Zustand entsprechen. |
| S12 Sichern, wiederherstellen und austauschen | Aufgaben- und App-Backups, Vergleich, Seitenwiederherstellung und offene Einzelexporte sind vorhanden; Pinnwandlayout liegt in den Einstellungen. | FP-07 ergänzt einen offenen Dateibaum mit Manifest und Verlustbericht; WA-22 klärt den Sicherungsumfang. Notion, Heptabase und Joplin zeigen Unterschiede zwischen Austausch und Wiederherstellung. | Mehr Ausgabewege können irreführen. Test: dokumentierte Objekt-, Anhangs- und Verweiszahlen, Dateinamenkollisionen, Unicode und fehlende Dateien; unabhängige Lesbarkeit. Vollständigen Restore nur für das dafür vorgesehene Format verlangen. |
| S13 Externe KI-Ergebnisse kontrolliert übernehmen | Kontextpaket, Prüfsummen, Feldvergleich, Konflikt- und Ungültigstatus sowie Vorschlagsbackup sind vorhanden. | FP-06 verwendet das vorhandene Feld `instructions` und wiederverwendbare Aufträge; kein Endpunkt. Auch eine böswillige oder fehlerhafte Antwort bleibt Eingabe, keine Anweisung. | Nutzer geben gewählte private Inhalte bewusst an ein externes Werkzeug weiter; der Bedienweg muss den Umfang zeigen. Test: falsche Version oder Kennung, geänderte Basis, Duplikate, teilweise ungültige Antwort und Abbruch; bestätigte Übernahme als ein Undo-Schritt. |
| S14 In kleinem Fenster oder mit großer Schrift arbeiten | Mindestgröße 860 × 700, responsiver Inspektor, ausgeblendete Metadaten und Buttonschutz aus B15 sind vorhanden. | E-U1 als eigener reduzierter Modus statt allgemeiner Mindestgrößensenkung; Microsoft To Do als Referenz. Getrennte Fenstergrößen speichern, Tastaturzugang und Palette bewahren. | Ein Speziallayout vergrößert die Zahl der Prüfkombinationen. Test: Zielgröße erst nach Probe festlegen; große Schrift und DPI, alle Aktionen erreichbar, keine abgeschnittenen Inhalte oder unerreichbaren Menüs. Rückkehr zum Normalmodus ohne Verlust. |
| S15 Kreative Inhalte mit Aufgaben und Wissen verbinden | Zeichnungen dienen als Symbole, Titelbilder und Pinnwandkarten; Bildfolgen sind seit 3.40.0 vorhanden. | Die vorhandene Werkstatt als Inhaltsquelle vertiefen. Aseprite und Pixelorama dienen als Vergleich für Frame- und Exportsemantik, nicht als Auftrag für eine vollständige Werkzeugkopie. | Ebenen, GIF und allgemeines Fremd-SVG wären neue Ziele. Test: Zeichnung als Symbol und Seiteninhalt bis ins Backup verfolgen, Bildfolge nach Export und Undo erhalten; statische Vorschau klar kennzeichnen. Kalte Bildkonversion A31 gesondert prüfen. |
| S16 Einen Notion-Bestand kontrolliert übernehmen und aktualisieren | ZIP mit Markdown/CSV, Vorschau, Verlustbericht, Quellenmetadaten und Wiedererkennung; Unterseiten werden in Ordner und Seiten überführt. | Die bestehende Quelle vor weiteren Importquellen nach WA-19 vertiefen. Gleichzeitig geänderte lokale und externe Seiten ausdrücklich als Konflikt zeigen. | Ein Export bildet Notion nicht verlustfrei ab. Test: unveränderter Wiederimport erzeugt keine Dubletten; verschobene Quelle, doppelte Kennungen, fehlender Anhang, lokale Änderung, Abbruch und Wiederherstellung prüfen. |
| S17 Zugänglich arbeiten | Semantikadapter und Runtimevorbereitung sind vorhanden; vollständige Readerabläufe sind nicht abgenommen. | Paket 8 mit VoiceOver, NVDA und Orca am tatsächlichen Lieferstand prüfen. Rolle, Name, Wert, Aktion und Lebensdauer gemeinsam behandeln. | Ein eigener Runtimepatchsatz erzeugt dauerhafte Pflegekosten. Test: tatsächliche Readerausgabe und externer Fokus, entfernte Widgets, Unicode und Textcursor; kein nativer Absturz. Vorhandene Attribute allein genügen nicht. |
| S18 Auf einem anderen Rechner denselben Stand starten | Python-Fassung 3.43.1, eigenständige Pakete 3.42.0 und FP-01-Kandidat auf Upstream unterscheiden sich; die Mac-Kopie ist unvollständig. | Gemeinsame Lieferidentität, Hashmanifest und kurze Angabe des Startwegs; Veröffentlichungstore getrennt behandeln. | Mehr Artefakte erhöhen das Risiko auseinanderlaufender Stände. Test: alle gewählten Startwege zeigen denselben vereinbarten Funktionsumfang; native Starts ohne Rückgriff auf externe Quellen prüfen. Abweichungen sichtbar nennen, statt Gleichheit aus Versionsnummern abzuleiten. |

## 11. Systematische Codeanalyse

### 11.1 Geltungsbereich und Belegstärke

Die Untersuchung bezieht sich auf die unveränderte lokale Produktionslogik von `claude/tag3390-sichtbarkeit`, Commit `c0252ba`, Glide 3.43.1/Format 25. Die inzwischen vorausliegende Remote-Fassung `origin/main` (`9ec474b`) wurde zusätzlich lesend auf FP-01 geprüft; ihre Implementierung und Testdateien sind keine lokale Auslieferung. Maßgeblich für die Beziehung der Arbeitsstände bleibt §9.

Alle 67 eigenen Laufzeitdateien direkt unter `src/glide` wurden strukturell erfasst: Imports, Klassen, Funktionen, Zuständigkeiten und vorhandene Prüfwege. Der getrennte `drawing_prototype.pyw` wurde ausdrücklich ausgeschlossen. Fremdcode unter `vendor` wurde nicht als eigener Produktionscode gezählt. 62 Dateien enthalten keinen eigenen `tkinter`-Import; dieser syntaktische Befund beweist keine vollständige Seiteneffektfreiheit. `runtime_check` importiert Tk nur zum Anzeigen einer Fehlermeldung. P8-Adapter sind bereits im 3.43.1-Quellbaum vorhanden; daraus folgt keine vollständige native Readerabnahme.

`app.pyw` hat 61.256 Zeilen und 41 Klassen; `ListApp` umfasst davon 46.929 Zeilen mit 1.634 direkten Methoden. Diese Größen erklären, warum Daten-, Ansichts- und Fehlerwege schwer gemeinsam zu ändern sind. Sie belegen keinen Performanceengpass. Die vertieften Aufrufprüfungen und gezielten Proben unten liefern die fachlich belastbaren Gründe für Änderungen.

**Untersuchungstiefe:** S = Struktur/Zuständigkeit/Prüfzuordnung; V = zusätzlich kritische Funktionen mit Aufrufern/Gegenwegen vertieft. V bedeutet keine vollständige Zeilen-, Plattform- oder Zweigabdeckung. Das zugehörige JSON-Modulinventar hält vorhandene Unit-Namensbezüge fest; diese belegen keinen neuen Testlauf. Tk-nahe Bild-/Logo-/Hintergrundmodule werden vor allem über bestehende Integrationssuiten geprüft.

### 11.2 Abdeckungsregister aller eigenen Laufzeitmodule

Alle nachfolgenden Dateien liegen unter [src/glide](../01_Repository/Glide/src/glide); Unit-Prüfquellen unter [tests/unit](../01_Repository/Glide/tests/unit). Zeilenzahlen stammen aus dem selben AST-Inventar.

| Modul | Rolle | Zeilen | Eigener Tk-Import | Tiefe |
|---|---|---:|---|---|
| `accessibility.py` | Attribute und deutsche Aufgabenwerte (P8-Vorbereitung) | 117 | nein | S |
| `accessibility_bindings.py` | Semantikbindung. Meldungsbündelung und Lebensdauer | 95 | nein | S |
| `action_catalog.py` | Aktionskennungen und Editorbefehle | 281 | nein | S |
| `animation.py` | Frame-IDs. Dauern. Wiedergabe. PNG-Ausgaben | 329 | nein | V |
| `animation_export.py` | Mehrdateiausgabe mit rückrollbarem Austausch | 82 | nein | V |
| `app.pyw` | Tk-Oberfläche. Datenadapter. Mutation. Import/Export. Start | 61.256 | ja | V |
| `appearance.py` | Systemmodus und Hell-/Dunkelpaar | 80 | nein | S |
| `attachment_paths.py` | Portable flache Anhangspfade und Kollisionsschlüssel | 29 | nein | S |
| `backdrop.py` | Hintergrundgeometrie und PNG-Daten | 455 | nein | S |
| `backup_diff.py` | Lesender Vergleich zweier Datenstände | 116 | nein | S |
| `backup_snapshot.py` | Eingefrorene Sicherungsbytes und Anhangsauswahl | 127 | nein | V |
| `busy_calendar.py` | Begrenztes Lesen der Kalenderquelle und Jahresfenster | 166 | nein | V |
| `calendar_service.py` | Worker. Quellgeneration und Ergebnisübernahme | 181 | nein | V |
| `capture_parser.py` | Deutsche Schnelleingabe einschließlich Wiederholungsanker | 730 | nein | S |
| `content_search.py` | Normalisierung. Rang. Ausschnitt und Fundstellen | 118 | nein | V |
| `core_accessibility.py` | Adapter für Aufgaben-Kernablauf und Inspektorfokus | 393 | nein | S |
| `daily_hints.py` | Fällige Tageshinweise und persistente Zustellbelege | 227 | nein | V |
| `day_proposal.py` | Erklärbare Tagesauswahl und Budget | 71 | nein | S |
| `day_relief.py` | Umplanungsvorschau. Bilanz und Konfliktprüfung | 129 | nein | V |
| `drawing.py` | Zellmodell. Aktionspuffer. Paletten und Rasterausgabe | 1.445 | nein | V |
| `drawing_image.py` | Tk-Bilder. Referenzaufbereitung und Miniaturen | 310 | ja | S |
| `eisenhower.py` | Quadranten und Ablegeänderung | 81 | nein | S |
| `exchange_patch.py` | Kontextpaket. Feldprüfung und Änderungskonflikte | 210 | nein | S |
| `filter_explain.py` | Filterbedingungen und verständliche Gründe | 110 | nein | S |
| `focus_timer.py` | Pause. verstrichene Zeit und Buchungsjournal | 89 | nein | V |
| `glide_start.py` | Launcher und Bytecode-Cache | 63 | nein | V |
| `glyph_metrics.py` | Optische Symbolmitte aus TrueType-Glyphen | 177 | nein | S |
| `home_tiles.py` | Kachelkatalog und normalisierte Auswahl | 161 | nein | S |
| `ics_busy.py` | ICS-Belegzeiten. Ausnahmen und Verlustmeldungen | 345 | nein | S |
| `ics_recurrence.py` | Begrenzte RRULE-Teilmenge und Expansion | 239 | nein | S |
| `ics_timezone.py` | VTIMEZONE und Sommerzeitübergänge | 177 | nein | V |
| `image_preview.py` | Plattformlader. Konversion und Bildcache | 337 | ja | V |
| `interaction_policy.py` | Palettensuche. Hinweise. Datenanzeige und X11-Regeln | 135 | nein | S |
| `logo.py` | Tk-Logo und App-Symbol | 185 | ja | S |
| `logo_raster.py` | Transparente. geglättete PNG-Raster | 86 | nein | S |
| `motion.py` | Unterbrechbare Übergänge und Abbau | 78 | nein | V |
| `notion_archive.py` | Begrenztes ZIP-Lesen. Quellenkennungen. Verluste | 349 | nein | V |
| `notion_hierarchy.py` | Unterseiten und bestehende Zielordner planen | 112 | nein | V |
| `notion_import.py` | Ausgewählte Inhalte mit Fabriken vorbereiten | 242 | nein | S |
| `notion_reimport.py` | Quell-/Lokaländerungen und Konfliktauswahl | 131 | nein | V |
| `object_references.py` | Typisierte Verweise. Graph und Remapping | 126 | nein | V |
| `occupied_time.py` | Intervallvereinigung und lokale Tagesprojektion | 198 | nein | S |
| `page_features.py` | Live-Listen. Titelbilder und Vorlagenvorschau | 130 | nein | S |
| `page_markdown.py` | Markdown-/Seitendokument-/Druckabbildung | 613 | nein | V |
| `page_restore.py` | Selektiver Restoreplan mit ID- und Referenzschutz | 245 | nein | V |
| `planning.py` | Bearbeitungstag. Kapazität und Zeitzuweisung | 120 | nein | V |
| `preview_tools.py` | Linux-Konverterauswahl und JPEG-Abmessungen | 77 | nein | S |
| `release_notes.py` | Katalog und einmalige Neuigkeitenkarte | 136 | nein | S |
| `render_retention.py` | Hostgebundene Widgets. Vergleich und Bindungen | 137 | nein | V |
| `repeat_ics.py` | Klemmsemantik zwischen Glide und RRULE | 114 | nein | V |
| `repeat_rules.py` | Sechs alte Regeln und Überspringen | 204 | nein | V |
| `restore_assets.py` | Exklusive Anhangsdateien. Rückbau und Übernahme | 120 | nein | V |
| `routines.py` | Routinenauswahl und Tagesfortschritt | 115 | nein | S |
| `runtime_check.py` | Mindestlaufzeit; Tk nur für Fehlermeldung | 63 | nur Fehlermeldung | V |
| `save_comparison.py` | Verlauf. Teilbaumhashes und Teilvergleich | 156 | nein | V |
| `schema_backups.py` | Formatstand und bytegenaue Vorsicherung | 61 | nein | V |
| `sidebar_policy.py` | Arten-/Bereichsgrenzen und Vorlagenzuordnung | 119 | nein | S |
| `source_metadata.py` | Quellzuordnung über Kopie. Restore und Dateiumzug | 241 | nein | V |
| `svg_geometry.py` | SVG-Geometrie und Farben | 226 | nein | S |
| `symbol_policy.py` | Schriftabdeckung und Text-Rückfälle | 91 | nein | S |
| `task_editing.py` | Dreiwegevergleich des Inspektor-Feldvertrags | 65 | nein | V |
| `task_references.py` | Heimat. Textquellen. Titel und ID-Remapping | 128 | nein | V |
| `timezones.py` | Gebündelte IANA-Daten und Windows-Zuordnung | 109 | nein | V |
| `today_view.py` | Heute-Abschnitte und nächste Aufgabe | 113 | nein | V |
| `ui_design.py` | Gemeinsame Abstände. Größen und Breiten | 47 | nein | S |
| `view_metrics.py` | Kennzahlen und begrenzte Datumsnormalisierung | 80 | nein | S |
| `week_planning.py` | Wochenbilanz und freie Zeitfenster | 57 | nein | S |

**Weitere eigene Liefer-/Prüfpfade:** `packaging/paket/package_sources.py` wurde auf reale Quellerfassung und Plattformauswahl gelesen, `compiled_contract.py` auf Vergleich kompilierter Codeobjekte einschließlich verschachtelter Funktionen. `glide_start` und `runtime_check` wurden mit ihren direkten Starteinstiegen abgeglichen. Python-Abgleich, Standprüfung, native Laufzeit, Bundle-/EXE-Proben und deren tatsächliche Ergebnisse stehen im QA-/Lieferabgleich; diese statische Durchsicht ersetzt keinen Paketbau. Der bestehende Zeichenprototyp ist weder Appmodul noch Lieferbestand. Ressourcen, fremde Bibliotheken und die eigene native Tk-Erweiterung sind getrennte Prüfgegenstände; die native Erweiterung wurde hier nicht zeilenweise oder mit Readern abgenommen.

### 11.3 Vertiefte Aufruf- und Datenflüsse

| Bereich | Untersuchte Kette und tragfähiger Schutz | Grenze/Einordnung |
|---|---|---|
| Mutation → Datei | Aktion → `item_change`/`sidebar_change` oder älterer direkter Schnappschuss → `save_items` → Vergleich/Verlauf/Vorsicherung → temporäre JSON-Datei mit fsync → Austausch; Windows-Sperren begrenzt wiederholt | Generische Fehler lassen RAM/dirty stehen, besondere Importe rollen explizit zurück; kein einheitlicher Transaktionsvertrag. A32/A33 |
| Laden/Migration | JSON → Normalisierung → Format-/Artenprüfung → UI → Migration; `SchemaBackups` sichert vor Überschreiben | Neues Aufgabenformat ist schreibgeschützt; UI liegt trotzdem in der Dateifehlergrenze. A34 |
| Notion/Seitenrestore | begrenztes Archiv/eingefrorene Sicherung → Vorschau/Fingerprint → eingefrorene Anhänge → exklusive Stagingdateien → reine Inhaltsplanung → Schema → gemeinsame Übernahme | Rückbau löscht eigene Dateien, technische IDs werden geprüft. Schutz hängt zugleich an Flush und Guard: A32/A35 |
| Fokus/Erinnerungen | `focus_timer` → Settings-Journal → Aufgabenzeit → Journal löschen; Zustellbelege vor Anzeige und in Undo-Snapshots | Vorher/Nachher erkennt beide Crashfenster, Konflikt bleibt offen; Zustellung nur bei laufender App. Kein neuer reproduzierter Zeitbuchungsfehler |
| Kalender/Zonen | lokale ICS → begrenzter Parser/RRULE → Worker-Jahresfenster → Generation/Quellhash → lokale Tagesbilanz | Endliche Grenzen, begrenzter Fenstercache, alte Ergebnisse verworfen. Fehler heißt unbekannte Belegung. Quelle wird ausdrücklich neu geladen |
| Suche/Filter/Cache | `quick_open_results` → `content_search`; Filter → `filter_explain`; Ansichten → gemeinsame Gruppierung; `render_pass` hält Kennzahlen nur je Aufbau, Speichern leert sie | Kein neuer gemessener Suchengpass; kein FTS-Vorgriff. `RetainedWidgets` bindet Widgets an Host/IDs. Einmaliges `today_view`-Deduplizieren nach Objektidentität ist kein persistenter Objektcache |
| Pixel/Animation | strikte Zell-/Framevalidierung → eigene Puffer → `store_drawing` → Speicherweg; `animation_export` hält Mehrdateiausgabe rückrollbar | Globale, Pixel- und Pinnwand-Undo-Puffer haben unterschiedliche Geltungsräume; FP-01 muss Fokus/Wechsel gemeinsam belegen |

### 11.4 Neue konkrete Befunde und Gegenprüfungen

Die [isolierte Probe](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/probe_codegrenzen.py) und ihr [Ergebnis](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/ergebnis_codegrenzen.json) dokumentieren gezielte Fehlerinjektionen ohne Tk-Fenster, mit künstlichem `GLIDE_DATA_DIR` vor dem Import. Produktionsmethoden laufen unverändert; UI-/Dateiadapter werden dort ersetzt, wo die konkrete Fehlergrenze untersucht wird. Quell-SHA-256 ist festgehalten. Das sind Reproduktionen der Schutzlücken, keine Statistik über ihre natürliche Häufigkeit und keine vollständige Bedienabnahme.

| Kennung | Einordnung / Sicherheit | Priorität und Ablage |
|---|---|---|
| A31 | Konkret begründetes Reaktionsrisiko; synchroner Aufruf statisch eindeutig; typische reale Dauer ungemessen | P1, WA-26 |
| A32 | Nachgewiesener Fehler des Schutzrückwegs bei vollem Undo-Stapel; hoch; am Upstream-Stand `9ec474b` unverändert | P0 innerhalb der Schutzrunde (Begründung unten), WA-27 |
| A33 | Nachgewiesener lokaler Undo-Fehler bei Speicherfehlschlag; hoch; Korrektur im Remote-FP-01-Kandidaten vorhanden und dort durch Ausführung bestätigt | FP-01 prüfen/abschließen, keinen parallelen Neubau beginnen |
| A34 | Nachgewiesene Fehlklassifizierung einer injizierten UI-Ausnahme; hoch; natürliches Auftreten ungemessen; am Upstream-Stand unverändert | P1, WA-28 |
| A35 | Nachgewiesener verlorener Bool-Vertrag; hoch; konkrete Folge je Caller weiter integrationsprüfen; am Upstream-Stand unverändert | P1, WA-29 |
| A36 | Datensperre `glide.lock`: defekte oder unlesbare Lockdatei gilt als frei, weitere Lücken an den Rändern; die Aufgabendatei schützt der Kennungsvergleich vor `save_items`. Konkret begründetes Risiko, teilweise per Probe belegt, kein Datenverlustnachweis | P1, WA-30 |

**A31 – Kalte Bildvorschauen können den UI-Thread blockieren.** `image_preview.py:189`, `PreviewCache.convert`, wartet synchron auf `subprocess.run(..., timeout=45)`. `GalleryView._convert_next` (`app.pyw:11574`) und `_load_home_gallery_thumbnail` (24592) rufen es aus `after` auf; `PageEditor.render_image` (10971) aus einem eigenen verzögerten Lambda. `reference_png_path` (46192) verwendet denselben synchronen Konverter im Zeichnungsweg. `after` macht einen blockierenden Aufruf nicht asynchron. Besonders betroffen sind kalte JPEG-/HEIC-/WebP-Vorschauen unter Windows mit PowerShell/WIC und unter Linux mit Systemwerkzeug; native Mac-`nsimage`-Bilder benötigen diesen Weg meist nicht. Eine einzelne langsame oder hängende Konversion kann Eingaben, Abbruch und UI-Timer bis zum 45-Sekunden-Limit zurückhalten. Demgegenüber verwendet `request_cover_conversion` (44364) bereits einen Worker: derselbe Nutzerbedarf hat zwei verschiedene Reaktionsverträge.

Vorhandene Prüfungen `test_bilder330`, `test_befunde330`, `test_release37` und `test_preview_tools` belegen Formate/Rückfälle; sie belegen keinen maximalen Ereignisschleifenabstand bei künstlich langsamem Konverter. Lösung: eine gemeinsame begrenzte Konversionswarteschlange, Ergebnisse über Polling im UI-Thread, deduplizierte Pfad-/Dateistand-Aufträge, Generation und Hostlebensdauer, klares Retry für Fehlversuche. PhotoImages bleiben im UI-Thread. Der frühere Host darf nach Navigation nicht angesprochen werden. Zusätzlicher Größen-/Dateiaufbewahrungsvertrag für `_sizes` und Konversionsdateien ist innerhalb WA-26 mitzudenken: Bild-LRU 160 begrenzt nicht diese Nebenbestände; daraus wurde kein gemessener Speicherengpass abgeleitet. Aufwand M (mehrere UI-Caller, Plattformgegenproben), kein Format und keine neue Laufzeitabhängigkeit; Regressionsrisiko mittel.

**A32 – Der Wächter kann bei 20 Undo-Schritten nicht zurückrollen.** `guarded_structural_change` (`app.pyw:50137`) merkt sich `depth_before`. `snapshot_undo` (49994) und `trim_undo_stack` (50026) halten die maximale Länge 20; `item_change` trimmt nach markierter Änderung ebenfalls vor Ende des äußeren Wächters. Bei bereits 20 Schritten bleibt die Tiefe nach einer neuen Aktion 20. Stellt der Wächter dann eine fehlende ID fest oder erhält er `DataIntegrityError`, ruft er `rollback_to_undo_depth(20)` (50175): `len <= depth` liefert `False`, obwohl der neueste Schnappschuss existiert. `report_integrity_stop` behauptet trotzdem, der frühere Stand sei vollständig wiederhergestellt. Die Probe mit zwei Punkten verliert absichtlich einen Punkt: Tiefe 0/19 stellt beide wieder her, Tiefe 20 behält nur einen; jeweils mit direktem `snapshot_undo` und mit echtem `item_change`-Rahmen.

Betroffen sind die Schutzgarantien von Gruppieren/Auflösen, Seitenleistenverschieben, Aufgabenverlegen, Zeichenübernahme, Notion-Übernahme und Einzelrestore. Das beweist **keinen heute spontan verlierenden normalen Gruppieralgorithmus**, sondern einen reproduzierbar versagenden Schutz, sobald ein solcher Umbaufehler auftritt. `test_datenintegritaet.py:126` injiziert Verlust/`DataIntegrityError` bereits, setzt dazu aber einen frischen Stapel auf und deckt die volle Grenze nicht ab. Im gelesenen Remote-FP-01-Diff bleibt die Tiefenregel erhalten. Lösung: eigener unveränderlicher Transaktionsschnappschuss/Token über die ganze Guard-Lebensdauer oder erst nach erfolgreichem Guard trimmen; Rückweg-Erfolg und tatsächliche ID-Wiederkehr prüfen, keine pauschale Rettungsmeldung. Tests Tiefe 0/19/20, direkter Snapshot/Wrapper, Fehler vor/nach Speichern, fehlgeschlagener Rückweg, Reload und Redo-Kandidat. Aufwand S–M; keine Migration; Wechselwirkung FP-01 hoch.

**A33 – Lokales Undo verliert bei Schreibfehler den Schritt und meldet Erfolg.** `undo_last_change` (`app.pyw:50069`) poppt, ruft `apply_snapshot`, meldet `feedback('undone')`. `_apply_snapshot` (50040) wertet `save_items` nur für Seitenleistenaufbau aus und liefert kein Ergebnis. Damit ist der Schritt auch bei fehlgeschlagener Speicherung verbraucht; RAM/Datei unterscheiden sich und die Erfolgsmeldung ist unzutreffend. Die gezielte Probe erzwingt eine erfolglose Snapshotanwendung und erhält Stapeltiefe 0 mit `undone`. Vorhandene lokale Tests prüfen zahlreiche Undo-/Schreibpfade, aber nicht diesen globalen Undo-Abbruchvertrag. **Lesend bestätigt in `origin/main`:** FP-01 ergänzt Rückgabewert, aktuellen Gegenstand, RAM-Rückweg und Wiederherstellung des Schrittes; `test_wiederholen.py` besitzt dafür den Fall `schreibfehler`. Daher Korrektur dort gezielt abnehmen und liefern, keine zweite Implementierung. Eine vorhandene Testdatei ersetzt weder Ausführung noch native/lieferbezogene Bestätigung.

**A34 – Ein Darstellungsfehler wird zum beschädigten Datenbestand erklärt.** `load_items` (`app.pyw:41885`) führt nach erfolgreichem JSON/Normalisieren auch `update_sidebar_list`/`refresh_tree` im selben `try` aus. Das folgende `except (..., tk.TclError)` ruft `handle_unreadable_save_file` (41981). Ein injizierter reiner `tk.TclError` beim Zeichnen einer gültigen Format-25-Datei erzeugt deshalb „Speicherdatei beschädigt“, eine bytegenaue `liste_unlesbar_*`-Kopie und einen leeren **schreibfähigen** RAM-Bestand. Die Originaldatei bleibt in dieser Probe zunächst identisch; eine folgende reguläre Speicherung kann den leeren Bestand darüber schreiben. Die vorhandene Kopie verhindert Totalverlust aller Wiederherstellungswege, die Fehlermeldung führt den Anwender aber zur falschen Ursache.

Die Datei-/Altformatproben in `test_features330` und Datenintegrität prüfen echte Eingabefehler/Formatgrenzen, keine injizierte reine UI-Ausnahme zwischen Laden und Darstellung. Lösung: Lesen/Normalisieren in eigenen transaktionsartigen Schritt, dann Bestandsübernahme, dann gesonderter UI-Aufbau; UI-Ausnahme lässt gültigen Datenstand erhalten und wird als UI-Fehler gemeldet. Nur echte Daten-/Lesefehler dürfen den Leerstartpfad erreichen. Grenztests gültige Datei+TclError/ValueError im UI, ungültige JSON, neueres Format, Sicherungsfehler und späteres Autosave mit Dateivergleich. Aufwand S–M, kein Format; Startablauf-/Migrationsregressionen gezielt prüfen.

**A35 – Editor-Flush verwirft die Erfolgsinformation.** `flush_rich_note` (`app.pyw:44188`) ruft `editor.flush()` sowie `flush_drawing_editor()` auf und liefert immer `None`. `PageEditor.flush` (9965) und `DrawingEditor.flush` (13493) können bei Validierungs-/Schreibfehler `False` liefern. Geprüfte Caller wie `change_page_feature` (44230), `create_list_from_template` (44476), `new_page_from_markdown` (44855), `apply_notion_selection` (55618) und `apply_page_restore` (55766) fragen ausdrücklich `is False` ab: Diese Barriere ist unerreichbar. Die Probe bestätigt beide Fehlerrichtungen; auch im Erfolgsfall kommt `None` zurück. Navigation/Export/Ende verwenden teilweise gar keinen Rückgabewert; dort muss der jeweilige gewünschte Fehlervertrag ausdrücklich geprüft werden.

Ein Schreibfehler kann den neuen Inhalt bereits im RAM/dirty halten; deshalb ist aus dem Adapterfehler allein kein allgemeiner Datenverlust abzuleiten. Validierungsfehler vor Modellübernahme oder Abbau eines noch nicht übertragenen Editors sind jedoch ein konkretes Folgerisiko. Bestehende Richnote-/Pixel-/Notion-Brückentests decken einzelne Speicherrückgaben ab, aber die verlorene aggregierte Rückgabe nicht. Lösung: gemeinsamer `True`/`False`-Vertrag, beide Editoren berücksichtigen, abhängige Übernahme bei `False` stoppen und Eingabefläche erhalten; alle Aufrufer vorab nach gewünschtem Abbruchverhalten inventarisieren. Tests Erfolg, kein Editor, jeder Einzelfehler, beide Fehler und echte Seiten-/Restore-/Export-Caller. Aufwand S–M; keine Migration, Nutzerentscheidung nicht nötig.

**Gegenprobe am Upstream-Stand (Gegenprüfung 18.10.2026):** Dieselben zwölf Fehlerinjektionen liefen zusätzlich gegen `9ec474b` (App-SHA-256 `61f7b96394f0ced5…`). Einzige Anpassung der [Probenvariante](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/probe_codegrenzen_upstream.py): ein Platzhalter für `sync_current_list_reference`, weil FP-01 den Undo-Weg über `undo_state` führt. [Ergebnis](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/ergebnis_codegrenzen_9ec474b.json): A33 ist dort behoben – der Schritt bleibt auf dem Stapel, der Arbeitsspeicher kehrt zum Dateistand zurück, es erscheint keine Erfolgsmeldung. A32 (Tiefe 20, beide Varianten), A34, A35 und A27 verhalten sich unverändert. Die Wiederholung der Originalprobe am lokalen Stand ergab eine bytegleiche Ergebnisdatei. Folge: Die Schutzrunde setzt auf dem FP-01-Stand auf; WA-27–WA-29 bleiben dort nötig.

**A32 präzisiert (Gegenprüfung):** `item_change` speichert beim Verlassen (`save_items`), also bevor der äußere Wächter den Bestand vergleicht. Bei Tiefe 20 steht ein injizierter Verlust deshalb bereits in der Datei, der Rückweg bleibt wirkungslos, und `report_integrity_stop` meldet trotzdem „Abgebrochen – keine Daten verloren … Der vorherige Stand ist vollständig wiederhergestellt.“ Der Vorzustand liegt in diesem Fall noch oben auf dem Rückgängig-Stapel; Strg+Z stellt ihn in derselben Sitzung wieder her – die Meldung hält genau davon ab. Zusätzlich wertet `rollback_to_undo_depth` in beiden Fassungen das Speicherergebnis von `apply_snapshot` nicht aus; auch ein gescheitertes Zurückschreiben würde als vollständige Wiederherstellung gemeldet. **Einstufung:** Ein Schaden setzt voraus, dass eine Umbauaktion selbst Punkte verliert; der Wächter ist die zweite Verteidigungslinie. Das begründet den ersten Platz innerhalb der Schutzrunde (P0 dort). Nach D51 und Plan §19.5 darf diese Runde als begrenzte Korrekturlieferung vorgezogen werden; ein Einzelfix nur für A32 wäre dagegen unvollständig, weil WA-28/WA-29 denselben Fehlervertrag berühren. Zusätzliche Akzeptanzfälle: Datei nach Wächterabbruch bytegleich zum Vorzustand; Rettungsmeldung nur bei tatsächlich wiedergekehrten IDs und erfolgreicher Speicherung, sonst ehrlicher Hinweis auf Rückgängig.

**A36 – Datensperre mit Fail-open-Rändern (Gegenprüfung 18.10.2026).** Untersucht in `c0252ba`: `read_foreign_lock` (`app.pyw:17549`), `acquire_data_lock` (17593), `release_data_lock` (17620), `refresh_data_lock` (17633), Start (15759), Ordnerwechsel (17670–17719), Beenden (40347) und die Schreibwege. Die Sperre ist eine App-eigene JSON-Datei mit Rechner, PID, Kennung und Zeitstempel, keine Dateisystemsperre; geschrieben wird sie über `write_json_atomic` (temporäre Datei, fsync, Austausch). Tragender Schutz: `save_items` (42216) und mehrere direkte Schreibaktionen rufen vor dem Schreiben `refresh_data_lock` auf; steht dort eine fremde Kennung, wird die Instanz schreibgeschützt. Eine verdrängte Instanz überschreibt die Aufgabendatei damit nicht still, sondern erhält beim nächsten Speichern die Schreibschutzmeldung. Die [isolierte Probe](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/probe_datensperre.py) ([Ergebnis](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/ergebnis_datensperre.json), 14 Fälle, temporärer Datenordner, kein Tk-Fenster) bestätigt diesen Kern und belegt die folgenden Ränder:

| Teil | Befund | Beleg |
|---|---|---|
| L1 Erkennen | Eine defekte, nicht als Objekt lesbare oder nicht zu öffnende Lockdatei gilt als frei (`except … return None`); der Start überschreibt sie und arbeitet schreibfähig | Probe: defektes JSON, JSON-Liste, Lockpfad als Verzeichnis |
| L2 Erwerben | Lesen und anschließendes Ersetzen ohne exklusives Anlegen; zwei gleichzeitige Starts können sich beide für Besitzer halten, bis eine Instanz speichert | statisch; kein Rennen zweier Prozesse ausgeführt |
| L3 Erneuern | Kein Takt: der Zeitstempel wird nur bei Schreibaktionen erneuert. Nach 8 Stunden ohne Speichern gilt die Sperre auch bei lebendem Prozess auf demselben Rechner als verwaist | Probe |
| L4 Nebendateien | `save_settings` (17815), `save_window_geometry` und die Fokuszeit beim Beenden prüfen nur das gemerkte Flag `_data_read_only`, ohne Erneuerung. Eine verdrängte Instanz kann `settings.json` (gespeicherte Filter, Seitenleistenorte, Zustellbelege, Fokusjournal) bis zu ihrem nächsten `save_items` überschreiben | statisch; die Probe zeigt nur das unveränderte Flag |
| L5 Verlust der Datei | Fehlt die Lockdatei beim Erneuern, verschluckt `refresh_data_lock` den Fehler, bleibt schreibfähig und legt sie nicht neu an; eine danach startende Instanz sieht keine Sperre | Probe |
| Freigabe | korrekt: ein fremder Lock wird nicht gelöscht | Probe |

Einordnung: konkret begründetes Risiko mit teilweise belegtem Fail-open-Verhalten; **kein Nachweis eines Datenverlusts** und keine gemessene Häufigkeit. Bei zwei Rechnern über einen Cloud-Ordner bleibt eine Grenze, die keine Lockdatei schließen kann: Bis der Abgleich die Sperre überträgt, sieht keine Seite eine fremde Sperre; der Warndialog weist darauf hin. Lösungsrichtung (WA-30): defekte oder unlesbare Lockdatei nicht als frei werten, sondern schreibgeschützt mit erklärender Meldung und bewusster Übernahme öffnen; exklusiver Erwerb (exklusive Anlage plus Kennungsprüfung nach dem Schreiben); seltene Erneuerung auch ohne Schreibaktion oder Alterung nur ohne lebenden lokalen Prozess; eine gemeinsame Schreibschranke für alle Schreibwege einschließlich Einstellungen; fehlende Lockdatei neu anlegen oder schreibschützen. Tests: alle Probenfälle, zwei echte Prozesse in einem temporären Ordner, Einstellungsschreiben nach Verdrängung, Beenden mit laufendem Fokus-Timer. Aufwand S–M, kein Datenformat. Der Undo-/Flush-Vertrag ist kaum berührt; WA-30 ist deshalb unabhängig von WA-27–WA-29 umsetzbar, aber sinnvoll in derselben Schutzrunde zu prüfen.

**Nachverfolgung alter Befunde:** A26 bleibt eine fachliche Doppelung, kein automatisch löschbarer Duplikatcode: `repeat_rules` besitzt Glides Monatsende-Anker und sechs gespeicherte Altarten, `ics_recurrence` die größere RFC-Teilmenge. FP-02 muss sie erst über eine Fassade vereinheitlichen und alte Terminfolgen als Vertrag behalten. A27 ist präzisiert: `SETTINGS_VERSION=2` existiert, aber `load_settings` sperrt eine höhere Marke nicht; `normalize_personal_settings` setzt jede Eingabe auf 2. Die neue Probe 999 → 2 erhält ein unbekanntes Oberfeld und entfernt ein unbekanntes Filterunterfeld. WA-09 bleibt vor FP-04 erforderlich; FP-03 kann einen eigenen Oberfeldschlüssel nutzen. A28–A30 werden nicht neu als offen geführt: `repeat_ics` bildet die Klemmform, der Parser behandelt Ankertage vollständig, der Aufgaben-ICS-Import nutzt den gebündelten Zonenresolver. Die alten Gegenproben und heutigen Unit-/Integrationsverträge sind die zuständigen Nachweise.

### 11.5 Tragfähige technische Entwicklungsmöglichkeiten

Die folgenden Größenordnungen sind Planungseinschätzungen, keine Zusage: S = etwa 1–3 konzentrierte Entwicklungstage, M = etwa 3–8, L = mehrere Wochen einschließlich Integration; Plattform-/Menschenabnahmen können länger dauern. Vorarbeiten für neue Pakete folgen weiter D50/D51 und der bestätigten Paketplanung.

| Option | Problem/Nutzen und betroffene Funktionen | Daten/Plattform/Abhängigkeiten | Einführung, Prüfung, Rückfall und Aufwand | Einordnung |
|---|---|---|---|---|
| Tk/JSON behalten, Fehlergrenzen zuerst schließen | A32–A35 und A31 beheben konkrete Schutz-/Reaktionslücken in bestehenden Alltagswegen | Kein Formattor erforderlich; alle Plattformen; vorhandene Standardbibliothek | Kleine gemeinsam geprüfte Schutzrunde; Fehlerinjektionen plus betroffene echte Caller, Undo/Neustart/Dateibytes. Git-Rückfall möglich, solange Datenvertrag gleich. S–M je Befund, gemeinsamer Zuschnitt spart Doppelprüfung | Innerhalb D03/D16/D17, empfohlen |
| Fachliche Dienste gezielt extrahieren | Mutationsresultat, Transaktionsschnappschuss, Flush-Ergebnis und Importplanung aus `ListApp` lösen; verhindert nächste inkonsistente Variante | Tk-freie Dienste mit injizierten Datei-/Uhr-/Fabrikadaptern; bestehende UI-Einstiege bleiben. Kein neues Datenformat allein durch Extraktion | Eine fachlich vollständige Kette pro angefasstem Paket, erst Referenzfälle, dann Delegation und Gegenprobe. Alter Adapter kurzfristig rückschaltbar. M je Dienst; großflächiger Gesamtabgleich widerspräche D40 | Innerhalb D17/D40 bei konkretem Paket |
| Gemeinsamer Hintergrunddienst für Konversion | Ein Worker-Vertrag für Galerie, Seite, Titelbild und Zeichnungsreferenz; Ereignisschleife bleibt ansprechbar | Dateibytes im Worker, Tk-Bilder nur Hauptthread; begrenzte Parallelität, Generation und Abbruch; WIC/sips/Linux separat prüfen | Bestehenden Titelbildweg als fachliche Referenz verwenden, keine unkontrollierte Threadvermehrung. Konverter künstlich verlangsamen/fehlschlagen lassen, wechseln/schließen/retry. Synchroner Rückfall nur als ausdrücklich blockierender Sonderweg. M | WA-26, keine Richtungsentscheidung |
| Cache/Index erst nach Messung | Such-, Speicher- oder Kartengrenze reproduzierbar messen; verhindert zusätzliche Invalidierungszustände ohne belegten Nutzen | Rendercache existiert bereits; löschbarer Suchcache nach D16 möglich, JSON bleibt Quelle. Für Bildnebenbestände zunächst klare Größen-/Aufbewahrungsgrenzen | Gleiche Fixture, warm/kalt, Median/p95 und Ereignisschleifenabstand; Export/Undo/Import/Tageswechsel prüfen. Cache jederzeit löschbar. S für Messung, Umsetzung erst nach Ergebnis | Bestehende D16/P07-Regel beibehalten |
| JSON durch SQLite als Hauptspeicher ersetzen | Könnte bei belegter großer Schreib-/Abfragebelastung Teilupdates/Transaktionen erlauben; für heutige Fehler A32–A35 unnötig | Änderung D16 nötig; einmalige Migration, Integrität von Anhängen/Backups, Exportverlustfreiheit und Altleserschutz neu lösen; Standardbibliothek vorhanden, neues Speicherverhalten dennoch großer Vertrag | Erst >20.000-Punkte-Referenzfälle und unabhängige Lastbelege, danach lesender Prototyp/Exporter/Restore und getrennte Testablage. Rückfall nur mit geprüfter JSON-Ausgabe/Backup. L, hoher Migrationsanteil | Langfristige Option, derzeit kein neuer Anlass zur Auswahl |
| Toolkit wechseln (z.B. Qt) | Könnte native Editoren/Semantik anders lösen; Nutzen erst gegenüber dem laufenden Tk-9.1-Zugänglichkeitsweg belegen | Ändert D03/Q2; neue Laufzeit-/Paket-/Lizenzprüfung; große Teile von 61.256 Tk-Zeilen und deren Prüfadapter neu zu bauen; JSON kann zunächst bleiben | Vorher einen begrenzten Aufgaben-/Inspektorablauf in getrenntem Prototyp mit gleichen Reader-/DPI-/Tastaturfällen vergleichen. Keine Produktionsmigration vor Entscheidung; alter Tk-Stand bleibt Rückfall. Mehrere Monate, hohe Unsicherheit | Nur bei konkretem Scheitern/Abnahmegrenze neu entscheiden |
| Web-/Mehrgeräte-/CRDT-Kern | Erst bei bewusst gewähltem Bedarf an Mehrgerätebearbeitung: Konfliktmodell, Synchronisation und andere Oberflächen | Ändert grundlegende lokale Produktgrenzen und G23/Q3; neue Infrastruktur, Laufzeiten und Datenschutz-/Betriebsverträge; kein begründeter Fix für heutige Schutzfehler | Reiner Konzept-/Datenaustauschprototyp, vollständiges Export-/Restore-/Offlinekonzept vor Umsetzung. Kein kurzer Rückfall aus synchronisierten Konfliktzuständen. Mehrere Monate bis eigenes Projekt | Theoretische Richtung, nicht aus dieser Analyse beauftragt |

**Empfehlung:** Die konkreten Schutzwege, Ergebnisverträge und Bildjobs zuerst vereinheitlichen; bestehende Tk-freie Fachkerne weiterverwenden. Weder Monolithgröße noch die gefundenen Adapterfehler rechtfertigen heute einen Wechsel von Toolkit oder Hauptspeicher. Ein größerer Umbau braucht eine neue, überprüfbare Anforderung, die der gezielte Weg nicht erfüllt.

### 11.6 Prüfgrenzen und nächste eindeutige Nachweise

Diese Runde führt keinen weiteren störenden GUI-Volllauf und keine native Readerabnahme aus. Die Headless-Proben ersetzen gezielt UI-/Schreibadapter; echte Interaktionsauswirkungen müssen bei der jeweiligen Korrektur nachgetestet werden. Es wurden weder Codezeilenabdeckung gemessen noch fremde Bibliotheken sicherheitsgeprüft noch ein formaler Sicherheitsvollscan behauptet. Systematische Strukturabdeckung aller eigenen Module bedeutet ausdrücklich nicht vollständige Fehlerfreiheit.

Offen bleiben die natürlichen Ereignisse, die A32/A34 auslösen, repräsentative kalte Bildkonversionszeiten einschließlich UI-Takt unter Windows/Linux und vollständige native Paket-/Zugänglichkeitsabnahme. Ein fehlender natürlicher Auslöser schwächt die Aussage über die Häufigkeit, nicht die reproduzierte Schutzlücke. Der direkte Start von `app.pyw` wiederholt außerdem die Python-Minimalprüfung des Launchers nicht; schon der Import bestimmt/erstellt Datenpfade. Die Architektur wurde deshalb präzisiert, anstatt pauschal „vor jedem Datenzugriff“ zu behaupten. Der vorhandene abgeschlossene Baseline-/Liefernachweis bleibt historisch gültig; die neuen konkreten Fehlerbarrieren gehören vor die nächste belastbare Freigabeaussage. Die Datensperrprobe ersetzt weder ein Rennen zweier echter Prozesse noch einen Abgleich über einen Cloud-Ordner zwischen zwei Rechnern; L2 und L4 sind nur statisch belegt.

## 12. Abdeckung und Abschlussabgleich

Die Statuswerte beschreiben diese Untersuchung: **untersucht**, **teilweise untersucht**, **noch offen**, **durch konkrete fehlende Voraussetzung blockiert**, **mit Begründung nicht relevant**. Offene Produktentscheidungen verhindern nicht den Abschluss ihrer Entscheidungsvorlage. Praktische Abnahmen bleiben als offene Abnahmen erkennbar.

| Auftragsbereich | Abdeckung | Ergebnis / verbleibende konkrete Grenze |
|---|---|---|
| 1 Ziel/Tiefe und 2 Quellen | untersucht | Alle 16 Eingangsquellen, Code, Tests, Lieferbelege und die spätere Planung wurden einbezogen; die Belegarten bleiben getrennt. |
| 3 Arbeitsorganisation | untersucht | Getrennte Stränge, Abhängigkeitsfolge in §9.1 und eindeutige A-/FP-/WA-/E-/D-Kennungen; der zweite Auftragsabgleich steht hier. |
| 4 Tatsächlicher Stand | untersucht | Lokale und entfernte Git-Stände, Hashes, Pakete, Laufzeit und Verhältnis der Prüfungen in §9; keine Integration. |
| 5 Dokumente/Aufbewahrung | untersucht | Inventar in §7; 48 aktive Dokumente bewertet, keine aktiven Konfliktkopien, begründete Beibehaltung. Private Rohdaten wurden nicht gelesen. |
| 6 Frühere Analysen | untersucht | §6 stellt Umsetzung, überholte Aussagen, Vertiefung und neue Fehlergrenzen gegenüber. |
| 7 Funktions-/Aufgabeninventar | untersucht | Plan §18 enthält Kennung, Herkunft, Verbindlichkeit, Bearbeitungsstand, Restumfang, Module, Prüfung, Paket und Entscheidung. |
| 8 Aktuelle Konkurrenz | untersucht; benannte Einzelquellen teilweise verifiziert | Marktdokument mit Quellen, Abrufdatum, Varianten und Grenzen; keine Produktinstallation. Der nicht erneut bestätigte ältere Space-Bezug ist ausdrücklich begrenzt. |
| 9 Nutzungsszenarien | untersucht | S01–S18; theoretische Abläufe und tatsächlich ausgeführte Proben sind getrennt. Konkurrenzqualität und persönliche Eignung wurden nicht praktisch gemessen. |
| 10 Bestehende Pakete | untersucht | Plan §19 mit Ziel, Restumfang, Daten, Migration, Oberfläche, Tests, Risiko, Aufwand, Abhängigkeiten und nützlichen Ausbaustufen. |
| 11 Codebasis | untersucht, Tiefe ausgewiesen | Alle 67 Produktionsmodule sind strukturell erfasst; kritische Aufrufer und Datenflüsse wurden vertieft. Der Prototyp ist als isolierte Bedienprobe abgegrenzt und wurde nicht in gleichem Umfang strukturell analysiert. Dies beweist keine vollständige Fehlerfreiheit. |
| 12 Alternativen/Grundrichtungen | untersucht | §11 enthält Architekturalternativen; heutige Grenzen, begrenzte Entscheidungsänderungen und grundlegende Richtungswechsel sind getrennt. |
| 13 Backlog/Reihenfolge | untersucht | Ausschließlich im Plan: Schutzkorrekturen, Lieferabschluss, bestätigte Ausbauten, Vorschläge und bedarfsabhängige Auslöser sind getrennt; D51 ist berücksichtigt. |
| 14 Entscheidungen | untersucht | Vollständiges Register in Plan §20; bestehende Kennungen und Antworten bleiben erhalten. Empfehlungen sind keine Beschlüsse. |
| 15 Dauerhafte Ablage | untersucht | Bestehende zuständige Dokumente fortgeschrieben; zusätzlich nur der datierte QA-Nachweis. |
| 16 Grenzen | untersucht | Keine Änderungen an Produktion oder Nutzerdaten, keine verändernden Git-Aktionen und keine Installation; fehlende Prüfplattformen konkret benannt. |
| 17 Abschlussprüfung | untersucht | Stand-, Link-, Index-, Hash-, Datenschutz- und Aufbewahrungsprüfung im Nachweis; ein grüner Dokumentationslauf ist keine Releasefreigabe. |
| 18 Ergebnisübersicht | untersucht | Übergabe mit lesbarer Navigation zu Stand, Paketen und Entscheidungen sowie Abschlussbericht im Chat. |
| Native Mac-/Linux-/Tk-9.1-/Readerbedienung in dieser Runde | durch fehlenden aktiven Prüfplatz blockiert | Auf der Referenzplattform mit eingefrorenem Produktionskandidaten durchführen; vorhandene historische Belege bleiben auf ihren Umfang begrenzt. |
| Menschen-, DPI-, Mehrmonitor-, Trackpad- und Readerabnahme | noch offen | Manuelle Prüfliste; ein automatischer Probelauf ersetzt keine Freigabe des Inhabers. |
| Echte Nutzerdaten/private Fehlerprotokolle | mit Begründung nicht relevant | Für die Schutzbefunde genügen künstliche Fehlerinjektionen und Codeanalyse; keine gesonderte Berechtigung für Originaldaten angefordert. |
| Gegenprüfung: Datensperre (Fail-open-Lock) | untersucht | A36/WA-30 in §11.4 mit Probe und Aufruferprüfung; Rennen zweier Prozesse und Cloud-Abgleich offen |
| Gegenprüfung: A32–A35/A27 am Upstream-Stand | untersucht | Gegenprobe `9ec474b`: A33 behoben, übrige unverändert (§11.4) |
| Gegenprüfung: Deep-Research-Vollbericht | durch fehlende Quelle blockiert | Volltext lag nicht vor; nichts daraus übernommen (§12.2) |
| Gegenprüfung: Temp-Bestände, Sicherung, Integrationsprotokoll | untersucht | §12.2 mit Hashes, Status und Sicherungsmanifest |
| Gegenprüfung: Vorher/Nachher-Abgleich Marktdokument | teilweise untersucht | Linkbilanz in §12.2; Einzelbegründung je entfallener Quelle offen |
| Gegenprüfung: Nachweismatrix je Teilanforderung, Aussagenregister | teilweise untersucht | Diese Tabelle und §6 bleiben auf Bereichsebene; keine Zeile je prüfbarer Teilanforderung |

### 12.1 Folgefragen und eindeutige Ablage

Alle während der Runde neu entdeckten Folgefragen haben einen Ort: Schutzfehler A31–A36 in §11 und zugehörige WA-/FP-Aufgaben im Plan, darunter die Datensperre A36/WA-30 aus der Gegenprüfung; fehlender Mac-Lieferstand/Versionsgleichheit in §9 und QA; D51/Phasenauswahl in Arbeitsrichtung/Plan §20; Backup-/Exportumfang FP-07/WA-22; neue Importquellen WA-19; Wochenritual WA-20; Fundorte WA-21; Seriendetails WA-23/24; relative Bearbeitungszeit von Seiten WA-25; Kompakt-/Nebenansicht/Notion-Muster E-U1–E-U3. Erkenntnisse erzeugen hier keine weitere Aufgabensammlung.

Unabhängig von offenen Produktwahlen sind Dokumentabgleich, reproduzierbare Schutzproben, konkreter Prüfvertrag und Vorbereitung des Lieferabgleichs möglich. Die eigentlichen Korrekturen und sämtliche Feature-Umsetzungen gehören in den folgenden Umsetzungsauftrag. Kein neuer Versions- oder Veröffentlichungstermin wird aus dieser Analyse abgeleitet.

### 12.2 Quellen und Rekonstruktionsbilanz der Gegenprüfung

Die Abschlussfassung dieses Analyseauftrags (18.10.2026, 13:23–13:38) wurde danach gegen den ausführlicheren Claude-Auftrag vom selben Tag gegengeprüft. Vor jeder Änderung wurde der uncommittete Stand gesichert: 22 geänderte versionierte Dokumente und 34 Dateien des Nachweisordners, je Datei mit SHA-256, dazu ein Gesamt-Patch gegen `c0252ba`, abgelegt außerhalb des Repositorys. Das [Sicherungsmanifest](../01_Repository/Glide/tests/qa-3.43.1/standanalyse_2026-10-18/sicherungsmanifest_gegenpruefung.json) liegt im Nachweisordner. Wiederherstellung: Datei aus der Sicherung an denselben Pfad kopieren und den Hash vergleichen oder den Patch auf `c0252ba` anwenden. Die Sicherung ist Schutzmaterial, keine zweite Dokumentation.

| Quelle (Temp-Ordner, vergänglich) | Größe · Zeit · SHA-256 | Inhalt | Status |
|---|---|---|---|
| `glide_analyse_18_basis.md` | 45.157 B · 18.10. 00:58 · `b44d8f42…` | Analyseentwurf mit Platzhalter `<!-- CODEBERICHT -->` | integriert; in dieser Analyse ist kein Platzhalter mehr vorhanden |
| `glide-codeanalyse-20261018-va1rrnyp/codeanalyse_teilbericht.md` | 27.679 B · 00:55 · `ff28cf15…` | technischer Codex-Teilbericht | §11.1–§11.6 zeilengleich (ohne Links und Überschriften); seine zusammengezogenen Schreibweisen sind in §11 korrigiert |
| `glide_uebergabe_18.md` | 11.133 B · 00:56 · `6424e01c…` | Übergabeentwurf | durch die Übergabe vom 18.10. ersetzt |
| `glide_standanalyse_20261018.py` | 7.988 B · 00:47 · `eb54958f…` | erzeugt `ausgangsstand.json` | statisch gelesen, nicht erneut ausgeführt. `initial_worktree_clean: true` und `schema: 25` sind im Skript fest gesetzt, nicht gemessen |
| `glide_dokukorrekturen_18.py` (Plural) | 9.978 B · 00:53 · `aeccee37…` | schreibendes Dokumentkorrekturskript | nicht ausgeführt. Die im Verlauf genannte Singularfassung `glide_dokukorrektur_18.py` existiert nicht |
| `glide-markt-vor-konsolidierung-2026-10-18.md` | 80.916 B · 17.10. 01:53 · `281d64f3…` | Marktdokument vor der Konsolidierung | inhaltsgleich mit `c0252ba`; Linkbilanz unten |
| `glide_integration_18.py`, `glide_lesbarkeit_18.py`, `glide_abschluss_18.py`, `glide_plan_sprachrest_18.py`, `glide_qa_abschnitt_18.md`, `glide_final_links_18.py` | 18.10. 13:23–13:37 | Werkzeuge der Abschlussrunde | Herkunft der Fassung 13:32–13:38; nicht erneut ausgeführt |

**Sauberer Ausgangsstand:** Die Angabe „zu Beginn sauber“ stammt aus dem fest gesetzten Skriptwert und ist nicht unabhängig gemessen. Plausibel bleibt sie: letzter Commit 17.10. 02:20, danach keine Git-Einträge, Marktvorfassung bytegleich mit `c0252ba`, alle 22 geänderten Dateien mit Zeitstempel 18.10. 13:32–13:38. Datenformat 25 bestätigt die CI-Versionsprüfung unabhängig.

**Deep-Research-Bericht:** Der Volltext der Deep-Research-Antwort aus dem Referenzgespräch lag weder dem Auftragsexport noch der Gegenprüfung vor; der Verlauf lieferte nur Platzhalter. Keine Aussage daraus ist übernommen. Die vom Inhaber genannten Auditpunkte (voller Undo-Stapel, Erfolgsmeldungen, Fail-open-Lock) sind als Prüfkandidaten in §11.4 bearbeitet. Sobald der Bericht zugänglich ist, seine Einzelbehauptungen hier einordnen.

**Linkbilanz Marktdokument:** Die Vorfassung enthielt 104 externe Links, die aktuelle Fassung 112. 62 Links der Vorfassung sind entfallen, 55 davon stehen in keinem aktuellen Dokument mehr. Ein Teil ist ersetzt (etwa das umgezogene Super-Productivity-Repository, Sekundärquellen durch Herstellerseiten), ein Teil ohne Verbleib, darunter die Tcl/Tk-9.1-Seite und python.org-Hinweise zu Tk 9 unter macOS, die den laufenden Tk-9.1-Weg betreffen. Die Vorfassung bleibt in Git abrufbar. Eine Einzelbegründung je entfallener Quelle ist offen und gehört zur nächsten Marktpflege; sie blockiert keine Umsetzung.

| Quelle | Ziel | Status | Gegenprüfung |
|---|---|---|---|
| Codex-Teilbericht | §11 | übernommen, Schreibweisen korrigiert | Textvergleich; Proben wiederholt, Ergebnis bytegleich |
| Gegenprobe `9ec474b` | §9.1, §11.4, Plan §18.3, QA-Bericht | neu übernommen | Ergebnisdatei im Nachweisordner |
| Datensperrprüfung | §11.4 (A36), Plan WA-30, QA-Bericht | neu | Probe und statische Aufruferprüfung |
| A32-Präzisierung | §11.4, Plan WA-27 | neu | `item_change`, `rollback_to_undo_depth` und `report_integrity_stop` in beiden Fassungen gelesen |
| Auftragsgrenze in Regeldateien | AGENTS.md, CLAUDE.md | entfernt; Sitzungsstand steht in der Übergabe | Diff |
| Deep-Research-Volltext | – | offen, Quelle fehlt | – |
| Marktvorfassung | Markt und Vorbilder | Linkbilanz erfasst, Einzelbegründung offen | Linkvergleich gegen `c0252ba` |
