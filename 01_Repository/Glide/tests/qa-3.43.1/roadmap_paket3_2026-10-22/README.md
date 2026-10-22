# Roadmap-Paket 3 – Strukturabschluss und Kalenderwechsel

22.10.2026 · lokaler Kandidat Glide 3.43.1 · Aufgabenformat 26 · keine Lieferung

Auftrag: „Weitermachen mit der Feature-Umsetzung“. Aufgabenstatus und Rest stehen in [Plan §21.9](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#219-drittes-umsetzungspaket-strukturabschluss-und-kalenderwechsel), Verhalten in [Funktionen](../../../docs/20_FUNKTIONEN.md). Dieser Ordner enthält Prüfbelege, keine zweite Roadmap.

## Quelle und Umfang

Ausgangs-App `fefde636c8b7a639adf4d86f7e8cac7567037a81b80b87d812f0d827bdc3a20e`; vor Produktionsänderungen Arbeitsbestand inventarisiert und betroffene Originale privat außerhalb des Projekts gesichert. Bestehender Speicherergebnisfall und Datenintegrität mit 130 Gruppenkombinationen grün. [Inventar](inventar_vorher.json).

Abschluss-App `604014f9a85e9c38a2d19141a3b1039a7a9f798c39d7dcbcb0387569b0f1f68f`. Produktionsdelta nur `app.pyw`, `calendar_service.py`, `save_result.py`; keine neue Laufzeitdatei oder Abhängigkeit. [Quell-/Test-/Ressourcenmanifest](quellmanifest.json). Alle Produktionsdateien blieben während der gebündelten Prüfung und Messung unverändert; nach dem Schutzlauf wurde ausschließlich ein ungültiger Farbwert im neuen Test korrigiert.

Sieben Caller: Gruppieren, Auflösen, Ordnerpapierkorb, Ordnerauflösen, Einzelfarbe, direkte Papierkorbwiederherstellung und -leerung. Vorhandene Rahmen, IDs, sofortiges Speichern und Undo/Redo bleiben. Ein Hauptdateifehler lässt eine offene rücknehmbare Änderung; kein Erfolgstoast und kein falsches True beim direkten Restore. Editorübernahme erfolgt vor dem Entfernen eines Ordners. Nach Dialog/Snapshot aktuelle Objekte lesen. `finish_change_ui` schützt nach erfolgreichem Schreiben den UI-Nachlauf, führt übrige Schritte weiter und ergänzt den unveränderlichen Speicherausgang; keine Hauptdateirücknahme wegen Anzeige-/Warnungsfehler. Der Guard berücksichtigt regulär verdrängte alte Papierkorb-Punkte bei 200 Einträgen.

Der Kalender prüft nach dem Reader nochmals Generation/Schließen. Überholte Leseaufträge expandieren nicht; weiterhin genau ein Worker. Bereits laufendes Lesen oder Expandieren wird dadurch nicht unterbrochen.

## Ausgeführte Prüfungen

Windows, Python 3.14 / Tk 9.0.4, künstliche temporäre `GLIDE_DATA_DIR` vor Appimport. Unabhängige Codegegenprüfung ohne GUI; keine neuen Bildschirmgeometrien oder Gestaltungskomponenten. Geänderte Rollen sind vorhandene Zustands-/Fehlermeldungen und Auswahl im Listen-/Seitenleisten-/Papierkorbkontext. Physische Bedien-, DPI-, Reader- und Mehrplattformabnahme bleibt offen.

| Prüfung | Tatsächlicher Abschluss |
|---|---|
| Fachlogik | [856/856 grün](fachlogik.json), darunter 19 Kalenderfälle und sechs Speicherergebnisfälle. Vorgeschriebener `PYTHONUTF8=1`-Modus; der Vorlauf ohne diesen Modus bleibt mit fünf Lesekodierungsfehlern separat erhalten |
| Schutzrunde | [Gebündelt 15/16 grün](schutzrunde.json); einzig roter Fall erwartete den ungültigen Farbwert `red`. Reine Testkorrektur auf echten Palettenschlüssel, anschließend [derselbe Fall grün](struktur_ergebnis_final.json). Zusammen alle 16 Fälle am unveränderten Produktionsstand abgedeckt; kein nachträglich umetikettierter Gesamtlauf |
| Datenintegrität | 130 Gruppieren-/Auflösen-Kombinationen und bestehende Wächter-/Zieh-/Listen-/Papierkorbwege grün; [Laufstatus](app_pruefungen.json) |
| Wiederholen | [Neun Aktionen bytegleich und drei Schritte in Folge](redo_matrix.json), [Schreibfehler](redo_schreibfehler.json) grün |
| App-Audit | Bestehender `audit_app.py`-Durchlauf ohne Befunde, einschließlich Ordnerhierarchie und Wiederherstellung |
| Neue Fehlergrenzen | Nicht übernommener Seitentext, frische Dialog-/Snapshotreferenzen, 20er-Undo, 200er-Papierkorb, Hauptdateifehler, Anzeige-/Warnungsfehler nach Commit, Undo/Redo und Neustart |
| Syntax | 174 Quell-/Unit-/betroffene Integrationsdateien im Speicher geparst, ohne Bytecodeausgabe |

**Rote Gegenproben:** [Erfolgsfeedback](gegenprobe_struktur_ergebnis.json), [Dialogreferenz](gegenprobe_struktur_dialog.json) und [Editorverlust](gegenprobe_struktur_editor.json) scheitern auf der unveränderten Ausgangs-App an den erwarteten Verhaltensfehlern. [UI-Nachlauf vor Korrektur](gegenprobe_ui_folgefehler.json) reproduziert den weitergereichten Ansichtsfehler nach erfolgreichem Schreiben. Vier neue Kalenderfälle waren vor der erneuten Gültigkeitsprüfung rot; [Kalenderzusammenfassung](kalender_pruefungen.json). Rohprotokolle bleiben als ausgeschlossene lokale `.log`-Dateien erhalten.

## Leistung und Grenzen

[Messskript](messung_mutationen.py), [Rohwerte und Profil](messung_mutationen.json): je Größe eigener temporärer Bestand/Tk-Interpreter, ein Erstaufruf und fünf warme Wiederholungen je Einzel-/100er-Aktion. Reales synchrones `toggle_done` einschließlich Snapshot, Sofortspeicherung und Refresh; nachlaufende Tk-Ereignisse sind nicht Teil der Zeitwerte. Quelle vor, während und nach der Messung hashgleich.

| Aufgaben | Einzelaktion Median | 100 ausgewählt Median |
|---:|---:|---:|
| 100 | 17,94 ms | 17,63 ms |
| 1.000 | 48,29 ms | 51,63 ms |
| 5.000 | 199,00 ms | 190,42 ms |
| 10.000 | 378,89 ms | 402,87 ms |

Getrenntes Profil mit Profilerlast bei 10.000/100: Gesamt 1.208 ms, Refresh 585 ms, Speicherabschluss 464 ms, darin Vergleich 253 ms und Verlauf 71 ms; Snapshot 17 ms mit zlib 2,5 ms. JSON-Kodierung 82 ms und atomare Schreibaufrufe einschließlich Einstellungen 38 ms. Inklusive Kategorien überlappen und dürfen nicht addiert werden. Desktopwerte, kein heutiger Vorher-/Nachhergewinn, p95- oder nativer End-to-End-Nachweis.

[Kalenderablauf](kalender_messung.py), [Ergebnis](kalender_messung.json): Ereignisbarrieren belegen eine eingesparte alte Expansion bei einem Quellwechsel. Die zusätzlich dargestellten Arbeitskosten sind ausdrücklich simuliert, keine gemessenen Millisekunden. Bereits gestartete Expansion bleibt seriell; ihr eigener Budget-/Abbruchvertrag ist offen.

## Abschlussgrenze

[Abschlussprüfung](ergebnis.json) hält Stand-/Link-/Datenschutz-/Diffprüfung, Quellenkontrolle und unveränderte Python-Lieferung fest. Alle 101 registrierten Integrationssuiten wurden hier nicht erneut vollständig ausgeführt. Kein Versionswechsel, Lieferabgleich, Build, Commit oder Push. `07_Python-Versionen` bleibt 3.43.1 / Format 25, eigenständige Pakete bleiben 3.42.0. Native Gesamtmatrix und menschliche Abnahmen folgen dem gesonderten D51-Phasenabschluss.
