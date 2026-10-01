# Glide – kompakte Weitergabe an einen neuen Chat

Stand: 11.09.2026. Diesen Text als Kontext für die Fortsetzung verwenden.

## Auftrag und aktuelle Prioritäten

Glide ist eine lokale, deutschsprachige Aufgabenanwendung für macOS und Windows. Arbeite pragmatisch, datenschonend und mit möglichst wenigen Abhängigkeiten. Bestehende Funktionen und Nutzerdaten bewahren.

Der Nutzer möchte mögliche Erweiterungen gegenüber Todoist, Microsoft To Do, Planner und Google Keep beurteilen. Seine jüngste Korrektur ist maßgeblich:

1. **Erinnerungen haben Vorrang.** Datum/Uhrzeit und Wiederholungen existieren; eine verlässliche Erinnerungsfunktion fehlt.
2. **Pinnwand und Reiteransicht für Listenelemente sind ausdrücklich erwünscht.** Vorläufige Lesart der Reiter: Aufgaben oder Aufgabengruppen innerhalb einer bestehenden Liste. Die genaue Ebene ist noch offen.
3. **Keine zusätzlichen Ablagefächer oder parallele Statusverwaltung:** „In Bearbeitung“ und Labels erfüllen diesen Zweck bereits.
4. **Keine neue Projektmappe als Datenstruktur:** Ordner, Listen, Beschreibungen und Anhänge existieren. Ein möglicher Mehrwert wäre lediglich eine ergänzende Ansicht derselben Inhalte.

Der letzte Auftrag war, diese Weitergabe und eine separate [Vorschlagsdatei](Glide_Funktionsvorschlaege_2026-09-11.md) zu erstellen. Die neuen Funktionen wurden dadurch noch nicht implementiert; die gesamte Ideensammlung ist keine pauschale Umsetzungsfreigabe. Bei einer Fortsetzung den konkreten Auftrag des Nutzers und diese Prioritäten beachten.

## Arbeitsorte

Workspace: `/Users/shaye/Library/CloudStorage/OneDrive-Persönlich/Glide ToDo`

Relative Pfade ab Workspace:

- Kanonischer Code: `01_Repository/Glide/src/glide/app.pyw`
- Arbeitsregeln: `01_Repository/Glide/AGENTS.md`
- Startbare Arbeitskopie: `07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.7.0.pyw`, mit vollständigem Ressourcenordner.
- Aktuelle technische Übergabe: `01_Repository/Glide/docs/09_PROJECT_HANDOFF.md`
- Vorrangiger Nachtrag: `01_Repository/Glide/docs/26_MAC_VORLAGEN_UND_ABLAGE_3.7.0.md`
- Produktgrenzen / Architektur: `docs/01_PRODUCT_CONSTRAINTS.md` und `docs/02_ARCHITECTURE.md` im kanonischen Projekt.

## Verifizierter Ausgangsstand

Unveröffentlichter Entwicklungsstand **3.7.0**; Aufgabenformat **12**, Einstellungen **2**, Vorlagenformat **2**. Python/Tk, lokale Ablage, ohne erforderliches Konto oder Internet.

Bereits vorhanden: verschachtelte Ordner/Listen, Aufgaben/Gruppen/Überschriften/Long-Tasks, Unterpunkte, Labels, Wichtigkeit, Fälligkeit mit Uhrzeit, Wiederholungen, Suche, Kalender, Anhänge, Papierkorb, Rückgängig, Vorlagen und Import/Export. Die Startseite enthält unter anderem analoge Uhr, Mondphase, Tagesziel und Aktivitätsanzeige.

Die vorherigen sechs Änderungswünsche wurden umgesetzt:

- Mac-Bildlauf: MouseWheel und Tk-9-TouchpadScroll; horizontale Gesten werden nicht zu vertikalem Scrollen.
- Vorlageneditor: vollständige Hell-/Dunkeldarstellung und Detailmasken wie bei normalen Aufgaben/Listen; isolierter Entwurf mit Abbruch ohne Übernahme.
- Vollständige Struktur- und Detailbearbeitung, Labels, Anhänge und relative Vorlagentermine.
- 16 Praxisvorlagen, darunter Immobilien, WordPress, WEG und Baukommunikation; reproduzierbar erzeugte Beispieldateien.
- Listenübersicht mit Pfad, Kennzahlen, Labels und getrennten Vorschauen der nächsten Aufgaben.
- Dokumentation, Ressourcen, Arbeitskopie und Beispiele abgeglichen; alte Dateien nachvollziehbar archiviert, keine endgültige Löschung und keine Änderung echter Nutzdaten.

## Prüfstand und Grenzen

Der gespeicherte vollständige Prüflauf vom 11.09.2026 ist erfolgreich: elf Testsuiten, Syntax, Versionskonsistenz, Dokumentation und Beispielabgleiche. Nachweis: `01_Repository/Glide/tests/qa-3.7.0/macos-nachbesserung/final/ergebnis.json`, Exitcode 0, macOS/Python 3.14.5.

**Weiter offen:** physischer Trackpad-Test und vollständige native Sichtabnahme, weitere DPI-/Monitor-Konfigurationen, Screenreader, Langzeitbetrieb, Installer und Signierung. Automatisierte Widgettests belegen keine abgeschlossene manuelle Abnahme. Die UI-Abnahme war zuletzt wegen fehlendem Zugang zur entsperrten Oberfläche nicht möglich.

## Regeln für weitere Implementierung

- Vor Codeänderungen `AGENTS.md` lesen, Ausgangstest und Nutzdatenpfade prüfen. Tests ausschließlich mit isoliertem `GLIDE_DATA_DIR`.
- Datenformatänderungen benötigen Migration, Originalsicherung und passende Tests.
- Bestehende Änderungswege `item_change`, `sidebar_change`, `guarded_structural_change` und `run_modal` verwenden; Symbole aus `ICONS`.
- Keine neue Laufzeitabhängigkeit ohne dokumentierte Entscheidung. Vor dem Überschreiben bestehender Dokumente den Originalstand im lokalen Archiv sichern.
- Kanonischen Code, startbare Arbeitskopie und Ressourcen konsistent halten. Prüfgrenzen offen nennen.
- OneDrive ist externe Dateisynchronisation, kein sicherer gleichzeitiger Mehrbenutzerbetrieb.
- Aufgabenbackups enthalten derzeit weder persönliche Einstellungen noch den separaten Vorlagenkatalog.

Nächster sinnvoller Einstieg: Erinnerungen anhand der separaten Vorschlagsdatei konkretisieren; Auslösung bei laufender/geschlossener App, nach Ruhezustand und Neustart getrennt prüfen. Vorhandene Fristen- und Wiederholungslogik wiederverwenden. Pinnwand und Reiter müssen bestehende Objekte referenzieren und dürfen keine parallelen Aufgabenkopien erzeugen.
