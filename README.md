# Glide – Aufgaben und Listen

Lokale, deutschsprachige Desktop-App für Aufgaben, Listen, Seiten, Notizen, Notizbücher, Galerien, Pinnwände und Pixelzeichnungen. Kernfunktionen arbeiten ohne Internet, Konto oder Cloudservice; die Daten liegen in einer eigenen JSON-Datei außerhalb des Programmordners. Python/Tk, nur Standardbibliothek (optional mitgeliefertes `tkinterdnd2`).

**Stand:** 3.32.3 · Aufgabenformat 20 · 01.10.2026

## Inhalt dieses Repositorys

| Ordner | Inhalt |
|---|---|
| [`07_Python-Versionen/`](07_Python-Versionen/) | Startbarer Laufzeitstand 3.32.3, bytegleich zur Arbeitskopie des Inhabers (139 Laufzeitdateien, Prüfsummen in [`sha256_07_Laufzeitdateien.txt`](00_Arbeitsvorbereitung/Analyse_2026-10-01/ergebnisse/sha256_07_Laufzeitdateien.txt)) |
| [`00_Arbeitsvorbereitung/`](00_Arbeitsvorbereitung/README.md) | Übergaben, Planung, Entscheidungen, Analyse vom 01.10.2026 |

Nicht enthalten: kanonischer Quellbaum `01_Repository/Glide` (`src/glide/app.pyw`, Tests, Verträge, Pflegewerkzeuge, CHANGELOG), macOS-Bundle, Grafik-Master. Siehe Entscheidung [E01](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md#e01--repository-und-git).

Namen: Die Hauptdatei heißt hier `Glide-Aufgaben-und-Listen_v3.32.3.pyw` (im Projekt `src/glide/app.pyw`), der Starter `Schnellstart.pyw` (im Projekt `glide_start.py`).

## Starten

```sh
cd 07_Python-Versionen
python3 Schnellstart.pyw      # empfohlen: Bytecode-Cache außerhalb des Ordners
```

- **Empfohlen:** Python 3.14 mit Tk 9; der python.org-Installer für macOS enthält ab 3.14.5 Tk 9.0.3.
- **Python 3.13 mit Tk 8.6:** startet ohne Systemmitteilungen und SVG-Vorschau.
- **Linux:** Distributions-Tk mit Xft verwenden (z. B. `python3-tk`); Bildvorschau dort nur PNG/GIF/SVG.
- **Zum Ausprobieren** eine getrennte Ablage verwenden: `GLIDE_DATA_DIR=/pfad/zum/testordner python3 Schnellstart.pyw`.
- Ältere Glide-Fassungen nie mit einem Format-20-Bestand starten (siehe [`07_Python-Versionen/README.md`](07_Python-Versionen/README.md)).

## Einstieg in Planung und Analyse

1. [Arbeitsvorbereitung – Index](00_Arbeitsvorbereitung/README.md): was gilt, wo was steht
2. [Entwicklungsplan ab 3.33](00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md)
3. [Entscheidungsvorlage E01–E10](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md)
4. [Bestandsaufnahme Code und Dokumentation](00_Arbeitsvorbereitung/Glide_Bestandsaufnahme_Code_und_Dokumentation_2026-10-01.md) · [Konkurrenz- und Featurematrix](00_Arbeitsvorbereitung/Glide_Konkurrenz_und_Featurematrix_2026-10-01.md) · [Produktprinzipien und UX-Prüfung](00_Arbeitsvorbereitung/Glide_Produktprinzipien_und_UX-Pruefung_2026-10-01.md)

Arbeitsregeln für Claude-Code-Sitzungen: [`CLAUDE.md`](CLAUDE.md).

## Lizenzen Dritter

- `07_Python-Versionen/vendor/tkinterdnd2`: MIT; tkdnd BSD-artig (siehe `vendor/provenance.json`).
- Schriften: DejaVu (eigene Lizenz) und Pixelify Sans (SIL OFL 1.1), siehe `resources/fonts/`.

Inhaberangaben und Lizenz von Glide selbst sind noch offen (Inhaberentscheidung).
