# Glide – Übergabe an eine neue Sitzung

Stand 16.10.2026 · Glide 3.43.0 · Aufgabenformat 25 · für den nächsten Chat oder Bearbeiter

Einstieg für jede Sitzung. Zusammengeführt am 03.10.2026 aus Sitzungsübergabe, Projektübergabe, Startkontext und dem Sitzungsprotokoll vom 24.–26.09.2026; die Vorfassungen trägt Git. Dieses Dokument sagt, wo was steht, was gilt und was als Nächstes ansteht – es ersetzt nicht die Fachdokumente.

**UI-/UX-Feature-Paket 15.10.2026 – als 3.43.0 geliefert (D50):** [Ausführungsprompt](Featurepaket_UI_UX/PROMPT.md) mit [Originalauftrag](Featurepaket_UI_UX/AUFTRAG.md), [28 Bildreferenzen](Featurepaket_UI_UX/BILDREFERENZEN.md) und [Design Richtlinien](../01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md). B01–B20 umgesetzt und automatisch geprüft; A01–A03 untersucht, die Auswahl E-U1–E-U4 liegt beim Inhaber ([Entwicklungsplan §17](Glide_Entwicklungsplan.md#17-ui-ux-feature-paket-aus-nutzerbeobachtungen-15102026)). Die Originalbilder sind lokal vom Git-Upload ausgeschlossen; bei Wechsel zu einem anderen Dienst das Paket einschließlich `bilder/` mitgeben.

**Vorabprüfung 15.10.2026:** [Bestands- und Dokumentationsprüfung](../01_Repository/Glide/tests/qa-3.42.0/bestandspruefung_2026-10-15/README.md) erfasst alle Projektbereiche einschließlich ignorierter Dateien, Vorlagen und Pakete. Veraltete aktive Aussagen korrigiert, fünf Rest-/Dubletten-Dateien entfernt. Drei binäre Löschkandidaten bleiben durch lokale Richtlinie blockiert. Der lokale 3.42.0-Quell-/07-Stand bleibt unverändert; GitHub führt bereits eine neuere, noch nicht gelieferte 4.0-Vorbereitung. Historische native Mac-Liefernachweise sind keine Aussage über die heutige unvollständige Windows-Kopie des Mac-Bundles.

## 1. In fünf Sätzen

- Glide ist eine lokale, deutschsprachige Aufgaben-, Notiz-, Seiten- und Pixel-App in Python 3.14 mit Tk 9: `src/glide/app.pyw` und 66 Begleitmodule; neue Fachlogik nach D17 Tk-frei.
- Aktuell lokal bereitgestellt ist **3.43.0** (UI-/UX-Paket, D50, Apphash 2feea1ee, Datenformat 25): eingefrorene Windows-Vollprüfung 101 Schritte grün einschließlich aller 92 Suiten und 711 Units; Pflichtsuite `test_uiux_paket` 16/16, rote Gegenprobe gegen 3.42.0 16/16. `07_Python-Versionen` (67 Code-/146 Ressourcendateien) und Showcase bytegleich. Native Linux-/Windows-Matrix laut [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). **Noch offen:** Mac-Vollprüfung, Mac-Bundle und eigenständige Pakete 3.43.0 (bis dahin 3.42.0), Menschenabnahme.
- Der Inhaber startet Glide **nur** aus `07_Python-Versionen` oder `01_Repository/Glide/build/macos/Glide.app`; eine Änderung ist erst bei ihm, wenn beide per SHA-256 abgeglichen sind.
- Beauftragt sind Performance-Fortsetzung und größere Feature-Pakete aus Analyse, Recherche und Konkurrenzdokumenten (05./07.10.2026). [Entwicklungsplan §4.4](Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026) legt die Paketfolge fest. Umfangreiche gezielte Prüfung und ein gemeinsamer eingefrorener Volllauf je Paket; keine erneute Freigabe je Teilfeature. Offene Produktentscheidungen bleiben dem Inhaber vorbehalten.
- Antworten, Dokumente und Oberfläche sind deutsch.

## 2. Wo was liegt

| Was | Wo |
|---|---|
| Arbeitsregeln und Abschlusskriterium | [`01_Repository/Glide/AGENTS.md`](../01_Repository/Glide/AGENTS.md), für Claude Code zusätzlich `CLAUDE.md` in der Wurzel |
| Aufgaben, Stufen, Ziele | [Entwicklungsplan](Glide_Entwicklungsplan.md) |
| Entscheidungen D01–D49 (D49 mit Korrekturvorbehalt), frühere Antworten, Leitgedanken | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Produktgrenzen, sechs Prinzipien, Prinzipien-Check | [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Code | `01_Repository/Glide/src/glide/` – Module siehe [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Datenformat, Backups, Austausch | [Daten und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfen | [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), Ergebnisse im QA-Bericht, Nachweise unter `tests/qa-<Version>/` |
| Startbare Fassung | Gelieferte 3.43.0 / 2feea1ee: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.43.0.pyw` und `Schnellstart.pyw`; 67 Code-/146 Ressourcen-/sechs Showcase-Dateien bytegleich. Eigenständige Pakete (Mac-Bundle, `build/windows/Glide-3.42.0`) tragen noch 3.42.0 |
| macOS-Bundle | Historischer 3.42.0-Liefernachweis: 330 Dateien/29 Symlinks und native Signatur/Start grün. Heutige Windows-Arbeitskopie: 327/330 Manifestdateien vorhanden und hashgleich; drei Python.framework-Dateien fehlen, keine aktuelle Mac-Paketfreigabe. Windows-Paket `build/windows/Glide-3.42.0/Glide.exe`: 102/102 Hashes korrekt, unsigniertes Entwicklungsartefakt |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung, Abweichungen Dokumentation ↔ Code | [Analyse](Glide_Analyse.md) |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz, GitHub-Auftritt | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Regeln für Dokumente, Zuständigkeiten | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
| Git | 16.10.2026: Arbeitszweig `claude/ui-ux-paket` ab `origin/main` `27bac83` (enthält P8-Vorbereitung bis PR #26) mit Kandidat `2e7d890` und Lieferung 3.43.0; Pull Request auf `main` als Merge-Commit. Frühere gelieferte Basis `05483a8` (3.42.0) auf `codex/glide-fortsetzung-3410`. Keine alten Komplettdateien zurückkopieren. `core.fileMode=false`; Nutzer-Skills, Stash, Sicherungszweig und separate Worktrees erhalten |
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
- **Abnahme einer Version** auf dem Mac: `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.43.0/<Name> --timeout 900` – aktuell 92 Integrationssuiten, Unit-Tests, Showcase, fünf Analysen. Für die private 4.0-Vorbereitung eigene Tk-9.1-Erweiterung über `PYTHONPATH` und `--zugang-nativ`; ab Version 4 native Kernprüfung immer Pflicht. Gelieferte 3.43.0 mit dem damaligen Prüfstand aus 90 Suiten abgenommen.
- **Windows:** `tests\tools\windows_vollpruefung.cmd` (dieselbe Vollprüfung mit Python 3.14/Tk 9 und Fensterfotos); Anleitung und Rückmeldung in der [Prüfliste, B0](Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung).
- **Lieferweg je Version:** CHANGELOG → `versionswechsel.py` → 07-README (Lieferabsatz, Module) → Nachweisrahmen → Standprüfung → eingefrorene Kopie außerhalb von OneDrive (ohne `.git`, `.claude`, `archiv`, `build`) → `pruefen.py --modus voll` → in der Kopie `abgleich_07.py` und `showcase_abgleich.py` → 07 und 05 zurückspielen → `baue_app.py`, Signatur prüfen → Nachweise, QA-Bericht, Plan → CI-Grundstufe → Commit. Beim Vormerken die neue Hauptdatei ausführbar setzen (`git update-index --chmod=+x 07_Python-Versionen/Glide-Aufgaben-und-Listen_v<Version>.pyw`), weil die Arbeitskopie Dateimodi nicht übernimmt. Fällt mit dem Versionswechsel ein eingecheckter Nachweis aus der Aufbewahrung, die Verweise im QA-Bericht auf den festen Git-Stand umstellen (`https://github.com/n05a-design/glide-to-do/blob/<Commit>/…`); 3.33.17 ist bereits auf `6098877` fixiert; 3.33.18 ist auf `cbd8939` fixiert; für 3.38.0 sind auch die auslaufenden 3.33.19-Verweise auf `6098877` festgesetzt. Mit 3.42.0 fiel 3.36.0 aus der Aufbewahrung (Verweise auf `3f752654`), mit 3.43.0 fiel 3.37.0 heraus (Verweise auf Liefercommit `0e7b358`). Beim nächsten Versionswechsel fällt 3.38.0 heraus.
- **Prüffallstricke:** Konsolenausgabe nie in den OneDrive-Ordner umleiten (Exit 120); keine UI-Suiten parallel zur Vollprüfung oder zu Messungen; erzeugte Mehrfachklicks brauchen Zeitstempel (`time=`), sonst zählt Tk sie als eine Folge; Dialogknöpfe zeigen „Speichern“ statt „Speichern …“ (`RoundedButton.action_text`).

## 6. Was als Nächstes ansteht

- **Aktueller Lieferstand 16.10.2026:** 3.43.0 (UI-/UX-Paket) automatisch geprüft und nach 07/05 geliefert; [Nachweis](../01_Repository/Glide/tests/qa-3.43.0/ui_ux_paket_2026-10-16/README.md). Vorher 3.42.0 (Paket 7) vollständig einschließlich Paketen geliefert; [Lieferabschluss](../01_Repository/Glide/tests/qa-3.42.0/eigenstaendige_pakete_2026-10-13/lieferabschluss.json).
- **Priorität ab 15.10.2026 (D50):** Das [UI-/UX-Feature-Paket](Featurepaket_UI_UX/PROMPT.md) geht dem Abschluss von Paket 8 vor; bei unvereinbaren Vorgaben gilt das UI-/UX-Paket. Paket 8 / 4.0.0 bleibt auf dem unten dokumentierten Vorbereitungsstand pausiert und wird danach auf den neuen Stand gebracht. Pakete 1–7 und FP-00 sind geliefert; die Folgepakete aus D49 bleiben für die neue Planung offen, keine weitere Paketumsetzung automatisch starten. Bereits gewählte Funktionsoptionen bleiben erhalten, Veröffentlichungstore unverändert.
- **Aktiver Arbeitsstand:** `claude/ui-ux-paket` bis zum Merge (siehe Git-Zeile in §2). Nächste Schritte: auf dem Referenz-Mac eingefrorene Mac-Vollprüfung und `packaging/macos/baue_app.py` für 3.43.0; Antworten E-U1–E-U4 einholen ([Entwicklungsplan §17.3](Glide_Entwicklungsplan.md#173-entscheidungsvorlagen-für-den-inhaber)); danach Paket 8 auf den 3.43.0-Stand bringen.
- **Paket 7 / 3.42.0 abgeschlossen:** Mac-Bau3 und Windows-Paketlauf 38547672592 grün, 65 Paket-Werkzeugtests. App-/Ressourcenbaum seit der erfolgreichen nativen Vollmatrix unverändert; aktueller Prüfbootstrap zusätzlich nativ belegt. Alle roten Lizenz-/PE-/Startprüfer-Vorläufe bleiben im Paketnachweis. Windows-ACL-Sperren ausschließlich im vergänglichen Hosted-CI, niemals an Inhaberinstallationen; ursprüngliche Zugriffsregeln geprüft, AI-Rohmarkerdifferenz ausdrücklich dokumentiert. Root-07, Mac-Bundle und Windows-Paket geliefert; ab jetzt P8 auf diesen Lieferstand bringen.
- **Paket 8 / 4.0.0 aktiv:** 57 Semantikfälle, elf Runtimeverträge, 79 Paket-/zwölf Reader-Prüferfälle und drei Versionsvertragsfälle grün. Zehnter nativer Lauf 38741910227: Linux/Windows Runtime, Tcl4 und GUI10 grün; Linux Unicode/Caret/ACTIVE/Disabled und exklusiver Fokus extern grün. Orca-Erfassung/Suche gesprochen, danach nativer SIG11-Absturz. Callbackdatentypen und GObject-Lebensdauer im Anbieter korrigiert, externe Lebensdauerprobe und Crashdiagnose vorbereitet. NVDA meldet Arbeitsbereiche: Heute jetzt korrekt; weitere Aufgabenwahl braucht Navigation über Abschnittszeilen. Native MSAA-Probe auf tatsächlichen Tk-Client-HWND korrigiert. Windows-Paketprozess/Kernablauf grün; Gesamtstart wegen zweier abweichend restaurierter originaler CI-Symlinks rot, Linkhandle-Restaurierung vorbereitet. Native11 und vollständige Readerabläufe offen. Vollprüfstand91 mit verpflichtender eigener9.1 ab Version4 vorbereitet; finale eingefrorene Vollmatrix und Pakete offen. Abschlussauftrag15.10: laufendesP8 abschließen, Folgepakete fürNeuplanungoffenhalten; Root weiter geliefert3.42.0. [Nachweise](../01_Repository/Glide/tests/qa-3.42.0/zugang400_vorbereitung_2026-10-14/README.md).
- **Ablage:** 3.43.0 hält Nachweise/Archive nur für die sieben neuesten Versionen (3.38.0–3.43.0 einschließlich 3.39.1) und Fensterbilder nur für die drei neuesten; mit dem Versionswechsel entfielen Archivdatei, Nachweise und Releaseplanung von 3.37.0. Git trägt frühere Nachweise. Mit dem nächsten Versionswechsel fällt 3.38.0 heraus: aktive Verweise vorher auf einen festen Git-Lieferstand umstellen.
- **Menschenabnahme:** Manuelle Windows-/Linux-Sichtfälle W01/W06–W09, DPI/Mehrmonitor, echte Tastatur/Maus/Trackpad und Reader nach der [Prüfliste](Glide_Manuelle_Pruefung.md) getrennt offen. Native Windows-Vollprüfungen bis 3.42.0 einschließlich 3.39.1 grün; kein menschliches Testergebnis daraus ableiten. Reale zusätzliche Reader-Prüfplätze am 13.10.2026 beantwortet: „Keiner der beiden Prüfplätze“. Außer Mac/VoiceOver stehen dem Inhaber somit keine Windows-/NVDA- oder Linux-/Orca-Prüfplätze zur Verfügung. Automatisierte native Prüfungen weiterführen; die tatsächlichen Reader-/Menschenabnahmen bleiben eigene offene Tore, kein Verzicht daraus ableiten.
- **Veröffentlichungstore:** I1–I5/I9–I11 bleiben nach D43 gesondert offen (Inhaberangaben, Glide-Lizenz, öffentliche Signaturen/Konten, Marke, Systeminstallation, Fremdbildrechte, Historienumschreibung, GitHub-Auftritt). Keine Käufe, Historienumschreibung oder stillen Bildlöschungen aus der Fortsetzung ableiten.


**Abschlussauftrag 15.10.2026:** Der Inhaber möchte die nächsten Schritte und Pakete neu strukturieren. Zunächst die laufenden 4.0-Arbeiten samt notwendigen Korrekturen, Prüfungen und umsetzbaren Kernfunktionen zum gesicherten Abschluss bringen. Danach Übergabe mit tatsächlichem Lieferstand, umgesetztem Umfang, Prüfbelegen und ausdrücklich offenen Abnahmen; weitere Folgepakete erst aus der neuen Planung starten. D49-Auswahlinhalte bleiben erhalten, ihre Ausführungsfolge wird anschließend neu geordnet.
