# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 15: Befehlsverlauf – Rückgängig und Wiederholen für Mementos und Befehle, ohne Tk (Phase 4).

Der Host entscheidet, was ein Schritt ist; die Shell führt den Ablauf von
Rückgängig und Wiederholen einheitlich, auch für den Fehlerfall. Zwei Arten
von Schritten lassen sich mischen:

- **Memento:** ein Zustandsabbild des Hosts. `capture()` liefert den
  aktuellen Stand, `apply(state)` stellt einen Stand her und meldet, ob das
  gelang (etwa ob Speichern klappte). Scheitert `apply`, bringt
  `rollback(state)` den Arbeitsspeicher auf den Stand davor zurück; beide
  Stapel bleiben dann unverändert.
- **Befehl:** ein Objekt mit `undo()` und `redo()` (Basisklasse `Command`
  mit `execute`). Neue Projekte arbeiten meist so.

Der Rückgängig-Stapel ist eine gewöhnliche Liste. Gehört sie dem Host, reicht
er sie über `stack` als Liste oder als Abfrage (`lambda: self.undo_stack`)
herein; die Shell liest sie bei jedem Aufruf neu. Wiederholen führt
`RedoHistory` aus `redo_history` mit derselben Gültigkeitsregel wie bisher:
Eine gespeicherte Änderung oder ein neuer Schritt verwirft es.

Die Ergebnisse `EMPTY`, `DONE`, `FAILED` und `HANDLED` sind Kennungen, keine
Texte; Meldungen an Nutzer formuliert der Host.
"""

from glide_shell.redo_history import DEFAULT_LIMIT, RedoHistory

EMPTY = "empty"
DONE = "done"
FAILED = "failed"
HANDLED = "handled"


class Command:
    """Basis für Befehlsobjekte: `execute` ändert, `undo` nimmt zurück, `redo` wiederholt."""

    label = ""

    def execute(self):
        raise NotImplementedError("Command.execute must be implemented by the host")

    def undo(self):
        raise NotImplementedError("Command.undo must be implemented by the host")

    def redo(self):
        self.execute()


def is_command(entry):
    """Ein Schritt mit eigenem `undo` und `redo`; alles andere gilt als Memento."""
    return callable(getattr(entry, "undo", None)) and callable(getattr(entry, "redo", None))


def _identity(entry):
    return entry


def _ignore(*_args):
    return None


class CommandHistory:
    """Rückgängig-Stapel und Wiederholen mit einheitlichem Erfolgs- und Fehlerweg."""

    def __init__(self, capture=None, apply=None, rollback=None, *, stack=None, redo=None,
                 limit=DEFAULT_LIMIT, can_trim=None, prepare=None, link=None):
        self.limit = max(1, int(limit))
        self._capture = capture
        self._apply = apply
        self._rollback = rollback or _ignore
        self._stack = [] if stack is None else stack
        self._redo = RedoHistory(self.limit) if redo is None else redo
        self._can_trim = can_trim
        # `prepare` macht aus einem gespeicherten Schritt den herzustellenden Stand;
        # `link` überträgt Angaben vom Schritt auf den gerade erfassten Stand.
        self._prepare = prepare or _identity
        self._link = link or _ignore

    @property
    def undo_stack(self):
        return self._stack() if callable(self._stack) else self._stack

    @property
    def redo(self):
        return self._redo() if callable(self._redo) else self._redo

    def __len__(self):
        return len(self.undo_stack)

    def can_undo(self):
        return bool(self.undo_stack)

    def can_redo(self):
        return self.redo.validate(self.undo_stack)

    def note_write(self):
        """Ein gespeicherter Schreibvorgang; danach gilt kein altes Wiederholen."""
        self.redo.note_write()

    def record(self, state=None, trim=True):
        """Den Stand vor einer Änderung als Rückgängig-Schritt ablegen."""
        if state is None:
            if self._capture is None:
                raise ValueError("record() needs a state or a capture callback")
            state = self._capture()
        self.undo_stack.append(state)
        if trim:
            self.trim()
        return state

    def execute(self, command):
        """Befehl ausführen und als Schritt merken; ein Fehler legt nichts ab."""
        command.execute()
        self.undo_stack.append(command)
        self.trim()
        return command

    def trim(self):
        """Stapel auf die Höchstzahl kürzen, außer der Host hält ihn gerade fest."""
        if self._can_trim is not None and not self._can_trim():
            return False
        stack = self.undo_stack
        while len(stack) > self.limit:
            stack.pop(0)
        return True

    def undo(self):
        """Letzten Schritt zurücknehmen; liefert EMPTY, DONE oder FAILED."""
        stack, redo = self.undo_stack, self.redo
        if not stack:
            return EMPTY
        redo.validate(stack)
        if is_command(stack[-1]):
            command = stack.pop()
            try:
                command.undo()
            except Exception:
                stack.append(command)
                raise
            redo.push(command, stack)
            return DONE
        current = self._capture()
        entry = stack.pop()
        self._link(entry, current)
        if self._apply(self._prepare(entry)):
            redo.push(current, stack)
            return DONE
        stack.append(entry)
        self._rollback(current)
        return FAILED

    def redo_step(self, handle=None):
        """Letztes Rückgängig wiederholen; `handle(entry)` darf Sonderschritte selbst übernehmen.

        Liefert EMPTY, DONE, FAILED oder HANDLED.
        """
        stack, redo = self.undo_stack, self.redo
        if not redo.validate(stack):
            return EMPTY
        entry = redo.pop()
        if handle is not None and handle(entry):
            return HANDLED
        if is_command(entry):
            try:
                entry.redo()
            except Exception:
                redo.restore(entry)
                raise
            stack.append(entry)
            self.trim()
            redo.mark(stack)
            return DONE
        before = self._capture()
        self._link(entry, before)
        stack.append(before)
        if self._apply(self._prepare(entry)):
            self.trim()
            redo.mark(stack)
            return DONE
        stack.pop()
        self._rollback(before)
        redo.restore(entry)
        return FAILED

    def clear(self):
        """Laden eines anderen Bestands: beide Stapel leeren."""
        del self.undo_stack[:]
        self.redo.clear()
