"""Inhaltssuche ohne Tk, Datei-I/O oder dauerhaften Index (G14, erste Stufe)."""


def search_key(text):
    """Bestehende Suchsemantik: zusammenhängender Text, ae/oe/ue/ss."""
    value = ' '.join(str(text or '').split()).casefold()
    for original, replacement in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        value = value.replace(original, replacement)
    return value


def title_rank(text, key):
    value = search_key(text)
    if not key or value.startswith(key):
        return 0
    if any(word.startswith(key) for word in value.split()):
        return 1
    return 2 if key in value else None


def list_content(entry):
    """Nur sichtbarer Text; keine IDs, Formatmarken, URLs oder Bildbytes."""
    document = entry.get('rich_note')
    return tuple(text for text in (
        entry.get('note'), document.get('text') if isinstance(document, dict) else None
    ) if isinstance(text, str) and text.strip())


def _normal(text):
    """Wie `search_key`, aber ohne Leerraum zu verändern; je Zeichen unabhängig."""
    value = text.casefold()
    for original, replacement in (('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss')):
        value = value.replace(original, replacement)
    return value


def _original_index(plain, position):
    """Index des Originalzeichens, aus dem die normalisierte Position `position` stammt.

    Die Normalisierung wirkt je Zeichen und verlängert höchstens (ä → ae,
    ß → ss, Ligaturen); deshalb genügt eine Halbierungssuche über die Länge
    normalisierter Anfangsstücke – in C statt Zeichen für Zeichen (P07, 3.34.0).
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

    Dieselbe Gleichheit wie die Suche (Groß/Klein, ä/ae, ö/oe, ü/ue, ß/ss,
    Leerraum zusammengezogen), damit ein Treffer im Dokument genau dort
    markiert wird, wo die Suche ihn gefunden hat (G14h seit 3.34.0).
    """
    if not key:
        return []
    original = str(text or '')
    normal, offsets = [], []
    leer = False
    for index, character in enumerate(original):
        if character.isspace():
            if not leer:
                normal.append(' ')
                offsets.append(index)
            leer = True
            continue
        leer = False
        for teil in search_key(character):
            normal.append(teil)
            offsets.append(index)
    flach = ''.join(normal)
    spans = []
    position = flach.find(key)
    while position != -1 and len(spans) < limit:
        spans.append((offsets[position], offsets[position + len(key) - 1] + 1))
        position = flach.find(key, position + len(key))
    return spans
