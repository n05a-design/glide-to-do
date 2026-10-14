"""Eigenständiges Entwicklungspaket ausschließlich im nativen lokalen Bauordner.

Die Quellen bleiben unverändert. Lizenzbelege müssen vor dem Bau vollständig
mit Komponenten und SHA-256 erfasst sein; die echte Laufzeitprobe folgt separat.
"""
import argparse
import ast
import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import sysconfig
import tempfile

from compiled_contract import inspect_archive
from package_sources import TARGETS, identity, in_onedrive, manifest
from package_spec import specification, windows_version
from license_contract import macos_native_components, windows_native_components, pure_components, resource_components, validate_components
from runtime_provenance import validate_runtime_proof

PIN = "6.22.3"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def check_native(target):
    system, machine, _dnd = TARGETS[target]
    actual = platform.machine().lower()
    actual = "x86_64" if actual in ("amd64", "x64") else actual
    if sys.platform != system or actual != machine:
        raise RuntimeError("Das Paket muss auf seiner nativen Zielplattform gebaut werden.")
    if sys.version_info[:2] != (3, 14):
        raise RuntimeError("Die gewählte Laufzeit braucht Python 3.14.")
    if importlib.metadata.version("pyinstaller") != PIN:
        raise RuntimeError("Der Bau braucht PyInstaller " + PIN + ".")
    # Tcl ohne Tk-Initialisierung: kein Fenster/Reader wird beim Bauen geöffnet.
    import _tkinter
    import tkinter
    tcl = tkinter.Tcl()
    version = str(tcl.call("info", "patchlevel"))
    if not version.startswith("9.") or not _tkinter.TK_VERSION.startswith("9."):
        raise RuntimeError("Python muss mit Tcl/Tk 9 verbunden sein.")
    return dict(python=sys.version.split()[0], tcl=version, tk_compiled=_tkinter.TK_VERSION,
                platform=sys.platform, machine=actual, pyinstaller=PIN)


def stage_licenses(source, stage, runtime):
    source = source.resolve()
    document = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    if document.get("runtime") != runtime:
        raise ValueError("Lizenzbestand und tatsächlich gewählte Baulaufzeit unterscheiden sich.")
    records = document.get("components", [])
    if not records or any(not isinstance(item, dict) for item in records):
        raise ValueError("Unvollständiges Lizenz-Komponentenverzeichnis.")
    names = {item.get("name") for item in records}
    required = {"Python", "Tcl", "Tk", "PyInstaller", "PyInstaller-Hooks", "tkinterdnd2", "tkdnd", "Glide", "Glide-Schriften"}
    if not required <= names:
        raise ValueError("Fehlende Lizenzkomponenten: " + ", ".join(sorted(required - names)))
    hashes = {}
    for item in records:
        if not item.get("version") or not item.get("source") or not item.get("files"):
            raise ValueError("Komponenten brauchen Version, Herkunft und Lizenzdateien.")
        for name, digest in item["files"].items():
            relative = Path(name)
            if relative.is_absolute() or ".." in relative.parts or "\\" in name:
                raise ValueError("Ungültiger Lizenzpfad.")
            path = source / relative
            if path.is_symlink() or not path.is_file() or not path.resolve().is_relative_to(source):
                raise ValueError("Lizenzdatei fehlt oder verlässt den Lizenzbestand: " + name)
            if sha(path) != digest or not path.read_text(encoding="utf-8").strip():
                raise ValueError("Lizenzdatei stimmt nicht: " + name)
            target = stage / "licenses" / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            hashes[name] = digest
    write(stage / "licenses" / "manifest.json", document)
    return dict(components=records, sha256=hashes)


