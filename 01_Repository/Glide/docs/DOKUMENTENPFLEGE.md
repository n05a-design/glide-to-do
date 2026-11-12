# Regeln für die Dokumentenpflege

**Schutzauftrag 08.11.2026:** Im laufenden Gesamt-/Steps-Audit bleiben die historischen Originalnachweise erhalten. Die vorbereitete Alterskürzung von `tests/qa-3.50.0` und der zugehörigen Releaseplanungsfixture wurde zurückgenommen; 225 Dateien gegen die Git-Blobs von Main `d7e017f` geprüft. `ablagegroesse.GESCHUETZTE_QA_VERSIONEN` und `GESCHUETZTE_REFERENZEN` schützen diesen konkreten Bestand auch vor `ablage_kuerzen.py`. Die Größen-, Bild- und Fremdrestprüfungen gelten weiter. Der ursprüngliche Kürzungsnachweis bleibt datierte Vorgeschichte, der [Bewahrungsnachtrag](../tests/qa-3.50.7/validierung_2026-11-07/bewahrung_nachtrag.json) belegt die Rücknahme. Allgemeine neue Archivkopien entstehen dadurch nicht.

Stand 12.11.2026 · Glide 3.55.1 · Aufgabenformat 26

Am 04.11.2026 zusammengeführt und gekürzt: chronologische Auditwiederholungen durch Provenienzverweise ersetzt; geltende Regeln und Zuständigkeiten erhalten.

Gilt seit dem Auftrag des Inhabers vom 03.10.2026 („jetzt wird auch mal wieder gelöscht anstatt immer nur archiviert und `_Z` zu schreiben“) und ersetzt alle früheren Archivierungsregeln.

## Grundsätze

**Explizite Grafikausnahme 05.11.2026 (D62):** Bisherige Logo-Dateien auf Benutzerauftrag unter `20_Grafik_Master/01_Logo/Archiv` mit Hashmanifest erhalten. Keine neue allgemeine Archivregel für Dokumente, Fixtures oder QA.

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
| Verbindliches Modul-, Feature- und Bausteininventar, Wiederverwendung, Testkatalog und Systempflege | [Glide-System](../src/glide/README.md) (einzige vollständige aktuelle Tabelle) |
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

- Standzeile („Stand TT.MM.JJJJ · Glide X.Y.Z …“) und Inhalt zusammen nachführen; `versionswechsel.py` hebt die Standzeilen, ersetzt aber keinen inhaltlichen Abgleich von Status, Entscheidungen und Prüfgrenzen. Aktive Tabellen, Einstieg und Entscheidungsregister auf dieselbe aktuelle Statusquelle ausrichten; ein neuer Banner allein berichtigt keine alte Lieferzeile. Datierte Belege unverändert lassen.
- Neue Funktion: Abschnitt in [Funktionen](20_FUNKTIONEN.md), Zeile im [Glide-System](../src/glide/README.md), Marke im Entwicklungsplan, Zeile im QA-Bericht, Eintrag im CHANGELOG. Neue/umbenannte/gelöschte Module und Tests erfordern ebenfalls im selben Commit System-und-Modulpflege; die CI prüft Dateivollständigkeit. **Eigenständige Systemversion:** `GLIDE_SYSTEM_VERSION` und der Versionsverlauf im Glide-System werden bei jeder inhaltlichen Pflege synchron aktualisiert (V1.0 als Initialstand, unabhängig von der Glide-App-Version); keine versionsbenannten Kopien des Katalogs erstellen. Keine eigene Vertragsdatei je Version.
- Vor dem Commit `python3 -B tests/tools/ci_grundstufe.py` (Stand, Links, Index, Datenschutz, Ablagegröße, Synchronisation).
- Produktionskommentare erklären Invarianten, technische Gründe und Plattformbesonderheiten; Auftragsnummern und Entwicklungserzählungen gehören ins CHANGELOG. Eine reine Kommentarbereinigung lässt den Syntaxbaum unverändert.

## Was die Standprüfung erzwingt

`tests/tools/standpruefung.py` (Regeln R1–R15) prüft alle aktiven Markdown-Dokumente: Standzeile mit der aktuellen Version, Formatstufen gegen den Code, bekannte überholte Aussagen, vollständige Modullisten, erreichbare relative Links, aktuelle Titel und erste Vollprüfungsaufrufe, Suitezahl in Standzeilen. Erzeugte Pakete unter `build/` sind Kopien, keine aktiven Dokumente. Dokumente mit Version oder Datum im Namen sowie der gehashte Mac-Paketlizenzbeleg gelten als festgeschrieben; seit 03.10.2026 gibt es unter den gepflegten Dokumenten keine mehr.

