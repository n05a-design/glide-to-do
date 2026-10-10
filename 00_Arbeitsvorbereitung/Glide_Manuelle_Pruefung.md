# Manuelle Prüfung – Glide

Stand 10.10.2026 · Glide 3.36.0 · Aufgabenformat 23 · manuelle Sitzungen offen; B1 automatisch geprüft

Einzige Prüfliste für alles, was nur am echten Gerät geht. Zusammengeführt am 03.10.2026 aus der fortgeschriebenen Prüfliste (Ursprung 3.30.0, enthielt die Listen 3.28 und 3.29) und der Windows-Anleitung; die Zuordnung der 201 Ausgangspunkte trägt Git. Automatisch geprüft ist die Logik ([Prüfplan](../01_Repository/Glide/docs/05_QA_TESTPLAN.md), [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md)); offen bleiben Handgefühl, Plattformen und fremde Programme.

**Sitzungen:** A am Mac (etwa 60 Minuten), B am Windows-PC nach der Vollprüfung, C Bildschirmleser und Tastatur, D Linux (falls vorhanden), E nur durch den Inhaber.

**Sprintnachlauf 3.36.0, getrennt offen:** Auf Mac, Windows und Linux jeweils Startseite öffnen → Liste → zurück, auch bei 860 × 700/großer Schrift und Hell/Dunkel: Scrollleiste sichtbar und mit Maus/Trackpad bedienbar. Bibliothek weit scrollen, Aufgabe in einer Karte ändern/Undo, Titel/Vorschautext ändern und Karten umordnen: Fokus/Scrollposition und Inhalte bleiben nachvollziehbar. Einstellungen öffnen, Kapazität ändern/Abbrechen, erneut öffnen (alter gespeicherter Wert); danach Design/Schrift ändern und erneut öffnen. Alle Vorschauen beim Scrollen erreichbar, Escape/Fenster-X beendet den Dialog. Windows zusätzlich vorhandene Fälle W01/W06–W08 (Titelkürzung, Dialogbreiten und Tabellenfeldabstände), Linux N08 (native Bildvorschau) nach der jeweiligen automatischen Vollprüfung durchführen. Diese Punkte sind durch Screenshots und CI noch nicht menschlich abgenommen.

## Rahmen

- Immer mit getrennter Ablage prüfen: `GLIDE_DATA_DIR` auf einen Testordner
  setzen. Beispielinhalt: den [Showcase](../05_Probelisten_Testdaten/Showcase/README.md)
  über seinen eigenen Starter oder den Rundgang
  (`01_Repository/Glide/tests/fixtures/beispiele/glide_rundgang.glidebackup`)
  über Datei › Listen/Ordner hinzufügen … einlesen. B2 nutzt eine
  unveränderte Kopie des eigenen Windows-Bestands; keine Prüfung verändert
  das Original.
- Befunde mit einem Bildschirmfoto nur des Glide-Fensters festhalten und im
  QA-Bericht der Version eintragen.

## A. Mac (etwa 60 Minuten)

- [ ] **A1 Programmsymbol:** Beide bereits abgeglichenen Startfassungen mit
      geerbtem `GLIDE_DATA_DIR` auf einen Testordner starten: Python-Fassung
      über `07_Python-Versionen/Schnellstart.pyw`, Bundle über
      `build/macos/Glide.app/Contents/MacOS/Glide` direkt aus derselben
      Terminalumgebung. Ein Finder-Start übernimmt diese Terminalvariable
      nicht. Im Dock stehen Glide-Name und Glide-Symbol. Für diese Sichtprüfung
      keinen ungeprüften Neubau über den ausgelieferten Stand schreiben.
- [ ] **A2 Logo:** Bei breitem Fenster steht das Logo links neben Titel und
      Unterzeile, auf der Flucht der Seitenleiste. Fenster schmal ziehen: Das
      Logo weicht, der Titel rückt an den Rand. Akzentfarbe wechseln
      (Einstellungen, ganz oben): Das Logo folgt. Auf dem Retina-Bildschirm
      ist es scharf. Klick auf das Logo öffnet „Über Glide“ mit Logo.
- [ ] **A3 Lupe:** ⌕ öffnet die gemeinsame Palette für Inhalte und Aktionen; sie wirkt so schwer wie die übrigen höchstens vier Kopfsymbole.
- [ ] **A4 Arbeitsfläche:** Pinnwand (Spalten), Liste, Tabelle, Seite und
      Zeichnung reichen bis zur Unterkante der Seitenleiste. Der Hinweis
      unten in der Liste ist gut lesbar. Einen Punkt markieren: Die
      Auswahlleiste ersetzt den Hinweis, nichts springt.
- [ ] **A5 Pixel-Werkstatt mit Maus und Trackpad:**
  - Strg+Mausrad zoomt um den Zeiger, die mittlere Maustaste verschiebt.
  - Linie, Rechteck und Ellipse mit Umschalt und Alt ziehen.
  - Rechtsklick malt mit der zweiten Farbe.
  - Schnelle diagonale und kreisförmige Züge haben keine Lücken.
