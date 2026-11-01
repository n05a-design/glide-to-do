# WA-36: Seitenleiste und Erinnerungsstatus nach dem Speichern

Stand 01.11.2026 · Glide 3.50.0 · Aufgabenformat 26 · MacBook Air M2, macOS 27.2, Python 3.14 mit python.org-Tk, künstliche Daten

**Auftrag:** Fortsetzung WA-36 nach §21.38 („Seitenleisten-/Erinnerungsnachlauf nach dem Speichern noch nicht optimiert“) im Rahmen „komplett immer weiter umsetzen“ (31.10.2026). Reine Laufzeitänderung ohne Verhaltens-, Format- oder Oberflächenänderung; keine Lieferung (bei Codex), kein Git.

## Befund vorher

Profil des Abhakens bei 10.000 Aufgaben (cProfile, deshalb absolut überhöht): Der Neuaufbau der Seitenleiste nach jedem Speichern bestand zu rund 80 % aus vier Vollscans über den Bestand – Zahl hinter „Heute“ (Pool und Tagesplan je einmal), Labelzähler, Zeilentexte und Listenzähler. Teuer war dabei weniger die Prüfung je Aufgabe als der Durchlauf selbst: `walk_items` legte für jede Aufgabe einen weiteren Generator an, auch ohne Unterpunkte (1,15 Mio. Aufrufe für zehn Abhakvorgänge). Listenzähler wurden je Aufbau mehrfach berechnet (Zeile, Ordnersumme, Zeilentext). Der Erinnerungsstatus prüfte nach jedem Speichern jede Aufgabe über `reminder_event`.

## Änderungen

| Stelle | Änderung | Warum verhaltensgleich |
|---|---|---|
| `walk_items`, `count_items` | Rekursion nur bei vorhandenen Unterpunkten | Die Normalisierung führt `children` immer als Liste; eine leere Liste lieferte schon vorher nichts |
| `list_item_count` (neu) | Punkte einer Liste je Aufbau einmal (`render_cached`, Schlüssel Listenobjekt); genutzt von Seitenleistenzeile, Eingang, Ordnersumme und Zeilentext | Innerhalb eines Aufbaus ändert sich der Bestand nicht (bestehender Vertrag von `render_pass`) |
| `_collect_today_view_pool` | erst Rohwerte `due`/`planned_date` prüfen | `normalize_due` liefert für leere Rohwerte immer `None` |
| `_collect_plan_day_entries` | erst Rohwert `planned_date` prüfen | Zieltag ist nie leer; leerer Rohwert ergibt `None` ≠ Zieltag |
| `count_labelled_items` | erst Rohwert `labels` prüfen | `item_labels` liefert für leere/fehlende Zuordnung `[]` |
| `reminder_rows` | Aufgaben ohne Feld `reminder` überspringen | `reminder_event` liefert dann immer `None`; Werte ungleich `None` gehen unverändert in die bisherige Prüfung (auch fehlerhafte) |

## Prüfung

- **Differential** (`differential_seitenleiste.py`): acht Zufallsbestände mit Unterpunkten bis Tiefe 4, allen Arten, ungültigen Datumswerten, unbekannten/System-/leeren Labels, Ordnern und Archiv; je Anfangszustand und sechs Abhakwechsel. Verglichen werden alle Zeilen aller Seitenleistenbäume, Heute-/Label-/Ordner-/Listenzähler, Heute-Pool, Tagespläne dreier Tage, Abschnitte von „Heute“ und Baumdurchlauf zwischen Vorher-Stand und neuem Stand. Ergebnis: siehe Abschnitt „Endstand“.
- **Regressionstest** in `test_fortsetzung33311` (WA-36-Block): Baumdurchlauf und Zähler gegen einen ungekürzten Referenzdurchlauf, Heute-Pool/Tagesplan/Labelzähler gegen Referenzbedingungen, Listenzähler je Aufbau genau einmal, sichtbarer Seitenleistenzähler, Erinnerungszeilen gegen Referenz über alle Arten/Zustände.
- **Breite Regression** nach der Seitenleistenstufe (App `3925c546…`): 23 Integrationssuiten grün (u. a. Arbeitsmodi 32/32, UI/UX 17/17, Schutzrunde 16/16, Mutationsreste, Datenintegrität, Speichervergleich, Wiederanlauf).

## Messung

