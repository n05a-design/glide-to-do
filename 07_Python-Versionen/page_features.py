"""Live-Listen, Titelbilder und gefüllte Vorlagenvorschauen; ohne Tk (Format 23)."""
import copy
from bisect import bisect_left, bisect_right
from datetime import date, timedelta
import re

import drawing
import object_references as objects


def block_lines(document, line):
    """Halboffenes Zeilenintervall eines Blocks (nullbasiert), mit Kindzeilen.

    Tabellen und mehrzeilige Codebereiche bleiben zusammen. Eine Aufklappzeile
    nimmt ihre eingerückten Kinder mit, auch wenn diese gerade verborgen sind.
    """
    rows = document.get('text', '').split('\n')
    starts, offset = [], 0
    for row in rows:
        starts.append(offset)
        offset += len(row) + 1
    line = max(0, min(len(rows) - 1, line))
    first, last = line, line + 1
    spans = document.get('spans', ())
    for span in spans:
        if span['tag'] in ('table', 'codeblock') and span['start'] < offset:
            a = max(0, bisect_right(starts, span['start']) - 1)
            b = bisect_right(starts, max(span['start'], span['end'] - 1))
            if a <= line < b:
                first, last = min(first, a), max(last, b)
    def tags(row):
        return {s['tag'] for s in spans if s['start'] <= starts[row] < s['end']}
    if 'toggle' in tags(first):
        levels = [0] * len(rows)
        for span in spans:
            tag = span['tag']
            if tag.startswith('indent') and tag[6:].isdigit():
                for row in range(bisect_left(starts, span['start']), bisect_left(starts, span['end'])):
                    levels[row] = max(levels[row], int(tag[6:]))
        while last < len(rows) and levels[last] > levels[first]:
            last += 1
    return first, last


def move_document_block(document, first, last, target):
    """Verschiebt einen Block vor eine Zeilengrenze; Format/IDs bleiben erhalten.

    Alle Versätze zählen Python-Zeichen, auch Emoji. Über mehrere Blöcke
    laufende Formate werden an den Schnittkanten geteilt und neu zugeordnet.
    Das Eingabedokument wird nie verändert. Ergebnis: (Dokument, Textversatz).
    """
    text = document.get('text', '')
    rows = text.split('\n')
    count = len(rows)
    if not (0 <= first < last <= count and 0 <= target <= count):
        raise ValueError('Ungültige Blockposition.')
    if first <= target <= last:
        return copy.deepcopy(document), sum(len(row) + 1 for row in rows[:first])
    order = list(range(count))
    selected = order[first:last]
    del order[first:last]
    insertion = target if target < first else target - (last - first)
    order[insertion:insertion] = selected
    starts, offset = [], 0
    for row in rows:
        starts.append(offset)
        offset += len(row) + 1
    result = copy.deepcopy(document)
    result['text'] = '\n'.join(rows[i] for i in order)
    mapped, position = {}, 0
    for index in order:
        mapped[index] = position
        position += len(rows[index]) + 1
    result['spans'] = []
    for span in document.get('spans', ()):
        low_row = max(0, bisect_right(starts, span['start']) - 1)
        high_row = bisect_left(starts, span['end'])
        for index in range(low_row, high_row):
            low = max(span['start'], starts[index])
            high = min(span['end'], starts[index] + len(rows[index]) + 1)
            a = mapped[index] + low - starts[index]
            b = min(len(result['text']), mapped[index] + high - starts[index])
            if low < high and a < b:
                result['spans'].append(dict(span, start=a, end=b))
    result['spans'].sort(key=lambda s: (s['start'], s['end'], s['tag']))
    return result, mapped[first]


def card_summary(entry):
    """Lesender Kartenauszug und offene eigene Aufgaben; keine Objektkopie."""
    doc = entry.get('rich_note') or {}
    text = str(doc.get('text') or entry.get('note') or entry.get('description') or '')
    text = re.sub(r'[\ufffc\u25be\u25b8]', ' ', text)
    text = ' '.join(text.split())
    excerpt = text[:157].rstrip()+'…' if len(text) > 160 else text
    count = sum(item.get('kind', 'task') == 'task' and not item.get('done')
                for item in objects.walk(entry.get('items', [])))
    return excerpt, count


def live_lists(values):
    if values is None:
        return []
    if not isinstance(values, list) or len(values) > 20:
        raise ValueError('Eine Seite darf höchstens 20 Live-Listen enthalten.')
    if any(objects.parse(value) is None or objects.parse(value)[0] != 'list' for value in values):
        raise ValueError('Ungültiges Ziel einer Live-Liste.')
    return list(dict.fromkeys(objects.uri(*objects.parse(value)) for value in values))


