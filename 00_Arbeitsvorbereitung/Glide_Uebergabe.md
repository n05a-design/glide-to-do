# Glide – Übergabe an eine neue Sitzung

Stand 27.10.2026 · Glide 3.47.0 · Aufgabenformat 26 · Quelle/Python-Lieferung 3.47.0; eigenständige Pakete 3.45.0

**Aktueller Dokumentations-/Pushauftrag 27.10.2026:** Dokumentation erneut inhaltlich prüfen und anschließend alle Projektänderungen pushen. [Plan §21.25](Glide_Entwicklungsplan.md#2125-dokumentabgleich-und-pushauftrag-vom-27102026). Arbeitszweig `codex/glide-3.47-folgepakete`, Basis `origin/main` `1f4dbf8`; Quellbaum gegenüber dem vorherigen HEAD vor Übernahme identisch. Commit/Push nach abschließender CI autorisiert. D09: Rohprotokolle, QA-Fensterbilder, Originalreferenzbilder und lokale Tk-Prüfumgebung bleiben lokal.

**Aktuell 3.47.0 (27.10.2026):** Folgepakete Mehrfachplanung und Nebenansichtsverlauf umgesetzt. Aufgabenformat 26; normale Erledigung, bestehende Planung/Undo und Haupteditor bleiben erhalten. 13 neue Tk-freie Tests, echte neue Bedienwege und 606 Knopfprüfungen im Vorlauf grün; endgültige gezielte Arbeitsmodiprüfung und Lieferabschluss im [Nachweis](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/README.md). Keine neue vollständige 104-Suiten-Endmatrix oder native Paketfreigabe. Eigenständige Windows-/Mac-Pakete weiterhin 3.45.0, Menschen-/Plattformtore offen.

**Vorheriger Abschluss: zwei Featurepakete auf 3.46.0 / Format 26 umgesetzt und als Python-Fassung geliefert (D57).** Tagessteuerung mit Planung/Fokus/Vorschlag aus der Startseite; Nebenansicht mit Suche/Trefferwechsel/Abschnittssprüngen. 959 Fachtests, 19 echte Arbeitsmodifälle und 393 Knopfprüfungen grün. Breiter Windows-Lauf nach 94 erfolgreichen Suiten unterbrochen; zehn verbleibende Suiten im getrennten Restlauf grün, kein einzelner vollständig grüner Volllauf. Python-Lieferung: 88 Code-Dateien und 147 Ressourcen bytegleich, neue Aktions-/Undo-/Suchwege und sechs Ansichten aus 07 grün. [Plan §21.23](Glide_Entwicklungsplan.md#2123-zwei-featurepakete-und-versionsfortschritt-3460), [Endgültige Abschlusswerte und Grenzen](../01_Repository/Glide/tests/qa-3.46.0/zweierpaket_2026-10-27/README.md). Eigenständige Pakete bleiben 3.45.0; Linux-/Tk-9.1-Ursache und native Abnahmen getrennt offen.

**Vorheriger Lieferabschluss: Lieferungen und beide eigenständigen Pakete auf 3.45.0 aktualisiert.** App `d516ca67…`; Python-Lieferung mit 86 Code-Dateien und 147 Ressourcen bytegleich. Windows-Vollprüfung: 123 Schritte, 122 ausgeführt/grün, eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Windows-Paket neu gebaut/gestartet, Mac-Paket nativ gebaut, signatur- und isoliert startgeprüft. [Nachweis](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md), [Plan §21.20](Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450). Menschliche und öffentliche Releaseabnahme bleiben getrennt offen.

Am 25.10.2026 zusammengeführt und gekürzt: aktuelle Standmatrix anstelle mehrerer konkurrierender „Aktuell“-Absätze. Historische Hashes, Prüfläufe und Git-Aufträge bleiben im QA-Bericht und in ihren ursprünglichen Nachweisen erhalten.

## 1. Tatsächlicher Stand

**Vorheriger Lieferauftrag 26.10.2026:** „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Danach ausdrücklich GitHub Actions mit macOS-Runner und „weiter“ beauftragt. Native Bauten und Lieferabgleich sind abgeschlossen; strenge CI-Abschlusswerte stehen im Paketnachweis. Quell-/Workflowtransport auf `codex/glide-paketabschluss-3.45.0`, kein Merge oder öffentliche Veröffentlichung.

| Ebene | Tatsächlicher Stand am 27.10.2026 |
|---|---|
| Quelle | Glide 3.47.0 / Format 26, Mehrfachplanung und Nebenansichtsverlauf umgesetzt. 88 Laufzeitdateien plus separater Prototyp, App `dd26a038…`; [eingefrorene Hashes](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/quellstand.json). |
| Neue Funktionen | Tagesauswahl über Seiten/aktive Listen, gemeinsam planen/entplanen mit bestehender Kapazitätsvorschau und einem Undo/Redo. Nebenansicht: Zurück/Vorwärts/Alt+Pfeil, Such-/Lese-/Auswahlzustand, aktueller Verlauf und Inhaltswechsel; [Plan §21.24](Glide_Entwicklungsplan.md#2124-folgepakete-mehrfachplanung-und-nebenansichtsverlauf-3470). |
| Gezielte lokale Prüfung | 22 Arbeitsmodifälle abgedeckt: eingefrorener Lauf 21 grün/eine alte Knopferwartung rot; dieser Fall nach gezielter Erwartungskorrektur grün. Produktionsquelle unverändert. 13 neue reine Tests, 606 neue Knopfprüfungen, endgültige Aufnahmen. [Nachweis](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/README.md). |
| CI-Grundstufe | Strenger 3.47.0-Lauf grün: 19/19 Schritte, 193 Werkzeugtests (ein Skip), zweimal 972 Fachtests, fünf Analysen, Startprobe und bytegleiche Python-Lieferung. 93 Dokumente geprüft. [Nachweis](../01_Repository/Glide/tests/qa-3.47.0/folgepakete_2026-10-27/README.md). Remote-Läufe und historischer Linux-/Tk-9.1-Kompaktfall bleiben getrennt. |
| Vollprüfung lokal | Ursprünglicher 3.46.0-Lauf nach 94 erfolgreichen Suiten mit Prozess-/Werkzeugabbruch unvollständig, kein Abschlussbericht. Zehn verbleibende Suiten im getrennten Restlauf grün; Quell-/Prüfhashes unverändert. Analysen/Reproduktionen und genaue Fortsetzungsbilanz im [Nachweis](../01_Repository/Glide/tests/qa-3.46.0/zweierpaket_2026-10-27/README.md). Die vollständig grüne 3.45.0-Vollprüfung bleibt ausschließlich ihrem damaligen Stand zugeordnet. |
| Menschliche Abnahme | D55-Punkte 1–4 bestätigt, einschließlich Rechtsklick-Gegenprobe. Punkt 5: alter Menüweg bestätigt; korrigiertes Kürzel und neuer erster Menüeintrag noch nicht menschlich gegengeprüft. Neue Funktionen, Screenreader, zwei Bildschirme, offene Schrift-/DPI-Konfigurationen und Mac bleiben offen. Native Computerbedienung nach Esc-Stopp nicht fortgesetzt. [Prüfliste](Glide_Manuelle_Pruefung.md#arbeitsmodi-und-seitenbedienung-d55-lokaler-kandidat-auf-3440). |
| Python-Lieferung 07 | 3.47.0 / Format 26, App `dd26a038…`; 88 Code-/147 Ressourcendateien bytegleich. Beide neuen echten Paketfälle direkt aus 07 grün; Module dort aufgelöst. Atomarer Lieferweg behebt den aufgetretenen Windows-Mappingfehler beim Kopieren der Vorlagen. |
| Showcase / Pakete | Showcase 3.47.0: Import/Neustart und sechs Lieferdateien bytegleich geprüft. Eigenständige Windows-/Mac-Pakete bleiben vorheriger 3.45.0-Stand: Windows 103 Dateien, Mac 333 Dateien/29 Symlinks, damalige native Bau-/Start-/Signaturbelege unverändert. Mac-Weitergabe über geprüftes TAR; lokale .app ist NT-Inspektionskopie. |
| Git lokal | Arbeitszweig `codex/glide-3.47-folgepakete`, Basis/HEAD vor Transport `1f4dbf8`. Neuer ausdrücklicher Dokumentations-/Pushauftrag autorisiert Commit und Push aller Projektänderungen nach CI; konkrete Transportbestätigung im Abschluss dieser Sitzung. |
| GitHub | `origin/main` am 27.10.2026 per Fetch auf `1f4dbf8` bestätigt, enthält die zwei früheren Mergecommits #42/#43; Dateibaum vor diesem Auftrag identisch zu `089ae83`. Neue 3.47.0-Remoteprüfung nicht behauptet. Frühere Paketläufe gelten ausschließlich 3.45.0. |

**Git-Transport für den Paketauftrag:** Nach der ausdrücklichen Wahl von GitHub Actions wurden Quell-/Baucode und abschließende Liefer-/Dokumentänderungen auf `codex/glide-paketabschluss-3.45.0` übertragen. Die hier referenzierten nativen Prüfläufe bleiben ihren konkreten Quellcommits zugeordnet. Kein Merge oder öffentliche Veröffentlichung durch diesen Auftrag; ein Kandidaten-Push ersetzt keine Produkt-/Menschenabnahme.

**Native Prüfbedingungen:** Der Inhaber hat am 26.10. bestätigt: „Automatische Fensterverwaltung ist aktiv“. Das ist ein zusätzlicher möglicher Einfluss auf Geometrie und Fokus; die Startgröße 1280 × 860 stammt auch aus dem App-Konstruktor. Die Ursache sämtlicher roter nativer Fälle ist dadurch nicht belegt. Keine Änderung an Fensterverwaltung oder fremden Prozessen.

**Herkunft:** Der Phasenabschluss vom 22.10.2026 (FP-01–FP-06, FP-07 Stufe 1, WA-26–WA-31, Roadmap-Pakete 1–3) liegt in 3.44.0; D55 und das Speicherpaket sind nun in 3.45.0 gebündelt. Historische Prüfungen bleiben ihren damaligen Bytes zugeordnet: [Phase 3.44.0](../01_Repository/Glide/tests/qa-3.44.0/phasenabschluss_2026-10-22/README.md), [D55](../01_Repository/Glide/tests/qa-3.44.0/arbeitsmodi_2026-10-23/README.md), [GitHub 23.–25.10.](../01_Repository/Glide/tests/qa-3.44.0/github_pruefung_2026-10-23/README.md), [Speicherpaket](../01_Repository/Glide/tests/qa-3.44.0/speicherstatus_2026-10-25/README.md). Analyse/Gutachten stehen in [Analyse §13](Glide_Analyse.md#13-neuuntersuchung-vom-21102026), Aufgaben ausschließlich im [Plan §21](Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026).

## 2. Zuständige Dokumente

Die Quellen ergänzen sich nach Gegenstand. Ein Auftrag oder Beschluss bestimmt den Umfang; Code und Nachweise belegen getrennt, was tatsächlich implementiert, geprüft und geliefert ist. Ein älterer Plantext ersetzt keinen neueren konkreten Auftrag, ein grüner Test keine Produktentscheidung.

| Thema / Lesefolge | Verbindliche Quelle |
|---|---|
| Arbeitsregeln und Produktgrenzen | [AGENTS.md](../01_Repository/Glide/AGENTS.md), [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Bestätigte Richtung D01–D57, konkrete Aufträge und Prüfablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); D49 bleibt Auslegung mit Korrekturvorbehalt, neue Entscheidungen ab D58 |
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

Die aktuellen Folgepakete stehen in [Plan §21.24](Glide_Entwicklungsplan.md#2124-folgepakete-mehrfachplanung-und-nebenansichtsverlauf-3470), der Dokumentations-/Pushauftrag in §21.25; der vorherige Abschluss steht in [Plan §21.23](Glide_Entwicklungsplan.md#2123-zwei-featurepakete-und-versionsfortschritt-3460), der vorherige Techniknachlauf in §21.21, der abgeschlossene Liefer-/Paketauftrag in [§21.20](Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450). Nächste Arbeit:

1. **Linux-/Tk-9.1-Kompaktfall gezielt nachprüfen:** Neue Ereignisspur und getrennte Assertions auswerten. Der lokal behobene fehlende-Release-Fall beweist noch nicht die Ursache des damaligen CI-Fehlers; keine spekulative Geometriekorrektur.
2. **Technische Folge konsolidiert fortsetzen:** Speicherkoordinator/lesenden Vergleich erhalten; der erste Widgetbereich (Heute/Nächste Aufgabe) ist unter WA-39/32 ausgelagert. Weitere Kachel-/Dialog-/Themebereiche nur bei konkretem Nutzen, bestehendes Startseitenmodell weiterverwenden. RuntimePaths/-Config und weitere Zustands-/Callergrenzen nach WA-49/37/38; reale Refreshkosten nach WA-36 messen. Phasen und Abschlusskriterien ausschließlich §21.21, keine parallelen Kennungen.
3. **Menschenabnahme fortsetzen:** D55-Punkt 5, Sicherungsübersicht/Anhangsrückfrage sowie Reader-, Schrift-, DPI- und Mehrmonitorfälle der [Prüfliste](Glide_Manuelle_Pruefung.md); Punkte 1–4 bleiben abgenommen. Native Bedienung nach Esc-Stopp nur auf neuen konkreten Bedienauftrag.
4. **Offene native Lieferung/Abnahme nach D51:** Quelle/Python-Lieferung sind 3.46.0; eigenständige Windows-/Mac-Pakete bleiben 3.45.0. Neue native Paketbauten, Linux-/Mac-Matrix und Menschenabnahme bleiben getrennte offene Tore. Der unterbrochene Volllauf bleibt erhalten. Kein automatischer Commit/Push/Merge aus dem Featureauftrag.

Offen beim Inhaber: I12 (CodeQL-Einrichtung), Übernahme von tkinterdnd2 0.6.4 (WA-44), E-U1 B, E-U2 B/C, E-U3 B (WA-25) und Blockziehen, E-P1–E-P5, Integrationsrichtung E-I1, WA-23/24, FP-07 Stufe 2 (Canvas); E-U1 A–E-U3 A sind seit D55 gewählt. Paket 8 / 4.0.0 bleibt vorbereitet und pausiert. D53 erlaubt Neubewertungen, aktiviert keinen Anbieter; D52–D54 verlangen zentrale Roadmap, appweite Designgeltung und Pflege ohne automatische Feature-/Git-/Releaseentscheidung.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei; bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Keine echten Nutzerdaten oder privaten Fehlerprotokolle aus diesem Auftrag ableiten.
- Neue ausführbare Änderungen brauchen passende Prüfungen; alte Vollmatrix nur ihren eingefrorenen Bytes zuordnen. Vor einem konkret beauftragten Commit CI-Grundstufe; `--lieferstand-streng` erst beim gemeinsamen Lieferabschluss. Git-Schreibaktionen brauchen einen konkreten Auftrag; „pushen“ vom 26.10. gilt für den oben beschriebenen Kandidaten.
- Phasenabschluss: Version und Quell-/Prüf-/Ressourcenstand einfrieren, Voll-/native Matrix prüfen, anschließend 07/Showcase/Pakete und SHA-256 abgleichen. Kein Abgleich auf einen laufenden ungeprüften Kandidaten. Nach einem Versionswechsel unter Windows Zeilenenden der `eol=lf`-Dateien kontrollieren (`git ls-files --eol`), `versionswechsel.py` schreibt inzwischen ausdrücklich LF; tatsächlichen Stand trotzdem kontrollieren.
- Originalreferenzen, aktuelle QA-Versionen/-Bilder, Migrationsfixtures, Showcase und vorhandene Lieferpakete nach den Pflege- und Aufbewahrungsregeln schützen; historische Nachweise nicht nachträglich grün schreiben.

## 6. Bewusste Grenzen

Der lokale Abschluss 3.45.0 unterscheidet die eingefrorene Windows-Vollprüfung, nachfolgende Korrekturen mit gezielten Prüfungen und Python-Lieferung von der vollständigen Produkt-/Releaseabnahme. Native Mac-/Linux-/Readerabläufe, DPI/Mehrmonitor, physische Bedienung sowie Rechte-, Lizenz-, Signatur- und Veröffentlichungstore bleiben ausdrücklich offen. Neue Markt- oder Nutzungsbehauptungen werden aus der Zusammenführung nicht abgeleitet.
