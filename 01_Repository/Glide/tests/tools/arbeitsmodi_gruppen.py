# SPDX-License-Identifier: MPL-2.0
"""Verpflichtende serielle Prüfgruppen; Fallbestand bleibt in test_arbeitsmodi."""
import ast

GRUPPEN = ("bedienung", "planung", "navigation", "geometrie", "abschluss")
GRENZEN = ("kartenflaechen", "gestaltung", "side_verweisaktionen", "menschen3503", "neuerungen3")


def gruppen(faelle):
    faelle = tuple(faelle)
    if len(set(faelle)) != len(faelle):
        raise ValueError("Doppelte Arbeitsmodifälle")
    starts = [faelle.index(name) for name in GRENZEN]
    if starts[0] != 0 or starts != sorted(starts):
        raise ValueError("Arbeitsmodigrenzen fehlen oder stehen falsch")
    ends = starts[1:] + [len(faelle)]
    return {name: faelle[start:end] for name, start, end in zip(GRUPPEN, starts, ends)}


def fallbestand(pfad):
    """Deklaration ohne App-/Tk-Import lesen; keine zweite Fallliste pflegen."""
    tree = ast.parse(pfad.read_text(encoding="utf-8"))
    declarations = [node.value for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(target, ast.Name) and target.id == "FAELLE" for target in node.targets)]
    if len(declarations) != 1:
        raise ValueError("Kein eindeutiger Arbeitsmodibestand")
    faelle = ast.literal_eval(declarations[0])
    implemented = {node.name.removeprefix("fall_") for node in tree.body
                   if isinstance(node, ast.FunctionDef) and node.name.startswith("fall_")}
    if set(faelle) != implemented:
        raise ValueError("Arbeitsmodibestand und implementierte Fälle unterscheiden sich")
    return faelle
