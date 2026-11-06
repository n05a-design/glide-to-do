# Menschliche Abnahme 3.50.2 – begonnen

Auftrag des Inhabers am 04.11.2026: „Ich möchte die menschliche Abnahme jetzt machen.“

## Prüfstand und Grenze

- Windows, eingefrorene Quellfassung 3.50.2 / Aufgabenformat 26 aus `40c20fd62db6ec31b4e3668dfc9e7f1550f67974`, Zweig `codex/glide-3.50.2-ci-korrekturen`.
- App-SHA-256: `6a51be0a2d2e318aabe7d025ef7bb8a64c54d9397de6b0059af74248c1346c26`.
- 265 Dateien der Quellablage einschließlich Ressourcen in eine eigene lokale Prüffassung kopiert und einzeln per SHA-256 verglichen. Original-Showcase als Ausgangsdaten; eigener frischer `GLIDE_DATA_DIR` außerhalb OneDrive. Laufzeitprobe: Python 3.14.7, Tcl/Tk 9.1.0 mit vorhandener eigener Windows-Erweiterung.
- Das ist eine Bedien-/Sichtprüfung der Quellfassung. Die abschließende Prüfung tatsächlich gelieferter eigenständiger Pakete bleibt separat; laut Übergabe tragen vorhandene Lieferpakete noch 3.50.0. Keine neue Vollmatrix oder aktuelle Remoteauswertung in dieser Vorbereitung.
- Die lokale Laufablage enthält eingefrorene Quelle, Dateimanifest, Showcase, synthetische Arbeitsdaten, Startkontext und einen Starter für den Wiederanlauf mit denselben Daten. Keine echten Nutzerdaten übernehmen.

Startkontrolle: Der erste lokale Prüfstarter importierte vor abgeschlossener UI-Initialisierung; danach war ein leerer Anfangsbestand sichtbar. Vorlauf regulär geschlossen und erhalten. Nur den lokalen Starter angepasst: Import nach dem Anlaufen der Ereignisschleife in eine neue synthetische Ablage, elf Dokumente ausdrücklich geprüft. Startkontext meldet elf Dokumente und 26 direkt enthaltene Punkte (Unterpunkte nicht mitgezählt); das Briefing einschließlich Bild ist sichtbar. Dies ist ein eigener Vorbereitungsbeleg, keine menschliche Freigabe und kein geprüfter Produktfix.

