"""Aufgabenmarken, Heimat und Textquellen ohne Tk (Format 21)."""
import re


TASK_TAG = re.compile(r'^(item|taskref):([A-Za-z0-9_-]{1,64})$')


def task_id(tag, *, owned=False):
    match = TASK_TAG.fullmatch(tag) if isinstance(tag, str) else None
    return match.group(2) if match and (not owned or match.group(1) == 'item') else None


def walk(items):
    for item in items or []:
        yield item
        yield from walk(item.get('children', []))


def document_ids(document, *, owned=False):
    return {identity for span in (document or {}).get('spans', [])
            if (identity := task_id(span.get('tag'), owned=owned))}


def sources(lists, *, pages_only=False):
    """Textquellen und Heimatseiten, ohne archivierte Dokumente."""
    result = {}
    targets = {item['id']: item for entry in lists for item in walk(entry.get('items', []))}
    for entry in lists:
        kind = entry.get('list_kind', 'tasks')
        if entry.get('archived') or kind not in ('page', 'note') or (pages_only and kind != 'page'):
            continue
        identities = document_ids(entry.get('rich_note'))
        identities.update(item['id'] for item in walk(entry.get('items', [])))
        identities.update(child['id'] for identity in list(identities)
                          for child in walk(targets.get(identity, {}).get('children', [])))
        for identity in identities:
            result.setdefault(identity, []).append(entry['id'])
    return result


def reference_document(document, identities):
    """Nach Heimatwechsel bleibt die Zeile ein Verweis; Bilder/Formate bleiben."""
    identities = set(identities)
    return dict(document, spans=[dict(span, tag='taskref:' + identity)
                if span.get('tag', '').startswith('item:')
                and (identity := task_id(span['tag'])) in identities else dict(span)
                for span in document.get('spans', [])])


def remap(document, mapping):
    for span in (document or {}).get('spans', []):
        identity = task_id(span.get('tag'))
        if identity in mapping:
            span['tag'] = span['tag'].split(':', 1)[0] + ':' + mapping[identity]


def text_titles(document):
    text = (document or {}).get('text', '')
    result, seen = {}, set()
    for span in (document or {}).get('spans', []):
        identity = task_id(span.get('tag'))
        if not identity:
            continue
        start = span['start']
        while start < span['end']:
            end = text.find('\n', start)
            end = len(text) if end < 0 else end
            title = ' '.join(text[start:min(end, span['end'])].split())
            if title and (identity, start) not in seen:
                result.setdefault(identity, []).append(title)
                seen.add((identity, start))
            start = end + 1
    return result


def edited_titles(previous, current):
    """Nur geänderte Zeilentitel; neue/entfernte Verweise benennen kein Ziel um."""
    before, after = text_titles(previous), text_titles(current)
    result = {}
    for identity, titles in after.items():
        old = before.get(identity, [])
        if len(old) != len(titles):
            continue
        changed = [title for a, title in zip(old, titles) if a != title]
        if changed and len(set(changed)) == 1:
            result[identity] = changed[0]
    return result


def undo_titles(current, target, targets, *, prior_document=None, prior_titles=None):
    """Text-Undo benennt nur Ziele um, die noch dem eigenen Textstand entsprechen."""
    before, after = text_titles(current), text_titles(target)
    cached = text_titles(prior_document) if prior_document is not None else {}
    result = {}
    for identity, old in before.items():
        wanted = after.get(identity, [])
        state, item, _ = targets.get(identity, ('missing', None, None))
        if (wanted and state == 'active' and ' '.join(str(item.get('text') or '').split()) == old[0]
                and wanted[0] != old[0]):
            desired = wanted[0]
            prior = (prior_titles or {}).get(identity)
            if prior is not None and cached.get(identity) and prior != cached[identity][0]:
                # Ein Darstellungsabgleich im Flush ist keine eigene Titeländerung.
                if prior == ' '.join(str(item.get('text') or '').split()):
                    continue
                desired = prior
            result[identity] = desired
    return result


def target_index(lists, trash):
    result = {}
    for entry in lists:
        for item in walk(entry.get('items', [])):
            result[item['id']] = ('active', item, entry)
    for entry in trash:
        payload = entry.get('payload') or entry.get('item') or entry.get('list') or entry.get('folder') or {}
        containers = [payload, *payload.get('lists', [])]
        for container in containers:
            for item in walk([container] if 'text' in container else []):
                result.setdefault(item['id'], ('trash', item, None))
            for item in walk(container.get('items', [])):
                result.setdefault(item['id'], ('trash', item, None))
    return result


def status(identity, lists, trash):
    return target_index(lists, trash).get(identity, ('missing', None, None))
