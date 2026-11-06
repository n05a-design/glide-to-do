# Gleichmäßiger Seitenleistenabstand – 3.50.4

Stand 05.11.2026 · Aufgabenformat 26

Direkter menschlicher Befund: Bei Hover über „Startseite“ ist die Luft nach oben größer als links/rechts. Kontexte: volle Seitenleiste, Systemnavigation, Hover-/Auswahlfläche; bestehende Karten-/Auswahl-/Hoverrollen erhalten.

Die Kartenpolsterung betrug bereits 10 px. Dazu kamen 4 px oberer Packabstand und eine leere native Tabellenkopfzeile mit weiteren 2 px. Die Systemnavigation zeigt jetzt ausdrücklich keine Kopfzeile und erhält keinen zusätzlichen oberen Packabstand. Der sichtbare Zeilenhintergrund liegt damit oben/links/rechts jeweils 10 px innerhalb der äußeren Karte.

- Bestehende `menschen3503`-Baseline auf `85a61f0a…` vor Produktionsänderung grün.
- Neuer Fall `seitenleistenabstand3504` auf derselben Vorfassung gezielt rot: 16/10/10 px. Die Prüfung misst die tatsächliche Zeilen-Boundingbox gegen die äußere Karte, nicht nur Packattribute.
- App `a536c8d4…`: 16 Hover-/Geometrievarianten grün, Hell/Dunkel/Glas, mittlere/große Schrift, 860/1280 px, Rückkehr aus schmaler/ausgeblendeter Seitenleiste. Symbolhintergrund und Entfernen des Hovers mitgeprüft. Fall in `--fall alle` registriert, nun 48 Fälle.
- Buchbreite 64/64 und bestehende `menschen3503`, `seitenleiste_kontext`, `side_abschnitte`, `werkzeugzeile` grün. Syntax sowie Quelle/Python mit 93 Code-Dateien/171 Ressourcen bytegleich.
- Windows-Sichtaufnahmen mit künstlichen Daten unter `%USERPROFILE%/gq/sidebar4/bilder/`; Hellaufnahme visuell kontrolliert. JSON-Rohbelege und Eingangshash im [Ergebnis](ergebnis.json).

Keine neue strenge Grundstufe, native Plattformmatrix oder menschliche Freigabe auf diesem Hash. Buch-Punkt 6 und neuer Abstand bleiben bis zur menschlichen Rückmeldung offen. Der Benutzer übernimmt native Neubauten heute Abend. Keine Git-/Releaseaktion.
