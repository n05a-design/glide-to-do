# Manuelle Prüfung 3.3.0

Stand: 04.09.2026 · App-Version 3.3.0 · Datenformat 10

Diese Liste enthält **ausschließlich**, was die automatisierten Läufe nicht
abdecken können. Was sie abdecken, steht in
`01_Repository/Glide/docs/07_QA_BERICHT.md`; dort steht auch, warum die Punkte
hier offen bleiben müssen.

Vor jedem Durchgang: einen eigenen Datenordner setzen, damit nichts Echtes
angefasst wird.

```powershell
$env:GLIDE_DATA_DIR = "$env:USERPROFILE\Glide-Probe"
pythonw "07_Python-Versionen\Glide-Aufgaben-und-Listen_v3.2.0.pyw"
```

Als Datengrundlage eignet sich
`05_Probelisten_Testdaten\Glide-Funktionsvorschau_3.2.0.glidebackup`: zehn Listen
in fünf teils verschachtelten Ordnern, 140 Punkte über alle vier Arten, neun
Labels über alle sieben Palettenfarben, überfällige und künftige Fristen, drei
Papierkorbeinträge. **Ein Komplettbackup ersetzt den vorhandenen Bestand** –
deshalb vorher den eigenen Datenordner setzen (siehe oben).

Die ältere `Glide-Funktionsvorschau.glidebackup` liegt im `Archiv`; ihre Liste
„00 Was Glide kann“ zeigt jede Art, Wichtigkeit, Farbe und jeden
Fälligkeitszustand genau einmal und eignet sich weiterhin für eine schnelle
Sichtprüfung.

---

## 1 Darstellung Windows

- [ ] Skalierung 100 %: Schriftgrößen, Zeilenhöhen, Abstände stimmig
- [ ] Skalierung 125 %: nichts abgeschnitten, keine überlappenden Beschriftungen
- [ ] Skalierung 150 %: Dialogschaltflächen bleiben vollständig sichtbar
- [ ] Zwei Monitore mit unterschiedlicher Skalierung: Fenster wechseln
- [ ] Dunkle Titelleiste erscheint im Dunkelmodus, auch nach dem Umschalten
- [ ] Fenster startet auf dem sichtbaren Bildschirm, auch nach Monitorwechsel
- [ ] **Label-Chips:** Fläche und Text in allen sieben Farben lesbar, Radius
      wirkt rund, Chips brechen bei schmalem Fenster um
- [ ] **Symbole aus `ICONS` (neu in 3.2.0, Textzeichen):** ↓ ◐ ‼ × ◈ ▦ ⊕ ☾ ☀
      werden dargestellt und **nicht als leere Kästen** – das ist der Kernpunkt
      der Umstellung und unter Linux nicht abschließend prüfbar
- [ ] Das Fälligkeitssymbol ▦ nimmt bei einem überfälligen Punkt die Warnfarbe an
- [ ] Das Labelsymbol ◈ steht in der Farbe seines Labels
- [ ] Wichtigkeitsmarker (⚐ ⚑ 🚩) und der Gruppenmarker 📁 werden dargestellt.
      **Gruppenmarker und höchste Wichtigkeitsstufe verwenden noch Emoji** – wenn sie als leere Kästen erscheinen
      oder die Zeilenhöhe sprengen, ist das der Beleg dafür, dass sie ebenfalls
      auf Textzeichen umgestellt werden müssen

## 2 Darstellung macOS

- [ ] Retina: keine unscharfen Kanten an Chips und Schaltflächen
- [ ] Hell und Dunkel über den Themenschalter wechseln; automatisches Folgen der Systemeinstellung nicht als zugesicherte Funktion voraussetzen
- [ ] Menüleiste und Fenstertitel korrekt beschriftet
- [ ] **Label-Chips** wie oben

## 3 Eingabe und Bedienung

- [ ] Drag & Drop mit der Maus: Liste in Ordner, Ordner in Ordner (obere Kante
      sortiert, Mitte legt hinein, untere Kante sortiert)
- [ ] Drag & Drop mit dem Trackpad: dieselben Wege
- [ ] Aufgabe auf eine Seitenleisten-Liste ziehen
- [ ] Shift + Drag erzeugt einen Unterpunkt
- [ ] Pfeiltasten überspringen die Fortsetzungszeilen eines Long-Tasks
- [ ] Alt+↑/↓ verschiebt, Alt+←/→ rückt aus und ein
- [ ] Entf in der Seitenleiste, Rückschritt unter macOS
- [ ] Mausrad in allen Dialogfeldern: Titel, Beschreibung, Anhänge, Labellisten
- [ ] Tastaturbedienung ohne Maus: Anlegen, Bearbeiten, Verschieben, Löschen

## 3b Neu in 3.3.0 – zuerst prüfen

