"""Quellvertrag und Plattformauswahl für eigenständige Entwicklungspakete, ohne Tk."""
import ast
import hashlib
from pathlib import Path, PurePosixPath
import re

TARGETS = {"macos-arm64": ("darwin", "arm64", "osx-arm64-tcl9"),
           "windows-x64": ("win32", "x86_64", "win-x64-tcl9")}
CONSTANTS = frozenset(("APP_NAME", "APP_VERSION", "APP_BUNDLE_ID", "APP_USER_MODEL_ID"))


def identity(source, version):
    values = {}
    for node in ast.parse(source).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id in CONSTANTS:
                if target.id in values:
                    raise ValueError("Mehrdeutige Produktkennung: " + target.id)
                value = ast.literal_eval(node.value)
                if not isinstance(value, str) or not value:
                    raise ValueError("Ungültige Produktkennung: " + target.id)
                values[target.id] = value
    if set(values) != CONSTANTS:
        raise ValueError("Unvollständige Produktkennungen")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version) or values["APP_VERSION"] != version:
        raise ValueError("Quellversion und VERSION unterscheiden sich")
    return values


def included(relative, target):
    if target not in TARGETS:
        raise ValueError("Unbeauftragte Paketplattform")
    p = PurePosixPath(relative)
    if p.as_posix() != relative or p.is_absolute() or not p.parts or any(part in (".", "..") for part in p.parts) or "\\" in relative:
        raise ValueError("Ungültiger Quellpfad")
    if any(part in ("archiv", "__pycache__", ".git", ".DS_Store") for part in p.parts):
        return False
    if len(p.parts) == 1:
        return (p.name == "app.pyw" or p.suffix == ".py") and p.name != "drawing_prototype.py"
    if p.parts[0] == "resources":
        return True
    if p.parts[0] != "vendor":
        return False
    if p.parts[:3] == ("vendor", "tkinterdnd2", "tkdnd"):
        return len(p.parts) > 3 and p.parts[3] == TARGETS[target][2]
    return True


def manifest(source, target):
    source = Path(source)
    files = {}
    for path in sorted(source.rglob("*")):
        relative = path.relative_to(source).as_posix()
        if not included(relative, target):
            continue
        if path.is_symlink():
            raise ValueError("Quell-Symlink ist kein nachvollziehbarer Paketbestand: " + relative)
        if path.is_file():
            files[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    needed = ("app.pyw", "vendor/tkinterdnd2/__init__.py", "vendor/tkinterdnd2/TkinterDnD.py",
              "vendor/tkinterdnd2/LICENSE", "vendor/provenance.json",
              "vendor/tkinterdnd2/tkdnd/" + TARGETS[target][2] + "/pkgIndex.tcl")
    if not all(path in files for path in needed):
        raise ValueError("Unvollständiger Quell-/DND-Bestand für " + target)
    if not any(p.startswith("resources/fonts/") for p in files):
        raise ValueError("Schriftressourcen fehlen")
    if not any(p.startswith("resources/logo/") for p in files):
        raise ValueError("Logoressourcen fehlen")
    return files


def in_onedrive(path):
    """Liegt der Pfad in einem OneDrive-Synchronordner (macOS CloudStorage oder Windows-Benutzerordner)?

    Ein Ordnername, der „OneDrive“ nur als Teil enthält, zählt nicht; maßgeblich
    sind die Synchronordner `OneDrive`, `OneDrive-<Konto>` und `OneDrive - <Firma>`.
    """
    for part in Path(path).parts:
        name = part.casefold()
        if name == "onedrive" or name.startswith(("onedrive-", "onedrive - ")):
            return True
    return False
