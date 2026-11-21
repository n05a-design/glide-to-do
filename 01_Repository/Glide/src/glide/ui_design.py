# SPDX-License-Identifier: MPL-2.0
"""Gemeinsame Gestaltungsskalen und reine Regeln für Titel und Herkunft.

Vier Inhaltsstufen: Seitentitel, Abschnitt, Inhalt und Zusatzangabe.
Bestehende Symbol- und Bediengrößen bleiben unabhängig davon. Die neutralen
Textregeln (Kürzen, Breitenausgleich, ruhige Umbruchbreite) liegen seit V1.69
in `glide_shell.text_fit` (S10, D98); dieses Modul reicht sie weiter und
behält Grenzen, Skalen und Glide-Layouts.
"""
from types import MappingProxyType

from glide_shell import text_fit as _text_fit
from glide_shell.text_fit import HAIR_SPACE, aligned_markers, pad_to_width, settled_wrap_width  # noqa: F401
import i18n as glide_i18n

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
        return glide_i18n.t("mod.ui_design.remaining_text.left", 'noch {rest}', rest=rest) if short else (glide_i18n.t("mod.ui_design.remaining_text.1_character_left", "noch 1 Zeichen") if rest == 1 else glide_i18n.t("mod.ui_design.remaining_text.characters_left", 'noch {rest} Zeichen', rest=rest))
    if rest == 0:
        return glide_i18n.t("mod.ui_design.remaining_text.0_left", "0 übrig") if short else glide_i18n.t("mod.ui_design.remaining_text.no_characters_left", "keine Zeichen mehr frei")
    return glide_i18n.t("mod.ui_design.remaining_text.too_many", '{wert} zu viel', wert=-rest) if short else (glide_i18n.t("mod.ui_design.remaining_text.1_character_too_many", "1 Zeichen zu viel") if rest == -1 else glide_i18n.t("mod.ui_design.remaining_text.characters_too_many", '{wert} Zeichen zu viel', wert=-rest))


def limit_message(limit=TITLE_MAX_CHARS, dropped=0, short=False):
    """Klare Meldung, wenn eine Eingabe die Grenze überschreiten würde (D67)."""
    if short:
        return glide_i18n.t("mod.ui_design.limit_message.shortened", '{int} gekürzt', int=int(dropped)) if dropped else f"max. {int(limit)}"
    text = glide_i18n.t("mod.ui_design.limit_message.at_most_characters", 'Höchstens {int} Zeichen', int=int(limit))
    return text + (glide_i18n.t("mod.ui_design.limit_message.not_taken_over", ' · {int} nicht übernommen', int=int(dropped)) if dropped else "")


def clip_title(text, limit=TITLE_MAX_CHARS, ellipsis="..."):
    """Zeichengrenze einschließlich Auslassung; keine Änderung am Quellobjekt."""
    return _text_fit.clip(text, limit, ellipsis)



def edited_title(text, previous):
    """Alttitel bei reinen Metadatenänderungen bewahren, geänderte Titel begrenzen."""
    return text if text == previous else clip_title(text)


def task_title(text, description="", *, preserve=False):
    """Neue Titel begrenzen und ihr Original sichern; Altdaten vollständig bewahren."""
    clipped = text if preserve else clip_title(text)
    if clipped != text:
        description = (glide_i18n.t("mod.ui_design.task_title.original_title", '{rstrip}\n\nOriginaltitel:\n{text}', rstrip=str(description or "").rstrip(), text=text)).lstrip()
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


fit_text = _text_fit.fit



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


def reflow_repeats(width, seen, now, last_at, quiet=1.0, window=None, last_window=None):
    """Ob eine Neuumbruch-Breite in einer schnellen Folge schon an der Reihe war.

    Die Aufgabenliste bricht Langtexte nach jeder Breitenänderung neu um. Bei
    geöffnetem Inspektor schaukelten Umbruch, Zeilenaktionen und Spaltenbreite
    einander auf (Mac 1710 × 1112, 21.11.2026: 209 → 215 → 221 → 225 → 209 …
    ohne Ende). Kommt eine Breite innerhalb von `quiet` Sekunden nach dem
    letzten Umbruch wieder, ist das diese Schaukel: kein weiterer Umbruch.
    Nach einer ruhigen Pause gilt jede Breite wieder als neu, so dass Öffnen
    und Schließen des Inspektors normal umbrechen. Ändert sich die
    Fensterbreite (`window` gegenüber `last_window`), ist das eine äußere
    Größenänderung und keine Schaukel: Jede Breite gilt dann wieder als neu,
    auch wenn der Nutzer die Größe innerhalb einer Sekunde zurücknimmt.
    `seen` gehört dem Aufrufer.
    """
    if now - last_at > quiet or window != last_window:
        seen.clear()
    if width in seen:
        return True
    seen.add(width)
    return False


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


DRAWING_DISPLAY_PROFILES = MappingProxyType({
    "standard": "Standard", "extended": "Erweitert",
    "animation": "Animation", "pixelate": "Bilder pixeln",
})


def normalize_drawing_profile(value):
    """Ungültige/alte Einstellungswerte ändern keine Werkzeuge oder Dokumente."""
    return value if isinstance(value, str) and value in DRAWING_DISPLAY_PROFILES else "standard"


def drawing_controls(profile):
    """Sichtbare Zusatzleisten; Zeichnungs- und Werkzeugzustand bleiben gleich."""
    return {"standard": (), "extended": ("animation", "reference"),
            "animation": ("animation",), "pixelate": ("reference",)}[normalize_drawing_profile(profile)]
