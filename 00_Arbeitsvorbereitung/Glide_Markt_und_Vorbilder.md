# Glide – Markt und Vorbilder

Stand 13.10.2026 · Glide 3.39.0 · Hersteller-Matrix vom 01.10.2026, gezielte Abgleiche 05./07.10.2026, Sprintrecherche 08.10.2026, Wettbewerbs- und Open-Source-Analyse mit Codeprüfung 13.10.2026 (§9); Glide-Codeabgleich 09.10.2026 und 13.10.2026 (3.39.0)

Zusammengeführt am 03.10.2026 aus der Konkurrenz- und Featurematrix und der Konkurrenzübersicht vom 01.10.2026; diese hatten die älteren Recherchen vom 16.–25.09.2026, den Funktionsvergleich zur Zeichenfläche, die SVG-Untersuchung und das Konzept „Seiten wie Notion“ bereits eingeordnet. Am 06.10.2026 um die Wettbewerbsteile des nicht übernommenen Richtungsentwurfs vom 03.10.2026 ergänzt: Belegstufen, Steckbriefe mit Stärke, Grenze und Bedeutung, die ungekürzte Matrix, der Vergleich nach Dimensionen und überholte Aussagen. Die Vorfassungen trägt Git. Die Lücken N01–N20 und G01–G32 stehen mit Status im [Entwicklungsplan](Glide_Entwicklungsplan.md).

**Verlässlichkeit:** Glides Spalte stammt aus dem Code (Stand 3.35.0, abgeglichen am 09.10.2026). Die breite Matrix beruht auf Herstellerangaben und Berichten vom 01.10.2026; die Kurzfassung zu Glide, ChatGPT Space und Notion in Abschnitt 1.1 und der gezielte Abgleich in Abschnitt 6 berücksichtigen die Recherche vom 05.10.2026. Es liegt kein praktischer Vergleichstest aller Produkte vor. Vorteile, Positionierung und Übertragbarkeit sind Einschätzungen, keine Messwerte; veränderliche Herstellerangaben vor neuen Entscheidungen erneut prüfen.

**Überholt:** Ältere Analysen vom 16.–18.09.2026 (in Git) enthalten Aussagen, die nicht mehr gelten:

1. „Notion ist kein Ziel“ – seit der Aussage des Inhabers vom 26.09.2026 ist Notions Seitenkonzept ausdrücklich gewünscht, nur nicht der Baukasten.
2. Bearbeitungstag getrennt von der Fälligkeit ist kein exklusives Glide-Merkmal (Things: Startdatum/Deadline; Todoist: Datum/Deadline).
3. Natürliche Eingabe ist bei Todoist nicht nur Pro; Things hat natürliche Datumseingabe in Termin- und Erinnerungsfeldern.
4. Mobile bedeutet nicht zwingend Konto und Server (Super Productivity, Joplin); Glides Desktop-Fokus ist eine Entscheidung (D03), keine technische Notwendigkeit.
5. Alte Ausschlüsse (Rich Text, Seiten, Rückverweise, Animation) sind durch spätere Entscheidungen ersetzt; es gelten [Produktgrenzen](../01_Repository/Glide/docs/01_PRODUCT_CONSTRAINTS.md) und [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md).

## 1. Ergebnis

1. Glides Funktionsbreite ist für ein Ein-Personen-Projekt außergewöhnlich. In der **Tagesführung** (Bearbeitungstag ≠ Fälligkeit, Kapazität, Zeitblöcke, Heute/Demnächst, Tagesbeginn und -abschluss, Zeiterfassung) liegt Glide auf dem Niveau spezialisierter Planer. Die Kombination aus Pixel-Werkstatt und Pinnwand mit echten Aufgabenkarten ist im untersuchten Feld besonders; eine weltweite Alleinstellung wurde nicht nachgewiesen.
2. **AFFiNE** und **AppFlowy** decken die Kombination „Seiten + Datenbanken + Leinwand + lokal“ quelloffen ab. Glides Abgrenzung läuft deshalb über die Tagesführung, nicht über die Kombination.
3. **Verbleibende Lücken:** Barrierefreiheit über Tk 9.1 und ein Paket mit eigenem Python (beide im bestätigten Sprint); Inspektor und Felder am Objekt sind seit 3.38.0 geliefert. Lücken aus der Codeanalyse vom 13.10.2026 (Wiederholen, Wiederholungsregeln, gespeicherte Ansichten, Seitenkarten, offene Ausgabeformate) stehen in §9.4. Seit dem Sprint vom 08./09.10.2026 geschlossen: Erscheinungsbild „wie System“, Fundstellen im Dokument, Bilder in Druck/Markdown, erklärte Filter und geprüfte KI-Änderungsvorschläge; ein Suchindex ist nach Messung nicht nötig. Automatisch geprüft auf dem Referenz-Mac; menschliche Abnahme offen. Bewusst nicht: Erinnerungen bei geschlossener App, eigener Sync und Mobil.
4. **Stand der Technik 2026 ist KI** (Todoist Ramble und MCP, Notion Custom Agents, Apple Intelligence). Glides Antwort ist entschieden (Q3): Austausch über Dokumente statt Schnittstelle (G24).
5. **Bedienkomfort und Informationsarchitektur** lagen hinter den Vorbildern: nicht zu wenig Funktion, sondern zu viel dauerhaft sichtbar. UX1 (3.33.11–3.33.16) und die ruhige Oberfläche (3.33.21) haben die Kopfzeile auf vier Symbole, Hinweise auf Bedarf und die Pinnwand auf eine Werkzeugzeile gebracht; die Bedienfläche über dem Inhalt ist noch nicht neu gemessen.

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

**Glide-Stand 3.35.0 (Codeabgleich 09.10.2026):** Tagesvorschlag und Fokus seit 3.33.14, Aufgaben im Notiztext seit 3.33.15, gemeinsame Befehlspalette seit 3.33.16, Wochenplanung und Verweise mit Rückverweisen seit 3.33.17, Live-Listen, Titelbilder und Vorlagenvorschau seit 3.33.18 (Format 23). Im Sprint dazu: Termine überspringen, Erinnerung beim Erfassen und Routinen (3.33.20), hell/dunkel nach System und schmale Seitenleiste (3.33.21), Seitenbilder in Druck und Markdown, Fundstellen und erklärte Filter (3.34.0), geprüfte KI-Änderungsvorschläge und Sicherungsvergleich (3.35.0). Jede Version auf dem Referenz-Mac automatisch geprüft; Windows zuletzt 3.33.18, menschliche Abnahme offen. Herstellerangaben behalten ihre ausdrücklich genannten Recherchezeitpunkte. Details: [Funktionen](../01_Repository/Glide/docs/20_FUNKTIONEN.md), [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md).

