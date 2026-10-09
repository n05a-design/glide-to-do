# Glide – Übergabe an eine neue Sitzung

Stand 09.10.2026 · Glide 3.35.0 · Aufgabenformat 23 · für den nächsten Chat oder Bearbeiter

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
| Entscheidungen D01–D17, frühere Antworten, Leitgedanken des Inhabers | [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) |
| Produktgrenzen, sechs Prinzipien, Prinzipien-Check | [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) |
| Code | `01_Repository/Glide/src/glide/` – Module siehe [Architektur](../01_Repository/Glide/docs/02_ARCHITECTURE.md) |
| Verhalten der Funktionen | [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md) |
| Datenformat, Backups, Austausch | [Daten und Migration](../01_Repository/Glide/docs/06_DATA_BACKUP_MIGRATION.md) |
| Prüfen | [Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), Ergebnisse im QA-Bericht, Nachweise unter `tests/qa-<Version>/` |
| Startbare Fassung | `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.33.18.pyw`; nach grüner Vollprüfung 28 Code-Dateien/131 Ressourcen und Showcase SHA-256-abgeglichen |
| macOS-Bundle | `01_Repository/Glide/build/macos/Glide.app` trägt seit 09.10.2026 **3.33.18** (Mac-Vollprüfung Exitcode 0, Ad-hoc-Signatur, SHA-256-gleich zu 07); menschliche Abnahme offen. Kennung `de.shaye.glide` (Windows `Shaye.Glide`) |
| Pflegewerkzeuge | [`scripts/pflege/`](../01_Repository/Glide/scripts/pflege/README.md): Versionswechsel, Abgleich nach 07, Kürzen der Ablage, Messungen, Pfadbereinigung |
| Demo- und Testdaten | `05_Probelisten_Testdaten/Showcase` (eigener Starter), Fixtures unter `01_Repository/Glide/tests/fixtures` |
| Analyse: Funktionen, Oberfläche, Entscheidungen, Nutzung, Abweichungen Dokumentation ↔ Code | [Analyse](Glide_Analyse.md) |
| Markt und Vorbilder | [Markt und Vorbilder](Glide_Markt_und_Vorbilder.md) |
| Manuelle Prüfung | [Prüfliste](Glide_Manuelle_Pruefung.md) |
| Veröffentlichung, Store, Lizenz, GitHub-Auftritt | [Veröffentlichung](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md) |
| Regeln für Dokumente, Zuständigkeiten | [Dokumentenpflege](../01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) |
| Grafik-Master | `20_Grafik_Master` (Logo, App-Symbol, Affinity-Quelle, Inspiration, Beispielbilder) |
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
  - Die Arbeitskopie hat CRLF; außerhalb von `01_Repository/Glide` regelt keine `.gitattributes` die Zeilenenden (W03). Dateien von dort vor dem Commit in einem Linux-Klon nach LF normalisieren.
  - Windows zeigt Dateinamen teils kleingeschrieben (`glide-showcase.glidebackup`); maßgeblich ist die Schreibweise in Git.
  - OneDrive legt Konfliktkopien `<Name>-<Gerätename>.md` an, und eine dort liegende Arbeitskopie kann veraltete Fassungen behalten. Mit 3.33.8 gelangten so sechs Kopien und die am 03.10.2026 aufgelöste Projektübergabe ins Repository, vier Hauptdokumente waren dabei gekürzt. Am 05.10.2026 zusammengeführt. Vor jedem Commit neu hinzugefügte Dateien und stark geschrumpfte Dokumente prüfen (W04).
  - In PowerShell heißt der Benutzerordner `$env:USERPROFILE`, nicht `%USERPROFILE%`.
