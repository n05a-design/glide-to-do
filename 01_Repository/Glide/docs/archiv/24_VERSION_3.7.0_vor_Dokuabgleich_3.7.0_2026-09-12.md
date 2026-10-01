# Glide 3.7.0 – kompakte Übersicht und erweiterte Seitendetails

Stand: 07.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

## Änderungen

| Rückmeldung | Verhalten in 3.7.0 |
|---|---|
| Listen-Symbol zu hoch | Nur das Symbol neben der Überschrift „Listen“ sitzt tiefer. Andere Navigationssymbole und Vorlagen bleiben auf ihrer bisherigen Achse. |
| Vorlagen scrollen ohne Überlauf | Der Scrollbereich ist mindestens so hoch wie der sichtbare Bereich; ohne Überlauf bleibt er oben und blendet die Leiste aus. |
| Startseite unten zeitweise nicht scrollbar | Diagramme, Chips und untergeordnete Flächen reichen das Mausrad an ihre Scrollfläche weiter. Die Leiste verändert die Inhaltsbreite nicht mehr. |
| Kachelübersicht zu schmal | Kacheln nutzen die vollständige Hauptbereichsbreite. Die Scrollleiste liegt im äußeren Rand. |
| Kacheln zu hoch | Kleinere Innenabstände, höchstens zwei Vorschaupunkte, kürzere Beschreibung und kein Leerraum durch gestreckte Nachbarkacheln. |
| Bearbeiten direkt an der Kachel | Neben „Liste öffnen“ beziehungsweise „Ordner öffnen“ steht „Bearbeiten“. |
| Mehr Seitendetails | Zwei Spalten mit Titel/Beschreibung sowie Farbe, Labels und lokalen Anhängen; feste Speichern-/Abbrechen-Aktionen unten. |
| Labels nicht scrollbar | Das Mausrad funktioniert auf Label-Chips, Auswahlmarken und Zeilen; die Bestätigung bleibt unten stehen. |
| Datum im Jahresraster | Beim Darüberfahren erscheinen Wochentag, Datum und Bearbeitungszahl des Tages. |
| Statistik nach dem Löschen | Gebuchte Tageswerte bleiben erhalten; der aktuelle Bestand zählt ausschließlich noch vorhandene Aufgaben. |

## Statistik und Aufbewahrung

„Erledigt in den letzten 7 Tagen“ verwendet die lokal gebuchten Erledigungen.
Das Löschen, endgültige Entfernen oder Wiederherstellen einer Aufgabe zieht
keine gebuchte Erledigung ab. Der Jahresanzeiger verwendet tägliche erfolgreiche
Aufgabenänderungen und ältere Erledigungszahlen als Mindestwert, ohne beide
für denselben Tag zu addieren. Eine Löschung ist selbst eine Aufgabenänderung.
Gruppen und Überschriften zählen nicht als erledigte Aufgaben.

Die täglichen Historien werden rollierend bis 371 Tage zurück
aufbewahrt. Fehlende frühere Erledigungsdaten können nicht nachträglich aus
gelöschten Aufgaben rekonstruiert werden. Die Historien liegen in `settings.json`;
ein Aufgabenbackup enthält sie nicht. Für ihre Übertragung den gesamten
Datenordner bei geschlossener App kopieren.

## Datenformat 12

Listen und Ordner erhalten jeweils ein `attachments`-Array mit demselben
Dateivertrag wie Aufgaben. Fehlende Felder aus älteren Daten werden als leere
Liste ergänzt. Vor dem ersten Überschreiben älterer lokaler Daten wird deren
unveränderter Inhalt unter `backups/liste_vor_format12_<Zeitstempel>.json`
gesichert. Diese Rückfallkopie wird nicht von der normalen Backuprotation
entfernt. Scheitert sie, wird der neue Datenstand nicht über die alte Datei
geschrieben.

Voll- und Teilbackups, ergänzender Import, eigene Vorlagen, Listenkopien und
Papierkorb erhalten Containeranhänge. Importierte Dateien bekommen neue
Speicherpfade; vorhandene Bytes werden nicht überschrieben. Entfernen eines
Anhangs löst die Zuordnung, bewahrt die lokale Datei für Rückgängig und ältere
Datenstände. Format 12 wird von älteren Glide-Versionen nicht unterstützt.

## Prüfung

Der gezielte Rundlauf `tests/integration/test_release37.py` ist erfolgreich:
Originalkopie bei Migration und Datenordnerwechsel, Schreibschutz bei fehlgeschlagener Migrationskopie, Containeranhänge durch Backup/Import/Vorlage/Kopie/
Papierkorb/Wiederherstellung, Pfadprüfung, Statistik nach endgültigem Löschen,
Bearbeitungsfenster in Hell und Dunkel, Label- und Diagrammmausrad,
Datumszuordnung aller Jahresfelder und tatsächlich geöffnetes Hinweisfenster und unterdrücktes Scrollen ohne Überlauf.

Der vollständige Lauf umfasst elf Suiten, zwei Analysen sowie den
reproduzierbaren Vergleich von Beispiel- und Releasebackups. Sein Ergebnis
steht unter `tests/qa-3.7.0/automatisch/ergebnis.json` (Exitcode 0, 2026-09-07T20:56:02).
Alle App-Tests verwenden einen temporären `GLIDE_DATA_DIR`. Reale Nutzdaten
wurden nicht verändert. Eigene Windows-Aufnahmen liegen unter
`tests/qa-3.7.0/oberflaeche` und wurden auf Lesbarkeit und erreichbare Aktionen
geprüft. Die frühere 3.6-Leistungsmessung wurde nicht als 3.7-Messung umbenannt.

Offen bleiben längere reale Nutzung, andere DPI-/Mehrmonitor-Konfigurationen
und macOS. Installer, Signierung und Storeveröffentlichung sind separate
Arbeitsschritte; dieser Stand ist eine startbare Python-Version.

## Einstieg

- [Quelltext](../src/glide/app.pyw)
- [Datenvertrag](06_DATA_BACKUP_MIGRATION.md)
- [Prüfplan](05_QA_TESTPLAN.md)
- [Startkontext](03_STARTKONTEXT.md)
- [Vorheriger UI-Stand 3.6.0](<archiv/23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0_vor_Nachbesserung_2026-09-11.md>)

Die startbare Python-Kopie und sämtliche Schriftressourcen werden abschließend im Hashmanifest `tests/qa-3.7.0/abschluss-kontrolle.json` gegen die Quelle geprüft. Der erste Prüflauf ist unter `erstlauf/` erhalten: Zwei ältere Prüferwartungen (Dialogparameter und zusätzliche Anhangs-Scrollleiste) mussten an die neue Maske angepasst werden. Der abschließende Vollmodus ist vollständig grün.

## Nachbesserung vom 11.09.2026

Mac-Trackpad unter Tk 9, vollständige isolierte Vorlagenbearbeitung, 16 Praxisvorlagen,
relative Termine mit Vorlagenformat 2 und verbesserte Aufgaben-Vorschauen.
Der aktuelle [Nachtrag mit Migration, Bedienung und Prüfgrenzen](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
hat für diese Punkte Vorrang vor dem Prüfstand vom 07.09.2026.
