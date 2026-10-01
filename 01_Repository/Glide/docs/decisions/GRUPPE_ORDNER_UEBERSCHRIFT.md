# Gruppe, Ordner oder Zwischenüberschrift?

Stand: 01.10.2026 · Glide 3.33.1 · Entscheidung unverändert gültig, ergänzt um die Abgrenzung zum Gruppieren nach Feld (3.30). Die Checkliste aus 3.22 ist kein viertes Mittel: Sie gliedert einen einzelnen Punkt in Schritte ohne eigene Termine, Labels oder Anhänge.

Drei Mittel, um Ordnung zu schaffen, und die Frage, wann welches. Diese
Entscheidung stand seit 2.11.0 aus; sie wurde nachgeholt, weil in der
Benutzung genau die Verwechslung auftrat, die sie verhindern soll.

## Die kurze Antwort

| Mittel | Ebene | Was es aufnimmt | Wofür |
|---|---|---|---|
| **Zwischenüberschrift** | in einer Liste | nichts | Abschnitte sichtbar machen |
| **Gruppe** | in einer Liste | Punkte derselben Liste | zusammengehörige Aufgaben bündeln |
| **Ordner** | in der Seitenleiste | ganze Listen | Listen zu einem Vorhaben zusammenfassen |

Die Faustregel: **Ordnest du Aufgaben oder Listen?** Aufgaben ordnet die
Gruppe, Listen der Ordner. Wer nur eine Trennlinie mit Beschriftung braucht,
nimmt die Zwischenüberschrift – sie kostet nichts und nimmt nichts auf.

## Zwischenüberschrift

Eine Beschriftung mitten in der Liste. Sie trägt keinen Status, keine Frist,
keine Wichtigkeit, und sie nimmt keine Punkte auf. Alles, was unter ihr steht,
steht dort, weil es dort einsortiert wurde – nicht, weil die Überschrift es
enthielte.

Richtig für: „Vormittag" / „Nachmittag", „Vor Ort" / „Im Büro", Phasen eines
Ablaufs, bei dem die Punkte trotzdem in einer Reihe bleiben sollen.

Falsch für: alles, was man später zusammen verschieben, zuklappen oder zählen
will. Dafür gibt es die Gruppe.

## Gruppe

Ein Punkt, der andere Punkte enthält. Sie lässt sich zuklappen, verschieben und
auflösen; ihr Zähler nennt die Zahl der enthaltenen Aufgaben. Eine Gruppe trägt
selbst keinen Erledigt-Status, keine Frist und keine Wichtigkeit – sie ist ein
Behälter, keine Aufgabe.

Richtig für: „Angebot einholen" mit den drei Anrufen darunter; einen
Arbeitsschritt, der aus mehreren Handgriffen besteht; alles, was man als Block
an eine andere Stelle ziehen will.

Falsch für: Dinge, die inhaltlich zusammengehören, aber nie gemeinsam bewegt
werden – dort genügt eine Zwischenüberschrift.

**So kommt etwas hinein** (seit 3.0.2 drei Wege):

- mehrere Punkte auswählen und **Strg+G** – legt sie in eine neue Gruppe
- einen Punkt **auf die Mitte** einer Gruppenzeile ziehen – legt ihn hinein
- **Shift+Ziehen** auf einen beliebigen Punkt – macht einen Unterpunkt daraus

Ein Zug an den **oberen oder unteren Rand** der Gruppenzeile sortiert daneben
ein, nicht hinein. Dieselbe Unterscheidung wie in einem Dateimanager.

**Nicht zu verwechseln mit** „Art → Jeden Punkt zur leeren Gruppe machen": Das
wandelt jeden markierten Punkt einzeln in eine leere Gruppe um. Der Eintrag hieß
bis 3.0.1 „In Gruppe umwandeln" und stand direkt neben „Auswahl gruppieren" –
beides klang gleich und tat Gegenteiliges. Wer damit fünf Punkte markierte,
bekam fünf leere Gruppen und keine, die etwas enthielt.

## Ordner

Ein Behälter für ganze Listen in der Seitenleiste, bis zu fünf Ebenen tief.
Ordner enthalten niemals einzelne Aufgaben – nur Listen und weitere Ordner.

Richtig für: ein Projekt mit mehreren Listen; ein Jahr mit einer Liste je
Quartal; die Trennung von Beruflichem und Privatem.

Falsch für: Aufgaben eines einzelnen Vorhabens. Eine Liste, die nur drei Punkte
enthält, braucht keinen eigenen Ordner – sie braucht eine Gruppe in einer
größeren Liste.

## Warum es bei drei Mitteln bleibt

Der naheliegende Gedanke wäre, Gruppe und Ordner zu einem Begriff zu
verschmelzen. Dagegen spricht, was sie aufnehmen: Eine Gruppe lebt **in** einer
Liste und kann nur deren Punkte enthalten; ein Ordner lebt **über** den Listen
und kann keine einzelne Aufgabe aufnehmen. Ein gemeinsamer Begriff müsste beides
können – und damit gäbe es keinen Ort mehr, an dem klar wäre, ob ein Ding eine
Aufgabe oder eine Liste ist.

Die Zwischenüberschrift wiederum ist der billigste Fall: Wer nur eine Zäsur
will, soll dafür keinen Behälter anlegen müssen, den er später auflösen muss.

## Was daraus folgt

- Der Zähler einer leeren Gruppe zeigt seit 3.0.2 „(leer)" statt „(0)". Die Null
  ließ offen, wofür sie steht.
- „Auswahl gruppieren" steht auf der obersten Menüebene, nicht mehr unter „Art".
- Die Hinweiszeile nennt den Weg, einen Punkt in eine Gruppe zu ziehen.

## Gruppieren nach Feld ist Ansicht (seit 3.30)

Liste, Tabelle und Pinnwand können nach Fälligkeit, Bearbeitungstag,
Wichtigkeit, Label oder Erledigt gruppieren; das Spaltenboard auf Ordner- und
globaler Pinnwand zusätzlich nach Liste. Das ist **kein viertes Mittel der
Ordnung**, sondern eine Sicht auf dieselben Punkte.

**Abgrenzung zu den drei Strukturmitteln:**

- Die Abschnittsköpfe sind keine Punkte. Sie werden nicht gespeichert, nicht
  exportiert und nicht gezählt.
- Eine Gruppe, eine Zwischenüberschrift und ein Ordner bleiben unberührt. In
  der gruppierten Liste lösen sich Zwischenüberschriften nur für die Anzeige
  auf, Unterpunkte bleiben unter ihrem Elternpunkt.
- Ziehen zwischen Abschnitten ändert genau das Feld, nach dem gruppiert ist –
  nie die Struktur.
- Die Wahl der Gruppierung ist eine Einstellung je Liste (`list_group_by`) bzw.
  je Pinnwand (`group_by`).

**Wann was:**

- Soll etwas dauerhaft zusammengehören, bleibt es bei Gruppe, Überschrift oder
  Ordner.
- Soll derselbe Bestand für eine Frage anders sortiert erscheinen („was ist
  heute dran?“, „was ist wichtig?“), ist Gruppieren das Mittel.

