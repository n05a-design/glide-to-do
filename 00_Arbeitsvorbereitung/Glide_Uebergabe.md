# Glide – Übergabe an eine neue Sitzung

Stand 10.10.2026 · Glide 3.35.0 · Aufgabenformat 23 · für den nächsten Chat oder Bearbeiter

Einstieg für jede Sitzung. Zusammengeführt am 03.10.2026 aus Sitzungsübergabe, Projektübergabe, Startkontext und dem Sitzungsprotokoll vom 24.–26.09.2026; die Vorfassungen trägt Git. Dieses Dokument sagt, wo was steht, was gilt und was als Nächstes ansteht – es ersetzt nicht die Fachdokumente.

## 1. In fünf Sätzen

- Glide ist eine lokale, deutschsprachige Aufgaben-, Notiz-, Seiten- und Pixel-App in Python 3.14 mit Tk 9: `src/glide/app.pyw` und 35 Begleitmodule; neue Fachlogik nach D17 Tk-frei.
- Aktueller Stand ist **3.35.0** (Sprint vom 08./09.10.2026 abgeschlossen): Tempo (3.33.19), Komfort (3.33.20), ruhige Oberfläche (3.33.21), Wissen und Seiten (3.34.0), Pixel und Austausch (3.35.0). Jede Version mit Pflichtsuite und Gegenprobe, eingefrorenem Mac-Volllauf (3.35.0: Exit 0, 99 ausgeführt, 82 Integrationssuiten, 257 Unit-Tests) sowie bytegleicher Lieferung in 07, Showcase und Bundle. Windows-Vollprüfung zuletzt 3.33.18; Windows-Nachprüfung, Linux-Sichtprüfung und menschliche Abnahme offen. [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).
- Der Inhaber startet Glide **nur** aus `07_Python-Versionen` oder `01_Repository/Glide/build/macos/Glide.app`; eine Änderung ist erst bei ihm, wenn beide per SHA-256 abgeglichen sind.
- Beauftragt sind Performance-Fortsetzung und größere Feature-Pakete aus Analyse, Recherche und Konkurrenzdokumenten (05./07.10.2026). [Entwicklungsplan §4.4](Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026) legt die Paketfolge fest. Umfangreiche gezielte Prüfung und ein gemeinsamer eingefrorener Volllauf je Paket; keine erneute Freigabe je Teilfeature. Offene Produktentscheidungen bleiben dem Inhaber vorbehalten.
- Antworten, Dokumente und Oberfläche sind deutsch.

## 2. Wo was liegt

