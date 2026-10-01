# Ablageprüfung – 11.09.2026 (historischer Prüfstand)

Dieses Dokument ist ein abgeschlossener Nachweis und wird nicht nachgezogen. Der aktuelle Stand steht im [Dokumentationsindex](00_INDEX.md) und im [QA-Bericht](07_QA_BERICHT.md).

Dieser datierte Abgleich beschreibt die damalige 3.7-Ablage. Für den heutigen
Stand sind der [Dokumentationsindex](00_INDEX.md) und der
[QA-Bericht](07_QA_BERICHT.md) maßgeblich.

## Ergebnis

40 überholte Dateien wurden aus aktiven Verzeichnisebenen in den jeweils lokalen
Archiv-Unterordner verschoben. Von 37 überarbeiteten Dokumenten und Arbeitsdateien
wurde zuvor eine Kopie gesichert. Keine Datei wurde endgültig gelöscht.
Das [Archivmanifest](../tests/qa-3.7.0/macos-nachbesserung/archiv_manifest.json)
nennt Quelle, Archivziel, Aktion und SHA-256 des Ausgangsstands.

## Aktiver Bestand

- `src/glide/app.pyw` ist die kanonische App. Die Python-Datei unter
  `07_Python-Versionen` wird samt vollständigen Ressourcen bytegleich mitgeführt.
- `src/glide/resources/templates/glide_vorlagen.glidetemplates` ist der kanonische
  Katalog. Die benannte Importkopie liegt unter `05_Probelisten_Testdaten`.
- In `05_Probelisten_Testdaten` liegen inzwischen die aktuellen Aufgabenbackups
  `Glide-Funktionsvorschau_3.13.0.glidebackup` und
  `Glide-Releaseplanung_3.13.0.glidebackup`; die damaligen 3.7-Dateien bleiben
  als historische Vorgänger erhalten.
- Die bisherigen Word-Berichte einschließlich des 3.7-Berichts vor dieser
  Nachbesserung sind archiviert. Aktuelle Anleitung, Auftragsabgleich und QA
  stehen als direkt lesbare Markdown-Dokumente zur Verfügung.
- Versionsgebundene Oberflächen- und QA-Berichte von 3.4 bis 3.6 wurden unter
  `docs/archiv` eingeordnet. Aktuelle Dateilinks wurden auf die neuen Ziele umgestellt.
- Historische Import-Fixtures unter `tests/fixtures` bleiben als bewusst
  benötigte Migrationseingänge erhalten. Alte QA-Nachweise und Grafikquellen
  unter `50_Ablage` und `20_Grafik_Master` bleiben ebenfalls erhalten.
- Store-Arbeitsunterlagen bleiben Entwürfe. Ihre externen Anforderungen wurden
  in diesem Auftrag nicht neu recherchiert und sind vor Einreichung zu prüfen.

## Backupprüfung

Alle 13 `.glidebackup`-Dateien in der Arbeitsablage und ihrem Archiv ließen sich
als ZIP mit gültigem JSON lesen; die ZIP-Prüfsummen sind gültig. Die beiden
aktuellen Backups werden außerdem durch den echten App-Import geprüft und mit
ihren Erzeugern verglichen. Ein lesbares historisches Archiv ist keine Freigabe
seines Inhalts für einen aktuellen Arbeitsbestand.

Das [Backupinventar](../tests/qa-3.7.0/macos-nachbesserung/backup_inventar.json)
verzeichnet Schema- und App-Versionen. Echte Nutzdatenverzeichnisse, persönliche
Backups und die vom Benutzer gezeigten Original-Screenshots wurden nicht verändert.

## Pflege

Aktuelle Arbeitskopien nur aus der kanonischen Quelle erzeugen. Vor einer
Überarbeitung eine versionierte Archivkopie im selben Bereich erstellen.
Archivdateien sind Nachweise, keine parallel zu pflegenden Arbeitsfassungen.
`README.md` in der übergeordneten Glide-Ablage ist der gemeinsame Einstieg.
