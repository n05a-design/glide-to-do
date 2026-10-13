"""Native Bibliothekspfade eines eigenen Mac-Pakets lesen, keine App ausführen."""
from pathlib import Path
import argparse,json,subprocess
MAGIC={b'\xfe\xed\xfa\xce',b'\xce\xfa\xed\xfe',b'\xfe\xed\xfa\xcf',b'\xcf\xfa\xed\xfe',b'\xca\xfe\xba\xbe',b'\xbe\xba\xfe\xca',b'\xca\xfe\xba\xbf',b'\xbf\xba\xfe\xca'}

def audit(bundle):
    bundle=bundle.resolve();executable=bundle/'Contents/MacOS/Glide';records={};errors=[]
    files=[]
    for p in bundle.rglob('*'):
        if p.is_symlink():
            if not p.resolve().is_relative_to(bundle):errors.append('Symlink verlässt Paket: '+str(p.relative_to(bundle)))
            continue
        if p.is_file():
            with p.open('rb') as f:magic=f.read(4)
            if magic in MAGIC:files.append(p)
    def commands(p):
        result={"rpaths":[],"imports":[],"ids":[]};lines=subprocess.check_output(['otool','-arch','arm64','-l',str(p)],text=True).splitlines()
        for i,line in enumerate(lines):
            if line.strip()=='cmd LC_RPATH':
                result["rpaths"].append(lines[i+2].strip().split(' (offset ',1)[0].removeprefix('path '))
            if line.strip() in ('cmd LC_LOAD_DYLIB','cmd LC_LOAD_WEAK_DYLIB','cmd LC_REEXPORT_DYLIB','cmd LC_LAZY_LOAD_DYLIB','cmd LC_LOAD_UPWARD_DYLIB','cmd LC_ID_DYLIB'):
                name=lines[i+2].strip().split(' (offset ',1)[0].removeprefix('name ')
                result['ids' if line.strip()=='cmd LC_ID_DYLIB' else 'imports'].append(name)
        return result
    def resolve(name,owner):
        return Path(name.replace('@loader_path',str(owner.parent)).replace('@executable_path',str(executable.parent))).resolve()
    exe_paths=commands(executable)["rpaths"]
    for p in sorted(files):
        architectures=subprocess.check_output(['lipo','-archs',str(p)],text=True).strip().split()
        if architectures!=['arm64']:errors.append('Architektur: '+str(p.relative_to(bundle))+' '+repr(architectures))
        loads=commands(p)
        entries=[]
        for name in loads["imports"]:
            if name.startswith(('/usr/lib/','/System/Library/')):
                entries.append(dict(name=name,typ='Systembibliothek'));continue
            if name.startswith('@rpath/'):
                candidates=[resolve(base,p)/name[len('@rpath/'):] for base in loads["rpaths"]]
                candidates += [resolve(base,executable)/name[len('@rpath/'):]for base in exe_paths]
            else:candidates=[resolve(name,p)]
            found=next((q.resolve()for q in candidates if q.is_file() and q.resolve().is_relative_to(bundle)),None)
            if found is None:errors.append(str(p.relative_to(bundle))+': nicht intern auflösbar '+name)
            entries.append(dict(name=name,typ='Paketbibliothek',ziel=str(found.relative_to(bundle))if found else None))
        records[str(p.relative_to(bundle))]=dict(architekturen=architectures,install_names=loads["ids"],imports=entries)
    if not records:errors.append('Keine nativen Binärdateien geprüft')
    return dict(exitcode=int(bool(errors)),binaerdateien=len(records),dateien=records,befunde=errors)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('bundle',type=Path);parser.add_argument('--protokoll',type=Path,required=True);args=parser.parse_args();result=audit(args.bundle);args.protokoll.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(result['binaerdateien'],'native Dateien,',len(result['befunde']),'Befunde');raise SystemExit(result['exitcode'])
