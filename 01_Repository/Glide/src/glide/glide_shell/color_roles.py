# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 21: portable colour-role contract and theme provider (Shell 0.10.0).

Tk-free. Every shell component reads colours from a *role dictionary* the host
supplies; this module defines which roles a complete theme has, neutral light
and dark defaults, how a host brings its own brand colour, and a small provider
that notifies views when the theme changes (light, dark, system, accent).

Role names follow the vocabulary Glide already uses, so `glide_bento`'s
`BentoContext.resolve_color` understands a theme from this module without a
mapping (``card``, ``bg``, ``line``, ``text``, ``muted``, ``ui_accent``).

Public interface:

- `CORE_ROLES`: roles every complete theme defines.
- `DERIVED_ROLES`: optional roles and the core role they fall back to.
- `neutral_theme(mode)`: neutral light or dark theme (`"light"`/`"dark"`).
- `complete(roles)`: copy with all derived roles filled in.
- `with_accent(roles, accent, on_accent=None)`: brand colour for accent, focus
  and selection; text on the accent is chosen by contrast when not given.
- `validate(roles)`: list of problems (missing roles, bad colours, contrast
  below WCAG 2.2 AA for text roles); empty means usable.
- `contrast_ratio(a, b)`, `relative_luminance(colour)`: WCAG formulas.
- `ThemeProvider`: holds mode, accent and per-mode overrides; `roles()`
  returns the resolved dictionary, `subscribe(callback)` returns an
  unsubscribe function, `set_mode`/`set_accent` notify subscribers once.

