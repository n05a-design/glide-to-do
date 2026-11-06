# Übernahmeinventar Mac/PC-01 → Git – Glide 3.50.5

Stand 06.11.2026, 11:42 MEZ · Aufgabenformat 26 · Plan §21.72 · D64

**Auftrag 06.11.2026:** „Bitte nicht vergessen, dass die Ergänzungen von der MacOS Version auch essenziell sind und geprüft werden muss, welche Änderungen in die aktuelle Version mit übernommen werden müssen, diese dürfen nicht vernachlässigt werden.“ Zusammengeführt wird nach D64 erst nach dem Mac-Gesamtlauf; dieses Inventar hält **jetzt** fest, was dabei übernommen werden muss. Es ist eine Momentaufnahme: Mac und PC-01 schreiben weiter in die OneDrive-Ablage. Vor der Zusammenführung mit `dreiweg.py` neu erzeugen und mit dieser Liste abgleichen; nichts aus dieser Liste darf ohne Begründung entfallen.

## Verglichene Stände

| Seite | Stand |
|---|---|
| Basis | Git-Commit `40c20fd6` (Ausgangspunkt der OneDrive-Ablage) |
| Ablage | OneDrive-Projektordner, App `f3afb8fe…`: PC-01-Titelstand `246c6c3b…` plus Mac-Callback-Korrektur; Mac-Gesamtlauf darauf seit 10:09 aktiv |
| Git | Zweig `claude/macos-vollprufung-app-paket-6054fc` auf `main` `5e63ea34`, App `cb4a7aad…`, mit Release-Entwurf (D64) |

Dreiwegevergleich je Datei, Text zeilenendenneutral, Binär bytegenau ([Inventar](inventar.json), [Skript](dreiweg.py)): **37 nur in der Ablage geändert, 40 beidseitig, 23 nur in Git**; identische Dateien ausgelassen.

## Pflichtübernahmen aus der Ablage

**Anwendung (verändert das Verhalten, neuer Apphash nötig):**

| Änderung | Dateien | Herkunft |
|---|---|---|
| `_register_after` behält nur noch lebende Tk-Aufträge (`after info`); behebt das wachsende Callback-Register aus dem Mac-Dauerlauf | `app.pyw` | Mac, Gegenprobe `test_aufraeumen330.py --callback-register` vorher rot, nachher grün |
| Titelgrenze 40 Zeichen auch für Vorlagenimport, kopierte Einträge, Einträge aus Anhängen, Auftragsrezepte und Titelfelder (`limit_title_entry`); `edited_task_title` bewahrt unveränderte Alttitel und legt lange neue Eingaben vollständig in die Beschreibung | `app.pyw`, `ui_design.py`, `exchange_recipes.py` (`normalize_update`) | PC-01 (D63-Folge) |
| Python-Lieferung gleichziehen | `07_Python-Versionen/…v3.50.5.pyw`, `ui_design.py`, `exchange_recipes.py` | über `abgleich_07.py` |

**Tests und Prüfwerkzeuge:**

| Datei | Inhalt |
|---|---|
| `tests/integration/test_aufraeumen330.py` | Callback-Register-Gegenprobe, Galerietitelfälle |
| `tests/integration/test_template_workflows.py`, `test_auftraege.py`, `test_arbeitsmodi.py`, `test_features320.py` | Titelgrenze in Vorlagen, Aufträgen, kopierten Einträgen und Kalenderimport (39/40/41/300 Zeichen) |
| `tests/integration/test_features328.py` | reduzierte Blockleiste: Überschriften/Code weiter über „Umwandeln in“ im Kontextmenü |
| `tests/unit/test_ui_design.py`, `tests/unit/test_exchange_recipes.py` | `edited_task_title`, `normalize_update` |
| `tests/tools/dauerlauf.py` | misst zusätzlich echte offene Tk-Aufträge |
| `tests/tools/pruefablauf.py`, `test_pruefablauf.py` | Einfrieren mit `--no-hardlinks` (Prüfablage auf anderem Laufwerk) |
| `tests/tools/symbolpruefung.py` | prüft die freigegebene statt nur die eingestellte Symbolschrift |
| `packaging/macos/baue_app.py` | Bauanleitung auf `build/macos-vorstufe` (AST unverändert) |

