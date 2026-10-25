# Sicherheit

Glide verarbeitet lokale Nutzerdaten und lokale Anhänge. Die Anwendung überträgt diese Daten nicht selbstständig an externe Dienste und öffnet keine Netzwerkverbindungen. Links in Notizen (nur `http(s)://` und `mailto:`) gibt sie ausschließlich auf Klick an den Standardbrowser weiter.

## Grundregeln

- Keine Zugangsdaten, privaten Schlüssel, Zertifikatsdateien oder Signing-Secrets in diesem Repository speichern.
- `.glidebackup` nur aus vertrauenswürdiger Quelle importieren. Glide prüft Pfade, Größen, Schema, Kompressionsrate, Dateianzahl, Symlinks und referenzierte Dateien und akzeptiert die Formate 4 bis 26 (`MIN_PORTABLE_BACKUP_SCHEMA_VERSION` bis `DATA_SCHEMA_VERSION`). Das ersetzt keine allgemeine Malwareprüfung des Betriebssystems.
- Beim Hinzufügen erzeugt Glide unter `attachments/` eine atomar geschriebene lokale Kopie. Der Speichername entsteht seit 2.5.5 aus derselben geprüften Funktion wie beim Backup-Import und wird vor dem Kopieren validiert, damit kein Pfad entsteht, den die Anwendung später nicht mehr auflösen kann. Der Inhalt der Datei wird nicht auf Schadsoftware geprüft.
- Ein Komplettimport ersetzt den Aufgabenbestand. „Listen/Ordner hinzufügen“ ergänzt den Bestand. Glide legt vorher automatisch ein vollständiges `vor_import_*.glidebackup` unter `backups/` an und schreibt die neuen Daten erst nach vollständiger Prüfung.
- Vor Datenmigrationen und Releases ein vollständiges Backup erstellen.
- Finale Installer und DMGs vor Veröffentlichung signieren, verifizieren und mit SHA-256-Hashes dokumentieren.

## Vertrauensgrenzen

