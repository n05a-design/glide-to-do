# Glide – Einstieg in die Arbeitsablage

**Repository und Planung (01.10.2026):** Diese Ablage liegt im GitHub-Repository `n05a-design/glide-to-do`. Die Wurzel ist der Projektordner, der Quellbaum liegt in `01_Repository/Glide`. Uploads immer in diese Struktur, nie in einen Unterordner; sonst brechen die Querverweise. Arbeitsregeln für Claude Code: [CLAUDE.md](CLAUDE.md). Analyse und nächste Schritte: [Entwicklungsplan ab 3.33](00_Arbeitsvorbereitung/Glide_Entwicklungsplan_3.33ff_2026-10-01.md) und [beschlossene Entscheidungen D09–D17](00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md).

**3.33.0 startet mit T2/P09a:** Formatsicherung einmal je Dateistand und keine ungenutzte Tabellenmessung. [Fundament-Vertrag und Anschluss](01_Repository/Glide/docs/73_FUNDAMENT_3.33.0.md). Aktive Arbeitskopie: `Github/glide-to-do`.

**Neu am 29.09.2026:**

- das **Logo** aus den neuen Mastern in `20_Grafik_Master`: links neben dem
  Titel (ab der ersten Breitenstufe), in „Über Glide“, im Startfenster und
  als Programmsymbol, in der Oberfläche in der gewählten Akzentfarbe;
- die **Lupe ⌕** in der Kopfzeile für die Suche über Seiten, Punkte und
  Aktionen (auch Strg/Cmd+O);
- die Startseite ohne die Eingabeleiste unten;
- **Inhaltskarten bis ganz unten** – Hinweis und Auswahlleiste stehen im Fuß
  der Karte;
- Sicherungen nur bei Änderung, dazu je Tag der letzte Stand 14 Tage;
- eine Startprüfung, die ältere Bestände gleich umstellt;
- ein Belastungstest für Speichern und Laden;
- der Bereich **„Notizen +“** in der Seitenleiste – Seiten, Listen, Notizen –
  mit Notizübersicht; zugeklappte Ordner bleiben zu, und Bibliotheken und
  Notizbücher haben „+“ und „…“ wie Ordner.

