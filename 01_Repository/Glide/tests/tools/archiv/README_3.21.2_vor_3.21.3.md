# Prüfwerkzeuge für Glide 3.21.2

Stand 14.09.2026 · Glide 3.21.2 · Aufgabenformat 15 · Einstellungen 2 · Vorlagen 2

Prüfläufe verwenden `TZ=Europe/Berlin`, wenn der Aufrufer keine Zone vorgibt: In UTC ist jeder Zeitzonenfehler unsichtbar, weil der Versatz null ist.

Alle Werkzeuge werden aus dem Repository gestartet. Windows-Nachweis:
Python 3.12.7, Tk 8.6.13. Werkzeuge benötigen eine grafische Sitzung, soweit sie
echte Tk-Fenster prüfen. Linux kann dafür Xvfb verwenden; das ersetzt keine
native Windows- oder macOS-Abnahme.

| Werkzeug | Zweck |
|---|---|
| `pruefen.py --modus voll --protokoll PFAD` | Achtzehn Suiten, Konsistenz, Analysen, Daten-Reproduktion, Bilder |
| `beispieldaten.py --ziel DATEI` | Demonstrationsbestand Format 14 erzeugen und importieren |
| `releasedaten.py --ziel DATEI --stichtag 2026-09-13` | Drei Release-Arbeitslisten für 3.14 mit Quellen und Codebelegen |
| `screenshots.py` | Linux/X11-Aufnahmen eigener Testfenster; Windows nutzt `pruefen.py --screenshots` oder die `--screenshots`-Option der Integrationssuiten |
| `symbolpruefung.py` | Private App-Schrift registrieren und tatsächliche Glyphenfamilien messen |
| `leistungspruefung.py --ziel DATEI.json` | Lokale synthetische Neudarstellungs-/Speichermessung |
| `dauerlauf.py --minuten 10 --aufgaben 4000 --ziel DATEI.json` | Dauer- und Belastungslauf: wachsende Callbacks, Undo-Stände, Speicher und Unversehrtheit nach dem Neuladen |
| `analyse_statisch.py`, `analyse_erreichbarkeit.py` | Quelltextbefunde und Referenzen, keine Laufzeitgarantie |

`dauerlauf.py` gehört bewusst nicht in den Standardlauf: Er misst nichts, was
in Sekunden sichtbar wird, sondern ob über Stunden etwas wächst, das nicht
wachsen darf. Zehn Minuten sind das Minimum, damit der 15-Sekunden-Takt der
Erinnerungen oft genug feuert; `--minuten 1 --aufgaben 500` ist ein Rauchtest
des Werkzeugs, kein Nachweis. Exitcode 1 bei einem Befund.

Der Release-Erzeuger aktualisiert Planungsfristen anhand des Stichtags, nicht
automatisch die Webquellen. Codeabgleich 13.09.2026; ältere Quellenabrufe stehen
in den Arbeitslisten. [QA](../../docs/07_QA_BERICHT.md),
[Historische Leistungsmessung 3.6](<../../docs/archiv/21_LEISTUNGSBERICHT_3.6.0_vor_Nachbesserung_2026-09-11.md>).

`test_features314.py` ergänzt Planung, Aufwand, Datenformat-14-Migration und Sicherungsfehler, gemeinsame Aktionen, Vorlagen/Backups/Exporte sowie Dialoge in beiden Themes.
