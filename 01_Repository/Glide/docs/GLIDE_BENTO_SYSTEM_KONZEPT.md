# Glide Bento Box System – Architektur- und UI-Kompositionskonzept

Stand 24.11.2026 · Glide 1.0.2 · Glide Bento Version 0.1.0 · Glide-System V1.87 · Glide Shell 0.6.2 · Format 26 · Entscheidung D100

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

---

## 8. Vollständiger Bento-Komponentenkatalog (0.1.0 und geplanter Ausbau)

Der Komponentenbestand von `glide_bento` gliedert sich in deklarative Datenstrukturen, Layout-Engines, visuelle Kartenkomponenten und interaktive Hilfselemente:

| Komponente | Quelldatei | Zweck & Öffentliche API | Unterstützte Varianten & Zustände | Aktueller Einsatzort | Geplanter Ausbau (0.2.0+) |
|---|---|---|---|---|---|
| **`BentoCard`** | `card.py` | Universeller Karten-Container. API: `BentoCard(parent, spec, context)`. | Varianten: `standard`, `compact`, `featured`, `ghost`. Zustände: Normal, Hover, Focus, Selected. | Startseite `home_task_tiles.py` (Pilot). | Subtile Randverläufe, adaptive Schatten, Tastaturfokus-Ring. |
| **`BentoHeader`** | `card.py` | Kopfleiste für Karten mit Titel, Unterzeile, Symbol und Aktionen. API: `set_title()`, `add_action()`. | Varianten: `default`, `compact`, `minimal`. | Startseiten-Kacheln. | Integrierte Status-Badges, Tooltip-Anbindung. |
| **`BentoGrid`** | `grid.py` | Responsiver Raster-Container mit Canvas-Scrollsupport und dynamischem Spaltenumbruch. | Spalten: 1, 2 oder 3 Spalten basierend auf Breite. | Startseite `render_home`. | Multi-Span Rendering (`col_span=2`), ruckelfreies Resize. |
| **`BentoContext`** | `context.py` | Dependency-Injection-Behälter für Theme, Schriften, Icons und Lokalisierung. | Auflösung über Host-Provider oder neutrale Fallbacks. | Alle Bento-Widgets. | Dynamisches Event-Abonnement bei Theme-Wechsel ohne Neuaufbau. |
| **`BentoTokens`** | `tokens.py` | Semantische Design-Tokens für Abstände, Radien, Höhen und Typografie. | Immutable Dataclass mit Skalen. | `card.py`, `grid.py`, `components.py`. | Vollständiger Abgleich mit Host-Thementokens (Variante C). |
| **`BentoCardSpec`** | `specs.py` | Deklarative Spezifikation einer Karte (ID, Titel, Span, Gewicht, Inhalt). | `col_span` (1..3), `weight`, `priority`, `min_height`. | Kachel-Definitionen in `app.pyw`. | Deklarative Sichtbarkeitsregeln, Persistenzschlüssel. |
| **`BentoGridSpec`** | `specs.py` | Deklarative Rasterspezifikation (Lücken, Schwellenwerte, Randabstände). | Standard-Gaps: 12 px, Margin: 16 px, Breakpoints: 616/932 px. | `grid.py`. | Benutzerdefinierte Breakpoints je Host. |
| **`BentoLayoutPlan`**| `specs.py` | Unveränderlicher Berechnungsplan für die Kartenplatzierung. | Spaltenanzahl, Spaltenbreiten, Karten-zu-Spalte-Zuordnung. | Ausgabe von `BentoLayoutPlanner`. | Zeilen- und Spaltenkoordinaten für Multi-Span-Karten. |
| **`BentoLayoutPlanner`**| `layout.py` | Deterministischer, Tk-freier Layout-Rechner mit gieriger Spaltenverteilung. | Reine Berechnungslogik ohne Tkinter-Import. | `grid.py`, Unittests T341. | Echter 2-von-3-Spalten-Algorithmus mit Lückenminimierung. |
| **`BentoMetric`** | `components.py` | Darstellung prominenter Kennzahlen (Zahl, Einheit, Trend, Beschriftung). | Varianten: `large`, `medium`, `compact`. | Heute-Zusammenfassung auf Startseite. | Miniatur-Sparklines / Verlaufsbalken. |
| **`BentoActions`** | `components.py` | Einheitliche Aktionsleiste für sekundäre Kartenaktionen. | Anordnung: Horizontal rechtsbündig oder vertikal gestapelt. | Fußleisten komplexer Kacheln. | Dropdown-Menü-Unterstützung für Overflow-Aktionen. |
| **`BentoEmptyState`**| `components.py` | Visueller Leerzustand mit Illustration/Symbol, Titel, Text und Aktion. | Kompakt oder zentriert. | Leere Startseiten-Bereiche. | Universeller Einsatz in Fachmodulen (WA-52). |
| **`BentoDivider`** | `components.py` | Feine Trennlinie nach D83-Gestaltungsregeln. | Horizontal oder vertikal, 1 px Höhe. | Kachel-Gliederung. | Themenangepasste Randüberblendung. |
| **Bento Demo** | `demo.py` | Standalone-Referenzanwendung (`python -m glide_bento.demo`). | Demonstriert alle Komponenten ohne Glide-Import. | Manuelle Sichtprüfung und Verifikation. | Interaktive Regler für Schwellenwerte und DPI-Skalierung. |
| **Bento Selftest** | `selftest.py` | Autonomer 13-Punkte-Selbsttest (`python -m glide_bento.selftest`). | Prüft Importe, Layoutdeterminismus, Tokens und Widgets. | CI-Grundstufe und Paketbau. | Erweiterung auf 15 Checks (Multi-Span- und Tokenverträge). |

