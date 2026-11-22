# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 12: Text in eine Breite bringen, ohne Tk (S10, D98).

Reine Regeln, die jede Tk-Anwendung für Beschriftungen braucht:
- `clip` kürzt auf eine Zeichengrenze einschließlich Auslassung,
- `fit` kürzt einzeilig auf eine Pixelbreite; gemessen wird über eine vom
  Host gelieferte Funktion (etwa `font.measure`),
- `settled_wrap_width` beruhigt eine Umbruchbreite, die mit der
  Spaltenbreite schaukelt,
- `pad_to_width` und `aligned_markers` gleichen Zeichen wie „✓“ und „□“
  mit schmalen Leerzeichen auf eine Breite an.

Grenzen, Schriftskalen und Glide-Layouts (`task_title`, `today_columns`,
`page_icon_layout`) bleiben beim Host in `ui_design.py`. Der vollständige
Text bleibt immer beim Aufrufer. Vertrag: `tests/unit/test_shell_d98.py`.
"""

HAIR_SPACE = "\u200a"


def clip(text, limit, ellipsis="..."):
    """Zeichengrenze einschließlich Auslassung; keine Änderung am Quellobjekt."""
    text = str(text or "")
    if len(text) <= limit:
        return text
    if limit < len(ellipsis):
        return ""
    return text[:limit - len(ellipsis)].rstrip() + ellipsis


def fit(text, measure, width, ellipsis="…"):
    """Einzeilig kürzen, bis `measure(text)` in `width` passt."""
    if not text or width <= 0:
        return ""
    if measure(text) <= width:
        return text
    if measure(ellipsis) > width:
        return ""
    low, high = 0, len(text)
    while low < high:
        mid = (low + high + 1) // 2
        if measure(text[:mid] + ellipsis) <= width:
            low = mid
        else:
            high = mid - 1
    return text[:low].rstrip() + ellipsis


def settled_wrap_width(width, seen):
    """Umbruchbreite, die auch bei einer Layoutschaukel zur Ruhe kommt.

    `seen` sammelt die Breiten, die bei unveränderter Fensterbreite schon
    gesetzt wurden. Eine neue Breite gilt wie gemeldet. Kehrt eine gesehene
    wieder, gilt die engste gesehene Breite. Der Aufrufer leert `seen`,
    sobald das Fenster seine Breite ändert.
    """
    if width in seen:
        return min(seen)
    seen.add(width)
    return width


def pad_to_width(text, target, measure, filler=HAIR_SPACE, limit=12):
    """`text` mit schmalen Leerzeichen so nah wie möglich auf `target` Pixel bringen."""
    best, best_error = text, abs(target - measure(text))
    current = text
    for _ in range(limit):
        if measure(current) >= target:
            break
        current += filler
        error = abs(target - measure(current))
        if error < best_error:
            best, best_error = current, error
    return best


def aligned_markers(markers, measure, filler=HAIR_SPACE):
    """Zeichen gleicher Rolle (etwa „✓“ und „□“) auf eine gemeinsame Breite bringen."""
    markers = tuple(dict.fromkeys(markers))
    target = max(measure(marker) for marker in markers)
    return {marker: pad_to_width(marker, target, measure, filler) for marker in markers}
