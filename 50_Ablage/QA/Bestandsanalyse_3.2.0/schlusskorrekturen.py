from dokumente_abgleichen import ROOT
from pathlib import Path

def replace(name, pairs):
    path=ROOT/name
    text=path.read_text(encoding='utf-8')
    for old,new in pairs:
        if old not in text:
            raise ValueError(f'{name}: {old[:50]}')
        text=text.replace(old,new)
    path.write_text(text,encoding='utf-8')

replace('docs/decisions/PRODUCT_IDENTITY.md', [
    ('| Max. Verschachtelung | 100 Ebenen | `MAX_ITEM_DEPTH` |', '| Lade-/Normalisierungsgrenze der Punkttiefe | 100; vor UI-Mutationen noch nicht durchgehend eingehalten | `MAX_ITEM_DEPTH`; offene Lücke in `../11_BESTANDSANALYSE.md` |')])
replace('docs/09_PROJECT_HANDOFF.md', [
    ('| Manuelle Prüfung Windows/macOS | **nie erfolgt** |', '| Vollständige manuelle Plattformmatrix | **offen**; Windows-Arbeitsdaten in Hell/Dunkel visuell geprüft |'),
    ('Die Datei enthält heute keine Phasenstruktur.', 'Die Datei enthält nummerierte Abschnitte 1–10; eine frühere elfte Phase ist unbelegt.'),
    ('Vorgang gemeldet. Jede Aktion, die Punkte umordnet, läuft darunter.', 'Vorgang gemeldet. Das ist die Zielregel für Umbauaktionen; beispielsweise\n   `indent_selected` und `outdent_selected` laufen derzeit nur im\n   Änderungsrahmen, ohne diesen zusätzlichen Wächter.'),
    ('*jede* Änderung.', 'viele Änderungen. `add_child_item` und\n   `apply_sidebar_rename` nutzen noch eigene Snapshot-/Speicherfolgen'),
])
replace('docs/02_ARCHITECTURE.md', [
    ('Jede Aktion, die Punkte umordnet, läuft unter `guarded_structural_change`. Der', 'Zielvorgabe: Jede Aktion, die Punkte umordnet, soll unter\n`guarded_structural_change` laufen. Die Umsetzung ist noch nicht lückenlos:\n`indent_selected` und `outdent_selected` verwenden nur `item_change`. Der'),
    ('Seit 3.1.0 läuft jede Änderung an Punkten durch `item_change` und jede an Listen\nund Ordnern durch `sidebar_change`.', 'Seit 3.1.0 bündeln `item_change` und `sidebar_change` viele Änderungen an\nPunkten, Listen und Ordnern. Die vollständige Nutzung bleibt die Zielvorgabe:\n`add_child_item` und `apply_sidebar_rename` haben noch eigene Snapshot-/\nSpeicherfolgen. Die ausdrücklich gesonderten Import-/Backup-Wege bleiben\nebenfalls außerhalb dieser Rahmen.'),
])
replace('README.md', [
    ('**Ein gemeinsamer Rahmen für jede Änderung.**', '**Gemeinsame Rahmen für Änderungen.**'),
    ('Jede Umbauaktion läuft unter einem Bestandswächter, der', 'Viele Umbauaktionen laufen unter einem Bestandswächter, der'),
    ('## Dokumentation und Release-Arbeitslisten', 'Die vollständige Einbindung aller Änderungswege in Rahmen und Bestandswächter\nist noch offen, unter anderem bei `add_child_item`, `apply_sidebar_rename`\nund dem Ein-/Ausrücken. Siehe Bestandsanalyse.\n\n## Dokumentation und Release-Arbeitslisten'),
])
for name in ('docs/05_QA_TESTPLAN.md','docs/06_DATA_BACKUP_MIGRATION.md'):
    path=ROOT/name
    text=path.read_text(encoding='utf-8').replace('512 MB','512 MiB')
    path.write_text(text,encoding='utf-8')

replace('docs/12_ABSCHLUSSBERICHT.md', [
    ('Der App-Quelltext blieb unverändert', 'Außerdem werden gemeinsame Änderungsrahmen und Bestandswächter noch nicht\nvon allen vorgesehenen Wegen verwendet; diese Architekturreststellen sind\nals offen dokumentiert. Der App-Quelltext blieb unverändert'),
])

path=Path(__file__).with_name('bestandsbericht.py')
text=path.read_text(encoding='utf-8')
text=text.replace("body += '## Codeprüfung und Prozessverbesserung\\n\\n' + audit + '\\n'", "body += '## Codeprüfung und Prozessverbesserung\\n\\n' + audit + '\\n'\n    body += '''\n+### Ergänzender Architekturabgleich\n+\n+Die gemeinsame Änderungslogik ist noch nicht lückenlos umgesetzt.\n+`indent_selected` (12905) und `outdent_selected` (12923) verwenden\n+`item_change` ohne zusätzlichen Bestandswächter. `add_child_item` (11803)\n+und `apply_sidebar_rename` (5532) nutzen noch direkte Snapshot-/Speicherfolgen.\n+Die Dokumentation hatte die verbindliche Zielregel als vollständig erreichten\n+Istzustand ausgegeben. Dieser Überanspruch ist korrigiert; eine strukturelle\n+Umstellung der verbleibenden Aufrufer wurde nicht eigenmächtig vorgenommen.\n+Status: **GEMELDET**, wichtiger Architekturrest, kein hier neu reproduzierter\n+Datenverlust. Vor weiterer Änderung gezielt mit Rückgängig-/Fehlerpfaden prüfen.\n+\n+`audit_app.py` enthält nummerierte Abschnitte 1 bis 10. Die Behauptung, es\n+gebe keinerlei Phasenstruktur, war falsch; nur die frühere elfte Phase bleibt\n+ohne Originaldatei/Git-Historie unbelegt.\n+\n+'''\n")
text=text.replace('\n+', '\n')
path.write_text(text,encoding='utf-8')
print('Unabhängige Schlussbefunde in aktiven Dokumenten berücksichtigt.')
