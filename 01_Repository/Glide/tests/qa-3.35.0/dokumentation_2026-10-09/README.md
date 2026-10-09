# Dokumentationsprüfung 3.35.0 (09.10.2026)

Stand 09.10.2026 · Glide 3.35.0 · Nachlauf ohne neue App-Version · Referenz-Mac, Python 3.14.5, Tk 9.0.3

Auftrag des Inhabers: „Eine komplette Überprüfung der lokalen Dokumentation, mit Stand, Inhalt, Aktualität und die veralteten Stände dementsprechend löschen.“ Geprüft wurden alle 44 Markdown-Dokumente außerhalb der Nachweisordner gegen Code, Prüfergebnisse und die Regeln der [Dokumentenpflege](../../../docs/DOKUMENTENPFLEGE.md). Vor den Löschungen wurde der Sprintstand eingecheckt (Commit `6098877`), damit Git jede Vorfassung trägt.

## Ergebnis

| Dokument | Befund | Änderung |
|---|---|---|
| Entwicklungsplan | Dutzende Aufgaben 3.33.9–3.33.18 noch „◐ … native Abnahme offen“, obwohl die Mac-Volläufe ab 3.33.18 sie abdecken; Paketbeschreibungen, Messerzählungen, Verträge und erledigte Aufgabenkarten als Zwischenstände; Inhaberentscheidungen doppelt (§11 und §15.3) | auf den Ist-Stand verdichtet (103 → 44 KB); menschliche Abnahme gesammelt unter I6; Entscheidungen E-S1–E-S8 in §11 zusammengeführt; Sprint als §14 |
| Übergabe | Startfassung und Bundle 3.33.18, 76 Suiten, „Bundle weiter 3.33.6“, Aufforderung zum Commit | Ist-Stand 3.35.0; Lieferweg und Prüffallstricke in den Prüfabschnitt; neue Lehren (sofort committen, OneDrive und Git/Signatur) |
| QA-Bericht | ausführliche Absätze bis 3.33.6 statt der sieben neuesten Versionen; Zeilen für 3.33.19–3.33.21 fehlten; Befund- und Nachlaufzeilen außerhalb der Aufbewahrung | sieben neueste ausführlich, ältere als Zeile (47 → 25 KB) |
| CHANGELOG | elf statt sieben Versionen ausführlich | 3.33.13–3.33.16 als Zeile |
| Analyse | Bestand und Funktionsanalyse vom 08.10.2026 nannten inzwischen geschlossene Lücken | fortgeschrieben auf 3.35.0; Oberflächenbefunde mit Stand; offene Inhaberfragen als Verweis auf den Plan |
| Markt und Vorbilder | Glide-Seite auf Stand 3.33.18 | auf 3.35.0; Sprintrecherche mit Umsetzungsstand |
| Manuelle Prüfung | Verweise auf Fotoordner außerhalb der Aufbewahrung, ⌘-Symbol aus der Zeit vor U01, keine Punkte für 3.33.19–3.35.0 | A27, B1i, D3, D4 neu; B1 auf den automatischen Stand |
| Arbeitsrichtung, Funktionen, Prüfplan, Produktregister, Veröffentlichung | einzelne Statusangaben („native Mac-Abnahme offen“, 170 Unit-Tests, FTS5 „geplant“) | nachgeführt; Paketprüfungen im Prüfplan aufsteigend geordnet |
| Wurzel-README, Probedaten, Archiv in 07 | „Aktuelles Paket 3.33.18“, Releaseplanung 3.33.18, Archiv „3.33.12 bis 3.33.17“ | auf 3.35.0 (in 07 nur die README, keine Lieferdatei) |

Unverändert: Showcase-README (bytegleiche Lieferkopie mit Prüfsumme), Belege der Nachweisordner (in `qa-3.33.18/seiten_2026-10-08` nur ein datierter Vermerk zu den entfernten Bildern), datierte Herstellerangaben.

## Ablage

- `scripts/pflege/ablage_kuerzen.py` kannte die Altersgrenze für Fensterbilder nur für Ordner `fenster/`; die Dokumentenpflege verlangt sie für jeden Bildordner. `tests/tools/ablagegroesse.py` prüft jetzt auch `fensterbilder/` und `screenshots/` (Werkzeugtest ergänzt). Dadurch entfielen 24 nie versionierte Bilder aus 3.33.17/3.33.18.
- Lokale Rohprotokolle der Nachweisordner 3.33.13–3.33.16 (nur `*.log`) nach der Versionsgrenze gelöscht.
- Eine leere Objektdatei in `.git/objects` (OneDrive) betraf nur einen lokalen Codex-Checkpoint, nicht die Zweige; aus dem Objektordner genommen.

## Prüfung

| Schritt | Ergebnis |
|---|---|
| Standprüfung | 53 aktive Dokumente, alle Standangaben passen zu 3.35.0 |
| Sprungmarken | alle `#`-Anker zwischen den Dokumenten gültig (eigene Prüfung nach dem Umnummerieren) |
| [CI-Grundstufe](ci/ergebnis.json) | Exitcode 0: Syntax, Versionen, Dokumentation, Fixtures, Werkzeug- und Unit-Tests, fünf Analysen, Startprobe, Lieferstand (07 bytegleich zu `src/glide`), Datenschutz, Ablagegröße, Synchronisation; Fremdcodeabgleich ohne Netz nur als Hinweis. App-Code und Lieferdateien in `07_Python-Versionen` gegenüber Commit `6098877` unverändert |