---

## 9. Token-Reconciliation: Variantenvergleich und Architekturentscheidung

Zwischen dem Host-Gestaltungsmodul `src/glide/ui_design.py` und dem Bento-Token-Modul `src/glide/glide_bento/tokens.py` existieren derzeit parallele Skalen für Abstände (`SPACING`), Radien (`RADII`), Schriftgrößen und Zeilenhöhen. Um Doppelpflege und Brüche zu vermeiden, wurden drei Architekturvarianten untersucht:

### 9.1 Die drei Varianten im Vergleich

- **Variante A: Foundation-Tokens in die Framework Shell auslagern (`glide_shell.tokens`)**
  - *Konzept:* Die Framework Shell definiert neutrale Basisskalen. Glide und Bento importieren diese.
  - *Bewertung:* Widerspricht dem Shell-Prinzip (D86, D94–D99): Die Shell soll rein funktionale Desktop-Mechanismen (Fenster, Modal, Lifetime) bereitstellen und keine starren Designvorgaben machen. Verschiedene Hosts (z. B. Glide vs. Chess) benötigen unterschiedliche Grundästhetiken.
- **Variante B: Eigenständiges Token-Paket (`glide_tokens`)**
  - *Konzept:* Ein fünftes separates Mini-Paket nur für Design-Tokens.
  - *Bewertung:* Unnötiger administrativer Aufwand; erzeugt Fragmentierung, zusätzliche Importpfade und erhöht den Pflegeaufwand bei jedem Versionswechsel unverhältnismäßig.
- **Variante C: Expliziter Host-Context-Token-Vertrag (Empfohlen für Bento 0.2.0)**
  - *Konzept:* `glide_bento` definiert rein semantische Tokens (`BentoTokens`) mit neutralen Standardwerten für Standalone-Demos und Fremdhosts. Beim Start injiziert der konkrete Host (Glide über `ui_design.py`) seine aktiven Werte in den `BentoContext`.
  - *Vorteile:*
    1. **100 % Entkopplung:** Bento bleibt völlig frei von Glide-Code.
    2. **Keine Doppelpflege:** Glide pflegt seine Master-Skalen zentral in `ui_design.py`.
    3. **Portabilität:** Folgeprojekte (STEPS, Chess) übergeben einfach ihre eigenen Tokens.
    4. **Sicherheit:** Fehlt die Host-Injektion, greifen robuste neutrale Fallbacks.

