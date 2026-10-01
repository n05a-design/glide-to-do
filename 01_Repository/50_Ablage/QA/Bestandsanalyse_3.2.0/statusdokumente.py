"""Aktuellen Prüfstand von historischen Aussagen trennen."""
from dokumente_abgleichen import ROOT, save

save('docs/09_STARTKONTEXT.md', '''# Startkontext für einen neuen Bearbeiter

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
`docs/09_ARBEITSAUFTRAG_BESTANDSANALYSE.md` erhalten.

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
''')

save('docs/07_QA_BERICHT.md', '''# QA-Bericht 3.2.0

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Aktueller Nachweis

Die Bestandsanalyse wurde auf Windows mit Python 3.12.12 und Tcl/Tk 8.6.17
ausgeführt. Alle App-Imports und Prüfungen nutzen isolierte Testdaten. Die
gebündelte Python-3.12.14-Laufzeit konnte Tcl nicht initialisieren; verwendet
wurde die vorhandene, funktionierende Python/Tk-Installation von Inkscape.
Das ist eine Prüf-Laufzeit und keine neue Produktabhängigkeit.

| Prüfung | Ausgangslauf | Nach Korrektur |
|---|---|---|
| Integration `test_glide.py` | Abbruch: veraltetes Attribut `system_box` | bestanden |
| Datenintegrität `test_datenintegritaet.py` | Abbruch: leere Zeilengeometrie vor Windows-Mapping | bestanden |
| App-Durchlauf `audit_app.py` | keine Befunde | keine Befunde |
| Syntax/Version | App 3.2.0, Schema 10 | unverändert; zentraler Prüfablauf prüft mit |
| Statische Analyse | 0 nie genannte Funktionen/Konstanten | keine Quelländerung |
| Erreichbarkeit | 508/520, 0 gleiche Methodenstrukturen | Kandidaten sind keine bewiesenen toten Funktionen |

Logs liegen im äußeren Workspace unter
`50_Ablage/QA/Bestandsanalyse_3.2.0/`; der abschließende Gesamtlauf wird dort
gesondert festgehalten. Die Release-Arbeitsdaten werden zusätzlich über den
Backup-Prüf- und Normalisierungspfad im Integrationstest kontrolliert.

## Gezielte Testkorrekturen

1. Der nur unter Windows laufende Layouttest verwies auf `system_box`, das
   seit dem Wegfall des Systemrahmens nicht mehr existiert. Er prüft jetzt
   Reihenfolge und Abstand des realen `system_listbox` und ausdrücklich das
   Fehlen des alten Rahmens.
2. Windows meldet für den Kopfblock 43 Pixel und für den festen Themenschalter
   42 Pixel angeforderte Höhe. Der Vergleich erlaubt höchstens einen Pixel
   native Schriftmetrik-Differenz. Die Höhe der Labelzeile mit/ohne Labels wird
   weiterhin **exakt gleich** verlangt. Das ist keine Behauptung pixelgleicher
   Bedienelemente; die Darstellung ist zusätzlich visuell zu prüfen.
3. Der Datenintegritätstest verarbeitet nach dem Aufbau einmal die
   Windows-Fensterereignisse mit `root.update()`, bevor er Drag-Koordinaten
   ausliest. Alle Bestands- und Strukturassertionen bleiben unverändert.

Der produktive App-Quelltext und die gleichlautende externe `.pyw` blieben
bytegleich. App-SHA-256:
`6309f2669f5490777d342138e9fe304b27a4e728404d0359952e3cd4bfc01715`.

## Codebefunde und Grenzen

- 14.591 Textzeilen, 539 Funktionen/Methoden, 133 Konstanten, 25 Funktionen
  über 80 Zeilen, 102 wörtlich doppelte Blöcke; `insert_tree_items` hat
  146 Zeilen und neun Verschachtelungsebenen. Zeilenangaben folgen dem
  aktuellen Analysewerkzeug, nicht dem gerundeten Übergabetext.
- 18 breite `except Exception` im aktuellen Code; die ältere Prüfung von 20
  Stellen ist historisch. Es wurde keine pauschale erneute Bereinigung gemacht.
- Die frühere Aussage „0 Emoji im Quelltext“ war falsch: Gruppenmarker 📁,
  Wichtigkeit hoch 🚩 und Beschreibungsmarker 📝 (an zwei Stellen) sind noch
  vorhanden. Die Tabellenprüfung von `ICONS` erfasst sie nicht.
- `run_modal` ist der einzige `wait_window`-Pfad. Weitere Grabs dienen
  Dropdowns, der kontrollierten Übergabe an native Dialoge und der Rückgabe.
- Das zu 3.0.1 gemeldete Einfrieren wurde nicht reproduziert. Der in 3.1.0
  zentralisierte Grab-Lebenszyklus adressiert einen plausiblen Mechanismus;
  die Behebung der ursprünglichen Meldung bleibt **NICHT VERIFIZIERT**.

Einzelfunde mit Fundstelle, Maßnahme und nächstem Test stehen in
`11_BESTANDSANALYSE.md`. Es wurden weder der Monolith aufgeteilt noch Symbole
ersetzt oder Datenformate geändert.

## Sichtprüfung und historische Nachweise

Die zwölf vorhandenen Linux-Aufnahmen unter
`50_Ablage/Screenshots/3.2.0/` sind historische Nachweise der früheren Runde.
Sie sind keine Windows-/macOS- oder Store-Abnahme. Die neuen Release-Arbeitsdaten
werden gesondert in Windows eingelesen und als Sichtnachweis aufgenommen;
Pfad und Prüfergebnis stehen im Bestandsbericht.

Die früheren ausführlichen QA-Berichte sind in `archiv/` erhalten. Die
behaupteten Zufallsläufe aus 2.11.0 wurden nicht wiederholt; das zugehörige
Werkzeug fehlt. Der behauptete Verlust einer „Phase 11“ lässt sich ohne
Git-Historie oder Originaldatei nicht belegen. `pyflakes` ist kein aktuelles
Projektgate; es wurde keine zusätzliche Testabhängigkeit installiert.

## Noch manuell zu prüfen

- Windows: mehrere Monitore und DPI-Stufen, echte Strg-/Shift-Auswahl,
  Drag & Drop, Textzeichen, lange Benutzung mit verschachtelten Dialogen.
- macOS: gesamte Plattformmatrix einschließlich Cmd-Auswahl, Cmd+Q,
  nativer Dateidialoge, Darstellung und Dateipfade.
- Wiederherstellung mit Kopien echter Daten und Anhänge; Verhalten großer
  Bestände ist trotz technischer Validierungslimits nicht als performant belegt.
- Installer/App-Bundle, Signatur, Notarisierung, gegebenenfalls Sandbox und
  Store-Import: offen, weil keine fertigen Build-Artefakte vorliegen.

Wiederholbarer Prüfaufruf und Voraussetzungen: `../tests/README.md`.
''')

