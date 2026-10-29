"""Unveraendertes Pruefskript mit protokolliertem Interpreter-/Debuggerzustand."""
import argparse
import faulthandler
import json
import os
from pathlib import Path
import runpy
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--metadata',type=Path,required=True)
parser.add_argument('--script',type=Path,required=True)
args,remaining=parser.parse_known_args()


def context():
    return dict(python=sys.version,dev_mode=sys.flags.dev_mode,
        faulthandler=faulthandler.is_enabled(),xoptions=sys._xoptions,
        trace_hook=None if sys.gettrace() is None else type(sys.gettrace()).__name__,
        profile_hook=None if sys.getprofile() is None else type(sys.getprofile()).__name__,
        monitoring_tools={str(i):sys.monitoring.get_tool(i) for i in range(6)},
        debugger_modules=[name for name in sys.modules if name.startswith(('pydevd','_pydevd','debugpy'))],
        debugger_environment_names=[name for name in os.environ if name.startswith(('PYDEVD','DEBUGPY'))],
        malloc_override=os.environ.get('PYTHONMALLOC'))


metadata=dict(before=context(),completed=False)
args.metadata.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
sys.argv=[str(args.script),*remaining]
sys.path[0]=str(args.script.parent)
try:
    runpy.run_path(str(args.script),run_name='__main__')
finally:
    # Ein nativer Abbruch erreicht diesen Block nicht.
    metadata.update(after=context(),completed=True)
    args.metadata.write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
