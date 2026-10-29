"""Gezielte, nachpruefbare Korrekturen bestehender Dokumente; keine Appmutation."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
changes = []


def change(name, old, new):
    path = ROOT / name
    text = path.read_text(encoding='utf-8')
    if new in text:
        return
    assert text.count(old) == 1, (name, text.count(old), old[:90])
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    path.write_text(text.replace(old, new), encoding='utf-8')
    changes.append(dict(path=name, before_sha256=before,
        after_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), old=old, new=new))


change('01_Repository/Glide/tests/qa-3.48.0/last_fenster_2026-10-27/README.md',
    'B760M-DS3H-DD3H-DDR4-rev-1x', 'B760M-DS3H-DDR4-rev-1x')
change('01_Repository/Glide/packaging/README.md',
    '**Aktueller Quellkandidat 3.47.0:** Mehrfachplanung und Nebenansichtsverlauf ergänzen Tagessteuerung/Suche und die vorherigen Technik-/Startseitenpakete. Kopier-/Baulisten enthalten alle 88 Laufzeitdateien, auch `persistence.py` und `home_task_tiles.py`. Die bestehenden Windows-/Mac-Pakete bleiben beim eingefrorenen 3.45.0-Abschluss `d516ca67…`; neue Funktionen oder eine Versionszeile ersetzen keinen Paketneubau. [Gemeinsamer Quell-/Prüf-/Lieferstand](../tests/qa-3.46.0/zweierpaket_2026-10-27/README.md).',
    '**Aktueller Quellkandidat 3.48.0:** Tagesnavigation, gemeinsame Wichtigkeit/Labels und Verweisnavigation ergänzen die bisherigen Tages-/Nebenansichtspakete. Kopier-/Baulisten enthalten alle 88 Laufzeitdateien, auch `persistence.py` und `home_task_tiles.py`. Python-Lieferung 3.47.0; Windows-/Mac-Pakete bleiben beim eingefrorenen 3.45.0-Abschluss `d516ca67…`. WA-41 und Lieferabschluss sind offen; neue Funktionen oder eine Versionszeile ersetzen keinen Paketneubau. [Aktueller Quell-/Prüf-/Lieferstand](../tests/qa-3.48.0/dreierpaket_2026-10-27/README.md).')
change('01_Repository/Glide/tests/README.md',
    'Aktuell 3.47.0: `test_arbeitsmodi.py` enthält 22 echte Bedien-/Geometriefälle, einschließlich seitenübergreifender Tagesauswahl, gemeinsamer Planung und Nebenansichtsverlauf. 13 neue reine Auswahl-/Verlaufstests ergänzen die Home-/Side-Gruppen; Quellmanifest, eingefrorener Lauf und gezielte Erwartungskorrektur stehen im [Nachweis](qa-3.47.0/folgepakete_2026-10-27/README.md). Die 104 registrierten Suiten sind weiterhin kein neuer bestandener Volllauf.',
    'Aktuell 3.48.0: `test_arbeitsmodi.py` enthält 26 echte Bedien-/Geometriefälle, einschließlich Tagesnavigation, gemeinsamer Wichtigkeit/Labels und interner Verweisnavigation. `test_featurephase348.py` ergänzt die reinen Fachgrenzen. 986 Fachtests und die 26 Arbeitsmodifälle sind grün; der breite Windows-Lauf bleibt wegen WA-41 ohne grünen Gesamtabschluss ([Nachweis](qa-3.48.0/dreierpaket_2026-10-27/README.md)). Python-Lieferung 3.47.0, native Pakete 3.45.0. [Datei-/Dokumentaudit](qa-3.48.0/dokumentationsaudit_2026-10-27/README.md) startet keine App-/Lasttests. Vorheriger gezielter Stand 3.47.0: 22 Arbeitsmodifälle und 13 neue reine Auswahl-/Verlaufsfälle ([historischer Nachweis](qa-3.47.0/folgepakete_2026-10-27/README.md)). Die 104 registrierten Suiten sind weiterhin kein neuer bestandener Volllauf.')
change('01_Repository/Glide/tests/README.md', 'D55 (lokaler Kandidat auf 3.44.0):',
    'D55 (historischer Einführungsnachweis mit 13 Fällen; seit 3.45.0 geliefert):')
change('01_Repository/Glide/docs/05_QA_TESTPLAN.md',
    '**D55 – Arbeitsmodi und Seitenbedienung (lokaler Kandidat):** `test_arbeitsmodi.py` gehört mit zwölf Appfällen zur Pflichtmatrix:',
    '**D55 – Arbeitsmodi und Seitenbedienung (seit 3.45.0 geliefert):** Der ursprüngliche D55-Schnitt von `test_arbeitsmodi.py` gehört zur Pflichtmatrix (13 Fälle einschließlich Kontextmenünachlauf; heute 26 Fälle mit Folgepaketen):')
change('01_Repository/Glide/docs/05_QA_TESTPLAN.md',
    'Bisher nur Linux/Tk 8.6; Windows-/Mac-Lauf am nächsten Phasenende.',
    'Windows-Funktions-/Geometrienachweise liegen inzwischen vor; aktuelle Ergebnisse und offene native Mac-/Linux-/Reader-/Menschenabnahmen stehen getrennt im [QA-Bericht](07_QA_BERICHT.md).')
change('01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md',
    'Seit D55 (23.10.2026) ist jeweils Option A gewählt und als lokaler Kandidat umgesetzt',
    'Seit D55 (23.10.2026) ist jeweils Option A gewählt, seit 3.45.0 geliefert und in 3.48.0 weiter ergänzt')
change('05_Probelisten_Testdaten/README.md',
    'Die Dateien sind bytegleiche Kopien von `01_Repository/Glide/tests/fixtures/showcase` (Abgleich `scripts/pflege/showcase_abgleich.py`, SHA-256 in `manifest.json`). Git speichert gleiche Inhalte nur einmal.',
    'Die gelieferte Showcase-Basis bleibt 3.47.0; ihre Dateihashes stehen in `manifest.json`. Die Quellfixtures wurden bereits auf Kandidat 3.48.0 angehoben und sind deshalb derzeit nicht insgesamt bytegleich zur Lieferung. Der nächste freigegebene Abgleich erfolgt mit `scripts/pflege/showcase_abgleich.py`; WA-41 verhindert aktuell diesen Lieferabschluss.')
change('05_Probelisten_Testdaten/README.md', 'glide_releaseplanung_3.47.0.glidebackup', 'glide_releaseplanung_3.48.0.glidebackup')
for name in ('01_Repository/Glide/tests/fixtures/showcase/README.md', '05_Probelisten_Testdaten/Showcase/README.md'):
    change(name, 'die aktuelle Arbeitsrichtung mit D01–D50 (D49 mit Korrekturvorbehalt)',
        'die aktuelle Arbeitsrichtung mit D01–D57 (D49 mit Korrekturvorbehalt)')
change('01_Repository/Glide/tests/fixtures/showcase/README.md',
    'Stand 27.10.2026 · Glide 3.48.0 · Lieferdaten in Speicherstufe 26',
    'Stand 27.10.2026 · Glide 3.48.0 · Quellfixtures in Speicherstufe 26; Showcase-Lieferung separat 3.47.0')
change('00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md',
    'D01–D56 mit D49-Korrekturvorbehalt erhalten; neue Entscheidungen ab D57',
    'D01–D57 mit D49-Korrekturvorbehalt erhalten; neue Entscheidungen ab D58')
change('00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md',
    'D56 beauftragt die lokale Weiterentwicklung zu 3.45.0; nächste freie Entscheidungsnummer D58.',
    'D56 beauftragt die lokale Weiterentwicklung zu 3.45.0, D57 wählt Tagessteuerung und Nebenansicht; nächste freie Entscheidungsnummer D58.')
plan = (ROOT / '00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md').read_text(encoding='utf-8')
old = next(line for line in plan.splitlines() if line.startswith('| **WA-41 –'))
new = ('| **WA-41 – unerklärter Speicherlast-/Interpreterausfall (P1, Untersuchung)**; Ausgang 3.44.0, erneut unter 3.48.0 | '
    '**WA-41A:** Sporadische native Abbrüche 0xC0000005/0xC0000409, interne Cacheausführung und wechselnde Typfehler unter Python 3.14.7/3.14.8/3.15.2. '
    '**WA-41B:** Ein isolierter Vergleichsfehler nach Laden in Runde 5; konkrete abweichende Felder noch offen. '
    'Die ursprüngliche Suite behält 26.420 Punkte/40 Runden und alle Assertions. Spätere grüne Läufe erklären frühere rote nicht; keine Ursache und kein Datenverlust im echten Bestand belegt | '
    'Vorrangig [Übergabe Abschnitt 0](Glide_Uebergabe.md#0-sofortübergabe-wa-41--zuerst-lesen) übernehmen: acht vorhandene Minidumps und feste Eingangsdatei lokal gesichert, '
    '470-Dateien-Referenz und uncommitteten 3.48.0-Kandidaten erhalten. WHEA-/CPU-Spur ist eine Hypothese. Nutzer möchte vorerst keine BIOS-/CPU-Änderungen oder unnötigen Intel-Lastläufe; '
    'später bei konkretem Auftrag kontrollierter AMD-Vergleich. Fehlender externer Export bleibt als nicht bestätigt markiert. A/B getrennt klären, Datenkonsistenz bleibt eigenständiges Release-Tor; '
    'kein Abschwächen der Kriterien, keine Lieferung/Freigabe. Befundgeschichte und Gegenproben in §21.26 und dessen Nachweisen |')
if old != new:
    change('00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md', old, new)
change('00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md',
    'Prüfplatz und Wartebedingungen mit Diagnose bleiben wichtig |',
    'Prüfplatz und Wartebedingungen mit Diagnose bleiben wichtig. Neuer gesonderter Befund 27.10.: frische 3.15-venv nach 40 erfolgreichen Runden mit `PermissionError` beim Lesen nach hartem Testschreiberabbruch rot (Originalsuite Zeile 282). Kein nativer WA-41-Beleg oder bestätigter Produktfehler; Prozess-/Dateibesitz unter venv bei späterem Auftrag separat untersuchen ([Nachweis](../01_Repository/Glide/tests/qa-3.48.0/last_fenster_2026-10-27/README.md)) |')
change('01_Repository/Glide/src/glide/README.md',
    'Lokaler Quellstand 3.47.0: Mehrfachplanung auf der Startseite und flüchtiger Nebenansichtsverlauf vertiefen die Tagessteuerung/Suche aus 3.46.0. 88 Laufzeitdateien plus separater Zeichenprototyp, Aufgabenformat 26 unverändert. [Gezielte Prüfung und tatsächliche Lieferstände](../../tests/qa-3.47.0/folgepakete_2026-10-27/README.md).',
    'Lokaler Quellkandidat 3.48.0: Tagesnavigation, gemeinsame Wichtigkeit/Labels und Verweisnavigation ergänzen Tagessteuerung und Nebenansichtsverlauf. 88 Laufzeitdateien plus separater Zeichenprototyp, Aufgabenformat 26 unverändert. Python-Lieferung 3.47.0, native Pakete 3.45.0; WA-41 und Lieferabschluss offen. [Gezielte Prüfung und tatsächliche Lieferstände](../../tests/qa-3.48.0/dreierpaket_2026-10-27/README.md).')
change('01_Repository/Glide/packaging/runtime/README.md',
    'der aktuelle lokale Python-Lieferstand ist 3.43.1;',
    'der aktuelle lokale Python-Lieferstand ist 3.47.0, die nativen Pakete sind 3.45.0 und der Quellkandidat 3.48.0;')
out = HERE / 'gezielte_ersetzungen.json'
previous = json.loads(out.read_text(encoding='utf-8')) if out.exists() else []
out.write_text(json.dumps(previous + changes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(replacements=len(changes), files=len({r['path'] for r in changes}))))
