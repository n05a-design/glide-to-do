# Startkontext für einen neuen Bearbeiter

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Projekt

Glide ist eine lokale, deutschsprachige Aufgaben- und Listen-App aus Python und
Tkinter. Windows und macOS sind Zielplattformen. Kein Konto, keine eigene Cloud,
keine Telemetrie und kein Netzwerkclient in der Kernanwendung.

Der kanonische Quellstand liegt relativ zum Workspace unter
`01_Repository/Glide/src/glide/app.pyw`. Ein früherer Linux-Arbeitspfad ist keine
Voraussetzung. Der Monolith bleibt erhalten, das Datenformat bleibt 10.

## Zuerst lesen

`AGENTS.md`, `docs/01_PRODUCT_CONSTRAINTS.md`, `docs/02_ARCHITECTURE.md`,
`docs/09_PROJECT_HANDOFF.md`, `docs/11_BESTANDSANALYSE.md`.
Bei Widersprüchen gilt der geprüfte Quellstand; historische Berichte sind keine
aktuellen Prüfnachweise. Der ursprüngliche Arbeitsauftrag ist als Referenz in
`docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` erhalten – **abgeschlossen und nicht
erneut auszuführen**. Offene Arbeit steht in `docs/09_PROJECT_HANDOFF.md`,
Abschnitt 13.

## Architektur und Daten

- Änderungen an Punkten über `item_change`, an Listen/Ordnern über
  `sidebar_change`; Wirkung mit `ChangeRecord.mark()` melden.
- Umbauaktionen zusätzlich unter `guarded_structural_change`; der
  Änderungsrahmen liegt darin. Auswahl mit `selected_items_for_change` prüfen.
- Modale Dialoge warten ausschließlich mit `run_modal`. Dropdowns und native
  Dateidialoge haben ergänzende, kontrollierte Grab-Lebenszyklen.
- Testisolierung: `GLIDE_DATA_DIR` vor dem Import setzen. Echte Nutzdaten nie
  für Tests verwenden. `.pyw` mit `SourceFileLoader` laden.
- `active_list_id` und `app_title` zusammenhalten; `save_items` synchronisiert
  den Titel sonst in die falsche Liste zurück.
- Portable Backups unterstützen Schema 4 bis 10. Die Verzeichnis-Migration
  und die alte Labelfarbzuordnung sind seit 3.2.0 entfernt.
- `ICONS` enthält Textzeichen (`⊕`, `▦`, `◈`). Die vollständige Umstellung
  ist offen: Gruppenmarker, hohe Wichtigkeit und Beschreibungsmarker sind noch
  Emoji außerhalb der Tabelle. Gruppenmarker auch im TXT-Import/-Export.

## Prüfstand

Der aktuelle Windows-Prüflauf verwendet Python 3.12.12 und Tk 8.6.17. Alle drei
Suiten sind nach gezielten Plattformkorrekturen im Testaufbau lauffähig; den
verbindlichen Abschlussstand samt Logs nennt `docs/07_QA_BERICHT.md`.
Der App-Quelltext wurde bei der Bestandsanalyse nicht verändert.

Gemeinsamer Aufruf mit einer Python-Installation einschließlich funktionierendem Tk:

```text
python tests/tools/pruefen.py --modus schnell
```

Ein grüner Lauf ersetzt keine manuelle Windows-/macOS-Prüfung. Besonders offen:
verschachtelte Dialoge bei längerer Nutzung, mehrere Monitore/DPI,
Cmd-Tasten auf macOS, reale Eingabegeräte, Backup-Restore mit Datenkopien,
Installation und Signatur.

## Erledigt und offen

- Dokumente, Word-Arbeitsgrundlage und äußere Produktunterlagen wurden auf
  3.2.0 abgeglichen; ältere Fassungen bleiben in den jeweiligen Archiven.
- `tests/tools/pruefen.py` bündelt den Prüfablauf; `releasedaten.py` erzeugt
  ein gemeinsames Komplettbackup mit drei Release-Arbeitslisten.
- Das gemeldete Einfrieren ist weiterhin **NICHT VERIFIZIERT**: Die zentrale
  Grab-Rückgabe beseitigt einen plausiblen Mechanismus, die ursprüngliche
  Meldung wurde nicht reproduziert.
- `insert_tree_items` hat neun Verschachtelungsebenen. Ein Refactoring ist
  nicht beauftragt. Weitere Befunde stehen in der Bestandsanalyse.
- Publisher, Kontakt/URLs, Preis, Lizenz, Kennungen, Zielarchitekturen und
  Markenfreigabe sind Inhaberentscheidungen; Packaging/Signing fehlen.
- Anhangs-Drag-&-Drop und ein Ersatz der Treeview sind nicht umgesetzt und
  nicht zur eigenmächtigen Umsetzung freigegeben.

## Arbeitsweise

Kleine nachvollziehbare Schritte, keine Datenverluste, keine neue
Laufzeitabhängigkeit. Bestehende Gestaltung erhalten: Grau im Dunkelmodus,
Dunkelblau im Hellmodus, native Ordner-Klappdreiecke. Historische Dokumente und
Fixtures erhalten; alte Versionsnummern darin nicht auf 3.2.0 umetikettieren.
Changelog, relevante Dokumente und ausdrücklich offene Prüfungen mitführen.