### 9.2 Entscheidungsmatrix

| Kriterium | Variante A (Shell) | Variante B (Eigenes Paket) | Variante C (Host-Injection) |
|---|---|---|---|
| **Abhängigkeitsrichtung** | ✕ Shell wird mit UI-Design belastet | ◐ Erzeugt neues Modul | ✅ Perfekt: Host → Context → Bento |
| **Portabilität für Fremdhosts** | ◐ Bindet Fremdhosts an Shell-Tokens | ◐ Zusätzliche Abhängigkeit | ✅ Jeder Host liefert eigene Tokens |
| **Migrationsaufwand** | Hoch (Umbau von Shell und Host) | Hoch (Neues Paket) | **Niedrig (Adapter in `BentoContext`)** |
| **Vermeidung von Doppelpflege** | ✅ Zentral in Shell | ✅ Zentral im Paket | ✅ Zentral im jeweiligen Host |
| **Shell-Unabhängigkeit** | ✕ Verletzt D94/D99-Entkopplung | ✅ Shell bleibt frei | ✅ Shell bleibt frei |
| **Wartbarkeit & Testbarkeit** | Moderat | Aufwendig | **Hervorragend (Unit-Tests via Mock-Context)** |

**Architekturempfehlung:** Umsetzung von **Variante C** im Übergabepaket 1 für Bento 0.2.0.

---

## 10. Multi-Span Layout-Algorithmus (Spezifikation für Bento 0.2.0)

In Bento 0.1.0 unterstützen Karten entweder eine einzelne Spalte (`col_span=1`) oder die volle Breite über alle verfügbaren Spalten (`span="full"`). Bento 0.2.0 führt echte Mehrspaltenkarten ein (`col_span=2` im 3-Spalten-Raster).

### 10.1 Trennung von visueller Variante und Spaltenbelegung

Um semantische Klarheit zu gewährleisten, werden Layout-Geometrie und visuelle Darstellung strikt entkoppelt:

1. **`col_span` (Layout-Geometrie):** Gibt an, wie viele Spalten die Karte im aktuellen Spaltenraster belegt (`1`, `2`, oder `3`).
2. **`variant` (Visuelle Stilistik):** Bestimmt Rahmen, Polsterung und Hintergrund (`standard`, `compact`, `featured`, `ghost`).
3. **`priority` (Informationsdichte):** Steuert das Verhalten bei Platzmangel (`high`, `normal`, `low`).

### 10.2 Reflow-Regeln bei variabler Fensterbreite

Der `BentoLayoutPlanner` wendet folgende deterministische Reflow-Regeln an:

```text
3-Spalten-Raster (Breite >= 932 px):
┌───────────────────────┬───────────────────────┬───────────────────────┐
│     Karte A (span=2)                          │     Karte B (span=1)  │
├───────────────────────┼───────────────────────┼───────────────────────┤
│     Karte C (span=1)  │     Karte D (span=1)  │     Karte E (span=1)  │
└───────────────────────┴───────────────────────┴───────────────────────┘

2-Spalten-Raster (616 px <= Breite < 932 px):
┌───────────────────────────────────────────────┬───────────────────────┐
│     Karte A (span=2 -> belegt volle 2 Spalten)                        │
├───────────────────────────────────────────────┬───────────────────────┤
│     Karte B (span=1)                          │     Karte C (span=1)  │
├───────────────────────────────────────────────┼───────────────────────┤
│     Karte D (span=1)                          │     Karte E (span=1)  │
└───────────────────────────────────────────────┴───────────────────────┘

1-Spalten-Raster (Breite < 616 px):
┌───────────────────────────────────────────────────────────────────────┐
│     Karte A (span=1, volle Fensterbreite)                             │
├───────────────────────────────────────────────────────────────────────┤
│     Karte B (span=1, volle Fensterbreite)                             │
├───────────────────────────────────────────────────────────────────────┤
│     Karte C (span=1, volle Fensterbreite)                             │
└───────────────────────────────────────────────────────────────────────┘
```

