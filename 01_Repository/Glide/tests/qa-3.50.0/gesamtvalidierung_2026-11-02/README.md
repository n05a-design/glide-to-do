# Gesamtvalidierung nach Claudes UI-Runde – Glide 3.50.0, 02.11.2026

Nutzerauftrag: Dokumentation und Dateien nach Funktionen, Features und tatsächlichem Stand überprüfen, App-Codebasis validieren, committen und pushen. [Maßgeblicher Plan §21.51](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2151-gesamtvalidierung-nach-claudes-ui-runde).

## Umfang und Befunde

Die gewählten Produktfunktionen und UI-Nachläufe sind vorhanden. [Implementierungsabgleich](umfangsabgleich.json) ordnet die jüngsten Wünsche konkreten Klassen/Methoden und ihren ursprünglichen Nachweisen zu. Er ersetzt keine Bedienprüfung; dafür läuft die vollständige eingefrorene Regression. Datenformat 26, Einstellungen 2 und Version 3.50.0 bleiben erhalten.

„Alle begonnenen Arbeiten fertig“ wäre weiterhin falsch: WA-32/39 (appweite Gestaltung/Komponenten), WA-36 (Performance), WA-37/38/40 (Caller-/Fehlerklassifikation) sind teilweise; WA-46 (SBOM) sowie WA-49/50 (Initialisierung/Modulbudget) fehlen; WA-41-Ursachen sind offen. Diese bestehenden technischen Vorhaben bleiben im Plan, statt aus grünen Tests als erledigt abgeleitet zu werden. Ungewählte Optionen und die nach D58 zurückgestellte Readerabnahme sind keine begonnenen aktuellen UI-Funktionen.

Die aktiven Einstiege nannten noch den älteren Oberflächenstand, während Labels in der Kartenecke, schmale Hinweisflächen, Werkzeugabstand, Pinnwandgrund und Seitenfuß bereits implementiert waren. Zusätzlich behauptete Plan §21.48 noch „Mac-App nicht neu gebaut“, obwohl dessen QA-Ordner bereits native Bau-/Start-/Installationsbelege enthält; diese Lieferangabe ist berichtigt. Handbuch, Index, Übergabe, Arbeitsrichtung und README werden auf denselben aktuellen Nachweis ausgerichtet; frühere QA-Berichte behalten ihre damaligen Eingaben.

## Abhängigkeiten

