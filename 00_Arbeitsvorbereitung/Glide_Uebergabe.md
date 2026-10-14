# Glide – Übergabe an eine neue Sitzung

Stand 14.10.2026 · Glide 3.42.0 · Aufgabenformat 25 · für den nächsten Chat oder Bearbeiter

Einstieg für jede Sitzung. Zusammengeführt am 03.10.2026 aus Sitzungsübergabe, Projektübergabe, Startkontext und dem Sitzungsprotokoll vom 24.–26.09.2026; die Vorfassungen trägt Git. Dieses Dokument sagt, wo was steht, was gilt und was als Nächstes ansteht – es ersetzt nicht die Fachdokumente.

## 1. In fünf Sätzen

- Glide ist eine lokale, deutschsprachige Aufgaben-, Notiz-, Seiten- und Pixel-App in Python 3.14 mit Tk 9: `src/glide/app.pyw` und 62 Begleitmodule; neue Fachlogik nach D17 Tk-frei.
- Aktuell lokal bereitgestellt ist **3.41.0** (Notion-Import und Seitenwiederherstellung, Paket 6, Apphash 4dedf0c5, Datenformat 25): eingefrorene Mac-Vollprüfung Exit 0, 106 ausgeführt/zwei übersprungen, 89 Suiten/638 Units. 215 Liefer-/123 Bundle-Dateien bytegleich, Bau- und Rückkopiesignaturen grün. Native Linux-/Windows-Matrix am Kandidaten `1bc2db1` vollständig grün (je 107/1, 18 Defektgegenproben); nach erneutem Hash-/Signaturabgleich automatisch geliefert. Menschen-/DPI-/Readerabnahme getrennt.
- Der Inhaber startet Glide **nur** aus `07_Python-Versionen` oder `01_Repository/Glide/build/macos/Glide.app`; eine Änderung ist erst bei ihm, wenn beide per SHA-256 abgeglichen sind.
- Beauftragt sind Performance-Fortsetzung und größere Feature-Pakete aus Analyse, Recherche und Konkurrenzdokumenten (05./07.10.2026). [Entwicklungsplan §4.4](Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026) legt die Paketfolge fest. Umfangreiche gezielte Prüfung und ein gemeinsamer eingefrorener Volllauf je Paket; keine erneute Freigabe je Teilfeature. Offene Produktentscheidungen bleiben dem Inhaber vorbehalten.
- Antworten, Dokumente und Oberfläche sind deutsch.

## 2. Wo was liegt

