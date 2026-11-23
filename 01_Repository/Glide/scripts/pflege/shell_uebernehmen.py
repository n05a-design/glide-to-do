# SPDX-License-Identifier: MPL-2.0
"""Übernimmt das Paket `glide_shell` in ein Folgeprojekt und prüft bestehende Kopien (D95).

Aufruf (Ziel ist der Quellordner des Folgeprojekts, in dem `glide_shell/` liegen soll):

    python3 -B scripts/pflege/shell_uebernehmen.py <Ziel>                   # anlegen oder aktualisieren
    python3 -B scripts/pflege/shell_uebernehmen.py --commit <Rev> <Ziel>    # reproduzierbar aus einem Commit
    python3 -B scripts/pflege/shell_uebernehmen.py --pruefen <Ziel>         # nur prüfen, nichts schreiben
    python3 -B scripts/pflege/shell_uebernehmen.py --ersetzen <Ziel>        # lokale Änderungen überschreiben

Das Werkzeug kopiert alle `*.py` und `*.md` aus `src/glide/glide_shell` sowie
den vollständigen Lizenztext `LICENSE` (MPL-2.0) aus der Repository-Wurzel nach
`<Ziel>/glide_shell` und schreibt daneben `SHELL_MANIFEST.json` mit
`SHELL_VERSION`, Glide-Systemversion, Quell-Commit, ob die Quelle diesem Commit
entspricht (`quelle_unveraendert`), Lizenz und SHA-256 jeder Datei.

Quelle:

- Ohne `--commit` dient die Arbeitskopie als Quelle. Ist sie im Shell-Ordner
  oder beim Lizenztext lokal verändert (auch unversionierte Dateien), verweigert
  das Werkzeug die Übernahme mit Exitcode 3; `--unsauber-erlauben` übernimmt
  bewusst und vermerkt `quelle_unveraendert: false`.
- Mit `--commit <Rev>` liest das Werkzeug genau die versionierten Dateien dieses
  Commits aus Git, unabhängig von der Arbeitskopie (reproduzierbare Übernahme).

Ziel:

- Stimmt die Kopie mit ihrem eigenen, gültigen Manifest überein, wird sie
  ersetzt. Dateien, die das alte Manifest nennt und die es in der Quelle nicht
  mehr gibt, werden entfernt; Dateien ohne Manifesteintrag bleiben stehen.
  Liefert die Shell neu eine Datei, die es in der Kopie schon ohne
  Manifesteintrag und mit anderem Inhalt gibt, bricht das Werkzeug ab.
- Weicht eine Datei von ihrem Manifest ab, ist das Manifest ungültig oder fehlt
  es bei einem nicht leeren Ordner, bricht das Werkzeug ab; `--ersetzen`
  überschreibt dann bewusst.

`--pruefen` meldet je Datei `aktuell`, `veraltet` (unverändert, aber älter
als die Quelle), `verändert` (abweichend vom eigenen Manifest), `fehlt`,
`neu in der Quelle`, `nicht mehr in der Quelle` oder `zusätzlich` (ein Modul
ohne Manifesteintrag, das als `glide_shell.<name>` importierbar wäre) sowie
Verstöße gegen das Manifestschema; Exitcode 0 nur, wenn alles aktuell ist.
Ohne Glide-Checkout prüft das Folgeprojekt seine Kopie mit
`python -m glide_shell.selftest` (Prüfung `manifest`).

Exitcodes: 0 in Ordnung, 1 Prüfung mit Abweichung, 2 Übernahme verweigert
(Konflikt im Ziel), 3 Quelle unbrauchbar (fehlt, beschädigt, lokal verändert
ohne Zustimmung oder Commit unbekannt).
"""
import argparse
import ast
import hashlib
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.parse

REPO = pathlib.Path(__file__).resolve().parents[2]
QUELLE = REPO / "src" / "glide" / "glide_shell"
LIZENZ = REPO.parents[1] / "LICENSE"
PAKET = "glide_shell"
MANIFEST = "SHELL_MANIFEST.json"
LIZENZDATEI = "LICENSE"
# Quelltext und die Anleitungen für Folgeprojekte; dazu der Lizenztext.
ANTEILE = (".py", ".md")
SEMVER = re.compile(r"\d+\.\d+\.\d+")
HEX64 = re.compile(r"[0-9a-f]{64}")
HEX40 = re.compile(r"[0-9a-f]{40}")
OK, ABWEICHUNG, VERWEIGERT, QUELLFEHLER = 0, 1, 2, 3


class QuellFehler(Exception):
    """Die Quelle ist nicht nutzbar (Exitcode 3)."""


def sha(pfad):
    return hashlib.sha256(pfad.read_bytes()).hexdigest()


def sha_bytes(inhalt):
    return hashlib.sha256(inhalt).hexdigest()


def version_aus_text(text):
    """SHELL_VERSION aus dem Quelltext von `__init__.py`; None, wenn sie fehlt oder kein SemVer ist."""
    try:
        baum = ast.parse(text)
    except SyntaxError:
        return None
    for knoten in baum.body:
        if (isinstance(knoten, ast.Assign) and isinstance(knoten.value, ast.Constant)
                and any(getattr(z, "id", None) == "SHELL_VERSION" for z in knoten.targets)):
            wert = knoten.value.value
            return wert if isinstance(wert, str) and SEMVER.fullmatch(wert) else None
    return None


def shell_version(ordner=QUELLE):
    pfad = ordner / "__init__.py"
    wert = version_aus_text(pfad.read_text(encoding="utf-8")) if pfad.is_file() else None
    if wert is None:
        raise QuellFehler(f"{pfad}: SHELL_VERSION fehlt oder ist kein SemVer")
    return wert


