# Manuelle Prüfung – Glide 2.6.0

Diese Liste deckt genau das ab, was **nicht** automatisiert geprüft wird. Der
Integrationstest übernimmt Datenmodell, Migration, Backup, Menüaufbau,
Geometrie und Anhangslogik; hier geht es um Sicht, Eingabegeräte, Plattform
und reale Daten.

Vorbereitung: `GLIDE_DATA_DIR` auf einen leeren Ordner setzen oder vorher ein
Komplettbackup der eigenen Daten anlegen. Testbestand aus
`05_Probelisten_Testdaten/probelisten_2.6.0_komplettbackup.glidebackup` laden.

## Gruppen

- [ ] Punkt per Rechtsklick in eine Gruppe umwandeln und zurückwandeln.
- [ ] Mehrere Punkte markieren und über „Auswahl gruppieren“ zusammenfassen.
- [ ] Gruppe auflösen; die Unterpunkte stehen danach an ihrer Stelle.
- [ ] Gruppe mit Leertaste und Doppelklick auf- und zuklappen.
- [ ] Gruppe per Drag & Drop verschieben, einrücken, in eine andere Gruppe ziehen.
- [ ] Gruppe in eine andere Liste verschieben.
- [ ] Fortschrittsanzeige zählt die Gruppe nicht mit.
- [ ] Seitenleistenzähler der Liste zählt die Gruppe nicht mit.
- [ ] Gruppe erscheint nicht in „In Bearbeitung“, ihre datierten Unterpunkte schon.
- [ ] Filter „Nur offene Punkte“: Gruppe bleibt sichtbar, solange ein offener Unterpunkt existiert.
- [ ] Gruppe mit Beschreibungstext, Anhang und Farbe versehen.
- [ ] Gruppe exportieren nach TXT, Datei wieder importieren, Gruppe bleibt Gruppe.

## Kontextmenüs

Jedes Menü einmal öffnen und **jeden** Eintrag ausführen:

- [ ] Aufgabe im Aufgabenbaum
- [ ] Gruppe im Aufgabenbaum – gesperrte Einträge dürfen nicht auslösen
- [ ] Mehrfachauswahl aus Aufgaben und Gruppen
- [ ] leerer Bereich der Liste
- [ ] Liste in der Seitenleiste
- [ ] Eingang in der Seitenleiste – Umbenennen und Entfernen bleiben gesperrt
- [ ] „In Bearbeitung“ in der Seitenleiste
- [ ] Ordner in der Seitenleiste
- [ ] Zeile in der Ordnerübersicht
- [ ] leerer Bereich der Ordnerübersicht
- [ ] Zeile in „In Bearbeitung“ – Änderung wirkt auf die Quellliste
- [ ] Escape und Klick daneben schließen jedes Menü, ohne Daten zu ändern

## Darstellung

- [ ] Hauptüberschrift erscheint unter Windows in „Segoe UI Black“, nicht im normalen Fett.
- [ ] Hell- und Dunkelmodus: Gruppen, Farben, Marker, Trennlinie, Menüs.
- [ ] Sehr langer Listentitel: Überschrift kürzt mit `…`, Design-Umschalter und Fortschrittszeile bleiben sichtbar.
- [ ] Fenster auf Mindestgröße 860 × 700: alle Aktionsreihen bleiben erreichbar.
- [ ] Fenster auf einem zweiten Monitor positionieren, Monitor abmelden, neu starten: Fenster ist sichtbar.
- [ ] DPI-Skalierung 125 % und 150 % unter Windows.
- [ ] Emoji-Marker (Ordner, Fahnen, Kalender, Büroklammer) werden auf allen Testsystemen dargestellt.

## Eingabe und Plattform

- [ ] Alle Tastenkürzel unter Windows mit NumLock an und aus.
- [ ] Alle Tastenkürzel mit CapsLock an und aus.
- [ ] macOS: Cmd+Q bei ungespeicherten Änderungen fragt nach.
- [ ] macOS: Rückschritt löscht den ausgewählten Punkt, nicht im Eingabefeld.
- [ ] macOS: Command-Kürzel für Speichern, Export, Import, Design, neue Liste, Gruppieren.
- [ ] macOS: Menü- und Hilfetexte zeigen „Cmd“, nicht „Strg“.
- [ ] macOS: Dateidialog im Punktdetails-Dialog öffnen und schließen; der Dialog bleibt danach bedienbar.
- [ ] Rechtsklick über Zweifingertipp und über Ctrl+Klick auf dem Mac.
- [ ] Mausrad in Seitenleiste und Aufgabenbaum.

## Daten

- [ ] Komplettbackup mit realen Daten erstellen und in einen leeren Datenordner zurückspielen.
- [ ] Bestand aus Format 5 laden: alle Punkte erscheinen als Aufgaben.
- [ ] Bestand aus Format 2 laden (Legacy-Probeliste).
- [ ] Anhang hinzufügen, öffnen, entfernen; Quelldatei danach löschen, Anhang bleibt nutzbar.
- [ ] Anhang mit ungewöhnlichem Dateinamen testen, etwa `Notiz.` oder `daten.jsön`.
- [ ] Große Liste mit mehreren hundert Punkten: Scrollen, Suche, Filter, Rückgängig.
- [ ] Export nach TXT, Markdown und CSV; CSV in Excel öffnen, Spalte „Art“ prüfen.

## Nach dem Build

- [ ] Start ohne installiertes Python auf einer Clean Machine.
- [ ] Silent-Installation und Silent-Uninstall unter Windows.
- [ ] Nutzerdaten überleben eine Neuinstallation.
- [ ] macOS: Gatekeeper akzeptiert die notarisierte App.
