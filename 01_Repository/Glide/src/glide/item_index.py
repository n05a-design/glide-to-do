"""Kurzlebige ID-Auflösung für eine zusammenhängende Aktion, ohne Tk.

Der Index hält Originalreferenzen. Nach Ereignis-/Dialoggrenzen, Undo oder
Strukturänderungen wird eine neue Projektion erzeugt; kein langlebiger Cache.
Bei mehrfachen IDs gilt wie bei rekursiver Suche der erste Tiefensuchtreffer.
"""


class ItemIndex:
    def __init__(self, items=(), *, lists=None):
        self._items = {}
        self._lists = {}
        entries = ((None, items),) if lists is None else (
            (entry, entry.get('items', ())) for entry in lists)
        for entry, roots in entries:
            stack = [(roots, None, iter(enumerate(roots)))]
            while stack:
                siblings, parent, iterator = stack[-1]
                try:
                    position, item = next(iterator)
                except StopIteration:
                    stack.pop()
                    continue
                identity = item.get('id')
                if identity and identity not in self._items:
                    self._items[identity] = (item, siblings, position, parent)
                    self._lists[identity] = entry
                children = item.get('children') or ()
                if children:
                    stack.append((children, item, iter(enumerate(children))))

    def get(self, identity):
        return self._items.get(identity)

    def in_list(self, identity):
        found = self.get(identity)
        return (*found[:3], self._lists[identity]) if found else None

    def selected(self, identities):
        return {identity: self._items[identity] for identity in dict.fromkeys(identities)
                if identity in self._items}