Die Ansicht „Labels“, die Chipdarstellung und die Spaltenbreiten sind neu
beziehungsweise umgestellt. Sie liefen bisher **ausschließlich unter Linux/Xvfb**.
Alles hier ist auf Windows und macOS ungeprüft.

### Ansicht „Labels“ – Aufbau

- [ ] Die Zeile steht in der Seitenleiste zwischen „In Bearbeitung“ und „Verspätet“ und trägt das Symbol `◈`.
- [ ] Der Zähler nennt die Punkte mit mindestens einem eigenen Label; ein Punkt mit drei Labels wird **einmal** gezählt.
- [ ] Je Label eine Gruppe, in der Reihenfolge der Labelverwaltung, „Ohne Label“ als letzte Gruppe.
- [ ] „Long-Task“ und „Überschrift“ bilden **keine** Gruppe.
- [ ] Gruppenzeile und Punkte stehen in der Farbe des Labels; im Dunkelmodus ebenfalls lesbar.
- [ ] Ein Punkt mit mehreren Labels erscheint in jeder zugehörigen Gruppe.
- [ ] Die Labelspalte rechts zeigt die **übrigen** Labels, nicht das der Gruppe.
- [ ] Doppelklick und Enter öffnen den Punkt in seiner Quellliste.
- [ ] Rechtsklick bietet dieselben Aktionen wie in „In Bearbeitung“.
- [ ] Suche und der Filter „Nur offene Punkte“ wirken auch hier.

### Ansicht „Labels“ – Ziehen (der kritische Teil)

Mit **realer Maus** prüfen, nicht nur mit kurzem Klick-Ziehen:

- [ ] Punkt von Gruppe A nach B ziehen: A verschwindet aus seinen Labels, B kommt hinzu, **alle übrigen Labels bleiben unverändert**.
- [ ] Das neue Label steht an derselben Position wie das alte – in der Listenansicht bleibt dasselbe Label als erstes sichtbar.
- [ ] Punkt aus „Ohne Label“ in eine Gruppe ziehen: Label wird vergeben.
- [ ] Punkt in „Ohne Label“ ziehen: **nur** das Label der Herkunftsgruppe verschwindet, andere bleiben.
- [ ] Zug in die eigene Gruppe bewirkt nichts.
- [ ] Punkt mit 20 Labels in eine weitere Gruppe ziehen: Hinweisfenster, **keine** Änderung, nichts wird abgeschnitten.
- [ ] Beim Überfahren wird die Zielgruppe hervorgehoben.
- [ ] Nach dem Zug steht die Auswahl auf der Zeile in der neuen Gruppe.
- [ ] Strg+Z (macOS: Cmd+Z) nimmt den Zug vollständig zurück, **und die Ansicht bleibt die Labelansicht**.
- [ ] Nach dem Zurücknehmen stimmen Zähler und Gruppengrößen wieder.

### Labelchips

- [ ] Chips sind an allen vier Seiten vollständig gerundet, nichts wirkt abgeschnitten – im Label-Manager, im Kopfbereich und in der Labelauswahl.
- [ ] Bei 100 %, 125 % und 150 % Anzeigeskalierung (Windows) sowie auf einem Retina-Display (macOS) prüfen.
- [ ] Der Auswahlrahmen in der Labelauswahl folgt der Rundung.

### Spalten in der Liste

- [ ] Kalendersymbol `▦` und Labelsymbol `◈` stehen in allen Zeilen an derselben Stelle – nichts wandert von Zeile zu Zeile.
- [ ] Liste ohne Fälligkeiten: keine leere Fälligkeitsspalte.
- [ ] Liste mit Datum **und** Uhrzeit: nichts wird abgeschnitten.
- [ ] Langer Labelname (14 Zeichen und mehr) plus Zähler „+n“: vollständig lesbar.
- [ ] Fenster schmaler ziehen: erst weichen die Labels, dann die Fälligkeit; der Aufgabentext bekommt den Platz.
- [ ] Fenster wieder breiter ziehen: beide Spalten kommen korrekt zurück.
- [ ] Zwischen Listen wechseln: die Spaltenbreite passt sich an, ohne dass die Zeilen flackern.

## 3a Neu seit 2.11.0 – mit Vorrang prüfen

Diese Punkte sind neu oder wurden umgestellt und lassen sich unter Linux/Tk
nicht abschließend prüfen. Die ersten beiden Blöcke haben Vorrang.

### Das gemeldete Einfrieren (3.0.1, Griffrückgabe seit 3.1.0 überarbeitet)

**Der wichtigste Punkt dieser Runde.** Die Griffrückgabe modaler Dialoge wurde
überarbeitet. Das ist eine Maßnahme gegen einen plausiblen Fehlerpfad.
**Reproduzieren ließ sich die gemeldete Störung nie**; die vollständige Behebung
ist NICHT VERIFIZIERT. Erforderlich sind reproduzierbare Dialogfolgen und Dauerbenutzung.

