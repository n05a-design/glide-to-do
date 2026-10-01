# QA-Bericht – Glide 3.15.0

Stand 13.09.2026 · macOS · Python 3.14.5

Alle App-Importe verwenden temporäre `GLIDE_DATA_DIR`; echte Nutzerdaten wurden nicht als Testbestand geöffnet.

Der 3.14-Stand ist mit 18 Suiten und Exitcode 0 abgenommen: [Abschlusslauf 3.14](../tests/qa-3.14.0/abschluss/ergebnis.json).

Für 3.15 sind alle neunzehn Suiten, beide statischen Analysen sowie Beispiel- und Releaseabgleich in einer Linux-Vorabumgebung (Python 3.12, Tk 8.6 unter Xvfb) mit Exitcode 0 gelaufen; ausgenommen blieben dort nur der Dokumentationsindex und eine nicht mitkopierte Referenzdatei. Die neue [Planungsansichtssuite](../tests/integration/test_features315.py) prüft Rechenregeln und Grenzwerte, Normalisierung und Rückfall der Tageskapazität, Menge, Reihenfolge, Zähler und Leertext der Tagesplanung, Tageswechsel, Such- und Offenfilter, Punktaktionen mit Rückgängig, ungültige Bearbeitungstage, Serienvorrücken, die filterabhängige Tabellensumme, die Startseitenzeile und den Einstellungsdialog in Hell/Dunkel bei 780×640.

Drei bestehende Suiten wurden an die neue Systemzeile und die neue Startseitenaktion angepasst: Reihenfolge und Symbolzahl der Seitenleiste in `test_glide.py` und `test_ui_polish36.py`, die Liste der Schnellzugriffe in `test_ui_polish36.py`. Vorlagenkatalog sowie Beispiel- und Releasedaten wurden neu erzeugt und tragen `app_version` 3.15.0; die Vorfassung des Katalogs liegt im Ressourcenarchiv.

Der maßgebliche Abschlusslauf auf macOS mit Python 3.14.5 steht noch aus:
`python3 tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.15.0/abschluss`. Sein Ergebnis wird hier ergänzt.

Zur Vorgeschichte des 3.14-Nachweises: Ein erster Lauf war mit Exitcode 1 abgebrochen, weil `FORM_KEYS` in `tests/integration/test_datenintegritaet.py` noch den 3.13-Feldsatz erwartete, während die Punktmaske bereits `planned_date` und `estimated_minutes` zurückgibt. Die Erwartungsliste wurde ergänzt, der Anwendungscode blieb unverändert; der Wiederholungslauf mit achtzehn Suiten bestand mit Exitcode 0.

Eine Portabilitätsgrenze der Vorabumgebung ist bekannt: `test_glide.py` erwartet die Beispieldatei als `Glide_Beispieldaten.glidebackup`, im Repository liegt sie als `glide_beispieldaten.glidebackup`. Unter macOS und Windows ist das gleichbedeutend, unter Linux nicht.

Native Windows-Abnahme, Screenreader, physisches Trackpad, DPI/Mehrmonitor, realer Ruhezustand und Langzeitbetrieb bleiben offen. Automatische Dialogprüfungen ersetzen keine vollständige Sichtabnahme. Ein erfolgreicher Quelltest ist keine signierte oder veröffentlichte Anwendung.
