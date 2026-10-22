# FP-03 Stufe 2 – gespeicherte Darstellung

21.10.2026 · lokaler Quellkandidat 3.43.1 · Aufgabenformat 26 · Einstellungen 2 · keine Lieferung

Quelle `src/glide/app.pyw`: `fefde636c8b7a639adf4d86f7e8cac7567037a81b80b87d812f0d827bdc3a20e`. Das Ausgangsmanifest gehört zum vorherigen Roadmap-Paket 1; dessen Belege werden nicht überschrieben. Neue Fachlogik bleibt im bereits bestehenden Tk-freien `view_definition.py`.

## Umgesetzt

Je gespeicherter Ansicht Liste, Tabelle oder Spaltenboard, Gruppierung, Sortierfeld/Richtung, Tabellenspalten samt Herkunftsliste und Breiten. „Als Ansicht speichern …“ übernimmt aus Liste/Tabelle/Spaltenboard die aktuellen Such-/Offen-/Bereichsregeln oder kopiert eine Ansicht mit neuer ID. Dieselben Originalaufgaben, keine freien Kartenkopien. Gruppenwechsel durch Ziehen bzw. Alt+Links/Rechts nutzt den bisherigen Mutations-/Sofortspeicher-/Undo-Weg.

`saved_view_layouts_v1` liegt getrennt auf oberster Einstellungsebene. Alte Leser erhalten ihn; Neustart und App-Sicherung stellen ihn wieder her. Unbekannte Felder erhalten, ungültige Darstellung sichtbar melden und als Liste öffnen; Ersetzen bewusst bestätigen. Ohne neue Darstellungsdefinition bleibt die historische Filterreihenfolge erhalten. Die bisherige Kartengrenze des Spaltenboards bleibt.

## Gezielte Prüfungen

- 847 Fachlogiktests grün, davon 13 für Ansichtsbedingungen/Darstellung. Prüflog und Hash des unveränderten Fachmoduls werden mitgeführt.
- 15 echte Ansichtenfälle: bisherige Bedingungen/Erklärung, Alle/Oder, Persistenz, Fehler, tatsächlich ausgelieferter Altleser, 30 alte Filterkombinationen, Dialog normal/groß, 10.000-Punkte-Auswertung sowie sechs neue Darstellungsfälle. Die separate Nachprüfung des vollständigen Pakets steht in `ansichten_final.json`.
- Der UI-Fall startet in einem eigenen frischen Prozess, damit alte Tk-Stile/Schriften nach Test-Neustarts nicht als App-Zustand erscheinen. Vier konkrete UI-Konfigurationen: 860×700/groß/hell/Hinweise aus; 1280×800/mittel/dunkel/Hinweise an; 860×700/mittel/Glas dunkel mit Verlauf/Hinweise an; 1280×800/groß/Glas hell mit Verlauf/Hinweise aus. Je Liste/Tabelle/Spaltenboard und Dialog: 16 Aufnahmen. Automatische Geometrie-/Funktionsprüfung aller Varianten; die im Ergebnis bezeichneten repräsentativen Aufnahmen wurden zusätzlich angesehen. Keine vollständige Kreuzmatrix und keine physische DPI-/Reader-/Mehrplattformabnahme.
- Die bestehende `test_oberflaeche33321.py` besteht ihre Funktionsprüfungen (Exitcode 0) am Stand vor der letzten neuen Hostbindung. Nach dem Fensterabbau meldet ihr älterer Testaufbau ungültige nachlaufende Callbacknamen; deshalb kein sauberer nativer Gesamtnachweis. Die letzte Einzeilenänderung betrifft nur das neue Gruppierungsfeld des gespeicherten Spaltenboards.

Der kombinierte Vorlauf machte die Bindung eines neuen Auswahlfelds an den voreingestellten statt den tatsächlichen Tk-Host sichtbar: nach mehreren Interpreterwechseln wurde die Gruppierung leer angezeigt. `gegenprobe_ui_host.json` hält die rote UI-Probe fest; der abschließende vollständige Ansichtenlauf prüft den expliziten Host und alle anderen Einstiegspfade. Sichtproben fanden außerdem den doppelten alten Umschalter und anfangs leere Listenspalten. Der gespeicherte Kontext nutzt nun einen Umschalter und blendet leere Gruppen zunächst aus.

## Zusatz-Audit und Grenzen

Der nachgereichte „Technische Deep-Research-Audit“ bestätigt die technische Richtung, hat aber keinen Zugriff auf den lokalen Entwicklungsstand und liefert im übergebenen Text keinen vollständigen Detailbericht. Seine historischen Lock-/Strukturangaben ersetzen die aktuellen lokalen Belege nicht. Die mögliche Wartezeit durch einen laufenden alten Kalenderauftrag ist statisch plausibel und in Plan §21.8 als begrenzter WA-36-Prüfpunkt eingetragen; hier keine Wartezeitmessung und kein Kalenderdatenfehler belegt. 5.000 Aufgaben ergänzen die nächste einschlägige Ende-zu-Ende-Leistungsmessung.

Kein neuer Versionswechsel, kein Commit/Push, kein 101-Suiten-/CI-Gesamtlauf und keine Synchronisation nach 07 bzw. Neubau der Pakete. Die Lieferung bleibt auf ihrem bisherigen Stand. Gemeinsamer Phasenabschluss nach D51 gesondert.
