from pathlib import Path
import hashlib, importlib.util, json, shutil, sys

ROOT = Path.cwd()
TEMP = Path(__file__).resolve().parent
DEST = ROOT / "50_Ablage/Archiv/Werkzeuge_3.21.4"

def load(name):
    spec = importlib.util.spec_from_file_location(name, DEST / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

# Abort if the reviewed starting state changed in the meantime.
state = json.loads((TEMP / "ausgangsbestand.json").read_text())
for rel, info in state.items():
    assert digest(ROOT / rel) == info["sha256"], "Zwischenzeitlich verändert: " + rel
assert not DEST.exists(), "Werkzeugarchiv existiert bereits"
DEST.mkdir(parents=True)
shutil.copytree(TEMP / "quellstand", DEST / "quellstand")
for p in (TEMP / "werkzeuge").iterdir():
    if p.is_file():
        shutil.copy2(p, DEST / p.name)

ablage = load("ablegen_3214")
# The delivered script only backs up six kinds of files. Preserve every
# changed repository file, including source, version and test tools.
for _, rel in ablage.ZIELE:
    p = Path(rel)
    ablage.ARCHIVIEREN.setdefault(rel, f"{p.stem}_3.21.3_vor_3.21.4{p.suffix}")

sys.argv = [str(DEST / "ablegen_3214.py"), str(DEST / "quellstand")]
assert ablage.main() == 0

fort = load("fortschreiben_3214")
# Keep prior documents in their own folder, including CHANGELOG.
def archive_target(self, rel):
    p = self.pfad(rel)
    folder = fort.vorhandenes_archiv(p.parent) or p.parent / "archiv"
    stem = p.stem if fort.re.search(r"_\d+\.\d+\.\d+$", p.stem) else f"{p.stem}_3.21.3"
    return (folder / f"{stem}_vor_3.21.4{p.suffix}").relative_to(self.wurzel).as_posix()
fort.Lauf.archivziel = archive_target
# A passed test must not be claimed before a current test result exists.
key = "40_Store_Material/Produktdatenblatt_3.21.4.md"
fort.REGELN[key] = tuple(rule for rule in fort.REGELN[key] if "maßgebliche Lauf" not in rule[1] and "auf macOS" not in rule[1]) + (
    (True,
     "Der 3.21-Stand ist lokal geprüft. Der maßgebliche Lauf zu 3.21.2 bestand am 14.09.2026\nauf macOS mit Python 3.14.5 mit Exitcode 0: 25 Suiten, statische Analysen sowie\nBeispiel- und Releaseabgleich. Der Nachweis je Stand steht im QA-Bericht.",
     "Der maßgebliche macOS-Abschlusslauf zu 3.21.4 steht bis zum dokumentierten\nPrüfergebnis aus. Der Nachweis je Stand steht im QA-Bericht."),
)
original_index = fort.index_ergaenzen
extra_rules = json.loads((TEMP / "ergänzungen.json").read_text())
def reviewed_index(run):
    for rel, rules in extra_rules.items():
        body = run.lese(rel)
        for old, new in rules:
            if new in body:
                continue
            if old not in body:
                run.fehler.append("Ergänzung: Pflichtstelle fehlt in " + rel)
                continue
            body = body.replace(old, new, 1)
        run.setze(rel, body)
    original_index(run)
fort.index_ergaenzen = reviewed_index

sys.argv = [str(DEST / "fortschreiben_3214.py"), str(DEST), "--probe"]
assert fort.main() == 0
sys.argv = sys.argv[:-1]
assert fort.main() == 0
print("\nÜbernahme abgeschlossen; Originalwerkzeuge und Originalpaket unverändert archiviert.")
