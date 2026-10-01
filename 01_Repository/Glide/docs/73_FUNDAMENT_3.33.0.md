# Glide 3.33.0 – erstes Fundament aus der Claude-Planung

Stand 01.10.2026 · Glide 3.33.0 · Aufgabenformat 20

Der Auftrag vom 01.10.2026 startet die Umsetzung der neuen Entwicklungsplanung. Dieser begrenzte erste Schnitt erledigt T2 und P09a/W1 vor den größeren Oberflächenänderungen. Die frühere Reservierung 3.32.4 wird dadurch ersetzt; die übrigen Zielnummern sind weiterhin Planungsreservierungen.

## Abgleich der Ablage

Aktive Git-Arbeitskopie: `Github/glide-to-do`, Quelle der Wahrheit nach D09. GitHub und lokales HEAD standen beim Beginn auf `569020ef65880b28a50408e229a8027ba2a65898`. Die Hauptdatei 3.32.3 entsprach dem zuvor geprüften Stand (SHA-256 `24b21a71791dd6eff387dc889d099a7a7d3afc261d7243c9ff51994ba6cca1bb`). Claude hat Analysen, Planung und Entscheidungen ergänzt; die Laufzeitbasis dieses Vergleichs blieb gleich.

- `00_Arbeitsvorbereitung`: aktuelle Entscheidungen, Entwicklungsplan, Featurematrix und Übergabe.
- `01_Repository/Glide`: aktive Quelle, Verträge und Tests.
- `07_Python-Versionen`: ausgelieferte Python-Fassung.
- `05_Probelisten_Testdaten/Showcase`: isolierter Demonstrationsbestand.
- `Archiv/Glide_3.32.3_Claude_Code_2026-10-01` und `93_Zwischenstände`: unveränderte historische Belege, keine weiteren aktiven Quellbäume.
- Der frühere Projektpfad `Glide ToDo` enthielt nur noch abschließende QA-Dateien. 61 fehlende Dateien wurden ohne Konflikte in die neue Arbeitskopie übernommen; [Nachweis](../tests/qa-3.33.0/fundament_2026-10-01/ablageabgleich.json).
- Drei frühere Rechercheprotokolle fehlen im GitHub-Bestand. Aktive Verweise kennzeichnen diesen Verlust. Die originale Vorsicherung der Core-Fixture wurde im Zwischenstandsabbild gefunden und mit der erwarteten SHA-256 bytegleich wiederhergestellt. Historische Prüfbehauptungen werden damit nicht erneut bestätigt; kein erzeugter Ersatz gilt als Original.
- Viele anfängliche Git-Abweichungen waren ausschließlich Dateimodusänderungen durch den Umzug; fremde Änderungen werden nicht zurückgesetzt.
- Ein macOS-Bundle war in der neuen Arbeitskopie nicht vorhanden. Aus der unveränderten 3.32.3-Quelle wurde vor den Änderungen ein Entwicklungsbundle als Rückfallstand gebaut. Quellbaum und vorhandene Python-Laufzeit wurden vollständig gesichert.

[Neue Entwicklungsplanung](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md), [Entscheidungen](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md), [Eingangsmanifest](../tests/qa-3.33.0/fundament_2026-10-01/eingangsstand.json).

