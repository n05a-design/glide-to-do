# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 26: symbol contract, providers, favourites and safe resource checks (Shell 0.11.0).

Tk-free. A symbol is described by `Symbol`; where it comes from is a
*provider* – a callable that returns symbols. The shell itself owns no product
symbols: system glyphs, Glide's pixel drawings, STEPS notation or chess pieces
are provided by their host and stay in the host's responsibility. The registry
combines providers for one picker, search and favourites without copying
resources.

`Symbol` fields: `id` (stable, ``<provider>:<local id>``), `label`, `category`,
`origin` (``system``/``host``/``user``/``import``), `kind` (``glyph``,
``pixel``, ``png``, ``svg``), `sizes`, `color` (``mono`` follows the theme text
colour, ``multicolor`` keeps its colours), `license` (SPDX id or a short
note; required for shipped collections), `resource` (opaque reference the
provider understands), `keywords`, `extra` (product-specific, untouched).

Public interface:

- `Symbol`, `SymbolRegistry(providers)` with `register_provider(name, fn)`,
  `symbols(category=None)`, `categories()`, `search(text)`, `get(id)`.
- `SymbolState(favorites, recent, limit)` – favourites and recently used ids
  as plain lists for the host's own storage (`to_dict`/`from_dict`).
- `inspect_svg(data)` and `inspect_png(data)` – checks for untrusted input:
  size limit, well-formed XML without DOCTYPE/entities, no scripts, event
  handlers, `foreignObject`, external references or `data:` URIs other than
  images; PNG signature, dimensions and size limit. Both return
  `(ok, problems, info)` and never execute or fetch anything.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
import struct
import xml.etree.ElementTree as ET

ORIGINS = ("system", "host", "user", "import")
KINDS = ("glyph", "pixel", "png", "svg")
MAX_SVG_BYTES = 512 * 1024
MAX_PNG_BYTES = 4 * 1024 * 1024
MAX_PNG_SIDE = 2048


@dataclass(frozen=True)
class Symbol:
    id: str
    label: str
    category: str
    origin: str
    kind: str
    sizes: tuple = (16,)
    color: str = "mono"
    license: str | None = None
    resource: object = None
    keywords: tuple = ()
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        if ":" not in self.id or not self.id.split(":", 1)[1]:
            raise ValueError(f"symbol id must be '<provider>:<id>', got {self.id!r}")
        if self.origin not in ORIGINS or self.kind not in KINDS:
            raise ValueError(f"{self.id}: origin or kind invalid")
        if self.color not in ("mono", "multicolor"):
            raise ValueError(f"{self.id}: color must be 'mono' or 'multicolor'")
        object.__setattr__(self, "sizes", tuple(self.sizes))
        object.__setattr__(self, "keywords", tuple(self.keywords))

    def matches(self, query):
        q = query.casefold().strip()
        return not q or any(q in str(v).casefold() for v in (self.label, self.category, self.id, *self.keywords))


class SymbolRegistry:
    """Combines providers; each provider is asked again on `refresh()`."""

    def __init__(self, providers=None):
        self._providers = dict(providers or {})
        self._symbols = {}
        self.problems = []
        self.refresh()

    def register_provider(self, name, provider):
        if not callable(provider):
            raise TypeError("provider must be callable")
        self._providers[name] = provider
        self.refresh()

    def refresh(self):
        self._symbols, self.problems = {}, []
        for name, provider in self._providers.items():
            try:
                for symbol in provider() or ():
                    if not isinstance(symbol, Symbol) or not symbol.id.startswith(name + ":"):
                        self.problems.append(f"{name}: symbol ignored ({getattr(symbol, 'id', symbol)!r})")
                        continue
                    if symbol.origin == "system" and not symbol.license:
                        self.problems.append(f"{symbol.id}: shipped symbol without licence ignored")
                        continue
                    self._symbols.setdefault(symbol.id, symbol)
            except Exception as error:  # noqa: BLE001 – a broken provider must not hide the others
                self.problems.append(f"{name}: provider failed ({error})")
        return self

    def symbols(self, category=None):
        return [s for s in self._symbols.values() if category is None or s.category == category]

    def categories(self):
        return list(dict.fromkeys(s.category for s in self._symbols.values()))

    def search(self, query, category=None):
        return [s for s in self.symbols(category) if s.matches(query)]

    def get(self, symbol_id):
        return self._symbols.get(symbol_id)

    def __len__(self):
        return len(self._symbols)


