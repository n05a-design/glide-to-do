# Glide – Funktionsvorschläge und Prioritäten

Stand: 11.09.2026 · Ausgangspunkt: Glide 3.7.0

Diese Datei dokumentiert Vorschläge für die Zukunft und die jüngsten Rückmeldungen des Nutzers. Sie beschreibt keine bereits ausgelieferten Erweiterungen und keine pauschale Beauftragung des gesamten Umfangs. Projektstand und Entwicklungsregeln stehen in der [kompakten Weitergabe](Glide_Weitergabe_neuer_Chat_2026-09-11.md).

## 1. Maßgebliche Rückmeldung des Nutzers

| Thema | Einordnung |
|---|---|
| Erinnerungsfunktion | Höchste ausdrücklich genannte Priorität. |
| Pinnwand | Ausdrücklich positiv bewertet; als zusätzliche Ansicht bestehender Inhalte ausarbeiten. |
| Reiteransicht für Listenelemente | Ausdrücklich positiv bewertet; Ebene und Verhalten noch konkretisieren. |
| Analoge Ablagefächer | Kein eigenständiger Ausbaupunkt: „In Bearbeitung“ und Labels decken den Zweck bereits ab. |
| Projektmappe | Überschneidet sich mit dem bestehenden Ordner-/Listensystem. Keine zusätzliche Hierarchie einführen. |

## 2. Erinnerungen – zuerst ausarbeiten

### Ziel

Glide soll rechtzeitig und nachvollziehbar an Aufgaben erinnern. Vorhandene Fälligkeiten mit Datum/Uhrzeit und Wiederholungen bilden die Grundlage. Die Erinnerung ist ein eigener Zeitpunkt und ändert nicht automatisch die fachliche Fälligkeit.

Beispiel: „Exposé am Freitag um 12 Uhr abgeben“, Erinnerung am Donnerstag um 15 Uhr. Ein Aufschub der Erinnerung verschiebt die Abgabefrist nicht.

### Vorgeschlagener Funktionsumfang

- Erinnerung direkt in der bestehenden Aufgabenmaske aktivieren; schnellen Standard und erweiterte Einstellungen anbieten.
- Wahl zwischen festem Zeitpunkt und Abstand zur Fälligkeit, etwa „einen Tag vorher“. Bei Aufgaben ohne Uhrzeit einen verständlichen Standard anzeigen.
- Aktionen: Aufgabe öffnen, Erinnerung verschieben, Aufgabe erledigen. „Schlummern“ verändert nur die Erinnerung.
- Offene und verpasste Hinweise in einer Erinnerungsübersicht nachvollziehen.
- Geänderte Fälligkeiten aktualisieren relative Erinnerungen; fest gewählte Erinnerungszeiten bleiben erkennbar unabhängig.
- Erledigte oder gelöschte Aufgaben lösen keine neuen Hinweise aus. Verhalten bei Wiederherstellung aus dem Papierkorb ausdrücklich festlegen.
- Wiederholungen verwenden die bestehende Serienlogik; nach Abschluss muss der nächste Hinweis genau zum nächsten Vorkommen gehören.
- Nach Neustart oder Ruhezustand verpasste Hinweise gesammelt und ohne Mehrfachauslösung behandeln.
- Zeitzonenwechsel und Sommer-/Winterzeit berücksichtigen; Speicherung und Anzeige der Zeitpunkte eindeutig definieren.
- Später optional mehrere Erinnerungen pro Aufgabe, individuelle Standards und Ruhezeiten ergänzen.

### Umsetzung in überprüfbaren Stufen

| Stufe | Erwartetes Verhalten | Grenze |
|---|---|---|
| Erste nutzbare Stufe | Lokale Terminprüfung bei laufender App, gespeicherte Erinnerungen, Aufschub, Erledigen und Behandlung verpasster Hinweise beim nächsten Start. | Darf nicht als Erinnerung bei geschlossener App beworben werden. |
| Ziel für den Desktop-Alltag | Systembenachrichtigungen und ein ausdrücklich festgelegtes Verhalten bei geschlossenem Fenster, beendetem Programm, An-/Abmeldung und Neustart. | Plattformintegration für macOS und Windows separat entwerfen und testen. Ein ausgeschaltetes Gerät kann keinen lokalen Hinweis anzeigen. |
| Weiterer Ausbau | Mehrere Hinweise, Ruhezeiten, Vorlage-Vorgaben und feinere Wiederholungsoptionen. | Erst ergänzen, wenn Auslösung und Datenhaltung verlässlich sind. |

