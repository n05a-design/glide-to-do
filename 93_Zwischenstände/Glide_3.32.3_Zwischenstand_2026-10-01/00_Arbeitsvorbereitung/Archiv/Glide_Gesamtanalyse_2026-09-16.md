# Glide – Aufgaben und Listen
## Vollständige Projekt-, Produkt- und Wettbewerbsanalyse

**Stand der Analyse: 16.09.2026**  
**Aktueller dokumentierter Produktstand: Glide 3.21.4**  
**Aufgaben-/Datenformat: 15 · Einstellungen: 2 · Vorlagenformat: 2**

---

# 1. Gesamturteil

Glide ist im aktuellen Stand keine frühe To-do-App mehr, sondern ein bereits umfangreicher **lokaler Desktop-Aufgaben- und Planungsmanager** mit eigener Planungslogik, mehreren Ansichten desselben Datenbestands, Vorlagen- und Workflow-System, lokalen Anhängen, Erinnerungen, Kalenderimport und -export, Änderungsverlauf, robustem Backup-/Migrationskonzept und einer ungewöhnlich umfangreichen internen Qualitätssicherung.

Die funktionale Entwicklung ist dabei **weiter fortgeschritten als die eigentliche Produktveröffentlichung**.

Der vollständige Abschlusslauf für 3.21.4 wurde am 15.09.2026 auf macOS mit Python 3.14.5 erfolgreich durchgeführt: 39 Prüfschritte, davon 37 ausgeführt, alle 25 Testsuiten, drei Analysen sowie Beispiel- und Releasedatenabgleiche bestanden. Übersprungen wurden ausschließlich die plattformgebundene Screenshot-Erzeugung und die menschliche Sichtprüfung.

Damit sind die verbleibenden Hauptprobleme **nicht mehr fehlende Kernfunktionen**. Sie liegen inzwischen hauptsächlich bei:

- nativer Windows- und visueller Plattformabnahme,
- Packaging und Distribution,
- Signierung und Notarisierung,
- endgültiger Produkt-/Plattformidentität,
- Marken- und Lizenzentscheidung,
- Endnutzer-Onboarding,
- Langzeit-/Performance-Nachweisen,
- und der technischen Wartbarkeit des stark gewachsenen Anwendungskerns.

Glide befindet sich deshalb in einer Übergangsphase:

> **vom umfangreich entwickelten und gut geprüften Quellprojekt zum installierbaren, nativ abgenommenen und vermarktbaren Desktopprodukt.**

---

# 2. Was die zuletzt gefundenen Dateien zusätzlich verändern

Die drei zuletzt gefundenen Dokumente verändern den aktuellen Funktionsstand kaum, aber sie verbessern die **Entwicklungshistorie und Anforderungsnachverfolgung** deutlich.

## 2.1 Ursprünglicher Funktionsauftrag ist nachvollziehbar

`25_FEATURE_ABGLEICH_3.7.0.md` dokumentiert den früheren Auftrag mit **22 einzelnen Anforderungen** und ordnet ihnen Umsetzung und Nachweise zu. Dazu gehören unter anderem Navigation, Farben, Listen-/Ordnerdialoge, lokale Schriftressourcen, Datenordner und Sperrdatei, Vorlagen, Export, Personalisierung, Jahresanzeige und Materialoptik.

Das ist relevant, weil Glide damit nicht als ungeplant gewachsene Ansammlung von Features einzuordnen ist. Ein erheblicher Teil der Oberfläche und Datenfunktionen entstand aus einem dokumentierten Anforderungskatalog.

Das historische Dokument trennt außerdem sauber zwischen tatsächlich umgesetzten Funktionen und bloß bewerteten Ideen. Frei wählbares Datumsformat, Kachelreihenfolge, Standardliste und Begrüßungston waren beispielsweise Erweiterungsideen; weitere analoge Anzeigeelemente wurden bewertet, aber ausdrücklich nicht umgesetzt.

## 2.2 Die Reiterfunktion hat eine klare Produktentscheidung

Der historische Reiterentwurf dokumentiert eine wichtige Entscheidung:

**Reiter werden vom Nutzer gezielt für vorhandene Punkte geöffnet. Gruppen werden nicht automatisch zu Reitern.**

Ein Reiter ist nur eine weitere Sicht auf dasselbe Objekt. Es entstehen keine Kopie, kein neuer Status und keine parallele Datenhaltung.

Das passt zu einem zentralen Architekturprinzip von Glide:

> **Mehrere Ansichten – ein Datenobjekt.**

Auch offene Reiter gehören deshalb nicht zu den Aufgabendaten, sondern zum persönlichen Ansichtszustand in `settings.json`.

## 2.3 Die Dokumentationspflege ist historisch nachvollziehbar

Der zusätzliche Dokumentationsabgleich zeigt, dass ältere technische Fassungen nicht einfach überschrieben wurden. Überholte Dokumente wurden archiviert, historische Nachweise erhalten und aktuelle Einstiege auf einen kanonischen Dokumentationspfad umgestellt.

Das bestätigt die inzwischen erkennbare Dokumentationsstrategie:

**Aktuelle Dokumente werden fortgeschrieben. Historische Funktions-/Versionsverträge bleiben eingefrorene Nachweise.**

---

# 3. Produktdefinition

Die Projektdokumentation definiert Glide aktuell als:

> eine deutschsprachige lokale Desktop-Anwendung für Aufgaben, Listen und Ordner, deren Kernfunktionen kein Internet, Benutzerkonto oder Cloudservice benötigen.

Diese Definition ist wichtiger als einzelne Features, weil daraus die Produktgrenzen folgen.

## Zielrichtung

Glide ist primär:

**persönliches Aufgabenmanagement + Tagesplanung + visuelle Organisation + lokale Datenhaltung.**

