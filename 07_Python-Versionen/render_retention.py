"""Lebensdauer und Abgleich wiederverwendbarer Ansichtsbausteine, ohne Tk.

Fabriken und Widgets werden vom Aufrufer übergeben. Daten werden nach Inhalt
verglichen; gleiche IDs dürfen nach Undo andere Python-Objekte bezeichnen.
"""
from collections import defaultdict
from contextlib import contextmanager
import inspect


def snapshot(value, seen=None):
    """Unveränderlicher Vergleichsstand, auch für gebundene UI-Aktionen."""
    if value is None or isinstance(value, (str, bytes, int, float, bool)):
        return value
    seen = set() if seen is None else seen
    if id(value) in seen:
        return ("reference", id(value))
    seen = seen | {id(value)}
    if isinstance(value, dict):
        return tuple(sorted(((snapshot(k, seen), snapshot(v, seen)) for k, v in value.items()), key=lambda pair: repr(pair[0])))
    if isinstance(value, (tuple, list)):
        return tuple(snapshot(v, seen) for v in value)
    if inspect.ismethod(value):
        return (value.__func__, id(value.__self__))
    if inspect.isfunction(value):
        closure = tuple(snapshot(cell.cell_contents, seen) for cell in value.__closure__ or ())
        return (value.__code__, snapshot(value.__defaults__, seen),
                snapshot(value.__kwdefaults__, seen), closure)
    return (type(value), id(value))


class RetainedWidgets:
    """Bausteine je Host und logischem Bereich, keine globalen Widget-Caches."""

    def __init__(self, configurable=()):
        self.configurable = configurable
        self.records = {}
        self.scopes = {}
        self.begin()

    def begin(self):
        self.positions = defaultdict(int)
        self.used = set()
        self.next_scopes = defaultdict(set)
        self.scope_key = None
        self.pack_order = {}

    @contextmanager
    def scope(self, key):
        old = self.scope_key
        self.scope_key = key
        try:
            yield
        finally:
            self.scope_key = old

    def keep_scope(self, key):
        keys = self.scopes.get(key, set())
        self.used.update(keys)
        self.next_scopes[key].update(keys)

    def make(self, factory, parent, *args, retention_key=None, **options):
        parent_key = (self.scope_key, id(parent))
        if retention_key is None:
            position = self.positions[parent_key]
            self.positions[parent_key] += 1
            key = (*parent_key, position)
        else:
            key = (*parent_key, "key", retention_key)
        signature = (snapshot(factory), snapshot(args), snapshot(options))
        old = self.records.get(key)
        if old and old[1].winfo_exists():
            previous, widget, previous_options = old
            if previous == signature:
                self.used.add(key)
                self.next_scopes[self.scope_key].add(key)
                return widget
            if factory in self.configurable and previous[:2] == signature[:2] and options.keys() == previous_options.keys():
                changed = {name: value for name, value in options.items()
                           if snapshot(value) != previous_options[name]}
                widget.configure(**changed)
            else:
                widget.destroy()
                widget = factory(parent, *args, **options)
        else:
            widget = factory(parent, *args, **options)
        self.records[key] = (signature, widget, {name: snapshot(value) for name, value in options.items()})
        self.used.add(key)
        self.next_scopes[self.scope_key].add(key)
        return widget

    def bind(self, widget, sequence, callback, add=None):
        callbacks = getattr(widget, "_retained_bindings", None)
        if callbacks is None:
            callbacks = widget._retained_bindings = {}
        key = (sequence, add)
        if key not in callbacks:
            widget.bind(sequence, lambda event, k=key: callbacks[k](event), add=add)
        callbacks[key] = callback

    def pack(self, widget, *args, **options):
        # Neue optionale Kinder müssen an ihrer Stelle erscheinen, auch wenn
        # nachfolgende Geschwister aus dem vorigen Aufbau erhalten bleiben.
        host = options.get("in_", widget.master)
        previous = self.pack_order.get(id(host))
        siblings = host.pack_slaves()
        placement = {}
        if previous is not None and previous is not widget and previous in siblings:
            index = siblings.index(previous) + 1
            if index >= len(siblings) or siblings[index] is not widget:
                placement["after"] = previous
        elif previous is None and siblings and siblings[0] is not widget:
            placement["before"] = siblings[0]
        self.pack_order[id(host)] = widget
        return self._geometry(widget, "pack", args, options, placement)

    def grid(self, widget, *args, **options):
        return self._geometry(widget, "grid", args, options)

    @staticmethod
    def _geometry(widget, manager, args, options, placement=None):
        signature = (manager, snapshot(args), snapshot(options))
        if placement or getattr(widget, "_retained_geometry", None) != signature or widget.winfo_manager() != manager:
            getattr(widget, manager)(*args, **options, **(placement or {}))
            widget._retained_geometry = signature

    def end(self):
        for key in self.records.keys() - self.used:
            _signature, widget, _options = self.records.pop(key)
            if widget.winfo_exists():
                widget.destroy()
        self.scopes = dict(self.next_scopes)

    def clear(self):
        self.used.clear()
        self.next_scopes.clear()
        self.end()
