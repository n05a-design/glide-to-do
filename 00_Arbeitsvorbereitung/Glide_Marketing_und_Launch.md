# Glide – Marketing, Launch, Positionierung & Community

Stand 24.11.2026 · Glide 1.0.3 · Aufgabenformat 26

Dieses Dokument ist die verbindliche strategische Quelle für Glides Marktpositionierung, Zielgruppenansprache, Marketing-Assets, Launch-Kommunikation, Webpräsenz und Nutzervalidierung nach der Veröffentlichung von Glide 1.0.2. Aufgaben und Meilensteine stehen im [Entwicklungsplan](Glide_Entwicklungsplan.md), technische Befunde in der [Analyse](Glide_Analyse.md), Architekturentscheidungen in der [Arbeitsrichtung](../01_Repository/Glide/docs/ARBEITSRICHTUNG.md) und Verteilungswege in [docs/10_VEROEFFENTLICHUNG.md](../01_Repository/Glide/docs/10_VEROEFFENTLICHUNG.md).

---

## 1. Strategische Marktpositionierung & Kernbotschaft

Glide ist die ruhige, lokale Arbeitsumgebung für Menschen, die Aufgaben, Notizen, visuelle Pinnwände und kreative Pixel-Entwürfe an einem einzigen Ort zusammenführen möchten – ohne Cloud-Zwang, ohne Benutzerkonto, ohne monatliche Abonnementkosten und entwickelt mit dem Ziel, kognitive Reizüberflutung zu minimieren.

### 1.1 Der Kern-Claim
- **Primärer Produkt-Claim (Verbindliche Inhaberentscheidung D72 / D74):**
  - **Deutsch:** *Aufgaben planen. Ideen verbinden. Selbst gestalten.*
  - **Englisch:** *Plan tasks. Connect ideas. Shape your world.*
- **Sekundärer alternativer Marketing-Claim:**
  - **Deutsch:** *Klarheit für deine Tage. Raum für deine Ideen.*
  - **Englisch:** *Calm planning for your days. Space for your ideas.*

### 1.2 Die drei Säulen des Produktversprechens
1. **Kognitive Entlastung statt Überwachung (Calm Tech):**
   Glide erinnert nicht aggressiv, zählt keine Streaks und monetarisiert keine Aufmerksamkeit. Es schützt die tägliche Arbeitszeit durch realistische Kapazitätsgrenzen (WA-12), visuelle Ruhe (P1–P6) und eine typografisch ausgewogene Oberfläche.
2. **Kompromisslose Datenhoheit (Local-First):**
   Alle Daten liegen in lesbaren, offenen Formaten (JSON, Markdown, JSON Canvas 1.0) auf dem lokalen Rechner des Nutzers. Kein Login, kein Tracker, keine Cloud-Abhängigkeit. Portabel auf USB-Sticks und Netzlaufwerken einsetzbar.
3. **Einzigartige Werkzeug-Synthese:**
   Glide schließt die Lücke zwischen reinen To-Do-Listen (Things, Todoist), unstrukturierten Notiz-Vaults (Obsidian), überladenen All-in-One-Monolithen (Notion) und visuellen Whiteboards (Miro, Milanote) – ergänzt durch eine integrierte Pixel-Werkstatt für Icons, Cover und Sprites.

---

## 2. Zielgruppenstrategie (§39)

Glide spricht sechs differenzierte Nutzergruppen an, von denen fünf als Kernzielgruppen gezielt gefördert werden, während eine Gruppe explizit als Nicht-Zielgruppe abgegrenzt wird:

### Profil 1: Kreative, Designer, Illustratoren & Game-Art-Künstler (Priorität: Sehr hoch)
1. **Demografie & Berufsfeld:** UI/UX-Designer, freiberufliche Illustratoren, Game-Designer, Grafikdesigner (22–45 Jahre).
2. **Pain Points & Frustrationen:** Zerrissenheit zwischen gestalterischen Notizen, Aufgaben und Moodboards; Tools wie Notion sind oft träge und textlastig; Whiteboards wie Miro sind teuer und cloudgebunden; ständige Unterbrechungen durch Projektmanagement-Tools.
3. **Bisher genutzte Werkzeuge:** Notion, Milanote, PureRef, Apple Notizen, Aseprite, Figma.
4. **Typischer Trigger-Moment:** Frustration über träge Ladezeiten bei großen Boards in Online-Tools oder der Wunsch, Aufgaben und visuelle Skizzen für ein Kundenprojekt an einem einzigen, offline verfügbaren Ort zu bündeln.
5. **Core Value Proposition:** Aufgaben, strukturierte Notizen, visuelle Pinnwände und ein nativer Pixel-Editor in einer einzigen schnellen, nativen Desktop-Anwendung.
6. **Feature-Priorität:** 1. Visuelle Pinnwand (Canvas mit Bildkarten), 2. Integrierte Pixel-Werkstatt (Spritesheet/Cover-Export), 3. Adaptive Titelbildzuschnitte & ruhige Typografie.
7. **Konvertierungs- & Einstiegspfad:** Download des DMG/Installers über GitHub -> Start mit dem "Kreativ-Projekt"-Template -> Erstellen eines Moodboards mit Pinnwandkarten -> Zeichnen eines Icons in der Pixel-Werkstatt.
8. **Bedenken & Vorbehalte:** "Ist Tkinter nicht altbacken?", "Gibt es Stiftunterstützung auf dem iPad?", Gatekeeper-Warnung beim ersten Öffnen.
9. **Entkräftungsstrategie:** Zeigen des modernen Bento-Box- und Pinnwand-Designs; transparente Aufklärung über die lokale Datenhoheit und offene Standards; einfache 2-Klick-Anleitung für macOS Gatekeeper und Windows SmartScreen.
10. **Messaging Tone:** Ästhetisch, inspirierend, respektvoll gegenüber handwerklichem Schaffen, visuell orientiert.
11. **Primärer Kanal:** Behance, Dribbble, Mastodon (Design-Bubble), Indie Hackers, Reddit (`r/pixelart`, `r/design`).
12. **Erfolgskriterium (Aktivierung):** Der Nutzer legt innerhalb von 24 Stunden mindestens ein Notizbuch mit einem Pixel-Cover und ein Pinnwand-Board mit 3 Karten an.
13. **Empfohlenes Onboarding-Szenario:** Geführte Vorlage "Design-Projekt: Markenentwicklung & Icon-Set".

---

### Profil 2: Freelancer, Solopreneure & Berater (Priorität: Sehr hoch)
1. **Demografie & Berufsfeld:** IT-Freelancer, Strategieberater, Autoren, Solo-Unternehmer (28–55 Jahre).
2. **Pain Points & Frustrationen:** Chronische Überbuchung durch Kundenprojekte; unklare Tageskapazitäten; teure Software-Abonnements (Sunsama 20 $/Monat, Notion 10 $/Monat); Angst vor Datenlecks bei sensiblen Kundendaten.
3. **Bisher genutzte Werkzeuge:** Sunsama, Todoist, Asana, Excel, Trello.
4. **Typischer Trigger-Moment:** Erneute Jahresrechnung für ein ungenutztes Cloud-Tool oder Burnout-Gefühl durch eine To-Do-Liste mit 80 unerledigten Aufgaben.
5. **Core Value Proposition:** Realistische Tagesplanung mit festen Kapazitätsgrenzen und Entlastungsdialog – 100% lokal, diskret und dauerhaft kostenlos unter MPL-2.0.
6. **Feature-Priorität:** 1. Tageskapazität & Entlastungsdialog (WA-12), 2. Notizbücher mit Bearbeitungszeiten, 3. Fundortübersicht aller offenen Aufgaben (WA-21).
7. **Konvertierungs- & Einstiegspfad:** Download -> Import vorhandener Aufgaben oder manuelle Eingabe von 5 Kernaufgaben für heute -> Warnung bei Kapazitätsüberschreitung -> Durchführung des Entlastungsdialogs.
8. **Bedenken & Vorbehalte:** "Kann ich meine Zeiten für die Rechnungsstellung exportieren?", "Gibt es eine mobile App für unterwegs?".
9. **Entkräftungsstrategie:** Roadmap für WA-08 (Soll-Ist-Zeiterfassungs-Export); Anleitung für synchrone Nutzung über Nextcloud/Synology/USB-Stick.
10. **Messaging Tone:** Professionell, beruhigend, pragmatisch, wertschätzend für Lebenszeit.
11. **Primärer Kanal:** LinkedIn, Hacker News, Freelancer-Podcasts, Substack.
12. **Erfolgskriterium (Aktivierung):** Nutzer schließt an drei aufeinanderfolgenden Tagen seine Tagesplanung unterhalb des Kapazitätslimits ab.
13. **Empfohlenes Onboarding-Szenario:** Vorlage "Kundenwoche: 3 Retainer & administrative Entlastung".