Es ist aktuell ausdrücklich **kein**:

- Team-Projektmanagementsystem,
- Cloudservice,
- kollaborativer Workspace,
- vollständiger Wissensmanager,
- Rich-Text-Notizeditor,
- Mail-Client,
- Kalender-Synchronisationsdienst,
- oder SaaS-Dienst mit Konto-/Lizenzserver.

Mehrbenutzerbetrieb, Konfliktzusammenführung, eigener Cloudservice, Telemetrie, Mehrsprachigkeit, externe Mail-/Kalenderintegration, Rich Text und Push bei geschlossener App sind aktuell dokumentierte Produktgrenzen.

Das ist bei der Konkurrenzanalyse wichtig:

**Nicht jede fehlende Konkurrenzfunktion ist automatisch ein Entwicklungsdefizit.**

---

# 4. Technischer Aufbau und Projektbestand

Der aktuelle Anwendungskern liegt in:

`src/glide/app.pyw`

Die Anwendung verwendet Python, Tk/Tcl und die Standardbibliothek. Die mitgelieferte DejaVu-Sans-Familie wird privat innerhalb des Prozesses registriert und nicht systemweit installiert.

## Projektbestand lässt sich in sieben Ebenen gliedern

### Anwendung

- `app.pyw`
- Ressourcen
- Schriftdateien
- Vorlagenkatalog

### Nutzerdaten

- Aufgabenbestand
- Einstellungen
- Vorlagen
- Anhänge
- Backups
- Lock-Datei
- Datenordner-Zeiger

### Aktuelle technische Dokumentation

Unter anderem:

- Produktgrenzen
- Architektur
- Startkontext
- QA-Testplan
- Daten-/Backup-/Migrationsvertrag
- QA-Bericht
- Projektübergabe
- Release-Checkliste
- Dokumentationsindex

### Versionierte Funktionsverträge

Von Erinnerungen über Reiter/Pinnwand, Tagesplanung, Backup und CSV bis zu ICS-Import/-Export.

### Historisches Archiv

Ältere Bestandsanalysen, Abschlussberichte, Featureabgleiche und Versionsdokumente bleiben als Nachweise erhalten.

### QA- und Analysewerkzeuge

Unter anderem:

- `pruefen.py`
- `analyse_statisch.py`
- `analyse_erreichbarkeit.py`
- `standpruefung.py`
- `dauerlauf.py`
- `leistungspruefung.py`
- `screenshots.py`
- `symbolpruefung.py`

### Reproduzierbare Projektbestände

- Beispielbestand
- Vorlagenbestand
- Release-Arbeitsbestand
- Referenz-Fixtures verschiedener Datenformate

Das Repository ist damit **deutlich strukturierter als der eigentliche Produktionscode**.

---

# 5. Daten- und Objektmodell

Glide arbeitet mit einem klaren hierarchischen Modell.

## Ordner

Ordner strukturieren **Listen und weitere Ordner**.

Maximal sind fünf Ordnerebenen vorgesehen.

## Listen

Listen enthalten die eigentlichen Punkte.

## Aufgaben

Normale ausführbare Punkte mit Eigenschaften wie:

- erledigt,
- Wichtigkeit,
- Fälligkeit,
- Fälligkeitszeit,
- Wiederholung,
- Benachrichtigung,
- Bearbeitungstag,
- Aufwand,
- Labels,
- Farbe,
- Beschreibung,
- Anhänge.

## Long-Tasks

Long-Tasks sind mehrzeilige, notizähnliche Punkte, bleiben aber Teil des Aufgabenmodells.

## Gruppen

Gruppen organisieren Punkte innerhalb einer Liste.

Sie sind ein Container und selbst keine erledigbare Aufgabe.

## Überschriften

Überschriften sind reine visuelle Gliederungselemente.

Die interne Produktregel lässt sich daher sehr einfach ausdrücken:

> **Aufgaben ordnet die Gruppe; Listen ordnet der Ordner.**

Diese semantische Trennung ist für das spätere Onboarding besonders wichtig.

---

# 6. Aktueller Funktionsumfang

## Aufgabenmanagement

Umgesetzt sind unter anderem:

- Aufgaben
- Unterpunkte
- Long-Tasks
- Gruppen
- Überschriften
- Fälligkeiten
- Uhrzeiten
- sechs Wiederholungsarten
- Wichtigkeiten
- Labels
- Farben
- Beschreibungen
- lokale Anhänge
- Mehrfachauswahl
- Drag-and-drop
- Suche
- Offen-Filter
- Rückgängig
- Papierkorb
- Änderungsverlauf

---

# 7. Planungssystem – eine der stärksten Produktideen

Besonders relevant ist die Trennung von drei verschiedenen Konzepten.

## Fälligkeit

Die Fälligkeit beantwortet:

> **Bis wann muss etwas erledigt sein?**

Sie ist die eigentliche Deadline.

## Bearbeitungstag

Seit 3.14 besitzen Aufgaben und Long-Tasks zusätzlich einen freiwilligen `planned_date`.

Der Bearbeitungstag beantwortet:

> **Wann möchte ich daran arbeiten?**

Ein Bearbeitungstag kann ausdrücklich ohne Fälligkeit existieren.

## Mein Tag

„Mein Tag“ ist wiederum eine **bewusst zusammengestellte Auswahl**.

Geplante Aufgaben werden nicht automatisch in „Mein Tag“ übernommen.

Damit existieren drei getrennte Ebenen:

**Deadline → Planung → persönlicher Fokus**

Das ist produktseitig wesentlich klarer als ein einziges universelles Datumsfeld.

## Geschätzter Aufwand

