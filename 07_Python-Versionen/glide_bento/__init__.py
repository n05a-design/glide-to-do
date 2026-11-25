# SPDX-License-Identifier: MPL-2.0
"""Glide Bento Box System – Wiederverwendbare UI-Kompositionsschicht (D100).

Stellt generische Bento-Karten, adaptive Raster, semantische Tokens und einen
deterministischen Layout-Planner für Python/Tkinter bereit. Frei von Glide-Fachlogik.
"""

from .tokens import BentoTokens, DEFAULT_TOKENS
from .context import BentoContext
from .specs import BentoCardSpec, BentoGridSpec, BentoLayoutPlan
from .layout import BentoLayoutPlanner
from .card import BentoCard, BentoHeader
from .grid import BentoGrid
from .components import BentoMetric, BentoActions, BentoEmptyState, BentoDivider

BENTO_VERSION = "0.1.0"
__version__ = BENTO_VERSION

__all__ = [
    "BENTO_VERSION",
    "__version__",
    "BentoTokens",
    "DEFAULT_TOKENS",
    "BentoContext",
    "BentoCardSpec",
    "BentoGridSpec",
    "BentoLayoutPlan",
    "BentoLayoutPlanner",
    "BentoCard",
    "BentoHeader",
    "BentoGrid",
    "BentoMetric",
    "BentoActions",
    "BentoEmptyState",
    "BentoDivider",
]
