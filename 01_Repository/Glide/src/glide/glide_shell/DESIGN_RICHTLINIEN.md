# Portabler Designvertrag für Folgeprojekte der Glide Shell

Stand 28.11.2026 · Glide 1.0.3 · Glide Shell 0.10.0 · Lizenz MPL-2.0

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
| `require_shell` / `compatible` | `compat` | Verbraucher (Bento, Hosts) prüfen beim Import ihre Shell-Mindestversion (seit 0.7.0). |
| `check_project` | `conformance` | Prüft Schichten, öffentliche Module, Zyklen und Versionen eines Hosts (seit 0.7.0). |
| `misspelled` / `LayeredChecker` | `spellcheck` | Rechtschreibvertrag: Host liefert Engine und Wörterbuch, markiert Befunde mit eigener Farbe (seit 0.8.0). |
| `ShowcaseRegistry` / `shell_entries` | `showcase` | Galerie-Register: jede allgemeine Komponente mit Builder, Zuständen und Einsatzort (seit 0.7.0). |
| `ThemeProvider` / `validate` / `with_accent` | `color_roles` | Farbrollen (14 Kernrollen im Glide-Vokabular), neutrale Hell-/Dunkelthemen, eigene Markenfarbe, WCAG-2.2-AA-Prüfung, Benachrichtigung bei Themenwechsel (seit 0.10.0). |
| `SettingsRegistry` / `shell_settings` | `settings_registry` | Einstellungen beschreiben, prüfen, gruppieren; Speicherformat bleibt beim Host (seit 0.10.0). |
| `ShellButton` / `SearchField` / `Tooltip` / `Toolbar` | `controls` | Allgemeine Knöpfe (feste Größen 28/34/42 px, sichtbarer Fokus), Suchfeld, Tooltip, gruppierte Werkzeugleiste mit Umbruch (seit 0.10.0). |
| `WorkspaceHost` / `Workspace` | `workspaces` | Arbeitsbereiche des Hosts mit Navigation, Statuszeile, Kürzeln und Abbau; kein Datenmodell (seit 0.10.0). |
| `add_shutdown` / `shutdown` | `app_host` | Geordnetes Beenden: Aufräumschritte rückwärts, danach Zeitgeber und Fenster (seit 0.10.0). |

---

## 4. Gestaltungsfreiheit des Hosts (Produktspezifische Grenzen)

Folgende Bereiche gehören ausdrücklich zur **Domäne des Host-Projekts** und werden **nicht** aus Glide übernommen:
1. **Markenidentität:** Produktname, Logo, Anwendungs-Icon, Markenzeichen und produktspezifische Farbtöne (z. B. Glides Violett `#9E4AC8`).
2. **Maskottchen & spielerische Elemente:** Charaktere, Maskottchen (z. B. Gismo) oder themenfremde Illustrationen.
3. **Fachlayouts:** Spezifische Inhaltsanordnungen wie Kanban-Boards, Kachel-Dashboards, Notizeditoren oder Tabellenraster.
4. **Fachbegriffe & Lokalisierung:** Anwendungsfachsprache, Fachkataloge und Übersetzungen.

---

## 5. Shell-First-Vertrag (D105, D106)

Die Glide Shell ist das verbindliche technische und gestalterische Fundament jeder Anwendung, die auf ihr aufbaut (Glide, STEPS, Chess & Chains und künftige Desktopanwendungen). Die Fachanwendung entsteht in dieser Architektur; ein eigenes allgemeines UI-System daneben ist nicht vorgesehen.

### 5.1 Abhängigkeiten

| Richtung | Zulässig | Prüfung |
|---|---|---|
| Fachanwendung → Glide Shell | nur öffentliche Module aus `glide_shell.__all__` | `python -m glide_shell.conformance <Quellordner>` (Regel `public-api`) |
| Fachanwendung → Glide Bento | öffentliche Exporte aus `glide_bento.__all__` | Import, Selbsttest |
| Glide Bento → Glide Shell | öffentliche Shell-Module; `SHELL_MIN_VERSION` muss passen | Regeln `bento-imports`, `versions`; Abbruch mit `ShellVersionError` beim Import |
| Glide Shell → Standardbibliothek, `tkinter` | ja | Regel `shell-imports` |
| Shell → Bento oder Fachlogik, Bento → Fachlogik, Zyklen | **nie** | Regeln `shell-imports`, `bento-imports`, `cycles` |

Ein natives Tk-Widget in der Fachanwendung ist kein Verstoß. Entscheidend ist, ob es allgemeine Framework-Arbeit leistet, also in die Shell oder nach Bento gehört, oder fachspezifisch ist.

### 5.2 Entscheidungsreihenfolge für Entwicklungsagenten

1. Verbindliche Anforderung des Nutzers bzw. Inhabers.
2. Aktuelle Architekturentscheidungen des Projekts.
3. Shell- und Bento-Verträge (dieses Dokument, [Bento-Designvertrag](../glide_bento/BENTO_DESIGN_CONTRACT.md), Anleitungen im Paket).
4. Gemeinsames Designsystem: P1–P6, Abschnitte 2 und 3 dieses Dokuments.
5. Vorhandene Komponenten: Bausteintabelle im [README](README.de.md), Galerie-Register `glide_shell.showcase` und `glide_bento.showcase`.
6. Fachspezifische Projektregeln.
7. Begründete projektspezifische Ausnahme nach 5.5.
8. Neuentwicklung nur bei tatsächlichem Bedarf, und zuerst als allgemeine Framework-Erweiterung, wenn mehrere Anwendungen sie brauchen.

