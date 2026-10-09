# Arbeitsregeln für Claude Code – Glide

Stand 10.10.2026 · Glide 3.35.0

Sprache: Deutsch (Antworten, Dokumente, UI-Texte). Diese Datei verweist nur auf die verbindlichen Projektregeln und ergänzt, was für Claude-Code-Sitzungen im Repository gilt. Regeln nicht hier doppeln, sondern an der Quelle pflegen.

## Struktur

- Repository-Wurzel = Projektordner:
  - `00_Arbeitsvorbereitung` – Übergabe, Entwicklungsplan, Markt und Vorbilder, manuelle Prüfliste
  - `01_Repository/Glide` – Quellbaum: `src/glide/app.pyw`, Tests, Dokumentation, Pflegewerkzeuge
  - `07_Python-Versionen` – startbarer, bytegleicher Lieferstand
  - `05_Probelisten_Testdaten` (Showcase), `20_Grafik_Master` (Grafikquellen)
- Querverweise setzen genau diese Struktur voraus.

## Lesereihenfolge

1. [01_Repository/Glide/AGENTS.md](01_Repository/Glide/AGENTS.md) – verbindliche Arbeitsregeln und Abschlusskriterium
2. [Übergabe](00_Arbeitsvorbereitung/Glide_Uebergabe.md) und [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) – Stand, verbindliche Entscheidungen D01–D43, beauftragte Arbeit, Abnahme
3. [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md) – Aufgaben mit Status, Stufen, Ziele; Verhalten der Funktionen in [Funktionen](01_Repository/Glide/docs/20_FUNKTIONEN.md)
4. [Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) vor jeder Dokumentänderung: ein Thema, ein Dokument; zusammenführen und löschen statt archivieren (Auftrag vom 03.10.2026)
5. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern)

## Ergänzungen für diese Umgebung

- **Auftrag:** Nur den ausdrücklich beauftragten Schnitt umsetzen; offene Auswahl nicht selbst entscheiden. Bereits Entschiedenes (Q1–Q5, D01–D43, Produktgrenzen) nicht erneut vorlegen. Der neue Sprint wird gemeinsam geplant (Entwicklungsplan §15); Runden 1–6 sind entschieden, acht Versionen in §15.7/§15.8 vorgeschlagen; Gesamtplanbestätigung offen. Neue oder angefasste Fachlogik als Tk-freies Modul mit Unit-Tests (D17).
- **Daten:** Nie echte Nutzerdaten; `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner setzen. Werkzeuge mit `python3 -B` starten.
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

Größere Feature-Pakete sind seit 07.10.2026 beauftragt; Umfang und Folgepakete im [Entwicklungsplan §4.4](00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026). Ein gemeinsamer eingefrorener Volllauf je Paket, gezielte Teilprüfungen bleiben Pflicht.
