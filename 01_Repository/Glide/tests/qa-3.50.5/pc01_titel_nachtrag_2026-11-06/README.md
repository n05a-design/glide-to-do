# PC 01 – Titel- und Prüfkopienachtrag 3.50.5

Benutzerauftrag 06.11.2026: Titelgrenzen in Test/Implementierung/Dokumentation abgleichen, vollständige Prüfmatrix starten und die letzten eigenen Änderungen committen. Merge übernimmt der Benutzer. Integration auf bereits gemergtem `main` `5e63ea346ae970d49269389011ed3f793aafc0ba`, Branch `codex/glide-3.50.5-titel-nachtrag`, getrennte lokale Arbeitskopie. Nur eigene Änderungen übernommen; neuere Kopf-/Bildfolgenkorrekturen erhalten. App `389cf046…`, Version 3.50.5 / Datenformat 26.

## Inhalt

Zentrale 40-Zeichen-Regel für neue/geänderte Titel auch in vollständigen Vorlagen, neuen Duplikaten samt Unteraufgaben, Vorlagenimport, Galeriebildtiteln und eigenen Austauschaufträgen. Lange neue Originaltitel in Beschreibung/Notiz erhalten, auch über Speichern/Laden. Unveränderte alte Titel, Quellen, Wiederherstellung und Export bewahren. Kalenderfaltung mit 300-Zeichen-Bestandstitel beibehalten und neue Grenzfälle ergänzen. `--no-hardlinks` für unabhängige Git-Objektkopien auf E; Byte-/Dateiidentität im Werkzeugtest prüfen.

## Nachweise und Grenzen

PC 01: AMD Ryzen 7 5800X3D, Python 3.14.7 x64 / Tcl/Tk 9.0.4, ausschließlich synthetische Daten. Drei getrennte rote Vorproben zu Vorlage/Galerie/Originalerhalt nach Korrektur grün. Frühere gemeinsame Fassung `246c6c3b…`: acht gezielte Gruppen einschließlich 32 Titelkonfigurationen und strenge Grundstufe 19/19 grün (zweimal 1.135 Fachtests, 244 Werkzeugtests/ein Skip). Diese Werte gelten nicht automatisch für die integrierte Fassung.

Neue gezielte Prüfung, strenge Grundstufe und anschließend breite Folge werden hier ergänzt. Voll-/Design-/Gestaltungs-/Leistungs-/Dauerlauf, native Pakete und Menschenabnahme getrennt ausweisen. Grüne GitHub-Läufe #276/#277 betreffen den Vorstand; #279 auf Merge `5e63ea34` war beim Nachlesen noch aktiv. Keine Übertragung von Online-Prüfungen auf neue Titelbytes. Kein Release oder menschlicher Freigabehaken durch den Commit.


## Bestätigte Prüfung des integrierten Nachtrags

Alle acht gezielten Gruppen grün: zehn Titel- und acht Auftrags-Fachtests, echte Auftragsdialoge, Kalenderexport/-import, Vorlagen, Galerie und Titelmatrix mit 32 Konfigurationen. Strenge CI-Grundstufe **19/19 grün**, Exitcode 0: zweimal **1.135 Fachtests**, **245 Werkzeugtests (ein Skip)**, Analysen, Startprobe, strenger Python-Lieferabgleich, Fremdcode, Datenschutz, Ablage und Synchronisation. [Maschinenlesbare Commitprüfung](commitpruefung.json).

Fortsetzung der vollständigen seriellen Prüfmatrix seit 09:43 MEZ unter `E:/gq/m1106-094317`, Status in `status.json`. Nach dem grünen Vorlauf/CI hat der vollständige Vollmodus tatsächlich begonnen; Design/UI-UX, Gestaltung/alle Arbeitsmodi, Leistung und zehnminütiger Dauerlauf folgen automatisch. Die alte Matrix `p1106-092856` wurde mit erhaltenem Zwischenstand kontrolliert beendet, da die gemergte Grundlage neuere UI-Korrekturen enthält. Kein verdeckter Neustart nach einem Produktfehler, keine Erfolgsübertragung von alten Bytes.

Die App-Prüfkopie trägt `389cf046…`; der zusätzliche Git-Blobhash steht im JSON, weil Git Textdateien gemäß `.gitattributes` auf LF normalisiert. Quelle und Python-Lieferung sind sowohl in der Arbeitskopie als auch im Git-Index bytegleich. Voll-/Gesamtabschluss, native Tk-9.1-Abnahme und eigenständige Paketlieferung des Nachtrags stehen noch aus. Der lokale Commit ist keine Veröffentlichung oder Menschenabnahme.
