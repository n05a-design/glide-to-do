# Aktiver Showcase und Testdatenpflege

Stand 01.10.2026 · Glide 3.32.3 · Aufgabenformat 20

Der Inhaber hat einen vollständigen, bearbeitbaren Showcase bestehender Funktionen beauftragt und die Motive unter `20_Grafik_Master/06_Beispielbilder` bereitgestellt. Die Umsetzung ergänzt Daten, Generator, Starter und Pflichtprüfung. Anwendung, Datenformat, Gestaltung und Startfassungen bleiben unverändert. Die offene Richtungsauswahl autorisiert dadurch keine zusätzlichen Produktfunktionen.

## Gelieferter Bestand

Zehn zusammenhängende Projektdokumente im fiktiven Parkquartier, vier Ordner einschließlich Bibliothek, Notizbuch und archivierter Vorbereitung. Das Teilbackup enthält 26 Punkte, das App-Backup 28 Punkte einschließlich zweier Eingangspunkte. Sechs Originalmotive werden in einer beschrifteten Galerie gezeigt; drei erscheinen über den wirklichen Seiteneditor im Briefing, mittig/links/rechts. Insgesamt 15 Anhangdateien, darunter JPEG, PNG, ICO, GPL, HEX, CSV und TXT. Auch Aufgabe, Liste und Ordner tragen Anhänge.

Zwei Projektpinnwände zeigen freie Karten/Verbindungen/Bereich und Spalten nach Bearbeitungstag. Die App-Variante ergänzt eine globale Pinnwand, Startseiteninhalt, Favoriten, angeheftete Dokumente, einen gespeicherten Freigabefilter und 22 Vorlagen einschließlich zweier zusätzlicher portabler Beispiele. Das Protokolltemplate füllt Wochentag/KW automatisch und fragt das Projekt ab; Aufgaben und Bildanhang bleiben erhalten.

Der [Showcase-Starter](../../../05_Probelisten_Testdaten/Showcase/Showcase_starten.pyw) lädt die Basis einmalig in `Showcase/Arbeitsstand`. Weitere Starts behalten Bearbeitungen. Die persönliche Glide-Ablage wird nicht verwendet. Die [Nutzeranleitung](../../../05_Probelisten_Testdaten/Showcase/README.md) beschreibt auch Hinzufügen per Teilbackup und den Ersatzcharakter eines App-Restores.

Die bestehende Funktionsvorschau wurde mit dem unveränderten Erzeuger auf **01.10.2026** aktualisiert. Sie bleibt der breitere Spezialbestand mit 170 Punkten, sieben Farben, Papierkorb- und Kalenderfällen. Der einfache Rundgang mit Fensteraufnahmen vom 27.09.2026 und die historische Releaseplanung bleiben erhalten. Aktuelle Backups verschieben konkrete Termine beim Einlesen nicht automatisch.

## Funktionsabdeckung

| Familie | Sichtbares Arbeitsbeispiel | Prüfung |
|---|---|---|
| Dokumentarten | Umsetzungsliste, Protokollnotiz, Briefingseite, Galerie, Pixelskizze | Alle fünf Arten tatsächlich öffnen; vollständiger Import und Neustart |
| Ordner und Navigation | Standardprojekt, Bibliothek, Notizbuch, Archiv, angeheftetes Briefing | Arten/IDs, Ansichtswechsel und Archivdatum; allgemeine Bedienwege in Pflichtsuiten |
| Aufgabenstruktur | Aufgabe, Long-Task, Überschrift, Gruppe/Unterpunkte, Checkliste | Referenzintegrität, echte Statusaktion und Undo; Checklisten/Wiederholungen in Pflichtsuiten |
| Planung und Zeit | Bearbeitungstag, Fälligkeit, Uhrzeit, Aufwand, erfasste Zeit, überfällige Aufgabe | Beide Datumsfelder unabhängig; aktuelle Tagesabschlusswarteschlange; Datumsaktionen in Pflichtsuiten |
| Wiedervorlagen | Sechs Wiederholungsarten, relative und feste Erinnerung, Routinecheckliste | Vollständigkeit der Regeln; Kalender-/Erinnerungsrundlauf in vorhandenen Suiten |
| Beziehungen | Steckbrief → Entwurf → Freigabe; Links und Wartebeziehung | IDs nach Hinzufügen, Vollrestore und Neustart gültig |
| Bilder und Anhänge | Sechs Originalmotive, Bildunterschriften, drei Bildmodi, Aufgabe/Liste/Ordner | ZIP-CRC, Schema/Pfade, tatsächliche native Vorschauen auf macOS, portable Vorlagenanhänge |
| Seitenformatierung | Überschriften, Listen, Nummern, Zitat, Codeblock, Aufgaben und geschlossener Klappblock | Echt öffnen/schließen und Zustand speichern; allgemeine Klappbindungen in `test_klappmechanismen3321` |
| Pinnwände | Freie Projektfläche, Spalten nach Bearbeitungstag, globale Auswahl | Karten, Zeichnungsverweis, Bereiche/Verbindungen und Remapping; Boardaktionen in Pflichtsuiten |
| Pixel-Werkstatt | 32 × 32 Dokument, 16 × 16 Symbol, PNG-Referenz und ICO | Zellmodell, Ansicht und Anhänge; tatsächlicher ICO-/Palettenexport in `test_etappe1_332` |
| Vorlagen und Tagesabschluss | Datumsplatzhalter, Projektabfrage, Notiz mit Aufgaben/Anhang, Wochenstart und Tagebuch | Vorlage wirklich anlegen; ausschließlich Projekt abfragen; Tagesabschluss öffnen; G03/G11 in Etappensuite |
| Klappen, Drag-and-drop, Performance | Realer Dokumentbestand als zusätzliche Abnahmegrundlage | Bestehende Pflichtsuiten 3.32.1/3.32.2/3.32.3; Bilderbestand für künftiges P04-Profiling verwendbar |
| Austausch und Wiederanlauf | Teilbackup, App-Backup, portabler Vorlagenkatalog und Datei-Anhänge | Tatsächlicher Hinzufüge-/Restorepfad, Export und separater Neustartprozess; CSV/ICS/Markdown/Druckaufbereitung in bestehenden Suiten |

