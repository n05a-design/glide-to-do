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

**Nicht übernommen, weil auf `main` schon vorhanden:** Leitsatz, drei Säulen und Stufen (Entwicklungsplan §1), Produktprinzipien P1–P6 mit Hausregeln und Prinzipien-Check, „Was Glide ist und nicht wird“, Grenzen einzelner Funktionen (Produktgrenzen), Entscheidungen D01–D17 und frühere Antworten, Arbeitsablauf (Arbeitsrichtung), Ergebnis und Positionierung (Markt und Vorbilder §1, §5), Wegweisungen (Empfohlener Fokus in §1.1, Priorität in §6, Kernfolge und Ausbauprogramm im Entwicklungsplan), Richtung der Veröffentlichung (Veröffentlichung), Aufgaben der Auswahl A–H (Entwicklungsplan; die Bedeutung der Buchstaben kam erst mit der Vollständigkeitsprüfung hinzu).

## Vollständigkeitsprüfung der Dokumentation

Im Anschluss beauftragt („anschließend Dokumentation auf Vollständigkeit prüfen“). Geprüft wurden alle 43 gepflegten Markdown-Dokumente außerhalb der Nachweise.

| Prüfung | Ergebnis |
|---|---|
| Einarbeitung des Richtungsentwurfs, 61 Kernaussagen | alle auffindbar; ergänzt wurden die Bedeutung der Auswahl A–H mit Bearbeitungstiefe (Entwicklungsplan §11) und die Regel „neue Entscheidungen als D18 ff.“ (Arbeitsrichtung) |
| Index, Ordner-READMEs, Zuständigkeiten | alle Dokumente im Index; Index, Dokumentenpflege und Übergabe („Wo was liegt“) um Leitgedanken, GitHub-Auftritt, Produktgrenzen und Dokumentenpflege ergänzt |
| Code gegen Dokumentation | alle 15 Module in Architektur und Quell-README, acht Tk-freie Fachmodule mit Unit-Tests im Prüfplan, alle 66 Integrationssuiten im Prüfplan, alle Pflege- und Prüfwerkzeuge in ihren READMEs, 3.33.7/3.33.8 in Funktionen, Architektur, Daten, QA-Bericht und CHANGELOG. Korrigiert: D17-Stand „sieben“ → „acht Module“; Projekt-README nennt die Inhaltssuche und die offene Lizenz |
| Kennungen | 208 verwendete Kennungen; nicht erklärt war G27 („`app.pyw` aufteilen“, jetzt bei D17); T1 und T8 sind Messbezeichnungen der Bestandsaufnahme vom 01.10.2026 und im Satz erläutert. Der Prinzipien-Check verweist jetzt auf Grundbegriffe und Index, der Index erklärt die Punktarten |
| Offene Inhaberpunkte | Übergabe §7, Arbeitsrichtung und Entwicklungsplan §11 nennen jetzt dieselben Punkte (A–H, D07, G21, G26, I1–I11, AU03, OB04, AU07) |

**Hinweis ohne Änderung:** 3.33.7 wurde nie nach `07_Python-Versionen` geliefert (direkt 3.33.6 → 3.33.8); deshalb liegen dort mit der aktuellen Fassung sechs statt sieben Versionen. Die Archiv-README sagt das nicht. Sie gehört zum Lieferstand und wird erst in der nächsten Produktionsrunde nachgeführt.

## Prüfung

CI-Grundstufe bestanden ([Ergebnis](ci/ergebnis.json)): Stand-, Link- und Indexprüfung, Startprobe, Lieferstand bytegleich, Datenschutz, Ablagegröße. Zusätzlich alle Markdown-Sprungmarken im Repository geprüft: keine fehlt. Eine Vollprüfung ist nicht nötig, weil kein ausführbarer Pfad geändert wurde.
