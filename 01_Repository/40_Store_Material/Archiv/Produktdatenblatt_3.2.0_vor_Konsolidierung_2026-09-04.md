# Glide – Produktdatenblatt

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

Alle Angaben in diesem Dokument sind aus dem Quellcode belegt. Sie sind die
gemeinsame Grundlage für Microsoft- und Apple-Formulare, für Website- und
Exposétexte. Was hier nicht steht, ist eine Geschäfts- oder Rechtsentscheidung
und liegt in `00_Arbeitsvorbereitung/Entscheidungen/`.

Vorgängerfassung: `Archiv/Produktdatenblatt_2.6.0.md`. Sie beschrieb einen
Stand ohne Labels, Papierkorb, Kalender, Long-Task und Zwischenüberschrift.

---

## Kurzbeschreibung

**Bis 100 Zeichen**
Aufgaben und Listen für den Desktop. Ohne Konto, ohne Cloud, alle Daten bleiben auf dem Gerät.

**Bis 250 Zeichen**
Glide verwaltet Aufgaben, verschachtelte Listen und Notizen direkt auf dem Rechner. Kein Benutzerkonto, keine Cloudpflicht, keine Werbung, keine Datenerhebung. Ordner, Gruppen, Labels, Fälligkeiten mit Uhrzeit, Anhänge, Papierkorb und ein Dunkelmodus sind eingebaut.

## Langbeschreibung

Glide ist eine schlanke Aufgaben- und Listen-App für Windows und macOS. Sie
startet ohne Anmeldung, arbeitet vollständig offline und legt jede Datei im
Benutzerordner des jeweiligen Systems ab. Es gibt keinen Server, keinen Account
und keinen Zwang zu einem Abonnement.

Aufgaben lassen sich verschachteln. Wer Struktur braucht, hat drei Mittel mit
klarer Aufgabenteilung: eine **Zwischenüberschrift** gliedert eine Liste optisch,
eine **Gruppe** fasst Punkte derselben Liste zusammen, und ein **Ordner** fasst
ganze Listen zusammen – bis zu fünf Ebenen tief. Ein **Long-Task** ist eine
Aufgabe, deren vollständiger Text über mehrere Zeilen sichtbar bleibt.

Ein fester Eingang nimmt auf, was noch nicht einsortiert ist. Zwei Ansichten
entstehen automatisch aus allen Listen: **In Bearbeitung** sammelt jede datierte
Aufgabe in zeitlicher Reihenfolge, **Verspätet** zeigt, was überfällig ist. Ein
**Kalender** stellt dieselben Fälligkeiten als Wochen- oder Monatsraster dar –
rein lokal, ohne Anbindung an einen externen Kalenderdienst.

Zu jeder Aufgabe gehören optional eine Fälligkeit mit freiwilliger Uhrzeit, eine
von vier Wichtigkeitsstufen, eine Farbe, mehrere **Labels**, ein längerer
Beschreibungstext und beliebig viele Dateianhänge. Anhänge werden als lokale
Kopie im Datenordner gespeichert, sodass die Aufgabe auch dann vollständig
bleibt, wenn die Originaldatei verschoben oder gelöscht wird.

Gelöschtes ist nicht fort: Punkte, Listen und Ordner wandern in einen
**Papierkorb** und kehren von dort an ihre alte Stelle zurück. Jede Aktion, die
Punkte umordnet, läuft unter einem Bestandswächter, der vor und nach der Aktion
alle Punkte zählt und bei einer Lücke den vorherigen Stand herstellt.

Für den Austausch gibt es Export als TXT, Markdown und CSV, Import aus TXT sowie
ein vollständiges, portables Backup, das die Anhänge einschließt. Automatische
Sicherungen laufen im Hintergrund mit.

## Funktionsliste

**Struktur**

- Verschachtelte Aufgaben, technisch bis 100 Ebenen
- Vier Punktarten: Aufgabe, Gruppe, Long-Task, Zwischenüberschrift
- Listen und Ordner; Ordner ineinander bis fünf Ebenen tief
- Geschützter Eingang für Unsortiertes

