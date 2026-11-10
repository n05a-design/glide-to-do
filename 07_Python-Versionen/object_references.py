# SPDX-License-Identifier: MPL-2.0
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


USAGE_KIND_LABELS = {
    'home': 'Heimat',
    'reference': 'Objektverweis',
    'rich_link': 'Textverknüpfung',
    'task_line': 'Aufgabenzeile',
    'live_list': 'Live-Liste',
    'relation': 'Aufgabenbeziehung',
    'pinboard': 'Pinnwand',
    'mention': 'Erwähnt ohne Verweis',
}


@dataclass(frozen=True)
class UsageLocation:
    kind: str
    source: tuple
    state: str
    title: str
    detail: str = ''
    scope: str = ''
    line: int = 0
    mention: object = None
    context: str = ''

    @property
    def kind_label(self) -> str:
        return USAGE_KIND_LABELS.get(self.kind, self.kind)


def _folder_path(folder_id, folders_by_id):
    names, seen, current = [], set(), folder_id
    while current and current in folders_by_id and current not in seen:
        seen.add(current)
        folder = folders_by_id[current]
        names.append(str(folder.get('title') or 'Ordner').strip() or 'Ordner')
        current = folder.get('parent_id')
    return ' › '.join(reversed(names))


def _line_excerpt(text, start, end):
    if not isinstance(text, str) or not text:
        return 1, ''
    start = max(0, min(len(text), int(start or 0)))
    end = max(start, min(len(text), int(end or start)))
    line_no = text.count('\n', 0, start) + 1
    line_start = text.rfind('\n', 0, start) + 1
    line_end = text.find('\n', end)
    if line_end < 0:
        line_end = len(text)
    snippet = ' '.join(text[line_start:line_end].split())
    if len(snippet) > 96:
        snippet = snippet[:95] + '…'
    return line_no, snippet


def _item_parent_map(items):
    parents = {}
    def descend(children, parent=None):
        for item in children or ():
            if isinstance(item, dict) and 'id' in item:
                if parent is not None:
                    parents[item['id']] = parent
                descend(item.get('children', ()), item)
    descend(items)
    return parents


