# Arbeitsregeln für Claude Code – Glide

Stand 29.10.2026 · Glide 3.49.0 · Aufgabenformat 26 · Python-Lieferung 3.47.0, eigenständige Pakete 3.45.0

Aktueller Gesamtauftrag 29.10.2026: alle begonnenen, übergangenen und unvollständig abgeschlossenen Glide-Arbeiten selbstständig abarbeiten; keine Rückfragen im beauftragten Umfang. Quelle 3.49.0/Format 26, Python/Showcase 3.47.0, native Pakete 3.45.0. Maßgeblich sind [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Plan §21.30](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2130-gesamtabschluss-begonnener-arbeiten). A01-Prüfadapter und gestoppte Folge in 13 Bereichssuiten/136 Fällen grün; WA-09 lokal umgesetzt, fünf Appfälle plus 21 Regressionen grün. Frühere eingefrorene WA-09-CI grün; neuere Mutations-CI nativ rot, siehe folgender Schnitt. [Aktueller Nachweis](01_Repository/Glide/tests/qa-3.49.0/abschlussreste_2026-10-29/README.md). Gesamtauftrag, WA-41, weitere technische Restumfänge und aktuelle Lieferung/native/Menschenabnahmen offen. Intel-Prüfplatz erfasst; neue AMD-Belege synchronisiert, MacBook M2 zusätzlich angekündigt. Ergebnisse pro Gerät und eingefrorenem Stand unter `13_TK-Test-Umgebung` trennen. Keine Veröffentlichung, Git-Pushes oder BIOS-/CPU-Änderungen aus der Fortsetzung ableiten.

Neuester Schnitt (§21.31): Labelanlage, Erledigte entfernen und Umbenennen plus Wächterprojektion für Aufgaben in gelöschten Listen. Aktuelle 17 Mutations- und 16 Schutzfälle grün; neue Intel-CI-Grundprüfung rot (erster Fachlauf 1.074 grün, zweiter ohne Systemzeitzonen nativer `0xC0000409`-Cacheabbruch). Rotbeleg, Windows-Ereignisse und FullMemory-Dump gesichert, Ursache offen. „Liste leeren“ inzwischen ebenfalls gezielt geschlossen (§21.32): 7 neue + 17 Mutations- + 16 Schutzfälle grün auf `39499ab3…`. Apple-Silicon-/Rosetta-Prüfprofil ergänzt; 231 Werkzeugtests grün (ein Skip), einschließlich Apple-Profil und Zählvertrag, keine native M2-Ausführung. Gerätevergleich danach eingeordnet und gemeinsame Glyphen-/Neustart-/JPEG-Prüffehler korrigiert (§21.34); PC-02 ist instabiler Prüfplatz. Nächster Einstieg: `add_item`/`add_item_advanced` und WA-42-Kindprozess-Folgestopp der CI; unerklärten ersten roten Leeren-Speicherfehlerfall erhalten. Gesamtauftrag unverändert offen.

Sprache: Deutsch (Antworten, Dokumente, UI-Texte). Diese Datei verweist nur auf die verbindlichen Projektregeln und ergänzt, was für Claude-Code-Sitzungen im Repository gilt. Regeln nicht hier doppeln, sondern an der Quelle pflegen.

## Struktur

- Repository-Wurzel = Projektordner:
  - `00_Arbeitsvorbereitung` – Übergabe, Entwicklungsplan, Markt und Vorbilder, manuelle Prüfliste
  - `01_Repository/Glide` – Quellbaum: `src/glide/app.pyw`, Tests, Dokumentation, Pflegewerkzeuge
  - `07_Python-Versionen` – startbarer separater Lieferstand; aktueller Quell-/Lieferabgleich im [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md)
  - `05_Probelisten_Testdaten` (Showcase), `20_Grafik_Master` (Grafikquellen)
- Querverweise setzen genau diese Struktur voraus.

## Lesereihenfolge

1. [01_Repository/Glide/AGENTS.md](01_Repository/Glide/AGENTS.md) – verbindliche Arbeitsregeln und Abschlusskriterium
2. [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) – Stand, Entscheidungen D01–D57 (D49 als Auslegung mit Korrekturvorbehalt), beauftragte Arbeit, Abnahme
3. [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) – Aufgaben mit Status, Stufen, Ziele; Verhalten der Funktionen in [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md)
4. [Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) vor jeder Dokumentänderung: ein Thema, ein Dokument; zusammenführen und löschen statt archivieren (Auftrag vom 03.10.2026)
5. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern)

