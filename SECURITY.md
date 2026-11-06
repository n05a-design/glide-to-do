# Sicherheitsrichtlinie

Stand 06.11.2026 · Glide 3.50.5 · Erster öffentlicher Stand (öffentliche erste Beta); 3.50.3–3.50.5 ändern nur Oberfläche und Titelgrenzen, die hier beschriebenen Vertrauensgrenzen bleiben unverändert

Glide verarbeitet Aufgaben, Notizen, Seiten, Pinnwände und Anhänge lokal. Die Kernanwendung benötigt weder Konto noch Netzwerkzugriff. Bewusst angeklickte Weblinks und Anhänge werden an das jeweilige Standardprogramm übergeben; die dortige Verarbeitung liegt außerhalb von Glide. Die verbindlichen [technischen Sicherheitsgrenzen](01_Repository/Glide/SECURITY.md) ergänzen diese Richtlinie.

## Unterstützte Fassungen

Sicherheitskorrekturen gehen in den aktuellen 3.50-Stand auf `main` und anschließend in die Python-Fassung und die nativen Pakete. Der tatsächliche Paket- und Prüfstand ist im [QA-Bericht](01_Repository/Glide/docs/07_QA_BERICHT.md) dokumentiert. Frühere Entwicklungsfassungen erhalten keine eigene Wartungszusage.

## Schwachstelle melden

Bitte vertraulich über [Security → Report a vulnerability](https://github.com/n05a-design/glide-to-do/security/advisories/new) melden. Sicherheitsfunde gehören nicht in öffentliche Issues.

Hilfreich sind die betroffene App- und Paketversion, Betriebssystem, gegebenenfalls Python-/Tk-Version, reproduzierbare Schritte sowie erwartetes und tatsächliches Verhalten. Verwende künstliche Beispieldaten und entferne Zugangsdaten, echte Inhalte, Benutzerpfade und private Anhänge aus Belegen.

Nach Eingang wird der Befund bewertet, mit künstlichen Daten nachvollzogen und bei Bestätigung mit einer geprüften Korrektur bearbeitet. Bei Bedarf folgt ein Security Advisory. Feste Reaktionsfristen werden derzeit nicht zugesagt.

## Umfang und Vertrauensgrenzen

- Anwendung unter `01_Repository/Glide/src/glide` und ihre Lieferkopie in `07_Python-Versionen`.
- Unvertrauenswürdige Eingaben: Sicherungen, Vorlagen, Austauschdateien, Notion-Archive, CSV, ICS, Markdown und Anhänge. Auch lokale Dateien können manipuliert sein.
- Datenhaltung: Originalbestand, Sicherungen, Einstellungen, Sperrbesitz und Wiederherstellung; Schutz vor unbemerktem Überschreiben oder Datenverlust.
- Mitgelieferter nativer Code, Systemdecoder, Paketierung, Bauabhängigkeiten, Prüf-/Pflegewerkzeuge und GitHub-Workflows.
- Berichtenswert sind erreichbare Verletzungen dieser Grenzen mit nachvollziehbarem Einfluss auf Vertraulichkeit, Integrität oder Verfügbarkeit. Die lokale Ausführung allein macht einen Befund nicht unerheblich.

Reine Fehler in unverändertem Python, Tcl/Tk oder dem Betriebssystem bitte zusätzlich dem jeweiligen Hersteller melden. Fehler in Glides Nutzung oder Paketierung dieser Komponenten bleiben im Umfang. Diese Richtlinie führt keine weiteren Befundausnahmen oder akzeptierten Risiken ein.

## Schutz der Projektablage

GitHub Actions verwendet begrenzte Berechtigungen, Checkout ohne gespeicherte Zugangsdaten und unveränderliche Action-Commits. Bauabhängigkeiten sind mit Version und Original-SHA-256 festgelegt; pip erzwingt ihre Hashprüfung. Die CI prüft unter anderem Tests, Lieferabgleich, Fremdcodeherkunft, Benutzerpfade und Ablagegrenzen. Laufberichte belegen jeweils nur ihren tatsächlichen Quellstand.

Schlüssel, Zertifikate, Tokens, echte Nutzerbestände, Rohlogs und lokale Arbeitskopien gehören nicht in die öffentliche Ablage. `.gitignore` schützt vor versehentlichem Hinzufügen neuer Dateien; bereits versionierte Dateien, `git add -f` und Webuploads erfordern weiterhin Prüfung. Paketprüfungen und Signaturen sind im [Liefernachweis](01_Repository/Glide/docs/07_QA_BERICHT.md) getrennt ausgewiesen.
