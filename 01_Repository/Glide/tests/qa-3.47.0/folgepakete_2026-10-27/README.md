# Folgepakete – Mehrfachplanung und Nebenansichtsverlauf

Stand 27.10.2026 · Glide 3.47.0 · Aufgabenformat 26

Fortsetzungsauftrag „weiter“ nach den beiden gewählten Bereichen Tagessteuerung/Nebenansicht (D57). [Einzige Roadmap, §21.24](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2124-folgepakete-mehrfachplanung-und-nebenansichtsverlauf-3470). Kein neuer Anbieter, neue Inhaltsart, Laufzeitpaket, Git- oder Veröffentlichungsauftrag.

## Umfang und Vorläufe

- Tagessteuerung: Auswahlmodus mit zehn Zeilen je Seite, stabile Auswahl über alle Seiten und Listen, alle offenen Tagesaufgaben auswählen/leeren/beenden. Gemeinsame Planung/Entplanung über bestehende Kapazitäts-/Datumsvorschau, ein Undo/Redo, Fälligkeit erhalten. Vor und nach Dialogen aktuelle Auswahl, Aufgaben, Tagesbezug und Schreibbesitz prüfen; alte Menüs übernehmen keine geänderte Auswahl. Erledigte/archivierte/entfernte Ziele zählen nicht.
- Nebenansicht: maximal 30 Stationen je Sitzung mit Suche/aktivem Treffer, Zeilenauswahl und Leseposition. Zurück/Vorwärts/Alt+Pfeil, aktueller Verlauf und direkter vorhandener Inhaltswähler. Gelöschte Zwischenziele werden übersprungen; auch aus inzwischen fehlendem Inhalt zurück. Neue Navigation ersetzt Vorwärtszweige. Historie flüchtig, bei Wechsel des Datenpfads zurückgesetzt.

Baseline: sieben Kachel- und 18 Nebenansichtstests sowie bestehender echter Tagessteuerungsfall grün. Neue Tk-freie Tests und betroffene Bestandsgruppen: 40 Home-/35 Side-Tests grün, darunter 13 neue Auswahl-/Verlaufstests. Neue echte Mehrfachplanung grün: 21 offene Aufgaben aus zwei Listen über drei Seiten, Auswahl ohne Datei-/Undo-/Erledigungswirkung, Morgen/ohne Tag mit einem Undo/Redo, Fälligkeit, Dialogabbruch/Alterung, Sperre, Tageswechsel und readonly. Echter Verlauf grün. Größen-/Designvorlauf: 606 Knopfprüfungen in vier Startseiten- und drei Nebenansichtskonfigurationen grün.

Rote Vorläufe bleiben erhalten: Die erste Verlaufprobe maß die vorhandene automatische 400-ms-Notizspeicherung mit. Der Test hält diesen Timer nun ausdrücklich getrennt, um eine erzwungene Übernahme durch Navigation zu erkennen; Produktionsautosave unverändert. Der zweite Vorlauf wartete nicht auf die vorhandene verzögerte Menüausführung; der Harness wartet nun wie die bestehenden Fälle auf den Ereignisnachlauf. Keine Grenzwerte gelockert, keine Produktionskorrektur dafür.

## Versions- und Prüfgrenze

Die reguläre Versionspflege brach nach Aktualisierung der Versionskonstanten und zwei Fixturegeneratoren beim atomaren Ersetzen der Showcase-App-Datei mit Windows-Zugriffsfehler 5 ab. Die restlichen Generatoren und Standpflege wurden gezielt abgeschlossen (Showcase außerhalb OneDrive erzeugt, atomar übernommen, 16 Vorlagendatensätze, 42 Standdokumente und 31 Kürzungen nach bestehender Regel); kein Git-Indexzugriff. Ursache eines fremden Dateibesitzes ist daraus nicht belegt, keine fremden Prozesse beendet.

Endgültige Paketprüfung, Quellhashes, Python-/Showcase-Lieferung und CI stehen unten; das vollständige aktuelle Dokumentregister und lokale Verweise/Anker in der [Schlusskontrolle](abschluss.json). Die historische breite 3.46.0-Prüfung und ihr Restlauf gelten ihren damaligen Bytes. Keine neue vollständige 104-Suiten-Matrix, Linux-/Mac-/Reader-/DPI-/Mehrmonitor- oder menschliche Abnahme aus diesem begrenzten Featurepaket. Eigenständige Windows-/Mac-Pakete bleiben bis zu einem tatsächlichen Neubau 3.45.0. Kein Commit/Push/Merge.

## Endgültige gezielte Prüfung und Lieferung

