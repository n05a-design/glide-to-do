#!/usr/bin/env python3.12
"""Statische Analyse des Quelltexts – Befundliste ohne Ausführung.

Erster von zwei Wegen. Dieser hier liest den Syntaxbaum und fragt: Was ist
definiert, was wird genannt, was ist auffällig groß oder verschachtelt? Der
zweite Weg (analyse_erreichbarkeit.py) geht vom Einstiegspunkt aus und fragt,
was von dort überhaupt zu erreichen ist. Zwei Verfahren, weil jedes für sich
Fehler macht: Der Syntaxbaum kennt keine Aufrufe über getattr, die
Erreichbarkeit kennt keine Bindungen, die Tk zur Laufzeit herstellt.

Aufruf:

    python3.12 tests/tools/analyse_statisch.py [--quelle PFAD] [--grenze N]

Die Ausgabe ist bewusst knapp: Zahlen und die auffälligsten Fälle, nicht der
ganze Bestand.
"""

from __future__ import annotations

import argparse
import ast
import collections
import hashlib
import pathlib
import re
import sys

REPOSITORY_ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPOSITORY_ROOT / "src" / "glide" / "app.pyw"
# Dateien, in denen ein Name genannt sein darf, damit er als benutzt gilt.
USAGE_SEARCH = [
    REPOSITORY_ROOT / "src" / "glide" / "app.pyw",
    REPOSITORY_ROOT / "tests" / "integration" / "test_glide.py",
    REPOSITORY_ROOT / "tests" / "integration" / "test_datenintegritaet.py",
    REPOSITORY_ROOT / "tests" / "integration" / "audit_app.py",
    REPOSITORY_ROOT / "tests" / "tools" / "screenshots.py",
]


def load(path):
    text = path.read_text(encoding="utf-8")
    return text, ast.parse(text, filename=str(path))


def function_length(node):
    return (node.end_lineno or node.lineno) - node.lineno + 1


def max_depth(node, depth=0):
    """Tiefste Verschachtelung von Verzweigungen und Schleifen in einer Funktion."""
    nesting = (ast.If, ast.For, ast.While, ast.With, ast.Try)
    deepest = depth
    for child in ast.iter_child_nodes(node):
        step = depth + 1 if isinstance(child, nesting) else depth
        deepest = max(deepest, max_depth(child, step))
    return deepest


