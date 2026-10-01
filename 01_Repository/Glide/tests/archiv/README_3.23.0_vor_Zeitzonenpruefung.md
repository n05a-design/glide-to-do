# Prüfungen für Glide 3.22.0

Stand 18.09.2026 · Glide 3.23.0 · Aufgabenformat 16 · 27 Suiten und vier Analysen. Alle Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen.

Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.22.0/abschluss`.

Der Prüfstand setzt `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt. In UTC ist jeder Zeitzonenfehler unsichtbar, weil der Versatz null ist: Der `UNTIL`-Fehler aus 3.21.0 war in einer UTC-Vorabumgebung grün und fiel erst im macOS-Lauf auf.

## Was der Vollmodus umfasst

| Gruppe | Inhalt |
|---|---|
| Vorprüfungen | Syntax, Versionskonsistenz (VERSION, `APP_VERSION`, Hauptsuite, CHANGELOG), Dokumentationsindex mit Linkzielen, Fixtures samt historischen Referenzformaten |
| 27 Suiten | Kernfunktionen, Datenintegrität, Audit, Themes, UI, Vorlagen, Backups, Migration, Benachrichtigungen, Reiter/Pinnwand, Schnellerfassung und Filter, „Mein Tag“, Tabellenansicht, Planung und Aufwand, Tagesplanung, App-Backup, Druck/PDF, CSV-Import, Änderungsverlauf, Kalenderausgabe, Kalenderimport, Checkliste und seit 3.23 Designsystem, Anzeigemodi, Austauschformat und Pinnwandfläche |
| Drei Analysen | `analyse_statisch.py`, `analyse_erreichbarkeit.py` und seit 3.21.3 `standpruefung.py` (Standangaben und Formatstufen der Dokumente gegen VERSION und `DATA_SCHEMA_VERSION`) |
| Reproduktion | Beispieldaten und Releasedaten neu erzeugen und mit den Fixtures vergleichen; Bilder nur auf geeigneten Plattformen |

Übersprungen bleiben regelmäßig nur die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung; beide sind ausdrücklich manuelle Aufgaben.

## Gezielte Läufe

- `python3 tests/integration/test_ui39.py` – eingebettete Dropdowns, echte Außenklickereignisse, Tastatur, unveränderte modale Grabs, Dialoggrößen, Kopfzeile, Einstellungen, Seitenleiste und App-Aktionen.
- `python3 tests/integration/test_workspace310.py` – Reiter und Pinnwände, Referenzidentität, Einstellungen und native Tk-Ereignisse.
- `python3 tests/integration/test_features314.py` – Planung, Aufwand, Datenformat-14-Migration und Sicherungsfehler, gemeinsame Aktionen, Vorlagen, Backups, Exporte sowie Dialoge in beiden Themes.
- `python3 tests/tools/standpruefung.py` – nur die Standangaben und Formatstufen; läuft ohne Tk und in Sekunden.

Termine in Suiten liegen bewusst in der Zukunft. Ein Punkt mit Fälligkeit „heute 14:00“ und relativer Erinnerung wurde ab 13:30 Ortszeit mitten im Lauf ausgeliefert und veränderte den Bestand – zwei Suiten schlugen dadurch tageszeitabhängig fehl.

[Aktueller QA-Bericht](../docs/07_QA_BERICHT.md) · [Prüfplan und manuelle Grenzen](../docs/05_QA_TESTPLAN.md).