- [ ] **A6 Ziehen mit Maus und Trackpad:**
  - Pinnwandkarten zwischen Spalten ziehen;
  - Bereiche am Kopf ziehen und in der Größe ändern;
  - Zeitblöcke im Stundenraster ziehen;
  - in Seiten Bilder an der Ecke ziehen und in eine andere Spaltenhälfte
    ziehen;
  - Bilder aus dem Finder in Seite und Galerie ziehen;
  - Punkte auf „Heute“ in der Seitenleiste ziehen;
  - den Detailbereich in der Breite ziehen;
  - bestehende Seiten-, Listen- und Notizbereiche umordnen und in passende
    Ordner ziehen: korrekte Vorschau/Zielposition, Arten/IDs erhalten, Undo;
    neutrales Umordnen verändert keine Termine.
- [ ] **A7 Gedrücktes Mausrad:** oben, unten, links und rechts außerhalb der
      Totzone halten; die Fläche läuft selbst und stoppt beim Loslassen.
- [ ] **A8 Systemmitteilungen:**
  - Ansicht › Systemmitteilung testen: macOS fragt einmal nach der
    Erlaubnis, danach erscheint die Probe.
  - Einschalten und eine Erinnerung in zwei Minuten setzen: genau eine
    Mitteilung.
  - Drei zur selben Zeit: eine Sammelmeldung.
  - Aus `Glide.app` gestartet erscheint sie unter „Glide“.
- [ ] **A9 Druck und PDF im Browser:** „Präsentation als PDF …“, „Folien als
      PDF …“ und „Drucken und PDF …“ öffnen, als PDF sichern und lesen. Eine
      Zeichnungskarte ist scharf.
- [ ] **A10 Fremde Programme:**
  - eine Palette `.gpl` in Aseprite oder Pixelorama öffnen und zurück
    importieren;
  - ein Zeichnungs-SVG im Browser und in Affinity oder Illustrator öffnen;
  - nach dem Speichern dort in Glide importieren: verlustfrei oder mit
    verständlicher Ablehnung;
  - eine Seite „Als Markdown speichern …“ und in einem Markdown-Programm
    mit Bildern öffnen.
- [ ] **A11 Tempo, gefühlt:**
  - Pinnwand mit 500 Karten und Galerie mit 100 Bildern: scrollen und ziehen
    bleiben flüssig.
  - Eine lange Seite scrollt endlos und ruhig.
  - Schnell hintereinander abhaken und umbenennen: keine Verzögerung.
  - `Schnellstart.pyw` zweimal starten: kalten/warmen Start vergleichen;
    keine allgemeine Zeitgarantie.
  - Bibliothek unverändert aktualisieren, Status ändern und umordnen:
    Verhalten mit den Performance-Regeln der Architektur vergleichen. Ansichtswechsel, Speichern und
    viele tatsächlich dargestellte Karten separat beobachten.
- [ ] **A12 Zwangsbeenden:** Einen Punkt ändern und Glide sofort hart beenden
      (Aktivitätsanzeige › Sofort beenden). Nach dem Neustart ist die
      Änderung da.
- [ ] **A13 Sichtprüfung der Designs:**
  - Hell, Dunkel, Liquid Glass hell und dunkel, Pixel und Kontrast, je mit
    und ohne Hintergrundverlauf.
  - Fenster vergrößern, verkleinern und die Seitenleiste umschalten: keine
    Kanten, Versätze oder Bildreste; Titel und Hinweise gut lesbar.
  - Gismo im Dopamin-Design zehnmal füttern, spielen, ruhen: nichts wird
    weiß.
- [ ] **A14 Kalender im kleinen Fenster:** Monatsansicht bei 860 × 700;
      Einträge enden mit „…“, volle Tage zeigen „+N“. Diese Texte liegen
      auf einer Zeichenfläche und werden nicht automatisch gemessen.
- [ ] **A15 Globale Suche** (seit 29.09.2026 ohne Schatten): in allen Designs
      über Startseite, Liste, Pinnwand und Seite öffnen. Rahmen in der
      Akzentfarbe, die Fläche hebt sich ab; ein Klick daneben schließt sie.
- [ ] **A16 Seitenleiste mit Seiten, Listen und Notizen** (29.09.2026):
  - Reihenfolge Seiten, Listen, Notizen. Der Pfeil klappt seinen Bereich
    ein, der Titel öffnet die Übersicht, „+“ legt an.
  - Den Ordner mit der geöffneten Liste zuklappen, dann einen Punkt abhaken,
    umbenennen und die Ansicht wechseln: Der Ordner bleibt zu.
  - Über einer Bibliothek und einem Notizbuch erscheinen beim Überfahren „+“
    und „…“; „+ › Neuer Unterordner …“ legt einen Unterordner derselben Art
    an.
  - Bei 860 × 700 bleibt die Überschrift „Notizen“ sichtbar, und eine
    geöffnete Notiz zeigt mehrere Zeilen Text.