**Recherche-Nachprüfung:** Notion/Things-Angaben stichprobenartig an offiziellen Release Notes bestätigt; Things-3.23-Datum auf 21.08.2026 korrigiert. Die [Tcl/Tk-Seite](https://www.tcl-lang.org/software/tcltk/9.1.html) nennt nun 9.1.0 vom 29.09.2026. N12 benötigt weiter G26 und eigene Screenreader-Abnahme; diese Runde installiert keine neue Laufzeit. Nachtrag in der [Featurematrix](../../../00_Arbeitsvorbereitung/Glide_Konkurrenz_und_Featurematrix_2026-10-01.md).

## Änderungen und Invarianten

**T2:** `schema_backups.py` führt die Fachlogik ohne Tk. Es merkt Dateipfad, Inode, Größe, Änderungszeit und Metadatenzeit sowie die Formatnummer. Der Ladeweg liefert diese Nummer direkt aus dem schon gelesenen JSON. Ohne Ladeinformation wird dieselbe Datei einmal gelesen. Austausch oder Änderung invalidiert den Wert. Es wird weder der gesamte Datenbestand dauerhaft zusätzlich gehalten noch die Datei erst bei späterem Autosave gesichert.

Die neun bestehenden `ensure_schema<N>_backup`-Einstiege bleiben erhalten. Jede erforderliche Rückfallkopie bleibt bytegenau, unrotiert und unter dem bisherigen Dateinamen. Scheitert eine Kopie, bleibt die Prüfung unbestätigt und der Save bricht vor dem Überschreiben ab; Wiederholung versucht erneut zu sichern. Laden setzt sämtliche Formatprüfungen einschließlich Format 12 zurück. Unlesbare und neuere Bestände behalten die vorhandenen Schutzwege.

**P09a/W1:** `content_column_widths` kehrt in Tabelle und Bibliothek sofort zurück. Nur die Liste nutzt diese Inhaltsbreiten. Schrift-, Zeit- und Labelbreiten in der Liste werden weiter nach dem bisherigen Verfahren berechnet. Tabellenbreiten bleiben unter ihrem eigenen Spaltenvertrag.

Keine Datenmigration, keine neue Abhängigkeit. Dokumentarten, Aufgabenidentität, atomare Speicherung, Sperren, Undo und Mutationsgrenzen bleiben erhalten. Beide Lieferwerkzeuge nehmen das neue Modul ausdrücklich mit.

## Prüfungen

- Passende Baseline: bestehende Datenintegritätsprüfung mit 130 Kombinationen bestanden.
- Acht Unit-Tests: Formate 4–20, bytegenaue Sicherung, Parseranzahl, Ladeinformation, fehlende Datei, ungültige Formatwerte, Dateiaustausch, Änderung, Kopierfehler/Retry und unlesbares JSON.
- Neue Pflichtintegration `test_fundament333.py`: tatsächliche Speicher-/Ladewege, Dirty-Zustand, Sicherungsfehler und Wiederholung, keine erneute JSON-Lesung der Datendatei nach Laden, unveränderte Listenbreiten, Tabellen-/Listenwechsel und Callbackfehler.
- QA-Hintergrundfenster nehmen auf macOS tatsächlich keine Mausereignisse entgegen. `pruefe_tk.py` kontrolliert die native Eigenschaft an Hauptfenster, Dialog und Tooltip sowie synthetische Tk-Bindungen. Das betrifft ausschließlich Prüfprozesse. Der Negativtest erkennt den alten fehlerhaften Hintergrund (Exitcode 1), der neue besteht (Exitcode 0).
- Ein datumsabhängiger Wiederholungstest nutzt einen relativen zukünftigen Prüftermin, damit heute fällige Erinnerungen seinen Vergleich nicht verändern.
- Pflichtstand jetzt 59 Integrationssuiten, eine Unit-Test-Stufe, Showcase und fünf Analysen.

Der [abschließende Volllauf](../tests/qa-3.33.0/fundament_2026-10-01/vollpruefung/ergebnis.json) ist grün: 76 automatische Schritte, 59 Integrationssuiten, acht Unit-Tests, Showcase und fünf Analysen grün; 140 Python-/54 Bundle-Dateien bytegleich, Signatur gültig, getrennter Showcase-Starter bei Erststart und Neustart geprüft. [QA-Bericht](07_QA_BERICHT.md) und [Lieferabgleich](../tests/qa-3.33.0/fundament_2026-10-01/auslieferung.json). Physische Maus-/Trackpad-/OS-Fokusbedienung, Windows/Linux, Mehrmonitor/DPI und Screenreader bleiben manuell offen. Entwicklungsbundle weiterhin ad hoc signiert, mit installiertem Python; kein öffentliches Release.

## Vergleichbare Messung

[Alternierender Vergleich](../tests/qa-3.33.0/fundament_2026-10-01/funktionsmessung.json): gleicher Prozess auf macOS/Python 3.14.5/Tk 9.0.3, 5.000 Aufgaben, Aufwärmen und zwölf Runden mit wechselnder Reihenfolge.

| Funktion | Alt, Median | Neu, Median | Nach Laden |
|---|---:|---:|---:|
| Formatsicherungsprüfung | 161,406 ms | 17,896 ms | 0,064 ms |
| JSON-Leseläufe pro Prüfung | 9 | 1 | 0 |
| Ungenutzte Inhaltsbreiten der Tabelle | 77,117 ms | 0,001 ms | – |

Rohwerte und p95 liegen im JSON. Die alten Methoden werden aus dem gesicherten Quellstand geladen, keine neu geschriebene Simulation. Listenbreiten wurden vorher gegen das alte Verfahren verglichen. Diese Werte isolieren die betroffenen Funktionen. Die ersten vollständigen Ansichts-/Speicherserien schwankten unter unterschiedlicher Rechnerlast stark; sie liegen unverändert im Nachweisordner und werden nicht als allgemeiner Beschleunigungsnachweis ausgegeben. Der Gesamt-Speicherpfad und die Startseite brauchen weitere Arbeit.

## Anschluss und Entscheidungen

D12 am 01.10.2026 vollständig bestätigt: Heute (zusammengeführt), Gismo, Woche, Zuletzt bearbeitet, Angeheftet, **Zeichnungen, Pinnwand-Vorschau**. Eigene bestehende Auswahl bleibt beim späteren Umbau erhalten.

[Konkrete Codeeinstiege und Abnahmekriterien](../tests/qa-3.33.0/fundament_2026-10-01/anschluss_codeabgleich.json).

Nächste notwendige Performance-Schnitte: Startseite/P09b → P04 Bildlayout → P06 verbleibende Doppelaktualisierungen → P08 Verlaufsvergleich. Danach UX1 in begrenzten Schnitten: stabile Aktionskennungen vor Menüumbenennung; Kopfzeile und Befehlspalette; D11 Hinweiszeilen bei Bedarf; sieben Standardkacheln und automatische Designwahl. Parser/Feldchips folgen nach D10, danach Heute/Demnächst, Fokus und Eisenhower; schließlich Aufgaben im Notiztext und Referenzwege.

Offen bleiben D07 erst zur Pixel-Etappe, Importquelle und Buildwerkzeug erst bei Austausch/Verteilung sowie Inhaberangaben/Store/Marke. Keine bereits beschlossenen D09–D17 erneut vorlegen. Das ursprüngliche Screenshotproblem mit Seitenbildern gilt ohne konkreten reproduzierbaren Ablauf weiterhin als offen.
