# Glide – Übergabe an eine neue Sitzung

Stand 22.10.2026 · Glide 3.44.0 · Aufgabenformat 26 · Python-Lieferung 3.44.0, eigenständige Pakete 3.42.0

**Aktuell nach Phasenabschluss 3.44.0 (22.10.2026):** Der bisher nur lokal liegende Featurekandidat (FP-01–FP-06, FP-07 Stufe 1, WA-26, Schutzrunde WA-27–WA-30, Roadmap-Pakete 1–3) ist auf ausdrücklichen Auftrag als **3.44.0** versioniert, auf einer eingefrorenen Kopie vollständig unter Windows geprüft, nach `07_Python-Versionen` und in den Showcase geliefert und über einen Pull Request in `main` zusammengeführt. Der Vorlauf der Vollprüfung fand 120 Schritte, davon 109 grün, 10 rot und 1 übersprungene Sichtprüfung. Ursachen: fehlender Aktionskatalogeintrag „Als Ansicht speichern …“ aus FP-03 Stufe 2 (fünf Suiten), zwei veraltete Prüferwartungen an Format 25 bzw. ICS vor FP-02, die seit WA-31 gehaltene Sperrdatei im Markdown-Bytevergleich, ein Showcase ohne FP-02-Serie und ein nicht reproduzierbarer Fokusfall in `test_ui39`; korrigiert und im Abschlusslauf ⟨ABSCHLUSS⟩. Quelle und Python-Lieferung tragen wieder denselben Stand (SHA-256-Abgleich). Offen: Mac-Vollprüfung und -Bundle, eigenständige Pakete 3.44.0, native Linux-/Mac-Matrix und menschliche Abnahmen. [Plan §21.10](Glide_Entwicklungsplan.md#2110-phasenabschluss-3440), [Phasennachweis](../01_Repository/Glide/tests/qa-3.44.0/phasenabschluss_2026-10-22/README.md).

**Vorgeschichte der Phase (18.–22.10.2026):** WA-26, FP-05, FP-06, FP-04, FP-07 Stufe 1, FP-03 beide Stufen und FP-02 beide Stufen (Aufgabenformat 26) wurden nacheinander gezielt geprüft; anschließend Roadmap-Paket 1 (WA-31 Schreibbesitz, WA-36 Mehrfachauflösung, WA-37/38 Speicher-/Mutationsergebnis, kritische WA-40-Pfade, vollständige FP-06-Vorschau), Paket 2 (FP-03 Stufe 2) und Paket 3 (Strukturcaller, Editorübernahme vor Ordnerpapierkorb, UI-Folgefehlervertrag, Kalenderwechsel). Einzelbelege: [Plan §21.7–§21.9](Glide_Entwicklungsplan.md#217-erstes-umsetzungspaket-schreibbesitz-mehrfachaktionen-und-ki-vorschau) und die Paketnachweise unter `tests/qa-3.43.1/`. Die eingereichte Codevalidierung und der Zusatz-Audit sind in [Analyse §13.8/§13.10](Glide_Analyse.md#138-abgleich-der-eingereichten-codevalidierung) eingeordnet.

## 1. Tatsächlicher Stand

| Ebene | Stand nach Phasenabschluss 22.10.2026 | Bedeutung |
|---|---|---|
| Git | Zweig `claude/phasenabschluss-3.44.0` von `1042727`: Kandidat unverändert gesichert (`5e915a7`), Versionswechsel (`d17675e`), Vollprüfung/Lieferung/Dokumente; Pull Request in `main` ⟨PR⟩ | Vorher lag die gesamte Featurearbeit uncommittet im lokalen Zweig `codex/bildvorschauen-wa26-2026-10-18`; GitHub-`main` stand auf `1042727` |
| Quelle | 3.44.0 / Format 26, Einstellungen 2, 79 eigene Laufzeitdateien plus Prototyp, 101 Integrationssuiten, 857 Fachtests, 152 Werkzeugtests | Abschluss-App-SHA-256 und Manifest im Phasennachweis |
| Windows-Vollprüfung | eingefrorene Kopie außerhalb von OneDrive, Python 3.14.7 / Tk 9.0.4: ⟨ABSCHLUSS⟩ | Vorlauf mit echten Befunden bleibt als roter Beleg erhalten |
| CI-Grundstufe | ⟨CI⟩ | GitHub-Lauf nach dem Push separat gelesen |
| Python-Lieferung `07_Python-Versionen` | 3.44.0 / Format 26, bytegleich zu `src/glide` (SHA-256); 3.43.1 im Archiv, 3.39.0 nach Aufbewahrungsregel entfallen | Quelle und Lieferung tragen wieder denselben Stand |
| Showcase `05_Probelisten_Testdaten` | 3.44.0 / Format 26, Bearbeitungstag 22.10.2026, bytegleich zur Fixture | über echten Import/Neustart abgeglichen |
| Eigenständige Pakete / Mac-Bundle | weiter 3.42.0; lesen Format 26 nur schreibgeschützt | Neubau, Mac-Vollprüfung und Signatur bleiben offen |

Verbindliche Quell-/Prüf-/Liefermatrix: [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Ältere Bestands-/Paketbelege bleiben ihren damaligen Bytes zugeordnet, etwa die [Bestandsaufnahme 21.10.](../01_Repository/Glide/tests/qa-3.43.1/standaufnahme_2026-10-21/README.md) und das [Dokumentations-Vorinventar 22.10.](../01_Repository/Glide/tests/qa-3.43.1/dokumentationsaudit_2026-10-22/README.md).

**Git-Aufträge:** Der einmalige Auftrag vom 21.10. bleibt nach roter Grundstufe ohne Commit/Push beendet ([Nachweis](../01_Repository/Glide/tests/qa-3.43.1/gitauftrag_2026-10-21/README.md)). Der ausdrückliche Auftrag vom 22.10. („… den finalen Stand auf Github pushen und mergen …“) ist davon getrennt und mit diesem Phasenabschluss ausgeführt; er gilt nicht als Dauerfreigabe für künftige Commits oder Releases.

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

Bestehende Quellen fortschreiben: ein Thema, ein Dokument. Der Phasenabschluss vom 22.10. hat aktive Versions-, Format-, Liefer-, Aufgaben- und Git-Statusaussagen in allen fortgeschriebenen Dokumenten auf 3.44.0 abgeglichen (Plan §16/§18/§19/§21, Funktionen, Datenvertrag, Architektur, Prüfplan, QA-Bericht, READMEs); historische Messergebnisse und Paketnachweise bleiben unverändert. Kein zweiter Plan oder neues Gesamtdokument.

Die globale Ablageprüfung vom 18.10. einschließlich Git und damaliger Arbeitskopien bleibt im [Ablagenachweis](../01_Repository/Glide/tests/qa-3.43.1/ablageaudit_2026-10-18/README.md). Der Phasenabschluss ersetzt diese physische Vollinventur nicht. Der uncommittete Kandidat wurde vor jeder Änderung unverändert als Commit `5e915a7` gesichert; andere lokale Zweige und vier Stashes blieben unangetastet. Mehrdeutige Dateien, alte Affinity-Quellen, andere Zweige und Stashes werden nicht aufgrund eines Ignore-Eintrags oder historischen Löschwunschs entfernt.

Der [UI-/UX-Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md), [Bildzuordnung](Featurepaket_UI_UX/BILDREFERENZEN.md) und 28 lokale Originalbilder bleiben Eingangsbelege. Bilder enthalten teilweise Kontoangaben, bleiben vom Git-Upload ausgeschlossen und müssen bei Rechner-/Agentenwechsel ausdrücklich mitgegeben werden. Aufgabenstatus nur im Plan §17/§21.

## 4. Nächste Arbeit und offene Entscheidungen

Reihenfolge und Begründung stehen in [Plan §21.10](Glide_Entwicklungsplan.md#2110-phasenabschluss-3440). Kurz:

1. **Lieferabschluss 3.44.0 vervollständigen:** Mac-Vollprüfung auf dem Referenz-Mac, `packaging/macos/baue_app.py` mit SHA-256-/Signaturprüfung, eigenständige Pakete 3.44.0 (Windows/Mac) und das Ergebnis der GitHub-Linux-/Windows-Matrix nach dem Merge lesen. Erst dann gilt die Phase nach AGENTS.md für den Inhaber als vollständig angekommen.
2. **Menschenabnahme** der gesammelten 3.44.0-Punkte nach der [Prüfliste](Glide_Manuelle_Pruefung.md), zuerst Format-26-Umstellung mit einer Kopie eines echten Bestands.
3. **Technische Folge:** übrige direkte Mutationscaller (WA-37/38) nach konkreter Fehlerwirkung, Leistungsarbeit an Refresh/Bestandsvergleich (WA-36), ein begrenzter Ansichtspilot WA-39/WA-32. Die alten Neubauvorschläge implementierter FP-Stufen nicht erneut ausgeben.

Offen beim Inhaber und nicht durch diesen Abschluss entschieden: E-U1–E-U3, E-P1–E-P5, Integrationsrichtung E-I1, WA-23/24, FP-07 Stufe 2 (Canvas). Paket 8 / 4.0.0 bleibt vorbereitet und pausiert. D53 erlaubt Neubewertungen, aktiviert keinen Anbieter; D52–D54 verlangen zentrale Roadmap, appweite Designgeltung und Pflege ohne automatische Feature-/Git-/Releaseentscheidung.

## 5. Arbeits- und Prüfregeln

- Deutsch, lokale Kernfunktionen, neue Fachlogik nach D17 Tk-frei; bestehende Mutationseinstiege und modale Dialogführung erhalten.
- Tests setzen vor dem Import einen temporären `GLIDE_DATA_DIR`; Windows-Ausgabe mit `PYTHONUTF8=1`. Keine echten Nutzerdaten oder privaten Fehlerprotokolle aus diesem Auftrag ableiten.
- Neue ausführbare Änderungen brauchen passende Prüfungen; alte Vollmatrix nur ihren eingefrorenen Bytes zuordnen. Vor einem konkret beauftragten Commit CI-Grundstufe; `--lieferstand-streng` erst beim gemeinsamen Lieferabschluss. Der beendete Git-Auftrag bleibt beendet.
- Phasenabschluss: Version und Quell-/Prüf-/Ressourcenstand einfrieren, Voll-/native Matrix prüfen, anschließend 07/Showcase/Pakete und SHA-256 abgleichen. Kein Abgleich auf einen laufenden ungeprüften Kandidaten. Nach einem Versionswechsel unter Windows Zeilenenden der `eol=lf`-Dateien kontrollieren (`git ls-files --eol`), weil `versionswechsel.py` mit Plattform-Zeilenenden schreibt.
- Originalreferenzen, aktuelle QA-Versionen/-Bilder, Migrationsfixtures, Showcase und vorhandene Lieferpakete nach den Pflege- und Aufbewahrungsregeln schützen; historische Nachweise nicht nachträglich grün schreiben.

## 6. Bewusste Grenzen

Der Phasenabschluss 3.44.0 ist eine automatische Windows-Abnahme mit Python-Lieferung (Linux/Tk 8.6 nur über die CI-Grundstufe), keine vollständige Produkt- oder Releaseabnahme. Native Mac-/Linux-/Readerabläufe, die unvollständige lokale Mac-Kopie, DPI/Mehrmonitor, physische Bedienung sowie Rechte-, Lizenz-, Signatur- und Veröffentlichungstore bleiben ausdrücklich offen. Neue Markt- oder Nutzungsbehauptungen werden aus der Zusammenführung nicht abgeleitet.
