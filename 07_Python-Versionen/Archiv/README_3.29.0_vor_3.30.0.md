# Aktuelle startbare Python-Fassung

Glide 3.29.0 · Entwicklungsstand 24.09.2026 · Aufgabenformat 19 · Vorlagenformat 2

[Glide-Aufgaben-und-Listen_v3.29.0.pyw](Glide-Aufgaben-und-Listen_v3.29.0.pyw)
ist die bytegleiche Arbeitskopie des kanonischen Codes. Seit 3.29.0 gehören
[`drawing.py`](drawing.py) und [`drawing_image.py`](drawing_image.py) als
bytegleiche Module in denselben Ordner; ohne sie startet die Anwendung nicht.
Der vollständige Nachbarordner `resources` gehört ebenfalls dazu. Mit einem Tk-fähigen Python starten;
eine laufende ältere Instanz vorher schließen.

Neu in 3.29: Zeichnungsseiten als eigene Listenart mit eingebetteter
128-×-128-Fläche, Autosave, PNG-Referenz und Nachzeichnung. Aufgabenformat 19
legt beim ersten Speichern eines älteren Bestands die unveränderte Sicherung
`liste_vor_format19_<Zeitstempel>.json` an; Glide 3.28 kann den gespeicherten
Bestand danach nicht mehr öffnen.

Seit 3.28 gibt es Tagebuch-Ordner und datierte Notizseiten mit Favorit, Stimmung, Ort,
Schreibimpulsen, Suche und Vorlagen. Gismo besitzt pflegbare Zustände, die
Pinnwandvorschau ist informativer, schmale Fenster priorisieren Kernaktionen,
und gedrücktes Mausrad plus Zeigerbewegung scrollt kontinuierlich.

Nach `Füttern`, `Spielen` oder `Ruhen` aktualisiert Gismo nur noch seine drei
Pflegebalken und den eigenen Zeichenzustand. Der besonders im Dopamin-Design
sichtbare vollständige Startseiten-Neuaufbau entfällt.

Aufgabenformat 18 ergänzt Tagebuch-Metadaten und erzeugt vor der ersten
Migration eine unveränderte Rückfallkopie. Benachrichtigungen funktionieren
weiterhin nur bei laufender App. Vorherige startbare Fassungen liegen im
Unterordner `Archiv`, darunter 3.28.0; 3.27.0 ist dort als undokumentierter
UI-/UX-Zwischenstand erhalten.

[Zeichnungsseite 3.29](../01_Repository/Glide/docs/65_ZEICHNUNGSSEITE_3.29.0.md) ·
[Tagebuch und UI 3.28](../01_Repository/Glide/docs/59_TAGEBUCH_UND_UI_3.28.0.md) ·
[Prüfstand](../01_Repository/Glide/docs/07_QA_BERICHT.md) ·
[Dokumentationsindex](../01_Repository/Glide/docs/00_INDEX.md)
