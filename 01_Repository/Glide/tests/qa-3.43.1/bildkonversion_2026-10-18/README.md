# WA-26 – Bildvorschauen ohne blockierenden Konverter

Stand 18.10.2026 · lokaler Prüfkandidat 3.43.1 / Format 25 auf PR #37 (`1042727`). Keine neue Lieferung.

## Änderung

`image_conversion.py` enthält die Tk-freie Dateikonversion und den gemeinsamen Dienst: ein Worker, höchstens 32 wartende Aufträge, ein begrenzter Ergebnisspeicher, 45 Sekunden Zeitlimit und Abbruch mit Beenden/Einsammeln des Kindprozesses. Nur erfolgreiche vollständige Ergebnisse zum unveränderten Quelldateistempel werden atomar in den Cache übernommen. Fehlversuche werden gespeichert und nicht durch jedes Neuzeichnen wiederholt.

Galerie, Seiten, Startseite, Titelbilder, Pinnwand und Zeichnungsreferenzen verwenden `PreviewCache.request_conversion`. Ein Tk-Timer prüft bis zu 64 Beobachter pro Schritt. Tk-Bilder und Rückrufe entstehen ausschließlich im Hauptthread. Hostabbau räumt Beobachter und Bindungen auf und bricht allein nicht mehr benötigte Aufträge ab; neue Dateigenerationen verdrängen alte Ergebnisse. In den vorhandenen Seitenbild-, Galerie- und Titelbildmenüs erscheint nach Fehlschlag „Vorschau erneut laden“. Zeichnungsreferenzen können erneut gewählt werden. Keine neue Laufzeitabhängigkeit und kein Datenformatwechsel.

## Prüfung und Gegenprobe

- Die [erste Fachtestsuite](units.json) umfasst 768 bestandene Tests, darunter 14 neue Fälle zu Konversion, Atomarität, Teilfehlern, Quellwechsel, Queue/Deduplizierung, Fehlercache/Retry und echten Prozess-Abbrüchen/Zeitlimits. Rohprotokolle bleiben lokal.
- Die neue Pflichtsuite hält einen Konverter künstlich an und prüft echte Galerie-, Seiten-, Startseiten-, Titelbild- und Referenzeinstiege. Ein Tk-Rückruf muss währenddessen ausgeführt werden, der Konverter darf nicht im Hauptthread laufen. Dazu kommen Retry, Hostabbau, Quellgeneration und 120 Anfragen über einen gemeinsamen Poller.
- Die [App-Adapter-Gegenprobe](gegenprobe_final.json) verwendet ausschließlich die unveränderte App aus `1042727` mit den neuen Hilfsmodulen. Sechs alte App-Wege müssen rot sein. Direkte Dienst-/Hostprüfungen mit den neuen Hilfsmodulen dürfen grün sein; sie sind keine Gegenprobe gegen die vollständigen alten Hilfsmodule. Es wird keine 9/9-Defektgegenprobe behauptet.
- Die [reale Windows-WIC-Konversion](wic_windows.json) erzeugte ein gültiges PNG mit 1600 × 1085 Pixeln. Das ist ein lokaler Funktionsnachweis, kein allgemeiner Performancevergleich.
- [Quellstand vor den seriellen Abschlussprüfungen](quellstand.json). Die [seriellen Bereichsprüfungen](regression_final.json) bestanden für Pflichtsuite, `test_bilder330.py` und `test_wissen3340.py`. Danach wurde die neue Statusbeschriftung auf die Kachelbreite begrenzt und die [gesamte neue Pflichtsuite erneut ausgeführt](pflichtsuite_abschluss.json): neun Fälle grün, einschließlich kleiner Kacheln bei 860 × 700. [Abschließender Quellstand](quellstand_abschluss.json), [Abgleich](quellstand_abschluss_abgleich.json). Vorläufe bleiben erhalten.

## Grenzen und Lieferung

Die ausgelagerten Unterprozesse blockieren die Rendercallbacks nicht mehr. Native Tk-Dekodierung und Dateimetadatenzugriffe bleiben im Hauptthread; große native PNG/SVG-Dateien sind kein pauschal gelöstes Performanceproblem. Die reale macOS-/Linux-Konverterabnahme, menschliche Sichtprüfung und der D51-Phasenabschluss bleiben offen. Für native Tk-Bilder gelten weiterhin die Grenzen des jeweiligen Tk. Ein alter blockierender `PreviewCache.convert`-Werkzeugweg bleibt verfügbar, wird aber von keinem App-Renderweg mehr aufgerufen; die Zeichnungsreferenz verlangt bei Konversionsformaten einen zuvor angelegten Cache.

07, Showcase und vorhandene Pakete sind unverändert. Echte Nutzerdaten wurden nicht verwendet. Der neue Schnitt bleibt bis zum gemeinsamen Phasenabschluss ohne eigene Zwischenversion.

## Abschlussbilanz

[Gesamtergebnis](ergebnis.json): neun UI-Fälle grün, sechs alte App-Adapter erwartungsgemäß rot und drei direkte aktuelle Dienst-/Hostfälle grün; 768 Fachtests einschließlich 14 neuer Tests sowie 152 Werkzeugtests bestanden. Beide bestehenden Bild-/Wissenssuiten bestanden. [783 geschützte Dateien](lieferstand_unveraendert.json) sind vollständig hashgleich; [Datenschutzprüfung](datenschutz.json) ohne Fund. [Kandidatenmanifest](kandidat_manifest.json) mit 73 eigenen Laufzeitdateien. Die alte Synchronkonversion ist im App-Code nicht mehr aufgerufen.
