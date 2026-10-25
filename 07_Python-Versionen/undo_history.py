"""Wiederholen nach Rückgängig (FP-01) ohne Tk.

Die App führt ihren Rückgängig-Stapel weiter selbst; dieses Modul hält den
Wiederholen-Stapel daneben und entscheidet, ob er noch gilt. Gut drei Dutzend
Stellen legen einen Rückgängig-Schritt an und nehmen ihn wieder zurück, wenn
eine Aktion nichts bewirkt hat oder scheitert. Statt jede davon anzufassen,
gilt eine Regel: Der Stapel bleibt gültig, solange Tiefe und oberstes Objekt
des Rückgängig-Stapels und der Schreibzähler des Bestands so sind wie nach dem
letzten Rückgängig oder Wiederholen. Eine wirkungslose Aktion, die einen
Schritt anlegt und wieder entfernt, ändert daran nichts; jede gespeicherte
Änderung und jeder neue Schritt verwirft ihn.

Die Einträge selbst sind für dieses Modul undurchsichtig: Schnappschüsse im
Format des Rückgängig-Stapels oder Flächenstände der Pinnwand.
"""

DEFAULT_LIMIT = 20


class RedoHistory:
    """Wiederholen-Schritte mit derselben Höchstzahl wie „Rückgängig“."""

    def __init__(self, limit=DEFAULT_LIMIT):
        self.limit = max(1, int(limit))
        self._entries = []
        self._writes = 0
        self._mark = None

    def __len__(self):
        return len(self._entries)

    @property
    def writes(self):
        return self._writes

    def note_write(self):
        """Ein erfolgreicher Schreibvorgang des Bestands; danach gilt kein alter Schritt."""
        self._writes += 1

    def clear(self):
        """Laden, Wächterabbruch oder eine neue Flächenänderung verwerfen den Stapel."""
        self._entries.clear()
        self._mark = None

    @staticmethod
    def _top(undo_stack):
        return undo_stack[-1] if undo_stack else None

    def _matches(self, undo_stack):
        if self._mark is None:
            return False
        depth, top, writes = self._mark
        # Identität statt Gleichheit: Ein neuer Schritt mit zufällig gleichem
        # Inhalt ist trotzdem ein neuer Schritt.
        return depth == len(undo_stack) and writes == self._writes and top is self._top(undo_stack)

    def mark(self, undo_stack):
        """Stand nach einem Rückgängig oder Wiederholen festhalten."""
        self._mark = (len(undo_stack), self._top(undo_stack), self._writes)

    def validate(self, undo_stack):
        """Ungültig gewordene Schritte verwerfen; meldet, ob noch einer bleibt."""
        if self._entries and not self._matches(undo_stack):
            self.clear()
        return bool(self._entries)

    def peek(self):
        """Der nächste Schritt, ohne ihn zu entnehmen – für Hinweise, die genau ihn meinen."""
        return self._entries[-1] if self._entries else None

    def push(self, entry, undo_stack):
        """Nach einem Rückgängig: den Stand davor als nächsten Schritt merken.

        Der Aufrufer prüft vorher mit `validate`, damit ein schon ungültiger
        Rest nicht unter den neuen Schritt gerät.
        """
        self._entries.append(entry)
        del self._entries[:-self.limit]
        self.mark(undo_stack)

    def pop(self):
        """Den nächsten Schritt entnehmen; der Aufrufer prüft vorher `validate`."""
        return self._entries.pop()

    def restore(self, entry):
        """Ein gescheitertes Wiederholen legt seinen Schritt unverändert zurück.

        Der Aufrufer hat Bestand und Rückgängig-Stapel auf den Stand davor
        zurückgesetzt; die Marke von vorher gilt deshalb weiter.
        """
        self._entries.append(entry)
        del self._entries[:-self.limit]


def board_redo_entry(scope, restored, current, label):
    """Wiederholen-Schritt für eine zurückgenommene Flächenänderung der Pinnwand.

    `restored` ist der Flächenstand nach dem Rückgängig, `current` der davor.
    Wiederholen ist nur erlaubt, solange die Fläche noch `restored` zeigt.
    """
    return {"kind": "board", "scope": scope, "restored": restored, "board": current, "label": label}


def is_board_entry(entry):
    return isinstance(entry, dict) and entry.get("kind") == "board"
