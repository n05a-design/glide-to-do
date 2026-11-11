# SPDX-License-Identifier: MPL-2.0
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


def zoomed_image(kind, width, height, factor):
    """Wie ein Kartenbild beim Pinnwandzoom mitwächst (31.10.2026).

    `photo` skaliert in Vierteln über zoom/subsample. `nsimage` (macOS) kennt
    beides nicht und wird aus derselben Quelle in Zielgröße neu gezeichnet.
    Andere Bildtypen bleiben unskaliert stehen, statt die Zeichnung abzubrechen.
    """
    if kind == 'photo':
        return ('photo', int(round(factor*4)), 4)
    if kind == 'nsimage':
        return ('nsimage', max(1, round(width*factor)), max(1, round(height*factor)))
    return None


from dataclasses import dataclass
import object_references as objects


CANVAS_COLORS = {
    'delete': '1',
    'overdue': '1',
    'priority_high': '1',
    'due_today': '2',
    'priority_medium': '2',
    'import': '2',
    'flag': '3',
    'export': '4',
    'confirm': '4',
    'add': '4',
    'due_action': '5',
    'clear': '5',
    'priority_low': '5',
    'accent': '6',
    'ui_accent': '6',
}


@dataclass(frozen=True)
class CanvasExportReport:
    scope_title: str
    areas_count: int
    cards_count: int
    edges_count: int
    losses: tuple

    def summary_text(self):
        lines = [
            f'JSON Canvas 1.0 Export · {self.scope_title or "Pinnwand"}',
            f'Exportiert: {self.cards_count} Karte(n), {self.areas_count} Bereich(e), {self.edges_count} Verbindung(en).',
        ]
        if self.losses:
            lines.append('')
            lines.append('Formatbedingte Abweichungen (Verlustbericht):')
            for entry in self.losses:
                lines.append(f'• {entry}')
        else:
            lines.append('')
            lines.append('Alle Elemente wurden ohne Formatverluste übertragen.')
        return '\n'.join(lines)


def _canvas_color(value):
    if not isinstance(value, str) or not value:
        return None
    if value.startswith('#') and len(value) == 7:
        return value.upper()
    return CANVAS_COLORS.get(value)


def _edge_sides(from_box, to_box):
    fx, fy, fw, fh = from_box
    tx, ty, tw, th = to_box
    fcx, fcy = fx + fw / 2.0, fy + fh / 2.0
    tcx, tcy = tx + tw / 2.0, ty + th / 2.0
    dx, dy = tcx - fcx, tcy - fcy
    if abs(dx) >= abs(dy):
        return ('right', 'left') if dx >= 0 else ('left', 'right')
    return ('bottom', 'top') if dy >= 0 else ('top', 'bottom')