Vor einer Entscheidung für Hilfsprozess, Autostart oder neue Abhängigkeiten bestehende Architektur und Plattformmöglichkeiten prüfen. Solche Änderungen dokumentieren; nicht nebenbei Systemdienste installieren. Die lokale Nutzung ohne Konto oder Internet bleibt erhalten.

### Wesentliche Abnahmekriterien

1. Eine fällige Erinnerung erscheint einmal; wiederholtes Öffnen oder Neustarten erzeugt keine unmittelbaren Duplikate.
2. Aufschieben bleibt nach Neustart erhalten und verändert nicht die Fälligkeit.
3. Erledigen, Löschen und Terminänderungen entfernen oder aktualisieren noch ausstehende Hinweise.
4. Ruhezustand, verpasste Termine und Uhrumstellungen führen zu nachvollziehbarem Verhalten.
5. Wiederkehrende Aufgaben erzeugen Hinweise für das korrekte nächste Vorkommen.
6. Datenmigration und Backup/Restore erhalten die Konfiguration; wiederhergestellte alte Termine lösen keinen unkontrollierten Benachrichtigungssturm aus.
7. Die Oberfläche erklärt die tatsächlich unterstützten Betriebszustände und gegebenenfalls fehlende Systemberechtigungen.

## 3. Reiteransicht für Listenelemente

### Arbeitshypothese

Innerhalb einer bestehenden Liste lassen sich einzelne Aufgaben, Gruppen oder Long-Tasks als Reiter öffnen. Der gewählte Reiter zeigt die vollständigen Details samt Unterpunkten, Beschreibung, Labels und Anhängen. Die Reiter sind eine Navigationsform; die ursprüngliche Struktur bleibt erhalten.

**Noch nicht entschieden:** Sollen einzelne Punkte eigene Reiter erhalten oder sollen Gruppen die Reiter bilden und ihre zugehörigen Aufgaben anzeigen? Beides ist möglich; eine kleine Vorschau mit einer echten Beispiel-Liste sollte diese Entscheidung erleichtern. Eine zusätzliche Ansicht für mehrere offene Listen ist eine andere, ebenfalls denkbare Funktion.

### Sinnvolle Bedienung

- Listenansicht und Reiteransicht je Liste umschaltbar machen.
- Reiter gezielt öffnen und schließen; Schließen löscht das Element nicht.
- Lange Titel kürzen, den vollständigen Namen zugänglich halten und bei vielen Reitern eine Übersicht anbieten.
- Beschriftung, Fokus, Tastaturwechsel und Hell-/Dunkeldarstellung konsistent gestalten.
- Reiterreihenfolge zunächst als Ansichtseinstellung behandeln. Eine Änderung der tatsächlichen Aufgabenreihenfolge darf nur ausdrücklich erfolgen.
- Ausgewähltes Element und gewünschte Ansicht bei Rückkehr wiederfinden.

## 4. Pinnwand als ergänzende Arbeitsansicht

### Ziel und Anwendungsfälle

Vorhandene Aufgaben, Notizen und Anhänge einer Liste oder eines Ordners räumlich anordnen. Beispiele: Exposé-Produktion mit Bildauswahl und Prüfpunkten, Website-Relaunch mit Seitenideen, Besprechungsvorbereitung mit offenen Fragen.

### Vorgeschlagener Einstieg

- Bestehende Elemente als Karten anheften, frei verschieben und optional an einem Raster ausrichten.
- Titel, relevante Labels, Fälligkeit und kurze Vorschau anzeigen; Kartendetails öffnen dieselbe vorhandene Bearbeitungsmaske.
- Nach vorhandenen Labels filtern und Elemente visuell zusammenstellen.
- Positionen und Kartengrößen getrennt vom fachlichen Inhalt speichern.
- „Von Pinnwand entfernen“ und „Aufgabe löschen“ eindeutig trennen.
- Zusätzlich eine geordnete Kartenansicht und Tastaturbedienung anbieten; freie Positionierung darf keine Bedienvoraussetzung sein.
- Bei vielen Elementen Suche, sichtbaren Fokus und eine Funktion zum Wiederfinden außerhalb des sichtbaren Bereichs vorsehen.

Spätere Optionen: Verbindungen zwischen Karten, Bildvorschauen, neue Notizzettel und Zoom. Eine gezeichnete Verbindung ist zunächst eine visuelle Beziehung; eine verbindliche Aufgabenabhängigkeit benötigt eine eigene, explizite Funktion.

**Datenregel:** Eine Aufgabe in Liste, Reiter und Pinnwand bleibt dasselbe Objekt mit derselben Identität. Erledigen, Umbenennen oder Terminänderungen müssen in allen Ansichten übereinstimmen. Board-Spalten dürfen vorhandene Labels verwenden und sollen kein konkurrierendes Statussystem erzwingen.

