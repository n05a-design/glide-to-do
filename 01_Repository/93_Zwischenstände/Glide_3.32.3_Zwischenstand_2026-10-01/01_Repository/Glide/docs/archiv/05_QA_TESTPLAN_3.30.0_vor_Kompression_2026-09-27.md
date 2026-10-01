# Prüfplan – Glide 3.30.0

Stand 27.09.2026 · Glide 3.30.0 · Aufgabenformat 20 · alle App-Tests mit isoliertem `GLIDE_DATA_DIR`

Vollständiger Lauf: `python tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.30.0/abschluss`; er umfasst alle Suiten, Syntax-, Versions-, Dokument- und Fixtureprüfung, Zeitzonenmessung, fünf Analysen, reproduzierte Beispiel-/Releasedaten und Screenshots. Die Zahl der Schritte steht im Quelltext. `test_features328.py` ergänzt Tagebuch, Format 18, konturlose Menüs, neutrale Aktionen und die verdichtete Notizwerkzeugleiste. `test_features329.py` prüft die Zeichnungsseite: Format-19-Vorsicherung, Ablehnung unbekannter Listenarten, eingebettete Fläche ohne Extrafenster, Pinselvorschau je Zoom, gebündeltes Autosave und Schreibfehler, Referenz-PNG, Nachzeichnung mit Vorher-Snapshot, Rückgängig-Semantik, Duplizieren, Papierkorb, Voll- und additiver Import, Teilbackup, Austausch, Vorlagen, JSON-/SVG-Datei-Rundlauf und Tagebuchübersicht. Manuell bleiben Maus- und Trackpadbedienung, DPI, Mehrmonitor, Screenreader und der Illustrator-/Affinity-Rundlauf.

Seit 3.30.0 kommen zwei Suiten dazu.

- **`test_drawing330.py`** prüft den Zeichenkern:
  - Aktionspuffer, Formen, Symmetrie, Muster, Kachel;
  - Bereiche und Auswahl, Farbe ersetzen, Palette kompaktieren;
  - Paletten `.gpl`/`.hex`, PNG-Kodierung und Größen 16–128.
- **`test_features330.py`** prüft die Oberfläche und die Datenwege aller
  3.30-Pakete:
  - Zeichen-Editor und Format 20 mit Vorsicherung und Verweisen;
  - Beziehungen, Zeiterfassung, Pixelsymbole und Archiv;
  - Galerie, Pfadzeile, Rückgängig-Hinweis und Suche Strg/Cmd+O;
  - Tagesbeginn und Wochenrückblick;
  - Startseite anpassen und Angeheftetes;
  - Gruppierung in Liste und Tabelle sowie Spaltenboard (500 Karten im
    Grenzwert);
  - Karteninhalt, Zeichnungskarten, Bereiche, Aufräumen, Weiterdenken,
    Verbindungen und Hintergrund;
  - Tagebuch mit allen Inhaltsarten und die Anlageoption Pinnwand;
  - Abschnitte der Seitenleiste, Chipzeile und Leerzustände;
  - Design „Pixel“, Detailbereich, Vorlagen mit Eingabefeldern, Zeitblöcke
    und Präsentation;
  - Referenz-Fixture Format 20 als Fixpunkt;
  - Regressionen der mitbehobenen Leisten- und Linienfehler;
  - aus dem Ausbau: Zeitblöcke ziehen und Alt+↑/↓, Karten-Rückgängig,
    Folien- und Notizfolien-Druckseite, der vollständige Detailbereich,
    Gismo im Leerzustand, Pixelschrift samt Prüfsummen;
  - Datenschutz: eine neuere Speicherdatei bleibt schreibgeschützt, eine
    unlesbare wird gesichert, die Rückfallerkennung warnt, doppeltes Beenden
    lässt `window.conf` stehen;
  - aus dem zweiten Ausbau: Anhänge im Detailbereich, Zeichnungs-PNG in der
    Druckseite, Gruppierung mit Überschriften und Nummern, Stundenraster;
  - aus dem dritten Ausbau:
    - Ziehen aus der Liste ins Stundenraster (mit Bildschirmkoordinaten,
      Vorschau und Rückgängig);
    - gruppierte Tabelle mit Nummern und Überschriften;
    - „Pinnwand öffnen“ aus der Tabelle;
    - Linux-Schriftregistrierung mit nachgebildetem Fontconfig;
  - aus der Überarbeitung für kleine Fenster: sortierte gruppierte Tabelle
    mit Überschriften.