def _git(*argumente, text=True):
    try:
        return subprocess.run(["git", "-C", str(REPO), *argumente], capture_output=True, text=text, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None


def quell_commit():
    lauf = _git("rev-parse", "HEAD")
    return (lauf.stdout.strip() or None) if lauf and lauf.returncode == 0 else None


def quelle_unveraendert():
    """True, wenn `glide_shell` und der Lizenztext dem Quell-Commit entsprechen; None ohne Git."""
    lauf = _git("status", "--porcelain", "--untracked-files=all", "--", str(QUELLE), str(LIZENZ))
    return not lauf.stdout.strip() if lauf and lauf.returncode == 0 else None


def _quelle_arbeitskopie(unsauber_erlauben):
    if not (QUELLE / "__init__.py").is_file():
        raise QuellFehler(f"{QUELLE}: Shell-Quelle fehlt")
    if not LIZENZ.is_file():
        raise QuellFehler(f"{LIZENZ}: Lizenztext fehlt")
    unveraendert = quelle_unveraendert()
    if unveraendert is False and not unsauber_erlauben:
        raise QuellFehler(f"{QUELLE}: lokal verändert gegenüber dem Commit – committen, mit --commit "
                          "aus einem Commit übernehmen oder mit --unsauber-erlauben bewusst übernehmen")
    dateien = {p.name: p.read_bytes() for p in sorted(QUELLE.iterdir()) if p.is_file() and p.suffix in ANTEILE}
    dateien[LIZENZDATEI] = LIZENZ.read_bytes()
    system = REPO / "GLIDE_SYSTEM_VERSION"
    return {"dateien": dateien, "commit": quell_commit(), "unveraendert": unveraendert,
            "system": system.read_text(encoding="utf-8").strip() if system.is_file() else None}


def _git_datei(commit, pfad):
    lauf = _git("show", f"{commit}:{pfad}", text=False)
    if not lauf or lauf.returncode != 0:
        raise QuellFehler(f"{commit[:12]}:{pfad} fehlt im Commit")
    return lauf.stdout


def _quelle_commit(rev):
    lauf = _git("rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if not lauf or lauf.returncode != 0 or not lauf.stdout.strip():
        raise QuellFehler(f"{rev}: Commit unbekannt")
    commit = lauf.stdout.strip()
    praefix = _git("rev-parse", "--show-prefix").stdout.strip()
    ordner = f"{praefix}src/glide/glide_shell/"
    liste = _git("ls-tree", "--full-tree", "--name-only", commit, ordner)
    namen = [pathlib.PurePosixPath(z).name for z in liste.stdout.splitlines()] if liste.returncode == 0 else []
    namen = sorted(n for n in namen if pathlib.PurePosixPath(n).suffix in ANTEILE)
    if "__init__.py" not in namen:
        raise QuellFehler(f"{commit[:12]}: Shell-Quelle fehlt im Commit")
    dateien = {n: _git_datei(commit, ordner + n) for n in namen}
    dateien[LIZENZDATEI] = _git_datei(commit, LIZENZDATEI)
    system = _git_datei(commit, f"{praefix}GLIDE_SYSTEM_VERSION").decode("utf-8").strip()
    return {"dateien": dateien, "commit": commit, "unveraendert": True, "system": system}


def quelle_lesen(commit=None, unsauber_erlauben=False):
    """Liefert die zu übernehmende Quelle; QuellFehler, wenn sie fehlt, beschädigt oder unsauber ist."""
    quelle = _quelle_commit(commit) if commit else _quelle_arbeitskopie(unsauber_erlauben)
    try:
        version = version_aus_text(quelle["dateien"]["__init__.py"].decode("utf-8"))
    except UnicodeDecodeError:
        version = None
    if version is None:
        raise QuellFehler("__init__.py der Quelle: SHELL_VERSION fehlt oder ist kein SemVer")
    quelle["version"] = version
    quelle["hashes"] = {name: sha_bytes(inhalt) for name, inhalt in quelle["dateien"].items()}
    return quelle


def quelldateien():
    """SHA-256 der Shell-Dateien der Arbeitskopie (ohne Sauberkeitsprüfung)."""
    return quelle_lesen(unsauber_erlauben=True)["hashes"]


def manifest_fehler(daten, ordner=None):
    """Verstöße gegen das Manifestschema; leer, wenn das Manifest gültig und in sich stimmig ist."""
    if not isinstance(daten, dict):
        return ["kein JSON-Objekt"]
    fehler = []
    dateien = daten.get("dateien")
    if daten.get("paket") != PAKET:
        fehler.append(f"paket ist nicht {PAKET}")
    if daten.get("lizenz") != "MPL-2.0":
        fehler.append("lizenz ist nicht MPL-2.0")
    if not (isinstance(daten.get("shell_version"), str) and SEMVER.fullmatch(daten["shell_version"])):
        fehler.append("shell_version fehlt oder ist kein SemVer")
    commit = daten.get("quell_commit")
    if commit is not None and not (isinstance(commit, str) and HEX40.fullmatch(commit)):
        fehler.append("quell_commit ist kein Commit-Hash")
    if not isinstance(dateien, dict) or "__init__.py" not in dateien:
        return fehler + ["dateien fehlt oder nennt kein __init__.py"]
    for name, wert in sorted(dateien.items()):
        if (not isinstance(name, str) or name in ("", ".", "..") or "/" in name or "\\" in name or
                name == MANIFEST or name.startswith(".") or ".." in name or os.path.basename(name) != name):
            fehler.append(f"unzulässiger Dateiname {name!r}")
        elif not (isinstance(wert, str) and HEX64.fullmatch(wert)):
            fehler.append(f"{name}: kein SHA-256")
        elif ordner is not None and (ordner / name).is_symlink():
            fehler.append(f"{name}: symbolischer Link ist unzulässig")
    if ordner is not None and (ordner / MANIFEST).is_symlink():
        fehler.append(f"{MANIFEST}: symbolischer Link ist unzulässig")
    if ordner is not None and not fehler and (ordner / "__init__.py").is_file():
        version = version_aus_text((ordner / "__init__.py").read_text(encoding="utf-8", errors="replace"))
        if version != daten["shell_version"]:
            fehler.append(f"shell_version {daten['shell_version']} widerspricht __init__.py ({version})")
    return fehler


def manifest_lesen(ordner):
    """(Manifest, Fehlerliste); (None, []) ohne Manifest."""
    pfad = ordner / MANIFEST
    if not pfad.is_file():
        return None, []
    if pfad.is_symlink():
        return {}, [f"{MANIFEST}: symbolischer Link ist unzulässig"]
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}, ["nicht lesbar"]
    return daten, manifest_fehler(daten, ordner)


def schreiben_atomar(ziel, inhalt):
    fd, temp = tempfile.mkstemp(dir=ziel.parent, prefix="." + ziel.name + ".")
    try:
        with os.fdopen(fd, "wb") as datei:
            datei.write(inhalt)
        os.replace(temp, ziel)
    except BaseException:
        pathlib.Path(temp).unlink(missing_ok=True)
        raise


def lokale_abweichungen(ordner, manifest):
    """Dateien der Kopie, die nicht mehr ihrem eigenen Manifest entsprechen."""
    if not isinstance(manifest, dict) or not isinstance(manifest.get("dateien"), dict):
        return []
    abweichend = []
    for name, wert in sorted(manifest["dateien"].items()):
        pfad = ordner / name
        if pfad.is_symlink():
            abweichend.append((name, "symbolischer Link"))
        elif not pfad.is_file():
            abweichend.append((name, "fehlt"))
        elif sha(pfad) != wert:
            abweichend.append((name, "verändert"))
    return abweichend


def fremde_kollisionen(ordner, manifest, quelle):
    """Eigene Dateien ohne Manifesteintrag, die eine neue Shell-Datei gleichen Namens überschreiben würde."""
    return [name for name in sorted(quelle) if name not in manifest["dateien"]
            and (ordner / name).is_file() and sha(ordner / name) != quelle[name]]


def zusaetzliche_module(ordner, bekannt):
    """Module im Paketordner ohne Eintrag, die als `glide_shell.<name>` importierbar wären."""
    return sorted(p.name for p in ordner.iterdir()
                  if p.name not in bekannt and (p.suffix == ".py" or (p.is_dir() and (p / "__init__.py").is_file())))


def pruefen(ordner, quelle=None):
    """(Manifest, Zeilen) der Kopie gegenüber der Quelle; Manifestfehler stehen als Zeilen `SHELL_MANIFEST.json`."""
    quelle = quelle if quelle is not None else quelldateien()
    manifest, fehler = manifest_lesen(ordner)
    eigen = manifest["dateien"] if manifest and not fehler else {}
    zeilen = []
    if manifest is None:
        zeilen.append((MANIFEST, "fehlt"))
    else:
        zeilen.extend((MANIFEST, f"ungültig: {f}") for f in fehler)
    for name in sorted(set(quelle) | set(eigen)):
        pfad = ordner / name
        if pfad.is_symlink():
            zeilen.append((name, "symbolischer Link (unzulässig)"))
        elif name not in quelle:
            zeilen.append((name, "nicht mehr in der Quelle"))
        elif not pfad.is_file():
            zeilen.append((name, "fehlt" if name in eigen else "neu in der Quelle"))
        elif name in eigen:
            if sha(pfad) != eigen[name]:
                zeilen.append((name, "verändert"))
            elif sha(pfad) == quelle[name]:
                zeilen.append((name, "aktuell"))
            else:
                zeilen.append((name, "veraltet"))
        elif manifest is not None and not fehler:
            zeilen.append((name, "ohne Manifesteintrag"))
        elif sha(pfad) == quelle[name]:
            zeilen.append((name, "aktuell"))
        else:
            zeilen.append((name, "verändert"))
    zeilen.extend((name, "zusätzlich, ohne Manifesteintrag als Modul importierbar")
                  for name in zusaetzliche_module(ordner, set(quelle) | set(eigen) | {"__pycache__"}))
    return (manifest if not fehler else None), zeilen


def _verweigern(ordner, manifest, fehler, quelle):
    """Gründe, die Übernahme ohne `--ersetzen` abzulehnen; leer, wenn sie gefahrlos ist."""
    vorhanden = [p.name for p in ordner.iterdir() if p.name not in (MANIFEST, "__pycache__")]
    hinweis = " – mit --ersetzen bewusst überschreiben"
    symlinks = [p.name for p in ordner.iterdir() if p.is_symlink()]
    if symlinks:
        return [f"{name}: symbolischer Link im Zielordner (unzulässig){hinweis}" for name in sorted(symlinks)]
    if manifest is None:
        return [f"{ordner}: Ordner ist nicht leer und hat kein {MANIFEST}{hinweis}"] if vorhanden else []
    if fehler:
        return [f"{MANIFEST}: ungültig ({f}){hinweis}" for f in fehler]
    gruende = [f"{name}: {art} gegenüber {MANIFEST}{hinweis}" for name, art in lokale_abweichungen(ordner, manifest)]
    gruende += [f"{name}: eigene Datei ohne Manifesteintrag, die Shell liefert jetzt dieselbe Datei{hinweis}"
                for name in fremde_kollisionen(ordner, manifest, quelle)]
    return gruende


PROJEKT_WURZEL_MARKER = (
    ".git",
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "Pipfile",
    "requirements.txt",
    "AGENTS.md",
    "CLAUDE.md",
)


def ermittle_projekt_root(ordner, explizit=None):
    """Ermittelt die Projektwurzel für den Agenten-Bootstrap.

    Unterscheidet eindeutig zwischen:
    - Glide-Repository-Wurzel (wird als Ziel abgewiesen)
    - Consumer-Projektwurzel (wo AGENTS.md, .agents/, .claude/ platziert werden)
    - Shell-Zielverzeichnis (ordner, wo glide_shell/ liegt)
    """
    quelle = QUELLE.resolve()
    repo_src = (REPO / "src").resolve()

    if explizit is not None:
        root = pathlib.Path(explizit).expanduser().resolve()
        if root == quelle or quelle in root.parents or repo_src in root.parents or root == REPO.resolve():
            raise ValueError(f"Projektwurzel {root} darf nicht im Glide-Repository liegen")
        if root.exists() and not root.is_dir():
            raise ValueError(f"Projektwurzel {root} ist kein Verzeichnis")
        return root

    # Automatische Erkennung: Aufstieg von ordner.parent
    start = ordner.parent.resolve()
    kandidat = start
    while True:
        if kandidat == quelle or quelle in kandidat.parents or repo_src in kandidat.parents or kandidat == REPO.resolve():
            break
        for marker in PROJEKT_WURZEL_MARKER:
            if (kandidat / marker).exists():
                return kandidat
        if kandidat.parent == kandidat:
            break
        kandidat = kandidat.parent

    # Layout-Heuristik für Standard-Python-Strukturen (z. B. projekt/src/app/glide_shell)
    if start.parent.name == "src" and start.parent.parent != start.parent:
        return start.parent.parent
    if start.name == "src" and start.parent != start:
        return start.parent

    # Flache Struktur als Standard-Fallback: consumer/glide_shell -> consumer
    return start


def _rel_url(ziel_pfad, basis_ordner):
    """Berechnet einen relativen POSIX-Pfad für Markdown-Links mit RFC 3986-Codierung."""
    rel = os.path.relpath(ziel_pfad, basis_ordner).replace("\\", "/")
    return urllib.parse.quote(rel, safe="/@:")


def generiere_bootstrap_inhalte(projekt_root, shell_ordner):
    """Erzeugt dynamisch korrekte Inhalte für AGENTS.md und die Skills mit exakten relativen Pfaden."""
    anleitung_de = shell_ordner / "KI_ANLEITUNG_NEUE_PROJEKTE.md"
    anleitung_en = shell_ordner / "AI_GUIDE_NEW_PROJECTS.md"
    startprompt = shell_ordner / "STARTPROMPT_KI.md"
    design = shell_ordner / "DESIGN_RICHTLINIEN.md"
    manifest = shell_ordner / "SHELL_MANIFEST.json"

    link_de_root = _rel_url(anleitung_de, projekt_root)
    link_en_root = _rel_url(anleitung_en, projekt_root)
    link_prompt_root = _rel_url(startprompt, projekt_root)
    link_design_root = _rel_url(design, projekt_root)
    link_manifest_root = _rel_url(manifest, projekt_root)

    rel_shell_from_root = os.path.relpath(shell_ordner, projekt_root).replace("\\", "/")
    cmd_cd_posix = ""
    cmd_cd_ps = ""
    if rel_shell_from_root not in (".", "glide_shell"):
        parent_dir = rel_shell_from_root.rsplit("/", 1)[0]
        cmd_cd_posix = f"cd {shlex.quote(parent_dir)} && "
        ps_path = parent_dir.replace("'", "''")
        cmd_cd_ps = f"Set-Location -LiteralPath '{ps_path}' -ErrorAction Stop; "

    selftest_cmd_posix = f"{cmd_cd_posix}python3 -m glide_shell.selftest"
    selftest_cmd_ps = f"{cmd_cd_ps}python -m glide_shell.selftest"
    selftest_cmd = selftest_cmd_posix
    if cmd_cd_posix:
        selftest_doc = f"`{selftest_cmd_posix}` (Windows: `{selftest_cmd_ps}`)"
    else:
        selftest_doc = f"`python3 -m glide_shell.selftest` (Windows: `python -m glide_shell.selftest`)"

    inhalt_agents = (
        "# Einstieg für KI-Agenten (Folgeprojekt mit Glide Shell)\n\n"
        f"Dieses Projekt nutzt die **Glide Shell** (`{rel_shell_from_root}/`) als anwendungsneutrales Desktop- und Tk-Fundament.\n\n"
        "## Verbindliche Quellen für Agenten\n\n"
        f"1. **KI-Anleitung für neue Projekte:** [`{rel_shell_from_root}/KI_ANLEITUNG_NEUE_PROJEKTE.md`]({link_de_root}) "
        f"(Englisch: [`{rel_shell_from_root}/AI_GUIDE_NEW_PROJECTS.md`]({link_en_root}))\n"
        f"2. **Startprompt für KI-Sitzungen:** [`{rel_shell_from_root}/STARTPROMPT_KI.md`]({link_prompt_root})\n"
        f"3. **Portabler Designvertrag:** [`{rel_shell_from_root}/DESIGN_RICHTLINIEN.md`]({link_design_root})\n"
        f"4. **Shell-Manifest:** [`{rel_shell_from_root}/SHELL_MANIFEST.json`]({link_manifest_root})\n"
        f"5. **Selbsttest der Shell:** {selftest_doc}\n\n"
        "## Grundregeln\n\n"
        f"- **Keine Modifikation der Shell:** Die Dateien unter `{rel_shell_from_root}/` werden nicht manuell editiert; Updates erfolgen über `shell_uebernehmen.py`.\n"
        "- **Fachlogik im Host:** Fachlogik, Domänenmodelle und Fach-UI gehören in das Host-Projekt, nicht in die Shell.\n"
        "- **Designvertrag einhalten:** Universelle Gestaltungsregeln P1–P6, B15 (Knopfschutz), B11 (Hierarchie vor Metadaten), Fokus und Kontrast gelten für alle Oberflächen.\n"
    )

    skill_agents_dir = projekt_root / ".agents" / "skills" / "glide-shell"
    link_de_agents = _rel_url(anleitung_de, skill_agents_dir)
    link_prompt_agents = _rel_url(startprompt, skill_agents_dir)
    link_design_agents = _rel_url(design, skill_agents_dir)
    link_manifest_agents = _rel_url(manifest, skill_agents_dir)

    inhalt_skill_agents = (
        "---\n"
        "name: glide-shell\n"
        "description: Anleitung und Regeln für die Nutzung der Glide Shell in diesem Projekt. Verwenden bei UI-Entwicklung mit Tkinter, Dialogen, Tastaturkürzeln oder beim Aktualisieren der Shell.\n"
        "---\n\n"
        "# Glide Shell – Projektnutzung\n\n"
        "Dieses Projekt verwendet die **Glide Shell** als UI-Fundament.\n\n"
        "## Wichtige Referenzen\n\n"
        f"- Anleitung: [KI_ANLEITUNG_NEUE_PROJEKTE.md]({link_de_agents})\n"
        f"- Startprompt: [STARTPROMPT_KI.md]({link_prompt_agents})\n"
        f"- Portabler Designvertrag: [DESIGN_RICHTLINIEN.md]({link_design_agents})\n"
        f"- Manifest: [SHELL_MANIFEST.json]({link_manifest_agents})\n\n"
        "## Regeln\n\n"
        f"- Dateien in `{rel_shell_from_root}/` nicht manuell ändern.\n"
        f"- Vor und nach UI-Arbeiten: {selftest_doc}.\n"
        "- Designvertrag (P1–P6, B15, B11, Kontrast, Fokus) beachten.\n"
    )

    skill_claude_dir = projekt_root / ".claude" / "skills" / "glide-shell"
    link_de_claude = _rel_url(anleitung_de, skill_claude_dir)
    link_prompt_claude = _rel_url(startprompt, skill_claude_dir)
    link_design_claude = _rel_url(design, skill_claude_dir)
    link_manifest_claude = _rel_url(manifest, skill_claude_dir)

    inhalt_skill_claude = (
        "---\n"
        "name: glide-shell\n"
        "description: Anleitung und Regeln für die Nutzung der Glide Shell in diesem Projekt. Verwenden bei UI-Entwicklung mit Tkinter, Dialogen, Tastaturkürzeln oder beim Aktualisieren der Shell.\n"
        "---\n\n"
        "# Glide Shell – Projektnutzung\n\n"
        "Dieses Projekt verwendet die **Glide Shell** als UI-Fundament.\n\n"
        "## Wichtige Referenzen\n\n"
        f"- Anleitung: [KI_ANLEITUNG_NEUE_PROJEKTE.md]({link_de_claude})\n"
        f"- Startprompt: [STARTPROMPT_KI.md]({link_prompt_claude})\n"
        f"- Portabler Designvertrag: [DESIGN_RICHTLINIEN.md]({link_design_claude})\n"
        f"- Manifest: [SHELL_MANIFEST.json]({link_manifest_claude})\n\n"
        "## Regeln\n\n"
        f"- Dateien in `{rel_shell_from_root}/` nicht manuell ändern.\n"
        f"- Vor und nach UI-Arbeiten: {selftest_doc}.\n"
        "- Designvertrag (P1–P6, B15, B11, Kontrast, Fokus) beachten.\n"
    )

    return inhalt_agents, inhalt_skill_agents, inhalt_skill_claude


class BootstrapTransaction:
    """Verwaltet den transaktionssicheren Bootstrap mit Snapshot und Rollback."""

    def __init__(self, projekt_root, shell_ordner, ersetzen=False):
        self.projekt_root = pathlib.Path(projekt_root).resolve()
        self.shell_ordner = pathlib.Path(shell_ordner).resolve()
        self.ersetzen = ersetzen
        self.files_before = {}
        self.dirs_created = []

    def prepare(self):
        targets = [
            self.projekt_root / "AGENTS.md",
            self.projekt_root / ".agents" / "skills" / "glide-shell" / "SKILL.md",
            self.projekt_root / ".claude" / "skills" / "glide-shell" / "SKILL.md",
        ]
        for t in targets:
            try:
                t.parent.resolve().relative_to(self.projekt_root)
            except ValueError:
                raise ValueError(f"Sicherheitsfehler: Zielpfad {t} liegt außerhalb der Projektwurzel {self.projekt_root}")

            if t.is_symlink():
                link_ziel = (t.parent / os.readlink(t)).resolve()
                try:
                    link_ziel.relative_to(self.projekt_root)
                except ValueError:
                    raise ValueError(f"Sicherheitsfehler: Symlink {t.name} verweist auf externes Ziel außerhalb des Projekts ({link_ziel})")
                self.files_before[t] = ("symlink", os.readlink(t))
            elif t.is_dir():
                raise ValueError(f"{t}: Zielpfad ist ein Verzeichnis (Dateityp unzulässig)")
            elif t.is_file():
                self.files_before[t] = ("file", t.read_bytes())
            elif t.exists():
                raise ValueError(f"{t}: Zielpfad ist ein unzulässiger Dateisystemtyp")
            else:
                self.files_before[t] = ("absent", None)

    def execute(self):
        inhalt_agents, inhalt_agents_skill, inhalt_claude_skill = generiere_bootstrap_inhalte(
            self.projekt_root, self.shell_ordner
        )
        meldungen = []
        agents_md = self.projekt_root / "AGENTS.md"
        skill_agents = self.projekt_root / ".agents" / "skills" / "glide-shell" / "SKILL.md"
        skill_claude = self.projekt_root / ".claude" / "skills" / "glide-shell" / "SKILL.md"

        plan = [
            (agents_md, inhalt_agents, "Agenten-Einstiegspunkt"),
            (skill_agents, inhalt_agents_skill, "Antigravity/Codex-Skill"),
            (skill_claude, inhalt_claude_skill, "Claude-Skill"),
        ]

        for target_file, content, label in plan:
            file_type, old_data = self.files_before.get(target_file, ("absent", None))
            existed = (file_type != "absent")
            if existed and not self.ersetzen:
                meldungen.append(f"{target_file.relative_to(self.projekt_root)}: existiert bereits (unverändert beibehalten)")
                continue

            if target_file.is_symlink():
                target_file.unlink()

            cur = target_file.parent
            parents_to_create = []
            while cur != self.projekt_root and not cur.exists():
                parents_to_create.append(cur)
                cur = cur.parent
            for p in reversed(parents_to_create):
                p.mkdir(parents=True, exist_ok=True)
                if p not in self.dirs_created:
                    self.dirs_created.append(p)

            schreiben_atomar(target_file, content.encode("utf-8"))
            action = "aktualisiert" if existed else "angelegt"
            meldungen.append(f"{target_file.relative_to(self.projekt_root)}: {action} ({label})")

        return meldungen

    def rollback(self):
        """Führt Rollback aus und gibt eine Liste aller aufgetretenen Fehler zurück.

        Gibt eine leere Liste zurück, wenn der Rollback vollständig und verifiziert erfolgreich war.
        """
        errors = []
        for target_file, (file_type, old_data) in self.files_before.items():
            try:
                if file_type == "absent":
                    target_file.unlink(missing_ok=True)
                elif file_type == "file":
                    if target_file.is_symlink() or target_file.is_dir():
                        target_file.unlink(missing_ok=True)
                    schreiben_atomar(target_file, old_data)
                elif file_type == "symlink":
                    target_file.unlink(missing_ok=True)
                    target_file.symlink_to(old_data)
            except Exception as exc:
                errors.append(f"{target_file.name}: Wiederherstellung fehlgeschlagen ({exc})")

        for d in reversed(self.dirs_created):
            try:
                if d.exists() and not any(d.iterdir()):
                    d.rmdir()
            except Exception as exc:
                errors.append(f"{d.name}: Verzeichnisbereinigung fehlgeschlagen ({exc})")

        # Integritätsprüfung nach Rollback
        for target_file, (file_type, old_data) in self.files_before.items():
            try:
                if file_type == "absent":
                    if target_file.is_symlink() or target_file.exists():
                        errors.append(f"{target_file.name}: Datei sollte nach Rollback nicht existieren")
                elif file_type == "file":
                    if target_file.is_symlink():
                        errors.append(f"{target_file.name}: ist nach Rollback symbolischer Link statt Datei")
                    elif not target_file.is_file():
                        errors.append(f"{target_file.name}: fehlt nach Rollback")
                    elif target_file.read_bytes() != old_data:
                        errors.append(f"{target_file.name}: Dateiinhalt weicht nach Rollback ab")
                elif file_type == "symlink":
                    if not target_file.is_symlink():
                        errors.append(f"{target_file.name}: ist nach Rollback kein symbolischer Link")
                    elif os.readlink(target_file) != old_data:
                        errors.append(f"{target_file.name}: Symlink-Ziel weicht nach Rollback ab")
            except Exception as exc:
                errors.append(f"{target_file.name}: Integritätsprüfung nach Rollback fehlgeschlagen ({exc})")

        return errors


def pruefe_bootstrap(projekt_root, shell_ordner):
    """Prüft den Agenten-Bootstrap inhaltlich und strukturell.

    Gibt ein Dict zurück: {rel_name: (status, detail_meldung)}

    Statuswerte:
    - korrekt verwaltet: Entspricht exakt dem aktuellen generierten Standard
    - gültig angepasst: Eigene Datei, aber mit gültigem YAML-Frontmatter (bei Skills)
                        und funktionierenden relativen Links zur Shell
    - veraltet: Datei existiert, aber verweist auf tote Pfade oder alte Shell-Strukturen
    - beschädigt: Dateisystemfehler, ungültiges YAML-Frontmatter oder beschädigte Syntax
    - nicht vorhanden: Datei fehlt
    - nicht überprüfbar: Lesefehler / Berechtigungsproblem
    """
    projekt_root = pathlib.Path(projekt_root).resolve()
    shell_ordner = pathlib.Path(shell_ordner).resolve()

    standard_agents, standard_skill_agents, standard_skill_claude = generiere_bootstrap_inhalte(
        projekt_root, shell_ordner
    )

    ziele = [
        (projekt_root / "AGENTS.md", standard_agents, "AGENTS.md", False),
        (projekt_root / ".agents" / "skills" / "glide-shell" / "SKILL.md", standard_skill_agents, ".agents/skills/glide-shell/SKILL.md", True),
        (projekt_root / ".claude" / "skills" / "glide-shell" / "SKILL.md", standard_skill_claude, ".claude/skills/glide-shell/SKILL.md", True),
    ]

    ergebnisse = {}

    for pfad, standard_inhalt, rel_name, is_skill in ziele:
        if pfad.is_symlink():
            ergebnisse[rel_name] = ("beschädigt", "symbolischer Link ist unzulässig")
            continue
        if pfad.is_dir():
            ergebnisse[rel_name] = ("beschädigt", "ist ein Verzeichnis statt regulärer Datei")
            continue
        if not pfad.exists():
            ergebnisse[rel_name] = ("nicht vorhanden", "Datei fehlt")
            continue

        try:
            inhalt = pfad.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            ergebnisse[rel_name] = ("beschädigt", "kein gültiges UTF-8")
            continue
        except OSError as exc:
            ergebnisse[rel_name] = ("nicht überprüfbar", f"Lesefehler ({exc})")
            continue

        if inhalt == standard_inhalt:
            ergebnisse[rel_name] = ("korrekt verwaltet", "entspricht dem aktuellen Standard")
            continue

        fehlliste = []

        if is_skill:
            if not inhalt.startswith("---\n"):
                fehlliste.append("fehlendes YAML-Frontmatter (muss mit '---' beginnen)")
            else:
                ende = inhalt.find("\n---\n", 4)
                if ende == -1:
                    fehlliste.append("unvollständiges YAML-Frontmatter (schließendes '---' fehlt)")
                else:
                    fm = inhalt[4:ende]
                    if "name:" not in fm or "description:" not in fm:
                        fehlliste.append("YAML-Frontmatter muss 'name' und 'description' enthalten")

        link_muster = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
        links = link_muster.findall(inhalt)
        tote_links = []
        for text, url in links:
            url_clean = url.strip()
            if url_clean.startswith(("http://", "https://", "mailto:", "#")):
                continue
            ziel_rel = urllib.parse.unquote(url_clean.split("#")[0])
            if not ziel_rel:
                continue
            ziel_datei = (pfad.parent / ziel_rel).resolve()
            if not ziel_datei.exists():
                tote_links.append(f"{ziel_rel}")

        if tote_links:
            fehlliste.append(f"tote Dokumentverweise: {', '.join(tote_links[:3])}")

        if "glide_shell" not in inhalt:
            fehlliste.append("keine Referenz auf glide_shell enthalten")

        if fehlliste:
            if any("tote Dokumentverweise" in f for f in fehlliste):
                ergebnisse[rel_name] = ("veraltet", "; ".join(fehlliste))
            else:
                ergebnisse[rel_name] = ("beschädigt", "; ".join(fehlliste))
        else:
            ergebnisse[rel_name] = ("gültig angepasst", "benutzerdefinierte Inhalte mit gültigen Verweisen und Frontmatter")

    return ergebnisse


def bootstrap_agenten(projekt_ordner, shell_ordner=None, ersetzen=False):
    """Kompatibilitäts-Funktion für Agenten-Bootstrap mit atomarem Rollback bei Fehlern."""
    p_root = pathlib.Path(projekt_ordner).resolve()
    s_ordner = pathlib.Path(shell_ordner).resolve() if shell_ordner else (p_root / PAKET)
    tx = BootstrapTransaction(p_root, s_ordner, ersetzen=ersetzen)
    tx.prepare()
    try:
        return tx.execute()
    except BaseException as exc:
        rollback_errors = tx.rollback()
        if isinstance(exc, (KeyboardInterrupt, SystemExit)):
            raise
        if rollback_errors:
            raise RuntimeError(
                f"Agenten-Bootstrap fehlgeschlagen ({exc}) und Rollback unvollständig: {'; '.join(rollback_errors)}"
            ) from exc
        raise RuntimeError(
            f"Agenten-Bootstrap fehlgeschlagen ({exc}) – Rollback erfolgreich ausgeführt"
        ) from exc


def uebernehmen(ordner, ersetzen=False, quelle=None, agenten_bootstrap=False, projekt_root=None):
    quelle = quelle if quelle is not None else quelle_lesen(unsauber_erlauben=True)
    ordner_existierte = ordner.exists()
    ordner.mkdir(parents=True, exist_ok=True)
    manifest, fehler = manifest_lesen(ordner)
    if not ersetzen:
        gruende = _verweigern(ordner, manifest, fehler, quelle["hashes"])
        if gruende:
            if not ordner_existierte and not any(ordner.iterdir()):
                ordner.rmdir()
            return VERWEIGERT, gruende

    # Phase 1: Vollständige Vorbereitung der Sicherung (vor Beginn jeder Mutation)
    bootstrap_tx = None
    if agenten_bootstrap:
        try:
            root_dir = ermittle_projekt_root(ordner, projekt_root)
            bootstrap_tx = BootstrapTransaction(root_dir, ordner, ersetzen=ersetzen)
            bootstrap_tx.prepare()
        except ValueError as fehler_bootstrap:
            if not ordner_existierte and not any(ordner.iterdir()):
                ordner.rmdir()
            return VERWEIGERT, [f"Agenten-Bootstrap abgewiesen: {fehler_bootstrap}"]

    backup_temp = tempfile.TemporaryDirectory(prefix="glide-shell-backup-")
    backup_ordner = pathlib.Path(backup_temp.name)
    try:
        for item in ordner.iterdir():
            if item.name == "__pycache__":
                continue
            ziel_backup = backup_ordner / item.name
            if item.is_symlink():
                ziel_backup.symlink_to(os.readlink(item))
            elif item.is_file():
                shutil.copy2(item, ziel_backup)
            elif item.is_dir():
                shutil.copytree(item, ziel_backup, symlinks=True)

        quell_namen = {p.name for p in ordner.iterdir() if p.name != "__pycache__"}
        backup_namen = {p.name for p in backup_ordner.iterdir()}
        if quell_namen != backup_namen:
            raise RuntimeError(f"Snapshot unvollständig: {quell_namen - backup_namen} fehlt im Backup")
    except BaseException as fehler_snapshot:
        backup_temp.cleanup()
        if not ordner_existierte and not any(ordner.iterdir()):
            ordner.rmdir()
        if isinstance(fehler_snapshot, (KeyboardInterrupt, SystemExit)):
            raise fehler_snapshot
        return ABWEICHUNG, [f"Sicherung fehlgeschlagen ({fehler_snapshot}) – Zielordner unverändert beibehalten"]

    # Phase 2: Mutation des Zielordners mit garantierter Rollback-Möglichkeit
    try:
        alt = manifest["dateien"] if manifest and not fehler else {}
        vorhanden = sorted(p.name for p in ordner.iterdir() if p.name not in (MANIFEST, "__pycache__"))
        meldungen = []

        # Schritt 1: Quell-Dateien schreiben
        for name, inhalt in quelle["dateien"].items():
            schreiben_atomar(ordner / name, inhalt)

        # Schritt 2: Veraltete Shell-Dateien entfernen
        for name in sorted(set(alt) - set(quelle["dateien"])):
            (ordner / name).unlink(missing_ok=True)
            meldungen.append(f"{name}: entfernt (nicht mehr Teil der Shell)")

        # Schritt 3: Fremde Dateien beibehalten
        fremd = sorted(n for n in vorhanden if n not in quelle["dateien"] and n not in alt)
        meldungen.extend(f"{name}: bleibt stehen (kein Teil der Shell)" for name in fremd)

        # Schritt 4: Manifest schreiben
        daten = {"paket": PAKET, "shell_version": quelle["version"], "glide_system_version": quelle["system"],
                 "quell_commit": quelle["commit"], "quelle_unveraendert": quelle["unveraendert"],
                 "lizenz": "MPL-2.0", "dateien": quelle["hashes"]}
        schreiben_atomar(ordner / MANIFEST, (json.dumps(daten, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))

        # Schritt 5: Verifizierung des Ergebnisses
        abw = [f"{name}: {art} nach dem Kopieren" for name, art in pruefen(ordner, quelle["hashes"])[1] if art != "aktuell"]
        if abw:
            raise RuntimeError("; ".join(abw))

        herkunft = (quelle["commit"] or "ohne Git")[:12] + ("" if quelle["unveraendert"] is not False else " + lokale Änderungen")
        meldungen.append(f"glide_shell {quelle['version']} ({herkunft}) mit {len(quelle['dateien'])} Dateien nach {ordner}")
        if bootstrap_tx is not None:
            meldungen.extend(bootstrap_tx.execute())
        return OK, meldungen

    except BaseException as fehler_kopie:
        # Rollback: Zustand exakt aus dem verifizierten Backup wiederherstellen
        rollback_fehler = []
        if bootstrap_tx is not None:
            b_errors = bootstrap_tx.rollback()
            if b_errors:
                rollback_fehler.extend([f"Bootstrap-Rollback: {e}" for e in b_errors])

        try:
            if not ordner_existierte and not any(backup_ordner.iterdir()):
                shutil.rmtree(ordner, ignore_errors=False)
            else:
                backup_namen = {p.name for p in backup_ordner.iterdir()}
                for item in list(ordner.iterdir()):
                    if item.name == "__pycache__":
                        continue
                    if item.name not in backup_namen:
                        if item.is_dir() and not item.is_symlink():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                for item in backup_ordner.iterdir():
                    ziel_item = ordner / item.name
                    if item.is_symlink():
                        ziel_item.unlink(missing_ok=True)
                        ziel_item.symlink_to(os.readlink(item))
                    elif item.is_file():
                        shutil.copy2(item, ziel_item)
                    elif item.is_dir():
                        if ziel_item.exists():
                            if ziel_item.is_symlink():
                                ziel_item.unlink()
                            else:
                                shutil.rmtree(ziel_item)
                        shutil.copytree(item, ziel_item, symlinks=True)

                # Integritätsprüfung nach Rollback von ordner
                for item in backup_ordner.iterdir():
                    ziel_item = ordner / item.name
                    if item.is_symlink():
                        if not ziel_item.is_symlink() or os.readlink(ziel_item) != os.readlink(item):
                            rollback_fehler.append(f"Shell-Rollback: {item.name} Symlink weicht nach Wiederherstellung ab")
                    elif item.is_file():
                        if not ziel_item.is_file() or sha(ziel_item) != sha(item):
                            rollback_fehler.append(f"Shell-Rollback: {item.name} Datei weicht nach Wiederherstellung ab")
        except Exception as fehler_rollback:
            rollback_fehler.append(f"Shell-Rollback fehlgeschlagen ({fehler_rollback})")

        if isinstance(fehler_kopie, (KeyboardInterrupt, SystemExit)):
            raise fehler_kopie

        if rollback_fehler:
            return ABWEICHUNG, [
                f"Übernahme fehlgeschlagen ({fehler_kopie}) und Rollback unvollständig: {'; '.join(rollback_fehler)}"
            ]
        return ABWEICHUNG, [f"Übernahme fehlgeschlagen ({fehler_kopie}) – Rollback ausgeführt (Zustand vollständig wiederhergestellt)"]

    finally:
        backup_temp.cleanup()


def zielordner(text):
    ziel = pathlib.Path(text).expanduser().resolve()
    ordner = ziel if ziel.name == PAKET else ziel / PAKET
    quelle = QUELLE.resolve()
    if ordner == quelle or quelle in ordner.parents or (REPO / "src").resolve() in ordner.parents:
        return None
    return ordner


def _pruefen_ausgeben(ordner, quelle, agenten_bootstrap=False, projekt_root=None):
    if not ordner.is_dir():
        print(f"{ordner}: keine Kopie vorhanden")
        return ABWEICHUNG
    manifest, zeilen = pruefen(ordner, quelle["hashes"])
    stand = manifest.get("shell_version") if manifest else "ohne gültiges Manifest"
    print(f"Kopie {stand}, Quelle {quelle['version']} ({(quelle['commit'] or 'ohne Git')[:12]})")
    for name, art in zeilen:
        print(f"  {name}: {art}")
    shell_ok = OK if manifest and all(art == "aktuell" for _, art in zeilen) else ABWEICHUNG

    bootstrap_ok = OK
    if agenten_bootstrap:
        root_dir = ermittle_projekt_root(ordner, projekt_root)
        print(f"Agenten-Bootstrap ({root_dir}):")
        b_ergebnisse = pruefe_bootstrap(root_dir, ordner)
        for rel_name, (status, detail) in b_ergebnisse.items():
            print(f"  {rel_name}: {status} ({detail})")
            if status not in ("korrekt verwaltet", "gültig angepasst"):
                bootstrap_ok = ABWEICHUNG

    return OK if (shell_ok == OK and bootstrap_ok == OK) else ABWEICHUNG


def main(argv=None):
    parser = argparse.ArgumentParser(description="glide_shell in ein Folgeprojekt übernehmen oder eine Kopie prüfen")
    parser.add_argument("ziel", help="Quellordner des Folgeprojekts (oder dessen glide_shell-Ordner)")
    gruppe = parser.add_mutually_exclusive_group()
    gruppe.add_argument("--pruefen", action="store_true", help="nur prüfen, nichts schreiben")
    gruppe.add_argument("--ersetzen", action="store_true", help="lokale Änderungen bewusst überschreiben")
    parser.add_argument("--commit", metavar="REV", help="Shell aus diesem Commit statt aus der Arbeitskopie lesen")
    parser.add_argument("--unsauber-erlauben", action="store_true",
                        help="lokal veränderte Shell-Quelle bewusst übernehmen (im Manifest vermerkt)")
    parser.add_argument("--agenten-bootstrap", "--agent-bootstrap", action="store_true",
                        help="erstellt minimale AGENTS.md und Skills für lokale KI-Agenten im Projektordner")
    parser.add_argument("--projekt-root", "--project-root", metavar="PFAD",
                        help="Projektwurzel des Folgeprojekts für den Agenten-Bootstrap (Standard: automatisch ermittelt)")
    args = parser.parse_args(argv)
    ordner = zielordner(args.ziel)
    if ordner is None:
        print("Ziel liegt im Glide-Quellbaum; Folgeprojekte übernehmen die Shell in ihren eigenen Ordner")
        return VERWEIGERT

    projekt_root_dir = None
    if args.agenten_bootstrap or args.projekt_root:
        try:
            projekt_root_dir = ermittle_projekt_root(ordner, args.projekt_root)
        except ValueError as fehler:
            print(f"Projektwurzel unzulässig: {fehler}")
            return VERWEIGERT

    try:
        quelle = quelle_lesen(args.commit, args.unsauber_erlauben or args.pruefen)
    except QuellFehler as fehler:
        print(f"Quelle unbrauchbar: {fehler}")
        return QUELLFEHLER
    if args.pruefen:
        return _pruefen_ausgeben(ordner, quelle, agenten_bootstrap=args.agenten_bootstrap,
                                 projekt_root=projekt_root_dir)
    code, meldungen = uebernehmen(ordner, ersetzen=args.ersetzen, quelle=quelle,
                                  agenten_bootstrap=args.agenten_bootstrap,
                                  projekt_root=projekt_root_dir)
    for zeile in meldungen:
        print(zeile)
    return code


if __name__ == "__main__":
    sys.exit(main())