---

### Profil 3: Persönliche Produktivität, Minimalisten & ADHS-Fokus (Priorität: Hoch)
1. **Demografie & Berufsfeld:** Neurodivergente Wissensarbeiter, Minimalisten, Studierende, Privatnutzer (18–50 Jahre).
2. **Pain Points & Frustrationen:** Paralyse durch unendliche Listen und Gamification; "Streak-Scham" bei ausgelassenen Tagen; Reizüberflutung durch Benachrichtigungen, Badges und Animationen; Konfigurationsfalle ("Productivity Procrastination").
3. **Bisher genutzte Werkzeuge:** Tiimo, Llama Life, Things 3, Papiernotizbücher, TickTick.
4. **Typischer Trigger-Moment:** Überwältigung durch eine wachsende Aufgabenliste und das Gefühl des Versagens beim Öffnen herkömmlicher Planer.
5. **Core Value Proposition:** Radikale kognitive Ruhe. Keine Streaks, keine roten Alarmfarben, keine Bestrafung für Unerledigtes. Der Entlastungsdialog fragt sanft: "Morgen weiter oder heute reduzieren?".
6. **Feature-Priorität:** 1. Sanfter Entlastungsdialog ohne Beschämung, 2. Natürliche Datumseingaben ("heute", "morgen", "freitag"), 3. Visuelle Ruhe durch Bento-Karten und gedeckte Farbpaletten.
7. **Konvertierungs- & Einstiegspfad:** Direkter portabler Start ohne Registrierung -> Nutzen des "Heute"-Fokus -> Erleben der Ruhe beim Abhaken ohne Konfetti-Animationen.
8. **Bedenken & Vorbehalte:** "Ist das wieder ein Tool, das ich nach 3 Tagen vergesse?", "Verliere ich den Überblick ohne Push-Mitteilungen?".
9. **Entkräftungsstrategie:** Positionierung als sicherer Hafen statt Antreiber; bewusstes Design ohne Push-Zwang; portable Dateiablage.
10. **Messaging Tone:** Sanft, nicht wertend, achtsam, aufgeräumt, ermutigend.
11. **Primärer Kanal:** Mastodon (`#ADHD`, `#neurodiversity`), Reddit (`r/ADHD`, `r/productivity`), YouTube (Minimalismus-Kanäle).
12. **Erfolgskriterium (Aktivierung):** Nutzer nutzt den Entlastungsdialog, ohne Aufgaben frustriert zu löschen oder die App zu deinstallieren.
13. **Empfohlenes Onboarding-Szenario:** Vorlage "Ruhiger Fokus: 3 Dinge am Tag".

---

### Profil 4: Entwickler, Open-Source- & Tech-Enthusiasten (Priorität: Hoch)
1. **Demografie & Berufsfeld:** Software-Entwickler, DevOps-Engineers, Linux-Nutzer, Open-Source-Beitragende (20–48 Jahre).
2. **Pain Points & Frustrationen:** Vendor Lock-in proprietärer Systeme; binäre Datenbanken ohne Git-Versionierung; ressourcenhungrige Electron-Apps, die 1 GB RAM belegen; mangelnde Skriptbarkeit.
3. **Bisher genutzte Werkzeuge:** Obsidian, Super Productivity, Emacs Org-Mode, Taskwarrior, VS Code.
4. **Typischer Trigger-Moment:** Ärger über eine Electron-App, die den Laptop-Lüfter anwirft, oder der Wunsch, Aufgaben strukturiert an KI-Coding-Agenten (Claude Code, Antigravity, Copilot) zu übergeben.
5. **Core Value Proposition:** Schlanke Python/Tkinter-Architektur (< 80 MB RAM), reine Text-/JSON-Dateien, vollständiger JSON Canvas 1.0 Export und ein offizieller dokumentbasierter `glide-to-do` Agent-Skill.
6. **Feature-Priorität:** 1. `glide-to-do` Agent-Skill & strukturierte Exporte, 2. Vollständige Tastaturbedienung ohne Mauszwang, 3. JSON Canvas 1.0 & Markdown-Kompatibilität.
7. **Konvertierungs- & Einstiegspfad:** Klonen des Repositories oder `pip install` bzw. GitHub Prerelease Download -> Inspektion von `data/` -> Einbinden des Agent-Skills in die eigene Entwicklungsumgebung.
8. **Bedenken & Vorbehalte:** "Warum Tkinter statt Web/Rust?", "Ist die Performance bei 10.000 Aufgaben ausreichend?".
9. **Entkräftungsstrategie:** Verweis auf die saubere Framework-Shell-Trennung (T319), native Tk 9 / Cocoa-Bindung, zero external backend dependencies und transparente Regressionstests (T340).
10. **Messaging Tone:** Technisch präzise, faktenbasiert, transparent bezüglich Architektur und Codequalität.
11. **Primärer Kanal:** GitHub Trending, Hacker News ("Show HN"), Lobste.rs, Reddit (`r/commandline`, `r/python`, `r/opensource`).
12. **Erfolgskriterium (Aktivierung):** Erfolgreicher Import oder Export von Aufgaben via Markdown oder Interaktion über den Agent-Skill.
13. **Empfohlenes Onboarding-Szenario:** Vorlage "Sprint-Planung & Feature-Backlog für Open-Source-Projekte".

---

### Profil 5: Studierende, Forschende & Wissensarbeiter (Priorität: Mittel)
1. **Demografie & Berufsfeld:** Universitätsstudierende, Doktoranden, Gymnasiallehrer, Sachbuchautoren (19–40 Jahre).
2. **Pain Points & Frustrationen:** Zersplitterung zwischen Recherchematerialien, Semesterarbeiten und Abgabefristen; Prüfungsangst durch unklare Zeithorizonte; Datenverlust bei Cloud-Pannen.
3. **Bisher genutzte Werkzeuge:** OneNote, Notion, Zotero, Apple Erinnerungen, GoodNotes.
4. **Typischer Trigger-Moment:** Semesterbeginn, Vorbereitung auf eine Abschlussarbeit oder der Verlust des Zugriffs auf eine Universitäts-Cloud-Lizenz.
5. **Core Value Proposition:** Ein persönlicher Studienbegleiter: Vorlesungsnotizen, Literatur-Checklisten, Prüfungs-Countdowns und visuelle Themenlandkarten in einem einzigen, zuverlässigen Offline-Notizbuch.
6. **Feature-Priorität:** 1. Strukturierte Notizbücher mit Bearbeitungszeiten, 2. Fundortübersicht für Recherchenotizen, 3. Pinnwand für thematische Querverbindungen.
7. **Konvertierungs- & Einstiegspfad:** Download der portablen Version -> Anlegen eines Notizbuchs pro Seminar -> Strukturierung des Semesters mit Deadlines.
8. **Bedenken & Vorbehalte:** "Kann ich PDFs direkt annotieren?", "Kann ich mit Kommilitonen in Echtzeit zusammenarbeiten?".
9. **Entkräftungsstrategie:** Klare Positionierung als individueller Denkraum; Verweis auf D05 (bewusste Begrenzung zur Vermeidung von Komplexität) und offene Markdown-Exporte für Gruppenarbeiten.
10. **Messaging Tone:** Strukturiert, akademisch seriös, bildungsorientiert, aufgeräumt.
11. **Primärer Kanal:** Studierenden-Foren, Universitäts-Subreddits, Notion-Alternativen-Blogs.
12. **Erfolgskriterium (Aktivierung):** Anlegen von mindestens zwei Notizbüchern mit verknüpften Aufgaben für eine Seminararbeit.
13. **Empfohlenes Onboarding-Szenario:** Vorlage "Semesterplaner: Hausarbeit, Klausurphase & Leseliste".

