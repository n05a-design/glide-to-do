"""Lesbarer Gesamtexport (FP-07/1), ausschließlich Standardbibliothek und ohne Tk.

Der fertige Zielordner entsteht erst durch Umbenennen eines vollständigen
Geschwisterordners. Bestehende Ziele und Quelldateien werden nie überschrieben.
INVENTAR.json erhält zusätzlich sämtliche übergebenen Objektfelder; dies ist
kein Glide-Sicherungsformat und kein Versprechen eines Wiederimports.
"""
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from urllib.parse import quote

import object_references as objects
import page_markdown
import drawing
import task_references


class ExportCancelled(Exception):
    """Bewusster Abbruch, bevor der fertige Ordner veröffentlicht wurde."""


def label(value):
    """Objektnamen bleiben auch mit Markdownzeichen ein einzelner Linktext."""
    return ''.join('\\'+c if c in '\\`*_[]()' else c for c in ' '.join(str(value).split()))


def filename(title, identity, suffix=""):
    suffix = re.sub(r'[^A-Za-z0-9.]', '_', suffix)[:12]
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', str(title or 'Ohne Titel'))
    name = re.sub(r'\s+', ' ', name).strip(' .')[:40].rstrip(' .') or 'Ohne Titel'
    # Auch CON.txt oder gleiche Titel auf einem anderen Dateisystem sind sicher.
    tag = hashlib.sha256(str(identity).encode('utf-8')).hexdigest()[:12]
    return f'_{name}-{tag}{suffix}'


