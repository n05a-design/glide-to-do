"""Additive Einstellungsfelder erhalten; bekannte Felder weiter streng prüfen (WA-09).

Keine Auswertung unbekannter Inhalte und kein Ersatz für ein Format-Tor bei
geänderter Semantik. Grenzen und Pflichtkennungen bleiben beim Normalisierer.
"""
import copy


FILTER_FIELDS = frozenset(('id', 'name', 'query', 'list_ids', 'label_ids', 'status',
    'importance', 'due', 'label_mode', 'source', '_view', '_layout'))
TAB_FIELDS = frozenset(('list_id', 'item_id', 'used'))
CARD_FIELDS = frozenset(('list_id', 'item_id', 'x', 'y', 'scale', 'show'))
EDGE_FIELDS = frozenset(('from', 'to', 'style', 'label', 'dash', 'color'))
AREA_FIELDS = frozenset(('id', 'name', 'color', 'x', 'y', 'w', 'h'))
BOARD_FIELDS = frozenset(('cards', 'connections', 'connection_style', 'layout',
    'snap', 'object_snap', 'navigator', 'zoom', 'preview', 'auto', 'width',
    'group_by', 'collapsed', 'hide_empty', 'only_open', 'show_description',
    'show_checklist', 'color_mode', 'color_source', 'areas', 'auto_connect',
    'background', 'print_background'))


def preserve(raw, normalized, known):
    """Tiefe Kopie unbekannter Schlüssel, überlagert durch geprüfte Werte.

    Auch weggelassene ungültige bekannte Felder dürfen nicht zurückkehren.
    Temporäre Filterfelder gehören deshalb ausdrücklich zur bekannten Menge.
    """
    extra = {key: value for key, value in raw.items() if key not in known}
    return copy.deepcopy({**extra, **normalized})


def opaque_card(card):
    """Unverstandene Kartentypen von entfernten bekannten Objekten trennen."""
    identity = card.get('item_id')
    if not isinstance(identity, str) or not 0 < len(identity) <= 200:
        return False
    kind = card.get('kind')
    if isinstance(kind, str) and kind and kind not in ('task', 'page', 'drawing'):
        return True
    return ':' in identity and not identity.startswith('page:')


def prune_cards(board, valid):
    """Bekannte gelöschte Karten entfernen, fremde Karten/Kanten nur aufbewahren.

    `valid` ordnet die aufgelöste Kennung dem aktuellen Listen-/Objektpaar zu.
    Die UI verwendet weiterhin ausschließlich tatsächlich aufgelöste Karten.
    """
    cards = [copy.deepcopy(card) for card in board['cards']
             if card['item_id'] in valid or opaque_card(card)]
    for card in cards:
        if card['item_id'] in valid:
            card['list_id'] = valid[card['item_id']][0]['id']
    ids = {card['item_id'] for card in cards}
    edges = [copy.deepcopy(edge) for edge in board.get('connections', [])
             if edge['from'] in ids and edge['to'] in ids]
    return cards, edges
