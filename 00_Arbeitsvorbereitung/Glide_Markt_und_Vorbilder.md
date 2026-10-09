# Glide – Markt und Vorbilder

Stand 09.10.2026 · Glide 3.35.0 · Hersteller-Matrix vom 01.10.2026, gezielte Abgleiche 05./07.10.2026, Sprintrecherche 08.10.2026; Glide-Codeabgleich 08.10.2026

Zusammengeführt am 03.10.2026 aus der Konkurrenz- und Featurematrix und der Konkurrenzübersicht vom 01.10.2026; diese hatten die älteren Recherchen vom 16.–25.09.2026, den Funktionsvergleich zur Zeichenfläche, die SVG-Untersuchung und das Konzept „Seiten wie Notion“ bereits eingeordnet. Am 06.10.2026 um die Wettbewerbsteile des nicht übernommenen Richtungsentwurfs vom 03.10.2026 ergänzt: Belegstufen, Steckbriefe mit Stärke, Grenze und Bedeutung, die ungekürzte Matrix, der Vergleich nach Dimensionen und überholte Aussagen. Die Vorfassungen trägt Git. Die Lücken N01–N20 und G01–G32 stehen mit Status im [Entwicklungsplan](Glide_Entwicklungsplan.md).

**Verlässlichkeit:** Glides Spalte stammt aus dem Code (Stand 3.33.18, abgeglichen am 08.10.2026). Die breite Matrix beruht auf Herstellerangaben und Berichten vom 01.10.2026; die Kurzfassung zu Glide, ChatGPT Space und Notion in Abschnitt 1.1 und der gezielte Abgleich in Abschnitt 6 berücksichtigen die Recherche vom 05.10.2026. Es liegt kein praktischer Vergleichstest aller Produkte vor. Vorteile, Positionierung und Übertragbarkeit sind Einschätzungen, keine Messwerte; veränderliche Herstellerangaben vor neuen Entscheidungen erneut prüfen.

**Überholt:** Ältere Analysen vom 16.–18.09.2026 (in Git) enthalten Aussagen, die nicht mehr gelten:

1. „Notion ist kein Ziel“ – seit der Aussage des Inhabers vom 26.09.2026 ist Notions Seitenkonzept ausdrücklich gewünscht, nur nicht der Baukasten.
2. Bearbeitungstag getrennt von der Fälligkeit ist kein exklusives Glide-Merkmal (Things: Startdatum/Deadline; Todoist: Datum/Deadline).
3. Natürliche Eingabe ist bei Todoist nicht nur Pro; Things hat natürliche Datumseingabe in Termin- und Erinnerungsfeldern.
4. Mobile bedeutet nicht zwingend Konto und Server (Super Productivity, Joplin); Glides Desktop-Fokus ist eine Entscheidung (D03), keine technische Notwendigkeit.
5. Alte Ausschlüsse (Rich Text, Seiten, Rückverweise, Animation) sind durch spätere Entscheidungen ersetzt; es gelten [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) und [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md).

## 1. Ergebnis

1. Glides Funktionsbreite ist für ein Ein-Personen-Projekt außergewöhnlich. In der **Tagesführung** (Bearbeitungstag ≠ Fälligkeit, Kapazität, Zeitblöcke, Heute/Demnächst, Tagesbeginn und -abschluss, Zeiterfassung) liegt Glide auf dem Niveau spezialisierter Planer. Die Kombination aus Pixel-Werkstatt und Pinnwand mit echten Aufgabenkarten ist im untersuchten Feld besonders; eine weltweite Alleinstellung wurde nicht nachgewiesen.
2. **AFFiNE** und **AppFlowy** decken die Kombination „Seiten + Datenbanken + Leinwand + lokal“ quelloffen ab. Glides Abgrenzung läuft deshalb über die Tagesführung, nicht über die Kombination.
3. **Verbleibende Lücken:** Erscheinungsbild „wie System“, der Ausbau von Inspektor und Barrierefreiheit sowie die nächste Such-/Indexstufe. Fokus und Tagesvorschlag, Aufgaben im Notiztext, gemeinsame Befehlspalette, eingebettete Wochenplanung, lokale Verweise/Rückverweise, Live-Listen, Titelbilder und Vorlagenvorschau sind mit 3.33.14–3.33.18 Windows/Python geprüft und geliefert. Native und menschliche Abnahme bleiben offen. Bewusst nicht: Erinnerungen bei geschlossener App, eigener Sync und Mobil.
4. **Stand der Technik 2026 ist KI** (Todoist Ramble und MCP, Notion Custom Agents, Apple Intelligence). Glides Antwort ist entschieden (Q3): Austausch über Dokumente statt Schnittstelle (G24).
5. **Bedienkomfort und Informationsarchitektur** liegen hinter den Vorbildern: nicht zu wenig Funktion, sondern zu viel dauerhaft sichtbar (UX1 im Entwicklungsplan).

### 1.1 Kurzfassung: Glide, ChatGPT Space und Notion

**Empfehlung:** Glide auf einen fertigen persönlichen Tagesablauf mit vollständigem lokalem Datenbestand ausrichten: erfassen, einen machbaren Tag planen, arbeiten und abschließen. Der mögliche Kaufgrund ist weniger Einrichtung und laufende Pflege. Eine bessere Bedienbarkeit gegenüber Space oder einem gut eingerichteten Notion-System ist bislang nicht durch Nutzertests belegt.

**USPs als strategische Einordnung, keine weltweit geprüfte Alleinstellung:**

| Produkt | Stärkster Kernnutzen / USP | Konsequenz für Glide |
|---|---|---|
| **ChatGPT Space** | Aus Arbeitskontext gemeinsam mit KI unmittelbar Ergebnisse entwickeln: bearbeitbare Seiten, Dateien, Menschen und KI im selben Arbeitsbereich. | Aufgaben aus vorhandenem Kontext zu gewinnen kann manuelle Erfassung sparen. Glide muss zusätzliche Pflege vermeiden. |
| **Notion** | Ein anpassbares gemeinsames System für Wissen, Projekte und strukturierte Arbeit, einschließlich Aufgaben und Agenten. | Glides Vorteil muss im fertigen Ablauf liegen, nicht allein in einzelnen Aufgabenfeldern oder Ansichten. |
| **Glide** | Einen machbaren persönlichen Arbeitstag planen, ohne zuerst ein eigenes Produktivitätssystem einzurichten; der Arbeitsbestand bleibt lokal und ohne Konto nutzbar. | Tagesführung, einfache Bedienung und Datenkontrolle als zusammenhängenden Nutzen zeigen. |

