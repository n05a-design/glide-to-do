# SPDX-License-Identifier: MPL-2.0
"""Internationalisierung (i18n) für Glide (M100).

Zentrale Spracherkennung, Katalogladung und Übersetzung für Deutsch und Englisch.
Erfüllt das Qualitätsbudget (WA-50): importiert ausschließlich die Standardbibliothek,
kein Tkinter-Bezug, alle Funktionen <= 50 Zeilen, Verzweigungstiefe <= 15.
"""

import json
import locale
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

DEFAULT_LANGUAGE = "de"
SUPPORTED_LANGUAGES: Tuple[str, ...] = ("de", "en")
LANGUAGE_NAMES: Dict[str, str] = {
    "system": "Automatisch (System)",
    "de": "Deutsch",
    "en": "English",
}

_CATALOGS: Dict[str, Dict[str, str]] = {}
_ACTIVE_LANGUAGE: str = DEFAULT_LANGUAGE


def get_locales_dir() -> Path:
    """Gibt den Pfad zum Verzeichnis der Übersetzungskataloge zurück."""
    return Path(__file__).resolve().parent / "resources" / "locales"


def detect_system_language() -> str:
    """Ermittelt die bevorzugte Sprache des Betriebssystems.

    Prüft nacheinander Umgebungsvariablen (LANGUAGE, LC_ALL, LC_MESSAGES, LANG)
    sowie locale.getlocale(). Fällt bei englischer Kennung auf 'en', sonst auf 'de' zurück.
    """
    for var in ("LANGUAGE", "LC_ALL", "LC_MESSAGES", "LANG"):
        val = os.environ.get(var)
        if val:
            prefix = val.split(".")[0].split("_")[0].lower()
            if prefix == "en":
                return "en"
            if prefix == "de":
                return "de"
    try:
        loc = locale.getlocale()[0]
        if loc:
            prefix = loc.split("_")[0].lower()
            if prefix == "en":
                return "en"
    except Exception:
        pass
    return DEFAULT_LANGUAGE


def resolve_language(preference: Optional[str]) -> str:
    """Löst eine Spracheinstellung ('system', 'de', 'en' oder None) deterministisch auf."""
    if not preference or preference == "system":
        return detect_system_language()
    norm = preference.strip().lower()
    if norm in SUPPORTED_LANGUAGES:
        return norm
    return DEFAULT_LANGUAGE


def load_catalog(lang: str) -> Dict[str, str]:
    """Lädt einen Übersetzungskatalog aus der entsprechenden JSON-Ressource.

    Nutzt internen Cache. Schlägt das Laden fehl, wird ein leeres Dict zurückgegeben.
    """
    if lang in _CATALOGS:
        return _CATALOGS[lang]
    catalog_path = get_locales_dir() / f"{lang}.json"
    if not catalog_path.is_file():
        _CATALOGS[lang] = {}
        return _CATALOGS[lang]
    try:
        raw_text = catalog_path.read_text(encoding="utf-8")
        data = json.loads(raw_text)
        if isinstance(data, dict):
            _CATALOGS[lang] = {str(k): str(v) for k, v in data.items()}
        else:
            _CATALOGS[lang] = {}
    except Exception:
        _CATALOGS[lang] = {}
    return _CATALOGS[lang]


def set_language(preference: Optional[str]) -> str:
    """Setzt die aktive Sprache anhand der Nutzerpräferenz oder des Systems."""
    global _ACTIVE_LANGUAGE
    resolved = resolve_language(preference)
    _ACTIVE_LANGUAGE = resolved
    load_catalog(resolved)
    if resolved != DEFAULT_LANGUAGE:
        load_catalog(DEFAULT_LANGUAGE)
    return _ACTIVE_LANGUAGE


def get_language() -> str:
    """Liefert den Code der aktuell aktiven Sprache ('de' oder 'en')."""
    return _ACTIVE_LANGUAGE


def get_supported_languages() -> Tuple[str, ...]:
    """Liefert die Liste aller direkt unterstützten Sprachkürzel."""
    return SUPPORTED_LANGUAGES


def get_language_display_names() -> Dict[str, str]:
    """Liefert die für Menschen lesbaren Namen der Sprachoptionen."""
    return dict(LANGUAGE_NAMES)


def safe_format(template: str, kwargs: Dict[str, Any]) -> str:
    """Formatiert einen Text mit Variablen; fängt Formatierungsfehler sicher ab."""
    if not kwargs:
        return template
    try:
        return template.format(**kwargs)
    except (KeyError, ValueError, IndexError):
        return template


def t(key: str, default: Optional[str] = None, **kwargs: Any) -> str:
    """Übersetzt einen Schlüssel in der aktiven Sprache mit Fallback und Formatierung.

    1. Prüft den aktiven Katalog (_ACTIVE_LANGUAGE).
    2. Fällt auf den Standardkatalog ('de') zurück, falls der Schlüssel fehlt.
    3. Fällt auf `default` oder den übergebenen `key` zurück.
    4. Interpoliert kwargs sicher mit safe_format.
    """
    active_cat = load_catalog(_ACTIVE_LANGUAGE)
    if key in active_cat:
        return safe_format(active_cat[key], kwargs)
    if _ACTIVE_LANGUAGE != DEFAULT_LANGUAGE:
        default_cat = load_catalog(DEFAULT_LANGUAGE)
        if key in default_cat:
            return safe_format(default_cat[key], kwargs)
    fallback = default if default is not None else key
    return safe_format(fallback, kwargs)


def clear_cache() -> None:
    """Leert den Katalog-Cache und setzt die aktive Sprache auf den Standard zurück."""
    global _ACTIVE_LANGUAGE
    _CATALOGS.clear()
    _ACTIVE_LANGUAGE = DEFAULT_LANGUAGE
