"""Dreiwegevergleich: Basis (Git-Commit der Ablage) ↔ OneDrive-Ablage ↔ Git-Zweig.

Aufruf: python -B dreiweg.py <ablage> <zweig> <basis-commit> <ausgabe.json>
Vergleicht Textdateien zeilenendenneutral, Binärdateien bytegenau.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ablage, zweig, basis, ausgabe = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], Path(sys.argv[4])


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, check=True).stdout


def liste(repo):
    raw = git(repo, "ls-files", "-z", "--cached", "--others", "--exclude-standard")
    return {p.decode("utf-8") for p in raw.split(b"\0") if p}


def norm(data):
    if data is None:
        return None
    if b"\0" not in data[:8000]:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def datei(root, rel):
    p = root / rel
    return p.read_bytes() if p.is_file() else None


basis_liste = {p.decode("utf-8") for p in git(zweig, "ls-tree", "-r", "-z", "--name-only", basis).split(b"\0") if p}
pfade = sorted(liste(ablage) | liste(zweig) | basis_liste)
ergebnis = {}
for rel in pfade:
    if rel.startswith(".claude/worktrees/"):
        continue
    b = norm(git(zweig, "show", f"{basis}:{rel}") if rel in basis_liste else None)
    o = norm(datei(ablage, rel))
    g = norm(datei(zweig, rel))
    if o == g:
        continue
    if o == b:
        art = "nur_git"
    elif g == b:
        art = "nur_ablage"
    else:
        art = "beidseitig"
    zustand = lambda h, ref: "fehlt" if h is None else ("gleich_basis" if h == ref else "geaendert")
    ergebnis[rel] = {"art": art, "ablage": zustand(o, b), "git": zustand(g, b)}

zaehlung = {}
for eintrag in ergebnis.values():
    zaehlung[eintrag["art"]] = zaehlung.get(eintrag["art"], 0) + 1
ausgabe.write_text(json.dumps({"basis": basis, "zaehlung": zaehlung, "dateien": ergebnis}, ensure_ascii=False, indent=1),
                   encoding="utf-8")
print(json.dumps(zaehlung))
