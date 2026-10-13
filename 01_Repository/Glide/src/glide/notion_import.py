"""Ausdrücklich gewählte Notion-Seiten ohne Tk und ohne Bestandsmutation planen."""
import copy
from dataclasses import dataclass
import hashlib
import mimetypes
from pathlib import PurePosixPath
import uuid

import notion_archive as archive
import notion_hierarchy as hierarchy
import notion_reimport as reimport
import object_references as objects
import page_restore
import source_metadata
import task_references as tasks


@dataclass(frozen=True)
class Selection:
    rows: tuple
    page_ids: tuple
    folders: object
    assets: tuple
    source_paths: tuple
    current_hash: str
    losses: tuple
    report_id: str
    report_asset_id: str


@dataclass(frozen=True)
class Content:
    lists: tuple
    folders: tuple
    trash: tuple
    imported_ids: tuple
    report_id: str
    current_hash: str


def select(current, export, comparison, selected_keys, overwrite_keys, original_bytes, *,
           target_folder_id=None, max_depth=5, new_id=None):
    """Nur auswählbare Zeilen; Kennungen und Ordner vor dem Dateikopieren festlegen."""
    rows = reimport.selected_changes(comparison, selected_keys, overwrite_keys)
    if not rows:
        raise ValueError('Keine Seite zur Übernahme ausgewählt.')
    if not isinstance(original_bytes, bytes) or len(original_bytes) > archive.MAX_ARCHIVE_BYTES:
        raise ValueError('Ungültiges oder zu großes Originalarchiv.')
    if tuple(row.page for row in comparison.rows) != export.pages:
        raise ValueError('Der Vergleich gehört nicht zu diesem Export.')
    records = source_metadata.records(current.get('lists', []))
    by_key = {record.key: record for record in records}
    occupied = {identity for _kind, identity in objects.nodes(current.get('lists', []), current.get('trash', []))}
    occupied.update(value['id'] for value in current.get('folders', []))
    occupied.update(value['id'] for value in current.get('trash', []))
    factory = new_id or (lambda: uuid.uuid4().hex)
    def fresh():
        for _attempt in range(100):
            value = factory()
            if (isinstance(value, str) and 1 <= len(value) <= 64 and value not in occupied
                    and all(c.isascii() and (c.isalnum() or c in '_-') for c in value)):
                occupied.add(value)
                return value
        raise ValueError('Keine freie Kennung für den Import verfügbar.')
    page_ids = {record.key: record.target_id for record in records}
    for row in rows:
        record = by_key.get(row.page.key)
        if row.status in ('changed', 'conflict'):
            if record is None or row.target_id != record.target_id:
                raise ValueError('Die gewählte Quellzuordnung ist veraltet.')
        else:
            if row.status == 'new' and record is not None:
                raise ValueError('Die Quelle ist inzwischen zugeordnet.')
            page_ids[row.page.key] = fresh()
    report_id = fresh()
    folder_plan = hierarchy.prepare([row.page for row in rows], current.get('folders', []),
        current.get('lists', []), target_folder_id=target_folder_id, max_depth=max_depth,
        new_id=fresh, occupied_ids=occupied)
    paths = sorted({path for row in rows for path in row.page.asset_paths})
    assets, source_paths = [], []
    for path in paths:
        identity = 'notion-' + hashlib.sha256(path.encode()).hexdigest()[:32]
        storage = 'attachments/' + identity + '.source'
        data = export.members[path]
        assets.append(dict(id=identity, name=PurePosixPath(path).name, storage=storage, size=len(data),
                           mime=mimetypes.guess_type(path)[0] or 'application/octet-stream'))
        source_paths.append((storage, path))
    report_asset_id = 'notion-export-' + hashlib.sha256(original_bytes).hexdigest()[:32]
    assets.append(dict(id=report_asset_id, name='Notion-Originalexport.zip',
                       storage='attachments/' + report_asset_id + '.zip',
                       size=len(original_bytes), mime='application/zip'))
    source_paths.append((assets[-1]['storage'], None))
    losses = tuple(export.losses) + archive.unresolved_links(export, page_ids)
    return Selection(tuple(rows), tuple(page_ids.items()), folder_plan, tuple(assets),
                     tuple(source_paths), page_restore.fingerprint(current), losses,
                     report_id, report_asset_id)


