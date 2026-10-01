# QA-Bericht – Glide 3.14.0

Stand 13.09.2026 · macOS · Python 3.14.5

Alle App-Importe verwenden temporäre `GLIDE_DATA_DIR`; echte Nutzerdaten wurden nicht als Testbestand geöffnet.

Vor den Änderungen bestand der 3.13-Ausgangsstand alle 17 Suiten und beide Analysen: [Ausgangslauf](../tests/qa-3.14.0/ausgang-3.13.0/ergebnis.json). Die neue [Planungssuite](../tests/integration/test_features314.py) ist separat erfolgreich gelaufen. Sie prüft Datenmigration, Sicherungsfehler, Eingabegrenzen, Mehrfachbearbeitung, Undo, Kopien, Artwechsel, Wiederholung, Vorlagen, Backup, Papierkorb, Exporte und echte Dialoge in Hell/Dunkel bei 780×640.

Der Gesamtlauf mit 18 Suiten und reproduzierten Beispiel-/Releasedaten wird nach dem abschließenden Dokumentationsabgleich ausgeführt. Sein Ergebnis wird hier ergänzt.

Native Windows-Abnahme, Screenreader, physisches Trackpad, DPI/Mehrmonitor, realer Ruhezustand und Langzeitbetrieb bleiben offen. Automatische Dialogprüfungen ersetzen keine vollständige Sichtabnahme. Ein erfolgreicher Quelltest ist keine signierte oder veröffentlichte Anwendung.
