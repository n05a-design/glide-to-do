"""Typisierte lokale Verweise und abgeleitete Rückverweise (Format 22), ohne Tk."""
import re
import copy
from dataclasses import dataclass
from urllib.parse import quote, unquote
from content_search import search_key, match_spans

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


@dataclass(frozen=True)
class Mention:
    source: tuple
    field: str
    text: str
    start: int
    end: int

    def excerpt(self):
        """Drei Teile für eine Markierung im unveränderten Originaltext."""
        first, last = max(0, self.start - 35), min(len(self.text), self.end + 55)
        return (('…' if first else '') + self.text[first:self.start],
                self.text[self.start:self.end],
                self.text[self.end:last] + ('…' if last < len(self.text) else ''))


def unlinked_mentions(target, index):
    """FP-05: sichtbare Texte aktiver Quellen, ohne Index oder gespeicherte Treffer.

    Der Aufrufer liefert denselben ID-/Archivindex wie für Rückverweise.
    Ganze Wörter zählen mit der Suchnormalisierung; URLs, Code und bereits
    verknüpfte Spannen bleiben ausgenommen. Reine Beschreibungen verwenden
    den bestehenden ausdrücklichen Objektverweis statt eines neuen Textformats.
    """
    state, holder, _ = index.get(target, ('missing', {}, None))
    title = str(holder.get('title') or '').strip() if target and target[0] == 'list' else ''
    key = search_key(title)
    if state != 'active' or len(title) < 4 or not key:
        return []
    value = uri(*target)
    result = []
    for source, (state, holder, _) in index.items():
        if state != 'active' or source == target:
            continue
        document = holder.get('rich_note') or {}
        fields = [('rich_note', document.get('text', ''))] if source[0] == 'list' else []
        plain = holder.get('note' if source[0] == 'list' else 'description', '')
        if value not in holder.get('references', []) and plain != document.get('text'):
            fields.append(('note' if source[0] == 'list' else 'description', plain))
        for field, text in fields:
            if not isinstance(text, str) or key not in search_key(text):
                continue
            excluded = [(m.start(), m.end()) for m in re.finditer(r'(?:\w+://|www\.|mailto:)[^\s]+', text)]
            if field == 'rich_note':
                excluded.extend((span['start'], span['end']) for span in document.get('spans', [])
                                if span.get('tag', '').startswith(('link:', 'taskref:'))
                                or span.get('tag') in ('code', 'codeblock'))
            for start, end in match_spans(text, key, limit=len(text)):
                if ((start and (text[start - 1].isalnum() or text[start - 1] == '_'))
                        or (end < len(text) and (text[end].isalnum() or text[end] == '_'))):
                    continue
                if any(start < b and end > a for a, b in excluded):
                    continue
                result.append(Mention(source, field, text, start, end))
    return result


def linked_mention_document(holder, mention, target, tag):
    """Bestehendes Format-22-Linkformat; Text und andere Formatierungen bleiben."""
    document = copy.deepcopy(holder.get('rich_note') or {})
    if mention.field != 'rich_note' or document.get('text') != mention.text:
        raise ValueError('Die Fundstelle hat sich inzwischen geändert.')
    if not tag.startswith('link:') or tag in document.get('links', {}):
        raise ValueError('Ungültige Linkmarke.')
    document.setdefault('links', {})[tag] = uri(*target)
    document.setdefault('spans', []).append(dict(tag=tag, start=mention.start, end=mention.end))
    return document
