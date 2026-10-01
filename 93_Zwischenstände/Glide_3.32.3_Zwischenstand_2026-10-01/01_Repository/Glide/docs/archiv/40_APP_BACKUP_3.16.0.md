# Vollständiges App-Backup – Glide 3.16.0

Stand: 13.09.2026 · interner Entwicklungsstand · Aufgabenformat 14 · Einstellungen 2 · Vorlagen 2

Ein Aufgabenbackup enthält Listen, Ordner, Punkte, Labels, Papierkorb und Anhänge. Was
bisher fehlte, sind die persönlichen Einstellungen, der Vorlagenkatalog und die
Aktivitätsdaten – genau die Teile, die ein Gerätewechsel oder ein Neuaufsetzen sonst
verliert. 3.16 fasst alles in einem Archiv zusammen und zeigt vor dem Wiederherstellen,
was darin steckt.

## Bedienung

- **Datei → Vollständiges App-Backup speichern …** schreibt ein Archiv mit der Endung
  `.glideapp`. Die Erfolgsmeldung nennt denselben Inhaltsüberblick, den auch die
  Wiederherstellung zeigt, samt Zahl der enthaltenen Anhangsdateien.
- **Datei → App-Backup wiederherstellen …** liest ein `.glideapp` oder ein
  `.glidebackup` und öffnet zuerst die **Inhaltsvorschau**: Erzeugerversion,
  Datenformat, Zeitstempel, Aufgaben, Listen, Ordner, Gruppen und Überschriften,
  Labels, Papierkorbeinträge, Anhänge, Vorlagen im Archiv und erfasste Aktivitätstage.
- Darunter stehen vier einzeln zuschaltbare Bereiche: **Aufgaben** (mit Ordnern,
  Labels, Papierkorb und Anhängen), **persönliche Einstellungen**, **Vorlagenkatalog**
  und **Aktivitätsdaten**. Bereiche, die das Archiv nicht enthält, sind gesperrt.
- Ohne Auswahl passiert nichts; Abbrechen und Escape lassen den Bestand unverändert.
  Der Dialog ist in Hell und Dunkel, in allen Schriftgrößen und bei kleiner
  Fensterhöhe vollständig bedienbar.

## Archivaufbau

Das Archiv ist dasselbe ZIP wie ein Komplettbackup: `data.json` plus die referenzierten
Anhangsdateien. Neu ist im JSON der Abschnitt `app_backup` **neben** den Aufgabenfeldern:

```
app_backup = {
  "format_version": 1,
  "settings":  { persönliche Einstellungen, ohne Tageshistorien, mit "theme" },
  "templates": { "format_version": 2, "templates": [ … ] },
  "activity":  { "completion_history": { … }, "activity_history": { … } }
}
```

Weil der Abschnitt neben den Aufgaben liegt und die Schemaprüfung unbekannte Felder
nicht verwirft, bleibt ein `.glideapp` für ältere Glide-Fassungen ein gültiges
Aufgabenbackup: Sie lesen die Listen und ignorieren den Rest. Umgekehrt ist ein
gewöhnliches `.glidebackup` ein App-Backup ohne Zusatzteil – die Vorschau weist die
fehlenden Bereiche ausdrücklich als „nicht enthalten“ aus.

Ein unbekannter `format_version`-Wert, ein falscher Typ in einem der drei Abschnitte,
eine Datei ohne Archivstruktur oder ein Archiv aus einer fremden Anwendung werden mit
Begründung abgewiesen, ohne den Bestand zu berühren. Die bestehenden Grenzen für
Mitgliederzahl, Datengröße und Anhangsgröße gelten unverändert.

## Wiederherstellung

Die Aufgaben laufen durch denselben geprüften Importpfad wie ein Komplettbackup:
Schemaprüfung, Abgleich der Anhänge, Zwischenablage der Dateien, Sicherung des
vorherigen Stands als `vor_import_<Zeitstempel>.glidebackup` und erst danach das
atomare Ersetzen. Die Rückfrage des Imports entfällt, weil die Inhaltsvorschau sie
bereits ersetzt.