- [ ] Eingabemaske öffnen → darin die **Farbauswahl** eines Labels öffnen und
      schließen → die Maske nimmt weiterhin Eingaben an
- [ ] Eingabemaske öffnen → darin **„＋ Neues Label“** anlegen (Name und Farbe)
      → die Maske nimmt weiterhin Eingaben an
- [ ] Eingabemaske öffnen → **Kalender** über den Kalenderknopf öffnen und
      schließen → die Maske nimmt weiterhin Eingaben an
- [ ] Aus der Labelverwaltung heraus die Farbauswahl öffnen und schließen
- [ ] Aus dem Kalenderfenster heraus eine Aufgabe anlegen (Doppelklick auf einen
      Tag) → nach dem Schließen ist der Kalender weiterhin bedienbar
- [ ] „In Liste verschieben“ aus dem Kontextmenü, Dialog abbrechen → Hauptfenster
      reagiert
- [ ] Nach jedem dieser Wege: Hauptfenster anklicken, Menü öffnen, tippen
- [ ] **Dauerlauf:** die App eine längere Sitzung normal benutzen und darauf
      achten, ob ein Fenster stehen bleibt, das keine Eingabe mehr annimmt

### Symbole als Textzeichen (3.2.0)

Siehe Abschnitt 1 und 2. Zusätzlich:

- [ ] TXT-Export öffnen: Gruppenmarker 📁, Überschriftenmarker § und
      Long-Task-Marker » sind lesbar
- [ ] Diese TXT-Datei wieder importieren → Gruppen, Überschriften und Long-Tasks
      kommen als solche zurück

### Rückgängig (3.1.0)

- [ ] Eine Aktion ausführen, die **nichts** ändert – etwa dieselbe Farbe erneut
      setzen oder dieselbe Wichtigkeit – dann Strg+Z: Es muss der **davor**
      liegende echte Schritt zurückgenommen werden, nicht nichts
- [ ] Mehr als 20 Änderungen hintereinander, dann wiederholt Strg+Z: Es lassen
      sich 20 Schritte zurücknehmen

### Datenordner (3.2.0)

- [ ] Auf einem Rechner mit Daten unter einem früheren Programmnamen starten →
      Glide beginnt mit einer **leeren** Ablage und greift nicht mehr darauf zu
- [ ] Ein Komplettbackup einer älteren Fassung lässt sich weiterhin einlesen

### Mehrfachauswahl und Kontextmenü (2.11.0, weiterhin offen)

- [ ] **Windows/Linux:** Strg+Klick wählt einen Punkt zur Auswahl dazu und beim
      erneuten Klick wieder ab
- [ ] **Windows/Linux:** Rechtsklick öffnet weiterhin das Kontextmenü, an Punkt,
      Liste und Ordner
- [ ] **Windows/Linux:** Strg+Klick öffnet **kein** Kontextmenü mehr
- [ ] **macOS:** Cmd+Klick wählt mehrfach aus
- [ ] **macOS:** Strg+Klick öffnet weiterhin das Kontextmenü
- [ ] Shift+Klick wählt weiterhin einen Bereich
- [ ] Die Hinweiszeile unter der Liste nennt die richtige Taste (Strg bzw. Cmd)

### Umbenennen in der Seitenleiste (3.0.0)

- [ ] Klick auf eine **bereits ausgewählte** Liste öffnet nach kurzer Verzögerung
      das Eingabefeld
- [ ] Doppelklick öffnet **nicht** das Umbenennen, sondern die Liste
- [ ] Klick auf das **Klappdreieck** eines Ordners klappt nur auf und zu
- [ ] F2 und das Kontextmenü öffnen dasselbe Feld
- [ ] Leerer Name wird verworfen, der alte bleibt

### Papierkorb für einzelne Punkte (2.11.0, weiterhin offen)

- [ ] Punkt löschen → liegt im Papierkorb, mit Art und Herkunftsliste in der Zeile
- [ ] Punkt mit Unterpunkten löschen → alle Unterpunkte sind im Eintrag enthalten
- [ ] Wiederherstellen setzt ihn **an dieselbe Stelle** zurück, nicht ans Ende
- [ ] App schließen und neu starten → der Eintrag steht noch im Papierkorb
- [ ] Punkt mit Anhang löschen, Komplettbackup schreiben, zurücklesen → Anhang da
- [ ] Herkunftsliste vorher löschen → der Punkt kommt trotzdem zurück

### Eingabemaske, Kalender, Uhrzeit (2.11.0/2.12.0, weiterhin offen)

