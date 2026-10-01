# Glide – Konzept „Seiten wie Notion“, offene Punkte und Vorschläge

Stand 27.09.2026 · Glide 3.30.0 · entschieden; Stufe 1, Ordnertypen, Seitenbereich und Galerie sind umgesetzt
(Vertrag 66, Abschnitt 2.11). Der Entwurf vor der Entscheidung liegt in
[Archiv](Archiv/Glide_Konzept_Seiten_wie_Notion_2026-09-26_Entwurf_vor_Entscheidung.md).

## 0. Entscheidungen des Nutzers am 26.09.2026

- **Seite und Notiz bleiben getrennt.** Eine Notiz (Tagebuch) ist etwas
  anderes als eine Seite.
- **Wofür Seiten da sind:** vor allem für den Empfang KI-erzeugter Seiten und
  Berichte. Wichtig sind ein endlos scrollender, leichter Lesefluss und
  einfache Bedienung.
- **Aufgaben in Seiten** sind voll integriert und unterstützen alle
  Glide-Funktionen.
- **Zuletzt und Favoriten** gibt es, aber im Seitenkontext, nicht mit Listen
  gemischt.
- **Felder:** keine eigenen Felder je Liste. Felder werden Glide-weit angelegt
  und lassen sich überall verwenden.
- **Ordnertypen:**
  - „Ordner“ (bisher „Standard“): darin kann alles liegen;
  - „Bibliothek“: Sammlung, etwa Bücher;
  - „Notizbuch“ (bisher „Tagebuch“).

**Umsetzung am 26.09.2026 (Stufe 1):**

- die Seitenart „Seite“ mit Weg A, Markdown-Übernahme, Aufgaben als echte
  Punkte, Lesespalte, Kürzeln, „/“-Menü und Export;
- die Übersicht „Seiten“ mit Favoriten, Zuletzt und allen Seiten;
- die drei Ordnertypen: In einer Bibliothek entstehen Seiten.

**Als Nächstes:**

- Glide-weite Felder mit Tabellen- und Galerieansicht einer Bibliothek;
- Titelbild und Unterseiten.

## 1. Anlass

Der Nutzer hat am 26.09.2026 geschrieben: „Ich will allgemein mehr werden wie
Notion, die App gefällt mir sehr gut.“ Er wünscht sich neue Listenarten,
zuerst eine **erweiterte Notiz**, die wie eine Notion-Seite aufgebaut ist.

**Ein Richtungswechsel:**

- Die [Wettbewerbsrecherche vom 25.09.2026](Glide_Wettbewerbsrecherche_Modernisierung_2026-09-25.md)
  hielt in Abschnitt 5.3 fest: „Glide soll Notion nicht als Baukasten
  nachbauen.“
- Dieses Dokument trennt deshalb das, was Notion zu einem angenehmen
  *Schreib- und Ordnungsort* macht, vom *Datenbank-Baukasten*.
- Ersteres passt zu Glide, Letzteres bleibt nach Abschnitt 7 der Recherche
  außen vor – es sei denn, der Nutzer entscheidet anders.

**Grundlage:**

- vier Bildschirmfotos des Nutzers von Notion (Home mit Titelbild und
  Linkspalten, eine nummerierte Liste, eine Textseite, die Seitenleiste mit
  „Recents“ und „Favorites“);
- die Recherche vom 25.09.2026.

## 2. Was Notion in den Bildschirmfotos ausmacht

| Merkmal | Wirkung | In Glide heute |
|---|---|---|
| Titelbild über der Seite, großes Seitensymbol | Seite hat Charakter, wird wiedererkannt | Pixelsymbol je Liste (AO-050), kein Titelbild |
| Großer Titel, viel Weißraum, schmale Textspalte | ruhiges Lesen | Titel in der Kopfzeile, Inhalt füllt die Breite |
| Blöcke: Überschrift, Text, Liste, Nummerierung, Link | man schreibt einfach los, Struktur entsteht beim Schreiben | Notiz mit B/I/U/H2/Liste/Link (`RichNoteEditor`) |
| Spalten mit Linksammlungen („Alltägliches“, „Leben“) | Startseite als eigene Übersicht | Startseite aus festen Kacheln |
| Seiten in Seiten, Pfad oben („08 Bücher / 2025.01.08 Seoul“) | beliebig tiefe Ablage | Ordner (5 Ebenen) mit Listen |
| Seitenleiste: Zuletzt, Favoriten | schneller Rückweg | „Angeheftet“ auf der Startseite, Verlauf |
| „/“ für Befehle, Leertaste für KI | alles über die Tastatur | Aktionssuche („Aktionen“ in der Kopfzeile) und Schnellöffnen (Strg/Befehl+O), keine „/“-Befehle |

## 3. Vorschlag: neue Seitenart „Seite“

