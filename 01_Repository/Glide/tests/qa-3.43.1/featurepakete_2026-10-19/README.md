# FP-07 Stufe 1 und FP-04 – Umsetzung und gemeinsame Prüfung

Stand 19.10.2026 · Glide 3.43.1 · Aufgabenformat 25 · lokaler Prüfkandidat, keine Lieferung

Der ausdrückliche Zweipaketauftrag ergänzt FP-07 Stufe 1 (gesamter lesbarer Markdownbaum) und FP-04 (Originalseiten und Notizen auf Pinnwänden) im bestehenden Kandidaten auf `1042727`. WA-26, FP-05, FP-06 und die integrierte Schutzrunde bleiben erhalten. Die App-Datei trägt SHA-256 `ca2130336fe1a1f66341a4a995c4043da3373bd930ffe5579ae4d3fac09b0e2d`; maßgeblich ist das [vollständige Manifest](quellstand_abschluss.json), weil sich Hilfsmodule und Prüfungen auch ohne Änderung dieses Einzelhashes ändern können.

Verhalten und Grenzen stehen im [Funktionsvertrag](../../../docs/20_FUNKTIONEN.md), die Ablage im [Datenvertrag](../../../docs/06_DATA_BACKUP_MIGRATION.md). JSON Canvas gehört zur weiterhin offenen zweiten Stufe. Markdown ist kein garantiert rückimportierbares Backup; die vollständige App-Sicherung bleibt der Restaurierungsweg.

## Gezielte Nachweise

- [FP-07, drei Fälle](05_markdown_abschluss.json): 11 Listen/Seiten, vier Ordner, 24 Originalaufgaben und genau 24 Checkboxen, 21 Anhangverweise auf 15 unterschiedliche Dateien, 40 Ausgabedateien und 55 gültige relative Links. SHA-256-Manifest, Abbruch, bestehendes Ziel, Flush-Abbruch sowie tatsächlicher Menü-/Paletteneintrag geprüft. Die unabhängige Vorschaukonversion wird für den vollständigen Bytevergleich bereits vor Laden des künstlichen Showcase pausiert; die Ausgabe selbst läuft durch den echten Dialog und Hintergrundworker. Die Bildkonversion hat eine eigene Pflichtsuite; der gesonderte Nachweis einer realen Windows-WIC-Konversion steht im [WA-26-Nachweis](../bildkonversion_2026-10-18/README.md).
- [FP-04, sechs Fälle](05_seitenkarten_abschluss.json): Anheften und Flächen-Undo/Redo, Originaländerungen, Verschieben/Verbinden/Entfernen, Archiv-/Lösch-Undo, echte Mausgeste und normaler Klick, Titelbild, Präsentation/Druck, Eingabetaste und vollständige App-Sicherung. Der echte ausgelieferte Leser 3.43.1 mit App-Hash `ed2b7eb…` öffnet und bereinigt dieselbe künstliche Datenablage und schreibt den neuen obersten Namespace unverändert zurück; der neue Leser stellt Kartenpositionen und Kanten wieder her. Dies ist kein allgemeiner Funktions- oder Importnachweis der älteren Fassung.
- Der Kartenaufbau vergleicht im selben Kandidaten 200 Aufgabenkarten mit 150 Aufgaben-/50 Seitenkarten. Beide Darstellungen werden vorgewärmt und in fünf Paaren mit wechselnder Reihenfolge gemessen; die Grenze bleibt unverändert maximal +10 %. Rohwerte und Verhältnis stehen im FP-04-Ergebnis.
- [Drei rote FP-07-Gegenproben](05_markdown_gegenprobe.json) und [sechs rote FP-04-Gegenproben](05_seitenkarten_gegenprobe.json) gegen die per Hash bestätigte App vor den beiden Paketen. Aktuelle Hilfsmodule bleiben vorhanden: dies sind App-Adapter-Gegenproben, kein vollständiger alter Quellbaum.
- [Gezielte Aufrufbilanz](gezielte_pruefung_abschluss.json) einschließlich der bestehenden Katalogsuiten 3.22 und 3.25; Gesamtabschluss unten.