def collect_definitions(tree):
    """Alle Methoden, Funktionen und Klassenkonstanten mit ihrem Ort."""
    functions = []
    constants = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for entry in node.body:
                if isinstance(entry, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    functions.append((f"{node.name}.{entry.name}", entry.name, entry))
                elif isinstance(entry, ast.Assign):
                    for target in entry.targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constants.append((f"{node.name}.{target.id}", target.id, entry))
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append((node.name, node.name, node))
    return functions, constants


def usage_counts(names):
    """Zählt, wie oft jeder Name im Projekt genannt wird – Definition eingerechnet."""
    haystack = "\n".join(
        path.read_text(encoding="utf-8") for path in USAGE_SEARCH if path.is_file()
    )
    counts = {}
    for name in names:
        counts[name] = len(re.findall(rf"\b{re.escape(name)}\b", haystack))
    return counts


def duplicate_blocks(text, minimum_lines=6):
    """Findet wörtlich gleiche Codeblöcke ab einer Mindestlänge.

    Vergleicht normalisierte Zeilen (ohne Einrückung und Kommentare), damit
    dieselbe Logik an zwei Stellen auffällt, auch wenn sie unterschiedlich tief
    eingerückt steht.
    """
    lines = text.splitlines()
    normalised = []
    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            normalised.append(None)
        else:
            normalised.append((index + 1, stripped))

    seen = collections.defaultdict(list)
    for start in range(len(normalised) - minimum_lines):
        window = normalised[start:start + minimum_lines]
        if any(entry is None for entry in window):
            continue
        body = "\n".join(entry[1] for entry in window)
        digest = hashlib.sha1(body.encode("utf-8")).hexdigest()
        seen[digest].append(window[0][0])

    findings = []
    for digest, positions in seen.items():
        if len(positions) > 1:
            # Überlappende Treffer derselben Stelle zusammenfassen.
            spread = [positions[0]]
            for value in positions[1:]:
                if value - spread[-1] > minimum_lines:
                    spread.append(value)
            if len(spread) > 1:
                findings.append((len(spread), spread))
    findings.sort(key=lambda entry: -entry[0])
    return findings


def suspicious_patterns(text):
    """Muster, die erfahrungsgemäß auf Reste oder Nachlässigkeit hindeuten."""
    checks = {
        "bare except": r"^\s*except\s*:",
        "except Exception (breit)": r"^\s*except Exception",
        "pass als einziger Rumpf": r"^\s*pass\s*$",
        "TODO/FIXME/HACK": r"#\s*(TODO|FIXME|HACK|XXX)",
        "auskommentierter Code": r"^\s*#\s*(if|for|while|def|class|return|self\.)\b",
        "print im Quelltext": r"^\s*print\(",
        "doppelte Leerzeilen (3+)": r"\n\n\n\n",
    }
    result = {}
    for label, pattern in checks.items():
        result[label] = len(re.findall(pattern, text, flags=re.MULTILINE))
    return result


def migration_weight(text):
    """Wie viel Quelltext dient allein alten Datenformaten?

    Zählt Zeilen in Blöcken, die auf Formatversionen kleiner als die aktuelle
    prüfen. Grobe Näherung, aber sie zeigt die Größenordnung.
    """
    lines = text.splitlines()
    marker = re.compile(r"(version|format)\s*(<|<=|==)\s*\d|DATA_SCHEMA_VERSION\s*(<|<=)")
    hits = [index + 1 for index, line in enumerate(lines) if marker.search(line)]
    legacy_words = len(re.findall(r"\b(legacy|migration|migrate|altdaten|abwärts)\w*", text, re.I))
    return hits, legacy_words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quelle", default=str(DEFAULT_SOURCE))
    parser.add_argument("--grenze", type=int, default=80, help="Zeilen, ab denen eine Funktion als lang gilt")
    args = parser.parse_args()

    path = pathlib.Path(args.quelle)
    text, tree = load(path)
    lines = text.count("\n") + 1

    functions, constants = collect_definitions(tree)
    names = {short for _full, short, _node in functions} | {short for _full, short, _node in constants}
    counts = usage_counts(names)

    print(f"QUELLE  {path.relative_to(REPOSITORY_ROOT)}  ({lines} Zeilen)")
    print(f"        {len(functions)} Funktionen/Methoden, {len(constants)} Konstanten")
    print()

    # --- Nie genannte Namen -------------------------------------------------
    unused_functions = sorted(
        full for full, short, _node in functions
        if counts.get(short, 0) <= 1 and not short.startswith("__")
    )
    unused_constants = sorted(
        full for full, short, _node in constants if counts.get(short, 0) <= 1
    )
    print(f"NIE GENANNT  {len(unused_functions)} Funktionen, {len(unused_constants)} Konstanten")
    for name in unused_functions:
        print(f"   fn  {name}")
    for name in unused_constants:
        print(f"   c   {name}")
    print()

    # --- Nur einmal genannt: Kandidaten für Inlining -------------------------
    single_use = sorted(
        full for full, short, _node in functions
        if counts.get(short, 0) == 2 and not short.startswith("__")
    )
    print(f"NUR EINMAL BENUTZT  {len(single_use)} Funktionen (Definition + ein Aufruf)")
    for name in single_use[:25]:
        print(f"   fn  {name}")
    if len(single_use) > 25:
        print(f"   … und {len(single_use) - 25} weitere")
    print()

    # --- Größe und Verschachtelung ------------------------------------------
    long_functions = sorted(
        ((function_length(node), full, node.lineno) for full, _short, node in functions),
        reverse=True,
    )
    over_limit = [entry for entry in long_functions if entry[0] > args.grenze]
    print(f"LANG  {len(over_limit)} Funktionen über {args.grenze} Zeilen")
    for length, full, lineno in over_limit[:15]:
        print(f"   {length:5d} Z.  Zeile {lineno:6d}  {full}")
    if len(over_limit) > 15:
        print(f"   … und {len(over_limit) - 15} weitere")
    print()

    deep = sorted(
        ((max_depth(node), full, node.lineno) for full, _short, node in functions),
        reverse=True,
    )
    print("TIEF VERSCHACHTELT  (Ebenen aus if/for/while/with/try)")
    for depth, full, lineno in deep[:8]:
        print(f"   {depth:5d}     Zeile {lineno:6d}  {full}")
    print()

    # --- Wörtliche Dopplungen ----------------------------------------------
    duplicates = duplicate_blocks(text)
    print(f"DOPPELTE BLÖCKE  {len(duplicates)} Stellen mit mindestens 6 gleichen Zeilen")
    for count, positions in duplicates[:12]:
        print(f"   {count}× ab Zeilen {', '.join(str(p) for p in positions[:6])}")
    print()

    # --- Muster -------------------------------------------------------------
    print("MUSTER")
    for label, count in suspicious_patterns(text).items():
        print(f"   {count:5d}  {label}")
    print()

    # --- Altlasten ----------------------------------------------------------
    hits, legacy_words = migration_weight(text)
    print(f"ALTDATEN  {len(hits)} Zeilen prüfen auf Formatversionen, {legacy_words} Nennungen von Migration/Legacy")
    if hits:
        print(f"   Zeilen: {', '.join(str(h) for h in hits[:20])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