Die Standprüfung kontrolliert definierte Muster und Dateiziele. Beim fachlichen Abgleich zusätzlich Symbolnamen, Aufrufer und relevante Tests im Quellstand prüfen. Bei Markdown-Links mit Fragment auch die Zielüberschrift oder den expliziten HTML-Anker prüfen. Releaseaussagen mit dem tatsächlich getesteten Commit und den jeweiligen Jobs abgleichen.

## Pflegevertrag und frühere Audits

Seit D52–D54 führt jede Entwicklungsrunde den bestehenden Entwicklungsplan fort. Auftrag/Entscheidung, Implementierung, Prüfung, Lieferung und menschliche Abnahme getrennt ausweisen. Designvorgaben bleiben in den Design Richtlinien, externe Fakten im Marktbericht, technische Befunde in der Analyse und Ergebnisse im QA-Bericht. Keine parallele Roadmap und keine wiederholten Sitzungsberichte in Einstiegsdateien anlegen. Dort auf den aktuellen zuständigen Abschnitt verweisen, damit derselbe Status nicht an mehreren Stellen veraltet.

Die zweiwöchentliche Recherche darf belegte Fakten und markierte Vorschläge lokal aktualisieren; sie entscheidet keine Features und führt keine Git-/Releaseaktion aus. Ihr tatsächlicher Automationsstatus ist bei Bedarf gesondert zu prüfen.

Frühere Datei-/Dokumentaudits stehen in [Analyse §13.17](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1317-datei--und-dokumentationsaudit-vom-27102026), [§13.20](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1320-einarbeitung-des-abnahmeaudits-und-dateiabgleich-vom-29102026) und [§13.21](../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1321-abschlussabgleich-von-roadmap-featurelisten-und-dokumentation). Die datierten Nachweise bleiben innerhalb ihrer Aufbewahrung erhalten; frühere Fundzahlen sind keine heutigen Bestandszahlen. Der Word-/PDF-Abnahmebericht ist ein unveränderter Prüfbeleg. Historische Referenzen beim Kürzen auf eine belegte Git-Fassung umstellen; vorhandene Linkanker bei präziseren Überschriften als Alias erhalten.

Separate Worktrees, Branches, Stashes und Git-Objekte gehören nicht zur Dokumentbereinigung. Arbeitskopien erst nach Prüfung ihrer eigenen Änderungen und lokalen Belege sowie gesicherter Integration auflösen. Ignorierte Dateien sind nicht automatisch entbehrlich. Crashdumps, Originaleingänge und Nutzerreferenzen nach ihrem Zweck prüfen; keine Sammellöschung aufgrund eines Ignore-Eintrags.

Die [Bereinigung vom 04.11.2026](https://github.com/n05a-design/glide-to-do/blob/61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d/01_Repository/Glide/tests/qa-3.50.2/dokumentpflege_2026-11-04/README.md) enthält Dokumentregister, Einzeldatei-Löschmanifest und Abschlussprüfungen. Es entstehen keine neuen Dokumentarchive; Git trägt die Vorfassungen.

## Öffentliche Featurepflege ab 3.50.0

Bei jeder erfolgreich umgesetzten oder geänderten Nutzerfunktion werden im selben Arbeitsgang README › „Was Glide kann“, `20_FUNKTIONEN.md`, `release_notes.CATALOG`, CHANGELOG und Entwicklungsplan inhaltlich abgeglichen. Marketing nennt verfügbare Fähigkeiten und keine ungeprüften Versprechen. Datierte Prüfbelege bleiben unverändert; aktuelle Lieferstände kommen ausschließlich aus dem neuesten QA-/Liefernachweis. Die Standprüfung bleibt Pflicht. Öffentliche Bezeichnung von 3.50.0: „Erster öffentlicher Stand“, interner Status: „öffentliche erste Beta“.

**Versionspflege 05.11.2026, 3.50.4:** 19 überalterte 3.47.0-Dateien vorab bytegleich lokal gesichert und nach der vorhandenen Aufbewahrungsregel gekürzt; acht historische Links auf bytegleich verifizierte Git-Fassung umgestellt. Git-Index unverändert. Pfad-/Hashmanifest im 3.50.4-Abnahmenachweis.
