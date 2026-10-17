# FP-01 Wiederholen nach Rückgängig – Kandidat 17.10.2026

Stand 17.10.2026 · Kandidat auf Glide 3.43.1 (keine Lieferung, keine neue Version) · Datenformat 25 · Windows 11 Pro, Python 3.14.7, Tk 9.0.4, künstliche Daten

Durch D49 beauftragt (E-W1 A/V), begonnen auf Anweisung des Inhabers vom 17.10.2026. Umgesetzt auf `claude/fp01-wiederholen` ab `main` `8eeff81`. Abnahmekriterien und Tests nach [Entwicklungsplan, FP-01](../../../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#fp-01-wiederholen-nach-rückgängig-wa-01). Die Lieferung als eigene Version steht aus; bis dahin tragen `07_Python-Versionen` und das Bundle 3.43.1.

## Umfang

- **Stufe 1:** Wiederholen für alle Wege über den Rückgängig-Stapel; Bearbeiten › Wiederholen (Kennung `redo_last_change`), Befehlspalette, Überlaufmenü der Kopfzeile, Strg/Cmd+Umschalt+Z, unter Windows zusätzlich Strg+Y; nach „Rückgängig“ im Hinweis bietet derselbe Hinweis „Wiederholen“; Textfelder und Zeichenfläche behalten ihre Stapel. Kürzelübersicht und Handbuch nennen den Weg.
- **Stufe 2:** Flächenänderungen der Pinnwand (Aufräumen, Bereiche) lassen sich wiederholen; der Änderungsverlauf verweist mit „Sicherungen vergleichen …“ auf ältere Stände.
- **Technik:** Tk-freies `undo_history.py` mit Gültigkeitsregel (Tiefe und oberstes Objekt des Rückgängig-Stapels, Schreibzähler aus `save_items`) statt Eingriffen an den rund 30 Rücknahmestellen; `ListApp` bleibt Adapter (D17). Grenze 20 wie beim Rückgängig, nur im Arbeitsspeicher.
- **Abweichung vom Entwurf:** Der Sicherheitspunkt des Autospeicherns ohne ausstehende Änderung zählt nicht als Schreibvorgang; sonst verfiele Wiederholen nach wenigen Minuten ohne jede Änderung. Jede andere gespeicherte Änderung, auch ein Zustellbeleg, verwirft die Schritte.
- **Verhaltensänderung:** Scheitert beim Rückgängig das Speichern, bleiben Bestand und Stapel wie vorher. Bisher nahm Rückgängig den Bestand dann nur im Arbeitsspeicher zurück (rote Gegenprobe im Fall `schreibfehler`).

## Prüfung

| Prüfung | Ergebnis |
|---|---|
| Unit `tests/unit/test_undo_history.py` | 12/12 grün; alle Units 726/726, Werkzeugtests 152/152 |
| Pflichtsuite `tests/integration/test_wiederholen.py` | 9/9 grün ([Bericht](pflichtsuite.json)) |
| Rote Gegenprobe gegen 3.43.1 (`main` `8eeff81`) | 9/9 rot mit dem Ursprungsmangel ([Bericht](gegenprobe.json)) |
| Berührte Bestandssuiten | 57 Suiten, die Rückgängig, Hinweis, Aktionsliste, Menü oder Verlauf berühren: 55 im ersten Lauf grün. `test_wissen3340` ersetzte `show_undo_toast` durch eine Attrappe ohne den neuen Parameter – behoben mit eigener Methode `show_redo_toast`, Signatur unverändert, danach grün. `test_features330` verlangte, dass der Hinweis nach „Rückgängig“ verschwindet; FP-01 lässt ihn „Wiederholen“ anbieten, Zusicherung an den Vertrag angepasst. Dieselbe Suite scheitert auf diesem Rechner unabhängig davon in Zeile 308 (Zoom der Zeichenfläche), auch an `main` `8eeff81` in 2/2 Läufen; eine Diagnosekopie ohne diese eine Zusicherung läuft vollständig grün. Nach dem Umbau des Hinweises die fünf Hinweis-Suiten erneut: 5/5 grün ([Zusammenfassung](ergebnis.json)) |
| Abhaken bei 5.000 Punkten (§10, `messung_speicherweg.py --items 5000 --lokale-punktmutation`, abwechselnd) | Kandidat 126 / 110 ms, 3.43.1 111 / 119 ms (Median); kein Unterschied über der Streuung, beide auf diesem Rechner um das Ziel 120 ms |
| Zusatzspeicher bei 10.000 Punkten | 405 KiB je Wiederholen-Schritt, höchstens 20 Schritte = 7,9 MiB |
| Standprüfung, Dokumentlinks, Linux-Gegenprobenanker | grün; alle 18 Anker vorhanden |
| CI-Grundstufe Windows | bestanden (Exit 0): Syntax, Versionen 3.43.1/Format 25, Dokumentation, Fixtures, 152 Werkzeugtests, 726 Units auch ohne Systemzeitzonen, fünf Analysen, Startprobe, Fremdcode, Datenschutz, Ablagegröße, Synchronisation; Lieferstand als zulässiger Hinweis (Hauptdatei, `action_catalog.py`, `undo_history.py` noch nicht in 07) ([Protokoll](grundstufe.json)) |

Fälle der Pflichtsuite: `matrix` (anlegen, löschen, verschieben, einrücken, gruppieren, abhaken mit Wiederholung, einplanen, entlasten, importieren; je Rückgängig und genau ein Wiederholen, gespeicherter Bestand bytegleich; drei Schritte in Folge), `gueltigkeit` (wirkungslose Aktion behält, Autospeichern ohne/mit ausstehender Änderung, neue Änderung, Zustellbeleg, Wächterabbruch, Neustart, Laden eines anderen Datenordners), `schreibfehler` (Rückgängig und Wiederholen je einmal gescheitert, danach gelungen), `fokusbuchung`, `editoren` (Textfeld, Zeichenfläche), `pinnwand` (Fläche, neue Fläche verwirft, gemischte Folge mit Punktänderung), `bedienwege` (Menü, Palette, Kürzelbeschriftung, Hinweis, Überlaufmenü), `verlauf`, `messung` (Grenze 20, Zusatzspeicher).

## Offen

- Lieferung: Versionswechsel, eingefrorene Vollprüfung, GitHub-Matrix, `abgleich_07.py`, Mac-Bundle – mit der Lieferung.
- Native Tastenwege unter macOS (Cmd+Umschalt+Z) und Linux/X11 mit Tk 9.1: erst die GitHub-Matrix und der Referenz-Mac belegen sie.
- Menschenabnahme nach der [Prüfliste](../../../../../00_Arbeitsvorbereitung/Glide_Manuelle_Pruefung.md#wiederholen-nach-rückgängig-fp-01-in-arbeit).