Seit 3.14 können Aufgaben zusätzlich einen Aufwand zwischen 1 und 60.000 Minuten erhalten.

## Tageskapazität

3.15 ergänzt daraus die Tagesplanung und eine persönliche Tageskapazität.

Die Bilanz wird aus dem aktuellen Bestand berechnet und nicht separat gespeichert.

Dadurch nähert sich Glide einem persönlichen Workload-Planner an, ohne daraus ein komplexes Ressourcenmanagementsystem zu machen.

---

# 8. Ansichten

Ein wichtiges Prinzip lautet:

> **Ansichten referenzieren vorhandene Objekte, statt parallele Aufgabenbestände anzulegen.**

Das betrifft unter anderem:

- Listenansicht
- Tabellenansicht
- Reiter
- Pinnwand
- In Bearbeitung
- Verspätet
- Labels
- gespeicherte Filter
- Mein Tag
- Tagesplanung

## Reiter

Aufgabe, Long-Task oder Gruppe können als Reiter geöffnet werden.

Maximal zwölf Punktreiter bleiben gleichzeitig geöffnet; beim dreizehnten wird der am längsten unbenutzte geschlossen.

## Pinnwand

Punkte können in Listen- oder Ordnerpinnwänden als Karten dargestellt werden.

Dabei bleiben sie dieselben Aufgabenobjekte. Bis zu 500 Karten je Pinnwand sind dokumentiert.

## Tabellenansicht

Die Tabelle bildet verschachtelte Aufgaben flach ab und besitzt listenspezifische Spalten.

## Gespeicherte Filter

Filter sind gespeicherte Ansichtsdefinitionen, keine Datenkopien.

Dieses Konzept ist konsistent und sollte auch bei zukünftigen Funktionen beibehalten werden.

---

# 9. Erinnerungen und Benachrichtigungen

Glide besitzt seit 3.8 lokale Erinnerungen.

Möglich sind unter anderem:

- zur Fälligkeit,
- 10 Minuten vorher,
- eine Stunde vorher,
- einen Tag vorher,
- eigener Minutenabstand,
- fester einmaliger Zeitpunkt.

Aufgaben und Long-Tasks unterstützen Erinnerungen; Gruppen und Überschriften nicht.

Die Anwendung prüft im laufenden Zustand alle 15 Sekunden.

## Stufe A – vorhanden

Wenn Glide läuft, aber verdeckt oder minimiert ist, kann Taskleiste beziehungsweise Dock Aufmerksamkeit anfordern, ohne den Fokus zu stehlen.

## Stufe B – geplant

Eine echte native Systembenachrichtigung unter dem Namen Glide ist an Packaging gebunden.

Dazu werden unter Windows eine stabile AppUserModelID und unter macOS ein echtes `.app`-Bundle mit Bundle-Identifier benötigt.

## Stufe C – bewusst nicht umgesetzt

Ein separater Hintergrund-/Autostartprozess für Meldungen bei vollständig geschlossener App ist derzeit ausdrücklich ausgeschlossen.

Grund ist nicht fehlendes Know-how, sondern das Risiko eines zweiten Prozesses auf derselben lokalen beziehungsweise extern synchronisierten Datenablage. Datenintegrität hat hier bewusst Vorrang.

Diese Architektur sollte im Marketing korrekt dargestellt werden.

---

# 10. Vorlagen und Workflows

Die Vorlagenfunktion ist inzwischen ein wesentlicher Bestandteil und nicht nur ein Nebenfeature.

Aktuell existieren **16 Praxisvorlagen**.

## Listenbasierte Vorlagen

Unter anderem:

- Tagesplanung
- Projektstart
- Einkauf
- Wochenplanung
- Besprechung
- Reise
- Einarbeitung
- Veröffentlichung
- Haushalt
- Rückblick

## Ordner-/Projektvorlagen

Unter anderem:

- Projekt
- Veranstaltung
- Immobilienvermarktung
- WordPress-Relaunch
- WEG-Verwaltung
- Baukommunikation

Die Vorlage „Einarbeitung“ enthält beispielsweise Aufgaben wie Arbeitsplatz und Zugänge vorbereiten und beschreibt damit das **Onboarding einer Person**, nicht das Onboarding in Glide selbst.

Der Vorlagenkatalog unterstützt deutlich mehr als leere Checklisten:

- Beschreibungen,
- Labels,
- Phasen,
- Gruppen,
- Überschriften,
- Unterpunkte,
- Long-Tasks,
- Fristen,
- teilweise Bearbeitungstage,
- Aufwände,
- Wiederholungen,
- Anhänge,
- verschachtelte Ordnerstrukturen.

Das macht die Vorlagen zu einem echten **Workflow-Starter-System**.

---

# 11. Note-Taking-Fähigkeiten

Glide besitzt inzwischen durchaus Notizfunktionen, ist aber **kein vollständiges PKM- oder Note-Taking-System**.

## Vorhanden

Notizkontext kann über:

- Aufgabenbeschreibungen,
- Long-Tasks,
- Listenbeschreibungen,
- Ordnerbeschreibungen,
- Anhänge,
- Besprechungsvorlagen,
- Reiter,
- Pinnwände

abgebildet werden.

Das reicht gut für:

- Briefings,
- kurze Protokolle,
- Arbeitsnotizen,
- Entscheidungsnotizen,
- Aufgabenhintergrund,
- projektnahes Referenzmaterial.

## Nicht vorhanden

Im vorliegenden Produktmodell fehlen bewusst beziehungsweise derzeit:

- echter Rich-Text-Editor,
- frei verlinkte Wissensseiten,
- Backlinks,
- Knowledge Graph,
- Block-Editor,
- eingebettete Datenbanken,
- Web Clipper,
- OCR-/Dokumentsuche,
- umfangreiche Mediennotizen,
- Notizversionierung,
- Plugin-Ökosystem.

