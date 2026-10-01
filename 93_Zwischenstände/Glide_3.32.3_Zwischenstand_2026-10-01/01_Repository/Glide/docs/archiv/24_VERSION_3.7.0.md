# Glide 3.7.0 – Vorlagen, Mac-Bedienung und dynamische Übersicht

Stand: 12.09.2026 · Aufgabenformat 12 · Einstellungen 2 · Vorlagenformat 2

## Änderungen

| Rückmeldung | Verhalten in 3.7.0 |
|---|---|
| Listen-Symbol zu hoch | Nur das Symbol neben der Überschrift „Listen“ sitzt tiefer. Andere Navigationssymbole und Vorlagen bleiben auf ihrer bisherigen Achse. |
| Vorlagen scrollen ohne Überlauf | Der Scrollbereich ist mindestens so hoch wie der sichtbare Bereich; ohne Überlauf bleibt er oben und blendet die Leiste aus. |
| Startseite unten zeitweise nicht scrollbar | Diagramme, Chips und untergeordnete Flächen reichen das Mausrad an ihre Scrollfläche weiter. Die Leiste verändert die Inhaltsbreite nicht mehr. |
| Kachelübersicht zu schmal | Kacheln nutzen die vollständige Hauptbereichsbreite. Die Scrollleiste liegt im äußeren Rand. |
| Kacheln zu hoch | Eigene Inhaltshöhe in unabhängig gestapelten Spalten, drei getrennte Vorschaupunkte, 16 px Innenabstand und 12 px Zwischenraum; keine Typzeile. |
| Bearbeiten direkt an der Kachel | Neben „Liste öffnen“ beziehungsweise „Ordner öffnen“ steht „Liste bearbeiten“ beziehungsweise „Ordner bearbeiten“; die Aktionen umbrechen und werden bei Tastaturfokus sichtbar. |
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

Der damalige kombinierte Prüflauf auf macOS/Python 3.14.5 bestand mit Exitcode 0:
elf Testsuiten, zwei statische Analysen sowie Beispiel-/Releaseabgleiche.
Die neuen UI-Änderungen wurden nicht auf einem Windows-System ausgeführt.
Frühere Windows-Protokolle belegen ausschließlich den damaligen Quellstand.
Native Sichtabnahme, physisches Trackpad, weitere DPI/Monitore, Screenreader,
Langzeitbetrieb, Installer und Signierung bleiben offen.

[Aktueller Gesamtlauf](../../../../50_Ablage/QA/qa-3.7.0/dynamische-kacheln/abschluss/ergebnis.json) · [QA und Grenzen](../07_QA_BERICHT.md).

## Einstieg

- [Quelltext](../../src/glide/app.pyw)
- [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md)
- [Prüfplan](../05_QA_TESTPLAN.md)
- [Startkontext](../03_STARTKONTEXT.md)
- [Vorheriger UI-Stand 3.6.0](23_KACHELUEBERSICHT_UND_JAHRESANZEIGE_3.6.0_vor_Nachbesserung_2026-09-11.md)

Arbeitskopie und sieben Ressourcen sind bytegleich mit dem Projekt.
[Quellstand-Prüfsummen](../../../../50_Ablage/QA/qa-3.7.0/dynamische-kacheln/gepruefter_quellstand_sha256.json).

## Vorlagen und Mac-Bedienung

Vollständiger isolierter Vorlageneditor mit App-Farben, Labels, Anhängen,
relativen Terminen und erhaltener Baumstruktur; 16 Praxisvorlagen.
Mac-Auswahlfelder einschließlich Popup verwenden App-Farben, während Windows
und Linux den bisherigen OptionMenu-Pfad behalten. Die Bestandsübersicht nutzt
1–3 unabhängig gestapelte Spalten mit eigener Inhaltshöhe, ohne redundante
Typzeile, mit 16 Pixel Innenabstand und 12 Pixel Kartenabstand. Vollständige
Öffnen-/Bearbeiten-Aktionen umbrechen und werden beim Tastaturfokus sichtbar.

Details: [Vorlagen-/Mac-Nachtrag](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md) und
[dynamische Kacheln](29_DYNAMISCHE_KACHELN_3.7.0.md).
