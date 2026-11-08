# Außenabstände – Glide 3.50.0, 02.11.2026

Nutzerauftrag: allgemein oben mehr Platz, links/rechts/unten kleinere Abstände. Begrenzter Layoutnachlauf im 3.50-Quellkandidaten; keine neue Funktion, kein Datenformat- oder Abhängigkeitswechsel und kein neuer öffentlicher Release. Aufgabenstatus im [Plan §21.45](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2145-außenabstände-des-hauptfensters).

## Änderung

| Äußerer Fensterrand | Vorher | Nachher |
|---|---:|---:|
| Oben | 4 px | 12 px |
| Links / rechts | 28 px | 22 px |
| Unten | 14 px | 10 px |
| Links / rechts im Kompaktmodus | 14 px | 10 px |

`ListApp.WINDOW_PAD_X`, `WINDOW_PAD_Y` und `COMPACT_WINDOW_PAD_X` verwenden die vorhandene Gestaltungsskala. Start und Rückweg des Kompaktmodus greifen auf dieselben Werte zu. Kopf-/Inhaltsflucht, volle/schmale/ausgeblendete Seitenleiste sowie innere Karten-, Feld- und Dialogabstände bleiben erhalten. Betroffene Designkontexte und Regel stehen in den [Design Richtlinien](../../../docs/DESIGN_RICHTLINIEN.md).

## Ausgeführte Prüfung

- [Bestehende Gestaltungsbaseline](baseline.json): vor der Änderung 219 Knopfprüfungen in fünf Größen-/Schrift-/Designkonfigurationen ohne Befund; künstlicher temporärer `GLIDE_DATA_DIR`.
- [Gestaltung nachher](gestaltung.json): 221 Knopfprüfungen in denselben fünf Konfigurationen grün. Mehr nutzbare Breite erlaubt zusätzliche sichtbare Kopfaktionen; keine neue Aktion angelegt.
- [Kompaktmodus](kompakt.json): echte Kürzel/Einstiege, 480 × 560, getrennte Fensterlagen, Neustart und 26 Knopfprüfungen grün.
- [Beta350](beta350.json): zehn Designs, Hintergrundfarben, drei Fenstergrößen, volle Seitenleiste, Fluchten, echtes Blockziehen/Undo/Redo/Abbruch/Schreibschutz grün.
- [Appweiter Knopfschutz](knopfschutz.json): 1.120 Kontrollen in sieben Ansichten und fünf Dialogen, zwei Größen und Schriftgrößen, Hinweise an/aus; kein Befund.
- [Reale Ränder vorher](raender_vorher.json) / [nachher](raender_nachher.json): relativ zu den echten Tk-Fensterkoordinaten gemessen, auch nach Rückkehr aus dem Kompaktmodus. Kopf-/Inhaltsflucht 0 px Abweichung. Lokale Aufnahmen unter `fensterbilder/`, mit künstlichen Showcase-Daten und eigener Tk 9.1; sie sind keine menschliche Gesamt-/DPI-/Mehrmonitorabnahme.
- [Abschließende CI-Grundstufe](grundstufe.json): 19 Schritte grün, 238 Werkzeugtests (drei Skips), zweimal 1.112 Fachtests (je ein Skip), Syntax/Versionen/435 aktive Dokumentlinks/Analysen/Startprobe, strenger Python-Lieferabgleich und 116 Vendor-Dateien gleich dem Original; Abruf über die vorhandene System-CA-Datei.

Der vorherige [Abschlussaudit](../abschlussabgleich_2026-11-02/README.md) bleibt ein Beleg vor dieser Produktionsänderung. Alte Vollmatrix-/Paketnachweise werden nicht als Prüfung der neuen Appbytes ausgegeben. Keine zusätzliche Unit-Suite für die bloße Änderung dreier Layoutwerte angelegt; die vorhandenen echten Bedien-/Geometrieprüfungen decken den betroffenen Weg ab.

## Lieferung und Grenzen

Python-Fassung nach `07_Python-Versionen` abgeglichen: 91 Code- und 147 Ressourcen-/Vendordateien ohne Abweichung. Eigenständige Mac-App mit eigener Tk 9.1 gebaut, kompilierten Quellcode/Lizenzen geprüft und isoliert ohne externes Python gestartet; 463 Dateien bei der lokalen Installation gleich dem Bauinventar, Ad-hoc-Signatur grün. Aktive App `~/Applications/Glide.app`, frühere App unverändert unter `~/Applications/Glide-vor-Abstaenden-20261102.app`; altes öffentliches TAR bleibt erhalten, neuer Kandidat separat unter `build/macos/Kandidaten`. [Nativer Bau](mac_bau.json), [isolierter Bau-Start](mac_start_bau.json), [Lieferabgleich](mac_lieferung.json) und [Start der gelieferten App](mac_start_lieferung.json). Native Paketstände, App-/Archivhashes und tatsächlicher Mac-Start stehen im [maschinellen Abschluss](ergebnis.json). Der Windows-EXE-Stand des ersten öffentlichen 3.50-Releases wird durch einen lokalen Mac-Bau nicht aktualisiert; eine neue native Windows-Lieferung bleibt am gemeinsamen Phasenabschluss auszuführen. Windows kann die neue Python-Fassung nutzen.

Die Version bleibt für diesen begrenzten Layoutnachlauf 3.50.0. Der Inhaber prüft weiterhin die reale Bedienung, DPI und mehrere Monitore; Reader ist nach D58 bis Bedarf zurückgestellt. Frühere Nachweise und Pakete bleiben als Rückweg erhalten.