### Einordnung

Glide sollte daher nicht als „Notion-/Obsidian-Ersatz“ positioniert werden.

Besser:

> **Task-Manager mit starkem Arbeitskontext und leichten Notizfunktionen.**

---

# 12. Datenhaltung

Die Nutzdaten sind vom Programm getrennt.

Dokumentiert sind unter anderem:

| Bestandteil | Zweck |
|---|---|
| `liste_speicher.json` | Listen, Ordner, Aufgaben, Labels, Papierkorb, Verlauf usw. |
| `settings.json` | persönliche Einstellungen und UI-Zustände |
| `vorlagen.json` | eigener Vorlagenkatalog |
| `attachments/` | lokale Anhänge |
| `backups/` | Sicherungen |
| `glide.lock` | lokale Belegungssperre |
| `datenordner.json` | gerätebezogener Ablagezeiger |

Plattformabhängig wird ein Benutzer-Datenordner verwendet; für Tests überschreibt `GLIDE_DATA_DIR` den Pfad.

Glide greift für seine Kernfunktionen weder auf ein Benutzerkonto noch auf einen eigenen Server zu.

---

# 13. Datenformat 15

Das aktuelle Aufgabenformat ist **15**.

Die Evolutionslogik ist bemerkenswert konservativ.

## Format 14

3.14 ergänzte:

- `planned_date`
- `estimated_minutes`

## Format 15

3.19 ergänzte den dauerhaften Änderungsverlauf.

Ein vereinfachtes Modell sieht konzeptionell so aus:

```text
Glide-Datenbestand
├── version = 15
├── folders
├── lists
│   └── items
├── labels
├── trash
├── active references
└── history
```

Ein Aufgabenelement kann unter anderem enthalten:

```text
text
done
importance
due
due_time
repeat
reminder
planned_date
estimated_minutes
kind
color
labels
description
attachments
children
```

Der Verlauf liegt getrennt daneben.

## Migrationsprinzip

Vor einem Formatsprung wird eine unveränderte Originalkopie angelegt.

Beispielsweise:

`liste_vor_format15_<Zeitstempel>.json`

Scheitert diese Sicherung, wird der ältere Bestand nicht überschrieben.

Das ist für eine lokale Desktopanwendung ein solides Sicherheitsprinzip.

---

# 14. Änderungsverlauf

Das Datenformat 15 besitzt einen persistenten Verlauf mit maximal 4.000 Einträgen.

Er kann unter anderem Vorgänge wie:

- angelegt,
- geändert,
- erledigt,
- wieder geöffnet,
- verschoben,
- umbenannt,
- Papierkorb,
- Wiederherstellung,
- endgültig entfernt

erfassen.

Wichtig:

Der Verlauf ist **kein vollständiges Version-Control-System**.

Er speichert beispielsweise nicht die alten vollständigen Feldinhalte und bietet keine Wiederherstellung einer früheren Punktversion.

Undo und Verlauf sind bewusst getrennt. Ein Undo verändert den Bestand erneut und erzeugt entsprechend einen weiteren Verlaufsvorgang.

---

# 15. Automatisches Speichern und lokale Sicherungen

Im Anwendungscode sind mehrere Schutzebenen erkennbar:

- Autosave: **alle 5 Minuten**
- mindestens 10 Sicherungen behalten
- maximal 40 automatische JSON-Sicherungen
- frühestens nach 120 Sekunden erneut sichern
- zeitbezogene Backuprotation

Diese lokale Sicherung ist von den exportierbaren Backups zu unterscheiden.

---

# 16. Portable Aufgabenbackups

`.glidebackup` ist technisch ein ZIP-Archiv aus:

- `data.json`
- referenzierten Anhängen.

Das System prüft unter anderem Archivpfade, Größen und Datenstruktur.

Dokumentierte Sicherheitsgrenzen umfassen:

- bis 512 MiB je Anhang,
- maximal 2 GiB entpackte Daten,
- maximal 32 MiB Daten-JSON,
- technisches Validierungslimit 200.000 Punkte,
- maximale Punkttiefe 100.

Diese Grenzwerte sind technische Sicherheitsgrenzen und ausdrücklich keine Performancezusage.

---

# 17. Vollständiges App-Backup

Seit 3.16 gibt es zusätzlich `.glideapp`.

Dieses Archiv erweitert das normale Aufgabenbackup um:

- persönliche Einstellungen,
- Vorlagen,
- Aktivitätsdaten.

Vor einer Wiederherstellung zeigt Glide eine Inhaltsvorschau mit Version, Datenformat und Mengen an. Einzelne Bereiche lassen sich getrennt auswählen.

Vor dem Ersetzen entstehen wiederum Rückfallsicherungen für:

- Aufgaben,
- Einstellungen,
- Vorlagen.

## Grenzen des Backup-Konzepts

Nicht vorhanden sind derzeit:

- automatisches Offsite-Backup,
- Cloudbackup,
- Backup-Zeitplan,
- Zusammenführen zweier vollständiger Bestände,
- Passwortschutz,
- Backupverschlüsselung,
- interne Versionsgeschichte innerhalb eines Archivs.

### Bewertung

Das lokale Backupkonzept ist **für eine Desktop-App bereits ungewöhnlich ausgereift**.

Was fehlt, ist weniger eine weitere lokale Backupfunktion als ein verständliches Konzept für:

> **„Was passiert, wenn der gesamte Computer ausfällt?“**

---

# 18. Extern synchronisierte Datenordner

Glide darf seinen Datenordner in einem extern synchronisierten Ordner verwenden.

Das ist aber ausdrücklich **keine Glide-Synchronisierung**.

