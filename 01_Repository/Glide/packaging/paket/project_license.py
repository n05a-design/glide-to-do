# SPDX-License-Identifier: MPL-2.0
"""MPL-Original und zugänglichen Quellstand für neue Binärpakete beilegen."""
import hashlib
from pathlib import Path
import subprocess


SOURCE_REPOSITORY = "https://github.com/n05a-design/glide-to-do"


def stage_project_license(repo, destination, source=None):
    """Einen unveränderten Git-Quellstand als Bezugsquelle nennen.

    Der Aufrufer baut aus repo/src/glide. Fremdkomponenten werden separat
    erfasst; ihre Originalbelege und die historische Lizenzbasis bleiben erhalten.
    """
    repo, destination = Path(repo).resolve(), Path(destination)
    if source is not None and Path(source).resolve() != repo / "src/glide":
        raise ValueError("Paketquelle muss dem erfassten Repository-Quellbaum entsprechen.")
    root = repo.parents[1]
    paths = ["LICENSE", "01_Repository/Glide/LICENSE.md", "01_Repository/Glide/VERSION",
             "01_Repository/Glide/src/glide", "01_Repository/Glide/packaging"]
    def git(*args):
        return subprocess.check_output(["git", "-C", str(root), *args],
                                       text=True, encoding="utf-8", timeout=30).strip()
    revision = git("rev-parse", "HEAD")
    if git("status", "--porcelain", "--untracked-files=all", "--", *paths):
        raise ValueError("Paketquellen oder Lizenzhinweise sind nicht im Git-Commit gesichert.")
    # Git-Originalbytes statt plattformabhängiger Checkout-Zeilenenden.
    terms = subprocess.check_output(["git", "-C", str(root), "show", "HEAD:LICENSE"], timeout=30)
    if not terms.startswith(b"Mozilla Public License Version 2.0") or b"Exhibit A" not in terms:
        raise ValueError("Vollständige MPL-2.0-Originaldatei fehlt.")
    url = f"{SOURCE_REPOSITORY}/tree/{revision}"
    notice = (
        "Glide steht unter der Mozilla Public License 2.0 (SPDX: MPL-2.0).\n"
        "Der vollständige Lizenztext liegt in Glide-MPL-2.0.txt.\n"
        f"Zugehöriger Quellcode: {url}\n"
        f"Quellarchiv: {SOURCE_REPOSITORY}/archive/{revision}.zip\n"
        "Die Eingabedateien dieses Baus stehen mit SHA-256 in glide-input.json.\n"
        "Bei Weitergabe geänderter Fassungen muss der entsprechende Quellcode\n"
        "der abgedeckten Dateien nach MPL 2.0 Abschnitt 3 zugänglich sein.\n"
        "Drittkomponenten und Ressourcen behalten ihre eigenen Lizenzbedingungen.\n"
        "Namens- und Markenrechte werden durch die MPL nicht eingeräumt.\n"
    )
    files = {"Glide-MPL-2.0.txt": terms,
             "Glide-Lizenzstatus.md": subprocess.check_output(
                 ["git", "-C", str(root), "show", "HEAD:01_Repository/Glide/LICENSE.md"], timeout=30),
             "Glide-Quellcode.txt": notice.encode("utf-8")}
    destination.mkdir(parents=True, exist_ok=True)
    for name, data in files.items():
        (destination / name).write_bytes(data)
    return dict(name="Glide", version=(repo / "VERSION").read_text(encoding="utf-8").strip(),
                license="MPL-2.0", source=url,
                files={name: hashlib.sha256(data).hexdigest() for name, data in files.items()})
