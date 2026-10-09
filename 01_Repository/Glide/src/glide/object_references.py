"""Typisierte lokale Verweise und abgeleitete Rückverweise (Format 22), ohne Tk."""
import re
from urllib.parse import quote, unquote

URI = re.compile(r'^glide://(list|item)/([^/?#]+)$')


def parse(value):
    if not isinstance(value, str) or len(value) > 2048:
        return None
    match = URI.fullmatch(value)
    if not match:
        return None
    try:
        identity = unquote(match.group(2), errors='strict')
    except (ValueError, UnicodeError):
        return None
    if not identity or len(identity) > 256 or any(ord(char) < 32 for char in identity):
        return None
    if quote(identity, safe='').lower() != match.group(2).lower():
        return None
    return match.group(1), identity


def uri(kind, identity):
    if not isinstance(identity, str):
        raise ValueError('Ungültige Verweiskennung')
    value = f'glide://{kind}/{quote(identity, safe="")}'
    if parse(value) is None:
        raise ValueError('Ungültiges Verweisziel')
    return value


def normalize(values):
    if values is None:
        return []
    if not isinstance(values, list) or len(values) > 200:
        raise ValueError('Ungültige oder zu viele lokale Verweise')
    if any(parse(value) is None for value in values):
        raise ValueError('Ungültiger lokaler Verweis')
    return list(dict.fromkeys(uri(*parse(value)) for value in values))


def walk(items):
    for item in items or []:
        yield item
        yield from walk(item.get('children', []))


def nodes(lists, trash=()):
    result = {}
    def register(entry, state):
        if isinstance(entry, dict) and 'id' in entry:
            result.setdefault(('list', entry['id']), (state, entry, entry))
            for item in walk(entry.get('items', [])):
                result.setdefault(('item', item['id']), (state, item, entry))
    for entry in lists:
        register(entry, 'archived' if entry.get('archived') else 'active')
    for deleted in trash:
        payload = deleted.get('payload') or deleted.get('list') or deleted.get('item') or deleted.get('folder') or {}
        if 'text' in payload:
            for item in walk([payload]):
                result.setdefault(('item', item['id']), ('trash', item, None))
        elif 'items' in payload:
            register(payload, 'trash')
        for entry in payload.get('lists', []):
            register(entry, 'trash')
    return result


def graph(lists, trash=()):
    """Eine Berechnung, lineare Kosten; Titel oder Python-Objektadressen sind keine IDs."""
    index = nodes(lists, trash)
    outgoing, incoming = {}, {}
    for key, (_, holder, _) in index.items():
        targets = {parse(value) for value in holder.get('references', [])} - {None}
        if key[0] == 'list':
            targets.update(parse(value) for value in holder.get('live_lists', []) if parse(value))
            doc = holder.get('rich_note') or {}
            used = {span.get('tag') for span in doc.get('spans', [])}
            targets.update(parse(value) for tag,value in doc.get('links', {}).items() if tag in used and parse(value))
            for span in doc.get('spans', []):
                tag = span.get('tag', '')
                if tag.startswith('taskref:'):
                    targets.add(('item', tag.split(':', 1)[1]))
        else:
            targets.update(('item', identity) for identity in holder.get('links', []))
        outgoing[key] = targets
        for target in targets:
            incoming.setdefault(target, set()).add(key)
    return index, outgoing, incoming


def remapped(value, containers, items):
    target = parse(value)
    if target is None:
        return value
    kind, identity = target
    return uri(kind, (containers if kind == 'list' else items).get(identity, identity))


def remap_holder(holder, containers, items):
    if 'references' in holder:
        holder['references'] = [remapped(value, containers, items) for value in holder['references']]
    if 'live_lists' in holder:
        holder['live_lists'] = [remapped(value, containers, items) for value in holder['live_lists']]
    doc = holder.get('rich_note') or {}
    for tag, value in list(doc.get('links', {}).items()):
        doc['links'][tag] = remapped(value, containers, items)


def caption(key, index):
    state, holder, source = index.get(key, ('missing', {}, None))
    title = str((holder.get('text') if key[0] == 'item' else holder.get('title')) or '').strip()
    if key[0] == 'item':
        title = ' '.join(title.split())
        if len(title) > 120:
            title = title[:119] + '…'
    label = title or 'Ziel fehlt'
    if state == 'trash':
        label += ' · im Papierkorb'
    elif state == 'archived':
        label += ' · im Archiv'
    if key[0] == 'item' and source:
        label += ' · ' + str(source.get('title') or 'Liste')
    return state, label
