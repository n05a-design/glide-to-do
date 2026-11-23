# Portabler Designvertrag für Folgeprojekte der Glide Shell

Stand 23.11.2026 · Glide 1.0.2 · Glide Shell 0.6.2 · Lizenz MPL-2.0

Dieses Dokument definiert den verbindlichen, transportablen Gestaltungs- und Interaktionsvertrag für alle Anwendungen, die die **Glide Shell** als UI-Fundament einsetzen. Es ist offline-fähig und unabhängig vom Glide-Hauptrepository nutzbar.

---

## 1. Universelle Gestaltungsgrundsätze P1–P6

Jedes Projekt, das auf der Glide Shell aufbaut, wendet die sechs fundamentalen Gestaltungsprinzipien an:

| Grundsatz | Bedeutung für die Oberfläche | Konkrete Richtlinie |
|---|---|---|
| **P1 Funktioniert selbstverständlich** | Die naheliegende Handlung führt ohne Hinweistexte zum Ziel. Systemkonventionen (Hell/Dunkel, Escape zum Schließen, Tab zur Navigation, Standardkürzel) werden gewahrt. | Keine überflüssigen Erklärtexte für Standard-Aktionen. |
| **P2 Form folgt Funktion** | Farbe kennzeichnet Rolle, Größe drückt Wichtigkeit aus, Position zeigt Zusammengehörigkeit. Keine rein dekorativen Elemente im Standard. | Visuelle Hierarchie statt Schmuckelementen. |
| **P3 Keine Funktion doppelt** | Für jede Absicht existiert genau ein primärer interaktiver Weg. Menüleiste, Tastaturkürzel und Befehlsauswahl spiegeln denselben Weg. | Redundante Parallelsteuerungen vermeiden. |
| **P4 Kein Platz verschwenden** | Inhalt hat stets Vorrang vor der Bedienoberfläche. Feste Werkzeug- und Kopfleisten bleiben kompakt und einzeilig. | Maximale Nutzfläche für Arbeitsinhalte. |
| **P5 Nur das Wesentliche** | Der Standardzustand zeigt die für den aktuellen Kontext notwendigen Informationen. | Fortgeschrittene Aktionen nach Bedarf einblenden oder in Menüs führen. |
| **P6 Geringe Komplexität** | Stabile, verständliche Begriffe und logische visuelle Gruppen. | Wiedererkennbare Muster über alle Fenster hinweg. |

---

## 2. Verbindliche Einzelvorgaben für Oberflächen

### B15 – Bedienelemente schützen (Button-Schutz)
- **Regel:** Jeder interaktive Button und jedes Steuerelement muss in den vorgesehenen Fenstergrößen vollständig sichtbar, lesbar und erreichbar bleiben.
- **Konsequenz:** Texte, Hinweisfelder, Statusmeldungen oder Bilder dürfen Bedienflächen weder überdecken noch abschneiden. Reicht der Platz nicht aus, müssen Layout, Umbruch oder Scrollbereich dynamisch reagieren.
- **Mindestgröße:** Haupt- und Dialogfenster sind über `window_geometry.clamp` auf ergonomische Mindestmaße begrenzt.

### B11 – Informationshierarchie vor starrer Metadatenbreite
- **Regel:** Primäre Inhaltsinformationen (z. B. Titel, Arbeitsinhalte) haben stets Vorrang vor nachrangigen Metadaten (z. B. Zeitstempel, Tags, IDs).
- **Konsequenz:** Metadaten beanspruchen nur so viel Breite wie ihr tatsächlicher Inhalt. Bei Platzmangel weichen Metadaten oder werden ausgeblendet; primäre Titel werden mit `text_fit.clip` oder `text_fit.fit` ergonomisch gekürzt, nicht blind abgeschnitten.

### B01 / B16 – Unmittelbare Rückmeldung
- **Regel:** Jede Interaktion (Klick, Tastendruck, Scrollen) erfordert eine sofortige Rückmeldung im selben Tk-Ereigniszyklus.
- **Konsequenz:** Keine blockierenden Schlafzeiten (`time.sleep`) im UI-Thread. Längere Operationen entkoppeln oder asynchron ausführen.

