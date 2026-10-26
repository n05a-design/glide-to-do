# Weiterentwicklung zu Glide 3.45.0

Auftrag und Umsetzung 25.–26.10.2026 · Aufgabenformat 26 · Einstellungen/Vorlagen 2.

D56 verlangt weitere Features und den Versionsfortschritt auf 3.45 vor dem nächsten Push. Umgesetzt sind Sicherungsübersicht mit Suche, Metadaten, lesender Inhaltszusammenfassung, direktem Vergleich und bestätigtem Wiederherstellungsweg, die Anhangsrückfrage WA-48 und robuste Windows-Bildpfade WA-51. D55-Arbeitsmodi, Rechtsklick-/Kompaktmoduskorrekturen, kurze Umschaltbefehle und Speicherstatus/Retry aus dem vorherigen Kandidaten sind gebündelt. Neue Fachlogik liegt Tk-frei in `backup_catalog.py` und `attachment_policy.py`. Keine neue Laufzeitabhängigkeit oder Datenformatstufe.

## Quellstand und Prüfbilanz

| Ebene | Nachweis und Grenze |
|---|---|
| Eingefrorene Basis | App `72e7fb6b8967ee211a00a5e46d21420898290e7d4cbb522ee60f687587925308`; 2.488 kopierte Dateien, 512 Quell-/Prüfdateien vor Start hashgleich zur Arbeitskopie. [Manifest](quellmanifest.json). |
| Gemeinsame Windows-Vollprüfung | Python 3.14.7 / Tk 9.0.4, 123 Schritte: **119 grün, drei rot, eine menschliche Sichtprüfung übersprungen**. Alle 104 Integrationssuiten ausgeführt, 101 grün. Dieser Lauf bleibt rot dokumentiert. [Originalergebnis](windows_voll/ergebnis.json). |
| Endgültige Quelle | App `2e69d8759d1c109c91bbed5662b10700368dc78a627545650c1046dc2c606dea`. Acht gegenüber der Basis geänderte Quell-/Prüfdateien; davon zwei Produktionsdateien. Zusätzlich atomarer Showcase-Lieferweg, fünf Pflege-/Paketwerkzeuge im Abschlussmanifest gehasht. [Abschlussmanifest mit Delta](quellmanifest_abschluss.json). |
| Gezielter Abschlussnachlauf | Die drei roten Suiten vollständig nachgeprüft, dazu Speicherstatus 4/4 und Schutzrunde 16/16; alle fünf Suiten grün. [Ergebnis](nachlauf_abschluss/ergebnis.json), [Speicherstatus](test_speicherstatus_abschluss.json), [Schutzrunde](test_schutzrunde_abschluss.json). |
| Neue Oberfläche | [7/7 Fälle grün](ui_abschluss.json): echter Menü-/Katalogweg, Filter/Leerzustand, beschädigte/externe Datei, Vergleich mit gleichen Dateinamen, bestätigter Restore-Abbruch, Anhangseditor und echte Vorgabe „Nein“, 24 Knopfprüfungen bei zwei Größen/zwei Schriften sowie fünfmaliger Dialogabbau ohne erhaltene Suchrückrufe. |
| CI-Grundstufe | **Strenger Abschluss Exitcode 0, alle 19 Schritte ausgeführt:** 172 Werkzeugtests (einer übersprungen), zweimal 911 Fachtests, fünf Analysen, Tk-/Startprobe, bytegleiche Python-Lieferung, 116 Vendor-Dateien, Datenschutz, Ablagegröße und Synchronisation grün. [Abschlusslauf](ci_abschluss/ergebnis.json). Der [frühere Kandidatenlauf](ci_kandidat/ergebnis.json) bleibt mit seinem damaligen Lieferhinweis erhalten. |

