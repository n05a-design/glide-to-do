# Offene Entscheidungen – Glide 3.21.4

Stand: 15.09.2026 · Glide 3.21.4 · interner Entwicklungsstand

## Erledigt mit 3.21.4

**Wann das Ergebnis eines Prüflaufs in die Dokumente kommt.** Bis 3.21.2 stand
es immer erst in den Dokumenten der **nächsten** Version – der Lauf fand ja nach
der Ablage statt. Folge: Jeder Stand behauptete in seinem eigenen QA-Bericht,
sein Prüflauf stehe noch aus, und wer nur diesen Stand las, hielt ihn für
ungeprüft. Entschieden: Das Ergebnis wird nach dem Lauf in QA-Bericht,
Weitergabe und Technische Fakten **derselben** Version nachgetragen; der
Ablageweg in der Weitergabe hat dafür einen achten Schritt. Der 3.21.3-Lauf ist
so eingetragen.

**Prüft `standpruefung.py` auch Formatstufen.** Aus 3.21.3 als Datumsfrage
aufgeworfen, für die Formatstufen jetzt entschieden: R6 bis R8 prüfen eine
Formatstufe gegen `DATA_SCHEMA_VERSION`, einen Formatbereich gegen
`MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis dorthin und eine Tabellenzeile
„Datenformat“/„App-Version“ gegen beide Werte. Drei der fünf Formatbefunde
dieses Stands hätte das mechanisch gefunden. Die Werte liest das Werkzeug über
den Syntaxbaum aus `app.pyw` – ein Import würde Tk starten und den echten
Nutzerdatenordner anfassen.

**`SEQUENCE` in der Kalenderausgabe.** Beim Abgleich der Verträge gegen den Code
aufgefallen: `SEQUENCE` steht fest auf `0` und steigt nie. Der 3.20.0-Vertrag
versprach daraus eine Aktualisierung im Zielkalender. Entschieden als
Produktentscheidung, nicht als Fehler: Die Identität trägt allein die stabile
UID; ob ein Kalender einen Termin ersetzt, entscheidet er selbst. Ein steigendes
`SEQUENCE` wäre nur ehrlich, wenn Glide Änderungen an einem einmal
ausgegebenen Termin verfolgen würde – das wäre Synchronisierung (siehe unten).
Der Vertrag sagt es jetzt so.

## Neu aufgeworfen

### Prüft `standpruefung.py` auch Datumsangaben

Aus 3.21.3 **unverändert offen** – die Formatstufen sind der beantwortete Teil,
das Datum nicht. Eine Standzeile „Stand 13.09.2026 · Glide 3.21.4“ wäre
regelkonform und trotzdem irreführend. Die Prüfung könnte das Datum gegen den
obersten Änderungsverlaufseintrag stellen. Dagegen spricht unverändert, dass ein
Dokument beim Fortschreiben inhaltlich unverändert bleiben kann und ein neues
Datum dann eine Pflege behauptet, die nicht stattgefunden hat. Zu entscheiden,
wenn eine Datumsangabe das nächste Mal auffällt.

### Wie viele Dokumente noch ausgeliefert statt fortgeschrieben werden

Vier Dateien gehen jetzt über den SHA-256-Abgleich: `tests/README.md`,
`tests/fixtures/README.md`, `tests/tools/README.md`, `src/glide/README.md`. Alle
vier trugen Angaben, die bei jedem Stand hätten mitgehen müssen – bei
`tests/tools/README.md` waren es „Achtzehn Suiten“ bei tatsächlich 25, „Format
14“, „für 3.14“ und ein Windows-Nachweis ohne Datum. Das Muster ist damit
belegt: Ein Dokument, das **im Quellstand** liegt, gehört zum Quellstand und
nicht in die Fortschreibung. Offen bleibt der Umkehrschluss für die 38 Dokumente
unter `docs/`: Sie liegen ebenfalls im Quellstand, sind aber lang, und jede
Änderung müsste dann durch die Arbeitskopie laufen statt durch eine gezielte
Regel mit Pflichtstelle. Empfehlung unverändert: beim nächsten größeren Umbau
eines Dokuments einzeln entscheiden, nicht pauschal umstellen.

### Falsche Codeaussagen – woran es lag

Kein Einzelbefund, sondern ein Muster: Die aufgeführten Aussagen stehen in **Bedienverträgen**,
also in den Dokumenten, die eine Funktion beim Bau beschreiben und danach als
historisch gelten. Sie wurden geschrieben, bevor der Code fertig war, und
danach nie mehr gegen ihn gehalten. Drei Wege sind denkbar: (a) den Vertrag nach
der Umsetzung einmal förmlich gegenprüfen und das im Ablageweg festschreiben,
(b) Zusagen, die eine Konstante betreffen, im Vertrag an den Konstantennamen
binden, damit `grep` sie findet, (c) die Verträge als historisch akzeptieren und
allein das Produktdatenblatt als verbindliche Verhaltensbeschreibung führen.
Empfehlung: (a) und (b) zusammen; (c) verliert zu viel. Zu entscheiden beim
nächsten Funktionsstand – 3.21.4 hat keinen.

## Aus früheren Ständen weiterhin offen

### Store-Angaben sind sieben Versionen alt

Unverändert aus 3.21.3, nur die Formatzahl ist berichtigt:
`40_Store_Material/Apple` und `Microsoft` sind auf Grundlage von Glide 3.14.0
und Aufgabenformat 14 erhoben (Quellenabruf 04.09.2026). Beide Dokumente sagen
das deutlich, die Angaben selbst sind nicht nachgezogen. Zu entscheiden vor
einer Einreichung: vollständig neu erheben, oder nur die Funktionsliste gegen
das Produktdatenblatt abgleichen und die Plattformvorgaben separat prüfen.

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
entsteht beim nächsten Start neu. Neu ist nur, dass die Prüfliste die Ausnahme
jetzt ausdrücklich nennt: In 3.21.3 verlangte der Archivschritt „aktiv nur die
aktuelle Fassung, README, `resources/` und `Archiv/`“ und wäre an diesem Ordner
immer fehlgeschlagen. Zu entscheiden: beim nächsten Aufräumen von Hand
entfernen, oder dauerhaft ignorieren.

### Synchronisierung von Kalendern

Der Import legt an und erkennt eigene Punkte über die `UID` wieder, aktualisiert
aber keine vorhandenen; die Ausgabe hält `SEQUENCE` fest auf `0`. Ein echter
Abgleich wäre Synchronisierung – mit Konfliktregeln, Löschweitergabe und
Abonnements. Bleibt eine eigene Entscheidung.

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
