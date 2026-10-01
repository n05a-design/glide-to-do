from pathlib import Path
from zipfile import ZipFile
from lxml import etree as ET
import csv
import hashlib
import json

namespace={'__file__':__file__}
exec(Path(__file__).with_name('update_workspace_docs.py').read_text(encoding='utf-8').split('# Historical version-labelled')[0],namespace)
ROOT,QA,preserve,write=(namespace[k] for k in ('ROOT','QA','preserve','write'))
revision=json.loads((QA/'docx_revision_manifest.json').read_text(encoding='utf-8'))
ref,out=Path(revision['reference']),Path(revision['output'])
assert hashlib.sha256(ref.read_bytes()).hexdigest()==revision['reference_sha256']
assert hashlib.sha256(out.read_bytes()).hexdigest()==revision['output_sha256']
ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with ZipFile(ref) as a, ZipFile(out) as b:
    for name in revision['preserved_parts']:assert a.read(name)==b.read(name),name
    x,y=(ET.fromstring(z.read('word/document.xml')) for z in (a,b))
    counts={tag:[len(r.findall('.//w:'+tag,ns)) for r in (x,y)] for tag in ['sectPr','tbl','drawing','bookmarkStart']}
    assert all(a==b for a,b in counts.values()),counts
    assert [ET.tostring(e) for e in x.findall('.//w:sectPr',ns)]==[ET.tostring(e) for e in y.findall('.//w:sectPr',ns)]
    pages=json.loads((QA/'bookmark_pages.json').read_text(encoding='utf-8-sig'))
    nav=0
    for h in y.findall('.//w:hyperlink',ns):
        anchor=h.get('{'+ns['w']+'}anchor')
        if anchor in pages:
            assert h.findall('.//w:t',ns)[-1].text==str(pages[anchor]),anchor
            nav+=1
    assert nav==23,nav
assert len(list((QA/'final4').glob('page-*.png')))==22

# The original Word baseline is retained as both reference copy and moved original.
ledger=namespace['ledger']
original_rel='10_Dokumentation/2.6.0 – Glide_Arbeitsvorbereitung_Codex_Build_Release_Plan.docx'
for action,p in [('copy',ref),('move',ref.with_name(ref.stem+'_Original_verschoben_2026-09-04.docx'))]:
    if not any(e['archive']==str(p.relative_to(ROOT)) for e in ledger):
        ledger.append({'source':original_rel,'archive':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'action':action,'reason':'Word 2.6.0 unverändert erhalten; Vorlage für formatgetreue Fortschreibung 3.2.0'})
(QA/'external_archive_manifest.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')

report=f'''# Nachweis Dokumentation und externe Dateien

Stand: 04.09.2026 · App 3.2.0 · Datenformat 10

## Word-Endfassung

`{out.relative_to(ROOT)}`

22 Seiten, alle finalen PNG-Seiten 1 bis 22 vollständig visuell geprüft.
Keine abgeschnittenen Texte oder Bilder, keine unlesbaren Zeichen, Tabellenköpfe
wiederholt, Fußzeilen unverändert positioniert. Zwei im Zwischenrender erkannte
Umbruchprobleme gezielt korrigiert. Historische Vorlage, Farben, Schriften,
17 Tabellen, Bild und 23 Navigationsziele erhalten. Titel-/Kapitelformat bleibt
auf Nutzerwunsch vorlagengetreu; keine generische Neugestaltung.

Export: installiertes Microsoft Word, unsichtbar und schreibgeschützt; kein
Save durch Word. Canonical `render_docx.py` mit vorhandenem Word-PDF als
Konverterfallback rasterisiert. LibreOffice ist nicht installiert. Die
Sandbox-Freigabe erlaubte den lokalen Word-Export; keine Ablehnung offen.

Endhash SHA-256: `{revision['output_sha256']}`.
Referenzhash SHA-256: `{revision['reference_sha256']}`.
Strukturzählung Referenz/Final: `{counts}`.
23 TOC-Seitenzahlen stimmen mit den tatsächlichen Word-Bookmarks überein.
Alle nicht zur Bearbeitung freigegebenen Paketbestandteile sind bytegleich.
`docx_revision_manifest.json` nennt die gezielten Absatz- und Paketänderungen.

## Externe Fortschreibung

Entscheidungen 3.2.0 neu erstellt; Vorgänger 2.6.0/2.11.0 aus den aktiven
Bereichen in das jeweilige Archiv verschoben. Technische Fakten, manuelle
Prüfliste, importierbare TXT-Liste, Produktdatenblatt, Microsoft-/Apple-Angaben
und Bereichs-README sachlich fortgeschrieben. Alle Änderungen haben vorab
verifizierte Archivkopien, siehe `external_archive_manifest.json`.

Wesentliche Korrekturen: Schema 10; tatsächliche Dateien statt geplanter Module;
TXT kein vollständiges Backup; automatische Dateizugriffe korrekt beschrieben;
Systemanforderungen und gebündelte Laufzeit bis zum Build offen; Altersfreigabe
und Barrierefreiheit nicht als Codefakt behauptet; Einfrieren NICHT VERIFIZIERT;
Emoji-Ausnahmen und die reproduzierten Grenzen 21 Labels/Tiefe 101 offengelegt.

Store-Recherche unterscheidet MSI/EXE von MSIX und Mac Store von Direktvertrieb.
Quellen und Abrufdatum stehen direkt in den Plattformdokumenten. Die aktuelle
MSI/EXE-Quelle nennt keine Pixelgrenzen; diese bleiben UNGEKLÄRT. Preis,
Lizenz, Publisher, Kennungen und Vertriebsweg bleiben Inhaberentscheidungen.

Historische Daten, Python-Versionen, Dokumente, Bilder und Testeingaben behalten
ihren tatsächlichen alten Stand. Es wurde keine Datei gelöscht. Kein App-Code
und keine Repository-Datei wurde durch diesen Teilauftrag geändert.
'''
(QA/'QA_ABSCHLUSS.md').write_text(report,encoding='utf-8')

manifest=ROOT/'50_Ablage/QA/Dokumentation/MANIFEST_SHA256.csv'
preserve(manifest)
old_rows={r['NewRelativePath'].replace('\\','/'):r for r in csv.DictReader(manifest.open(encoding='utf-8-sig'))}
rows=[]
for p in sorted(manifest.parent.rglob('*')):
    if not p.is_file() or p==manifest:continue
    rel=p.relative_to(ROOT).as_posix()
    old=old_rows.get(rel,{})
    rows.append({'OriginalRootFolder':old.get('OriginalRootFolder','Konsolidierung_3.2.0'),'OriginalRelativePath':old.get('OriginalRelativePath',p.relative_to(manifest.parent).as_posix()),'NewRelativePath':rel,'Bytes':p.stat().st_size,'SHA256':hashlib.sha256(p.read_bytes()).hexdigest().upper()})
with manifest.open('w',encoding='utf-8-sig',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=['OriginalRootFolder','OriginalRelativePath','NewRelativePath','Bytes','SHA256'])
    writer.writeheader();writer.writerows(rows)
for row in rows:
    p=ROOT/row['NewRelativePath'];assert p.exists() and hashlib.sha256(p.read_bytes()).hexdigest().upper()==row['SHA256']
print(json.dumps({'pages':22,'navigation_targets':nav,'structure_counts':counts,'preserved_parts':len(revision['preserved_parts']),'archive_records':len(ledger),'qa_manifest_files':len(rows),'docx_sha256':revision['output_sha256']},ensure_ascii=False))