---

### Nicht-Zielgruppe: Unternehmen, Großteams & Enterprise-Projektmanagement
1. **Abgrenzung:** Glide ist **kein** Jira, Asana, Monday.com oder Microsoft Project.
2. **Begründung:** Glide verzichtet bewusst auf Benutzerverwaltung, Multi-User-Rechte, Cloud-Synchronisation, Zeiterfassungsfreigaben und Überwachungsdashboards für Vorgesetzte (D02, D86).
3. **Kommunikative Haltung:** Transparent und wertschätzend ablehnen. "Wenn Sie ein Tool suchen, um die Arbeitszeit von 50 Mitarbeitern zu überwachen, ist Glide nicht das richtige Werkzeug. Wenn diese 50 Mitarbeiter jedoch für ihre eigene, ungestörte Denkarbeit einen ruhigen Rückzugsort suchen, ist Glide perfekt."

---

## 3. Marketingmaterial-Briefings (§40)

Um die Veröffentlichung von Glide 1.0.2 professionell zu begleiten, werden neun standardisierte Produktionsbriefings definiert:

| Nr. | Asset-Name | Format / Spezifikation | Dauer / Umfang | Visueller Inhalt & Kernaussage | Call to Action | Zielgruppe |
|---|---|---|---|---|---|---|
| **B01** | **Hero-Produktvideo (Release v1.0.2)** | MP4 (H.264), 1920x1080 @ 60fps, 16:9 | 35–40 Sekunden | Format A (v1.0.2 Stand): Schnellerfassungs-Flow -> Strukturierte Notizbücher -> Pinnwand-Canvas -> Pixel-Werkstatt -> Tageskapazitäts-Schutz. Sanfte Typografie, echte Software-Aufnahmen ohne Bento. | "Download Glide 1.0.2 on GitHub – 100% Free & Local" | Designer, Freelancer, Techies |
| **B01b**| **Preview-Trailer (Bento System)** | MP4 (H.264), 1920x1080 @ 60fps, 16:9 | 25–30 Sekunden | Format B (Vorschau auf `main` / v1.1.0): Modulares Bento-Dashboard, adaptive 3-/2-spaltige Anordnung, Kachel-Presets und Widget-Metriken. | "Explore Glide Bento on GitHub main" | UI/UX-Designer, Entwickler |
| **B02** | **Feature-GIF-Serie** | GIF & WebM, 1280x720, optimierte Palette | 6 Loops à 4–8s | Siehe §4.1: Schnellerfassung, Pinnwand-Kabel, Shortcuts, Export, Paletten, Bento-Vorschau. | In Docs & Readme eingebettet | Alle Zielgruppen |
| **B03** | **Download-Grafiken** | PNG & SVG, 1200x630 (OG-Image) & Badges | 5 Grafiken (Win Setup/ZIP, Mac DMG/TAR, Quellstart, Hash, Skill) | Betriebssystem-Icons mit klaren Versionsangaben (v1.0.2, Stand 24.11.2026), SHA-256-Badge und Prerelease-Kennzeichnung (macOS Apple Silicon & Windows x64 nativ; Linux & Intel-Macs via Quellstart). | "Herunterladen für macOS / Windows" | Erstbesucher |
| **B04** | **Bento-Screenshots (Entwicklungsstand)** | PNG, 2560x1440 Retina, Lossless | 4 Hero-Shots (Hell, Dunkel, Split, Kompakt) | Bento-Startseite (Stand `main`): Metriken, Heute-Liste, Notizbuch-Raster und Pinnwand-Vorschau. | Zur Verwendung in Pressekit & Readme | Presse, Designer |
| **B05** | **Feature-Cards** | PNG, 1080x1080 (1:1) & 1200x675 (16:9) | 6 Cards für Social Media | Großes Bildzitat der Funktion (z.B. Entlastungsdialog), kurzer Claim, Tastenkürzel. | "Entdecke ruhige Produktivität" | Social Media (Mastodon, X) |
| **B06** | **Vergleichsmatrix** | PNG & PDF (Vektor), 1920x1080 | 1 Übersichtsgrafik | Differenzierte Matrix Glide vs. Notion vs. Things 3 vs. Sunsama vs. Obsidian (§18.2). | "Vergleiche die Ansätze" | Wechselbereite Nutzer |
| **B07** | **Pressekit-Paket** | ZIP-Archiv mit Markdown, Logos & Assets | One-Pager + 10 Hi-Res Shots | Factsheet, Gründerphilosophie, Datenschutzversprechen, offizielle Logos (Dark/Light). | "Pressekontakt via GitHub" | Tech-Journalisten, Blogger |
| **B08** | **Beispielprojekte** | `.glideexchange` & ZIP | 3 Beispieldaten-Sätze | Vollwertige, vorbefüllte Welten: 1. "Design-Sprint", 2. "Freelancer-Woche", 3. "Masterarbeit". | "Mit einem Klick importieren" | Einsteiger |
| **B09** | **Tutorial-Grafiken** | PNG & SVG mit Schrittnummerierung | 10 Infografiken (T01–T10) | Schrittweise Anleitung für Tastaturkürzel, Gatekeeper-Bypass, Safe Agent Import und JSON Canvas. | "Lies die Schritt-für-Schritt-Anleitung" | Wissensarbeiter |

---

## 4. Produktvideo-Storyboards (§41)

Die Videostrategie wird strikt nach veröffentlichter Version und Arbeitsstand zweigeteilt:
- **Format A:** Offizielles Release-Video für Version v1.0.2 (Fokus auf bereits freigegebene Kernfunktionen ohne Bento).
- **Format B:** Vorschau-Trailer für das Glide Bento Box System `0.1.0` (Vorschau auf Branch `main` nach Glide 1.0.2).

---

### 4.1 Format A: Release-Video Glide 1.0.2 (Laufzeit: 38 Sekunden)

**Titel:** *Glide – Der ruhige Raum für deine Gedanken*  
**Laufzeit:** 38 Sekunden  
**Sounddesign:** Ruhiger, warmer Lo-Fi-Piano-Akkord zum Auftakt; dezente, haptische Klickgeräusche (Mechanical Keyboard); kein hektischer Beat.

```
0:00 ── Szene 1: Schnellerfassung ──> 0:06 ── Szene 2: Visuelle Pinnwand ──> 0:14
0:14 ── Szene 3: Strukturierte Notizen ──> 0:22 ── Szene 4: Kapazität & Schutz ──> 0:30
0:30 ── Szene 5: Pixel-Werkstatt & Cover ──> 0:35 ── Szene 6: Endcard & Download ──> 0:38
```

#### Szene 1: Schnellerfassung & Chaos-Befreiung (0:00 – 0:06)
- **Visuelle Handlung:** Nahaufnahme des Glide-Fensters. Ein Nutzer tippt blitzschnell über die Schnellerfassung: `Kundenpräsentation vorbereiten morgen 90m`. Das System hebt `morgen` und `90m` sanft hervor und ordnet die Aufgabe sofort ein.
- **Voiceover (DE):** "Gedanken festhalten, bevor sie verfliegen. Ohne Klickmarathon. Ohne Reizüberflutung."
- **Voiceover (EN):** "Capture thoughts before they slip away. No friction. No distractions."
- **Text-Overlay:** *Schnellerfassung mit natürlicher Spracheingabe.*
- **UI-Elemente:** Quick-Entry-Overlay, System-Schriftbild.

