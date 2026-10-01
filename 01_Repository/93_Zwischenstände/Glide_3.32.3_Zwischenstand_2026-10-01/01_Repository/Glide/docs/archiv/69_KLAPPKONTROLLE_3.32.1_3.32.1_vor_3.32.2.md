# Klappkontrolle – Glide 3.32.1

Stand 30.09.2026 · Glide 3.32.1 · Aufgabenformat 20

Auftrag D08: Labelgruppen lassen sich nicht schließen; alle Klappmechanismen
kontrollieren und bessere Kontrollmechanismen schaffen. D01–D06 sind in der
[Arbeitsplanung](../../../00_Arbeitsvorbereitung/Glide_Arbeits_und_Featureplanung_2026-09-30.md)
verbindlich übernommen. D07 bleibt nach Erklärung offen.

## Fehler und Korrekturen

1. `on_label_view_drag_start` fing auch Pfeilklicks ab und gab `break` zurück,
   ohne die Gruppe zu klappen. `refresh_label_overview` öffnete außerdem jede
   Gruppe grundsätzlich. Die neue Bedienprobe scheiterte im Ausgangsstand
   an „Labels: Pfeilklick muss schließen“, obwohl `test_features325` grün war.
   Jetzt bedient die Drag-Klickroute dieselbe Klapplogik wie Liste/Tabelle.
2. Tk meldet `TreeviewOpen` vor dem Umschalten. Bisher wurde der alte Zustand
   gespeichert. Lesen erfolgt jetzt gebündelt im Leerlauf; programmgesteuerte
   globale Klappaktionen merken ihren Zustand ebenfalls.
3. `Treeview.see` öffnet Vorfahren. Bei einer Wiederherstellung der Auswahl
   wird jetzt über alle Vorfahren geprüft, ob der Weg bereits geöffnet ist.
   Explizite Sprünge zu einer Aufgabe dürfen weiterhin deren Weg öffnen.
4. Die Bedienprobe verschachtelter Seitenordner fand einen Callbackfehler:
   `refresh_folder_overview` und `refresh_library_table` fügten denselben
   Unterordner ein. Die Bibliotheksroute zweigt jetzt vor der normalen
   Ordnerdarstellung ab.
5. Bereichspfeile Seiten/Listen/Notizen und Angeheftet waren nicht per Tab
   erreichbar. Sie erhalten Fokus und Enter-/Leertastenbindungen. Seiten-
   und Listenpfeile zeigen den bestehenden Hoverzustand auch bei Fokus.

Die neue Einstellung `label_sections_closed` speichert nur Zeilenkennungen,
normalisiert Typ, Präfix, Dubletten und Länge. Sie verändert keine Aufgaben,
keinen Aufgaben-Undo und keinen Datenformatvertrag. Fehlende Einstellung
bedeutet wie bisher zunächst geöffnet. Individuelle Ordner- und Punktzustände
bleiben wie bisher sitzungslokal; Bereichs- und Abschnittszustände werden in
Einstellungen gespeichert. Keine Änderung der Hinweisgestaltung.

## Kontrollmatrix