def cover(value):
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError('Ungültiges Titelbild.')
    if value.get('kind') == 'image' and isinstance(value.get('attachment'), str):
        if re.fullmatch(r'[A-Za-z0-9_-]{1,64}', value['attachment']):
            return {'kind': 'image', 'attachment': value['attachment']}
    if value.get('kind') == 'drawing':
        return {'kind': 'drawing', 'document': drawing.DrawingModel.from_document(value.get('document')).to_document()}
    raise ValueError('Ungültiges Titelbild.')


def live_rows(target, lists, trash=(), folders=()):
    """Frischer Zustand des Heimatorts, niemals Aufgaben kopieren oder rekursiv einbetten."""
    key = objects.parse(target)
    state, holder, _ = objects.nodes(lists, trash).get(key, ('missing', {}, None))
    by_id = {folder.get('id'): folder for folder in folders}
    parent, seen = holder.get('folder_id'), set()
    while state == 'active' and parent in by_id and parent not in seen:
        seen.add(parent)
        folder = by_id[parent]
        if folder.get('archived'):
            state = 'archived'
        parent = folder.get('parent_id')
    rows = []
    def walk(items, depth=0):
        for item in items:
            if item.get('kind', 'task') == 'task':
                rows.append((item['id'], str(item.get('text') or ''), bool(item.get('done')),
                             item.get('due'), depth))
            walk(item.get('children', []), depth + 1)
    if state in ('active', 'archived'):
        walk(holder.get('items', []))
    return state, str(holder.get('title') or 'Ziel fehlt'), rows


def prepare_template(template, today):
    """Dieselben Datumsverschiebungen und offenen Aufgaben für Vorschau und Übernahme."""
    result = copy.deepcopy(template)
    payload = result.get('payload')
    if not isinstance(payload, dict):
        return result
    anchor = result.get('schedule_anchor')
    try:
        offset = (today - date.fromisoformat(anchor)).days if anchor else 0
    except (ValueError, TypeError):
        offset = 0
    for entry in payload.get('lists', []):
        for item in objects.walk(entry.get('items', [])):
            item['done'] = False
            for field in ('planned_date', 'due'):
                if offset and item.get(field):
                    item[field] = (date.fromisoformat(item[field]) + timedelta(days=offset)).isoformat()
            if offset and item.get('due') and item.get('repeat'):
                for field in ('start', 'ende'):
                    if item['repeat'].get(field):
                        item['repeat'][field] = (date.fromisoformat(item['repeat'][field]) + timedelta(days=offset)).isoformat()
    result.pop('schedule_anchor', None)  # Eine vorbereitete Vorlage wird nur einmal verschoben.
    roots = payload.get('folders') if result.get('kind') == 'folder' else payload.get('lists')
    roots = [root for root in roots or [] if result.get('kind') != 'folder' or not root.get('parent_id')]
    if roots:
        roots[0].update({key: copy.deepcopy(result.get(key)) for key in ('title', 'note', 'color', 'labels')})
    return result


def template_preview(template, names=None):
    """Lesbare Vorschau auch vollständiger Ordner, Unteraufgaben und Seitentexte."""
    lines = [str(template.get('title') or 'Vorlage'), str(template.get('note') or ''), '']
    payload = template.get('payload') or {}
    for folder in payload.get('folders', []):
        lines.append('Ordner: ' + str(folder.get('title') or 'Ordner'))
    entries = payload.get('lists') or [template]
    for entry in entries:
        if entry is not template:
            lines.extend(['', str(entry.get('title') or 'Liste'), str(entry.get('note') or '')])
        text = (entry.get('rich_note') or {}).get('text')
        if text:
            lines.extend(['', text])
        if entry.get('cover'):
            lines.append('Titelbild: ' + ('Pixelzeichnung' if entry['cover'].get('kind') == 'drawing' else 'Bilddatei'))
        for value in entry.get('live_lists', []):
            lines.append('Live-Liste: ' + (names or {}).get(value, 'Liste außerhalb der Vorlage'))
        def walk(items, depth=0):
            for item in items:
                if isinstance(item, str):
                    lines.append('  ' * depth + '□ ' + item)
                    continue
                text = str(item.get('text') or '')
                dates = ' · '.join(f'{label} {item[field]}' for field,label in
                                 (('due', 'fällig'), ('planned_date', 'geplant')) if item.get(field))
                lines.append('  ' * depth + '□ ' + text + (' · ' + dates if dates else ''))
                if item.get('description'):
                    lines.append('  ' * (depth+1) + str(item['description']))
                walk(item.get('children', []), depth+1)
        walk(entry.get('items', []))
        if entry.get('attachments'):
            lines.append('Anhänge: ' + ', '.join(str(a.get('name') or 'Datei') for a in entry['attachments']))
    return '\n'.join(lines).strip()


def place_roots(lists, folders, folder_id):
    """Neue Wurzeln vor dem Commit einordnen; interne Eltern und Kennungen bleiben."""
    if not folder_id:
        return
    for folder in folders:
        if not folder.get('parent_id'):
            folder['parent_id'] = folder_id
    for entry in lists:
        if not entry.get('folder_id'):
            entry['folder_id'] = folder_id
