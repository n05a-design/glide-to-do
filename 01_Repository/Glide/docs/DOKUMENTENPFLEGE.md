# Regeln für die Dokumentenpflege

Stand 29.10.2026 · Glide 3.49.0 · Datenformat 26

**Lokaler Abgleich 29.10.2026:** Abnahmebefunde in den zuständigen Quellen eingearbeitet; [Analyse §13.20](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026), [Dateiinventar/Dokumentregister/Schlusskontrollen](../tests/qa-3.49.0/dokumentabgleich_2026-10-29/README.md). Der Word-/PDF-Bericht bleibt ein unveränderter datierter Prüfbeleg. Historische QA-Rohdaten, Originalreferenzen und Lieferstände werden nicht umetikettiert oder aus diesem Abgleich gelöscht.

Gilt seit dem Auftrag des Inhabers vom 03.10.2026 („jetzt wird auch mal wieder gelöscht anstatt immer nur archiviert und `_Z` zu schreiben“) und ersetzt alle früheren Archivierungsregeln.

Abgleich 18.10.2026: [Dokumentregister und konkrete Pflegeergebnisse](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#7-dokumentenpflege-und-zuständigkeit). Originalaufträge, D45-Tafeln, Migrationsfixtures und Paketlizenzkopien wurden von entbehrlichen Themendubletten unterschieden; ein erforderlicher Lieferbeleg ist kein zweites aktuelles Fachdokument. D51 bündelt mehrere Pakete in einer Prüfphase, ohne die Aufbewahrungsregeln zu verändern.

## Grundsätze

- **Ein Thema, ein Dokument.** Beschreiben zwei Dokumente dasselbe, werden sie zusammengeführt; das überholte wird gelöscht, nicht archiviert. Git trägt jede Vorfassung (`git log --follow <Datei>`).
- **Fortschreiben statt kopieren.** Keine Versionskopie, keine `archiv/`-Ordner, keine `_Z`-Vormerkung für Dokumente. Dateinamen tragen kein Datum und keine Version; der Stand steht in der Standzeile.
- **Erledigtes kennzeichnen statt aufbewahren.** Aufgaben tragen im [Entwicklungsplan](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) ihre Marke (✅ erledigt mit Version, ◐ teilweise, ▶ beauftragt, ○ offen, ◇ Zukunft, ✕ bewusst nicht). Abgeschlossene Versionen stehen im [QA-Bericht](07_QA_BERICHT.md) und im CHANGELOG.
- **Code-relevant oder aktuell.** Behalten wird, was den heutigen Code, seine Prüfung, Daten, Entscheidungen oder die offene Planung beschreibt. Recherchen und Zwischenstände werden nach Übernahme ihrer gültigen Ergebnisse gelöscht.
- **Aufbewahrung:** Archive und Nachweise nur der sieben neuesten Versionen (`07_Python-Versionen/Archiv`, `tests/qa-<Version>`, Releaseplanungen; je Datenformat bleibt eine Releaseplanung als Lesbarkeitsbeleg), Fensterbilder nur der drei neuesten. Rohprotokolle (`*.log`) bleiben lokal und werden nie versioniert; auch lokale Rohprotokolle und Fensterbilder werden nach diesen Versionsgrenzen gekürzt. `scripts/pflege/ablage_kuerzen.py` erfasst versionierte und neue, nicht ausgeschlossene Dateien; die CI-Grundstufe prüft versionierte Dateien (Schritt „Ablagegröße“). Beide erfassen ausgeschlossene lokale Altdateien nicht. Deshalb bei einer Ablageprüfung zusätzlich den tatsächlichen Dateibestand einschließlich ausgeschlossener QA- und Fixture-Archive prüfen. Die Bild-Altersgrenze gilt unabhängig vom Unterordnernamen (`fenster/`, `screenshots/`, `fensterbilder/`); das Git-Verbot neuer `fenster/`-Fotos ist kein lokaler Löschgrund innerhalb der drei neuesten Versionen. Separate Git-Worktrees bleiben eigenständige Arbeitskopien.
- **Leere Ordner** und Ordner, die nur README und Archiv enthalten, werden aufgelöst.
- **Synchronisationskopien** (`<Name>-<Gerätename>.md`, etwa von OneDrive) sind keine Dokumente: mit dem Original zusammenführen, dann löschen. Eine Kopie im Index ist kein Ersatz für die Zusammenführung.
- **Belege bleiben Belege:** Nutzeraufträge, Messwerte und Prüfergebnisse innerhalb der Aufbewahrung werden nicht umetikettiert oder nachträglich geändert.
- **Nutzerreferenzen für offene Anforderungen:** Der Auftrag vom 15.10.2026 verlangt, das [UI-/UX-Paket](../../../00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md) mit Originalauftrag und 28 Screenshots für spätere Agenten zu erhalten. Das sind Eingangsreferenzen, keine neu erzeugten QA-Fensterbilder. Solange Anforderungen oder ihre Referenzfunktion offen sind, nicht mit der Drei-Versionen-Grenze für QA-Aufnahmen entsorgen. Originalbilder wegen Kontoangaben lokal und vom Git-Upload ausgeschlossen halten; bei Übergaben ausdrücklich mitgeben. Nach Abschluss Zweck und Verlinkung prüfen, keine ungeprüfte Sammellöschung.

## Dokumente und ihre Zuständigkeit

| Thema | Einziges Dokument |
|---|---|
| Einstieg, Stand, Regeln, nächste Schritte | `00_Arbeitsvorbereitung/Glide_Uebergabe.md` |
| Aufgaben, Backlog, Stufen, Ziele | `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md` |
| Analyse (Funktionen, Oberfläche, Entscheidungen, Nutzung, Abgleich Dokumentation ↔ Code) | `00_Arbeitsvorbereitung/Glide_Analyse.md` |
| Markt und Vorbilder | `00_Arbeitsvorbereitung/Glide_Markt_und_Vorbilder.md` |
| Manuelle Prüfung (Mac, Windows, Linux) | `00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md` |
| Ausführbarer UI-/UX-Nutzerauftrag und Eingangsreferenzen vom 15.10.2026 | `00_Arbeitsvorbereitung/Featurepaket_UI_UX/PROMPT.md`; Originalauftrag, Bildzuordnung und Manifest daneben; Aufgabenstatus ausschließlich im Entwicklungsplan |
| Konkrete Gestaltungsvorgaben des Benutzers, Informationshierarchie, Buttonschutz | [DESIGN_RICHTLINIEN.md](DESIGN_RICHTLINIEN.md); bestehende Produkt-/Architekturregeln referenzieren, nicht kopieren |
| Entscheidungen, Leitgedanken des Inhabers, Arbeitsablauf | [ARBEITSRICHTUNG.md](ARBEITSRICHTUNG.md) |
| Produktgrenzen und Prinzipien | [01_PRODUCT_CONSTRAINTS.md](01_PRODUCT_CONSTRAINTS.md) |
| Architektur, Performance-Regeln, Tk-Fallstricke | [02_ARCHITECTURE.md](02_ARCHITECTURE.md) |
| Prüfplan | [05_QA_TESTPLAN.md](05_QA_TESTPLAN.md) |
| Datenformat, Backups, Austauschformat | [06_DATA_BACKUP_MIGRATION.md](06_DATA_BACKUP_MIGRATION.md) |
| Geprüfter Stand | [07_QA_BERICHT.md](07_QA_BERICHT.md) |
| Veröffentlichung, Lizenz, Signierung, Store, GitHub-Auftritt | [10_VEROEFFENTLICHUNG.md](10_VEROEFFENTLICHUNG.md) |
| Verhalten der Funktionen | [20_FUNKTIONEN.md](20_FUNKTIONEN.md) |
| Vorlagen in der Praxis | [27_VORLAGEN_PRAXISANLEITUNG.md](27_VORLAGEN_PRAXISANLEITUNG.md) |
| Sicherheitsregeln und Vertrauensgrenzen der Anwendung | `SECURITY.md` im Quellbaum; Meldeweg und Schutz des öffentlichen Repositorys in `SECURITY.md` der Wurzel |
| Eingereichte externe Analysen, Validierungen und Gutachten | kein eigenes Dokument: Einordnung in der Analyse (§13.8, §13.10, §13.12), Aufgaben im Entwicklungsplan, Eingangshash und Prüfprovenienz im QA-Nachweis der Runde |
| Einzelentscheidungen mit eigenem Gegenstand | `decisions/` (Produktregister, tkdnd, Arbeitsbegleiter, Gruppe/Ordner/Überschrift, Systembenachrichtigungen) |
| Änderungsverlauf | `CHANGELOG.md` (sieben neueste Versionen ausführlich, ältere als Zeile) |

Neue Dokumente unter `docs/` nur, wenn kein bestehendes das Thema trägt; sie gehören in den [Index](00_INDEX.md).

## Pflege bei jeder Runde

- Standzeile („Stand TT.MM.JJJJ · Glide X.Y.Z …“) und Inhalt zusammen nachführen; `versionswechsel.py` hebt die Standzeilen, ersetzt aber keinen inhaltlichen Abgleich von Status, Entscheidungen und Prüfgrenzen.
- Neue Funktion: Abschnitt in [Funktionen](20_FUNKTIONEN.md), Marke im Entwicklungsplan, Zeile im QA-Bericht, Eintrag im CHANGELOG. Keine eigene Vertragsdatei je Version.
- Vor dem Commit `python3 -B tests/tools/ci_grundstufe.py` (Stand, Links, Index, Datenschutz, Ablagegröße, Synchronisation).
- Produktionskommentare erklären Invarianten, technische Gründe und Plattformbesonderheiten; Auftragsnummern und Entwicklungserzählungen gehören ins CHANGELOG. Eine reine Kommentarbereinigung lässt den Syntaxbaum unverändert.

## Was die Standprüfung erzwingt

`tests/tools/standpruefung.py` (Regeln R1–R14) prüft alle aktiven Markdown-Dokumente: Standzeile mit der aktuellen Version, Formatstufen gegen den Code, bekannte überholte Aussagen, vollständige Modullisten, erreichbare relative Links, aktuelle Titel und erste Vollprüfungsaufrufe, Suitezahl in Standzeilen. Erzeugte Pakete unter `build/` sind Kopien, keine aktiven Dokumente. Dokumente mit Version oder Datum im Namen sowie der gehashte Mac-Paketlizenzbeleg gelten als festgeschrieben; seit 03.10.2026 gibt es unter den gepflegten Dokumenten keine mehr.

## Ablageprüfung vom 18.10.2026

**Pflegevertrag seit D52–D54 (21.10.2026):** Jede Entwicklungsrunde führt den bestehenden Entwicklungsplan fort, insbesondere seinen aktuellen Roadmap-Abgleich, und trennt Auftrag/Entscheidung von Implementierung, Prüfung, Lieferung und menschlicher Abnahme. Gestaltung bleibt allein in den appweit geltenden Design Richtlinien, externe Fakten im Marktbericht, technische Befunde in der Analyse und Resultate im QA-Bericht. Die zweiwöchentliche Recherche darf belegte Fakten und markierte Vorschläge lokal aktualisieren; sie entscheidet keine Features und führt keine Git-/Releaseaktion aus. Keine parallele Roadmap oder wiederholte chronologische Aufgabenliste anlegen.

Der [globale Nachweis](../tests/qa-3.43.1/ablageaudit_2026-10-18/README.md) erfasst Dateien, Ordner, vollständige Hashes und Dokumentzuständigkeiten einschließlich Git und lokaler Arbeitskopien. Ignorierte Dateien sind nicht automatisch entbehrlich. Originalreferenzen, aktuelle QA-Bilder, Migrationsfixtures und bestehende Lieferstände werden unabhängig vom Git-Status geschützt. Historische Rohbelege bleiben historisch; doppelte Erzählungen werden in der aktuellen Quelle zusammengeführt.

Git-Objektverdichtung erfolgt ohne History-, Ref- oder Reflogverlust und mit Objektmengenvergleich. Arbeitskopien entfallen erst nach Prüfung ihrer eigenen Änderungen und lokalen Belege, Sicherung außerhalb der Projektwurzel und Integration; Branches und Stashes bleiben erhalten. Ein abgelehnter Löschschritt bleibt mit seinem tatsächlichen Ergebnis im Journal.

## Ablageprüfung vor Push und Merge vom 25.10.2026

Der [Nachweis vom 25.10.2026](../tests/qa-3.44.0/ablagepruefung_2026-10-25/README.md) prüfte den gesamten tatsächlichen Bestand einschließlich ignorierter QA-Dateien, Git und separater Arbeitskopien. Die Aufbewahrungsgrenzen sind eingehalten; Originalbilder, Fixtures und Lizenz-/Lieferkopien bleiben erhalten. Identischer Inhalt ist bei Showcase-/Fixture-Spiegeln und eigenständigen Lieferressourcen beabsichtigt. Die geplante Cachebereinigung wurde von der automatischen Freigabeprüfung vor Ausführung blockiert; keine Einsparung behaupten. Git-Historie, Stashes und die fünf Worktrees bleiben erhalten. Gegenwärtige Mergegrenzen stehen im Entwicklungsplan, technische Einzelbefunde im datierten Nachweis.

## Dokumentabgleich vor Push vom 27.10.2026

Der erneute Auftrag prüft das Dokumentregister gegen Quelle 3.47.0 / Format 26, die gezielten Paketfälle und tatsächliche Python-/Showcase-Lieferung. Inhaltliche Befunde und Korrekturen stehen allein in [Analyse §13.16](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1316-dokumentabgleich-vor-dem-push-am-27102026), Gitauftrag/Aufgaben im [Plan §21.25](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2125-dokumentabgleich-und-pushauftrag-vom-27102026); vollständiges Register/Links/Anker und CI im [Nachweis](../tests/qa-3.47.0/folgepakete_2026-10-27/README.md). Historische Ergebnisse bleiben unverändert. Präzise Ignore-Regeln halten neue QA-Screenshots und die lokale Tk-Prüfumgebung vom Gittransport fern; sie löschen keine lokalen Dateien.

## Erneuter Datei- und Dokumentabgleich für 3.48.0

Auftrag vom 27.10.2026: alle Dateien nach Inhalt, Stand und Version prüfen. Aktuelle Korrekturen in [Analyse §13.17](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1317-datei--und-dokumentationsaudit-vom-27102026); Inventar/Hashes, Register und Grenzen im [Audit](../tests/qa-3.48.0/dokumentationsaudit_2026-10-27/README.md). Historische Rohbelege behalten ihre damaligen Angaben; spätere Korrekturen stehen als Nachtrag davor. Die 470-Dateien-Referenz des Featurelaufs bleibt erhalten, obwohl eine enthaltene README anschließend berichtigt wurde. Den neuen Dokumentabschluss mit dessen Auditnachweis beurteilen, den alten Hashabschluss nicht umetikettieren.

595 lokale QA-Dateien liegen außerhalb der aktuellen Aufbewahrung: zehn Rohlogs 3.42.0 und 585 Fensterbilder 3.43.1–3.45.0. Einzelpfad/Hash/Grund sind erfasst, Status **offene Bereinigungskandidaten**; aus dem Prüfauftrag keine Sammellöschung vorgenommen. Die 28 Original-Nutzerbilder bleiben unabhängig davon geschützt. Zusätzliche WA-41-Sicherung mit Dumps/Anfangsbestand explizit Git-ausgeschlossen; kein öffentliches Uploadpaket.