`test_mindestgroesse330.py` misst jede Ansicht bei 860 × 700 in fünf
Kombinationen aus Design, Schriftgröße und Fenstergröße, dazu 1400 × 700.
Befunde sind:

- Überstand über Fenster- oder Elternrand;
- gequetschte Knöpfe;
- abgeschnittener Labeltext;
- seitlicher Überstand auf Scrollflächen.

Die Suite braucht keine Bildschirmaufnahme. Sie misst auch jeden Dialog der
Menüleiste bei seiner Mindestgröße, in mittlerer und großer Schrift.

`test_kontrast330.py` misst in allen zehn Designs den Kontrast jedes
dargestellten Texts: Labels, Eingaben, farbige Zeilen und jeden Knopf in drei
Zuständen. Die Grenze ist WCAG AA (4,5:1, große Schrift 3:1). Texte auf
Zeichenflächen misst sie nicht.

`test_hintergrund330.py` prüft die Hintergrundverläufe:

- alle 50 Entwürfe und die Lesezone mit 4,5:1;
- den Einbau in drei Designs, Glas-Tönung, Menü und Zwischenspeicher;
- das Abschalten und die Auswahl in den Einstellungen;
- seit der Rückmeldung außerdem Schrift statt Pille, Milchglas für Kacheln,
  Listen und Fenster und den Glanz im Innenrand;
- den Start im schmalen Fenster als eigenen Prozess. Ein nativer Absturz
  lässt sich nur so beobachten; der Test erkennt den alten Fehler.

`test_rueckmeldung330.py` prüft die Punkte der Rückmeldung:

- gleiche Unterkanten in sieben Ansichten;
- die Kopfzeilenreihenfolge über Dichtewechsel;
- den Verlauf als Knopf und Karte;
- die Seitenleiste ohne „In Bearbeitung“, „Verlauf“ und Klapppfeil;
- „In Bearbeitung“ als Abschnitt in „Mein Tag“;
- die ruhige Zeichenfläche und die Auswahl;
- seit der zweiten Rückmeldung außerdem:
  - Farbregel, Kennzahlen als Text und „Startseite anpassen“ unten;
  - Eingabe und Leisten je Ansicht;
  - „Erledigte Punkte löschen“ samt Rückgängig und gepacktem
    Rückgängig-Speicher;
  - den Punktdialog mit Verlauf (ohne Endlosschleife);
  - kein Neuzeichnen beim Verschieben.

`test_seiten330.py` prüft die Seitenart:

- Markdown-Rundlauf;
- Seite aus Markdown mit echten Aufgaben;
- Editor: Abhaken, Titel, Enter, Löschen und Rückgängig, Kürzel, Einfügen;
- Export, Seitenübersicht, Ordnertypen und Speichern.

`test_aufraeumen330.py` prüft das Aufräumen, den Seitenbereich und die
Galerie vom 27.09.2026:

- Kopfzeile aus Symbolen, ein Zeichen je Bedeutung;
- keine Knöpfe unter dem Listenbaum, Anlegen-Menü, „…“ an Listenzeilen;
- Auswahlleiste nur mit Auswahl, Ansichtsumschalter;
- Seite ohne Eingabe und Suche auch nach einer Zeichnung;
- Textlogo in der Akzentfarbe, Gismo ohne Rechteck, Fahne unten,
  „Startseite anpassen“ ohne Kästen;
- Pinnwandzeile und Spaltenbreite;
- Seitenbereich, Seitenvorlagen, `.glidepage` hin und zurück, Aufgabenmarken
  nach Vorlage, Duplikat und Import;
- Galerie: Bilder, Kacheln, Großansicht, Titel und Notiz, Entfernen mit
  Rückgängig, Speichern, Einstellungen.

