# Glide – Übergabe an eine neue Sitzung

Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Python-Lieferung und eigenständige Windows-/Mac-Pakete 3.45.0

**Aktuell: Lieferungen und beide eigenständigen Pakete auf 3.45.0 aktualisiert.** App `d516ca67…`; Python-Lieferung mit 86 Code-Dateien und 147 Ressourcen bytegleich. Windows-Vollprüfung: 123 Schritte, 122 ausgeführt/grün, eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Windows-Paket neu gebaut/gestartet, Mac-Paket nativ gebaut, signatur- und isoliert startgeprüft. [Nachweis](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md), [Plan §21.20](Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450). Menschliche und öffentliche Releaseabnahme bleiben getrennt offen.

Am 25.10.2026 zusammengeführt und gekürzt: aktuelle Standmatrix anstelle mehrerer konkurrierender „Aktuell“-Absätze. Historische Hashes, Prüfläufe und Git-Aufträge bleiben im QA-Bericht und in ihren ursprünglichen Nachweisen erhalten.

## 1. Tatsächlicher Stand

**Auftrag 26.10.2026:** „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Danach ausdrücklich GitHub Actions mit macOS-Runner und „weiter“ beauftragt. Native Bauten und Lieferabgleich sind abgeschlossen; strenge CI-Abschlusswerte stehen im Paketnachweis. Quell-/Workflowtransport auf `codex/glide-paketabschluss-3.45.0`, kein Merge oder öffentliche Veröffentlichung.

