# SPDX-License-Identifier: MPL-2.0
"""Inhaltssuche ohne Tk, Datei-I/O oder dauerhaften Index (G14, erste Stufe)."""
import unicodedata


def _fold(value):
    """Gemeinsame Gleichheit: NFC, Groß/Klein, ä/ae, ö/oe, ü/ue, ß/ss.

    NFC zuerst, damit zerlegte Umlaute (``u`` + U+0308, etwa aus macOS-
    Dateinamen oder kopiertem Text) wie zusammengesetzte gefunden werden.
    """
    value = unicodedata.normalize('NFC', value).casefold()
    for original, replacement in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        value = value.replace(original, replacement)
    return value


def search_key(text):
    """Bestehende Suchsemantik: zusammenhängender Text, ae/oe/ue/ss, NFC."""
    return _fold(' '.join(str(text or '').split()))


def title_rank(text, key):
    value = search_key(text)
    if not key or value.startswith(key):
        return 0
    if any(word.startswith(key) for word in value.split()):
        return 1
    return 2 if key in value else None


def matching_templates(templates, query):
    """Titel, Beschreibung und enthaltene Titel durchsuchen; Bestandsreihenfolge bewahren."""
    words = search_key(query).split()
    def texts(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ("title", "text", "note", "description") and isinstance(child, str):
                    yield child
                elif isinstance(child, (dict, list)):
                    yield from texts(child)
        elif isinstance(value, list):
            for child in value:
                if isinstance(child, str):
                    yield child
                else:
                    yield from texts(child)
    return [template for template in templates
            if all(word in search_key(" ".join(texts(template))) for word in words)]


def list_content(entry):
    """Nur sichtbarer Text; keine IDs, Formatmarken, URLs oder Bildbytes."""
    document = entry.get('rich_note')
    return tuple(text for text in (
        entry.get('note'), document.get('text') if isinstance(document, dict) else None
    ) if isinstance(text, str) and text.strip())


def _normal(text):
    """Wie `search_key`, aber ohne Leerraum zu verändern."""
    return _fold(text)


def _original_index(plain, position):
    """Index des Originalzeichens, aus dem die normalisierte Position `position` stammt.

    Die Länge normalisierter Anfangsstücke wächst nie, wenn ein Zeichen
    hinzukommt (ä → ae, ß → ss, Ligaturen verlängern; ein Kombinationszeichen
    verschmilzt höchstens mit seinem Grundzeichen); deshalb genügt eine
    Halbierungssuche – in C statt Zeichen für Zeichen (P07, 3.34.0).
    """
    lo, hi = 0, len(plain)
    while lo < hi:
        mid = (lo + hi) // 2
        if len(_normal(plain[:mid + 1])) > position:
            hi = mid
        else:
            lo = mid + 1
    return lo


def content_excerpt(text, key, limit=100):
    """Kurzer Originaltext um den Treffer, auch bei Umlaut-Umschreibungen."""
    if not key or limit < 4:
        return ''
    plain = ' '.join(str(text or '').split())
    normal = _normal(plain)
    position = normal.find(key)
    if position < 0:
        return ''
    if len(normal) == len(plain):
        first, last = position, position + len(key)
    else:
        first = _original_index(plain, position)
        last = _original_index(plain, position + len(key) - 1) + 1
    start = max(0, first - 24)
    end = min(len(plain), max(last, start + limit - 2))
    if end - start > limit - 2:
        start = first
        end = min(len(plain), start + limit - 2)
    return ('…' if start else '') + plain[start:end] + ('…' if end < len(plain) else '')


def match_content(title, texts, key):
    """Titel vor Inhalt; bei Inhaltstreffern ab zwei Zeichen mit Ausschnitt."""
    score = title_rank(title, key)
    if score is not None:
        return score, ''
    if len(key) >= 2:
        for text in texts:
            excerpt = content_excerpt(text, key)
            if excerpt:
                return 3, excerpt
    return None, ''


def match_spans(text, key, limit=500):
    """(Start, Ende) aller Vorkommen von `key` im Originaltext, als Zeichenpositionen.

    Dieselbe Gleichheit wie die Suche (NFC, Groß/Klein, ä/ae, ö/oe, ü/ue,
    ß/ss, Leerraum zusammengezogen), damit ein Treffer im Dokument genau dort
    markiert wird, wo die Suche ihn gefunden hat (G14h seit 3.34.0). Ein
    Grundzeichen und seine folgenden Kombinationszeichen gelten als eine
    Gruppe; ein Treffer schließt die Kombinationszeichen mit ein.
    """
    if not key:
        return []
    original = str(text or '')
    normal, starts, ends = [], [], []
    leer = False
    index, length = 0, len(original)
    while index < length:
        character = original[index]
        if character.isspace():
            if not leer:
                normal.append(' ')
                starts.append(index)
                ends.append(index + 1)
            leer = True
            index += 1
            continue
        leer = False
        end = index + 1
        while end < length and unicodedata.combining(original[end]):
            end += 1
        for teil in _fold(original[index:end]):
            normal.append(teil)
            starts.append(index)
            ends.append(end)
        index = end
    flach = ''.join(normal)
    spans = []
    position = flach.find(key)
    while position != -1 and len(spans) < limit:
        spans.append((starts[position], ends[position + len(key) - 1]))
        position = flach.find(key, position + len(key))
    return spans