Die Lock-Datei kann nicht verhindern, dass auf zwei Geräten jeweils eine noch nicht synchronisierte Kopie gleichzeitig verändert wird.

Der vorgesehene Ablauf ist deshalb:

**Glide schließen → Synchronisierung vollständig abwarten → auf anderem Gerät öffnen.**

Glide bietet aktuell:

**dateibasierte Portabilität**

statt

**verteilte Synchronisation mit Konfliktauflösung**.

---

# 19. Import und Export

## TXT und Markdown

Geeignet als lesbare Austauschformate.

Nicht als verlustfreier vollständiger Rückweg gedacht.

## CSV

3.18 bringt einen umfangreichen CSV-Import:

- Erkennung von Trennzeichen,
- Erkennung verschiedener Kodierungen,
- Spaltenzuordnung,
- Vorschau,
- Verschachtelung,
- Rückgängig,
- Import in verschiedene Ziele.

Grenzen:

- kein XLSX,
- keine Anhänge aus einer Spalte,
- keine Erinnerungen/Wiederholungen aus einer Spalte,
- kein Abgleich mit vorhandenen Aufgaben,
- keine gespeicherten Mappingprofile,
- maximal 5.000 Zeilen,
- 64 Spalten,
- 12 MB.

## Drucken/PDF

Glide erzeugt HTML und übergibt den eigentlichen Druck beziehungsweise die PDF-Ausgabe an die Betriebssystem-/Browserfunktion.

Das vermeidet eine eigene PDF-Laufzeitabhängigkeit.

---

# 20. Kalenderexport und -import

## ICS-Ausgabe

Seit 3.20 kann Glide Kalenderdateien erzeugen.

Es handelt sich ausdrücklich um eine **Dateiausgabe**, nicht um eine Kalenderverbindung.

Kein:

- Konto,
- Abonnement,
- automatischer Rückweg,
- laufender Sync.

Auch Punkte ohne Fälligkeit können bei aktivierter Planungsoption über ihren Bearbeitungstag als Planungstermin ausgegeben werden.

## ICS-Import

3.21 liest eine vom Nutzer gewählte ICS-Datei.

Eigene Glide-UIDs werden beim Rundlauf wiedererkannt und nicht doppelt angelegt. Fremde UIDs werden dagegen nicht dauerhaft gespeichert; dieselbe fremde Kalenderdatei zweimal zu importieren kann entsprechend doppelte Aufgaben erzeugen.

Grenzen:

- maximal 2.000 Termine,
- maximal 12 MB,
- keine Kalender-Synchronisierung,
- keine Teilnehmer,
- keine Anhänge,
- keine EXDATE-Ausnahmen,
- keine VTODO/VJOURNAL-Objekte,
- keine importierten VTIMEZONE-Definitionen.

---

# 21. Oberfläche und Bedienkonzept

Glide hat sich stark von einer einfachen Tk-Liste entfernt.

## Zentrale Oberflächenbereiche

Unter anderem:

- Startseite
- Vorlagen
- Listen/Ordner
- In Bearbeitung
- Mein Tag
- Tagesplanung
- Labels
- Verspätet
- Papierkorb
- Kalender

## Personalisierung

Dokumentiert beziehungsweise umgesetzt sind:

- Hell-/Dunkelmodus
- Akzentfarbe
- drei Schriftgrößen
- Startansicht
- Wochenbeginn
- Sekundenanzeige
- Mondphase
- Jahres-/Aktivitätsanzeige
- Materialoptik
- persönlicher Name/Monogramm
- Tagesziel
- Tageskapazität

---

# 22. Onboarding

Hier muss zwischen **Entwickler-Onboarding** und **Endnutzer-Onboarding** unterschieden werden.

## Entwickler-Onboarding: stark

Bereits vorhanden sind:

- `03_STARTKONTEXT.md`
- Architektur
- Projektübergabe
- Datenvertrag
- QA-Bericht
- Dokumentationsindex
- Release-Checkliste

Für die Weiterentwicklung ist das inzwischen gut.

## Endnutzer-Onboarding: noch nicht ausreichend nachgewiesen

Im vorliegenden Bestand sehe ich dagegen **keinen dedizierten First-Run-Onboarding-Ablauf**.

Vorlagen und Beispieldaten helfen beim Einstieg, ersetzen aber kein Produkt-Onboarding.

### Sinnvoller First-Run-Ablauf

Ein sehr kurzes Glide-Onboarding sollte fünf Dinge erklären:

1. **Ordner → Listen → Gruppen → Aufgaben**
2. **Fälligkeit ≠ Bearbeitungstag ≠ Mein Tag**
3. **Listenansicht, Tabelle, Reiter und Pinnwand zeigen dieselben Aufgaben**
4. **Wo die Daten liegen und wie ein Backup erzeugt wird**
5. **Benachrichtigungen funktionieren nur entsprechend dem jeweiligen Betriebszustand**

---

# 23. Branding und Produktidentität

## Technische Produktidentität: weit entwickelt

`PRODUCT_IDENTITY.md` dokumentiert bereits:

- Produktname
- Version
- Datenformat
- Plattformpfade
- Backupformat
- Grenzen
- Sprache
- Schrift
- Symbole
- technische Identitäten

## Geschäftliche Markenidentität: noch offen

Noch nicht endgültig festgelegt sind unter anderem:

- Publisher/Herausgeber
- Copyright-Zeile
- Datenschutz-URL
- Lizenzmodell
- Preis/Monetarisierung
- Windows-AppUserModelID
- Inno-Setup-AppId
- macOS-Bundle-Identifier
- macOS-Mindestversion
- Zielarchitekturen
- Sicherheitskontakt
- professionelle Markenprüfung „Glide“

---