class SymbolState:
    """Favourites and recently used symbol ids; the host stores `to_dict()` itself."""

    def __init__(self, favorites=(), recent=(), limit=24):
        self.limit = int(limit)
        self.favorites = [i for i in favorites if isinstance(i, str)]
        self.recent = [i for i in recent if isinstance(i, str)][: self.limit]

    def toggle_favorite(self, symbol_id):
        if symbol_id in self.favorites:
            self.favorites.remove(symbol_id)
            return False
        self.favorites.append(symbol_id)
        return True

    def used(self, symbol_id):
        if symbol_id in self.recent:
            self.recent.remove(symbol_id)
        self.recent.insert(0, symbol_id)
        del self.recent[self.limit:]

    def to_dict(self):
        return {"favorites": list(self.favorites), "recent": list(self.recent)}

    @classmethod
    def from_dict(cls, data, limit=24):
        data = data if isinstance(data, dict) else {}
        return cls(data.get("favorites") or (), data.get("recent") or (), limit)


_EVENT_ATTR = re.compile(r"^on[a-z]+$", re.I)
_FORBIDDEN_TAGS = {"script", "foreignobject", "iframe", "object", "embed", "audio", "video", "handler"}


def _local(tag):
    return tag.rsplit("}", 1)[-1].casefold()


def inspect_svg(data):
    """(ok, problems, info) for untrusted SVG bytes; nothing is rendered or fetched."""
    problems = []
    if not isinstance(data, (bytes, bytearray)):
        return False, ["not bytes"], {}
    if len(data) > MAX_SVG_BYTES:
        return False, [f"larger than {MAX_SVG_BYTES} bytes"], {}
    kopf = bytes(data[:4096]).lower()
    if b"<!doctype" in kopf or b"<!entity" in bytes(data).lower():
        return False, ["DOCTYPE or ENTITY declarations are not allowed"], {}
    try:
        root = ET.fromstring(bytes(data))
    except ET.ParseError as error:
        return False, [f"not well-formed XML ({error})"], {}
    if _local(root.tag) != "svg":
        return False, ["root element is not <svg>"], {}
    for element in root.iter():
        name = _local(element.tag)
        if name in _FORBIDDEN_TAGS:
            problems.append(f"<{name}> is not allowed")
        for attr, value in element.attrib.items():
            attr_l = _local(attr)
            if _EVENT_ATTR.match(attr_l):
                problems.append(f"event attribute {attr_l} is not allowed")
            if attr_l == "href" or attr_l.endswith(":href"):
                v = value.strip().casefold()
                if not (v.startswith("#") or v.startswith("data:image/png") or v.startswith("data:image/jpeg")):
                    problems.append(f"external reference {value[:60]!r} is not allowed")
            if "url(" in value.casefold() and not re.search(r"url\(\s*#", value, re.I):
                problems.append(f"external url() in {attr_l} is not allowed")
        if name == "style" and element.text and ("@import" in element.text or re.search(r"url\(\s*(?!#)", element.text)):
            problems.append("external stylesheet reference is not allowed")
    info = {"width": root.attrib.get("width"), "height": root.attrib.get("height"), "viewBox": root.attrib.get("viewBox")}
    return not problems, sorted(set(problems)), info


def inspect_png(data):
    """(ok, problems, info) for untrusted PNG bytes: signature, IHDR, dimensions, size."""
    if not isinstance(data, (bytes, bytearray)):
        return False, ["not bytes"], {}
    if len(data) > MAX_PNG_BYTES:
        return False, [f"larger than {MAX_PNG_BYTES} bytes"], {}
    if bytes(data[:8]) != b"\x89PNG\r\n\x1a\n" or bytes(data[12:16]) != b"IHDR":
        return False, ["not a PNG file"], {}
    width, height = struct.unpack(">II", bytes(data[16:24]))
    if not (0 < width <= MAX_PNG_SIDE and 0 < height <= MAX_PNG_SIDE):
        return False, [f"dimensions {width}x{height} outside 1–{MAX_PNG_SIDE}"], {"width": width, "height": height}
    return True, [], {"width": width, "height": height}
