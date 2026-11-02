# Pixelsymbole – Glide 3.50.0, 02.11.2026

Zwei Nutzeraufträge: Abstand eigener Symbole zum Seitenleistentext korrigieren; Seitentitel bündig zum Fließtext halten und ein Symbol links davor anzeigen, ohne den Titel zu verschieben. Aktueller Aufgabenstand im [Plan §21.46](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2146-pixelsymbole-seitenleistenabstand-und-feste-titelkante).

## Umsetzung

- Seitenleistenbäume: eigene Symbole erhalten eine transparente Anzeigevariante mit 8 px Abstand rechts. Originalzeichnung, Daten, Symbole anderer Kontexte und Zeilen ohne eigenes Symbol bleiben erhalten. Symbolbreite einschließlich Abstand fließt in die Titelkürzung ein, auch nach einem Breitenwechsel. Varianten teilen den Cache nach Inhalt und Skalierung.
- Seitentitel: reines Textlabel auf der Kante des Fließtexts; kein Bild im selben Label und keine eingefügten Leerzeichen. Das separat fokussierbare Symbol sitzt mit 8 px Abstand links davor, innerhalb des Leserands. Eine Tk-freie Geometrieregel begrenzt die ganzzahlige Skalierung auf Rand und erste Titelzeile. Titelklick benennt um; Symbolklick sowie Return/Leertaste am Symbol öffnen seine Bearbeitung. Kopfaktionen bleiben am rechten Ende erreichbar.
- Die Außenabstände aus dem [vorherigen Nachlauf](../aussenabstaende_2026-11-02/README.md) bleiben erhalten. Kein Datenformat-, Einstellungs-, Abhängigkeits- oder öffentlicher Releasewechsel.

## Tatsächliche Prüfungen

| Beleg | Ergebnis |
|---|---|
| [Baseline Kopfaktionen](baseline.json) | Vor Produktionsänderung bestehender Fall grün, 19 Knopfprüfungen |
| [Seitenleiste vorher](seitenleiste_vorher.json) / [nachher](seitenleiste_nachher.json) | Reale Treeview-Elementpositionen: 0 → 8 px Abstand bei Seite, Ordner und eingerückter Liste, Hell/Dunkel; Zeile ohne Symbol unverändert |
| [Titel vorher](titel_vorher.json) / [nachher](titel_nachher.json) | Zwölf Messungen bei 860/1280 px, mittlerer/großer Schrift und schmaler/voller Lesebreite: vorher 2 px ohne Symbol bzw. 48 px mit Symbol abweichend, nachher durchgehend 0 px; Symbolabstand 8 px, vollständig innerhalb des Leserands |
| [Aktualisierte Kopfprobe gegen die Vorfassung](rot_kopfverweise.json) | Gezielt rot wegen tatsächlicher Titelverschiebung; keine Schwächung des alten Bedienvertrags |
| [Kopfprobe neu](kopfverweise.json) | Geometrie, Kopfaktionen, Symbolklick/Return/Leertaste und Titelklick grün |
| [Gestaltung](gestaltung.json), [Kompaktmodus](kompakt.json), [Schreibschutz](schreibschutz.json) | Bestehende Fälle grün, 212 bzw. 26 Knopfprüfungen; keine Änderungen im Schreibschutz |
| [CI-Grundstufe](grundstufe.json) | 19 Schritte grün. 1.113 Fachtests (zweimal. je ein Skip). 238 Werkzeugtests (drei Skips). Syntax/Versionen/439 aktive Dokumentlinks/fünf Analysen/Startprobe. strenger Python-Lieferabgleich und 116 Vendor-Dateien bytegleich zum Original |

Die zusätzliche Grenzprüfung für `ui_design.page_icon_layout` liegt im vorhandenen `test_ui_design.py`: Symbol bleibt vor der unveränderten Textkante, innerhalb von Rand/Zeilenhöhe; kein Platz ergibt keine überdeckende Platzierung. Der bestehende Kopfaktionsfall prüft die neue tatsächliche Geometrie und die getrennten Maus-/Tastaturwege. Alle Bedienproben verwenden künstliche Daten in temporärem `GLIDE_DATA_DIR`.

Lokale Sichtaufnahmen mit künstlicher Seite unter `fensterbilder/`; vorhandene Screenshots des Nutzers wurden nicht in das Repository übernommen. Kein neuer vollständiger 108-Suiten-Volllauf oder menschlicher DPI-/Mehrmonitorabschluss behauptet. Frühere Nachweise bleiben an ihre ursprünglichen Quell-/Lieferbytes gebunden.

## Lieferung

Python-Fassung nach `07_Python-Versionen` abgeglichen: 91 Code- und 147 Ressourcen-/Vendordateien ohne Abweichung. Eigenständige Mac-App mit eigener Tk 9.1 neu gebaut und isoliert ohne externes Python gestartet; 463 Paketdateien der Installation gleich dem Bauinventar, Ad-hoc-Signatur grün. Aktive App `~/Applications/Glide.app`, vorheriger Abstandsnachlauf unter `~/Applications/Glide-vor-Pixelsymbolen-20261102.app` unverändert erhalten; neues Kandidaten-TAR separat unter `build/macos/Kandidaten`. [Bau](mac_bau.json), [isolierter Start](mac_start_bau.json), [Lieferabgleich](mac_lieferung.json) und [Start der installierten App](mac_start_lieferung.json); App-/Archivhashes und Zusammenfassung im [maschinellen Abschluss](ergebnis.json). Die Windows-EXE bleibt beim ursprünglichen öffentlichen 3.50-Stand; die neue Python-Fassung ist plattformübergreifend nutzbar. Native Windows-Lieferung am gemeinsamen Phasenabschluss, menschliche Bedien-/DPI-/Mehrmonitorprüfung weiterhin offen. Reader nach D58 bis Bedarf zurückgestellt.
