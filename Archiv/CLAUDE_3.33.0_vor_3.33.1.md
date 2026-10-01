# Arbeitsregeln für Claude Code – Glide

Stand 01.10.2026 · Glide 3.33.0

Sprache: Deutsch (Antworten, Dokumente, UI-Texte). Diese Datei verweist nur auf die verbindlichen Projektregeln und ergänzt, was für Claude-Code-Sitzungen im Repository gilt. Regeln nicht hier doppeln, sondern an der Quelle pflegen.

## Struktur

- Repository-Wurzel = Projektordner:
  - `00_Arbeitsvorbereitung` – Planung, Entscheidungen, Übergaben
  - `01_Repository/Glide` – Quellbaum: `src/glide/app.pyw`, Tests, Verträge, Pflegewerkzeuge
  - `07_Python-Versionen` – startbarer, bytegleicher Lieferstand
  - weitere Ablageordner
- Querverweise setzen genau diese Struktur voraus.

## Lesereihenfolge

1. [01_Repository/Glide/AGENTS.md](01_Repository/Glide/AGENTS.md) – verbindliche Arbeitsregeln und Abschlusskriterium
2. [Sitzungsübergabe](00_Arbeitsvorbereitung/Glide_Sitzungsuebergabe_2026-09-30.md) und [Arbeitsrichtung](01_Repository/Glide/docs/ARBEITSRICHTUNG.md) – Stand, verbindliche Entscheidungen D01–D17, beauftragte Arbeit, Abnahme
3. [Entwicklungsplan ab 3.33](00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md) und [Beschlüsse D09–D17 vom 01.10.2026](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md#beschlüsse-vom-01102026)
4. [Dokumentenpflege](01_Repository/Glide/docs/DOKUMENTENPFLEGE.md) vor jeder Dokumentänderung
5. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern)

## Ergänzungen für diese Umgebung

- **Auftrag:** Nur den ausdrücklich beauftragten Schnitt umsetzen; offene Auswahl (A–H, D07) nicht selbst entscheiden. Bereits Entschiedenes (z. B. Q3, G07, D09–D17, Produktgrenzen) nicht erneut vorlegen. Neue oder angefasste Fachlogik als Tk-freies Modul mit Unit-Tests (D17).
- **Daten:** Nie echte Nutzerdaten; `GLIDE_DATA_DIR` vor dem Import auf einen temporären Ordner setzen. Werkzeuge mit `python3 -B` starten.
- **Linux-Container:**
  - Möglich sind Standprüfung (`python3 -B tests/tools/standpruefung.py` in `01_Repository/Glide`), Syntaxprüfung, Startprobe unter Xvfb (Tk 8.6), `scripts/pflege/messung_speicherweg.py` und `tests/qa-3.32.3/pruefaufrufe_2026-10-01/werkzeuge/pruefaufrufe_probe.py`.
  - Nicht möglich sind macOS/Tk-9-Abnahme, Bundlebau und physische Bedienung. Ergebnisse als „Linux/Tk 8.6, künstliche Daten“ kennzeichnen.
- **Lieferstand:** `07_Python-Versionen` und `src/glide` nur im Rahmen einer Produktionsrunde ändern (Versionswechsel, `abgleich_07.py`, SHA-256).
- **Git-Regeln der Ablage:**
  - `vendor/**` und `resources/fonts/**` werden unverändert gespeichert (`-text`).
  - tkdnd-`.so` sind ausdrücklich erlaubt.
  - `*.log` und `*.glidebackup` schließt `01_Repository/Glide/.gitignore` weitgehend aus; Prüfprotokolle unter `tests/qa-*/` sind seit D09 freigegeben.

Lokaler Start 3.33.0: T2/P09a zuerst. Aktiver Projektpfad `Github/glide-to-do`. D12 jetzt vollständig: Zeichnungen und Pinnwand-Vorschau. [Fundament-Vertrag](01_Repository/Glide/docs/73_FUNDAMENT_3.33.0.md).