| Was | Wo |
|---|---|
| Arbeitsregeln und Abschlusskriterium | [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md), für Claude Code zusätzlich `CLAUDE.md` in der Wurzel |
| Aufgaben, Stufen, Ziele | [Entwicklungsplan](Glide_Entwicklungsplan.md) |
| Entscheidungen D01–D29, frühere Antworten, Leitgedanken des Inhabers | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Produktgrenzen, sechs Prinzipien, Prinzipien-Check | [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Code | `01_Repository/Glide/src/glide/` – Module siehe [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Datenformat, Backups, Austausch | [Daten und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfen | [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), Ergebnisse im QA-Bericht, Nachweise unter `tests/qa-<Version>/` |
| Startbare Fassung | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.35.0.pyw` mit `Schnellstart.pyw`; 37 Code-Dateien, 131 Ressourcen und Showcase SHA-256-abgeglichen |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` (lokal, nicht versioniert) trägt **3.35.0**, Ad-hoc-Signatur, SHA-256-gleich zu 07; menschliche Abnahme offen. Kennung `de.shaye.glide` (Windows `Shaye.Glide`) |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung, Abweichungen Dokumentation ↔ Code | [Analyse](Glide_Analyse.md) |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz, GitHub-Auftritt | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Regeln für Dokumente, Zuständigkeiten | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
| Git | Standardzweig `main` (3.35.0 über Pull Request #16, 09.10.2026); neue Arbeit auf einem eigenen Zweig `claude/<Thema>` und per Pull Request. Die Arbeitskopie liegt in OneDrive und hat `core.fileMode=false`. Die als „prunable“ gelisteten Worktrees gehören zur Windows-Arbeitskopie (`C:/…`) – nie vom Mac aus `git worktree prune`. Stash vom 04.10.2026 und Zweig `codex/local-before-sync-…` gehören dem Inhaber |
| Fehlerprotokoll des Inhabers | `~/Library/Application Support/Glide/fehlerprotokoll.txt` – nur mit Erlaubnis lesen, nur Fehlereinträge |

## 3. Regeln, die immer gelten

- **Echte Daten nur als Kopie und nur mit Erlaubnis.** Tests und Messungen immer mit temporärem `GLIDE_DATA_DIR`, vor dem Import gesetzt. Originale nie verändern; nur Zahlen berichten.
- **Fotos nur vom eigenen Glide-Fenster** (macOS `screencapture -l <Fensternummer>`, Windows `PrintWindow`), nie vom Bildschirm.
- **Plattformunabhängig:** keine Funktion nur für eine Plattform, keine neue Laufzeitabhängigkeit ohne Entscheidung.
- **Form folgt Funktion und die sechs Produktprinzipien** ([Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)); Farben nur über `BUTTON_ROLE_RULES`.
- **Jede Produktionsrunde bekommt eine Version** (`scripts/pflege/versionswechsel.py`). Reine Dokumentations-, Ablage- oder Werkzeugnachläufe bekommen einen datierten Nachweis zur unveränderten App-Version.
- **Ablage:** Das öffentliche Repository `n05a-design/glide-to-do` ist maßgeblich (D09). Uploads nur in die Projektstruktur, keine Benutzerpfade, keine Rohprotokolle, keine Archivkopien. Archive und Nachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten ([Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md)).
- **Dokumente:** ein Thema, ein Dokument; zusammenführen und löschen statt archivieren; Erledigtes im Entwicklungsplan markieren.

## 4. Lehren aus den bisherigen Runden

- **Rückwärtsverhalten messen, nicht annehmen:** 3.29 überschreibt einen Format-20-Bestand bei der ersten Eingabe. Vor jedem Formatwechsel die Vorgängerversion mit einer Kopie echter Daten prüfen; der Schutz vor unbekannten Formaten muss eine Version vorher im Code sein (seit 3.30 vorhanden).
- **Erst nach dem Abgleich erledigt:** Am 29.09.2026 prüfte der Inhaber einen alten Stand, weil 07 und Bundle nicht nachgezogen waren.
- **Vollprüfung ohne Last und ohne Eingaben** – Einzelheiten im [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md#regeln).
- **Optionen mit Empfehlung vorlegen:** nummerierte Fragen mit Optionen, Vor- und Nachteilen, je einer Empfehlung und der Wahl „erste Stufe oder vollständig“ machen Rückfragen kurz und erlauben eine Kurzantwort (etwa „D09 B, D10 A“); Lizenzfragen gleich mit Quelle und Lizenz vorlegen.
- **Inhaberentscheidungen früh abfragen:** Kennungen, Logo und Signatur blockieren Paketierung und Mitteilungen.
- **Planung nach jeder Etappe inhaltlich abgleichen**, nicht nur Statusspalten. Bekannte Grenzen sind die nächste Aufgabenliste.
- **Jede neue Oberfläche** bei 860 × 700 und großer Schrift prüfen; Farben als Rollen planen, damit die Kontrastprüfung greift.
- **Aktionskennungen seit 3.33.11:** Menü und Palette verwenden stabile IDs; Beschriftungen können sich ändern. Bei Ausführung die aktuelle Menüposition ermitteln, Copy/Paste/Undo mit Editorfokus prüfen (R2).
- **Rückfallwege und Prüfwerkzeuge sichtbar prüfen:** Der Tk-8.6-Rückfall des Logos war grün getestet und unter Windows doch treppig. Die Windows-Dunkelaufnahme war byte-gleich mit der hellen. Ein Qualitätskriterium bzw. ein einfacher Vergleich hätte beides sofort gezeigt.
- **Windows-Arbeitskopie in OneDrive:**
  - Die Arbeitskopie hat CRLF; seit 08.10.2026 legt die Wurzel-`.gitattributes` die Zeilenenden für die ganze Ablage fest (W03).
  - Windows zeigt Dateinamen teils kleingeschrieben (`glide-showcase.glidebackup`); maßgeblich ist die Schreibweise in Git.
  - OneDrive legt Konfliktkopien `<Name>-<Gerätename>.md` an, und eine dort liegende Arbeitskopie kann veraltete Fassungen behalten. Mit 3.33.8 gelangten so sechs Kopien und die am 03.10.2026 aufgelöste Projektübergabe ins Repository, vier Hauptdokumente waren dabei gekürzt. Am 05.10.2026 zusammengeführt. Vor jedem Commit neu hinzugefügte Dateien und stark geschrumpfte Dokumente prüfen (W04).
  - In PowerShell heißt der Benutzerordner `$env:USERPROFILE`, nicht `%USERPROFILE%`.
- **Sofort nach jeder Lieferung committen:** Die Nachweise 3.33.13–3.33.16 waren nie eingecheckt und sind mit der Aufbewahrung verschwunden; nur ihre Werte im QA-Bericht blieben.
- **Git und Signatur im OneDrive-Ordner:** OneDrive kann Git-Objekte leeren (09.10.2026: ein leerer Baum in einem lokalen Codex-Checkpoint) und lässt `codesign --verify` direkt im Ordner scheitern; die Signatur deshalb im Bauordner und auf einer Rückkopie prüfen. Eine leere, verwaiste `.git/index.lock` ohne laufenden Git-Prozess hält `ablage_kuerzen.py` an.
- Technische Fallstricke (Menübefehle unter macOS, `update()` in Rückrufen, Tk 9 und `place`, Bindtags, Leinwand ohne Kantenglättung, Design statt `theme_name`): [Architektur, Abschnitt 5](../01_Repository/Glide/docs/02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt).

## 5. Prüfen

- **Windows-Konsole:** Vor Prüfbefehlen in PowerShell `$env:PYTHONUTF8="1"` setzen; sonst kann die Ausgabe einer Fehlermeldung mit Checkbox-Zeichen unter cp1252 abbrechen, bevor das Gesamtprotokoll geschrieben wird.
- **Vor jedem Commit:** `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` aus `01_Repository/Glide` (braucht Python mit tkinter, unter Linux Xvfb). Im Linux-Container möglich: CI-Grundstufe, Startprobe, `messung_speicherweg.py`; nicht möglich: macOS/Tk-9-Abnahme, Bundlebau, physische Bedienung. Ergebnisse als „Linux/Tk 8.6, künstliche Daten“ kennzeichnen.
- **Abnahme einer Version** auf dem Mac: `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.35.0/<Name> --timeout 900` – 82 Integrationssuiten, Unit-Tests, Showcase, fünf Analysen.
- **Windows:** `tests\tools\windows_vollpruefung.cmd` (dieselbe Vollprüfung mit Python 3.14/Tk 9 und Fensterfotos); Anleitung und Rückmeldung in der [Prüfliste, B0](Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung).
- **Lieferweg je Version:** CHANGELOG → `versionswechsel.py` → 07-README (Lieferabsatz, Module) → Nachweisrahmen → Standprüfung → eingefrorene Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `archiv`, `build`) → `pruefen.py --modus voll` → in der Kopie `abgleich_07.py` und `showcase_abgleich.py` → 07 und 05 zurückspielen → `baue_app.py`, Signatur prüfen → Nachweise, QA-Bericht, Plan → CI-Grundstufe → Commit. Beim Vormerken die neue Hauptdatei ausführbar setzen (`git update-index --chmod=+x 07_Python-Versionen/Glide-Aufgaben-und-Listen_v<Version>.pyw`), weil die Arbeitskopie Dateimodi nicht übernimmt. Fällt mit dem Versionswechsel ein eingecheckter Nachweis aus der Aufbewahrung, die Verweise im QA-Bericht auf den festen Git-Stand umstellen (`https://github.com/n05a-design/glide-to-do/blob/<Commit>/…`); beim nächsten Wechsel betrifft das 3.33.17 (Commit `6098877`).
- **Prüffallstricke:** Konsolenausgabe nie in den OneDrive-Ordner umleiten (Exit 120); keine UI-Suiten parallel zur Vollprüfung oder zu Messungen; erzeugte Mehrfachklicks brauchen Zeitstempel (`time=`), sonst zählt Tk sie als eine Folge; Dialogknöpfe zeigen „Speichern“ statt „Speichern …“ (`RoundedButton.action_text`).

## 6. Was als Nächstes ansteht

- **Neuer Sprint, Phase 1 seit 09.10.2026, fortgesetzt 10.10.2026:** Einstieg vollständig gelesen; `main` war sauber und enthielt PR #16 (`b5f5c22`). Planung auf `claude/glide-sprint-2026-10-09`, App und Lieferung bleiben 3.35.0. [Entwicklungsplan §15](Glide_Entwicklungsplan.md#15-neuer-feature-sprint-ab-09102026-gemeinsame-planung): Runden 1–3 entschieden (D18–D29), Wortlaute in der Arbeitsrichtung. Animation A/V; Referenzweg B/V, Bild 1; OB02/OB03/N05/KO04 vollständig; Tageshinweise A/V; Notion A/V; PyInstaller 6.22.3 für Mac/Windows A/V; Logo B+C+D+F; gesamte ICONS-Tabelle mit Systemzeichen. Ausgewähltes Bild im Grafik-Master gesichert. Weitere Funktionen bleiben zur gemeinsamen Auswahl, neue Entscheidungen ab D30. Erst das ausdrückliche „ja“ zum fertigen Paketplan erlaubt Produktionsänderungen. Nach jeder Antwort Entscheidungsregister und Aufgaben sofort nachführen.
- **Weitere Entscheidungen des Inhabers:** Runde 4 zu E-S8a ICS, E-S8b Bewegung, Bedienfläche, P03-Rest, E01-Rest und Linux-Matrix gestellt, Antwort offen. Danach Screenreader/Tk 9.1, Seitenwiederherstellung, neue Vorschläge V01/V02, P05, Logo-Master und externe Abnahmetore/I1–I11. E-S1–E-S7 entschieden, ausgenommen Logo-Master LG04; ihre Umsetzung steht aus. Stash, `codex/`-Zweig und Windows-Worktrees unangetastet.
- **Sprint abgeschlossen** (3.33.19–3.35.0, eingecheckt am 09.10.2026): Abgleich, Abweichungen und Offenes in [Entwicklungsplan §14.2](Glide_Entwicklungsplan.md#142-abschlussabgleich-abs-09102026); Ergebnisse je Version im QA-Bericht.
- **Planungsprüfung 10.10.2026:** [Nachweis](../01_Repository/Glide/tests/qa-3.35.0/planung_2026-10-10/README.md). Strenge CI auf isolierter Projektkopie grün, App/07/Showcase und Bundle unverändert. Im Arbeitsordner schlägt nur die Standprüfung der externen unversionierten `Apple Design Skill.md` fehl (keine Glide-Standzeile); Datei unverändert belassen. Der rote Vorlauf ist erhalten. Künftige Prüfungen müssen diesen Unterschied ausdrücklich ausweisen, bis die externe Datei außerhalb der Projektablage liegt.
- **Prüfungen außerhalb des Macs:** Windows-Vollprüfung des Stands 3.35.0 (deckt W02 und die Lieferungen ab 3.33.19), Windows-Sichtprüfung W01/W06–W08 (B1a), Linux-Sichtprüfung der JPEG-Vorschau (N08), menschliche Abnahme I6 ([Prüfliste](Glide_Manuelle_Pruefung.md)).
- **Ohne Entscheidung möglich, aber nicht beauftragt:** Bedienfläche nach U09/OB05 neu messen (Ziel ≤ 15 %), P03-Rest, Linux-Kalibrierung der Integrationssuiten; Stufe 5 nur auf ausdrücklichen Auftrag.

## 7. Offen beim Inhaber

Vollständige Liste mit Stand und Empfehlungen: [Entwicklungsplan §11](Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber).

- **Entscheidungen:** E-S8 (AU07/OB04), Logo-Master LG04, Qualitäts-/Zukunftskandidaten und weitere Bearbeitungstiefe A–H, soweit nicht bereits D18–D29 abdecken. E-S1–E-S7 sind entschieden; ihre Umsetzung steht aus.
- **Freigaben und Konten:** I1 Inhaberangaben, I2 Lizenz, I3 Developer-ID und Code-Signing-Zertifikat, I4 Markenprüfung, I5 aktuelles Python auf dem Mac (3.14.5 trägt die Volläufe), I9 Rechte an Fremdbildern, I10 Git-Historie, I11 GitHub-Auftritt.
- **Prüfungen:** I6 Windows-Vollprüfung des aktuellen Stands und menschliche Prüfsitzungen nach der [Prüfliste](Glide_Manuelle_Pruefung.md).
