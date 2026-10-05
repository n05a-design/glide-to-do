# Regeln für die Dokumentenpflege

Stand 05.10.2026 · Glide 3.33.8 · Datenformat 20

Gilt seit dem Auftrag des Inhabers vom 03.10.2026 („jetzt wird auch mal wieder gelöscht anstatt immer nur archiviert und `_Z` zu schreiben“) und ersetzt alle früheren Archivierungsregeln.

## Grundsätze

- **Ein Thema, ein Dokument.** Beschreiben zwei Dokumente dasselbe, werden sie zusammengeführt; das überholte wird gelöscht, nicht archiviert. Git trägt jede Vorfassung (`git log --follow <Datei>`).
- **Fortschreiben statt kopieren.** Keine Versionskopie, keine `archiv/`-Ordner, keine `_Z`-Vormerkung für Dokumente. Dateinamen tragen kein Datum und keine Version; der Stand steht in der Standzeile.
- **Erledigtes kennzeichnen statt aufbewahren.** Aufgaben tragen im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) ihre Marke (✅ erledigt mit Version, ◐ teilweise, ▶ beauftragt, ○ offen, ◇ Zukunft, ✕ bewusst nicht). Abgeschlossene Versionen stehen im [QA-Bericht](07_QA_BERICHT.md) und im CHANGELOG.
- **Code-relevant oder aktuell.** Behalten wird, was den heutigen Code, seine Prüfung, Daten, Entscheidungen oder die offene Planung beschreibt. Recherchen und Zwischenstände werden nach Übernahme ihrer gültigen Ergebnisse gelöscht.
- **Aufbewahrung:** Archive und Nachweise nur der sieben neuesten Versionen (`07_Python-Versionen/Archiv`, `tests/qa-<Version>`, Releaseplanungen; je Datenformat bleibt eine Releaseplanung als Lesbarkeitsbeleg), Fensterbilder nur der drei neuesten, Rohprotokolle (`*.log`) nie. `scripts/pflege/ablage_kuerzen.py` kürzt, die CI-Grundstufe prüft (Schritt „Ablagegröße“).
- **Leere Ordner** und Ordner, die nur README und Archiv enthalten, werden aufgelöst.
- **Belege bleiben Belege:** Nutzeraufträge, Messwerte und Prüfergebnisse innerhalb der Aufbewahrung werden nicht umetikettiert oder nachträglich geändert.

## Dokumente und ihre Zuständigkeit

| Thema | Einziges Dokument |
|---|---|
| Einstieg, Stand, Regeln, nächste Schritte | `00_Arbeitsvorbereitung/Glide_Uebergabe.md` |
| Aufgaben, Backlog, Stufen, Ziele | `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md` |
| Markt und Vorbilder | `00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md` |
| Manuelle Prüfung (Mac, Windows, Linux) | `00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md` |
| Entscheidungen und Arbeitsablauf | [ARBEITSRICHTUNG.md](ARBEITSRICHTUNG.md) |
| Produktgrenzen und Prinzipien | [01_PRODUCT_CONSTRAINTS.md](01_PRODUCT_CONSTRAINTS.md) |
| Architektur, Performance-Regeln, Tk-Fallstricke | [02_ARCHITECTURE.md](02_ARCHITECTURE.md) |
| Prüfplan | [05_QA_TESTPLAN.md](05_QA_TESTPLAN.md) |
| Datenformat, Backups, Austauschformat | [06_DATA_BACKUP_MIGRATION.md](06_DATA_BACKUP_MIGRATION.md) |
| Geprüfter Stand | [07_QA_BERICHT.md](07_QA_BERICHT.md) |
| Veröffentlichung, Lizenz, Signierung, Store | [10_VEROEFFENTLICHUNG.md](10_VEROEFFENTLICHUNG.md) |
| Verhalten der Funktionen | [20_FUNKTIONEN.md](20_FUNKTIONEN.md) |
| Vorlagen in der Praxis | [27_VORLAGEN_PRAXISANLEITUNG.md](27_VORLAGEN_PRAXISANLEITUNG.md) |
| Einzelentscheidungen mit eigenem Gegenstand | `decisions/` (Produktregister, tkdnd, Arbeitsbegleiter, Gruppe/Ordner/Überschrift, Systembenachrichtigungen) |
| Fehlerdiagnosen bis zur Übernahme ihrer Ergebnisse | `diagnosen/` (Logo-Kantenglättung); danach löschen |
| Änderungsverlauf | `CHANGELOG.md` (sieben neueste Versionen ausführlich, ältere als Zeile) |

Neue Dokumente unter `docs/` nur, wenn kein bestehendes das Thema trägt; sie gehören in den [Index](00_INDEX.md).

## Pflege bei jeder Runde

- Standzeile („Stand TT.MM.JJJJ · Glide X.Y.Z …“) und Inhalt zusammen nachführen; `versionswechsel.py` hebt die Standzeilen, ersetzt aber keinen inhaltlichen Abgleich von Status, Entscheidungen und Prüfgrenzen.
- Neue Funktion: Abschnitt in [Funktionen](20_FUNKTIONEN.md), Marke im Entwicklungsplan, Zeile im QA-Bericht, Eintrag im CHANGELOG. Keine eigene Vertragsdatei je Version.
- Vor dem Commit `python3 -B tests/tools/ci_grundstufe.py` (Stand, Links, Index, Datenschutz, Ablagegröße).
- Produktionskommentare erklären Invarianten, technische Gründe und Plattformbesonderheiten; Auftragsnummern und Entwicklungserzählungen gehören ins CHANGELOG. Eine reine Kommentarbereinigung lässt den Syntaxbaum unverändert.

## Was die Standprüfung erzwingt

`tests/tools/standpruefung.py` (Regeln R1–R14) prüft alle aktiven Markdown-Dokumente: Standzeile mit der aktuellen Version, Formatstufen gegen den Code, bekannte überholte Aussagen, vollständige Modullisten, erreichbare relative Links, aktuelle Titel und erste Vollprüfungsaufrufe, Suitezahl in Standzeilen. Dokumente mit Version oder Datum im Namen gelten als festgeschrieben; seit 03.10.2026 gibt es unter den gepflegten Dokumenten keine mehr.