**Aufgaben**

- Fälligkeitsdatum mit freiwilliger Uhrzeit, Hervorhebung von heute und überfällig
- Vier Wichtigkeitsstufen
- Sieben Farben für Aufgaben, Listen und Ordner
- Labels mit eigener Farbe an Punkten, Listen und Ordnern
- Beschreibungstext für Aufgaben, Listen und Ordner
- Dateianhänge als verwaltete lokale Kopie, bis 512 MB je Datei

**Ansichten**

- Abgeleitete Ansichten „In Bearbeitung“ und „Verspätet“ über alle Listen
- Kalender als Wochen- oder Monatsraster
- Ordnerübersicht
- Papierkorb mit Wiederherstellung an die ursprüngliche Stelle
- Volltextsuche über Titel, Beschreibung, Anhangsnamen, Status und Datum
- Filter „Nur offene Punkte“

**Bedienung**

- Drag & Drop für Reihenfolge, Verschachtelung und Verschieben zwischen Listen
- Mehrfachauswahl, Rückgängig über 20 Schritte, Kopieren und Einfügen
- Umbenennen von Listen und Ordnern direkt in der Seitenleiste
- Kontextmenüs auf allen Oberflächen
- Tastaturbedienung mit plattformgerechten Kürzeln
- Hell- und Dunkelmodus

**Daten**

- Export: TXT, Markdown, CSV · Import: TXT
- Portables Komplettbackup einschließlich Anhänge (`.glidebackup`)
- Automatische Sicherungen der letzten 40 Stände
- Bestandswächter gegen Datenverlust bei Umbauaktionen

## Systemvoraussetzungen

| | Windows | macOS |
|---|---|---|
| Betriebssystem | Windows 10 oder 11 | *offen, Empfehlung macOS 12 oder neuer* |
| Architektur | *offen, Empfehlung x64* | *offen, Empfehlung Universal 2* |
| Laufzeit | in der App enthalten | in der App enthalten |
| Internet | nicht erforderlich | nicht erforderlich |
| Benutzerkonto | nicht erforderlich | nicht erforderlich |
| Speicherbedarf Programm | folgt aus dem Build | folgt aus dem Build |

Aus dem Quellcode belegt: Die Anwendung nutzt ausschließlich die
Python-Standardbibliothek und Tk. Getestet mit Python 3.12 und Tk 8.6. Die
Mindestfenstergröße beträgt 860 × 700 Pixel.

**Noch nicht bestätigt:** Alle automatisierten Prüfungen liefen unter Linux mit
Tk 8.6. Schriftmetrik, DPI-Skalierung und native Dialoge verhalten sich unter
Windows und macOS anders; eine manuelle Prüfung dort steht aus.

## Datenspeicherung