[PyPI-Abgleich](abhaengigkeiten.json) aller neun gepinnten Bau-/Vendorpakete: sechs Pins entsprechen der neuesten veröffentlichten Version. Neuere Fassungen sind [hooks-contrib 2026.9](https://pypi.org/project/pyinstaller-hooks-contrib/), [setuptools 84.2.1](https://pypi.org/project/setuptools/) und [tkinterdnd2 0.7.0](https://pypi.org/project/tkinterdnd2/). Kein ungeprüfter Pin-/Vendorwechsel in einer Bestandsvalidierung; Übernahme braucht Änderungsvergleich, Originalhashes und native Bau-/Start-/DnD-Nachweise. „Alle Abhängigkeiten neueste Fassung“ wird nicht behauptet.

## Validierung

- [Baseline-Grundstufe](baseline_grundstufe.json): 19 Schritte einschließlich Syntax, Versionen, Dokumentlinks, zweimal Fachlogik, Werkzeugtests, fünf Analysen, Startprobe, strengem Python-/Vendorabgleich grün.
- [Eingefrorene vollständige native Prüfung](vollpruefung.json): mit Python 3.14.5 und eigener Tk 9.1 abgeschlossen: 126 automatisierte Schritte einschließlich aller 108 Integrationssuiten grün. Zwei übrige Zeilen sind Linux-spezifische Screenshots bzw. menschliche Sichtabnahme. Native Zugangsbindungen, synthetische Daten und Prozess-/Integritätswächter aktiv; [Integritätsbericht](integritaet.json) ohne Quell-/Dokumentänderung und [Einfrierabgleich](einfrierabgleich.json) bytegleich. Der erste Lauf stoppte korrekt an `test_logo330`: überholte feste Mindesthöhe 40 px gegenüber 38 px im ausdrücklich verkleinerten Kopf. [Rotbeleg](vollpruefung_vorlauf.json) bleibt erhalten. Der Test wird auf den tatsächlichen B05-Vertrag (Unterzeilen-Grundlinie und Seitenverhältnis, zusätzlich zu Fluchten/Kontrast) ausgerichtet; keine Appänderung oder bloße Herabsetzung einer Zahl. Die gezielte Suite ist grün; eine isolierte 4-px-Positionsmutante scheitert ausdrücklich an der neuen Grundlinienprüfung ([Prüfvertrag](logo_pruefvertrag.json)). Der anschließende vollständige Lauf ist grün; keine Menschen-/Readerabnahme daraus ableiten.
- [Aktuelle Grundstufe](grundstufe.json), [Lieferstand](lieferstand.json), [GitHub-Prüfungen](github.json), [Abschluss](ergebnis.json).

Echte Nutzdaten und Wiederanlaufsperre werden nicht verändert. Prüfkopie/Rohlogs bleiben lokal außerhalb OneDrive. Nur bereinigte Berichte werden versioniert. Bereits vorgefundene lokale `.local`-/Altnachweise unter `qa-3.43.1` bleiben außerhalb des Commits.

## Lieferung und Grenzen

Python-Fassung ist bytegleich. Installierte Mac-App entspricht nach dem Startseitenfix Quelle `067e683b…` (neu gebaut, Vorfassung `Glide-vor-Startseitenlayout-20261102.app` erhalten); [463 Dateien und Ad-hoc-Signatur](mac_abgleich.json) unabhängig abgeglichen, [Bau](mac_bau.json), [Start des Baus](mac_start_bau.json). [Erneuter isolierter Start](mac_start_installiert.json) mit blockiertem externem Python, Bau-/Runtimeablage und Projekt grün, einschließlich nativem Accessibility-Kernablauf. Der ursprüngliche öffentliche Windows-Stand enthält die jüngsten UI-Nachläufe nicht; das eigenständige Windows-Paket aus GitHub-Lauf 41525034740 (Quelle `067e683b…`, 104 Dateien gegen Bauinventar, Startprobe mit gesperrtem externem Python grün) liegt getrennt als Kandidat unter `build/windows/Kandidaten/Glide-3.50.0-gesamtvalidierung` ([Lieferstand](lieferstand.json)). Ursprüngliche öffentliche Archive bleiben an ihre bisherigen Hashes gebunden. Kein neuer öffentlicher Release und keine automatische Zusammenführung des Prüfbranches.

**Pfadvorlauf:** Der zweite lokale Vollstart stoppte in Markdown-Export-Unit-Tests, weil der zusätzlich verschachtelte Prüf-/Temp-Pfad die bewusst unterstützte Ausgabeortgrenze von 130 Zeichen überschritt. [Beleg](vollpruefung_pfadvorlauf.json). Keine Änderung der Produktgrenze oder Lockerung der Tests; der Nachlauf verwendet wie vorgesehen eine kurze lokale Prüfablage außerhalb OneDrive.

**Native Sichtbelege:** [Fensterprobe](sichtprobe.py) und [Ergebnis](sichtpruefung.json): Seite mit grünem Ecklabel und einzeiligem Speicherstatus sowie Liste mit rechtem Ansichtsumschalter und vollständig sichtbaren Zeilenaktionen. Eigene synthetische Fenster per Fenster-ID aufgenommen und angesehen; fremde OS-Überlagerungen werden dabei nicht erfasst. Dies ersetzt keine menschliche Bedien-/DPI-/Mehrmonitorabnahme. PNGs unter `fensterbilder/`.

**Mac-Archiv:** [Separates Kandidatenarchiv](mac_archiv.json) des tatsächlich installierten Bundles: 463 Dateien, 30 Symlinks und Dateimodi streng geprüft. Ursprüngliches öffentliches TAR unverändert. [Zusätzlicher nativer GitHub-Bau](mac_ci.json) grün; alle 208 Eingaben entsprechen Git einschließlich der Checkout-Regeln. Zehn lokale CRLF/LF-Unterschiede explizit erfasst, deshalb kein identischer Paketbyte-Stand behauptet.

## Abschluss (Quelle `067e683b…`, Commit `47bfced`)

- [GitHub-Lauf 41525034740](github.json) vollständig grün: Grundstufe, Vollprüfung Linux/Xvfb und Windows mit eigener Tk 9.1, eigenständiges Windows-Paket. Die vorherigen roten Läufe (Linux-Timeout in `test_arbeitsmodi`, Windows `test_logo330`) sind damit behoben: Ursache des Linux-Hängers war der [1-px-Zyklus der Startseite](../startseitenlayout_2026-11-02/README.md), die 40-px-Logogrenze war überholt.
- Mac nativ auf `067e683b…`: 21 betroffene Suiten grün (Startseite, Tag, Woche, Planen, Heute, beide Logo-Suiten, Fenster, Fläche/15 %, Arbeitsmodi mit allen 43 Fällen, UI-Paket, Kopf, Pinnwand, Kartenfuß, Mindestgröße). Der eingefrorene Volllauf 126/126 oben gehört zu `672ffadd…`.
- [Aktuelle Grundstufe](grundstufe.json) bestanden, Standprüfung ohne Befund, keine Benutzerpfade.
- [Abschluss](ergebnis.json): offen bleiben nur die menschliche Abnahme, die in §21.44 genannten technischen Restvorhaben und Abhängigkeitsupdates als eigener Bauschnitt. Kein neuer öffentlicher Release.