- [ ] **A17 Rückmeldung vom Abend** (29.09.2026, echte Maus und Trackpad):
  - Notizbereich zuklappen: kein stehengebliebenes „Tagebuch“.
  - Pinnwand mit zwei Fingern quer scrollen.
  - Jeden Dialogbefehl der Menüleiste einmal wählen, auch ohne „…“: Jedes Fenster
    erscheint vorn, auch „Referenzbild laden …“ und der Knopf „Referenz“ der
    Zeichnungsseite (PNG, JPEG, HEIC, SVG).
  - Seite und Notiz: Rechtsklick, Formatleiste über einer Markierung,
    „Umwandeln in“, Zeile nach oben und unten; Aufklappliste zu- und
    aufklappen, Glide neu starten: der Zustand bleibt; „Mehr › Gliederung“.
  - Bild in einer Seite an der Ecke größer ziehen: der Rahmen folgt flüssig.
  - Knopffarben: Rot nur bei Löschen, Grün nur bei Bestätigen, Lila bei
    Hinzufügen, die Glocke gelb.
  - Scrollen auf Startseite und „Listen und Ordner“ mit Verlauf: spürbar
    flüssiger als vorher; kurz versetzte Flächen während des Scrollens sind
    bekannt.
- [ ] **A18 Ausbau Etappe 1** (3.32.0, 30.09.2026):
  - Eine 16×16-Zeichnung als Symbol (ICO, Grund durchsichtig) exportieren und
    im Finder bzw. Explorer ansehen; als favicon.ico im Browser öffnen.
  - Eine echte Aseprite-Datei und Adobe-Farbfelder (.ase) als Palette
    importieren.
  - Eine eigene Vorlage mit „{{Wochentag}} KW {{KW}} – {{Projekt}}“ verwenden:
    Nur „Projekt“ wird gefragt.
  - Abends „Tagesabschluss …“: Offenes auf morgen legen, Rückblick in die
    Tagesnotiz übernehmen.
  - **Hänger:** Über die Menüleiste „Hilfe › Über Glide“ öffnen und mit OK
    schließen, ebenso „Tastenkürzel anzeigen“, „Datei › Neu anlegen › Neue Liste“
    und Cmd+Q mit Rückfrage – Glide reagiert danach sofort weiter.
  - **Seite mit Bildern:** Eine Seite mit mehreren Bildern öffnen, zu einer
    anderen Liste und zurück wechseln, das Fenster größer und kleiner ziehen
    und scrollen – kein Hänger, keine Fehlermeldung.

- [ ] **A19 Klappmechanismen (D08):** einzelne Labels einschließlich „Ohne
      Label“, Aufgaben-/Gruppenfächer, verschachtelte Bibliotheken, Seiten/Listen/
      Notizen und Angeheftet per Pfeil und Tastatur auf/zu. Suche, Refresh,
      Bearbeiten, Undo, Ansichtswechsel und Neustart: Zustände bleiben erhalten.
      Globale Auf-/Zuklappaktion prüfen; keine versehentliche Navigation/Drag.
- [ ] **A20 Drag-Ziele (D04/D02):** Bereichswechsel mit Maus/Trackpad bei
      gescrollter Seitenleiste, gültigem/ungültigem Ziel und Abbruch. Vorschau
      entspricht dem tatsächlichen Ziel; ein Undo-Schritt stellt den Bestand
      wieder her. Neutrales Umordnen erhält Bearbeitungstag und Fälligkeit.
- [ ] **A21 Karten/Aktionsleisten:** Tk-/OS-Fokus und Scrollposition beim
      wiederholten Refresh mit physischer Tastatur prüfen; Status/Titel/Label/
      Notiz/Bild ändern, Undo, Tageswechsel, Schrift/Design/Breite wechseln.
      Öffnen wirkt auf das aktuelle Objekt; Entfernen/Archiv/Rückkehr zeigen
      keine veralteten Vorschauen. Hintergrundtests belegen keinen OS-Fokus.

- [ ] **A22 Vier Bereiche (3.33.1):** Seiten, Listen, Notizen, Zeichnungen
      ein- und ausblenden; Inhalte nur im passenden Bereich anlegen und
      hineinziehen; im Notizbuch eine datierte Zeichnung anlegen; gemischte
      Altordner erscheinen vollständig unter Listen. Neustart erhält die
      Sichtbarkeit. Dialog „Neu anlegen“ bei niedrigem Bildschirm zweispaltig.
