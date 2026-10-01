# Arbeitsregeln für Claude Code – Glide

Sprache: Deutsch (Antworten, Dokumente, UI-Texte). Diese Datei ist die **lebende** Kurzfassung. Die [Claude-Übergabe 3.32.3](00_Arbeitsvorbereitung/CLAUDE_UEBERGABE_Glide_3.32.3.md) ist ein eingefrorener Stand und wird nicht geändert.

## Lesereihenfolge

1. [00_Arbeitsvorbereitung/README.md](00_Arbeitsvorbereitung/README.md) – was gilt
2. [Claude-Übergabe §3–§6](00_Arbeitsvorbereitung/CLAUDE_UEBERGABE_Glide_3.32.3.md) – Entscheidungen D01–D08, beauftragte Arbeit, Regeln
3. [Entwicklungsplan](00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md) und offene [Entscheidungen E01–E10](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)
4. Erst dann die betroffene Codestelle **und ihre Aufrufer** (Funktionsnamen suchen, nicht Zeilennummern; Methodennamen sind teils mehrfach vergeben)

## Grenzen des Auftrags

- Nur den ausdrücklich beauftragten Schnitt umsetzen. Offene Auswahl (A–H, E01–E10, D07) nicht selbst entscheiden.
- Empfehlungen sind keine Aufträge.
- `07_Python-Versionen/` ist ein **bytegleicher Lieferstand**. Dort nichts ändern außer im Rahmen einer Produktionsrunde:
  - neue Version,
  - CHANGELOG/Vertrag/QA nachführen,
  - SHA-256-Abgleich (`00_Arbeitsvorbereitung/Analyse_2026-10-01/ergebnisse/sha256_07_Laufzeitdateien.txt` neu erzeugen).
- Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung. Nur Standardbibliothek + tkinter (+ optional `vendor/tkinterdnd2`).

## Unverhandelbare technische Regeln (aus Übergabe §6)

- **Mutationsrahmen:**
  - Punkte über `item_change`,
  - Listen/Ordner über `sidebar_change`,
  - Umbauten zusätzlich `guarded_structural_change`,
  - Dialoge über `run_modal`.
- **Speichern:** atomar mit `fsync`, Sperre, Sicherungen, Vorsicherungen, Migrationen und Fehleranzeige erhalten. Kein verzögertes ungesichertes Speichern.
- **Neues Datenfeld oder neue Art:** Datenformat-Tor – Formatversion, Vorsicherung, Migration, Altleser schreibgeschützt, Tests.
- **Rückrufe:** Kein `update()`/`update_idletasks()` in Rückrufen, die sich selbst auslösen können. Ersetzte Bindungen und `after`-Aufträge freigeben.
- **Menüs:** Menübefehle laufen über `defer_window_menu_commands`; Tests nach `menu.invoke()` kontrolliert `update()`.
- **Menübeschriftungen sind Schlüssel** für `ACTION_GROUPS`/App-Aktionen. Vor dem Umbenennen Zuordnung prüfen (Risiko R2).
- **Farben** nur über `BUTTON_ROLE_RULES` (Rot Löschen, Grün Bestätigen, Lila Hinzufügen, Gelb Hinweis). Symbole aus `ICONS`.
- **Undo kann Python-Objekte ersetzen:** Befehle lesen Daten über IDs, nicht über gehaltene Referenzen.
- **Feste Kennungen:** macOS `de.shaye.glide`, Windows `Shaye.Glide`.

## Daten und Tests

- **Nie echte Nutzerdaten.** `GLIDE_DATA_DIR` auf einen temporären Ordner setzen, **bevor** Glide importiert wird.
- **Fotos** nur vom eigenen Glide-Fenster bzw. einer Xvfb-Anzeige, auf der nur Glide läuft.
- **In dieser Linux-Umgebung möglich** (siehe [Analyse-README](00_Arbeitsvorbereitung/Analyse_2026-10-01/README.md)):
  - Syntaxprüfung,
  - Startprobe und Ansichtsprobe unter Xvfb mit Tk 8.6,
  - Persistenzmessung.
- **Nicht möglich:** macOS/Tk-9-Abnahme, die 58 Integrationssuiten (nicht im Repository), physische Bedienung. Ergebnisse entsprechend kennzeichnen („Linux/Tk 8.6, künstliche Daten“).
- **Messungen:** vorher/nachher in gleicher Umgebung, Aufwärmen, Median und p95, Rohwerte ablegen. Eine Optimierung gilt erst bei nachgewiesenem Gewinn als erfolgreich.
- **Werkzeuge** mit `python3 -B` starten. `_glide_laden.py` verhindert Bytecode im Laufzeitordner.

## Dokumentation

- Bestehende Dokumente nicht löschen. Vor dem Überschreiben eines Dokuments die Vorfassung nach `00_Arbeitsvorbereitung/Archiv/<Name>_<Version>_vor_<Anlass>.md` kopieren. Überholtes mit `_Z` kennzeichnen.
- Neue Entscheidungen datiert in die Entscheidungsvorlage bzw. Arbeitsplanung, nicht in den Entwicklungsplan.
- Neue Funktionen vor Umsetzung durch den Prinzipien-Check ([UX-Prüfung §4](00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)).
- In lebenden Dokumenten Funktionsnamen statt Zeilennummern verwenden.

## Produktprinzipien (Kurzform)

Apple-like (funktioniert ohne Hinweistext) · Form folgt Funktion · keine Funktion doppelt · kein Platz verschwendet · nur das Wesentliche sichtbar · geringe Komplexität. Funktionen leben eingebettet, nicht in Zusatzfenstern; Seitenleiste, Kopf und Inhalt springen nie.