def content(selection, current, export, stored, *, page_factory, item_factory, folder_factory,
            now, max_trash=200, new_id=None, current_asset_hashes=None):
    """Dateien sind bereits exklusiv kopiert; derselbe Plan erzeugt einen einzigen Undo-Schritt."""
    if page_restore.fingerprint(current) != selection.current_hash:
        raise ValueError('Der Bestand hat sich geändert; bitte erneut vergleichen.')
    if set(stored) != {value['id'] for value in selection.assets}:
        raise ValueError('Die Importdateien sind nicht vollständig zugeordnet.')
    originals = {value['storage']: value for value in selection.assets}
    hashes = dict(current_asset_hashes or {})
    assets_by_path = {}
    for storage, path in selection.source_paths:
        if path is not None:
            attachment = stored[originals[storage]['id']]
            assets_by_path[path] = attachment
            hashes[attachment['id']] = hashlib.sha256(export.members[path]).hexdigest()
    ids = dict(selection.page_ids)
    folder_ids = dict(selection.folders.page_folders)
    lists = copy.deepcopy(current.get('lists', []))
    trash = copy.deepcopy(current.get('trash', []))
    occupied = {identity for _kind, identity in objects.nodes(lists, trash)}
    occupied.update(folder.identity for folder in selection.folders.folders)
    occupied.update(ids.values());occupied.add(selection.report_id)
    occupied.update(value['id'] for value in trash)
    factory = new_id or (lambda: uuid.uuid4().hex)
    def fresh():
        for _attempt in range(100):
            identity = factory()
            if (isinstance(identity, str) and 1 <= len(identity) <= 64 and identity not in occupied
                    and all(c.isascii() and (c.isalnum() or c in '_-') for c in identity)):
                occupied.add(identity)
                return identity
        raise ValueError('Keine freie Aufgaben- oder Papierkorbkennung verfügbar.')
    def new_item(text, done):
        item = item_factory(text, done=done)
        item['id'] = fresh()
        return item
    imported = []
    for row in selection.rows:
        page = row.page
        identity = ids[page.key]
        document, items = archive.bind_page_tasks(
            archive.page_document(export, page, ids, assets_by_path), new_item)
        attachments = [copy.deepcopy(assets_by_path[path]) for path in page.asset_paths]
        replacement = page_factory(page.title, list(items), list_id=identity, list_kind='page',
                                   folder_id=folder_ids[page.key], rich_note=document, attachments=attachments)
        original = next((value for value in lists if value['id'] == identity), None)
        if original is not None:
            if original.get('list_kind') != 'page':
                raise ValueError('Die Zielkennung gehört keiner Seite.')
            # Nur von Notion übernommene Inhalte ersetzen. Glide-Metadaten,
            # Titelbild und Anhänge daraus bleiben erhalten und kontrollierbar.
            retained = copy.deepcopy(original)
            retained.update({key: replacement[key] for key in
                             ('title', 'items', 'rich_note', 'folder_id', 'updated_at')})
            retained['attachments'] = attachments
            cover = retained.get('cover') or {}
            if cover.get('kind') == 'image':
                attached = next((value for value in original.get('attachments', [])
                                 if value['id'] == cover.get('attachment')), None)
                if attached is not None:
                    retained['attachments'].append(copy.deepcopy(attached))
            # Frühere Aufgaben bleiben für bestehende Verweise im Papierkorb.
            for item in original.get('items', []):
                trash.insert(0, dict(id=fresh(), kind='item', deleted_at=now, list=None, folder=None,
                    item=copy.deepcopy(item), origin_folder_id=original.get('folder_id'),
                    origin_folder_title='', origin=dict(list_id=identity, list_title=original.get('title', ''),
                                                         parent_item_id=None, index=None)))
            replacement = retained
        asset_hashes = {value['id']: hashes[value['id']] for value in replacement['attachments']
                        if value['id'] in hashes}
        # Erhaltene Glide-Dateien gehören zum Vergleich; der Aufrufer ergänzt
        # deren Hashes ausdrücklich, statt einen sauberen Stand zu erfinden.
        for value in replacement['attachments']:
            if value['id'] not in asset_hashes or len(asset_hashes[value['id']]) != 64:
                raise ValueError('Ein erhaltenes Titelbild braucht seinen aktuellen Dateihash.')
        record = reimport.SourceRecord(page.key, identity, page.source_hash,
                                       reimport.content_fingerprint(replacement, asset_hashes), page.path)
        replacement['notion_source'] = record.to_document()
        lists = [replacement if value['id'] == identity else value for value in lists]
        if original is None:
            lists.append(replacement)
        imported.append(identity)
    if len(trash) > max_trash:
        raise ValueError('Die Übernahme würde den Papierkorb kürzen; bitte zuerst Platz schaffen.')
    lines = ['Notion-Importbericht', '', f'{len(imported)} Seite(n) ausdrücklich übernommen.', '',
             'Originalexport: als ZIP-Anhang vollständig erhalten.',
             'Frühere Seitenaufgaben bleiben im Papierkorb; andere Seiten bleiben erhalten.', '',
             'Übernommene Quellen:']
    lines.extend(row.page.path for row in selection.rows)
    lines += ['', 'Verluste und offene Verweise:']
    lines.extend(f'{loss.path}: {loss.message}' for loss in selection.losses)
    if not selection.losses:
        lines.append('Keine gemeldet.')
    report = page_factory('Notion-Importbericht', [], list_id=selection.report_id, list_kind='page',
                          rich_note=dict(text='\n'.join(lines), spans=[], links={}),
                          attachments=[copy.deepcopy(stored[selection.report_asset_id])])
    lists.append(report)
    folders = copy.deepcopy(current.get('folders', []))
    folders.extend(folder_factory(folder.title, folder_id=folder.identity, parent_id=folder.parent_id,
                                 notion_source_key=folder.source_key) for folder in selection.folders.folders)
    return Content(tuple(lists), tuple(folders), tuple(trash), tuple(imported),
                   selection.report_id, selection.current_hash)