**Belegte Unterschiede und Grenzen:**

- **Space** ist mehr als eine einfache To-do-App: Checklisten, Tabellen, direkte Bearbeitung, Zusammenarbeit und erstellbare interaktive Werkzeuge sind dokumentiert. Ein standardisiertes persönliches Aufgabenmodell mit Aufwand und Tageskapazität sowie vollständiger Offline-Betrieb sind in den geprüften Quellen nicht dokumentiert. Das bedeutet nicht, dass solche Funktionen technisch unmöglich sind. [Produktseite](https://chatgpt.com/features/space/), [Pages](https://learn.chatgpt.com/docs/space/pages)
- **Notion** besitzt Task-Datenbanken, My Tasks, Unteraufgaben, Abhängigkeiten und Kalenderplanung. Bearbeitungstag neben Fälligkeit sowie Kapazität über Formeln und Rollups sind konfigurierbar. Agenten und externe KI-Anbindung erhöhen die Überschneidung mit Space. [Aufgaben](https://www.notion.com/help/guides/give-your-to-dos-a-home-with-task-databases), [Kalender](https://www.notion.com/help/use-notion-calendar-with-notion), [Eigenschaften](https://www.notion.com/help/database-properties), [Rollups](https://www.notion.com/help/relations-and-rollups), [Custom Agents](https://www.notion.com/help/custom-agents), [MCP](https://www.notion.com/help/notion-mcp)
- **Glides Datenvorteil** ist der vollständige lokale Primärbestand ohne Konto. Notion bietet ebenfalls Offline-Nutzung, jedoch für heruntergeladene beziehungsweise zwischengespeicherte Inhalte eines Cloudsystems. Glide fehlen gemeinsame Bearbeitung und komfortable Gerätesynchronisation; Erinnerungen benötigen die laufende App, Kalender werden über Dateien ausgetauscht. [Notion offline](https://www.notion.com/help/use-pages-offline), [Glide-Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md)

**Glide-Stand 3.33.18 (Codeabgleich 08.10.2026):** Tagesvorschlag und Fokus seit 3.33.14, Aufgaben im Notiztext und Aufgabenverweise seit 3.33.15, gemeinsame Befehlspalette und Bedienkomfort seit 3.33.16, eingebettete Wochen-/Monatsplanung und lokale Seiten-/Listen-/Aufgabenverweise mit Rückverweisen seit 3.33.17. Seit 3.33.18 ergänzen Live-Listen mit Originalaufgaben, Titelbilder und gefüllte Vorlagenvorschau den Anlegen-Weg. Format 23 schützt diese Erweiterungen. Windows-Vollprüfung, Python-/Showcase-Lieferung und strenge CI sind grün; native und menschliche Abnahme offen. Der dateibasierte KI-Austausch ändert seit 3.35.0 auch vorhandene Aufgaben – über ein Kontextpaket und einen geprüften Änderungsvorschlag mit Konflikterkennung (G24); Stand des Sprints bis 3.35.0 in Abschnitt 4.1 und der Matrix. Herstellerangaben behalten ihre ausdrücklich genannten Recherchezeitpunkte. Details: [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md), [Entwicklungsplan §4.4](Glide_Entwicklungsplan.md#44-größere-umsetzungspakete-auftrag-07102026).

**Empfohlener Fokus** (seit 05.10.2026 im [Ausbauprogramm des Entwicklungsplans](Glide_Entwicklungsplan.md#43-ausbauprogramm-alltag-komfort-und-oberfläche) eingeplant; Umsetzung je Paket nach Auftrag):

1. Sichere, schnelle Basis und weniger dauerhaft sichtbare Bedienung; Heute, nächste Handlung und verfügbare Zeit erhalten den stärksten visuellen Rang.
2. Tagesplanung und Umplanung vereinfachen: Aufgaben verschieben, ohne ihre Fälligkeit unbeabsichtigt zu ändern; wenige Pflichtangaben und brauchbare Vorgaben.
3. Fokus und Tastaturbedienung auf der vorhandenen Zeiterfassung ausbauen.
4. Aufgaben und Projektwissen so verbinden, dass Suche und doppelte Pflege sinken.
5. Den beschlossenen dateibasierten KI-Austausch bei Bedarf gezielt vereinfachen; Änderungen prüfbar übernehmen (seit 3.35.0 umgesetzt, G24) und Dubletten vermeiden.

**Zielgruppe und Marke:** Als erste Zielgruppe eignen sich Menschen, die überwiegend am Desktop mehrere eigene Projekte bearbeiten, etwa Gestaltung, Schreiben, Entwicklung und persönliche Wissensarbeit. Pixel-Werkstatt und Gismo dienen als optionale persönliche Signatur; ein Hauptkaufgrund ist bislang nicht belegt. Die älteren Rundgangbilder erlauben keine vollständige visuelle Bewertung von 3.33.7. „Ruhige Tagesplanung“ ist zudem bereits bei [Sunsama](https://www.sunsama.com/) besetzt; lokale Aufgaben, Zeiterfassung und Fokus bietet auch [Super Productivity](https://super-productivity.com/).

**Formulierung zum Testen:**

> **Plane einen Tag, der zu deiner Zeit passt.**
> Glide verbindet Aufgaben und Projektwissen mit einer fertigen Tagesplanung. Dein Arbeitsbestand bleibt auf deinem Rechner – ohne Konto.

**Nachweis:** Mit 12–15 passenden Nutzern über zwei bis drei Wochen gegen eine gut eingerichtete Notion-Tagesplanung mit Calendar und einen brauchbaren Space-Ablauf testen. Einrichtung und tägliche Pflege getrennt messen; zusätzlich doppelte Erfassung, Umplanung und freiwillige weitere Nutzung erfassen. Ein Preisvorteil ist nicht belegt: vorhandene Konkurrenzabos können geringe Zusatzkosten bedeuten; Glides öffentliche Preis- und Lizenzbedingungen sind offen.

## 2. Vorbilder des Inhabers

Belegstufen: **ausdrücklich belegt** (persönliche Aussage oder Entscheidung dokumentiert) · **als Vorbild benannt** (für einen Bereich vorgegeben am 25.09.2026, Einzelmerkmale aus der Recherche) · **Recherchebezug** (betrachtet, keine persönliche Vorliebe belegt). Die Aussagen im Wortlaut stehen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md#leitgedanken-des-inhabers).

| Produkt | Belegstufe | Übernommene Merkmale | Bewusst anders |
|---|---|---|---|
| **Notion** | ausdrücklich belegt: „Die App gefällt mir sehr gut“ (26.09.2026), Glide soll allgemein mehr wie Notion werden; Bilder als Referenz für Schreiben und Erscheinungsbild | Endlos scrollende Seite, leichter Lesefluss, Seiten für KI-Berichte, integrierte Aufgaben, Formatleiste bei Markierung, Rechtsklick „Umwandeln in“, Aufklapp- und Hinweisblöcke, großer Seitentitel, Weißraum, Bibliotheken und Galerien, Favoriten und Zuletzt im Seitenkontext | Seite und datierte Notiz getrennt; keine Unterseiten; Aufgaben sind echte Glide-Aufgaben; Felder Glide-weit statt je Liste; keine Spalten; Desktop zuerst; kein Datenbank-Baukasten |
| **Trello** | als Vorbild benannt (Pinnwand) | Karten in Spalten, Cover und Farben, einklappbare Listen, derselbe Inhalt in mehreren Kontexten | keine Cover aus Bildarchiven im Netz |
| **OneNote** | als Vorbild benannt (Pinnwand) | freie Anordnung, Notizbuchcharakter, große Fläche, Linien/Karo | keine Handschrift |
| **FigJam** (Figma als Whiteboard) | als Vorbild benannt (Pinnwand) | Klebezettel, beschriftete Verbinder, benannte Bereiche, Auswahl aufräumen, schnell den nächsten Zettel | keine Zettel ohne Aufgabe |
| **Microsoft Planner** | als Vorbild benannt (Aufgaben auf der Pinnwand) | Gruppieren nach Status, Termin oder Label; Ziehen ändert die passende Eigenschaft (D02); Checkliste, Beschreibung, Bild auf der Karte | – |
| **Affinity** | als Vorbild benannt (Zeichnen und künstlerische Entfaltung) | kontextbezogene Werkzeuge, direkte Farbauswahl und Paletten, Vorschau, Zwischenstände, Exportablauf | kein Vektor- oder Layoutumfang; die Pixel-Nische ist eigene Vorgabe (25.09.2026) |

Recherchebezug ohne belegte persönliche Vorliebe: Todoist, TickTick, Things, Sunsama, Akiflow, Obsidian, Anytype, Capacities, Evernote, Miro, Aseprite, Pixelorama, Asana, ClickUp und monday.com.

## 3. Vergleichsfeld und Entwicklung 2026

Je Produkt: Stärke einschließlich der Entwicklung bis 01.10.2026, Grenze und Bedeutung für Glide. Herstellerangaben und Berichte vom 01.10.2026; Grenzen und Bedeutung sind Einschätzungen.

**Aufgaben und Tagesplanung**

| Produkt | Stärke und Entwicklung | Grenze | Bedeutung für Glide |
|---|---|---|---|
| [Todoist](https://www.todoist.com/features) | Natürliche Schnelleingabe, Datum und Deadline getrennt, Liste/Board/Kalender; 2026 Ramble (Sprache → Aufgaben mit Feldern) und offizieller MCP-Server ([Ramble](https://www.todoist.com/help/articles/from-voice-to-tasks-ramble-july-1), [Changelog 2026](https://www.todoist.com/help/articles/2026-changelog)) | Konto und Cloud; Kalenderlayout, Dauer und Deadlines teils nur in Bezahltarifen | Natürliche Erfassung ist Standard – Glide hat sie seit 3.33.3 |
| [Things 3](https://culturedcode.com/things/support/articles/2803579/) | Ruhiger Ablauf Heute/Demnächst/Jederzeit/Irgendwann, Startdatum ≠ Deadline; 3.23 (21.08.2026) frühes Erledigen von Wiederholungen, 3.24 Schlummer-Intervalle und Siri-Anbindung ([Release Notes](https://culturedcode.com/things/support/articles/1100684/)) | nur Apple-Geräte, getrennte Käufe | Feinschliff statt Funktionsfülle – das Apple-Prinzip; Vorbild für D14 |
| [TickTick](https://ticktick.com/features) | Aufgaben, Kalender, Kanban, Gewohnheiten, Pomodoro, Eisenhower; 8.0 vorgeschlagene Tagesaufgaben, Jahres-Heatmap ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/)) | dichte Oberfläche, vieles Premium | Fokus neben der Aufgabe (G05); bestätigt Tagesbeginn und Heatmap |
| [Super Productivity](https://super-productivity.com/) | lokal, ohne Konto, MIT; Fokus/Pomodoro, Zeiterfassung, Timeboxing, Eisenhower, optionaler WebDAV-Sync | eher Arbeitszeit als Seiten und Bibliotheken | direktester lokaler Planer-Konkurrent; Fokus und Zeit gehören zusammen |
| [Sunsama](https://www.sunsama.com/) | geführte Tagesplanung, Zeitblöcke, Tagesabschluss, Wochenanalyse | Abonnement; lebt von gepflegter Routine | Maßstab für Tagesbeginn und -abschluss; Schätzung und echte Zeit nebeneinander |
| [Akiflow](https://akiflow.com/) | Universal Inbox, Time Blocking, automatische Planung | Abonnement, Integrationspflege | Zeit durch Ziehen sichtbar zuweisen; freie Zeitfenster vorschlagen (B-03) |
| [Microsoft To Do](https://www.microsoft.com/en-us/microsoft-365/microsoft-to-do-list-app) | „Mein Tag“ ohne Einrichtung verständlich | wenig Struktur, Konto | Tagesfokus, den man sofort versteht |
| Apple Erinnerungen/Notizen | iOS/macOS 27: Erinnerung in eigenen Worten, Felder am Objekt, Notizen als Markdown ([9to5Mac](https://9to5mac.com/2026/06/12/heres-everything-new-for-reminders-in-ios-27/)) | Apple-Plattform, Apple Intelligence | Felder am Objekt statt Dialog – stützt den Inspektor (N05/U12) |

**Seiten, Notizen und Wissen**

| Produkt | Stärke und Entwicklung | Grenze | Bedeutung für Glide |
|---|---|---|---|
| [Notion](https://www.notion.com/help/writing-and-editing-basics) | Seiten und Blöcke, Slash-Menü, Datenbanken mit Ansichten, Galerie, Titelbild; Offline-Modus seit 2.53 (08/2025), 3.2 KI-Notizen und Agenten mobil, 3.3 Custom Agents mit Zeitplänen und MCP ([2.53](https://www.notion.com/en-gb/releases/2025-08-19), [3.2](https://www.notion.com/de/releases/2026-01-20)) | Datenbankpflege kostet Aufmerksamkeit; Richtung Team-Automation | zentrales Vorbild für Editor, Bibliotheken, Navigation und Aufgaben im Kontext; „Notion kann nicht offline“ ist kein Unterscheidungsmerkmal mehr (Abschnitt 6) |
| [AFFiNE](https://github.com/toeverything/affine) | Dokument und Leinwand sind dieselbe Seite, Kanban, lokal-first mit optionaler Cloud, KI | schwach in persönlicher Tagesplanung (Einschätzung) | stärkster Vergleich für Pinnwand + Seiten; Abgrenzung über die Tagesführung |
| [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | Tabelle, Board, Kalender, Galerie; lokale KI über Ollama | große Laufzeitabhängigkeit für lokale KI | lokale KI ist machbar, widerspricht aber Glides Abhängigkeitsregel |
| [Obsidian](https://obsidian.md/) | lokale Markdown-Dateien, Rückverweise, Canvas; 1.10 Bases mit Gruppieren und Zusammenfassungen ([Changelog](https://obsidian.md/changelog/2025-10-01-desktop-v1.10.0/)) | Aufgabenplanung braucht Plugins und Eigenbau | stabile Verweise und Rückverweise (G08/G30); feste Glide-Felder bleiben richtig |
| [Logseq](https://discuss.logseq.com/t/whats-new-with-logseq-db-may-16th-2026/35020) | 2.0 Beta mit typisierten Eigenschaften, Wechsel von Dateien zu SQLite | Datenverlustrisiko beim Wechsel | Warnbeispiel; bestätigt D16 (JSON beschleunigen statt SQLite als Hauptspeicher) |
| [Capacities](https://capacities.io/), [Heptabase](https://wiki.heptabase.com/roadmap), [Anytype](https://github.com/anyproto/anytype-ts), Craft | typisierte Objekte, Tagesnotizen, Karten auf Whiteboards mit „wo liegt diese Karte überall“, lokale verschlüsselte Objekte (Anytype) | Umgewöhnung an Objektmodelle; teils Cloud-Sync | Aufgaben im Wissenskontext sind Branchenstandard; Bibliotheken mit festen Eigenschaften |
| [OneNote](https://support.microsoft.com/en-us/onenote/take-and-format-notes) | Notizbücher, frei platzierte Inhalte, Tags | To-do-Tags ersetzen keine Planung | Notizbuchgefühl; Aufgaben bleiben echte Objekte |
| [Evernote](https://evernote.com/en-us/features/notes-app), [Joplin](https://joplinapp.org/), [Google Keep](https://support.google.com/keep/answer/6191044?hl=de) | Sammeln, Web Clipper und Suche (Evernote); lokal mit optionalem Sync (Joplin); geringe Schwelle (Keep) | Cloud und Tarife bzw. Einrichtungsaufwand bzw. wenig Struktur | Wiederfinden ist Kernnutzen (G14); Eingang sichtbar, bis eingeordnet (U07) |

**Boards, Pinnwände und Teamwerkzeuge**

| Produkt | Stärke und Entwicklung | Grenze | Bedeutung für Glide |
|---|---|---|---|
| [Trello](https://trello.com/en/pricing) | anschaulicher Kartenfluss, Cover, Checklisten, Spiegelkarten | Konto; Ansichten je Tarif | einfaches Kanban, Karte bearbeiten mit Kontext |
| [Microsoft Planner](https://support.microsoft.com/en-us/planner/compare-microsoft-planner-basic-vs-premium-plans) | Gruppieren nach Status, Termin, Label; Premium mit Abhängigkeiten | lizenzabhängig; das Update 2026 nimmt Whiteboard-Reiter und iCalendar-Feed heraus ([Neowin](https://www.neowin.net/amp/microsoft-confirms-major-2026-update-to-remove-several-planner-features-add-new-ones/)) | nur noch Referenz für die Gruppierungslogik |
| [FigJam](https://help.figma.com/hc/en-us/articles/15300412458647-Explore-FigJam-files), [Miro](https://miro.com/features/) | Zettel, Verbinder, Bereiche, Aufräumen; Frames und Präsentation | Objekte sind keine Aufgaben; für eine persönliche Fläche überdimensioniert | benannte Bereiche, beschriftete Verbindungen, Präsentation aus Bereichen (vorhanden) |
| [Asana](https://asana.com/features/project-management), [ClickUp](https://clickup.com/features/views), [monday.com](https://monday.com/capabilities) | Verantwortung, Abhängigkeiten, viele Ansichten, Automationen | Team- und Prozesspflege, tarifabhängig | eine Aufgabe in mehreren Kontexten ohne Kopie; Blockaden sichtbar – Team bleibt außen vor |

**Zeichnen und Pixel**

| Produkt | Stärke und Entwicklung | Grenze | Bedeutung für Glide |
|---|---|---|---|
| [Affinity](https://www.canva.com/newsroom/news/all-new-affinity/) | Vektor, Pixel und Layout in einer App, kontextbezogene Studios | viel größerer Umfang; Aktivierung über Canva-Konto | kontextbezogene Werkzeugleisten, erreichbare Farben, klarer Export |
| [Aseprite](https://www.aseprite.org/) | Pixel-Art, Ebenen, Animation, Zwiebelhaut, Spritesheet | spezialisiert, kein Organisationswerkzeug | Animation als eigener, begrenzter Arbeitsbereich (G17, D07) |
| [Pixelorama](https://orama-interactive.itch.io/pixelorama) | quelloffen; indizierte Farben, Paletten, Tilemaps, PNG/GIF/Spritesheet | Einarbeitung | Palettenverwaltung und Umfärben über indizierte Farben (G19) |
| [Lospec](https://lospec.com/palette-list) | Palettenverzeichnis | – | Paletten-Import (GPL/HEX, seit 3.32.0 auch Aseprite/ASE) |

**Laufzeit:** [Tcl/Tk 9.1.0](https://www.tcl-lang.org/software/tcltk/9.1.html) (29.09.2026) bringt eine Screenreader-Grundlage; der python.org-Installer für macOS liefert ab Python 3.14.5 Tk 9.0.3. Chance für Barrierefreiheit (N12) und gleiche Verteilung auf allen Plattformen (D15).

**Gezielter Herstellerabgleich 07.10.2026:** [Sunsamas tägliche Planung](https://help.sunsama.com/docs/usage-guides/daily-planning/) und [Super Productivity](https://super-productivity.com/) bestätigen Tagesplanung sowie Fokus/Pomodoro und Timeboxing als zusammenhängende Alltagsabläufe. Daraus wird für Glide ein lokaler Weg vom begründeten Vorschlag zum Zeitblock und zur nächsten Aufgabe abgeleitet. Dies ist eine gezielte Aktualisierung dieser beiden Vorbilder, keine neue Prüfung der gesamten Matrix.

## 4. Featurematrix

● vorhanden · ◐ teilweise, eingeschränkt oder nur im Bezahltarif · ○ fehlt · P per Erweiterung · – nicht Zweck · ? nicht verifiziert
**Gl** Glide 3.35.0 · **No** Notion · **Td** Todoist · **Th** Things 3 · **TT** TickTick · **SP** Super Productivity · **AF** AFFiNE · **AP** AppFlowy · **Ob** Obsidian · **Ap** Apple Erinnerungen + Notizen

| Bereich | Funktion | Gl | No | Td | Th | TT | SP | AF | AP | Ob | Ap | Glide |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Erfassen | Natürliche Eingabe mit sichtbarer Erkennung | ● | ◐ | ● | ● | ● | ◐ | – | – | P | ● | seit 3.33.3, Wiederholungen seit 3.33.4, Erinnerungen seit 3.33.20 |
| | Systemweite Schnellerfassung | ○ | ● | ● | ● | ● | ◐ | ? | ? | ◐ | ● | bewusst nicht (G07) |
| | KI-/Spracherfassung | ○ | ● | ● | ◐ | ? | ○ | ◐ | ◐ | P | ● | bewusst nicht (Q3) |
| Planen | Bearbeitungstag getrennt von Fälligkeit | ● | ◐ | ● | ● | ◐ | ◐ | – | ◐ | P | ○ | D01 |
| | Heute-Ansicht ohne Dubletten | ● | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ● | D14, seit 3.33.6 |
| | Tageskapazität, Aufwand | ● | – | ◐ | ○ | ◐ | ● | – | – | – | ○ | Kapazität je Wochentag |
| | Zeitblöcke, Stundenraster | ● | ◐ | ◐ | ○ | ● | ● | ○ | ◐ | P | ◐ | |
| | Kalender Monat/Woche | ● | ● | ◐ | ◐ | ● | ◐ | ? | ● | P | ● | eingebettet seit 3.33.17 (N04/AU04) |
| | Tagesbeginn, Tagesabschluss, Wochenrückblick | ● | ○ | ◐ | ○ | ◐ | ● | ○ | ○ | P | ○ | Modi von Heute |
| | Wiederholungen | ● | ◐ | ● | ● | ● | ● | ○ | ? | P | ● | Termine überspringen seit 3.33.20 |
| | Erinnerung bei geschlossener App | ○ | ● | ● | ● | ● | ◐ | ○ | ◐ | P | ● | bewusst nicht (N09) |
| | Fokusansicht/Pomodoro | ● | ○ | ○ | ○ | ● | ● | ○ | ○ | P | ○ | Fokus mit Pause, Wechsel und Zeitbuchung seit 3.33.14 (G05/AU05) |
| | Zeiterfassung je Aufgabe | ● | ◐ | ○ | ○ | ◐ | ● | ○ | ○ | P | ○ | eine laufende Erfassung |
| | Eisenhower | ● | ◐ | ○ | ○ | ● | ● | ○ | ◐ | P | ○ | Gruppierung seit 3.33.5 |
| | Abhängigkeiten | ● | ● | ○ | ○ | ○ | ○ | ○ | ○ | P | ○ | „wartet auf“ (`blocked_by`) mit Kreisprüfung |
| | Gewohnheiten | ○ | ◐ | ○ | ○ | ● | ◐ | ○ | ○ | P | ○ | vorerst nicht (G06) |
| Ordnen | Listen, Ordner, Labels, Archiv, Papierkorb | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | |
| | Gespeicherte Filter | ● | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | erklären Treffer und Ausgeblendetes seit 3.34.0 |
| | Board/Kanban | ● | ● | ● | ○ | ● | ● | ● | ● | ◐ | ● | Pinnwand als Board |
| | Tabelle | ● | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ○ | |
| | Galerie/Karten | ● | ● | ○ | ○ | ○ | ○ | ? | ● | ◐ | ○ | |
| | Vorlagen | ● | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ◐ | mit selbstfüllenden Platzhaltern |
| | Unteraufgaben, Checklisten | ● | ● | ● | ● | ● | ● | ◐ | ◐ | P | ● | |
| Wissen | Block-Editor mit „/“-Menü | ● | ● | – | – | ◐ | ◐ | ● | ● | ◐ | ◐ | |
| | Bilder in Seiten | ● | ● | – | – | ◐ | ○ | ● | ● | ● | ● | Druck und Markdown mit Bildern seit 3.34.0; Linux JPEG nur mit Systemwerkzeug (N08) |
| | Echte Aufgaben im Dokument | ● | ◐ | – | – | – | – | ◐ | ◐ | P | ◐ | Seiten und Notiztext mit Original-IDs seit 3.33.15 (G29/G31/G32) |
| | Verweise und Rückverweise | ● | ● | ○ | ○ | ○ | ○ | ● | ● | ● | ● | lokale Seiten-/Listen-/Aufgabenverweise und abgeleitete Rückverweise seit 3.33.17 (G08/G30) |
| | Volltextsuche im Inhalt | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | seit 3.33.7 Inhalte von Seiten/Notizen und Beschreibungen; Fundstellen markiert seit 3.34.0; kein FTS5 nötig (P07: 66,6 ms bei 10.000 Punkten) |
| | Eigenschafts-/Datenbankansichten | ◐ | ● | – | – | – | – | ● | ● | ● | – | feste Glide-Felder (bewusst) |
| | Tagesnotiz, Notizbuch | ● | ◐ | – | – | ◐ | ◐ | ● | ? | ● | ○ | |
| | Seitensymbol, Titelbild | ● | ● | – | – | – | – | ● | ● | P | ○ | Pixelsymbol; Titelbild als lokales Bild oder Pixelzeichnung seit 3.33.18 (G09) |
| | Markdown-Import/-Export | ● | ● | ◐ | ◐ | ◐ | ◐ | ● | ● | ● | ◐ | |
| Visuell | Freie Leinwand mit echten Aufgabenkarten | ● | ○ | ○ | ○ | ○ | ○ | ● | ○ | ● | ◐ | |
| | Pixel-Zeichnen und Symbol-Export | ● | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | besondere Kombination |
| | Animation | ○ | – | – | – | – | – | – | – | – | – | G17, D07 offen |
| Daten | Ohne Konto vollständig nutzbar | ● | ○ | ○ | ● | ○ | ● | ● | ◐ | ● | ◐ | |
| | Offene lokale Datei | ● | ○ | ○ | ○ | ○ | ◐ | ◐ | ◐ | ● | ○ | eine lesbare JSON-Datei |
| | Automatische Sicherungen, Versionen | ● | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ● | ◐ | Sicherungen, Tagesstände, Verlauf; Stände vergleichen seit 3.35.0 |
| | Sync zwischen Geräten | ◐ | ● | ● | ● | ● | ● | ● | ● | ● | ● | Datenordner in Cloud-Ablage, ohne Zusammenführen |
| | Mobile Apps | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | zurückgestellt (D03) |
| | Windows, macOS, Linux | ● | ◐ | ● | ○ | ● | ● | ● | ● | ● | ○ | Linux eingeschränkt (Tk 8.6, Bildformate) |
| | Import aus anderen Apps | ◐ | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ○ | CSV/MD/ICS; Notion/Todoist fehlt (G21) |
| | Kalenderdatei (ICS) | ● | ◐ | ● | ◐ | ● | ◐ | ○ | ○ | P | ● | als Datei, kein Abo |
| | Eingebaute KI | ○ | ● | ● | ◐ | ? | ○ | ● | ● | P | ● | bewusst nicht (Q3) |
| | Schnittstelle für Assistenten (API/MCP) | ◐ | ● | ● | ◐ | ◐ | ? | ? | ◐ | ◐ | ◐ | `.glideexchange`; Dokumente statt Schnittstelle (Q3) |
| Bedienung | Eine Befehlspalette | ● | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ● | ○ | gemeinsame Inhaltssuche und Aktionen seit 3.33.16 (U01) |
| | Erscheinungsbild wie System | ○ | ● | ● | ● | ● | ● | ● | ● | ● | ● | N01 |
| | Rückgängig auch für Strukturänderungen | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | ● | 20 Schritte, Bestandswächter |
| | Hilfe in der App | ● | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Handbuch, Kürzel; Hinweise je Ansicht einklappbar seit 3.33.16 (D11/U02) |
| | Beispielinhalt | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Showcase und Rundgang; Einstieg bewusst nicht |
| | Screenreader | ○ | ? | ? | ● | ? | ? | ? | ? | ? | ● | N12 nach Tk 9.1 |

### 4.1 Vergleich nach Dimensionen

Einordnung der Matrix und der UX-Befunde; die Messwerte stehen im [Entwicklungsplan, Abschnitt 10](Glide_Entwicklungsplan.md#10-messbare-ziele).

| Dimension | Maßstab | Glide 3.35.0 (Codeabgleich 09.10.2026) | Lücke | Konsequenz |
|---|---|---|---|---|
| Funktionen | Notion (Breite), TickTick (Planung + Fokus), AFFiNE (Seite + Leinwand) | sehr breit; Verweise, Fokus, Aufgaben im Notiztext, Live-Liste und Titelbild seit 3.33.14–3.33.18, Routinen seit 3.33.20; Bilder in Druck/Markdown, Trefferhervorhebung und erklärte Filter seit 3.34.0, Sicherungsvergleich seit 3.35.0 | im Sprint geschlossen; offen bleiben die an Inhaberentscheidungen gebundenen Pakete (E-S1–E-S8) | keine neue Breite ohne Entscheidung (Entwicklungsplan §15.3) |
| Alltag | Things (Heute → Demnächst), Sunsama (Ritual) | Heute/Demnächst, Tagesvorschlag, verfügbare Zeit, Fokus, Wochenplanung; seit 3.33.20 Termine überspringen, Routinen in „Heute“, Erinnerung beim Erfassen | keine Gewohnheitsstatistik (bewusst, G06) | geschlossen mit KO02, AU06, KO03 |
| Komfort | Todoist (Erfassung), Apple (Felder am Objekt) | Feldchips, Einplanen-Menü, gemeinsame Palette, Rückgängig überall; seit 3.33.20 mehrzeiliges Einfügen, zuletzt benutzte Ziele, „+“ und Umschalt+Enter | Detailbearbeitung doppelt | Inspektor N05/KO04 nach I7 |
| Tempo | Things, Apple: jede Aktion unter 100 ms | 3.33.19 auf dem Referenz-Mac: Abhaken 17 / 61 / 118 ms bei 1.000 / 5.000 / 10.000 Punkten (im Akkubetrieb bis 119 ms bei 5.000); unveränderte Startseite 0,3 ms, Neuaufbau 270–300 ms; Seite mit 30 Bildern beim Tippen 3 ms | Neuaufbau der Startseite und Einstellungsfenster (≈ 560 ms) begrenzt durch Tk-Zeichnen; Abhaken über 5.000 Punkte linear | Stufe 0 bis auf den Neuaufbau erledigt (P04, P06r, P03r, P08c in 3.33.19); weitere Gewinne nur mit anderem Zeichenweg |
| Gestaltung | Things, Notion: viel Weißraum, wenige Bedienelemente | höchstens 4 Kopfsymbole, keine Symbole mit Mehrfachbedeutung, einklappbare Hinweise (3.33.16); „+“ statt zweier Textknöpfe (3.33.20); hell/dunkel nach System, neutrale aktive Zustände, schmale Seitenleiste (3.33.21) | Referenzentwürfe für Heute, Liste und Seite | OB02/OB03 nach I7 |
| Hilfe | Things („Neu in …“), Notion | Handbuch, Kürzel, Showcase; Hinweise einklappbar (D11); seit 3.33.20 einmalige Karte „Neu in Glide“ nach einem Update | – | geschlossen mit N07 |
| Marke | Things (eine starke Gestalt), Notion (Minimalismus) | Logo, Gismo, Design „Pixel“ | zehn Designs verwässern die Gestalt; Namenskollision „Glide“ | Signaturdesign vorn mit „Automatisch (hell/dunkel)“ (N01/U17), Gismo als Markenfigur, Markenprüfung (I4) |
| KI 2026 | Todoist Ramble/MCP, Notion Agents, Apple Intelligence | `.glideexchange` für externe KI; seit 3.35.0 Kontextpaket und geprüfte Änderungsvorschläge (G24) | keine direkte Schnittstelle – bewusst (Q3) | geschlossen mit G24; Anhänge im Austausch weiter bewusst nicht |

## 5. Positionierung

> **Glide ist der ruhige, lokale Arbeitsplatz für den eigenen Tag:** planen mit Bearbeitungstag, Fälligkeit und Kapazität; erledigen mit Zeit und Fokus; festhalten in Seiten, Notizbuch und Pinnwand; alles in einer eigenen Datei, ohne Konto. Die Pixel-Werkstatt ist die persönliche Signatur.

- **Stärken vertiefen:** Tagesführung (G05), Aufgaben im Kontext (G29, G31, G08/G30), Wiederfinden (G14), weniger dauerhaft sichtbare Bedienung (UX1).
- **Nische sichtbar machen:** Im untersuchten Feld verbindet keine Anwendung Organisation mit einem echten Pixelraster. Die Nische wird stärker, je sichtbarer Pixelbilder in der Organisation werden: Pixelsymbole an Listen und Ordnern, Kachel „Zeichnungen“, Galerie, Zeichnung als Pinnwandkarte, Titelbild als Pixelzeichnung (G09).
- **Nicht nachbauen:** Team, Cloud, frei definierbare Datenbanken, eingebaute Cloud-KI.
- **Marke:** Der Name „Glide“ kollidiert mit bekannten Produkten (etwa der No-Code-Plattform Glide); Markenprüfung durch den Inhaber (I4). Gismo und das Pixel-Design sind die stärksten Wiedererkennungsmerkmale.

## 6. Verifizierter Abgleich und Konsequenzen (05.10.2026)

Gezielte Prüfung der folgenden Herstellerquellen; kein Praxistest und keine neue Vollprüfung sämtlicher Produkte/Matrixfelder. Ältere Versions-, Tarif- und KI-Aussagen in Abschnitt 3 bleiben Recherchekontext vom 01.10.2026 und sind für neue Entscheidungen erneut zu prüfen. Herstellerangaben und unsere Konsequenzen sind getrennt:

| Vorbild | Aktuell belegtes Verhalten | Einschätzung / Konsequenz für Glide |
|---|---|---|
| Notion | [Offline-Seiten](https://www.notion.com/help/use-pages-offline) in Desktop/Mobil auf allen Plänen; einzeln herunterladen, Unterseiten separat, Datenbanken zunächst erste 50 Zeilen der ersten Ansicht. [Workspace-Suche](https://www.notion.com/help/search) durchsucht Inhalte, mit Grenzen bei Kommentaren und Eigenschaften. | Offline allein grenzt Glide nicht ab; vollständiger eigener Bestand ohne Download-Auswahl und Konto ist die präzisere Positionierung. Inhaltssuche schließt eine konkrete Alltagsschwäche. |
| Obsidian | [Suche](https://obsidian.md/help/Plugins/Search) durchsucht Notizen und Canvases, mit Operatoren. [Rückverweise](https://obsidian.md/help/plugins/backlinks) zeigen verknüpfte und unverknüpfte Erwähnungen. | Nach dem ersten Suchschnitt Referenzregeln und Rückverweise priorisieren. Eine neue Operatorsprache ist für die erste Glide-Stufe unnötig. |
| Todoist | [Quick Add](https://www.todoist.com/help/todoist/features/use-task-quick-add-in-todoist-va4Lhpzz) setzt Datums-/Label-/Erinnerungsfelder beim Erfassen. | Bestehende deutsche Erfassung mit sichtbaren Chips weiter pflegen; kein zusätzlicher Erfassungsweg. |
| Super Productivity | [Herstellerseite](https://super-productivity.com/): Aufgaben, Zeiterfassung, Fokus/Pomodoro und Timeboxing; lokale Daten, offline und ohne Konto, Synchronisierung optional. | Direkter Vergleich für den persönlichen Tag: Fokus ist eine echte Lücke. Bestehende Zeiterfassung nutzen und genau-einmal-Buchung prüfen. |
| AFFiNE | [Herstellerseite](https://affine.pro/) positioniert Dokumente und Whiteboard als gemeinsamen Wissensarbeitsplatz. | Seiten/Pinnwand allein sind keine belastbare Alleinstellung. Tagesplanung und persönliche Pixelgestaltung verbinden statt freien Datenbankumfang kopieren. |

**Priorität aus diesem Abgleich:** sichere/schnelle Basis → wiederfinden (G14 erste Stufe) → weniger Oberfläche (Aktionskennungen/UX1) → fokussiert erledigen → Aufgaben im Text und Rückverweise. Der erste Suchschnitt darf vor UX1 erfolgen, weil er den vorhandenen Suchweg ergänzt, keine neue Oberfläche einführt und keine Aktionsnamen verändert. FTS5 erst nach Messung, als löschbarer Cache. Umsetzung und Prüfgrenzen stehen ausschließlich im Entwicklungsplan und QA-Bericht.

## 7. Recherche 08.10.2026 für den Sprint

Gezielte Recherche am 08.10.2026 zu den Aufgaben des Sprints ([Entwicklungsplan §15](Glide_Entwicklungsplan.md#15-sprint-ab-08102026-aufgabenkatalog)). Herstellerseiten und Primärquellen haben Vorrang; Berichte Dritter sind als solche gekennzeichnet. Kein Praxistest. **Fakt** = in der Quelle belegt, **Folgerung** = eigene Einschätzung für Glide.

| Thema | Fakt (Quelle, Abruf 08.10.2026) | Folgerung für Glide | Aufgabe |
|---|---|---|---|
| Wiederholungen | Things 3.23 (Blogbeitrag 19.08.2026): Wiederkehrende Aufgaben lassen sich vor ihrem Termin erledigen, die nächste Kopie folgt der Regel; beim Verschieben fester Reihen „Make Exception“ oder „Update Rule“; „Create Next Copy“; mehrere Reihen pausieren. Ein eigenes „Überspringen“ nennt der Beitrag nicht. [Things-Blog](https://culturedcode.com/things/blog/2026/08/repeating-to-dos-refined/) | Frühes Erledigen mit genau einem Folgetermin ist Erwartung. Glide braucht zusätzlich einen ausdrücklichen Weg, einen oder alle verpassten Termine zu überspringen, ohne Erledigung zu buchen. | KO02 |
| Erinnerung beim Erfassen | Todoist Quick Add: Erinnerung mit „!“ direkt gefolgt von der Zeit, Beispiele „!14:00“, „!30 min before“. [Todoist-Hilfe](https://todoist.com/help/articles/task-quick-add-va4Lhpzz) | In Glide ist „!“ bereits Wichtigkeit (`!hoch`); deshalb deutsche Wörter („erinnern 9 Uhr“, „Erinnerung 30 min vorher“) und `/erinnern`, sichtbar als Chip. | KO03 |
| Mehrere Zeilen einfügen | Todoist fragt nach dem Einfügen einer Liste „Add X tasks?“ mit „Cancel“, „Add 1 task“, „Add X tasks“; vorher gewählte Felder gelten für alle. [Todoist-Hilfe](https://www.todoist.com/help/articles/add-or-manage-multiple-tasks-in-todoist-PcPoskdUp) | Gleiches Muster mit drei Wahlmöglichkeiten; jede Zeile durch den deutschen Parser. | KO05 |
| Vorgeschlagene Aufgaben, Routinen | TickTick 8.0 (01/2026) mit „Suggested Tasks“ im Heute-Bereich; Juni 2026 Erinnerungen, die bis zur Erledigung wiederholen ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/), [Releasebot, Dritte](https://releasebot.io/updates/ticktick)). Sunsama wird in Rezensionen 2026 als geführtes Tagesritual mit Überplanungswarnung beschrieben (Dritte, z. B. [Asian Efficiency](https://www.asianefficiency.com/schedule-management/sunsama-review/)) | Glide hat Vorschlag und Überplanungshinweis seit 3.33.13/3.33.14. Wiederkehrende Morgen-/Abendabläufe gehören sichtbar in „Heute“, ohne Gewohnheitsstatistik. | AU06 |
| Erscheinungsbild wie System | TIP 750 (Status Final, Ziel Tk 9.1): `wm attributes -appearance light/dark/auto`, `winfo isdark`, virtuelle Ereignisse `<<AppearanceChanged>>`. [TIP 750](https://core.tcl-lang.org/tips/doc/main/tip/750.md). Auf dem Referenz-Mac liefert Tk 9.0.3 `tk::unsupported::MacWindowStyle isdark` (geprüft am 08.10.2026: 1 im Dunkelmodus) | Erkennung je Plattform mit Rückfall: macOS über Tk, Windows über die Registry der Standardbibliothek, Linux über die Desktop-Einstellung; unter Tk 9.1 über `winfo isdark`. Keine Abhängigkeit. | N01 |
| Laufzeit | Tcl/Tk 9.1.0 am 29.09.2026 mit Screenreader-Unterstützung ([Tcl/Tk 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html), [`tk accessible`](https://www.tcl-lang.org/man/tcl9.1/TkCmd/accessible.html)). python.org führt Python 3.14.8 (30.09.2026); der macOS-Installer bringt seit 3.14.5 Tk 9.0.3 ([python.org](https://www.python.org/downloads/mac-osx/), [Ankündigung](https://discuss.python.org/t/python-org-macos-installer-users-of-tkinter-python-3-14-with-tcl-tk-9-0-3-instead-of-8-6-17/107206)) | Screenreader bleibt an die Paketierung (D15/G26) gebunden, weil die Installer noch Tk 9.0 liefern. I5 auf 3.14.8 aktualisieren; W09 (Absturz mit 3.14.8 unter Windows) weiter beobachten. | N12, I5 |
| Lokaler Planer | Super Productivity 19.0.1 (laut Softpedia 15.09.2026, Dritte): Live-Markdown in Notizen, Mehrfachauswahl mit Sammelaktionen, Wiederherstellungsschnappschüsse auf dem Gerät, deutliche Hervorhebung eines über die Suche erreichten Elements. [Softpedia](https://mac.softpedia.com/progChangelog/Super-Productivity-Changelog-143674.html) | Bestätigt Glides Richtung (Sammelaktionen, Sicherungen); konkret übernehmbar: Fundstelle nach der Suche hervorheben, Sicherungsstände vergleichbar machen. | G14h, F-03 |
| Wissensbasis | Obsidian 1.14.3 (29.09.2026): Gruppieren in Bases über ein Menü, neu gestalteter Leerzustand mit direkten Anlegewegen. [Changelog](https://obsidian.md/changelog/2026-09-29-desktop-v1.14.3/) | Leerzustände mit genau einem klaren Anlegeweg. | U20 |
| Felder am Objekt | iOS 27 Erinnerungen: ein Metadatenrahmen um die aktive Erinnerung ersetzt die Leiste über der Tastatur (9to5Mac, 29.09.2026). [9to5Mac](https://9to5mac.com/2026/09/29/heres-everything-new-for-reminders-in-ios-27/) | Stützt N05/KO04 (Inspektor, Felder am Objekt); weiter an I7 gebunden. | N05, KO04 |
| Notion | Keine offizielle Veröffentlichung nach dem 28.08.2026 gefunden; Notion 3.6 (01.07.2026) mit externen Agenten. [Releases](https://www.notion.com/releases/2026-07-08) | Keine neue Konsequenz; Q3 bleibt. | – |

**Grenzen dieser Recherche:** Für macOS 27 Erinnerungen und Sunsamas Routinen fanden sich keine Herstellerangaben; Aussagen Dritter sind nicht geprüft. Preise und Tarife wurden nicht erneut geprüft.
