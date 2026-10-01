# QA-Bericht – Glide 3.30.0

Stand 30.09.2026 (Nachprüfung und Version 3.31.0) · App 3.31.0 · Datenformat 20 · macOS, Python 3.14.5, Tk 9.0.3

## Ergebnis 3.30.0

3.30.0 setzt die Modernisierung mit Aufgabenformat 20 um
([Vertrag 3.30](66_MODERNISIERUNG_3.30.0.md)). Geprüft wurde auf dem
Entwicklungs-Mac mit isoliertem `GLIDE_DATA_DIR`.

### Nachprüfung und Version 3.31.0 vom 30.09.2026 – maßgeblicher Endstand

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitte 2.17 und 2.18.
Protokoll: [`tests/qa-3.31.0/nachpruefung_2026-09-30`](../tests/qa-3.31.0/nachpruefung_2026-09-30/ergebnis.json).

- **Ergebnis:** Exitcode 0; 69 automatisierte Schritte, 54 Suiten. Übersprungen
  wie immer unter macOS: Screenshots (nur Linux/Windows) und die Sichtprüfung
  durch eine Person.
- **Erster Lauf** (`nachpruefung_erster_lauf_2026-09-30`): Exitcode 1.
  `test_template_workflows` und `test_features330` hingen an der alten
  Versionsnummer (Vorlagenkatalog, Referenz Format 20). Vorlagen neu erzeugt;
  die Referenz trägt fest 3.30.0, die Version, mit der Format 20 kam.
- **Fenster:** `test_fenster330` öffnete 41 Fenster über Menüleiste,
  „+“-Menüs, Kontextmenüs und Knöpfe; je ein Foto des eigenen Fensters liegt
  unter `fenster/`. Die Dateiauswahl des Systems (etwa beim Referenzbild)
  lässt sich nicht automatisch bedienen. Geprüft wird, dass der Befehl sie
  nach dem Schließen des Menüs aufruft und dass das Fenster danach erscheint.
  Mit echter Maus bleibt das Punkt A17 der manuellen Prüfliste.
- **Tempo** gegen reines Tk (49,2 ms je Bild): Liste 73,8, Tabelle 24,9,
  Seite 77,3, Startseite mit Verlauf 73,6, „Listen und Ordner“ mit Verlauf
  124,2 ms. Die Übersicht liegt damit bei rund 8 Bildern je Sekunde, vorher 3,5.
- **Abgleich:** `07_Python-Versionen` und `build/macos/Glide.app` tragen
  denselben Code (SHA-256). Vorher liefen dort noch Dateien vom 29.09.2026,
  13:37. Deshalb sah der Inhaber die Fehler weiter.
- **Gefunden bei der Nachprüfung:** Das „…“ einer überfahrenen Zeile blieb
  beim Einklappen von Seiten und Notizen stehen (behoben, geprüft).

### Logo, Sicherungen und Notizbereich vom 29.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitte 2.15 und 2.16,
nach den Antworten auf die
[Prüfung vom 28.09.2026](../../../00_Arbeitsvorbereitung/Glide_Pruefung_und_Entscheidungen_2026-09-28.md)
und dem zweiten Auftrag des Tages (Notizen in der Seitenleiste).

- **Neue Suiten:**
  - `test_logo330`: Master, Einfärbung, Lage, Breitenstufe, Rückfall,
    Programmsymbol, Lupe;
  - `test_kartenfuss330`: 51 Ansichtswechsel, Karte bis unten, Kartenfuß;
  - `test_speicherlast330`: 26.420 Punkte, Speichern 0,57 s, Laden 0,62 s;
  - `test_notizbereich330`: Einklappen in drei Bäumen, Notizbereich,
    Ordner, kleine Fenster.
- **Gefunden und behoben:**
  - Der Belastungstest fand Verweise auf endgültig entfernte Punkte.
  - Ein Prüflauf über 306 Ansichtswechsel fand 52 Befunde zur Startseite.
  - Der Neuaufbau der Seitenleiste klappte zugeklappte Ordner wieder auf.
  - Bei 860 × 700 blieb vom Notiztext nur ein Strich.
  - Tk 9 blendete nach dem Auspacken des Kartenfußes den Rahmen einer
    ausgeblendeten Karte wieder ein (`test_ui_updates`; nachgestellt mit
    reinem Tk).
  - `test_reminders` und `test_release37` erwarteten die Umstellung erst beim
    ersten Speichern. Seit der Startprüfung stellt schon das Laden um; beide
    sind angepasst.
- **Sichtprüfung eigener Aufnahmen** (nur das Glide-Fenster, künstliche
  Daten, 1300 × 900 und 860 × 700):
  - Seitenleiste mit Seiten, Listen und Notizen;
  - Notizübersicht;
  - Notiz bei Mindestgröße, vorher und nachher.
- **Schnelllauf während der Arbeit** (Protokoll nur im Arbeitsordner):
  Exitcode 1 mit vier Befunden. Drei davon waren schon behoben, als der
  Lauf endete: Dokumentindex, `test_ui_updates` und `test_reminders`. Den
  vierten, `test_release37`, hat die Anpassung oben erledigt.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/logo_notizen_2026-09-29/ergebnis.json),
  14:02 Uhr): **Exitcode 0**, 66 automatisierte Schritte:
  - Syntax (140 Quelldateien), Dokumentationsindex mit 1122 Links;
  - 51 Suiten und fünf Analysen;
  - Beispiel- und Releasedaten neu erzeugt und verglichen.

  Bilder und Sichtprüfung sind plattformbedingt übersprungen.
- **Danach:**
  - `build/macos/Glide.app` neu gebaut, mit dem Glide-Symbol;
  - `07_Python-Versionen` per SHA-256 bytegleich (158 Dateien), die
    startbare Kopie startet.
- **Offen:** die verdichtete
  [Prüfliste 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md),
  besonders A1 bis A4 und A16 am Mac sowie die Windows-Vollprüfung (B1).

### Tk 9, Bilder in Seiten und feste Bestandteile vom 27.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.14, nach der
[Entscheidungsvorlage vom 27.09.2026](../../../00_Arbeitsvorbereitung/Glide_Bestandspruefung_und_Entscheidungen_2026-09-27.md).

- **Neue Suiten:** `test_bilder330` (Seitenbilder, Vorschauen, Galerie,
  tkdnd, Systemmitteilung, „/“-Befehle, wiederkehrende Checkliste, Tempo,
  Rundgang) und `test_festlayout330` (neun Ansichten, zwei Größen, mit und
  ohne Auswahl).
