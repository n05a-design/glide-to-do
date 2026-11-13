# SPDX-License-Identifier: MPL-2.0
"""Gemeinsame Gestaltungsskalen und reine Regeln für Titel und Herkunft.

Vier Inhaltsstufen: Seitentitel, Abschnitt, Inhalt und Zusatzangabe.
Bestehende Symbol- und Bediengrößen bleiben unabhängig davon.
"""
from types import MappingProxyType

SPACING = MappingProxyType({value: value for value in
                           (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 22, 24, 28, 30)})
RADII = MappingProxyType({"card": 18, "field": 16})
FONT_SIZES = MappingProxyType({"caption": 9, "source": 9, "body": 12, "section": 16, "title": 22})
ROW_HEIGHTS = MappingProxyType({"task": 36})
TITLE_MAX_CHARS = 40
BUTTON_TEXT_MAX_CHARS = 24


def remaining_text(length, limit=TITLE_MAX_CHARS, short=False):
    """Restzähler einer begrenzten Eingabe (D67, 07.11.2026): zählt von der Grenze herunter."""
    rest = int(limit) - max(0, int(length or 0))
    if rest > 0:
        return f"noch {rest}" if short else ("noch 1 Zeichen" if rest == 1 else f"noch {rest} Zeichen")
    if rest == 0:
        return "0 übrig" if short else "keine Zeichen mehr frei"
    return f"{-rest} zu viel" if short else ("1 Zeichen zu viel" if rest == -1 else f"{-rest} Zeichen zu viel")


def limit_message(limit=TITLE_MAX_CHARS, dropped=0, short=False):
    """Klare Meldung, wenn eine Eingabe die Grenze überschreiten würde (D67)."""
    if short:
        return f"{int(dropped)} gekürzt" if dropped else f"max. {int(limit)}"
    text = f"Höchstens {int(limit)} Zeichen"
    return text + (f" · {int(dropped)} nicht übernommen" if dropped else "")


def clip_title(text, limit=TITLE_MAX_CHARS, ellipsis="..."):
    """Zeichengrenze einschließlich Auslassung; keine Änderung am Quellobjekt."""
    text = str(text or "")
    if len(text) <= limit:
        return text
    if limit < len(ellipsis):
        return ""
    return text[:limit - len(ellipsis)].rstrip() + ellipsis


def edited_title(text, previous):
    """Alttitel bei reinen Metadatenänderungen bewahren, geänderte Titel begrenzen."""
    return text if text == previous else clip_title(text)


def task_title(text, description="", *, preserve=False):
    """Neue Titel begrenzen und ihr Original sichern; Altdaten vollständig bewahren."""
    clipped = text if preserve else clip_title(text)
    if clipped != text:
        description = (str(description or "").rstrip() + "\n\nOriginaltitel:\n" + text).lstrip()
    return clipped, description


def edited_task_title(text, previous, description=""):
    """Unveränderte Alttitel bewahren; neue lange Eingaben vollständig sichern."""
    return task_title(text, description, preserve=text == previous)


def display_title(text, measure, width, limit=TITLE_MAX_CHARS):
    """Zeichen- und Pixelgrenze gemeinsam; vollständiger Titel bleibt beim Aufrufer."""
    return fit_text(clip_title(" ".join(str(text or "").split()), limit), measure, width, ellipsis="...")


