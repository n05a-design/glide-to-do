#!/usr/bin/env python3
"""Gezielte 3.6.0-Prüfung für neue, plattformunabhängige Bausteine."""

from __future__ import annotations

import importlib.util
import importlib.machinery
import json
import os
import tempfile
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
_isolated = tempfile.TemporaryDirectory(prefix="glide-36-units-")
os.environ["GLIDE_DATA_DIR"] = _isolated.name
loader = importlib.machinery.SourceFileLoader("glide_app_36", str(ROOT / "src/glide/app.pyw"))
spec = importlib.util.spec_from_loader(loader.name, loader)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert mod.APP_VERSION == "3.33.1"
assert mod.moon_phase_info(date(2000, 1, 6))["percent"] == 0
assert mod.moon_phase_info(date(2000, 1, 20))["percent"] > 90

settings = mod.ListApp.normalize_personal_settings({
    "settings_version": 1,
    "completion_history": {
        (date.today() - timedelta(days=370)).isoformat(): 2,
        (date.today() - timedelta(days=372)).isoformat(): 3,
        "kein-datum": 9,
    },
    "show_moon_phase": False,
    "show_yearly_stats": True,
    "week_start": "sunday",
    "ui_font_size": "gross",
    "glass_mode": True,
})
assert settings["settings_version"] == 2
assert len(settings["completion_history"]) == 1
assert settings["week_start"] == "sunday"
assert settings["ui_font_size"] == "gross"
assert settings["show_moon_phase"] is False
assert settings["show_yearly_stats"] is True
assert settings["glass_mode"] is True

solid = mod.ListApp.normalize_personal_settings({"glass_mode": False})
assert solid["glass_mode"] is False

templates = mod.ListApp.normalize_template_records({"templates": [
    {"id": "custom", "kind": "list", "title": "  Eigene Liste ", "items": ["A", "B"]},
    {"id": "folder", "kind": "folder", "title": "Projekt", "items": ["Plan"]},
]})
assert [item["kind"] for item in templates] == ["list", "folder"]
assert templates[0]["title"] == "Eigene Liste"
assert templates[0]["items"] == ["A", "B"]
assert templates[1]["kind"] == "folder"

stats = mod.YearHeatmap.statistics({
    date.today().isoformat(): 4,
    (date.today() - timedelta(days=1)).isoformat(): 2,
})
assert stats == {"active_days": 2, "total": 6, "best_day": 4, "streak": 2}

print("Glide v3.6.0 neue Bausteine: Mondphase, Jahresanzeige, Einstellungen und Vorlagen: OK")
_isolated.cleanup()