## Abschließender Gesamtstand

Die eingefrorene Windows-Vollprüfung ist erfolgreich: 118 Schritte, 117 erfolgreich ausgeführt, 1 menschliche Sichtprüfung übersprungen; 99 Integrationssuiten und 803 Fachlogiktests. Die separate CI-Grundstufe endete ebenfalls mit Exitcode 0: 19 Schritte, davon 18 ausgeführt und 1 Hinweis. 152 Werkzeugtests sowie nochmals 803 Fachlogiktests ohne Systemzeitzonen bestanden. [Zusammenfassung](abschluss.json), [vollständige Schrittbilanz](vollpruefung_abschluss.json), [CI-Schrittbilanz](ci_abschluss.json). Die Hinweise werden dort einzeln genannt; insbesondere ist die ältere Lieferung keine aktuelle Quellenlieferung.

Die erneute [Hash-, Schutzdatei- und Git-Prüfung](validierung.json) gleicht alle 661 eingefrorenen Eingaben ab und führt den erlaubten Dokumentnachlauf einzeln auf. Alle 783 geschützten Liefer-, Beispiel-, Grafik- und Fixturedateien sind unverändert. [Inventur der gesamten Ablage](inventur_abschluss.json), [Datei- und Abschnittslinks](dokumentverweise_abschluss.json), [Benutzerpfadprüfung einschließlich neuer Dateien](datenschutz_abschluss.json). Rohlogs und lokale Hilfsskripte sind ignoriert. Ein älterer QA-Nachweis enthielt noch einen persönlichen Benutzerpfad; die [Maskierung](datenschutzbereinigung.json) erhält die Testergebnisse und den lokalen Rohbeleg. Die erzeugten Screenshots wurden durch den Assistenten angesehen; dies ist keine menschliche oder native Mehrplattformabnahme.

## Vorläufe und gefundene Korrekturen

Der [ursprüngliche aktive 97-Suiten-Vorlauf](../vollpruefung_2026-10-18/README.md) fand zwei Ausfälle derselben Pinnwand-Bildkonversion: Ein Controller wurde als Tk-Host übergeben. Die Canvas-Lebensdauer und der Kontextwechsel sind korrigiert; ein neuer Pinnwandfall ist auf dem Ausgangsstand rot und nachher grün. Das UI-/UX-Prüfwerkzeug beendet vor einem Interpreterwechsel seine Timer und Bindungen.

Der [unvollständige eingefrorene Vorlauf mit beiden neuen Paketen](vollpruefung_02_unvollstaendig.json) endete nach 43 Schritten: 40 ausgeführt, drei fehlgeschlagen. Zwei Fehler waren die fehlende Katalogzuordnung des Gesamtexports; die dritte Prüfung maß den Zeichnungszoom vor dem vorgesehenen 30-ms-Configure-Rückruf. Derselbe Zoomfehler wurde am unveränderten App-Ausgangsstand mit identischen Maßen reproduziert. Die Prüfung wartet jetzt begrenzt auf den echten Rückruf und behält die Größenassertion; vollständige Suite auf altem und neuem App-Stand grün, gültige zu große Zoomstufe in der kontrollierten Gegenprobe rot. Die Zeichenklasse ist AST-gleich geblieben. [Abgrenzung und Belege](zeichen_pruefzeitpunkt.json).

Die Prüfung einer vollständigen Ziehgeste deckte zusätzlich auf, dass der erste Mausdruck die Zielpinnwand durch Navigation abbaut. Die neue Hostbindung hält den Kontext bis zum Loslassen; die echte Geste und der gewöhnliche Klick sind jetzt geprüft. Im Gesamtexport wurde außerdem die doppelte Checkboxdarstellung eingebetteter Aufgaben behoben: Ein Vorkommen bleibt ein relativer Verweis, eine Originalaufgabe hat genau eine Checkbox. Gliederungszeilen sind keine Aufgaben. Codebeispiele mit Glide-URIs bleiben wörtlicher Text.

