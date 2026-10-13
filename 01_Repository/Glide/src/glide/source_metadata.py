"""Notion-Zuordnungen beim Lesen, Kopieren und Verlegen von Anhängen erhalten."""
import copy
import hashlib
from pathlib import PurePosixPath
from notion_reimport import SourceRecord, content_fingerprint
import object_references as objects
import task_references as tasks


def normalize(document, target_id, list_kind):
    if document is None:
        return None
    record = SourceRecord.from_document(document)
    if list_kind != "page" or record.target_id != target_id:
        raise ValueError("Die Notion-Quellenzuordnung gehört nicht zu dieser Seite.")
    path = PurePosixPath(record.source_path)
    if (path.is_absolute() or "\\" in record.source_path or ".." in path.parts
            or ":" in record.source_path or any(ord(c) < 32 for c in record.source_path)):
        raise ValueError("Der Notion-Quellpfad ist kein relativer Exportpfad.")
    return record.to_document()


def records(pages):
    """Nur lebende Seiten zuordnen; Papierkorb ist kein vorhandenes Importziel."""
    result, seen_keys, seen_targets = [], set(), set()
    for page in pages:
        value = normalize(page.get("notion_source"), page.get("id"), page.get("list_kind"))
        if value is None:
            continue
        record = SourceRecord.from_document(value)
        if record.key in seen_keys or record.target_id in seen_targets:
            raise ValueError("Die Notion-Quellenzuordnung ist im Bestand nicht eindeutig.")
        seen_keys.add(record.key)
        seen_targets.add(record.target_id)
        result.append(record)
    return tuple(result)


def independent_copy(page):
    """Eine echte Seitenkopie ist kein zweites Ziel derselben Exportquelle."""
    result = copy.deepcopy(page)
    result.pop("notion_source", None)
    return result


def independent_collection(pages, folders):
    """Hinzufügen aus einer Sicherung erzeugt unabhängige neue Container."""
    pages = [independent_copy(page) for page in pages]
    folders = copy.deepcopy(folders)
    for folder in folders:
        folder.pop('notion_source_key', None)
    return pages, folders


def restored_source(page, target_id, live_pages):
    """Papierkorb-Rückkehr zuordnen, ohne eine lebende Quellseite zu verdoppeln.

    Eine neue Zielkennung ändert keine Inhalte. Die alte Inhaltsprüfsumme
    bleibt erhalten, damit geänderte Ordner, Aufgaben oder Anhänge weiterhin
    als lokale Bearbeitung erkannt werden.
    """
    source = normalize(page.get("notion_source"), page.get("id"), page.get("list_kind"))
    if source is None:
        return None
    record = SourceRecord.from_document(source)
    if any(existing.key == record.key for existing in records(live_pages)):
        return None
    return SourceRecord(record.key, target_id, record.source_hash,
                        record.local_hash, record.source_path).to_document()


def source_pages(collection):
    """Quellzuordnungen lebender Seiten und gelöschter Seiten gemeinsam erfassen."""
    lists, trash = collection
    candidates = list(lists) + [entry.get('list') for entry in trash
                               if isinstance(entry, dict)]
    return [page for page in candidates if isinstance(page, dict)
            and page.get('notion_source') is not None]


def _asset_holders(holder):
    yield holder
    for key in ('items', 'children'):
        for child in holder.get(key, []):
            yield from _asset_holders(child)


def staged_source_hashes(collection, staged_files, *, max_bytes):
    """Nur tatsächlich referenzierte Quellseiten-Dateien begrenzt prüfen."""
    if type(max_bytes) is not int or max_bytes < 0:
        raise ValueError('Ungültige Dateiprüfgrenze.')
    storages = {attachment['storage'] for page in source_pages(collection)
                for holder in _asset_holders(page) for attachment in holder.get('attachments', [])}
    result, total = {}, 0
    for storage in sorted(storages):
        path = staged_files.get(storage)
        if path is None:
            raise ValueError('Eine Datei der Quellseite fehlt im geprüften Zwischenstand.')
        digest = hashlib.sha256()
        with open(path, 'rb') as source:
            while block := source.read(128 * 1024):
                total += len(block)
                if total > max_bytes:
                    raise ValueError('Die Dateiprüfung überschreitet ihre Gesamtgrenze.')
                digest.update(block)
        result[storage] = digest.hexdigest()
    return result


