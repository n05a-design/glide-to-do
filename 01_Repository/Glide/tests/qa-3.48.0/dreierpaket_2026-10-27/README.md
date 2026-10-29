# Drei Featurepakete: Tagesnavigation, Mehrfachfelder und Verweise

Stand 27.10.2026 · Glide 3.48.0 · Aufgabenformat 26

**Weiterführende WA-41-Analyse:** [24 zusätzliche Gegenproben und Ursachenbewertung](../wa41_2026-10-27/README.md). Interner Python-Cacheabbruch und Fehler auch nach Appimport ohne Fenster/Schreiber; keine Ursache bestätigt, keine Produktionsänderung oder Releasefreigabe. Dieser Phasenbericht und seine ursprünglichen Ergebnisse bleiben erhalten.

Auftrag: Featureumsetzung mit drei Paketen und größerem gemeinsamen Fortschritt; routinemäßige Tests ausdrücklich erst nach deren Implementierung. Der konkrete Schnitt vertieft die bereits gewählten Bereiche Tagessteuerung/Nebenansicht (D57); keine neue Inhaltsart, Integration oder Abhängigkeit. Verbindliche Quellen: [Plan §21.26](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2126-drei-featurepakete-tagesnavigation-mehrfachfelder-und-verweise-3480), [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md).

## Umfang und Prüfvertrag

1. Tagesnavigation: Heute, Vor-/Folgetag, beliebiges Datum und Tagesplan öffnen. Planung/Kapazität und Fälligkeit beziehen sich auf den angezeigten Tag; Tagesziel, nächste Aufgabe und Tagesvorschlag bleiben an Heute gebunden. Navigation ändert keine Aufgaben. Auswahl endet bei Tages-/Datenpfadwechsel; Zustand flüchtig und ohne Formatänderung.
2. Mehrfachfelder: Wichtigkeit 0–3 sowie reguläre Labels ausdrücklich hinzufügen/entfernen, auch listen-/seitenübergreifend. Verschiedene bestehende Labels bleiben erhalten; Systemlabels werden nicht zur impliziten Typumwandlung angeboten. Vor und nach dem Snapshot aktuelle Auswahl, IDs, Tag, Archiv-/Erledigungsstatus und Schreibbesitz prüfen. Kapazitätsfehler vor jeglicher Teiländerung; No-op ohne Undo, ein gemeinsames Undo/Redo und kein Erfolg nach Schreibfehler.
3. Nebenansicht: gültige interne Textlinks anklickbar; vorhandene Verweise/Rückverweise von Inhalt und ausgewählter Aufgabe in durchsuchbarer Aktionsauswahl. Heimatcontainer und Aufgabenmarkierung über vorhandenen Vorschauweg; aktueller Verlauf erhalten. Keine Bearbeitung und kein erzwungenes Speichern des Hauptentwurfs. Fehlende, gelöschte oder nicht darstellbare Ziele benennen; alte Menüs prüfen Beziehungen erneut.

Gestaltungskontexte: Startseite/Kacheln, Heute/Tagesplanung, Liste/Auswahl, Nebenansicht und Aktionsauswahl. B02/B06/B11/B15/B17/B19, D55/D57; bestehende Rollenfarben, ICONS, ButtonFlow, Trägerflächen und semantische Fokusnamen. Tagessteuerung bleibt in der scrollenden Kachel, Verweiswahl in der bestehenden eingebetteten Auswahl. Mindestgröße/große Schrift/Hell/Dunkel/Verlauf, 280-px-Nebenansicht und Kompaktmodus sind Prüfziele, keine vorweggenommene Abnahme.

## Ausgangsstand und Reihenfolge

Arbeitskopie vor Änderungen sauber, HEAD `2b1ee0f` (3.47.0). Die dokumentierte vorherige strenge CI-Grundstufe ist historische Baseline; in dieser Runde wurde gemäß direktem Auftrag vor vollständiger Implementierung keine Testsuite ausgeführt. Syntax-, Unit-, Bedien-, Design- und gemeinsame Regression folgen anschließend. Alle Appimporte der Prüfungen verwenden temporäre `GLIDE_DATA_DIR`-Ordner.

## Ergebnisse

Ergebnisse stehen in den folgenden Abschnitten. Die Featureprüfungen sind grün; der breite Lastbefund bleibt offen und verhindert den Lieferabschluss. Frühere rote/unvollständige Prüfungen behalten ihre Aussage. Native macOS-/Linux-/Reader-/DPI-/Mehrmonitor- und Menschenabnahme sowie eigenständige Paketbauten bleiben getrennte Tore; kein Git-Schreib- oder Veröffentlichungsauftrag aus dieser Featurefortsetzung.