- [ ] „Erweitert“ neben „Hinzufügen“ öffnet die vollständige Maske
- [ ] Was in der Schnelleingabe steht, ist im Titelfeld vorbelegt
- [ ] Schnelleingabe funktioniert unverändert: tippen, Enter, fertig
- [ ] Anlegen und Bearbeiten zeigen **dieselben** Felder
- [ ] Labelauswahl ist ein **Aufklappfeld mit Mehrfachauswahl** (seit 2.12.0),
      keine Chipfläche
- [ ] Kalender öffnet als eigenes Fenster über den Kalenderknopf
- [ ] Tag anklicken schreibt ins Datumsfeld; Datum tippen springt in den Monat
- [ ] „Heute“, „Morgen“ und „Keine Fälligkeit“ wirken
- [ ] Uhrzeit eintragen → erscheint in der Liste hinter dem Datum
- [ ] Fälligkeit entfernen → die Uhrzeit verschwindet mit
- [ ] Unlesbare Uhrzeit („25:99“) → Meldung, Fenster bleibt offen
- [ ] Anhang schon beim Anlegen mitgeben
- [ ] Auf einem kleinen Bildschirm (etwa 1366 × 768): Die Maske bleibt
      vollständig sichtbar und scrollt; „Anlegen“ ist erreichbar
- [ ] Doppelklick auf einen Kalendertag öffnet dieselbe Maske mit gesetztem Datum
- [ ] Bei schmalem Fenster wird „Erweitert“ **ausgeblendet**, nicht gequetscht

### Datenintegrität (2.11.0, weiterhin offen)

- [ ] Punkte gruppieren und wieder auflösen → alle Punkte sind da, in der
      richtigen Reihenfolge, auch die aus der Mitte
- [ ] Gruppe mit Unterpunkten auflösen → Unterpunkte bleiben sichtbar, nicht
      hinter einem Klapppfeil
- [ ] Punkt auf die **Mitte** einer Gruppenzeile ziehen → er landet **in** der
      Gruppe; oberer und unterer Rand sortieren daneben (seit 3.0.2)
- [ ] Mehrere Punkte markieren und ziehen → **alle** bewegen sich mit
- [ ] Auswahl auf eine Seitenleisten-Liste ziehen → Rückfrage erscheint, nennt
      Ziel und Anzahl
- [ ] Diese Rückfrage ablehnen → nichts ändert sich
- [ ] Strg+Z nach jedem dieser Schritte stellt den vorherigen Stand her

## 4 Plattformdialoge

- [ ] Datei anhängen über den nativen Dateidialog
- [ ] Anhang mit Umlauten und Leerzeichen im Namen
- [ ] Anhang öffnen startet das zugeordnete Programm
- [ ] Export nach TXT, Markdown, CSV: Speicherort wählbar, Datei lesbar
- [ ] Komplettbackup speichern und wieder laden
- [ ] Cmd+Q unter macOS geht über die Speicherabfrage

## 5 Reale Daten

- [ ] Kopie des echten Datenordners über `GLIDE_DATA_DIR` laden
- [ ] Alle Listen, Ordner und Punkte vollständig vorhanden
- [ ] Speichern, Backup, Import, Wiederherstellen durchspielen
- [ ] Automatische Sicherungen entstehen, Rotation greift
- [ ] Nach dem Durchgang: Original unverändert (Zeitstempel prüfen)

## 6 Dauerlauf

- [ ] Anwendung mehrere Stunden offen lassen, Autosave beobachten
- [ ] Bestand mit über 1 000 Aufgaben: Aufbau der Liste, Suche, Filter
- [ ] Fenster wiederholt sehr schmal und sehr breit ziehen
- [ ] Zwischen allen Ansichten wechseln, ohne dass die Auswahl verloren geht

## 7 Installation (sobald ein Build existiert)

- [ ] Installer auf einem Rechner **ohne Python** ausführen
- [ ] Silent-Installation `/SILENT`
- [ ] Upgrade über eine ältere Installation, Daten bleiben erhalten
- [ ] Deinstallation entfernt das Programm, **nicht** den Datenordner
- [ ] macOS: Gatekeeper beim ersten Start, Notarisierung greift

---

## Befundbogen

| Datum | Plattform | Punkt | Befund | Erledigt |
|---|---|---|---|---|
|  |  |  |  |  |


## Belegte Grenzbefunde vom 04.09.2026

Die deklarierten Grenzen sind nicht auf jedem Änderungspfad durchgesetzt:
`sync_item_kind_label` kann ein Systemlabel an 20 Nutzerlabels anhängen und
damit 21 erzeugen. `make_subitem` kann Tiefe 101 erzeugen; die spätere
Normalisierung lehnt diesen Bestand ab. Beide Fälle wurden isoliert reproduziert.
App-Code unverändert; gezielte Behebung und Regression vor Release offen.
Nachweise: `../../01_Repository/Glide/docs/11_BESTANDSANALYSE.md`.
