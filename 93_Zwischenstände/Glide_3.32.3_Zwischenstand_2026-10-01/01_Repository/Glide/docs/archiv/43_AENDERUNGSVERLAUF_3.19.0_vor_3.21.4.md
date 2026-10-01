# Dauerhafter Änderungsverlauf – Glide 3.19.0

Stand: 13.09.2026 · interner Entwicklungsstand · **Aufgabenformat 15** · Einstellungen 2 · Vorlagen 2

Rückgängig reicht nur bis zum Programmstart, und der Papierkorb weiß nur, dass etwas
gelöscht wurde – nicht, wann eine Frist verschoben oder ein Punkt umbenannt wurde. 3.19
führt ein dauerhaftes Protokoll: Was sich im Bestand geändert hat, bleibt nachlesbar, auch
Wochen später.

## Wie der Verlauf entsteht

Der Verlauf wird **nicht** an jeder Bedienstelle einzeln mitgeschrieben, sondern beim
Speichern aus dem Vergleich zweier Stände abgeleitet: Glide hält den letzten gespeicherten
Bestand als Vergleichsstand und bildet beim nächsten Speichern die Unterschiede auf
Ereignisse ab.

Das ist die tragende Entscheidung dieses Pakets. Ihr Vorteil: **jede** Änderung wird
erfasst, gleich über welchen Weg sie kam – Klick, Tastatur, Kontextmenü,
Mehrfachbearbeitung, Ziehen, Import, Vorlage, Wiederherstellung, Serienvorrücken. Es gibt
keine Bedienstelle, die man vergessen kann, und künftige Funktionen erscheinen
automatisch im Verlauf. Der Preis: Der Verlauf beschreibt das **Ergebnis**, nicht die
Absicht. Er nennt „Fälligkeit geändert", nicht „über das Kontextmenü geändert", und was
innerhalb eines Speichervorgangs zusammen passiert, erscheint als eine Gruppe von
Ereignissen mit demselben Zeitstempel.

## Erfasste Vorgänge

| Ereignis | Wird ausgelöst durch |
| --- | --- |
| Angelegt | neuer Punkt, neue Liste, neuer Ordner, neues Label |
| Geändert | Text, Beschreibung, Wichtigkeit, Fälligkeit, Uhrzeit, Wiederholung, Erinnerung, Bearbeitungstag, Aufwand, Farbe, Labels, Art, Anhänge – die geänderten Felder stehen im Eintrag |
| Erledigt / Wieder offen | Erledigt-Zustand eines Punkts |
| Verschoben | anderer Elternpunkt, andere Liste, anderer Ordner |
| Umbenannt | Titel einer Liste oder eines Ordners |
| In den Papierkorb | Punkt, Liste oder Ordner gelöscht |
| Wiederhergestellt | Rückholen aus dem Papierkorb |
| Endgültig entfernt | Papierkorb geleert oder Eintrag endgültig gelöscht |
| Bestand ersetzt | Wiederherstellung eines Backups oder App-Backups |

Jeder Eintrag trägt Zeitpunkt (auf die Sekunde), Vorgang, Art des Objekts, den Namen des
Objekts zum Zeitpunkt des Ereignisses, die zugehörige Liste und – bei Änderungen – die
betroffenen Felder. Namen werden auf 120 Zeichen gekürzt; Beschreibungen, Notizen und
Anhangsinhalte werden **nicht** mitgeschrieben, nur die Tatsache ihrer Änderung.

## Sammeleinträge