Tempo misst keine Suite; die Messwerte stehen in Vertrag 66, Abschnitt 2.10.
Das Aussehen selbst prüft nur die Sichtprüfung.

`test_paketierung330.py` prüft die Kennungen und das Windows-Skript. Unter
macOS baut die Suite zusätzlich das Entwicklungsbundle und prüft dessen
Signatur, ohne es zu starten.

Unter Windows startet `tests/tools/windows_vollpruefung.cmd` dieselbe
Vollprüfung. Das Skript prüft vorher Python/Tk und OneDrive-Platzhalter.
Anleitung: `00_Arbeitsvorbereitung/Checklisten/Windows_Pruefung_3.30.0.md`.

UI-Messtests nicht parallel zur Vollprüfung laufen lassen. Im Lasttest vom
26.09.2026 scheiterte unter vierfacher Last die Knopfsichtbarkeit in
`test_ui_followup36`; der Test scrollt seitdem vor jeder Messung neu. Die
Wiederholung mit vier parallelen Läufen war danach 4/4 grün. Auch Dateien im
Dokumentbestand – etwa Archivkopien – erst nach dem Lauf anlegen: Der
Dokumentationsschritt prüft ganz am Anfang, ob jede Datei im Index steht.

Die manuelle Prüfliste 3.30.0 liegt in
`00_Arbeitsvorbereitung/Checklisten/Manuelle_Pruefung_3.30.0.md`.

Der Schritt **Zeitzone** misst seit 3.23.0 den Versatz, der für die Suiten tatsächlich gilt, statt ihn nur zu setzen. Gemessen wird im Kindprozess mit derselben Umgebung, die auch die Suiten bekommen; mitgemessen wird, ob die Zone eine Sommerzeitregel kennt, denn die Fehlerklasse um Serienenden hängt daran. Ein Versatz von null ist kein Fehler der Anwendung, sondern eine fehlende Absicherung: Der Lauf endet dann mit Exitcode 2 – unvollständig, nicht bestanden.

`TZ=Europe/Berlin` wird nur dort gesetzt, wo die Laufzeit die Variable auswertet. **Windows gehört nicht dazu**: Es kennt kein `time.tzset()` und liest aus dem Namen keine Zone, sondern eine erfundene ohne Sommerzeitregel und mit einem Versatz, den es an diesem Tag nicht gibt. Dort gilt die Systemzeitzone; ein gesetztes `TZ` meldet der Schritt als Befund. Auf den übrigen Plattformen gibt `TZ` weiterhin die Zone vor, wenn der Aufrufer eine nachstellen will.

`test_features323.py` prüft das zusammengeführte Designsystem mit allen sieben Designs und der Migration alter Einstellungen, die Glasschicht samt Verlauf, die neue Reihenfolge der Systemzeilen mit eingerücktem Eingang, die Richtung der Tagespfeile, den Renderdurchlauf mit Zwischenspeicher und seiner Leerung beim Speichern, die einheitliche Kalenderauswahl, die veränderbaren und gespeicherten Spaltenbreiten, die Sortierung per Einzelklick, die linksbündige Ausrichtung aller sieben Tabellen, die Hover- und Auswahlkontraste in jedem Design, das mehrspaltige Bearbeitungsfenster, das globale Auf- und Zuklappen mit sichtbarem Pfad zur offenen Liste, die Kopfzeilendichte mit Überlaufmenü, die fünf Anzeigemodi der Listenansicht samt Checklisten- und Anhangzeilen, den Rundlauf des Austauschformats einschließlich Markdown-Ebene, die Pinnwandverbindungen mit Persistenz, den Fokusmodus und die Flächenausgabe als PDF. Der Regressionstest zum leeren Spaltenfenster (`dialog_label`) liegt ebenfalls hier. [Designsystem](50_DESIGNSYSTEM_3.23.0.md) · [Leistung und Oberfläche](51_LEISTUNG_UND_OBERFLAECHE_3.23.0.md) · [Austauschformat](52_AUSTAUSCHFORMAT_3.23.0.md) · [Pinnwand](53_PINNWAND_ARBEITSFLAECHE_3.23.0.md) · [Anzeigemodi](54_ANZEIGEMODI_3.23.0.md).