def current_sources(pages, resolve_path, *, max_bytes):
    """Lokale Dateien begrenzt vergleichen; fehlende Bytes sind ein sichtbarer Konflikt."""
    if type(max_bytes) is not int or max_bytes < 0:
        raise ValueError('Ungültige Dateiprüfgrenze.')
    source_metadata.records(pages)
    page_hashes, file_hashes, issues, total = {}, {}, [], 0
    by_storage = {}
    for page in pages:
        if not page.get('notion_source'):
            continue
        assets = [value for holder in [page, *tasks.walk(page.get('items', []))]
                  for value in holder.get('attachments', [])]
        for asset in assets:
            storage = asset['storage']
            if storage not in by_storage:
                digest = hashlib.sha256();size = 0
                try:
                    path = resolve_path(asset)
                    if not path:
                        raise OSError('Anhangspfad fehlt')
                    with open(path, 'rb') as stream:
                        while block := stream.read(128*1024):
                            size += len(block);total += len(block)
                            if total > max_bytes:
                                raise ValueError('Die Dateiprüfung überschreitet ihre Gesamtgrenze.')
                            digest.update(block)
                    by_storage[storage] = digest.hexdigest()
                    if size != asset['size']:
                        issues.append(archive.Loss(page['title'], 'local-asset-size',
                                      'Die heutige Anhangsgröße stimmt nicht mit dem gespeicherten Stand überein: '+asset['name']))
                except OSError:
                    by_storage[storage] = 'unlesbar'
                    issues.append(archive.Loss(page['title'], 'local-asset-missing',
                                  'Ein heutiger Anhang fehlt oder ist nicht lesbar: '+asset['name']))
            previous = file_hashes.get(asset['id'])
            if previous is not None and previous != by_storage[storage]:
                raise ValueError('Die heutige Anhangskennung ist nicht eindeutig.')
            file_hashes[asset['id']] = by_storage[storage]
        page_hashes[page['id']] = reimport.content_fingerprint(page, file_hashes)
    return page_hashes, file_hashes, tuple(issues)
