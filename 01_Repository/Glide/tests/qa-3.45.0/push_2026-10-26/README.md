# Push des vorhandenen Glide-3.45.0-Kandidaten

Auftrag 26.10.2026: „pushen“. Zielzweig `codex/glide-3.45.0`, Basis `origin/main` `291c393c4027f96864772031e9fbeaf0e858afdc`. Der ursprüngliche lokale Zweig `claude/phasenabschluss-3.44.0` bleibt bei `71854ec`. Der Kandidat enthält Sicherungsübersicht/Anhänge, Speicherstatus, D55-Korrekturen, WA-12 und Verweisvorschau.

## Abgleich und Uploadumfang

[Ausgangslage](ausgangslage.json) hält den ursprünglichen Git-Stand, die kuratierten Pfade und lokale Ausnahmen fest. Keine unerwartet fehlenden Remote-Dateien; nur dokumentierte Aufbewahrungsabgänge. Die leere `.git/index.lock` vom 23.10. war nicht exklusiv geöffnet; kein schreibender Git-Prozess lief. Sie wurde vor dem Staging nach `.git/index.lock.stale-20261026-push` verschoben, nicht gelöscht. Andere lokale Zweige, Stashes und Arbeitskopien bleiben erhalten.

Lokale Rohprotokolle, sechs neue Vollprüfbilder und `tk910-src.zip` bleiben außerhalb des Commitumfangs. Neue öffentliche Nachweise enthalten relative Projektpfade. Die Glide-Prüfung läuft zusätzlich bei Push auf `codex/**`; bisher wurden nur `main` und `claude/**` berücksichtigt.

## Prüfung

Frische [CI-Grundstufe](ci_grundstufe/ergebnis.json) vor dem konkreten Commit unter Windows/Python 3.14.7, mit temporärem `GLIDE_DATA_DIR` und ohne strengen Lieferabgleich: Exitcode 0, 19 Schritte, davon 18 ausgeführt und ein erwarteter Lieferhinweis. 172 Werkzeugtests (einer übersprungen), zweimal 920 Fachtests, fünf Analysen, Tk-/Startprobe, 116 Vendor-Dateien, Datenschutz, Aufbewahrung und Synchronisationsprüfung grün. Alle fünf Featurehashes entsprechen dem vorherigen gezielt grünen Stand; die 56 geänderten Code-/Workflowpfade entsprechen dem Index ([SHA-256](gepruefte_codepfade.json)). Kein Schlüsselmuster im ausgehenden Textbestand gefunden; Diff-Prüfung grün. Die vorhandenen gezielten Fach-/Bediennachweise gelten weiter: [WA-12](../freigaben_2026-10-26/README.md), [Verweisvorschau](../verweisvorschau_2026-10-26/README.md), [Lieferabschluss davor](../weiterentwicklung_2026-10-25/README.md).

## Grenzen

Quellkandidat 3.45.0 / Aufgabenformat 26. Die Python-Lieferung bleibt beim Abschluss `2e69d875…`; drei Laufzeitunterschiede (`app.pyw`, `day_proposal.py`, `side_view.py`) sind als Kandidatenhinweis zulässig. Eigenständige Pakete/Mac-Bundle weiter 3.42.0. Kein neuer Voll-/Lieferabschluss oder Zusammenführen nach `main` aus diesem Auftrag.

Der Inhaber bestätigt aktive automatische Fensterverwaltung. Dies ist ein möglicher zusätzlicher Einfluss auf die offenen nativen Fokus-/Inspektor-/Tastaturfälle; keine pauschale Ursachenzuordnung. Historische rote Prüfungen bleiben rot dokumentiert. D55-Menschenabnahme Punkt 5, Reader, DPI/Mehrmonitor und Mac bleiben eigene offene Tore. Fensterverwaltung und fremde Prozesse wurden nicht verändert.