## Ergänzungen für diese Umgebung

- **Auftrag:** Den beauftragten Schnitt vollständig umsetzen; offene Produktauswahl nicht selbst entscheiden. D01–D57 und Produktgrenzen erhalten, D49 mit Korrekturvorbehalt. Aktuelle Umsetzung/Prüfung/Lieferung und konkrete Gitautorisierung ausschließlich aus Übergabe, Arbeitsrichtung und Entwicklungsplan lesen. Historische Belege behalten ihre Stände. Appweiter Gestaltungsvertrag sind die [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md); neue/angefasste Fachlogik bleibt Tk-frei mit Unit-Tests (D17).
- **Daten:** Nie echte Nutzerdaten; `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner setzen. Werkzeuge mit `python3 -B` starten.
- **Skills:** Projekt-Skills liegen unter `.claude/skills/<Name>/SKILL.md` und werden in jeder Claude-Code-Sitzung erkannt, auch in der Cloud, aber nur bei passender Aufgabe geladen; lose `.md`-Dateien oder `skills-main/` im Projektordner erkennt Claude nicht. Fremdskills mit ihrer Lizenz ablegen und nicht um Glide-Regeln ergänzen; die bleiben in den verbindlichen Quellen. Aktiver Gestaltungsskill ist `design-richtlinien` (B20, 15.10.2026): ein Einstieg, der auf [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md) verweist. Der frühere Fremdskill (MIT, `emilkowalski/skills`; Fassung des Inhabers ohne „Initial Response“) liegt unverändert mit Lizenz unter `referenzen/`; er ist für das Web geschrieben: Grundsätze übernehmen, CSS-/JS-Beispiele nicht auf Tk übertragen.
- **Linux-Container:**
  - Möglich sind die CI-Grundstufe (`python3 -B tests/tools/ci_grundstufe.py --protokoll <Ordner>` in `01_Repository/Glide`; braucht ein Python mit tkinter) mit Stand-, Link- und Ablageprüfung, Startprobe unter Xvfb (Tk 8.6) und `scripts/pflege/messung_speicherweg.py`.
  - Nicht möglich sind macOS/Tk-9-Abnahme, Bundlebau und physische Bedienung. Ergebnisse als „Linux/Tk 8.6, künstliche Daten“ kennzeichnen.
- **Lieferstand:** `07_Python-Versionen` und `src/glide` nur im Rahmen einer Produktionsrunde ändern (Versionswechsel, `abgleich_07.py`, SHA-256).
- **Git-Regeln der Ablage:**
  - `vendor/**` und `resources/fonts/**` werden unverändert gespeichert (`-text`).
  - tkdnd-`.so` sind ausdrücklich erlaubt.
  - Das Repository ist öffentlich: `*.log` bleibt ausgeschlossen (Rohprotokolle lokal), `*.glidebackup` bis auf Fixtures. Keine Benutzerpfade in versionierten Dateien – vor Uploads `scripts/pflege/pfade_bereinigen.py`; die CI prüft das.
  - Keine Archivkopien von Fixtures oder Showcase, keine Fensterbilder (`fenster/`) neuer Vollprüfungen; Archive und Nachweise nur der sieben neuesten Versionen, Fensterbilder nur der drei neuesten (`scripts/pflege/ablage_kuerzen.py`). Vorfassungen trägt Git. Die CI prüft das (Schritt „Ablagegröße“).
  - Was `.gitignore` abfängt und wo sie nicht schützt (bereits versionierte Dateien, `git add -f`, Web-Upload), steht in ihrem Kopf.

Aktiver Projektpfad `Github/glide-to-do`.

Größere Feature-Pakete sind seit 07.10.2026 beauftragt; Umfang und Folgepakete im [Entwicklungsplan §4.4](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026). D51 bündelt mehrere Pakete je Phase: ein gemeinsamer eingefrorener Volllauf am Phasenende, gezielte Teilprüfungen bleiben Pflicht. E-P1–E-P5 sind noch offene Auswahlvorlagen.