Neben Aufgaben, Notiz, Zeichnung und Pinnwand kommt eine fünfte Seitenart
„Seite“ hinzu. Die bisherige Notiz (Tagebuch) bleibt, wie sie ist.

### 3.1 Inhalt aus Blöcken

- **Text:** Absatz, Überschrift 1–3, Zitat, Hinweisbox mit Symbol, Code,
  Trennlinie.
- **Listen:** Aufzählung, Nummerierung, Umschalter (aufklappbar) und Aufgabe
  mit Kästchen.
  - Eine Aufgabe ist ein echter Glide-Punkt. Sie erscheint in „Mein Tag“,
    trägt Fälligkeit, Labels und Wichtigkeit und zählt in den Kennzahlen.
  - Das ist die Brücke, die Notion nicht hat: Schreiben und Planen im selben
    Dokument.
- **Verweise:**
  - Unterseite: ein Block, der eine eigene Seite öffnet.
  - Link auf eine Liste, eine Zeichnung oder eine Pinnwand.
  - Rückverweise: „Hier erwähnt in …“. Verknüpfungen gibt es seit 3.30
    bereits für Punkte.
- **Eingebettete Ansichten:** Eine Glide-Liste, eine Zeichnung oder ein
  Pinnwandausschnitt steht als Block in der Seite. Ein Klick öffnet sie.
- **Bild:** lokal, in den Anhängen der Seite gespeichert.
- **Spalten:** zwei oder drei nebeneinander, wie auf der Notion-Home.

### 3.2 Bedienung

- Enter beginnt einen neuen Block, Tab rückt ein.
- „/“ öffnet ein Blockmenü mit Suche.
- Markdown-Kürzel beim Tippen:
  - `#`, `##` und `###` für Überschriften;
  - `-` für eine Aufzählung, `1.` für eine Nummerierung;
  - `[]` für eine Aufgabe, `>` für ein Zitat, `---` für eine Trennlinie.
- Jeder Block hat links einen Griff: ziehen zum Verschieben, Klick öffnet
  Umwandeln, Duplizieren und Löschen.
- Rückgängig gilt für jeden Schritt (bestehender Rückgängig-Speicher).

### 3.3 Seitenkopf

- **Titelbild:** ein lokales Bild, oder aus Glide selbst eine Pixelzeichnung
  oder ein Hintergrundverlauf. Das ist die Verbindung zur Pixel-Nische. Bilder
  aus dem Netz gibt es nicht (Recherche, Abschnitt 7).
- **Seitensymbol:** das vorhandene Pixelsymbol, groß über dem Titel.
- **Lesebreite:** Der Text steht in einer ruhigen Spalte (etwa 720 Pixel).
  Umschaltbar auf volle Breite.

### 3.4 Seitenleiste

- Die Abschnitte „Zuletzt“ und „Favoriten“ kommen oben in die Seitenleiste.
  „Favoriten“ ersetzt das bisherige „Angeheftet“ und zeigt denselben Bestand.
- Unterseiten erscheinen im Baum unter ihrer Seite, wie Listen unter einem
  Ordner.

### 3.5 Technik

| Weg | Beschreibung | Vorteil | Nachteil |
|---|---|---|---|
| A: ein Textfeld mit Blöcken als Formatierung | `RichNoteEditor` wird erweitert: Blöcke sind markierte Absätze; Kästchen, Bilder und Trennlinien sind eingebettete Widgets im Text | schnell, flüssig auch bei langen Seiten, Tk-nah | Ziehen einzelner Blöcke und Spalten nur eingeschränkt |
| B: ein Widget je Block | jede Zeile ein eigenes Eingabefeld in einer scrollbaren Fläche | echtes Notion-Gefühl: Griff, Ziehen, Spalten | in Tk bei hunderten Blöcken träge; viel Aufwand für Cursorführung über Blockgrenzen |

**Empfehlung:** Weg A mit Spalten als eigener Blockart (eingebettete
Textfelder). Das ist in Tk der stabile Weg; Ziehen von Blöcken geht über den
Griff am Absatz.

**Datenformat:** Aufgabenformat 21 mit Migration, Sicherung und Tests
(AGENTS.md).

- neue Seitenart `page`;
- Blöcke als Liste `{typ, text, spans, kinder, item_id}`;
- Titelbild und Spalten als Seiteneigenschaften.

Ältere Glide-Versionen öffnen Format 21 schreibgeschützt (seit 3.30
vorhanden).

### 3.6 Umfang und Reihenfolge

1. Seitenart „Seite“ mit Textblöcken, Überschriften, Listen, Aufgaben als
   echte Punkte, „/“-Menü und Markdown-Kürzeln. Format 21.
2. Seitenkopf: Titelbild, großes Symbol, Lesebreite.
3. Unterseiten, Seitenverweise und Rückverweise; „Zuletzt“ und „Favoriten“ in
   der Seitenleiste.
