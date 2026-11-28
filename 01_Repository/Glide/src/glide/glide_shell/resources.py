# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 27: bounded caches with explicit keys, budgets and diagnostics (Shell 0.11.0).

Tk-free. Every cache has an owner and a purpose, a key built from all
parameters that change the result (resource identity, content version,
theme, scale, size), an entry and a cost budget, LRU eviction, invalidation
by predicate and hit/miss statistics. Caches hold *derived* data only
(rendered images, converted pixels, layout measurements) – never primary user
data. There is no global unbounded cache; a host creates one per purpose and
drops it with its view (`clear`).

Public interface:

- `BoundedCache(name, max_entries, max_cost=None, cost=None, on_evict=None)`:
  `get(key, default=None)`, `put(key, value)`, `get_or_create(key, factory)`,
  `invalidate(predicate)`, `clear()`, `stats()` (hits, misses, evictions,
  entries, cost, hit_rate), `__len__`, `__contains__`.
- `cache_key(*parts, **named)` – stable tuple key from hashable parts.

Thread safety: the cache is meant for the Tk thread. `background.TaskQueue`
delivers results on that thread, so no lock is needed; a cache shared across
threads must be wrapped by the caller.
"""
from __future__ import annotations

from collections import OrderedDict


def cache_key(*parts, **named):
    return tuple(parts) + tuple(sorted(named.items()))


class BoundedCache:
    def __init__(self, name, max_entries, max_cost=None, cost=None, on_evict=None):
        if int(max_entries) < 1:
            raise ValueError("max_entries must be at least 1")
        self.name = name
        self.max_entries = int(max_entries)
        self.max_cost = max_cost
        self.cost = cost or (lambda _value: 1)
        self.on_evict = on_evict
        self._items = OrderedDict()
        self._costs = {}
        self._total = 0
        self.hits = self.misses = self.evictions = 0

    def get(self, key, default=None):
        if key in self._items:
            self._items.move_to_end(key)
            self.hits += 1
            return self._items[key]
        self.misses += 1
        return default

    def put(self, key, value):
        if key in self._items:
            self._drop(key, evicted=False)
        kosten = max(0, int(self.cost(value)))
        if self.max_cost is not None and kosten > self.max_cost:
            return value  # larger than the whole budget: deliver, but do not keep
        self._items[key] = value
        self._costs[key] = kosten
        self._total += kosten
        while len(self._items) > self.max_entries or (self.max_cost is not None and self._total > self.max_cost):
            self._drop(next(iter(self._items)), evicted=True)
        return value

    def get_or_create(self, key, factory):
        sentinel = object()
        value = self.get(key, sentinel)
        if value is sentinel:
            value = factory()
            if value is not None:
                self.put(key, value)
        return value

    def invalidate(self, predicate):
        """Remove every entry whose key satisfies `predicate`; returns the number removed."""
        weg = [k for k in self._items if predicate(k)]
        for key in weg:
            self._drop(key, evicted=False)
        return len(weg)

    def clear(self):
        for key in list(self._items):
            self._drop(key, evicted=False)

    def _drop(self, key, evicted):
        value = self._items.pop(key)
        self._total -= self._costs.pop(key, 0)
        if evicted:
            self.evictions += 1
        if self.on_evict is not None:
            self.on_evict(key, value)

    def stats(self):
        gesamt = self.hits + self.misses
        return {"name": self.name, "entries": len(self._items), "cost": self._total, "max_entries": self.max_entries,
                "max_cost": self.max_cost, "hits": self.hits, "misses": self.misses, "evictions": self.evictions,
                "hit_rate": round(self.hits / gesamt, 3) if gesamt else None}

    def __len__(self):
        return len(self._items)

    def __contains__(self, key):
        return key in self._items
