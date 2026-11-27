# SPDX-License-Identifier: MPL-2.0
"""Glide Bento Box System – Wiederverwendbare UI-Kompositionsschicht (D100).

Stellt generische Bento-Karten, adaptive Raster, semantische Tokens und einen
deterministischen Layout-Planner für Python/Tkinter bereit. Frei von Glide-Fachlogik.

Seit 0.3.0 prüft das Paket beim Import, ob die installierte Glide Shell zu
`SHELL_MIN_VERSION` passt (`glide_shell.compat.require_shell`); eine zu alte
oder inkompatible Shell bricht mit `ShellVersionError` ab, statt später an
einer fehlenden Funktion zu scheitern. `glide_bento.showcase` liefert die
Galerie-Einträge der Komponenten.
"""
from glide_shell.compat import ShellVersionError, require_shell

# Kleinste Shell-Fassung, gegen die Bento gebaut und geprüft ist.
SHELL_MIN_VERSION = "0.7.0"
require_shell(SHELL_MIN_VERSION, "glide_bento")

from .tokens import BentoTokens, DEFAULT_TOKENS
from .context import BentoContext
from .specs import BentoBand, BentoCardSpec, BentoGridSpec, BentoLane, BentoLayoutPlan
from .layout import BentoLayoutPlanner, effective_span
from .card import BentoCard, BentoHeader
from .grid import BentoGrid
from .components import BentoMetric, BentoActions, BentoEmptyState, BentoDivider

BENTO_VERSION = "0.3.0"
__version__ = BENTO_VERSION

__all__ = [
    "BENTO_VERSION",
    "SHELL_MIN_VERSION",
    "ShellVersionError",
    "__version__",
    "BentoTokens",
    "DEFAULT_TOKENS",
    "BentoContext",
    "BentoCardSpec",
    "BentoGridSpec",
    "BentoLayoutPlan",
    "BentoBand",
    "BentoLane",
    "BentoLayoutPlanner",
    "effective_span",
    "BentoCard",
    "BentoHeader",
    "BentoGrid",
    "BentoMetric",
    "BentoActions",
    "BentoEmptyState",
    "BentoDivider",
]