#### Szene 2: Die visuelle Pinnwand (0:06 – 0:14)
- **Visuelle Handlung:** Sanfte Kamerafahrt auf die Pinnwand (Canvas). Drei Bildkarten werden platziert. Eine Verbindungslinie schnappt mit magnetischer Eleganz zwischen Notizkarte und Aufgabenblock ein.
- **Voiceover (DE):** "Verbinde, was zusammengehört. Deine Notizen, Skizzen und Aufgaben auf einer freien Fläche."
- **Voiceover (EN):** "Connect what matters. Notes, sketches, and tasks on an open visual canvas."
- **Text-Overlay:** *Visuelle Pinnwand · Voller JSON Canvas 1.0 Standard.*
- **UI-Elemente:** Canvas-Nodes, bezier-basierte Verbindungslinien, Bildkarten mit adaptivem Beschnitt.

#### Szene 3: Strukturierte Notizen & Bücher (0:14 – 0:22)
- **Visuelle Handlung:** Wechsel in ein Projekt-Notizbuch. Strukturierter Text mit Checklisten. Am rechten Rand zeigt der Aufgabeninspektor die verknüpften Fälligkeiten. Ein Klick auf "Fundorte" zeigt alle verstreuten Erwähnungen.
- **Voiceover (DE):** "Schreibe mit Fokus. Deine Dokumente bleiben bei dir – in offenem Markdown, ohne Cloud-Zwang."
- **Voiceover (EN):** "Write in depth. Your documents stay with you – open Markdown, zero cloud lock-in."
- **Text-Overlay:** *Offenes Markdown · Lokale JSON-Dateien · Lokale Datenhaltung.*
- **UI-Elemente:** Texteditor mit Markdown-Formatierung, Seitenleiste, Fundortübersicht.

#### Szene 4: Tageskapazität & Kognitiver Schutz (0:22 – 0:30)
- **Visuelle Handlung:** Blick auf die "Heute"-Ansicht. Der Nutzer plant eine vierte Aufgabe ein. Der Tagesbalken erreicht 110%. Ein dezenter, warmer Dialog öffnet sich: *Tageskapazität überschritten (5,5h von 5,0h)*. Der Nutzer wählt gelassen: *Aufgabe auf morgen verschieben*. Der Balken wird wieder ruhig grün.
- **Voiceover (DE):** "Ein Planer, der dich schützt, statt dich anzutreiben. Plane nur, was du heute wirklich schaffen kannst."
- **Voiceover (EN):** "A planner that protects your time instead of pushing you. Keep today realistic."
- **Text-Overlay:** *Tageskapazität & Sanfter Entlastungsdialog.*
- **UI-Elemente:** Kapazitätsanzeige, Entlastungsdialog-Aktionen.

#### Szene 5: Integrierte Pixel-Werkstatt & Cover-Gestaltung (0:30 – 0:35)
- **Visuelle Handlung:** Kurzer Schnitt in die Pixel-Werkstatt: Ein Icon wird mit der 16-Farben-Palette pixelgenau schattiert und direkt als Titelbild für das Notizbuch übernommen.
- **Voiceover (DE):** "Von der schnellen Skizze bis zum eigenen Buch-Cover. Alles an einem Ort."
- **Voiceover (EN):** "From a quick sketch to your custom cover. All in one place."
- **Text-Overlay:** *Integrierte Pixel-Werkstatt · Kreativer Ausgleich.*
- **UI-Elemente:** Pixel-Canvas, Farbauswahl, Notizbuch-Titelbild.

#### Szene 6: Endcard & GitHub Release v1.0.2 (0:35 – 0:38)
- **Visuelle Handlung:** Schlichter, eleganter Ausklang. Zentriertes Glide-Logo. Darunter der verbindliche Claim (D72/D74) und die Download-Hinweise für macOS (Apple Silicon arm64), Windows (x64) sowie Quellstart für Linux und macOS Intel.
- **Voiceover (DE):** "Glide 1.0.2. Jetzt quelloffen und kostenlos auf GitHub."
- **Voiceover (EN):** "Glide 1.0.2. Open source and free on GitHub now."
- **Text-Overlay:**
  **Glide 1.0.2**  
  *Aufgaben planen. Ideen verbinden. Selbst gestalten.*  
  `github.com/n05a-design/glide-to-do` · MPL-2.0
- **Audio:** Warmer Schlussakkord.

---

### 4.2 Format B: Preview-Trailer Glide Bento Box System (Laufzeit: 26 Sekunden)

**Titel:** *Glide Bento – Die modulare Startseite der nächsten Generation*  
**Laufzeit:** 26 Sekunden  
**Sounddesign:** Moderner, rhythmischer Ambient-Synth mit sanften Klicks; technisch fokussiert.

```
0:00 ── Szene B1: Modulare Übersicht ──> 0:08 ── Szene B2: Adaptive Spalten ──> 0:16
0:16 ── Szene B3: Widget-Interaktion ──> 0:22 ── Szene B4: Entwicklungs-Endcard ──> 0:26
```

#### Szene B1: Modulare Übersicht (0:00 – 0:08)
- **Visuelle Handlung:** Die neue Bento-Startseite öffnet sich. Strukturierte Kacheln ordnen Aufgaben, Metriken, Notizbuch-Raster und Pinnwand-Vorschau in einem harmonischen Raster an.
- **Voiceover (DE):** "Ein Blick, der Ordnung schafft. Das neue Glide Bento Box System."
- **Voiceover (EN):** "Clarity at a glance. The new Glide Bento Box System."
- **Text-Overlay:** *Glide Bento System 0.1.0 · Modulare Startseite.*
- **UI-Elemente:** BentoGrid, BentoCard, BentoHeader, BentoMetric.

#### Szene B2: Adaptive Spalten & Responsivität (0:08 – 0:16)
- **Visuelle Handlung:** Das Fenster wird verkleinert. Das Layout wechselt nahtlos und flackerfrei vom 3-spaltigen Standard-Grid in das 2-spaltige Fokus-Grid. Die Karten passen ihren Inhalt harmonisch an.
- **Voiceover (DE):** "Passt sich deinem Bildschirm an. Vom großen Monitor bis zum kompakten Laptop."
- **Voiceover (EN):** "Adapts to your screen. From widescreen displays to compact laptops."
- **Text-Overlay:** *Adaptive Spaltenplanung · 3-Spalten & 2-Spalten Layout.*
- **UI-Elemente:** Responsive Breakpoints, dynamische Kachelreorganisation.

#### Szene B3: Widget-Interaktion & Schnellaktionen (0:16 – 0:22)
- **Visuelle Handlung:** Klick auf eine Schnellaktion in der Heute-BentoCard; die Tageskapazität aktualisiert sich live; Umschalten zwischen Kompakt- und Detailansicht.
- **Voiceover (DE):** "Schnelle Aktionen, lebendige Metriken, nahtlose Navigation."
- **Voiceover (EN):** "Quick actions, live metrics, seamless navigation."
- **Text-Overlay:** *BentoActions · Live-Metriken · Nahtlose Shell-Integration.*
- **UI-Elemente:** BentoActions, BentoMetric, Hover-Zustände.

#### Szene B4: Entwicklungs-Endcard (0:22 – 0:26)
- **Visuelle Handlung:** Vorschau-Badge: "Entwicklungsstand auf main – Vorschau auf kommende Releases". Verweis auf die Dokumentation und das Repository.
- **Voiceover (DE):** "Das Bento-System wächst auf GitHub main. Gestalte die Zukunft von Glide mit."
- **Voiceover (EN):** "The Bento System is evolving on GitHub main. Shape the future with us."
- **Text-Overlay:**
  **Glide Bento 0.1.0** · Preview auf `main`  
  `src/glide/glide_bento` · MPL-2.0
- **Audio:** Sanfter Ausklang.

---

## 5. Feature-GIF- & Tutorial-Strategie (§42)

### 5.1 Spezifikation der 6 Feature-GIFs

Alle GIFs werden mit 1280x720 Pixeln bei 30 fps und einer Farbreduktion auf 128 Farben mit dezentem Dithering gerendert, um Dateigrößen unter 2,5 MB zu garantieren.

1. **GIF 01 – Natürliche Schnellerfassung:**
   - *Ablauf:* Cursor öffnet das Schnellerfassungsfeld mit `Cmd+N` / `Strg+N`. Eingabe von `Steuerunterlagen sortieren freitag 45m !hoch`. Live-Tagging der Bestandteile in sanften Farben. Bestätigung mit `Enter`. Die Aufgabe reiht sich lautlos ein.
   - *Dauer:* 4,5 Sekunden Loop.
