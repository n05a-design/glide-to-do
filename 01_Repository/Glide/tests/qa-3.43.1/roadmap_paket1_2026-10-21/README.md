# Erstes Roadmap-Paket – 21.10.2026

Lokaler Umsetzungskandidat Glide 3.43.1 / Aufgabenformat 26. Auftrag: mit der Roadmap beginnen, zusammenhängende Funktionen bündeln und Prüfarbeit angemessen halten. Status und Rest in [Plan §21.7](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#217-erstes-umsetzungspaket-schreibbesitz-mehrfachaktionen-und-ki-vorschau), Verhalten in [Funktionen](../../../docs/20_FUNKTIONEN.md), Einordnung in [Analyse §13.9](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#139-erste-roadmap-umsetzung-und-wirkungsbeleg). Dieser Ordner enthält Nachweise, keine zweite Roadmap.

## Quelle und Umfang

Vorher-App `3b93a24a8584821d77f8ff0f74b0c681e1555dea4fe9953a7b54edf3d9fd65ac`; Arbeitsbestand und relevante Dateien vor Änderungen privat außerhalb des Projekts gesichert. Die unmittelbar vorherige Dokumentationsgrundstufe und die erneut ausgeführten zwölf Lock-Fachtests plus ein Sperr-Appfall waren grün. Die Vorherquelle für die Messung ist diese gesicherte Arbeitsfassung, kein mit Versionsstring gleichgesetztes Git-/Lieferartefakt.

Breite Paketprüfung an App `559c738d54d5e5323186715601f43498d2207b860893b2de207a5775aa872698`: [damals eingefrorenes Quell-/Test-/Ressourcenmanifest](quellmanifest_zwischenstand.json), während des Laufs unverändert. Abschluss-App `45354b6350f09638b80fd5e5a9740f15c337c3c128a74a097d9a5e8949454519`: [Abschlussmanifest](quellmanifest.json) nach gezielter Freigabe-/Ordnerkorrektur. [Delta](abschluss_delta.json) belegt, dass nur drei Sperr-/Ordnerfunktionen und der zugehörige Appfall geändert wurden; alle übrigen Fachmodule/Werkzeuge blieben unverändert. 79 eigene Laufzeitdateien plus getrennter Prototyp; 101 registrierte Integrationssuiten bleiben unverändert, vorhandene Suiten wurden erweitert. Neue Module `item_index.py` und `save_result.py` sind in den vorhandenen Liefer-/Bundlelisten registriert; Lieferwerkzeuge wurden nicht schreibend ausgeführt.

Umgesetzt: lokaler OS-Schutz über die Schreibsitzung und strikte Erneuerung (WA-31); kurzlebige Mehrfachauflösung in Auswahl, Erledigen, Zählung, Serien und Checklisten (WA-36); explizites Speicher-/Mutationsresultat mit Bool-Fassade und nachgelagerten Settings (WA-38/37); kritische False-/Folgefehlergrenzen (WA-40); vollständig lesende FP-06-Auftrags-/Kontextvorschau. Kein Datenformatwechsel, keine neue Laufzeitabhängigkeit, kein verzögertes Speichern und kein dauerhafter Globalcache.

## Gebündelte Prüfung

Windows, Python 3.14.7 / Tk 9.0.4, künstliche temporäre Datenordner vor App-Import. Ein gesammelter Lauf am stabilen Zwischenstand `559c738d…`, keine CI-/Vollmatrix nach jedem Teilschritt. [Zusammenfassung](pruefungen.json); anschließende gezielte Appnachläufe unten.

| Bereich | Tatsächliches Ergebnis |
|---|---|
| Tk-freie Fachlogik | 843/843 grün; darunter 1.000 OS-Sperrübergaben zwischen zwei echten Prozessen und Wiedererwerb nach Prozessabbruch. Dies ist Backend-Stress, kein 1.000-facher vollständiger Appstart |
| Werkzeugtests | 152/152 grün |
| Schutz-/Mutations-Appwege | [13/13 grün](schutzrunde.json): bisherige Guards/Load/Flush/Byte-Rückweg, neue Sitzung/Erneuerungsfehler/alte Tokens, Hauptdatei-/Backup-/UI-/Meldungs-/Settingsausgang, No-op, Mehrfachauswahl, ein Undo/Redo und frische Originale nach Bestätigung |
| KI-Aufträge | [6/6 grün](auftraege.json): vorhandene Datei-/Clipboard-/Vorlagen-/Importerwege und vollständige lesende Vorschau für Create/Patch, ohne Dateiziel oder Clipboardänderung. Windows-Aufnahme gesichtet; Rohbild bleibt privat |
| Serien | [Vorrücken](serien_vorruecken.json) und [Schreibfehler](serien_schreibfehler.json) grün |
| Wiederholen nach Rückgängig | [Schreibfehler](redo_schreibfehler.json) und [echte Bedienwege](redo_bedienwege.json) grün |

Insgesamt 23 passende Appfälle. Der neue Vorschaufall prüft lange ungekürzte Anweisungen, Scope, lesenden Zustand, vollständiges Scrollen und erreichbaren Schließenknopf. Geprüfte UI-Rollen: Kontextkopf, Feld/Vorschau und fester Aktionsfuß im bestehenden Dialog, keine neue Hauptnavigation. Physische Tastatur-/Reader-/DPI-/Mac-/Linux-Menschenabnahme bleibt getrennt offen.

**Erwartet rote Gegenproben am gesicherten Vorherstand `3b93a24a…`:** [Sitzung](gegenprobe_sitzung.json) scheitert daran, dass der lebende Besitzer nach Zeitablauf verdrängt wird; [Mehrfachaktion](gegenprobe_mehrfach.json) an 2.705 einzelnen Suchstarts statt weniger als 50. Beide Fehler sind fachlich erwartete Altstandbefunde, keine fehlenden neuen API-Namen. Der Kandidat besteht dieselben Fälle (Mehrfachweg: vier Suchstarts). Diese roten Ergebnisse bleiben separat und werden nicht als Fehler des grünen Paketlaufs umetikettiert.

**Gezielter Abschluss am Kandidaten `45354b63…`:** Eine zusätzliche [Gegenprobe am Zwischenstand](gegenprobe_freigabe_vor_abschluss.json) zeigte noch Schreiben nach Freigabe mit leerem Token. Der Abschluss merkt echte erworbene Sitzungen und erlaubt dann bis zum Neuerwerb kein Schreiben; reine Prüf-/Vorschauadapter ohne Erwerb bleiben kompatibel. Eine [Ordnerwechselprobe am Nachlauf](gegenprobe_ordnerwechsel_vor_abschluss.json) traf unter Windows auf die gehaltene Bytebereichssperre beim Kopieren von `glide.lock.acquire`; beide lokalen Sperrdateien werden nun nicht mitkopiert. [Abschließende Sitzung einschließlich Kopieren/Hin-/Rückwechsel](abschluss_sitzung.json), [Speicherergebnis](abschluss_speicherergebnis.json), [Mehrfachweg](abschluss_mehrfach.json) und [separate Ordnerprobe](abschluss_ordnerwechsel.json) sind grün. Der kleine Delta ist separat belegt; unveränderte Fach-/Werkzeugtests und übrige breite Appbelege wurden nicht erneut als kompletter Lauf ausgegeben. Die frühere [Zwischenabschlussprüfung](ergebnis_zwischenstand.json) bleibt datiert erhalten.

## Frische Leistungsprobe

[Vorherwerte](leistung_vorher.json), [Paketzwischenstand `559c738d…` und Profil](leistung_nachher.json), [ausführbare Messprobe](messung.py). Je Stand ein eigener Python-Prozess, je Größe ein neuer Interpreter/temporärer Bestand, je Aktion ein erster Aufruf plus fünf warme Wiederholungen. Reale Auswahl/`toggle_done`, Snapshot, Sofortspeicherung und synchroner Refresh; nachlaufende Tk-Ereignisse sind nicht Teil des Zeitwerts. Der abschließende Delta verändert diese Pfade einer erworbenen Sitzung nicht und wird nicht als neue Messausführung ausgegeben. Desktoplast, keine allgemeine Referenzgerätezusage. Prozentwerte werden nicht als Plattformabnahme interpretiert.

| Gesamtaufgaben / Auswahl | Vorher Median | Paket Median |
|---|---:|---:|
| 100 / eine Aufgabe | 26,5 ms | 31,4 ms |
| 100 / 100 Aufgaben | 49,6 ms | 28,0 ms |
| 1.000 / eine Aufgabe | 90,3 ms | 99,4 ms |
| 1.000 / 100 Aufgaben | 295,0 ms | 92,4 ms |
| 10.000 / eine Aufgabe | 722,3 ms | 746,2 ms |
| 10.000 / 100 Aufgaben | 3.105,3 ms | 791,2 ms |

Der Gewinn betrifft Mehrfachaktionen; Einzelaktionen sind in dieser Messung nicht allgemein schneller. Das separate Profil erklärt Restkosten und ist selbst kein Gewinnbeleg. Ein früherer Altstand-Vorlauf mit Tk-Ereignisnachlauf überschritt das 45-Sekunden-Budget in `get_selected_item_ids` über Auswahl-/Fußzeilencallbacks; er wurde abgebrochen und liefert keinen vollständigen Ende-zu-Ende-Wert. Ein weiterer Paketvorlauf lief durch, wird aber nicht mit dem fehlenden Altstand-Endwert verglichen. Der finale synchrone Vergleich oben verwendet dieselbe Messmethode auf beiden Seiten.

## Abschlussgrenze

[Ergebnis](ergebnis.json) enthält Syntax-/Versions-/Dokument-/Link-/Datenschutzprüfung, die abschließende Unverändertheitskontrolle sowie den getrennten Lieferstand. Alle Logs und ursprünglichen Zwischenfehler bleiben privat; die publizierbaren Ergebnisse enthalten keine Benutzerpfade. Frühere rote Vorläufe werden nicht rückwirkend umetikettiert.

Keine neue komplette CI-/101-Suiten-/Native-Matrix, kein Versionswechsel, Lieferabgleich, Build, Commit oder Push. Die Python-Lieferung bleibt 3.43.1 / Format 25, unverändert und mit nun 22 Unterschieden zur Quelle; eigenständige Pakete bleiben 3.42.0. Größere WA-39-/WA-32-Auslagerungen, weitere direkte Caller, allgemeine Fehlerklassifikation und weitere Render-/Snapshotoptimierungen sind durch den ersten Schnitt nicht erledigt. Lokaler OS-Lock ist kein verteilter Cloud-Lock; Altclients ohne Erwerbsprotokoll sind keine vollständig abgefangenen Writer.