### B03 – Ergonomische Bewegung & Übergänge
- **Regel:** Visuelle Übergänge (Animationen, Statuswechsel) dauern höchstens 150 ms und unterstützen das Begreifen der Zustandsänderung.
- **Konsequenz:** Übergänge sind über `motion.Transitions` jederzeit unterbrechbar (schnelles Wiederholen bricht Vorläufer sauber ab) und respektieren Benutzereinstellungen für reduzierte Bewegung.

### B10 / B12 / B14 – Semantische Symbole
- **Regel:** Symbole tragen eine eindeutige, feste Bedeutung (z. B. ◂/▸ zum Blättern, ▸/▾ zum Aufklappen).
- **Konsequenz:** Standard-Unicode-Symbole oder konsistente Systemglyphen verwenden. Keine mehrdeutigen oder rein dekorativen Piktogramme.

### Kontrast & Typografie (WCAG 2.2 AA)
- **Mindestkontrast:** Normaler Text muss ein Kontrastverhältnis von mindestens 4,5:1 zum Hintergrund aufweisen; große Schriften (ab 18 pt bzw. 14 pt fett) mindestens 3:1.
- **Farbunabhängigkeit:** Informationen dürfen nicht ausschließlich über Farbnuancen transportiert werden; stets Form, Text oder Symbole zur Verstärkung einsetzen.

### Fokus & Tastaturbedienbarkeit
- **Vollständigkeit:** Alle interaktiven Elemente müssen über die Tastatur (Tab, Shift+Tab, Pfeiltasten, Enter, Leertaste) bedienbar sein.
- **Sichtbarkeit:** Fokussierte Elemente zeigen einen deutlich wahrnehmbaren Fokusindikator.
- **Abbruch:** Modale Dialoge und temporäre Ansichten lassen sich jederzeit mit Escape schließen.

---

## 3. Technischer Schnittstellenvertrag der Shell

Die Glide Shell stellt neutrale Mechanismen bereit, die der Host mit seinen spezifischen Werten versorgt:

| Schnittstelle | Modul | Zweck & Nutzung durch den Host |
|---|---|---|
| `set_font_provider(fn)` | `custom_controls` | Registriert Host-Schriftauflösung `fn(size, *styles) -> tkFont`. |
| `set_ink_provider(fn)` | `custom_controls` | Registriert Host-Metrikrechner für genaue Textpositionierung und optische Mitte. |
| `set_backdrop_painter(fn)` | `custom_controls` | Registriert Zeichenfunktion für themenabhängige Hintergründe auf Canvas-Widgets. |
| `system_appearance.resolve` | `system_appearance` | Löst ein Farbwörterbuch `{"light": {...}, "dark": {...}}` systemkonform auf. |
| `primary_shortcuts` | `app_host` | Liefert plattformkonforme Kürzel (macOS Cmd vs. Windows/Linux Strg). |
| `bind_shortcuts` | `app_host` | Bindet eine Liste von Kürzeln an ein Fenster. |
| `install_close` | `app_host` | Richtet sauberes Fensterschließen und macOS-Quit-Handler ein. |
| `create_dialog` / `run_modal` | `modal_session` | Einheitliche, sichere Modalsitzungen mit Fokusspeicher und -rückgabe. |
| `Transitions` | `motion` | Verwaltete, unterbrechbare UI-Übergänge im Lebenszyklus eines Widgets (`AfterScope`). |
| `CommandHistory` | `command_history` | Universelle Undo/Redo-Verwaltung für Befehlsobjekte oder Zustandsschnappschüsse. |
| `clamp` / `format_geometry` | `window_geometry` | Begrenzt Fenstermaße auf Bildschirmgrenzen und Mindestgrößen. |

---

## 4. Gestaltungsfreiheit des Hosts (Produktspezifische Grenzen)

Folgende Bereiche gehören ausdrücklich zur **Domäne des Host-Projekts** und werden **nicht** aus Glide übernommen:
1. **Markenidentität:** Produktname, Logo, Anwendungs-Icon, Markenzeichen und produktspezifische Farbtöne (z. B. Glides Violett `#9E4AC8`).
2. **Maskottchen & spielerische Elemente:** Charaktere, Maskottchen (z. B. Gismo) oder themenfremde Illustrationen.
3. **Fachlayouts:** Spezifische Inhaltsanordnungen wie Kanban-Boards, Kachel-Dashboards, Notizeditoren oder Tabellenraster.
4. **Fachbegriffe & Lokalisierung:** Anwendungsfachsprache, Fachkataloge und Übersetzungen.
