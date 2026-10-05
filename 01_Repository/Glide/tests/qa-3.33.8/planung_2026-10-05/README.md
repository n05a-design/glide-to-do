# Ausbauprogramm Alltag, Komfort und Oberfläche – Planungsnachweis

05.10.2026 · App 3.33.8 unverändert, kein Versionswechsel · Linux/Tk 8.6, künstliche Daten · Ausgangsstand `fec3d54` (main nach PR #13)

Auftrag des Inhabers vom 05.10.2026: „Mehr Features, Mehr Quality of Life Updates, Mehr Unterstützung im Alltag und eine modernere Oberfläche genau wie in der Konkurrenz Analyse beschrieben“; Umfang und Arbeitsdokument daran anpassen. Reine Planungsarbeit: Code, Lieferstand und Datenformat sind unverändert.

## Ergebnis

- **Entwicklungsplan, neuer Abschnitt 4.3** mit 19 neuen Paketen, abgeleitet aus [Markt und Vorbilder](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md) (Abschnitte 1, 1.1, 3 und 6):
  - Oberfläche OB01–OB06
  - Komfort KO01–KO06
  - Alltag AU01–AU07
- **Bereits vorhandene Funktionen** wurden im Code geprüft und nicht neu geplant: Tagesbeginn/-abschluss, Wochenrückblick, Kapazität, Stundenraster, Jahres-Heatmap, mehrzeiliges Einfügen in Listen, Seitenleiste ein/aus, Startseitendichte, Wochenplanungsvorlage, Fokusmodus der Pinnwand.
- **Reihenfolge in drei Wellen.** Die beauftragte Kernfolge bleibt erhalten: Aktionskennungen → UX1 → G05/H-02 → G29/G31/G32.
- **Weitere Ergänzungen im Entwicklungsplan:** neue Ziele, die Risiken R12–R14, die Inhaberaufgabe I7 und drei offene Inhaberfragen (AU03, OB04, AU07).
- **Nachgeführte Dokumente:**
  - [Arbeitsrichtung](../../../docs/ARBEITSRICHTUNG.md): Auftrag und offene Fragen
  - [Übergabe](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md): nächste Schritte und I7
  - [Markt und Vorbilder](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md): Verweis auf die Einplanung

## Glide-Arbeitskopie

Zusätzlich ist eine Glide-Austauschdatei (`.glideexchange`, Austauschformat 1) entstanden, die der Inhaber in Glide importieren kann. Sie ist bewusst nicht versioniert, damit es kein zweites Planungsdokument gibt; maßgeblich bleibt der Entwicklungsplan.

Geprüft mit Glides eigenem Weg (`parse_exchange_document`, danach `apply_exchange_payload` in einem temporären `GLIDE_DATA_DIR`):
- 0 Fehler, 0 Warnungen, keine unbekannten Felder
- Inhalt: 1 Ordner, 6 Listen, 39 Aufgaben, 6 Langtexte, 9 Zwischenüberschriften, 49 Checklistenschritte, 6 Labels
- Alle Listen liegen im Ordner.

## Prüfung

CI-Grundstufe mit strengem Liefervergleich bestanden ([Ergebnis](ci/ergebnis.json)). Sie umfasst Stand-, Link- und Indexprüfung, Startprobe, Lieferstand bytegleich, Datenschutz und Ablagegröße. Eine Vollprüfung ist nicht nötig, weil kein ausführbarer Pfad geändert wurde.