def relocated(page_before, page_after, asset_hashes_before, asset_hashes_after):
    """Saubere Zuordnung nur nach reinem Anhangsumzug neu verankern.

    Der Aufrufer übergibt den tatsächlich verlegten Seitenstand und die
    vollständig gelesenen Anhangshashes. Lokale Bearbeitungen bleiben vom
    zuletzt übernommenen Stand verschieden und werden nicht sauber erklärt.
    """
    before = normalize(page_before.get("notion_source"), page_before.get("id"),
                       page_before.get("list_kind"))
    result = copy.deepcopy(page_after)
    if before is None:
        result.pop("notion_source", None)
        return result
    if (page_after.get("id") != page_before.get("id")
            or page_after.get("list_kind") != "page"):
        raise ValueError("Beim Verlegen von Anhängen wurde die Seitenkennung geändert.")
    def canonicalized(original, changed):
        result = copy.deepcopy(changed)
        old_attachments = original.get("attachments", [])
        new_attachments = result.get("attachments", [])
        if len(old_attachments) != len(new_attachments):
            raise ValueError("Die Anhänge wurden beim Verlegen verändert.")
        reverse = {}
        for old, new in zip(old_attachments, new_attachments):
            old_id, new_id = old["id"], new["id"]
            if new_id in reverse and reverse[new_id] != old_id:
                raise ValueError("Die neuen Anhangskennungen sind nicht eindeutig.")
            if (old_id not in asset_hashes_before or new_id not in asset_hashes_after
                    or asset_hashes_before[old_id] != asset_hashes_after[new_id]):
                raise ValueError("Die Anhangsbytes wurden beim Verlegen verändert oder fehlen.")
            reverse[new_id] = old_id
            new["id"], new["storage"] = old_id, old["storage"]
        document = result.get("rich_note") or {}
        for image in (document.get("images") or {}).values():
            image["attachment"] = reverse.get(image.get("attachment"), image.get("attachment"))
        cover = result.get("cover") or {}
        if cover.get("kind") == "image":
            cover["attachment"] = reverse.get(cover.get("attachment"), cover.get("attachment"))
        for key in ("items", "children"):
            old_children, new_children = original.get(key, []), result.get(key, [])
            if len(old_children) != len(new_children):
                raise ValueError("Der Seiteninhalt wurde beim Verlegen verändert.")
            if key in result:
                result[key] = [canonicalized(old, new) for old, new in zip(old_children, new_children)]
        result.pop("notion_source", None)
        return result
    canonical_before = independent_copy(page_before)
    if canonical_before != canonicalized(page_before, page_after):
        raise ValueError("Der Seiteninhalt wurde beim Verlegen von Anhängen verändert.")
    record = SourceRecord.from_document(before)
    if content_fingerprint(page_before, asset_hashes_before) == record.local_hash:
        record = SourceRecord(record.key, record.target_id, record.source_hash,
                              content_fingerprint(result, asset_hashes_after), record.source_path)
    result["notion_source"] = record.to_document()
    return result


def relocated_collections(before, after, storage_hashes_before, storage_hashes_after):
    """Vollrestore: lebende Seiten und Papierkorb nach Dateiumzug neu verankern.

    `before` und `after` sind jeweils (Listen, Papierkorb). Die Inhaltsprüfung
    berücksichtigt auch Anhänge an Seitenaufgaben. Keine Eingabe wird verändert.
    """
    def asset_hashes(page, stored):
        result = {}
        for holder in _asset_holders(page):
            for attachment in holder.get('attachments', []):
                identity, storage = attachment['id'], attachment['storage']
                if storage not in stored:
                    raise ValueError('Die geprüften Dateibytes einer Quellseite fehlen.')
                digest = stored[storage]
                if identity in result and result[identity] != digest:
                    raise ValueError('Eine Anhangskennung bezeichnet unterschiedliche Dateibytes.')
                result[identity] = digest
        return result

    result = copy.deepcopy(after)
    originals, changed = source_pages(before), source_pages(result)
    if len(originals) != len(changed):
        raise ValueError('Die Quellseiten wurden während des Dateiumzugs verändert.')
    for original, page in zip(originals, changed):
        updated = relocated(original, page, asset_hashes(original, storage_hashes_before),
                            asset_hashes(page, storage_hashes_after))
        page.clear()
        page.update(updated)
    return result


def selectively_restored(original, restored, asset_hashes_before, asset_hashes_after,
                         live_pages, remapped_items=()):
    """Quellbindung beim Einzelrestore erhalten, technische ID-Wechsel prüfen.

    Andere lebende Ziele derselben Quelle behalten Vorrang. Eigene Änderungen
    der gesicherten Seite bleiben Konflikte; eine geänderte heutige Einordnung
    zählt weiterhin als lokale Bearbeitung.
    """
    result = copy.deepcopy(restored)
    if original.get('id') != restored.get('id'):
        raise ValueError('Die Seitenkennung darf beim Einzelrestore nicht wechseln.')
    mapping = restored_source(original, restored['id'],
                              [page for page in live_pages if page.get('id') != restored['id']])
    if mapping is None:
        result.pop('notion_source', None)
        return result
    pairs = tuple(remapped_items)
    reverse = {new: old for old, new in pairs}
    if (len(reverse) != len(pairs) or len({old for old, _new in pairs}) != len(pairs)
            or set(reverse).intersection(reverse.values())):
        raise ValueError('Die Aufgabenkennungen wurden nicht eindeutig umgelegt.')
    canonical = copy.deepcopy(result)
    if 'folder_id' in original:
        canonical['folder_id'] = original['folder_id']
    else:
        canonical.pop('folder_id', None)
    for item in tasks.walk(canonical.get('items', [])):
        item['id'] = reverse.get(item['id'], item['id'])
        for field in ('links', 'blocked_by'):
            if field in item:
                item[field] = [reverse.get(identity, identity) for identity in item[field]]
        objects.remap_holder(item, {}, reverse)
    tasks.remap(canonical.get('rich_note'), reverse)
    objects.remap_holder(canonical, {}, reverse)
    canonical['notion_source'] = mapping
    # Prüft Inhalt und Dateibytes streng, bevor eine saubere Prüfsumme umzieht.
    relocated(original, canonical, asset_hashes_before, asset_hashes_after)
    record = SourceRecord.from_document(mapping)
    if (content_fingerprint(original, asset_hashes_before) == record.local_hash
            and result.get('folder_id') == original.get('folder_id')):
        record = SourceRecord(record.key, record.target_id, record.source_hash,
                              content_fingerprint(result, asset_hashes_after), record.source_path)
    result['notion_source'] = record.to_document()
    return result
