# SPDX-License-Identifier: MPL-2.0
"""Bento data contracts for visualisations, Tk-free (Bento 0.4.0).

The host computes its values; Bento only checks, scales and lays them out.
Missing values stay missing: `None` is never turned into zero, it is drawn as
a gap and counted in `Series.missing`. Invalid values (NaN, infinities,
non-numbers) are reported and treated as missing.

Public interface:

- `Point(id, label, value, category=None, time=None, color=None, meta=None)` – one
  element with a stable id (selection and hover refer to it).
- `Series(id, label, points, unit="", color=None)` with `values()`, `valid()`,
  `missing`, `problems`, `extent()`.
- `series(id, label, pairs, unit="")` – shortcut from `(label, value)` pairs;
  ids become ``"<series id>:<index>"``.
- `extent(series_list, include_zero=True, stacked=False)` → `(low, high)` or
  `None` when no valid value exists.
- `nice_ticks(low, high, count=5)` → tick values with a 1-2-2.5-5 step.
- `scale(value, low, high, length)` → pixel offset (0..length).
- `format_value(value, unit="", digits=None)` – compact, locale-neutral text.
- `Node(id, label, parent=None, value=None)`, `Edge(source, target, label="")`,
  `layer_layout(nodes, edges)` → `{id: (layer, order)}` for trees and directed
  graphs (cycles are broken deterministically and reported).
- `Span(id, label, start, end, lane=None)` for timelines; `time_extent(spans)`.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math


def _number(value):
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and math.isfinite(value):
        return float(value)
    return None


@dataclass(frozen=True)
class Point:
    id: str
    label: str
    value: object
    category: str | None = None
    time: object = None
    color: str | None = None
    meta: dict = field(default_factory=dict)

    @property
    def number(self):
        return _number(self.value)


@dataclass
class Series:
    id: str
    label: str
    points: list
    unit: str = ""
    color: str | None = None
    problems: list = field(default_factory=list)

    def __post_init__(self):
        self.points = list(self.points)
        seen = set()
        for point in self.points:
            if point.id in seen:
                self.problems.append(f"{self.id}: duplicate point id {point.id!r}")
            seen.add(point.id)
            if point.value is not None and point.number is None:
                self.problems.append(f"{self.id}/{point.id}: invalid value {point.value!r} treated as missing")

    def values(self):
        return [p.number for p in self.points]

    def valid(self):
        return [v for v in self.values() if v is not None]

    @property
    def missing(self):
        return sum(1 for v in self.values() if v is None)

    def extent(self):
        werte = self.valid()
        return (min(werte), max(werte)) if werte else None


def series(series_id, label, pairs, unit="", color=None):
    return Series(series_id, label, [Point(f"{series_id}:{i}", str(l), v) for i, (l, v) in enumerate(pairs)],
                  unit=unit, color=color)


def extent(series_list, include_zero=True, stacked=False):
    werte = []
    if stacked:
        laenge = max((len(s.points) for s in series_list), default=0)
        for i in range(laenge):
            plus = sum(v for s in series_list if i < len(s.points) for v in [s.points[i].number] if v is not None and v > 0)
            minus = sum(v for s in series_list if i < len(s.points) for v in [s.points[i].number] if v is not None and v < 0)
            werte += [plus, minus]
    else:
        for s in series_list:
            werte += s.valid()
    if not werte:
        return None
    low, high = min(werte), max(werte)
    if include_zero:
        low, high = min(low, 0.0), max(high, 0.0)
    if low == high:
        low, high = (low - 1, high + 1) if low else (0.0, 1.0)
    return low, high


def nice_ticks(low, high, count=5):
    if high < low:
        low, high = high, low
    spanne = high - low or abs(high) or 1.0
    roh = spanne / max(1, count - 1)
    basis = 10 ** math.floor(math.log10(roh))
    schritt = next(m * basis for m in (1, 2, 2.5, 5, 10) if m * basis >= roh)
    start = math.floor(low / schritt) * schritt
    ticks, wert = [], start
    while wert <= high + schritt * 1e-9:
        ticks.append(round(wert, 10))
        wert += schritt
    if ticks[-1] < high:
        ticks.append(round(ticks[-1] + schritt, 10))
    return ticks


def scale(value, low, high, length):
    if high == low:
        return 0.0
    return (value - low) / (high - low) * length


def format_value(value, unit="", digits=None):
    if value is None:
        return "–"
    v = float(value)
    if digits is None:
        digits = 0 if v == int(v) else (1 if abs(v) >= 10 else 2)
    groesse = abs(v)
    if groesse >= 1e9:
        text = f"{v / 1e9:.1f}G"
    elif groesse >= 1e6:
        text = f"{v / 1e6:.1f}M"
    elif groesse >= 1e4:
        text = f"{v / 1e3:.1f}k"
    else:
        text = f"{v:.{digits}f}"
    return f"{text} {unit}".strip() if unit else text


@dataclass(frozen=True)
class Node:
    id: str
    label: str
    parent: str | None = None
    value: object = None


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    label: str = ""


def layer_layout(nodes, edges=()):
    """{node id: (layer, order)} plus problems; parents and edge sources come first."""
    ids = [n.id for n in nodes]
    kanten = [(n.parent, n.id) for n in nodes if n.parent] + [(e.source, e.target) for e in edges]
    kanten = [(a, b) for a, b in kanten if a in ids and b in ids and a != b]
    eingang = {i: set() for i in ids}
    for a, b in kanten:
        eingang[b].add(a)
    ebene, probleme, offen = {}, [], list(ids)
    while offen:
        bereit = [i for i in offen if all(q in ebene for q in eingang[i])]
        if not bereit:  # cycle: break at the first remaining node in input order
            knoten = offen[0]
            probleme.append(f"cycle broken at {knoten!r}")
            eingang[knoten] = {q for q in eingang[knoten] if q in ebene}
            continue
        for i in bereit:
            ebene[i] = 1 + max((ebene[q] for q in eingang[i]), default=-1)
            offen.remove(i)
    reihen = {}
    ergebnis = {}
    for i in ids:
        reihe = reihen.setdefault(ebene[i], [])
        ergebnis[i] = (ebene[i], len(reihe))
        reihe.append(i)
    return ergebnis, probleme


@dataclass(frozen=True)
class Span:
    id: str
    label: str
    start: float
    end: float | None = None
    lane: str | None = None


def time_extent(spans):
    werte = [s.start for s in spans if _number(s.start) is not None]
    werte += [s.end for s in spans if _number(s.end) is not None]
    return (min(werte), max(werte)) if werte else None