## Gezielte Ergebnisse und gefundene Korrekturen

- 986 Fachtests grün; davon 14 neue reine Datums-/Mehrfachfeld-/Verweisgrenzen. Der erste Funktionsvorlauf scheiterte ausschließlich an der neuen Test-Knopfsuche (Symbolpräfix bei Tagesplan öffnen); Helper präzisiert, Produktionsfunktion unverändert. Beide Belege bleiben erhalten.
- [Arbeitsmodivorlauf](arbeitsmodi_vorlauf.json): 26/26 echte Fälle grün. Enthalten sind bisherige Kompakt-/Nebenansichts-/Planungs-/Verlaufswege und die drei neuen Featurefälle. Neue Gestaltung: 372 Knopfprüfungen in vier Größen-/Schrift-/Designkonfigurationen, darunter 480 × 560/groß/kompakt, drei Scrolllagen und Nebenansicht bei 280 px. Hinweise an/aus; Datumsspalte vollständig oder ausgeblendet. Vier neue Startseiten- und drei Nebenansichtsaufnahmen lokal; Kompakt-/Dunkelaufnahmen gesichtet.
- Die Sichtprüfung fand das vorherige feste 92-px-Datumsfeld in der Nebenansicht abgeschnitten. Es misst jetzt vollständigen Text und blendet die Spalte bei zu wenig Titelraum ganz aus (B11); kein Grenzwert gelockert. Sämtliche 26 Fälle danach grün.
- Der Versionswechsel hat gemäß Aufbewahrungsregel 111 veraltete Dateien gekürzt. Dabei wurden historische 3.42.0-Verweise unauflösbar; zusätzlich hatte die automatische Standpflege zwei aktuelle Beleglinks auf eine noch nicht existente Folgepaketablage umgestellt. Betroffene Links gezielt korrigiert: historische Ziele im unveränderten Git-Commit verifiziert, aktuelle Anleitung auf die vorhandene 3.48.0-Fixture. [Dokumentnachlauf](dokumentnachlauf.json): 89 registrierte Dokumente, keine Standbefunde und 357 lokale Markdown-Dateilinks geprüft.

## Breite Windows-Prüfung und WA-41

Die eingefrorene Kopie liegt außerhalb OneDrive; [470 Quell-/Prüf-/Ressourcen-/Fixturehashes](quellstand.json) wurden vor/nach dem Start gegen die Arbeitskopie abgeglichen. Die ausführbaren Dateien bleiben unverändert. Die ursprüngliche breite Prüfung enthält die noch nicht korrigierten Dokumentlinks und bleibt deshalb auch nach deren gezieltem grünen Nachlauf historisch rot.

Im abgeschlossenen breiten Versuch ist der bereits dokumentierte WA-41-Lastfehler erneut aufgetreten: `test_speicherlast330`, Windows-Zugriffsverletzung `0xC0000005` (3221225477), bei Runde/Speichern im reinen `save_comparison.history_value` über `PersistenceCoordinator`. Der Trace belegt den Absturzort, keine Ursache und keinen Zusammenhang mit den neuen Features. Keine spekulative Appänderung oder Abschwächung des Lasttests. Restmatrix und isolierte Gegenproben sind unten getrennt ausgewiesen; der ursprüngliche rote Log bleibt lokal erhalten. Release-/Menschen-/native Pakettore werden dadurch nicht freigegeben.

## Abgeschlossener breiter Versuch und gezielte Nachprüfung

Der [ursprüngliche Windows-Vollversuch](windows_vollpruefung/ergebnis.json) ist vollständig durchgelaufen: 123 Schritte, 116 ausgeführt/grün, sechs rot, eine menschliche Sichtprüfung übersprungen. Alle 104 Integrationssuiten ausgeführt. Die roten Schritte sind Dokumentation/Standprüfung (neun inzwischen korrigierte Links), Speicherlast sowie drei Altlesersuiten. Die isolierte Kopie war ohne Git-Historie erstellt; damit fehlte ausschließlich den historischen Proben eine Voraussetzung. [Gezielter Nachlauf](nachpruefung.json) derselben unveränderten Suiten mit rein lesendem Zugriff auf die vorhandenen gepinnten Commits: Seitenkarten, Ansichten und Wiederholungsregeln vollständig grün. Kein Testkriterium oder Appcode dafür geändert. Vier übrige Analysen, Showcase, Beispiel-/Release-Reproduktion und Screenshots grün. Die aktuellen Dokumente wurden getrennt nachgeprüft; der ursprüngliche rote Gesamtbericht bleibt unverändert.

