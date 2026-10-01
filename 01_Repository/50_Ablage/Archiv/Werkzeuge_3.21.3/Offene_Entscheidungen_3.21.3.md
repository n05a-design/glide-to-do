# Offene Entscheidungen – Glide 3.21.3

Stand: 14.09.2026 · Glide 3.21.3 · interner Entwicklungsstand

## Erledigt mit 3.21.3

**Übertragungspakete in `Claude outputs`.** Aus 3.21.2 offen, jetzt entschieden:
Die drei ZIP-Pakete liegen unter `50_Ablage/Archiv/Uebertragungspakete`, wo auch
die Werkzeugordner der Versionssprünge liegen. Die Variante „als Sitzungsablage
stehen lassen" wurde verworfen: Ein Ordner mit Versionsnummern im Namen, der
nicht zur Ablagestruktur gehört, sieht bei jeder späteren Prüfung wie eine
vergessene Fassung aus.

**Startbare Fassungen in `07_Python-Versionen`.** Nicht vorher aufgeworfen,
sondern beim Archivnachweis gefunden: Neun Fassungen von 3.14.0 bis 3.21.2 lagen
aktiv neben der aktuellen, während das Archiv nur bis 3.13.0 reichte. Sie liegen
jetzt im Archiv; der Ordner-README sagt es ausdrücklich, damit die Regel beim
nächsten Stand nicht wieder ausfällt.

**Wie die Aktualität von Dokumenten geprüft wird.** Entschieden zugunsten eines
eigenen Prüfschritts (`tests/tools/standpruefung.py`) statt größerer
Sorgfalt beim Fortschreiben. Sorgfalt hat zweimal nicht gereicht.

## Neu aufgeworfen

### Prüft `standpruefung.py` auch Datumsangaben

Heute prüft sie Versionen, nicht Daten. Eine Standzeile
„Stand 13.09.2026 · Glide 3.21.3" wäre regelkonform und trotzdem irreführend –
genau so stand es im QA-Bericht und im PROJECT_HANDOFF. Die Prüfung könnte das
Datum der Standzeile gegen das Datum des obersten Änderungsverlaufseintrags
prüfen. Dagegen spricht, dass ein Dokument beim Fortschreiben inhaltlich
unverändert bleiben kann und ein neues Datum dann eine Pflege behauptet, die
nicht stattgefunden hat. Zu entscheiden, wenn eine Datumsangabe das nächste Mal
auffällt.

### Dokumente ausliefern statt fortschreiben

`tests/README.md` und `tests/fixtures/README.md` gehen seit 3.21.3 über den
SHA-256-Abgleich des Ablageskripts: Sie werden als Ganzes geschrieben und können
deshalb nicht teilweise überholt sein. Für die 15 Dokumente unter `docs/` wäre
derselbe Weg denkbar. Dagegen spricht der Umfang – sie sind lang, und jede
Änderung müsste dann durch die Arbeitskopie laufen statt durch eine gezielte
Regel mit Pflichtstelle. Empfehlung: beim nächsten größeren Umbau eines Dokuments
einzeln entscheiden, nicht pauschal umstellen.

### Store-Angaben sind sieben Versionen alt

`40_Store_Material/Apple` und `Microsoft` sind auf Grundlage von Glide 3.14.0
und Datenformat 13 erhoben (Quellenabruf 04.09.2026). Beide Dokumente sagen das
jetzt deutlich, aber die Angaben selbst sind nicht nachgezogen: Der
Funktionsumfang ist seit 3.14 um sieben Stufen gewachsen. Zu entscheiden vor
einer Einreichung: vollständig neu erheben, oder nur die Funktionsliste gegen
das Produktdatenblatt abgleichen und die Plattformvorgaben separat prüfen.

## Aus früheren Ständen weiterhin offen

### Wie viel Prüfbestand gehört in die mitgelieferte Datei

Unverändert aus 3.21.2. Der Beispielbestand hat 166 Punkte in 12 Listen, weil
jede Funktion seit 3.14 eine sichtbare Wirkung haben soll. Sobald eine weitere
Funktion eigene Prüfpunkte braucht, empfiehlt sich eine **zweite**, ausdrücklich
als Prüfbestand benannte Datei und ein Rückschnitt der Funktionsvorschau auf
Anschauung.

### Schreibungsabhängigkeit des Beispielbackups

Weiter offen aus 3.21.0. `tests/integration/test_glide.py` erwartet
`Glide_Beispieldaten.glidebackup`, im Repository liegt
`glide_beispieldaten.glidebackup`. Unter macOS und Windows identisch, unter Linux
nicht; in der Vorabumgebung per Kopie umgangen. Empfehlung unverändert: die
Erwartung im Test auf die tatsächliche Schreibung ziehen – eine Zeile, ohne
Risiko für andere Stellen.

### `07_Python-Versionen/__pycache__`

Unverändert aus 3.21.2. Bytecode zu 3.6 und 3.7. Die Geräteverbindung darf nicht
löschen, und ein `__pycache__` ins Archiv zu verschieben wäre unsinnig – es
entsteht beim nächsten Start neu. Zu entscheiden: beim nächsten Aufräumen von
Hand entfernen, oder dauerhaft ignorieren.

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
