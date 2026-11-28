# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 25: software catalog and product manifests for an ecosystem (Shell 0.11.0).

Tk-free, no network. A catalog is a versioned JSON document (format
`glide-software-catalog`, version 1) that lists products with stable ids. The
shell ships the ecosystem catalog `ECOSYSTEM_CATALOG.json` next to this module;
a host may load another file with the same contract. Catalog data describes
products in general; the *local* app version and the installed framework
versions come from the running host (`AppInfo`) and are never written into the
catalog.

Rules of the contract:

- Only known facts. Every optional field may be missing; `UNKNOWN` (the string
  ``"unknown"``) marks a field that was checked and is not known. Hosts show
  missing and unknown fields as absent, never as invented values.
- Links are plain `https://` URLs and open only on a deliberate user action
  (`open_link` with a host-supplied opener). Nothing is fetched automatically.
- Texts may carry language variants: ``{"de": "...", "en": "..."}``;
  `text(value, language)` picks one with fallback to English, then German.

Public interface:

- `Product` (frozen dataclass) and `Catalog` (`products`, `get`, `others(id)`,
  `categories()`, `problems`), `load(path)`, `load_ecosystem()`, `parse(data)`.
- `AppInfo(product_id, name, version, status, frameworks, extra)` and
  `system_info(root=None)` – Python, Tk, OS and framework versions for an about view.
- `text(value, language)`, `validate_url(url)`, `open_link(url, opener)`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import platform
import re
import sys

FORMAT = "glide-software-catalog"
VERSION = 1
UNKNOWN = "unknown"
STATUSES = ("concept", "development", "prerelease", "released", "maintenance", "discontinued", UNKNOWN)
PLATFORMS = ("windows", "macos", "linux")
LINK_KEYS = ("website", "repository", "documentation", "download")
ECOSYSTEM_CATALOG = Path(__file__).with_name("ECOSYSTEM_CATALOG.json")
_ID = re.compile(r"^[a-z0-9][a-z0-9._-]{1,63}$")
_URL = re.compile(r"^https://[A-Za-z0-9.-]+(?::\d+)?(?:/[^\s]*)?$")
_HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def text(value, language="en"):
    """A plain string or one language variant (fallback en → de → first)."""
    if isinstance(value, dict):
        for key in (language, "en", "de"):
            if isinstance(value.get(key), str) and value[key].strip():
                return value[key]
        return next((v for v in value.values() if isinstance(v, str)), "")
    return value if isinstance(value, str) else ""


def validate_url(url):
    """True for an absolute https URL without whitespace."""
    return isinstance(url, str) and bool(_URL.match(url))


def open_link(url, opener):
    """Open `url` through the host's opener after validation; False if refused."""
    if not validate_url(url) or not callable(opener):
        return False
    opener(url)
    return True


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    summary: object = ""
    description: object = ""
    category: object = ""
    features: tuple = ()
    brand_color: str | None = None
    logo: str | None = None
    icon: str | None = None
    links: dict = field(default_factory=dict)
    license: str | None = None
    platforms: tuple = ()
    version: str | None = None
    status: str = UNKNOWN
    languages: tuple = ()
    publisher: str | None = None

    def known(self, name):
        """Value of field `name`, or None when it is missing or marked unknown."""
        value = getattr(self, name, None)
        if value in (None, "", (), {}) or value == UNKNOWN:
            return None
        return value

    def link(self, key):
        url = self.links.get(key)
        return url if validate_url(url) else None


class Catalog:
    def __init__(self, products=(), problems=(), source=None, catalog_version=None):
        self._products = {p.id: p for p in products}
        self.problems = list(problems)
        self.source = source
        self.catalog_version = catalog_version

    def products(self):
        return list(self._products.values())

    def get(self, product_id):
        return self._products.get(product_id)

    def others(self, product_id):
        """All products except `product_id` (the "more programs" list)."""
        return [p for p in self._products.values() if p.id != product_id]

    def categories(self, language="en"):
        return list(dict.fromkeys(text(p.category, language) for p in self._products.values() if p.known("category")))

    def __len__(self):
        return len(self._products)


