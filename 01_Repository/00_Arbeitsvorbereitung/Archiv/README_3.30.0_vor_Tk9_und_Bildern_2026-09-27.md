# Arbeitsvorbereitung

Stand 27.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · Einstellungen 2 · Vorlagen 2

## Für neue Arbeiten zuerst lesen

0. [Bestandsprüfung, offene Aufgaben und Entscheidungsvorlage 27.09.2026](Glide_Bestandspruefung_und_Entscheidungen_2026-09-27.md) – Vollständigkeit, Abgleich mit dem Code, Recherche (Tk 9), Entscheidungen E-01 bis E-13 offen
1. [Sitzungsprotokoll und Lehren 24.–26.09.2026: was die Planung traf, was nicht, Empfehlungen](Glide_Sitzungsprotokoll_und_Lehren_2026-09-24_bis_26.md)
2. [Vertrag Modernisierung 3.30: umgesetzter Umfang, Format 20, Abweichungen](../01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md) und [Projektübergabe](../01_Repository/Glide/docs/09_PROJECT_HANDOFF.md)
3. [Manuelle Prüfung 3.30](Checklisten/Manuelle_Pruefung_3.30.0.md) – offen vor jeder Freigabe, dazu [Windows-Vollprüfung 3.30](Checklisten/Windows_Pruefung_3.30.0.md) mit Startpaket, [3.29](Checklisten/Manuelle_Pruefung_3.29.0.md) und [3.28](Checklisten/Manuelle_Pruefung_3.28.0.md)
4. [Aufgabenkatalog Modernisierung, Pinnwand-Board, Ordner und Pixel-Werkstatt](Glide_Aufgabenkatalog_Modernisierung_2026-09-25.md) – umgesetzt mit 3.30.0, Status je Paket
5. [Arbeitsvorbereitung dazu: Rahmen, Datenstrategie, Entscheidungen vom 25.09.2026, Etappen](Glide_Arbeitsvorbereitung_Modernisierung_2026-09-25.md)
6. [Umsetzbare Aufgabensammlung Zeichenfläche mit Status 3.30](Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md) – offen nur der Vorrat ZF-200/ZF-300
7. Offene Inhaberentscheidungen: Abschnitt „Offen“ im [Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md); eine eigene Entscheidungsliste führt die Arbeitsvorbereitung nicht mehr (ältere unter `Entscheidungen/Archiv`)

Recherchen (Befunde gültig, Ist-Angaben zu Glide beschreiben ihren Datumsstand):

- [Wettbewerbsrecherche 25.09.2026](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
- [Konzept „Seiten wie Notion“ 26.09.2026](Glide_Konzept_Seiten_wie_Notion_2026-09-26.md) – entschieden, Stufe 1, Seitenbereich und Galerie umgesetzt
- [Funktionsvergleich und Zeichenflächenkonzept 23.09.2026](Glide_Funktionsvergleich_und_Zeichenflaeche_2026-09-23.md)
- [SVG- und Zeichnungsdaten-Untersuchung 23.09.2026](Glide_SVG_und_Zeichnungsdaten_Untersuchung_2026-09-23.md)

Vorgeschichte (archiviert): [Zeichenflächen-Übergabe](../01_Repository/Glide/docs/archiv/62_ZEICHENFLAECHE_WEITERGABE_2026-09-24.md),
[Archiv- und Dokumentationsprüfung](../01_Repository/Glide/docs/archiv/63_ARCHIV_UND_DOKUMENTATIONSPRUEFUNG_2026-09-24.md),
[Zeichnungsseite 3.29](../01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md).

Die zweiten Stufen aus dem Katalog sind seit dem Ausbau vom 25.09.2026
umgesetzt. Der zweite Ausbau vom 26.09.2026 hat mehrere frühere Grenzen
geschlossen:

- Anhänge im Detailbereich;
- Zeichnungen in Folien;
- Stundenraster;
- Gruppierung mit Überschriften.

Der dritte Ausbau vom selben Tag hat die danach verbliebenen Grenzen
geschlossen:

- Ziehen aus der Liste ins Raster;
- gruppierte Tabelle mit Nummern und Überschriften;
- Pixelschrift unter Linux.

Seit der Überarbeitung für kleine Fenster zeigt Glide bei Mindestgröße nur
das Wichtigste, ohne Quetschung. Die Suite `test_mindestgroesse330` prüft das,
auch für alle Dialoge. Weitere Suiten sichern ab:

- `test_kontrast330`: WCAG AA in allen Designs;
- `test_paketierung330`: die Paketierungsvorstufe (Kennungen `de.shaye.glide`
  und `Shaye.Glide`).

Für ein echtes App-Symbol fehlt noch ein Export des Logos als PNG.

Seit dem 26.09.2026 bietet Glide je Design fünf Hintergrundverläufe
(Vertrag 66, Abschnitt 2.8); `test_hintergrund330` sichert sie ab.

Das [Konzept „Seiten wie Notion“](Glide_Konzept_Seiten_wie_Notion_2026-09-26.md)
ist entschieden. Stufe 1 und die Ordnertypen sind umgesetzt, seit dem
27.09.2026 auch der eigene Seitenbereich mit Vorlagen und dem Format
`.glidepage` sowie die Galerie, dazu die Bibliothek als Tabelle und
„Notizbuch“ statt „Tagebuch“. Offen sind Titelbild und Unterseiten; es
enthält außerdem Optimierungs- und Funktionsvorschläge.

Offen sind nur die „Bekannten Grenzen“ im Vertrag 3.30. Für die Einreichung
liegt ein
[Produktdatenblatt-Entwurf](../40_Store_Material/Produktdatenblatt_3.30.0_Entwurf.md)
bereit. Nicht
gewählt wurden der Einstieg für neue Nutzer und eigene Felder je Liste.
**Glide 3.29 nach der Umstellung nicht mehr starten** – es überschreibt einen
Format-20-Bestand (siehe Prüfliste 3.30).

Weiterhin aktive Querschnittsunterlagen sind der knappe
[Glide-Austauschformat](../01_Repository/Glide/docs/52_AUSTAUSCHFORMAT_3.23.0.md),
die [Fehlerprotokoll-Übersicht](Fehlerprotokolle/README.md) und die
[Releasecheckliste](../01_Repository/Glide/docs/10_RELEASE_CHECKLIST.md).

Abgeschlossene Prüfungen, alte Chat-Weitergaben, Analysen vor der
Zeichenflächenrecherche, technische Fakten früherer Versionen und
Umsetzungshilfen bis 3.26 liegen unter `Archiv/`. Sie sind nur bei einer
konkreten historischen Frage zu öffnen. Fortgeltende technische Verträge und
der aktuelle Dokumentationsindex liegen unter `01_Repository/Glide/docs/`.

Eine erfolgreich geprüfte Python-Fassung ist noch kein signiertes Releasepaket.
