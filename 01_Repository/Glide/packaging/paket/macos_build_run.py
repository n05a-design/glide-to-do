"""Vorab- und Abschlussvertrag des nativen Mac-Baulaufs, ohne GUI."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile

from package_sources import identity, in_onedrive, manifest


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_inventory(repo):
    """Genau die Bauquellen sowie Werkzeuge, Originalbelege und Symbole erfassen."""
    repo = Path(repo).resolve()
    files = {"src/glide/" + name: digest
             for name, digest in manifest(repo / "src/glide", "macos-arm64").items()}
    extra = [repo / name for name in ("VERSION", "LICENSE.md", "requirements/build-macos.txt",
                                     "assets/icons/glide_macos_1024.png")]
    extra += [path for path in (repo / "packaging").rglob("*")
              if path.is_file() and "__pycache__" not in path.parts]
    for path in extra:
        if path.is_symlink():
            raise ValueError("Bauquelle ist ein Symlink: " + str(path))
        files[path.relative_to(repo).as_posix()] = sha(path)
    return files


def validate_destination(repo, destination):
    """Niemals Quelle, OneDrive oder einen bereits vorhandenen Ordner verwenden."""
    destination = Path(destination).expanduser()
    if any(ord(char) < 32 for char in str(destination)):
        raise ValueError("Steuerzeichen im Baupfad sind unzulässig.")
    if destination.exists() or destination.is_symlink():
        raise ValueError("Bauziel existiert bereits; einen neuen Ordner wählen.")
    parent = destination.parent.resolve(strict=True)
    destination = parent / destination.name
    repo = Path(repo).resolve()
    if destination == repo or destination.is_relative_to(repo) or repo.is_relative_to(destination):
        raise ValueError("Bauziel muss vollständig außerhalb des Repositorys liegen.")
    if in_onedrive(destination):
        raise ValueError("Bauziel muss außerhalb von OneDrive liegen.")
    return destination


def validate_runtime(expected, actual):
    """Keine aktualisierte Versionsangabe für abweichende Originalbelege erfinden."""
    keys = ("python", "tcl", "tk_compiled", "platform", "machine")
    if any(actual.get(key) != expected.get(key) for key in keys):
        required = ", ".join(f"{key}={expected.get(key)}" for key in keys)
        raise ValueError("Baulaufzeit passt nicht zu den Original-Lizenzbelegen. Erforderlich: " + required)


def native_runtime():
    if sys.platform != "darwin" or platform.machine().lower() != "arm64":
        raise RuntimeError("Dieser Baulauf benötigt einen echten macOS-arm64-Pythonprozess.")
    import _tkinter
    import tkinter
    return dict(python=sys.version.split()[0], tcl=str(tkinter.Tcl().call("info", "patchlevel")),
                tk_compiled=_tkinter.TK_VERSION, platform=sys.platform, machine=platform.machine().lower())


def native_tools():
    required = ("codesign", "sips", "iconutil", "otool", "lipo", "tar", "sandbox-exec", "xcode-select")
    missing = [name for name in required if shutil.which(name) is None]
    if missing:
        raise RuntimeError("Native Bauwerkzeuge fehlen: " + ", ".join(missing))
    selected = subprocess.run(["/usr/bin/xcode-select", "-p"], capture_output=True, text=True, timeout=15)
    if selected.returncode:
        raise RuntimeError("Apple Command Line Tools sind nicht eingerichtet; kein automatischer Installationsversuch.")


def prepare(repo, destination=None):
    repo = Path(repo).resolve()
    runtime = native_runtime()
    basis = json.loads((repo / "packaging/paket/lizenzen/macos/manifest.json").read_text(encoding="utf-8"))
    validate_runtime(basis["runtime"], runtime)
    native_tools()
    version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    identity((repo / "src/glide/app.pyw").read_text(encoding="utf-8"), version)
    inventory = source_inventory(repo)
    if destination is None:
        parent = Path(tempfile.gettempdir()).resolve()
        if in_onedrive(parent) or parent == repo or parent.is_relative_to(repo):
            raise ValueError("Temporärordner ist kein unabhängiger nativer Bauort; --ziel verwenden.")
        destination = Path(tempfile.mkdtemp(prefix=f"glide-macos-{version}-", dir=parent))
    else:
        destination = validate_destination(repo, destination)
        destination.mkdir(mode=0o700)
    write(destination / "eingang.json", dict(version=version, selected_runtime=runtime,
          required_runtime=basis["runtime"], source_sha256=inventory))
    return destination


def verify_sources(repo, initial):
    if source_inventory(repo) != initial["source_sha256"]:
        raise ValueError("Bauquellen wurden seit Beginn verändert; kein gültiger Abschluss.")


def verify_archive(archive, package, expected):
    """Archivinhalt samt Symlinkzielen und Dateimodi gegen das native Paket prüfen."""
    package = Path(package)
    with tarfile.open(archive, "r:gz") as stream:
        members = stream.getmembers()
        prefix = package.name + "/"
        if any(member.name != package.name and not member.name.startswith(prefix) for member in members):
            raise ValueError("Archiv enthält Dateien außerhalb des gewählten App-Bundles.")
        files = {member.name[len(prefix):]: member for member in members
                 if member.isfile() or member.islnk()}
        if set(files) != set(expected):
            raise ValueError("Dateimenge des Mac-Archivs entspricht nicht dem Baumanifest.")
        for name, member in files.items():
            with stream.extractfile(member) as content:
                actual = hashlib.sha256(content.read()).hexdigest()
            if actual != expected[name] or member.mode & 0o7777 != (package / name).stat().st_mode & 0o7777:
                raise ValueError("Archivinhalt oder Dateimodus weicht ab: " + name)
        links = {member.name[len(prefix):]: member.linkname for member in members if member.issym()}
        actual_links = {path.relative_to(package).as_posix(): os.readlink(path)
                        for path in package.rglob("*") if path.is_symlink()}
        if links != actual_links:
            raise ValueError("Symlinks des Mac-Archivs entsprechen nicht dem nativen Bundle.")
    return dict(files=len(files), symlinks=len(links), modes_preserved=True)


def finish(repo, build, archive):
    repo, build, archive = Path(repo).resolve(), Path(build).resolve(), Path(archive).resolve()
    if not archive.is_relative_to(build) or not archive.is_file():
        raise ValueError("Archiv fehlt oder liegt außerhalb des gewählten Bauordners.")
    initial = json.loads((build / "eingang.json").read_text(encoding="utf-8"))
    verify_sources(repo, initial)
    proof = json.loads((build / "bau/bau-ergebnis.json").read_text(encoding="utf-8"))
    smoke = json.loads((build / "startprobe.json").read_text(encoding="utf-8"))
    if proof["version"] != initial["version"] or proof["runtime"] != initial["required_runtime"]:
        raise ValueError("Gebautes Paket stimmt nicht mit Version und ausgewählter Laufzeit überein.")
    if proof["target"] != "macos-arm64" or proof["native"]["exitcode"] or smoke["exitcode"]:
        raise ValueError("Native Paket- oder isolierte Startprüfung ist nicht grün.")
    if not smoke.get("nur_kindprozess_gesperrt") or not smoke.get("system_installationen_unveraendert"):
        raise ValueError("Nachweis des unveränderten Systems und Prozessschutzes fehlt.")
    package = build / "bau/dist/Glide.app"
    archive_proof = verify_archive(archive, package, proof["package_sha256"])
    digest = sha(archive)
    archive.with_name(archive.name + ".sha256").write_text(digest + "  " + archive.name + "\n", encoding="utf-8")
    report = dict(exitcode=0, version=initial["version"], target="macos-arm64",
                  archive=archive.name, sha256=digest, archive_validation=archive_proof,
                  source_files=len(initial["source_sha256"]), sources_unchanged=True,
                  signature=proof["signatur"], native_start_verified=True,
                  developer_id_and_notarization="offen; Entwicklungsartefakt")
    write(build / "abschluss.json", report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "finish"))
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--ziel", type=Path)
    parser.add_argument("--archiv", type=Path)
    args = parser.parse_args()
    if args.mode == "prepare":
        print(prepare(args.repo, args.ziel))
    elif args.ziel is None or args.archiv is None:
        parser.error("finish benötigt --ziel und --archiv")
    else:
        print(json.dumps(finish(args.repo, args.ziel, args.archiv), ensure_ascii=False))


if __name__ == "__main__":
    main()