- **Gemessen:** Speichern bei 2.128 Punkten 535 → 164 ms; JSON in einem Stück
  mit denselben Bytes (Test). Vorschau eines JPEG über `nsimage` 20 ms,
  HEIC beim ersten Mal 145 ms.
- **Sichtprüfung eigener Aufnahmen** (nur das Glide-Fenster, künstliche
  Daten): Seitenbilder links, rechts und mittig mit Umfluss; Werkzeugleiste
  von Seite, Zeichnung und Galerie; Pinnwand mit Fußhinweis; Suche mit
  runden Ecken und Schatten in Hell und Dunkel; Rundgang.
  - Dabei gefunden und behoben: Bildflächen saßen um den Innenabstand
    versetzt (`place` unter Tk 9); die Suche schnitt die Kopfknöpfe an; die
    Überschrift „Seiten“ blieb nach dem Designwechsel dunkel; der
    Pinnwand-Fußhinweis blieb leer.
- **Erster Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/tk9_bilder_erster_lauf_2026-09-27/ergebnis.json)):
  Exitcode 1. `test_features312`/`315` – die Kennzahlen in „Mein Tag“ waren
  auf zwei Zeilen gekürzt (jetzt drei, voller Text im Tooltip);
  `test_workspace310` – beim Markieren ausgepackter Hinweis ging nach der
  Pinnwand verloren (echter Fehler, jetzt wird er geleert statt ausgepackt).
- **Zweiter Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/tk9_bilder_zweiter_lauf_2026-09-27/ergebnis.json)):
  Exitcode 1, nur `test_features330` – die Grenze der Pinnwand-Hintergrund-
  punkte zählte die Randreihen nicht mit (Altbefund, im Einzellauf grün).
  Jetzt zählt sie exakt.
- **Dritter Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/tk9_bilder_2026-09-27/ergebnis.json), 20:16 Uhr):
  **Exitcode 0** – 62 automatisierte Schritte ausgeführt:
  - Syntax (132 Quelldateien), Dokumentationsindex mit 1101 Links;
  - 47 Suiten;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:** alles in der Prüfliste 3.30, Abschnitt „Tk 9, Bilder in Seiten
  und feste Bestandteile“, besonders Maus und Trackpad beim Verschieben und
  Größenziehen, Systemmitteilungen am Gerät, Windows (Vorschau, Ziehen,
  Infobereich) und Linux.

### Kompression, Bibliothekstabelle und Notizbuch vom 27.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.13.

- **Titelgrenze mit einer Kopie im Testordner geprüft:** Ein 69 Zeichen langer
  Titel wird beim Laden auf 40 Zeichen gekürzt. Vorher entsteht die Sicherung
  `liste_vor_titelkuerzung_*.json` mit dem Originaltitel; danach folgen
  Speichern und Meldung.
- **Raster gemessen:** Notiz, Seite, Zeichnung und Galerie stehen links 24,
  rechts 14 und unten 24 Pixel vom Kartenrand, wie die Aufgabenliste. Vorher
  lagen Werkzeugleiste und Text der Notiz links und rechts 10 Pixel vom Rand.
- **Hinweise:** Nach mehrfachem Neusetzen erscheint beim Überfahren genau ein
  Hinweis; ein Klick schließt ihn. Die Ursache der gestapelten Schatten und
  des „diagonal fliegenden“ Fensters lag in `add_tooltip`.
- **Sichtprüfung eigener Aufnahmen** (nur das Glide-Fenster): Kopf mit kurzer
  Beschreibung, Klapppfeile, Bibliothekstabelle, Notizseite.
  - Dabei gefunden und behoben: der doppelte, versetzte Leertext über der
    Notiz sowie Umschalter und „Anzeige“ in der Bibliothek.
- **Paralleler Suitenlauf:** Er fand, dass die nachgeführte
  Leertext-Beschriftung in „Mein Tag“ wieder erschien
  (`test_kontrast330`). Behoben: Sie folgt nur, solange sie gezeigt wird.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/kompression_2026-09-27/ergebnis.json), 12:21 Uhr): **Exitcode 0** im ersten Lauf –
  alle 60 automatisierten Schritte bestanden:
  - Syntax (125 Quelldateien), Dokumentationsindex mit 1076 Links;
  - 45 Suiten;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:** Sichtprüfung durch den Nutzer (Prüfliste, Abschnitt
  „Kompression“), insbesondere die Titelkürzung beim ersten Start mit dem
  echten Bestand.

### Aufräumen, Seitenbereich und Galerie vom 27.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.12.

- **Rundgang:** Alle Hauptansichten wurden mit Beispieldaten aufgenommen und
  auf Doppelungen und Formen ohne Funktion durchgesehen; der Nutzer wählte
  aus der Liste aus.
  - Aufgenommen wird seitdem nur das Glide-Fenster (`screencapture -l`).
  - Der erste Versuch erfasste den ganzen Bildschirm und wurde gelöscht.
- **Kästen hinter Text:** Die Suche über 18 Ansichten und Zustände (Dunkel und
  Hell mit Verlauf) findet nach der Korrektur keine Beschriftung mehr, die als
  Kasten auf dem Verlauf steht. Vorher fand sie die drei in „Startseite
  anpassen“.
- **Neue Suite `test_aufraeumen330`:** Kopfzeile, Seitenleiste, Auswahlleiste,
  Umschalter, Seite nach Zeichnung, Textlogo, Gismo, Fahne, Pinnwandzeile,
  Spaltenbreite, Seitenbereich, Seitenvorlagen, `.glidepage` hin und zurück,
  Aufgabenmarken nach Vorlage, Duplikat und Import, Galerie.
- **Gefundene Folgen:** Tests für die neue Leiste, die Systemzeilen, den
  Umschalter und die Listenarten angepasst. Das Symbol „edit“ war indirekt in
  Gebrauch (Vorlagenseite); die Schnellerfassung trägt deshalb ↯ statt ✎.
- **Probeläufe:**
  - Galerie mit PNG und JPEG: Vorschau über `sips`, Titel und Notiz,
    Entfernen mit Rückgängig, Speichern.
  - `.glidepage` einer Bibliothek exportiert und importiert, Aufgaben
    verbunden; eine Datei mit Listen wird abgewiesen.
