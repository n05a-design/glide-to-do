# Aufgabenoberfläche – Liefernachweis 3.38.0

Stand 11.10.2026 · Glide 3.38.0 · Aufgabenformat 23 · Mac vollständig grün, native Matrix ausstehend

Paket 3 setzt S26-01/02/03/04/07/13 vollständig nach D22–D25/D31/D32 um.
Ausgangslieferung 3.37.0, Liefercommit `0e7b358`. Alle bisherigen Felder bleiben
im gemeinsamen Inspektor; kleine Fenster nutzen die Inhaltsfläche.

| Tor | Ergebnis |
|---|---|
| Gemeinsamer Inspektor | 22 gezielte Szenarien grün: sechs Kontexte, volle Felder, Schreibschutz, Konflikt, echter Dateischreibfehler/Retry, Auswahl, Checkliste, Wiederholung, Zustellbelege, modale Feldauswahl und Neustart |
| Direkte Felder | 30 Klickgruppen grün: vier Listenansichten, Pinnwand frei/geordnet/Spalten bei 75/150 %, Live-Listen, echter Dokumentdoppelklick; Modifier bleiben Auswahl |
| Fachlogik | 11 Dreiwege-/Feldkonflikttests und sieben Zeit-/Abbruchtests grün |
| Vorversion | vier getrennte passende Assertion-Gegenproben gegen unveränderte 3.37.0 rot |
| Beschädigte Kandidaten | vier Funktionsdefekte plus vier [Kalibrierdefekte](kalibriergegenproben.json) passend rot, positive Kontrollläufe grün; native Matrix prüft insgesamt 15 Defektfälle |
| Bedienfläche | sechs echte Inhaltswidgets × drei Größen × zwei Schriftgrößen; [Geometrie](geometrie.json) |
| Bewegung | reparierter Quellstand: 215 Abschlüsse/Abbrüche, maximal 106,46 ms; Fokus sofort, Abschaltung/Schließen räumen auf; [Reparaturnachmessung](uebergang-lieferstand.json), [erste Reihe](uebergang-erste-messung.json) |
| Eigene Fensterbilder | Hell/Dunkel, große Schrift, Mindestgröße und Inspektor; lokal betrachtet, keine menschliche Abnahme |
| Tempo vor/nach | reparierter Quellstand: Abhaken 1.000/5.000/10.000: 15,7/61,1/114,8 ms Median; Suche 66,4/73,1 ms; Startseite kalt 294 ms, warm 79/83; Einstellungen 179 ms zuerst, warm 139/142. Alle verbindlichen Grenzen eingehalten. [Beide Reihen/Vergleich](tempo.json) |
| Mac-Vollprüfung eingefroren | erster Freeze vollständig ausgewertet, Exit 1, 848 Dateien unverändert; [roter Vorlauf](mac-vorlauf.json). Elf [Reparatursuiten](reparaturproben.json) grün. Zweite Vollprüfung Exit 0: 102 ausgeführt/zwei übersprungen, 85 Suiten/294 Unit-Tests; alle 852 Dateien nach Lauf unverändert; [grüner Volllauf](mac-voll.json) |
| Native Linux-/Windows-Matrix | ausstehend |
| 07 und Showcase | 42 Code-/141 Ressourcen-/sechs Showcase-Dateien SHA-256-gleich; [Abgleich](lieferabgleich.json) |
| Mac-Entwicklungsbundle | 42 Code-/55 Plattformressourcen gleich Quelle; Ad-hoc-Signatur im Bauordner und auf Rückkopie grün; [Bundle](bundle.json) |
| Menschen-/DPI-/Mehrmonitorabnahme | getrennt offen |

Die Geometrie beginnt am oberen Fensterrand ohne Betriebssystem-Titelleiste
und endet am tatsächlichen Aufgabenbaum, Seitentitel bzw. Pinnwandcanvas.
Bei 1280 × 800 sind es 119/118/115 px (höchstens 14,875 %), zuvor 216 px
am Aufgabenbaum. 1280 × 840 wird zusätzlich berichtet. Die Mindestgröße
860 × 700 hat Lesbarkeit/Erreichbarkeit als Tor, nicht die 15-Prozent-Grenze.

Bestandsprüfungen behalten ihre Feld-, Abbruch-, Speicher- und Undo-Kriterien;
neu angelegte ungespeicherte Punkte prüfen weiterhin die Anlegemaske. Geänderte
Aufgaben verwenden den Inspektor. Ein früher fälschlich als Eingabeänderung
erkannter Wiederholungsanker/Zustellbeleg ist korrigiert; der unveränderte
Komforttest bestätigt Überspringen mit genau einem Undo. Schreibfehler der
Checklistenbearbeitung lassen Modell/Datei/Verlauf/Undo unverändert.
Rohprotokolle und Fensterbilder bleiben außerhalb OneDrive und Git.

Die allgemeine Ansichtserie zeigt neben schnellerer Liste (267 → 146 ms Median)
auch langsamere Bibliothek (408 → 470 ms) und Notiz (262 → 380 ms).
Die Notizverzögerung blieb in der Diagnose auch ohne Animation; der Python-Anteil
liegt bei rund 32/33 ms, die zusätzliche Zeit überwiegend im nativen Zeichnen.
Es gibt für diese beiden Wege kein separates absolutes Paket-3-Ziel. Die Werte
bleiben als Performancebefund sichtbar; keine pauschale Beschleunigung behauptet.
Notizen behalten ihre bisherige Leseschrift; Seiten nutzen die vier gewählten Stufen.

Der erste unveränderte Freeze meldet echte Fehler in der Labelauswahl
(zwei falsche Objektzugriffe) und im isolierten Vorlageneditor (irrtümlicher
Hauptinspektor-Aufruf). Beide sind im Lieferkandidaten korrigiert. Zwei alte
Prüfungen werden am passenden neuen Einstieg fortgeführt: alle fünf Dialogleisten
am ungespeicherten Langtext, Fortschritt und Datum an Unterzeile bzw. Titel.
Die erste Kopie bleibt für den roten Nachweis unverändert. Beide Temporeihen tragen ihren jeweiligen Apphash. Die zweite Vollprüfung
und Lieferabgleiche sind grün; native Matrix und Produktionsabschluss bleiben offen.

Die Reparaturreihe trägt App-SHA `5661381d659b8dc79735383cf5c55ae5f8b79e752bfcec68240d208a2ec1865b`. Alle elf betroffenen/ergänzenden Suiten sind grün. Der Vorlage bleibt ihre isolierte vollständige Entwurfsmaske; sie gehört nicht zu den sechs gewählten Hauptansichtskontexten. Zeilenknöpfe sind ausdrücklich zugewiesen, damit die unverändert strenge Attributprüfung sie ohne Ausnahme nachweist. Die allgemeine Ansichtserie bestätigt Bibliothek 470 ms / Notiz 380 ms Median; der Performancebefund bleibt offen sichtbar.

Die erste strenge Grundstufe meldete zwei eigene Bewegungsnachweise aufgrund ihrer Dateinamen als mögliche Synchronisationskopien ([Ergebnis](ci-erstlauf.json)). Die drei Nachweisdateien sind eindeutig umbenannt; Inhalte und Apphash bleiben unverändert. Die vollständig wiederholte strenge Grundstufe ist grün ([Ergebnis](ci-lokal.json)); der bekannte lokale SSL-Hinweis bleibt dokumentiert.
