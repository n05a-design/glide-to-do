# Bestandsaufnahme und Dokumentabgleich – 21.10.2026

Dokumentationsnachlauf zu Glide 3.43.1 / Aufgabenformat 26. Ergebnisse stehen in der bestehenden [Analyse §13.7](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#137-konsolidierte-bestandsaufnahme-und-dokumentabgleich), im [Entwicklungsplan §21](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#21-roadmap-abgleich-vom-21102026), der [Übergabe](../../../../../00_Arbeitsvorbereitung/Glide_Uebergabe.md) und im [QA-Bericht](../../../docs/07_QA_BERICHT.md). Dieser Ordner trägt ausschließlich Prüfprovenienz.

## Ausgang und Umfang

Vor Änderungen wurden 1.533 nicht ignorierte Projektdateien mit relativen Pfaden, Größe und SHA-256 aufgenommen. Ausgang: Zweig `codex/bildvorschauen-wa26-2026-10-18`, HEAD `10427276b97e10528759cc42b0d23f757ca14843`, 70 geänderte versionierte Dateien und 32 unversionierte Statuseinträge, teils Ordner; leerer Index. Die damaligen Dokumentbytes und Git-Diffs sind privat außerhalb der Projektwurzel gesichert. Das [Ausgangsmanifest](ausgangsmanifest.json) enthält keine absoluten Benutzerpfade. Ignorierte Builds, `.git`-Innendaten und lokale Originalbilder sind nicht Teil dieser 1.533 Dateien; dies ist keine Wiederholung der globalen Ablageinventur vom 18.10.

GitHub-`main` wurde über die verbundene GitHub-Schnittstelle lesend abgefragt und stand auf demselben Commit wie HEAD. Kein Fetch/Merge, Commit, Push, Versionswechsel, Build oder Lieferabgleich. Der beendete einmalige Git-Auftrag bleibt ein eigener historischer Nachweis.

## Beleggrenzen

- Aktueller App-SHA-256 `3b93a24a8584821d77f8ff0f74b0c681e1555dea4fe9953a7b54edf3d9fd65ac`; alle 78 direkten Pythondateien sind hashgleich zum FP-02-Quellmanifest, darunter 77 Laufzeitdateien und ein isolierter Prototyp. 101 registrierte Integrationssuiten sind eine Inventarzahl.
- Die 73 passenden Fachtests und zwölf Appfälle stammen aus dem gelesenen FP-02-Paketabschluss. Die 99-Suiten-Vollprüfung und die ältere grüne FP-03-CI behalten ihre eigenen Quellhashes. Breite Analyse und roter Git-Auftrag werden nicht rückwirkend umgedeutet.
- Die Python-Lieferung trägt dieselbe App-Version, aber Format 25 und App-SHA `ed2b7eb64cc3fc14f00a4e909c7693c34102e46e393b5937158bb7d7e25176d3`: frisch ermittelt 18 Laufzeitabweichungen plus fehlendes `resources/exchange_recipes.json`.
- Paketmetadaten nennen weiterhin 3.42.0. Die drei dokumentierten Mac-Frameworkfehlstellen wurden erneut auf Existenz geprüft. Historische vollständige Pakethashes sind kein aktueller Start-/Signaturtest.

## Tatsächliche Nachprüfung

Die neue CI-Grundstufe ist mit Exitcode 0 bestanden: 19 Schritte, 18 ausgeführt und ein erwarteter Lieferhinweis. 831 Fachlogiktests bestanden mit und nochmals ohne Systemzeitzonen, 152 Werkzeugtests sowie fünf Analysen und die Tk-Startprobe sind grün. Der Lauf nutzte Python 3.14.7 unter Windows und künstliche Daten. [CI-Ergebnis](ci_ergebnis.json); Rohlogs bleiben privat außerhalb des Projekts. Die Dokumente wurden anschließend um das Ergebnis ergänzt und separat erneut auf Stand, Verweise und Datenschutz geprüft.

Ergebnis, Dokumentänderungen und Abschlussvergleich stehen in [ergebnis.json](ergebnis.json), die direkt erhobenen Versions-/Lieferangaben in [stand.json](stand.json), der lesende Remoteabruf in [remote.json](remote.json). Keine neue 101-Suiten-Vollmatrix, native Plattformprüfung, Menschenabnahme oder Releasefreigabe. Historische Nachweise und Originalreferenzen bleiben unverändert.
