# Vertiefte Codebasisprüfung – lokaler Techniknachlauf 3.45.0

Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Python 3.15.1 / Windows / Tk 9.0.4

Eingang des Inhabers: „Glide 3.45.0 – Vertiefte Codebasisprüfung“, anschließend „bitte verarbeiten und in die lokale Dokumentation und App einarbeiten“. Einordnung ausschließlich in [Analyse §13.15](../../../../../00_Arbeitsvorbereitung/Glide_Analyse.md#1315-vertiefte-codebasisprüfung-vom-26102026), Aufgaben und Restumfang ausschließlich im [Plan §21.21](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2121-vertiefte-codebasisprüfung-und-technikpaket). Diese Datei hält die ausgeführten Nachweise, keinen zweiten Arbeitsplan.

## Basis und Änderungen

Basis `089ae83`, App `d516ca67…`, geprüfter Lieferabschluss mit 86 Laufzeitdateien. Der unveränderte vollständige Kompaktfall und Speicherergebnisfall sind grün: [Kompaktbaseline](kompakt_baseline.json), [Speicherbaseline](speicher_baseline.json). Vor Produktionsänderungen außerdem zehn Vergleichs- und 16 Konvertertests grün. Nutzerdaten waren über temporäre `GLIDE_DATA_DIR` isoliert.

Neuer Tk-freier Koordinator `persistence.py`: explizite Operationen, ein Schreibaufruf, unveränderter `SaveResult`-/Bool-Vertrag; UI, Besitz-/Wächterprüfung und vorhandene Migration/Dateifunktionen bleiben im Adapter. Vergleichsfunktionen sind lesend; Abschlusszeitübernahme heißt ausdrücklich `prepare_save_comparison`. Kürzelzustand hat einen Tk-freien Übergang und Rücksetzung beim Modifierende/Hauptfensterfokusverlust. Konverterdiagnose hält höchstens 16 Fehlerklassen mit begrenzten Zählern; Hauptthread protokolliert neue Klassen ohne Pfad/Fehlertext/Auftragsschlüssel/Traceback und ohne erneuten Eintrag derselben gehaltenen Klasse. Erwartete negative Ergebnisse und Abbrüche bleiben ruhig.

[Prüfskript](pruefung.py) und [JSON mit AST-Inventar, Quellmanifest, Rohmessungen und Fachtests](pruefung.json) sind reproduzierbar. Basismethoden/-zeilen stimmen mit dem Revieweingang überein: 65.371 Hauptdateizeilen, 3.064 Funktionen, `ListApp` 49.887 Zeilen/1.742 direkte Methoden. Kandidat: 65.373/3.070 bzw. 49.888/1.744; 87 eigene Laufzeitdateien, plus Prototyp und zwei vendierte Pythondateien insgesamt 90. Hauptdateianteil an diesen Quelldateibytes rund 81,5 %. Der kleine Koordinator verkleinert `ListApp` noch nicht.

Das AST-Inventar zählt 2.546 unterschiedliche `self`-Attributnamen in der Basis, 496 Attribute mit Store-Kontext und 468 einfache direkte `Assign`-Ziele. Das sind verschiedene Zählregeln, keine unabhängigen Variablen; Methoden/Konstanten sind im Namensinventar enthalten. Der Bericht nennt dafür etwa 2.542/492 ohne ausführbares Zählskript. Die Zahlen werden mit ihren Definitionen erhalten, nicht still gleichgesetzt. Statische Aufrufstellen sind keine Laufzeitmessungen.

## Ausgeführte Prüfung

| Prüfung | Ergebnis / Nachweis |
|---|---|
| Sechs betroffene Fachsuiten | 58/58 grün, keine übersprungenen Fälle; Koordinator-/Commitfehler, SaveResult, Vergleich, Teilvergleich, Kürzelzustand und Konversion. Syntax aller 87 Laufzeitdateien grün; [JSON](pruefung.json) |
| Semantischer Vergleich gegen den eingefrorenen alten Code | 240 Fälle mit gleichen Aufgaben-JSONbytes, Verlaufswerten und Prüfsummen, einschließlich Scope, neuer Kindpunkte, doppelter Listen-IDs, Gruppen, alter Abschlüsse und Wiederöffnen; [Skript](pruefung.py) |
| Schutzrunde, echte Appwege | 16/16 grün, einschließlich realer Prozesse, Schreibbesitz, Guard-Rückweg/Originalbytes, Editorübernahme, ein Undo, Speicher-/Settings-/Folgefehler; [JSON](schutzrunde.json) |
| Speicherstatus, echte Appwege | 4/4 grün: Autosave/Retry, Nebendateien, Größenlimit/Originalerhalt, Sicherungsreserve/Import; [JSON](speicherstatus.json) |
| Bestehender Speichervergleich | `python -B tests/integration/test_speichervergleich3339.py` Exitcode 0: Vergleich, Unterbäume, Undo, Schreibfehler/Retry, `record_activity=False`, Reload. Dieser Lauf hat keinen zusätzlichen Git-Differenzialmodus aktiviert; die 240 Gegenfälle stehen getrennt oben |
| Bildkonversion | 11/11 grün, einschließlich bestehender Renderwege/Abbruch/Generation/Retry/Queue und neuer Hauptthread-/Datensparsamkeits-/Deduplizierungsprobe; [JSON](bildkonversion.json) |
| Fehlendes K-Loslassen | Unveränderte gelieferte App bewusst rot: Flag bleibt nach Strg-Loslassen gesetzt. [Alte Gegenprobe](kompakt_regression_alt.json). Gleicher Fall im Kandidaten grün; interner Fokuswechsel erhält das Paar, Hauptfensterfokusverlust setzt zurück. [Korrektur](kompakt_regression_neu.json) |
| Bestehender Kompaktfall | Grün; vollständiges Ereignispaar, reiner Release-Ersatz, Editor-/Hauptfensterweg, falsche Modifier, Menü, getrennte Fensterlagen/Neustart und 26 B07/B15-Knopfprüfungen; [JSON samt Ereignisspur](kompakt.json) |
| Kompaktansichten | Grün; 112 Knopfprüfungen bei 480 × 560/großer Schrift in Liste, Heute, Seite und Startseite, Menü vollständig; [JSON](kompakt_ansichten.json) |

Die Ereignisspur enthält synthetische Eingänge, tatsächlich empfangenen Ereignistyp, Modifierbits, Ereigniszeit, Modus, Merker, Mindestmaß und Fokus vor/nach dem Ereignis, ohne Textinhalte. Sie wird auch bei einer roten Prüfung gespeichert. Die vorher kombinierte Assertion von Modus und Mindestmaß ist getrennt. Damit ist ein künftiger Linuxfall genauer auswertbar. **Die lokale fehlende-Release-Gegenprobe beweist nicht die Ursache des historischen Linux-/Tk-9.1-CI-Fehlers.** Linux, Tk 9.1 und X11-Autorepeat wurden hier nicht ausgeführt.

## Begrenzte Teilmessung

Nur Abschlusszeitübernahme und Vergleich, vollständiger Scope mit künstlichen flachen Aufgaben; sieben abwechselnd angeordnete Messpaare je Größe, frische Datenkopien außerhalb des Zeitfensters. Median und empirisches p95 (bei sieben Werten der größte Wert) in Millisekunden:

| Aufgaben | Vorher Median / p95 | Nachher Median / p95 |
|---|---:|---:|
| 100 | 0,76 / 0,89 | 0,58 / 0,65 |
| 1.000 | 5,71 / 8,69 | 5,79 / 7,10 |
| 5.000 | 28,73 / 37,86 | 30,29 / 46,96 |
| 10.000 | 56,37 / 67,37 | 57,03 / 66,83 |

Die neue explizite Zeitstempelübernahme liest betroffene Bäume einmal zusätzlich ohne erneute JSON-Kodierung der Teilbäume. Diese kleine Messung zeigt keinen allgemeinen Geschwindigkeitsgewinn und keine belastbare p95-Verbesserung. Sie enthält keinen echten Gesamtmutations-, JSON-Schreib-, Backup-, Refresh- oder Ereignisnachlauf. Das vorhandene Ende-zu-Ende-Profil und WA-36 bleiben maßgeblich.

## Abschlussgrenze

Lokaler Quellkandidat 3.45.0 / Format 26; sechs Laufzeitunterschiede zum abgeschlossenen Lieferstand: `app.pyw`, `compact_mode.py`, `save_comparison.py`, `image_conversion.py`, `image_preview.py` und neu `persistence.py`. Quellhashes stehen im Manifest des JSON-Nachweises. Kopier-/Baulisten und Modulübersichten sind ergänzt, die Lieferung wurde nicht überschrieben. Keine neue Vollmatrix, kein 07-Abgleich, Paketbau, Versionswechsel oder Git-Schreibaktion. Vorherige breite/nativ geprüfte Lieferungen bleiben bei ihren ursprünglichen Bytes; Linux-/Mac-/Reader-/DPI-/Mehrmonitor- und Menschenabnahme bleiben gesondert offen. Quellen-/Dokumentationsabschluss und Linkprüfung stehen im [Abschlussabgleich](abschluss.json).
