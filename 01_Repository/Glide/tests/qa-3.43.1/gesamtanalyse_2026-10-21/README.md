# Breite Gesamtanalyse – 21.10.2026

Analyse- und Planungsnachweis zu Glide 3.43.1. Kein Produktionsumbau, keine Lieferung und keine Freigabe des neuesten FP-02-Kandidaten. Die Ergebnisse gehen in die bestehende [Analyse](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md), den [Marktbericht](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md), den einzigen [Entwicklungsplan](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) und die [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md) ein.

## Untersuchungsstand und Wiederholbarkeit

Aus der aktiven Arbeitskopie wurden 668 ausgewählte Quell-, Prüf-, Ressourcen- und Dokumentdateien außerhalb der Projektablage eingefroren; beim Kopieren keine instabilen Dateien. Git-Ausgangspunkt `10427276b97e10528759cc42b0d23f757ca14843`, Zweig `codex/bildvorschauen-wa26-2026-10-18`. Das [Manifest](ausgangsmanifest.json) bezeichnet die einzelnen Bytes. **App-SHA-256 `916c77701bd645227a734a0f8a5f10be65046f0b5c6d29feeafac203debe72f2`**; schon Format-26-Zwischenstand, noch vor dem späteren FP-02-Abschluss. Die aktive Arbeitskopie wurde parallel weiterentwickelt. Deshalb werden sämtliche Laufresultate hier diesem eingefrorenen Zwischenstand zugeordnet.

Python 3.14.7, Windows 11, Tcl/Tk 9.0.4; temporärer `GLIDE_DATA_DIR` vor jedem App-Import, ausschließlich künstliche Daten. Keine Installation, keine Nutzerdaten, keine Übernahme von Fremdcode. Vollständige lokale Rohlogs und die eingefrorene Kopie sind nicht Teil eines öffentlichen Git-Uploads. JSON-Protokolle sind für die Veröffentlichung um Benutzerpfade bereinigt; Resultate und Quellenhashes bleiben erhalten.

## Tatsächlich ausgeführte Methoden

