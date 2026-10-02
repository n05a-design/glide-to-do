# Glide 3.33.2 – Startseite „Ruhig“ und Aufbaukosten

Stand 02.10.2026 · Glide 3.33.2 · Aufgabenformat 20

Auftrag vom 02.10.2026: Startseiten-Standard nach D12 zusammen mit dem beauftragten Rest P03 (Startseite). Grundlage sind die Beschlüsse in der [Arbeitsrichtung](ARBEITSRICHTUNG.md) und der [Entscheidungsvorlage](../../../00_Arbeitsvorbereitung/Glide_Entscheidungsvorlage_2026-10-01.md#d12--standard-der-startseite). Keine Datenformatänderung, keine neue Abhängigkeit.

## Bedienvertrag D12

| Kachel | Standard | Inhalt |
|---|---|---|
| Heute | ja | Tagesziel, als Nächstes, eingeplant, heute fällig, „Mein Tag öffnen“ |
| Gismo | ja | Begleiter |
| Die nächsten sieben Tage | ja | Fälligkeiten je Tag |
| Zuletzt bearbeitet | ja | |
| Pinnwand-Vorschau | ja | |
| Zeichnungen | ja | |
| Angeheftet | ja | |
| Uhr, Begrüßung, Nächste Aufgabe, Vorlagen, Bestand und alle übrigen | nein | wählbar |

- **Zusammengeführte Kachel „Heute“:** Sie zeigt Tagesziel und nächste Aufgabe nur, solange die Kacheln „Begrüßung“ bzw. „Nächste Aufgabe“ ausgeblendet sind. Jede Angabe steht damit genau einmal auf der Startseite (`home_tiles.today_sections`).
- **Eigene Auswahl bleibt:** Eine gespeicherte Reihenfolge ist eine eigene Auswahl und bleibt nach dem Update unverändert. Ohne gespeicherte Reihenfolge gilt der Standard. Wer die Startseite nie eingerichtet hatte, sieht nach dem Update die sieben Kacheln; die übrigen bleiben über „Startseite anpassen“ erreichbar.
- **Korrektur:** Bis 3.33.1 speicherte das Ein- und Ausblenden im Bearbeitungsmodus nur die ausgeblendeten Kacheln. Ohne gespeicherte Reihenfolge setzte der nächste Start den Standard wieder ein, eine eingeblendete Kachel war danach weg. Ein- und Ausblenden halten jetzt die ganze Auswahl fest (`home_tiles.own_selection`).
- **Zurücksetzen:** „Standard wiederherstellen“ im Dialog „Startseite einrichten“ setzt den Entwurf auf den Standard. Entspricht die gespeicherte Auswahl dem Standard, bleibt die Startseite „nicht eingerichtet“ und folgt einem künftigen Standard.

Die Fachlogik ist Tk-frei in `home_tiles.py` (D17): Kachelbestand mit Begründungen, Standard, Normalisierung der Einstellungen, eigene Auswahl, Zurücksetzen und die Regel der zusammengeführten Kachel. Acht Unit-Tests.

## Aufbaukosten (Rest P03)

Profil und Gegenproben (macOS, 1.000 Punkte, zwölf Kacheln) zeigten, wohin die Zeit eines Neuaufbaus geht: Python legt die Kacheln in rund 90 ms an, der Rest ist Tk-Layout. Das Layout pendelt sich über viele Runden ein, rund zehn Größenmeldungen je Widget. Daraus folgen vier Änderungen; jede betrifft Verhalten, das gleich bleibt:

1. **Größenmeldungen des Hauptfensters in Tcl filtern.** Zwei `<Configure>`-Bindungen am Hauptfenster galten über dessen Bindtag für jedes Kind; Python prüfte rund 5.000-mal je Aufbau, ob das Ereignis vom Hauptfenster kam. `bind_main_window_resize` vergleicht `%W` in Tcl und ruft Python nur für das Fenster selbst. Das wirkt in jeder Ansicht.
2. **Gerundete Flächen und Knöpfe einmal je Leerlauf zeichnen** (`DeferredDrawCanvas`). Größenänderungen planen eine Zeichnung im nächsten Leerlauf; `_draw()` bleibt für Design und Hover sofort. Ein ausstehender Auftrag wird beim Zerstören abgemeldet.
3. **Umbruchbreite nur bei Änderung setzen.** Ein erneutes Setzen derselben Breite stieß eine weitere Layoutrunde an.
4. **Hintergrundfarben nur nach Designwechsel setzen.** Dieselbe Farbe erneut zu setzen zeichnete die ganze Startseite neu (rund 37 ms).

Geprüft und verworfen: Ausblenden der Startseite während des Neuaufbaus (kein Gewinn), Abschalten der globalen `<Map>`-Bindung (rund 10 ms, bei aktivem Hintergrund nötig), dauerhaftes Vorhalten der Schriften (kein Gewinn).

## Messung

[Zusammenfassung](../tests/qa-3.33.2/startseite_2026-10-02/messung/zusammenfassung.json): macOS, Python 3.14.5, Tk 9.0; `scripts/pflege/messung_startseite.py` mit 1.000 Punkten, Terminen über die Woche, drei Zeichnungen und zwei angehefteten Seiten; je Lauf sechs warme Runden; alter (3.33.1) und neuer Code abwechselnd in vier Paaren. Median der Paarmediane, die vier Paare lagen jeweils innerhalb von etwa 1 %.

| Startseite | Wechsel von einer Liste | Aktualisierung an Ort und Stelle | Widgets |
|---|---:|---:|---:|
| 3.33.1, zwölf Standardkacheln | 789,7 ms | 764,2 ms | 180 |
| 3.33.2, dieselben zwölf Kacheln | 636,3 ms | 620,7 ms | 180 |
| 3.33.1 mit sieben D12-Kacheln | 593,3 ms | 547,4 ms | 110 |
| **3.33.2, Standard mit sieben Kacheln** | **547,8 ms** | **506,7 ms** | 114 |

Für jemanden ohne eigene Auswahl sinkt der Aufbau damit um rund ein Drittel (Aktualisierung 764 → 507 ms); bei gleicher Kachelzahl tragen die Aufbauänderungen rund 19 % bei. Die zusammengeführte Kachel „Heute“ bringt vier Widgets mehr. Das vorhandene Ansichtswerkzeug (`messung_performance.py`, zwei Paare, jeweils eigener Standard) zeigt zusätzlich die Bibliothek schneller (974 → 856 ms), weil der Tcl-Filter in jeder Ansicht wirkt; Liste, Tabelle, Seite mit Bildern und Notiz bleiben unverändert (±2 %).

Grenzen: eine Maschine, künstliche Daten, Messung schließt drei Tk-Zeichendurchläufe ein; kein allgemeines Latenzversprechen. Die frühere Linux-Zahl des Plans (348 ms, Beispieldaten) ist mit dieser Messung nicht vergleichbar.

## Prüfung

Neue Pflichtsuite `test_startseite3332.py` über echte Wege: neuer Bestand mit sieben Kacheln; „Heute“ mit Tagesziel und nächster Aufgabe; Einblenden von Begrüßung, Nächste Aufgabe und Uhr über die „+“-Knöpfe des Bearbeitungsmodus; keine doppelte Angabe; Auswahl nach erneutem Laden der Einstellungen erhalten; „Standard wiederherstellen“ und „Speichern“ im Dialog; Größenmeldungen eines Kindes erreichen Python nicht, eine Fenstergrößenänderung schon; fünf Größenmeldungen ergeben eine Zeichnung; Zerstören mit ausstehender Zeichnung ohne Fehler; Farben nach Designwechsel. Gegenprobe: Mit dem Stand 3.33.1 scheitert die Suite am Standard.

Fünf bestehende Suiten prüfen Kacheln, die nicht mehr zum Standard gehören (Begrüßung mit Schnellzugriff, Bestand mit Jahresanzeige). Sie blenden diese Kacheln jetzt über `set_home_tile_hidden` ein, statt sich auf den alten Standard zu verlassen: `test_features315`, `test_release37`, `test_ui_polish36`, `test_ui_updates`, `test_ui_followup36`.

## Abschluss 02.10.2026

[Nachweis](../tests/qa-3.33.2/startseite_2026-10-02/README.md), [Vollprotokoll](../tests/qa-3.33.2/startseite_2026-10-02/vollpruefung/ergebnis.json), [Quellstand](../tests/qa-3.33.2/startseite_2026-10-02/quellstand.json), [Lieferabgleich](../tests/qa-3.33.2/startseite_2026-10-02/auslieferung.json).

- **Vollprüfung Exitcode 0:** 78 Schritte – Syntax, Version, Dokumentation, Fixtures, Unit-Tests, alle 61 Integrationssuiten, Showcase, fünf Analysen, Beispiel- und Releasedaten; Screenshot-Erzeuger und menschliche Sichtprüfung plattformbedingt übersprungen. Quellstand (329 Dateien) vor und nach dem Lauf unverändert.
- **Erster Versuch** (`vollpruefung_versuch1`): alle Suiten grün, nur die statische Attributprüfung rot – die Hilfsklasse für das gebündelte Zeichnen erbte nicht von `tk.Canvas`. Sie heißt jetzt `DeferredDrawCanvas`; gezielte Suiten und der zweite Volllauf grün.
- **Auslieferung:** `abgleich_07.py` ohne Abweichung (3.33.1-Hauptdatei als `_Z` archiviert), Bundle neu gebaut; 143 Dateien in `07_Python-Versionen` und 57 im Bundle per SHA-256 gleich `src/glide`; Bundle 3.33.2, `de.shaye.glide`, Signatur gültig. Showcase mit `showcase_abgleich.py` ausgeliefert.
- **Manuell offen:** physische Bedienung der Startseite (Einblenden, Zurücksetzen, Hover der Knöpfe), Windows/Linux, DPI/Mehrmonitor und Screenreader.

## Anschluss

Das Ziel „Startseite höchstens 150 ms“ ist mit diesem Schnitt nicht erreicht. Der verbleibende Aufwand ist Tk-Layout je Widget; ein weiterer großer Schritt wäre, unveränderte Kacheln beim Aktualisieren zu erhalten statt neu aufzubauen – wie die Bibliothekskarten in 3.32.3, mit vollständiger Invalidierung (Daten, Datum, Design, Schrift, Spalten, Auswahl). Danach P04 Bildlayout, P06r, P08 sowie die Einblendung des Einstellungsfensters. Physische Bedienung, Windows/Linux, DPI und Screenreader bleiben offen.