Vor dem Ersetzen von Einstellungen oder Vorlagen entstehen
`settings_vor_restore_<Zeitstempel>.json` und `vorlagen_vor_restore_<Zeitstempel>.json`
im Backup-Ordner. Scheitert eine dieser Sicherungen oder das anschließende Schreiben,
bleibt der vorherige Stand im Speicher und auf der Platte bestehen und die
Wiederherstellung meldet den Fehler.

**Datenregel:** `today_plan`, `saved_filters`, `active_saved_filter`, `open_tabs`,
`active_tab`, `pinboards`, `table_columns` und die Liste zuletzt bearbeiteter Listen
verweisen auf Punkt- und Listen-IDs. Sie werden nur übernommen, wenn im selben Vorgang
auch die Aufgaben aus diesem Archiv kommen – sonst zeigten sie auf Objekte, die es hier
nicht gibt. Aktivitätsdaten sind ein eigener Bereich, damit ein Blick in ein fremdes
Archiv die eigene Jahresanzeige nicht überschreibt. Ein mitgesichertes Farbschema wird
mit den Einstellungen übernommen.

## Grenzen

Keine Cloudsicherung, kein Zeitplan, keine automatische Sicherung auf ein anderes
Gerät: Das Archiv entsteht, wenn man es anfordert. Kein Zusammenführen zweier Bestände
– die Aufgaben ersetzen, was vorhanden ist; für ergänzendes Hinzufügen bleibt
„Listen/Ordner hinzufügen …“ zuständig. Kein Teilrestore einzelner Listen aus einem
App-Backup, keine Versionsgeschichte innerhalb des Archivs, kein Passwortschutz und
keine Verschlüsselung. Der Datenordner-Zeiger und die Fenstergeometrie liegen außerhalb
der Einstellungsdatei und wandern nicht mit. Keine neue Laufzeitabhängigkeit, kein
Hintergrundprozess, kein Netzzugriff.

## Abnahmekriterien

1. Ein geschriebenes Archiv enthält alle vier Bereiche und lässt sich ohne
   Fehlermeldung wieder einlesen.
2. Dieselbe Datei bleibt als Aufgabenbackup gültig; die Schemaprüfung akzeptiert sie
   mit `portable=True`.
3. Die Vorschau nennt Erzeugerversion, Datenformat, Zeitstempel und alle Mengen; sie
   verändert nichts am Bestand.
4. Jeder Bereich lässt sich einzeln wiederherstellen, ohne die anderen zu berühren.
5. Ohne die Aufgaben des Archivs bleiben Ansichtsverweise leer.
6. Vor dem Ersetzen liegen Sicherungen für Aufgaben, Einstellungen und Vorlagen im
   Backup-Ordner.
7. Ungültige `format_version`, falsche Abschnittstypen, Nicht-Archive und fremde
   Archive werden abgewiesen, ohne etwas zu ändern.
8. Keine Auswahl und Abbruch lassen Bestand und Einstellungen unverändert.
9. Ein Archiv ohne Zusatzteil sperrt die drei Extrabereiche im Dialog.
10. Der Dialog ist in Hell und Dunkel bei 780×640 vollständig erreichbar.

## Prüfung

Die Suite `tests/integration/test_features316.py` prüft mit isoliertem `GLIDE_DATA_DIR`
Archivaufbau und Abschnittstrennung, den Rundlauf über echte Dateien, die Verträglichkeit
mit dem Aufgabenimport, alle Vorschauwerte einschließlich Anhangszählung über Listen,
Ordner und Punkte, sieben Varianten ungültiger Zusatzabschnitte, Nicht-Archiv und
fremdes Archiv, die vier Teilbereiche einzeln und gemeinsam, das Verwerfen der
Ansichtsverweise, die drei Rückfallsicherungen, leere Auswahl, Abbruch, gesperrte
Bereiche und den Dialog in beiden Themes bei 780×640. Der Gesamtlauf umfasst damit
20 Suiten. [QA-Bericht](../07_QA_BERICHT.md) · [Datenvertrag](../06_DATA_BACKUP_MIGRATION.md) ·
[Release-Checkliste](../10_RELEASE_CHECKLIST.md)