- [ ] **A23 Startseite „Ruhig“ (3.33.2):** sieben Kacheln; in „Heute“ stehen
      Tagesziel und nächste Aufgabe genau einmal. Begrüßung oder Uhr über „+“
      einblenden, Glide neu starten: Auswahl bleibt. „Standard
      wiederherstellen“; Hover der Knöpfe.
- [ ] **A24 Schnelleingabe (3.33.3/3.33.4):** „Angebot schicken morgen bis
      Freitag !hoch #Label 45 min“ tippen: Chips erscheinen beim Tippen, × nimmt
      einzeln zurück, Return legt an, Rückgängig. „Sport jeden Montag 18 Uhr“:
      Wiederholung mit Fälligkeit, steht im Kalender, Abhaken erzeugt den
      Folgetermin. Chipleiste bei großer Schrift und schmalem Fenster.
- [ ] **A25 Eisenhower (3.33.5):** Board „Gruppieren: Dringlichkeit ×
      Wichtigkeit“; Karten mit echter Maus zwischen den vier Spalten ziehen;
      eine Karte mit Fälligkeit in zwei Tagen nach „Einplanen“ ziehen: Glide
      lehnt ab und sagt warum; Rückgängig.
- [ ] **A26 Heute und Demnächst (3.33.6):** Abschnitte in fester Reihenfolge,
      keine Aufgabe doppelt; Verweis „Demnächst“ mit Doppelklick und Return;
      „Tag …“ startet Tagesbeginn und Tagesabschluss; ◀/▶ zu anderen Tagen;
      Abschnitte zuklappen und neu starten.

- [ ] **A27 Sprint 3.33.19–3.35.0** (mit getrennter Testablage, echte Maus, Trackpad und Tastatur):
  - **Komfort (3.33.20):** Wiederkehrende Aufgabe über das Kontextmenü „Diesen Termin überspringen“; „erinnere 9 Uhr“ in der Eingabezeile ergibt einen Chip; mehrere Zeilen einfügen fragt nach; „+“ und Umschalt+Enter; nach einem Update erscheint einmal die Karte „Neu in Glide“; Routinen in „Heute“ abhaken.
  - **Ruhige Oberfläche (3.33.21):** Einstellungen › „Automatisch hell/dunkel“ einschalten und das Erscheinungsbild in den Systemeinstellungen wechseln – Glide folgt ohne Neustart; Ansicht › „Seitenleiste schmal“; Gismo-Pflegeknöpfe erscheinen beim Überfahren; Pinnwand mit einer Werkzeugzeile und Menü „…“; Seitentitel über der Lesespalte.
  - **Wissen und Seiten (3.34.0):** zwei Bilder auf aufeinanderfolgenden Absätzen überlappen nicht; Mehr › „Drucken und PDF …“ zeigt die Bilder; „Als Markdown speichern …“ und „Markdown als Seite öffnen“ bringen die Bilder zurück; ein Suchtreffer öffnet die Seite mit markierten Fundstellen, Esc hebt auf; im gespeicherten Filter „Warum steht das hier?“; Alt+Pfeile im Seitenbaum.
  - **Pixel und Austausch (3.35.0):** Doppelklick auf eine Farbe der Farbleiste zeigt die Umfärbung vor der Rückfrage; Symbolexport zeigt 16/32/48 px hell und dunkel; „Für KI bereitstellen …“ mit Zweck „überarbeiten“ und einen von Hand geänderten Vorschlag importieren (Konflikt nach einer Zwischenänderung sichtbar); Datei › Sicherung › „Sicherungen vergleichen …“.

## B. Windows-PC (nach der Vollprüfung)

- [ ] **B0 Windows-Vollprüfung – Anleitung**

Dieselbe Vollprüfung wie am Mac (`tests/tools/pruefen.py --modus voll`), gestartet über `windows_vollpruefung.cmd`. Sie umfasst alle Integrationssuiten aus `SUITEN` (3.35.0: 82), Unit-Tests, Showcase, fünf Analysen und die Reproduktion von Beispiel- und Releasedaten. Seit 05.10.2026 legt sie wie am Mac von jedem geprüften Fenster ein Foto ab. Dauer am Arbeitsrechner: 15–20 Minuten.

**Vorbereitung (einmalig je Rechner):**