### 10.3 Platzierungs- und Antikollisions-Algorithmus

1. **Zeilen-Tracking:** Der Planner führt ein Belegungs-Array für jede Spalte mit aktuellem Höhenstand (`column_heights = [0, 0, 0]`).
2. **Span-Prüfung:** 
   - `col_span=1`: Wird in die Spalte mit der minimalen Höhe gesetzt (`min(column_heights)`).
   - `col_span=2` (im 3-Spalten-Raster): Prüft die beiden möglichen Spaltenpaare (Spalte 0+1 vs. Spalte 1+2). Wählt das Paar, dessen maximale Höhe geringer ist. Beide Spalten werden auf `max(h_a, h_b) + card_height` angeglichen.
   - `col_span=3` oder `span="full"`: Wird über alle Spalten gelegt; alle Spalten werden auf `max(column_heights) + card_height` gesetzt.
3. **Widget-Retention:** Bei Neuberechnung durch Fenster-Resize werden bestehende Tk-Karten-Instanzen wiederverwendet und lediglich per `grid(row=..., column=..., columnspan=...)` neu positioniert. Kein Flackern, kein Zerstören des internen Widget-Zustands.
4. **Fokus-Erhalt:** Der aktive Tastaturfokus bleibt während des Spaltenumbruchs auf dem fokussierten Element erhalten.

---

## 11. Theme-, Font- und Icon-Fallbacks

`glide_bento` stellt sicher, dass Komponenten sowohl in einer vollwertigen Desktop-App als auch in isolierten Testumgebungen oder fremden Hosts fehlerfrei rendern:

- **Farben:** `BentoContext.colors` löst semantische Rollen (`bg_card`, `fg_primary`, `border_subtle`, `accent`) auf. Ist kein Host-Theme registriert, greift eine barrierefreie, neutrale Palette (WCAG AA konform).
- **Typografie:** Primärfont wird über `context.resolve_font(size, weight)` angefordert. Kann der Host keine Schriften liefern, fällt Bento robust auf Tk-Standardfonts (`TkDefaultFont`, `Helvetica`, `Arial`) zurück.
- **Icons:** Bento verwendet ausschließlich textuelle Unicode-Symbole oder vom Host bereitgestellte Canvas-Zeichenroutinen. Keine externen Bilddateien im Bento-Kern.

---

## 12. Gewichtete Platzierung vs. Masonry-Engine

Der `BentoLayoutPlanner` arbeitet mit einem **deterministischen gewichteten Slot-Modell**:
- Jede Karte deklariert ein relatives Inhaltsgewicht (`weight: int`, z. B. 1 für Einzeiler, 3 für Aufgabenlisten).
- Dies ermöglicht eine rein mathematische Verteilung ohne vorheriges Zeichnen der Widgets.
- **Abgrenzung zu dynamischem Masonry:** Eine echte Masonry-Engine misst die Pixelhöhe erst nach dem Rendern auf dem Bildschirm. Dies führt in Tkinter oft zu zwei aufeinanderfolgenden Geometrie-Events (Flimmern / Flackern beim Resize). Glides deterministisches Vorab-Gewichtsmodell vermeidet Resize-Oszillationen vollständig.

---

## 13. Strategische Bento-Versionsroadmap (0.1.0 bis 1.0.0)