2. **GIF 02 – Visuelle Pinnwand & Magnetische Verbindungen:**
   - *Ablauf:* Eine Notizkarte und eine Bildkarte werden auf der Pinnwand verschoben. Mit der Maus wird vom Verbindungspunkt der Notizkarte ein Faden gezogen, der magnetisch am Bild einrastet. Beschriftung der Kante mit "Referenz".
   - *Dauer:* 5,2 Sekunden Loop.
3. **GIF 03 – Mauslose Tastaturnavigation:**
   - *Ablauf:* Einblenden von Tastatur-Shortcuts als Overlay (`J`/`K` für Navigation, `X` zum Erledigen, `E` für Inspektor, `1`-`4` für Priorität). Flüssiges Durchwandern der Tagesaufgaben in 120 WPM Geschwindigkeit.
   - *Dauer:* 6,0 Sekunden Loop.
4. **GIF 04 – Das Glide Bento Dashboard:**
   - *Ablauf:* Die Startseite öffnet sich. Sanfter Übergang zwischen 3-spaltigem Standard-Layout und 2-spaltigem Fokusmodus beim Ändern der Fensterbreite. Aufklappen einer Bento-Karte zur Detailansicht.
   - *Dauer:* 5,5 Sekunden Loop.
5. **GIF 05 – Nahtloser Import & Export:**
   - *Ablauf:* Drag & Drop einer Markdown-Datei in Glide -> Sofortiges Erscheinen als formatierte Notizseite. Export einer Pinnwand nach JSON Canvas 1.0 mit Öffnen in einem Canvas-Viewer.
   - *Dauer:* 6,8 Sekunden Loop.
6. **GIF 06 – Ästhetischer Paletten- und Themenwechsel:**
   - *Ablauf:* Umschalten über `Cmd+T` / `Strg+T` von "Pinnwand Warm" zu "Studio Dunkel" und "Papier Klar". Die Typografie und UI-Elemente passen sich ohne Flackern adaptiv an.
   - *Dauer:* 4,8 Sekunden Loop.

---

### 5.2 Zehnteilige Tutorial-Roadmap (T01 – T10)

| Nr. | Tutorial-Titel | Kerninhalt & Lernziel | Format | Zielgruppe |
|---|---|---|---|---|
| **T01** | *In 3 Minuten startklar* | Download, Gatekeeper/SmartScreen Bestätigung, Erststart, das erste Notizbuch. | Text + 3 Bilder | Alle Einsteiger |
| **T02** | *Tagesplanung ohne Stress* | Feste Kapazitäten definieren, realistische Puffer, Arbeiten mit dem Entlastungsdialog. | Interaktiver Guide | Freelancer, ADHS-Fokus |
| **T03** | *Die Tastatur als Steuerpult* | Alle Kernshortcuts für Navigation, Erfassung, Tags und Notizaufrufe. | Cheatsheet + GIF | Power-User, Entwickler |
| **T04** | *Visuelles Denken auf der Pinnwand* | Moodboards anlegen, JSON Canvas 1.0 Export, Karten verbinden und gruppieren. | Schritt-für-Schritt | Designer, Kreative |
| **T05** | *Notizen & Bücher strukturieren* | Markdown-Syntax in Glide, Checklisten, Bearbeitungszeiten und Fundortübersicht. | Dokumentation | Wissensarbeiter |
| **T06** | *Pixel-Art für Nicht-Künstler* | Icons und Cover mit 16 Farben zeichnen, Eckstempel anwenden, Sprites exportieren. | Video-Short (60s) | Designer, Neugierige |
| **T07** | *Lokale Datensicherung & Sync* | Speicherorte verstehen, Sync via Nextcloud/Synology, USB-Stick-Portabilität. | Sicherheitsleitfaden | Datenschutz-Fokussierte |
| **T08** | *Der Glide Agent-Skill für LLMs* | Anbindung an Claude Code, Antigravity und Codex; strukturierte Prompts; Safe Import. | Entwickler-Tutorial | Entwickler, KI-Nutzer |
| **T09** | *Bento Boxen anpassen* | Das Bento-System verstehen, Layouts skalieren, eigene Modulkombinationen. | Architektur-Guide | Fortgeschrittene |
| **T10** | *Großprojekte in Glide meistern* | Komplexe Vorhaben mit Notizbüchern, Meilensteinen und Tagesfokus zerlegen. | Case Study | Selbstständige, Autoren |

---

## 6. Pressekit & Brand Guidelines (§43)

### 6.1 Logo & Wortmarke
- **Wortmarke:** `Glide` (Großes G, runde und geometrische Minuskeln).
- **Claim:**
  - **Primär (Inhaberentscheidung D72 / D74):** *Aufgaben planen. Ideen verbinden. Selbst gestalten.*
  - **Sekundär (Marketing-Baseline):** *Klarheit für deine Tage. Raum für deine Ideen.*
- **Schutzraum:** Mindestens die Höhe des Großbuchstabens `G` auf allen vier Seiten.
- **Mindestgröße:** Digital: 32 px Höhe; Print: 12 mm Höhe.
- **Hintergründe:** Das primäre Logo steht auf dunklem Graphit (`#18191B`) oder warmem Papierweiß (`#F8F9FA`). Niemals auf unruhig gemusterten Hintergründen platzieren.

### 6.2 Offizielle Farbpalette

| Farbrolle | Hex-Code | RGB | Verwendung | Kontrast (APCA / WCAG) |
|---|---|---|---|---|
| **Base Slate (Dunkel)** | `#1E2024` | `30, 32, 36` | Primärer Fensterhintergrund im Dunkelmodus | Basis |
| **Paper Canvas (Hell)** | `#F5F6F8` | `245, 246, 248` | Primärer Fensterhintergrund im Hellmodus | Basis |
| **Card Surface (Dark)** | `#282A30` | `40, 42, 48` | Bento-Karten, Pinnwand-Karten Hintergrund | 1:1.3 zu Base |
| **Card Surface (Light)**| `#FFFFFF` | `255, 255, 255` | Bento-Karten, Notizseiten im Hellmodus | 1:1.1 zu Canvas |
| **Text Primary (Dark)** | `#EAECEF` | `234, 236, 239` | Haupttext, Titel im Dunkelmodus | > 12:1 (AAA) |
| **Text Primary (Light)**| `#1A1D20` | `26, 29, 32` | Haupttext, Titel im Hellmodus | > 13:1 (AAA) |
| **Text Muted** | `#8A909A` | `138, 144, 154` | Metadaten, Datumsangaben, Shortcuts | > 4.5:1 (AA) |
| **Accent Amber (Fokus)**| `#D97706` | `217, 119, 6` | Kapazitätswarnungen, aktive Foki, Pins | > 4.8:1 auf Dark |
| **Accent Teal (Ruhig)** | `#0D9488` | `13, 148, 136` | Erledigt-Status, sichere Kapazität, Links | > 4.5:1 auf Dark |
| **Accent Berry** | `#9333EA` | `147, 51, 234` | Pixel-Werkstatt, Spezialkategorien | > 4.5:1 auf Light |

### 6.3 Typografie-Hierarchie
Glide setzt kompromisslos auf native, hochoptimierte Systemschriften, um null Ladezeit und perfektes Schrift-Rendering auf jedem Betriebssystem zu gewährleisten:
- **macOS:** `SF Pro Display` (Titel) / `SF Pro Text` (Fließtext) / `SF Mono` (Code & Zeitangaben)
- **Windows:** `Segoe UI Variable Display` (Titel) / `Segoe UI` (Fließtext) / `Cascadia Code` (Code)
- **Linux:** `DejaVu Sans` / `Ubuntu` / `Liberation Mono`

**Hierarchie:**
- H1 (Fenstertitel, Dashboard): 22–24 pt, Bold, Letter-Spacing -0.02em.
- H2 (Abschnitts- & Bento-Titel): 16–18 pt, Semi-Bold.
- H3 (Kartenheader, Dialoge): 13–14 pt, Medium.
- Body (Fließtext, Notizen): 13–14 pt, Regular, Zeilenabstand 1.45.
- Caption (Shortcuts, Metadaten): 10–11 pt, Regular, dezent abgesetzt.

