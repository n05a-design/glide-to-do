from pathlib import Path
namespace={'__file__':__file__}
exec(Path(__file__).with_name('update_workspace_docs.py').read_text(encoding='utf-8').split('# Historical version-labelled')[0],namespace)
edit=namespace['edit']
edit('00_Arbeitsvorbereitung/Notizen/Technische_Fakten_3.2.0.md',[
('Jede Aktion, die Punkte umordnet – Gruppieren, Auflösen, Ziehen, Ein- und\nAusrücken, Verschieben in eine andere Liste – zählt vor und nach der Aktion alle\nPunkt-IDs in allen Listen und im Papierkorb.', 'Der Bestandswächter zählt bei den damit eingerahmten Umbauaktionen vor und nach\nder Aktion alle Punkt-IDs in Listen und Papierkorb. Die Abdeckung ist noch\nnicht lückenlos: `indent_selected` verwendet nur `item_change`; weitere direkte\nÄnderungspfade wie `add_child_item` und `apply_sidebar_rename` bleiben zu prüfen.'),
('**Änderungsrahmen (3.1.0).** Jede Änderung an Punkten läuft durch\n`item_change`, jede an Listen und Ordnern durch `sidebar_change`.', '**Änderungsrahmen (3.1.0).** `item_change` und `sidebar_change` sind die zentralen\nRahmen und laut Projektregel für neue Änderungen verbindlich. Im Bestand sind\nnoch direkte Änderungswege vorhanden; eine lückenlose Umstellung ist nicht belegt.'),
])
edit('40_Store_Material/Produktdatenblatt_3.2.0.md',[
('Jede Aktion, die\nPunkte umordnet, läuft unter einem Bestandswächter, der vor und nach der Aktion\nalle Punkte zählt und bei einer Lücke den vorherigen Stand herstellt.', 'Ein Bestandswächter\nprüft die damit eingerahmten Umbauaktionen und stellt bei erkanntem Verlust den\nVorstand her. Die Umstellung ist noch nicht lückenlos; vor einer Release-Zusage\nsind direkte Änderungswege und die dokumentierten Grenzbefunde zu beheben.'),
])