def write_tree(snapshot, target, data_root, *, cancel=None):
    """Snapshot ohne Mutation ausgeben; Ziel muss neu sein, jeder Pfad <=240.

    Fehlende/unsichere Anhänge und Verweise stehen mit Objektkennung im Bericht.
    Ein Schreibfehler/Abbruch verwirft ausschließlich den eigenen Stagingordner.
    """
    snapshot = copy.deepcopy(snapshot)
    target = Path(target).absolute()
    data_root = Path(data_root).absolute()
    if target.exists() or target.is_symlink():
        raise FileExistsError('Der Ausgabeordner existiert bereits.')
    if not target.parent.is_dir():
        raise ValueError('Der übergeordnete Ausgabeordner fehlt.')
    if len(str(target)) > 130:
        raise ValueError('Bitte einen kürzeren Ausgabeort wählen (höchstens 130 Zeichen).')
    if target.resolve() == data_root.resolve() or data_root.resolve() in target.resolve().parents:
        raise ValueError('Die Ausgabe muss außerhalb der Glide-Datenablage liegen.')
    losses = []
    inventory = {'format': 'Glide-Markdown-Inventar', 'version': 1,
                 'objekte': [], 'anhaenge': [], 'hinweise': losses, 'bestand': snapshot}
    paths, folder_paths, attachment_paths, attachment_records, attachment_digests = {}, {}, {}, {}, {}
    lists, folders = snapshot.get('lists', []), snapshot.get('folders', [])
    holders = []
    seen = set()

    def check():
        if cancel is not None and cancel.is_set():
            raise ExportCancelled('Ausgabe abgebrochen.')

    def note(kind, owner, field, detail):
        losses.append({'art': kind, 'objekt': owner, 'feld': field, 'detail': detail})

    def bounded(relative, title, identity, suffix):
        if len(str(target / relative)) > 240:
            relative = Path('_Lange_Pfade') / filename(title, identity, suffix)
            note('pfad', identity, 'folder_id', 'Langer Ordnerpfad in _Lange_Pfade abgeflacht.')
        return relative

    by_folder = {f['id']: f for f in folders}
    if len(by_folder) != len(folders):
        raise ValueError('Doppelte Ordnerkennungen.')

    def folder_path(identity, trail=()):
        if identity in folder_paths:
            return folder_paths[identity]
        folder = by_folder.get(identity)
        if folder is None:
            return Path()
        if identity in trail:
            note('ordner', identity, 'parent_id', 'Zyklische Ordnerzuordnung; an Wurzel ausgegeben.')
            return Path()
        parent = folder.get('parent_id')
        if parent and parent not in by_folder:
            note('ordner', identity, 'parent_id', 'Übergeordneter Ordner fehlt.')
        base = folder_path(parent, (*trail, identity))
        relative = bounded(base / filename(folder.get('title'), 'folder:'+identity),
                           folder.get('title'), 'folder:'+identity, '')
        # Reserviert auch Platz für die Dateien innerhalb dieses Ordners.
        if len(str(target/relative)) > 175:
            relative = Path('_Lange_Pfade') / filename(folder.get('title'), 'folder:'+identity)
            note('pfad', identity, 'parent_id', 'Tiefer Ordnerbaum abgeflacht.')
        folder_paths[identity] = relative
        return relative

    def register(kind, holder, relative):
        key = kind, holder.get('id')
        if not isinstance(key[1], str) or not key[1] or key in seen:
            raise ValueError('Fehlende oder doppelte Objektkennung.')
        seen.add(key)
        paths[key] = relative
        holders.append((kind, holder, relative))
        inventory['objekte'].append({'art': kind, 'id': key[1], 'datei': relative.as_posix()})

    for folder in folders:
        register('folder', folder, folder_path(folder['id'])/'INDEX.md')
    for entry in lists:
        parent = entry.get('folder_id')
        if parent and parent not in by_folder:
            note('ordner', entry.get('id'), 'folder_id', 'Heimatordner fehlt; an Wurzel ausgegeben.')
        relative = bounded(folder_path(parent)/filename(entry.get('title'), entry.get('id'), '.md'),
                           entry.get('title'), entry.get('id'), '.md')
        register('list', entry, relative)
        for item in objects.walk(entry.get('items', [])):
            key = 'item', item.get('id')
            if not isinstance(key[1], str) or not key[1] or key in seen:
                raise ValueError('Fehlende oder doppelte Punktkennung.')
            seen.add(key)
            paths[key] = Path(relative.as_posix()+'#punkt-'+quote(key[1], safe=''))
            inventory['objekte'].append({'art': 'item', 'id': key[1], 'datei': str(paths[key]).replace('\\', '/')})

    stage = Path(tempfile.mkdtemp(prefix='.glide-md-', dir=target.parent))
    try:
        def output(relative, content):
            check()
            path = stage/relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8', newline='\n')

        def digest_file(path):
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    check();digest.update(chunk)
            return digest.hexdigest()

        def link(source, destination):
            raw, _, anchor = str(destination).replace('\\', '/').partition('#')
            value = os.path.relpath(stage/raw, (stage/source).parent).replace('\\', '/')
            return quote(value, safe='/.-_')+('#'+anchor if anchor else '')

        def rewrite(text, source, owner):
            def replace(match):
                key = objects.parse(match.group(0))
                if key in paths:
                    relative = link(source, paths[key])
                    return relative if part[max(0, match.start()-2):match.start()] == '](' else f'[Verweis]({relative})'
                note('verweis', owner, 'references', 'Ziel fehlt: '+match.group(0))
                return match.group(0)
            result = []
            # Code ist wörtlicher Inhalt; dort stehende URI-Beispiele sind
            # keine aufzuschlüsselnden Objektverweise.
            for index, part in enumerate(re.split(r'(```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`)', text)):
                result.append(part if index % 2 else re.sub(
                    r'glide://(?:list|item)/[^\s)<>\]"\x00-\x1f]+', replace, part))
            return ''.join(result)

        def attachment(holder, value, relative):
            owner = holder['id']
            storage = value.get('storage')
            record_key = owner, value.get('id'), storage
            if record_key in attachment_records:
                record = attachment_records[record_key]
                return link(relative, record['datei']) if record['status'] == 'kopiert' else None
            record = {'objekt': owner, 'id': value.get('id'), 'name': value.get('name'), 'status': 'fehlt'}
            attachment_records[record_key] = record
            inventory['anhaenge'].append(record)
            parts = storage.replace('\\', '/').split('/') if isinstance(storage, str) else []
            if (not parts or parts[0] != 'attachments' or any(p in ('', '.', '..') for p in parts)
                    or any(':' in p for p in parts)):
                note('anhang', owner, str(value.get('id')), 'Ungültiger Ablagepfad.')
                return None
            source = data_root.joinpath(*parts)
            if any(p.is_symlink() or p.is_junction() for p in (source, *source.parents)):
                note('anhang', owner, str(value.get('id')), 'Symlink/Junction wird nicht verfolgt.')
                return None
            if not source.is_file():
                note('anhang', owner, str(value.get('id')), 'Datei fehlt.')
                return None
            dest = attachment_paths.get(storage)
            if dest is None:
                dest = Path('_Anhaenge')/filename(value.get('name'), storage, Path(value.get('name') or '').suffix[:12])
                attachment_paths[storage] = dest
                path = stage/dest;path.parent.mkdir(parents=True, exist_ok=True)
                digest = hashlib.sha256()
                with source.open('rb') as src, path.open('xb') as dst:
                    before = os.fstat(src.fileno())
                    while data := src.read(1024*1024):
                        check();dst.write(data);digest.update(data)
                    after = os.fstat(src.fileno())
                    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                        raise OSError('Eine Anhangsdatei wurde während der Ausgabe verändert.')
                record['sha256'] = digest.hexdigest()
                attachment_digests[storage] = record['sha256']
            else:
                record['sha256'] = attachment_digests[storage]
            record.update(datei=dest.as_posix(), status='kopiert')
            return link(relative, dest)

        labels = {v['id']: str(v.get('name') or v['id']) for v in snapshot.get('labels', [])}
        readable = {'id', 'title', 'text', 'kind', 'list_kind', 'note', 'description', 'done', 'children',
                    'items', 'attachments', 'rich_note', 'folder_id', 'parent_id', 'references', 'links',
                    'live_lists', 'labels', 'archived', 'due', 'due_time', 'planned_date', 'planned_time',
                    'importance', 'estimate_minutes'}

        def metadata(holder):
            return '\n'.join(f'- {key}: {json.dumps(holder[key], ensure_ascii=False)}' for key in (
                'id', 'kind', 'list_kind', 'archived', 'due', 'due_time', 'planned_date',
                'planned_time', 'importance', 'estimate_minutes') if key in holder)

        def details(holder, relative):
            result = []
            if holder.get('labels'):
                result.append('Labels: '+', '.join(label(labels.get(v, v)) for v in holder['labels']))
            for value in holder.get('attachments', []):
                ref = attachment(holder, value, relative)
                name = label(value.get('name') or 'Anhang')
                image = Path(name).suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg')
                result.append(('!' if image else '')+f'[{name}]({ref})' if ref else 'Fehlender Anhang: '+name)
            for field in ('references', 'live_lists'):
                for uri in holder.get(field, []):
                    key = objects.parse(uri)
                    result.append(f'[Verweis]({link(relative, paths[key])})' if key in paths else 'Verweisziel fehlt: '+uri)
                    if key not in paths:note('verweis', holder['id'], field, uri)
            for identity in holder.get('links', []):
                key = 'item', identity
                result.append(f'[Aufgabe]({link(relative, paths[key])})' if key in paths else 'Aufgabenziel fehlt: '+identity)
                if key not in paths:note('verweis', holder['id'], 'links', identity)
            for field, value in holder.items():
                if field not in readable and value not in (None, '', [], {}, False):
                    note('darstellung', holder['id'], field,
                         'Im Inventar vollständig erhalten; in Markdown ohne ausführbares Glide-Verhalten.')
            return result

        task_count = 0
        for kind, holder, relative in holders:
            check()
            lines = ['# '+label(holder.get('title') or 'Ohne Titel'), '', metadata(holder), '']
            lines += [str(holder.get('note') or ''), str(holder.get('description') or ''), '']
            doc = holder.get('rich_note')
            if isinstance(doc, dict) and doc.get('text'):
                if doc.get('spans'):
                    note('darstellung', holder['id'], 'rich_note.spans',
                         'Markdown bildet Grundformate ab; vollständige Formatbereiche und Klappzustände im Inventar.')
                by_id = {i['id']: i for i in objects.walk(holder.get('items', []))}
                body_doc = copy.deepcopy(doc)
                reference_spans = []
                for span in body_doc.get('spans', []):
                    identity = task_references.task_id(span.get('tag'))
                    if identity:
                        if ('item', identity) in paths:
                            reference_spans.append(span)
                            body_doc.setdefault('links', {})[span['tag']] = objects.uri('item', identity)
                        else:
                            note('verweis', holder['id'], 'rich_note.spans', 'Aufgabenziel fehlt: '+identity)
                # Jede Aufgabe bekommt unten genau eine Checkbox und einen Anker.
                # Ihre eingebetteten Vorkommen bleiben Verweise auf dieses Original.
                body_doc['spans'] = [s for s in body_doc.get('spans', [])
                    if s.get('tag') != 'task' or not any(
                        r['start'] < s['end'] and r['end'] > s['start'] for r in reference_spans)]
                image_map = {a.get('id'): a for a in holder.get('attachments', [])}
                # Anhänge werden unten einmal kopiert. Bildverweise verwenden dieselben Dateien.
                def image_source(info):
                    value = image_map.get(info.get('attachment'))
                    if value is None:
                        note('anhang', holder['id'], str(info.get('attachment')), 'Bildkennung fehlt.')
                        return 'Fehlendes Seitenbild', ''
                    return str(value.get('name') or 'Bild'), attachment(holder, value, relative) or ''
                lines.append(page_markdown.page_to_markdown(body_doc,
                    task_state=lambda identity: (by_id[identity]['text'], by_id[identity].get('done')) if identity in by_id else None,
                    image_source=image_source))
                table_rows = [line for line in doc['text'].splitlines() if line.strip().startswith('|')]
                if table_rows:
                    table_path = relative.with_name(relative.stem+'.tabellen.csv')
                    (stage/table_path).parent.mkdir(parents=True, exist_ok=True)
                    with (stage/table_path).open('w', encoding='utf-8-sig', newline='') as stream:
                        writer = csv.writer(stream)
                        for line in table_rows:
                            if not re.fullmatch(r'[\s|:\-]+', line):
                                writer.writerow([v.strip() for v in line.strip().strip('|').split('|')])
                    lines.append(f'[Tabellen als CSV]({link(relative, table_path)})')
            if holder.get('drawing'):
                picture = relative.with_suffix('.png')
                (stage/picture).parent.mkdir(parents=True, exist_ok=True)
                (stage/picture).write_bytes(drawing.DrawingModel.from_document(holder['drawing']).to_png())
                lines.append(f'![Zeichnung]({link(relative, picture)})')
            lines += details(holder, relative)
            rows = []
            def items(values, depth=0):
                nonlocal task_count
                for item in values:
                    prefix = '  '*depth
                    marker = f'- [{"x" if item.get("done") else " "}] ' if item.get('kind', 'task') == 'task' else '- '
                    lines.extend(['', f'<a id="punkt-{quote(item["id"], safe="")}"></a>',
                                  prefix+marker+label(item.get('text') or ''),
                                  metadata(item), str(item.get('description') or '')])
                    lines.extend(details(item, relative))
                    rows.append(item)
                    if item.get('kind', 'task') == 'task':task_count += 1
                    items(item.get('children', []), depth+1)
            items(holder.get('items', []))
            if kind == 'folder':
                for child_kind, child, child_path in holders:
                    if (child_kind == 'folder' and child.get('parent_id') == holder['id'] or
                            child_kind == 'list' and child.get('folder_id') == holder['id']):
                        lines.append(f'- [{label(child.get("title") or "Ohne Titel")}]({link(relative, child_path)})')
            output(relative, rewrite('\n'.join(lines)+'\n', relative, holder['id']))
            if rows:
                path = relative.with_suffix('.csv')
                (stage/path).parent.mkdir(parents=True, exist_ok=True)
                with (stage/path).open('w', encoding='utf-8-sig', newline='') as stream:
                    fields = ['id', 'text', 'done', 'due', 'due_time', 'planned_date', 'planned_time',
                              'importance', 'estimate_minutes', 'description', 'labels', 'kind']
                    writer = csv.DictWriter(stream, fieldnames=fields, extrasaction='ignore')
                    writer.writeheader()
                    for item in rows:
                        check();writer.writerow({key: json.dumps(item.get(key), ensure_ascii=False) for key in fields})
        if snapshot.get('trash'):
            note('darstellung', 'bestand', 'trash', 'Papierkorb vollständig im Inventar, außerhalb der aktiven Markdownstruktur.')
            output(Path('Papierkorb.md'), '# Papierkorb\n\nVollständige abgelegte Objekte, keine aktiven Aufgaben:\n\n```json\n'
                   +json.dumps(snapshot['trash'], ensure_ascii=False, indent=2)+'\n```\n')
        if snapshot.get('pinboards'):
            note('darstellung', 'bestand', 'pinboards', 'Layout und Verbindungen im Inventar; keine interaktive Pinnwand in Markdown.')
        inventory['zaehlung'] = {'listen_seiten': len(lists), 'ordner': len(folders), 'aufgaben': task_count,
                                'anhangverweise': len(inventory['anhaenge']),
                                'anhangdateien': len(attachment_paths)}
        output(Path('INVENTAR.json'), json.dumps(inventory, ensure_ascii=False, indent=2)+'\n')
        index = ['# Glide – Gesamtausgabe', '', 'Lesbarer Export; kein garantiert rückimportierbares Backup.',
                 'Zur vollständigen Wiederherstellung die Glide-App-Sicherung verwenden.', '',
                 json.dumps(inventory['zaehlung'], ensure_ascii=False), '', '## Inhalt', '']
        index += [f'- [{label(h.get("title") or "Ohne Titel")}]({link(Path("INDEX.md"), p)})' for _, h, p in holders]
        index += ['', '## Erhalt und Grenzen', '',
                  'Objektfelder, Papierkorb und Pinnwanddaten stehen vollständig in INVENTAR.json.',
                  'Wiederholungen, Erinnerungen, Zeichnungen/Animationen, Darstellung und Bedienzustände',
                  'haben im Markdown kein ausführbares Verhalten. Nicht dargestellte Felder sind einzeln zugeordnet.', '']
        index += [f'- {v["objekt"]} · {v["feld"]}: {v["detail"]}' for v in losses]
        output(Path('INDEX.md'), '\n'.join(index)+'\n')
        manifest = {p.relative_to(stage).as_posix(): digest_file(p)
                    for p in sorted(stage.rglob('*')) if p.is_file()}
        output(Path('MANIFEST.json'), json.dumps({'sha256': manifest}, ensure_ascii=False, indent=2)+'\n')
        check()
        # Eigener Claim serialisiert Glide-Exporte desselben Ziels. Auf Windows
        # verweigert rename zusätzlich jedes inzwischen angelegte fremde Ziel.
        claim = target.parent/('.glide-md-'+hashlib.sha256(target.name.encode()).hexdigest()[:16]+'.lock')
        fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            os.close(fd)
            if target.exists() or target.is_symlink():
                raise FileExistsError('Der Ausgabeordner wurde inzwischen angelegt.')
            check()
            os.rename(stage, target)
        finally:
            claim.unlink()
        return {'zaehlung': inventory['zaehlung'], 'hinweise': losses, 'dateien': len(manifest)+1}
    finally:
        if stage.exists():
            shutil.rmtree(stage)