| Was | Wo |
|---|---|
| Arbeitsregeln und Abschlusskriterium | [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md), für Claude Code zusätzlich `CLAUDE.md` in der Wurzel |
| Aufgaben, Stufen, Ziele | [Entwicklungsplan](Glide_Entwicklungsplan.md) |
| Entscheidungen D01–D48, frühere Antworten, Leitgedanken des Inhabers | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Produktgrenzen, sechs Prinzipien, Prinzipien-Check | [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Code | `01_Repository/Glide/src/glide/` – Module siehe [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Datenformat, Backups, Austausch | [Daten und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfen | [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), Ergebnisse im QA-Bericht, Nachweise unter `tests/qa-<Version>/` |
| Startbare Fassung | Gelieferte 3.41.0 am Hash 4dedf0c5: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.41.0.pyw` mit `Schnellstart.pyw`; 63 Code-/146 Ressourcen-/sechs Showcase-Dateien bytegleich. Mac/Linux/Windows automatisch grün; Lieferabschluss belegt |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` trägt **3.41.0 / 4dedf0c5**; 63 Code-/60 Mac-Ressourcen gleich Quelle, Ad-hoc-Signatur im Bauordner und auf Rückkopie grün. Tatsächliche Menschenabnahme offen. Kennung `de.shaye.glide` (Windows `Shaye.Glide`) |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung, Abweichungen Dokumentation ↔ Code | [Analyse](Glide_Analyse.md) |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz, GitHub-Auftritt | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Regeln für Dokumente, Zuständigkeiten | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
| Git | Fortsetzung `codex/glide-fortsetzung-3410`, P7-Kandidat zuletzt `795f47b`. Der Inhaber hat PR #20 und #21 extern zusammengeführt; `main` zuletzt `c38b1d0`, in den Kandidaten ohne Inhaltsänderung übernommen. Die lokale OneDrive-Arbeitskopie bleibt bis zur fertigen Lieferung auf 3.41.0 (`3f752654`); kein Main-Push oder Merge durch diese Fortsetzung. `core.fileMode=false`. Windows-Worktrees mit `C:/…` nie vom Mac aus bereinigen; Stash vom 04.10.2026 und Sicherungszweig `codex/local-before-sync-…` gehören dem Inhaber. |
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
- **Abnahme einer Version** auf dem Mac: `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.42.0/<Name> --timeout 900` – 90 Integrationssuiten, Unit-Tests, Showcase, fünf Analysen.
- **Windows:** `tests\tools\windows_vollpruefung.cmd` (dieselbe Vollprüfung mit Python 3.14/Tk 9 und Fensterfotos); Anleitung und Rückmeldung in der [Prüfliste, B0](Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung).
- **Lieferweg je Version:** CHANGELOG → `versionswechsel.py` → 07-README (Lieferabsatz, Module) → Nachweisrahmen → Standprüfung → eingefrorene Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `archiv`, `build`) → `pruefen.py --modus voll` → in der Kopie `abgleich_07.py` und `showcase_abgleich.py` → 07 und 05 zurückspielen → `baue_app.py`, Signatur prüfen → Nachweise, QA-Bericht, Plan → CI-Grundstufe → Commit. Beim Vormerken die neue Hauptdatei ausführbar setzen (`git update-index --chmod=+x 07_Python-Versionen/Glide-Aufgaben-und-Listen_v<Version>.pyw`), weil die Arbeitskopie Dateimodi nicht übernimmt. Fällt mit dem Versionswechsel ein eingecheckter Nachweis aus der Aufbewahrung, die Verweise im QA-Bericht auf den festen Git-Stand umstellen (`https://github.com/n05a-design/glide-to-do/blob/<Commit>/…`); 3.33.17 ist bereits auf `6098877` fixiert; 3.33.18 ist auf `cbd8939` fixiert; für 3.38.0 sind auch die auslaufenden 3.33.19-Verweise auf `6098877` festgesetzt. Mit 3.42.0 fällt 3.36.0 aus der Aufbewahrung; ihre QA-Verweise sind auf Liefercommit `3f752654` festgesetzt. Beim nächsten Versionswechsel fällt 3.37.0 heraus.
- **Prüffallstricke:** Konsolenausgabe nie in den OneDrive-Ordner umleiten (Exit 120); keine UI-Suiten parallel zur Vollprüfung oder zu Messungen; erzeugte Mehrfachklicks brauchen Zeitstempel (`time=`), sonst zählt Tk sie als eine Folge; Dialogknöpfe zeigen „Speichern“ statt „Speichern …“ (`RoundedButton.action_text`).

## 6. Was als Nächstes ansteht

- **Aktueller Lieferstand 13.10.2026:** 3.41.0 (Paket 6) vollständig automatisch geliefert. Frische eingefrorene Mac-Vollprüfung 106/2, 89 Suiten/638 Units, 1.064 Dateien unverändert; [native Matrix 38441333442](https://github.com/n05a-design/glide-to-do/actions/runs/38441333442) am Kandidaten `1bc2db1` grün (Linux/Windows je 107/1, 18 Defektgegenproben). 215 Liefer-/123 Bundle-Dateien nach der Matrix erneut bytegleich, Bau-/Rückkopiesignaturen grün. Die drei nativen Vorbefunde sind korrigiert, rote Vorläufe bleiben im [Paketnachweis](../01_Repository/Glide/tests/qa-3.41.0/notion_wiederherstellung_2026-10-13/README.md). Menschenabnahme getrennt offen.
- **Bestätigte Fortsetzung:** Pakete 1–6 und FP-00 (3.39.1) geliefert; jetzt 3.42.0 eigenständige Pakete → 4.0.0 zugänglicher Aufgaben-Kernablauf → Folgepakete nach Entwicklungsplan §16.7 (D49). Der Inhaber hat diese Reihenfolge im aktuellen Chat ausdrücklich zur Fortsetzung bestätigt. Gewählte Optionen nicht erneut vorlegen; neue Produktentscheidungen ab D50, technische Routineentscheidungen dokumentieren. Keine öffentliche Releasefreigabe.
- **Aktiver Arbeitsstand:** `codex/glide-fortsetzung-3410`; private Prüf-/Vorbereitungskopien unter `~/.codex/workspaces/glide-fortsetzung-2026-10-13`, Fortsetzungsdaten in `state.json`. Die früheren Codex-Vorbereitungen unter `~/.codex/workspaces/glide-sprint-2026-10-09` und Claudes separate Arbeitsbereiche sind erhalten. Stash, Sicherungszweig, Windows-Worktrees und Nutzer-Skills unverändert lassen.
- **Paket 7 / 3.42.0 in Prüfung:** Mac-Paketbau und tatsächlicher isolierter Start grün (64 Codeobjekte, 53 native arm64-Dateien, 23 Lizenzkomponenten, 330 Dateien/29 Symlinks); zweite eingefrorene Mac-Vollprüfung 107/2, 90 Suiten/638 Units, 1.060 Dateien unverändert. Kandidaten-07/Showcase und Bundle bytegleich. Native Matrix 38475080827 bestand Grundstufe und Linux-/Windows-Vollprüfung (je 108/1, 18 passende Linux-Defektgegenproben); der anschließende Windows-Paketjob war rot. Versionsgenaue libmpdec-/zlib-ng-Lizenzbelege und PE-Anbieter sind nachgeführt; Windows-Bau inzwischen grün (64 Codeobjekte, 29 native x64-Dateien, 102 Dateien, 28 Lizenzkomponenten). Die tatsächliche ACL-Startprobe fand mehrere Fehler im Prüfer. Aktueller Nachlauf `795f47b`: FileIO-EACCES anerkennen, Dateiinhalt/Ausführung gezielt sperren, Root-Sperre vor Restaurierung lösen und jede Original-DACL nachher exakt vergleichen. 56 Paket-Werkzeugtests und strenge CI grün; native Wiederholung 38543868019 läuft. Frischer eingefrorener Mac-Prüfstand mit 1.071 Dateien vorbereitet. Apphash d6709820 unverändert; Root-07 und Root-Bundle bleiben bis Abschluss 3.41.0. Alle roten Vorläufe bleiben im Paketnachweis, kein erfolgreicher Windows-Start daraus abgeleitet.
- **Paket 8 / 4.0.0 vorbereitet:** In der privaten `paket8-kandidat` sind drei Tk-freie Semantikmodule mit 42 grünen Fällen und additive Anbindungen an die aktuelle 3.42.0-App vorhanden. Checkliste verwendet echte Checkboxen mit 0/1 und kanonischem Variablenrollback, deutsche Namen/Werte und aktuelle Aktionsziele; bestehende Mutationseinstiege bleiben. Eigener gepinnter Tcl/Tk-9.1-/CPython-Runtimebuilder für die drei nativen Prüfplattformen vorbereitet (vier reine Vertragstests); bisher nur frühere Mac-Tcl-Konsole belegt, neue GUI-/Bau-/Readerproben offen. Native Aqua-Getter-/Aktionsprobe, AT-SPI-Textverbraucher und NVDA-2026.2-SpeechSpy-Probe mit gepinnten Originalen und künstlicher App vorbereitet, noch nicht ausgeführt. Die Quellanalyse hat offene native Verträge bei Aqua-Aktionswarteschlange/schreibgeschützten Feldern sowie Linux-Text-/Selektionsplatzhaltern erkannt: zuerst nativ reproduzieren, dann gezielt in der eigenen Runtime korrigieren. Neue 24-Komponenten-Lizenzbasis einschließlich utf8proc vorbereitet, Mac-Tcl-Konsole/Lizenzgenerator grün; beide eigenen 4.0-Pakete, Gegenproben und tatsächliche Readerabnahme bleiben offen. Keine alte komplette Appdatei oder Einmal-Builder übernehmen; P8 vor Weiterarbeit auf den fertigen P7-Lieferstand bringen.
- **Ablage beim nächsten Versionswechsel:** 3.36.0 fällt aus den sieben neuesten Versionen. Aktive lokale QA-Verweise vorher auf einen festen aktuellen Git-Lieferstand umstellen; tatsächlichen Bestand einschließlich ausgeschlossener alter Logs/Fensterbilder prüfen. Git trägt frühere Fassungen.
- **Menschenabnahme:** Manuelle Windows-/Linux-Sichtfälle W01/W06–W09, DPI/Mehrmonitor, echte Tastatur/Maus/Trackpad und Reader nach der [Prüfliste](Glide_Manuelle_Pruefung.md) getrennt offen. Native Windows-Vollprüfungen bis 3.41.0 einschließlich 3.39.1 grün; kein menschliches Testergebnis daraus ableiten. Reale zusätzliche Reader-Prüfplätze am 13.10.2026 beantwortet: „Keiner der beiden Prüfplätze“. Außer Mac/VoiceOver stehen dem Inhaber somit keine Windows-/NVDA- oder Linux-/Orca-Prüfplätze zur Verfügung. Automatisierte native Prüfungen weiterführen; die tatsächlichen Reader-/Menschenabnahmen bleiben eigene offene Tore, kein Verzicht daraus ableiten.
- **Veröffentlichungstore:** I1–I5/I9–I11 bleiben nach D43 gesondert offen (Inhaberangaben, Glide-Lizenz, öffentliche Signaturen/Konten, Marke, Systeminstallation, Fremdbildrechte, Historienumschreibung, GitHub-Auftritt). Keine Käufe, Historienumschreibung oder stillen Bildlöschungen aus der Fortsetzung ableiten.