1. **Prüflaufzeit Python 3.14 mit Tk 9:** Der Starter nimmt der Reihe nach:
   - `-PythonExecutable <Pfad>`;
   - die separate Laufzeit `$env:USERPROFILE\.cache\glide-qa\python-3.14.8\runtime\python.exe`;
   - `py -3.14`;
   - zuletzt `python`.

   Er gibt Python- und Tk-Version aus (`package provide Tk`, nicht die Tcl-Version). Ist Python älter als 3.14 oder Tk älter als 9, endet er mit Exitcode 3, bevor eine Suite läuft. Historisch wurde am 05.10.2026 eine separate 3.14.8-Laufzeit geprüft; am aktuellen Arbeitsrechner läuft die installierte Python-Fassung 3.14.7/Tk 9.0.4 über `py -3.14`, die separate Laufzeit ist hier nicht vorhanden ([Herkunft und Herstellerhash](https://github.com/n05a-design/glide-to-do/blob/254541aeae4577c0529d1ef768846a5c4546e59f/01_Repository/Glide/tests/qa-3.33.8/windows_2026-10-05/prueflaufzeit.json)). Auf einem anderen Rechner entweder Python 3.14 von [python.org](https://www.python.org/downloads/windows/) installieren (Option „tcl/tk and IDLE“, Python-Starter `py`) oder die separate Laufzeit anlegen. Diese ändert weder PATH noch Standardinstallation:

   ```powershell
   $ziel = "$env:USERPROFILE\.cache\glide-qa\python-3.14.8"
   New-Item -ItemType Directory -Force $ziel | Out-Null
   Invoke-WebRequest https://www.python.org/ftp/python/3.14.8/python-3.14.8-amd64.zip -OutFile "$ziel\paket.zip"
   (Get-FileHash "$ziel\paket.zip" -Algorithm SHA256).Hash  # 4873947A8AFC037846B180312B83C744A4146A851CFD316A75C3125A4D8299DA
   Expand-Archive "$ziel\paket.zip" "$ziel\runtime"
   ```

   Der Hash ist der des Herstellers (Paketindex `python.org/ftp/python/index-windows.json`, Eintrag `pythoncore-3.14-64`, 3.14.8). Weicht er ab, nicht entpacken. In PowerShell heißt der Benutzerordner `$env:USERPROFILE`. `%USERPROFILE%` ersetzt nur die Eingabeaufforderung (`cmd`); PowerShell nimmt es wörtlich und legt etwa mit `New-Item` einen Ordner dieses Namens an.
2. **Projektordner:** die Git-Arbeitskopie `glide-to-do` aktuell ziehen (`git pull`). Liegt sie in OneDrive:
   - Den Ordner per Rechtsklick auf „Immer auf diesem Gerät behalten“ stellen und warten, bis alle Dateien heruntergeladen sind. Nur online verfügbare Platzhalter ließen den Lauf 3.28 scheitern; das Skript bricht dann mit Exitcode 4 ab.
   - `git status` muss sauber sein. OneDrive-Konfliktkopien (`<Name>-<Gerätename>.md`) vorher löschen; sie sind keine Projektdateien.
3. Glide schließen.

**Prüfung starten:**

- **Doppelklick:**
  `01_Repository\Glide\tests\tools\windows_vollpruefung.cmd`;
- **oder in PowerShell** aus `01_Repository\Glide`:
  `powershell -NoProfile -ExecutionPolicy Bypass -File tests\tools\windows_vollpruefung.ps1`.

Während des Laufs öffnen und schließen sich Glide-Fenster im Vordergrund. Den Hintergrundmodus des Mac gibt es unter Windows nicht. Deshalb Maus und Tastatur nicht benutzen, den Rechner nicht sperren und keine rechenintensiven Programme starten: Einige Oberflächentests messen Layouts und reagieren auf Last.

**Ergebnis:**

- Am Ende stehen **Exitcode** und Protokollordner, zum Beispiel
  `tests\qa-<Version>\windows_<Datum>_<Uhrzeit>`:
  - `0`: alle automatischen Schritte bestanden;
  - `1`: mindestens ein Schritt gescheitert, die Logdatei im Ordner nennt ihn;
  - `2`: unvollständig, weil Tk oder die Zeitzonenmessung fehlte;
  - `3`: Python/Tk ungeeignet;
  - `4`: OneDrive-Platzhalter.
- **Sichtprüfung der Aufnahmen** (nur lokal, nicht hochladen):
  - `screenshots\release_hell.png` und `release_hell_dunkel.png`: Releaseplanung im hellen und im dunklen Gegenstück des Standarddesigns. Die beiden Bilder müssen sich unterscheiden; der Erzeuger bricht sonst ab.
  - `fenster\*.png`: jedes geprüfte Fenster einzeln.

  Auf Schärfe, Logo mit glatten Kanten und abgeschnittene Texte ansehen. Seitenleistentitel ohne „…“ müssen vollständig sein (Vorbefund W01, siehe B1a). Das Design „Pixel“ prüfst du von Hand (B3).
- **Zurückmelden:** Exitcode, Name des Protokollordners und Befunde der Sichtprüfung. Der Agent liest `ergebnis.json` über den verknüpften Rechner oder als Anhang. Er legt den Nachweis unter `tests/qa-<Version>/` an und überträgt das Ergebnis in den [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). Rohprotokolle (`*.log`) und Bilder bleiben lokal.

**Ohne Starter:** Bei Bedarf die Vollprüfung mit ausdrücklicher Laufzeit starten. Die Ausgabe der ersten Zeile prüfen, weil dieser Weg Tk 9 nicht erzwingt:

```powershell
$py = "$env:USERPROFILE\.cache\glide-qa\python-3.14.8\runtime\python.exe"
& $py -B tests\tools\pruefe_tk.py   # erwartet: Tk 9.0.x
& $py -B tests\tools\pruefen.py --modus voll --protokoll tests\qa-<Version>\windows_manuell --timeout 900
```

Ergebnis und tatsächlich verwendete Python-/Tk-Version dokumentieren; kein Windows-Nachweis wird aus dem Mac-Lauf abgeleitet.

- [x] **B1 Vollprüfung (automatisch):** Windows zuletzt 3.33.18 (08.10.2026): Exit 0, 95 Schritte, 76 Integrationssuiten, 170 Unit-Tests, Lieferung bytegleich ([Nachweis](../01_Repository/Glide/tests/qa-3.33.18/seiten_2026-10-08/README.md)). Referenz-Mac 3.35.0 (09.10.2026): Exit 0, 99 ausgeführt, 82 Integrationssuiten, 257 Unit-Tests ([Nachweis](../01_Repository/Glide/tests/qa-3.35.0/austausch_2026-10-09/README.md)). Für 3.33.19–3.35.0 steht die Windows-Vollprüfung nach B0 aus; die menschliche Sichtprüfung bleibt je Lauf übersprungen, deshalb sind B1a–B1i offen.
- [ ] **B1a Sichtprüfung der Aufnahmen am Gerät:** Die Fotos des nächsten Windows-Laufs (B0) unter `tests\qa-<Version>\<Lauf>\…\fenster` und `screenshots` durchsehen (sie bleiben lokal). Die Vorbefunde mit Testablage in Glide nachstellen:
  - **W01** Seitenleiste: Lange Listentitel enden mit „…“, kürzere stehen vollständig da („Unterlagen & Assets“).
  - **W05** (auf dem Mac behoben in 3.33.21) Datei › Datenaustausch › „Für KI bereitstellen …“ und Ansicht › Liste › „Tabellenspalten …“: Ist die Fensterbreite angemessen, stehen die Knöpfe rechts wie in den übrigen Dialogen?
  - **W06** „Neue Liste“ mit der Art Aufgaben bzw. Pinnwand und „Neuer Ordner“ mit Ordner, Buch und Notizbuch: Sind Überschrift und Feldbeschriftungen sichtbar? Mehrmals hintereinander öffnen.
  - **W07** Zeichnung › Referenz mit einem PNG › „Ganzes Bild zeigen“: Steht der Hinweistext genau einmal da?
  - **W08** Rechtsklick auf eine Liste › „Pixelsymbol …“: Ist das Raster groß genug zum Zeichnen?

  B2–B13 bleiben physische Inhaberprüfungen.
- [ ] **B1b Gestaltungsabnahme U10/U19/OB01 (3.33.12, OB06):** Die Vorher-Fotos von 3.33.12 liegen außerhalb der Aufbewahrung; die Gestaltung am laufenden Stand beurteilen: Liste und Heute, 1280 × 800 und 860 × 700, hell und dunkel, mit getrennter Testablage auch große Schrift. Titel hat Vorrang vor Kennzahlen, Herkunft rechts ist lesbar, Kopf und Zeilen wirken ruhig. Lange Kennzahlen mit Auslassung und vollständigem Tooltip prüfen; Aufgaben ohne Fälligkeit zeigen kein Datum. Die automatisierte Geometrie- und Bedienprüfung ersetzt diese Bewertung nicht. Entscheidung im [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md) festhalten; Fotos bleiben lokal/unversioniert.
- [ ] **B1c KO01/AU02 (3.33.13):** am laufenden Stand bei
      860 × 700 und 1280 × 800, hell/dunkel bewerten. Zwei Aufgaben aus verschiedenen
      Quelllisten in Heute markieren, Rechtsklick → Einplanen → Morgen:
      Fälligkeit/Uhrzeit/Aufwand bleiben; ein Strg+Z nimmt beide zurück.
      Strg+Umschalt+P, Kalenderaktion beim Überfahren einer Zeile und Datum …
      mit Abbruch prüfen. Freie Zeit/Überplanung vor Übernahme mit dem Profil
      des Zieltags vergleichen, Aufgaben ohne Schätzung getrennt. Tagesbeginn:
      dieselben sechs Ziele; Ohne Tag erhält die Uhrzeit. Nach Neustart prüfen.
      Automatische Nachweise ersetzen diese physische Gestaltungsabnahme nicht.

- [ ] **B1d Tagespaket (3.33.14):** mit getrennter Testablage Rückblick → „Was passt heute?“ → Raster bedienen. Gründe/Auswahlbudget einschließlich unbekannter Kapazität und fehlender Schätzung prüfen; Übernahme am festen Kartenfuß auch bei 860 × 700/großer Schrift erreichbar. Mehrfachauswahl mit Strg+Umschalt+T planen, Raster mit Tab/Enter/Alt+Pfeilen/Entf/Esc bedienen und rücknehmen. Fokus mit Strg+Umschalt+F, Pause/Fortsetzen, Beenden & Buchen und Erledigt & weiter; Pausenzeit zählt nicht, Abschluss und Zeit gemeinsam rücknehmbar. Hell/dunkel, echte Tastatur/Screenreader/DPI und Wiederaufnahme nach Neustart prüfen; automatische Nachweise ersetzen diese Bewertung nicht.

- [ ] **B1e Aufgaben im Wissen (3.33.15):** Mit separater Testablage eine Aufgabe im Notiztext erzeugen und denselben Punkt in der Notizliste abhaken/umbenennen. Vorhandene Aufgabe über „Mehr › Aufgabe verknüpfen …“ zweimal einsetzen, einen Verweis löschen und den anderen bearbeiten. Auch einen Verweis auf einen Punkt derselben Notiz löschen: Punkt bleibt. Heimatzeile trotz zweitem Verweis löschen: Punkt im Papierkorb; Undo/Redo ohne Duplikat. Seitenaufgabe mit Unterpunkten „In Liste übernehmen …“; gleiche IDs und Verweiszeile erhalten, globales Undo prüfen. Ansicht › Aus Seiten und Textquelle öffnen; Archiv, Papierkorb, endgültig fehlendes Ziel, Text-Undo/Redo, Import und Neustart. Mehrzeiliger Klartext darf keine Verweiskennung in neue Absätze tragen. Bei Mindestfenster/großer Schrift/hell/dunkel Ziele und fehlende Ziele gut lesbar; echte Tastatur/DPI/Screenreader prüfen. Format-21-Vorsicherung und Hinweis verstehen; ältere Fassungen nur auf separaten Kopien prüfen. Automatische Prüfung ersetzt diese Bedienabnahme nicht.

- [ ] **B1f Bedienkomfort (3.33.16):** Strg+O und Befehlsfilter `>` mit echtem Editorfokus, Escape und Rückkehr prüfen; Kopfaktionen und Kontextmenüs erreichbar. Hinweise über `?` ein-/ausblenden, Neustart; Bibliothekskacheln mit Maus/Return/Leertaste öffnen, Fußaktionen und Archivkontext. Bearbeitungstag und Fälligkeit nebeneinander lesbar, mindestens 860 × 700, große Schrift und hell/dunkel; native DPI/Mehrmonitor prüfen.

- [ ] **B1g Wissen und Woche (3.33.17):** Strg+K, Woche/Monat und Wochenrückblick ohne Modalität. Mehrfachauswahl per Tastatur einplanen, Maus/Trackpad auf sichtbare Tagesziele ziehen, Randscrollen und Abbruch außerhalb; Fälligkeit unverändert, je ein Undo. Kapazität/fehlende Schätzung verstehen, vorgeschlagenes Zeitfenster ausdrücklich bestätigen oder abbrechen. Seiten-/Listen-/Aufgabenverweise über @ und Kontextmenü; Rückverweise nach Umbenennen, Archiv, Papierkorb, Undo und Neustart prüfen. Kleine Fenster/große Schrift scrollen den Inhalt, Datum und Planungsaktionen im Fuß erreichbar. Vorsicherungs-/Schreibschutzhinweise mit separaten Testkopien verstehen; Linux-, DPI-/Tastatur- und menschliche Abnahme offen.

- [ ] **B1h Seiten im Alltag (3.33.18):** In separater Testablage Live-Liste einbetten; Originalaufgabe per Leertaste abhaken, Details öffnen, Quelle umbenennen/archivieren/löschen, Undo und Verknüpfung lösen. Mehrere und leere Quellen, lange Titel sowie Mindestfenster/große Schrift/hell-dunkel prüfen. Lokales Titelbild und Pixelzeichnung wählen, Bibliothekskarte ansehen, Kopie/Backup/Import/Papierkorb/Neustart. Vorlagen aus dem Anlegen-Menü ausfüllen und Vorschau einschließlich Termine/Titelbild lesen; Escape erhält den Bestand, Return legt an. Native DPI/Screenreader und menschliche Gestaltung prüfen; automatische Nachweise ersetzen diese Abnahme nicht.

- [ ] **B1i Sprint 3.33.19–3.35.0 unter Windows:** dieselben Wege wie A27; zusätzlich „Automatisch hell/dunkel“ mit dem Windows-Farbmodus (Registrierung), Drucken und PDF im Standardbrowser, Markdown-Bildverweise mit Laufwerksbuchstaben, Kontextpaket und Vorschlag mit Umlauten im Dateinamen, Doppelklick-Geschwindigkeit der Farbleiste nach Windows-Einstellung.

- [ ] **B2 Windows-Bestand (Format 17, Inhaberprobe):** Eine unveränderte
      Kopie des eigenen Bestands in einer getrennten Testablage mit
      `GLIDE_DATA_DIR` und aktueller Fassung aus `07_Python-Versionen` öffnen.
      Original erhalten; die folgenden Umstellungshinweise gelten beim ersten
      tatsächlichen Wechsel von Format 17 auf 20.
  - Der Hinweis „Bestand umgestellt“ erscheint.
  - Im Backup-Ordner liegen `liste_vor_format20_*.json`, gegebenenfalls
    `liste_vor_titelkuerzung_*.json`, und die Meldung „Titel gekürzt“.
  - Listen, Notizen, Papierkorb und Pinnwände sind vollständig.
- [ ] **B3 Design „Pixel“:** Seitentitel und Kachelköpfe in Pixelify Sans,
      Umlaute und ß korrekt.
- [ ] **B4 Skalierung:** 100, 150 und 200 % sowie zwei Monitore. Logo,
      Pixelsymbole und Zeichnungen sind scharf.
- [ ] **B5 Logo und Lupe:**
  - Mit Python 3.14 (Tk 9) ist das Logo glatt, auch bei 150 und 200 %; mit
    3.13 (Tk 8.6) ist es eine Fläche mit harten Kanten, Fenster- und
    Taskleistensymbol sind dann ebenfalls treppig. Ursache und Lösungswege:
    [Diagnose](../01_Repository/Glide/docs/diagnosen/LOGO_KANTENGLAETTUNG.md).
  - Die Lupe ⌕ ist lesbar; bitte notieren, aus welcher Schrift sie kommt
    (`tests/tools/symbolpruefung.py`).
- [ ] **B6 Startmenü-Verknüpfung:**
  `powershell -ExecutionPolicy Bypass -File packaging\windows\verknuepfung_anlegen.ps1`.
  - „Glide“ mit Glide-Symbol erscheint im Startmenü.
  - Glide startet ohne Konsolenfenster.
  - Das Fenster gruppiert sich in der Taskleiste unter der Verknüpfung.
- [ ] **B7 Hintergrundverläufe:** wie A13, besonders Größenänderung und
      Scrollen ohne Bildreste.
- [ ] **B8 Vorschauen:** JPEG, TIFF, BMP und SVG in der Galerie; HEIC und
      WebP nur mit den Microsoft-Erweiterungen.
- [ ] **B9 Ziehen aus dem Explorer** in Seite und Galerie.
- [ ] **B10 Systemmitteilung:** Mit der ersten Mitteilung erscheint das
      Glide-Symbol im Infobereich; ein Klick holt Glide nach vorn.
- [ ] **B11 Druck und PDF** wie A9.
- [ ] **B12 Beenden mit Alt+F4:** Der nächste Start öffnet in derselben
      Größe und Lage.
- [ ] **B13 Anhänge an Aufgaben:** Eine Datei mit Umlaut und Leerzeichen im
      Namen, auch eine nur online verfügbare OneDrive-Datei, über den
      Detailbereich anhängen.
  - Glide kopiert sie in die Testablage (`attachments`); Doppelklick öffnet
    sie im zugeordneten Programm (`os.startfile`).
  - Die Listenanzeige „Anhänge“ zeigt Name und Größe.
  - Komplettbackup in einer zweiten Testablage einlesen: Der Anhang ist da und
    öffnet sich.

## C. Bildschirmleser und Tastatur (VoiceOver bzw. NVDA)

- [ ] **C1** Seitenleiste, Suche, Detailbereich und Anpassen-Modus der
      Startseite sind erreichbar und werden sinnvoll angesagt.
- [ ] **C2 Zeichenfläche:**
  - Mit Tab bis zur Fläche; der gestrichelte Zellcursor ist sichtbar.
  - Die Statuszeile wird angesagt.
  - Pfeiltasten, Leertaste und die Werkzeugtasten wirken.
- [ ] **C3** Bilder in Seiten sind als Fläche erreichbar; der Text liest sich
      ohne Ankerzeichen.

## D. Linux (falls vorhanden)

- [ ] **D1** Design „Pixel“ zeigt die Pixelschrift, ohne dass sie installiert
      ist (Fontconfig).
- [ ] **D2** Vorschauen PNG, GIF und SVG; Logo und Lupe erscheinen.
- [ ] **D3 JPEG-Vorschau (N08, 3.34.0):** mit installiertem `gdk-pixbuf-thumbnailer` bzw. `djpeg` erscheinen JPEG-Bilder in Galerie und Seite, ohne Werkzeug der Platzhalter mit Endung; Referenzbild aus JPEG in der Zeichnung.
- [ ] **D4 Automatisch hell/dunkel (3.33.21)** über `gsettings` bzw. Portal.

## E. Nur durch den Inhaber

- Signatur, Notarisierung und Installer.
- Markenprüfung.
- Store-Freigabe.