| Methode | Ergebnis / Grenze |
|---|---|
| Rekonstruktion und Quellenabgleich | 18-teiligen ursprünglichen Analyseauftrag, Regeln, Entscheidungen, bisherigen Plan, frühere Code-/Leistungsbefunde und Originalaufträge gelesen; keine verlorenen Aussagen erfunden |
| Quellen-/Standvarianten | eingefrorene lokale Bytes, laufender Kandidat, PR37/Remote-CI, 07 und Pakete ausdrücklich getrennt; ältere Lieferhashes nicht neu gemessen oder als aktuelle Lieferung bezeichnet |
| Vollständiges strukturelles Codeinventar | [Inventar](inventar_code.json), [Kennzahlen](code_kennzahlen.json): 77 Laufzeitdateien plus isolierter Prototyp; alle ASTs parsebar, Imports/Definitionen/Aufrufe/Testnamensbezüge erfasst. Keine Behauptung vollständiger Zeilen- oder Zweigprüfung |
| Statische Analyse | ursprünglicher Zählweg nach 150 s abgebrochen; in einem geladenen Modul ausschließlich Wortzählung durch gleichwertigen Einpasszähler ersetzt, 31 Regex-Gegenvergleiche, 2.912 Namen. Restliche Analyse unverändert; Exit 0 in 5,35 s. [Methodenbeleg](statische_analyse_vollstaendig.json) |
| Unabhängige Erreichbarkeit | Originalwerkzeug ausgeführt, Exit 0; 162 unaufgelöste Kandidaten sind wegen dynamischer Bindungen und enger Testauswahl kein Löschbeweis |
| Attribute, Duplikate und Designinventar | alle drei Werkzeuge ausgeführt; Attribute: keine Befunde in 40/41 Klassen, unbekannte Windows-Basisklasse ausgenommen. Neun Wiederholungsgruppen semantisch eingeordnet. Designinventar erfasst nur ausgewählte Quellbereiche, kein appweiter Konformitätsbeweis |
| Fachlogik | [820 Unit-Tests grün](fachlogik.json), 18,859 s eigentliche Testzeit; gilt für den eingefrorenen Zwischenstand |
| Echte Bereichs-/UI-Wege | [Acht Suiten](bereichspruefungen.json), davon sechs vollständig grün: Schutzrunde 10, Bildkonversion 10, Erwähnungen 6, KI-Aufträge 5, Markdownbaum 3, UI-/UX-Paket 17 Fälle. Ansichten 7/9; Seitenkarten drei Fälle im Rohlog grün, danach Abbruch. Kein pauschales Grün |
| Altleser-/Formatgrenze | rote Altleserfälle verwenden bereits Format 26 gegen ausgelieferte Format-25-App; Schutzdialog blockiert damaligen Testadapter. Separat auftretender Tcl-Cleanupfehler. Das ist weder ein Nachweis lesbarer neuer Daten im Altleser noch eine endgültige Fehlerabgrenzung der neuesten Tests |
| Mehrprozess-Sperrübergänge | [Vier Gegenproben](sperruebergaenge.json), reales Erwerbsprotokoll, kontrollierter Lesezeitpunkt: alter Besitzer löscht bzw. überschreibt neuen Lock. Gegenkontrolle bewahrt bereits vor dem Lesen fremden Token; Häufigkeit nicht gemessen |
| Empirische Leistung | drei Tk-Interpreter/Datenordner nacheinander in **einem** Python-Prozess; je 100/1.000/10.000 Aufgaben, erster Aufruf und sieben warme Werte für Rendern/Suche/Filter/Speichern/echtes Erledigen. [Rohwerte](ui_und_leistung/leistung_und_ui.json); Importcache bleibt, p95 aus sieben Werten ist nur das Maximum |
| Profiling / Speicher | getrennte fünf Suchaufrufe unter cProfile; 40 Ansichtswechsel unter tracemalloc. Keine RSS-/native Tk-/Langzeit-Leckbehauptung. Keine Optimierung oder vorher/nachher-Wirkung gemessen |
| Visueller Audit | [19 frische eigene Fensteraufnahmen](sichtpruefung/sichtpruefung.json), einzeln gesichtet; neun angeforderte Navigationen in zwei Layouts plus Einstellungen. Die Navigation „Liste“ öffnet wegen gespeicherter Ansicht tatsächlich das Spaltenboard: ausdrücklich kein neuer Foto-Nachweis der schlichten Liste. Weitere zwei fachliche Dialog-/Seitenbilder geprüft. Der erste Captureversuch scheiterte an falschem Kalender-Methodennamen; Messdaten davor bleiben erhalten, Capture gesondert erfolgreich |
| Primärquellen / Fremdcode | aktuelle Herstellerhilfen für Aufgaben-, Wissens-, Board-, Pixel- und Integrationsmodelle; datierte Grenzen und URLs im Marktbericht. Super-Productivity-Regelmodell und AppFlowy-README/Lizenz konkret gelesen. Kein praktischer Fremdprodukt-Benchmark |
| Szenarien / Paketprüfung / Architektur | 18 Szenarien aus der bisherigen Analyse mit neuen Bereichsbelegen abgeglichen; Paketprüfung nach 14 Dimensionen und inkrementelle Architekturvarianten im zentralen Plan/Analyse nachgeführt |
| Dokumente / Abschluss | kanonische Zuständigkeit erhalten, neue Befunde auf bestehende IDs und ergänzte WA-Kennungen abgebildet. Link-, Stand- und Datenschutzprüfung separat im Abschlussbeleg. Keine vollständige Phasenmatrix durch diese Analyse ersetzt |

Die Skripte [Sperrprobe](probe_sperruebergaenge.py), [Leistungsmessung](probe_leistung_und_ui.py) und [korrigierte Sichtaufnahme](probe_sichtpruefung.py) erwarten `--app` auf eine gesicherte `src/glide/app.pyw` und `--out` auf einen neuen Nachweisordner (Sperrprobe: Aufrufoptionen im Skript beachten). Nicht gegen einen parallel veränderten Stand messen. Der erste Leistungs-/Captureversuch ist einschließlich Fehlstatus dokumentiert; das korrigierte Capture schreibt einen eigenen Bericht.

## Wichtigste Folgerungen

Der größte hier gemessene Großbestandsaufwand liegt im echten Mutationsweg mit Speichern und Darstellung, nicht in der isolierten Suche: bei 10.000 Punkten warme Medianwerte 781–858 ms gegenüber 24–41 ms Suche. Erst dessen Profil und unveränderte Daten-/Undo-Verträge erlauben eine sinnvolle Optimierung. Der neue Lock-Übergangsfehler bleibt ein begrenzter, reproduzierter Schutzbefund. Designübertragung benötigt gemeinsame semantische Rollen und Bereichsabnahmen; reine Ersetzung aller Pixelwerte wäre durch die Befunde nicht gedeckt.

Die später ausgeführte rote Grundstufe des [einmaligen Git-Auftrags](../gitauftrag_2026-10-21/README.md) gehört zum gleichzeitig weiterentwickelten Kandidaten. Sie ersetzt weder die hiesigen grünen Teilprüfungen noch wird sie durch diese aufgehoben. Native Mac/Linux-/Reader-, DPI-/Mehrmonitor-/Menschenabnahmen, praktische Konkurrenzvergleiche, vollständige Releaseprüfung und Lieferungen bleiben offen.
