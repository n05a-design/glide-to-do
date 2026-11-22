# SPDX-License-Identifier: MPL-2.0
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

Der Wiederholen-Stapel `RedoHistory` liegt seit V1.67 in
`glide_shell.redo_history` (D96); hier bleiben die Pinnwand-Einträge.
"""

from glide_shell.redo_history import DEFAULT_LIMIT, RedoHistory  # noqa: F401 – bisherige Aufrufstellen


def board_redo_entry(scope, restored, current, label):
    """Wiederholen-Schritt für eine zurückgenommene Flächenänderung der Pinnwand.

    `restored` ist der Flächenstand nach dem Rückgängig, `current` der davor.
    Wiederholen ist nur erlaubt, solange die Fläche noch `restored` zeigt.
    """
    return {"kind": "board", "scope": scope, "restored": restored, "board": current, "label": label}


def is_board_entry(entry):
    return isinstance(entry, dict) and entry.get("kind") == "board"