Weitere rote bzw. unterbrochene Zwischenstände bleiben unverändert vorhanden. Der Cache-Hashvorlauf maß das asynchrone Aufräumen einer unabhängigen WIC-Temporärdatei; im finalen Exportnachweis wird die Vorschauanforderung kontrolliert pausiert, ohne Dateien vom Bytevergleich auszunehmen. Mehrere ursprüngliche Zoomsonden erzeugten keinen geeigneten Defekt; sie werden nicht als rote Gegenbelege gezählt.

Der [vollständige Vorlauf 04](vollpruefung_vorlauf04.json) bestand alle automatisierten Prüfungen: 118 Schritte, 117 ausgeführt, nur menschliche Sichtprüfung übersprungen. Die [CI-Grundstufe desselben Stands](ci_vorlauf04.json) endete mit Exitcode 0; Hinweise betrafen den absichtlich älteren Lieferstand und den nicht erreichbaren Originalpaketserver. Der danach separat nachgewiesene Leserfehler verwarf ab dem 1.001. Pinnwand-Kontext Seitenkarten. Die pauschale Kontextgrenze ist entfernt; fünf Modultests einschließlich unveränderter Ein-/Ausgabeeinstellungen sind grün, die neue Regression war vorher rot. [Grenzfallnachweis](kontextgrenze.json). Die Kontexte selbst waren im Vorlauf noch nicht abgesichert; deshalb wurde der korrigierte Stand in einem neuen eingefrorenen Gesamtlauf geprüft. [Vorheriges Quellmanifest](quellstand_vorlauf04.json) und [vorherige Sicherung](sicherung_vorlauf04.json) bleiben erhalten.

Drei unveränderte ältere Prüfsuiten melden beim Interpreterabbau weiterhin Tcl-`after`-Rückrufe: `test_ui_updates` (1), `test_oberflaeche33321` (3) und `test_wiederholen` (38). Dieselben Anzahlen stehen bereits im Ausgangslauf vor beiden neuen Paketen. Dies ist eine verbleibende Prüfumgebungsgrenze; der Gesamtlauf wird nicht als meldungsfrei dargestellt. [Vergleich zum Ausgangslauf](pruefwerkzeug_hinweise.json).

## Einfrieren und verbleibende Tore

[661 Eingaben](quellstand_abschluss.json) wurden vor dem neuen Vollprüflauf gehasht und in einem vollständig nachgeprüften ZIP außerhalb der Projektwurzel gesichert; [Sicherungsbeleg](sicherung_abschluss.json). Frühere Quell-/Vorläufe werden nicht überschrieben. Rohlogs, genaue lokale Sicherungsorte und Testorchestrierung bleiben lokal.

Keine neue Lieferung nach 07, kein Paketbau, keine Signatur oder Veröffentlichung. Native Mac-/Linux-/Reader- und physische DPI-/Mehrmonitorabnahme bleiben offen. Allgemeine WA-09-Zukunftsfeldtoleranz ist vom gezielt belegten Seitenkarten-Namespace getrennt.

Wiederholung aus `01_Repository/Glide`, mit temporärem `GLIDE_DATA_DIR` und `PYTHONUTF8=1`:

```text
python -B tests/integration/test_markdownbaum.py --report <neue Ergebnisdatei>
python -B tests/integration/test_seitenkarten.py --report <neue Ergebnisdatei>
python -B tests/tools/pruefen.py --modus voll --protokoll tests/qa-3.43.1/<neuer Lauf> --timeout 900
python -B tests/tools/ci_grundstufe.py --protokoll <neuer CI-Ordner> --timeout 900
```

Alle GUI-Suiten laufen seriell. `--fall` wählt einen gezielten Fall; `--app` ermöglicht die App-Adapter-Gegenprobe. Keine echten Nutzerdaten werden in den Prüfungen geöffnet.