Die Vollprüfung wurde außerhalb OneDrive in einer separaten Kopie mit eigenem Git-Index ausgeführt; kein Commit erzeugt, ursprünglicher Index unverändert. Der erste CopyFile2-Versuch scheiterte an einem langen Grafikpfad; die fertige Bytekopie behandelt Daten und Metadaten mit erweitertem Windows-Pfadpräfix. Private Pfade und Rohprotokolle bleiben lokal. Ein gezielter grüner Nachlauf ist keine neue vollständige eingefrorene Matrix an der endgültigen App; die Zuordnung von Basis, Delta und Nachlauf bleibt ausdrücklich erhalten.

## Befunde und Korrekturen

| Befund | Korrektur und Prüfung |
|---|---|
| `test_bilder330` erwartete rohe Pfade im PowerShell-Skript | Der Test prüft die exakten aus UTF-8/Base64 dekodierten Daten. Die echte Windows-WIC-Wandlung mit Apostroph, typografischen Anführungszeichen, Dollarzeichen und Semikolon ist grün; die vollständige Bildsuite ebenfalls. |
| Speicherstatusknopf verwendete die Löschrolle | Der Aufbau von `storage_notice` verwendet die neutrale Rolle. Vollständige Rollenprüfung `test_befunde330` und Speicherstatus 4/4 grün. |
| `test_fundament333` patchte den ersetzten JSON-Leseweg | Der Test injiziert am tatsächlich verwendeten begrenzten Reader `schema_backups.read_stream`; sein Schutz vor zusätzlichem Parsen bleibt erhalten. Ganze Suite grün. |
| Inhaltszusammenfassung zeigte den falschen Format-Schlüssel | `backup_catalog.describe` verwendet das kanonische `version`; Testfixtures übernehmen `app.data_payload`. Acht Katalogtests und echte Inhaltsprüfung grün. |
| Geschlossene Sicherungsdialoge behielten fünf Suchrückrufe | [Echte rote Gegenprobe](lebensdauer_gegenprobe.json); Such-Trace beim Dialogabbau entfernen. Ein erster Cleanup an einer gleichnamigen, falschen Codestelle war unwirksam ([roter Nachlauf](ui_abschluss_vorlauf.json)); dort zurückgenommen und in `show_backup_catalog` angebracht. Anschließend 7/7 grün, einschließlich Lebensdauerfall. |

Der [erste UI-Prüfvorlauf](ui_vorlauf.json) enthält drei falsche Testzugriffe (Registry-Attribut und Ellipsen in Knopftexten), die berichtigt wurden. Der [Zwischenstand](ui_zwischenstand.json) ist 6/6 grün; seine Fach-/Konverterprüfung umfasst acht Katalog-, fünf Typ-/Herkunfts- und 16 Bildkonverter-/Workerfälle, zusammen 29. Spätere Ergebnisse überschreiben die roten Nachweise nicht.

## GitHub-D55-Fehler #156

