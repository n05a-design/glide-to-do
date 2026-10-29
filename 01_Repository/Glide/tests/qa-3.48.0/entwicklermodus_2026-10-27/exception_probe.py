"""Gezielte Ausnahmeaufnahme: Builtinbindung und Bytecode am Serien-Generator."""
import builtins
import dis
import hashlib
import json
from pathlib import Path
import runpy
import sys
import types

HERE=Path(__file__).resolve().parent
QA=HERE.parent
FROZEN=Path((QA/'dreierpaket_2026-10-27/freeze_ort.log').read_text(encoding='utf-8').strip())
REPO=FROZEN/'01_Repository/Glide'
script=QA/'wa41_2026-10-27/probe.py'
original={name:getattr(builtins,name) for name in ('isinstance','dict','list')}
target=HERE/'exception_context.json'
result=dict(python=sys.version,dev_mode=sys.flags.dev_mode,completed=False,exception=None,frames=[])


def save():
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def instructions(code,adaptive):
    return [dict(offset=i.offset,operation=i.opname,argument=i.argrepr)
        for i in dis.get_instructions(code,adaptive=adaptive,show_caches=True)]


save()
sys.argv=[str(script),'--repo',str(REPO),'--output',str(HERE/'315_dev_capture.trace.log'),'--variant','normal']
sys.path[0]=str(script.parent)
try:
    runpy.run_path(str(script),run_name='__main__')
except BaseException as error:
    result['exception']=dict(type=type(error).__name__,message=str(error))
    tb=error.__traceback__
    while tb:
        frame=tb.tb_frame
        code=frame.f_code
        row=dict(file=Path(code.co_filename).name,function=code.co_name,line=tb.tb_lineno,last_instruction=tb.tb_lasti)
        result['frames'].append(row)
        save()
        if Path(code.co_filename).name=='repeat_rules.py':
            row['bindings']={name:dict(global_present=name in frame.f_globals,
                resolved_is_original=frame.f_globals.get(name,frame.f_builtins.get(name)) is reference,
                builtin_is_original=frame.f_builtins.get(name) is reference,
                builtin_type=type(frame.f_builtins.get(name)).__name__)
                for name,reference in original.items()}
            row['local_types']={name:type(value).__name__ for name,value in frame.f_locals.items()}
            row['co_code_sha256']=hashlib.sha256(code.co_code).hexdigest()
            save()
            if code.co_name=='<genexpr>':
                for adaptive in (False,True):
                    try:
                        row['adaptive' if adaptive else 'normal']=instructions(code,adaptive)
                    except BaseException as diagnostic_error:
                        row['disassembly_error']=type(diagnostic_error).__name__+': '+str(diagnostic_error)
                    save()
                # Nur kompilieren, keine Modulausfuehrung.
                fresh=compile(Path(code.co_filename).read_bytes(),code.co_filename,'exec')
                pending=[fresh]
                while pending:
                    candidate=pending.pop()
                    if candidate.co_qualname==code.co_qualname and candidate.co_firstlineno==code.co_firstlineno:
                        row['matches_fresh_source']=candidate.co_code==code.co_code
                        break
                    pending.extend(value for value in candidate.co_consts if type(value) is types.CodeType)
                save()
        tb=tb.tb_next
    result['completed']=True
    save()
    raise
else:
    result.update(completed=True,passed=True)
    save()
