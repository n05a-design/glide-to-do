# Glide – Übergabe an eine neue Sitzung

Stand 14.10.2026 · Glide 3.42.0 · Aufgabenformat 25 · für den nächsten Chat oder Bearbeiter

Einstieg für jede Sitzung. Zusammengeführt am 03.10.2026 aus Sitzungsübergabe, Projektübergabe, Startkontext und dem Sitzungsprotokoll vom 24.–26.09.2026; die Vorfassungen trägt Git. Dieses Dokument sagt, wo was steht, was gilt und was als Nächstes ansteht – es ersetzt nicht die Fachdokumente.

## 1. In fünf Sätzen

- Glide ist eine lokale, deutschsprachige Aufgaben-, Notiz-, Seiten- und Pixel-App in Python 3.14 mit Tk 9: `src/glide/app.pyw` und 62 Begleitmodule; neue Fachlogik nach D17 Tk-frei.
- Aktuell lokal bereitgestellt ist **3.42.0** (eigenständige Entwicklungspakete, Paket 7, Apphash d6709820, Datenformat 25): Mac-Vollprüfung 107/2, 90 Suiten/638 Units, 1.083 Dateien unverändert. Native Linux-/Windows-Vollmatrix je 108/1 am identischen Appbaum und 18 Defektgegenproben grün; beide tatsächlichen isolierten Paketstarts grün. 215 Liefer-/330 Mac-Paketdateien plus 29 Symlinks bytegleich, Rückkopiesignatur und tatsächlicher Root-Start grün; Windows-Paket mit 102 Dateihashes bereitgestellt. Menschen-/DPI-/Readerabnahme getrennt.
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
| Startbare Fassung | Gelieferte 3.42.0 / d6709820: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.42.0.pyw` und `Schnellstart.pyw`; 63 Code-/146 Ressourcen-/sechs Showcase-Dateien bytegleich. Python-Startweg bleibt verfügbar; eigenständige Pakete brauchen kein externes Python |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` trägt **3.42.0 / d6709820**, eigenes Python/Tcl-Tk; 330 Dateien/29 Symlinks gleich Bau3, Ad-hoc-Signatur auf Rückkopie und isolierter Root-Start grün. Windows-Paket: `01_Repository/Glide/build/windows/Glide-3.42.0/Glide.exe`, 102 Dateihashes geprüft, unsigniertes Entwicklungsartefakt. Menschenabnahme offen |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung, Abweichungen Dokumentation ↔ Code | [Analyse](Glide_Analyse.md) |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz, GitHub-Auftritt | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Regeln für Dokumente, Zuständigkeiten | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
| Git | Fortsetzung `codex/glide-fortsetzung-3410`, P7-Lieferabschluss `05483a8` gesichert und gepusht, P8 privat auf `codex/glide-zugang-400` in Vorbereitung. Der Inhaber hat PR #20/#21 extern zusammengeführt; `main` zuletzt `c38b1d0`, im Kandidaten enthalten. Kein Main-Push oder Merge durch diese Fortsetzung. `core.fileMode=false`; ursprüngliche Nutzer-Skills, Stash, Sicherungszweig und Windows-Worktrees unverändert lassen |
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