**WA-41-Diagnose:** Erster isolierter 3.48.0-Lauf vollständig grün: 26.420 Punkte/28,5 MB, 40 verlustfreie Runden, sechs harte Schreiberabbrüche, parallele Schreiber, Sperren/Sicherungen/Migrationen. Zweiter isolierter Lauf rot: Vergleich nach Laden in Runde 5 abweichend. Zusätzlicher Lauf mit unveränderten Kriterien und lediglich begrenzter Felddiagnose brach schon beim Laden mit internem `TypeError: 'tuple' object is not an iterator` in `repeat_rules.check_stored_series` ab; daher keine Felddifferenz gewonnen. Zusammen mit der ursprünglichen Zugriffsverletzung belegt das uneinheitliche Laufzeitfehler, aber weder deren Ursache noch Datenverlust in einem echten Bestand. Kein spekulativer produktiver Fix.

Die 3.47.0-Gegenprobe wurde aus unveränderten Git-Quellen bereitgestellt. Zwei vorbereitende Versuche scheiterten an fehlenden Fixturedateien der bewusst schmalen Kopie; sie sind keine Appfehler. Nach Ergänzung aller identischen aktuellen Prüf-Fixtures lief die originale Speicherlastsuite auf 3.47.0 vollständig grün durch. Daraus folgt keine Entwarnung für 3.48.0 oder Ursachenzuordnung. Alle Rohlogs bleiben lokal; der Nachlaufbericht trennt diese Versuche.

## Lieferentscheidung und Abschlussgrenze

**3.48.0 bleibt lokaler Featurekandidat.** Die drei Featurepakete sind implementiert, 986 Fachtests und alle 26 Arbeitsmodifälle einschließlich 372 neuer Knopfprüfungen grün. Die bestehende breite Regression ist bis auf den offenen Lastfall samt den beschriebenen korrigierten Prüfbedingungen abgedeckt. Es gibt keinen vollständig grünen 123-Schritte-Gesamtlauf und keine Releasefreigabe.

Wegen des realen Lastbefunds wurde kein neuer Abgleich nach 07 oder 05 und kein nativer Paketbau durchgeführt. Die startbare Python-/Showcase-Lieferung bleibt 3.47.0, die eigenständigen Windows-/Mac-Pakete 3.45.0. Sechs erwartete Unterschiede Quelle/07 (App, vier Fach-/UI-Module einschließlich Neuerungen, Vorlagenressource) werden ausdrücklich ausgewiesen. Neuerungen und Quell-Fixtures tragen bereits 3.48.0; das ist kein Lieferbeleg. Weitere Produktentscheidungen und Git-Schreibaktionen bleiben außerhalb dieses Auftrags.

Die abschließende aktuelle CI-Grundstufe ist bestanden: 19 Schritte, 18 ausgeführt/grün und ein erwarteter Lieferstandhinweis auf sechs Abstände. 193 Werkzeugtests (ein Skip), zweimal 986 Fachtests, fünf Analysen, Startprobe, Fremdcode-/Datenschutz-/Ablage-/Synchronisationskontrollen grün. Keine strenge Liefergleichheit, weil der Kandidat absichtlich nicht geliefert wurde. Ihr Ergebnis und die finale Quell-/Dokument-/Abstandsprüfung stehen unter `ci_abschluss/ergebnis.json` und `abschluss.json`; sie ersetzen den roten Lastnachweis nicht.

**Schlusskontrolle:** 470 eingefrorene Quell-/Prüf-/Ressourcen-/Fixturedateien unverändert, alle 235 alten Python-Lieferdateien nach ihren tatsächlichen historischen SHA-256-Bytes unverändert, 89 Dokumente/357 lokale Markdown-Dateilinks grün. Lokaler Featurekandidat nachgewiesen, keine neue Lieferung und keine Releasefreigabe. Der erste Git-Blobabgleich meldete acht Ressourcen wegen Git-Textnormalisierung abweichend; die tatsächlichen alten Lieferbytes sind laut historischem SHA-256-Manifest identisch.

**WA-50-Struktur:** Hauptdatei 65.830 → 66.035 Zeilen (+205), ListApp 1.773 → 1.784 direkte Methoden (+11). Neue Fachregeln in bestehenden Tk-freien Modulen; keine neue Laufzeitdatei, Abhängigkeit oder Formatstufe. Eine Verringerung der Integrationsklasse wird nicht behauptet.
