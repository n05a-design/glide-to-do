# Glide – Funktionsvorschläge und Prioritäten

Stand: 14.09.2026 · Glide 3.21.3 · Aufgabenformat 15

Diese Datei dokumentiert Vorschläge für die Zukunft und die jüngsten Rückmeldungen des Nutzers. Die erste lokale Erinnerungsstufe wurde nach dem Umsetzungsauftrag vom 12.09.2026 implementiert; Reiteransicht, Pinnwand, Schnellerfassung, gespeicherte Filter und „Mein Tag“ wurden ergänzt. In 3.13 ist die kompakte Tabellenansicht mit listenspezifischen Spalten umgesetzt. In 3.14 folgten Bearbeitungstag und Aufwand, in 3.15 die Tagesplanung mit Tageskapazität, in 3.16 das vollständige App-Backup, in 3.17 die Druck- und PDF-Ausgabe, in 3.18 der CSV-Import mit Spaltenzuordnung, in 3.19 der dauerhafte Änderungsverlauf mit Aufgabenformat 15, in 3.20 die Kalenderausgabe als ICS und in 3.21 der Kalenderimport aus ICS. Offen sind benutzerdefinierte Felder und darauf aufbauende eigene Ansichten; eine echte Kalendersynchronisierung bleibt bewusst außen vor. Es handelt sich weiterhin um einen unveröffentlichten Entwicklungsstand. Projektstand und Entwicklungsregeln stehen in der [kompakten Weitergabe](Glide_Weitergabe_neuer_Chat_2026-09-11.md).

## 1. Maßgebliche Rückmeldung des Nutzers

| Thema | Einordnung |
|---|---|
| Erinnerungsfunktion | Höchste ausdrücklich genannte Priorität. |
| Pinnwand | Ausdrücklich positiv bewertet; als zusätzliche Ansicht bestehender Inhalte ausarbeiten. |
| Reiteransicht für Listenelemente | Ausdrücklich positiv bewertet; Ebene und Verhalten noch konkretisieren. |
| Analoge Ablagefächer | Kein eigenständiger Ausbaupunkt: „In Bearbeitung“ und Labels decken den Zweck bereits ab. |
| Projektmappe | Überschneidet sich mit dem bestehenden Ordner-/Listensystem. Keine zusätzliche Hierarchie einführen. |

## 2. Erinnerungen – erste lokale Stufe umgesetzt

[Umsetzung 3.8.0, Bedienung und Grenzen](../01_Repository/Glide/docs/31_ERINNERUNGEN_3.8.0.md). Systembenachrichtigungen und Verhalten bei beendetem Programm sind noch auszubauen.

**Nachtrag 12.09.2026:** Die Plattformprüfung liegt vor. Eine Systembenachrichtigung mit Glide-Namen setzt auf beiden Plattformen eine installierte, beim Betriebssystem registrierte Anwendung voraus – unter Windows eine Startmenü-Verknüpfung mit AppUserModelID, unter macOS ein `.app`-Bundle. Der Schritt hängt damit am Installer, nicht am Anwendungscode. Ein Hilfsprozess mit Autostart wird wegen der Datenintegrität nicht eingeführt. [Entscheidung mit Betriebszuständen, Stufen und Grenzen](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md).

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
| Erste nutzbare Stufe – in 3.8.0 umgesetzt | Lokale Terminprüfung bei laufender App, gespeicherte Erinnerungen, Aufschub, Erledigen und Behandlung verpasster Hinweise beim nächsten Start. | Darf nicht als Erinnerung bei geschlossener App beworben werden. |
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

## 3. Reiteransicht für Listenelemente – umgesetzt in 3.10.0

[Bedienung, Daten und Grenzen](../01_Repository/Glide/docs/33_REITER_UND_PINNWAND_3.10.0.md).

### Arbeitshypothese

Innerhalb einer bestehenden Liste lassen sich einzelne Aufgaben, Gruppen oder Long-Tasks als Reiter öffnen. Der gewählte Reiter zeigt die vollständigen Details samt Unterpunkten, Beschreibung, Labels und Anhängen. Die Reiter sind eine Navigationsform; die ursprüngliche Struktur bleibt erhalten.

**Entschieden am 12.09.2026:** Reiter entstehen auf Zuruf aus einzelnen Punkten – Aufgaben, Long-Tasks und Gruppen –, nicht automatisch aus Gruppen. Die Gruppenvariante hätte in Listen ohne Gruppen leer laufen lassen und dem Nutzer die Auswahl aus der Hand genommen. Bedienung, Grenzen und Abnahmekriterien stehen im [Bedienvertrag](../01_Repository/Glide/docs/32_REITERANSICHT.md). Eine zusätzliche Ansicht für mehrere offene Listen ist eine andere, ebenfalls denkbare Funktion.

