# Glide – Übergabe an eine neue Sitzung

Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Python-Lieferung 3.45.0, eigenständige Pakete 3.42.0

**Aktuell: Verweisvorschau D55/WA-11 im Quellkandidaten umgesetzt.** App `b53e6822…`, WA-12 enthalten; 29 passende Fachfälle und zwei neue Bedienfälle grün. Breite native Fokus-/Inspektor-/Tastaturprüfung bleibt offen; rote Vorläufe erhalten. [Paketnachweis](../01_Repository/Glide/tests/qa-3.45.0/verweisvorschau_2026-10-26/README.md). Letzte Lieferung 3.45.0 `2e69d875…` separat nachgewiesen.

Am 25.10.2026 zusammengeführt und gekürzt: aktuelle Standmatrix anstelle mehrerer konkurrierender „Aktuell“-Absätze. Historische Hashes, Prüfläufe und Git-Aufträge bleiben im QA-Bericht und in ihren ursprünglichen Nachweisen erhalten.

## 1. Tatsächlicher Stand

**Aktueller Auftrag 26.10.2026:** „pushen“. Der vorhandene 3.45.0-Kandidat einschließlich WA-12 und Verweisvorschau wird auf `codex/glide-3.45.0` mit Basis `origin/main` `291c393` vorbereitet, nach frischer CI-Grundstufe committet und gepusht. [Git-Nachweis](../01_Repository/Glide/tests/qa-3.45.0/push_2026-10-26/README.md), [Plan §21.18](Glide_Entwicklungsplan.md#2118-git-auftrag-push-des-3450-kandidaten). Der vorherige Featureauftrag steht in §21.17; Lieferung und Menschenabnahme bleiben eigene Nachweise.

| Ebene | Tatsächlicher Stand am 26.10.2026 |
|---|---|
| Quelle | Quellkandidat 3.45.0 / Format 26, Einstellungen/Vorlagen 2; App `b53e6822…`, 85 Laufzeitdateien plus Prototyp, 104 Suiten, 15 Fälle in der Arbeitsmodussuite. [Quellstand](../01_Repository/Glide/tests/qa-3.45.0/verweisvorschau_2026-10-26/quellstand.json). |
| Neue Funktionen | WA-12 plus Verweisvorschau: lokale Links und Aufgaben in der Nebenansicht, Haupteditor erhalten, aktuelle ID-Auflösung und Taskmarkierung, Textkontext und Verweis-/Rückverweismenü. [Plan §21.17](Glide_Entwicklungsplan.md#2117-verweise-in-der-nebenansicht-nachschlagen-wa-11). |
| Gezielte lokale Prüfung | 29 passende Fachfälle (12 Nebenansicht, 3 Objektverweise, 14 Tagesvorschlag) und zwei neue Vorschau-Bedienfälle grün; 204 Knopfprüfungen in acht Konfigurationen. Weitere native D55-Fokus-/Inspektor-/Tastenläufe rot, teilweise auch an der unveränderten Lieferung; keine neue breite Freigabe. [Paketnachweis](../01_Repository/Glide/tests/qa-3.45.0/verweisvorschau_2026-10-26/README.md). |
| CI-Grundstufe | Aktueller Push-Kandidat `b53e6822…`: Exitcode 0, 19 Schritte (18 ausgeführt, ein erwarteter Lieferhinweis), 172 Werkzeugtests (einer übersprungen), zweimal 920 Fachtests, fünf Analysen, Startprobe und Ablagekontrollen grün. [Push-Prüfung](../01_Repository/Glide/tests/qa-3.45.0/push_2026-10-26/ci_grundstufe/ergebnis.json). Letzter strenger Lieferabschluss `2e69d875…`, vor WA-12: strenger Abschluss grün: Exitcode 0, alle 19 Schritte ausgeführt, 172 Werkzeugtests (einer übersprungen), zweimal 911 Fachtests, fünf Analysen, Startprobe, bytegleiche Lieferung, Datenschutz/Aufbewahrung/Synchronisation und 116 Vendor-Dateien. [Abschlusslauf](../01_Repository/Glide/tests/qa-3.45.0/weiterentwicklung_2026-10-25/ci_abschluss/ergebnis.json). |
| Vollprüfung lokal | Eingefrorener Windows-Lauf an App `72e7fb6b…`: 123 Schritte, 119 grün, drei rot, eine menschliche Sichtprüfung übersprungen. Alle 104 Suiten ausgeführt; 101 grün. Zwei veraltete Testannahmen und eine falsche Statusknopfrolle korrigiert; der rote Lauf bleibt erhalten. Nachlauf und Quelländerungen getrennt im [Nachweis](../01_Repository/Glide/tests/qa-3.45.0/weiterentwicklung_2026-10-25/README.md). Python 3.14.7 / Tk 9.0.4. |
| Menschliche Abnahme | D55-Punkte 1–4 bestätigt, einschließlich Rechtsklick-Gegenprobe. Punkt 5: alter Menüweg bestätigt; korrigiertes Kürzel und neuer erster Menüeintrag noch nicht menschlich gegengeprüft. Neue Funktionen, Screenreader, zwei Bildschirme, offene Schrift-/DPI-Konfigurationen und Mac bleiben offen. Native Computerbedienung nach Esc-Stopp nicht fortgesetzt. [Prüfliste](Glide_Manuelle_Pruefung.md#arbeitsmodi-und-seitenbedienung-d55-lokaler-kandidat-auf-3440). |
| Python-Lieferung 07 | Unverändert 3.45.0 / Format 26, App `2e69d875…`; damalige 85 Code-/147 Ressourcen-/Vendor-Dateien bytegleich geliefert und Lieferprobe grün. Seit WA-12 und Verweisvorschau unterscheiden sich Quelle und Lieferung in `app.pyw`, `day_proposal.py` und `side_view.py`. Gemeinsamer Lieferabschluss erst am nächsten Phasenende. |
| Showcase / Pakete | 3.45.0-Fixtures und Showcase geliefert; echter Import/Neustart und sechs Datei-Hashes grün. Eigenständige Pakete und Mac-Bundle bleiben 3.42.0; keine neue native Paket-/Signaturprüfung. |
| Git lokal | Push-Zweig `codex/glide-3.45.0`, Basis `origin/main` `291c393`; alter lokaler Zweig `claude/phasenabschluss-3.44.0` bei `71854ec` erhalten. Leere Indexsperre vom 23.10. nach Prozess-/Exklusivzugriffsprüfung als `.git/index.lock.stale-20261026-push` gesichert. Staging und frische CI-Grundstufe für den konkreten Auftrag; lokale Rohprotokolle, neue Vollprüfbilder und Tk-Quellarchiv ausgenommen. [Git-Nachweis](../01_Repository/Glide/tests/qa-3.45.0/push_2026-10-26/README.md). |
| GitHub | D55-Zwischenstand über PR #40 in `main` `291c393`. Glide #155 auf `facf61a` grün, #156 auf dem inhaltsgleichen Merge rot; CodeQL #55 grün. Der eingereichte Fehler ist eine zu breite Fehlerinjektion in `struktur_ergebnis`; bei erzwungener Sperrerneuerung lokal rot reproduziert und auf die Hauptdatei eingegrenzt. Kein neuer Remote-Lauf auf 3.45.0. [Snapshot](../01_Repository/Glide/tests/qa-3.45.0/weiterentwicklung_2026-10-25/github_d55_snapshot.json). |

**Git-Auftrag aktiv:** kontrollierter Abgleich mit dem aktuellen `main` erfolgt; keine unbeabsichtigt fehlende Remote-Datei. Commit und Push auf dem neuen Kandidatenzweig nach CI-Grundstufe, anschließend Remote-Hash prüfen. Der Push löst die Glide-Prüfung auch für `codex/**` aus. Ein Kandidaten-Push bleibt von Produkt-/Menschenabnahme getrennt.

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

Aktuelle Paketfolge und Grenzen stehen im [Plan §21.15](Glide_Entwicklungsplan.md#2115-weiterentwicklung-zu-3450-sicherungen-und-anhänge). Nach dem lokalen 3.45.0-Abschluss:

1. **Menschenabnahme fortsetzen:** D55-Punkt 5 (Kürzel, erster Menüeintrag und übrige Kompaktmodusfälle), Sicherungsübersicht/Anhangsrückfrage sowie Reader-, Schrift-, DPI- und Mehrmonitorfälle der [Prüfliste](Glide_Manuelle_Pruefung.md); Punkte 1–4 bleiben abgenommen.
2. **Native Lieferung vervollständigen:** Mac-Vollprüfung am Referenz-Mac und Mac-Bundle/eigenständige Pakete 3.45.0 mit ihren Hash-/Signaturprüfungen. Die vorhandenen Pakete bleiben 3.42.0; aktuelle Python-Lieferung und diese Plattformtore getrennt behandeln.
3. **Bei konkretem Git-Auftrag:** Remote-Abgleich und Indexsperre klären, überprüfbare Änderungen zusammenstellen, CI auf dem endgültigen Commit abwarten. Kein automatischer Commit/Push/Merge aus Featurearbeit.
4. **Nächste Feature-/Technikphase:** WA-43, übrige WA-37/38 nach konkreter Fehlerwirkung, gemessene WA-36-Leistungsarbeit und begrenzter WA-39/WA-32-Ansichtspilot. WA-48/WA-51 sowie das Speicherpaket sind umgesetzt; sie nicht erneut als offenen Neubau anbieten.

Offen beim Inhaber: I12 (CodeQL-Einrichtung), Übernahme von tkinterdnd2 0.6.4 (WA-44), E-U1 B, E-U2 B/C, E-U3 B (WA-25) und Blockziehen, E-P1–E-P5, Integrationsrichtung E-I1, WA-23/24, FP-07 Stufe 2 (Canvas); E-U1 A–E-U3 A sind seit D55 gewählt. Paket 8 / 4.0.0 bleibt vorbereitet und pausiert. D53 erlaubt Neubewertungen, aktiviert keinen Anbieter; D52–D54 verlangen zentrale Roadmap, appweite Designgeltung und Pflege ohne automatische Feature-/Git-/Releaseentscheidung.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei; bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Keine echten Nutzerdaten oder privaten Fehlerprotokolle aus diesem Auftrag ableiten.
- Neue ausführbare Änderungen brauchen passende Prüfungen; alte Vollmatrix nur ihren eingefrorenen Bytes zuordnen. Vor einem konkret beauftragten Commit CI-Grundstufe; `--lieferstand-streng` erst beim gemeinsamen Lieferabschluss. Git-Schreibaktionen brauchen einen konkreten Auftrag; „pushen“ vom 26.10. gilt für den oben beschriebenen Kandidaten.
- Phasenabschluss: Version und Quell-/Prüf-/Ressourcenstand einfrieren, Voll-/native Matrix prüfen, anschließend 07/Showcase/Pakete und SHA-256 abgleichen. Kein Abgleich auf einen laufenden ungeprüften Kandidaten. Nach einem Versionswechsel unter Windows Zeilenenden der `eol=lf`-Dateien kontrollieren (`git ls-files --eol`), weil `versionswechsel.py` mit Plattform-Zeilenenden schreibt.
- Originalreferenzen, aktuelle QA-Versionen/-Bilder, Migrationsfixtures, Showcase und vorhandene Lieferpakete nach den Pflege- und Aufbewahrungsregeln schützen; historische Nachweise nicht nachträglich grün schreiben.

## 6. Bewusste Grenzen

Der lokale Abschluss 3.45.0 unterscheidet die eingefrorene Windows-Vollprüfung, nachfolgende Korrekturen mit gezielten Prüfungen und Python-Lieferung von der vollständigen Produkt-/Releaseabnahme. Native Mac-/Linux-/Readerabläufe, die unvollständige lokale Mac-Kopie, DPI/Mehrmonitor, physische Bedienung sowie Rechte-, Lizenz-, Signatur- und Veröffentlichungstore bleiben ausdrücklich offen. Neue Markt- oder Nutzungsbehauptungen werden aus der Zusammenführung nicht abgeleitet.
