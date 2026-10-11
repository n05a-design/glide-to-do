# Aufgabenoberfläche – Liefernachweis 3.38.0

Stand 11.10.2026 · Glide 3.38.0 · Aufgabenformat 23 · Mac-Neuabnahme und Lieferabgleich grün, native Wiederholung offen

Paket 3 setzt S26-01/02/03/04/07/13 vollständig nach D22–D25/D31/D32 um.
Ausgangslieferung 3.37.0, Liefercommit `0e7b358`. Alle bisherigen Felder bleiben
im gemeinsamen Inspektor; kleine Fenster nutzen die Inhaltsfläche.
Aktueller App-SHA: `49ca48aad93d0be0ba9fce8dd0bd82e980e3eaa673ff549bdb3ba04614ebcf28`.

| Tor | Ergebnis |
|---|---|
| Gemeinsamer Inspektor | 22 gezielte Szenarien grün: sechs Kontexte, volle Felder, Schreibschutz, Konflikt, echter Dateischreibfehler/Retry, Auswahl, Checkliste, Wiederholung, Zustellbelege, modale Feldauswahl und Neustart |
| Direkte Felder | 30 Klickgruppen grün: vier Listenansichten, Pinnwand frei/geordnet/Spalten bei 75/150 %, Live-Listen, echter Dokumentdoppelklick; Modifier bleiben Auswahl |
| Fachlogik | 11 Dreiwege-/Feldkonflikttests und sieben Zeit-/Abbruchtests grün |
| Vorversion | vier getrennte passende Assertion-Gegenproben gegen unveränderte 3.37.0 rot |
| Beschädigte Kandidaten | vier Funktionsdefekte plus vier [Kalibrierdefekte](kalibriergegenproben.json) passend rot, positive Kontrollläufe grün; nächste native Wiederholung prüft insgesamt 17 Defektfälle |
| Bedienfläche | sechs echte Inhaltswidgets × drei Größen × zwei gültige Schriftstufen; [aktuelle Geometrie](bedienflaechenmessung.json) |
| Bewegung | aktueller Quellstand: 215 Abschlüsse/Abbrüche, maximal 114,55 ms; Fokus sofort, Abschaltung/Schließen räumen auf; [Nachmessung](plattformkorrektur.json) |
| Eigene Fensterbilder | sechs eigene NSView-Aufnahmen für Hell/Dunkel, große Schrift, Mindestgröße und Inspektor tatsächlich betrachtet; [Bildhashes und Befund](fenster-neustart.json); keine menschliche Abnahme |
| Fundamenttempo | aktueller Quellstand: Startseite kalt 267 ms, warm 74/82 ms Median/p95; Einstellungen zuerst 195 ms, warm 129/137 ms. D46/D47 eingehalten; [Nachmessung](plattformkorrektur.json) |
| Mac-Vollprüfung eingefroren | erneuter vollständiger Fensterfokuslauf Exit 0: 102 ausgeführt/zwei übersprungen, 85 Suiten/294 Unit-Tests; alle 862 Dateien nach Lauf unverändert; [Volllauf](mac-voll.json) |
| Native Linux-/Windows-Matrix | erster Lauf: Grundstufe grün, Linux drei Befunde, Windows gezielt abgebrochen; [Vorlauf](native-vorlauf.json). zweiter Lauf: Linux-Vollprüfung grün, Windows ein Prüfstandbefund; [Ergebnis](native-wiederholung.json). Zwei Werkzeuge gezielt korrigiert, [Nachlauf](../pruefstand_2026-10-11/README.md); erneute vollständige Matrix folgt |
| 07 und Showcase | 42 Code-/141 Ressourcen-/sechs Showcase-Dateien SHA-256-gleich; [Abgleich](lieferabgleich.json). Ausdrücklicher Fensterfokus des Showcase-Werkzeugs gezielt geprüft; [Werkzeugnachlauf](showcase-werkzeugnachlauf.json) |
| Mac-Entwicklungsbundle | 42 Code-/55 Plattformressourcen gleich Quelle; Ad-hoc-Signatur im Bauordner und auf Rückkopie grün; [Bundle](bundle.json) |
| Menschen-/DPI-/Mehrmonitorabnahme | getrennt offen |