# 24. Positionierung und Markenversprechen

„Local-first“ alleine ist inzwischen kein ausreichendes Alleinstellungsmerkmal.

Glides tatsächliche Differenzierung liegt in der **Kombination**.

## Empfehlenswerte Positionierung

> **Glide ist ein ruhiger, task-first Desktop-Planer für Menschen, die ihre Arbeit bewusst planen und ihre Daten selbst besitzen wollen – ohne Konto- oder Cloudzwang.**

## Drei Markenpfeiler

### Planen

Fälligkeit, Bearbeitungstag, Mein Tag, Aufwand und Tageskapazität.

### Organisieren

Listen, Ordner, Gruppen, Labels, Filter, Tabelle, Reiter, Pinnwand und Vorlagen.

### Besitzen

Lokale Daten, kontrollierte Migration, portable Backups, keine Telemetrie und keine zwingende Cloud.

Eine mögliche kurze Markenformel wäre:

> **Planen. Ordnen. Besitzen.**

Oder:

> **Plane deinen Tag. Ordne deine Arbeit. Behalte deine Daten.**

---

# 25. Aktueller Konkurrenzvergleich – Aufgabenmanagement

## Todoist

Todoist ist stark bei Cloud-Sync, Mobile, Teamfunktionen, Integrationen, natürlicher Sprache und Ökosystem.

Glide differenziert sich bei lokaler Datenhoheit, explizitem Backup-/Migrationsmodell, Trennung von Fälligkeit/Bearbeitungstag/Mein Tag, Tageskapazität und lokalen Ansichten.

## TickTick

TickTick ist funktional sehr breit und kombiniert Aufgaben, Kalender, Notizen, Habits, Pomodoro und weitere Produktivitätstools.

Glide sollte nicht versuchen, TickTick Feature für Feature nachzubauen.

## Microsoft To Do

Microsoft To Do ist deutlich einfacher, besitzt aber starke Microsoft-Integration und geräteübergreifende Synchronisation.

Glide ist strukturell und planungsseitig erheblich tiefer.

## Things

Things ist konzeptionell besonders relevant, weil es geplanten Start/„When“ und Deadline trennt.

Glide kann ein ähnliches Maß an Klarheit anstreben, kombiniert mit Windows-Unterstützung und lokaler Datenhoheit.

---

# 26. Aktueller Konkurrenzvergleich – Note-Taking und Wissensmanagement

## Notion

Notion ist Glide bei Dokumenten, Rich Text, Datenbanken, Relationen und Teamarbeit deutlich voraus.

Glide ist fokussierter bei persönlicher Aufgabenplanung und lokaler Kontrolle.

## Obsidian

Obsidian ist note-first und knowledge-first; Glide ist task-first und planning-first.

Glide sollte keinen Wissensgraphen- oder Plugin-Wettbewerb beginnen.

## Anytype

Anytype zeigt, dass „local-first“ allein kein ausreichender USP ist.

Glide sollte seine Stärke über Einfachheit, persönliche Planung und Transparenz definieren.

## Evernote

Evernote ist klar note-first und besonders stark bei Sammlung, Webrecherche und Dokumentablage.

Glide ist auf konkrete Arbeit, Planung und Tagesfokus ausgerichtet.

---

# 27. Zusammenfassende Wettbewerbsmatrix

| Bereich | Glide | Todoist | TickTick | Things | Notion | Obsidian | Anytype | Evernote |
|---|---|---|---|---|---|---|---|---|
| Aufgabenfokus | hoch | hoch | hoch | hoch | mittel/hoch | gering ohne Setup | mittel | mittel |
| Tagesplanung | hoch | hoch | hoch | sehr hoch | konfigurierbar | setupabhängig | konfigurierbar | mittel |
| Aufwand/Kapazität | integriert | Dauer vorhanden | stark | begrenzter | frei modellierbar | frei modellierbar | frei modellierbar | begrenzt |
| Notiztiefe | mittel | gering/mittel | mittel | gering/mittel | sehr hoch | sehr hoch | sehr hoch | sehr hoch |
| Lokale Datenhoheit | hoch | cloudzentriert | cloudzentriert | lokal möglich | cloudzentriert + Offline | sehr hoch | sehr hoch | cloudzentriert |
| Team/Kollaboration | nein | hoch | vorhanden | nein | sehr hoch | mit Zusatzdiensten | hoch | hoch |
| Mehrere Ansichten | hoch | hoch | hoch | mittel | sehr hoch | hoch | hoch | mittel |
| Mobile | nein | ja | ja | Apple | ja | ja | ja | ja |

---

# 28. Das tatsächliche Alleinstellungsmerkmal

Glide kombiniert:

1. **task-first statt workspace-first**
2. **Fälligkeit, Bearbeitungstag und Mein Tag als getrennte Konzepte**
3. **Aufwand und Tageskapazität**
4. **mehrere Sichten auf dieselben Aufgaben**
5. **umfangreiche Vorlagen**
6. **lokale Daten ohne Kontozwang**
7. **explizite Backup-/Migrationskontrolle**
8. **ruhige Desktopoberfläche**
9. **keine Telemetrie und keine zwingende Cloud**

Daraus ergibt sich:

> **Ein persönlicher Desktop-Planer, der nicht nur festhält, was erledigt werden muss, sondern auch wann du daran arbeiten willst – und bei dem deine Daten tatsächlich bei dir bleiben.**

---

# 29. Qualitätssicherung

Die interne QA ist mittlerweile eine der bemerkenswertesten Eigenschaften des Projekts.

Der vollständige Prüfplan umfasst 25 Testsuiten sowie Syntax-, Versions-, Dokument-, Fixture- und Analyseprüfungen und reproduziert zusätzlich Beispiel- und Releasedaten.

