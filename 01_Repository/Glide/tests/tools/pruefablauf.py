"""Gemeinsamer WA-42-Prüfwächter; ausschließlich künstliche Prozessdaten.

Belege und Prüfdaten bleiben nach Fehlern erhalten. Ein gestoppter Lauf darf
keinen weiteren Fall beginnen. Dokumentänderungen werden separat ausgewiesen,
heben den Integritätsstopp aber nicht auf.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from prozessdiagnose import systemkontext, pruefplatz


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def lokale_ablage(path=None, *, environment=None, system_temp=None):
    """Keine Prozessdaten in OneDrive oder im ursprünglichen System-Temp."""
    environment = os.environ if environment is None else environment
    candidate = Path(path or Path.home() / "GlidePruefung").expanduser().resolve()
    excluded = [Path(system_temp or tempfile.gettempdir()).resolve()]
    excluded.extend(Path(value).expanduser().resolve() for key, value in environment.items()
                    if key.casefold().startswith("onedrive") and value)
    if any(candidate.is_relative_to(root) for root in excluded) or any(
            part.casefold().startswith("onedrive") for part in candidate.parts):
        raise ValueError("Prüfablage muss außerhalb von OneDrive und System-Temp liegen")
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


def dateien(repo):
    """Ausführbare Quelle, Ressourcen, Fixtures und verbindliche Dokumente.

    Ergebnisse unter tests/qa-* und generierte Bauartefakte sind keine Eingaben.
    Auch neu angelegte/verlorene Eingabedateien werden erkannt.
    """
    repo = Path(repo).resolve()
    project = repo.parents[1]
    roots = [repo / name for name in ("src", "tests/tools", "tests/unit",
             "tests/integration", "tests/fixtures", "scripts", "packaging", "docs")]
    roots += [project / "00_Arbeitsvorbereitung", project / ".claude/skills"]
    roots += [project / "05_Probelisten_Testdaten", project / "07_Python-Versionen"]
    found = {path for root in roots if root.exists() for path in root.rglob("*")
             if path.is_file() and "__pycache__" not in path.parts
             and path.suffix.lower() not in (".pyc", ".pyo")}
    found.update(path for root in (project, repo) for path in root.glob("*.md"))
    if (repo / "VERSION").is_file():
        found.add(repo / "VERSION")
    return {path.relative_to(project).as_posix(): sha256(path) for path in sorted(found)}


def einfrieren(repo, ablage=None):
    """Aktuellen Arbeitsbaum kopieren; historische Gitobjekte lokal bereitstellen.

    Der Klon hat eigene Metadaten und verwendet ausschließlich lokale Gitobjekte.
    Aktuelle Änderungen und nicht ignorierte neue Dateien kommen aus der
    Arbeitskopie. Keine Checkout-/Resetaktion im ursprünglichen Repository.
    """
    repo = Path(repo).resolve()
    project = repo.parents[1]
    root = Path(tempfile.mkdtemp(prefix="pruefkopie-", dir=lokale_ablage(ablage)))
    frozen = root / "projekt"
    names = subprocess.run(["git", "-C", str(project), "ls-files", "-co", "--exclude-standard", "-z"],
                           capture_output=True, timeout=90, check=True).stdout.decode("utf-8").split("\0")
    selected = {name for name in names if name and (project / name).is_file()}
    # Referenzbilder und andere lokal gehaltene kanonische Eingaben werden
    # ebenfalls geschützt kopiert; Rohlogs/Dumps unter tests/qa-* bleiben außen.
    selected.update(dateien(repo))
    for name in selected:
        source = project / name
        if source.is_symlink() or not source.resolve().is_relative_to(project):
            raise ValueError(f"Prüfeingang enthält Link außerhalb des regulären Dateivertrags: {name}")
    original = {name: sha256(project / name) for name in sorted(selected)}
    proof = {"sha256": original, "source": str(project), "copy": str(frozen),
             "phase": "kopieren", "source_unchanged": False, "copy_equal": False,
             "git_history": "Lokaler Klon mit eigenen Metadaten; keine Netzwerkübertragung"}
    proof_path = root / "quellstand.json"
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    subprocess.run(["git", "clone", "--local", "--no-checkout", str(project), str(frozen)],
                   capture_output=True, timeout=90, check=True)
    subprocess.run(["git", "-C", str(frozen), "read-tree", "HEAD"],
                   capture_output=True, timeout=30, check=True)
    for name in original:
        source = project / name
        if source.is_symlink() or not source.resolve().is_relative_to(project):
            raise ValueError(f"Prüfeingang enthält Link außerhalb des regulären Dateivertrags: {name}")
        destination = frozen / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    source_after = {name: sha256(project / name) for name in original}
    copied = {name: sha256(frozen / name) for name in original}
    names_after = subprocess.run(["git", "-C", str(project), "ls-files", "-co", "--exclude-standard", "-z"],
                                 capture_output=True, timeout=90, check=True).stdout.decode("utf-8").split("\0")
    selected_after = {name for name in names_after if name and (project / name).is_file()}
    selected_after.update(dateien(repo))
    proof.update(source_unchanged=source_after == original and selected_after == selected,
                 copy_equal=copied == original, phase="geprüft")
    proof_path.write_text(json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not proof["source_unchanged"] or not proof["copy_equal"]:
        raise ValueError("Quellbestand während des Einfrierens verändert; Prüffolge nicht gestartet")
    return frozen / repo.relative_to(project), root


def laufzeit():
    try:
        import _tkinter
        tk = {"tk": _tkinter.TK_VERSION, "tcl": _tkinter.TCL_VERSION}
    except ImportError:
        tk = {"tk": None, "tcl": None}
    context = systemkontext()
    return {"python": sys.version, "executable": sys.executable,
            "executable_sha256": sha256(sys.executable), "platform": platform.platform(),
            "build": platform.python_build(), "systemkontext": context,
            "pruefplatz": pruefplatz(context), **tk}


class Pruefablauf:
    def __init__(self, repo, ablage=None, *, inventory=dateien, runtime=laufzeit):
        self.repo = Path(repo).resolve()
        self.inventory = inventory
        self.root = Path(tempfile.mkdtemp(prefix="lauf-", dir=lokale_ablage(ablage)))
        self.expected = inventory(self.repo)
        self.stopped = False
        self.rows = []
        self.report = {"started": datetime.now(timezone.utc).isoformat(),
                       "runtime": runtime(), "source": str(self.repo),
                       "sha256": self.expected, "cases": self.rows,
                       "input_contract": "Fixtures bytegehasht; selbstgenerierte UUIDs/Zeitstempel sind kein bytegleicher Replay.",
                       "release_ready": False}
        self.save()

    def save(self):
        path = self.root / "pruefablauf.json"
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(self.report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(temporary, path)

    def integrity(self):
        try:
            current = self.inventory(self.repo)
            names = sorted(set(self.expected) | set(current))
            changed = [name for name in names if current.get(name) != self.expected.get(name)]
        except OSError as error:
            return {"source": [], "documents": [], "read_error": type(error).__name__}
        return {"source": [name for name in changed if Path(name).suffix.lower() != ".md"],
                "documents": [name for name in changed if Path(name).suffix.lower() == ".md"]}

    def before(self, name, environment):
        if self.stopped:
            return None
        changes = self.integrity()
        if any(changes.values()):
            self.stopped = True
            self.report["integrity_stop"] = {"before": name, **changes}
            self.save()
            return None
        slug = re.sub(r"[^a-zA-Z0-9_-]", "_", name)[:70] or "fall"
        folder = self.root / f"{len(self.rows) + 1:03d}-{slug}"
        folder.mkdir()
        data = folder / "daten"
        temporary = folder / "temp"
        data.mkdir()
        temporary.mkdir()
        env = dict(environment, GLIDE_DATA_DIR=str(data), GLIDE_TEST_MODE="1",
                   TMP=str(temporary), TEMP=str(temporary), TMPDIR=str(temporary),
                   PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1", PYTHONFAULTHANDLER="1")
        row = {"case": name, "started": datetime.now(timezone.utc).isoformat(),
               "data": str(data), "temporary": str(temporary), "completed": False}
        self.rows.append(row)
        self.save()
        return env

    def after(self, *, ok, returncode=None, output=None, error=None):
        row = self.rows[-1]
        row.update(completed=True, passed=bool(ok), returncode=returncode,
                   finished=datetime.now(timezone.utc).isoformat())
        if output is not None:
            log = Path(row["data"]).parent / "prozess.log"
            log.write_text(output, encoding="utf-8")
            row["log_sha256"] = sha256(log)
        if error:
            row["error"] = error
        changes = self.integrity()
        row["integrity_after"] = changes
        if any(changes.values()):
            row["passed"] = False
            self.report["integrity_stop"] = {"after": row["case"], **changes}
        self.stopped = self.stopped or not row["passed"]
        self.report["stopped"] = self.stopped
        self.save()
        return row["passed"]

    def command(self, name, command, *, timeout, environment=None, cwd=None):
        env = self.before(name, os.environ if environment is None else environment)
        if env is None:
            return None
        self.rows[-1]["command"] = [str(value) for value in command]
        self.save()
        try:
            process = subprocess.Popen(command, cwd=cwd or self.repo, env=env,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       text=True, encoding="utf-8", errors="replace",
                                       start_new_session=os.name != "nt")
            self.rows[-1]["pid"] = process.pid
            self.save()
            try:
                stdout, stderr = process.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                if os.name == "nt":
                    subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                                   capture_output=True, timeout=30, check=False)
                else:
                    os.killpg(process.pid, signal.SIGKILL)
                process.kill()
                stdout, stderr = process.communicate(timeout=30)
                self.after(ok=False, returncode=process.returncode,
                           output=stdout + stderr, error="TimeoutExpired")
                raise subprocess.TimeoutExpired(command, timeout, output=stdout, stderr=stderr)
            result = subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
        except OSError as error:
            self.after(ok=False, error=type(error).__name__)
            raise
        self.after(ok=result.returncode == 0, returncode=result.returncode,
                   output=result.stdout + result.stderr)
        return result
