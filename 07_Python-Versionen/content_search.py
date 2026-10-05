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


def content_excerpt(text, key, limit=100):
    """Kurzer Originaltext um den Treffer, auch bei Umlaut-Umschreibungen."""
    if not key or limit < 4:
        return ''
    plain = ' '.join(str(text or '').split())
    # Erst den schnellen Normalvergleich; Positionsabbildung nur bei Treffer.
    if key not in search_key(plain):
        return ''
    offsets = []
    normalized = []
    for index, character in enumerate(plain):
        part = search_key(character) if not character.isspace() else ' '
        normalized.append(part)
        offsets.extend([index] * len(part))
    position = ''.join(normalized).find(key)
    first, last = offsets[position], offsets[position + len(key) - 1] + 1
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