### 6.4 Tone of Voice (Sprach- & Kommunikationsregeln)

| Prinzip | Do's (So kommuniziert Glide) | Don'ts (Vermeiden!) |
|---|---|---|
| **Echtheit & Ruhe** | "Schütze deine Tageskapazität." | "Maximiere dein Potenzial! Vernichte deine To-Dos!" |
| **Respekt für Zeit** | "Plane nur, was heute möglich ist." | "Schließe 10 Aufgaben ab, um dein Tagesziel zu erreichen!" |
| **Technisch ehrlich** | "Lokal gespeicherte JSON-Dateien ohne Cloudübertragung." | "Militärisch verschlüsselte Super-Cloud mit 100% KI-Magie." |
| **Transparenz** | "Unsignierter Prerelease – 2 Klicks zur Freigabe in Gatekeeper." | Verschweigen von Zertifikatswarnungen oder Beschönigen als Fehler des Nutzers. |
| **Lizenz & Open Source** | "Freie Software unter der Mozilla Public License 2.0." | "Dauerhaft kostenlos für immer" (klingt nach Freemium-Falle). |

---

## 7. Landingpage-Konzept (§44)

Die offizielle Produkt-Landingpage (vorgesehen unter `n05a-design.github.io/glide-to-do` oder eigenständiger Domain) strukturiert sich in 21 präzise definierte Abschnitte:

### 7.1 Vollständige 21-Sektionen-Struktur

1. **Top Announcement Bar:**  
   *Neu: Glide 1.0.2 Release jetzt auf GitHub verfügbar · Lokale Datenhaltung & ruhige Produktivität (Bento 0.1.0 Vorschau auf main)* (Link zu GitHub Releases).
2. **Navigation Header:**  
   Logo, Links zu *Philosophie*, *Funktionen*, *Bento System (Vorschau)*, *Dokumentation*, *GitHub* und primärer CTA-Button *Herunterladen (v1.0.2)*.
3. **Hero-Sektion:**  
   - Headline: *Aufgaben planen. Ideen verbinden. Selbst gestalten.* (Inhaberentscheidung D72/D74; sekundär: *Klarheit für deine Tage. Raum für deine Ideen.*)
   - Subline: *Die ruhige, lokale Arbeitsumgebung für Aufgaben, Notizen, visuelle Pinnwände und Pixel-Art. Ohne Cloud-Zwang, ohne Tracking, quelloffen.*
   - CTA-Duo: Primär `[Für macOS (Apple Silicon) herunterladen]` / `[Für Windows (x64) herunterladen]` + Quellstart-Hinweis für Linux & macOS Intel + Sekundär `[GitHub Repository ansehen]`.
   - Micro-Copy: *Glide 1.0.2 · Quelloffen unter MPL-2.0 · Lokale Datenhaltung ohne externe Server*.
4. **Hero Visual / Interaktiver Vorschau-Frame:**  
   Großer, hochauflösender Screenshot der Arbeitsumgebung mit Aufgaben, Pinnwand und Notizbüchern (Vorschau-Frame mit Bento-Dashboard als kommender Entwicklungsstand).
5. **Drei Grundpfeiler (Social Proof der Philosophie):**  
   - *1. Kognitive Ruhe:* Keine Benachrichtigungen, keine Streaks, kein Gamification-Druck.
   - *2. Volle Datenhoheit:* Reines lokales Dateisystem. Du besitzt deine Daten für immer.
   - *3. Vier Werkzeuge in Einem:* Aufgaben, Notizen, Canvas und Pixel-Studio nahtlos vereint.
6. **Das Bento-Dashboard (Glide Bento System `0.1.0` – Vorschau auf `main` nach Glide 1.0.2):**  
   Präsentation der modularen Startseite für zukünftige Releases. Interaktive Darstellung der Widgets: Tageskapazität, Schnellzugriff, offene Fälligkeiten.
7. **Produktsäule 1: Aufgaben & Tageskapazität (WA-12):**  
   Erklärung des kognitiven Schutzes. Warum feste Stundenlimits Überlastung verhindern und wie der sanfte Entlastungsdialog hilft.
8. **Produktsäule 2: Visuelle Pinnwand (JSON Canvas 1.0):**  
   Präsentation der freien Arbeitsfläche. Gedanken räumlich anordnen, Verbindungen ziehen, Ideen visuell reifen lassen.
9. **Produktsäule 3: Strukturierte Notizseiten & Bücher:**  
   Fokussiertes Schreiben in sauberem Markdown. Verknüpfung von Notizen mit konkreten Aufgabenzeiten.
10. **Produktsäule 4: Die integrierte Pixel-Werkstatt:**  
    Kreativer Ausgleich direkt im Werkzeug. Eigene Buch-Cover, Icons und Sprites mit harmonischen Farbpaletten gestalten.
11. **Produktsäule 5: Nahtloser Datenaustausch & Standards:**  
    Import und Export für Markdown, JSON Canvas 1.0 und Austauschformate. Keine Datensilos.
12. **Produktsäule 6: KI-Agenten-Bereitschaft (glide-to-do Skill):**  
    Wie Entwickler und Power-User lokale Aufgaben mit Claude, Antigravity oder Codex automatisieren – sicher und dokumentbasiert.
13. **Große Feature-Vergleichstabelle:**  
    Detaillierter Vergleich: Glide vs. Things 3 vs. Notion vs. Sunsama vs. Obsidian (§18.2).
14. **Lokale Architektur & Datenschutzversprechen:**  
    Erklärung des "Zero-Network-Default": Warum Glide keine Telemetrie sendet und keine Server benötigt.
15. **Transparente Installationsanleitung & Gatekeeper-Aufklärung:**  
    Klarer Kasten für macOS und Windows: Erklärung, warum der Prerelease aktuell als "nicht verifizierter Entwickler" eingestuft wird, und die 2 Klicks zur Ausführung.
16. **Nutzerstimmen & Entwickler-Zitate:**  
    Ausgewählte Zitate von Testnutzern aus der Kreativ-, Freelancer- und Open-Source-Community.
17. **Release-Historie & Versionsstatus:**  
    Transparenter Überblick über v1.0.2, das System V1.87 und die nächsten Meilensteine der Roadmap.
18. **Entwicklungs-Roadmap (Vorschau auf v1.0.3 & v1.1.0):**  
    Zeiterfassungs-Export (WA-08), Pufferzeiten (WA-12-Rest), Vorlagen-Bibliothek (L4).
19. **Open-Source-Community & Mitwirken:**  
    Einladung zur Mitarbeit auf GitHub: Issues, Discussions, Code-Beiträge und Dokumentation.
20. **Häufig gestellte Fragen (FAQ):**  
    8 ausführliche Antworten (Kosten, Sync, Mobil-App, Datensicherheit, Systemanforderungen).
21. **Footer & Impressum:**  
    Links zu GitHub, Lizenz (MPL-2.0), Dokumentation, Release Notes, Impressum und Datenschutzhinweis.

---

### 7.2 Zweisprachiges Copywriting (Auszug Hero-Bereich)

#### Deutsch (DE)
- **Titelzeile:** *Aufgaben planen. Ideen verbinden. Selbst gestalten.* (Sekundär: *Klarheit für deine Tage. Raum für deine Ideen.*)
- **Subline:** *Glide vereint Aufgaben, Notizen, visuelle Pinnwände und eine Pixel-Werkstatt in einer schnellen Desktop-App. 100% lokal, quelloffen und entwickelt mit dem Ziel, kognitive Reizüberflutung zu minimieren.*
- **Buttons:** `[Glide 1.0.2 herunterladen]` · `[Quellcode auf GitHub]`
- **Prerelease-Hinweis:** *Aktueller Prerelease v1.0.2 mit nativen Binärpaketen für macOS (Apple Silicon arm64) und Windows (x64); Quellstart für Linux und macOS Intel.*

