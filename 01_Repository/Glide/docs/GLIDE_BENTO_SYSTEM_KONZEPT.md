# Glide Bento Box System – Architektur- und UI-Kompositionskonzept

Stand 24.11.2026 · Glide Bento Version 0.1.0 · Glide-System V1.87 · Glide Shell 0.6.2 · Format 26 · Entscheidung D100

Das **Glide Bento Box System** (Kurzbezeichnung: **Glide Bento**, Paketname: `glide_bento`) ist eine wiederverwendbare, modulare UI-Kompositionsschicht für kartenbasierte Benutzeroberflächen, Bento-Dashboards und adaptive Inhaltsraster in Python/Tkinter. Es bildet die architektonische **Ebene B** im Glide-Gesamtsystem.

---

## 1. Vision und Zielsetzung

Glide besitzt eine eigenständige Aufgaben- und Projektanwendung (Ebene A), ein dokumentarisches Systemregister (Ebene D) und ein wiederverwendbares Desktop-Fundament (Glide Shell, Ebene C).

Glide Bento schließt die Lücke zwischen generischen Shell-Widgets und konkreter Anwendungsfachlogik:
- **Systematisierung statt Redesign:** Bestehende Gestaltungswerte (`ui_design.py`, `RADII`, `SPACING`, `FONT_SIZES`) werden semantisch abstrahiert, ohne die vertraute visuelle Identität von Glide zu verändern.
- **Wiederverwendbarkeit:** Kartenanatomie, Header, Aktionsleisten, Metriken und responsive Raster stehen anwendungsneutral zur Verfügung und können in Folgeprojekten (z. B. STEPS, Chess & Chains) genutzt werden.
- **Freiheit von Fachlogik:** Das Bento-System kennt weder Aufgaben noch Notizen noch Gismo noch Datenbanken. Es rendert generische Inhalts- und Aktionsstrukturen, die vom Host bereitgestellt werden.
- **Deterministische Layout-Engine:** Ein Tk-freier Layout-Planner berechnet Spaltenanzahl, Breiten und Kartenplatzierung rein mathematisch vor der Widget-Erzeugung.
- **Volle Theme- und Provider-Unterstützung:** Farben, Schriften, Icons und Lokalisierung werden strikt über den Host-Kontext bezogen.

---

## 2. Das 4-Ebenen-Architekturmodell

```text
┌────────────────────────────────────────────────────────┐
│               Ebene A – Glide Application              │
│  (Aufgaben, Notizen, Gismo, Lokalisierung, Fachdaten)  │
└───────────┬────────────────────────────────┬───────────┘
            │                                │
            ▼                                ▼
┌───────────────────────────┐   ┌───────────────────────────┐
│ Ebene B – Glide Bento Box │   │ Ebene C – Glide Shell     │
│  (Karten, Grid, Tokens,   ├──►│  (Fenster, Lifetime,      │
│   Layout-Engine, Specs)   │   │   Modal, Custom Controls) │
└───────────────────────────┘   └─────────────┬─────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │   Tkinter / Standard-Bib  │
                                └───────────────────────────┘

┌────────────────────────────────────────────────────────┐
│ Ebene D – Glide-System (Register & Dokumentenrahmen)    │
└────────────────────────────────────────────────────────┘
```

### Verbindliche Abhängigkeitsregeln

1. **Glide Application (Ebene A)** darf `glide_bento` und `glide_shell` importieren.
2. **Glide Bento (Ebene B)** darf die öffentliche Schnittstelle von `glide_shell` nutzen (`custom_controls`, `window_lifetime`, `text_fit`).
3. **Glide Bento darf NIEMALS** Module der Glide Application importieren (weder `app.pyw` noch `home_tiles` noch `home_dashboard`).
4. **Glide Shell (Ebene C)** bleibt vollständig unabhängig von `glide_bento`.
5. **Keine zirkulären Abhängigkeiten**, keine globalen Singleton-Kopplungen, keine festen Produktfarben im neutralen Bento-Kern.

---

## 3. Paketstruktur (`src/glide/glide_bento`)