### Sinnvolle Bedienung

- Listenansicht und Reiteransicht je Liste umschaltbar machen.
- Reiter gezielt öffnen und schließen; Schließen löscht das Element nicht.
- Lange Titel kürzen, den vollständigen Namen zugänglich halten und bei vielen Reitern eine Übersicht anbieten.
- Beschriftung, Fokus, Tastaturwechsel und Hell-/Dunkeldarstellung konsistent gestalten.
- Reiterreihenfolge zunächst als Ansichtseinstellung behandeln. Eine Änderung der tatsächlichen Aufgabenreihenfolge darf nur ausdrücklich erfolgen.
- Ausgewähltes Element und gewünschte Ansicht bei Rückkehr wiederfinden.

## 4. Pinnwand als ergänzende Arbeitsansicht – erste Stufe in 3.10.0

Umgesetzt: referenzierte Punkte aus Listen und Ordnern, verschiebbare Karten, Raster, geordnete Ansicht, drei Kartenbreiten, Label-/Textfilter und Tastaturbedienung. Karten enthalten Vorschauen bestehender Beschreibungen und Anhangzahlen; Dateien öffnen über die bestehenden Details. Bildkarten, Verbindungen, Zoom, neue Notizzettel und einzeln skalierbare Karten bleiben spätere Optionen. [Bedienvertrag](../01_Repository/Glide/docs/33_REITER_UND_PINNWAND_3.10.0.md).

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
| Globale Schnellerfassung | **Umgesetzt in 3.11.0:** Neue Aufgabe über Strg/Cmd+Alt+N aus jeder Glide-Ansicht erfassen, Ziel-Liste wählen und eine deutsche Frist mit Vorschau eingeben. Der Shortcut gilt innerhalb der laufenden App. |
| Bewusste Tagesauswahl | **Umgesetzt in 3.12.0:** „Mein Tag“ wählt Aufgaben aus mehreren Listen für den aktuellen Tag, unabhängig von ihren Fälligkeiten. Das bestehende Tagesziel zählt Abschlüsse und ersetzt diese Auswahl nicht. |
| Gespeicherte Filter | **Umgesetzt in 3.11.0:** Kombinationen aus Labels, Listen, Status, Wichtigkeit, Fälligkeit und Suchtext als wiederverwendbare Ansichten speichern; entfernte Referenzen werden sichtbar gemeldet. |
| Tabellenansicht | **Umgesetzt in 3.13.0:** Aufgaben einer Liste flach und kompakt bearbeiten; Aufgabe, Art, Fälligkeit, Wichtigkeit, Labels und Status als je Liste wählbare Spalten. |
| Bearbeitungstermin und Aufwand | **Umgesetzt in 3.14.0:** Optionaler Bearbeitungstag und Aufwand in Minuten, unabhängig von Fälligkeit und „Mein Tag“. Punktdetails, Mehrfachbearbeitung, Tabelle, Reiter, Vorlagen und Backups. |
| Tagesplanung und Tageskapazität | **Umgesetzt in 3.15.0:** Eigene Ansicht für alle Aufgaben mit Bearbeitungstag an einem wählbaren Tag, Aufwandssummen in Tagesplanung, „Mein Tag“, Tabelle und Startseite, Vergleich mit einer selbst gesetzten Tageskapazität. Keine Zeiterfassung, keine automatische Terminverteilung; Wochentagsprofil und Kapazität je Liste bleiben offen. |
| Vollständiges App-Backup | **Umgesetzt in 3.16.0:** Aufgaben, Anhänge, persönliche Einstellungen, Vorlagenkatalog und Aktivitätsdaten in einem `.glideapp`-Archiv; Wiederherstellung mit Inhaltsvorschau und einzeln zuschaltbaren Bereichen, Rückfallsicherungen für alle drei Bestandteile. Cloudsicherung, Zeitplan, Zusammenführen und Verschlüsselung bleiben offen. |
| Dauerhafter Änderungsverlauf | Änderungen und frühere Werte gezielt nachvollziehen; ergänzt das vorhandene Rückgängig innerhalb einer Sitzung. |
| Abhängigkeiten und Meilensteine | Voraussetzungen wie „Veröffentlichung erst nach Freigabe“ sichtbar machen; gesonderte Funktion, nicht aus Pinnwand-Linien ableiten. |
| Benutzerdefinierte Felder | Beispielsweise Objekt, Ansprechpartner, Kanal oder Kosten strukturiert pflegen und filtern. |
| Verknüpfte Notizen und Aufgaben | Eine Besprechungsnotiz mit mehreren Aufgaben verbinden und Rückverweise anzeigen. |
| Vorlagen mit Eingabefeldern | Projektname, Objektadresse, Ansprechpartner und Bezugsdatum einmal eingeben und in vorgesehenen Feldern übernehmen. Relative Termine existieren bereits. |
| Regeln für Abläufe | Vorhandene Labels, Termine oder Erledigungen als Auslöser für nachvollziehbare Folgeaktionen verwenden; Schleifen und unerwartete Massenänderungen vermeiden. |
| Erweiterte Notizen | Formatierter Text, eingefügte Bilder und einfache Markierungen oder Skizzen; normale Beschreibungen und Dateianhänge bestehen bereits. |
| Import und Integrationen | CSV mit Spaltenzuordnung ist in 3.18.0 umgesetzt, die Kalenderausgabe als ICS in 3.20.0; der Kalenderimport in 3.21.0; offen bleiben eine echte Kalendersynchronisierung und später gezielte Mailschnittstellen. Bestehende Glide-Importe und lesbare Exporte beibehalten. |
| Druck/PDF | **Umgesetzt in 3.17.0:** Tageszettel, Liste oder Ordner, Tagesplanung und Checkliste zum Abhaken als eigenständige HTML-Druckansicht, geöffnet im Standardprogramm; dessen Druckdialog liefert Papier oder PDF. Sieben Inhaltsoptionen. Seriendruck, eigenes Layout, Logo und DOCX/XLSX bleiben offen. |
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
| Waage | Geplanten Aufwand und verfügbare Kapazität vergleichen. | **Fachlich in 3.15.0 umgesetzt** als Summe mit Kapazitätsrest in Klartext; eine bildliche Waage bleibt eine optionale Darstellungsidee. |
| Kompass | Ein selbst gewähltes Ziel mit den zugehörigen nächsten Schritten hervorheben. | Ein Ziel muss ausdrücklich zugeordnet sein; keine scheinbar objektive Priorisierung erfinden. |
| Stecktafel mit begrenzten Plätzen | Beispielsweise drei bewusst ausgewählte aktuelle Aufgaben darstellen. | Ergänzende Fokusansicht vorhandener Aufgaben; keine weitere Statusverwaltung. |

