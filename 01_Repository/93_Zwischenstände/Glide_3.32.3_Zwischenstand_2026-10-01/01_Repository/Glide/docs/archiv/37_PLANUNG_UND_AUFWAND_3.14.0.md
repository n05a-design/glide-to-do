# Bearbeitungstag und Aufwand – Glide 3.14.0

Stand: 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14

Aufgaben und Long-Tasks haben zwei zusätzliche freiwillige Angaben: **Bearbeitungstag** und **geschätzter Aufwand in Minuten**. Die Fälligkeit bleibt die verbindliche Frist. Ein Bearbeitungstag kann auch ohne Fälligkeit gesetzt werden. „Mein Tag“ bleibt eine bewusst zusammengestellte Auswahl und übernimmt geplante Aufgaben nicht automatisch.

## Bedienung

- Unter **Punktdetails → Bearbeitungstag / Geschätzter Aufwand** einen Tag tippen oder im Kalender wählen. Der Aufwand akzeptiert ganze Minuten von 1 bis 60000. Leere Felder entfernen die jeweilige Angabe.
- Mehrere Aufgaben auswählen und **Bearbeiten → Bearbeitungstag und Aufwand …** öffnen. Die Aktion ist auch über **App-Aktionen** und Rechtsklick erreichbar. Nur angehakte Angaben werden übernommen. Bei gemischten Werten sind die Felder zunächst leer und nicht angehakt. Gruppen und Überschriften werden übersprungen.
- In der **Tabellenansicht → Spalten …** die Spalten Bearbeitungstag und Aufwand einblenden. Eine bereits gespeicherte Spaltenauswahl wird beibehalten; Listen ohne eigene Auswahl zeigen beide Spalten. Der Aufwand erscheint etwa als „1 h 30 min“.
- Ein geöffneter Punktreiter zeigt beide Werte. Bearbeiten, Kopieren, Verschieben und Rückgängig verwenden weiterhin dieselben Aufgabenobjekte.

## Wiederholungen und Vorlagen

Beim Vorrücken einer erledigten Serie wird der Bearbeitungstag geleert, damit kein vergangener Planungstag am nächsten Vorkommen hängt. Der geschätzte Aufwand bleibt erhalten. Endet die Serie, bleiben beide Angaben am abgeschlossenen Punkt stehen. Gewöhnliches Erledigen verändert sie nicht. Die Umwandlung in Gruppe oder Überschrift entfernt beide Angaben nur am umgewandelten Punkt.

Vorlagen übernehmen die Felder. Bei relativen Vorlagen verschiebt sich der Bearbeitungstag um denselben Abstand wie die Fälligkeit, auch wenn die Aufgabe keine Fälligkeit hat. Bei festen Vorlagen bleiben die Datumswerte unverändert. Die Aufwandsschätzung verändert sich beim Einsetzen nicht.

## Speicherung und Austausch

`planned_date` ist ein ISO-Datum oder `null`; `estimated_minutes` ist eine ganze Zahl von 1 bis 60000 oder `null`. Ältere Bestände erhalten leere Werte. Ungültige Werte werden vor einem Backupimport abgewiesen, einschließlich Papierkorb. Aufgabenformat **14** schützt die neuen Felder vor dem Öffnen in älteren App-Versionen.

Vor dem ersten Speichern älterer Daten entsteht `backups/liste_vor_format14_<Zeitstempel>.json` als unveränderte, unrotierte Originalkopie. Scheitert diese Sicherung, wird die Datendatei nicht überschrieben. Ein Downgrade auf 3.13 oder älter benötigt die alte Sicherung in einer separaten Ablage; Änderungen aus Format 14 sind darin nicht enthalten.

Voll-/Teilbackups, Vorlagen, Kopien und Papierkorb enthalten die Planungsfelder. TXT-Export und erneuter TXT-Import erhalten beide Angaben; Markdown stellt sie lesbar dar. CSV hängt **Bearbeitungstag** und **Aufwand (Minuten)** an die bisherigen elf Spalten an. Ein CSV-Import mit Spaltenzuordnung ist weiterhin eine offene Funktion.

Einstellungen und der separate Vorlagenkatalog bleiben außerhalb des Aufgabenbackups. Es gibt noch keine Kapazitätsplanung, Zeiterfassung, Auslastungsberechnung oder automatische Terminverteilung.

## Prüfung

Die Suite `tests/integration/test_features314.py` prüft Werte und Grenzen, Migration und Sicherungsfehler, Mehrfachbearbeitung, Rückgängig, Kopien, Artwechsel, Wiederholungen, Vollbackup, Papierkorb, Vorlagen, Exporte und echte Dialoge in Hell/Dunkel bei begrenzter Fensterhöhe. Der Gesamtlauf umfasst 18 Suiten. Den tatsächlichen Abschlussstand und verbleibende Plattformprüfungen dokumentiert der [QA-Bericht](../07_QA_BERICHT.md).

[Tabellenansicht](36_TABELLENANSICHT_3.13.0.md) · [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md) · [Funktionsübersicht](../../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-16.md)
