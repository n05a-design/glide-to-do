# Prüfwerkzeuge für Glide 3.7.0

Alle Werkzeuge werden aus dem Repository gestartet. Windows-Nachweis:
Python 3.12.7, Tk 8.6.13. Werkzeuge benötigen eine grafische Sitzung, soweit sie
echte Tk-Fenster prüfen. Linux kann dafür Xvfb verwenden; das ersetzt keine
native Windows- oder macOS-Abnahme.

| Werkzeug | Zweck |
|---|---|
| `pruefen.py --modus voll --protokoll PFAD` | Zehn Suiten, Konsistenz, Analysen, Daten-Reproduktion, Bilder |
| `beispieldaten.py --ziel DATEI` | Demonstrationsbestand Format 12 erzeugen und importieren |
| `releasedaten.py --ziel DATEI --stichtag 2026-09-07` | Drei Release-Arbeitslisten für 3.7 mit Quellen und Codebelegen |
| `screenshots.py` | Linux/X11-Aufnahmen eigener Testfenster; Windows nutzt `pruefen.py --screenshots` oder die `--screenshots`-Option der Integrationssuiten |
| `symbolpruefung.py` | Private App-Schrift registrieren und tatsächliche Glyphenfamilien messen |
| `leistungspruefung.py --ziel DATEI.json` | Lokale synthetische Neudarstellungs-/Speichermessung |
| `analyse_statisch.py`, `analyse_erreichbarkeit.py` | Quelltextbefunde und Referenzen, keine Laufzeitgarantie |

Der Release-Erzeuger aktualisiert Planungsfristen anhand des Stichtags, nicht
automatisch die Webquellen. Codeabgleich 07.09.2026; ältere Quellenabrufe stehen
in den Arbeitslisten. [QA](../../docs/07_QA_BERICHT.md),
[Historische Leistungsmessung 3.6](../../docs/21_LEISTUNGSBERICHT_3.6.0.md).