[Übersicht mit Entscheidungsmöglichkeiten vom 29.09.2026](00_Arbeitsvorbereitung/Glide_Uebersicht_und_Entscheidungen_2026-09-29.md) ·
[Vertrag 66, Abschnitte 2.15 und 2.16](01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

**Neu in 3.30** – die Modernisierung nach dem Aufgabenkatalog vom 25.09.2026:

- eine **Pixel-Werkstatt** mit Flächen von 16 bis 128 Zellen, sieben
  Werkzeugen, zwei Farben, Symmetrie, Mustern, Paletten, Rückgängig je Aktion
  und PNG-Export;
- **Pixelsymbole** für Listen und Ordner;
- eine **Startseite**, die man direkt auf der Seite ordnet, dazu angeheftete
  Seiten und Filter;
- **Seiten- und Befehlssuche** mit Strg/Cmd+O;
- ein **Spaltenboard**, das ein Feld setzt, sobald man eine Karte in eine
  andere Spalte zieht;
- **Pinnwand-Bereiche**, beschriftete Verbindungen und ein Präsentationsmodus;
- ein **Notizbuch** (bis 27.09.2026 „Tagebuch“) für alle Inhaltsarten;
- verknüpfte Punkte, Abhängigkeiten und Zeiterfassung;
- das **Archiv** statt Löschen;
- das Design **„Pixel“** mit der Pixelschrift „Pixelify Sans“;
- im Ausbau: Zeitblöcke ziehen, Folien als PDF, Rückgängig beim
  Kartenverschieben, ein Detailbereich mit allen Feldern und Gismo in
  Leerzuständen;
- im zweiten Ausbau (26.09.2026):
  - Anhänge direkt im Detailbereich;
  - Zeichnungen als Bild in Folien;
  - ein Stundenraster neben „Mein Tag“;
  - Gruppierung, die Überschriften und Nummern erhält;
- im dritten Ausbau (26.09.2026):
  - Punkte aus der Liste ins Stundenraster ziehen;
  - die gruppierte Tabelle mit Nummern und Überschriften;
  - die Pixelschrift auch unter Linux ohne Installation;
- bei kleinem Fenster nur das Wichtigste, ohne gequetschte oder
  angeschnittene Teile;
- alle Designs mit lesbarem Kontrast nach WCAG AA;
- ein macOS-Entwicklungsbundle „Glide.app“ (`packaging/macos/baue_app.py`)
  und feste Kennungen für Systembenachrichtigungen;
- je Design fünf Hintergrundverläufe zur Wahl; Kacheln, Listen und Fenster
  werden darüber zu Milchglas;
- eine aufgeräumte Oberfläche: Verlauf als Knopf in der Kopfzeile, „In
  Bearbeitung“ als Abschnitt in „Mein Tag“, Farbe nur mit Bedeutung;
- eine deutlich schnellere Oberfläche; `07_Python-Versionen/Schnellstart.pyw`
  startet ab dem zweiten Mal spürbar schneller.

Neu ist die Seitenart „Seite“: KI-Berichte als Markdown übernehmen, ruhig lesen, Aufgaben
darin wie überall in Glide. Dazu die Ordnertypen Ordner, Bibliothek und Notizbuch
([Konzept](00_Arbeitsvorbereitung/Glide_Konzept_Seiten_wie_Notion_2026-09-26.md)).

Seit dem 27.09.2026:

- Seiten haben einen eigenen Bereich „Seiten +“ mit Vorlagen und dem
  Austauschformat `.glidepage`; eine Bibliothek zeigt ihre Seiten als Tabelle.
- Die Galerie sammelt Bilder.
- Die Oberfläche ist kompakter:
  - Aktionsleiste nur bei Auswahl, Kopfzeile aus Symbolen;
  - einklappbare Seiten und Listen;
  - Titel höchstens 40 Zeichen, Beschreibung neben den Kennzahlen.
- „Tagebuch“ heißt „Notizbuch“.
- Seiten nehmen Bilder auf, die der Text umfließt; Bilder lassen sich
  verschieben, in der Größe ziehen und aus Finder/Explorer hineinziehen.
- Glide nutzt Tk 9: Vorschauen für mehr Bildformate und auf Wunsch
  Systemmitteilungen für Erinnerungen.
- „/“-Befehle beim Anlegen (/morgen, /wichtig …) und wiederkehrende
  Checklisten.
- Seitenleiste, Kopfzeile und Fläche bleiben beim Wechseln der Ansichten
  stehen; kein Ordnerpfad mehr über dem Titel.
- Probedaten „Rundgang“ in `05_Probelisten_Testdaten`.
- [Entscheidungsvorlage und Bestandsprüfung](00_Arbeitsvorbereitung/Glide_Bestandspruefung_und_Entscheidungen_2026-09-27.md).

**Nach dem Update Glide 3.29 nicht mehr starten:** Es überschreibt einen
Bestand im Format 20 bei der ersten Eingabe. Zurück nur über die Vorsicherung
`liste_vor_format20_*.json`.

Das Aufgabenformat ist jetzt 20.
[Modernisierung 3.30](01_Repository/Glide/docs/66_MODERNISIERUNG_3.30.0.md).

Neu in 3.29: **Zeichnungsseiten** als eigene Listenart. Die 128-×-128-Fläche
liegt direkt in der Seitenanzeige von Listen, Ordnern und Tagebüchern, speichert
automatisch und kann ein PNG als Referenz zeigen oder nachzeichnen.
[Zeichnungsseite 3.29](01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md).

Neu in 3.28: Tagebuchordner, datierte Notizseiten und vier Tagebuchvorlagen,
ein pflegbarer Gismo, eine informativere Pinnwandvorschau, kontinuierliches
Scrollen mit gedrücktem Mausrad und eine klar priorisierte Oberfläche für
schmale Fenster. Der nach dem Füttern sichtbare weiße Neuaufbau wurde behoben:
Gismo aktualisiert nur noch seine eigene Karte. [Tagebuch und UI](01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md) ·
[Flackern und Ablageprüfung](01_Repository/Glide/docs/60_FLACKERN_UND_ABLAGEPRUEFUNG_3.28.0.md).

Aktueller Entwicklungsstand: **3.33.1 vom 30.09.2026**, Datenformat 20. Die
Gesamtfreigabe richtet sich nach dem [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md);
ein Entwicklungsstand ist kein signiertes Release.

Durchgehende Grundlage, unabhängig von der jeweils neuesten Funktion:
verschachtelte Listen, Ordner, Notizbücher und Bibliotheken, Seiten, Galerien, Aufgaben, Long-Tasks,
Gruppen, Überschriften, Notizen, Fälligkeit, Wichtigkeit, Wiederholungen,
Erinnerungen, Labels, lokale Anhänge, Kalender, Suche, Rückgängig, Papierkorb,
16 vollständige Praxisvorlagen plus vier Notizbuch- und drei Seitenvorlagen sowie lokale Backups.

[3.14-Bedienung: Bearbeitungstag und Aufwand](01_Repository/Glide/docs/archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md) · [3.13-Bedienung: Tabellenansicht](01_Repository/Glide/docs/archiv/36_TABELLENANSICHT_3.13.0.md).

| Ordner | Aktueller Zweck |
|---|---|
| [01_Repository/Glide](01_Repository/Glide/README.md) | Kanonischer Quellcode, Tests und technische Dokumentation |
| [07_Python-Versionen](07_Python-Versionen/README.md) | Startbare, synchron gehaltene Python-Arbeitskopie mit Ressourcen |
| [05_Probelisten_Testdaten](05_Probelisten_Testdaten/README.md) | 16 Praxisvorlagen und drei aktuelle Beispielbackups, einschließlich „Rundgang“ |
| [00_Arbeitsvorbereitung](00_Arbeitsvorbereitung/README.md) | Planung, Entscheidungen, Sitzungsauswertung, manuelle Prüflisten |
| [20_Grafik_Master](20_Grafik_Master/README.md) | Logo, App-Symbol und Fav-Icon als SVG und PNG, Affinity-Quelle, Stilvorlagen |
| [40_Store_Material](40_Store_Material/README.md) | Entwürfe für die Veröffentlichung |
| [50_Ablage](50_Ablage/README.md) | Historische QA, Screenshots und Rückfallstände |
| [90_Testdaten_Extern](90_Testdaten_Extern/README.md) | Bewusst erhaltene ältere Importbeispiele |

**Dokumentationspflege:** Seit dem ausdrücklichen Auftrag vom 01.10.2026 werden doppelte und überholte Dokumente nach Wissensabgleich gelöscht. Aktuelle Quellen bleiben fortgeschrieben; gültige Funktionsverträge und Prüfbelege bleiben erhalten. [Wissenseinstieg und Bereinigungsnachweis](01_Repository/Glide/docs/75_DOKUMENTATIONSREDUKTION_UND_LOGOS_3.33.1.md).

[Erinnerungen: Bedienung und Grenzen](01_Repository/Glide/docs/archiv/31_ERINNERUNGEN_3.8.0.md) ·
[Systemmitteilungen: Stufen und Grenzen](01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md) ·
[Vorlagenanleitung](01_Repository/Glide/docs/27_VORLAGEN_PRAXISANLEITUNG.md) ·
[Ablageprotokoll](01_Repository/Glide/docs/archiv/28_ABLAGEPRUEFUNG_2026-09-11.md)

Die automatisierte Vollprüfung von 3.30.0 steht im
[QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md). Eine Freigabe ist
sie nicht. Offen bleiben:

- die manuelle Prüfung unter echtem Windows und macOS,
- DPI-Skalierung und Bildschirmleser,
- Signatur, Markenprüfung und Store.

[Aktueller QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md).

Alte Arbeitsversionen wurden nachvollziehbar in lokale Archiv-Unterordner verschoben.
Es wurden keine Dateien endgültig gelöscht und keine echten Nutzdaten importiert.

[Zeichenflächen-Aufgabensammlung](00_Arbeitsvorbereitung/Glide_Aufgabensammlung_Zeichenflaeche_2026-09-23.md) ·
[Kalenderimport aus ICS 3.21](01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md) ·
[Kalenderausgabe als ICS 3.20](01_Repository/Glide/docs/archiv/44_KALENDERAUSGABE_3.20.0.md) ·
[Dauerhafter Änderungsverlauf 3.19](01_Repository/Glide/docs/archiv/43_AENDERUNGSVERLAUF_3.19.0.md) ·
[CSV-Import mit Spaltenzuordnung 3.18](01_Repository/Glide/docs/archiv/42_CSV_IMPORT_3.18.0.md) ·
[Druck- und PDF-Ausgabe 3.17](01_Repository/Glide/docs/archiv/41_DRUCK_UND_PDF_3.17.0.md) ·
[Dokumentationsindex](01_Repository/Glide/docs/00_INDEX.md)