Materialwirkung und Bewegung dezent halten. Alle Ansichten müssen mit vorhandenen Schriftgrößen, Hell/Dunkel und Tastaturbedienung funktionieren. Reiter, Pinnwand und Instrumente sollen einzeln auswählbar sein, damit die Startseite übersichtlich bleibt.

## 8. Empfohlene nächste Reihenfolge

Angepasst am 12.09.2026 nach der [Entscheidung zu Systembenachrichtigungen](../01_Repository/Glide/docs/decisions/SYSTEMBENACHRICHTIGUNGEN.md):

1. Lokale Erinnerungsstufe 3.8.0 nativ abnehmen.
2. ~~Stufe A der Zustellung umsetzen~~ – **umgesetzt und automatisiert abgenommen am 12.09.2026**: Aufmerksamkeit über Taskleiste beziehungsweise Dock bei laufender App, abschaltbar und ohne Fokusdiebstahl. Die Sichtabnahme auf beiden Plattformen steht noch aus.
3. Reiteransicht – **umgesetzt in 3.10.0**, [Bedienvertrag](../01_Repository/Glide/docs/32_REITERANSICHT.md) liegt vor; sie hängt an keiner Paketierung.
4. Erste Pinnwand für dieselben Listenelemente – **umgesetzt in 3.10.0**. Weitere Optionen separat bewerten.
5. Stufe B – echte Systembenachrichtigungen – gemeinsam mit Installer und Signierung planen, nicht davor.
6. Schnellerfassung und gespeicherte Filter – **umgesetzt in 3.11.0**; Fristvorschau, Referenzprüfung, Rollback und GUI-Bedienung sind automatisiert geprüft.
7. Bewusste Tagesauswahl – **umgesetzt in 3.12.0** als „Mein Tag“; listenübergreifende Referenzen, Tageswechsel und Erledigungsstatus sind automatisiert geprüft.
8. Tabellenansicht für kompakte Mehrfachbearbeitung – **umgesetzt in 3.13.0**; Filter, Punktaktionen und Spaltenpersistenz sind automatisiert geprüft.