- **Erster Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/aufraeumen_erster_lauf_2026-09-27/ergebnis.json)):
  Exitcode 1. `test_glide` fand beim Ziehen in der Ordneransicht die
  erwartete Zeile nicht. Vier Einzelläufe danach blieben grün; die Ursache
  ist nicht festgestellt.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/aufraeumen_2026-09-27/ergebnis.json), 10:56 Uhr): **Exitcode 0** – alle 59
  automatisierten Schritte bestanden:
  - Syntax (123 Quelldateien), Dokumentationsindex mit 1058 Links;
  - 44 Suiten;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:**
  - Sichtprüfung durch den Nutzer (Prüfliste 3.30, neuer Abschnitt);
  - JPEG-Vorschau der Galerie unter Windows (dort ohne Vorschau);
  - der einmalige Befund in `test_glide` bei weiteren Läufen beobachten.

### Seiten und Ordnertypen vom 26./27.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.11.

- **Neue Suite `test_seiten330`:**
  - Markdown-Rundlauf mit allen Blockarten und Inline-Formaten;
  - Seite aus Markdown: Aufgaben werden echte Punkte, auffindbar und in
    „Mein Tag“ einplanbar;
  - Editor: Abhaken, Titel verlängern, Enter setzt Aufgaben fort, leere
    Aufgabe beendet die Liste, gelöschte Aufgabe in den Papierkorb und per
    Rückgängig zurück, Kürzel „## “, eingefügtes Markdown;
  - Export, Seitenübersicht (Favoriten und Zuletzt nur mit Seiten),
    Bereinigung der Einstellungen, Ordnertypen, Speichern und Laden.
- **Erster Vollmodus:** Er scheiterte an `test_mindestgroesse330`. Am Sonntag
  ist das Datum im Titel am längsten; die Kopfzeile zog den Innenabstand der
  Beschriftung nicht ab, der Titel blieb mit 485 px unter den geforderten
  490 px. Behoben in `update_header_title`.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/seiten_2026-09-27/ergebnis.json), 00:41 Uhr): **Exitcode 0** – alle 58
  automatisierten Schritte bestanden:
  - Syntax (121 Quelldateien), Dokumentationsindex mit 1043 Links;
  - 43 Suiten;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:** Sichtprüfung der Seite durch den Nutzer (Lesegefühl, Kürzel,
  „/“-Menü); Windows.

### Zweite Rückmeldung vom 26.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.10.

- **Punktdialog:** Mit Verlauf hing der Dialog in `update_idletasks` (100 %
  Rechenlast, gemessen mit Stapelauszug). Nach der Korrektur öffnet er ohne
  Verzögerung, in voller Größe, 19 von 23 Bedienelementen sofort sichtbar.
  Der Rest liegt im Bildlaufbereich.
- **Kästen auf dem Verlauf:** Die Suche über zwölf Ansichten nach
  Beschriftungen mit eigener Farbe direkt auf dem Verlauf fand nach der
  Korrektur nichts mehr.
- **Tempo:** Messwerte in Vertrag 66, Abschnitt 2.10. Die Messung lief mit
  Profiler, die Zahlen stammen vom Entwicklungs-Mac.
- **Sichtprüfung** (Dunkel/Glut, Hell/Pastell, Pixel/Plasma, Glas hell/Iris):
  - keine Lücken oder Kanten im Verlauf, Pixelblöcke nahtlos;
  - Farbregel eingehalten;
  - dabei gefunden und behoben: eine 1-Pixel-Linie an Kartenkanten, ein
    schmaler Streifen neben dem Datum, ungetönte Reste in der Seitenleiste
    und ein grüner Startseiten-Chip.
- **Gefundene Folgen:** Testanpassungen für die neue Farbregel, die
  Verlaufsstücke, die Kennzahlen als Text und die neue Aktion in der
  Aktionssuche.
- **Erster Vollmodus:** Er scheiterte an `test_features329`. Der Handler für
  horizontales Scrollen wurde von Tk ohne Ereignis aufgerufen; einzeln lief
  die Suite grün. Der Handler ist jetzt dagegen gefeit.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/rueckmeldung2_2026-09-26/ergebnis.json), 22:54 Uhr): **Exitcode 0** – alle 57
  automatisierten Schritte bestanden:
  - Syntax (118 Quelldateien), Dokumentationsindex mit 1028 Links;
  - 42 Suiten;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:** Windows; die neuen Punkte der Prüfliste; ob beim Scrollen noch
  Knöpfe verschwinden (nicht nachgestellt).

### Rückmeldung vom 26.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitte 2.8 und 2.9.

- **Absturz im hellen Glasdesign:**
  - Nachgestellt mit Kopien der Einstellungs- und Fensterdatei des Nutzers
    (mit Zustimmung). Die Prüfsummen der Originale sind unverändert.
  - Bedingung: Verlauf, Startseite, 860 Pixel Breite. Ursache: Bindtags der
    Hintergrundbilder.
  - Nach der Korrektur fünf Starts ohne Absturz.
  - `test_hintergrund330` startet den Fall jetzt als eigenen Prozess. Mit dem
    alten Bindtag endet er mit Signal −10, der Test erkennt das.
- **Abstände:** Gemessen wurden die Unterkanten in zehn Ansichten. Vorher
  lagen Pinnwand, Zeichenfläche und Verlauf 14 Pixel zu tief, die
  Startseite 4 Pixel zu hoch. Jetzt enden alle auf einer Linie.
- **Zeichenfläche:** Gemessen wurde die Flächenhöhe bei Raster, Vorschau,
  Werkzeugwechsel und Meldungen. Vorher schwankte sie um 14 bis 26 Pixel,
  jetzt bleibt sie konstant.
- **Milchglas und Hinweistexte:** Sichtprüfung auf dem Entwicklungs-Mac in
  „Glas hell/Iris“ und „Dunkel/Glut“. Es gibt keine Kästen mehr hinter
  Texten.
- **Gefundene Folgen der Änderungen:**
  - Sechs Suiten erwarteten noch die alten Seitenleistenzeilen oder den
    Klapppfeil. Sie sind angepasst.
  - `test_features315` fand, dass ein leerer Tag seinen Hinweis verlor, weil
    „In Bearbeitung“ die Ansicht füllte. Der Hinweis steht jetzt als eigene
    Zeile über den Abschnitten.
  - Der erste Vollmodus scheiterte nur an der Attributprüfung
    (`self.__dict__.setdefault`). Nach der Korrektur wurde er wiederholt.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/rueckmeldung_2026-09-26/ergebnis.json), 20:41 Uhr): **Exitcode 0** – alle 57
  automatisierten Schritte bestanden:
  - Syntax (116 Quelldateien) und Dokumentationsindex mit 1011 Links;
  - 42 Suiten, darunter die neue `test_rueckmeldung330`;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
