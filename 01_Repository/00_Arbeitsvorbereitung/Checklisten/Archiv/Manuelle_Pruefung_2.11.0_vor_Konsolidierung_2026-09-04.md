# Manuelle Prüfung 2.11.0

Stand: 03.09.2026 · App-Version 2.11.0 · Datenformat 10

Diese Liste enthält **ausschließlich**, was die automatisierten Läufe nicht
abdecken können. Was sie abdecken, steht in
`01_Repository/Glide/docs/07_QA_BERICHT.md`; dort steht auch, warum die Punkte
hier offen bleiben müssen.

Vor jedem Durchgang: einen eigenen Datenordner setzen, damit nichts Echtes
angefasst wird.

```powershell
$env:GLIDE_DATA_DIR = "$env:USERPROFILE\Glide-Probe"
pythonw "07_Python-Versionen\Glide-Aufgaben-und-Listen_v2.11.0.pyw"
```

Als Datengrundlage eignet sich `05_Probelisten_Testdaten\Glide-Funktionsvorschau.glidebackup`.
Die Liste **„00 Was Glide kann“** darin zeigt jede Art, jede Wichtigkeit, jede
der sieben Farben und jeden Fälligkeitszustand genau einmal – ideal für die
Sichtprüfung. Neu in der Vorschau: elf Termine mit Uhrzeit und ein gelöschter
Punkt im Papierkorb.

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
- [ ] Wichtigkeitsmarker (⚐ ⚑ 🚩), 📝 und 📎 werden dargestellt und nicht als
      leere Kästen

## 2 Darstellung macOS

- [ ] Retina: keine unscharfen Kanten an Chips und Schaltflächen
- [ ] Hell und Dunkel folgen der Systemeinstellung
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

## 3a Neu in 2.11.0 – mit Vorrang prüfen

Diese Punkte sind neu und lassen sich unter Linux/Tk nicht abschließend prüfen.
Der erste Block hat Vorrang: Er betrifft die Bedienung, die in dieser Runde
umgestellt wurde.

### Mehrfachauswahl und Kontextmenü

- [ ] **Windows/Linux:** Strg+Klick wählt einen Punkt zur Auswahl dazu und beim
      erneuten Klick wieder ab
- [ ] **Windows/Linux:** Rechtsklick öffnet weiterhin das Kontextmenü, an Punkt,
      Liste und Ordner
- [ ] **Windows/Linux:** Strg+Klick öffnet **kein** Kontextmenü mehr
- [ ] **macOS:** Cmd+Klick wählt mehrfach aus
- [ ] **macOS:** Strg+Klick öffnet weiterhin das Kontextmenü
- [ ] Shift+Klick wählt weiterhin einen Bereich
- [ ] Die Hinweiszeile unter der Liste nennt die richtige Taste (Strg bzw. Cmd)

### Papierkorb für einzelne Punkte

- [ ] Punkt löschen → liegt im Papierkorb, mit Art und Herkunftsliste in der Zeile
- [ ] Punkt mit Unterpunkten löschen → alle Unterpunkte sind im Eintrag enthalten
- [ ] Wiederherstellen setzt ihn **an dieselbe Stelle** zurück, nicht ans Ende
- [ ] App schließen und neu starten → der Eintrag steht noch im Papierkorb
- [ ] Punkt mit Anhang löschen, Komplettbackup schreiben, zurücklesen → Anhang da
- [ ] Herkunftsliste vorher löschen → der Punkt kommt trotzdem zurück

### Eingabemaske, Kalender, Uhrzeit

- [ ] „Erweitert“ neben „Hinzufügen“ öffnet die vollständige Maske
- [ ] Was in der Schnelleingabe steht, ist im Titelfeld vorbelegt
- [ ] Schnelleingabe funktioniert unverändert: tippen, Enter, fertig
- [ ] Anlegen und Bearbeiten zeigen **dieselben** Felder
- [ ] Kalender: Blättern, heutiger Tag hervorgehoben, ausgewählter Tag lila
- [ ] Tag anklicken schreibt ins Datumsfeld; Datum tippen springt in den Monat
- [ ] „Heute“, „Morgen“ und „Keine Fälligkeit“ wirken
- [ ] Uhrzeit eintragen → erscheint in der Liste hinter dem Datum
- [ ] Fälligkeit entfernen → die Uhrzeit verschwindet mit
- [ ] Unlesbare Uhrzeit („25:99“) → Meldung, Fenster bleibt offen
- [ ] Anhang schon beim Anlegen mitgeben
- [ ] Labelauswahl zeigt rund fünf Zeilen und scrollt darüber hinaus
- [ ] Auf einem kleinen Bildschirm (etwa 1366 × 768): Die Maske bleibt
      vollständig sichtbar und scrollt; „Anlegen“ ist erreichbar
- [ ] Doppelklick auf einen Kalendertag öffnet dieselbe Maske mit gesetztem Datum
- [ ] Menü „Fälligkeit → Datum wählen“ zeigt Kalender **und** Uhrzeit

### Datenintegrität

- [ ] Punkte gruppieren und wieder auflösen → alle Punkte sind da, in der
      richtigen Reihenfolge, auch die aus der Mitte
- [ ] Gruppe mit Unterpunkten auflösen → Unterpunkte bleiben sichtbar, nicht
      hinter einem Klapppfeil
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
