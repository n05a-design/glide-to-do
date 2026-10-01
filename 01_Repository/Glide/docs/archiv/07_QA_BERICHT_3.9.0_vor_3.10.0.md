# QA-Bericht – Glide 3.9.0

Stand 12.09.2026 · macOS · Python 3.14.5

Der vollständige unveränderte Ausgangslauf 3.8.0 war erfolgreich: zwölf Suiten, Syntax/Versionen/Dokumentation, zwei Analysen und reproduzierte Beispiel-/Releasedaten. [Ausgangsprotokoll](../tests/qa-3.9.0/oberflaeche/ausgang/ergebnis.json).

Die neue Suite `test_ui39.py` hat beide Themes, eingebettete Dropdowns, wiederholte Außerklicks, Tastatur, unveränderte Grabs, Fokusverlust, Zerstörung, kurze/hohe Dialoggrößen, Kopfzeile, Seitenleistenbreite/Speicherung und Menüparität bestanden. Die bisherigen Dialog- und Vorlagensuiten sind ebenfalls erfolgreich.

Die isolierte native macOS-Vorschau zeigte die kompakte Kopfzeile und den Aufgabenbereich. Die weitergehende Dialog-Sichtprüfung über das Computer-Use-Werkzeug blieb wegen wiederholter Zugriffszeitlimits unvollständig; daraus wird keine native Freigabe abgeleitet. Die eigenen Testdaten und die temporäre Vorschau-App wurden getrennt vom laufenden Nutzerbestand verwendet.

Im ersten Gesamtlauf bestanden elf der dreizehn Suiten. Zwei Befunde wurden danach korrigiert: eine alte Versionsassertion und ein beim Fensteraufbau bereits vorgemerktes Configure-Ereignis, das ein sofort geöffnetes Label-Popup schloss. Die betroffene UI-Suite wurde anschließend erfolgreich wiederholt. Dieser erste Lauf enthält Änderungen während der Ausführung und ist kein Abschlussnachweis.

Ein anschließender Lauf wurde während der Kachelprüfung zugunsten einer zusätzlich erkannten Tab-Fokuskorrektur abgebrochen und unter `tests/qa-3.9.0/oberflaeche/vor_tab_absicherung_abgebrochen` erhalten. Tab ermittelt sein Ziel nun erst nach Schließen der Popup-Fläche; der letzte Auswahlbereich kann dadurch kein zerstörtes Widget als Ziel erhalten.

**Der vollständige Abschlusslauf über den unveränderten finalen Quellstand war erfolgreich** (Abschluss 2026-09-12T19:12:04, Exitcode 0): 24 von 26 Schritten ausgeführt. Alle dreizehn Suiten, Syntax, Versions-/Dokumentprüfung, Fixtures, beide Analysen und Beispiel-/Release-Reproduktion sind erfolgreich. Übersprungen blieben ausschließlich plattformgebundene Screenshot-Erzeugung und manuelle Sichtprüfung.

[Abschlussprotokoll](../tests/qa-3.9.0/oberflaeche/abschluss/ergebnis.json) · [Geprüfte Quell-/Ressourcen-/Testprüfsummen](../tests/qa-3.9.0/gepruefter_quellstand_sha256.json).

Die startbare Datei `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.9.0.pyw` ist bytegleich zum kanonischen Quellstand. Ressourcen sind ebenfalls synchron. Nach diesem Lauf wurden keine Laufzeit- oder Testdateien verändert; nur der Ergebnistext und dessen Dokumentverweise wurden abgeschlossen.

Offen bleiben native Windows-Sichtprüfung, verschiedene DPI/Monitore, Screenreader, physischer Ruhezustand, reale Dock-/Taskleistenaufmerksamkeit, Langzeitbetrieb und signierte Installationspakete. Simulierte GUI-Ereignisse und Bildschirmhöhen sind keine Zielgeräteabnahme. Kein Schreiben in echte Nutzerdaten durch Tests.

[Bedien- und Datenvertrag 3.9](32_UI_UND_BEDIENUNG_3.9.0.md).