[Quellmanifest](quellstand.json): 89 direkte Quelltexte einschließlich des separaten Zeichenprototyps; davon 88 Liefer-/Laufzeitdateien, 147 Ressourcen und 280 Prüfdateien eingefroren. App `dd26a038f430860e41cfb2e703689ea0c4dd7bcacbc753277be89ade23c1f014`. [Eingefrorener Arbeitsmodilauf](arbeitsmodi_eingefroren.json): 21/22 grün; nur eine alte Erwartung im Papierkorbzustand rot, weil nun lesende Verlaufsknöpfe neben Schließen vorhanden sind. Ausschließlich diese Erwartung samt Kommentar angepasst, Produktionsquelle unverändert. [Gezielter vollständiger Nachlauf dieses Falls](nebenansicht_nachlauf.json) grün. Neue Geometrie 606 Knopfprüfungen grün, eigene Aufnahmen in `screenshots/` lokal.

Python 07: 88 Code-Dateien und 147 Ressourcen bytegleich. Ein tatsächlicher Windows-Mappingfehler 1224 betraf ausschließlich die Vorlagendatei. `abgleich_07.py` verwendet nun wie der Showcase-Abgleich die vorhandene atomare Kopierfunktion, damit ein gemapptes Ziel nicht in-place überschrieben wird; sechs vorhandene Pflegewerkzeugtests einschließlich Kopier-/Replacefehler erhalten die alten Zielbytes. Echter Abgleich danach grün. [Lieferprobe](python_lieferprobe.json) führt die beiden bestehenden neuen Paketfälle direkt gegen 07 aus; Version/Format und Modulherkunft aus 07 werden zusätzlich geprüft. Beide Fälle grün.

**Neuer Auftrag:** Dokumentation erneut analysieren/abgleichen, anschließend alle Projektänderungen pushen. Deshalb sind Commit/Push auf `codex/glide-3.47-folgepakete` nach Dokumentabgleich/CI autorisiert; die frühere lokale Gitgrenze dieses Featureauftrags bleibt historisch. Aktuelle Korrekturen in Analyse §13.16 und Plan §21.25. Neue Rohprotokolle, QA-Fensterbilder und lokale Tk-Prüfumgebung bleiben lokal. Die vollständige 104-Suiten-Endmatrix und native Pakete/Menschenabnahme bleiben offen.

## Dokumentabgleich und CI vor dem Push

Strenge lokale [CI-Grundstufe](ci_streng/ergebnis.json): Exitcode 0, 19/19 Schritte ausgeführt/grün. 193 Werkzeugtests (ein erwarteter Skip), zweimal 972 Fachtests einschließlich leerem System-TZPATH, fünf Analysen, isolierte Startprobe, strenger bytegleicher Python-Lieferstand, 116 originale Vendor-Dateien und Datenschutz-/Ablage-/Synchronisationskontrollen grün. Das Dokumentregister umfasst 93 Dokumente: 42 fortgeschriebene, 45 historische und sechs ohne Standaussage. Historische Befunde/rote Prüfungen wurden nicht zu neuen Erfolgen umgeschrieben.

Die inhaltlichen Korrekturen umfassen den veralteten Claude-Einstieg, Roadmap-Einstieg und D-Register; Source-/Python-/native Paketstände in Architektur/READMEs/Übergabe/Releasecheckliste; aktuelle Testfälle und Releaseplanungsdatei; sichere Trennung der Mac-Vorstufe vom eigenständigen Paket; LF-Schreibweise des Versionstools; historische statt vermeintlich heutige Analyse-/Readeraussagen und den neuen ausdrücklichen Gitauftrag. Quellen/Umfang stehen in Analyse §13.16, Aufgaben allein in Plan §21.25. Externe Marktquellen bleiben datiert, keine neue Markt-/Rechts-/Readerprüfung behauptet.

Die [Schlusskontrolle](abschluss.py) prüft unveränderte Quelltexte, den ausdrücklich ausgewiesenen einzelnen Prüf-Erwartungsnachlauf, aktuelle 22-Fälle-Abdeckung, beide Lieferfälle, sämtliche Lieferhashes, sechs Showcase-Dateien, das komplette Dokumentregister, aktuelle lokale Links/Überschriftenanker und Arbeits-/Index-Whitespace. QA-Screenshots wurden an künstlichen Daten gesichtet und bleiben lokal; die Leeren-Aktion verwendet die vorhandene semantische Leeren-Farbe, ohne Datenlöschung.

Gittransport: Basis `origin/main` `1f4dbf8` frisch gelesen, früherer Quellbaum identisch. Änderungen auf `codex/glide-3.47-folgepakete` vorbereitet; vier Nachweisdateien für öffentliche Ausgabe von Benutzerpfaden bereinigt (Rohprotokolle lokal). Konkrete Commit-/Pushbestätigung erfolgt nach dieser Prüfung, keine Merge- oder Produktveröffentlichungsfreigabe daraus ableiten.

Endgültige Schlusskontrolle grün: 93 Dokumente im Register, 911 aktuelle lokale Verweise und 242 Überschriftenanker, keine Quell-/Lieferabweichung und kein Arbeits-/Index-Whitespacefehler. Vollständiger Einzelbericht in `abschluss.json`.
