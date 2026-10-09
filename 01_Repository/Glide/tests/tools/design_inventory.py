"""OB01: statische Abstandsbestandsaufnahme der Hauptansichten (keine Tk-Imports).

Zählt Abstandsausdrücke und unterschiedliche auflösbare Werte. Direkte
Zahlen und gemeinsame Konstanten werden getrennt ausgewiesen; nicht auflösbare
dynamische Ausdrücke bleiben ausdrücklich im Ergebnis.
"""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[2]
SPACING_KEYS = {"padx", "pady", "ipadx", "ipady", "inner_pad_x", "inner_pad_y", "padding", "gap"}
VIEWS = {
    "Hauptfenster": ("create_ui",),
    "Kopf": ("update_page_chips", "fit_page_chips", "update_path_row", "update_page_labels"),
    "Startseite": ("_refresh_home", "create_home_panel", "render_home_tile"),
    "Heute": ("refresh_task_overview", "sync_plan_day_grid"),
    "Bibliothek": ("refresh_library_page", "create_library_panel"),
    # OB01r (3.33.21): Dialoge
    "Einstellungen": ("show_settings_dialog",),
    "Schnellerfassung": ("show_quick_capture",),
}


def inventory(path):
    tree = ast.parse(path.read_text(encoding="utf-8-sig"))
    cls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ListApp")
    constants = {t.id: n.value for n in cls.body if isinstance(n, ast.Assign)
                 for t in n.targets if isinstance(t, ast.Name)}
    sys.path.insert(0, str(REPO / "src/glide"))
    try:
        import ui_design
    except ImportError:
        ui_design = None

    def resolve(node):
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return [node.value]
        if isinstance(node, (ast.Tuple, ast.List)):
            return [v for part in node.elts for v in resolve(part)]
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "self" and node.attr in constants:
            return resolve(constants[node.attr])
        if (ui_design and isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute)
                and isinstance(node.value.value, ast.Name) and node.value.value.id == "glide_design"):
            return [getattr(ui_design, node.value.attr)[ast.literal_eval(node.slice)]]
        raise ValueError("dynamisch")

    result = {}
    for view, names in VIEWS.items():
        expressions, values, literals, shared, unknown = 0, [], 0, 0, []
        found = []
        for method in cls.body:
            if not isinstance(method, ast.FunctionDef) or method.name not in names:
                continue
            found.append(method.name)
            for call in (n for n in ast.walk(method) if isinstance(n, ast.Call)):
                for kw in call.keywords:
                    if kw.arg not in SPACING_KEYS:
                        continue
                    expressions += 1
                    def literal(node):
                        if (isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute)
                                and isinstance(node.value.value, ast.Name) and node.value.value.id == "glide_design"):
                            return False
                        return (isinstance(node, ast.Constant) and isinstance(node.value, (int, float))) or any(literal(n) for n in ast.iter_child_nodes(node))
                    if literal(kw.value):
                        literals += 1
                    if any(isinstance(n, ast.Attribute) for n in ast.walk(kw.value)):
                        shared += 1
                    try:
                        values.extend(resolve(kw.value))
                    except (ValueError, KeyError, AttributeError):
                        unknown.append(dict(method=method.name, expression=ast.unparse(kw.value)))
        result[view] = dict(methods=found, spacing_expressions=expressions, with_numeric_literals=literals,
                            with_shared_values=shared, distinct_values=sorted(set(values)),
                            distinct_value_count=len(set(values)), unresolved=unknown)
    return dict(source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), views=result)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--app", type=Path, default=REPO / "src/glide/app.pyw")
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(inventory(args.app), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("Abstandsbestandsaufnahme gespeichert")