```mermaid
flowchart TD
    V01["<b>Bento 0.1.0 (Foundation)</b><br/>Status: Auf main (V1.87)<br/>Kartenanatomie, 1-3 Spalten, Pilot Startseite"] --> V02["<b>Bento 0.2.0 (Consistency)</b><br/>Status: Spezifiziert (Phase 1)<br/>Multi-Span (col_span=2), Host-Context-Tokens"]
    V02 --> V03["<b>Bento 0.3.0 (Dashboards)</b><br/>Status: Geplant (Phase 2)<br/>Projekt-Dashboard L1, Personal Insights L2"]
    V03 --> V04["<b>Bento 0.4.0 (Custom Layouts)</b><br/>Status: Konzeptionell (Phase 4)<br/>Karten verschieben/ausblenden, Presets L3"]
    V04 --> V10["<b>Bento 1.0.0 (Stable Contract)</b><br/>Status: Zielzustand<br/>Garantierte API-Stabilität, Multi-Host-Einsatz"]
```

- **Bento 0.1.0 – Foundation (Aktueller Stand auf `main`, V1.87):**
  - Universelle Kartenanatomie (`BentoCard`, `BentoHeader`, `BentoMetric`, `BentoActions`).
  - Responsiver Container `BentoGrid` mit Schwellen bei 616 px und 932 px.
  - Pilotmigration der Glide-Startseite unter Beibehaltung aller 20 Kachelinhalte.
  - Autonomer Selbsttest (13 Checks) und Referenzdemo (`demo.py`).
- **Bento 0.2.0 – Composition & Consistency (Phase 1):**
  - Echtes 2-von-3-Spalten Multi-Span Layout (`col_span=2`).
  - Token-Harmonisierung über Host-Context-Injection (Variante C).
  - Dynamische Tastaturfokus-Führung über Kartenränder hinweg.
  - Erweiterte Komponenten-Galerie in der Standalone-Demo.
- **Bento 0.3.0 – Reusable Dashboards (Phase 2):**
  - Einsatz des Bento-Systems für das neue Projekt-Dashboard (Feature L1).
  - Standard-Karten für Meilensteine, Fortschritt und verknüpfte Notizen.
  - Integration von Personal Insights (Feature L2).
  - Übernahme-Test im Schwesterprojekt STEPS.
- **Bento 0.4.0 – Custom Layouts & Personalization (Phase 4):**
  - Nutzer können Kacheln auf dem Dashboard per Drag-and-drop anordnen.
  - Kacheln temporär ausblenden oder minimieren.
  - Persistierung des benutzerdefinierten Layouts in den Einstellungen.
  - Ein-Klick-Rücksetzung auf das empfohlene Standard-Raster.
- **Bento 1.0.0 – Stable Component Contract:**
  - Dauerhaft eingefrorene öffentliche API mit semantischer Versionierung.
  - Vollständige Unabhängigkeit von Tk-Versionen (Tk 8.6 und Tk 9.0+ kompatibel).
  - Voll dokumentierter Übernahmeleitfaden für externe Python/Tk-Anwendungen.

---

## 14. Projektübergreifende Übernahmestrategie (STEPS, Chess & Chains)

Glide Bento ist so konzipiert, dass es wie die Glide Shell als eigenständiges Unterpaket in Schwesterprojekte übernommen werden kann:

1. **Übernahmewerkzeug:** Ähnlich wie `shell_uebernehmen.py` wird ein Übernahmeskript `bento_uebernehmen.py` bereitgestellt, das den Stand von `src/glide/glide_bento` als isoliertes Paket kopiert.
2. **Keine Code-Änderungen im Folgeprojekt:** Das übernehmende Projekt ändert niemals Bento-Dateien von Hand, sondern steuert Darstellung und Inhalte ausschließlich über `BentoCardSpec`, `BentoGridSpec` und den `BentoContext`.
3. **Einsatz in STEPS:** STEPS nutzt Bento zur Darstellung von Schrittfolgen, Zielmetriken und Etappendashboards.
4. **Einsatz in Chess & Chains:** Nutzt Bento für Spielanalysen, Zugstatistiken und Notationstafeln.
