"""Lesender Quell-/Lieferabgleich für den datierten Abschlussaudit.

Aus dem Projektstamm: python3 -B tests/qa-3.50.0/abschlussabgleich_2026-11-02/pruefabgleich.py
Keine Appimports und kein Zugriff auf Nutzerdaten. Ergebnis auf stdout.
"""

import hashlib
import json
from pathlib import Path
import plistlib
import subprocess
import sys


REPO = Path(__file__).resolve().parents[3]
ROOT = REPO.parents[1]
BELEG = REPO / "tests/qa-3.50.0/oeffentliche_beta_2026-11-02"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def text_equal(first, second):
    try:
        return first.decode("utf-8").replace("\r\n", "\n") == second.decode("utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError:
        return False


def matrix_inputs():
    manifest = json.loads((BELEG / "matrix_eingaben.json").read_text())
    names = sorted(set(manifest["sha256"]) | set(manifest["local_crlf_only"]))
    refs = [f"{manifest['source_commit']}:{name}" for name in names]
    contents = subprocess.check_output(
        ["git", "cat-file", "--batch"], cwd=ROOT, input=("\n".join(refs) + "\n").encode()
    )
    offset = 0
    raw_equal = 0
    eol_only = []
    mismatches = []
    for name in names:
        header_end = contents.index(b"\n", offset)
        size = int(contents[offset:header_end].split()[2])
        expected = contents[header_end + 1:header_end + 1 + size]
        offset = header_end + size + 2
        path = ROOT / name
        if not path.is_file():
            mismatches.append({"path": name, "reason": "missing"})
        elif path.read_bytes() == expected:
            raw_equal += 1
        elif text_equal(path.read_bytes(), expected):
            eol_only.append(name)
        else:
            mismatches.append({"path": name, "reason": "content_changed"})
    return {"source_commit": manifest["source_commit"], "checked": len(names),
            "raw_equal": raw_equal, "line_endings_only": eol_only, "mismatches": mismatches}


def package_files(platform, target, archive):
    build = json.loads((BELEG / f"{platform}_bau.json").read_text())
    delivery = json.loads((BELEG / f"{platform}_lieferabgleich.json").read_text())
    base = REPO / "build" / target
    mismatches = [name for name, digest in build["package_sha256"].items()
                  if not (base / name).is_file() or sha(base / name) != digest]
    archive_sha = sha(REPO / "build" / archive)
    result = {"files_checked": len(build["package_sha256"]), "mismatches": mismatches,
              "archive_sha256": archive_sha,
              "archive_equal_delivery": archive_sha == delivery.get("archive_sha256", delivery.get("zip_sha256"))}
    if platform == "mac":
        result["version"] = plistlib.loads((base / "Contents/Info.plist").read_bytes())["CFBundleShortVersionString"]
        if sys.platform == "darwin":
            verify = subprocess.run(["codesign", "--verify", "--deep", "--strict", str(base.resolve())],
                                    capture_output=True, text=True)
            result["codesign_exitcode"] = verify.returncode
    return result


def python_delivery():
    source = REPO / "src/glide"
    target = ROOT / "07_Python-Versionen"
    names = [p for p in source.iterdir() if p.suffix in (".py", ".pyw")
             and p.name != "drawing_prototype.pyw"]
    for folder in ("resources", "vendor"):
        names.extend(p for p in (source / folder).rglob("*") if p.is_file()
                     and "__pycache__" not in p.parts and "archiv" not in p.parts)
    mismatches = []
    for path in names:
        relative = path.relative_to(source)
        renamed = {"app.pyw": "Glide-Aufgaben-und-Listen_v3.50.0.pyw", "glide_start.py": "Schnellstart.pyw"}
        destination = target / renamed.get(relative.as_posix(), relative)
        if not destination.is_file() or sha(path) != sha(destination):
            mismatches.append(relative.as_posix())
    return {"checked": len(names), "mismatches": mismatches}


def main():
    result = {"source_commit": git("rev-parse", "HEAD").decode().strip(),
              "app_sha256": sha(REPO / "src/glide/app.pyw"),
              "historical_matrix": matrix_inputs(), "python_delivery": python_delivery(),
              "packages": {
                  "mac": package_files("mac", "macos/Glide.app", "macos/Glide-3.50.0-macos-arm64.tar.gz"),
                  "win": package_files("win", "windows/Glide-3.50.0", "windows/Glide-3.50.0-windows-x64.zip")}}
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
