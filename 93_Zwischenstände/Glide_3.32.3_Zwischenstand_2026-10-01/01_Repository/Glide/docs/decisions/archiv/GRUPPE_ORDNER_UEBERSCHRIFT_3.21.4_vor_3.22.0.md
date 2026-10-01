# Gruppe, Ordner oder Zwischenüberschrift?

Stand: 14.09.2026 · Glide 3.21.4 · Entscheidung unverändert gültig.

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
