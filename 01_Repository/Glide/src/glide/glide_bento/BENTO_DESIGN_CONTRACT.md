# Bento Design Contract – Portabler Gestaltungsvertrag

Stand 26.11.2026 · Glide 1.0.3 · Bento Version 0.2.0 · Glide-System V1.88 · Entscheidung D100

Dieser Gestaltungsvertrag definiert die verbindlichen visuellen und interaktiven Standards für alle Bento-Komponenten (`glide_bento`). Er gilt gleichermaßen für Glide als Host sowie für jedes Folgeprojekt, das Bento übernimmt.

---

## 1. Gestaltungsleitsätze (P1–P6)

1. **P1 – Funktioniert selbstverständlich:** Vorhersagbare Ausrichtung, stabiler Tastaturfokus und deterministische Platzierung.
2. **P2 – Form folgt Funktion:** Karten dienen der Gliederung relevanter Inhalte; keine rein dekorativen Rahmen oder künstlichen Freiflächen.
3. **P3 – Keine Funktion doppelt:** Header-Aktionen, Kontextmenüs und Inhaltsknöpfe haben eindeutige, sich nicht überschneidende Aufgaben.
4. **P4 – Kein Platz verschwenden:** Ruhige, aber informationsdichte Flächen; leere Footer oder Header verbrauchen 0 px zusätzlichen Raum.
5. **P5 – Nur das Wesentliche:** Titel sind auf maximal 40 Zeichen begrenzt; Metadaten ordnen sich visuell dem Hauptinhalt unter.
6. **P6 – Geringe Komplexität:** Einfache, typisierte Datenklassen und klare Provider-Schnittstellen statt verschachtelter Widget-Hierarchien.

---

## 2. Kartenanatomie

Jede Bento-Karte (`BentoCard`) folgt einer dreiteiligen Grundstruktur:

```text
┌────────────────────────────────────────────────────────┐  ◄── card.radius (18 px), border_width (1 px)
│  [Icon]  Kartentitel               [Aktion / Status]   │  ◄── BentoHeader
│  Optionaler Untertitel                                 │
├────────────────────────────────────────────────────────┤  ◄── header_gap (8 px)
│                                                        │
│  Primärer Inhaltsbereich (BentoBody)                   │  ◄── padding_x (18 px), padding_y (15 px)
│  - Text, Kennzahlen (BentoMetric), Listen              │
│  - Aktionsreihen (BentoActions)                        │
│  - Eingebettete Host-Widgets                           │
│                                                        │
├────────────────────────────────────────────────────────┤  ◄── footer_gap (8 px)
│  Zusatzinformation / Sekundäraktion                    │  ◄── BentoFooter (optional)
└────────────────────────────────────────────────────────┘
```

### Regeln zur Anatomie:
- **Fluchten:** Header-Icons und Titel liegen auf einer gemeinsamen horizontalen Grundlinie.
- **Header-Aktionen:** Knöpfe im Header stehen rechtsbündig (`side="right"`) und haben eine Höhe von 28–32 px.
- **Buttonschutz (B15):** Interaktive Elemente dürfen bei Breitenänderungen niemals abgeschnitten oder überdeckt werden. Bei Platzmangel umbrechen Aktionen oder ordnen sich vertikal an.
- **Informationshierarchie (B11):** Primärinhalt (Body) ist visuell dominant. Sekundäre Texte nutzen `text_muted` und Schriftgröße 9–10 pt.

---

## 3. Semantische Token-Skalen

Bento-Komponenten verwenden ausschließlich semantische Tokens aus `glide_bento.tokens`:

| Kategorie | Token-Name | Standardwert | Zweck |
|---|---|---|---|
| **Abstände** | `gap_compact` | 8 px | Kompakter Komponentenabstand |
| | `gap_default` | 12 px | Standardabstand zwischen Karten (`HOME_CARD_GAP`) |
| | `gap_relaxed` | 16 px | Spaltenabstand im Raster (`HOME_TILE_GAP`) |
| | `grid_margin` | 16 px | Außenabstand des BentoGrid |
| **Innenabstand** | `card_padding_x` | 18 px | Horizontaler Innenabstand (`HOME_CARD_PAD_X`) |
| | `card_padding_y` | 15 px | Vertikaler Innenabstand (`HOME_CARD_PAD_Y`) |
| | `header_gap` | 8 px | Abstand zwischen Header und Body |
| | `footer_gap` | 8 px | Abstand zwischen Body und Footer |
| **Radien** | `card_radius` | 18 px | Eckenrundung von Bento-Karten |
| | `field_radius` | 16 px | Eckenrundung von Eingabefeldern |
| | `badge_radius` | 8 px | Eckenrundung von Markern und Kennzahlen |
| **Schriftgrößen** | `font_size_caption` | 9 pt | Metadaten, Quellen, kleine Zähler |
| | `font_size_small` | 10 pt | Kompakte Zeilen, Tabellenwerte |
| | `font_size_body` | 12 pt | Fließtext und primäre Aufgaben |
| | `font_size_subtitle`| 13 pt | Kartentitel im Standard-Header |
| | `font_size_title` | 16 pt | Abschnittsüberschriften |
| | `font_size_headline`| 22 pt | Hervorgehobene Kennzahlen |

---

## 4. Responsive Raster- und Spaltenregeln

Das Bento-Raster berechnet die Spaltenanzahl dynamisch aus der tatsächlich verfügbaren Inhaltsbreite:

$$\text{Spalten} = \begin{cases} 
1 & \text{für } \text{Breite} < 616\text{ px} \\
2 & \text{für } 616\text{ px} \le \text{Breite} < 932\text{ px} \\
3 & \text{für } \text{Breite} \ge 932\text{ px}
\end{cases}$$

- **Mindestkartenbreite:** Jede Standardkarte hat eine garantierte Mindestbreite von 300 px (`HOME_TILE_MIN_WIDTH`).
- **Greedy-Spaltenverteilung:** Karten mit normaler Breite werden deterministisch in die Spalte mit dem aktuell geringsten kumulierten Gewicht eingefügt. Dies verhindert einseitige Leerspalten neben hohen Karten.
- **Karten voller Breite:** Karten mit `span="full"` oder Variante `full_width` sitzen oberhalb des mehrspaltigen Rasters über die gesamte Inhaltsbreite.

---

## 5. Tastaturbedienung und Barrierefreiheit

- **Tastatur-Navigation:** 
  - Nur interaktive Karten oder Karten mit Fokus-Steuerelementen erhalten einen Tab-Stopp (`takefocus=True`). Rein informative Textkarten überspringen den Tab-Fokus.
  - Mit `Tab` und `Shift+Tab` wird zwischen interaktiven Elementen navigiert.
  - `Enter` und `Leertaste` lösen fokussierte Kartenaktionen aus.
- **Fokusring:** Ein fokussiertes Element zeigt einen deutlichen Fokusring mit 2 px Stärke (`focus_width`) in der Kontrastfarbe `theme["focus"]`.
- **Kontraste (WCAG 2.1 AA):**
  - Text zu Hintergrund: Mindestens 4,5:1 für Standardtext (12 pt), mindestens 3:1 für Überschriften (ab 16 pt fett).
  - UI-Bedienelemente und Rahmen zu Hintergrund: Mindestens 3:1.
  - Informationen werden niemals ausschließlich durch Farbe kodiert (immer Symbol oder Textbeistellung).

---

## 6. Host-Grenzen & Wiederverwendbarkeit

- `glide_bento` enthält **keine fest codierten Farbcodes** (#hex) in den Komponenten.
- Sämtliche Farben stammen aus `context.resolve_color(role)`.
- Texte, Icons und Tooltips werden vollständig vom Host übergeben.
- Keine Abhängigkeit von `ListApp`, SQLite, Persistenzformaten oder Anwendungsdaten.
