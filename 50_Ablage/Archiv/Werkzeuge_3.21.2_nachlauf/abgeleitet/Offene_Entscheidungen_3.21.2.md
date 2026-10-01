# Offene Entscheidungen – Glide 3.21.2

Stand: 14.09.2026 · interner Entwicklungsstand

## Erledigt mit 3.21.2

**Überholte Versionsangaben im Releasebestand.** Aus 3.21.1 offen, jetzt
entschieden: Die Angaben hängen an `APP_VERSION` und der neuen Modulkonstante
`DATA_SCHEMA_VERSION` in `tests/tools/releasedaten.py`. Dieselbe Konstante speist
die vorhandene Zusicherung gegen `app.DATA_SCHEMA_VERSION`. Die Variante „ganz
weglassen" wurde verworfen: Der Codebeleg gewinnt durch die Standangabe, wenn
sie stimmt.

## Neu aufgeworfen

### Wie viel Prüfbestand gehört in die mitgelieferte Datei

Der Beispielbestand ist auf 166 Punkte gewachsen, weil jede Funktion seit 3.14
eine sichtbare Wirkung haben soll. Das hat eine Grenze: Irgendwann wird die Datei
zum Testkatalog statt zur Anschauung, und wer sie einliest, sucht sich in 12
Listen zurecht. Zu entscheiden, wenn die nächste Funktion dazukommt:

- so weitermachen und die Prüfliste wachsen lassen, oder
- eine **zweite**, ausdrücklich als Prüfbestand benannte Datei einführen und die
  Funktionsvorschau auf Anschauung zurückschneiden (empfohlen, sobald eine
  weitere Funktion eigene Prüfpunkte braucht), oder
- Prüfpunkte ganz in die Suiten verlagern und in der Datei nur zeigen, wie Glide
  im Alltag aussieht.

### Schreibungsabhängigkeit des Beispielbackups

Weiter offen aus 3.21.0. `tests/integration/test_glide.py` erwartet
`Glide_Beispieldaten.glidebackup`, im Repository liegt
`glide_beispieldaten.glidebackup`. Unter macOS und Windows identisch, unter Linux
nicht; in der Vorabumgebung per Kopie umgangen. Empfehlung unverändert: die
Erwartung im Test auf die tatsächliche Schreibung ziehen – eine Zeile, ohne
Risiko für andere Stellen.

### Reste, die sich nicht verschieben lassen

`07_Python-Versionen/__pycache__` enthält Bytecode zu 3.6 und 3.7. Die
Geräteverbindung darf nicht löschen, und ein `__pycache__` ins Archiv zu
verschieben wäre unsinnig – es entsteht beim nächsten Start neu. Zu entscheiden:
beim nächsten Aufräumen von Hand entfernen, oder in eine `.gitignore`-artige
Ausnahme aufnehmen und dauerhaft ignorieren.

`Claude outputs` enthält drei ZIP-Pakete aus der Sitzung
(3.19.0-Quellstand, 3.21.0-Quellstand, 3.21.1-Ablagepaket). Sie sind vollständig
in der Ablage aufgegangen. Zu entscheiden: in `50_Ablage/Archiv` verschieben oder
als Sitzungsablage stehen lassen.

## Aus früheren Ständen weiterhin offen

### Synchronisierung von Kalendern

Der Import legt an und erkennt eigene Punkte über die `UID` wieder, aktualisiert
aber keine vorhandenen. Ein echter Abgleich wäre Synchronisierung – mit
Konfliktregeln, Löschweitergabe und Abonnements. Bleibt eine eigene Entscheidung.

### Nicht abbildbare Wiederholungsregeln

`COUNT`, `BYMONTHDAY`, `BYSETPOS` und Intervalle bei Wochen, Monaten und Jahren
werden verworfen und gezählt, statt still vereinfacht zu werden. Ob Glide eigene
Wiederholungsarten dafür bekommt, bleibt offen.

### Zeitzone des Prüfstands

`Europe/Berlin` ist die Vorgabe, wenn der Aufrufer keine Zone setzt. Das macht
Läufe vergleichbar und deckt beide Versätze ab, verdeckt aber eine
Zonenbesonderheit der jeweiligen Maschine. Für den Kalenderrundlauf fangen die
vier Zonen in `test_features321.py` das auf. Zu entscheiden, wenn weitere
zeitabhängige Funktionen hinzukommen.

### Benutzerdefinierte Felder

Nächste größere Idee: eigene Felder je Liste (neues Aufgabenformat 16) und darauf
aufbauende eigene Ansichten. Noch nicht begonnen; Format 15 bleibt bis dahin
unverändert.