- **Offen:** Windows-Darstellung und die neuen Punkte der Prüfliste.

### Hintergrundverläufe vom 26.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitt 2.8.

- **Neue Suite `test_hintergrund330`:** Sie prüft ohne Bildschirmaufnahme:
  - alle 50 Entwürfe und die Lesezone (4,5:1 samt Körnung);
  - den Einbau in drei Designs, die Glas-Tönung und das Menü;
  - den Zwischenspeicher im Testordner, das Abschalten und die Auswahl in
    den Einstellungen.
- **Sichtprüfung auf dem Entwicklungs-Mac:** Aufnahmen von Glas dunkel, Hell
  und Pixel. Befunde und Korrekturen:
  - Das Pixel-Dithering war zu unruhig → ruhigere Paletten, Schwelle 0,35.
  - Sterne unter dem Titel → in der Lesezone unterdrückt.
  - Eine Buchstabenkontur wirkte fett → Milchglas-Pille.
  - Der Fensterrand blieb einfarbig → das Hauptfenster bekommt einen eigenen
    Ausschnitt.
- **Erster Vollmodus:** Exitcode 1, nur in `test_glide`: Die Kopfspalte war
  39 statt 42 Pixel hoch.
  - Ursache: Das neue `CanvasLabel` maß knapper als ein Tk-Label.
  - Es misst jetzt pixelgleich (Rand und Zeilenhöhe wie ein Label, geprüft
    mit und ohne Umbruch und Innenabstand).
  - Danach waren die Hauptsuite und die sieben betroffenen Suiten grün.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/hintergrund_2026-09-26/ergebnis.json), 18:30 Uhr): **Exitcode 0** – alle 56
  automatisierten Schritte bestanden:
  - Syntax (114 Quelldateien) und Dokumentationsindex mit 996 Links;
  - 41 Suiten, darunter `test_hintergrund330`;
  - Analysen sowie Beispiel- und Releasedaten-Abgleich.
  - Bilder und Sichtprüfung sind plattformbedingt übersprungen.
- **Offen:** die Darstellung unter Windows, siehe die Prüfliste.

### Dialoge, Kontrast, Raster, Paketierung vom 26.09.2026

Umfang: [Vertrag 66](66_MODERNISIERUNG_3.30.0.md), Abschnitte 2.4 bis 2.7.

- **Dialoge:** 24 Dialoge der Menüleiste wurden bei ihrer Mindestgröße in
  mittlerer und großer Schrift gemessen.
  - Befunde: Anschnitte im Kalender, ein gequetschter Kalenderknopf,
    überstehende Aufklapppfeile und „Über Glide“ bei großer Schrift.
  - Der Messlauf fand außerdem einen Absturz von „In Liste verschieben“
    (`KeyError`).
  - Alles ist behoben; `test_mindestgroesse330` misst seitdem 43
    Dialogaufrufe mit.
- **Kontrast:** Die erste Messung fand im hellen Design 38 und im Glas-hell
  40 Farbpaare unter WCAG AA, in allen dunklen und bunten Designs die
  Hover-Schrift.
  - Die Grundpalette von Hell und Dunkel wurde korrigiert.
  - Dazu kommen Sicherheitsnetze für gemischte Designs und Knöpfe.
  - Die neue Suite `test_kontrast330` misst rund 13.700 Paare.
  - Eine Zwischenmessung meldete fälschlich 0, weil ein abgefangener Fehler
    die Knopfprüfung übersprang. Das ist behoben.
- **Stundenraster:** `test_features330` prüft zusätzlich das Raster statt
  der Liste im schmalen Fenster und das Einplanen über die Seitenleiste.
- **Paketierung:** Das Entwicklungsbundle wurde gebaut und mit getrenntem
  Datenordner gestartet.
  - macOS führt den Prozess als „Glide“ (`de.shaye.glide`, arm64); die Daten
    lagen nur im temporären Ordner.
  - Die neue Suite `test_paketierung330` baut das Bundle und prüft dessen
    Signatur.
  - Das Windows-Skript ist ungeprüft.
- **Abgebrochener Lauf:** Der erste Vollmodus scheiterte an `test_release36`
  und `test_ui_polish36`.
  - Die Nachkorrektur veränderte die Farben von Hell und Dunkel; die Suiten
    erwarten zu Recht, dass die Palette selbst gilt.
  - Die kontrastfesten Werte stehen jetzt in `PALETTE`. Der Lauf wurde
    abgebrochen und wiederholt.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/kontrast_paketierung_2026-09-26/ergebnis.json),
  15:28–15:46 Uhr): **Exitcode 0** – alle 55 automatisierten Schritte
  bestanden:
  - Syntax (111 Quelldateien), Versionskonsistenz, Dokumentationsindex mit
    973 Links;
  - 40 Suiten, darunter `test_mindestgroesse330`, `test_kontrast330` und
    `test_paketierung330`;
  - fünf Analysen;
  - Erzeugung und Abgleich von Beispieldaten und Releaseplanung.

  Die 48 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
  **Maßgeblicher automatisierter Nachweis des Endstands 3.30.0.**
- **Startbare Kopie:** `07_Python-Versionen` ist bytegleich und startet
  fehlerfrei. Der Stand davor liegt unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Kontrast_und_Paketierung_2026-09-26/`.

### Kleine Fenster vom 26.09.2026

Umfang ([Vertrag 66, Abschnitt 2.5](66_MODERNISIERUNG_3.30.0.md)):

- Höhenstufen;
- ganze Chips und gekürzte Unterzeilen;
- umbrechende Kennzahlen;
- ungequetschte Knöpfe;
- Tabellenspalten nach Priorität;
- Überschriften auch in der sortierten gruppierten Tabelle.

- **Sichtprüfung mit Aufnahmen** bei 860 × 700 (Beispieldaten, temporärer
  Datenordner):
  - vorher: unten abgeschnittene Aktionsreihen, „ınwa“ statt „Pinnwand“,
    eine Titelspalte von 60 px, ein Listenbaum mit zwei Zeilen;
  - nachher: sauber, die Aktionsreihe schließt bündig mit der Seitenleiste
    ab.

  Zwischendurch war der Bildschirm gesperrt; daraus entstand die
  Messprüfung.
- **Neue Suite `test_mindestgroesse330.py`:** 75 Ansichten in fünf
  Kombinationen aus Design, Schriftgröße und Fenstergröße ohne Befund.
  - Am vorherigen Stand fand dieselbe Messung 24 Befunde.
  - Während der Arbeit fand sie drei weitere Fehler: den Titel nach einem
    Schriftwechsel, den Titel nach einem Größenwechsel und „Raster“ bei
    großer Schrift.
- **Abgebrochener Lauf:** Der erste Vollmodus scheiterte an
  `test_features312` und `test_features315`. Die Kennzahlen rechts oben
  verloren beim Kürzen Abschnitte, die diese Suiten zu Recht erwarten. Jetzt
  brechen die Kennzahlen um und bleiben vollständig; der Lauf wurde
  abgebrochen und wiederholt.
- **Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/mindestgroesse_2026-09-26/ergebnis.json),
  13:18–13:31 Uhr): **Exitcode 0** – alle 53 automatisierten Schritte
  bestanden:
  - Syntax (108 Quelldateien), Versionskonsistenz, Dokumentationsindex mit
    957 Links;
  - 38 Suiten einschließlich `test_mindestgroesse330`;
  - fünf Analysen;
  - Erzeugung und Abgleich von Beispieldaten und Releaseplanung.

  Die 46 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
  Maßgeblicher Nachweis bis zur Runde mit Kontrast und Paketierung.
- **Startbare Kopie:** `07_Python-Versionen` ist per SHA-256 bytegleich und
  startet ohne Callback-Fehler. Der Stand davor liegt unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Mindestgroesse_2026-09-26/`.

