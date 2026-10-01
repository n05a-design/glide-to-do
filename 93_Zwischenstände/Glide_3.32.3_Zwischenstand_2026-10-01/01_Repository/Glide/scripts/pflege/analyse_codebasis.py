"""Statische Durchsicht von app.pyw: Größen, wiederholte Texte, identische Funktionen, häufige Aufrufe.

Aufruf: python3 scripts/pflege/analyse_codebasis.py
"""
import ast, collections, hashlib, re, sys
from pathlib import Path
quelle = (Path(__file__).resolve().parents[2] / "src/glide/app.pyw").read_text(encoding="utf-8")
baum = ast.parse(quelle)
zeilen = quelle.count("\n")
funktionen = [n for n in ast.walk(baum) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
klassen = [n for n in ast.walk(baum) if isinstance(n, ast.ClassDef)]
print(f"Zeilen {zeilen}, Klassen {len(klassen)}, Funktionen {len(funktionen)}")
groesste = sorted(klassen, key=lambda k: -(k.end_lineno - k.lineno))[:6]
print("Größte Klassen:", [(k.name, k.end_lineno - k.lineno) for k in groesste])
lang = sorted(funktionen, key=lambda f: -(f.end_lineno - f.lineno))[:12]
print("Längste Funktionen:", [(f.name, f.end_lineno - f.lineno) for f in lang])

# 1) Wiederholte Texte (ohne Docstrings, mindestens 8 Zeichen)
docs = set()
for n in ast.walk(baum):
    if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) and n.body and isinstance(n.body[0], ast.Expr) \
            and isinstance(getattr(n.body[0], "value", None), ast.Constant):
        docs.add(id(n.body[0].value))
texte = collections.Counter(n.value for n in ast.walk(baum) if isinstance(n, ast.Constant) and isinstance(n.value, str)
                            and id(n) not in docs and len(n.value) >= 8)
print("\nHäufigste Texte (>=8 Zeichen):")
for text, anzahl in texte.most_common(25):
    print(f"  {anzahl:4d} × {text[:70]!r}")

# 2) Gleiche Funktionskörper (normalisiert: Namen der Funktion egal)
def form(f):
    kopie = ast.parse(ast.unparse(f)).body[0]
    kopie.name = "_"
    if kopie.body and isinstance(kopie.body[0], ast.Expr) and isinstance(getattr(kopie.body[0], "value", None), ast.Constant):
        kopie.body = kopie.body[1:] or [ast.Pass()]
    return hashlib.sha1(ast.dump(kopie).encode()).hexdigest()
gruppen = collections.defaultdict(list)
for f in funktionen:
    if f.end_lineno - f.lineno >= 4:
        gruppen[form(f)].append((f.name, f.lineno, f.end_lineno - f.lineno))
doppelt = [g for g in gruppen.values() if len(g) > 1]
print(f"\nIdentische Funktionen (>=4 Zeilen): {len(doppelt)} Gruppen")
for g in sorted(doppelt, key=lambda g: -g[0][2])[:15]:
    print("  ", g)

# 3) Wiederkehrende Aufrufmuster
muster = collections.Counter()
for n in ast.walk(baum):
    if isinstance(n, ast.Call):
        try:
            text = ast.unparse(n)
        except Exception:
            continue
        if len(text) < 120:
            muster[text] += 1
print("\nHäufigste identische Aufrufe:")
for text, anzahl in muster.most_common(25):
    if anzahl >= 8:
        print(f"  {anzahl:4d} × {text[:100]}")
theme = collections.Counter(m.group(0) for m in re.finditer(r'(self\.|app\.)?theme\[["\'](\w+)["\']\]', quelle))
print("\ntheme[...]-Zugriffe gesamt:", sum(theme.values()))
fonts = collections.Counter(m.group(0) for m in re.finditer(r'app_font\([^)]*\)', quelle))
print("verschiedene app_font-Aufrufe:", len(fonts), "gesamt", sum(fonts.values()), "häufigste", fonts.most_common(6))
