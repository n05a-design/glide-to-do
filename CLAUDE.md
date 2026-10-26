# Arbeitsregeln für Claude Code – Glide

Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Python-Lieferung 3.45.0, eigenständige Pakete 3.42.0

Aktueller Fortsetzungsauftrag 26.10.2026: nächstes Feature lokal umsetzen. Nach WA-12 ist die Verweisvorschau D55/WA-11 ergänzt; App `b53e6822…`, 29 passende Fachfälle und zwei neue Bedienfälle grün. Breite native Fokus-/Inspektor-/Tastenprüfung bleibt offen; [Paketnachweis](01_Repository/Glide/tests/qa-3.45.0/verweisvorschau_2026-10-26/README.md), [Plan §21.17](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2117-verweise-in-der-nebenansicht-nachschlagen-wa-11). Quelle auf 3.45.0 / Format 26, 07 beim vorherigen Abschluss `2e69d875…`, drei Laufzeitunterschiede. D51-Phasenabschluss offen; kein Commit/Push.

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
2. [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) – Stand, Entscheidungen D01–D56 (D49 als Auslegung mit Korrekturvorbehalt), beauftragte Arbeit, Abnahme
3. [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) – Aufgaben mit Status, Stufen, Ziele; Verhalten der Funktionen in [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md)
4. [Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) vor jeder Dokumentänderung: ein Thema, ein Dokument; zusammenführen und löschen statt archivieren (Auftrag vom 03.10.2026)
5. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern)

## Ergänzungen für diese Umgebung

- **Auftrag:** Den beauftragten Schnitt vollständig umsetzen; offene Produktauswahl nicht selbst entscheiden. D01–D56 und Produktgrenzen erhalten, D49 mit seinem Korrekturvorbehalt. Quelle und Python-Lieferung tragen 3.45.0; D55 und Speicherpaket sind darin gebündelt. Ältere Paket-/Abnahmebelege bleiben ihren Ständen zugeordnet. D55-Punkte 1–4 unter Windows abgenommen, übrige Menschen-/Plattformtore offen; eigenständige Pakete/Mac-Bundle weiterhin 3.42.0, Paket 8 / 4.0.0 pausiert. Aktueller Stand in [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Plan §21.15](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2115-weiterentwicklung-zu-3450-sicherungen-und-anhänge), Prüfung/Lieferung im [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md). Appweiter Gestaltungsvertrag sind die [Design Richtlinien](01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md), neue oder angefasste Fachlogik bleibt Tk-frei mit Unit-Tests (D17).
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