Am 25.10.2026 gegen den Quellstand geprüft ([Analyse §13.12](../../00_Arbeitsvorbereitung/Glide_Analyse.md#1312-sicherheits--und-architekturgutachten-vom-25102026)). Geschützt werden Aufgaben, Notizen, Anhänge, Sicherungen, Einstellungen sowie später Releaseartefakte und Signaturidentität. Offene Punkte stehen mit Kennung im [Entwicklungsplan](../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#212-ergänztes-aufgabenregister-und-gemeinsame-komponenten); diese Tabelle ersetzt kein Penetrations- oder Fuzzingergebnis.

| Grenze | Was Glide heute absichert | Offen |
|---|---|---|
| Fremde Dateien: `.glidebackup`, `.glidetemplates`, `.glideexchange`, CSV, ICS, Notion-ZIP | Archive: Pfad-, Größen-, Eintrags-, Symlink-, Verschlüsselungs- und Kompressionsprüfung, Anhänge gestreamt ausgepackt, kein `extractall`. Austausch, CSV und ICS: höchstens 12 MiB, Feld- und Schemaprüfung. Sicherungen werden erst nach vollständiger Prüfung und nach einer Vorab-Sicherung übernommen, Importe sind ein Rückgängig-Schritt | Vorlagenimport prüft vorab nur 4 GiB und liest JSON vollständig in den Speicher (WA-47) |
| Eigener Datenordner, auch in einem Cloudordner | atomares Schreiben, lokale Sitzungssperre, Schreibschutz bei fremder oder unlesbarer Sperre, Startprüfung, Sicherungen nur bei Änderung | keine verteilte Sperre zwischen Rechnern (nacheinander arbeiten); Hauptdatei und Einstellungen ohne Vorabgrenze, vollständige Sicherungen scheitern über 32 MiB Daten ohne Frühwarnung (WA-47); stille Fehler beim Sicherungspunkt im Leerlauf und bei Einstellungen (WA-40) |
| Anhänge | Speichername nur `attachments/<Name>`, bereinigt und kanonisch aufgelöst, auch beim Import neu vergeben; höchstens 512 MiB je Datei | keine Malwareprüfung; Öffnen übergibt ohne Rückfrage an das Standardprogramm, auch bei ausführbaren Typen (WA-48) |
| Ausgaben: CSV, Druck-HTML, Markdown | Formelanfänge in CSV geschützt, HTML maskiert, keine externen Verweise in der Druckansicht | – |
| Systemdecoder und nativer Code (WIC über PowerShell, `sips`, `gdk-pixbuf-thumbnailer`/`djpeg`, tkDnD) | ein Wandlungs-Worker mit Warteschlange (32), Zeitlimit (45 s) und Abbruch; Unterprozesse ohne Shell; tkDnD nur mit geprüfter Prüfsumme | Pfade im PowerShell-Skript der Windows-Wandlung unvollständig maskiert (WA-51); ungeklärter nativer Windows-Absturz unter Last (WA-41); Beobachtung und Aktualisierung von tkDnD (WA-44) |
| GitHub Actions und Bauabhängigkeiten | nur Leserechte, keine Geheimnisse, Checkout ohne gespeichertes Token, Fremdcodevergleich gegen das PyPI-Original, feste Versionen | Actions über Tags statt Commit-SHA (WA-43); Bauabhängigkeiten ohne Hashes (WA-45); kein Release-Inventar (WA-46); CodeQL analysiert die Hauptdatei voraussichtlich nicht (I12) |
| Releaseartefakte und Signaturidentität | keine Secrets im Repository; Ablauf für Signatur und Notarisierung in der [Veröffentlichung](docs/10_VEROEFFENTLICHUNG.md#signierung-und-notarisierung) | noch nichts öffentlich signiert (I3) |
| Öffentliche Git-Historie | CI verhindert neue Benutzerpfade und Rohprotokolle; Secret Scanning aktiv | ältere Historie enthält gelöschte Protokolle mit Benutzerpfaden (I10) |

Missbrauchsfälle, an denen Änderungen zu messen sind: manipuliertes Backup oder Vorlagenpaket, ZIP-Bombe, Pfadtraversal, übergroßes JSON, schädlicher Anhang, Sperrkonflikt zweier Instanzen, kompromittierte Action oder Bauabhängigkeit, beschädigte Einstellungen, Absturz nach dem Schreiben der Hauptdatei.

## Mitgelieferter nativer Code

Seit dem 27.09.2026 liegt unter `src/glide/vendor/tkinterdnd2` die
Tk-Erweiterung tkDnD als native Bibliothek je Plattform (Herkunft und
Prüfsumme in `src/glide/vendor/provenance.json`,
[Entscheidung](docs/decisions/ABHAENGIGKEIT_TKDND.md)). Sie wird nur für das
Ziehen aus Finder/Explorer geladen. Vor einer Veröffentlichung muss sie mit
dem Release signiert und notarisiert werden; eine neue Fassung nur mit
geprüfter Prüfsumme übernehmen.

## Testläufe

Automatisierte und manuelle Tests dürfen den echten Datenordner nicht berühren. Dafür `GLIDE_DATA_DIR` auf ein temporäres Verzeichnis setzen. Die frühere Isolierung allein über `APPDATA` wirkte nur unter Windows. `GLIDE_DATA_DIR` muss **vor** dem Import des Moduls gesetzt sein; danach ist der Datenordner bereits bestimmt.

Seit 3.2.0 sucht Glide beim Start nicht mehr in Ordnern früherer Programmnamen nach Nutzerdaten. Der Datenordner ist der Standardordner, die über die gerätespezifische Zeigerdatei gewählte Ablage oder der über `GLIDE_DATA_DIR` gesetzte – ein Programmstart liest keine fremden Verzeichnisse mehr.

## Meldung und öffentliches Repository

Meldeweg, Umfang und die Schutzmaßnahmen des öffentlichen Repositorys (CI-Prüfungen, `.gitignore`, Secret Scanning, keine Rohprotokolle und Benutzerpfade) stehen in der [Sicherheitsrichtlinie](../../SECURITY.md).
