# Offene Entscheidungen – Glide 3.21.1

Stand: 14.09.2026 · interner Entwicklungsstand

## Neu aufgeworfen

### Überholte Versionsangaben im Releasebestand

`tests/tools/releasedaten.py` hängt in der Hilfsfunktion `code()` (Zeile 70) an **jeden**
Codebeleg den Zusatz „Stand: 3.14.0 / Datenformat 13." und trägt im Kopf eine Memo-Zeile
„Releaseplanung für Glide 3.14.0 / Datenformat 13 · Recherche 04.09.2026". Beides steht
seit 3.14 unverändert im mitgelieferten Releasebestand, obwohl die App bei 3.21.1 und
Format 15 liegt. Auch `DEFAULT_TARGET` zeigt noch auf
`glide_releaseplanung_3.14.0.glidebackup`.

Beim Prüfstand fällt es nicht auf: Der Abgleich vergleicht die Fixture mit ihrer eigenen
Neuerzeugung, beide tragen denselben überholten Text. Aufgefallen ist es beim
Versionssprung auf 3.21.1.

**Bewusst nicht mitbehoben.** 3.21.1 ist eine Fehlerbehebung mit engem Schnitt; eine
Textkorrektur quer durch den Beispielbestand ändert den Inhalt von 159 Punkten und
gehört in einen eigenen, prüfbaren Schritt. Zu entscheiden:

- die Angaben auf `APP_VERSION` und `DATA_SCHEMA_VERSION` umstellen, damit sie mit jedem
  Sprung mitwandern (empfohlen – derselbe Mechanismus, den die Memo-Zeile in Zeile 196
  schon nutzt), oder
- den Zusatz ganz weglassen, weil der Codebeleg ohne Versionsangabe auskommt, oder
- so lassen, weil der Bestand nur der Releaseplanung dient und niemand den Zusatz liest.

### Zeitzone des Prüfstands

`Europe/Berlin` ist jetzt die Vorgabe, wenn der Aufrufer keine Zone setzt. Das macht
Läufe über Maschinen hinweg vergleichbar und deckt beide Versätze ab, verdeckt aber eine
Zonenbesonderheit der jeweiligen Maschine. Die vier Zonen in `test_features321.py`
fangen das für den Kalenderrundlauf auf. Zu entscheiden, wenn weitere zeitabhängige
Funktionen hinzukommen: ob der Prüfstand einen zweiten Durchgang in einer westlichen
Zone bekommt, oder ob das bei den betroffenen Suiten bleibt.

## Aus 3.21.0 weiterhin offen

### Synchronisierung von Kalendern

Der Import legt an und erkennt eigene Punkte über die `UID` wieder, aktualisiert aber
keine vorhandenen. Ein echter Abgleich wäre Synchronisierung – mit Konfliktregeln,
Löschweitergabe und Abonnements. Bleibt eine eigene Entscheidung, nicht Teil des Imports.

### Schreibungsabhängigkeit des Beispielbackups

`tests/integration/test_glide.py` erwartet `Glide_Beispieldaten.glidebackup`, im
Repository liegt `glide_beispieldaten.glidebackup`. Unter macOS und Windows identisch,
unter Linux nicht. In der Vorabumgebung per Kopie umgangen. Zu entscheiden: Erwartung im
Test auf die tatsächliche Schreibung ziehen (empfohlen, einzeilig) oder die Datei
umbenennen und alle Verweise nachziehen.

### Nicht abbildbare Wiederholungsregeln

`COUNT`, `BYMONTHDAY`, `BYSETPOS` und Intervalle bei Wochen, Monaten und Jahren werden
verworfen und gezählt, statt still vereinfacht zu werden. Ob Glide eigene
Wiederholungsarten dafür bekommt, bleibt offen.
