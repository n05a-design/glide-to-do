# SPDX-License-Identifier: MPL-2.0
"""Shell-Paket 19: framework conformance check for a host project (Shell 0.7.0).

Tk-free, reads sources only as syntax trees. A host (Glide, a follow-up
project) runs it in its tests or CI:

    from glide_shell import conformance
    findings = conformance.check_project(source_root)

`source_root` is the folder that contains `glide_shell/` (and `glide_bento/`
when used) next to the host's own modules. Rules:

1. `glide_shell` imports only the standard library, `tkinter` and itself.
2. `glide_bento` imports only the standard library, `tkinter`, itself and the
   public shell modules listed in `glide_shell.__all__`.
3. Host modules import shell modules only by their public names (no
   `glide_shell._private`, no module missing from `__all__`).
4. No import cycle between framework modules.
5. The Bento copy's `SHELL_MIN_VERSION` is compatible with the shell copy
   (`compat.compatible` with `SHELL_COMPAT_SINCE`).
6. Since 0.10.0 (rule `host-api`): names a host imports from a shell module
   (`from glide_shell.app_host import AppHost`) exist in that module and are
   public (no leading underscore). This catches hosts written against another
   shell version before they fail at import time, for example after an update
   of a copied shell.

Findings are `Finding(rule, path, line, message)` tuples with English messages
(D96). An empty list means conform. Native Tk widgets inside host modules are
not findings: whether a widget is general framework work or product-specific
is a review question, not a syntax rule.
"""
from __future__ import annotations

import ast
import sys
from collections import namedtuple
from pathlib import Path

Finding = namedtuple("Finding", "rule path line message")

SHELL = "glide_shell"
BENTO = "glide_bento"
_STD = set(sys.stdlib_module_names) | {"tkinter", "__future__"}


def _tree(path):
    return ast.parse(Path(path).read_text(encoding="utf-8"), filename=str(path))


def imports(path):
    """(line, absolute module name) for each import; relative imports keep their dots."""
    result = []
    for node in ast.walk(_tree(path)):
        if isinstance(node, ast.Import):
            result.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            base = "." * node.level + (node.module or "")
            if node.level == 0 and node.module in (SHELL, BENTO):
                result.extend((node.lineno, f"{node.module}.{alias.name}") for alias in node.names)
            else:
                result.append((node.lineno, base))
    return result


def _constant(path, name):
    for node in _tree(path).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            if any(isinstance(t, ast.Name) and t.id == name for t in node.targets):
                return node.value.value
    return None


def public_shell_modules(shell_dir):
    for node in _tree(Path(shell_dir) / "__init__.py").body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__all__" for t in node.targets):
            return {e.value for e in node.value.elts if isinstance(e, ast.Constant)}
    return set()


def module_names(path):
    """Public top-level names (functions, classes, assignments) of a module file."""
    names = set()
    for node in _tree(path).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            names.add(node.target.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            names.update((a.asname or a.name).split(".")[0] for a in node.names)
    return {n for n in names if not n.startswith("_")}


def host_api_findings(shell_dir, path):
    """Rule `host-api` for one host file (see module docstring)."""
    findings, cache = [], {}
    for node in ast.walk(_tree(path)):
        if not (isinstance(node, ast.ImportFrom) and node.level == 0 and node.module
                and node.module.startswith(SHELL + ".") and node.module.count(".") == 1):
            continue
        modul = node.module.split(".")[1]
        datei = Path(shell_dir) / f"{modul}.py"
        if not datei.is_file():
            if not modul.startswith("_"):  # private modules are reported by rule `public-api`
                findings.append(Finding("host-api", str(path), node.lineno,
                                        f"{node.module} does not exist in this shell copy"))
            continue
        if modul not in cache:
            cache[modul] = module_names(datei)
        for alias in node.names:
            if alias.name != "*" and alias.name not in cache[modul]:
                findings.append(Finding("host-api", str(path), node.lineno,
                                        f"{node.module}.{alias.name} is not a public name of this shell copy"))
    return findings


def _resolve(package, name):
    if name.startswith("."):
        return f"{package}.{name.lstrip('.')}" if name.strip(".") else package
    return name


def _check_package(root, package, allowed, findings, rule):
    edges = {}
    for path in sorted((root / package).glob("*.py")):
        module = f"{package}.{path.stem}" if path.stem != "__init__" else package
        for line, name in imports(path):
            full = _resolve(package, name)
            top = full.split(".")[0]
            if full.startswith(package):
                edges.setdefault(module, set()).add(full)
                continue
            if top in _STD:
                continue
            if not allowed(full):
                findings.append(Finding(rule, str(path), line, f"{package} must not import {full}"))
    return edges


def _cycles(edges):
    found, state = [], {}

    def visit(node, stack):
        state[node] = 1
        for target in sorted(edges.get(node, ())):
            if state.get(target) == 1:
                found.append(stack[stack.index(target):] + [target] if target in stack else [node, target])
            elif state.get(target) is None:
                visit(target, stack + [target])
        state[node] = 2

    for start in sorted(edges):
        if state.get(start) is None:
            visit(start, [start])
    return found


def check_project(source_root, host_modules=None):
    """All findings for the project under `source_root` (see module docstring)."""
    from glide_shell.compat import compatible

    root = Path(source_root)
    findings = []
    shell_dir = root / SHELL
    if not (shell_dir / "__init__.py").is_file():
        return [Finding("layout", str(shell_dir), 0, "glide_shell package not found")]
    public = public_shell_modules(shell_dir)

    def shell_allowed(full):
        return False

    def bento_allowed(full):
        parts = full.split(".")
        return parts[0] == SHELL and (len(parts) == 1 or parts[1] in public)

    edges = _check_package(root, SHELL, shell_allowed, findings, "shell-imports")
    if (root / BENTO / "__init__.py").is_file():
        edges.update(_check_package(root, BENTO, bento_allowed, findings, "bento-imports"))
        minimum = _constant(root / BENTO / "__init__.py", "SHELL_MIN_VERSION")
        installed = _constant(shell_dir / "__init__.py", "SHELL_VERSION")
        since = _constant(shell_dir / "__init__.py", "SHELL_COMPAT_SINCE") or installed
        if minimum is None:
            findings.append(Finding("versions", str(root / BENTO / "__init__.py"), 0,
                                    "glide_bento declares no SHELL_MIN_VERSION"))
        elif not compatible(installed, minimum, since):
            findings.append(Finding("versions", str(root / BENTO / "__init__.py"), 0,
                                    f"glide_bento needs shell {minimum}, copy is {installed} (compatible since {since})"))
    for cycle in _cycles(edges):
        findings.append(Finding("cycles", " -> ".join(cycle), 0, "import cycle between framework modules"))
    host = host_modules if host_modules is not None else sorted(
        p for p in list(root.glob("*.py")) + list(root.glob("*.pyw")))
    for path in host:
        for line, name in imports(path):
            parts = name.split(".")
            if parts[0] == SHELL and len(parts) > 1 and (parts[1].startswith("_") or parts[1] not in public):
                findings.append(Finding("public-api", str(path), line, f"{name} is not a public shell module"))
        findings.extend(host_api_findings(shell_dir, path))
    return findings


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    findings = check_project(args[0] if args else ".")
    for finding in findings:
        print(f"[{finding.rule}] {finding.path}:{finding.line}: {finding.message}")
    print("conform" if not findings else f"{len(findings)} finding(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