### Dritter Ausbau vom 26.09.2026

Umfang, ohne neues Datenformat und ohne neue Einstellung:

- Punkte aus der Liste von „Mein Tag“ ins Stundenraster ziehen;
- die gruppierte Tabelle mit Nummern und Zwischenüberschriften;
- die Pixelschrift unter Linux über Fontconfig;
- mitbehoben: „Pinnwand öffnen“ aus der Tabelle.

- **Während der Umsetzung:** `test_features330.py` prüft zusätzlich:
  - Ziehen eines Punkts ohne Uhrzeit ins Raster über Bildschirmkoordinaten,
    mit Vorschaulinie und Rückgängig;
  - Nummern und Überschriften der gruppierten Tabelle, ohne Überschriften
    bei Spaltensortierung;
  - „Pinnwand öffnen“ aus der Tabelle;
  - die Linux-Registrierung mit nachgebildetem Fontconfig, samt Rückfall
    ohne Bibliothek.

  Der Menüfehler fiel auf, weil der neue Test die Tabelle zunächst über den
  Arbeitsbereich statt über `open_list_view` verließ.
- **Abgebrochener erster Lauf:** Die Archivkopien entstanden erst nach dem
  Start der Vollprüfung. Ihr Dokumentationsschritt meldete die noch nicht
  indizierten Kopien. Der Lauf wurde abgebrochen, sein Teilprotokoll
  verworfen und nach dem Dokumentabgleich neu gestartet.
- **Vollmodus ohne parallele Last**
  ([Protokoll](../tests/qa-3.30.0/ausbau3_2026-09-26/ergebnis.json),
  11:10–11:22 Uhr): **Exitcode 0** – alle 52 automatisierten Schritte
  bestanden:
  - Syntax (106 Quelldateien), Versionskonsistenz, Dokumentationsindex mit
    945 Links, Fixtures, Tk, Zeitzone;
  - 37 Suiten;
  - fünf Analysen;
  - Erzeugung und Abgleich von Beispieldaten und Releaseplanung.

  Die 45 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
  Maßgeblicher Nachweis bis zur Überarbeitung für kleine Fenster.