Fragen wie „Wie sieht ein Knopf aus?“, „Wie baue ich einen Dialog?“, „Wie reagiert eine Komponente auf die Themenfarbe?“ oder „Wie starte ich die Anwendung?“ beantwortet zuerst dieser Vertrag mit den Shell-Bausteinen. Ein eigener allgemeiner Entwurf ist nicht der Standard.

### 5.3 Gemeinsame Grundsätze

| Grundsatz | Bedeutung | Bestehende Regel |
|---|---|---|
| Shell First | Das Framework ist der Ausgangspunkt jeder allgemeinen Lösung | D86, D95, D105 |
| Glide as Showcase | Jede freigegebene allgemeine Komponente ist in Glide erreichbar und vorführbar | D105, Galerie in Glide |
| Reuse Before Creation | Vor jeder neuen Komponente prüfen, ob ein Baustein existiert | P3, Abschnitt 5.2 |
| Visual Consistency | Vergleichbare Komponenten haben gleiche Maße, Zustände und Interaktionen | P2, B10/B12/B14 |
| Pixel Precision | Abweichungen in Geometrie und Flucht werden an der Ursache behoben | B02, B05, B07–B09 |
| Direct Interaction | Arbeit beginnt unmittelbar, etwa mit direkter Eingabe in der Liste | P1, D105 |
| Feature Discoverability | Kernfunktionen sind sichtbar und verständlich erreichbar | P1, P5, B06 |
| Contextual Tools | Werkzeuge stehen gruppiert dort, wo sie wirken | P4, D61 |
| Predictable Drag & Drop | Die Ablagestelle ist vor der Mutation sichtbar | B01/B16 |
| Multiple Views, One Data Model | Ansichten teilen Objekte und Identitäten | P3, P6 |
| User-Controlled Workspace | Nutzer bestimmen Organisation, Sichtbarkeit und Navigation | P5 |
| Data Safety First | Integrität und Wiederherstellbarkeit haben Vorrang | D105 |
| Functional Completion | Fertig heißt erreichbar, nutzbar und geprüft | D105 |
| Versioned Evolution | Weiterentwickelte Bausteine erhalten eine neue Version | D104 |

### 5.4 Individualisierung

Über Schnittstellen und Werte des Hosts frei wählbar: Anwendungsname, Logo, App-Icon, Markenfarbe, fachliche Inhalte, Arbeitsbereiche, Visualisierungen und Navigationsinhalte (Abschnitt 4). Farben kommen als Rollenwörterbuch, Schriften über `set_font_provider`, Bento-Werte über `BentoContext.for_host`. Ändert sich die Themenfarbe, baut der Host mit dem neuen Rollenwörterbuch neu auf oder ruft `refresh_from_host`/`update_theme`; eine Komponente liest Farben nie aus eigenen Konstanten.

### 5.5 Ausnahmen

Eine Abweichung vom gemeinsamen Standard braucht einen Eintrag im Projekt mit: betroffenem Bereich, konkreter Anforderung, Begründung, geprüften vorhandenen Alternativen, technischen und Wartungsfolgen, Geltungsbereich und Prüfstatus. Profitieren mehrere Anwendungen davon, wird daraus eine Framework-Erweiterung statt einer Ausnahme.

### 5.6 Noch nicht in der Shell

Seit 0.10.0 (E02) liegen allgemeine Knöpfe, Suchfelder, Tooltips, Werkzeugleisten, der Theme-Provider (`color_roles`), ein Einstellungsregister und Arbeitsbereiche in der Shell (Abschnitt 3). Folgeprojekte nutzen diese statt eigener allgemeiner Fassungen. Glide selbst setzt bislang nur `SearchField` produktiv ein; seine älteren eigenen Knöpfe und Leisten bleiben bis zu einer gezielten Ablösung bestehen und sind kein Vorbild für Folgeprojekte.

Noch nicht in der Shell: Tabellen und Listen mit Sortierung und Filter, segmentierte Auswahl, Inline-Eingabe, aufklappbare Abschnitte, Fortschritts-, Datei- und Einstellungsdialoge als fertige Bausteine. Bedarf meldet ein Folgeprojekt über den Rückmeldevertrag (Entwicklungsplan §4.8.2); eine eigene allgemeine Komponente baut es dafür nicht.

### Aktionsgriff und Ablageanzeige (Shell 0.9.0)

`ActionHandle` nimmt die Glyphe, Farbrollen, Schrift und Innenabstände vom Host entgegen. Klick, Tastatur und Ziehen haben klar abgegrenzte Aufgaben. Nur wenn der Host eine Bewegung anbietet, erhält der Griff Drag-Bindungen. Leseränder in Texteditoren und der kompakte Griff vor der Aufgaben-Checkbox werden vom Host bemessen. **Griffachse:** Innerhalb einer Liste stehen alle Zeilengriffe einer Ansicht bündig auf einer senkrechten Achse. Der Host erzeugt sie über genau eine Griff-Fabrik (gleiche Breite, Schrift und Zeichnung) und richtet sie an der Listenkante aus, nicht an Zellkanten; Text und Markierung folgen dem gemessenen Textbeginn der Zeile. Vorbild ist Glide (`make_row_grip`, T360).

`DropIndicator` zeichnet über dem vorhandenen Ziel und belegt keinen Platz im Layout. Vor und nach einer Zeile steht eine horizontale Linie, im Zielcontainer und bei einem ungültigen Ziel eine Seitenmarkierung. Der Host liefert Zielrechteck, Einrückung, Themenfarbe und Gültigkeit.

Vergleichbare Symbolknöpfe erhalten feste quadratische Außenmaße und sichtbaren Tastaturfokus. `symbol_ink_offset` berechnet den Versatz aus Glyphenbegrenzung, Vorschub und Zeilenmetriken. Die App liefert die tatsächliche Schrift und ihre Skalierung.