| Mechanismus | Prüfung und Ergebnis im gezielten Lauf |
|---|---|
| Labelgruppen und Ohne Label | Echter Pfeilklick; native Links/Rechts-Class-Bindung; Neuaufbau mit ausgewähltem Kind; Wechsel zur Startseite und zurück; Filter ohne Treffer; globales Klappen; erneut geladene Einstellungen |
| In Bearbeitung / Mein Tag | Alle im Testbestand gerenderten Abschnittsköpfe, einschließlich Zeitplan, ohne Uhrzeit, Eingang, überfälliger und nächster Aufgaben; Pfeil, Links/Rechts, Neuaufbau und globale Aktionen |
| Listen / Tabellen | Unterpunkte, Aufgaben-Gruppen, generierte Gruppierungsfächer, verschachtelte Tabelle, ausgewähltes Kind, globale Aktionen; Aufgaben und Undo unverändert |
| Seitenleiste | Alle drei Bäume mit je verschachtelten Ordnern; Pfeilklick, native Links/Rechts-Bindung und Neuaufbau; Bereiche per Klick und registrierter Enter-/Leertastenbindung |
| Angeheftet / Ansichten | Kopf schließen und neu aufbauen; Angeheftet per registrierter Tastaturbindung öffnen; Ansichten über vorhandene Kopfbindung öffnen |
| Pinnwandspalten | Echter Canvas-Klick auf Spaltenkopf; schließen/öffnen; neu zeichnen; keine Karten-/Aufgabenänderung |
| Seiten-/Notizblöcke | Echter Text-Pfeilklick; Kind und Enkel verborgen, Folgekapitel sichtbar; gespeicherte Tags erneut laden; wieder öffnen |
| Labelauswahl / Einfachauswahl | Aufklappfelder öffnen/schließen, bestehende Auswahl bleibt erhalten |
| Vorlagen-Strukturbaum | Quellkontrolle: native Treeview ohne abfangende Drag-Klickbindung; `refresh_editor_tree` erfasst und restauriert bestehende Zustände. Bestehende Vorlagensuite bleibt Pflichtbestandteil |

Tastaturproben rufen die tatsächlich registrierte Tcl-Class-/Widget-Bindung
auf. Sie brauchen im Hintergrund keinen OS-Tastaturfokus. Physische Tabwege,
Trackpad/Doppelklick, VoiceOver, Windows/Linux bleiben Teil der manuellen
Plattformabnahme. Die automatisierte Probe ist kein Sichtprüfungsnachweis.

## Verbindliche Kontrollmechanismen

- `test_klappmechanismen3321.py` ist Bestandteil von `pruefen.py`, Schnell-
  und Vollmodus. Ein fehlender sichtbarer Pfeil oder eine fehlende geprüfte
  Tastaturbindung schlägt fehl; reine Settertests genügen nicht.
- Tk-Callbackfehler werden gesammelt, mit Stacktrace ausgegeben und führen
  zum Fehlschlag. Der verschachtelte Bibliotheksfehler ist damit dauerhaft
  Teil der Regression.
- Neue Klappflächen müssen in dieser Matrix und der Pflichtsuite ergänzt
  werden: schließen/öffnen, Neuaufbau, Auswahl in geschlossenem Kindpfad,
  gespeicherter Zustand nach dem geltenden Vertrag, keine Daten-/Undo-Wirkung.
- Bei Drag-Bindungen mit `break` immer prüfen, welche native Treeview-/Text-
  Funktion damit unterdrückt wird. Öffnungsereignisse niemals voreilig lesen.
- Testdaten und alle Einstellungen liegen ausschließlich im temporären
  `GLIDE_DATA_DIR`. Der startbare Stand 3.32.0 ist vollständig archiviert.

## Prüfstand und Lieferung

**Abgeschlossen:** Vollprüfung Exitcode 0, 71 automatisierte Schritte,
alle 56 Integrationssuiten und fünf Analysen bestanden.
[Vollprotokoll](../tests/qa-3.32.1/klappkontrolle_2026-09-30/ergebnis.json)
und [SHA-256-Abgleich](../tests/qa-3.32.1/klappkontrolle_2026-09-30/abgleich.json):
139 Dateien der Python-Fassung und 53 Dateien des macOS-Bundles bytegleich;
Version 3.32.1, `de.shaye.glide` unverändert, Ad-hoc-Signatur verifiziert.
Der [QA-Bericht](07_QA_BERICHT.md) nennt Vorsicherungen und manuelle Grenzen.
Eine laufende Glide-Instanz muss neu gestartet werden.

Performance-Pakete P01–P07, D04 und G29 bleiben geplante Folgerunden.
D01–D06 sind entschieden, D07 nach Begriffserklärung offen. D08 ist umgesetzt.