#### Englisch (EN)
- **Headline:** *Plan tasks. Connect ideas. Shape your world.* (Secondary: *Calm planning for your days. Space for your ideas.*)
- **Subline:** *Glide seamlessly brings together tasks, structured notes, visual pinboards, and a pixel-art workshop in a calm desktop environment. 100% local-first, open-source, designed to minimize cognitive overload.*
- **Buttons:** `[Download Glide 1.0.2]` · `[View Source on GitHub]`
- **Prerelease Badge:** *Current Prerelease v1.0.2 with native packages for macOS (Apple Silicon arm64) and Windows (x64); run from source on Linux and Intel Macs.*

---

### 7.3 Hosting-Evaluation für die Webpräsenz

| Kriterium | GitHub Pages (Empfohlen für Phase 1) | Cloudflare Pages (Empfohlen für Phase 2) | Netlify |
|---|---|---|---|
| **Repository-Integration** | **Perfekt** (Direkt aus `docs/` oder `gh-pages` Branch) | Sehr gut (Automatischer Git-Build) | Sehr gut (Automatischer Git-Build) |
| **Kosten** | 100% Kostenlos (unbegrenzt für Open Source) | 100% Kostenlos (sehr großzügiges Limit) | Kostenlos mit Bandbreiten-Deckel |
| **Datenschutz & DSGVO** | US-Hosting, kein Standard-AVV für Free | Globales Anycast-Netzwerk, EU-Optionen | US-basiert |
| **Eigene Domain & SSL** | Automatisch via Let's Encrypt | Automatisch via Cloudflare SSL | Automatisch via Let's Encrypt |
| **Performance (TTFB)** | Gut (~80–150 ms) | **Exzellent** (< 30 ms über Edge) | Sehr gut (~50–80 ms) |
| **Wartungsaufwand** | **Null** (Kein externes Konto erforderlich) | Gering (Cloudflare-Dashboard) | Gering (Netlify-Dashboard) |
| **Strategisches Urteil** | **Sofortige Empfehlung:** Start mit GitHub Pages (`n05a-design.github.io/glide-to-do`), da keine zusätzlichen Dienste oder Tokens konfiguriert werden müssen. | **Folgeschritt:** Sobald eine eigene Domain (z.B. `glide-app.org` oder `glide-planner.com`) geschaltet wird, Umzug auf Cloudflare Pages für maximale Geschwindigkeit. | Nur als Fallback, falls Cloudflare vermieden werden soll. |

---

## 8. GitHub-Präsenz & Community-Struktur (§45)

### 8.1 Repository About-Texte
- **Kurz (bis 140 Zeichen):**  
  *Ruhiger, lokaler Desktop-Planer für Aufgaben, Notizen, Pinnwand & Pixel-Art. 100% offline, kein Konto, quelloffen unter MPL-2.0.*
- **Mittel (bis 300 Zeichen):**  
  *Glide ist der kognitiv beruhigende Local-First-Arbeitsplatz für Windows, macOS und Linux. Verbindet realistische Tageskapazitätsplanung, Markdown-Notizen, visuelle Pinnwände (JSON Canvas 1.0) und eine Pixel-Werkstatt. Nativ für Windows (x64) & macOS (Apple Silicon); Quellstart für Linux. Quelloffen unter MPL-2.0.*
- **Englisch (Standard About):**  
  *Calm, local-first desktop workspace for realistic daily planning, structured notes, visual pinboards (JSON Canvas), and pixel art. 100% offline, no cloud lock-in, open-source under MPL-2.0.*

### 8.2 Analyse der 20 semantischen GitHub-Topics
1. `productivity` – Zentrales Suchfeld für Produktivitätssoftware.
2. `todo` – Standardkategorie für Aufgabenverwaltung.
3. `task-manager` – Präzise Einordnung für Anwender auf der Suche nach Things-/Todoist-Alternativen.
4. `local-first` – Kernbewegung moderner Softwarearchitektur (keine zwingende Cloud).
5. `offline-first` – Unverzichtbares Kriterium für datenschutzbewusste Nutzer.
6. `markdown` – Relevanz für Wissensarbeiter und Notizbuch-Nutzer.
7. `json-canvas` – Auffindbarkeit für das wachsende Canvas-Ökosystem (Obsidian-Nutzer).
8. `bento-grid` – Suchbegriff für moderne UI-Komposition und Design-Systeme.
9. `pixel-art` – Alleinstellungsmerkmal für die integrierte Kreativ-Werkstatt.
10. `calm-tech` – Positionierung gegen Reizüberflutung und Gamification.
11. `adhd-friendly` – Wichtige Zielgruppe für werkzeugunterstützte kognitive Entlastung.
12. `time-blocking` – Gezieltes Planen nach Tagesstunden und Kapazitäten.
13. `python` – Primäre Technologiesprache (Anziehung von Mitwirkenden).
14. `tkinter` – Referenzimplementierung moderner Oberflächen auf Basis von Tk 9.
15. `desktop-app` – Abgrenzung von reinen Web- und SaaS-Diensten.
16. `macos` – Relevanz für Apple-Silicon- und Intel-Desktop-Nutzer.
17. `windows` – Relevanz für Windows-10/11-Anwender.
18. `linux` – Relevanz für quelloffene Desktop-Umgebungen.
19. `open-source` – Unverzichtbares Metadatum für FOSS-Enthusiasten.
20. `mpl-2` – Rechtliche Klarheit über die Mozilla Public License 2.0.

### 8.3 Briefing für das Social Preview Image (1280x640 px)
- **Aufbau:** Dunkler Graphit-Hintergrund (`#18191B`) mit dezentem 1px-Raster im Hintergrund.
- **Zentrum links:** Elegantes Glide-Logo mit Text *Glide* in Weiß, darunter der Claim *Aufgaben planen. Ideen verbinden. Selbst gestalten.* (Inhaberentscheidung D72/D74) in Hellgrau (`#8A909A`) und die drei Badges `v1.0.2`, `100% Local-First`, `MPL-2.0`.
- **Zentrum rechts:** Perspektivisch leicht geneigter, gestochen scharfer Ausschnitt des Bento-Dashboards mit der aktiven Pinnwand und der Pixel-Werkstatt.
- **Typografie:** SF Pro / Segoe UI, absolut lesbar auch als verkleinertes Thumbnail (600x300 px) in Twitter/Mastodon-Feeds.

### 8.4 GitHub Discussions Struktur
Zur Bündelung von Anfragen und zur Vermeidung überquellender Issues werden fünf Diskussionskategorien aktiviert:
1. **Announcements (Ankündigungen):** Nur Lesezugriff für Nutzer; offizielle Release Notes, Meilensteine und Sicherheitsmeldungen durch Maintainer.
2. **Q&A (Fragen & Antworten):** Schnelle Hilfe bei Installation, Gatekeeper-Bypass, Tastenkombinationen und Dateispeicherung.
3. **Show and Tell (Zeigt eure Setups):** Nutzer teilen ihre Bento-Layouts, Pinnwand-Moodboards und Pixel-Cover.
4. **Ideas & RFCs (Vorschläge):** Diskussion neuer Funktionsvorschläge (z.B. L1–L5) vor der Aufnahme in den Entwicklungsplan.
5. **Design & Themes (Gestaltung):** Austausch über Farbpaletten, Typografie und barrierefreie Kontraste.