Verbindliche Kriterien bleiben in der [zentralen manuellen Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#aktuelle-abschlussrunde); diese Tabelle bündelt nur die Sitzungsfolge. Keine Freigabe aus automatischer Vorbereitung oder eigener Fenstersichtung ableiten.

## Menschliche Rückmeldungen

Prüfer: Inhaber. Datum: 04.11.2026. Zwei Teilrückmeldungen zu Block 1 liegen vor; Gerät, Bildschirm-Skalierung und tatsächlich geprüfte Monitore noch ergänzen. Keine Gesamtabnahme.

| Block | Umfang | Ergebnis |
|---|---|---|
| 1 | Ersteindruck, Hell/Dunkel, Braun/Blau, Liste/Heute/Seite/Ordner/Pinnwand, Seitenleistenbreiten, kleines Fenster, große Schrift, vier Schriftstile | begonnen: Anleitungspunkte 1/2 und Hell-/Dunkelwechsel bestätigt; Punkte 3/4/5 mit Layoutbefunden, Rückmeldungsblock abgeschlossen; Nachtest und weitere Teilumfänge offen |
| 2 | Anlegen, Bearbeiten, Unterpunkte, Mehrfachauswahl, Labels, Sortierung, Abbruch, Undo/Redo, Papierkorb | offen |
| 3 | Tag/Woche, Kapazität, Voraussetzungen, Fokusdauer und Aufgabenwechsel | offen |
| 4 | Seiten/Blöcke ziehen und abbrechen, Nebenansicht, Verweise, Suche, offene Entwürfe | offen |
| 5 | Pinnwand/Bilder/Pixelsymbole, Import/Export, Anhänge, Sicherung/Restore und Schreibschutz in Testablagen | offen |
| 6 | Normal schließen/Neustart, Schlafen/Aufwachen, physische DPI-/Mehrmonitorprüfung und Windows-Integration | offen |

Screenreader bleibt nach D58 bis Bedarf zurückgestellt. Mac/Linux, fremde Programme, Clean-Machine, Signatur/Installer und native Paketfreigaben werden nur nach tatsächlicher Prüfung bestätigt.

Rückmeldung je Teilpunkt: `Block / Handlung | bestanden oder konkreter Befund | Darstellung und Fenstergröße | Einschränkungen`. Nicht durchgeführte Teilpunkte bleiben offen; nach Korrekturen die betroffenen Quellbytes und notwendigen Wiederholungen neu zuordnen.

## Erste Teilrückmeldung des Inhabers – Block 1

Die Nummern beziehen sich auf die fünf Anleitungspunkte im Chat, nicht auf die sechs Sitzungsblöcke der Tabelle.

- **1 Briefing ansehen und scrollen:** „ja“, bestanden.
- **2 Ansichten wechseln:** „ja“, bestanden.
- **3 Fenster verkleinern/vergrößern:** „Kleinere Probleme“, mit den folgenden Befunden offen.
- **4 Hell/Dunkel und Fensterfarbe:** Funktionswechsel vom Inhaber bestätigt; zusätzliche Button-Gestaltungsbefunde siehe zweite Teilmeldung.
- **5:** Zweite Teilmeldung betrifft Labels/Buch/Seitenfuß. Daraus folgt keine gesonderte pauschale Freigabe großer Schrift, DPI oder weiterer Sitzungsblöcke.

| ID des Inhabers | Befund / gewünschte Änderung | Zugeordnete Bilder |
|---|---|---|
| 3.1 | Fälligkeit wird in der Tabelle abgeschnitten. Die drei rechten, nur bei Hover sichtbaren Symbole lassen die Zeilen ungewöhnlich wirken; Darstellung und Platzbedarf bei schmaler Breite korrigieren. Das gewünschte endgültige Sichtbarkeitsverhalten ist noch nicht näher bestimmt. | 01 |
| 3.2 | Eingabe „Neue Aufgabe“ und „Suchwort eingeben“ stehen zu dicht beieinander. | 02 |
| 3.3 | Aktionen niemals auf zwei Zeilen umbrechen; nur die wichtigsten direkt zeigen, damit Eingabe und Inhalt ausreichend Platz behalten. „Überschrift“ und „Code“ können aus der direkten Werkzeugzeile entfallen, da sie im Text geändert werden können. Vorgabe: eindeutige Bedienwege, keine unnötigen mehrfachen Wege für dieselbe Handlung. | 03 |
| 3.4 | Auch die Zeichenfläche enthält zu viele Aktionen; Oberfläche ausdünnen und übersichtlicher machen. | 04 |
| 3.5 | Unerwartetes Viereck/Markierung auf der Zeichenfläche: verschwindet bei Fenster-Fokusverlust und erscheint nach erneutem Klick ins Fenster wieder; auch bei aktivem Pinsel statt Auswahlwerkzeug. Ursache noch ungeprüft, keine Diagnose oder Behebung behauptet. | 04, 05 (Detail) |

Die fünf Originalbilder wurden bytegleich in der lokalen Laufablage unter `eingang/teilmeldung_01` gesichert; Hashmanifest liegt daneben. Die Zuordnung 01–05 entspricht der Reihenfolge der Anhänge. Die Bilder werden nicht öffentlich hochgeladen.

**Verbindliche Reihenfolge:** Der Inhaber setzt die Rückmeldung mit Punkt 4 fort. Bis zum Ende seiner Abnahme nur sammeln und dokumentieren; geöffnete eingefrorene Prüffassung 3.50.2 unverändert lassen. Anschließend die gesammelten Korrekturen in **3.50.3** einarbeiten und passende Prüfungen sowie einen eindeutig bezeichneten neuen Nachteststand bereitstellen. Noch kein Versionswechsel und keine Produktionskorrektur; keine Gesamtfreigabe oder Gitveröffentlichung aus dieser Rückmeldung ableiten.


## Zweite Teilmeldung und Abschluss dieses Rückmeldungsblocks

Der Inhaber hat seine Rückmeldung mit „Das war alles was ich dazu gefunden hatte“ abgeschlossen. Dies beendet den aktuellen Rückmeldungsblock, nicht die gesamte menschliche Abnahme aller Funktionen/Plattformen. Die Umsetzung der gesammelten Korrekturen in 3.50.3 ist damit gemäß vorherigem Auftrag begonnen; die eingefrorene Prüffassung 3.50.2 bleibt unverändert.

- **4:** Hell-/Dunkelwechsel funktionieren. Buttons außerhalb der beiden Hauptkarten erscheinen unterschiedlich; gemeinsame Buttonerzeugung, Größen, Konturen und Theme-/Host-Lebensdauer anhand des angehängten Skills prüfen und vereinheitlichen.
- **5:** Labels reserviert rechts Platz für drei Aktionen, obwohl diese dort nicht benutzt werden. Dasselbe in „Wissen und Bildmaterial“; dort sind Inhalte deshalb kaum nutzbar. Ungenutzte Reserve entfernen und verbleibende Buchspalten nach Inhalt und Priorität verteilen.
- **Seitenfuß:** „Erwähnt ohne Verweis“ hat zu viel linken/rechten Abstand; Karteninnenrand und Knopfbreite korrigieren.

Fünf Originalbilder und die unveränderte Datei Design-Richtlinien.md lokal in der Umsetzungslaufablage unter `eingang/teilmeldung_02` gesichert, Bildhashes im Manifest. Bild 01: Seitenwerkzeuge; 02: Buch-Eingabe/Suche; 03: Labels; 04: Seitenfuß; 05: Buchtabelle. Quelle ist die direkte Rückmeldung des Inhabers; die angehängte Skilldatei verweist auf den zentralen Designvertrag und wird nicht als eigenständiger neuer Regelkatalog kopiert.


## Dritte Rückmeldung – schmaler Kopf

05.11.2026: Der Inhaber meldet einen auf wenige Zeichen verkürzten Titel („Wiss…“) und beauftragt, ab knapper Breite die globalen Knöpfe rechts neben die Aufgabeneingabe zu verschieben. In der obersten Zeile verbleiben Titel und Datei/Bearbeiten/Ansicht/Hilfe. Originalbild bytegleich lokal unter `eingang/teilmeldung_03` mit Hashmanifest gesichert. Erweiterung des laufenden 3.50.3-Korrekturschnitts/D61; kein neuer Featureausbau und keine Menschenfreigabe des neuen Codes.
