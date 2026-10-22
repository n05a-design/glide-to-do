"""Seitenkarten vor alten Pinnwand-Bereinigern schützen, ohne Tk (FP-04).

Im RAM liegt die gemeinsame Pinnwand. Auf Platte enthält pinboards weiterhin
nur Aufgaben/Zeichnungen; Seitenkarten und ihre Kanten liegen in einem eigenen
obersten Schlüssel, den bereits veröffentlichte Leser unverändert erhalten.
"""
import copy
import base64
import mimetypes


def image_data(path):
    """Begrenztes Originalbild für die eigenständige Druckseite, ohne Konverter."""
    mime = mimetypes.guess_type(path)[0]
    if mime not in ('image/png', 'image/jpeg', 'image/gif', 'image/webp'):
        return None
    try:
        with open(path, 'rb') as stream:
            value = stream.read(6*1024*1024+1)
        if len(value) <= 6*1024*1024:
            return 'data:'+mime+';base64,'+base64.b64encode(value).decode('ascii')
    except OSError:
        return None
    return None

KEY = 'page_pinboards_v1'


def restore(settings):
    result = dict(settings)
    extra = result.pop(KEY, {})
    if not isinstance(extra, dict) or not extra:
        return result
    boards = result['pinboards'] = copy.deepcopy(result.get('pinboards', {}))
    if not isinstance(boards, dict):
        boards = result['pinboards'] = {}
    for scope, saved in extra.items():
        if (not isinstance(scope, str) or not isinstance(saved, dict)
                or scope != 'global' and not scope.startswith(('list:', 'folder:'))):
            continue
        board = boards.setdefault(scope, copy.deepcopy(saved.get('base', {})))
        if not isinstance(board, dict):
            continue
        cards = board.setdefault('cards', [])
        edges = board.setdefault('connections', [])
        if not isinstance(cards, list) or not isinstance(edges, list):
            continue
        known = {c.get('item_id') for c in cards if isinstance(c, dict)}
        for card in saved.get('cards', [])[:500] if isinstance(saved.get('cards'), list) else []:
            if (isinstance(card, dict) and isinstance(card.get('item_id'), str)
                    and card['item_id'].startswith('page:') and card['item_id'] not in known):
                positions = saved.get('positions')
                index = positions.get(card['item_id']) if isinstance(positions, dict) else None
                index = max(0, min(len(cards), index)) if type(index) is int else len(cards)
                cards.insert(index, copy.deepcopy(card));known.add(card['item_id'])
        for edge in saved.get('connections', [])[:2000] if isinstance(saved.get('connections'), list) else []:
            if isinstance(edge, dict) and edge not in edges:
                edges.append(copy.deepcopy(edge))
    return result


def persist(settings, lists):
    result = dict(settings)
    pages = {'page:'+entry['id'] for entry in lists
             if entry.get('list_kind') in ('page', 'note') and isinstance(entry.get('id'), str)}
    extra = {}
    boards = result['pinboards'] = dict(result.get('pinboards') or {})
    for scope, original in list(boards.items()):
        board = original
        cards = [c for c in board.get('cards', []) if c.get('item_id') in pages]
        if not cards:
            continue
        board = boards[scope] = copy.deepcopy(original)
        cards = [c for c in board.get('cards', []) if c.get('item_id') in pages]
        ids = {c['item_id'] for c in cards}
        edges = [e for e in board.get('connections', []) if e.get('from') in ids or e.get('to') in ids]
        base = {k: copy.deepcopy(v) for k, v in board.items() if k not in ('cards', 'connections')}
        positions = {card['item_id']: index for index, card in enumerate(board.get('cards', [])) if card['item_id'] in ids}
        extra[scope] = {'cards': cards, 'connections': edges, 'base': base, 'positions': positions}
        board['cards'] = [c for c in board.get('cards', []) if c.get('item_id') not in ids]
        board['connections'] = [e for e in board.get('connections', []) if e not in edges]
    if extra:
        result[KEY] = extra
    else:
        result.pop(KEY, None)
    return result
