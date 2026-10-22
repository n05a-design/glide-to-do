# Glide – Übergabe an eine neue Sitzung

Stand 22.10.2026 · Glide 3.44.0 · Aufgabenformat 26 · lokaler Featurekandidat, getrennte Lieferung

**Aktuell nach Roadmap-Paket 3 (22.10.2026):** Quelle `604014f9a85e9c38a2d19141a3b1039a7a9f798c39d7dcbcb0387569b0f1f68f`, weiterhin 3.43.1 / Format 26. Sieben weitere Struktur-/Seitenleistenadapter verwenden die gemeinsamen Änderungsrahmen; aktuelle Referenzen nach Dialog/Snapshot, Editorübernahme vor Ordnerpapierkorb und ehrliche Schreib-/UI-Folgeergebnisse. Der Kalender überspringt überholte Expansion nach dem Lesen. 856 Fachtests, 16 abgedeckte Schutzfälle und passende Datenintegritäts-/Redo-/Appregressionen; neuer 5.000er-Leistungspunkt. [Plan §21.9](Glide_Entwicklungsplan.md#219-drittes-umsetzungspaket-strukturabschluss-und-kalenderwechsel), [Prüfstand](../01_Repository/Glide/tests/qa-3.43.1/roadmap_paket3_2026-10-22/README.md). Kein neuer Gesamt-/Native-/Lieferabschluss.

**Aktuell nach Roadmap-Paket 2 (21.10.2026):** Lokaler Kandidat `fefde636c8b7a639adf4d86f7e8cac7567037a81b80b87d812f0d827bdc3a20e`, weiterhin 3.43.1 / Format 26. FP-03 Stufe 2 ergänzt gespeicherte Liste/Tabelle/Spaltenboard, Gruppierung, Sortierung, eigene Tabellenspalten/Breiten und „Als Ansicht speichern“. Eigener oberster Namespace, dieselben Originalaufgaben und bestehender Gruppen-/Undo-Weg. 847 Fachlogiktests; 15 gezielte Ansichtenfälle einschließlich Neustart, App-Sicherung, Altleser, Schreibfehler, echter Sortier-/Zieh-/Tastatureinstiege und vier UI-Konfigurationen. Die bestehende Oberflächenregression wurde vor der letzten Bindung des neuen Auswahlfelds an seinen Tk-Host geprüft; genaue Prüfstände im [Paketnachweis](../01_Repository/Glide/tests/qa-3.43.1/ansichten_darstellung_2026-10-21/README.md). Zusatz-Audit eingeordnet: Grundrichtung bestätigt, Kalender-Wartezeit als ungemessener WA-36-Prüfpunkt, kein Rücksetzen der bereits umgesetzten Schutzarbeit. Kein neuer 101-Suiten-/CI-/Native-/Lieferabschluss; 07 und Pakete bleiben unverändert.

Am 21.10.2026 zusammengeführt und gekürzt: aktueller Stand, Quellenhierarchie und Fortsetzung stehen hier; Aufgaben ausschließlich im Entwicklungsplan, technische Befunde in der Analyse, Prüfergebnisse im QA-Bericht. Historische Originalaufträge und Messbelege bleiben erhalten. Auf die Dokumentationsrunde folgt jetzt der ausdrückliche Auftrag, die Roadmap in zusammenhängenden Paketen mit angemessener Prüfarbeit umzusetzen.

**Erstes Roadmap-Paket umgesetzt:** WA-31 lokaler Sitzungsbesitz, WA-36 Mehrfachauflösung im Erledigen-/Zähl-/Serien-/Checklistenweg, WA-38/37 Speicher-/Mutationsresultate und kritische WA-40-Aufrufer; zusätzlich vollständige FP-06-Auftrags-/Kontextvorschau. Abschlussquelle `45354b63…`, weiterhin 3.43.1 / Format 26. 843 Fachtests, 152 Werkzeugtests und 23 passende Appfälle am breiten Zwischenstand grün; Freigabe-/Ordnerschranke danach gezielt nachgeprüft. Die Fachtests enthalten 1.000 echten OS-Sperrübergaben zwischen zwei Prozessen und Abbruchfreigabe. Kein neuer 101-Suiten-/Native-/Lieferabschluss. [Plan §21.7](Glide_Entwicklungsplan.md#217-erstes-umsetzungspaket-schreibbesitz-mehrfachaktionen-und-ki-vorschau), [Paketnachweis](../01_Repository/Glide/tests/qa-3.43.1/roadmap_paket1_2026-10-21/README.md).

**Zuvor eingearbeitet, eigener Dokumentationsbeleg:** Die vom Inhaber eingereichte „Validierung der Codebasis-Analyse“ wurde am damaligen Kandidaten `3b93a24a…` gegengeprüft und in [Analyse §13.8](Glide_Analyse.md#138-abgleich-der-eingereichten-codevalidierung) integriert. [Plan §21.6](Glide_Entwicklungsplan.md#216-technische-folge-aus-der-codevalidierung) war die technische Folge; deren anschließende Umsetzung steht oben und in §21.7. Die damaligen Dokumentprüfungen und unveränderten Quell-/Lieferhashes stehen im [Validierungsnachweis](../01_Repository/Glide/tests/qa-3.43.1/codevalidierung_2026-10-21/README.md); sie sind keine Prüfungen des späteren Umsetzungskandidaten.

## 1. Tatsächlicher Stand

| Ebene | Am 21.10.2026 festgestellter Stand | Bedeutung |
|---|---|---|
| Git-Basis | Zweig `codex/bildvorschauen-wa26-2026-10-18`, HEAD `1042727`; live gelesenes GitHub-`main` auf demselben Commit | Featurearbeiten liegen als umfangreiche lokale Änderungen vor. Vor dieser Dokumentrunde: 70 geänderte versionierte Dateien und 32 unversionierte Statuseinträge, teils Ordner; Index leer |
| Quellkandidat nach Roadmap-Paket 3 | 3.43.1 / Format 26, 79 eigene Laufzeitdateien plus Prototyp, unverändert 101 registrierte Integrationssuiten | Zusätzlich FP-03 beide Stufen, WA-31/36/37/38/40-Schnitte einschließlich Strukturabschluss/Kalenderwechsel und vollständige KI-Vorschau. Registrierung ist kein bestandener Gesamtlauf |
| Gezielter aktueller Nachweis | Paket 3: 856 Fachtests, 16 abgedeckte Schutzfälle, passende Integrationsregressionen und Messung; frühere FP-03-Belege bleiben getrennt | Alte Paket-1-/FP-02-/FP-03-/99-Suiten-/Analysebelege bleiben ihren jeweiligen Bytes zugeordnet; kein erneuter Gesamtabschluss |
| Vorherige Grundstufe vor Roadmap-Paket 1 | Exitcode 0; 19 Schritte, 18 ausgeführt und ein Lieferhinweis; 831 Fachtests mit/ohne Systemzeitzonen und 152 Werkzeugtests | Datierter Vorzustand `3b93a24a…`, kein neuer CI-/101-Suiten-/Native-Beleg für das nachfolgende Umsetzungspaket |
| Python-Lieferung `07_Python-Versionen` | weiterhin 3.43.1 / Format 25, unverändert; jetzt 22 Laufzeit-/Ressourcenunterschiede zur Quelle | Der neue Featureumfang ist dort noch nicht angekommen. Dieselbe Versionsnummer bezeichnet verschiedene Entwicklungsstände |
| Eigenständige Pakete | Mac und Windows weiter 3.42.0; drei bereits dokumentierte Frameworkdateien fehlen weiterhin in der lokalen Mac-Kopie | Keine neue Paket-, Start-, Signatur- oder Releasefreigabe. Frühere 102/102- bzw. 327/330-Hashnachweise bleiben datierte Belege |

Dateihashes, tatsächliche Nachprüfung und Grenzen: [Bestandsnachweis 21.10.](../01_Repository/Glide/tests/qa-3.43.1/standaufnahme_2026-10-21/README.md). Verbindliche Quell-/Prüf-/Liefermatrix: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Der eingefrorene breite Analysezwischenstand `916c777…` ist vom späteren FP-02-Abschluss getrennt; seine roten Teilprüfungen werden nicht rückwirkend geändert.

**Git-Auftrag beendet:** Der einmalige Auftrag vom 21.10. wurde verspätet zugestellt und nach roter Grundstufe sowie Änderungen während der Prüfung ohne Commit/Push beendet und deaktiviert. Spätere grüne Teilprüfungen reaktivieren ihn nicht. Der ältere Ablage-/PR-Auftrag vom 18.10. ist historische Auftragsherkunft. [Nachweis](../01_Repository/Glide/tests/qa-3.43.1/gitauftrag_2026-10-21/README.md).

## 2. Zuständige Dokumente

Die Quellen ergänzen sich nach Gegenstand. Ein Auftrag oder Beschluss bestimmt den Umfang; Code und Nachweise belegen getrennt, was tatsächlich implementiert, geprüft und geliefert ist. Ein älterer Plantext ersetzt keinen neueren konkreten Auftrag, ein grüner Test keine Produktentscheidung.

| Thema / Lesefolge | Verbindliche Quelle |
|---|---|
| Arbeitsregeln und Produktgrenzen | [AGENTS.md](../01_Repository/Glide/AGENTS.md), [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Bestätigte Richtung D01–D54, konkrete Aufträge und Prüfablauf | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md); D49 bleibt Auslegung mit Korrekturvorbehalt, neue Entscheidungen ab D55 |
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

Bestehende Quellen fortschreiben: ein Thema, ein Dokument. Diese Runde gleicht widersprüchliche aktive Format-, Feature-, Entscheidungs- und Git-Statusaussagen ab; sie verändert keine historischen Messergebnisse. Die Bestandsaufnahme liegt im bestehenden Analysekapitel, kein zweiter Plan oder neues Gesamtdokument entsteht.

Die globale Ablageprüfung vom 18.10. einschließlich Git und damaliger Arbeitskopien bleibt im [Ablagenachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Die heutige Dokumentrunde ersetzt diese physische Vollinventur nicht. Vorhandene Änderungen wurden vor der Bearbeitung privat außerhalb des Projekts gesichert. Mehrdeutige Dateien, alte Affinity-Quellen, andere Zweige und Stashes werden nicht aufgrund eines Ignore-Eintrags oder historischen Löschwunschs entfernt.

Der [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md), [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) und 28 lokale Originalbilder bleiben Eingangsbelege. Bilder enthalten teilweise Kontoangaben, bleiben vom Git-Upload ausgeschlossen und müssen bei Rechner-/Agentenwechsel ausdrücklich mitgegeben werden. Aufgabenstatus nur im Plan §17/§21.

## 4. Nächste Arbeit und offene Entscheidungen

Der erste zusammenhängende Umsetzungsstand steht in [Plan §21.7](Glide_Entwicklungsplan.md#217-erstes-umsetzungspaket-schreibbesitz-mehrfachaktionen-und-ki-vorschau). WA-31 wurde im Kandidaten geschlossen, WA-36/37/38/40 im abgegrenzten Umfang umgesetzt; weitere direkte Caller, gemessene Snapshot-/Schreib-/Renderkosten, größere WA-39-/WA-32-Auslagerungen bleiben Folgeschnitte. FP-03 Stufe 2 ist im Kandidaten umgesetzt (§21.8); weitere Strukturcaller und Kalenderwechsel wurden in §21.9 ergänzt. Die alten Neubauvorschläge nicht nochmals als unangetastete Aufgaben ausgeben. Gezielte Paketprüfungen bündeln; D51-Gesamt-/Native-/Lieferabschluss am gewählten Phasenende.

Die zusätzlichen WA-23/24-Optionen, E-U1–E-U3, E-P1–E-P5 und Integrationsauswahl E-I1 bleiben in ihren dokumentierten Grenzen offen. D53 erlaubt deren Neubewertung, aktiviert keinen Anbieter. D51 bündelt gezielte Paketprüfungen und einen eingefrorenen Gesamtabschluss am Phasenende; die vorgeschlagenen Gesamtphasen sind nicht pauschal bestätigt. Paket 8 / 4.0.0 ist vorbereitet, nicht geliefert. D52–D54 verlangen zentrale Roadmap, appweite Designgeltung und Pflege ohne automatische Feature-/Git-/Releaseentscheidung.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei; bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Keine echten Nutzerdaten oder privaten Fehlerprotokolle aus diesem Auftrag ableiten.
- Neue ausführbare Änderungen brauchen passende Prüfungen; alte Vollmatrix nur ihren eingefrorenen Bytes zuordnen. Vor einem konkret beauftragten Commit CI-Grundstufe; `--lieferstand-streng` erst beim gemeinsamen Lieferabschluss. Der beendete Git-Auftrag bleibt beendet.
- Phasenabschluss: Version und Quell-/Prüf-/Ressourcenstand einfrieren, Voll-/native Matrix prüfen, anschließend 07/Showcase/Pakete und SHA-256 abgleichen. Kein Abgleich auf einen laufenden ungeprüften Kandidaten.
- Originalreferenzen, aktuelle QA-Versionen/-Bilder, Migrationsfixtures, Showcase und vorhandene Lieferpakete nach den Pflege- und Aufbewahrungsregeln schützen; historische Nachweise nicht nachträglich grün schreiben.

## 6. Bewusste Grenzen

Die heutige Stand- und Dokumentationsprüfung ist keine neue vollständige Produktabnahme. Native Mac-/Linux-/Readerabläufe, die unvollständige lokale Mac-Kopie, DPI/Mehrmonitor, physische Bedienung sowie Rechte-, Lizenz-, Signatur- und Veröffentlichungstore bleiben ausdrücklich offen. Neue Markt- oder Nutzungsbehauptungen werden aus der Zusammenführung nicht abgeleitet.