save('docs/10_RELEASE_CHECKLIST.md', '''# Release-Checkliste

Stand: 04.09.2026 · App-Version 3.2.0 · Datenformat 10

## Source und Qualität

- [x] `VERSION`, `APP_VERSION`, Testprüfung und Changelog nennen 3.2.0.
- [x] Syntax und drei automatisierte Suiten auf Windows geprüft; Details und
  Testkorrekturen in `07_QA_BERICHT.md`.
- [x] Referenzbestände Schema 10, 9, 8, 7, 6, 5, 4 und 2 erhalten.
- [x] Bestandswächter und 130 Gruppen-Kombinationen automatisiert geprüft.
- [x] Statische und Erreichbarkeitsanalyse ausgewertet; keine automatischen
  Löschungen aus Erreichbarkeitsvermutungen abgeleitet.
- [x] Dokumente und Produktdatenblatt auf tatsächlichen Stand 3.2.0 abgeglichen.
- [ ] Vollständige manuelle Windows-/macOS-Matrix abgeschlossen.
- [ ] Einfrieren bei längerer Windows-Benutzung reproduziert oder belastbar
  ausgeschlossen; ursprüngliche Fehlermeldung weiterhin nicht verifiziert.
- [ ] Textzeichen, mehrfache DPI/Monitore und reale Eingabegeräte geprüft.
- [ ] Drei Emoji-Ausnahmen zur Textzeichen-Vorgabe entschieden und geprüft;
  bei Gruppenmarkern TXT-Kompatibilität bewahren.
- [ ] Backup und Restore mit Kopien realer Daten und Anhänge geprüft.
- [ ] Große Bestände auf Zielgeräten vermessen.

## Produktidentität

- [ ] Publisher, Copyright, Supportkontakt, Website und Datenschutz-URL festgelegt.
- [ ] Lizenzmodell und Preis entschieden; `LICENSE.md` ist weiterhin Platzhalter.
- [ ] Windows-Zielarchitektur, AppUserModelID und stabile Installer-ID festgelegt.
- [ ] macOS Bundle Identifier, Mindestversion und Architektur festgelegt.
- [ ] Namens-/Markenrisiko „Glide“ fachlich geprüft.

Technische Fakten und offene Entscheidungen: `decisions/PRODUCT_IDENTITY.md`.

## Build und Distribution

`packaging/` enthält eine Vorbereitungserklärung und Verzeichnisse; konkrete
Build-Konfigurationen und freigegebene Binärartefakte fehlen.

- [ ] Build-Abhängigkeiten gepinnt und reproduzierbarer PyInstaller-OneDir-Build.
- [ ] App-Icons aus freigegebenem Gestaltungsmaster abgeleitet.
- [ ] Windows-Installer und macOS-App/DMG auf Clean Machines geprüft.
- [ ] Windows-Binärdateien/Installer signiert und Zeitstempel verifiziert.
- [ ] macOS Developer-ID-Verteilung signiert, notarisiert, Ticket angeheftet
  und Gatekeeper geprüft.
- [ ] Falls Mac App Store: separater Sandbox-/Entitlement-/Zugriffsworkflow geprüft.
- [ ] SHA-256-Manifest und Release Notes für die tatsächlichen Binärartefakte.
- [ ] Finale Pakete unter äußerem `30_Release_Exports/3.2.0/` abgelegt;
  ein leerer Zielordner ist kein Buildnachweis.

## Store-Vorbereitung

- [x] Faktische Textgrundlage liegt im äußeren
  `40_Store_Material/Produktdatenblatt_3.2.0.md` vor.
- [x] Drei editierbare Arbeitslisten mit recherchierten Anforderungen und
  Quellen sind als gemeinsames Glide-Backup vorbereitet.
- [ ] Vertriebskanal je Plattform entschieden (Windows MSI/EXE oder MSIX;
  macOS direkte Verteilung oder Store).
- [ ] Datenschutzangaben gegen das endgültige Build einschließlich Installer,
  Website und optionalen Diensten geprüft und im jeweiligen Formular beantwortet.
- [ ] Zielplattform-Screenshots nach den gewählten Store-Vorgaben erstellt.
- [ ] Store-Texte, URLs und Altersfreigabe redaktionell/fachlich freigegeben.

## Status

3.2.0 bleibt ein interner Vorabstand. Automatisierte Source-Prüfungen sind kein
öffentliches Stable-Release. Vor Veröffentlichung fehlen insbesondere manuelle
Plattformabnahme, Produktidentität, reproduzierbare Builds, Signing und finale
Store-Materialien. Recherchierte Anforderungen sind mit Abrufdatum in den
Release-Arbeitslisten und Store-Unterlagen festgehalten und vor Einreichung
erneut zu prüfen.
''')

print('Statusdokumente aktualisiert.')
