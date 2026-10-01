# Pflegewerkzeuge

Stand 30.09.2026 · Glide 3.32.0 · Aufgabenformat 20

Werkzeuge für jede Arbeitsrunde und für Messungen. Sie löschen nichts; jede
überschriebene Datei liegt vorher im benachbarten Archiv.

| Werkzeug | Wozu | Aufruf |
|---|---|---|
| [versionswechsel.py](versionswechsel.py) | Hebt die Version: `VERSION`, `APP_VERSION`, Versionsprüfungen der Tests, Beispieldaten, Rundgang, Vorlagenkatalog, neue Releaseplanung und die Standangaben aller fortgeschriebenen Dokumente (mit Archivkopien `_<alt>_vor_<neu>`) | `python3 scripts/pflege/versionswechsel.py 3.33.0 01.10.2026` |
| [abgleich_07.py](abgleich_07.py) | Spielt den Stand aus `src/glide` nach `07_Python-Versionen` und prüft SHA-256 | `python3 scripts/pflege/abgleich_07.py` |
| [messung_ansichtswechsel.py](messung_ansichtswechsel.py) | Misst jeden Ansichtswechsel (Median in ms) und zeigt die teuersten Funktionen (cProfile) | siehe Kopf der Datei |
| [analyse_codebasis.py](analyse_codebasis.py) | Größte Klassen und Funktionen, wiederholte Texte, identische Funktionen, häufige Aufrufe | `python3 scripts/pflege/analyse_codebasis.py` |

**Reihenfolge einer Runde:**

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