| Ebene | Tatsächlicher Stand am 26.10.2026 |
|---|---|
| Quelle | Glide 3.45.0 / Format 26, App `d516ca67…`, Modell `ced120a5…`; 86 Laufzeitdateien plus Prototyp. [Aktueller Liefernachweis](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md). |
| Neue Funktionen | Startseitenmodell mit gemeinsamer Bestandsauswertung der sichtbaren Kacheln; bestehende Kacheln, Original-IDs, Aktionen und Gestaltung erhalten. WA-12 und Verweisvorschau bleiben enthalten. [Plan §21.19](Glide_Entwicklungsplan.md#2119-startseitenmodell-und-gemeinsame-bestandsauswertung), [Verweisvorschau §21.17](Glide_Entwicklungsplan.md#2117-verweise-in-der-nebenansicht-nachschlagen-wa-11). |
| Gezielte lokale Prüfung | Startseitenmodell: zwölf neue Fachtests, 13 Kacheltests und erweiterte Startseitensuite grün; Scopefreigabe bei Fehlern und Ereignisnachlauf sowie frische Werte nach Mutation/Undo geprüft. [Paketnachweis](../01_Repository/Glide/tests/qa-3.45.0/startseitenmodell_2026-10-26/README.md). Die 29 Fachfälle, zwei Vorschau-Bedienfälle und 204 Knopfprüfungen der [Verweisvorschau](../01_Repository/Glide/tests/qa-3.45.0/verweisvorschau_2026-10-26/README.md) bleiben ihrem damaligen Quellstand zugeordnet. Breite native D55-Abnahme weiterhin offen. |
| CI-Grundstufe | Strenger Lieferabschluss grün: 19/19 Schritte, 193 Werkzeugtests (einer übersprungen), zweimal 932 Fachtests, fünf Analysen, Startprobe und bytegleiche Python-Lieferung. [Paketnachweis](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md). GitHub-Windows-Voll-/Paketprüfung auf `6c342f8` grün; Linux/Tk-9.1-Kompaktkürzelfall rot, nicht pauschal als grün behandeln. |
| Vollprüfung lokal | Korrigierter Stand `d516ca67…`: 123 Schritte, 122 grün und eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Der erste rote Lauf bleibt erhalten. [Nachweise](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md). |
| Menschliche Abnahme | D55-Punkte 1–4 bestätigt, einschließlich Rechtsklick-Gegenprobe. Punkt 5: alter Menüweg bestätigt; korrigiertes Kürzel und neuer erster Menüeintrag noch nicht menschlich gegengeprüft. Neue Funktionen, Screenreader, zwei Bildschirme, offene Schrift-/DPI-Konfigurationen und Mac bleiben offen. Native Computerbedienung nach Esc-Stopp nicht fortgesetzt. [Prüfliste](Glide_Manuelle_Pruefung.md#arbeitsmodi-und-seitenbedienung-d55-lokaler-kandidat-auf-3440). |
| Python-Lieferung 07 | Glide 3.45.0 / Format 26, App `d516ca67…`; 86 Code-Dateien und 147 Ressourcen bytegleich. Echte Start-/Speicher-/Erledigen-/Undo-Probe aus 07 grün. |
| Showcase / Pakete | Showcase-Import/Neustart und sechs Lieferdateien geprüft. Windows-Paket 3.45.0: 103 Dateien, PE/Quellabgleich und lokale Startprobe grün. Mac-Paket 3.45.0: 333 Dateien/29 Symlinks, nativer Bau/Signatur/isolierter Start grün. Mac-Weitergabe über geprüftes TAR; lokale .app ist NT-Inspektionskopie. Alte aktive Pakete liegen im Archiv. |
| Git lokal | Kandidatenzweig `codex/glide-paketabschluss-3.45.0`; geprüfte Quell-/Baucodebasis `6c342f8`. Liefer- und Dokumentabschluss sind als Folgecommit auf demselben Zweig übertragen. Den konkreten aktuellen HEAD mit Git lesen; kein Merge durch diesen Auftrag. |
| GitHub | Nativer Maclauf [40328682255](https://github.com/n05a-design/glide-to-do/actions/runs/40328682255) auf `4e73220` grün; identische Appquellen. Maclauf auf `6c342f8` ebenfalls grün, dortige Grundstufe grün; restliche Remote-Matrix wird nicht pauschal als grün ausgegeben. |

**Git-Transport für den Paketauftrag:** Nach der ausdrücklichen Wahl von GitHub Actions wurden Quell-/Baucode und abschließende Liefer-/Dokumentänderungen auf `codex/glide-paketabschluss-3.45.0` übertragen. Die hier referenzierten nativen Prüfläufe bleiben ihren konkreten Quellcommits zugeordnet. Kein Merge oder öffentliche Veröffentlichung durch diesen Auftrag; ein Kandidaten-Push ersetzt keine Produkt-/Menschenabnahme.

**Native Prüfbedingungen:** Der Inhaber hat am 26.10. bestätigt: „Automatische Fensterverwaltung ist aktiv“. Das ist ein zusätzlicher möglicher Einfluss auf Geometrie und Fokus; die Startgröße 1280 × 860 stammt auch aus dem App-Konstruktor. Die Ursache sämtlicher roter nativer Fälle ist dadurch nicht belegt. Keine Änderung an Fensterverwaltung oder fremden Prozessen.

**Herkunft:** Der Phasenabschluss vom 22.10.2026 (FP-01–FP-06, FP-07 Stufe 1, WA-26–WA-31, Roadmap-Pakete 1–3) liegt in 3.44.0; D55 und das Speicherpaket sind nun in 3.45.0 gebündelt. Historische Prüfungen bleiben ihren damaligen Bytes zugeordnet: [Phase 3.44.0](../01_Repository/Glide/tests/qa-3.44.0/phasenabschluss_2026-10-22/README.md), [D55](../01_Repository/Glide/tests/qa-3.44.0/arbeitsmodi_2026-10-23/README.md), [GitHub 23.–25.10.](../01_Repository/Glide/tests/qa-3.44.0/github_pruefung_2026-10-23/README.md), [Speicherpaket](../01_Repository/Glide/tests/qa-3.44.0/speicherstatus_2026-10-25/README.md). Analyse/Gutachten stehen in [Analyse §13](Glide_Analyse.md#13-neuuntersuchung-vom-21102026), Aufgaben ausschließlich im [Plan §21](Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026).

## 2. Zuständige Dokumente

Die Quellen ergänzen sich nach Gegenstand. Ein Auftrag oder Beschluss bestimmt den Umfang; Code und Nachweise belegen getrennt, was tatsächlich implementiert, geprüft und geliefert ist. Ein älterer Plantext ersetzt keinen neueren konkreten Auftrag, ein grüner Test keine Produktentscheidung.

| Thema / Lesefolge | Verbindliche Quelle |
|---|---|
| Arbeitsregeln und Produktgrenzen | [AGENTS.md](../01_Repository/Glide/AGENTS.md), [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Bestätigte Richtung D01–D56, konkrete Aufträge und Prüfablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); D49 bleibt Auslegung mit Korrekturvorbehalt, neue Entscheidungen ab D57 |
| Aktueller Aufgabenstand und Reihenfolge | [Plan §21](Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026); vollständiges Inventar §18, Paketgrenzen §19, offene Auswahl §20 |
| Technische und methodische Befunde | [Analyse §13](Glide_Analyse.md#13-neuuntersuchung-vom-21102026), aktueller [Dokumentabgleich §13.7](Glide_Analyse.md#137-konsolidierte-bestandsaufnahme-und-dokumentabgleich) |
| Wettbewerbs- und Integrationsquellen | [Markt und Vorbilder §12](Glide_Markt_und_Vorbilder.md#12-erweiterte-recherche-vom-21102026); Herstellerrecherche mit eigenem Belegdatum, Empfehlungen bleiben Empfehlungen |
| Gestaltung für jede neue/angefasste Oberfläche | [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) mit Kontext-/Komponentenmatrix |
| Verhalten, Architektur, Daten und Migration | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md), [Datenvertrag](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Ausgeführte Prüfungen, Quellhashes und Lieferstände | [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md); Verfahren im [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md) |
| Tatsächliche native Bedien-/Readerabnahme | [Manuelle Prüfung](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Lizenz, Signierung und Produktidentität | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md), [Produktregister](../01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md) |
| Dokumentzuständigkeit und Aufbewahrung | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md), vollständiger [Index](../01_Repository/Glide/docs/00_INDEX.md) |

## 3. Auftrag und Bereinigung

Bestehende Quellen fortschreiben: ein Thema, ein Dokument. Die Gutachtenrunde vom 25.10. hat zusätzlich überholte Status- und Entscheidungsangaben (GitHub-Matrix, nächste D-Nummer, D55-Pushstand, Laufzeitprüfung, CodeQL-Wirkung) in Plan, Index, READMEs, Architektur und CHANGELOG bereinigt und diese Übergabe auf Verweise verdichtet. Der Phasenabschluss vom 22.10. hat aktive Versions-, Format-, Liefer-, Aufgaben- und Git-Statusaussagen in allen fortgeschriebenen Dokumenten auf 3.44.0 abgeglichen (Plan §16/§18/§19/§21, Funktionen, Datenvertrag, Architektur, Prüfplan, QA-Bericht, READMEs); historische Messergebnisse und Paketnachweise bleiben unverändert. Kein zweiter Plan oder neues Gesamtdokument.

Die globale Ablageprüfung vom 18.10. einschließlich Git und damaliger Arbeitskopien bleibt im [Ablagenachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Der Phasenabschluss ersetzt diese physische Vollinventur nicht. Der uncommittete Kandidat wurde vor jeder Änderung unverändert als Commit `5e915a7` gesichert; andere lokale Zweige und vier Stashes blieben unangetastet. Mehrdeutige Dateien, alte Affinity-Quellen, andere Zweige und Stashes werden nicht aufgrund eines Ignore-Eintrags oder historischen Löschwunschs entfernt.

Der [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md), [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) und 28 lokale Originalbilder bleiben Eingangsbelege. Bilder enthalten teilweise Kontoangaben, bleiben vom Git-Upload ausgeschlossen und müssen bei Rechner-/Agentenwechsel ausdrücklich mitgegeben werden. Aufgabenstatus nur im Plan §17/§21.

## 4. Nächste Arbeit und offene Entscheidungen

Der aktuelle Liefer-/Paketabschluss läuft nach [Plan §21.20](Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450). Funktionsumfang und gezielte Startseitenprüfung stehen in §21.15–§21.19. Nächste Schritte dieser Runde:

1. **Menschenabnahme fortsetzen:** D55-Punkt 5 (Kürzel, erster Menüeintrag und übrige Kompaktmodusfälle), Sicherungsübersicht/Anhangsrückfrage sowie Reader-, Schrift-, DPI- und Mehrmonitorfälle der [Prüfliste](Glide_Manuelle_Pruefung.md); Punkte 1–4 bleiben abgenommen.
2. **Beauftragte Lieferung vervollständigen:** Windows-Vollprüfung abschließen, 07/Showcase abgleichen sowie Windows-Paket bauen und mit künstlichen Daten starten. Mac-Bau und native Prüfung nach Klärung des erreichbaren arm64-Ausführungswegs. Die alten Pakete gelten erst nach tatsächlichem Neubau und passenden Belegen als ersetzt; ACL-Sperrproben bleiben auf vergängliche Hosted-CI-Runner begrenzt.
3. **Bei konkretem Git-Auftrag:** Remote-Abgleich und Indexsperre klären, überprüfbare Änderungen zusammenstellen, CI auf dem endgültigen Commit abwarten. Kein automatischer Commit/Push/Merge aus Featurearbeit.
4. **Nächste Feature-/Technikphase:** Startseitenpilot WA-39/WA-32/WA-36 aus [§21.19](Glide_Entwicklungsplan.md#2119-startseitenmodell-und-gemeinsame-bestandsauswertung) abschließen; weitere Ansichtsauslagerungen nur nach konkretem Nutzen. Offen bleiben WA-43, übrige WA-37/38 nach Fehlerwirkung und gemessene WA-36-Restkosten. WA-48/WA-51, Speicherpaket, WA-11/12 und die vorhandenen FP-Kerne nicht erneut als offenen Neubau anbieten.

Offen beim Inhaber: I12 (CodeQL-Einrichtung), Übernahme von tkinterdnd2 0.6.4 (WA-44), E-U1 B, E-U2 B/C, E-U3 B (WA-25) und Blockziehen, E-P1–E-P5, Integrationsrichtung E-I1, WA-23/24, FP-07 Stufe 2 (Canvas); E-U1 A–E-U3 A sind seit D55 gewählt. Paket 8 / 4.0.0 bleibt vorbereitet und pausiert. D53 erlaubt Neubewertungen, aktiviert keinen Anbieter; D52–D54 verlangen zentrale Roadmap, appweite Designgeltung und Pflege ohne automatische Feature-/Git-/Releaseentscheidung.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei; bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Keine echten Nutzerdaten oder privaten Fehlerprotokolle aus diesem Auftrag ableiten.
- Neue ausführbare Änderungen brauchen passende Prüfungen; alte Vollmatrix nur ihren eingefrorenen Bytes zuordnen. Vor einem konkret beauftragten Commit CI-Grundstufe; `--lieferstand-streng` erst beim gemeinsamen Lieferabschluss. Git-Schreibaktionen brauchen einen konkreten Auftrag; „pushen“ vom 26.10. gilt für den oben beschriebenen Kandidaten.
- Phasenabschluss: Version und Quell-/Prüf-/Ressourcenstand einfrieren, Voll-/native Matrix prüfen, anschließend 07/Showcase/Pakete und SHA-256 abgleichen. Kein Abgleich auf einen laufenden ungeprüften Kandidaten. Nach einem Versionswechsel unter Windows Zeilenenden der `eol=lf`-Dateien kontrollieren (`git ls-files --eol`), weil `versionswechsel.py` mit Plattform-Zeilenenden schreibt.
- Originalreferenzen, aktuelle QA-Versionen/-Bilder, Migrationsfixtures, Showcase und vorhandene Lieferpakete nach den Pflege- und Aufbewahrungsregeln schützen; historische Nachweise nicht nachträglich grün schreiben.

## 6. Bewusste Grenzen

Der lokale Abschluss 3.45.0 unterscheidet die eingefrorene Windows-Vollprüfung, nachfolgende Korrekturen mit gezielten Prüfungen und Python-Lieferung von der vollständigen Produkt-/Releaseabnahme. Native Mac-/Linux-/Readerabläufe, die unvollständige lokale Mac-Kopie, DPI/Mehrmonitor, physische Bedienung sowie Rechte-, Lizenz-, Signatur- und Veröffentlichungstore bleiben ausdrücklich offen. Neue Markt- oder Nutzungsbehauptungen werden aus der Zusammenführung nicht abgeleitet.