## 5. Projektmappe gegenüber vorhandenen Ordnern und Listen

Die bisherige Idee einer Projektmappe bietet als zusätzlicher Container keinen ausreichenden Mehrwert. Ordner bündeln bereits Listen; Beschreibungen, Labels und Anhänge sind vorhanden.

Ein möglicher späterer Unterschied wäre eine **zusammenfassende Ansicht eines vorhandenen Ordners**: offene Aufgaben aus seinen Listen, angeheftete Unterlagen und nächste Termine gemeinsam zeigen. Reiter könnten zwischen diesen vorhandenen Inhalten wechseln. Das wäre eine Erweiterung der Darstellung und keine neue Projektart, kein zusätzlicher Ablageort und keine Voraussetzung für Pinnwand oder Erinnerungen.

## 6. Weitere Funktionsideen – nachrangiger Vorrat

Die Reihenfolge in dieser Tabelle ist eine Empfehlung, keine bestätigte Umsetzungsreihenfolge.

| Vorschlag | Konkreter Mehrwert gegenüber dem aktuellen Stand |
|---|---|
| Globale Schnellerfassung | Neue Aufgabe über ein Tastenkürzel erfassen, ohne zuerst die richtige Liste zu öffnen; optional verständliche deutsche Datumserkennung mit Vorschau. |
| Bewusste Tagesauswahl | Aufgaben aus mehreren Listen für heute auswählen, unabhängig von ihren Fälligkeiten. Das bestehende Tagesziel zählt Abschlüsse und ersetzt diese Auswahl nicht. |
| Gespeicherte Filter | Kombinationen aus vorhandenen Labels, Listen, Wichtigkeit und Terminen als wiederverwendbare Ansichten speichern. |
| Tabellenansicht | Viele Aufgaben mit vergleichbaren Angaben kompakt bearbeiten; Spalten je Liste wählen. |
| Bearbeitungstermin und Aufwand | Geplanten Arbeitstag, verbindliche Frist und geschätzten Aufwand unterscheiden. Darauf später eine Kapazitätsplanung aufbauen. |
| Vollständiges App-Backup | Aufgaben, Anhänge, Einstellungen, Vorlagen und Aktivitätsdaten gemeinsam sichern und mit Inhaltsvorschau wiederherstellen. Der aktuelle Aufgabenbackup deckt nicht alles ab. |
| Dauerhafter Änderungsverlauf | Änderungen und frühere Werte gezielt nachvollziehen; ergänzt das vorhandene Rückgängig innerhalb einer Sitzung. |
| Abhängigkeiten und Meilensteine | Voraussetzungen wie „Veröffentlichung erst nach Freigabe“ sichtbar machen; gesonderte Funktion, nicht aus Pinnwand-Linien ableiten. |
| Benutzerdefinierte Felder | Beispielsweise Objekt, Ansprechpartner, Kanal oder Kosten strukturiert pflegen und filtern. |
| Verknüpfte Notizen und Aufgaben | Eine Besprechungsnotiz mit mehreren Aufgaben verbinden und Rückverweise anzeigen. |
| Vorlagen mit Eingabefeldern | Projektname, Objektadresse, Ansprechpartner und Bezugsdatum einmal eingeben und in vorgesehenen Feldern übernehmen. Relative Termine existieren bereits. |
| Regeln für Abläufe | Vorhandene Labels, Termine oder Erledigungen als Auslöser für nachvollziehbare Folgeaktionen verwenden; Schleifen und unerwartete Massenänderungen vermeiden. |
| Erweiterte Notizen | Formatierter Text, eingefügte Bilder und einfache Markierungen oder Skizzen; normale Beschreibungen und Dateianhänge bestehen bereits. |
| Import und Integrationen | CSV mit Spaltenzuordnung, Kalenderdateien, später gezielte Mail-/Kalenderschnittstellen. Bestehende Glide-Importe und lesbare Exporte beibehalten. |
| Druck/PDF | Tageszettel, Besichtigungschecklisten, Besprechungsagenden und Projektübersichten direkt brauchbar ausgeben. |
| Optionale KI | Aufgabenvorschläge aus Texten erstellen; Ergebnisse vor Übernahme prüfen und externe Datenübertragung steuerbar machen. Kein notwendiger Bestandteil der Kernfunktionen. |

Mobile Nutzung, eigene Synchronisation und Teamarbeit sind eigenständige große Ausbauschritte. Sie benötigen unter anderem Konfliktbehandlung, Berechtigungen und einen nachvollziehbaren Änderungsabgleich. Die bestehende OneDrive-Ablage ist dafür kein Ersatz.

