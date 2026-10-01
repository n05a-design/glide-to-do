from pathlib import Path
namespace={'__file__':__file__}
exec(Path(__file__).with_name('update_workspace_docs.py').read_text(encoding='utf-8').split('# Historical version-labelled')[0],namespace)
write,edit,ROOT,QA=(namespace[k] for k in ('write','edit','ROOT','QA'))
edit('00_Arbeitsvorbereitung/Checklisten/Glide_Veroeffentlichung_Checkliste.txt',[
('Die Fälligkeiten sind Vorschläge ab dem Tag der Erstellung und lassen sich gefahrlos verschieben.', 'Stand: App 3.2.0, Datenformat 10, 04.09.2026. Termine werden in dieser Zusatzliste vom Nutzer gesetzt; die reproduzierbare Releaseplanung nutzt relative Fälligkeiten.'),
('Windows .ico (16/32/48/64/128/256), macOS .icns (16 bis 1024, je @1x und @2x)', 'Windows .ico mindestens 16/24/32/48/256 px; klassisches macOS-iconset 16/32/128/256/512 Punkte in 1x/2x, daraus .icns'),
('2.4. ⚐ PNG-Satz 512 und 1024 für die Stores', '2.4. ⚐ Store-Logos anhand der aktuellen Plattformvorgaben erzeugen'),
('Ohne Notarisierung warnt Gatekeeper bei jedem Start.', 'Developer-ID-Signatur, Hardened Runtime, Notarisierung, Stapling und Gatekeeper am späteren Direkt-Build prüfen.'),
('Windows: Code-Signing-Zertifikat (OV oder EV) eines anerkannten Anbieters, Laufzeit meist ein bis drei Jahre. macOS: Developer-ID. Beides kostet Geld und braucht Vorlauf – am besten früh anstoßen.', 'Windows: vertrauenswürdige Signatur für Installer und PE-Dateien gemäß aktueller Store-Spezifikation. macOS-Direktvertrieb: Developer-ID. Anbieter, Kontozugang und Verfahren klären; keine Gebühr oder Laufzeit ohne aktuelles Angebot voraussetzen.'),
('Seit 3.2.0 ist Strg+Klick', 'Seit 2.11.0 ist Strg+Klick'),
('seit 3.2.0 im Papierkorb', 'seit 2.11.0 im Papierkorb'),
('die Testumgebung läuft unter Linux/Tk.', 'automatisierte Windows-Prüfung ist vorhanden, vollständige manuelle Gerätefreigabe bleibt offen.'),
])
for rel,text in {
'50_Ablage/QA/Dokumentation/README.md':'''# Dokumentprüfung

Stand: 04.09.2026 · Glide 3.2.0 · Datenformat 10

Aktueller Lauf: `Renderlaeufe/3.2.0_2026-09-04/`. Die Word-Vorlage 2.6.0
und die fortgeschriebene 3.2.0-Datei wurden mit installiertem Microsoft Word
schreibgeschützt nach PDF exportiert und über den Dokument-Renderer rasterisiert.
Das finale Inhaltsverzeichnis basiert auf den tatsächlich paginierten Bookmarks.

Historische Renderläufe bleiben unverändert. Das frühere Manifest ist vor der
Fortschreibung archiviert; `MANIFEST_SHA256.csv` enthält den aktuellen Bestand
dieses QA-Bereichs. Dateipfade sind relativ zur Workspace-Wurzel.
''',
'50_Ablage/QA/Dokumentation/Renderlaeufe/README.md':'''# Renderläufe der Dokumentation

Stand: 04.09.2026 · aktuelle Dokumentversion 3.2.0 · Datenformat 10

`3.2.0_2026-09-04/` enthält Referenzrender, Fortschreibungswerkzeug,
Paketvergleich, Archivmanifest und final geprüfte Seitenbilder.
Die früheren Läufe zu 2.5.1 und 2.5.2 bleiben historische Belege; ihre Namen
und Inhalte werden nicht auf 3.2.0 geändert. Auch identische Zwischenstände
bleiben erhalten. Es wurde kein Renderlauf gelöscht.

Archive werden dezentral im jeweiligen Ordner geführt. Das aktuelle SHA-256-
Manifest liegt eine Ebene höher, die unveränderte Vorgängerfassung in `Archiv/`.
''',
}.items():write(rel,text)

# Record intended layout corrections alongside the template contract.
p=QA/'artifact.md';s=p.read_text(encoding='utf-8')
s+='\nGezielte Layoutkorrektur nach Sichtprüfung: Kapitel 4 beginnt auf neuer Seite; der Produktgrenzen-Codeblock bleibt zusammen mit seiner Einleitung. Dies beseitigt zwei tatsächlich im Zwischenrender festgestellte verwaiste Teilblöcke.\n'
p.write_text(s,encoding='utf-8')
print('Text- und Navigationshinweise abgeschlossen.')