def _tuple_of_str(value):
    return tuple(v for v in value if isinstance(v, str)) if isinstance(value, (list, tuple)) else ()


def parse(data, source=None):
    """`Catalog` from a decoded JSON object; invalid products are skipped and reported."""
    problems = []
    if not isinstance(data, dict) or data.get("format") != FORMAT:
        return Catalog(problems=[f"not a {FORMAT} document"], source=source)
    if not isinstance(data.get("version"), int) or data["version"] > VERSION:
        return Catalog(problems=[f"catalog version {data.get('version')!r} is not supported (max {VERSION})"], source=source)
    produkte = []
    for index, roh in enumerate(data.get("products") or []):
        if not isinstance(roh, dict):
            problems.append(f"product #{index}: not an object")
            continue
        pid, name = roh.get("id"), roh.get("name")
        if not (isinstance(pid, str) and _ID.match(pid)) or not (isinstance(name, str) and name.strip()):
            problems.append(f"product #{index}: id or name invalid")
            continue
        if any(p.id == pid for p in produkte):
            problems.append(f"{pid}: duplicate id")
            continue
        links = {}
        for key, url in (roh.get("links") or {}).items():
            if key in LINK_KEYS and (url == UNKNOWN or validate_url(url)):
                links[key] = url
            else:
                problems.append(f"{pid}: link {key!r} ignored")
        farbe = roh.get("brand_color")
        if farbe is not None and not (isinstance(farbe, str) and _HEX.match(farbe)):
            problems.append(f"{pid}: brand_color ignored")
            farbe = None
        status = roh.get("status", UNKNOWN)
        if status not in STATUSES:
            problems.append(f"{pid}: status {status!r} unknown")
            status = UNKNOWN
        plattformen = tuple(p for p in _tuple_of_str(roh.get("platforms")) if p in PLATFORMS or p == UNKNOWN)
        produkte.append(Product(
            id=pid, name=name.strip(), summary=roh.get("summary", ""), description=roh.get("description", ""),
            category=roh.get("category", ""), features=tuple(roh.get("features") or ()),
            brand_color=farbe, logo=roh.get("logo") if isinstance(roh.get("logo"), str) else None,
            icon=roh.get("icon") if isinstance(roh.get("icon"), str) else None, links=links,
            license=roh.get("license") if isinstance(roh.get("license"), str) else None, platforms=plattformen,
            version=roh.get("version") if isinstance(roh.get("version"), str) else None, status=status,
            languages=_tuple_of_str(roh.get("languages")),
            publisher=roh.get("publisher") if isinstance(roh.get("publisher"), str) else None))
    return Catalog(produkte, problems, source=source, catalog_version=data.get("catalog_version"))


def load(path):
    """`Catalog` from a JSON file; an unreadable file yields an empty catalog with a problem."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        return Catalog(problems=[f"{Path(path).name}: {error}"], source=str(path))
    return parse(data, source=str(path))


def load_ecosystem():
    return load(ECOSYSTEM_CATALOG)


@dataclass(frozen=True)
class AppInfo:
    """What the running host reports about itself (never stored in the catalog)."""
    product_id: str
    name: str
    version: str
    status: str = UNKNOWN
    frameworks: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)


def system_info(root=None):
    """Runtime facts for an about or diagnostics view: Python, Tk, OS, framework versions."""
    from glide_shell import SHELL_VERSION
    info = {"python": platform.python_version(), "os": platform.platform(), "glide_shell": SHELL_VERSION,
            "glide_bento": getattr(sys.modules.get("glide_bento"), "BENTO_VERSION", None), "tk": None}
    if root is not None:
        try:
            info["tk"] = str(root.tk.call("info", "patchlevel"))
        except Exception:  # noqa: BLE001 – a destroyed root only loses this line
            info["tk"] = None
    return info
