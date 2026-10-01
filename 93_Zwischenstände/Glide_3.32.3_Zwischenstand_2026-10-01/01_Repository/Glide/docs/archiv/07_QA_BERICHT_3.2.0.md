# QA-Bericht 3.2.0

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
gesondert festgehalten: `abschluss/ergebnis.json`, Vollmodus, Exitcode 0.
Syntax, Versionen, Index, alle drei Suiten, beide Analysen und die semantische
Reproduktion beider Backupdateien sind erfolgreich. Die Release-Arbeitsdaten werden zusätzlich über den
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
wurden gesondert in Windows eingelesen und als Sichtnachweis aufgenommen.
Die finalen Bilder `abschluss/screenshots/release_hell.png` und
`abschluss/screenshots/release_hell_dunkel.png` im genannten QA-Ordner wurden
beide angesehen: Kopfbereich einschließlich der zwei Listenlabels ohne
Überlappung; dunkles Theme grau, alle drei Arbeitslisten sichtbar. Der
Unterschied 43/42 Pixel im angeforderten Kopfmaß bleibt als Messtoleranz
dokumentiert und verursachte hier keinen sichtbaren Überlauf.

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