### 8.5 GitHub Projects Setup (Now / Next / Later)
Das öffentliche GitHub Project Board wird in vier transparente Spalten gegliedert:
- **Now (In aktiver Bearbeitung):** Dokumentationskonsolidierung (PR #198), Standprüfung, Bento-Komponentenabgleich.
- **Next (Nächste Lieferstufe v1.0.3):** WA-08 (Soll-Ist-Zeiterfassungs-Export), WA-12-Rest (Pufferzeiten & Spätstart-Dialog).
- **Later (Mittelfristige Roadmap v1.1.0):** Bento 0.2.0 (Multi-Span Grid), L4 (Vorlagen-Bibliothek), M04 (Lokaler MCP-Server).
- **Shipped (Abgeschlossen):** v1.0.2 Prerelease, Bento 0.1.0 Grundgerüst, Framework-Shell 0.6.2.

### 8.6 GitHub Wiki & Packages Statement (I11 B)
- **GitHub Wiki:** Bleibt deaktiviert. Die gesamte Dokumentation liegt versionskontrolliert im Repository unter `docs/` und `00_Arbeitsvorbereitung/`, um Divergenz und veraltete Stände zu verhindern.
- **GitHub Packages:** Bleibt vorerst inaktiv. Glide liefert eigenständige Installer über GitHub Releases aus; PyPI- und Container-Releases sind für spätere Automationsstufen vorbehalten (D43).

---

## 9. Nutzerfeedback- & Validierungsprotokoll (§46)

Um den Erfolg von Glide 1.0.2 und der nachfolgenden Versionen systematisch zu messen, wird ein wiederholbares Validierungsverfahren definiert:

### 9.1 Rekrutierungsprofil für 5–10 freiwillige Testnutzer
- **Zusammensetzung:**
  - 2x Kreative / Designer (Fokus: Pinnwand, visuelle Ästhetik, Pixel-Werkstatt)
  - 2x Freelancer / Selbstständige (Fokus: Tageskapazität, Entlastungsdialog, Zeiterfassung)
  - 2x Entwickler / Tech-Enthusiasten (Fokus: Tastaturnavigation, Dateistruktur, Agent-Skill)
  - 2x Neurodivergente Nutzer / ADHS-Fokus (Fokus: Kognitive Ruhe, Überlastungsvermeidung)
  - 1x Student / Wissenschaftler (Fokus: Notizbücher, Fundorte)
- **Plattformverteilung:** Mindestens 4x macOS (mind. 1x Intel, 3x Apple Silicon), 4x Windows (Windows 10 & 11), 1x Linux.

### 9.2 Die 10 realistischen Testszenarien

1. **Szenario S01 – Erstinstallation & Gatekeeper:**  
   *Aufgabe:* Lade das DMG bzw. ZIP von GitHub herunter, installiere die Anwendung und starte sie zum ersten Mal.  
   *Erfolg:* Nutzer überwindet Gatekeeper / SmartScreen ohne Frustabbruch in unter 90 Sekunden.
2. **Szenario S02 – Schnellerfassung im Blindflug:**  
   *Aufgabe:* Erfasse 5 Aufgaben für diese Woche nur über die Tastatur mit Datum und Dauer.  
   *Erfolg:* Alle Aufgaben korrekt angelegt, keine Mausberührung erforderlich.
3. **Szenario S03 – Kognitiver Schutz & Kapazitätslimit:**  
   *Aufgabe:* Plane deinen heutigen Tag so voll, dass das Kapazitätslimit von 5 Stunden überschritten wird. Führe den Entlastungsdialog aus.  
   *Erfolg:* Nutzer versteht die visuelle Warnung sofort und verschiebt mindestens eine Aufgabe auf morgen.
4. **Szenario S04 – Das erste Projekt-Notizbuch:**  
   *Aufgabe:* Lege ein Notizbuch "Website Relaunch" an, schreibe eine formatierte Notiz und verknüpfe sie mit zwei Aufgaben.  
   *Erfolg:* Strukturierte Notiz angelegt, Checklistenpunkte reagieren auf Klick.
5. **Szenario S05 – Die kreative Pinnwand:**  
   *Aufgabe:* Öffne eine freie Pinnwand, platziere ein Bild und zwei Notizkarten und verbinde sie mit einer Linie.  
   *Erfolg:* Verbindungsfaden erfolgreich eingerastet, Zoom und Pan flüssig bedient.
6. **Szenario S06 – Die persönliche Pixel-Werkstatt:**  
   *Aufgabe:* Zeichne ein einfaches 16x16 Icon und weise es einem Notizbuch als Cover zu.  
   *Erfolg:* Icon gezeichnet und erfolgreich im Bento-Raster sichtbar gemacht.
7. **Szenario S07 – Fundortsuche nach einem Stichwort:**  
   *Aufgabe:* Finde eine vor 10 Minuten notierte Telefonnummer über die globale Fundortsuche.  
   *Erfolg:* Zielnotiz innerhalb von 5 Sekunden lokalisiert und geöffnet.
8. **Szenario S08 – Datenaustausch via Markdown:**  
   *Aufgabe:* Exportiere eine Seite nach Markdown und prüfe, ob die Datei lesbar im Dateisystem liegt.  
   *Erfolg:* Datei geöffnet und Inhalt bestätigt.
9. **Szenario S09 – Farbpaletten- & Nachtmodus-Wechsel:**  
   *Aufgabe:* Schalte das Design auf Dunkelmodus um und wähle die Palette "Studio".  
   *Erfolg:* Schneller Wechsel ohne Flackern, angenehme Lesbarkeit.
10. **Szenario S10 – Datenportabilität & Beenden:**  
    *Aufgabe:* Schließe Glide, kopiere den Datenordner auf einen USB-Stick und starte die portable Version auf einem Zweitrechner.  
    *Erfolg:* Alle Daten vollständig und unverändert geladen.

### 9.3 Beobachtungsbogen & Bewertungsmatrix

Jeder Testdurchlauf wird mit folgendem standardisierten Erfassungsraster protokolliert:

```markdown
### Testprotokoll – Testperson: [ID] · Datum: 24.11.2026 · Version: Glide 1.0.2

- **Betriebssystem:** macOS Sonoma (Apple Silicon) / Windows 11 / Linux
- **Vorerfahrung mit Tools:** Things 3, Notion, Obsidian, Papier
- **Szenario-Ergebnisse (1 = Gescheitert, 5 = Völlig reibungslos):**
  - S01 (Installation): [1–5] · Beobachtung / Zitat: "..."
  - S02 (Schnellerfassung): [1–5] · Beobachtung / Zitat: "..."
  - S03 (Entlastungsdialog): [1–5] · Beobachtung / Zitat: "..."
  - S04 (Notizbuch): [1–5] · Beobachtung / Zitat: "..."
  - S05 (Pinnwand): [1–5] · Beobachtung / Zitat: "..."
  - S06 (Pixel-Werkstatt): [1–5] · Beobachtung / Zitat: "..."
  - S07 (Fundorte): [1–5] · Beobachtung / Zitat: "..."
  - S08 (Export): [1–5] · Beobachtung / Zitat: "..."
  - S09 (Themen): [1–5] · Beobachtung / Zitat: "..."
  - S10 (Portabilität): [1–5] · Beobachtung / Zitat: "..."

- **Standardized Usability Metrics:**
  - **System Usability Scale (SUS):** Berechneter Score [0–100] (Ziel: > 82 = "Excellent")
  - **Customer Effort Score (CES):** "Wie leicht war es, deinen Tag zu planen?" [1 = Sehr schwer, 7 = Sehr leicht] (Ziel: > 6.0)
  - **Calmness Rating:** "Wie beruhigend wirkte die Oberfläche auf dich?" [1 = Hektisch/Reizüberflutet, 5 = Sehr ruhig/Angenehm] (Ziel: > 4.5)

- **Qualitative Beobachtungen:**
  - Was hat den Nutzer überrascht?
  - Wo gab es ein sichtbares Zögern (> 3 Sekunden)?
  - Welcher Satz fiel beim ersten Öffnen der Pinnwand?
```

### 9.4 Feedback-Schleifen & Schwellenwerte
- **Kritische Hürde:** Wenn mehr als 20% der Testnutzer bei Szenario S01 (Gatekeeper) scheitern, muss die README- und Landingpage-Dokumentation um animierte GIFs der Freigabe erweitert werden.
- **Kognitive Hürde:** Wenn das Calmness Rating unter 4.0 fällt, müssen UI-Ränder, Schriftgrößen oder Kontraste nach den Vorgaben von `DESIGN_RICHTLINIEN.md` weiter beruhigt werden.
- **Funktionale Hürde:** Wiederkehrende Wünsche fließen als RFC in `POST_RELEASE_ENTSCHEIDUNGSVORLAGEN.md` ein und werden dem Inhaber zur Entscheidung vorgelegt.