def usage_locations(target, lists, folders=(), trash=(), pinboards=None):
    """WA-21: Vollständige Fundortübersicht eines Objekts über alle Behälter."""
    if not isinstance(target, tuple) or len(target) != 2 or target[0] not in ('list', 'item'):
        return []
    index = nodes(lists, trash)
    folders_by_id = {f['id']: f for f in folders or () if isinstance(f, dict) and 'id' in f}
    for key, (state, holder, entry) in list(index.items()):
        if state == 'active' and entry:
            curr = entry.get('folder_id')
            seen = set()
            while curr and curr in folders_by_id and curr not in seen:
                seen.add(curr)
                if folders_by_id[curr].get('archived'):
                    index[key] = ('archived', holder, entry)
                    break
                curr = folders_by_id[curr].get('parent_id')
    if target not in index:
        return []

    target_state, target_holder, target_entry = index[target]
    try:
        target_uri = uri(*target)
    except ValueError:
        return []
    result = []

    # 1. Heimat (Übergeordneter Ordner bzw. Quellliste / Elternpunkt / Heimatzeile)
    if target[0] == 'list':
        folder_id = target_holder.get('folder_id') if isinstance(target_holder, dict) else None
        if folder_id and folder_id in folders_by_id:
            folder = folders_by_id[folder_id]
            f_state = 'archived' if folder.get('archived') or target_state == 'archived' else target_state
            path = _folder_path(folder_id, folders_by_id)
            result.append(UsageLocation(
                kind='home',
                source=('folder', folder_id),
                state=f_state,
                title=f'Ordner · {path}',
                detail='Übergeordneter Ordner',
                scope=f'folder:{folder_id}',
            ))
        else:
            result.append(UsageLocation(
                kind='home',
                source=target,
                state=target_state,
                title=caption(target, index)[1],
                detail='Oberste Ebene (ohne Ordner)',
            ))
    else:
        if target_entry and isinstance(target_entry, dict) and 'id' in target_entry:
            entry_key = ('list', target_entry['id'])
            e_state, e_label = caption(entry_key, index)
            parents = _item_parent_map(target_entry.get('items', ()))
            parent_item = parents.get(target[1])
            detail = 'Quellbehälter'
            if parent_item:
                p_title = ' '.join(str(parent_item.get('text') or '').split())[:60]
                detail = f'Unterpunkt von „{p_title}“'
            doc = target_entry.get('rich_note') or {}
            line_no = 0
            for span in doc.get('spans', ()):
                if span.get('tag') == f'item:{target[1]}':
                    line_no, snippet = _line_excerpt(doc.get('text', ''), span.get('start', 0), span.get('end', 0))
                    detail = f'Heimatzeile {line_no}' + (f': „{snippet}“' if snippet else '')
                    break
            result.append(UsageLocation(
                kind='home',
                source=entry_key,
                state=e_state,
                title=e_label,
                detail=detail,
                line=line_no,
            ))

    # 2. Ausdrückliche Objektverweise, Rich-Text-Links, Aufgabenzeilen, Live-Listen und Aufgabenbeziehungen
    target_folder_id = target_holder.get('folder_id') if target[0] == 'list' and isinstance(target_holder, dict) else None
    target_folder_ancestors = set()
    curr = target_folder_id
    while curr and curr in folders_by_id and curr not in target_folder_ancestors:
        target_folder_ancestors.add(curr)
        curr = folders_by_id[curr].get('parent_id')

    for source_key, (state, holder, entry) in index.items():
        if not isinstance(holder, dict):
            continue
        source_state, source_label = caption(source_key, index)

        # a) Ausdrückliche Objektverweise (`references`)
        if source_key != target and target_uri in (holder.get('references') or ()):
            result.append(UsageLocation(
                kind='reference',
                source=source_key,
                state=source_state,
                title=source_label,
                detail='Ausdrücklicher Objektverweis',
            ))

        if source_key[0] == 'list':
            # b) Rich-Text-Verknüpfungen (`link:`) und Aufgabenverweise (`taskref:` / `item:`)
            doc = holder.get('rich_note') or {}
            text = doc.get('text', '')
            links = doc.get('links') or {}
            seen_lines = set()
            for span in doc.get('spans', ()):
                tag = str(span.get('tag') or '')
                if tag.startswith('link:') and links.get(tag) == target_uri:
                    line_no, snippet = _line_excerpt(text, span.get('start', 0), span.get('end', 0))
                    if ('rich_link', line_no) not in seen_lines:
                        seen_lines.add(('rich_link', line_no))
                        result.append(UsageLocation(
                            kind='rich_link',
                            source=source_key,
                            state=source_state,
                            title=source_label,
                            detail=f'Zeile {line_no}' + (f': „{snippet}“' if snippet else ''),
                            line=line_no,
                        ))
                elif target[0] == 'item' and tag in (f'taskref:{target[1]}', f'item:{target[1]}'):
                    if tag.startswith('item:') and target_entry and source_key[1] == target_entry.get('id'):
                        continue
                    line_no, snippet = _line_excerpt(text, span.get('start', 0), span.get('end', 0))
                    if ('task_line', line_no) not in seen_lines:
                        seen_lines.add(('task_line', line_no))
                        label_kind = 'Eingebetteter Aufgabenverweis' if tag.startswith('taskref:') else 'Aufgabenzeile'
                        result.append(UsageLocation(
                            kind='task_line',
                            source=source_key,
                            state=source_state,
                            title=source_label,
                            detail=f'{label_kind} (Zeile {line_no})' + (f': „{snippet}“' if snippet else ''),
                            line=line_no,
                        ))

            # c) Live-Listen (`live_lists`)
            if target[0] == 'list' and source_key != target:
                for live_val in holder.get('live_lists') or ():
                    if live_val == target_uri:
                        result.append(UsageLocation(
                            kind='live_list',
                            source=source_key,
                            state=source_state,
                            title=source_label,
                            detail='Eingebettete Live-Liste',
                        ))
                    elif isinstance(live_val, str) and live_val.startswith('glide://folder/'):
                        fid = unquote(live_val.split('glide://folder/', 1)[1])
                        if fid in target_folder_ancestors:
                            f_title = _folder_path(fid, folders_by_id) or 'Ordner'
                            result.append(UsageLocation(
                                kind='live_list',
                                source=source_key,
                                state=source_state,
                                title=source_label,
                                detail=f'Über Ordner-Live-Liste „{f_title}“',
                            ))
        else:
            # d) Aufgabenbeziehungen (`links`, `blocked_by`)
            if target[0] == 'item' and source_key != target:
                if target[1] in (holder.get('links') or ()):
                    result.append(UsageLocation(
                        kind='relation',
                        source=source_key,
                        state=source_state,
                        title=source_label,
                        detail='Verknüpfte Aufgabe',
                    ))
                if target[1] in (holder.get('blocked_by') or ()):
                    result.append(UsageLocation(
                        kind='relation',
                        source=source_key,
                        state=source_state,
                        title=source_label,
                        detail='Blockiert diese Aufgabe (Abhängigkeit)',
                    ))

    if target[0] == 'item':
        for blocked_id in target_holder.get('blocked_by') or ():
            other_key = ('item', blocked_id)
            if other_key in index and other_key != target:
                o_state, o_label = caption(other_key, index)
                result.append(UsageLocation(
                    kind='relation',
                    source=other_key,
                    state=o_state,
                    title=o_label,
                    detail='Wird von dieser Aufgabe vorausgesetzt',
                ))

    # 3. Pinnwände (`pinboards`)
    if isinstance(pinboards, dict):
        card_key = f'page:{target[1]}' if target[0] == 'list' else target[1]
        for scope, board in sorted(pinboards.items(), key=lambda pair: str(pair[0])):
            if not isinstance(board, dict):
                continue
            cards = [c for c in board.get('cards') or () if isinstance(c, dict) and c.get('item_id') == card_key]
            if not cards:
                continue
            card = cards[0]
            edges = [e for e in board.get('connections') or ()
                     if isinstance(e, dict) and (e.get('from') == card_key or e.get('to') == card_key)]
            if scope == 'global':
                b_state = 'active'
                b_title = 'Globale Pinnwand'
                b_source = ('pinboard', 'global')
            elif isinstance(scope, str) and scope.startswith('list:'):
                lid = scope.split(':', 1)[1]
                b_source = ('list', lid)
                b_state, b_label = caption(b_source, index)
                b_title = f'Pinnwand · {b_label}'
            elif isinstance(scope, str) and scope.startswith('folder:'):
                fid = scope.split(':', 1)[1]
                folder = folders_by_id.get(fid)
                b_state = ('archived' if folder.get('archived') else 'active') if folder else 'missing'
                f_path = _folder_path(fid, folders_by_id) or 'Ordner'
                b_title = f'Ordner-Pinnwand · {f_path}'
                b_source = ('folder', fid)
            else:
                continue
            pos = f"Position ({int(card.get('x', 0))}, {int(card.get('y', 0))})"
            edge_info = f' · {len(edges)} Verbindung(en)' if edges else ''
            result.append(UsageLocation(
                kind='pinboard',
                source=b_source,
                state=b_state,
                title=b_title,
                detail=pos + edge_info,
                scope=scope,
            ))

    # 4. Unverknüpfte Erwähnungen (`unlinked_mentions` für Seiten/Listen/Notizen/Zeichnungen)
    if target[0] == 'list' and target_state == 'active':
        for hit in unlinked_mentions(target, index):
            m_state, m_label = caption(hit.source, index)
            excerpt = ''.join(hit.excerpt()).replace('\n', ' ')
            result.append(UsageLocation(
                kind='mention',
                source=hit.source,
                state=m_state,
                title=m_label,
                detail=f'„{excerpt}“',
                mention=hit,
            ))

    return result

