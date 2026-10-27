"""Führt bestehende Lieferdokumente nach überprüfter Lieferung gezielt fort."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ROOT = REPO.parents[1]
assert json.loads((HERE / 'lieferung.json').read_text(encoding='utf-8'))['exitcode'] == 0


def paragraph(path, prefix, replacement):
    text = path.read_text(encoding='utf-8-sig')
    parts = text.split('\n\n')
    index = next(i for i, value in enumerate(parts) if value.startswith(prefix))
    parts[index] = replacement
    path.write_text('\n\n'.join(parts), encoding='utf-8', newline='')


def replace(path, pairs):
    text = path.read_text(encoding='utf-8-sig')
    for old, new in pairs:
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8', newline='')


proof = 'tests/qa-3.45.0/paketabschluss_2026-10-26/README.md'
delivery = ROOT / '07_Python-Versionen/README.md'
paragraph(delivery, 'Die startbare Python-Fassung', 'Die startbare Python-Fassung `Glide-Aufgaben-und-Listen_v3.45.0.pyw` enthält den vollständigen aktuellen Quellstand: Sicherungen/Anhänge und Arbeitsmodi, Tagesvorschlag mit direkten Freigaben, Verweisvorschau und gemeinsames Startseitenmodell. Aufgabenformat 26; 86 Code-Dateien und 147 Ressourcen-/Vendor-Dateien bytegleich zur Quelle, echte Liefer-Start-/Speicher-/Undo-Probe grün. Auch die eigenständigen Windows-/Mac-Pakete sind 3.45.0. [Liefernachweis](../01_Repository/Glide/' + proof + '), [QA-Bericht](../01_Repository/Glide/docs/07_QA_BERICHT.md). In denselben Ordner gehören:')
replace(delivery, [('`home_tiles.py`, `capture_parser.py`', '`home_tiles.py`, `home_dashboard.py`, `capture_parser.py`'), ('build/windows/Glide-3.42.0/Glide.exe', 'build/windows/Glide-3.45.0/Glide.exe'), ('und die eigenständigen Pakete 3.42.0 öffnen Format 26 schreibgeschützt', 'und die früheren, jetzt archivierten Pakete 3.42.0 öffnen Format 26 schreibgeschützt; die aktuellen Pakete 3.45.0 verarbeiten Format 26')])

package = REPO / 'packaging/README.md'
paragraph(package, 'Stand 25.10.2026', 'Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Einstellungen 2 · Vorlagen 2')
paragraph(package, 'Die eigenständigen Entwicklungspakete', 'Die eigenständigen Entwicklungspakete für Windows x64 und macOS arm64 sind auf 3.45.0 neu gebaut und geprüft. Windows: 103 Dateien, Python 3.14.7/Tcl-Tk 9.0.4, kompilierter Quell-/PE-/Lizenzabgleich und lokale Startprobe grün. Mac: 333 Dateien und 29 interne Symlinks, Python 3.14.5/Tcl-Tk 9.0.3, nativer arm64-Bau, Mach-O-/Ad-hoc-Signaturprüfung und Prozesssandbox-Startprobe grün. Python-Lieferung bytegleich; alte aktive 3.42.0-Pakete liegen im jeweiligen `build/.../Archiv`. [Nachweise](../' + proof + '). Windows bleibt unsigniert; öffentliche Signaturen, Installer und Menschenabnahme sind eigene Tore.')
paragraph(package, '## Inhalt eines Pakets', '## Aktuelle Lieferartefakte\n\n- Windows: `build/windows/Glide-3.45.0/Glide.exe` und `build/windows/Glide-3.45.0-windows-x64.zip`.\n- Mac: `build/macos/Glide-3.45.0-macos-arm64.tar.gz` nativ entpacken. Die lokale `build/macos/Glide.app` ist eine Windows-Inspektionskopie mit NT-Linkzielen; native Weitergabe über das unveränderte TAR.\n- Wiederholbarer nativer Mac-Bau: `sh packaging/paket/baue_und_pruefe_macos.sh --python /Pfad/python3`; neuer Bauordner außerhalb OneDrive, exakte Originalruntime gemäß Lizenzmanifest. `.github/workflows/macos-paket.yml` führt denselben Weg auf einem nativen arm64-Runner aus. [Grüner nativer Lauf](https://github.com/n05a-design/glide-to-do/actions/runs/40328682255).\n\n## Inhalt eines Pakets')

functions = REPO / 'docs/20_FUNKTIONEN.md'
replace(functions, [('### Eigenständiger Start (3.42.0)', '### Eigenständiger Start (3.45.0)'), ('vorhandene Daten und Aufgabenformat 25 bleiben erhalten', 'vorhandene Daten bleiben erhalten; aktuelles Aufgabenformat ist 26')])

release = REPO / 'docs/10_VEROEFFENTLICHUNG.md'
paragraph(release, 'Stand 25.10.2026', 'Stand 26.10.2026 · Glide 3.45.0 · Entwicklungspakete geliefert, keine öffentliche Veröffentlichung · Aufgabenformat 26')
paragraph(release, '**Je Version', '**Aktueller Lieferstand 3.45.0 (26.10.2026):** Python-Fassung bytegleich, Windows-Paket und natives Mac-arm64-Paket neu gebaut und startgeprüft; Windows-Vollprüfung mit allen 104 Suiten grün. Mac-Ad-hoc-Signatur und isolierter Macstart grün. [Liefernachweis](../' + proof + '). Mac-/Linux-Vollmatrix und menschliche Releaseabnahme bleiben getrennt offen; die folgenden Haken bezeichnen den historischen Vollabschluss 3.42.0.')
paragraph(release, 'Die Haken beschreiben', 'Die Haken dokumentieren den historischen vollständigen Plattformabschluss 3.42.0. Die aktuelle Lieferung 3.45.0 übernimmt keine ungetesteten Mac-/Linux-/Menschenfreigaben daraus; aktuelle Belege stehen oben und im [QA-Bericht](07_QA_BERICHT.md).')
text = release.read_text(encoding='utf-8')
rows = text.splitlines()
for i, row in enumerate(rows):
    if row.startswith('- [x] Eigenständige Entwicklungspakete'):
        rows[i] = '- [x] Eigenständige Entwicklungspakete 3.45.0 mit Python 3.14/Tk 9 für macOS arm64 und Windows x64. Natives Mac-Paket mit Prozesssandbox und Ad-hoc-Signatur, Windows-Paket mit lokaler Startprobe und Hash-/PE-Abgleich geprüft. Windows-ACL-Sperrprobe bleibt dem vergänglichen Hosted-CI-Runner vorbehalten. Öffentliche Signaturen/Installer und Menschenabnahme bleiben offen. [Aktuelle Nachweise](../' + proof + ').'
release.write_text('\n'.join(rows) + '\n', encoding='utf-8', newline='')

handoff = ROOT / '00_Arbeitsvorbereitung/Glide_Uebergabe.md'
paragraph(handoff, 'Stand 26.10.2026', 'Stand 26.10.2026 · Glide 3.45.0 · Aufgabenformat 26 · Python-Lieferung und eigenständige Windows-/Mac-Pakete 3.45.0')
paragraph(handoff, '**Aktuell:', '**Aktuell: Lieferungen und beide eigenständigen Pakete auf 3.45.0 aktualisiert.** App `d516ca67…`; Python-Lieferung mit 86 Code-Dateien und 147 Ressourcen bytegleich. Windows-Vollprüfung: 123 Schritte, 122 ausgeführt/grün, eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Windows-Paket neu gebaut/gestartet, Mac-Paket nativ gebaut, signatur- und isoliert startgeprüft. [Nachweis](../01_Repository/Glide/' + proof + '), [Plan §21.20](Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450). Menschliche und öffentliche Releaseabnahme bleiben getrennt offen.')
paragraph(handoff, '**Aktueller Auftrag', '**Auftrag 26.10.2026:** „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Danach ausdrücklich GitHub Actions mit macOS-Runner und „weiter“ beauftragt. Native Bauten und Lieferabgleich sind abgeschlossen; strenge CI-Abschlusswerte stehen im Paketnachweis. Quell-/Workflowtransport auf `codex/glide-paketabschluss-3.45.0`, kein Merge oder öffentliche Veröffentlichung.')
text = handoff.read_text(encoding='utf-8'); rows = text.splitlines()
new_rows = {
'| Quelle |': '| Quelle | Glide 3.45.0 / Format 26, App `d516ca67…`, Modell `ced120a5…`; 86 Laufzeitdateien plus Prototyp. [Aktueller Liefernachweis](../01_Repository/Glide/' + proof + '). |',
'| CI-Grundstufe |': '| CI-Grundstufe | Ausgangsprüfung grün; strenger Abschluss nach Liefer-/Dokumentabgleich im [Paketnachweis](../01_Repository/Glide/' + proof + '). GitHub-Grundstufe auf `6c342f8` grün; weitergehende Remote-Matrix getrennt behandeln. |',
'| Vollprüfung lokal |': '| Vollprüfung lokal | Korrigierter Stand `d516ca67…`: 123 Schritte, 122 grün und eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Der erste rote Lauf bleibt erhalten. [Nachweise](../01_Repository/Glide/' + proof + '). |',
'| Python-Lieferung 07 |': '| Python-Lieferung 07 | Glide 3.45.0 / Format 26, App `d516ca67…`; 86 Code-Dateien und 147 Ressourcen bytegleich. Echte Start-/Speicher-/Erledigen-/Undo-Probe aus 07 grün. |',
'| Showcase / Pakete |': '| Showcase / Pakete | Showcase-Import/Neustart und sechs Lieferdateien geprüft. Windows-Paket 3.45.0: 103 Dateien, PE/Quellabgleich und lokale Startprobe grün. Mac-Paket 3.45.0: 333 Dateien/29 Symlinks, nativer Bau/Signatur/isolierter Start grün. Mac-Weitergabe über geprüftes TAR; lokale .app ist NT-Inspektionskopie. Alte aktive Pakete liegen im Archiv. |',
'| Git lokal |': '| Git lokal | Kandidatenzweig `codex/glide-paketabschluss-3.45.0`, Basis `origin/main` `cea01df`; übertragener Stand `6c342f8`. Liefer-/Dokumentabschluss folgt auf diesem Zweig; kein Merge. |',
'| GitHub |': '| GitHub | Nativer Maclauf [40328682255](https://github.com/n05a-design/glide-to-do/actions/runs/40328682255) auf `4e73220` grün; identische Appquellen. Maclauf auf `6c342f8` ebenfalls grün, dortige Grundstufe grün; restliche Remote-Matrix wird nicht pauschal als grün ausgegeben. |'}
for i,row in enumerate(rows):
    for prefix,replacement in new_rows.items():
        if row.startswith(prefix):rows[i]=replacement
    if row.startswith('2. **Native Lieferung vervollständigen:**'):
        rows[i]='2. **Native Restabnahmen:** Mac-/Linux-Vollmatrix sowie Reader-/DPI-/Mehrmonitor-/Menschenabnahme fortsetzen. Die aktuellen Python-/Windows-/Mac-Lieferungen sind 3.45.0; ein erneuter Paketneubau ist kein offener 3.42.0-Rest.'
handoff.write_text('\n'.join(rows)+'\n',encoding='utf-8',newline='')

plan=ROOT/'00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md'
text=plan.read_text(encoding='utf-8-sig'); start=text.index('### 21.20 Lieferabschluss und Paketbau 3.45.0')
text=text[:start]+'''### 21.20 Lieferabschluss und Paketbau 3.45.0

**Auftrag 26.10.2026:** „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Danach GitHub Actions mit macOS-Runner und „weiter“ gewählt. Python-Lieferung und tatsächliche native Windows-/Mac-Pakete sind nun 3.45.0 / Format 26; App `d516ca67…`, Modell `ced120a5…`.

| Teil | Belegter Abschluss / Grenze |
|---|---|
| Windows-Vollprüfung | 123 Schritte, 122 ausgeführt/grün, eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Der rote erste Lauf und Gegenproben bleiben erhalten. |
| Python und Showcase | 86 Code-Dateien plus 147 Ressourcen bytegleich; echte 07-Start-/Speicher-/Undo-Probe und Showcase-Import/Neustart grün. |
| Windows-Paket | 103 Paketdateien, 87 kompilierte Modulnachweise, PE-/Lizenz-/Quellabgleich und lokale Startprobe grün. `build/windows/Glide-3.45.0/Glide.exe` und Windows-ZIP geliefert. Keine lokale ACL-Sperrprobe. |
| Mac-Paket | Natives arm64-Paket mit Python 3.14.5/Tcl-Tk 9.0.3: 333 Dateien und 29 Symlinks, Mach-O/Ad-hoc-Signatur und Prozesssandbox-Startprobe grün. Kanonisches TAR geliefert; .app unter Windows nur NT-Inspektionskopie. |
| Fehlerkorrekturen | Vollständige gepinnte historische Altleser statt gemischter Module, kein Cacheaufbau beim Abbau; laufende Animation respektiert späteren Undo-Hinweis. B15 berücksichtigt Tk-Stapelreihenfolge mit Gegenprobe. Kein Grenzwert aufgeweicht. |
| Integrität | ZIP/TAR und Paketdateien hashgeprüft; drei zuvor fehlende Mac-Frameworkdateien wieder vollständig. Zehn reine Checkout-EOL-Unterschiede gesondert belegt; keine Code-/Binärabweichung. |
| Git und CI | Autorisierter Workflowtransport auf `codex/glide-paketabschluss-3.45.0`; Maclauf und Grundstufe auf übertragenem Stand grün. Strenger lokaler Abschluss im Paketnachweis; weitere Remote-Matrix und Menschenabnahme bleiben getrennt. Kein Merge oder öffentliche Veröffentlichung. |

**Nachweis:** [Liefer-/Paketabschluss 26.10.2026](../01_Repository/Glide/tests/qa-3.45.0/paketabschluss_2026-10-26/README.md). Aktive alte Pakete sind archiviert. Native Mac-/Linux-Vollmatrix, Reader/DPI/Mehrmonitor und echte Menschenabnahme sowie D43-Veröffentlichungstore werden durch die automatisierten Paketproben nicht ersetzt.
'''
rows=text.splitlines()
for i,row in enumerate(rows[:12]):
    if row.startswith('Einziges Planungsdokument:'):
        rows[i]='Einziges Planungsdokument für Aufgaben, Pakete, Reihenfolge und Entscheidungen. **Aktuell 26.10.2026:** Python-Lieferung und beide eigenständigen Pakete auf 3.45.0 aktualisiert; alle 104 Windows-Suiten grün, nativer Macbau/Signatur/isolierter Start grün. [Lieferabschluss §21.20](#2120-lieferabschluss-und-paketbau-3450). Menschliche und öffentliche Releaseabnahme bleiben offen.'
plan.write_text('\n'.join(rows)+'\n',encoding='utf-8',newline='')

direction=REPO/'docs/ARBEITSRICHTUNG.md'
paragraph(direction,'**Aktueller Liefer-/Paketauftrag','**Liefer-/Paketauftrag 26.10.2026:** „eigenständige Pakete sollen nicht weiterhin 3.42.0 sein, alles aktualisieren und prüfen.“ Anschließend GitHub Actions mit macOS-Runner und „weiter“ gewählt. Python-Lieferung und beide eigenständigen Pakete sind auf 3.45.0 aktualisiert; Windows-Vollprüfung und native Paketproben grün. [Plan §21.20](../../../00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md#2120-lieferabschluss-und-paketbau-3450), [Nachweis](../'+proof+'). Der erforderliche Quell-/Workflowtransport auf `codex/glide-paketabschluss-3.45.0` ist autorisiert; kein Merge oder öffentliche Veröffentlichung. D17/D51 und offene Menschen-/Plattformtore gelten weiter.')

qa=REPO/'docs/07_QA_BERICHT.md'
paragraph(qa,'Stand 26.10.2026','Stand 26.10.2026 · Glide 3.45.0 · Python-Lieferung und Windows-/Mac-Pakete 3.45.0 · Aufgabenformat 26')
replace(qa,[('**Aktueller Startseitenpilot','**Vorheriger Startseitenpilot'),('**Aktueller Fortsetzungsstand Verweisvorschau','**Vorheriger Fortsetzungsstand Verweisvorschau')])
text=qa.read_text(encoding='utf-8');marker='**Vorheriger Startseitenpilot'
entry='**Aktueller Liefer-/Paketabschluss 26.10.2026:** App `d516ca67…`; erneute Windows-Vollprüfung Exitcode 0: 123 Schritte, 122 grün, eine menschliche Sichtprüfung übersprungen; alle 104 Suiten grün. Python-Lieferung mit 86 Code-Dateien und 147 Ressourcen bytegleich; echte Liefer- und Showcaseprobe grün. Windows-Paket 103 Dateien mit PE-/Quell-/Lizenzabgleich und lokaler Startprobe; Mac-Paket 333 Dateien/29 Symlinks, nativer arm64-Bau, Mach-O/Ad-hoc-Signatur und Prozesssandbox-Start grün. Alte aktive 3.42.0-Pakete archiviert. [Abschlussnachweis](../'+proof+'). Strenge CI-Abschlusswerte dort; öffentliche und menschliche Freigabe sowie weitere native Matrix nicht daraus ableiten.\n\n'
qa.write_text(text.replace(marker,entry+marker,1),encoding='utf-8',newline='')

architecture=REPO/'docs/02_ARCHITECTURE.md'
replace(architecture,[('65.368 Zeilen nach','65.371 Zeilen nach'),('49.884 mit 1.742 direkten Methoden','49.887 mit 1.742 direkten Methoden')])
changelog=REPO/'CHANGELOG.md'
replace(changelog,[('## In Arbeit – Tagesvorschlag, Verweisvorschau und Startseitenmodell (26.10.2026)','## Ergänzungen und Lieferabschluss 3.45.0 (26.10.2026)')])
text=changelog.read_text(encoding='utf-8');marker='## Ergänzungen und Lieferabschluss 3.45.0 (26.10.2026)'
text=text.replace(marker,marker+'\n\n- **Alle Lieferungen aktualisiert:** Python-Fassung sowie echte Windows-/Mac-Pakete 3.45.0 geliefert und hashgeprüft. 104 Windows-Suiten grün; nativer Macbau, Signatur und isolierter Start grün. Animations-/Undo-Überlagerung korrigiert; Altleser- und Stapelreihenfolgeprüfungen repariert. [Nachweis]('+proof+').',1)
changelog.write_text(text,encoding='utf-8',newline='')
print('Lieferdokumentation gezielt fortgeschrieben')