4. Eingebettete Ansichten, Bilder, Spalten.
5. Import aus Notion (Markdown- und CSV-Export von Notion) und Export als
   Markdown.

Jede Stufe ist für sich nutzbar und wird einzeln geprüft.

## 4. Offene Punkte und Probleme

- **Beim Scrollen ausgeblendete Knöpfe:**
  - In den eigenen Aufnahmen fehlten keine Knöpfe.
  - Wahrscheinlich war es das langsame Nachzeichnen: Mit Verlauf kostete ein
    Scrollschritt 525 ms, jetzt rund 150 ms.
  - Falls es bleibt: Ansicht und Stelle nennen, am besten mit einem Bild.
- **Manuelle Prüfungen** (Prüfliste 3.30): Windows-Darstellung samt Verlauf,
  DPI, Bildschirmleser, echte Bedienung.
- **Veröffentlichung:**
  - Logo als PNG exportieren; bisher liegt nur `Glide-Logo.af` vor.
  - Release-Build, Signatur und Notarisierung.
  - Systembenachrichtigungen, Stufe B.
- **Linux:** Pixelschrift nur mit nachgebildeter Bibliothek geprüft.
- **Startseite:** Sie baut aus vielen verschachtelten Rahmen. Das bremst das
  Scrollen auch ohne Verlauf (rund 70 ms je Schritt). Ein Umbau auf eine
  einzige Zeichenfläche würde das halbieren (siehe Abschnitt 5).

## 5. Optimierungsvorschläge

| Vorschlag | Nutzen | Aufwand |
|---|---|---|
| Startseite ohne verschachtelte Rahmen (Kacheln direkt auf einer Fläche) | Scrollen etwa doppelt so schnell | mittel |
| Listenansicht nur sichtbare Zeilen aufbauen (bei sehr langen Listen) | schneller Seitenwechsel ab einigen hundert Punkten | mittel |
| Speichern im Hintergrund bündeln (mehrere Änderungen, ein Schreibvorgang) | weniger Plattenzugriffe, flüssigeres Tippen | klein |
| Startanzeige sofort, Daten danach laden | Fenster erscheint früher | klein |
| Bildvorschauen (Zeichnungen, Anhänge) zwischenspeichern | Startseite und Bibliothek schneller | klein |

## 6. Funktionsvorschläge und Arbeitserleichterung

- **Schnellnotiz überall:** Die Schnellerfassung legt wahlweise eine Seite an
  statt einer Aufgabe.
- **Tagesseite:** „Mein Tag“ bekommt eine Notizspalte für den Tag, eine Seite
  je Datum wie im Tagebuch.
- **Vorlagen für Seiten:** Meeting, Projektsteckbrief, Wochenrückblick.
  Vorlagen mit Feldern gibt es seit 3.30.
- **Wiederkehrende Checklisten:** Eine Checkliste setzt sich nach dem Erledigen
  selbst zurück (Einkauf, Reise).
- **Tastatur zuerst:** „/“-Befehle auch in Aufgabenlisten, etwa „/morgen“ oder
  „/wichtig“.
- **Fokusansicht:** eine Aufgabe groß, Zeiterfassung läuft, alles andere
  ausgeblendet.
- **Import aus Notion und Todoist, Export als Markdown:** für den Umzug und
  gegen das Gefühl, eingesperrt zu sein.

## 7. Fragen an den Nutzer

Die Fragen 1 bis 5 sind beantwortet (Abschnitt 0). Umgesetzt ist Weg A,
weil er das geforderte endlose, flüssige Scrollen trägt. Offen für die
nächste Stufe:

1. **Glide-weite Felder:** Welche Feldtypen zuerst? Vorschlag: Text, Zahl,
   Auswahl, Datum, Häkchen und Link.
2. **Bibliothek:** Soll sie ihre Seiten als Tabelle nach Feldern zeigen, als
   Galerie mit Titelbild oder als beides mit Umschalter?
3. **Wortwahl:** Überall „Notizbuch“ statt „Tagebuch“, also auch in den
   Tagesnotizen und Menüs? Bisher ist nur der Ordnertyp umbenannt.

**Nachtrag 27.09.2026** (Entscheidungen des Nutzers, umgesetzt):

- Seiten haben einen eigenen Bereich „Seiten +“ in der Seitenleiste,
  zwischen Papierkorb und „Listen +“, mit Bibliotheken („Bücher“).
- Seiten bekommen die Funktionen von Listen: Vorlagen und ein eigenes
  Austauschformat (`.glidepage`); Aufgaben und Labels teilen sie mit den
  Listen.
- „Eine Sammlung an Bildern ist eine Galerie“: neue Listenart „Galerie“.
  Frage 2 bleibt offen – ob die Bibliothek ihre Seiten zusätzlich als Galerie
  mit Titelbild zeigen soll.