Error behaviour: invalid colours raise `ValueError` in `with_accent` and
`contrast_ratio`; `validate` reports instead of raising. Messages are English
(D96).
"""
from __future__ import annotations

import re

LIGHT = "light"
DARK = "dark"
SYSTEM = "system"
MODES = (LIGHT, DARK, SYSTEM)

CORE_ROLES = ("bg", "card", "input", "input_border", "text", "muted", "placeholder", "line",
              "hover", "selection", "selection_text", "ui_accent", "confirm", "delete")
# Optional role -> core role used when the host does not set it.
DERIVED_ROLES = {"accent": "ui_accent", "focus": "ui_accent", "warning": "delete",
                 "disabled": "muted", "on_accent": "selection_text", "error": "delete"}
# (foreground, background, minimum ratio) checked by `validate` (WCAG 2.2 AA).
CONTRAST_PAIRS = (("text", "bg", 4.5), ("text", "card", 4.5), ("text", "input", 4.5),
                  ("muted", "card", 3.0), ("selection_text", "selection", 4.5))

_NEUTRAL = {
    LIGHT: {"bg": "#F5F5F7", "card": "#FFFFFF", "input": "#FFFFFF", "input_border": "#C7C7CC",
            "text": "#1C1C1E", "muted": "#636366", "placeholder": "#8E8E93", "line": "#E5E5EA",
            "hover": "#E8F0FE", "selection": "#2F6FDB", "selection_text": "#FFFFFF",
            "ui_accent": "#2F6FDB", "confirm": "#1E7D3A", "delete": "#C62828", "warning": "#9A5B00"},
    DARK: {"bg": "#1C1C1E", "card": "#2C2C2E", "input": "#3A3A3C", "input_border": "#636366",
           "text": "#F2F2F7", "muted": "#AEAEB2", "placeholder": "#8E8E93", "line": "#48484A",
           "hover": "#33415C", "selection": "#5E9BFF", "selection_text": "#0B1220",
           "ui_accent": "#5E9BFF", "confirm": "#4CC26B", "delete": "#FF6B6B", "warning": "#F0B44C"},
}
_HEX = re.compile(r"^#([0-9a-fA-F]{6})$")


def _rgb(colour):
    treffer = _HEX.match(str(colour).strip())
    if not treffer:
        raise ValueError(f"colour must be #RRGGBB, got {colour!r}")
    wert = treffer.group(1)
    return tuple(int(wert[i:i + 2], 16) for i in (0, 2, 4))


def relative_luminance(colour):
    """WCAG relative luminance of a `#RRGGBB` colour (0.0–1.0)."""
    def kanal(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (kanal(c) for c in _rgb(colour))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(a, b):
    """WCAG contrast ratio between two colours (1.0–21.0)."""
    la, lb = sorted((relative_luminance(a), relative_luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def neutral_theme(mode=LIGHT):
    """Neutral, AA-conform theme for `mode` (`light` or `dark`); a fresh dict."""
    if mode not in _NEUTRAL:
        raise ValueError(f"mode must be 'light' or 'dark', got {mode!r}")
    return complete(_NEUTRAL[mode])


def complete(roles):
    """Copy of `theme` with every derived role filled from its core role."""
    ergebnis = dict(roles)
    for rolle, quelle in DERIVED_ROLES.items():
        if rolle not in ergebnis and quelle in ergebnis:
            ergebnis[rolle] = ergebnis[quelle]
    return ergebnis


def with_accent(roles, accent, on_accent=None):
    """Brand colour as accent, focus and selection; readable text on it."""
    _rgb(accent)
    if on_accent is None:
        on_accent = "#FFFFFF" if contrast_ratio(accent, "#FFFFFF") >= contrast_ratio(accent, "#000000") else "#000000"
    _rgb(on_accent)
    ergebnis = dict(roles)
    ergebnis.update(ui_accent=accent, accent=accent, focus=accent, selection=accent,
                    selection_text=on_accent, on_accent=on_accent)
    return complete(ergebnis)


def validate(roles):
    """Problems of `theme` as English sentences; an empty list means usable."""
    probleme = [f"missing role {rolle!r}" for rolle in CORE_ROLES if rolle not in roles]
    for rolle, wert in sorted(roles.items()):
        try:
            _rgb(wert)
        except ValueError:
            probleme.append(f"role {rolle!r} is not #RRGGBB: {wert!r}")
    for vorne, hinten, minimum in CONTRAST_PAIRS:
        try:
            verhaeltnis = contrast_ratio(roles[vorne], roles[hinten])
        except (KeyError, ValueError):
            continue
        if verhaeltnis < minimum:
            probleme.append(f"contrast {vorne}/{hinten} is {verhaeltnis:.2f}, needs {minimum}")
    return probleme


class ThemeProvider:
    """Resolved theme for the current mode with change notification.

    `system_is_dark` is a callable the host passes (for example
    `lambda: system_appearance.tk_is_dark(root)`); it is asked only in
    `system` mode. `overrides` maps `light`/`dark` to role dictionaries that
    replace neutral values (the host's own palette or brand identity).
    """

    def __init__(self, mode=SYSTEM, accent=None, overrides=None, system_is_dark=None):
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
        self.mode = mode
        self.accent = accent
        self.overrides = {k: dict(v) for k, v in (overrides or {}).items()}
        self.system_is_dark = system_is_dark or (lambda: False)
        self._subscribers = []

    def resolved_mode(self):
        if self.mode == SYSTEM:
            return DARK if self.system_is_dark() else LIGHT
        return self.mode

    def roles(self):
        mode = self.resolved_mode()
        thema = neutral_theme(mode)
        thema.update(self.overrides.get(mode, {}))
        thema = complete(thema)
        return with_accent(thema, self.accent) if self.accent else thema

    def subscribe(self, callback):
        """Call `callback(theme)` after each change; returns an unsubscribe function."""
        self._subscribers.append(callback)

        def abmelden():
            if callback in self._subscribers:
                self._subscribers.remove(callback)
        return abmelden

    def notify(self):
        thema = self.roles()
        for callback in list(self._subscribers):
            callback(thema)
        return thema

    def set_mode(self, mode):
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
        self.mode = mode
        return self.notify()

    def set_accent(self, accent):
        if accent is not None:
            _rgb(accent)
        self.accent = accent
        return self.notify()