`attributpruefung.py` ergänzt seit 3.23.0 die Analysen: Sie sammelt je Klasse alle über `self` erreichbaren Namen – einschließlich der geerbten Tk-Basen – und meldet Aufrufe ohne Ziel. Der Befund, der zum leeren Spaltenfenster führte, wäre damit vor der Auslieferung sichtbar gewesen.

Die bisherigen Prüfungen für Datenintegrität, Migration, Vorlagen, Wiederholung, Benachrichtigungen und 3.9-Oberfläche bleiben erhalten. `test_workspace310.py` ergänzt:

- Aufgabenbackup vor/nach Öffnen, Schließen, Anheften, Bewegen und Abheften inhaltlich identisch.
- Globale Reitergrenze, LRU, Dubletten, Umordnung ohne Aufgabenumsortierung.
- Bearbeitung derselben Objekte, Erledigen/Undo, Gruppenunterpunkte, wiederkehrende Termine.
- Tatsächliche Tk-Tastatur- und Drag-Ereignisse, Label-/Textfilter und Wiederfinden weit entfernter Karten.
- Neustart mit gespeichertem Sichtzustand; Papierkorb entfernt Referenzen, Undo öffnet sie nicht erneut.
- Ordnerpinnwand mit Punkten aus Unterlisten und Wechsel zur richtigen Quellliste.
- Hell/Dunkel, 860×700 und 1440×1000, ein-/ausgeblendete Seitenleiste, Rückkehr von Startseite/Vorlagen, lange Texte.
- Ungültige Einstellungen und Schreibfehler ohne Verlust vorheriger Ansichtseinstellungen; keine Tk-Callbackfehler.
- Schnellerfassung mit deutscher Fristvorschau, Zielliste, Mehrfacherfassung und Undo; gespeicherte Filter mit dynamischen Zeiträumen, entfernten Referenzen, Trefferzahl und Einstellungs-Rollback.
- „Mein Tag“ mit listenübergreifender Auswahl, stabiler Reihenfolge, unabhängiger Fälligkeit, Persistenz und Schutz vor entfernten oder strukturellen Punkten.
- Tabellenansicht mit flacher Darstellung verschachtelter Aufgaben, identischen Punktaktionen, Such-/Offenfilter und listenspezifischer Spaltenauswahl in den Einstellungen.

Zusätzliche manuelle Abnahme: native Windows- und macOS-Eingabegeräte, Screenreader, mehrere Monitore/DPI, Schlafen/Aufwachen und Langzeitbetrieb. [QA-Bericht](07_QA_BERICHT.md) dokumentiert tatsächlich ausgeführte Nachweise.

`test_features321.py` prüft den Rundlauf über die eigene Ausgabe samt Duplikaterkennung, fremde Dateien mit gefalteten Zeilen, Escaping, BOM und LF-Zeilenenden, Ortszeit, UTC und TZID einschließlich unbekannter Zone, Ganztags- und Mehrtagestermine, beide Dauerangaben, alle abbildbaren und sechs nicht abbildbare Wiederholungsregeln, vier Erinnerungsfälle, alle Übersprungsgründe, den Zeitraumfilter, die Grenzen, beide Importziele, Rückgängig mit Labelrücknahme und den Dialog in beiden Themes. [Bedienung 3.21](45_KALENDERIMPORT_3.21.0.md).

`test_features320.py` prüft den Aufbau aller vier Umfänge, Ganztags- und Uhrzeittermine, die Dauerregeln, jede der sechs Optionen einzeln, alle sechs Wiederholungsarten samt Enddatum, beide Erinnerungsarten, Escaping und Zeilenfaltung einschließlich Rückfaltung, stabile UIDs über zwei Ausgaben, übersprungene Punkte ohne Fälligkeit, die Obergrenze von 2000 Terminen, atomares Schreiben samt abgewiesener Nutzdatendatei, die Unveränderlichkeit von Bestand und Verlauf sowie den Dialog in beiden Themes. [Bedienung 3.20](archiv/44_KALENDERAUSGABE_3.20.0.md).