def build(source, repo_version, destination, target, licenses, runtime_manifest=None):
    runtime = check_native(target)
    own_runtime = None
    if runtime['tcl'] == '9.1.0' or runtime['tk_compiled'] == '9.1':
        if runtime_manifest is None:
            raise ValueError('Tk 9.1 benötigt das geprüfte eigene Runtime-Baumanifest.')
        contract_path = Path(__file__).parents[1] / 'runtime/runtime_contract.py'
        spec = importlib.util.spec_from_file_location('glide_own_runtime_contract', contract_path)
        contract = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(contract)
        include = Path(sysconfig.get_path('include'))
        pins = dict(contract.PINS, python=contract.python_pin(runtime['python'],
                    (include / 'patchlevel.h').read_text(encoding='utf-8'),
                    free_threaded=bool(sysconfig.get_config_var('Py_GIL_DISABLED')),
                    debug=bool(sysconfig.get_config_var('Py_DEBUG'))))
        patches = json.loads(contract_path.with_name('patches.json').read_text(encoding='utf-8'))['patches']
        patches = [patch for patch in patches if patch['platform'] == sys.platform]
        import _tkinter
        own_runtime = validate_runtime_proof(runtime_manifest, runtime, _tkinter.__file__, pins=pins, patches=patches)
    source = source.resolve()
    destination = destination.resolve()
    if destination == source or destination.is_relative_to(source):
        raise ValueError("Bauordner muss außerhalb der Programmquellen liegen.")
    if in_onedrive(destination):
        raise ValueError("Bauordner muss außerhalb OneDrive liegen.")
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError("Für jeden Paketbau einen leeren eigenen Bauordner wählen.")
    product = identity((source / "app.pyw").read_text(encoding="utf-8"), repo_version)
    files = manifest(source, target)
    stage = destination / "quelle"
    stage.mkdir()
    for name, digest in files.items():
        original = source / name
        if sha(original) != digest:
            raise ValueError("Quelle hat sich während des Kopierens geändert: " + name)
        relative = "glide_app.py" if name == "app.pyw" else name
        output = stage / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, output)
        if sha(output) != digest:
            raise ValueError("Kopierabweichung: " + name)
    bootstrap = Path(__file__).with_name("start_glide.py")
    shutil.copy2(bootstrap, stage / bootstrap.name)
    runtime_contract = Path(__file__).with_name('runtime_paths.py')
    shutil.copy2(runtime_contract, stage / runtime_contract.name)
    license_proof = stage_licenses(licenses, stage, runtime)
    input_proof = dict(version=repo_version, target=target, product=product,
                       own_runtime=own_runtime,
                       runtime=runtime, sha256=files, bootstrap_sha256=sha(bootstrap),
                       runtime_contract_sha256=sha(runtime_contract),
                       licenses_sha256={"licenses/"+n:h for n,h in license_proof["sha256"].items()} |
                       {"licenses/manifest.json":sha(stage / "licenses/manifest.json")})
    write(stage / "glide-input.json", input_proof)
    (stage / "windows-version.txt").write_text(windows_version(product), encoding="utf-8")
    assets = source.parents[1] / "assets/icons"
    if target == "macos-arm64":
        png = assets / "glide_macos_1024.png"
        helper = source.parents[1] / "packaging/macos/baue_app.py"
        spec = importlib.util.spec_from_file_location("glide_existing_icon_builder", helper)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        icon = stage / "Glide.icns"
        module.baue_icns(png, icon, kleinbilder={
            size: source / "resources/logo" / f"glide-app-icon-macos-{size}.png" for size in (16,32)})
        icon_source = dict(file="assets/icons/glide_macos_1024.png", sha256=sha(png),
                           helper_sha256=sha(helper), generated_sha256=sha(icon))
    else:
        original = assets / "glide.ico"
        icon = stage / "Glide.ico"
        shutil.copy2(original, icon)
        icon_source = dict(file="assets/icons/glide.ico", sha256=sha(original), generated_sha256=sha(icon))
    input_proof["icon"] = icon_source
    write(stage / "glide-input.json", input_proof)
    modules = sorted(p.stem for p in stage.glob("*.py") if p.name != bootstrap.name)
    spec = destination / "Glide.spec"
    spec.write_text(specification(stage, target, product, icon, modules=modules), encoding="utf-8")
    command = [sys.executable, "-B", "-m", "PyInstaller", "--noconfirm", "--clean",
               "--distpath", str(destination / "dist"), "--workpath", str(destination / "arbeit"), str(spec)]
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    with (destination / "bau.log").open("w", encoding="utf-8") as log:
        result = subprocess.run(command, cwd=stage, env=environment, stdout=log, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError("Paketbau fehlgeschlagen; siehe bau.log im Bauordner.")
    package = (destination / "dist/Glide.app" if target == "macos-arm64" else destination / "dist/Glide")
    executable = package / ("Contents/MacOS/Glide" if target == "macos-arm64" else "Glide.exe")
    sources = {p.stem: p.read_bytes() for p in stage.glob("*.py") if p.name != bootstrap.name}
    compiled = inspect_archive(executable, sources, entry=(bootstrap.stem, bootstrap.read_bytes()))
    if manifest(source, target) != files:
        raise ValueError("Quellen wurden während des Baus verändert.")
    signatures = "unsigniertes Windows-Entwicklungsartefakt"
    native = None
    license_matrix = None
    if target == "macos-arm64":
        from pruefe_macho import audit
        native = audit(package)
        write(destination / "macho-nachpruefung.json", native)
        if native["exitcode"]:
            raise ValueError("Native Bibliothekspfade oder Architektur fehlerhaft; siehe macho-nachpruefung.json")
        binaries = macos_native_components(native["dateien"])
        subprocess.run(["codesign", "--verify", "--deep", "--strict", str(package)], check=True)
        signatures = "Ad-hoc-Signatur geprüft; Developer-ID bleibt offen"
    else:
        from windows_native import audit
        native = audit(package)
        write(destination / 'pe-nachpruefung.json', native)
        if native['exitcode']:
            raise ValueError('Native Windows-DLLs oder Architektur fehlerhaft; siehe pe-nachpruefung.json')
        binaries = windows_native_components(record['path'] for record in native['dateien'])
    import PyInstaller
    analysis = ast.literal_eval((destination / "arbeit/Glide/Analysis-00.toc").read_text(encoding="utf-8"))
    if not isinstance(analysis, tuple) or len(analysis) != 20:
        raise ValueError("Unbekanntes PyInstaller-Analyseformat")
    origins = dict(stage=stage, stdlib=sysconfig.get_path("stdlib"),
                   pyinstaller=Path(PyInstaller.__file__).parent)
    pure = pure_components(analysis[14], **origins)
    base = pure_components(analysis[19], **origins)
    resources = resource_components(name for name in files if name.startswith('resources/'))
    used = validate_components(pure | base | binaries | resources, license_proof["components"])
    license_matrix = dict(pure=pure, base=base, native=binaries, resources=resources, used_components=sorted(used))
    write(destination / "lizenzzuordnung.json", license_matrix)
    output_files = {p.relative_to(package).as_posix(): sha(p) for p in sorted(package.rglob("*"))
                    if p.is_file() and not p.is_symlink()}
    proof = dict(version=repo_version, target=target, runtime=runtime, input=input_proof,
                 licenses=license_proof, compiled_modules=compiled, package_sha256=output_files,
                 native=native, license_matrix=license_matrix,
                 signatur=signatures, startprobe="noch ausstehend")
    write(destination / "bau-ergebnis.json", proof)
    print("Paket gebaut und Quellcode verglichen; isolierte native Startprobe steht aus.")
    return package


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quelle", type=Path, required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--ziel", type=Path, required=True)
    parser.add_argument("--plattform", choices=tuple(TARGETS), required=True)
    parser.add_argument("--lizenzen", type=Path, required=True)
    parser.add_argument("--runtime-bau", type=Path, help="Geprüftes eigenes Tk-9.1-Baumanifest")
    args = parser.parse_args()
    build(args.quelle, args.version, args.ziel, args.plattform, args.lizenzen, args.runtime_bau)


if __name__ == "__main__":
    main()