Der Inhaber hat den Windows-Fehler aus [Lauf #156](https://github.com/n05a-design/glide-to-do/actions/runs/40224330702) eingereicht: einzig rot war `test_schutzrunde`, `struktur_ergebnis`, Zeile 900. Die übrigen 102 damaligen Suiten waren grün. [Snapshot](github_d55_snapshot.json): derselbe D55-Dateiinhalt war in #155 grün; #156 lief auf Merge `291c393`, CodeQL #55 war grün.

Die [deterministische Gegenprobe](github_156_gegenprobe.json) erzwingt die Erneuerung der Datensperre: Die pauschale Schreibfehlerinjektion trifft bereits `LOCK_FILE`, Gruppieren bricht korrekt vor der Änderung ab, `dirty` bleibt falsch und die alte Assertion schlägt fehl. Der bisher schon korrigierte Restore-Teil derselben Funktion zeigt die beabsichtigte Begrenzung; sie fehlte im Gruppier-Teil.

Der Test sperrt nun ausschließlich `SAVE_FILE`, lässt die echte Sperrerneuerung durch, erzwingt sie unabhängig von der Sekunde und verlangt den Nachweis beider Schreibwege. Dasselbe ist für Restore abgesichert. Die vollständige Schutzrunde besteht 16/16; Produktions-Lock und Mutationsschutz sind unverändert. Kein neuer Remote-Lauf auf dem lokalen 3.45.0-Stand, kein Commit/Push/Merge in dieser Runde.

## Lieferung, Dokumente und Aufbewahrung

Die Python-Lieferung ist 3.45.0: **85 Code-Dateien und 147 Ressourcen-/Vendor-Dateien bytegleich**, App-SHA wie die endgültige Quelle; die vorherige Hauptdatei 3.44.0 liegt im Archiv. [Hashmanifest](lieferung.json). Die [isolierte Lieferprobe](lieferprobe.json) ist grün. Der erste Showcase-Abgleich bestand den echten Import/Neustart, scheiterte dann beim direkten Überschreiben mit Windows `WinError 1224` ([roter Lieferlauf](lieferabschluss/ergebnis.json)). Der Pflegeweg ersetzt Lieferdateien jetzt atomar; zwei Fehlerproben erhalten den Altbestand. Der [echte Showcase-Nachlauf](lieferabschluss_nachlauf/ergebnis.json) ist grün, sechs Lieferdateien sind hashgleich. Die Werkzeugprüfung umfasst nun 172 statt 170 Fälle.

Der Versionswechsel erzeugt aktuelle Fixtures, Vorlagen, Rundgang, Showcase und Planungsdaten. Nach der Sieben-Versionen-Regel entfallen 19 alte Dateien; das [Aufbewahrungsmanifest](aufbewahrung_versionswechsel.json) belegt ihre Wiederherstellbarkeit aus Git. Keine einzigartigen Nutzerdaten entfernt, kein Git-Index geändert. Der erste Versionswechsel brach vor Ersetzen der App mit `OSError 22` ab; die App blieb vollständig erhalten. Der Pflegeweg schreibt nun atomar über eine Nachbardatei mit LF; gezielte Werkzeugtests prüfen Ersetzungsfehler, Vorschau und Kürzung ohne Git-Indexzugriff. Der folgende Versionswechsel war erfolgreich.

Übergabe, Plan, Analyse, Funktionen, Architektur, Gestaltungsvertrag, Änderungsliste, READMEs, Entscheidungen und explizite Liefer-/Paketmodullisten sind am selben Stand geführt. 52 geänderte/neue Markdown-Dateien mit 912 lokalen Datei-/Abschnittsverweisen waren ohne Befund ([Verweisprüfung](dokumentverweise_abschluss.json)); neue öffentliche Nachweise enthalten keine Benutzerpfade. Historische Referenzen wurden gezielt geprüft; feste alte Formatfixtures bleiben unverändert. Kein konkurrierender Plan und keine erneute Marktanalyse.

Die eigene temporäre Prüfkopie außerhalb des Projekts umfasst 497.350.175 Byte (rund 474 MiB). Ihr Löschen wurde **vor Ausführung automatisch mit „blocked by policy“ abgelehnt**; keine Einsparung behauptet, kein Ausweichverfahren benutzt. [Status](pruefkopie_bereinigung.json). Private Lage nur in der ignorierten `freeze_ort.log`. Andere Arbeitskopien, Caches und die ursprüngliche `.git/index.lock` blieben unangetastet.

## Offene Abnahmen

Native Mac-/Reader-/DPI-/Mehrmonitor- und menschliche Bedienabnahmen bleiben offen. D55-Punkte 1–4 sind bestätigt; Punkt 5 braucht die menschliche Gegenprobe des korrigierten Kürzels und neuen ersten Menüeintrags. Neue Sicherungs-/Anhangswege sind automatisch geprüft, nicht menschlich abgenommen. Eigenständige Pakete und Mac-Bundle bleiben 3.42.0. Die automatische Windows-Prüfung ersetzt diese Tore nicht; es gibt keine öffentliche Releasefreigabe.
