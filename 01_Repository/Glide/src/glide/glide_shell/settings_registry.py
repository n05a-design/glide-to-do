# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 22: settings registry for hosts (Shell 0.10.0).

Tk-free and storage-free. The shell does not own a settings file: the host
keeps its own persistent format (Glide: settings format 2) and uses this
registry to *describe* settings, fill defaults, validate values loaded from
anywhere and group them for a settings view. Shell-wide preferences that every
host has are offered as `shell_settings()`; product settings are registered by
the host with its own keys.

Public interface:

- `Setting(key, kind, default, group, label, choices=(), minimum=None,
  maximum=None, description="")` – `kind` is one of `bool`, `int`, `float`,
  `str`, `choice`. Invalid definitions raise `ValueError`.
- `SettingsRegistry(settings=())`: `register`, `extend`, `get`, `keys`,
  `groups`, `defaults()`, `coerce(key, value)` (returns a valid value or
  raises `ValueError`), `normalize(mapping)` -> `(values, problems)`:
  unknown keys are kept untouched (they belong to the host or a newer
  version), invalid values fall back to the default and are reported.
- `shell_settings()`: theme mode, accent, font scale, UI scale, reduced
  motion, language – all in group `"appearance"` or `"general"`.
- `framework_info()`: versions of the installed shell (and Bento when
  already loaded by the host) for a diagnostics or about view.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

KINDS = ("bool", "int", "float", "str", "choice")


@dataclass(frozen=True)
class Setting:
    key: str
    kind: str
    default: object
    group: str
    label: str
    choices: tuple = ()
    minimum: float | None = None
    maximum: float | None = None
    description: str = ""

    def __post_init__(self):
        if not self.key or not self.group or not self.label:
            raise ValueError("Setting needs key, group and label")
        if self.kind not in KINDS:
            raise ValueError(f"Setting {self.key!r}: kind must be one of {KINDS}")
        if self.kind == "choice" and self.default not in self.choices:
            raise ValueError(f"Setting {self.key!r}: default must be one of its choices")
        object.__setattr__(self, "choices", tuple(self.choices))
        self.coerce(self.default)

    def coerce(self, value):
        """Valid value for this setting or `ValueError`."""
        if self.kind == "bool":
            if isinstance(value, bool):
                return value
            raise ValueError(f"{self.key}: expected true/false, got {value!r}")
        if self.kind in ("int", "float"):
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise ValueError(f"{self.key}: expected a number, got {value!r}")
            if self.kind == "int":
                if float(value) != int(value):
                    raise ValueError(f"{self.key}: expected a whole number, got {value!r}")
                value = int(value)
            else:
                value = float(value)
            if self.minimum is not None and value < self.minimum or self.maximum is not None and value > self.maximum:
                raise ValueError(f"{self.key}: {value} outside {self.minimum}–{self.maximum}")
            return value
        if self.kind == "choice":
            if value in self.choices:
                return value
            raise ValueError(f"{self.key}: {value!r} is not one of {self.choices}")
        if not isinstance(value, str):
            raise ValueError(f"{self.key}: expected text, got {value!r}")
        return value


class SettingsRegistry:
    def __init__(self, settings=()):
        self._settings = {}
        self.extend(settings)

    def register(self, setting):
        if not isinstance(setting, Setting):
            raise TypeError("only Setting objects can be registered")
        if setting.key in self._settings:
            raise ValueError(f"duplicate setting key {setting.key!r}")
        self._settings[setting.key] = setting
        return setting

    def extend(self, settings):
        for setting in settings:
            self.register(setting)
        return self

    def get(self, key):
        return self._settings[key]

    def keys(self):
        return list(self._settings)

    def groups(self):
        """{group: [Setting, ...]} in registration order."""
        gruppen = {}
        for setting in self._settings.values():
            gruppen.setdefault(setting.group, []).append(setting)
        return gruppen

    def defaults(self):
        return {key: setting.default for key, setting in self._settings.items()}

    def coerce(self, key, value):
        return self._settings[key].coerce(value)

    def normalize(self, mapping):
        """(values, problems): defaults filled, invalid values replaced, unknown keys kept."""
        werte = dict(mapping or {})
        probleme = []
        for key, setting in self._settings.items():
            if key not in werte:
                werte[key] = setting.default
                continue
            try:
                werte[key] = setting.coerce(werte[key])
            except ValueError as fehler:
                probleme.append(str(fehler))
                werte[key] = setting.default
        return werte, probleme

    def __len__(self):
        return len(self._settings)


def shell_settings():
    """Shell-wide preferences; the host registers them next to its own."""
    return [
        Setting("shell.theme_mode", "choice", "system", "appearance", "Theme", choices=("system", "light", "dark")),
        Setting("shell.accent", "str", "", "appearance", "Accent colour", description="#RRGGBB or empty for the host default"),
        Setting("shell.font_scale", "float", 1.0, "appearance", "Text size", minimum=0.8, maximum=2.0),
        Setting("shell.ui_scale", "float", 1.0, "appearance", "Interface scale", minimum=0.75, maximum=3.0),
        Setting("shell.reduced_motion", "bool", False, "appearance", "Reduce motion"),
        Setting("shell.language", "str", "", "general", "Language", description="host language code or empty for system"),
    ]


def framework_info():
    """{"glide_shell": version, "glide_shell_compat_since": ..., "glide_bento": version or None}."""
    from glide_shell import SHELL_COMPAT_SINCE, SHELL_VERSION
    # The shell never imports Bento (layer rule 1); it reports Bento only when
    # the host has already loaded it.
    bento = sys.modules.get("glide_bento")
    return {"glide_shell": SHELL_VERSION, "glide_shell_compat_since": SHELL_COMPAT_SINCE,
            "glide_bento": getattr(bento, "BENTO_VERSION", None)}