- **Aktueller Lieferstand 14.10.2026:** 3.42.0 (Paket 7) automatisch geliefert; [Lieferabschluss](../01_Repository/Glide/tests/qa-3.42.0/eigenstaendige_pakete_2026-10-13/lieferabschluss.json). Mac 107/2, 1.083 eingefrorene Dateien unverändert; native Linux-/Windows-Vollsuiten je 108/1 am identischen Appbaum, 18 Defektgegenproben, Windows-Paketabschluss 38547672592 grün. Beide realen Startwege im Root aktualisiert und per Hash/Signatur/isoliertem Root-Start geprüft. Menschenabnahme bleibt getrennt offen.
- **Bestätigte Fortsetzung:** Pakete 1–7 und FP-00 (3.39.1) geliefert; jetzt 4.0.0 zugänglicher Aufgaben-Kernablauf → Folgepakete nach Entwicklungsplan §16.7 (D49). Der Inhaber hat die Reihenfolge bestätigt. Gewählte Optionen nicht erneut vorlegen; neue Produktentscheidungen ab D50, technische Routineentscheidungen dokumentieren. Keine öffentliche Releasefreigabe.
- **Aktiver Arbeitsstand:** `codex/glide-fortsetzung-3410`; private Prüf-/Vorbereitungskopien unter `~/.codex/workspaces/glide-fortsetzung-2026-10-13`, Fortsetzungsdaten in `state.json`. Die früheren Codex-Vorbereitungen unter `~/.codex/workspaces/glide-sprint-2026-10-09` und Claudes separate Arbeitsbereiche sind erhalten. Stash, Sicherungszweig, Windows-Worktrees und Nutzer-Skills unverändert lassen.
- **Paket 7 / 3.42.0 abgeschlossen:** Mac-Bau3 und Windows-Paketlauf 38547672592 grün, 65 Paket-Werkzeugtests. App-/Ressourcenbaum seit der erfolgreichen nativen Vollmatrix unverändert; aktueller Prüfbootstrap zusätzlich nativ belegt. Alle roten Lizenz-/PE-/Startprüfer-Vorläufe bleiben im Paketnachweis. Windows-ACL-Sperren ausschließlich im vergänglichen Hosted-CI, niemals an Inhaberinstallationen; ursprüngliche Zugriffsregeln geprüft, AI-Rohmarkerdifferenz ausdrücklich dokumentiert. Root-07, Mac-Bundle und Windows-Paket geliefert; ab jetzt P8 auf diesen Lieferstand bringen.
- **Paket 8 / 4.0.0 aktiv:** Private `paket8-kandidat` auf P7-Liefercommit `05483a8`, 50 Tk-freie Semantiktests und neun Runtime-/Patchverträge grün. Eigener gepinnter Mac-Tcl/Tk-9.1-Bau mit bestätigten Aqua-Korrekturen: zwölf native Getter-/Aktionsfälle grün, Original mit neun passenden Fehlern rot. Acht echte Glide-GUI-Prüfgruppen, bestehende Inspektorsuite und Tk-9.0-Rückfall grün; Undo-Haken und stabile Schritt-ID-Guards ergänzt, schreibgeschützte Auswahlfelder auch während offener Popups geschützt. [Vorprüfnachweise](../01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md). Erste native Linux-/Windows-Bauten am `154ccaf` vor GUI/Reader rot (HarfBuzz, Exportkennung); Nachlauf und native Wiederholung offen; Linux-Textplatzhalter zuerst nativ reproduzieren. Tatsächliche VoiceOver-/NVDA-/Orca-Ausgabe, eigene 4.0-Pakete und eingefrorene Vollmatrix bleiben offen. App-Version im privaten Zwischenstand weiterhin 3.42.0, keine 4.0-Lieferung. Root-07 und Bundle tragen unverändert die fertig gelieferte 3.42.0.
- **Ablage:** 3.42.0 hält Nachweise/Archive nur für die sieben neuesten Versionen und Fensterbilder nur für die drei neuesten. 565 ausgeschlossene alte QA-Dateien zusätzlich physisch entfernt; Git trägt frühere Nachweise. Mit 4.0.0 fällt 3.37.0 heraus: aktive Verweise vorher auf einen festen Git-Lieferstand umstellen und tatsächliche ausgeschlossene Logs/Fensterbilder erneut prüfen.
- **Menschenabnahme:** Manuelle Windows-/Linux-Sichtfälle W01/W06–W09, DPI/Mehrmonitor, echte Tastatur/Maus/Trackpad und Reader nach der [Prüfliste](Glide_Manuelle_Pruefung.md) getrennt offen. Native Windows-Vollprüfungen bis 3.41.0 einschließlich 3.39.1 grün; kein menschliches Testergebnis daraus ableiten. Reale zusätzliche Reader-Prüfplätze am 13.10.2026 beantwortet: „Keiner der beiden Prüfplätze“. Außer Mac/VoiceOver stehen dem Inhaber somit keine Windows-/NVDA- oder Linux-/Orca-Prüfplätze zur Verfügung. Automatisierte native Prüfungen weiterführen; die tatsächlichen Reader-/Menschenabnahmen bleiben eigene offene Tore, kein Verzicht daraus ableiten.
- **Veröffentlichungstore:** I1–I5/I9–I11 bleiben nach D43 gesondert offen (Inhaberangaben, Glide-Lizenz, öffentliche Signaturen/Konten, Marke, Systeminstallation, Fremdbildrechte, Historienumschreibung, GitHub-Auftritt). Keine Käufe, Historienumschreibung oder stillen Bildlöschungen aus der Fortsetzung ableiten.
