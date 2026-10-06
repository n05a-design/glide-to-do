# Richtungsentwurf eingearbeitet – Nachweis

06.10.2026 · App 3.33.8 unverändert, kein Versionswechsel · Linux/Tk 8.6, künstliche Daten · Ausgangsstand `254541a` (main nach PR #14)

Auftrag des Inhabers vom 06.10.2026: den nicht übernommenen Richtungsentwurf vom 03.10.2026 (PR #12, geschlossen; Inhalt in Git) in die bestehende Struktur einarbeiten und Dopplungen vermeiden. Kein neues Dokument; nur Teile, die auf `main` fehlten, wurden dort ergänzt, wo ihr Thema laut [Dokumentenpflege](../../../docs/DOKUMENTENPFLEGE.md) liegt. Code, Lieferstand und Datenformat sind unverändert.

## Was wohin kam

| Teil des Entwurfs | Ziel | Hinweis |
|---|---|---|
| Belegstufen der Vorbilder, Notion „Favoriten und Zuletzt“, Abgrenzungen bei Trello und FigJam | [Markt und Vorbilder §2](../../../../../00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md#2-vorbilder-des-inhabers) | Spalte „Belegstufe“ statt „Belegter Bezug“ |
| Steckbriefe mit Stärke, Grenze und Bedeutung (rund 30 Produkte) und Entwicklung 2026 | Markt und Vorbilder §3 | ersetzt die bisherige Kurztabelle; jedes Produkt steht nur einmal, alle Quellenlinks bleiben erhalten; AppFlowy verweist auf GitHub statt auf eine Fremddokumentation |
| Ungekürzte Featurematrix | Markt und Vorbilder §4 | 51 statt 28 Zeilen; die 03.10.2026 zusammengelegten Zeilen mit unterschiedlichen Werten wieder getrennt (Quelle: Matrix vom 01.10.2026), Glide-Stand 3.33.7 aus der bisherigen Matrix übernommen |
| Vergleich nach Dimensionen | Markt und Vorbilder §4.1 | auf 3.33.8 und das Ausbauprogramm nachgeführt; Messwerte bleiben im Entwicklungsplan §10 |
| Berichtigte ältere Bewertungen | Markt und Vorbilder, „Überholt“ | Notion-Offline entfällt, weil §1.1 und §6 es genauer belegen |
| Nische sichtbar machen | Markt und Vorbilder §5 | Wortlaut an „besondere Kombination, keine nachgewiesene Alleinstellung“ angepasst |
| Gedanken und Vorgaben des Inhabers | [Arbeitsrichtung, Leitgedanken](../../../docs/ARBEITSRICHTUNG.md#leitgedanken-des-inhabers) | nur Zeilen, die nicht schon in Entscheidungen, frühere Antworten oder Aufträge stehen |
| Ausschlüsse der Wettbewerbsrecherche vom 25.09.2026 (Klebezettel ohne Aufgabe, Freihand-Tinte, Bilder aus dem Netz, Web Clipper, Formulare, generative Bildfunktionen); „Apple-like“ | [Produktgrenzen](../../../docs/01_PRODUCT_CONSTRAINTS.md) | Prinzipien, Hausregeln und Prinzipien-Check standen bereits dort |
| GitHub-Stand, Empfehlungen zum Auftritt, Git-Historie | [Veröffentlichung, GitHub-Auftritt](../../../docs/10_VEROEFFENTLICHUNG.md#github-auftritt) | Stand am 06.10.2026 neu abgerufen |
| Offene Richtungsfragen R1–R3 | [Entwicklungsplan §11](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber) als I9–I11 | umbenannt, weil R1–R14 dort Risiken bezeichnen; Empfehlung zur ersten Importquelle bei G21 |
| Entscheidungsstil | [Übergabe §4](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md#4-lehren-aus-den-bisherigen-runden) | bestehende Lehre ergänzt |

**Nicht übernommen, weil auf `main` schon vorhanden:** Leitsatz, drei Säulen und Stufen (Entwicklungsplan §1), Produktprinzipien P1–P6 mit Hausregeln und Prinzipien-Check, „Was Glide ist und nicht wird“, Grenzen einzelner Funktionen (Produktgrenzen), Entscheidungen D01–D17 und frühere Antworten, Arbeitsablauf (Arbeitsrichtung), Ergebnis und Positionierung (Markt und Vorbilder §1, §5), Wegweisungen (Empfohlener Fokus in §1.1, Priorität in §6, Kernfolge und Ausbauprogramm im Entwicklungsplan), Richtung der Veröffentlichung (Veröffentlichung), Auswahl A–H (Entwicklungsplan).

## Prüfung

CI-Grundstufe bestanden ([Ergebnis](ci/ergebnis.json)): Stand-, Link- und Indexprüfung, Startprobe, Lieferstand bytegleich, Datenschutz, Ablagegröße. Zusätzlich alle Markdown-Sprungmarken im Repository geprüft: keine fehlt. Eine Vollprüfung ist nicht nötig, weil kein ausführbarer Pfad geändert wurde.
