# Glide – Produktdatenblatt

Stand: 01.09.2026 · App-Version 2.6.0 · Datenformat 6

Alle Angaben in diesem Dokument sind aus dem Quellcode belegt. Sie sind die
gemeinsame Grundlage für Microsoft- und Apple-Formulare, für Website- und
Exposétexte. Was hier nicht steht, ist eine Geschäfts- oder Rechtsentscheidung
und liegt in `00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_2.6.0.md`.

---

## Kurzbeschreibung

**Bis 100 Zeichen**
Aufgaben und Listen für den Desktop. Ohne Konto, ohne Cloud, alle Daten bleiben auf dem Gerät.

**Bis 250 Zeichen**
Glide verwaltet Aufgaben, verschachtelte Listen und Notizen direkt auf dem Rechner. Kein Benutzerkonto, keine Cloudpflicht, keine Werbung, keine Datenerhebung. Ordner, Gruppen, Fälligkeiten, Prioritäten, Anhänge und ein Dunkelmodus sind eingebaut.

## Langbeschreibung

Glide ist eine schlanke Aufgaben- und Listen-App für Windows und macOS. Sie
startet ohne Anmeldung, arbeitet vollständig offline und legt jede Datei im
Benutzerordner des jeweiligen Systems ab. Es gibt keinen Server, keinen Account
und keinen Zwang zu einem Abonnement.

Aufgaben lassen sich beliebig tief verschachteln. Wer Struktur braucht, fasst
Punkte zu Gruppen zusammen – eine Gruppe ist ein Ordner innerhalb der Liste, der
Unterpunkte sammelt, ohne selbst als Aufgabe zu zählen. Listen liegen wahlweise
frei oder in Ordnern; ein fester Eingang nimmt alles auf, was noch nicht
einsortiert ist, und die Ansicht „In Bearbeitung“ sammelt automatisch jede
datierte Aufgabe aus allen Listen in zeitlicher Reihenfolge.

Zu jeder Aufgabe gehören optional eine Fälligkeit, eine von vier
Wichtigkeitsstufen, eine Farbe, ein längerer Beschreibungstext und beliebig
viele Dateianhänge. Anhänge werden als lokale Kopie im Datenordner der App
gespeichert, sodass die Aufgabe auch dann vollständig bleibt, wenn die
Originaldatei verschoben oder gelöscht wird.

Für den Austausch gibt es Export und Import als TXT, Markdown und CSV sowie ein
vollständiges, portables Backup, das die Anhänge einschließt. Automatische
Sicherungen laufen im Hintergrund mit.

## Funktionsliste

- Verschachtelte Aufgaben ohne feste Tiefenbegrenzung
- Gruppen als Ordner innerhalb einer Liste
- Listen, Ordner und ein geschützter Eingang
- Abgeleitete Ansicht „In Bearbeitung“ über alle datierten Aufgaben
- Fälligkeitsdatum mit Kalenderauswahl, Hervorhebung von heute und überfällig
- Vier Wichtigkeitsstufen
- Sieben Farben für Aufgaben, Listen und Ordner
- Beschreibungstext für Aufgaben, Listen und Ordner
- Dateianhänge als verwaltete lokale Kopie
- Volltextsuche über Titel, Beschreibung, Anhangsnamen, Status und Datum
- Filter für offene und erledigte Punkte
- Drag & Drop für Reihenfolge, Verschachtelung und Verschieben zwischen Listen
- Mehrfachauswahl, Rückgängig, Kopieren und Einfügen
- Kontextmenüs auf allen Oberflächen
- Hell- und Dunkelmodus
- Export und Import: TXT, Markdown, CSV
- Portables Komplettbackup einschließlich Anhänge
- Automatische Sicherungen der letzten 40 Stände
- Tastaturbedienung mit plattformgerechten Kürzeln

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

## Datenspeicherung

| Ort | Pfad |
|---|---|
| Windows | `%APPDATA%\Glide\` |
| macOS | `~/Library/Application Support/Glide/` |
| Linux | `$XDG_DATA_HOME/Glide/` bzw. `~/.local/share/Glide/` |

Darin: `liste_speicher.json` (Nutzdaten), `settings.json` (Oberfläche),
`window.conf` (Fenstergeometrie), `backups/` (automatische Sicherungen),
`attachments/` (Anhangskopien). Nichts davon liegt im Installationsordner.

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

Empfohlene Motive, jeweils in Hell und Dunkel:

1. Hauptansicht mit Gruppen, Fälligkeiten und Farben
2. Seitenleiste mit Ordnern, Eingang und „In Bearbeitung“
3. Kontextmenü auf einer Aufgabe
4. Punktdetails mit Beschreibung und Anhang
5. Ordnerübersicht
6. Ansicht „In Bearbeitung“

Auflösungen richten sich nach den Store-Vorgaben; die App liefert bei
1000 × 800 Pixeln eine vollständige Ansicht.

## Was hier bewusst fehlt

Publisher, Copyright, Supportkontakt, Website, Datenschutz-URL, Preis,
Lizenzmodell, Bundle-IDs und die Markenlage zum Namen „Glide“. Das sind
Entscheidungen, keine Codefakten – sie stehen in
`00_Arbeitsvorbereitung/Entscheidungen/Offene_Entscheidungen_2.6.0.md`.