- **Startbare Kopie:** `07_Python-Versionen` ist per SHA-256 bytegleich zum
  Quellstand und startet ohne Callback-Fehler, mit 20 Vorlagen und
  Pixelify Sans. Den Stand vor dem dritten Ausbau sichert
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau3_2026-09-26/`; er
  startet ebenfalls fehlerfrei.
- **Linux:** Die Schriftregistrierung ist nicht auf einem echten
  Linux-Desktop geprüft. Das bleibt eine manuelle Prüfung.

### Zweiter Ausbau vom 26.09.2026

Umfang:

- Anhänge im Detailbereich;
- Zeichnungen als PNG in Druckseite und Folien;
- Stundenraster in „Mein Tag“;
- Gruppierung mit Überschriften und erhaltener Nummerierung;
- Windows-Prüfpaket;
- Entwurf des Produktdatenblatts.

Kein neues Datenformat; neu ist nur der Einstellungsschlüssel
`plan_day_grid`.

- **Während der Umsetzung:** `test_features330.py` wurde um vier Prüfungen
  erweitert (Anhänge mit Rückgängig, PNG in der Druckseite, Überschriften in
  gruppierten Listen, Stundenraster mit Ziehen und Rückgängig).
  - Gefunden und behoben: Doppelte Anhänge verglichen Quellpfade mit
    abgelegten Kopien; jetzt zählen Name und Größe.
  - Die neue Menüaktion fehlte in der Gruppenzuordnung der App-Aktionen.
- **Lasttest `test_ui_followup36`:** Vier gleichzeitige Läufe.
  - Erste Runde: 3 von 4 grün, keiner mit Datenunterschied. Die frühere
    Beobachtung zum Datenvergleich (siehe Nachprüfung unten) ließ sich damit
    nicht wiederholen.
  - Der eine Fehlschlag betraf die Knopfsichtbarkeit: Unter Last lag die
    Karte nach einmaligem Scrollen teils außerhalb des Sichtbereichs, und Tk
    blendet eingebettete Widgets dort aus.
  - Der Test scrollt jetzt vor jeder Messung neu. Die zweite Runde mit vier
    gleichzeitigen Läufen war **4 von 4 grün**. Die alte Fassung liegt in
    `tests/integration/archiv`.
- **Vollmodus ohne parallele Last**
  ([Protokoll](../tests/qa-3.30.0/ausbau2_2026-09-26/ergebnis.json),
  09:59–10:11 Uhr): **Exitcode 0** – alle 52 automatisierten Schritte
  bestanden:
  - Syntax (106 Quelldateien), Versionskonsistenz, Dokumentationsindex mit
    934 Links, Fixtures, Tk, Zeitzone;
  - 37 Suiten;
  - fünf Analysen;
  - Erzeugung und Abgleich von Beispieldaten und Releaseplanung.

  Die 45 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
  Übersprungen sind wie bisher die Bildaufnahmen und die Sichtprüfung.
  Maßgeblicher Nachweis bis zum dritten Ausbau.
- **Startbare Kopie:** `07_Python-Versionen` ist per SHA-256 bytegleich zum
  Quellstand. Der aktuelle Stand startete mit isoliertem Datenordner ohne
  Callback-Fehler: 20 Vorlagen, Pixelify Sans im Pixel-Titel. Den Stand vor
  dem zweiten Ausbau sichert
  `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau2_2026-09-26/`. Auch er
  startet fehlerfrei; ohne `resources` nutzt er die Systemschrift und die
  eingebauten Ersatzvorlagen.
- **Windows:** Das Prüfpaket ist erstellt, aber noch nicht auf einem
  Windows-Rechner gelaufen. Das bleibt Teil der Plattformabnahme.

### Ausbau vom 25./26.09.2026

Umfang:

- Zeitblöcke ziehen;
- Folien als PDF;
- Karten-Rückgängig;
- vollständiger Detailbereich;
- Gismo in Leerzuständen;
- Pixelschrift.

Dazu kommen die beim Ausbau gefundenen Schutzmaßnahmen für unlesbare und
neuere Speicherdateien sowie der Fix für doppeltes Beenden
([Vertrag, Abschnitt 9](66_MODERNISIERUNG_3.30.0.md#9-mitbehobene-befunde)).

- **Erster Vollmodus nach dem Ausbau**
  ([Protokoll](../tests/qa-3.30.0/ausbau_2026-09-25/ergebnis.json), bis
  00:01 Uhr): Exitcode 1, 49 von 52 Schritten bestanden.
  - `test_release37` und `test_reminders` legten wie ein Altbestand eine
    ältere Datei in einen Ordner, in dem schon Format 20 geschrieben war. Die
    neue Rückfallwarnung meldete sich zu Recht.
  - Korrektur in der App: Die Markierung `data_format_written` entsteht erst
    mit echtem Inhalt, und der Text nennt auch das Hineinkopieren einer
    älteren Datei. Beide Suiten liefen danach einzeln grün, ohne
    Teständerung.
  - Der **Release-Abgleich** scheiterte, weil der Lauf über Mitternacht ging:
    Er verglich das Momentdatum der Listen absolut, obwohl es ein Anlagetag
    ist. `pruefen.py` vergleicht es jetzt relativ zum Exporttag. Das war ein
    Fehler des Prüfwerkzeugs, der an jedem Tag nach der Erzeugung
    aufgetreten wäre.
- **Nachprüfung**
  ([Protokoll](../tests/qa-3.30.0/ausbau_nachpruefung_2026-09-26/ergebnis.json),
  00:02–00:18 Uhr): Exitcode 1, 51 von 52 Schritten bestanden. Übrig blieb
  `test_ui_followup36`: Eine frisch gescrollte Übersichtskarte meldete
  „Liste öffnen“ noch nicht als eingeblendet.
  - Zwei Einzelwiederholungen und zwei weitere Läufe einer Kopie mit
    Unterschiedsausgabe; drei davon ohne parallele Last – alle drei grün, die
    Kopien ohne jeden Datenunterschied.
  - Eine Wiederholung lief parallel zur Nachprüfung, also unter doppelter
    Last. Sie scheiterte stattdessen am Datenvergleich nach Speichern und
    Laden (Zeile 352). Nachstellen ließ sich das nicht; es bleibt als offene
    Beobachtung notiert.
  - Die Sichtbarkeitsprüfung wartet jetzt im selben Durchlauf auf den stabilen
    Endzustand wie seit 3.29 die Abstandsmessung (bis zu sechs Durchläufe).
    Die Anforderung selbst ist unverändert.
- **Abschlusslauf**
  ([Protokoll](../tests/qa-3.30.0/ausbau_abschluss_2026-09-26/ergebnis.json),
  00:28–00:46 Uhr): **Exitcode 0** – alle 52 automatisierten Schritte
  bestanden:
  - Syntax (107 Quelldateien), Versionskonsistenz, Dokumentationsindex mit
    916 Links, Fixtures, Tk, Zeitzone;
  - 37 Suiten einschließlich der erweiterten `test_features330.py`;
  - fünf Analysen;
  - Erzeugung und Abgleich von Beispieldaten und Releaseplanung.

  Die 45 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
  Maßgeblicher Nachweis bis zum zweiten Ausbau.
- **Echtdatenprobe** (mit Zustimmung, nur mit einer Kopie in einem
  temporären Ordner):
  - Umstellung von 6 Seiten und 138 Punkten ohne Inhaltsänderung;
  - Vorsicherung bytegleich, keine Meldung, kein Tk-Fehler;
  - Original vorher und nachher per SHA-256 gleich.

  Die Probe fand, dass Glide 3.29 den umgestellten Bestand bei der ersten
  Eingabe überschreibt. Daraus entstanden die Schutzmaßnahmen und die Warnung
  in allen Übergabedokumenten.
- **Startbare Kopie:** `07_Python-Versionen` ist nach dem Ausbau erneut per
  SHA-256 bytegleich zum Quellstand, einschließlich der neuen Schriftdateien.
  - Beide Fassungen starteten mit isoliertem Datenordner ohne Fehler: der
    aktuelle Stand mit Pixelify Sans im Pixel-Titel und der Stand vor dem
    Ausbau unter `Archiv/Glide-Aufgaben-und-Listen_v3.30.0_vor_Ausbau_2026-09-25/`.

### Erster Abschluss am 25.09.2026 (vor dem Ausbau)

- **Während der Umsetzung:** Nach jedem Paket liefen die neuen Suiten
  `test_drawing330.py` und `test_features330.py`, dazu die betroffenen älteren
  Suiten einzeln. Dabei gefundene Fehler sind behoben. Die schon in 3.29
  vorhandenen stehen im
  [Vertrag, Abschnitt 9](66_MODERNISIERUNG_3.30.0.md#9-mitbehobene-befunde).
- **Abschlusslauf im Vollmodus**
  ([Protokoll](../tests/qa-3.30.0/abschluss_2026-09-25/ergebnis.json)):
  **Exitcode 0** – alle 52 automatisierten Schritte bestanden:
  - Vorprüfungen: Syntax (107 Quelldateien), Versionskonsistenz (3.30.0,
    Format 20), Dokumentationsindex mit 898 Links, Fixtures (30 Backups und
    alle historischen Referenzformate), Tk, Zeitzone (CEST, +02:00);
  - alle 37 Suiten einschließlich `audit_app` und der neuen Suiten
    `test_drawing330.py` und `test_features330.py`.
    `test_vollpruefung325.py` durchläuft jetzt zehn Designs einschließlich
    „Pixel“ in drei Breiten und zwölf Ansichten;
  - die fünf Analysen (statisch, Erreichbarkeit, Standprüfung, Attribute,
    Dubletten);
  - Erzeugung und Abgleich der Beispieldaten und der Releaseplanung
    (Planungsstichtag 25.09.2026).

  Der Lauf dauerte rund 13 Minuten bei einer Grenze von 900 Sekunden je
  Suite. Die 45 Protokolle enthalten keinen Traceback und keinen Tk-Fehler.
- **Startbare Kopie:** `07_Python-Versionen` enthält
  `Glide-Aufgaben-und-Listen_v3.30.0.pyw`, beide Module und den
  Vorlagenkatalog. Alle Dateien sind per SHA-256 bytegleich zum Quellstand;
  ebenso die Nutzerkopie der Praxisvorlagen in `05_Probelisten_Testdaten`.
  3.29.0 liegt startfähig samt Modulen unter
  `Archiv/Glide-Aufgaben-und-Listen_v3.29.0/`.

Übersprungen bleiben plattformgebunden die Bildaufnahmen (nur Linux/X11 bzw.
Windows) und die Sichtprüfung. Bildschirmaufnahmen waren in der
Agentenumgebung nicht möglich. Die Darstellung wurde über Widgetgeometrie und
Zustandsprüfungen getestet, nicht mit dem Auge.

### Offen und nur manuell prüfbar

Die [Prüfliste 3.30](../../../00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md)
führt die Punkte einzeln auf. Zusammengefasst:

- Migration eines echten Bestands: mit einer Kopie automatisch geprüft;
  offen bleibt nur die Sichtkontrolle. **3.29 nach der Umstellung nicht mehr
  starten** – es überschreibt den Bestand;
- die Neuerungen des Ausbaus mit echter Bedienung: Zeitblöcke ziehen,
  Folien-PDF im Browser, Detailbereich mit Trackpad, Pixelschrift unter
  macOS und Windows;
- Bedienung mit echter Maus, Trackpad und Tastatur, vor allem Zeichnen und
  Ziehen im Board;
- Bildschirmleser (NVDA, VoiceOver);
- DPI-Skalierung mit 100, 150 und 200 % sowie zwei Monitore;
- ein Gesamtlauf unter Windows (fehlt seit 3.29);
- Druck und PDF mit und ohne Pinnwandhintergrund;
- flüssige Bedienung mit 500 Karten.

**Nicht durch Agenten prüfbar:**

- Signatur, Notarisierung und Installer;
- Markenprüfung;
- Store-Freigabe.

Die Prüflisten [3.29](../../../00_Arbeitsvorbereitung/Checklisten/Archiv/Manuelle_Pruefung_3.29.0_vor_Verdichtung_2026-09-29.md)
und [3.28](../../../00_Arbeitsvorbereitung/Checklisten/Archiv/Manuelle_Pruefung_3.28.0_vor_Verdichtung_2026-09-29.md)
sind ebenfalls noch offen.

## Ergebnis 3.29.0 (historisch)

3.29.0 integriert die Zeichnungsseite (Aufgabenformat 19). Geprüft wurde auf
dem Entwicklungs-Mac mit Python 3.14.5 und isoliertem `GLIDE_DATA_DIR`.

- **Ausgangslauf vor Beginn** (Schnellmodus,
  [Protokoll](../tests/qa-3.28.0/vor_zeichnungsintegration_2026-09-24/ergebnis.json)):
  dieselben fünf bekannten Altbefunde wie seit 3.28 (Fixture 3.26.0,
  Vorlagenreproduktion, `test_features313`, `test_features322`,
  `test_features328`).
- **Erster Vollmodus nach der Integration**
  ([Protokoll](../tests/qa-3.29.0/zeichnungsseite_2026-09-24/ergebnis.json)):
  Syntax, Versionskonsistenz, Dokumentationsindex (842 Links), Fixtures, Tk,
  Zeitzone, **alle 35 Suiten** einschließlich der neuen `test_features329.py`
  und **alle fünf Analysen** bestanden. Die fünf Altbefunde sind behoben. Rot
  blieben nur die erstmals seit 3.26 wieder ausgeführten Reproduktionsabgleiche
  von Beispiel- und Releasedaten: Der Vergleich behandelte die seit 3.26
  vorhandenen Listenzeitpunkte `created_at`/`updated_at` noch als Inhalt.
  Korrektur in `pruefen.py`: Diese Erzeugungszeitpunkte sind wie `exported_at`
  ausgenommen; das Tagebuch-Momentdatum wird relativ zum Exporttag verglichen.
- **Nachprüfung im Vollmodus**
  ([Protokoll](../tests/qa-3.29.0/zeichnungsseite_nachpruefung_2026-09-24/ergebnis.json)):
  **Exitcode 0** – alle 50 automatisierten Schritte bestanden: Vorprüfungen,
  35 Suiten, fünf Analysen sowie Erzeugung und Abgleich von Beispiel- und
  Releasedaten. Das ist der erste vollständig grüne Gesamtlauf seit 3.26.0;
  er ersetzt keine manuelle Plattformabnahme.
- **Abnahmelauf nach Rückmeldung** (Farbspektrum, Scrollbereich, zusätzliche
  Abnahmetests; [Protokoll](../tests/qa-3.29.0/abnahme_2026-09-24/ergebnis.json)):
  49 Schritte bestanden, **ein Befund** in `test_ui_followup36`: Innenabstand
  einer Bestandskarte nach Schriftwechsel und Resize (rechts 109 statt 16 px).
  Drei Einzelwiederholungen waren grün; der Bereich wurde in 3.29 nicht
  geändert. Ursache ist eine Layoutmessung vor dem letzten Tk-Durchlauf unter
  Last. Die Prüfung misst jetzt bis zu sechsmal den stabilen Endzustand; die
  Abstandsanforderung selbst ist unverändert.
- **Abnahme-Nachprüfung**
  ([Protokoll](../tests/qa-3.29.0/abnahme_nachpruefung_2026-09-24/ergebnis.json)):
  **Exitcode 0** – alle 50 automatisierten Schritte bestanden (Vorprüfungen,
  35 Suiten, fünf Analysen, Reproduktion von Beispiel- und Releasedaten).
  Maßgeblicher automatisierter Nachweis des Endstands 3.29.0.

Die einzelnen Abnahmekriterien der Etappe mit Nachweis stehen im
[Vertrag 3.29, Abschnitt 11](65_ZEICHNUNGSSEITE_3.29.0.md).

Übersprungen bleiben plattformgebunden die Bildaufnahmen (nur Linux/X11 bzw.
Windows) und die Sichtprüfung. Bildschirmaufnahmen waren in der
Agentenumgebung nicht erlaubt; die Einbettung der Zeichenfläche wurde über
Widgetgeometrie geprüft (1280 × 860: Fläche 922 × 616 Pixel; 860 × 700:
502 × 420 Pixel). Offen und manuell: [Prüfliste 3.29](../../../00_Arbeitsvorbereitung/Checklisten/Archiv/Manuelle_Pruefung_3.29.0_vor_Verdichtung_2026-09-29.md)
mit Maus/Trackpad, Tastatur und Screenreader, DPI, Mehrmonitor, Windows,
Designs und dem Illustrator-/Affinity-Rundlauf. Ein Windows-Gesamtlauf für
3.29.0 fehlt.

## Ergebnis 3.28.0 (historisch)

Der Funktionsstand 3.28 ist gezielt geprüft, aber **noch nicht als vollständiger
Release-Gesamtlauf freigegeben**. Der
[Schnelllauf](../tests/qa-3.28.0/abschluss_2026-09-23/ergebnis.json) bestätigt
Versionskonsistenz, Tk, Zeitzone, den Haupttest und den überwiegenden Teil der
Integrationssuiten. Sein Gesamtergebnis bleibt Exitcode 1, weil mehrere ältere
OneDrive-Platzhalter lokal nicht lesbar sind und zwei lang laufende UI-/
Gesamtprüfungen die bewusst gesetzte Grenze von 60 Sekunden überschritten.

Nach diesem Lauf wurden die veralteten Erwartungen der Vorlagenprüfung an die
vier neuen Tagebuchvorlagen angepasst. Die Vorlagenerzeugung verwendet nun
stabile Erstellungszeitpunkte. Anschließend bestanden einzeln:

- Syntaxprüfung des Quellstands und der startbaren 3.28-Kopie;
- `test_glide.py` einschließlich Kern-, Backup-, UI-, Ordner-, Papierkorb- und
  Migrationstests;
- `test_features328.py` für Format 18, Tagebuchdaten, Sicherung, Vorlagen,
  Menügestaltung, Aktionsfarben und verdichtete Notizwerkzeuge;
- `test_template_workflows.py` für 16 vollständige Projekt-/Listenvorlagen plus
  vier Tagebuchvorlagen, Reproduzierbarkeit, Migration und Dialoge;
- `test_features315.py` mit der seit 3.27 gültigen Tabellenfilter-Logik;
- im Schnelllauf unter anderem `test_datenintegritaet`, `audit_app`,
  `test_dialog_theme`, `test_ui_updates`, `test_glide_36`, `test_release36`,
  `test_ui_polish36`, `test_release37`, `test_reminders`, `test_ui39`,
  `test_workspace310` sowie die lesbaren Suiten 3.12 und 3.14 bis 3.26;
- Erreichbarkeits-, Attribut- und Dublettenprüfung. Die statische Analyse lief
  anschließend mit Exitcode 0 durch; ihre Größen- und Duplikathinweise sind
  Wartungshinweise, keine fehlgeschlagenen Funktionsprüfungen.

Nach der Meldung eines weißen Neuaufbaus beim Füttern von Gismo wurde der
Pflegepfad zusätzlich korrigiert und erneut geprüft. Der 3.28-Test läuft dafür
im Dopamin-Design, löst `Füttern` aus und weist nach, dass die vorhandenen
Pflegebalken aktualisiert werden, bestehen bleiben und kein `refresh_home()`
mehr aufgerufen wird. Syntax, Hauptsuite, Vorlagenworkflow und
Tagesplanungstest bestanden danach erneut. Die tatsächliche Sichtprüfung mit
echter Maus bleibt in `Manuelle_Pruefung_3.28.0.md` offen.
Der maschinenlesbare Nachweis liegt unter
[`tests/qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json`](../tests/qa-3.28.0/nachpruefung_flackern_2026-09-23/ergebnis.json).

Quelle und startbare Version sowie deren jeweiliger Vorlagenkatalog wurden nach
der letzten Korrektur erneut kopiert und per SHA-256 auf Bytegleichheit geprüft.
Alle App- und Integrationstests arbeiten mit temporären `GLIDE_DATA_DIR`-
Verzeichnissen; die Nutzerdaten wurden nicht als Testbestand geöffnet.

### Damalige Prüfblockaden (seit 3.29 aufgelöst)

Seit dem Vollmodus 3.29.0 sind alle hier genannten Dateien lokal lesbar. Am
25.09.2026 wurde das erneut geprüft:

- Die vier Dateien im Repository hat der Abschlusslauf 3.30.0 gelesen.
- `38_DOKUMENTATIONSABGLEICH_2026-09-13.md` liegt inzwischen unter
  `docs/archiv/`.
- Die Prüfliste 3.21.4 liegt unter
  `00_Arbeitsvorbereitung/Archiv/Arbeitsstaende_bis_3.26/Checklisten/`.

Die Zeitüberschreitungen von `test_ui_followup36.py` und
`test_vollpruefung325.py` traten mit der Grenze von 900 Sekunden je Suite
nicht mehr auf.

Damaliger Wortlaut: Folgende Dateien trugen auf diesem Rechner den
OneDrive-Platzhalterstatus und lieferten
`PermissionError: [Errno 13] Permission denied`:

- `tests/integration/test_features311.py` und `test_features313.py`;
- `tests/fixtures/current_v15/reference_v15.json` innerhalb von
  `test_features322.py`;
- ältere Beispiel-Fixtures, zuerst
  `tests/fixtures/beispiele/glide_releaseplanung_3.10.0.glidebackup`;
- `docs/38_DOKUMENTATIONSABGLEICH_2026-09-13.md`;
- außerhalb des Repositorys
  `00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.21.4.md`, wodurch die
  Standprüfung vor der inhaltlichen Auswertung abbrach.

`test_ui_followup36.py` überschritt wie bereits im 3.27-Ausgangsstand die
60-Sekunden-Grenze in der Fenstergrößen-/Ereignisverarbeitung. Der ältere
Sammeltest `test_vollpruefung325.py` überschritt dieselbe Grenze.

### Damalige manuelle Grenzen

Eine neue menschliche Sichtprüfung von 3.28 wurde nicht durchgeführt. Die vom
Nutzer gelieferten Bildschirmbilder dienten als Problembeleg, ersetzen aber
keinen abschließenden Bedienungstest. Ebenfalls offen blieben macOS, native
Druckdialoge, DPI-/Mehrmonitor-Sonderfälle, Screenreader, Installer,
Signierung/Notarisierung und reale Verteilung.