def page_icon_layout(left_padding, line_height, preferred_scale, cell_size=16, gap=8):
    """Symbol im linken Leserand halten; die Textkante bleibt bei x=0."""
    scale = min(max(1, int(preferred_scale)), int((left_padding - gap) // cell_size),
                int(line_height // cell_size))
    if scale < 1:
        return None
    size = cell_size * scale
    return scale, -size - gap, (int(line_height) - size) // 2


def fit_text(text, measure, width, ellipsis="…"):
    """Einzeilig kürzen; vollständiger Text bleibt beim Aufrufer erhalten."""
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


def today_columns(width, due, labels):
    """Titel behält mindestens 260 px, Herkunft höchstens 180 px rechts.

    Labels und Fälligkeit weichen bei Enge wie bisher; die Herkunft bleibt
    sichtbar. Die Quelle wird im verbleibenden Raum mit Auslassung gekürzt.
    """
    source = min(180, max(100, int(width * .25)))
    edge = 6
    # B11: Der Titel bleibt zusätzlich die breiteste Spalte. Seit der breiteren
    # Standardschrift Roboto Mono (D59) war die Fälligkeit mit Bearbeitungstag
    # sonst breiter als der Titel.
    if width - source - due - labels - 24 - edge < max(260, due + 1, labels + 1):
        labels = 0
    if width - source - due - 24 - edge < max(260, due + 1):
        due = 0
    gap = 24 if due or labels else 0
    return max(260, width - source - due - labels - gap - edge), due, labels, source, gap


# Widgetklassen, in denen Entf/Rücktaste Text bearbeiten (Mac-Abnahme 07.11.2026).
TEXT_INPUT_CLASSES = frozenset({"Entry", "Text", "TEntry", "Spinbox", "TSpinbox", "TCombobox"})


def widget_within(path, container):
    """Ob ein Tk-Widgetpfad gleich `container` ist oder darin liegt.

    Vergleicht mit Punkt als Trenner: `.!frame7` enthält nicht `.!frame70`.
    """
    if not path or not container:
        return False
    return path == container or path.startswith(container.rstrip(".") + ".")


def delete_key_edits_text(widget_class, path, input_paths=(), pane_path=None):
    """Ob Entf/Rücktaste im Widget Text bearbeiten statt einen Punkt zu löschen.

    Text-/Eingabefelder jeder Art, ausdrücklich genannte Eingaben (Eingabezeile,
    Suche) und alles in der Seitenansicht/dem Inspektor gelten als Text.
    """
    if path and path in set(input_paths or ()):
        return True
    if widget_class in TEXT_INPUT_CLASSES:
        return True
    return widget_within(path, pane_path)


def stale_empty_frame(has_slaves, configured_width, configured_height, requested_width, requested_height):
    """Ob ein leerer Rahmen noch die Größe seiner entfernten Kinder beansprucht.

    Tk setzt die Wunschgröße eines Rahmens beim Entfernen des letzten Kinds
    nicht zurück: Er bleibt so groß wie zuvor und zeigt eine leere Fläche
    (Mac-Abnahme 07.11.2026: „Erwähnt ohne Verweis“ zuklappen, Live-Liste
    lösen). Ein Rahmen ohne Kinder und ohne eigene Größenangabe hat Ruhegröße
    1 × 1; alles darüber ist ein Rest.
    """
    if has_slaves or configured_width or configured_height:
        return False
    return requested_width > 1 or requested_height > 1


def settled_wrap_width(width, seen):
    """Umbruchbreite, die auch bei einer Layoutschaukel zur Ruhe kommt.

    `seen` sammelt die Breiten, die bei unveränderter Fensterbreite schon
    gesetzt wurden. Eine neue Breite gilt wie gemeldet. Kehrt eine gesehene
    wieder, schaukeln Umbruch und Spaltenbreite einander auf; dann gilt die
    engste gesehene Breite, und jede weitere gesehene Breite ändert nichts.
    Der Aufrufer leert `seen`, sobald das Fenster seine Breite ändert.
    """
    if width in seen:
        return min(seen)
    seen.add(width)
    return width


HAIR_SPACE = "\u200a"


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
    """Erledigt-/Offen-Zeichen auf gleiche Breite bringen (Mac-Abnahme 07.11.2026).

    „✓“ und „□“ sind in den meisten Schriften unterschiedlich breit; vor
    Zeilentext gesetzt, sprang die Textkante erledigter Punkte nach rechts.
    """
    markers = tuple(dict.fromkeys(markers))
    target = max(measure(marker) for marker in markers)
    return {marker: pad_to_width(marker, target, measure, filler) for marker in markers}

