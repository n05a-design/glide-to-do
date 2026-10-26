"""Übernimmt ausschließlich den erfolgreich vollgeprüften Stand und geprüfte Pakete."""
import hashlib
import json
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import zipfile


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
WORKSPACE = REPO.parents[1]
BUILD = Path.home() / "AppData/Local/Glide-Builds/3.45.0-20261026-01"
VERSION = "3.45.0"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def checked_local_path(path):
    resolved = path.resolve()
    if not resolved.is_relative_to((REPO / "build").resolve()):
        raise ValueError("Lieferziel liegt außerhalb der Projekt-Buildablage")
    return resolved


def verify(package, expected):
    missing = [name for name, digest in expected.items()
               if not (package / name).is_file() or sha(package / name) != digest]
    if missing:
        raise ValueError("Paketdateien weichen ab: " + ", ".join(missing[:12]))


def prepare_copy(source, destination, proof):
    checked_local_path(destination)
    if destination.exists():
        verify(destination, proof["package_sha256"])
        return destination
    staging = checked_local_path(destination.with_name(destination.name + ".staging"))
    if staging.exists():
        raise ValueError("Staging existiert bereits; erst den vorhandenen Nachweis prüfen")
    shutil.copytree(source.resolve(), staging, symlinks=True)
    verify(staging, proof["package_sha256"])
    return staging


def main():
    full = load(HERE / "windows_voll_abschluss/ergebnis.json")
    if full["exitcode"] != 0:
        raise ValueError("Ohne grüne Vollprüfung keine Übernahme")
    windows = load(BUILD / "bau/bau-ergebnis.json")
    mac = load(BUILD / "mac-pruefung/belege/glide-macos-bau/bau/bau-ergebnis.json")
    assert load(HERE / "windows_paket_start.json")["exitcode"] == 0
    assert load(HERE / "mac_entpackpruefung.json")["exitcode"] == 0
    app_hash = sha(REPO / "src/glide/app.pyw")
    for proof in (windows, mac):
        assert proof["version"] == VERSION
        assert proof["input"]["sha256"]["app.pyw"] == app_hash
        assert proof["native"]["exitcode"] == 0

    win_target = checked_local_path(REPO / f"build/windows/Glide-{VERSION}")
    mac_target = checked_local_path(REPO / "build/macos/Glide.app")
    win_target.parent.mkdir(parents=True, exist_ok=True)
    mac_target.parent.mkdir(parents=True, exist_ok=True)
    win_staging = prepare_copy(BUILD / "bau/dist/Glide", win_target, windows)
    # Die aktive alte Mac-App erst nach vollständig geprüfter neuer Kopie bewegen.
    mac_staging_target = checked_local_path(REPO / f"build/macos/Glide-{VERSION}.app")
    mac_staging = prepare_copy(BUILD / "mac-pruefung/unpacked/Glide.app", mac_staging_target, mac)
    if win_staging != win_target:
        win_staging.rename(win_target)
    old_windows = checked_local_path(REPO / "build/windows/Glide-3.42.0")
    old_windows_archive = checked_local_path(REPO / "build/windows/Archiv/Glide-3.42.0")
    if old_windows.exists():
        if old_windows_archive.exists():
            raise ValueError("Vorhandenes Windows-Archiv nicht überschreiben")
        old_windows_archive.parent.mkdir(parents=True, exist_ok=True)
        old_windows.rename(old_windows_archive)
    if mac_staging != mac_staging_target:
        mac_staging.rename(mac_staging_target)
    if mac_target.exists():
        with (mac_target / "Contents/Info.plist").open("rb") as stream:
            previous_version = plistlib.load(stream)["CFBundleShortVersionString"]
        archive = checked_local_path(REPO / f"build/macos/Archiv/Glide-{previous_version}.app")
        if archive.exists():
            raise ValueError("Vorhandene Mac-Archivfassung nicht überschreiben")
        archive.parent.mkdir(parents=True, exist_ok=True)
        mac_target.rename(archive)
    mac_staging_target.rename(mac_target)
    verify(win_target, windows["package_sha256"])
    verify(mac_target, mac["package_sha256"])

    mac_archive = BUILD / f"mac-pruefung/artifact/Glide-{VERSION}-macos-arm64.tar.gz"
    expected_tar = load(BUILD / "mac-pruefung/artifact/abschluss.json")["sha256"]
    assert sha(mac_archive) == expected_tar
    copied_tar = checked_local_path(REPO / f"build/macos/{mac_archive.name}")
    shutil.copy2(mac_archive, copied_tar)
    shutil.copy2(mac_archive.with_name(mac_archive.name + ".sha256"), copied_tar.with_name(copied_tar.name + ".sha256"))
    assert sha(copied_tar) == expected_tar

    win_zip = checked_local_path(REPO / f"build/windows/Glide-{VERSION}-windows-x64.zip")
    with zipfile.ZipFile(win_zip, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(win_target.rglob("*")):
            if path.is_file():
                archive.write(path, f"Glide-{VERSION}/" + path.relative_to(win_target).as_posix())
    with zipfile.ZipFile(win_zip) as archive:
        assert archive.testzip() is None
        for name, digest in windows["package_sha256"].items():
            assert hashlib.sha256(archive.read(f"Glide-{VERSION}/" + name)).hexdigest() == digest
    win_zip.with_name(win_zip.name + ".sha256").write_text(sha(win_zip) + "  " + win_zip.name + "\n", encoding="ascii")

    copied = subprocess.run([sys.executable, "-B", "scripts/pflege/abgleich_07.py"], cwd=REPO,
                            capture_output=True, text=True, encoding="utf-8", check=True)
    sys.path.insert(0, str(REPO / "tests/tools"))
    from ci_grundstufe import lieferstand_abweichungen
    assert lieferstand_abweichungen() == []
    result = dict(exitcode=0, version=VERSION, app_sha256=app_hash,
                  python_delivery_equal=True, python_copy_output=copied.stdout,
                  windows_files=len(windows["package_sha256"]), mac_files=len(mac["package_sha256"]),
                  windows_zip=win_zip.relative_to(WORKSPACE).as_posix(), windows_zip_sha256=sha(win_zip),
                  mac_tar=copied_tar.relative_to(WORKSPACE).as_posix(), mac_tar_sha256=sha(copied_tar),
                  windows_exe=win_target.relative_to(WORKSPACE).as_posix() + "/Glide.exe",
                  mac_bundle=mac_target.relative_to(WORKSPACE).as_posix(),
                  mac_bundle_note="Windows-Inspektionskopie mit NT-Linkzielen; native Weitergabe nur über unverändertes TAR")
    (HERE / "lieferung.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
