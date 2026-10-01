#!/usr/bin/env python3.12
"""Erreichbarkeits- und Ähnlichkeitsanalyse – der zweite, unabhängige Weg.

Während `analyse_statisch.py` fragt „wird dieser Name irgendwo genannt?",
fragt dieses Werkzeug „ist diese Methode vom Programmstart aus zu erreichen?"
und „gibt es zwei Methoden, die dasselbe tun?". Beide Fragen führen zu anderen
Befunden:

- Eine Methode kann genannt werden und trotzdem unerreichbar sein, wenn ihr
  einziger Aufrufer selbst tot ist.
- Zwei Methoden können völlig verschieden heißen und Zeile für Zeile dieselbe
  Arbeit tun – wörtlicher Textvergleich findet das nicht, ein Vergleich der
  Struktur schon.

Zusätzlich prüft es Attribute: `self.x`, das gesetzt, aber nie gelesen wird,
ist ein Rest; `self.x`, das gelesen, aber nirgends gesetzt wird, ist ein Fehler.

Aufruf:

    python3.12 tests/tools/analyse_erreichbarkeit.py [--quelle PFAD]
"""

from __future__ import annotations

import argparse
import ast
import collections
import pathlib
import sys

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
TEST_FILES = [
    REPOSITORY_ROOT / "tests" / "integration" / "test_glide.py",
    REPOSITORY_ROOT / "tests" / "integration" / "test_datenintegritaet.py",
    REPOSITORY_ROOT / "tests" / "integration" / "audit_app.py",
    REPOSITORY_ROOT / "tests" / "tools" / "screenshots.py",
]
# Von hier aus beginnt die Suche. Alles, was Tk zur Laufzeit bindet, wird über
# die Zeichenkettensuche unten nachgereicht.
ENTRY_POINTS = {"__init__", "main", "create_ui", "create_menubar"}


class CallCollector(ast.NodeVisitor):
    """Sammelt je Methode, welche anderen Methoden sie aufruft."""

    def __init__(self):
        self.current = None
        self.calls = collections.defaultdict(set)
        self.attribute_writes = collections.defaultdict(set)
        self.attribute_reads = collections.defaultdict(set)
        self.references = collections.defaultdict(set)

    def visit_FunctionDef(self, node):
        previous, self.current = self.current, node.name
        self.generic_visit(node)
        self.current = previous

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Call(self, node):
        target = node.func
        if isinstance(target, ast.Attribute):
            self.calls[self.current].add(target.attr)
        elif isinstance(target, ast.Name):
            self.calls[self.current].add(target.id)
        # getattr(self, "name", …) und hasattr(self, "name") sind Lesezugriffe.
        # Ohne diesen Zweig hielte die Analyse jedes so gelesene Attribut für
        # einen Rest – und davon gibt es hier viele, weil Tk-Zustände oft mit
        # getattr und Vorgabewert abgefragt werden.
        if isinstance(target, ast.Name) and target.id in ("getattr", "hasattr", "setattr"):
            if len(node.args) >= 2 and isinstance(node.args[1], ast.Constant):
                value = node.args[1].value
                if isinstance(value, str):
                    if target.id == "setattr":
                        self.attribute_writes[value].add(self.current)
                    else:
                        self.attribute_reads[value].add(self.current)
                        self.references[self.current].add(value)
        self.generic_visit(node)

    def visit_Attribute(self, node):
        # self.name als Wert gelesen oder als Ziel geschrieben.
        if isinstance(node.value, ast.Name) and node.value.id == "self":
            if isinstance(node.ctx, ast.Store):
                self.attribute_writes[node.attr].add(self.current)
            else:
                self.attribute_reads[node.attr].add(self.current)
                # Eine Methode, die ohne Klammern genannt wird, ist ein
                # Rückruf: command=self.foo, bind(..., self.foo). Ohne diese
                # Zeile hielte die Analyse jeden Ereignishandler für tot.
                self.references[self.current].add(node.attr)
        self.generic_visit(node)


def structural_signature(node):
    """Struktur einer Funktion ohne Namen und Werte.

    Zwei Funktionen mit derselben Signatur tun strukturell dasselbe – auch wenn
    Variablen, Beschriftungen und Farben abweichen.
    """
    parts = []
    for child in ast.walk(node):
        if isinstance(child, ast.FunctionDef) and child is not node:
            continue
        parts.append(type(child).__name__)
    return tuple(parts)


