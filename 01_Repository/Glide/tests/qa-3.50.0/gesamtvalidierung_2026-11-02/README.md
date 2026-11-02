# Gesamtvalidierung nach Claudes UI-Runde – Glide 3.50.0, 02.11.2026

Nutzerauftrag: Dokumentation und Dateien nach Funktionen, Features und tatsächlichem Stand überprüfen, App-Codebasis validieren, committen und pushen. [Maßgeblicher Plan §21.51](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2151-gesamtvalidierung-nach-claudes-ui-runde).

## Umfang und Befunde

Die gewählten Produktfunktionen und UI-Nachläufe sind vorhanden. [Implementierungsabgleich](umfangsabgleich.json) ordnet die jüngsten Wünsche konkreten Klassen/Methoden und ihren ursprünglichen Nachweisen zu. Er ersetzt keine Bedienprüfung; dafür läuft die vollständige eingefrorene Regression. Datenformat 26, Einstellungen 2 und Version 3.50.0 bleiben erhalten.

„Alle begonnenen Arbeiten fertig“ wäre weiterhin falsch: WA-32/39 (appweite Gestaltung/Komponenten), WA-36 (Performance), WA-37/38/40 (Caller-/Fehlerklassifikation) sind teilweise; WA-46 (SBOM) sowie WA-49/50 (Initialisierung/Modulbudget) fehlen; WA-41-Ursachen sind offen. Diese bestehenden technischen Vorhaben bleiben im Plan, statt aus grünen Tests als erledigt abgeleitet zu werden. Ungewählte Optionen und die nach D58 zurückgestellte Readerabnahme sind keine begonnenen aktuellen UI-Funktionen.

Die aktiven Einstiege nannten noch den älteren Oberflächenstand, während Labels in der Kartenecke, schmale Hinweisflächen, Werkzeugabstand, Pinnwandgrund und Seitenfuß bereits implementiert waren. Handbuch, Index, Übergabe, Arbeitsrichtung und README werden auf denselben aktuellen Nachweis ausgerichtet; frühere QA-Berichte behalten ihre damaligen Eingaben.

## Abhängigkeiten

[PyPI-Abgleich](abhaengigkeiten.json) aller neun gepinnten Bau-/Vendorpakete: sechs Pins entsprechen der neuesten veröffentlichten Version. Neuere Fassungen sind [hooks-contrib 2026.9](https://pypi.org/project/pyinstaller-hooks-contrib/), [setuptools 84.2.1](https://pypi.org/project/setuptools/) und [tkinterdnd2 0.7.0](https://pypi.org/project/tkinterdnd2/). Kein ungeprüfter Pin-/Vendorwechsel in einer Bestandsvalidierung; Übernahme braucht Änderungsvergleich, Originalhashes und native Bau-/Start-/DnD-Nachweise. „Alle Abhängigkeiten neueste Fassung“ wird nicht behauptet.

## Validierung

- [Baseline-Grundstufe](baseline_grundstufe.json): 19 Schritte einschließlich Syntax, Versionen, Dokumentlinks, zweimal Fachlogik, Werkzeugtests, fünf Analysen, Startprobe, strengem Python-/Vendorabgleich grün.
- [Eingefrorene vollständige native Prüfung](vollpruefung.json): läuft mit Python 3.14.5 und eigener Tk 9.1, einschließlich nativer Zugangsbindungen, synthetischen Daten und Prozess-/Integritätswächter. Der erste Lauf stoppte korrekt an `test_logo330`: überholte feste Mindesthöhe 40 px gegenüber 38 px im ausdrücklich verkleinerten Kopf. [Rotbeleg](vollpruefung_vorlauf.json) bleibt erhalten. Der Test wird auf den tatsächlichen B05-Vertrag (Unterzeilen-Grundlinie und Seitenverhältnis, zusätzlich zu Fluchten/Kontrast) ausgerichtet; keine Appänderung oder bloße Herabsetzung einer Zahl. Die gezielte Suite ist grün; eine isolierte 4-px-Positionsmutante scheitert ausdrücklich an der neuen Grundlinienprüfung ([Prüfvertrag](logo_pruefvertrag.json)). Ein neuer vollständiger Lauf folgt; keine Menschen-/Readerabnahme daraus ableiten.
- [Aktuelle Grundstufe](grundstufe.json), [Lieferstand](lieferstand.json), [GitHub-Prüfungen](github.json), [Abschluss](ergebnis.json).

Echte Nutzdaten und Wiederanlaufsperre werden nicht verändert. Prüfkopie/Rohlogs bleiben lokal außerhalb OneDrive. Nur bereinigte Berichte werden versioniert. Bereits vorgefundene lokale `.local`-/Altnachweise unter `qa-3.43.1` bleiben außerhalb des Commits.

## Lieferung und Grenzen

Python-Fassung ist bytegleich. Installierte Mac-App entspricht Quelle `672ffadd…`; 463 Dateien und Ad-hoc-Signatur unabhängig abgeglichen. Der ursprüngliche öffentliche Windows-Stand enthält die jüngsten UI-Nachläufe noch nicht; nativer CI-Bau und konkrete Lieferung werden getrennt nachgewiesen. Ursprüngliche öffentliche Archive bleiben an ihre bisherigen Hashes gebunden. Kein neuer öffentlicher Release und keine automatische Zusammenführung des Prüfbranches.