`test_features319.py` prüft die Migration von Format 14 samt unveränderter Originalkopie, jeden erfassten Vorgang einzeln, die Feldliste bei Änderungen, Erledigen und Wiederöffnen, Verschieben zwischen Elternpunkt, Liste und Ordner, die drei Papierkorbvorgänge, Sammeleinträge an der Schwelle, die Obergrenze von 4000 Einträgen, den Rundlauf über Komplett- und Teilbackup, defekte und fremde Verlaufsfelder, die abschaltbare Erfassung, das Leeren, Suche und Filter sowie den Dialog in beiden Themes bei 780×640. Die Fixtureprüfung kennt die Formatstufen (14 für 3.14.0 bis 3.18.0, darüber 15); neu ist `tests/fixtures/current_v15/reference_v15.json`. [Bedienung 3.19](archiv/43_AENDERUNGSVERLAUF_3.19.0.md).

`test_features318.py` prüft den Rundlauf über eine echte CSV-Exportdatei, alle vier Trennzeichen und vier Kodierungen, Dateien mit und ohne Kopfzeile, die automatische Spaltenerkennung samt englischer Synonyme, jede Werteregel einschließlich Grenz- und Fehlwerten, Verschachtelung aus Ebene und Nummer mit Sprungbegrenzung, beide Importziele und die Ordneransicht, die Grenzen für Zeilen, Spalten und Dateigröße, den Bericht über übersprungene Zeilen und unlesbare Zellen, Rückgängig mit Labelrücknahme sowie den Dialog in beiden Themes bei 780×640. [Bedienung 3.18](archiv/42_CSV_IMPORT_3.18.0.md).

`test_features317.py` prüft das Grundgerüst aller vier Druckformate, die Abwesenheit externer Verweise, das Escaping von Titel, Punkttext und Beschreibung, jede der sieben Optionen einzeln, die Mengen je Format einschließlich leerer Auswahl, den Ordnerdruck, Art und Einrückung von Gruppen, die Obergrenze von 2000 Punkten, atomares Schreiben samt abgewiesener Nutzdatendatei und den Dialog in beiden Themes. [Bedienung 3.17](archiv/41_DRUCK_UND_PDF_3.17.0.md).

`test_features316.py` prüft Archivaufbau und Abschnittstrennung, den Rundlauf über echte Dateien, die Verträglichkeit mit dem Aufgabenimport, alle Vorschauwerte, sieben Varianten ungültiger Zusatzabschnitte, Nicht-Archiv und fremdes Archiv, die vier Teilbereiche einzeln und gemeinsam, das Verwerfen der Ansichtsverweise, die drei Rückfallsicherungen, leere Auswahl, Abbruch, gesperrte Bereiche und den Dialog in beiden Themes. [Bedienung 3.16](archiv/40_APP_BACKUP_3.16.0.md).

`test_features315.py` prüft die Rechenregeln der Aufwandsbilanz samt Grenzwerten, die Normalisierung und den Rückfall der Tageskapazität, Menge, Reihenfolge, Zähler und Leertext der Tagesplanung, den Tageswechsel, Such- und Offenfilter, Punktaktionen mit Rückgängig, ungültige Bearbeitungstage, das Serienvorrücken, die von Filtern abhängige Tabellensumme, die Startseitenzeile sowie den Einstellungsdialog in Hell/Dunkel bei 780×640. [Bedienung 3.15](archiv/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

`test_features314.py` prüft leere Altwerte, ungültige Datums-/Minutenwerte und Grenzen, Originaldateisicherung und Sicherungsfehler, Neuladen, Vollbackup, Papierkorb, Vorlagen mit relativen Terminen, TXT-Rundlauf, Markdown/CSV, Mehrfachbearbeitung mit Erhalten/Löschen, Undo, Artwechsel und Wiederholungen. Echte Dialoge prüfen Speichern, Validierung und Abbruch in Hell/Dunkel bei 780×640. [Bedienung 3.14](archiv/37_PLANUNG_UND_AUFWAND_3.14.0.md).
