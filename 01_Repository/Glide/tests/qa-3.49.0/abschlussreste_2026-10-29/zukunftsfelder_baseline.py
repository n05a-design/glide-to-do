"""Lesende WA-09-Gegenprobe ohne Fenster oder echte Nutzerdaten."""
import argparse
import hashlib
import copy
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace

OUT = Path(__file__).resolve().parent
REPO = OUT.parents[2]
parser = argparse.ArgumentParser()
parser.add_argument('--name', required=True)
args = parser.parse_args()
report = OUT/(args.name+'.json')
if report.exists():
    raise FileExistsError('Vorhandenen Beleg erhalten; neuen Namen verwenden.')
folder = Path(tempfile.mkdtemp(prefix='wa09-baseline-', dir=Path.home()/'GlidePruefung'))
os.environ['GLIDE_DATA_DIR'] = str(folder/'daten')
os.environ['GLIDE_TEST_MODE'] = '1'
source = REPO/'src/glide/app.pyw'
sys.path.insert(0, str(source.parent))
loader = importlib.machinery.SourceFileLoader('glide_wa09_baseline', str(source))
mod = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
sys.modules[loader.name] = mod
loader.exec_module(mod)
raw = {'saved_filters': [{'id':'f', 'name':'Test', 'future_condition':{'nested':[1,False]}}],
       'pinboards': {'global': {'future_board':{'nested':[1,False]}, 'cards': [
           {'item_id':'t','list_id':'l','x':17,'future_card':{'nested':[1,False]}},
           {'item_id':'embed:future','list_id':'l','kind':'future','payload':{'text':'bewahren'}}],
           'connections':[]}}}
normalized = mod.ListApp.normalize_personal_settings(copy.deepcopy(raw))
before_prune = copy.deepcopy(normalized)
task = {'id':'t','children':[]}
entry = {'id':'l','items':[task]}
work = object.__new__(mod.ItemWorkspace)
work.app = SimpleNamespace(settings=normalized,lists=[entry],walk_items=lambda values:iter(values),
                           is_heading_item=lambda value:False,get_folder=lambda value:None,
                           save_settings=lambda:True)
work.valid_cards = lambda scope:{'t':(entry,task)}
work.eligible_lists = lambda scope:[entry]
work.prune()
result = {'app_sha256':hashlib.sha256(source.read_bytes()).hexdigest(), 'future_filter_key_retained':'future_condition' in normalized['saved_filters'][0],
          'future_board_key_retained':'future_board' in normalized['pinboards']['global'],
          'future_card_key_retained':'future_card' in normalized['pinboards']['global']['cards'][0],
          'unknown_card_retained_after_prune':any(v['item_id']=='embed:future' for v in normalized['pinboards']['global']['cards']),
          'normalization_mutated_source':raw['pinboards']['global']['future_board']!={'nested':[1,False]},
          'normalized_before_prune':before_prune,'application_window_created':False}
report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k!='normalized_before_prune'},ensure_ascii=False))