def export_json_canvas(board, cards_info, scope_title=''):
    """WA-07 / FP-07 Stufe 2: Exportiert eine Pinnwand nach JSON Canvas 1.0 (`.canvas`).

    Erzeugt `{"nodes": [...], "edges": [...]}` nach der offenen Spezifikation
    JSON Canvas 1.0 sowie einen nachvollziehbaren Verlustbericht.
    """
    board = board if isinstance(board, dict) else {}
    cards_info = list(cards_info or ())
    nodes = []
    edges = []
    losses = []

    layout = board.get('layout', 'free')
    if layout in ('grid', 'columns'):
        losses.append(
            f'Die dynamische Anordnung ({ "Spaltenboard" if layout == "columns" else "Geordnete Karten" }) '
            'wurde mit ihren berechneten Kartenpositionen als statische Fläche übernommen.'
        )
    if board.get('collapsed'):
        losses.append('Eingeklappte Spaltenzustände des Spaltenboards sind in JSON Canvas 1.0 nicht darstellbar.')

    areas = [a for a in (board.get('areas') or ()) if isinstance(a, dict) and a.get('id')]
    if layout != 'columns':
        for area in areas:
            node = {
                'id': f"area:{area['id']}",
                'type': 'group',
                'x': int(round(area.get('x', 0))),
                'y': int(round(area.get('y', 0))),
                'width': max(120, int(round(area.get('w', 480)))),
                'height': max(80, int(round(area.get('h', 320)))),
                'label': str(area.get('name') or 'Bereich'),
            }
            color = _canvas_color(area.get('color'))
            if color:
                node['color'] = color
            nodes.append(node)

    node_boxes = {}
    has_interactive_checklists = False
    has_attachments = False
    for info in cards_info:
        if not isinstance(info, dict) or not info.get('id'):
            continue
        cid = str(info['id'])
        x = int(round(info.get('x', 0)))
        y = int(round(info.get('y', 0)))
        w = max(160, int(round(info.get('width', board.get('width', 300)))))
        h = max(80, int(round(info.get('height', 140))))
        node_boxes[cid] = (x, y, w, h)

        title = str(info.get('title') or 'Ohne Titel').strip()
        is_page = bool(info.get('is_page')) or cid.startswith('page:')
        md_lines = []
        if is_page:
            kind_label = str(info.get('kind_label') or 'Seite')
            md_lines.append(f'### {title} ({kind_label})')
        else:
            marker = '[x]' if info.get('done') else '[ ]'
            md_lines.append(f'### {marker} {title}')

        meta = []
        if info.get('importance_label'):
            meta.append(str(info['importance_label']))
        if info.get('planned'):
            meta.append(f"Bearbeitungstag: {info['planned']}")
        if info.get('due'):
            meta.append(f"Fällig: {info['due']}")
        if info.get('source_title') and not is_page:
            meta.append(f"Liste: {info['source_title']}")
        if meta:
            md_lines.append(' · '.join(meta))

        desc = str(info.get('description') or '').strip()
        if desc:
            md_lines.extend(('', desc))

        checklist = info.get('checklist') or ()
        if checklist:
            has_interactive_checklists = True
            md_lines.append('')
            for step in checklist:
                if isinstance(step, dict):
                    s_mark = '[x]' if step.get('done') else '[ ]'
                    md_lines.append(f"- {s_mark} {str(step.get('text') or '').strip()}")

        labels = [str(l).strip() for l in (info.get('labels') or ()) if str(l).strip()]
        if labels:
            md_lines.extend(('', 'Labels: ' + ', '.join(f'`{l}`' for l in labels)))

        attachments_count = int(info.get('attachments_count') or 0)
        if attachments_count > 0:
            has_attachments = True
            md_lines.append(f'Anhänge: {attachments_count}')

        ref_uri = info.get('uri')
        if not ref_uri:
            try:
                if cid.startswith('page:'):
                    ref_uri = objects.uri('list', cid.split(':', 1)[1])
                else:
                    ref_uri = objects.uri('item', cid)
            except ValueError:
                ref_uri = None
        if ref_uri:
            md_lines.extend(('', f'Verweis: `{ref_uri}`'))

        node = {
            'id': cid,
            'type': 'text',
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'text': '\n'.join(md_lines),
        }
        color = _canvas_color(info.get('color'))
        if color:
            node['color'] = color
        nodes.append(node)

    raw_cards = [c for c in (board.get('cards') or ()) if isinstance(c, dict) and c.get('item_id')]
    skipped_cards = sum(1 for c in raw_cards if str(c['item_id']) not in node_boxes)
    if skipped_cards and layout != 'columns':
        losses.append(f'{skipped_cards} ausgeblendete oder nicht mehr vorhandene Karte(n) wurden ausgelassen.')
    if has_interactive_checklists:
        losses.append('Abhakbare Checklisten und Live-Zähler wurden als statisches Markdown übernommen.')
    if has_attachments:
        losses.append('Lokale Dateianhänge und Vorschaubilder bleiben in der Glide-Ablage und sind als Anzahl vermerkt.')

    dashed_count = 0
    skipped_edges = 0
    for index, conn in enumerate(board.get('connections') or (), 1):
        if not isinstance(conn, dict):
            continue
        from_id = str(conn.get('from') or '')
        to_id = str(conn.get('to') or '')
        if from_id not in node_boxes or to_id not in node_boxes:
            skipped_edges += 1
            continue
        from_side, to_side = _edge_sides(node_boxes[from_id], node_boxes[to_id])
        style = conn.get('style', 'line')
        if style == 'forward':
            from_end, to_end = 'none', 'arrow'
        elif style == 'backward':
            from_end, to_end = 'arrow', 'none'
        elif style == 'both':
            from_end, to_end = 'arrow', 'arrow'
        else:
            from_end, to_end = 'none', 'none'
        edge = {
            'id': f'edge:{index}:{from_id}:{to_id}',
            'fromNode': from_id,
            'fromSide': from_side,
            'fromEnd': from_end,
            'toNode': to_id,
            'toSide': to_side,
            'toEnd': to_end,
        }
        if conn.get('label'):
            edge['label'] = str(conn['label'])
        color = _canvas_color(conn.get('color'))
        if color:
            edge['color'] = color
        if conn.get('dash'):
            dashed_count += 1
        edges.append(edge)

    if dashed_count:
        losses.append(
            f'{dashed_count} gestrichelte Verbindung(en) wurden als durchgezogene Kanten exportiert '
            '(JSON Canvas 1.0 definiert keine Strichart).'
        )
    if skipped_edges:
        losses.append(f'{skipped_edges} Verbindung(en) zu ausgeblendeten Karten wurden ausgelassen.')

    document = {'nodes': nodes, 'edges': edges}
    report = CanvasExportReport(
        scope_title=str(scope_title or 'Pinnwand'),
        areas_count=len(areas) if layout != 'columns' else 0,
        cards_count=len(node_boxes),
        edges_count=len(edges),
        losses=tuple(losses),
    )
    return document, report

