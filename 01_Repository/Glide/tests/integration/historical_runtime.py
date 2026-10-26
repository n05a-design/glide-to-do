"""Unveränderte Altleser samt passendem historischen Lieferbestand aus Git.

Die Hauptdateien im Archiv haben absichtlich keine eigenen Begleitmodule.
Altleser-Proben starten deshalb in einem neuen Prozess aus diesem kurzlebigen
Bestand, niemals mit den inzwischen fortgeschriebenen Modulen aus 07. Es wird
kein Produktionscode angepasst und kein Daten-/Speicherverhalten ersetzt.
"""
import ast
from contextlib import contextmanager
import hashlib
import io
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tempfile


# Erster vollständiger Liefercommit der tatsächlich archivierten Hauptdatei.
SNAPSHOTS = {
    "3.43.1": "b2af7a7e360764150c03e58321c96eb954398828",
    "3.40.0": "ba060bc5e0074c0f375b6da29b07450ab08b34be",
}
DELIVERY = "07_Python-Versionen"


def _git(repo, *arguments):
    # Auch ohne übergeordnete .gitattributes darf Windows beim Archivieren
    # keine CRLF-Arbeitskopie aus den geprüften Blobbytes erzeugen.
    result = subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf",
                             "-C", str(repo), *arguments],
                            capture_output=True, timeout=90)
    if result.returncode:
        raise RuntimeError("Historischer Git-Bestand nicht lesbar; Git-Historie vollständig "
                           "bereitstellen (kein automatischer Fetch): " +
                           result.stderr.decode("utf-8", errors="replace").strip())
    return result.stdout


def _version(data):
    values = []
    for node in ast.parse(data.decode("utf-8-sig")).body:
        if isinstance(node, ast.Assign) and any(
                isinstance(target, ast.Name) and target.id == "APP_VERSION"
                for target in node.targets):
            values.append(ast.literal_eval(node.value))
    if len(values) != 1 or values[0] not in SNAPSHOTS:
        raise ValueError("Kein eindeutig gepinnter historischer Altleser")
    return values[0]


def _write_archive(raw, destination):
    """Nur reguläre Git-Dateien übernehmen, ohne Pfad- oder Linkausbruch."""
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        for member in archive:
            relative = PurePosixPath(member.name)
            if (relative.is_absolute() or ".." in relative.parts or
                    "\\" in member.name or relative.as_posix() != member.name.rstrip("/")):
                raise ValueError("Unsicherer historischer Archivpfad")
            output = destination.joinpath(*relative.parts)
            if not output.resolve().is_relative_to(destination.resolve()):
                raise ValueError("Historischer Archivpfad verlässt den Prüfbestand")
            if member.isdir():
                output.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                output.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source, output.open("xb") as target:
                    target.write(source.read())
            else:
                raise ValueError("Historischer Prüfbestand enthält einen Link oder Spezialdatei")


@contextmanager
def historical_app(repo_root, archived_app):
    """Liefert die bytegleiche Hauptdatei neben ihrem vollständigen Lieferstand.

    `repo_root` ist die Git-Wurzel; `archived_app` bleibt unverändert. Der
    temporäre Bestand enthält alle damaligen Pythonmodule, Ressourcen und
    Vendor-Dateien, keine jüngeren Ergänzungen und keine alten Nebenarchive.
    Die gewählte Hauptdatei und der gepinnte Liefercommit müssen exakt passen.
    """
    repo, archived_app = Path(repo_root).resolve(), Path(archived_app).resolve()
    original = archived_app.read_bytes()
    version = _version(original)
    commit = SNAPSHOTS[version]
    resolved = _git(repo, "rev-parse", "--verify", commit + "^{commit}").decode().strip()
    if resolved != commit:
        raise ValueError("Historischer Liefercommit stimmt nicht mit dem Pin überein")
    name = f"Glide-Aufgaben-und-Listen_v{version}.pyw"
    committed = _git(repo, "show", f"{commit}:{DELIVERY}/{name}")
    if committed != original:
        raise ValueError("Archivierte Hauptdatei und historischer Lieferstand unterscheiden sich")
    tree = f"{commit}:{DELIVERY}"
    names = _git(repo, "ls-tree", "--name-only", "-z", tree).decode("utf-8").split("\0")
    modules = sorted(value for value in names if value.endswith(".py") and "/" not in value)
    if not modules or not {name, "resources", "vendor"} <= set(names):
        raise ValueError("Historischer Modul-/Ressourcen-/Vendorbestand ist unvollständig")
    raw = _git(repo, "archive", "--format=tar", tree, "--", name, *modules, "resources", "vendor")
    temporary_root = Path(tempfile.gettempdir()).resolve()
    if any(part.casefold() == "onedrive" or part.casefold().startswith(("onedrive-", "onedrive - "))
           for part in temporary_root.parts):
        raise ValueError("Historischer Prüfbestand braucht einen temporären Ort außerhalb OneDrive")
    with tempfile.TemporaryDirectory(prefix="glide-altleser-", dir=temporary_root) as directory:
        destination = Path(directory)
        _write_archive(raw, destination)
        result = destination / name
        if result.read_bytes() != original:
            raise ValueError("Historische Hauptdatei wurde beim Übernehmen verändert")
        # Ein kleiner maschinenlesbarer Beleg ist für den aufrufenden Test
        # verfügbar, ohne Daten oder Betrieb der alten App zu verändern.
        import json
        (destination / "historical-runtime.json").write_text(json.dumps({
            "version": version, "commit": commit,
            "app_sha256": hashlib.sha256(original).hexdigest(),
            "modules": modules,
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        yield result
