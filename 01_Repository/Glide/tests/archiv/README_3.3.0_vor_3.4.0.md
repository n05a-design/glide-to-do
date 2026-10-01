# Tests für Glide

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10.

Der gemeinsame Einstieg ist `python tests/tools/pruefen.py --modus schnell`.
Für Reproduktion der Beispiel-/Releasedaten und mögliche Linux-/Windows-Bilder:
`python tests/tools/pruefen.py --modus voll --protokoll PFAD`.
Voraussetzungen, Exitcodes und Grenzen beschreibt `tests/tools/README.md`.

Alle drei Suiten bleiben eigenständige, linear geschriebene Python-Skripte:

| Suite | Prüft |
|---|---|
| `integration/test_glide.py` | Kernverhalten, Versionen, alte Referenzformate, Backup/Import, Pfadsicherheit, Oberflächenzustände, Labels und Beispiel-/Release-Fixtures |
| `integration/test_datenintegritaet.py` | Bestandswächter, Gruppenauflösung in 130 Kombinationen, Papierkorb, Drag & Drop, Listenwechsel und Mehrfachauswahl |
| `integration/audit_app.py` | App-weiter Durchlauf und gesammelte Befunde; ein Befund führt zum Fehlerstatus |

Einzelaufrufe unter Windows/macOS mit Python 3.12 und funktionierendem Tk:

```
python tests/integration/test_glide.py
python tests/integration/test_datenintegritaet.py
python tests/integration/audit_app.py
```

Unter Linux ohne laufende grafische Sitzung jedem Einzelaufruf `xvfb-run -a`
voranstellen. Die Suiten setzen `GLIDE_DATA_DIR` vor dem App-Import auf isolierte
Testverzeichnisse; `%APPDATA%` allein genügt dafür nicht plattformübergreifend.
Native Testfenster können während der Prüfung kurz sichtbar sein.

Die Datenintegritätssuite verarbeitet vor koordinatenabhängigen Mausprüfungen
das native Fenstermapping. Unter Windows reicht `update_idletasks()` alleine
dafür nicht. Die Inhalts- und Datenverlustprüfungen gelten unverändert.

Automatisierte Tk-Prüfungen ersetzen weder längere Bedienung noch eine
Sichtprüfung auf Windows und macOS. Bei Layoutänderungen Bilder erzeugen und
tatsächlich ansehen; verbleibende Plattformprüfungen im QA-Bericht nennen.

Die bestehenden Suiten lassen temporäre Diagnosebestände nach einzelnen Läufen
liegen. Diese liegen außerhalb echter Nutzerdaten und können zur Fehlersuche
herangezogen werden. Das neue Prüfskript beseitigt keine bestehenden Dateien.
