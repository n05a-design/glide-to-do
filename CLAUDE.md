# Arbeitsregeln für Claude Code – Glide

Stand 12.11.2026 · Glide 3.55.0 · Aufgabenformat 26

Aktueller Quell-, Prüf- und Lieferstand: [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md). Aufgabenstatus und konkrete Gitautorisierung stehen im [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md).

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
2. [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) – Stand, Entscheidungen D01–D79 (D49 als Auslegung mit Korrekturvorbehalt), beauftragte Arbeit, Abnahme
3. [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) – Aufgaben mit Status, Stufen, Ziele; Verhalten der Funktionen in [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md)
4. [Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) vor jeder Dokumentänderung: ein Thema, ein Dokument; zusammenführen und löschen statt archivieren (Auftrag vom 03.10.2026)
5. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern)

## Ergänzungen für diese Umgebung

- **Auftrag:** Den beauftragten Schnitt vollständig umsetzen; offene Produktauswahl nicht selbst entscheiden. D01–D79 und Produktgrenzen erhalten, D49 mit Korrekturvorbehalt. Aktuelle Umsetzung/Prüfung/Lieferung und konkrete Gitautorisierung ausschließlich aus Übergabe, Arbeitsrichtung und Entwicklungsplan lesen. Historische Belege behalten ihre Stände. Appweiter Gestaltungsvertrag sind die [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md); neue/angefasste Fachlogik bleibt Tk-frei mit Unit-Tests (D17).
- **Daten:** Nie echte Nutzerdaten; `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner setzen. Werkzeuge mit `python3 -B` starten.
- **Pfadlängen und OneDrive (29.10.2026):** Der Projektordner liegt in OneDrive. OneDrive synchronisiert keine Pfade über 400 Zeichen einschließlich seines Cloudpräfixes; auf PC-01 scheiterte bereits ein lokaler Pfad von 402 Zeichen. Windows-Werkzeuge ohne Langpfadunterstützung brechen ab 260 Zeichen ab, Glide-Exportziele ab 130 (`markdown_tree`). Prüfkopien, Prüfdaten und Temp nur in kurzen lokalen Ordnern außerhalb OneDrive anlegen (Ablage höchstens so lang wie `%USERPROFILE%\gq\a1029-092252`). Nach `13_TK-Test-Umgebung` nur flache Belege übernehmen (Berichte, Logs, Manifeste, `quellstand.json`), nie `projekt/`, `.git`, `daten/` oder `temp/`; Muster ist `13_TK-Test-Umgebung/belege_ablegen.py`. Vor jedem Kopieren in OneDrive die längste Zielpfadlänge prüfen. Fehlt eine Datei auf einem anderen Gerät, zuerst einen Synchronisationsfehler ausschließen, bevor eine Fehlstelle befundet wird.
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