## 7. Analoge Gestaltung – weitere Ideen ohne neue Doppelstrukturen

Pinnwand und Reiter stehen bereits oben. Folgende Elemente bleiben optionale Gestaltungsideen:

| Element | Sinnvoller Einsatz | Voraussetzung oder Grenze |
|---|---|---|
| Karteikarten | Kompakte Darstellung vorhandener Aufgaben mit aufklappbaren Details. | Als Darstellung bestehender Elemente; keine separate Kartei-Datenbank. |
| Notizzettel | Kurze angeheftete Gedanken zu Liste oder Aufgabe. | Bei Erweiterung über vorhandene Beschreibungen hinaus ein klares Notizmodell vorsehen. |
| Lesebänder/Registermarken | Wichtige Stellen einer langen Liste wiederfinden. | Markierung und Filterung sollten mit Tastatur zugänglich sein. |
| Freigabestempel | Vorhandene Labels wie „Geprüft“ auffällig darstellen. | Keine rechtsverbindliche Freigabe oder bestätigte Identität suggerieren. |
| Kontrolltafel | Ausstehende Rückmeldungen, blockierende Angaben oder fällige Erinnerungen sichtbar machen. | Jede Anzeige nennt Ursache und öffnet die betroffenen Elemente; Farbe allein reicht nicht. |
| Mechanischer Zähler | Einen konkreten Bestand wie offene Rückmeldungen zeigen. | Keine pauschale Produktivitätsbewertung aus der Anzahl von Klicks oder Abschlüssen ableiten. |
| Waage | Geplanten Aufwand und verfügbare Kapazität vergleichen. | Erst sinnvoll mit tatsächlichen Aufwandsschätzungen und gepflegter Kapazität. |
| Kompass | Ein selbst gewähltes Ziel mit den zugehörigen nächsten Schritten hervorheben. | Ein Ziel muss ausdrücklich zugeordnet sein; keine scheinbar objektive Priorisierung erfinden. |
| Stecktafel mit begrenzten Plätzen | Beispielsweise drei bewusst ausgewählte aktuelle Aufgaben darstellen. | Ergänzende Fokusansicht vorhandener Aufgaben; keine weitere Statusverwaltung. |

Materialwirkung und Bewegung dezent halten. Alle Ansichten müssen mit vorhandenen Schriftgrößen, Hell/Dunkel und Tastaturbedienung funktionieren. Reiter, Pinnwand und Instrumente sollen einzeln auswählbar sein, damit die Startseite übersichtlich bleibt.

## 8. Empfohlene nächste Reihenfolge

1. Erinnerungsverhalten und Plattformgrenzen konkretisieren; anschließend eine verlässlich geprüfte Umsetzung beginnen, sobald beauftragt.
2. Reiteransicht an einer vorhandenen Beispiel-Liste skizzieren und die gewünschte Ebene bestimmen.
3. Pinnwand für dieselben Listenelemente entwickeln, sobald Umfang und Bedienung feststehen.
4. Danach Schnellerfassung und gespeicherte Filter bewerten.

Native Bedienung, Barrierefreiheit, Datenmigration, Wiederherstellung und Pflege der Arbeitskopie begleiten jeden Ausbauschritt. Größere Funktionen sollten vorhandene Daten- und Bedienlogik wiederverwenden; neue Architekturteile nur mit konkret belegtem Nutzen einführen.

## 9. Vergleichsquellen

Offizielle Quellen, im Gespräch am 11.09.2026 herangezogen. Tarif- und Plattformunterschiede sind bei späterer Planung erneut zu prüfen.

- Todoist: natürliche Datumseingabe, Ansichten und Trennung von geplantem Datum und Deadline: [Einstieg](https://www.todoist.com/help/todoist/get-started/get-started-with-todoist-OgNNJR). Gespeicherte Abfragen: [Filter](https://www.todoist.com/help/todoist/features/introduction-to-filters-V98wIH).
- Microsoft To Do: bewusst zusammengestellte Tagesauswahl: [My Day and suggestions](https://support.microsoft.com/en-us/todo/my-day-and-suggestions).
- Microsoft Planner: Premium-Funktionen wie Abhängigkeiten, Meilensteine und benutzerdefinierte Felder: [Advanced capabilities](https://support.microsoft.com/en-us/planner/teams/advanced-capabilities-with-premium-plans-in-planner).
- Google Keep: Notizen, Listen sowie Organisation mit Labels, Farben und angehefteten Inhalten: [How to use Google Keep](https://support.google.com/keep/answer/2888240?hl=en-GB).
