"""Originalbelege aus exakt gepinnten Tcl/Tk-9.1-Quellen vorbereiten; kein Runtimebau."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

from runtime_contract import PINS


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def comment(path, markers):
    data = path.read_bytes().split(b'*/', 1)[0] + b'*/\n'
    if not all(marker in data for marker in markers):
        raise ValueError('Originaler Lizenzkommentar fehlt: ' + path.name)
    return data


def prepare(basis, sources, destination):
    document = json.loads((basis / 'manifest.json').read_text())
    assert document['runtime']['tcl'] == '9.0.3'
    assert document['runtime']['python'] == '3.14.5'
    for record in document['components']:
        for name, digest in record['files'].items():
            assert Path(name).name == name and not (basis/name).is_symlink()
            assert sha(basis/name) == digest, name
    directories = {}
    for name, pin in PINS.items():
        path = sources/(name+'-9.1.0')
        assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path, text=True).strip() == pin
        assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=path, text=True)
        directories[name] = path
    assert not destination.exists()
    shutil.copytree(basis, destination)
    replacements = {
        'Tcl': ('tcl', {'Tcl-LICENSE.txt': (directories['tcl']/'license.terms').read_bytes()}),
        'Tk': ('tk', {'Tk-LICENSE.txt': (directories['tk']/'license.terms').read_bytes()}),
        'libtommath': ('tcl', {'libtommath-LICENSE.txt': (directories['tcl']/'libtommath/LICENSE').read_bytes()}),
        'Henry-Spencer-Regex': ('tcl', {'Henry-Spencer-Regex-LICENSE.txt': comment(
            directories['tcl']/'generic/regcustom.h', (b'Henry Spencer', b'Redistribution'))}),
        'NanoSVG': ('tk', {name+'-LICENSE.txt': comment(directories['tk']/'generic'/name,
                                                     (b'Copyright', b'redistribute'))
                          for name in ('nanosvg.h', 'nanosvgrast.h')}),
    }
    for record in document['components']:
        if record['name'] not in replacements:
            continue
        provider, files = replacements[record['name']]
        record.update(version='9.1.0' if record['name'] in ('Tcl', 'Tk') else 'aus '+provider.title()+' 9.1.0 '+PINS[provider],
                      source='https://github.com/tcltk/'+provider+'/tree/'+PINS[provider])
        for name, data in files.items():
            assert data.strip()
            (destination/name).write_bytes(data)
        record['files'] = {name: sha(destination/name) for name in files}
    utf8 = directories['tcl']/'utf8proc'
    header = (utf8/'utf8proc.h').read_text()
    for part, value in (('MAJOR', 2), ('MINOR', 12), ('PATCH', 0)):
        assert f'#define UTF8PROC_VERSION_{part} {value}' in header
    shutil.copy2(utf8/'LICENSE.md', destination/'utf8proc-LICENSE.txt')
    document['components'].append(dict(name='utf8proc', version='2.12.0 aus Tcl 9.1.0 '+PINS['tcl'],
        source='https://github.com/tcltk/tcl/tree/'+PINS['tcl']+'/utf8proc',
        files={'utf8proc-LICENSE.txt': sha(destination/'utf8proc-LICENSE.txt')}))
    document['runtime'].update(tcl='9.1.0', tk_compiled='9.1')
    document.update(quellpins=PINS, abnahme='Neue Originalbelege aus geprüften Git-Pins; tatsächlicher Runtime-/Paketabgleich noch offen.')
    (destination/'manifest.json').write_text(json.dumps(document, ensure_ascii=False, indent=2)+'\n')
    print(len(document['components']), 'Komponenten mit neuen Tcl/Tk-9.1-Originalbelegen vorbereitet; native Abnahme offen.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('basis', 'quellen', 'ziel'):
        parser.add_argument('--'+name, type=Path, required=True)
    args=parser.parse_args()
    prepare(args.basis.resolve(), args.quellen.resolve(), args.ziel.resolve())
