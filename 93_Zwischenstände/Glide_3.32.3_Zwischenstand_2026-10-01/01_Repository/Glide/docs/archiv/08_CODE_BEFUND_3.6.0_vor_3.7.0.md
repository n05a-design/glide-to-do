# Codebefund und bereinigte Grenzfälle – Glide 3.6.0

Stand: 06.09.2026 · App-Version 3.6.0 · Aufgabendatenformat 11

Dieses Dokument führt die früheren Codebefunde als Prüfspur weiter. Für den
aktuellen Release-Stand zählt der Quellcode unter `src/glide/app.pyw` zusammen
mit dem vollständigen Windows-Prüflauf; ältere Einzelberichte und ihre
unfertigen Befunde liegen unter `docs/archiv/`.

## Aktueller Befund

Die 3.6-Änderungen sind in einer einzelnen startbaren Tk-Datei gebündelt und
werden durch Syntax-, Erreichbarkeits- und Integrationsprüfungen abgedeckt.
Der vollständige Lauf vom 06.09.2026 meldete für alle sieben App-/Audit-Suiten
Exitcode 0. Es gibt keine offenen TODO-, FIXME- oder Debug-Print-Stellen in den
geprüften produktiven Pfaden. Die Erreichbarkeitsanalyse berücksichtigt
Callback-Bindungen und den Moduleinstieg; gemeldete Tk-Methodenattribute werden
nicht als tote Produktfunktionen gewertet.

## Befunde aus älteren Analysen und ihre 3.6-Behandlung

| Früherer Befund | Aktueller Umgang | Nachweis |
|---|---|---|
| Artwechsel konnte die 20-Normal-Labels-Grenze überschreiten | Vor dem Wechsel wird die resultierende Labelmenge geprüft. Bei Überschreitung bleibt der Punkt unverändert und erhält eine Warnung. | `set_item_kind`, `test_release36.py` |
| Verschieben konnte die Punkttiefe über 100 bringen | `make_subitem` berechnet Ziel- und Unterbaumhöhe vor der Mutation und bricht bei Überschreitung ab. Lade-, Import- und Kind-Anlage prüfen dieselbe Grenze. | `MAX_ITEM_DEPTH`, `make_subitem`, Integritäts- und 3.6-Suite |
| Uneinheitliche Emoji in Übersichten | Sichtbare Ordner-/Notiz-/Fälligkeitssymbole verwenden die zentrale `ICONS`-Tabelle und Textzeichen. Historische Emoji werden nur noch für das Lesen alter Eingaben akzeptiert; sie werden nicht neu geschrieben. Der Papierkorb bleibt als bewusstes semantisches Unicode-Zeichen bestehen. | `ICONS`, `DUE_COLUMN_ICON`, Symbolprüfung |
| Angeblich nicht erreichbare Callback-Methoden | Aufrufer über `command=`, `bind()` und den Moduleinstieg sind einbezogen. | `analyse_erreichbarkeit.py`, `audit_app.py` |
| Verlorene „Phase 11“ oder frühere Git-Stände | Ohne Git-Historie nicht rekonstruierbar; die aktuelle Auditphase ist im Repository vorhanden und wird ausgeführt. | `audit_app.py`, `tests/qa-3.6.0/abschluss/ergebnis.json` |

Die Korrekturen wurden nicht nur statisch eingetragen: Die neue Release-36-Suite
prüft den Labelgrenzfall, eine maximale Tiefenkette, Teilbackup/Import,
Vorlagenvalidierung, Sperrdateien, Datenordnerkopie und die Startansichten mit
isolierten Daten.

## Bewusst getrennte Grenzen

Ein echter Synchronisationsdienst, Konfliktzusammenführung, native macOS-
Abnahme, Mehrmonitor-/DPI-Matrix, Screenreaderprüfung, Langzeitmessung,
Installer, Signierung und Storefreigabe sind keine stillschweigend erledigten
Codebefunde. Sie stehen als Freigaben in `docs/10_RELEASE_CHECKLIST.md` und
`docs/18_QA_3.6.0.md`.

Die Tk-Treeview zeichnet ihre Auswahl als Rechteck. Runde Auswahl ist dort
nicht ohne einen Listenumbau möglich; umgesetzt sind die selbst gezeichneten
Label-Chips und Kalendertage. Die Materialoptik bleibt eine abschaltbare
getönte Oberfläche mit Glaskanten; echter selektiver Desktop-Blur ist im
separaten Glasbericht ausdrücklich abgegrenzt.

## Prüfpfad

```text
tests/tools/pruefen.py --modus voll --timeout 600 --protokoll tests/qa-3.6.0/abschluss
```

Das maschinenlesbare Ergebnis und die Hashes liegen unter
`tests/qa-3.6.0/abschluss/`.
