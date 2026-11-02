"""Erscheinungsbild „Automatisch (hell/dunkel)“ ohne Tk (N01 seit 3.33.21).

Glide kennt Designpaare (Hell/Dunkel, Liquid Glass, Minimal, Kontrast) und
zwei Designs nur auf dunklem Grund (Pixel, Dopamin). Folgt Glide dem System,
merkt es sich ein Paar: das helle und das dunkle Design. Für ein Design ohne
helles Gegenstück gilt bei hellem System „Hell“ – neue Farben entstehen nicht.

Erkannt wird der Systemmodus über Tk (macOS), die Registrierung (Windows) oder
die Desktop-Einstellung (Linux). Jede Erkennung darf scheitern; dann bleibt
das zuletzt gewählte Design stehen.
"""

LIGHT_FALLBACK = "light"


def pair_for(design, designs):
    """{"light": …, "dark": …} für ein Design aus der Designtabelle."""
    eintrag = designs.get(design)
    if eintrag is None:
        return None
    partner = eintrag.get("partner") or design
    if partner == design or partner not in designs:
        if eintrag.get("base") == "light":
            return {"light": design, "dark": design}
        return {"light": LIGHT_FALLBACK if LIGHT_FALLBACK in designs else design, "dark": design}
    if eintrag.get("base") == "light":
        return {"light": design, "dark": partner}
    return {"light": partner, "dark": design}


def normalize_auto(value, designs):
    """Gespeichertes Paar prüfen; Unlesbares oder Unbekanntes ergibt None (aus)."""
    if not isinstance(value, dict):
        return None
    hell, dunkel = value.get("light"), value.get("dark")
    if hell not in designs or dunkel not in designs:
        return None
    return {"light": hell, "dark": dunkel}


def resolve(auto, system_dark, current):
    """Wirksames Design: aus dem Paar nach Systemmodus, sonst das aktuelle."""
    if not auto or system_dark is None:
        return current
    return auto["dark"] if system_dark else auto["light"]


# --- Erkennung -----------------------------------------------------------
def windows_is_dark(read_value):
    """`read_value()` liefert AppsUseLightTheme (0 = dunkel) oder wirft OSError."""
    try:
        wert = read_value()
    except (OSError, ValueError, TypeError):
        return None
    if isinstance(wert, bool) or not isinstance(wert, int):
        return None
    return wert == 0


def linux_is_dark(color_scheme=None, gtk_theme=None):
    """Ausgabe von `gsettings get …` deuten: color-scheme zuerst, dann der GTK-Name."""
    schema = str(color_scheme or "").strip().strip("'\"").lower()
    if schema == "prefer-dark":
        return True
    if schema in ("prefer-light", "default") and not gtk_theme:
        return False
    thema = str(gtk_theme or "").strip().strip("'\"").lower()
    if thema:
        return thema.endswith("-dark") or ":dark" in thema
    return False if schema else None


def tk_is_dark(answer):
    """Antwort von `tk::unsupported::MacWindowStyle isdark` oder `winfo isdark` deuten."""
    text = str(answer).strip().lower()
    if text in ("1", "true", "yes"):
        return True
    if text in ("0", "false", "no"):
        return False
    return None
BACKGROUND_CHOICES = (
    ('Designvorgabe', 'default'), ('Wie die Fensterfläche · ohne Schatten', 'surface'),
    ('Lila', 'accent'), ('Blau', 'clear'), ('Türkis', 'due_action'),
    ('Grün', 'export'), ('Gelb', 'flag'), ('Rot', 'delete'),
    ('Braun', 'import'), ('Kontrastgrau', 'muted'),
)
BACKGROUND_KEYS = frozenset(key for _label, key in BACKGROUND_CHOICES)


def background_choice(value):
    return value if isinstance(value, str) and value in BACKGROUND_KEYS else 'default'


def with_background(theme, choice):
    """Nur den Hintergrund färben; Arbeitsflächen und Rollen bleiben erhalten."""
    from backdrop import hex_rgb, rgb_hex, mix, luminance
    result = dict(theme)
    choice = background_choice(choice)
    if choice == 'surface':
        result['bg'] = result['card']
        result['glass_shadow'] = result['card']
        result['glass_gradient'] = ''
    elif choice != 'default':
        # Ruhige Töne derselben festen Palette erhalten den Schriftkontrast.
        base = hex_rgb(result['bg'])
        share = 0.16 if luminance(base) < 0.2 else 0.08
        result['bg'] = rgb_hex(mix(base, hex_rgb(result[choice]), share))
    return result