Ein Datensatz kann Bedienhandlungen, Betriebssystemzustände oder Fehlerfälle nicht vollständig speichern. Deshalb ergänzen ausführbare Kontrollen die Beispiele. Es werden keine noch geplanten Funktionen als vorhanden dargestellt: allgemeine Typkonvertierung, Aufgaben direkt im Notiztext, GIF-Animation, Mobile und offene Richtungen bleiben außerhalb dieses Bestands. D01–D08 und die fortlaufende Performance-Abschlussaufgabe gelten weiter.

## Erzeugen, Prüfen, Ausliefern

- [showcase.py](../tests/tools/showcase.py) verwendet temporäres `GLIDE_DATA_DIR`, echte Objekt-/Anhang-/Seiten-/Vorlagen-APIs und einen frei wählbaren Datumsanker (`--tag YYYY-MM-DD`).
- [Quellenmanifest](../tests/fixtures/showcase/quellen.json) belegt sechs unveränderte Originaldateien; die Grafikmaster wurden nicht bearbeitet. Die Fixture hält lokale Kopien für spätere Erzeugung vor.
- [pruefe_showcase.py](../tests/tools/pruefe_showcase.py) ist zusätzlich zu 58 Integrationssuiten in beiden Prüfmodi verpflichtend. SHA-256, ZIP, Schema, Hinzufügen mit Erhalt vorhandener Daten, App-Restore, IDs/Anhänge, Ansichten, Bildvorschauen, Klappblock, Status-Undo, Vorlagen, Export und Neustart werden tatsächlich geprüft. Jede Tk-Callbackexception beendet die Abnahme negativ.
- [showcase_abgleich.py](../scripts/pflege/showcase_abgleich.py) prüft vor der Auslieferung, sichert ersetzte Basisdateien und vergleicht die sechs Nutzerkopien per SHA-256. Der bearbeitete Arbeitsstand wird nicht verändert.
- `versionswechsel.py` archiviert und erzeugt die Showcase-Basis mit. Nach der Vollprüfung den Datenabgleich zusätzlich ausführen. Jede neue implementierte Funktion bekommt ein geeignetes Beispiel oder eine ausführbare Bedienprüfung.

## Nachweise und Grenzen

[Vorsicherungen](../tests/qa-3.32.3/showcase_2026-10-01/vorsicherung.json), [gezielte Showcase-Abnahme](../tests/qa-3.32.3/showcase_2026-10-01/einzelpruefung.json), acht Aufnahmen ausschließlich des eigenen Glide-Fensters unter `tests/qa-3.32.3/showcase_2026-10-01/ansichten`. Briefing, Galerie, Projektboard und Startseite wurden angesehen. Die Schlussregression und der Auslieferungsabgleich werden separat protokolliert.

Physische Maus/Trackpad, OS-Fokus/Druckdialog, Windows/Linux, DPI/Mehrmonitor und Screenreader bleiben manuell offen. Das Entwicklungsbundle bleibt ad hoc signiert. Dieser Daten-/Werkzeugnachlauf ist keine Storefreigabe und kein neuer Performancenachweis.
