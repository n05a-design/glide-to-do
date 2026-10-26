# Tagesvorschlag mit direkten Freigaben (WA-12)

Fortsetzungsauftrag 26.10.2026 · Quellkandidat auf 3.45.0 · Aufgabenformat 26 unverändert.

Der bestehende Weg „Was passt heute?“ berücksichtigt jetzt Aufgaben, deren Abschluss andere Aufgaben freigibt. Überfällig, heute fällig, liegen geblieben und bald fällig behalten Vorrang; anschließend folgen direkte Freigaben vor lediglich wichtigen Aufgaben. Bei gleichem Freigabegrund stehen mehr Freigaben zuerst. Jede Zeile nennt die tatsächliche Zahl, etwa „gibt 2 weitere Aufgaben frei“; dringliche Aufgaben zeigen diese Zahl ergänzend zu ihrem bisherigen Grund.

Gezählt werden aktive offene Folgeaufgaben, für die genau eine offene direkte Voraussetzung übrig ist. Mehrere offene Voraussetzungen, erledigte oder archivierte Folgeaufgaben und Selbstbezüge erzeugen keine falsche Freigabezusage. Erledigungsstände archivierter Voraussetzungen werden nach demselben Vertrag wie `ListApp.open_blockers` aufgelöst; unbekannte Ziele blockieren dort bereits bisher nicht. Die Berechnung zählt direkte Folgen, keine transitive Kette. Blockierte Kandidaten, bereits heute und künftig geplante Aufgaben bleiben ausgeschlossen.

Die Freigabezahl ist Teil der Vorschau-Signatur. Ändert sich etwa eine archivierte Voraussetzung nach dem Öffnen, verlangt Übernehmen eine neu geprüfte Auswahl. Auswahl und Vorschau verändern keine Aufgaben; Übernahme setzt weiterhin ausschließlich den Bearbeitungstag mit bestehendem Ein-Undo-Weg. Einplanen erledigt keine Voraussetzung und ändert weder Fälligkeit, Aufwand noch Beziehungen.

## Prüfung

- Bestehende Baseline des Fachmoduls: 8/8 grün.
- [Rote Gegenprobe](fach_gegenprobe.json) am bisherigen Stand: 13 Fälle, neun grün, zwei Fehler und zwei fehlgeschlagene Assertions. Vier neue Verhaltensfälle fehlen erwartungsgemäß; der Ausschlussfall besteht bereits.
- [Fachabschluss](fach_abschluss.json): 14/14 grün, einschließlich direkter Kette/Zyklus, letzter offener Voraussetzung, gleicher Dringlichkeit, Zählung, Text, Budget, Unveränderlichkeit und archiviertem Statuswechsel.
- [Bestehende Tagespaketsuite mit neuem WA-12-Abschnitt](tagpaket.json): zehn Prüfgruppen grün. Echter Tagesbeginn-/Vorschlagsknopf, Auswahl, Übernahme, ein Undo/Redo und ungültig gewordene Vorschau geprüft; die bisherigen Kalender-/Fokus-/Schreibfehler-/Neustartfälle bleiben ebenfalls grün.
- Neuer Freigabetext in acht Vorschlagskonfigurationen (860 × 700 bzw. 1280 × 800, mittlere/große Schrift, Hell/Dunkel), zusätzlich acht Fokusregressionen geprüft. Keine neue Dauerleiste oder neue Bedienelemente.
- Warme vollständige Vorschlagsberechnung im künstlichen Bestand: bei 1.000 zusätzlichen Aufgaben Median 13,43 ms, bei 10.000 Median 159,40 ms, je fünf Messungen. Tatsächlich 1.005 bzw. 10.005 Kandidaten einschließlich Grundbestand; keine allgemeine Geschwindigkeitsverbesserung behauptet.

Syntax, Versionskonsistenz, Standprüfung der 80 aktiven Dokumente, Datei-/Abschnittsverweise und Datenschutz der neuen öffentlichen Nachweise sind grün. Der Standprüfungs-Vorlauf beanstandete die umformulierte Quell-README; eine ausdrückliche Standzeile ist ergänzt.

Windows, Python 3.14.7 / Tk 9.0.4. Alle App-Prüfungen verwenden vor Import einen temporären `GLIDE_DATA_DIR`. Native Mac-/Reader-/DPI- und menschliche Sicht-/Bedienabnahme bleiben offen.

## Quell- und Liefergrenze

[Quellstand mit vier Datei-Hashes](quellstand.json). Die Fachlogik liegt im vorhandenen Tk-freien `day_proposal.py`; `ListApp.day_proposal` liefert die kurzlebige Statusprojektion, `render_day_proposal` verwendet den erklärten Text. Keine neuen Laufzeitdateien, Abhängigkeiten, gespeicherten Felder oder Formatstufen. Bestehende Mutationseinstiege bleiben erhalten.

Der neue Funktionsstand ist lokal im Quellbaum umgesetzt. `07_Python-Versionen` enthält weiterhin den zuletzt geprüften 3.45.0-Abschluss mit App `2e69d875…`; Quelle und Lieferung unterscheiden sich jetzt in `app.pyw` und `day_proposal.py`. Der frühere strenge CI-/Voll-/Liefernachweis wird dem neuen Kandidaten nicht zugerechnet. Gemeinsamer Versions-/CI-/Voll-/Lieferabschluss folgt am nächsten Phasenende nach D51. Kein Commit, Push oder Merge; die vorhandene Git-Indexsperre bleibt unangetastet.
