# Schnellerfassung und gespeicherte Filter – Glide 3.11.0

Stand 13.09.2026 · Aufgabenformat 13 · Einstellungsformat 2

Glide ergänzt zwei Ansichten über dem vorhandenen Bestand. Beide Funktionen
arbeiten offline und ändern die Aufgabenstruktur nicht.

## Schnellerfassung

Die Schaltfläche „+“ in der Kopfzeile und **Strg/ Cmd + Alt + N** öffnen die
Schnellerfassung aus jeder Glide-Ansicht. Der Eingang ist voreingestellt; eine
andere Liste lässt sich direkt auswählen. Die Eingabe kann offen bleiben, um
mehrere Aufgaben nacheinander zu erfassen, oder die neue Aufgabe öffnet danach
ihre Quellliste.

Für eine optionale Fälligkeit versteht die Vorschau kurze deutsche Angaben:
„heute“, „morgen“, Wochentage, „in 3 Tagen“, „in 2 Wochen“, TT.MM.JJJJ oder
JJJJ-MM-TT. Eine Uhrzeit kann mit „um 14:30“ ergänzt werden. Nicht erkannte
Angaben werden vor dem Speichern als Fehler angezeigt.

## Gespeicherte Filter

Der Manager steht in der Seitenleiste und im Ansichtsmenü. Ein Filter speichert
einen Namen, optionalen Suchtext, eine Listen- und Labelauswahl, Status,
Wichtigkeit, Fälligkeit sowie die Verknüpfung mehrerer Labels. Fälligkeiten wie
„Heute“ und „Nächste 7 Tage“ werden beim Öffnen immer relativ zum aktuellen Tag
berechnet.

Ein gespeicherter Filter ist eine abgeleitete Ansicht: Punkte bleiben in ihren
Quelllisten und werden dort bearbeitet. Entfernte Listen oder Labels bleiben in
der Filterdefinition gekennzeichnet; dadurch werden nicht versehentlich fremde
Aufgaben aufgenommen. Die Ansicht bleibt nach einem Neustart erhalten.

Die persönliche Einstellungsdatei erhält dafür additive Felder
`saved_filters` und `active_saved_filter`. Aufgaben-, Backup- und Vorlagenformat
bleiben unverändert. Die Grenze liegt bei 100 gespeicherten Filtern.