**Belege (unverändert übernehmen, nicht umetikettieren):** `tests/qa-3.50.5/mac_2026-11-06/` (16 Dateien, einschließlich der ursprünglichen Rotläufe) und fünf PC-01-Belege vom 06.11. in `tests/qa-3.50.5/abnahme_2026-11-05/`.

**Dokumente (beidseitig geändert, inhaltlich zusammenführen):** Übergabe, Entwicklungsplan (Ablage §21.70 Mac und §21.71 PC-01 werden §21.73/§21.74, weil Git §21.70 Konkurrenzanalyse und §21.71 GitHub-Seite trägt; Git §21.72 Release), Analyse, manuelle Prüfung, QA-Bericht, CHANGELOG, Funktionen, Architektur, Prüfplan, Datenvertrag, Veröffentlichung, Arbeitsrichtung (Git D64), Design Richtlinien, READMEs, `CLAUDE.md`, `.gitignore`.

## Konflikte: beide Seiten haben dieselbe Stelle geändert

| Datei | Ablage | Git | Auflösung |
|---|---|---|---|
| `app.pyw` Bildfolgenexport | eigenes Popup `animation_export_menu` | Untermenü „Bildfolge exportieren“ (Produktbefund 3.50.3, `test_fenster330`/`test_animation3400`) | Git-Fassung behalten, Popup-Methode nicht übernehmen |
| `app.pyw` Kopfknöpfe bei Enge | Andocken an `tool_band_inner` | Andocken an `tool_band` mit fester Oberkante (Produktbefund Windows, `test_festlayout330`) | Git-Fassung behalten |
| `test_features321.py` | Titeltest mit vollständigem Parsergebnis | 40-Zeichen-Erwartung | beide Prüfungen vereinen |
| `test_features323.py` | Leserichtung je Packseite (`links_von`) | Packseite und rechter Löschknopf | beide Prüfungen vereinen |
| `test_uiux_paket.py` | eigener B16-Bildscrollweg | B16 synchronisiert auf fertige Bildanker (PR #62) | Git-Fassung als Grundlage, Ablageergänzung nur nach Einzelprüfung |
| `test_aufgaben3380.py` | Basisfassung | Langtext als Altdatenfall | Git-Fassung |

**Nur in Git und in der Ablage fehlend** (darf beim Zusammenführen nicht verloren gehen): `test_features330.py`, `test_kartenfuss330.py` (Erwartungen nach 3.50.3/D63), ci254-Belege, `linux_gegenproben.py`, Release-/Paketworkflows samt Tests. **Hinweis für den laufenden Mac-Gesamtlauf:** Weil der Ablage die Git-Anpassungen in `test_features330` und `test_kartenfuss330` fehlen, kann er dort an veralteten Erwartungen stoppen. Ein solcher Stopp wäre kein Produktbefund.

## Nicht übernehmen

- `20_Grafik_Master/01_Logo/Archiv/…/* 2.*` (sechs Dateien): Synchronisationskopien mit Leerzeichen-Ziffer-Namen, während die Originalnamen in der Ablage fehlen. Git trägt die Originale; vor dem Zusammenführen bytegleich vergleichen und in der Ablage bereinigen.
- `20_Grafik_Master/01_Logo/_verification_temp`: Prüfrest, in Git ausgeschlossen.
- `tests/qa-3.48.0/lokale_belege/…`: außerhalb der Aufbewahrung, in Git gekürzt.

## Nach der Zusammenführung

Der zusammengeführte Stand wird nach D65 sofort **3.50.6**: `versionswechsel.py 3.50.6`, zusammenfassender CHANGELOG-Abschnitt, einheitliche Dokumentstände, `abgleich_07.py`, Showcase, Ablage kürzen. Den 3.50.6-Apphash festhalten; Vollmatrix in GitHub sowie Mac-Volllauf, Dauerlauf und Paketbau auf genau diesem Stand, danach Tag `v3.50.6`. Erfolge auf `a4bfe4ed…` oder `f3afb8fe…` bleiben diesen Ständen zugeordnet und gelten nicht für den gemeinsamen Stand.

## Stand bei Übergabe von PC-02 (06.11.2026, 12:30 MEZ)

Der Mac-Gesamtlauf auf `f3afb8fe…` (gestartet 10:09) hatte bei Sitzungsende auf PC-02 noch kein Ergebnis in den Nachweis `tests/qa-3.50.5/mac_2026-11-06/` geschrieben. Die Rohdaten liegen bis zum Abschluss nur lokal auf dem Mac (`~/gq/mac3505-20261106/final3/`). Geschätzte Dauer nach früheren M2-Läufen vier bis fünf Stunden. Fortsetzung auf PC-01 oder Mac: Nachweis lesen, dann Übergabe §3 Schritte 5–7 (Zusammenführung nach diesem Inventar, 3.50.6 mit Abschlussaudit, Release-Entwurf). Die OneDrive-Ablage selbst ist bewusst noch nicht in Git zusammengeführt (D64); sie bleibt über OneDrive auf allen Geräten verfügbar.

**Merge-Plan für die Abschlusssitzung (geprüft 06.11.2026, 13:00, PC-02, per `git merge-tree` simuliert):**
- **Zweig 1 – `claude/macos-vollprufung-app-paket-6054fc` → `main`: zuerst, sofort möglich.** Enthält Release-Entwurf (D64/D65), Übernahmeinventar und bereits **beide** Konkurrenzstände (PR #65 und Nachtrag `5dca26ca`); konfliktfrei gegen `main`. PR anlegen, Vollmatrix grün abwarten, mergen. Damit ist `claude/docs-competitor-analysis-review-aa9f90` vollständig enthalten und wird **nicht** separat gemergt, sondern nach dem Merge geschlossen/gelöscht.
- **Zweig 2 – OneDrive-Ablage (Mac/PC-01) → neuer Zweig → `main`: erst nach dem Mac-Gesamtlauf (D64)** und auf dem Stand von `main` nach Zweig 1. Vorgehen nach dem Übernahmeinventar (`dreiweg.py` neu laufen lassen, Basis `40c20fd6`). Plan-Abschnitte der Ablage §21.70 (Mac) und §21.71 (PC-01) werden §21.73/§21.74, weil `main` §21.70–§21.72 trägt. Danach sofort 3.50.6 (D65).
- **`codex/glide-3.50.5-titel-nachtrag` (`8566fb0e`): nicht direkt mergen.** Er enthält die PC-01-Titelgrenze als Git-Commit, also denselben Inhalt wie die Ablage, und kollidiert nach Zweig 1 in Plan, Übergabe, QA-Bericht und `tests/tools/README.md`. In Zweig 2 als Quelle für Code und Tests nutzen (Dateien mit der Ablage vergleichen), danach schließen.
- **`codex/glide-3.50-timeoutdiagnose-20261102`:** zwei nicht übernommene Diagnose-Commits vom 02.11. (`a8bdd199`, `8ad342ac`, temporäre Linux-Reproduktion); bewusst nicht mergen, Löschen ist Inhaberentscheidung. Alle anderen Remote-Zweige sind vollständig in `main`.
- **Regel:** Immer nur einen Zweig zur Zeit mergen; danach die übrigen mit `main` aktualisieren. Maßgeblich ist der grüne Lauf nach dem Merge auf `main`, nicht der Lauf auf dem Zweig. Kein Tag vor Zweig 2 und 3.50.6.
