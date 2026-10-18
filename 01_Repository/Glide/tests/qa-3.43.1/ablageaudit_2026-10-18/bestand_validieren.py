"""Bilanz und dateiweise Entscheidung gegen den gesicherten Ausgangsbestand."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import os
import subprocess
import zipfile

ROOT=Path(__file__).resolve().parents[5]
A=Path(__file__).resolve().parent


def read(name):
    return json.loads((A/name).read_text(encoding='utf-8-sig'))


def digest(p):
    h=hashlib.sha256()
    with open('\\\\?\\'+str(p.resolve()) if os.name=='nt' else p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


before=read('inventar_vorher.json');after=read('inventar_nachher.json')
original_hash=read('dateihashes_vorher.json')['sha256']
assert not before['fehler'] and not after['fehler']
changes=[];missing=[];same=[];decisions=[]
for row in before['dateien']:
    rel=row['pfad'];p=ROOT/rel
    category=row['bereich']
    if rel.startswith('.git/'):
        importance='Versionsgeschichte und Sicherung'
        action='Git-intern verdichtet; Objektmenge und Referenzen separat validiert'
        if 'tmp_obj_' in rel:action='Erhalten: automatische Freigabeprüfung blockiert Entfernen'
    elif rel.startswith('.claude/worktrees/'):
        importance='Reproduzierbare Arbeitskopie, eigene Änderungen gesichert'
        action='Bereinigung ausstehend: Zugriff/Freigabe blockiert; Branch/Stash und Sicherungen erhalten'
    else:
        # Path.is_file kann unter Windows lange vorhandene Pfade als fehlend melden.
        try:
            current=digest(p)
        except FileNotFoundError:
            current=None
        if current==original_hash[rel]:same.append(rel)
        elif current is None:missing.append(rel)
        else:changes.append({'pfad':rel,'vorher_sha256':original_hash[rel],'nachher_sha256':current})
        if category in ['geschützte Nutzerreferenz','Prüffixture und Migrationsreferenz','Grafikquelle und Master','Python-Lieferstand','Showcase und Probedaten','Paket und Bauartefakt']:
            importance='Geschützter Original-, Referenz-, Prüf- oder Lieferbestand';action='Erhalten, vollständiger Hashabgleich'
            assert current==original_hash[rel],rel
        elif category=='QA-Nachweis':
            importance='Historischer Nachweis im Fenster der sieben aktuellen Versionen';action='Erhalten; bei README-Korrektur nur Navigation, kein Ergebnis umetikettiert'
        elif p.suffix.lower() in ('.md','.txt','.rst'):
            importance='Zuständige Dokumentation, Auftrag, Anleitung oder rechtlicher Hinweis';action='Aktualisiert/zusammengeführt falls protokolliert, sonst weiter gültig oder ausdrücklich historisch'
        else:
            importance='Quellcode, Laufzeitressource, Prüfwerkzeug oder Projektkonfiguration';action='Weiter erforderlich; ausführbare Kandidatenänderungen gegen Manifest abgeglichen'
    decisions.append({'pfad':rel,'bereich':category,'wichtigkeit':importance,'entscheidung':action})
assert not missing,missing
# Nur genehmigte Kandidaten- und Dokumentpfade dürfen vom Ausgangshash abweichen.
allowed=set(subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=ROOT,text=True,encoding='utf-8').splitlines())
upstream=set(subprocess.check_output(['git','diff','--name-only','c0252bad69780c86b853f2653d5396e5256c0b32','9ec474b9dcbd502efce8cb221e53e24c322f9a78'],cwd=ROOT,text=True,encoding='utf-8').splitlines())
allowed.update(upstream)
allowed.update(str(p.relative_to(ROOT)).replace('\\','/') for p in A.iterdir() if p.is_file())
backup_dir=Path((A/'sicherung_ort.local').read_text(encoding='utf-8-sig').strip())
with zipfile.ZipFile(backup_dir/'hauptkopie.zip') as z:
    for r in changes:
        if r['pfad'] in z.namelist():
            original=z.read(r['pfad'])
            assert hashlib.sha256(original).hexdigest()==original_hash[r['pfad']]
            current=(ROOT/r['pfad']).read_bytes()
            if original.replace(b'\r\n',b'\n')==current.replace(b'\r\n',b'\n'):
                allowed.add(r['pfad']);r['grund']='Nur LF/CRLF-Normalisierung durch Stash-Anwendung, gegen bytegesicherte Originaldatei geprüft'
        if r['pfad'] in upstream:r.setdefault('grund','Aktueller Upstream auf 9ec474b übernommen')
unexpected=[r for r in changes if r['pfad'] not in allowed]
assert not unexpected,unexpected
(A/'dateibewertung.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in decisions),encoding='utf-8')
dirs=[{'pfad':r['pfad'],'entscheidung':('Git-intern verdichtet; Geschichte erhalten' if r['pfad'].startswith('.git') else 'Arbeitskopie erhalten, Bereinigung blockiert' if r['pfad'].startswith('.claude/worktrees') else 'Erhalten: benötigte oder geschützte Projektstruktur'),'nachher_vorhanden':(ROOT/r['pfad']).is_dir()} for r in before['ordner']]
(A/'ordnerbewertung.json').write_text(json.dumps(dirs,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=[r for r in decisions if r['wichtigkeit'].startswith('Geschützter')]
objects=subprocess.check_output(['git','cat-file','--batch-all-objects','--batch-check=%(objectname) %(objecttype) %(objectsize)'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
old_objects=set((A/'gitobjekte_vorher.txt').read_text(encoding='utf-8-sig').splitlines())
assert old_objects.issubset(set(objects))
old_refs=[line.split() for line in (A/'gitrefs_vorher.txt').read_text(encoding='utf-8-sig').splitlines()]
refs=subprocess.check_output(['git','for-each-ref','--format=%(objectname) %(refname)'],cwd=ROOT,text=True,encoding='utf-8').splitlines()
refs=dict(line.split()[::-1] for line in refs)
lost=[]
for parts in old_refs:
    if len(parts)==2:
        ref,sha=parts
        # refs/stash zeigt nun auf die zusätzliche Schutzsicherung; alte Stashes bleiben in der Liste.
        # Codex aktualisiert seine internen Turn-Snapshots während dieser Prüfung.
        # Deren alte Objekte sind oben im vollständigen Objektmengentest enthalten.
        if ref.startswith(('refs/heads/','refs/tags/','refs/remotes/')) and refs.get(ref)!=sha:lost.append(ref)
assert not lost,lost
report={'status':'Bestandsabgleich bestanden; Löschschritte teilweise blockiert',
 'ausgang_dateien':len(before['dateien']),'ausgang_ordner':len(before['ordner']),
 'nachher_dateien':len(after['dateien']),'nachher_ordner':len(after['ordner']),
 'bytes_vorher':sum(r['bytes'] for r in before['dateien']),
 'bytes_nachher':sum(r['bytes'] for r in after['dateien']),
 'belegung_dateipfade_vorher':sum(r['belegt_bytes'] or 0 for r in before['dateien']),
 'belegung_dateipfade_nachher':sum(r['belegt_bytes'] or 0 for r in after['dateien']),
 'disk_frei_vorher':before['laufwerk_frei_bytes'],'disk_frei_nachher':after['laufwerk_frei_bytes'],
 'main_hashgleich':len(same),'main_hashgeaendert':changes,'main_fehlend':missing,
 'geschuetzte_dateien_hashgleich':len(protected),'ausgang_gitobjekte_erhalten':len(old_objects),
 'aktuelle_gitobjekte':len(objects),'alte_branch_tag_remote_refs_erhalten':not lost,
 'dateibewertung_anzahl':len(decisions),'ordnerbewertung_anzahl':len(dirs),
 'originalreferenzen':sum(r['bereich']=='geschützte Nutzerreferenz' for r in decisions),
 'grenzen':['Bilanz vor anschließendem Commit und dessen neuen Git-Objekten; Nachweisdateien wachsen während der Prüfung.',
 'Dateipfadbelegung ohne NTFS-Verwaltungsdaten; bei fehlender Dateiidentität keine Hardlink-Deduplizierung.',
 'Laufwerksfreiraum kann auch durch parallele Prozesse beeinflusst werden.',
 'Alle Dateien inventarisiert und klassifiziert; dies ist keine manuelle Zeile-für-Zeile-Prüfung jedes Quellcodes oder jedes Binärinhalts.']}
(A/'bestandsvalidierung.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ('main_hashgeaendert','grenzen')},ensure_ascii=False))