Hinzu kommen spezialisierte Werkzeuge für:

- statische Codeanalyse,
- Erreichbarkeitsanalyse,
- Dokumentationsstand,
- Screenshot-Erzeugung,
- Symbol-/Fontprüfung,
- Performance,
- Dauerbetrieb,
- Beispieldaten,
- Releasebestände,
- Vorlagen.

---

# 30. Noch nicht abgeschlossene Qualitätsnachweise

Offen sind weiterhin:

- native Windows-Prüfung,
- echte macOS-/Windows-Eingabegeräte,
- DPI und mehrere Monitore,
- Screenreader,
- Hochkontrast/RDP,
- physisches Schlafen/Aufwachen,
- Dock-/Taskleistenwirkung,
- Dauerlauf,
- real synchronisierte Datenordner.

Ein aktueller vollständiger Dauerlaufbericht und ein aktueller Performance-Baselinebericht liegen im vorliegenden Material nicht vor.

---

# 31. Architektur und technische Schulden

Die Architekturdatei bezeichnet `app.pyw` ausdrücklich als **kanonischen Python-/Tk-Monolithen**.

Die statische Analyse nennt für den Kern:

- 26.736 Zeilen,
- 953 Funktionen/Methoden,
- 253 Konstanten,
- 53 Funktionen mit mehr als 80 Zeilen.

Zusätzlich gibt es tiefe Verschachtelung und wiederkehrende Codeblöcke.

### Konsequenz

Der nächste technische Ausbau sollte nicht sofort weitere große Funktionspakete in denselben Monolithen schreiben.

Sinnvoll ist eine **stufenweise Konsolidierung**.

Kein Rewrite.

Keine gleichzeitige Änderung des Datenmodells.

Geeignete Extraktionsbereiche:

- Backup/Migration
- Import/Export
- Änderungsverlauf
- ICS
- große Dialoge
- gemeinsame UI-Helfer
- redundante Schema-Backupfunktionen

---

# 32. Umgesetzt, geplant, bewusst ausgeschlossen

## Umgesetzt

Unter anderem:

- Kern-Aufgabenmanagement
- verschachtelte Struktur
- Long-Tasks
- Gruppen/Überschriften
- Anhänge
- Labels
- Wiederholungen
- lokale Erinnerungen
- Dock-/Taskleistenaufmerksamkeit
- Reiter
- Pinnwand
- Schnellerfassung
- gespeicherte Filter
- Mein Tag
- Tabellenansicht
- Bearbeitungstag
- Aufwand
- Tageskapazität
- Tagesplanung
- vollständiges App-Backup
- Druck/PDF
- CSV-Import
- Änderungsverlauf
- ICS-Ausgabe
- ICS-Import
- 16 Praxisvorlagen
- umfangreiche Personalisierung

## Konkrete zukünftige Produktideen

- benutzerdefinierte Felder je Liste
- eigene Ansichten auf Basis dieser Felder
- größere Pinnwandfunktionen
- native Systembenachrichtigungen gemeinsam mit Packaging

## Bewusst derzeit ausgeschlossen

- eigener Cloudsync
- verteilte Konfliktauflösung
- Mehrbenutzerbetrieb
- Rich-Text-Editor
- Mehrsprachigkeit
- Mailintegration
- echte Kalendersynchronisierung
- Hilfsprozess für geschlossene App
- Telemetrie

---

# 33. Offene Entscheidungen

## Produkt und Geschäft

| Entscheidung | Status |
|---|---|
| Publisher/Herausgeber | offen |
| Copyright | offen |
| endgültige Supportstruktur | nicht vollständig finalisiert |
| Datenschutz-URL | offen |
| Lizenzmodell | offen |
| Preis | offen |
| Monetarisierung | offen |
| Vertriebskanäle | noch freizugeben |
| professionelle Markenprüfung | offen |

## Windows

- Zielarchitektur
- AppUserModelID
- Inno-Setup-AppId
- Installer
- Signierung

## macOS

- Bundle-Identifier
- Mindestversion
- Architektur
- Signierung
- Notarisierung

---

# 34. Fehlende Unterlagen beziehungsweise noch nicht nachgewiesene Ergebnisse

## Nicht mehr als fehlend anzusehen

Vorhanden sind inzwischen nachweislich:

- aktueller QA-Bericht
- QA-Testplan
- Architekturübersicht
- Produktgrenzen
- Daten-/Migrationsvertrag
- Dokumentationsindex
- Projektübergabe
- Release-Checkliste
- Produktidentitätsregister
- Systembenachrichtigungsentscheidung
- reproduzierbare Vorlagen
- Beispielbestand
- Release-Arbeitsbestand
- Codeanalyse

## Im vorliegenden Material noch nicht als abgeschlossen nachgewiesen

### Technische Nachweise

- aktueller nativer Windows-3.21.4-Gesamtlauf
- manuelle visuelle macOS-Abnahme
- manuelle visuelle Windows-Abnahme
- aktueller vollständiger Dauerlaufbericht
- aktueller Performance-Baselinebericht
- Screenreader-Abnahme
- Hochkontrast-Abnahme
- DPI-/Multi-Monitor-Testmatrix
- Sleep/Wake-Praxistest
- Clean-Machine-Installationsprüfung

### Packaging

- fertiger Windows-Installer
- fertiges macOS-App-Bundle
- reproduzierbare finale Packaging-Anleitung
- Signierungsnachweis
- Notarisierungsnachweis
- Upgrade-/Uninstall-Nachweis

### Produkt-/Rechtsunterlagen

- endgültige Datenschutzseite/-URL
- endgültiges Lizenzmodell
- Preis-/Monetarisierungsentscheidung
- endgültige Publisher-/Copyrightangaben
- Sicherheitskontakt
- Markenfreigabe