| Ort | Pfad |
|---|---|
| Windows | `%APPDATA%\Glide\` |
| macOS | `~/Library/Application Support/Glide/` |
| Linux | `$XDG_DATA_HOME/Glide/` bzw. `~/.local/share/Glide/` |

Darin: `liste_speicher.json` (Nutzdaten), `settings.json` (Oberfläche),
`window.conf` (Fenstergeometrie), `backups/` (automatische Sicherungen),
`attachments/` (Anhangskopien). Nichts davon liegt im Installationsordner.

Seit 3.2.0 liest Glide beim Start **keine** Verzeichnisse früherer
Programmnamen mehr aus. Der Datenordner ist ausschließlich der oben genannte
oder der über `GLIDE_DATA_DIR` gesetzte.

## Grenzen und Kennzahlen

| Feld | Wert |
|---|---|
| Max. Anhangsgröße | 512 MB je Datei |
| Max. Backupgröße | 2 GB gesamt, 32 MB Daten-JSON |
| Max. Aufgaben je Bestand | 200 000 |
| Max. Verschachtelung Punkte | 100 Ebenen |
| Max. Verschachtelung Ordner | 5 Ebenen |
| Max. Papierkorbeinträge | 200 |
| Max. Labels je Punkt | 20 |
| Rückgängig-Tiefe | 20 Schritte |
| Automatische Sicherungen | letzte 40 Stände |
| Lesbare Backup-Formate | 4 bis 10 |

## Datenschutz – Antworten für beide Fragebögen

| Frage | Antwort |
|---|---|
| Erhebt die App personenbezogene Daten? | Nein |
| Überträgt die App Daten an den Anbieter? | Nein |
| Überträgt die App Daten an Dritte? | Nein |
| Analyse, Tracking oder Telemetrie? | Nein |
| Werbung oder Werbe-IDs? | Nein |
| Benutzerkonto oder Anmeldung? | Nein |
| Netzwerkzugriff? | Keiner |
| Kaufabwicklung in der App? | Nein |
| Standortzugriff? | Nein |
| Kamera, Mikrofon, Kontakte, Kalender? | Nein |
| Zugriff auf Dateien | Nur auf Dateien, die der Nutzer über den Dateidialog selbst auswählt |
| Datenlöschung | Löschen des App-Datenordners entfernt alle Daten |

Belegt durch: kein Netzwerkmodul im Quellcode, keine Analytics-Bibliothek, keine
Authentifizierung. Dateizugriffe erfolgen ausschließlich über den
System-Dateidialog nach Nutzeraktion.

Die Kalenderansicht ist **kein** Widerspruch dazu: Sie zeigt ausschließlich die
eigenen Fälligkeiten, liest und schreibt keinen externen Kalender und braucht
kein Netzwerk.

## Einstufung

| Feld | Vorschlag | Begründung |
|---|---|---|
| Kategorie | Produktivität | Kernnutzen ist Aufgabenverwaltung |
| Nebenkategorie | Dienstprogramme | passt zur lokalen Ablage |
| Altersfreigabe | ohne Altersbeschränkung | kein nutzergenerierter Austausch, kein Netzwerk, keine Werbung, keine Käufe |
| Oberflächensprache | Deutsch | einsprachig; Mehrsprachigkeit ist ein bewusstes Nicht-Ziel |
| Barrierefreiheit | Tastaturbedienung vollständig, Kontraste in beiden Modi geprüft | Screenreader-Unterstützung nicht geprüft |

## Suchbegriffe

Aufgaben, Aufgabenliste, To-do, Todo, Checkliste, Listen, Notizen, Projekt,
Aufgabenverwaltung, offline, lokal, ohne Cloud, ohne Konto, Datenschutz,
Dunkelmodus, Desktop, Windows, macOS

## Screenshots – noch zu erstellen

Vorhanden sind Prüfaufnahmen unter `50_Ablage/Screenshots/3.2.0/`. Sie stammen
aus der Linux-Prüfumgebung und taugen **nicht** als Store-Material: Schriften
und Fensterrahmen entsprechen nicht den Zielplattformen.

Empfohlene Motive, jeweils in Hell und Dunkel, aufgenommen auf dem Zielsystem:

1. Hauptansicht mit Gruppen, Labels, Fälligkeiten und Farben
2. Seitenleiste mit Ordnern, Eingang, „In Bearbeitung“ und „Verspätet“
3. Kontextmenü auf einer Aufgabe
4. Punktdetails mit Beschreibung, Labels und Anhang
5. Kalenderansicht
6. Ordnerübersicht
7. Papierkorb

Auflösungen richten sich nach den Store-Vorgaben; die App liefert bei
1000 × 800 Pixeln eine vollständige Ansicht.

## Was hier bewusst fehlt

Publisher, Copyright, Supportkontakt, Website, Datenschutz-URL, Preis,
Lizenzmodell, Bundle-IDs und die Markenlage zum Namen „Glide“. Das sind
Entscheidungen, keine Codefakten – sie stehen in
`00_Arbeitsvorbereitung/Entscheidungen/` und in
`01_Repository/Glide/docs/decisions/PRODUCT_IDENTITY.md`.
