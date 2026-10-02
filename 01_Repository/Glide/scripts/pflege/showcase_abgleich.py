#!/usr/bin/env python3
"""Prüft und liefert den Showcase nach 05; verändert keinen Arbeitsstand.

Überschreibt die Lieferkopie ohne Archivkopie: Vorfassungen trägt Git. Bis
3.33.6 legte jeder Lauf rund 73 MB unter 05_Probelisten_Testdaten/Showcase/archiv ab.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

REPO = Path(__file__).resolve().parents[2]
BASE = REPO.parents[1]
SOURCE = REPO/"tests/fixtures/showcase"
TARGET = BASE/"05_Probelisten_Testdaten/Showcase"


def main():
    env = dict(os.environ)
    if sys.platform == "darwin":
        env["GLIDE_QA_HINTERGRUND"] = "1"
        env["PYTHONPATH"] = os.pathsep.join(filter(None, (str(REPO/"tests/tools/hintergrund"), env.get("PYTHONPATH"))))
    subprocess.run([sys.executable,"-B",str(REPO/"tests/tools/pruefe_showcase.py")],cwd=REPO,env=env,check=True)
    TARGET.mkdir(parents=True,exist_ok=True)
    names = ["Glide-Showcase.glidebackup","Glide-Showcase_App.glideapp","Glide-Showcase.glidetemplates",
             "manifest.json","Showcase_starten.pyw","README.md"]
    records = {}
    for name in names:
        source, target = SOURCE/name, TARGET/name
        assert source.is_file(), source
        shutil.copy2(source,target)
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256(target.read_bytes()).hexdigest() == sha
        records[name] = sha
    print(json.dumps({"ziel":str(TARGET),"sha256":records},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