`messung_seitenleiste.py`, je Stand/Größe/Bestand eigener Prozess, Median aus 11 Abhakvorgängen ohne Tk-Nachlauf. „leer“: Aufgaben ohne Termin/Label (Bestfall der Vorprüfungen); „gemischt“: 40 % Fälligkeit, 30 % Bearbeitungstag, 30 % Label, 20 % erledigt. Rohwerte in `ergebnis.json` (Stände `bf1f3154…` vorher, `3925c546…` Seitenleiste, `960977a4…` zusätzlich Erinnerungsstatus).

| 10.000 Aufgaben | Seitenleiste vorher → nachher | Erinnerungsstatus | Abhaken gesamt |
|---|---|---|---|
| leer | 16,0 → 6,0 ms (−63 %) | 3,9 → 1,6 ms | 119,6 → 105,1 ms (−12 %) |
| gemischt | 25,8 → 18,6 ms (−28 %) | 3,6 → 1,2 ms | 135,8 → 124,7 ms (−8 %) |

Bei 1.000 Aufgaben liegen Seitenleiste und Erinnerungsstatus unter 4 ms, Abhaken bei 17–21 ms (−6 % bzw. −8 %). Die im Profil genannten ~70 ms waren Profileraufschlag; ohne Profiler war der Nachlauf schon vorher klein. Den größten verbleibenden Anteil beim Abhaken haben das Schreiben (JSON-Kodierung und Datei) und der Baumaufbau der aktiven Liste.

## Endstand

Differential auf App `49ef0b26…` (Seitenleiste, Erinnerungsstatus und Featurenachtrag) gegen den Vorher-Stand: **8 von 8 Zufallsbeständen bytegleich** (je 337–419 Aufgaben, sieben Zustände). Gemeinsame Regression auf demselben Stand: 1.094 Fachtests (ein Skip) und 26 Integrationssuiten grün, darunter Arbeitsmodi 34/34, UI/UX 17/17, Schutzrunde 16/16, Mutationsreste, Datenintegrität, Speichervergleich, Wiederanlauf, UI-Nachtrag 3.6 und Release 3.7. Der anschließende Nachtrag „Als Nächstes“ und der eingefrorene Volllauf stehen im [Featurepaket](../featurepaket_2026-10-31/README.md).

## Restkosten und verworfene Option

Profil nach der Änderung (App `cb58fdea…`, 10.000 Aufgaben, je Abhakvorgang, mit Profileraufschlag): Undo-Schnappschuss ~19 ms (`PackedState`: kompaktes JSON plus zlib über alle Listen), Datendatei ~20 ms (JSON mit Einrückung, C-Kodierer), Baumaufbau der aktiven Liste ~34 ms, Speichervergleich der berührten Liste ~4 ms. Übrig bleibt also fast nur die Serialisierung des ganzen Bestands; sie ließe sich nur mit inkrementellem Speichern oder Schnappschüssen je Liste deutlich senken – ein Architekturschritt, kein verhaltensgleicher Kleinumbau.

Geprüft und **verworfen:** `pickle` statt JSON im Undo-Schnappschuss (Mikromessung 23 → 10 ms). `pickle` erhält mehrfach referenzierte Objekte als dieselben Objekte und Tupel als Tupel; JSON liefert bei jedem Rückgängig unabhängige Listen und Wörterbücher. Diese Eigenschaft trägt der Rückgängig-Speicher heute stillschweigend, deshalb keine Änderung ohne gesonderten Nachweis.

**Startseite (Messung 01.11.2026, App `fe552fce…`):** Rückkehr zur Startseite nach einer Änderung bei 10.000 gemischten Aufgaben im Median 357–360 ms. Davon entfällt der größte Teil auf den Tk-Aufbau der Kacheln; die Bestandsauswertung (`home_dashboard.build`, Dringlichkeitsrang je offener Aufgabe, Heute-Zähler, „Verspätet“ für Gismo) liegt bei zusammen rund 100 ms mit Profiler. Eine exakte Abkürzung des Dringlichkeitsrangs ohne Datumsrohwerte brachte nur 5–8 ms (1–2 %) und wurde deshalb **nicht übernommen**. Spürbar schneller würde die Startseite nur, wenn Kacheln gezielt statt vollständig neu aufgebaut würden.

## Grenzen

Linux-/Windows-Messungen und Tk 9.1 nicht wiederholt; Messung auf einem Gerät. Übrige Vollscans (Startseite, „Demnächst“) unverändert. WA-36 bleibt ◐.