**Eigener Produktabgleich 12.10.2026:** Fundament/Tempo 3.36.0 und Logo/Symbole 3.37.0 sind inzwischen mit Mac-/Linux-/Windows-Vollprüfung geliefert. Inspektor, direkte Felder, Textstufen und dezente Übergänge sind mit 3.38.0 und grüner Mac-/Linux-/Windows-Vollprüfung geliefert; Auswahl-/Menübefunde sind korrigiert und nachgeprüft. Menschliche Bedienung/DPI bleiben getrennt offen. Herstellerangaben oben werden dadurch nicht als neu recherchiert ausgegeben. Bestätigter Umfang und Folgepakete stehen im [Plan §15.7](Glide_Entwicklungsplan.md#157-bestätigter-gesamtplan-acht-produktionsversionen).

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
| | Animation | ○ | – | – | – | – | – | – | – | – | – | G17 durch D18 gewählt, Umsetzung in Paket 5 (3.40.0) |
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
| | Erscheinungsbild wie System | ● | ● | ● | ● | ● | ● | ● | ● | ● | ● | N01 ✅ 3.33.21 |
| | Rückgängig auch für Strukturänderungen | ● | ● | ◐ | ● | ◐ | ◐ | ● | ● | ● | ● | 20 Schritte, Bestandswächter |
| | Hilfe in der App | ● | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Handbuch, Kürzel; Hinweise je Ansicht einklappbar seit 3.33.16 (D11/U02) |
| | Beispielinhalt | ◐ | ● | ● | ● | ● | ◐ | ◐ | ◐ | ◐ | ◐ | Showcase und Rundgang; Einstieg bewusst nicht |
| | Screenreader | ○ | ? | ? | ● | ? | ? | ? | ? | ? | ● | N12 nach Tk 9.1 |

### 4.1 Vergleich nach Dimensionen

Einordnung der Matrix und der UX-Befunde; die Messwerte stehen im [Entwicklungsplan, Abschnitt 10](Glide_Entwicklungsplan.md#10-messbare-ziele).

| Dimension | Maßstab | Glide 3.35.0 (Codeabgleich 09.10.2026) | Lücke | Konsequenz |
|---|---|---|---|---|
| Funktionen | Notion (Breite), TickTick (Planung + Fokus), AFFiNE (Seite + Leinwand) | sehr breit; Verweise, Fokus, Aufgaben im Notiztext, Live-Liste und Titelbild seit 3.33.14–3.33.18, Routinen seit 3.33.20; Bilder in Druck/Markdown, Trefferhervorhebung und erklärte Filter seit 3.34.0, Sicherungsvergleich seit 3.35.0 | im Sprint geschlossen; offen bleiben die an Inhaberentscheidungen gebundenen Pakete (E-S1–E-S8) | keine neue Breite ohne Entscheidung (Entwicklungsplan §11) |
| Alltag | Things (Heute → Demnächst), Sunsama (Ritual) | Heute/Demnächst, Tagesvorschlag, verfügbare Zeit, Fokus, Wochenplanung; seit 3.33.20 Termine überspringen, Routinen in „Heute“, Erinnerung beim Erfassen | keine Gewohnheitsstatistik (bewusst, G06) | geschlossen mit KO02, AU06, KO03 |
| Komfort | Todoist (Erfassung), Apple (Felder am Objekt) | Feldchips, Einplanen-Menü, gemeinsame Palette, Rückgängig überall; seit 3.33.20 mehrzeiliges Einfügen, zuletzt benutzte Ziele, „+“ und Umschalt+Enter | Detailbearbeitung doppelt (bis 3.37.0); kein Wiederholen für Aufgaben- und Strukturänderungen (Codeprüfung 13.10.2026) | Inspektor N05/KO04 mit 3.38.0 geliefert; Wiederholen als Vorschlag FP-01 |
| Tempo | Things, Apple: jede Aktion unter 100 ms | 3.33.19 auf dem Referenz-Mac: Abhaken 17 / 61 / 118 ms bei 1.000 / 5.000 / 10.000 Punkten (im Akkubetrieb bis 119 ms bei 5.000); unveränderte Startseite 0,3 ms, Neuaufbau 270–300 ms; Seite mit 30 Bildern beim Tippen 3 ms | Neuaufbau der Startseite und Einstellungsfenster (≈ 560 ms) begrenzt durch Tk-Zeichnen; Abhaken über 5.000 Punkte linear | Stufe 0 bis auf den Neuaufbau erledigt (P04, P06r, P03r, P08c in 3.33.19); weitere Gewinne nur mit anderem Zeichenweg |
| Gestaltung | Things, Notion: viel Weißraum, wenige Bedienelemente | höchstens 4 Kopfsymbole, keine Symbole mit Mehrfachbedeutung, einklappbare Hinweise (3.33.16); „+“ statt zweier Textknöpfe (3.33.20); hell/dunkel nach System, neutrale aktive Zustände, schmale Seitenleiste (3.33.21) | Referenzentwürfe für Heute, Liste und Seite (Bild 1, D21) | OB02/OB03 mit 3.38.0 geliefert |
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

Gezielte Recherche am 08.10.2026 zu den Aufgaben des Sprints ([Entwicklungsplan §14](Glide_Entwicklungsplan.md#14-sprint-ab-08102026-aufgabenkatalog)). Herstellerseiten und Primärquellen haben Vorrang; Berichte Dritter sind als solche gekennzeichnet. Kein Praxistest. **Fakt** = in der Quelle belegt, **Folgerung** = eigene Einschätzung für Glide.

| Thema | Fakt (Quelle, Abruf 08.10.2026) | Folgerung für Glide | Aufgabe |
|---|---|---|---|
| Wiederholungen | Things 3.23 (Blogbeitrag 19.08.2026): Wiederkehrende Aufgaben lassen sich vor ihrem Termin erledigen, die nächste Kopie folgt der Regel; beim Verschieben fester Reihen „Make Exception“ oder „Update Rule“; „Create Next Copy“; mehrere Reihen pausieren. Ein eigenes „Überspringen“ nennt der Beitrag nicht. [Things-Blog](https://culturedcode.com/things/blog/2026/08/repeating-to-dos-refined/) | Frühes Erledigen mit genau einem Folgetermin ist Erwartung. Glide braucht zusätzlich einen ausdrücklichen Weg, einen oder alle verpassten Termine zu überspringen, ohne Erledigung zu buchen. | KO02 ✅ 3.33.20 |
| Erinnerung beim Erfassen | Todoist Quick Add: Erinnerung mit „!“ direkt gefolgt von der Zeit, Beispiele „!14:00“, „!30 min before“. [Todoist-Hilfe](https://todoist.com/help/articles/task-quick-add-va4Lhpzz) | In Glide ist „!“ bereits Wichtigkeit (`!hoch`); deshalb deutsche Wörter („erinnern 9 Uhr“, „Erinnerung 30 min vorher“) und `/erinnern`, sichtbar als Chip. | KO03 ✅ 3.33.20 |
| Mehrere Zeilen einfügen | Todoist fragt nach dem Einfügen einer Liste „Add X tasks?“ mit „Cancel“, „Add 1 task“, „Add X tasks“; vorher gewählte Felder gelten für alle. [Todoist-Hilfe](https://www.todoist.com/help/articles/add-or-manage-multiple-tasks-in-todoist-PcPoskdUp) | Gleiches Muster mit drei Wahlmöglichkeiten; jede Zeile durch den deutschen Parser. | KO05 ✅ 3.33.20 |
| Vorgeschlagene Aufgaben, Routinen | TickTick 8.0 (01/2026) mit „Suggested Tasks“ im Heute-Bereich; Juni 2026 Erinnerungen, die bis zur Erledigung wiederholen ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/), [Releasebot, Dritte](https://releasebot.io/updates/ticktick)). Sunsama wird in Rezensionen 2026 als geführtes Tagesritual mit Überplanungswarnung beschrieben (Dritte, z. B. [Asian Efficiency](https://www.asianefficiency.com/schedule-management/sunsama-review/)) | Glide hat Vorschlag und Überplanungshinweis seit 3.33.13/3.33.14. Wiederkehrende Morgen-/Abendabläufe gehören sichtbar in „Heute“, ohne Gewohnheitsstatistik. | AU06 ✅ 3.33.20 |
| Erscheinungsbild wie System | TIP 750 (Status Final, Ziel Tk 9.1): `wm attributes -appearance light/dark/auto`, `winfo isdark`, virtuelle Ereignisse `<<AppearanceChanged>>`. [TIP 750](https://core.tcl-lang.org/tips/doc/main/tip/750.md). Auf dem Referenz-Mac liefert Tk 9.0.3 `tk::unsupported::MacWindowStyle isdark` (geprüft am 08.10.2026: 1 im Dunkelmodus) | Erkennung je Plattform mit Rückfall: macOS über Tk, Windows über die Registry der Standardbibliothek, Linux über die Desktop-Einstellung; unter Tk 9.1 über `winfo isdark`. Keine Abhängigkeit. | N01 ✅ 3.33.21 |
| Laufzeit | Tcl/Tk 9.1.0 am 29.09.2026 mit Screenreader-Unterstützung ([Tcl/Tk 9.1](https://www.tcl-lang.org/software/tcltk/9.1.html), [`tk accessible`](https://www.tcl-lang.org/man/tcl9.1/TkCmd/accessible.html)). python.org führt Python 3.14.8 (30.09.2026); der macOS-Installer bringt seit 3.14.5 Tk 9.0.3 ([python.org](https://www.python.org/downloads/mac-osx/), [Ankündigung](https://discuss.python.org/t/python-org-macos-installer-users-of-tkinter-python-3-14-with-tcl-tk-9-0-3-instead-of-8-6-17/107206)) | Screenreader bleibt an die Paketierung (D15/G26) gebunden, weil die Installer noch Tk 9.0 liefern. I5 auf 3.14.8 aktualisieren; W09 (Absturz mit 3.14.8 unter Windows) weiter beobachten. | N12, I5 |
| Lokaler Planer | Super Productivity 19.0.1 (laut Softpedia 15.09.2026, Dritte): Live-Markdown in Notizen, Mehrfachauswahl mit Sammelaktionen, Wiederherstellungsschnappschüsse auf dem Gerät, deutliche Hervorhebung eines über die Suche erreichten Elements. [Softpedia](https://mac.softpedia.com/progChangelog/Super-Productivity-Changelog-143674.html) | Bestätigt Glides Richtung (Sammelaktionen, Sicherungen); konkret übernehmbar: Fundstelle nach der Suche hervorheben, Sicherungsstände vergleichbar machen. | G14h ✅ 3.34.0, F-03 ✅ 3.35.0 |
| Wissensbasis | Obsidian 1.14.3 (29.09.2026): Gruppieren in Bases über ein Menü, neu gestalteter Leerzustand mit direkten Anlegewegen. [Changelog](https://obsidian.md/changelog/2026-09-29-desktop-v1.14.3/) | Leerzustände mit genau einem klaren Anlegeweg. | U20 ✅ 3.33.20 |
| Felder am Objekt | iOS 27 Erinnerungen: ein Metadatenrahmen um die aktive Erinnerung ersetzt die Leiste über der Tastatur (9to5Mac, 29.09.2026). [9to5Mac](https://9to5mac.com/2026/09/29/heres-everything-new-for-reminders-in-ios-27/) | Stützt N05/KO04 (Inspektor, Felder am Objekt); weiter an I7 gebunden. | N05, KO04 ○ (I7) |
| Notion | Keine offizielle Veröffentlichung nach dem 28.08.2026 gefunden; Notion 3.6 (01.07.2026) mit externen Agenten. [Releases](https://www.notion.com/releases/2026-07-08) | Keine neue Konsequenz; Q3 bleibt. | – |

**Grenzen dieser Recherche:** Für macOS 27 Erinnerungen und Sunsamas Routinen fanden sich keine Herstellerangaben; Aussagen Dritter sind nicht geprüft. Preise und Tarife wurden nicht erneut geprüft.

## 8. Quellenabgleich für die neue Planung (09.10.2026)

Gezielte Primärquellen, kein praktischer Produktvergleich. Die Folgerungen sind Vorschläge für die gemeinsame Planung, keine Inhaberentscheidungen. Aufgaben und Auswahl ausschließlich im [Entwicklungsplan §15](Glide_Entwicklungsplan.md#15-neuer-feature-sprint-ab-09102026-gemeinsame-planung).

| Quelle | Belegtes Verhalten | Eigene Folgerung für Glide |
|---|---|---|
| [Aseprite: Spritesheets](https://www.aseprite.org/docs/sprite-sheet/) | Mehrere Frames in einem PNG, horizontal, vertikal oder als Raster; eigener Exportweg | E-S1 kann ohne GIF mit einem brauchbaren Austauschformat beginnen. GIF und Bearbeitungstiefe bleiben getrennte Auswahlfragen. |
| [Notion: Export](https://www.notion.com/help/export-your-content) | Markdown für Seiten, CSV für Datenbanken, ZIP mit getrennten Seiten/Dateien; Hinweisblöcke werden als HTML exportiert | E-S4: klar begrenzter Notion-Import mit Verlustbericht. V02 als zusätzlicher Vorschlag: wiederholte Übernahme desselben Exportinhalts erkennt unveränderte Quellen und zeigt Konflikte vor einer Änderung. Kein Anspruch auf vollständige Notion-Kompatibilität. |
| [Sunsama: Tagesplanung](https://help.sunsama.com/docs/usage-guides/daily-planning/) | Optionale Hinweise zur eingestellten Planungszeit; Aufwandsbilanz mit Überlastwarnung; Aufgaben ausdrücklich auf spätere Tage oder in den Vorrat verschieben | E-S3 bekommt getrennte Optionen für Vorgabe und Tiefe. V01: aus Glides vorhandener Überplanungswarnung direkt eine vom Nutzer ausgewählte Umplanung mit Vorher-/Nachher-Bilanz öffnen. Keine automatische Verteilung. |
| [PyInstaller: Voraussetzungen](https://pyinstaller.org/en/stable/requirements.html) | Dokumentation 6.22.3; Paketierung je Zielplattform, Linux benötigt Systemwerkzeuge; macOS-Pakete sind an die Bauumgebung gebunden | E-S5 muss native Bau- und Prüfumgebungen je Zielsystem einplanen. Ein erfolgreicher Mac-Bau ist kein Nachweis für Windows oder Linux. Werkzeugversion, Lizenz und Tk-Mitnahme vor der Entscheidungsrunde separat prüfen. |
| [Tk 9.1: accessible](https://www.tcl-lang.org/man/tcl9.1/TkCmd/accessible.html) | Rollen, Namen, Werte, Zustände, Aktionen, virtuelle zugängliche Objekte sowie Auswahl-/Fokusereignisse | N12 ist mehr als neue Beschriftungen: vollständiger Kernablauf braucht Tk-9.1-Laufzeit und tatsächliche Screenreader-Abnahme; erste Stufe und vollständiger Umfang getrennt anbieten. |

V01 und V02 sind neue Vorschläge aus diesen Quellen und dem vorhandenen Verhalten (`planning_summary`, ICS-UID-Duplikaterkennung). N13 (selektive Seitenwiederherstellung) ist bereits ein Zukunftskandidat aus dem Plan, keine neu entdeckte Lücke. Beim Abgleich die bislang falsche Glide-Markierung „Erscheinungsbild wie System“ in der Matrix auf den belegten Stand 3.33.21 berichtigt; keine Herstellerzeile neu bewertet.

**Vertiefung 10.10.2026 für E-S5:** [PyInstaller 6.22.3 – Lizenz](https://pyinstaller.org/en/stable/license.html) beschreibt GPL 2.0 mit Bootloader-Ausnahme und Apache 2.0 für einzelne Dateien; die Ausnahme erlaubt kommerzielle Bundles, Rechte der eingebetteten Abhängigkeiten bleiben zu beachten. [Betriebsweise](https://pyinstaller.org/en/stable/operating-mode.html) belegt Mitnahme des Python-Interpreters und plattformgebundene Bauten; ein Ordnerpaket ist leichter zu prüfen und startet ohne Entpacken einer Ein-Datei-App. Der [Tk-Hook im Tag v6.22.3](https://github.com/pyinstaller/pyinstaller/blob/v6.22.3/PyInstaller/hooks/hook-_tkinter.py) sammelt Tcl/Tk-Daten und bricht bei fehlenden Datenverzeichnissen ab. Die [macOS-Hinweise](https://pyinstaller.org/en/stable/feature-notes.html) beschreiben Ad-hoc-Signierung und warnen vor `argv_emulation` mit Tk. Folgerung für D27: Version fest pinnen, eigene Ressourcensuche und dynamische Importe ausdrücklich aufnehmen, Tcl/Tk und tkdnd nativ prüfen, öffentliche Signatur separat. Keine Lizenzentscheidung für Glide daraus ableiten. Notions Exportbeschreibung erneut geprüft: Datenbank-CSV und HTML-Hinweisblöcke müssen in Vorschau/Verlustbericht ausdrücklich eingeordnet werden; kein Datenbank-Nachbau.

**Laufzeitabgleich 10.10.2026 für N12:** Die [offizielle Tk-9.1.0-Veröffentlichung](https://github.com/tcltk/tk/releases/tag/core-9-1-0) nennt den 29.09.2026 als erste stabile Fassung, einschließlich Screenreader-Unterstützung. Die Distribution besteht aus Quellcode; angehängte automatische Binärbauten sind laut Hersteller ungeprüft und gegebenenfalls unsigniert. Die [Accessibility-Schnittstelle](https://www.tcl-lang.org/man/tcl9.1/TkCmd/accessible.html) bietet Rollen, Namen, Werte, Zustände und Fokus-/Auswahlereignisse; Canvas-Inhalt erhält keine automatische semantische Bedienbarkeit. Folgerung: N12 braucht eine ausdrücklich geprüfte Python-/Tk-9.1-Laufzeit und zugängliche Alternativen für eigene Canvas-Flächen sowie tatsächliche Screenreader-Abnahme. Die bislang geprüfte Glide-Laufzeit Tk 9.0.3 erfüllt diese Voraussetzung noch nicht.

## 9. Wettbewerbs- und Open-Source-Analyse (13.10.2026)

Auftrag des Inhabers vom 12./13.10.2026 (Kern): Markt, relevante Open-Source-Repositories und ihre Architektur untersuchen; die besten Ansätze kritisch bewerten und in die bestehende Glide-Architektur übertragen, ohne Notion zu kopieren. Leitfrage: Welche Konzepte machen Glide leistungsfähiger, intuitiver und langfristig wartbar, ohne Kernkompetenz und Stabilität zu gefährden?

**Methode und Grenzen:** Glide-Seite aus dem Code 3.39.0 (Apphash `7995ecbc…`, Abgleich in der [Analyse §8](Glide_Analyse.md#8-bestandsaufnahme-und-gap-analyse-13102026)). Fremdcode ausschließlich gelesen: die lokale AFFiNE-Kopie (Canary-Fassung 0.27.5, abgelegt 11.10.2026) und flache Klone vom 13.10.2026, je mit Commit; Lizenz und Aktivität über die GitHub-API. Kein Fremdcode ausgeführt, installiert oder in Glide übernommen. Herstellerangaben und Berichte Dritter sind als solche markiert; kein Praxistest. **Fakt** = in Code oder Quelle belegt, **Folgerung** = eigene Einschätzung, **Vorschlag** = Paket im [Entwicklungsplan §16](Glide_Entwicklungsplan.md#16-vorschläge-aus-wettbewerbs--und-open-source-analyse-13102026); Vorschläge sind keine Inhaberentscheidungen.

**Übertragbarkeit** (Spalte „Ü“): **1** direkt als technische Grundlage nutzbar · **2** mit Anpassungen übertragbar (Algorithmus/Semantik portieren) · **3** nur Architekturvorbild · **4** nur UX-Inspiration · **5** für Glide ungeeignet. Wiederverwendung von Quellcode ist in keinem Fall vorgesehen: Glide ist Python/Tk, alle untersuchten Projekte sind TypeScript, Rust, Dart, Go oder C++.

### 9.1 Steckbriefe der primär untersuchten Projekte

| Projekt (geprüfte Fassung) | Technik, Lizenz, Aktivität | Belegtes Kernkonzept (Fakt) | Grenze | Bedeutung für Glide (Folgerung) | Ü |
|---|---|---|---|---|---|
| **AFFiNE** (lokale Canary-Kopie 0.27.5; stabile 0.27.0 vom 15.07.2026; Releases bis Canary 12.10.2026) | TypeScript/React, Editor-Framework BlockSuite auf Yjs-CRDT, Electron, Rust-Teile, NestJS-Server. Lizenz laut Wurzel-`LICENSE`: MIT, ausgenommen `packages/backend` und `packages/common/native` (eigene EE-Lizenz); GitHub-API meldet `NOASSERTION`. Täglich aktiv | Ein Dokument hat Seiten- und Leinwandmodus über dieselben Blöcke; Datenbankblock mit Ansichten Tabelle/Kanban/Kalender als serialisierbare Ansichtsdefinitionen (Filterbaum, Gruppierung, Sortierung, Spalten); Dokumentverlauf über Schnappschüsse je Dokument (`nbstore/src/storage/history.ts`); lokaler Volltextindex mit BM25+; KI über den Server (Anbieter OpenAI, Anthropic, Gemini, fal; BYOK experimentell seit 0.27.0, auch „OpenAI-kompatible“ Endpunkte); 0.27.0 bringt Kalenderansicht und Importer für OneNote, Obsidian, Bear, Notion ([Herstellerblog](https://affine.pro/blog/whats-new-july-update-2026)) | keine persönliche Tagesführung (Bearbeitungstag, Kapazität, Zeitblöcke) im untersuchten Code; KI nur über Server; sehr großer Abhängigkeitsbaum | Stärkstes Vorbild für **Ansichtsdefinitionen** (FP-03), **Seiten als Karten auf der Fläche** (FP-04) und **Vorschau verlinkter Dokumente** („Peek“, WA-11). CRDT, Electron und Editor-Engine passen nicht zu Tk | 3 / 4 / 5 |
| **AppFlowy** (Release 0.14.2 vom 10.09.2026 laut [Release-Spiegel, Dritte](https://newreleases.io/project/github/AppFlowy-IO/AppFlowy/release/0.14.2); Klon `5cf3a36` vom 26.06.2026 trägt noch 0.11.4) | Flutter/Dart und Rust (`flowy-*`), SQLite, `flowy-sqlite-vec`; AGPL-3.0; aktiv (Push 08.10.2026) | Datenbank mit Grid/Board/Kalender, seit 0.14.2 Formularansicht; seit 0.13.0 ist jede Datenbankzeile eine eigene Seite (Dritte). Lokale KI über einen **separat installierten Ollama-Server**, Vorgaben `llama3.1` und `nomic-embed-text`, Vektorsuche in sqlite-vec (`flowy-ai/src/local_ai/controller.rs`, `resource.rs`) | AGPL; lokale KI setzt Fremdinstallation und mehrere GB Modelldaten voraus | Belegt, dass lokale KI als **externer Dienst plus schlanker Client** gebaut wird; Glide könnte das ohne Python-Abhängigkeit über die Standardbibliothek ansprechen, berührt aber Q3 (WA-10). „Zeile = Seite“ bestätigt Glides Inspektor-/Beschreibungsweg statt neuer Objektart | 3 / 5 |
| **Super Productivity** (19.2.0, Klon `c4c6959` vom 12.10.2026) | Angular, Electron/Capacitor; MIT; sehr aktiv | Lokal und ohne Konto; Wiederholungsmodell mit Intervall für jede Periode, n-tem Wochentag, letztem Monatstag, Folgetermin ab Erledigung, „erst nach Erledigung neu“, verpasste überspringen, gelöschte Einzeltermine, Unteraufgaben-Vorlagen (`features/task-repeat-cfg/task-repeat-cfg.model.ts`); Boards aus Filtern mit ein- und ausgeschlossenen Tags (`features/boards/boards.model.ts`); Arbeitsprotokoll mit Export (`features/worklog`); Synchronisation über Operationsprotokoll, Vektoruhren und Konfliktauflösung (`op-log/`: 159 Dateien in `sync` und `persistence`, 411 insgesamt, jeweils einschließlich Tests); Plugin-API und lokale REST-API | Synchronisation erzeugt hohe dauerhafte Komplexität | Direktester lokaler Planer-Vergleich. **Wiederholungssemantik** ist das konkreteste Übertragungsziel (FP-02); Boards mit Ausschluss-Tags stützen FP-03; Zeitprotokoll stützt WA-08. Sync-Aufwand bestätigt G23 ✕ | 2 / 3 / 5 |
| **Vikunja** (Klon `4e2a899` vom 12.10.2026) | Go und Vue; AGPL-3.0; aktiv | Jede Projektansicht (Liste, Gantt, Tabelle, Kanban) trägt eigene Filterabfrage und Spaltenmodus „manuell“ oder „aus Filtern“, eine Erledigt-Spalte setzt den Status (`pkg/models/project_view.go`); elf Beziehungsarten mit automatischer Gegenrichtung (`task_relation.go`); Filtersprache mit Komplexitätsgrenze | Team- und Serverprodukt | Ansicht = Filter + Darstellung (FP-03). Glides `links`, `blocked_by` und Unterpunkte decken die persönlichen Fälle ab; **keine neuen Beziehungsarten** | 3 / 4 |
| **ai-notion-clone** (EduartePaiva, Klon `c68ece5` vom 01.01.2025) | Next.js 15, React 19, Editor BlockNote 0.21, Liveblocks (Dienst) mit Yjs, Clerk (Anmeldedienst), Postgres/Drizzle, KI in separatem Cloudflare-Worker-Repository; MIT; rund 3.100 Zeilen TypeScript; seit 01.01.2025 kein Commit, 0 Sterne | Dokumente mit Echtzeitbearbeitung, Einladen (Besitzer/Bearbeiter), Übersetzen, „Chat to Document“. **Fehler im Code:** `src/components/chat-to-document.tsx` sendet als `question` den Dokumenttext statt der eingegebenen Frage; die Frage erreicht den KI-Dienst nie. `todo.md` nennt „finish base tutorial“ | Lernprojekt nach Tutorial; ohne eigene Persistenz des Dokuments, ohne Aufgaben, ohne Tests über eine Hilfsfunktion hinaus | Bestätigt: Ein „Notion-Klon“ dieser Art ist Editorbibliothek plus Clouddienste. Für Glide nur die Bedienidee „mit dem Dokument sprechen“, die das Kontextpaket (G24) lokal-kontrolliert abdeckt | 5 (Code) / 4 |
| **Blink.new-Klone** ([AI-Enhanced Notion Clone](https://blink.new/p/ai-notion-clone-c2b1mv4v), [NotionAI Workspace](https://blink.new/p/notion-ai-clone-4kzth6kt), Abruf 13.10.2026) | laut Seite Vite/React/TypeScript mit vom Anbieter verwalteter SQL-Datenbank, Anmeldung und Hosting; Codeexport nach GitHub angeboten; keine Lizenzangabe, kein Prompt, kein öffentliches Repository | Editor, verschachtelte Seiten, KI-Textbearbeitung bzw. KI-Suche; Erstellung „in etwa einer bzw. fünf Minuten“ (Herstelleraussage) | Kein überprüfbarer Code; Datenhaltung, Anmeldung und Hosting beim Anbieter; keine Migrationen, Tests oder Datenformatverträge erkennbar | **Prototypen, keine nachhaltig wartbare Grundlage.** Generatoren liefern schnell Oberflächen; Datenintegrität, Migration, Rückgängig und Prüfung – Glides eigentliche Stärken – liefern sie nicht. Keine Übernahme | 5 |
| **Buildin AI** ([buildin.ai](https://buildin.ai), Abruf 13.10.2026: Seite ohne lesbaren Inhalt) | kommerziell, kein Quellcode; laut Verzeichnis seit 09/2024, Freemium | Nur Dritte ([AI Indigo, 17.09.2026](https://aiindigo.com/blog/buildin-ai-review-the-all-in-one-workspace-reality-check-for-2026)): Wiki/Dokumente, Datenbanken, Kanban/Zeitleiste/Diagramme, Mindmaps umwandelbar in Seiten oder Einträge, KI strukturiert Notizen und Transkripte, **Linkvorschläge beim Tippen**, bezahlte Veröffentlichung | Offline/lokal, Plattformen und Export nicht belegt; Rezension nennt Lernkurve und schwache KI-Verknüpfungen | Positionierung „KI-Arbeitsbereich zum Bauen, Verwalten, Verkaufen“ ist Glide fremd. Übertragbar ist nur die Idee „Verknüpfung vorschlagen“, deterministisch als unverknüpfte Erwähnungen (FP-05). **Unbestätigt** | 4 |

### 9.2 Weitere Projekte und Produkte

| Produkt | Belegter Stand (Quelle, Abruf 12./13.10.2026) | Folgerung für Glide | Ü |
|---|---|---|---|
| Logseq | DB-Fassung 2.0 als öffentliche Beta seit 13.07.2026, SQLite wird kanonischer Speicher, Dateifassung als „Logseq OG“ getrennt ([Dritte](https://kompozy.io/news/logseq-2-0-db-version-beta)); AGPL-3.0 | Warnbeispiel bleibt: Speicherwechsel mit Datenverlustrisiko. D16 (JSON beschleunigen) bestätigt | 5 |
| Anytype | Desktop 0.54 mit Tabs (April 2026), Multi-Chats; Erinnerungen laut Forumstitel „local-first schwer“ ([Blog](https://blog.anytype.io/february-community-update-2026/)); Lizenz „Any Source Available“, kein OSI | Typisierte Objekte mit Relationen sind Standard; Glides feste Felder bleiben richtig. Glide hat lokale Erinnerungen bereits | 4 |
| SiYuan | 3.8.x mit erweiterten Datenbankansichten, KI-Agent und MCP ([Release-Spiegel](https://newreleases.io/project/github/siyuan-note/siyuan/release/v3.8.0)); CVE-2026-65605: unmaskierte Vorlagenspalte führt beim Ansehen einer Datenbank Code aus ([OSV](https://osv.dev/vulnerability/CVE-2026-65605)); AGPL-3.0 | Berechnete und Vorlagenfelder sind Angriffsfläche; Glides Verzicht auf Formelfelder senkt Risiko | 5 |
| Taskwarrior | Dringlichkeit als gewichtete Summe; Standardgewichte laut [Dokumentation](https://taskwarrior.org/docs/urgency/): +next 15, Fälligkeit 12, blockiert andere 8, Priorität 6/3,9/1,8, geplant 5, aktiv 4, Alter 2, blockiert −5, wartet −3. Laut Quellcode (`src/Task.cpp`) wächst der Fälligkeitsanteil linear von 0,2 (14 Tage vorher) auf 1,0 (7 Tage überfällig); MIT | Glides Tagesvorschlag ordnet bewusst nach erklärbaren Gründen. Übertragbar ist ein zusätzlicher Grund „gibt andere frei“ (WA-12), keine undurchsichtige Punktzahl | 2 |
| JSON Canvas | offenes Format 1.0 vom 11.03.2024: Knoten `text`/`file`/`link`/`group`, Kanten mit Seiten, Pfeilenden, Beschriftung, Farbe; Farbvorgaben „1“–„6“ ([Spezifikation](https://jsoncanvas.org/spec/1.0/)); Repository MIT | Glides Pinnwand (Karten, Bereiche, beschriftete Verbindungen mit Richtung) lässt sich verlustarm als `.canvas` ausgeben (FP-07). Eigener Schreiber in der Standardbibliothek | 1 |
| Notion | Desktop 3.7 vom 15.09.2026 laut [Wikipedia, Dritte](https://en.wikipedia.org/wiki/Notion_(productivity_software)); offizielle Notizen für September/Oktober nicht gefunden; Custom Agents, KI-Autofill, Skills (03/2026, Dritte) | Keine neue Konsequenz; Q3 bleibt | – |
| Obsidian | [1.14.3 vom 29.09.2026](https://obsidian.md/changelog/2026-09-29-desktop-v1.14.3/): Gruppieren in Bases über ein Menü, neue Leerzustände; 1.12.0 (10.02.2026): Kommandozeile, Rückverweise aus Canvas-Dateien | Gruppieren und Ansichten über demselben Bestand sind Standard (FP-03); Canvas als offenes Dateiformat (FP-07) | 4 |
| Todoist | [Changelog 2026](https://www.todoist.com/help/articles/2026-changelog-HD3jJAtLd), 10./17.09.2026: Filter in der Planungsseitenleiste des Kalenders, erledigte Wiederholungstermine erscheinen in Datumsansichten, Sync-Zurücksetzen verwirft keine ungesicherten Änderungen mehr | Erledigte Termine einer Serie sichtbar zu halten ist Erwartung (in FP-02 prüfen) | 4 |
| TickTick | 8.0 (04.01.2026): vorgeschlagene Aufgaben, Jahresansicht mit Heatmap ([AlternativeTo](https://alternativeto.net/news/2026/1/ticktick-8-0-adds-suggested-tasks-improved-yearly-monthly-views-and-customization-options/)); Juni 2026: Daueralarm bis zur Erledigung, Suchfilter (Dritte); KI-Sprachmodus und MCP **unbestätigt** | Glide hat Vorschlag und Heatmap; Daueralarm widerspricht der ruhigen Tagesführung | – |
| Microsoft Planner / To Do | Planner-Update 2026: Aufgabenchats, Whiteboard-Reiter und Loop-Komponenten entfallen ([Neowin](https://www.neowin.net/amp/microsoft-confirms-major-2026-update-to-remove-several-planner-features-add-new-ones/)); Umzug privater To-Do-Aufgaben in Planner ab 11/2026 nur aus KI-erzeugtem Tracker, **unbestätigt** | Planner bleibt nur Referenz für Gruppierungslogik (wie §3) | – |
| Trello | Eingang und Planer mit Kalenderverbindung (Ankündigung 2025, [Techzine](https://www.techzine.eu/blogs/applications/129033/atlassian-revamps-trello-introduces-new-inbox-and-planner)); 2026er Änderungen nicht belegt | Glide hat Eingang und Kalenderziehen bereits | – |
| Taskade, Capacities | Taskade: Agenten, Systemkern „TSK-1“ (07/2026), Modellwahl je Agent (08/2026), nur Dritte ([Lindy](https://wf.lindy.ai/blog/taskade-review)); Capacities: kein 2026er Changelog gefunden | Richtung „Agenten-Plattform“ liegt außerhalb der Produktgrenzen | 5 |

Nicht erneut geprüft und mit Stand 01.10.2026 in §3 belassen: Microsoft Loop, OneNote, Milanote, FigJam, ClickUp, Things, Sunsama, Akiflow, Trilium, Joplin.

### 9.3 Technische Code-Analyse: übertragbare Implementierungen

| Nr. | Implementierung (Projekt, Fundstelle) | Fakt | Folgerung für Glide | Art | Ü | Vorschlag |
|---|---|---|---|---|---|---|
| T01 | Ansichtsdefinition (AFFiNE `blocksuite/affine/data-view/src/core/filter/types.ts`, `eval.ts`, `view-presets/kanban/define.ts`) | Ansicht = JSON mit Spaltenliste (sichtbar/Reihenfolge), Filterbaum aus Gruppen `and`/`or` und Bedingungen `{Eigenschaft, Funktion, Argumente}`, `groupBy`, `sort`, Kopfzeilenzuordnung. Unbekannte Filterfunktionen werten als „trifft zu“ | Gleiches Modell als Tk-freies Modul über Glides festen Feldern; abweichend unbekannte Bedingungen **sichtbar ungültig** statt still erfüllt (passt zu D-03) | Idee/Algorithmus | 2 | FP-03 |
| T02 | Relative Datumsfilter (AFFiNE `packages/frontend/core/src/modules/workspace-property/types.ts`) | `last-7-days`, `this-week`, `this-month`, `this-quarter`, `before`/`after`/`between`, leer/nicht leer | Für Bearbeitungstag und Fälligkeit übernehmbar; ersetzt feste Fälligkeitsstufen nicht, ergänzt sie | Semantik | 2 | FP-03 |
| T03 | Regelbasierte Sammlungen (AFFiNE `modules/collection-rules`) | Sammlung = Filter + Gruppierung + Ordnung, ohne Kopie der Dokumente | Bestätigt: gespeicherte Ansicht ist reine Ableitung, keine Parallelstruktur | Architektur | 3 | FP-03 |
| T04 | Board aus Filtern (Super Productivity `boards.model.ts`; Vikunja `project_view.go`) | Spalte = Filter mit ein- und ausgeschlossenen Tags (alle/beliebig), Status, geplant ja/nein, Sortierung; Ablegen setzt die Tags der Spalte | Glides Gruppierung nach Feld (D02/D13) deckt das weitgehend; übernehmbar ist **Label ausschließen** als Filterbedingung | Semantik | 2 | FP-03 |
| T05 | Wiederholungsmodell (Super Productivity `task-repeat-cfg.model.ts`) | Intervall je Periode, Wochentage, n-ter/letzter Wochentag, letzter Monatstag, ab Erledigung, erst nach Erledigung, verpasste überspringen, Ausnahmen, Pause, Unteraufgaben-Vorlagen | Glide besitzt mit `ics_recurrence.py` (3.39.0) bereits einen geprüften RRULE-Rechner für INTERVAL, COUNT, UNTIL, BYDAY mit Ordinal, BYMONTHDAY, BYSETPOS; die Aufgabenwiederholung (`repeat_rules.py`) nutzt ihn nicht | Semantik + eigener Code | 2 | FP-02 |
| T06 | Dokumentverlauf (AFFiNE `nbstore/src/storage/history.ts`) | Schnappschuss je Dokument bei Änderung, Liste/Abruf/Rücksetzen je Zeitpunkt | Fortlaufende Seitenversionen sind nach D37 bewusst nicht gewählt; N13 (Seite aus Sicherung) deckt den Reparaturfall | Architektur | 5 | – |
| T07 | BM25+-Rangfolge über invertiertem Index (AFFiNE `nbstore/src/impls/idb/indexer/bm25.ts`, k = 1,2, b = 0,7, δ = 0,5) | rund 60 Zeilen Formel, Index in IndexedDB | Glides Suche ist mit 66,6 ms ausreichend schnell (P07 ✕). Nur die **Rangformel** könnte die Reihenfolge von Inhaltstreffern verbessern, ohne Index | Algorithmus | 2 | WA-15 (nur bei Bedarf) |
| T08 | KI-Anbieterabstraktion mit „OpenAI-kompatiblem“ Endpunkt (AFFiNE `backend/server/src/plugins/copilot/byok/types.ts`, EE-Lizenz) | ein Clientweg für Cloud- und lokale Modelle | Nur als Idee; Code unter EE-Lizenz. Für Glide relevant nur, wenn WA-10 entschieden wird | Idee | 3 | WA-10 |
| T09 | Lokale KI über Ollama (AppFlowy `flowy-ai/src/local_ai/*`, `flowy-sqlite-vec`) | Server-Erreichbarkeit prüfen, Modelle abfragen, Chat/Einbettung; fehlender Server wird als Zustand angezeigt | Muster „App läuft vollständig ohne, Dienst ist optional erkennbar“ passt zu Glides Prinzipien; sqlite-vec wäre eine native Abhängigkeit (✕) | Architektur | 3 | WA-10 |
| T10 | Vorschau verlinkter Dokumente (AFFiNE `modules/peek-view`) | Verweis öffnet eine Überlagerung statt Navigation | Glide hat den Inspektor für Aufgaben; Seitenverweise navigieren. Eine lesende Seitenvorschau im Inspektorbereich vermeidet Kontextverlust | UX | 4 | WA-11 |
| T11 | Notizen mit Koordinaten auf der Fläche (AFFiNE `model/src/blocks/note/note-model.ts`, `xywh`) | dieselben Blöcke im Dokument und auf der Leinwand | Glide trennt bewusst Seite und Pinnwand; die Pinnwand kennt bereits Seitenkarten (`page:`), lässt aber nur Zeichnungen zu (`ItemWorkspace.valid_pages`) | Idee | 4 | FP-04 |
| T12 | Operationsprotokoll und Vektoruhren (Super Productivity `op-log/sync`, `persistence`) | Konflikterkennung, LWW, Reparatur, Verschlüsselung | Bestätigt G23 ✕: Synchronisation wäre ein eigenes Produkt | Architektur | 5 | – |
| T13 | Dringlichkeit (Taskwarrior `src/Task.cpp`, `urgency_due`, `urgency_age`) | gewichtete, konfigurierbare Summe | Erklärbare Gründe behalten; „gibt andere frei“ als zusätzlicher Grund | Algorithmus | 2 | WA-12 |
| T14 | JSON Canvas (Spezifikation 1.0) | offenes Austauschformat für Leinwände | direkt als Ausgabeformat nutzbar | Format | 1 | FP-07 |

### 9.4 Featurematrix nach Funktionsbereichen (13.10.2026)

Ergänzt die funktionsgenaue Matrix in §4 um Umfang, Qualität und Integrationsaufwand je Bereich. Glide-Spalte aus dem Code 3.39.0 mit Belegstufe; Wettbewerbsspalte als Einschätzung aus den Quellen 01.–13.10.2026 (● vorhanden · ◐ teilweise · ○ fehlt · P per Erweiterung · – nicht Zweck), **AF** AFFiNE · **AP** AppFlowy · **No** Notion · **SP** Super Productivity · **Td** Todoist · **Ob** Obsidian. Aufwand S bis 1, M 2–4, L mehr als 4 Arbeitstage.

| Bereich | Glide 3.39.0: Umfang und Qualität | AF · AP · No · SP · Td · Ob | Lücke (Fakt → Folgerung) | Aufwand | Paket |
|---|---|---|---|---|---|
| Aufgabenverwaltung | rekursive Unterpunkte, Checklisten (≤ 50), „wartet auf“ mit Kreisprüfung, Verknüpfungen (≤ 50), Wichtigkeit, Aufwand, Zeit, gemeinsamer Inspektor (3.38.0); hoch [Code][Test] | ◐ · ◐ · ● · ◐ · ◐ · P | Rückgängig über 20 Schritte, aber **kein Wiederholen** für Aufgaben- und Strukturänderungen (nur Text- und Zeicheneditor) [Code] | M | FP-01 |
| Organisation | Listen, Ordner/Buch/Notizbuch, Labels, Gruppen, Zwischenüberschriften, Eingang, Archiv, Papierkorb; hoch | ● · ● · ● · ● · ● · ● | keine wesentliche | – | – |
| Planung | Bearbeitungstag ≠ Fälligkeit, Heute/Demnächst, Kapazität, Zeitblöcke, Woche/Monat, Vorschlag, Routinen, Fokus; 3.39.0 Tageshinweise, ICS-Belegzeiten, Entlasten (Mac-vollgeprüft); sehr hoch | ○ · ○ · ◐ · ● · ◐ · P | Wiederholungen: sechs Arten; kein Intervall für Woche/Monat/Jahr, kein n-ter Wochentag, nicht ab Erledigung, keine Pause [Code `repeat_rules.py`]; Schnelleingabe deutet Wiederholungsangaben mit Ankertag teilweise falsch, ICS-Austausch weicht am Monatsende ab (A28/A29) | S–M (Fehler) / M–L, Formattor | FP-00, FP-02 |
| Dokumentation | Block-Editor mit „/“-Menü, H1–H4, Aufgaben, Aufklapp-/Hinweisblöcke, Bilder mit Umfluss, Live-Listen, Titelbild, Markdown hin und zurück, Druck; hoch | ● · ● · ● · ◐ · – · ● | Unterseiten, Spalten, ziehbare Blöcke fehlen – bewusst (Produktgrenzen) | – | – |
| Datenbanken | feste Glide-Felder; Tabelle mit Spaltenwahl je Liste, Sortieren, Gruppieren, gespeicherte Filter; hoch für feste Felder | ● · ● · ● · – · – · ● | Gespeicherte Filter kennen weder Bearbeitungstag, Aufwand, „wartet auf“ noch Ausschluss; Darstellung (Ansicht, Gruppierung, Sortierung) wird nicht mitgespeichert [Code `SavedFilters`] | M–L | FP-03 |
| Ansichten | Liste, Tabelle, Pinnwand (frei/geordnet/Spalten), Kalender, Karten, Galerie, Heute, Demnächst, Wochenrückblick; sehr breit | ● · ● · ● · ◐ · ◐ · ● | Seiten und Notizen können nicht als Karte auf die Pinnwand (nur Zeichnungen) [Code `valid_pages`] | M | FP-04 |
| Verknüpfungen | Seiten-, Listen-, Aufgabenverweise mit Rückverweisen, Aufgaben im Text mit Original-ID, Live-Listen; hoch | ● · ◐ · ● · ○ · ○ · ● | unverknüpfte Erwähnungen fehlen; Verweise navigieren statt Vorschau | S–M / M | FP-05, WA-11 |
| Suche | Palette für Inhalte und Aktionen, markierte Fundstellen, erklärte Filter; 66,6 ms bei 10.000 Punkten; hoch | ● · ● · ● · ◐ · ● · ● | Rangfolge der Inhaltstreffer einfach (Titelrang) | S | WA-15 |
| Automatisierung | Wiederholungen, Routinen, Vorlagen mit Platzhaltern, Tageshinweise; keine Regeln | ○ · ○ · ● · ◐ · ◐ · P | keine wiederkehrenden Vorlagen; Regel-Engine bewusst nicht vorgeschlagen | M | WA-14 |
| KI | Austauschformat Stufe 1/2: Kontextpaket, geprüfte Änderungsvorschläge (Q3) | ● · ● · ● · ? · ● · P | wiederkehrende KI-Aufträge brauchen jedes Mal eigene Anweisungen; keine eingebaute KI (bewusst) | S–M | FP-06, WA-10 |
| Visualisierung | Pinnwand mit Bereichen, beschrifteten Verbindungen, Präsentation, PDF; Pixel-Werkstatt; Jahres-Heatmap | ● · ○ · ○ · ○ · ○ · ● | kein offenes Austauschformat der Pinnwand; Formen/Freihand bewusst nicht | S–M | FP-07 |
| Bedienbarkeit | Palette, stabile Aktionskennungen, Kontextmenüs, Tastaturwege auch für Pinnwand, Ziehen nach D02, Inspektor | ● · ● · ● · ● · ● · ● | Wiederholen fehlt (siehe oben); Screenreader in Paket 8 | M | FP-01 |
| Datenverwaltung | atomares JSON, Vorsicherung je Format, Sicherungen nur bei Änderung, Tagesstände, Teil-/Komplett-/App-Backup, Vergleich, CSV/MD/TXT/ICS/Druck/Austausch, Notion-Import in Paket 6; sehr hoch | ● · ● · ◐ · ● · ◐ · ● | kein Gesamtexport als offener Dateibaum in einem Schritt (nur je Liste/Ordner); Pinnwandlayout reist nur im App-Backup [Dok 06] | M | FP-07 |
| Individualisierung | zehn Designs einschließlich Dopamin und Liquid Glass, automatisch hell/dunkel, Akzent, Verläufe, Startseite, Schriftgröße, Kontrast WCAG AA | ◐ · ◐ · ◐ · ● · ◐ · ● | keine | – | – |

### 9.5 Bewertung der Entwicklungsrichtungen

- **Block-Editor (Auftrag 7.2):** *Fakt:* Glides `RichNoteEditor`/`PageEditor` speichert Text mit semantischen Spannen, bietet „/“-Menü, Umwandeln, Aufklappblöcke und echte Aufgaben mit ID. BlockSuite und BlockNote führen jeden Block als eigenes Objekt in einem CRDT-Baum. *Folgerung:* Ein vollständiger Block-Editor brächte Blockverweise und Ziehen von Blöcken, verlangte aber ein neues Seitendatenmodell, eine Migration aller Seiten und den Umbau des Tk-Textfelds – Aufwand L+, hohes Regressionsrisiko. Der praktische Nutzen ist mit gezielten Erweiterungen (unverknüpfte Erwähnungen, Seitenvorschau, Seitenkarten auf der Pinnwand, vorhandene Live-Listen) zum Bruchteil erreichbar. **Empfehlung: kein Block-Editor-Neubau.**
- **Flexible Ansichten (7.3):** *Fakt:* AFFiNE, Vikunja und Super Productivity definieren eine Ansicht als Filter plus Darstellung über **denselben** Daten; Glides gespeicherte Filter sind bereits reine Ableitungen. *Folgerung:* Erweiterung der vorhandenen gespeicherten Filter statt neuer Ansichtsart; keine Parallelstruktur. → FP-03.
- **Pinnwand und Arbeitsflächen (7.4):** *Fakt:* AFFiNE Edgeless ist eine eigene Vektor-Engine (Formen, Pinsel, Mindmaps, Rahmen, eigener Renderer). Die Tk-Leinwand glättet unter Windows und X11 nicht ([Architektur §5](../01_Repository/Glide/docs/02_ARCHITECTURE.md#zeichnen-und-bilder)); freie Klebezettel und Freihand sind Produktgrenze. *Folgerung:* Kein Whiteboard-Editor. Wert entsteht durch **Inhalte auf der vorhandenen Fläche** (Seiten/Notizen als Karten, FP-04) und **offene Ausgabe** (JSON Canvas, FP-07).
- **KI (7.5), lokal und extern getrennt:** *Lokal* (AppFlowy-Muster): externer Dienst wie Ollama mit Modell ab etwa 4–5 GB, 8–16 GB Arbeitsspeicher empfohlen, Antwort in Sekunden; Daten bleiben auf dem Rechner, keine laufenden Kosten, Wartung durch Modell- und Dienstwechsel, Glide muss bei fehlendem Dienst unverändert arbeiten. Technisch ohne Python-Abhängigkeit (Standardbibliothek-HTTP auf `localhost`), aber eine **Schnittstelle** im Sinn von Q3 → nur mit neuer Entscheidung (WA-10). *Extern* (Cloud-API, BYOK): widerspricht der Produktgrenze „eingebaute Cloud-KI“ → nicht vorgeschlagen; der Nutzer kann Cloud-KI weiterhin selbst über das Austauschformat nutzen. *Semantische Suche:* braucht Einbettungsmodell und Vektorsuche; ohne native Bibliothek nur langsam, Nutzen bei Glides Bestandsgrößen unbelegt → nicht jetzt. **Sofort Q3-konform möglich:** wiederverwendbare KI-Aufträge im Kontextpaket (FP-06).
- **Synchronisation, CRDT, Framework-Wechsel:** *Fakt:* Super Productivity braucht für Synchronisation, Persistenz und Konfliktlösung 159 Dateien, das Operationsprotokoll insgesamt 411 (jeweils einschließlich Tests); AFFiNE und AppFlowy bauen auf CRDT. *Folgerung:* Für ein lokales Ein-Personen-Werkzeug ohne Sync (G23 ✕) kein Nutzen; Kosten-Nutzen eines Toolkit-Wechsels im [Entwicklungsplan §16.6](Glide_Entwicklungsplan.md#166-architekturentscheidungen-geprüfte-alternativen).

**Antwort auf die Leitfrage (Kurzfassung):** Glides Funktionsbreite entspricht dem Feld; die wirksamsten Konzepte sind keine neuen Bereiche, sondern (1) Systemkonventionen vervollständigen (Wiederholen), (2) vorhandene Kernfunktionen vertiefen (Wiederholungsregeln, gespeicherte Ansichten), (3) Wissen und Pinnwand verbinden (Seitenkarten, unverknüpfte Erwähnungen), (4) offene Ausgabeformate als Datensouveränität und (5) KI-Komfort innerhalb von Q3. Bewusst nicht: Block-Editor-Neubau, Whiteboard-Engine, Datenbank-Baukasten, Sync/CRDT, eingebaute Cloud-KI, Toolkit-Wechsel. Pakete und Reihenfolge: [Entwicklungsplan §16](Glide_Entwicklungsplan.md#16-vorschläge-aus-wettbewerbs--und-open-source-analyse-13102026).

### 9.6 Quellen und Repositories (Abruf 12./13.10.2026)

| Quelle | Fassung / Commit | Lizenz (GitHub-API bzw. Datei) |
|---|---|---|
| AFFiNE, lokale Kopie `AFFiNE-canary` | `package.json` 0.27.5; [Releases](https://github.com/toeverything/AFFiNE/releases) bis 2026.10.12-canary.921 | MIT außer `packages/backend`, `packages/common/native` (EE); API `NOASSERTION`. Eigenständiges [BlockSuite-Repository](https://github.com/toeverything/blocksuite) MPL-2.0 – vor jeder Übernahme klären (nicht vorgesehen) |
| [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | `5cf3a36` (26.06.2026, Standardzweig); Release 0.14.2 laut Spiegel | AGPL-3.0 |
| [Super Productivity](https://github.com/johannesjo/super-productivity) | `c4c6959` (12.10.2026), 19.2.0 | MIT (Datei `LICENSE`) |
| [Vikunja](https://github.com/go-vikunja/vikunja) | `4e2a899` (12.10.2026) | AGPL-3.0 |
| [ai-notion-clone](https://github.com/EduartePaiva/ai-notion-clone) | `c68ece5` (01.01.2025) | MIT |
| [Taskwarrior](https://github.com/GothenburgBitFactory/taskwarrior) | Standardzweig 13.10.2026, `src/Task.cpp` | MIT |
| [JSON Canvas](https://github.com/obsidianmd/jsoncanvas) | Spezifikation 1.0 | MIT |
| [Logseq](https://github.com/logseq/logseq), [SiYuan](https://github.com/siyuan-note/siyuan), [Trilium](https://github.com/TriliumNext/Trilium) | nur Metadaten | AGPL-3.0 |
| [Anytype](https://github.com/anyproto/anytype-ts), [Joplin](https://github.com/laurent22/joplin) | nur Metadaten | API `NOASSERTION`; Lizenztext nicht geprüft |
| [Planify](https://github.com/alainm23/planify) | nur Metadaten | GPL-3.0 |

Ungeprüfte Lizenzfragen: Anytype- und Joplin-Lizenztexte, AFFiNE-EE-Lizenz im Detail, Lizenz des Blink-Exports. Keine dieser Fragen blockiert einen Vorschlag, weil kein Fremdcode übernommen wird.
