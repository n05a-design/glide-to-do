"""Rest des unterbrochenen Volllaufs; ursprünglicher Lauf bleibt unvollständig."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO/'tests/tools'))
frozen = json.loads((HERE/'vollpruefung_quellstand.json').read_text(encoding='utf-8'))
for folder, manifest in ((REPO/'src/glide', frozen['source_manifest']), (REPO, frozen['test_manifest'])):
    for name, expected in manifest.items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == expected, name
spec = importlib.util.spec_from_file_location('glide_full_resume', REPO/'tests/tools/pruefen.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
module.SUITEN = module.SUITEN[module.SUITEN.index('test_erwaehnungen.py'):]
(HERE/'vollpruefung_unterbrochen.json').write_text(json.dumps({
    'status':'unvollständig', 'prozess_exitcode':1073807364,
    'abschlussbericht_vorhanden':False,
    'letzte_bestaetigte_suite':'test_bildkonversion',
    'abbruch_waehrend':'test_erwaehnungen',
    'fortsetzung_ab':'test_erwaehnungen', 'rest_suiten':list(module.SUITEN),
    'hinweis':'Ursache des Prozess-/Werkzeugabbruchs nicht belegt; kein grüner Gesamtvolllauf.'
}, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
sys.argv = [str(REPO/'tests/tools/pruefen.py'), '--modus','voll','--protokoll',str(HERE/'windows_restlauf')]
raise SystemExit(module.main())