9. Bearbeitungstag und Aufwand – **umgesetzt in 3.14.0**.

10. Tagesplanung und Tageskapazität – **umgesetzt in 3.15.0**; Rechenregeln, Grenzwerte, Ansicht, Filter, Punktaktionen, Serien und Dialoge sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/39_KAPAZITAET_UND_TAGESPLANUNG_3.15.0.md).

11. Vollständiges App-Backup mit Inhaltsvorschau – **umgesetzt in 3.16.0**; Archivaufbau, Rundlauf, Vorschauwerte, ungültige Archive, Teilbereiche, Rückfallsicherungen und Dialoge sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/40_APP_BACKUP_3.16.0.md).

12. Druck- und PDF-Ausgabe – **umgesetzt in 3.17.0**; alle vier Formate, Escaping, Optionen, Mengen, Obergrenze, Dateischreibung und Dialoge sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/41_DRUCK_UND_PDF_3.17.0.md).
16. Kalenderimport aus ICS – **umgesetzt in 3.21.0**; Rundlauf mit Duplikaterkennung, Parser, Zeitzonen, Dauerangaben, Wiederholungsregeln, Erinnerungen, Übersprungsgründe, Zeitraumfilter, Grenzen, Ziele, Rückgängig und Dialog sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/45_KALENDERIMPORT_3.21.0.md). Nächste offene Ausbaustufen: benutzerdefinierte Felder und eigene Ansichten je Feld.
15. Kalenderausgabe als ICS – **umgesetzt in 3.20.0**; vier Umfänge, Termintypen, Dauerregeln, Optionen, Wiederholungen, Alarme, Format, stabile UIDs, Grenzen und Dialog sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/44_KALENDERAUSGABE_3.20.0.md). Nächste offene Ausbaustufen: benutzerdefinierte Felder, eigene Ansichten je Feld und ein Kalenderimport.
14. Dauerhafter Änderungsverlauf – **umgesetzt in 3.19.0** mit Aufgabenformat 15; Migration, alle erfassten Vorgänge, Sammeleinträge, Obergrenze, Backups, defekte Verlaufsfelder, Abschaltung, Leeren, Filter und Dialog sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/43_AENDERUNGSVERLAUF_3.19.0.md). Nächste offene Ausbaustufen: benutzerdefinierte Felder und eigene Ansichten je Feld.
13. CSV-Import mit Spaltenzuordnung – **umgesetzt in 3.18.0**; Erkennung von Trennzeichen und Kodierung, Spaltenzuordnung mit Vorbelegung, Vorschau, Werteregeln, Verschachtelung, beide Importziele, Grenzen, Importbericht und Rückgängig sind automatisiert geprüft. [Bedienvertrag](../01_Repository/Glide/docs/42_CSV_IMPORT_3.18.0.md). Nächste offene Ausbaustufen: dauerhafter Änderungsverlauf und benutzerdefinierte Felder.

Native Bedienung, Barrierefreiheit, Datenmigration, Wiederherstellung und Pflege der Arbeitskopie begleiten jeden Ausbauschritt. Größere Funktionen sollten vorhandene Daten- und Bedienlogik wiederverwenden; neue Architekturteile nur mit konkret belegtem Nutzen einführen.

## 9. Vergleichsquellen

Offizielle Quellen, im Gespräch am 11.09.2026 herangezogen. Tarif- und Plattformunterschiede sind bei späterer Planung erneut zu prüfen.

- Todoist: natürliche Datumseingabe, Ansichten und Trennung von geplantem Datum und Deadline: [Einstieg](https://www.todoist.com/help/todoist/get-started/get-started-with-todoist-OgNNJR). Gespeicherte Abfragen: [Filter](https://www.todoist.com/help/todoist/features/introduction-to-filters-V98wIH).
- Microsoft To Do: bewusst zusammengestellte Tagesauswahl: [My Day and suggestions](https://support.microsoft.com/en-us/todo/my-day-and-suggestions).
- Microsoft Planner: Premium-Funktionen wie Abhängigkeiten, Meilensteine und benutzerdefinierte Felder: [Advanced capabilities](https://support.microsoft.com/en-us/planner/teams/advanced-capabilities-with-premium-plans-in-planner).
- Google Keep: Notizen, Listen sowie Organisation mit Labels, Farben und angehefteten Inhalten: [How to use Google Keep](https://support.google.com/keep/answer/2888240?hl=en-GB).
