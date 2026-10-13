# Wettbewerbs- und Open-Source-Analyse (13.10.2026)

Stand 13.10.2026 · Glide 3.39.0 · Nachlauf ohne neue App-Version · Referenz-Mac, nur Lesen und Dokumentation, kein GUI-Lauf

Auftrag des Inhabers vom 12./13.10.2026: Bestandsaufnahme von Glide, Wettbewerbs- und Marktrecherche, technische Analyse ausgewählter Open-Source-Repositories, Featurematrix, Gap-Analyse, Feature-Backlog und Feature-Pakete, Roadmap und Fortschreibung der bestehenden Dokumentation. Ergebnis sind Vorschläge; keine Funktion ist ausgewählt, keine Produktionsdatei geändert. Fortsetzung am selben Tag auf „weiter“: Vorprüfungen zur Umsetzungsreife (Phase F) mit zwei neu belegten Fehlern (A28, A29) und einer unabhängigen Gegenrechnung des ICS-Serienrechners.

## Ergebnisse

| Inhalt | Ort |
|---|---|
| Bestandsaufnahme mit Statuswerten, technische Einschränkungen, Gap-Analyse, Einordnung | [Analyse §8](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#8-bestandsaufnahme-und-gap-analyse-13102026) |
| Neue Befunde Dokumentation ↔ Code A24–A29 | [Analyse §3](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#3-abgleich-dokumentation--implementierung) |
| Steckbriefe, Codeanalyse mit Fundstellen, Übertragbarkeit, Lizenzen, Featurematrix nach Funktionsbereichen, Bewertung der Entwicklungsrichtungen, Quellen | [Markt und Vorbilder §9](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md#9-wettbewerbs--und-open-source-analyse-13102026) |
| Backlog WA-01–WA-18, Feature-Pakete FP-00–FP-07, Entscheidungsvorlagen E-W1–E-W7, Architekturalternativen AE-1–AE-7, Reihenfolge, Umsetzungsreife, QA-Strategie, Vorprüfungen (§16.10) | [Entwicklungsplan §16](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#16-vorschläge-aus-wettbewerbs--und-open-source-analyse-13102026) |

Geänderte Dokumente: Analyse, Markt und Vorbilder, Entwicklungsplan, Übergabe (ein Eintrag in §6), README der Arbeitsvorbereitung, Architektur §1 (A24). Berichtigt: A24 (Plattformangabe der Architektur), A25 (Inspektor, OB02/OB03 und Animation in Markt §1/§4/§4.1).

## Vorgehen

- Glide: Code am Commit `c38d960` gelesen (`app.pyw`, Begleitmodule, Datenmodell `new_item`, `SavedFilters`, `ItemWorkspace`, Rückgängig-Weg, Wiederholungsrechner); Dokumente nach der Lesereihenfolge aus `CLAUDE.md`.
- Fremdprojekte: lokale AFFiNE-Kopie (Canary 0.27.5) und flache Klone vom 13.10.2026 in einem temporären Ordner außerhalb der Ablage – AppFlowy `5cf3a36`, Super Productivity `c4c6959`, Vikunja `4e2a899`, ai-notion-clone `c68ece5`, Taskwarrior (Standardzweig). Nur gelesen; nichts installiert, gebaut oder ausgeführt; kein Fremdcode übernommen. Lizenz und Aktivität über die GitHub-API.
- Herstellerseiten und Berichte Dritter mit Abrufdatum; Dritte und Unbestätigtes sind im Dokument gekennzeichnet.

## Vorprüfungen (Phase F)

| Werkzeug (in diesem Ordner) | Ergebnis |
|---|---|
| [gegenprobe_rrule.py](gegenprobe_rrule.py) → [gegenprobe_rrule.json](gegenprobe_rrule.json) | eigenständige RFC-5545-Tag-für-Tag-Abtastung gegen `ics_recurrence.dates`: 11.192 Regel-/Startkombinationen aus drei Zufallsreihen, 0 Abweichungen; 142 Fälle mit UNTIL vor DTSTART ausgenommen (Glide: kein Termin) |
| [probe_wiederholung.py](probe_wiederholung.py) → [probe_wiederholung.json](probe_wiederholung.json) | Schnelleingabe: 10 von 14 Wiederholungsangaben teilweise oder falsch gedeutet (A29). ICS-Ausgabe: 4 von 5 Monatsende-/Schaltjahrfällen weichen von Glides Folge ab, Korrekturvorschlag 5 von 5 gleich (A28) |

Beide Werkzeuge nur Standardbibliothek, ohne Tk, ohne Schreibzugriff; Aufruf aus `01_Repository/Glide` mit `python3 -B -I <Werkzeug> src/glide`. Weitere Codeprüfungen (Rückgängig-Inventar, Einstellungsnormalisierung, Austauschweg) mit Fundstellen im [Entwicklungsplan §16.10](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#1610-vorprüfungen-zur-umsetzungsreife-13102026).

## Prüfung

Siehe [ergebnis.json](ergebnis.json). Ausgeführt wurden ausschließlich Prüfungen ohne Tk-Fenster: Standprüfung, Dokumentationsindex und Links, Anker der geänderten Dokumente, Werkzeugtests, Synchronisationswächter, Ablagegröße, Syntaxprüfung, Benutzerpfadsuche in den geänderten Dateien und SHA-256 von App und Lieferstand. Bewusst nicht ausgeführt: CI-Grundstufe mit Startprobe, weil laut Übergabe während der nativen 3.39.0-Matrix keine lokalen GUI-Läufe stattfinden sollen; sie folgt beim nächsten Commit nach Übergabe §5.

Die verbleibenden Befunde der Standprüfung betreffen ausschließlich die unversionierten Fremddateien `Apple Design Skill.md` und `skills-main/` im lokalen Arbeitsordner (bekannt, Übergabe §6); sie sind nicht Teil des Projektprüfstands.
