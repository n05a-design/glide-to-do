# Prüfungen für Glide 3.13.0

Stand 12.09.2026. Alle Tests setzen vor dem App-Import einen temporären `GLIDE_DATA_DIR`; echte Nutzerdaten sind ausgeschlossen.

Vollständiger Lauf: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.13.0/abschluss`.

Siebzehn Suiten prüfen Kernfunktionen, Datenintegrität, Themes, UI, Vorlagen, Backups, Migration, Benachrichtigungen, Reiter/Pinnwand, Schnellerfassung/Filter, „Mein Tag“ und die Tabellenansicht. Hinzu kommen Syntax-/Versions-/Dokumentprüfung, historische Fixtures, zwei Analysen und reproduzierte Beispiel-/Releasedaten.

Gezielt: `python3 tests/integration/test_ui39.py` für eingebettete Dropdowns, echte Außenklickereignisse, Tastatur, unveränderte modale Grabs, Dialoggrößen, Kopfzeile, Einstellungen, Seitenleiste und App-Aktionen.

[Aktueller QA-Bericht](../docs/07_QA_BERICHT.md) · [Prüfplan und manuelle Grenzen](../docs/05_QA_TESTPLAN.md).

`test_workspace310.py` prüft Reiter und Pinnwände, Referenzidentität, Einstellungen und native Tk-Ereignisse.