def collect_methods(tree):
    methods = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for entry in node.body:
                if isinstance(entry, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    methods[entry.name] = (node.name, entry)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            methods.setdefault(node.name, ("<modul>", node))
    return methods


def string_referenced(text, names):
    """Namen, die als Zeichenkette vorkommen – Tk bindet vieles so."""
    referenced = set()
    for name in names:
        if f'"{name}"' in text or f"'{name}'" in text:
            referenced.add(name)
    return referenced


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quelle", default=str(DEFAULT_SOURCE))
    args = parser.parse_args()

    path = pathlib.Path(args.quelle)
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))

    methods = collect_methods(tree)
    collector = CallCollector()
    collector.visit(tree)

    test_text = "\n".join(f.read_text(encoding="utf-8") for f in TEST_FILES if f.is_file())

    # --- Erreichbarkeit -----------------------------------------------------
    reachable = set()
    queue = [name for name in ENTRY_POINTS if name in methods]
    # Was als Zeichenkette auftaucht, kann Tk zur Laufzeit binden.
    queue += sorted(string_referenced(text, set(methods)))
    while queue:
        name = queue.pop()
        if name in reachable:
            continue
        reachable.add(name)
        for callee in collector.calls.get(name, set()) | collector.references.get(name, set()):
            if callee in methods and callee not in reachable:
                queue.append(callee)

    unreachable = sorted(
        name for name in methods
        if name not in reachable and not name.startswith("__")
    )
    only_tests = [name for name in unreachable if f".{name}(" in test_text or f"app.{name}" in test_text]
    truly_unreachable = [name for name in unreachable if name not in only_tests]

    print(f"QUELLE  {path.relative_to(REPOSITORY_ROOT)}  ({len(methods)} Methoden)")
    print(f"ERREICHBAR vom Start aus: {len(reachable & set(methods))}")
    print()
    print(f"NICHT ERREICHBAR, aber in Tests benutzt: {len(only_tests)}")
    for name in only_tests[:20]:
        print(f"   t   {name}")
    print()
    print(f"NICHT ERREICHBAR und nicht in Tests: {len(truly_unreachable)}")
    for name in truly_unreachable:
        klass, node = methods[name]
        print(f"   ?   {klass}.{name}  (Zeile {node.lineno})")
    print()

    # --- Strukturell gleiche Methoden ---------------------------------------
    signatures = collections.defaultdict(list)
    for name, (klass, node) in methods.items():
        length = (node.end_lineno or node.lineno) - node.lineno + 1
        if length < 8:
            continue
        signatures[structural_signature(node)].append((f"{klass}.{name}", node.lineno, length))

    twins = [group for group in signatures.values() if len(group) > 1]
    twins.sort(key=lambda group: -sum(entry[2] for entry in group))
    print(f"STRUKTURELL GLEICH  {len(twins)} Gruppen von Methoden mit identischem Aufbau")
    for group in twins[:12]:
        names = ", ".join(f"{full} (Z. {line}, {length} Z.)" for full, line, length in group)
        print(f"   {names}")
    print()

    # --- Attribute ----------------------------------------------------------
    # Klassenattribute (Konstanten und Vorgabewerte) werden nicht über
    # self.x = … gesetzt, sondern im Klassenrumpf. Ohne diese Ergänzung stünden
    # alle Konstanten als „gelesen, nie gesetzt“ in der Liste.
    class_level = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for entry in node.body:
                targets = []
                if isinstance(entry, ast.Assign):
                    targets = entry.targets
                elif isinstance(entry, ast.AnnAssign):
                    targets = [entry.target]
                for target in targets:
                    if isinstance(target, ast.Name):
                        class_level.add(target.id)
                if isinstance(entry, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    class_level.add(entry.name)

    written = set(collector.attribute_writes) | class_level
    read = set(collector.attribute_reads)
    write_only = sorted(name for name in written - read if not name.startswith("__"))
    read_only = sorted(name for name in read - written if not name.startswith("__"))
    print(f"ATTRIBUTE  gesetzt, nie gelesen: {len(write_only)}")
    for name in write_only[:25]:
        print(f"   w   self.{name}")
    print()
    print(f"ATTRIBUTE  gelesen, nie gesetzt: {len(read_only)}  (meist Tk-Eigenschaften, aber Fehler möglich)")
    for name in read_only[:25]:
        print(f"   r   self.{name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