- Technische Fallstricke (Menübefehle unter macOS, `update()` in Rückrufen, Tk 9 und `place`, Bindtags, Leinwand ohne Kantenglättung, Design statt `theme_name`): [Architektur, Abschnitt 5](../01_Repository/Glide/docs/02_ARCHITECTURE.md#5-tk-fallstricke-teuer-gelernt).

## 5. Prüfen

- **Windows-Konsole:** Vor Prüfbefehlen in PowerShell `$env:PYTHONUTF8="1"` setzen; sonst kann die Ausgabe einer Fehlermeldung mit Checkbox-Zeichen unter cp1252 abbrechen, bevor das Gesamtprotokoll geschrieben wird.
- **Vor jedem Commit:** `python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` aus `01_Repository/Glide` (braucht Python mit tkinter, unter Linux Xvfb). Im Linux-Container möglich: CI-Grundstufe, Startprobe, `messung_speicherweg.py`; nicht möglich: macOS/Tk-9-Abnahme, Bundlebau, physische Bedienung. Ergebnisse als „Linux/Tk 8.6, künstliche Daten“ kennzeichnen.
- **Abnahme einer Version** auf dem Mac: `python3 -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.35.0/<Name> --timeout 900` – 76 Integrationssuiten, Unit-Tests, Showcase, fünf Analysen.
- **Windows:** `tests\tools\windows_vollpruefung.cmd` (dieselbe Vollprüfung mit Python 3.14/Tk 9 und Fensterfotos); Anleitung und Rückmeldung in der [Prüfliste, B0](Glide_Manuelle_Pruefung.md#b-windows-pc-nach-der-vollprüfung).
- **Historische Referenz:** 3.33.6 auf dem Mac vom 02.10.2026; aktueller Windows-/Python-Stand 3.33.18 im QA-Bericht. Vorhandenes Bundle weiter 3.33.6; keine native Mac-/Bundle-Abnahme der neuen Pakete behaupten.

## 6. Was als Nächstes ansteht

- **Sprint abgeschlossen** (3.33.19–3.35.0): Abgleich, Abweichungen und Offenes in [Entwicklungsplan §15.4](Glide_Entwicklungsplan.md#154-abschlussabgleich-abs-09102026).
- **Für den Inhaber:** Arbeitsstand committen (die Versionen 3.33.19–3.35.0 und ihre Nachweise sind nicht eingecheckt; die Aufbewahrung entfernt sonst weitere uneingecheckte Nachweise). Danach die Entscheidungen E-S1–E-S8 ([§15.3](Glide_Entwicklungsplan.md#153-benötigte-inhaberentscheidungen-stand-08102026)) – sie geben die nächsten Pakete frei.
- **Prüfungen außerhalb des Macs:** Windows-Vollprüfung des Stands 3.35.0 (deckt W02 und die Lieferungen ab 3.33.19), Windows-Sichtprüfung W07/W08 (B1a), Linux-Sichtprüfung der JPEG-Vorschau (N08), menschliche Abnahme I6 ([Prüfliste](Glide_Manuelle_Pruefung.md)).
- **Ohne Entscheidung möglich, aber nicht beauftragt:** Stufe 5 (N13, SQLite-Neubewertung, Vorrat) nur auf ausdrücklichen Auftrag.

## 6a. Verlauf des Sprints (Stand 09.10.2026)

Maßgeblich: [Entwicklungsplan §15](Glide_Entwicklungsplan.md#15-sprint-ab-08102026-aufgabenkatalog). Nachweise unter `01_Repository/Glide/tests/qa-<Version>/`.

| Version | Paket | Aufgaben | Nachweis |
|---|---|---|---|
| 3.33.19 | Tempo | P06r, P04, P03r, E01, P01r, P08c | `qa-3.33.19/tempo_2026-10-09/` |
| 3.33.20 | Komfort | KO02, KO03, KO05, KO06, U04, U20, N07, AB08, AU06 | `qa-3.33.20/komfort_2026-10-09/` |
| 3.33.21 | Ruhige Oberfläche | N01, U15, U05r, U09, U18, OB05, OB01r, W05 (W07/W08 ◇) | `qa-3.33.21/oberflaeche_2026-10-09/` |
| 3.34.0 | Wissen und Seiten | B4, G14h, D-03, H-02r, N08; P07 ✕ nach Messung | `qa-3.34.0/wissen_2026-10-09/` |
| 3.35.0 | Pixel und Austausch | G19, G-03, G24, F-03 | `qa-3.35.0/austausch_2026-10-09/` |

- **Phase 0:** A01, PR01 (Mac-Vollprüfung und Bundle 3.33.18), W03, W04, W10–W15, DOK3; W02 auf dem Mac erledigt, Windows offen.
- **Lieferweg je Version:** CHANGELOG → `versionswechsel.py` → 07-README (Lieferabsatz, Module) → Nachweisrahmen → Standprüfung → eingefrorene Kopie im Scratchpad (ohne `.git`, `.claude`, `archiv`, `build`) → `pruefen.py --modus voll` → in der Kopie `abgleich_07.py` und `showcase_abgleich.py` → 07 und 05 zurückspielen → `baue_app.py`, Signatur im Bauordner und auf Rückkopie prüfen (im OneDrive-Ordner selbst scheitert `codesign` am Dateianbieter) → Nachweise, QA-Bericht, Plan.
- **Prüffallstricke:** Konsolenausgabe nie in den OneDrive-Ordner umleiten (Exit 120); keine UI-Suiten parallel zur Vollprüfung oder zu Messungen; erzeugte Mehrfachklicks brauchen Zeitstempel (`time=`), sonst zählt Tk sie als eine Folge; Dialogknöpfe zeigen „Speichern“ statt „Speichern …“ (`RoundedButton.action_text`); eine verwaiste `.git/index.lock` (leer, kein Git-Prozess) hält `ablage_kuerzen.py` an.

## 7. Offen beim Inhaber

- Feature-Arbeit ist am 05.10.2026 beauftragt; Bearbeitungstiefe der Auswahl A–H je Paket; D07 erst zur Pixel-Etappe; Importquelle und Bauwerkzeug erst in Stufe 4; AU03, OB04 und AU07, wenn das jeweilige Paket des Ausbauprogramms ansteht.
- I1 Inhaberangaben bestätigen, I2 Lizenz veröffentlichen, I3 Developer-ID und Code-Signing-Zertifikat, I4 Markenprüfung, I5 Python 3.14.7 auf dem Mac installieren, I6 manuelle Prüfsitzungen nach grüner Windows-Vollprüfung 3.33.18 ([Prüfliste](Glide_Manuelle_Pruefung.md)), I7 Referenzentwürfe für „Heute“, Liste und Seite vor Welle 2 des Ausbauprogramms, I8 Lösungsweg für das Logo unter Tk 8.6 ([Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md)).
- I9 Rechte an Fremdbildern in `20_Grafik_Master` und im Showcase, I10 Git-Historie bereinigen, I11 GitHub-Auftritt ([Entwicklungsplan §11](Glide_Entwicklungsplan.md#11-nur-durch-den-inhaber)).

Die aktuellen Vollprüfungen liefen mit Python 3.14.7/Tk 9.0.4 auf Windows. I5 betrifft weiter den Mac.