```text
01_Repository/Glide/src/glide/glide_bento/
├── __init__.py                # Öffentliche API und BENTO_VERSION = "0.1.0"
├── tokens.py                  # Semantische Design-Tokens und Skalen
├── context.py                 # BentoContext & Host-Provider (Theme, Fonts, Icons)
├── specs.py                   # BentoCardSpec, BentoGridSpec & Datenklassen
├── layout.py                  # Tk-freier deterministischer Layout-Planner
├── card.py                    # BentoCard, BentoHeader, BentoBody, BentoFooter
├── grid.py                    # BentoGrid (Multi-Column-Container mit Scrollsupport)
├── components.py              # BentoMetric, BentoActions, BentoEmptyState
├── demo.py                    # Eigenständiger Referenzhost (python -m glide_bento.demo)
├── selftest.py                # Autonomer Bento-Selbsttest
├── README.md                  # Dokumentation für Entwickler (Englisch)
├── README.de.md               # Dokumentation für Entwickler (Deutsch)
└── BENTO_DESIGN_CONTRACT.md   # Portabler Design- und Gestaltungsvertrag
```

---

## 4. Semantische Token-Architektur

Das Token-System übersetzt fundamentale Skalen in nachvollziehbare semantische Rollen:

| Token | Wert / Basis | Semantische Bedeutung |
|---|---|---|
| `layout.gap.default` | 12 px (`SPACING[12]`) | Standard-Abstand zwischen Bento-Karten |
| `layout.margin.default` | 16 px (`SPACING[16]`) | Randabstand des Rasters zum Fenster |
| `card.radius` | 18 px (`RADII["card"]`) | Eckenradius von Bento-Karten |
| `card.padding.x` | 18 px (`SPACING[18]`) | Horizontaler Innenabstand der Karte |
| `card.padding.y` | 15 px (`SPACING[15]`) | Vertikaler Innenabstand der Karte |
| `card.header.gap` | 8 px (`SPACING[8]`) | Abstand zwischen Header und Body |
| `card.min_width` | 300 px | Minimale lesbare Breite einer Kachel |
| `card.row_height.task`| 36 px (`ROW_HEIGHTS["task"]`) | Zeilenhöhe für kompakte Einträge |

Farben und Stile werden zur Laufzeit über den `BentoContext` aufgelöst. Unterstützt werden Standard-, Dark-, Kontrast- und Glass-Themes.

---

## 5. Responsive Layout-Engine

Die Layoutberechnung erfolgt zweistufig:

1. **BentoLayoutPlanner (Tk-frei):**
   - Berechnet anhand der verfügbaren Inhaltsbreite und `card.min_width` (300 px) zzgl. Lücken (16 px) die optimale Spaltenzahl (1 Spalte < 616 px, 2 Spalten ab 616 px, 3 Spalten ab 932 px).
   - Platziert Vollbreitenkarten im oberen Kopfbereich (`span="full"`).
   - Verteilt variable Karten über einen deterministischen Greedy-Algorithmus auf die jeweils vertikal kürzeste Spalte.
2. **BentoGrid (Tk-Renderer):**
   - Überträgt das berechnete Raster verlustfrei auf Tkinter-Frames.
   - Verhindert Resize-Oszillationen durch Entprellung und Schwellenstabilisierung.
   - Unterstützt sanftes vertikales Scrollen ohne verschachtelte Scrollkonflikte.

---

## 6. Pilotmigration: Glide Home

Die Startseite von Glide (`render_home` in `app.pyw`) wird schrittweise auf Bento-Karten umgestellt:
- Bestehende 20 Kacheldefinitionen in `home_tiles.py` bleiben unverändert erhalten.
- Der Adapter `TileUI` in `home_task_tiles.py` nutzt Bento-Kartenkomponenten.
- Die Kacheln „Heute“, „Woche“, „Gismo“, „Zeichnungen“, „Galerie“, „Angeheftet“ usw. behalten 100 % ihrer Funktionen, Interaktionen und Tooltips.
- Keine Datenformatmigration: Datenformat 26 und das Austauschformat 2 bleiben unverändert.

---

## 7. Qualitätssicherung und Nachweise

- **Import-Isolation:** Ein dedizierter Test prüft, dass `glide_bento` keine Glide-Fachmodule importiert und `glide_shell` unabhängig von `glide_bento` bleibt.
- **Tk-freie Unittests:** Layout-Berechnungen werden ohne grafische Anzeige mathematisch auf Determinismus getestet.
- **Echte Tk-Integrationstests:** Karten, Header, Aktionen, Resize und Theme-Wechsel werden unter realem Tk (unter Xvfb im CI-Lauf) getestet.
- **Referenzhost:** `python3 -B -m glide_bento.demo` demonstriert alle Komponenten ohne Glide-Import.