Die Geometrie beginnt am oberen Fensterrand ohne Betriebssystem-Titelleiste
und endet am tatsächlichen Aufgabenbaum, Seitentitel bzw. Pinnwandcanvas.
Bei 1280 × 800 sind es in den vier Aufgabenansichten 117 px (14,625 %),
bei Seiten 116 px (14,5 %) und der Pinnwand 113 px (14,125 %).
1280 × 840 wird zusätzlich berichtet. Die Mindestgröße 860 × 700 hat
Lesbarkeit/Erreichbarkeit als Tor, nicht die 15-Prozent-Grenze.

Bestandsprüfungen behalten ihre Feld-, Abbruch-, Speicher- und Undo-Kriterien;
ungespeicherte neue Punkte prüfen die Anlegemaske, geänderte Aufgaben den
Inspektor. Wiederholungsanker/Zustellbeleg werden ohne Eingabe nicht geändert.
Schreibfehler der Checkliste erhalten Modell/Datei/Verlauf/Undo.
Rohprotokolle und Fensterbilder bleiben außerhalb OneDrive und Git.

Die ursprüngliche Ansichtserie am Apphash `5661381d…` zeigt neben schnellerer
Liste (267 → 146 ms Median) auch langsamere Bibliothek (408 → 470 ms)
und Notiz (262 → 380 ms). Die Notizverzögerung blieb ohne Animation;
der Python-Anteil lag bei rund 32/33 ms, zusätzliche Zeit überwiegend im
nativen Zeichnen. Kein separates absolutes Paket-3-Ziel für diese Wege;
der Performancebefund bleibt offen. Keine pauschale Beschleunigung behauptet.
Abhaken 1.000/5.000/10.000: 15,7/61,1/114,8 ms Median, Suche 66,4/73,1 ms
gehören ebenfalls zu diesem älteren Hash; [beide Reihen](tempo.json).
Notizen behalten ihre Leseschrift, Seiten nutzen die vier gewählten Stufen.

Historische Prüfstände bleiben mit ihrem jeweiligen Apphash erhalten:
Erster Freeze Exit 1, 848 Dateien unverändert ([Vorlauf](mac-vorlauf.json));
LabelDropdown-Objektzugriffe und isolierter Vorlageneditor danach korrigiert,
elf [Reparatursuiten](reparaturproben.json) grün. Die frühere grüne
852-Dateien-Vollprüfung steht vollständig in [Plattformkorrektur](plattformkorrektur.json).
Der native Erstlauf `e1e292f` meldete 121 px Seitenkante, einen abgeschnittenen
Erkennungschip und ein Fotowerkzeug am früheren Modalweg. Elf Defektfälle
passend rot, vier neue Fälle wegen roter positiver Basis nicht anerkannt.
Korrektur nutzt bestehenden ButtonFlow und entfernt zwei Pixel Außenabstand;
zwölf Foto-Einstiege grün, altes Werkzeug passend rot. Keine Grenzlockerung.

Nach Neustart verlorener temporärer Prüflauf ohne Ergebnis; neue Kopie am
aktuellen Hash: Hintergrundlauf 79 grün/23 rot/zwei übersprungen, 862 Dateien
unverändert. Synthetische Tastatureingaben erreichten ohne echten Fensterfokus
ihre Ziele nicht; eigener hängender Settings-Prozess als roter Abbruch beendet.
Unveränderte gezielte Fokusproben grün, anschließend die vollständige
Fensterfokusprüfung wiederholt und bestanden; [Diagnose](mac-hintergrund.json).
Ein eigener WindowServer-Fotoaufruf scheiterte; die oben belegten sechs Bilder
stammen aus dem eigenen NSView, alle sechs wurden tatsächlich betrachtet.

Die erste strenge Grundstufe meldete eigene Nachweisnamen als mögliche
Synchronisationskopien ([Erstlauf](ci-erstlauf.json)); eindeutige Namen lösten
diesen Werkzeugbefund, [damalige Wiederholung](ci-lokal.json) grün.
Beide Grundstufen gehören zum älteren Apphash. Die [neue strenge Grundstufe](grundstufenwiederholung.json) ist grün
(17 ausgeführt/ein bekannter lokaler SSL-Hinweis). Die vollständige native
Wiederholung bleibt vor dem Produktionsabschluss Pflicht.
