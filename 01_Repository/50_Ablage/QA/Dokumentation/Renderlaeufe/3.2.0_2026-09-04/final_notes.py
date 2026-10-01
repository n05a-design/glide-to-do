from pathlib import Path
namespace={'__file__':__file__}
exec(Path(__file__).with_name('update_workspace_docs.py').read_text(encoding='utf-8').split('# Historical version-labelled')[0],namespace)
write,edit,ROOT,QA=(namespace[k] for k in ('write','edit','ROOT','QA'))
edit('00_Arbeitsvorbereitung/README.md', [('Emoji-Ausnahmen für Gruppe und höchste Wichtigkeit bleiben', 'Emoji-Ausnahmen für Gruppe, höchste Wichtigkeit und Beschreibungsmarker bleiben')])
edit('07_Python-Versionen/README.md', [('alle Symbole als Textzeichen aus einer zentralen Tabelle (Anhang `⊕`, Fälligkeit `▦`)', 'zentrale Textsymbole in ICONS (Anhang `⊕`, Fälligkeit `▦`); Emoji-Ausnahmen bleiben für Gruppenmarker, höchste Wichtigkeit und Beschreibungsmarker')])
edit('30_Release_Exports/README.md', [('Die Ordner `2.5.1/` und `2.5.2/` sind vorbereitet, enthalten aber noch keinen\nfreigegebenen Build. Der aktuelle Source-Stand ist **3.2.0**; ein Build\nexistiert noch nicht, weil Produktidentität, Signing und Clean-Machine-Tests\noffen sind', 'Die frühere Dokumentation beschrieb vorbereitete Ordner `2.5.1/` und `2.5.2/`.\nDiese liegen aktuell nicht in diesem Bereich; vorhanden ist nur `Archiv/`.\nDer aktuelle Source-Stand ist **3.2.0** mit Datenformat **10**. Ein freigegebener\nBuild und ein Release-Ordner 3.2.0 existieren nicht. Build-Konfiguration,\nProduktidentität, Signing und Clean-Machine-Tests sind offen')])
print('Letzte Bestandsreferenzen korrigiert.')
