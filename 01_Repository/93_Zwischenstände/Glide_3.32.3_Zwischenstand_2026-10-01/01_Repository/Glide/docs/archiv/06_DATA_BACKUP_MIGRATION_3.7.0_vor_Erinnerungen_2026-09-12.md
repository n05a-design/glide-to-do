# Daten, Backups und Migration – Glide 3.7.0

Stand: 12.09.2026

| Datei/Format | Bedeutung | Transport |
|---|---|---|
| liste_speicher.json · Format 12 | Ordner, Listen, Punkte, Labels, Wiederholungen, Papierkorb | Aufgabenbackup |
| settings.json · Format 2 | Theme, Personalisierung, letzte Ansicht, Bearbeitungs-/Erledigungshistorie | Datenordnerkopie |
| vorlagen.json · Format 2 | System- und eigene Vorlagen | .glidetemplates oder Datenordnerkopie |
| attachments/ | Verwaltete lokale Anhangsdateien | ZIP-Backups einschließlich referenzierter Dateien |
| backups/ | Lokale Sicherungsstände | Datenordnerkopie |
| glide.lock | Temporäre Belegungsinformation | Nicht in die Ordnerkopie übernehmen |
| datenordner.json | Gerätebezogener Zeiger auf die Ablage | Nicht im Aufgabenbackup |

## Vollbackup und ergänzender Import

Ein `.glidebackup` ist ein ZIP mit `data.json` und referenzierten Anhängen.
Vollimport ersetzt den Bestand nach Validierung und vollständiger Sicherung.
Der ergänzende Import verwendet denselben begrenzten Archiv-/Stagingpfad und
erzeugt neue Listen-, Ordner-, Punkt- und Anhangs-IDs. Vorhandene Inhalte bleiben
erhalten. Eigene Labels werden zugeordnet oder mit konfliktfreiem Namen ergänzt;
feste Artlabels werden auf die lokalen Systemlabels abgebildet.

Teilbackups enthalten nur die ausgewählten Listen bzw. vollständigen
Ordnerzweige. Leere Unterordner bleiben enthalten. Externe Elternverweise werden
an der Exportgrenze gelöst. Inhalte, Farben, Labels, Fälligkeit/Uhrzeit,
Wiederholungen und Anhänge bleiben erhalten. TXT/Markdown sind lesbare Exporte;
der strukturtreue Ordner-Rundlauf ist das Glide-Backup.

Archivpfade, doppelte Namen, Symlinks, Größen und Kompressionsverhältnisse werden
geprüft. Anhangsdateien erhalten beim Import neue Speicherpfade und werden erst
vor dem atomaren Commit bereitgestellt. Fehler entfernen nur neu angelegte
Importdateien. Vorherige Nutzdaten werden nicht ersetzt, bevor die Prüfung
erfolgreich ist.

## Vorlagen

Zehn ausgearbeitete Listenvorlagen und sechs Ordnervorlagen werden bei fehlendem Katalog
angeboten. Ein absichtlich leer gespeicherter Katalog bleibt leer. Eigene
Vorlagen bewahren vollständige Teilpayloads einschließlich Unterpunkten und
Anhangsbytes. Beim Verwenden entstehen neue IDs; Aufgaben starten unerledigt.
Vorlagenbearbeitung verändert den Katalog erst im Arbeitsspeicher;
„Vorlagen speichern“ schreibt ihn atomar. Aufgabenbackups sichern den Katalog
nicht mit. Für ihn `.glidetemplates` exportieren.

## Wechsel der Ablage

Die Zeigerdatei liegt im normalen Benutzerbereich, unter Windows
`%APPDATA%/Glide/datenordner.json`. `GLIDE_DATA_DIR` hat Vorrang und eignet
sich für Tests. Ein leerer Zielordner erhält eine Kopie; ein vorhandener
Datenordner wird geöffnet. Der Quellordner bleibt erhalten. Die Kopie darf
nicht innerhalb ihrer Quelle liegen und keine bestehenden Zieldateien ersetzen.

Die Belegungsdatei wird anhand von Host, Prozess und Zeit geprüft. Bei erkannter
Fremdbelegung speichert dieser Start nicht. Sie kann keine zwei noch nicht
synchronisierten Cloudkopien verriegeln. Der Bedienablauf bleibt sequenziell:
Glide schließen, Abgleich abwarten, am nächsten Gerät öffnen.

## Kompatibilität und Grenzen

Version 3.7 erweitert das Aufgabenformat auf 12: Listen und Ordner erhalten
ein leeres `attachments`-Array, wenn es fehlt. Die Referenzen 4–12 und Legacy 2
bleiben erhalten. Die Migration von Format 10 zu 11 ergänzt Wiederholungen;
alte Punkte bleiben gültig. Einstellungserweiterungen sind additiv.
Unbekannte neuere Vorlagenformate werden abgewiesen.

Die historischen Grenzen für Punkttiefe und Labelanzahl sowie seltene
Strukturkombinationen sind im [historischen Befund](11_BESTANDSANALYSE.md)
beschrieben. Sie sind keine uneingeschränkte Freigabe sämtlicher denkbarer
Bestände. Der aktuelle [QA-Nachweis](24_VERSION_3.7.0.md) beschreibt die geprüften Fälle.

## Stand 3.7.0

Aktuelle Ergänzungen und Prüfnachweise: [Version 3.7.0](24_VERSION_3.7.0.md). Versionsgebundene 3.6-Berichte beschreiben den vorherigen Stand.

Vor dem ersten Überschreiben älterer lokaler Daten entsteht `backups/liste_vor_format12_<Zeitstempel>.json` mit unveränderten Originalbytes; die normale Rotation entfernt diese Kopie nicht. Wenn die Kopie fehlschlägt, wird der neue Datenstand nicht gespeichert. Containeranhänge werden bei Voll-/Teilbackup, ergänzendem Import, Vorlagen, Kopieren und Papierkorb mitgeführt. Ältere App-Versionen können Format 12 nicht lesen.

## Nachbesserung vom 11.09.2026

Mac-Trackpad unter Tk 9, vollständige isolierte Vorlagenbearbeitung, 16 Praxisvorlagen,
relative Termine mit Vorlagenformat 2 und verbesserte Aufgaben-Vorschauen.
Der aktuelle [Nachtrag mit Migration, Bedienung und Prüfgrenzen](26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md)
hat für diese Punkte Vorrang vor dem Prüfstand vom 07.09.2026.

## UI-Nachtrag 12.09.2026

Der thematisierte Vorlagenbaum, die Mac-Auswahlfelder und die dynamische
Kachelanordnung ändern kein Datenformat. Aufgaben bleiben Format 12,
Einstellungen Format 2 und Vorlagen Format 2. Alle bestehenden Migrations-
und Backup-Fixtures bleiben gültige Regressionseingänge; alte Nutzerbackups
werden nicht aufgrund ihres Alters entfernt.
