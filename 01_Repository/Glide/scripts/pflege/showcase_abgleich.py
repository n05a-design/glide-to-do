#!/usr/bin/env python3
"""Prüft und liefert den Showcase nach 05; verändert keinen Arbeitsstand."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime

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
        if target.exists() and target.suffix != ".md" and target.read_bytes() != source.read_bytes():
            archive = TARGET/"archiv"
            archive.mkdir(exist_ok=True)
            snapshot = archive/(target.stem+"_vor_Abgleich_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S_%f")+target.suffix)
            shutil.copy2(target,snapshot)
        shutil.copy2(source,target)
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        assert hashlib.sha256(target.read_bytes()).hexdigest() == sha
        records[name] = sha
    print(json.dumps({"ziel":str(TARGET),"sha256":records},ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
