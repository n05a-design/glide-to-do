# Sicherheit

Glide verarbeitet lokale Nutzerdaten und lokale Anhänge. Die Anwendung überträgt diese Daten nicht selbstständig an externe Dienste und öffnet keine Netzwerkverbindungen.

## Grundregeln

- Keine Zugangsdaten, privaten Schlüssel, Zertifikatsdateien oder Signing-Secrets in diesem Repository speichern.
- `.glidebackup` nur aus vertrauenswürdiger Quelle importieren. Glide prüft Pfade, Größen, Schema, Kompressionsrate, Dateianzahl, Symlinks und referenzierte Dateien und akzeptiert die Formate 4 bis 10 (`MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis `DATA_SCHEMA_VERSION`). Das ersetzt keine allgemeine Malwareprüfung des Betriebssystems.
- Beim Hinzufügen erzeugt Glide unter `attachments/` eine atomar geschriebene lokale Kopie. Der Speichername entsteht seit 2.5.5 aus derselben geprüften Funktion wie beim Backup-Import und wird vor dem Kopieren validiert, damit kein Pfad entsteht, den die Anwendung später nicht mehr auflösen kann. Der Inhalt der Datei wird nicht auf Schadsoftware geprüft.
- Ein Backup-Import ersetzt den gesamten Bestand. Glide legt vorher automatisch ein vollständiges `vor_import_*.glidebackup` unter `backups/` an und schreibt die neuen Daten erst nach vollständiger Prüfung.
- Vor Datenmigrationen und Releases ein vollständiges Backup erstellen.
- Finale Installer und DMGs vor Veröffentlichung signieren, verifizieren und mit SHA-256-Hashes dokumentieren.

## Testläufe

Automatisierte und manuelle Tests dürfen den echten Datenordner nicht berühren. Dafür `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis setzen. Die frühere Isolierung allein über `APPDATA` wirkte nur unter Windows. `GLIDE_DATA_DIR` muss **vor** dem Import des Moduls gesetzt sein; danach ist der Datenordner bereits bestimmt.

Seit 3.2.0 sucht Glide beim Start nicht mehr in Ordnern früherer Programmnamen nach Nutzerdaten. Der Datenordner ist damit ausschließlich der oben genannte oder der über `GLIDE_DATA_DIR` gesetzte – ein Programmstart liest keine fremden Verzeichnisse mehr.

## Meldung

Ein öffentlicher Sicherheitskontakt ist noch nicht festgelegt. Bis dahin dürfen Sicherheitsfunde nicht über öffentliche Issues mit echten Nutzerdaten oder Anhängen geteilt werden.