### Endnutzer

Im vorliegenden Dateisatz ist kein klarer abgeschlossener Nachweis für:

- First-Run-Onboarding
- kompakte Nutzer-Schnellstartanleitung
- nutzerorientierte Backup-/Recovery-Anleitung
- konsolidiertes Support-/Troubleshooting-Handbuch

---

# 35. Möglichkeiten

## 1. Eine Nische zwischen Things und Obsidian

**planungsorientierter als Obsidian, datenautonomer als Things.**

## 2. Windows + macOS als Chance

Ein ruhiger persönlicher Planer mit Windows-Unterstützung und lokaler Datenhoheit besitzt ein nachvollziehbares Profil.

## 3. Datenschutz und kleine Unternehmen

Die lokale Architektur kann für Anwender interessant sein, die Aufgaben und Projektkontext nicht zwingend in einen SaaS-Dienst legen wollen.

## 4. Branchenvorlagen

Vorlagen wie Immobilienvermarktung, WEG-Verwaltung, Baukommunikation und WordPress-Relaunch zeigen bereits den Nutzen realer Arbeitsabläufe.

## 5. Einfache Datenportabilität als Vertrauensargument

Backup, lokale Ablage und klare Migration lassen sich gut verständlich kommunizieren.

---

# 36. Herausforderungen

## Produktseitig

Die größte Gefahr ist Feature-Drift.

## Technisch

Der Monolith wächst.

## UX

Die Anzahl der Konzepte ist inzwischen erheblich.

## Release

Ein grüner Python-Quelltest ist noch kein installierbares Produkt.

## Branding

Der Name muss geklärt werden, bevor erhebliche Marketinginvestitionen entstehen.

---

# 37. Priorisierte nächste Aufgaben

## P0 – Releasefähigkeit nachweisen

1. Windows vollständig prüfen.
2. Native visuelle Abnahme.
3. Dauerlauf.
4. Performancebaseline.
5. Accessibility.

---

# 38. P0/P1 – Packaging

Danach:

1. Publisher festlegen
2. Markenfrage klären
3. Plattformidentitäten vergeben
4. Windows Installer bauen
5. macOS `.app` bauen
6. signieren
7. notarisierten Mac-Build erzeugen
8. Clean-Machine-Tests
9. Upgrade/Uninstall testen
10. native Systembenachrichtigungen Stufe B integrieren

---

# 39. P1 – Produktreife

## Endnutzer-Onboarding

Vor weiteren großen Features.

## Quick Start / Hilfe

Besonders:

- Datenordner
- Backup
- Restore
- Gruppen vs. Ordner
- Fälligkeit vs. Planung
- Benachrichtigungsgrenzen

## Kleiner Pilot

Ein begleiteter Pilottest mit wenigen geeigneten Einzelanwendern auf Windows und Mac wäre inzwischen wertvoller als weitere interne Features.

---

# 40. P2 – Technische Konsolidierung

Nach stabiler Releasebaseline:

- Modulgrenzen definieren
- Import/Export extrahieren
- Backup/Migration extrahieren
- History extrahieren
- große Dialoge zerlegen
- wiederkehrende UI-Helfer zusammenführen
- Erreichbarkeitskandidaten klassifizieren
- breit gefasste Exception-Behandlung überprüfen
- Duplikate abbauen

Dabei:

> **kein Big-Bang-Rewrite.**

---

# 41. P2/P3 – Neue Funktionen

Erst anschließend sollte entschieden werden, ob benutzerdefinierte Felder tatsächlich der nächste große Produktschritt werden.

Die strategische Frage lautet:

> **Soll Glide ein fokussierter persönlicher Planer bleiben oder zu einem konfigurierbaren Arbeitsdaten-System werden?**

Empfehlung:

**task-first bleiben.**

---

# 42. Gesamtbewertung

## Funktional

**weit fortgeschritten**

## Datenmodell

**klar und konservativ entwickelt**

## Backup

**stark**

## Dokumentation

**sehr stark für einen internen Entwicklungsstand**

## QA

**ungewöhnlich systematisch**

## Architektur

**funktional, aber wartungsintensiv**

## UI

**umfangreich und eigenständig**

## Onboarding

**Entwicklerseitig gut, endnutzerseitig noch klar verbesserungswürdig.**

## Branding

**technische Identität vorhanden; kommerzielle und rechtliche Markenidentität noch nicht abgeschlossen.**

## Note-Taking

**guter Aufgabenkontext, aber kein PKM-System.**

## Marktposition

Glide sollte **nicht über maximale Featurezahl** konkurrieren.

Sein sinnvollstes Profil ist:

> **ruhige persönliche Planung + visuelle Arbeitsorganisation + lokale Datenhoheit.**

---

# 43. Schlussfolgerung

Glide hat inzwischen eine belastbare eigene Produktidee.

Der Kern besteht aus einer interessanten Kombination:

**Deadline, Planungstag und Tagesfokus werden bewusst getrennt; Aufgaben können in mehreren Arbeitsansichten erscheinen, ohne dupliziert zu werden; Daten und Backups bleiben transparent lokal kontrollierbar.**

Die nächste Entwicklungsphase sollte deshalb nicht darin bestehen, möglichst schnell noch zehn weitere Features hinzuzufügen.

Die sinnvollste Reihenfolge lautet:

> **prüfen → paketieren → onboarden → pilotieren → konsolidieren → erst danach erweitern.**

Wenn diese Schritte sauber abgeschlossen werden, ist der nächste Engpass nicht mehr die Technik, sondern die Produktentscheidung:

> **Wie schmal und klar soll Glide langfristig bleiben?**

Genau darin liegt zugleich seine größte Chance.
