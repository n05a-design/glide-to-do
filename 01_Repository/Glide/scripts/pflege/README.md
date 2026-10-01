# Pflegewerkzeuge

Stand 01.10.2026 · Glide 3.33.1 · Aufgabenformat 20

Werkzeuge für jede Arbeitsrunde und für Messungen. Sie löschen nichts; jede
überschriebene Datei liegt vorher im benachbarten Archiv.

| Werkzeug | Wozu | Aufruf |
|---|---|---|
| [versionswechsel.py](versionswechsel.py) | Hebt die Version: `VERSION`, `APP_VERSION`, Versionsprüfungen der Tests, Beispieldaten, Rundgang, Showcase, Vorlagenkatalog, neue Releaseplanung und die Standangaben aller fortgeschriebenen Dokumente (mit Archivkopien `_<alt>_vor_<neu>`) | `python3 scripts/pflege/versionswechsel.py 3.33.0 01.10.2026` |
| [showcase_abgleich.py](showcase_abgleich.py) | Prüft den aktiven Showcase über tatsächlichen Import/Neustart und kopiert Basis, Vorlagen, Anleitung und Starter nach `05_Probelisten_Testdaten/Showcase`; Archivkopien, SHA-256, kein Eingriff in den bearbeiteten Arbeitsstand | `python3 -B scripts/pflege/showcase_abgleich.py` |
| [abgleich_07.py](abgleich_07.py) | Spielt den Stand aus `src/glide` nach `07_Python-Versionen` und prüft SHA-256 | `python3 scripts/pflege/abgleich_07.py` |
| [messung_ansichtswechsel.py](messung_ansichtswechsel.py) | Misst jeden Ansichtswechsel (Median in ms) und zeigt die teuersten Funktionen (cProfile) | siehe Kopf der Datei |
| [messung_performance.py](messung_performance.py) | Unprofilierter Vorher-/Nachher-Vergleich mit festen Aufgaben-, Notiz- und Bildseiteninhalten; erste/warme Wechsel, Median/p95 und Rohwerte | `python3 -B scripts/pflege/messung_performance.py --items 1000 --json <Ausgabe>`; `--app` für gesicherten Vergleichsstand |
| [analyse_codebasis.py](analyse_codebasis.py) | Größte Klassen und Funktionen, wiederholte Texte, identische Funktionen, häufige Aufrufe | `python3 scripts/pflege/analyse_codebasis.py` |
| [messung_speicherweg.py](messung_speicherweg.py) | Unprofilierter Vergleich des Speicherwegs bei wachsendem Bestand (P08, T2): erstes Speichern, Undo-Schnappschuss, `save_items`, Verlaufsvergleich, JSON, Abhaken über `item_change`; Aufwärmlauf, Median/p95, Rohwerte; `--profil` für cProfile | `python3 -B scripts/pflege/messung_speicherweg.py --items 10000 --json <Ausgabe>`; `--app` für gesicherten Vergleichsstand |

**Reihenfolge einer Produktionsrunde** (Dokumentations-/Werkzeugnachlauf nach [Arbeitsrichtung](../../docs/ARBEITSRICHTUNG.md)):

1. Vor der Änderung den startbaren Stand als Ordner in
   `07_Python-Versionen/Archiv` sichern.
2. Umsetzen und Einzelsuiten ausführen.
3. `versionswechsel.py`, danach von Hand die CHANGELOG-Überschrift und den
   Vertrag.
4. Vollprüfung: `python3 -B tests/tools/pruefen.py --modus voll --protokoll
   tests/qa-<Version>/<Name> --timeout 900` (unter macOS im Hintergrund).
5. `abgleich_07.py` und `python3 packaging/macos/baue_app.py --ziel build/macos`.
6. QA-Bericht, `qa-verlauf.md`, Index und Übergabe nachführen.

Erst nach Schritt 5 trägt die Glide-Fassung des Inhabers den Stand.

Seit 3.32.3 ergänzt die Pflichtsuite `tests/integration/test_library_performance3323.py --app <Quelle> --items 1000 --rounds 8 --measure <JSON>` die Messung um erneute Bibliotheksaktualisierungen innerhalb derselben Ansicht und neue Karten-/Aktionscontainer. Ein separater Aufwärmdurchlauf und Rohwerte bleiben im JSON; Dateischreiben und Ansichtswechsel sind andere Messgrößen. [Vertrag 71](../../docs/71_KARTEN_PERFORMANCE_3.32.3.md).

`versionswechsel.py` pflegt Standzeilen und Fixtures, keine semantischen Aufgabenstatus. Titel, erste Prüfaufrufe, beantwortete Entscheidungen und nächste Schritte zusätzlich abgleichen. Für Werkzeugnachläufe `python3 -B tests/tools/test_standpruefung.py`, Syntax/Version/Stand/Index/Links und unveränderte App-/Paket-Hashes prüfen; den früheren Volllauf nicht überschreiben.

Nach einem Versionswechsel den neu erzeugten Showcase nach der Vollprüfung mit `showcase_abgleich.py` ausliefern. Bilderquellen und Funktionsabdeckung stehen im [Showcase-Vertrag](../../docs/72_SHOWCASE_3.32.3.md). Kein Neubau unveränderter Laufzeitfassungen für einen reinen Datennachlauf.
