# Reiteransicht für Listenelemente – Bedienvertrag

Stand: 12.09.2026 · **Entwurf, noch nicht umgesetzt** · Zielversion 3.9.0 ·
Aufgabenformat bleibt 13, Einstellungen bleiben Format 2.

Entschieden am 12.09.2026: **Reiter entstehen auf Zuruf aus einzelnen Punkten**,
nicht automatisch aus Gruppen. Die Alternative – jede Gruppe wird ein Reiter –
wurde verworfen, weil sie in Listen ohne Gruppen leer läuft und dem Nutzer die
Auswahl aus der Hand nimmt. [Vorschläge](../../../00_Arbeitsvorbereitung/Glide_Funktionsvorschlaege_2026-09-11.md).

## Was ein Reiter ist

Ein Reiter ist eine **geöffnete Sicht auf einen vorhandenen Punkt**, nichts
weiter. Er legt keine Kopie an, ändert keine Reihenfolge und erzeugt keinen
Status. Dieselbe Aufgabe in Liste und Reiter ist dasselbe Objekt mit derselben
Identität: Wer sie im Reiter erledigt, hat sie in der Liste erledigt.

Geöffnet werden können Aufgaben, Long-Tasks und Gruppen. Überschriften nicht –
sie tragen keinen Inhalt, den ein Reiter zeigen könnte.

## Bedienung

Ein Punkt wird über sein Kontextmenü und über ein Tastenkürzel als Reiter
geöffnet. Die Reiterleiste erscheint über dem Arbeitsbereich und nur dann, wenn
mindestens ein Reiter offen ist; ohne Reiter sieht die App aus wie bisher.

Der erste Reiter ist immer **Liste** – die gewohnte Ansicht. Er lässt sich nicht
schließen. Jeder weitere Reiter trägt den gekürzten Titel seines Punktes; der
vollständige Titel steht im Tooltip und in der Detailansicht selbst.

Ein Reiter zeigt Titel, Beschreibung, Wichtigkeit, Fälligkeit mit Uhrzeit,
Wiederholung, Erinnerung, Labels, Anhänge und – bei einer Gruppe – ihre
Unterpunkte mit Erledigt-Häkchen. Bearbeitet wird über dieselbe vorhandene
Maske wie sonst; der Reiter ersetzt keine Eingabemaske, er zeigt an und öffnet.

Schließen entfernt den Reiter und sonst nichts. Das steht ausdrücklich hier,
weil ein Schließkreuz neben einer Aufgabe wie Löschen aussieht: Die Beschriftung
lautet „Reiter schließen", niemals „Entfernen". Für das Löschen bleibt der
vorhandene Weg über Papierkorb und Kontextmenü.

## Grenzen und Regeln

- **Höchstens zwölf** gleichzeitig offene Punktreiter. Beim dreizehnten wird der
  am längsten unbenutzte geschlossen, mit einem Hinweis in der Statuszeile.
  Ohne Grenze entsteht eine Leiste, in der niemand mehr etwas findet.
- Die Reiterreihenfolge ist eine Ansichtseinstellung. Sie ändert die
  Aufgabenreihenfolge nicht, auch nicht beim Verschieben von Reitern.
- Ein Reiter ist an seine Quellliste gebunden und wird mit ihr geöffnet.
- Wird der Punkt erledigt, bleibt der Reiter offen und zeigt ihn als erledigt.
  Wandert er in den Papierkorb oder verschwindet er durch einen Import, wird
  sein Reiter still geschlossen – ein Reiter auf ein nicht mehr vorhandenes
  Objekt hätte nichts anzuzeigen.
- Änderungen laufen über `item_change`; eine Bearbeitung im Reiter erscheint
  sofort in der Liste und umgekehrt. Keine zweite Datenhaltung, kein Zwischenspeicher.
- Tastatur: Reiter wechseln, schließen und zur Liste zurück sind erreichbar,
  ohne die Maus zu benutzen. Der Fokus bleibt nach dem Wechsel sichtbar.
- Hell und Dunkel wie überall; der aktive Reiter trägt die Akzentfarbe,
  der überfahrene den Hover-Ton.

## Daten

Offene Reiter sind **Ansichtszustand, keine Aufgabendaten**. Sie liegen in
`settings.json` unter `open_tabs` als Liste aus Listen- und Punktkennung, dazu
`active_tab`. Das Aufgabenformat bleibt bei 13, Backups bleiben unverändert.
Beim Start wird jede Kennung geprüft: Was es nicht mehr gibt, fällt weg.
Ein Aufgabenbackup transportiert keine Reiter – es enthält Aufgaben, nicht die
Sicht auf sie.

Ein Wiederherstellen aus dem Papierkorb öffnet keinen Reiter erneut. Kopierte
Punkte bekommen neue Identitäten und damit keine geerbten Reiter.

## Was nicht dazugehört

Keine Reiter für ganze Listen – dafür gibt es die Seitenleiste. Keine
Reiterebene über Ordner. Kein paralleler Status, kein zusätzliches Ablagefach.
Die Pinnwand bleibt ein eigener Ausbauschritt und benutzt dieselben Objekte.

## Abnahmekriterien

1. Ein geöffneter Reiter zeigt denselben Punkt wie die Liste; eine Änderung auf
   einer Seite erscheint sofort auf der anderen.
2. Schließen eines Reiters verändert keinen Bestand – Punktzahl und
   Identitäten sind davor und danach gleich.
3. Nach Neustart stehen dieselben Reiter offen, sofern ihre Punkte noch
   existieren; gelöschte fallen kommentarlos weg.
4. Der dreizehnte Reiter schließt genau einen anderen, nie mehrere.
5. Papierkorb schließt den zugehörigen Reiter, Wiederherstellen öffnet ihn nicht.
6. Tastaturbedienung erreicht jeden Reiter und die Liste.
7. Hell und Dunkel ohne Fremdfarben; lange Titel brechen die Leiste nicht.
8. Aufgabenformat und Backupinhalt sind vor und nach der Änderung gleich.