Wer 400 Zeilen aus einer CSV-Datei importiert, will keine 400 Verlaufseinträge. Ab
**25 gleichartigen Ereignissen** in einem Speichervorgang entsteht deshalb ein
Sammeleintrag („412 Punkte angelegt"), der die Einzelereignisse ersetzt und die Zahl
nennt. Darunter bleibt jedes Ereignis einzeln stehen.

## Bedienung

- **Ansicht → „Änderungsverlauf …"** oder Tastenkürzel **Strg/Cmd+H**; auch über die
  durchsuchbaren App-Aktionen.
- Die Tabelle zeigt Zeitpunkt, Vorgang, Objekt und Liste, die neuesten Einträge oben.
- **Suchfeld** über Objektname, Vorgang, Liste und Feldnamen; **Zeitraum** (alles, heute,
  7 Tage, 30 Tage) und **Art** (alles, Punkte, Listen und Ordner, Papierkorb) als
  Auswahlfelder. Die Kopfzeile nennt die Zahl der angezeigten und der gespeicherten
  Einträge.
- **„Als TXT speichern …"** schreibt die gerade angezeigte Auswahl als lesbare Textdatei.
- **„Verlauf leeren"** löscht das Protokoll nach Rückfrage vollständig; der Bestand bleibt
  unberührt. Das Leeren ist selbst kein Verlaufseintrag.
- In den Einstellungen schaltet **„Änderungen protokollieren"** die Erfassung ab.
  Ausgeschaltet entstehen keine neuen Einträge; vorhandene bleiben erhalten und lesbar.

## Datenvertrag Format 15

`glide_liste.json` erhält das Feld `history` **neben** den Aufgabenfeldern:

```
history = [
  { "id": "…", "at": "2026-09-13T21:15:04", "kind": "item|list|folder|label|data",
    "action": "created|updated|done|reopened|moved|renamed|trashed|restored|purged|replaced",
    "target": "Name zum Zeitpunkt des Ereignisses", "list": "Listentitel",
    "fields": ["due", "importance"], "count": 412 }
]
```

`fields` steht nur bei Änderungen, `count` nur bei Sammeleinträgen. Die Obergrenze liegt
bei **4000 Einträgen**; ist sie erreicht, fallen die ältesten weg. Einträge sind
unveränderlich – Glide schreibt sie nur an, korrigiert sie nie nachträglich.

**Migration:** Ein Bestand im Format 14 oder älter erhält beim ersten Speichern ein leeres
`history` und die Formatangabe 15. Vorher legt Glide, wie bei jedem Formatsprung, eine
unveränderte Kopie der Originaldatei als `liste_vor_format15_<Zeitstempel>.json` im
Backup-Ordner ab. Es entsteht **kein** rückwirkender Verlauf: Was vor der Umstellung
geschah, ist nicht rekonstruierbar, und Glide erfindet dafür keine Einträge.

Ein defektes, fremdes oder zu großes `history`-Feld wird beim Laden verworfen, ohne die
Aufgaben zu berühren – ein unlesbares Protokoll darf nie einen Bestand blockieren.
Komplettbackup und App-Backup führen den Verlauf mit, und ein vollständiges
Wiederherstellen übernimmt den Verlauf des Archivs samt einem Eintrag „Bestand ersetzt".
Ein **Teilbackup** ist ein Auszug einzelner Listen und enthält kein Protokoll; werden
Listen ergänzend hinzugefügt, bleibt der eigene Verlauf stehen und die neuen Objekte
erscheinen als angelegt. Ein Backup im Format 15 ist für ältere Glide-Fassungen
erwartungsgemäß nicht lesbar, umgekehrt werden Formate ab 4 weiterhin gelesen.

**Rückgängig und Verlauf sind getrennt:** Rückgängig stellt den Bestand wieder her, löscht
aber keine Verlaufseinträge – ein Protokoll, das sich selbst korrigiert, wäre keines. Die
Rücknahme erscheint stattdessen als weiteres Ereignis, weil sie den Bestand verändert.

## Grenzen

Kein Wiederherstellen eines einzelnen alten Wertes aus dem Verlauf – er ist ein Protokoll,
keine Versionsverwaltung; zum Zurücknehmen bleiben Rückgängig und Papierkorb zuständig, und
umgekehrt nimmt Rückgängig auch keine Verlaufseinträge zurück.
Keine alten Feldinhalte (nur welche Felder sich geändert haben), keine Verlaufsansicht am
einzelnen Punkt, kein Benutzer- oder Gerätebezug, keine Synchronisierung zwischen Geräten,
kein Export nach CSV oder JSON aus der Ansicht heraus, keine Filterung nach Feldnamen über
ein eigenes Auswahlfeld. Änderungen an Einstellungen, Vorlagen, Reitern, Pinnwänden und
gespeicherten Filtern sind kein Teil des Verlaufs – protokolliert wird der Aufgabenbestand.
Keine neue Laufzeitabhängigkeit, kein Hintergrundprozess, kein Netzzugriff.

## Abnahmekriterien

1. Ein Bestand im Format 14 wird beim ersten Speichern auf 15 gehoben, erhält ein leeres
   `history` und hinterlässt die Originalkopie im Backup-Ordner.
2. Jeder Vorgang der Tabelle oben erzeugt genau einen passenden Eintrag mit Zeitpunkt,
   Objektname und Liste; bei Änderungen stehen die betroffenen Felder darin.
3. Erledigen und Wiederöffnen erscheinen als eigene Vorgänge, nicht als „geändert".
4. Verschieben innerhalb einer Liste, zwischen Listen und zwischen Ordnern erscheint als
   „verschoben", nicht als Löschen plus Anlegen.
5. Papierkorb, Wiederherstellen und endgültiges Entfernen erzeugen die drei
   unterschiedlichen Vorgänge.
6. Ab 25 gleichartigen Ereignissen entsteht ein Sammeleintrag mit korrekter Zahl.
7. Die Obergrenze von 4000 Einträgen wird eingehalten; die ältesten fallen weg.
8. Der Verlauf übersteht Programmneustart und Komplettbackup-Rundlauf; ein Teilbackup
   trägt kein Protokoll, und ergänzendes Hinzufügen lässt den eigenen Verlauf stehen.
9. Ein defektes oder fremdes `history`-Feld wird verworfen, ohne die Aufgaben zu berühren.
10. Ausgeschaltete Protokollierung erzeugt keine neuen Einträge und löscht keine alten.
11. „Verlauf leeren" entfernt alle Einträge und lässt Aufgaben, Listen und Ordner
    unverändert.
12. Suche, Zeitraum- und Artfilter wirken einzeln und gemeinsam; der Dialog ist in Hell und
    Dunkel bei 780×640 vollständig erreichbar, und Ansehen verändert nichts.
13. Rückgängig stellt den Bestand wieder her und lässt die Verlaufseinträge stehen.

## Prüfung

Die Suite `tests/integration/test_features319.py` prüft mit isoliertem `GLIDE_DATA_DIR`
die Migration von Format 14 samt Originalkopie, jeden erfassten Vorgang einzeln, die
Feldliste bei Änderungen, Erledigen und Wiederöffnen, Verschieben in allen drei Varianten,
die drei Papierkorbvorgänge, Sammeleinträge an der Schwelle, die Obergrenze, den Rundlauf
über Komplett- und Teilbackup, defekte und fremde Verlaufsfelder, die abschaltbare
Erfassung, das Leeren, Suche und Filter sowie den Dialog in beiden Themes bei 780×640. Der
Gesamtlauf umfasst damit 23 Suiten.
[QA-Bericht](07_QA_BERICHT.md) · [Datenvertrag](06_DATA_BACKUP_MIGRATION.md) ·
[CSV-Import 3.18](42_CSV_IMPORT_3.18.0.md)
