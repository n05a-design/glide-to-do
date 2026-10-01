# QA-Bericht – Glide 3.14.0

Stand 13.09.2026 · macOS · Python 3.14.5

Alle App-Importe verwenden temporäre `GLIDE_DATA_DIR`; echte Nutzerdaten wurden nicht als Testbestand geöffnet.

Vor den Änderungen bestand der 3.13-Ausgangsstand alle 17 Suiten und beide Analysen: [Ausgangslauf](../tests/qa-3.14.0/ausgang-3.13.0/ergebnis.json). Die neue [Planungssuite](../tests/integration/test_features314.py) ist separat erfolgreich gelaufen. Sie prüft Datenmigration, Sicherungsfehler, Eingabegrenzen, Mehrfachbearbeitung, Undo, Kopien, Artwechsel, Wiederholung, Vorlagen, Backup, Papierkorb, Exporte und echte Dialoge in Hell/Dunkel bei 780×640.

Der Gesamtlauf mit 18 Suiten und reproduzierten Beispiel-/Releasedaten bestand am 13.09.2026 mit Exitcode 0: [Abschlusslauf](../tests/qa-3.14.0/abschluss/ergebnis.json). Enthalten sind Syntax-, Versions-, Dokumentations- und Fixtureprüfung, achtzehn Suiten, zwei statische Analysen sowie Beispiel- und Releaseabgleich. Übersprungen blieben allein die plattformgebundene Screenshot-Erzeugung und die Sichtprüfung. Automatisiert ist 3.14.0 damit abgenommen.

Ein erster Lauf desselben Tages war mit Exitcode 1 abgebrochen, weil `FORM_KEYS` in `tests/integration/test_datenintegritaet.py` noch den 3.13-Feldsatz erwartete, während die Punktmaske bereits `planned_date` und `estimated_minutes` zurückgibt. Die Erwartungsliste wurde ergänzt, der Anwendungscode blieb unverändert; der Wiederholungslauf ist der oben genannte Nachweis.

Reproduzierbar mit: `python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.14.0/abschluss`

Native Windows-Abnahme, Screenreader, physisches Trackpad, DPI/Mehrmonitor, realer Ruhezustand und Langzeitbetrieb bleiben offen. Automatische Dialogprüfungen ersetzen keine vollständige Sichtabnahme. Ein erfolgreicher Quelltest ist keine signierte oder veröffentlichte Anwendung.
