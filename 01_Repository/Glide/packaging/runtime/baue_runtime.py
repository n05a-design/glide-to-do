"""Native Tcl/Tk-9.1-Runtime und passende CPython-Erweiterung im eigenen Ziel.

Benötigt lokale, unveränderte Git-Quellen an den festgelegten Pins sowie den
nativen Compiler. Unter Windows aus einer x64-VS-Entwicklungsumgebung starten;
unter Linux sind ATK und Atk-bridge als Bauvoraussetzungen verpflichtend.
Kein Download, kein Administratorrecht und keine Systeminstallation.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import sysconfig
import tarfile

from runtime_contract import PINS, build_destination, extension_command, python_pin, require_atk
from runtime_patches import apply_patches


def execute(command, *, cwd, environment, log):
    with log.open('w', encoding='utf-8') as stream:
        result = subprocess.run([str(arg) for arg in command], cwd=cwd, env=environment,
                                stdout=stream, stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'{log.stem} fehlgeschlagen; siehe {log.name}.')
    print(log.stem + ': grün', flush=True)


def source_copy(source, pin, destination):
    source = source.resolve()
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=source, text=True).strip()
    if actual != pin or subprocess.check_output(['git', 'status', '--porcelain', '--untracked-files=all'],
                                               cwd=source, text=True):
        raise ValueError('Unveränderte gepinnte Git-Quelle erforderlich: ' + source.name)
    archive = destination.with_suffix('.tar')
    subprocess.run(['git', 'archive', '--format=tar', '--output', str(archive), pin], cwd=source, check=True)
    destination.mkdir()
    try:
        with tarfile.open(archive) as content:
            content.extractall(destination, filter='data')
    finally:
        archive.unlink()


def build(tcl_source, tk_source, python_source, destination):
    include = Path(sysconfig.get_path('include'))
    version = platform.python_version()
    python_commit = python_pin(version, (include / 'patchlevel.h').read_text(encoding='utf-8'),
                               free_threaded=bool(sysconfig.get_config_var('Py_GIL_DISABLED')),
                               debug=bool(sysconfig.get_config_var('Py_DEBUG')))
    machine = platform.machine().lower()
    machine = 'x86_64' if machine in ('amd64', 'x64') else machine
    system = sys.platform
    if (system, machine) not in (('darwin', 'arm64'), ('linux', 'x86_64'), ('win32', 'x86_64')):
        raise ValueError('Nur native macOS-arm64-, Linux-x64- und Windows-x64-Bauten sind geprüft.')
    destination = build_destination(destination, (tcl_source, tk_source, python_source))
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Für jeden Runtime-Bau ein leeres Ziel verwenden.')
    sources = destination / 'quellen'
    sources.mkdir()
    for kind, source, pin in (('tcl', tcl_source, PINS['tcl']), ('tk', tk_source, PINS['tk']),
                              ('python', python_source, python_commit)):
        source_copy(source, pin, sources / kind)
    if (sources / 'python/Include/patchlevel.h').read_bytes() != (include / 'patchlevel.h').read_bytes():
        raise ValueError('Installierter Python-Header weicht vom gepinnten Original ab.')
    patches = apply_patches(sources / 'tk', system)
    prefix = destination / 'runtime'
    build_root = destination / 'bau'
    extension = destination / 'python-extension'
    logs = destination / 'protokolle'
    for path in (prefix, build_root, extension, logs):
        path.mkdir()
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONUTF8='1')
    # Fremde Library-Overrides dürfen keine eigene Runtime vortäuschen.
    for key in ('TCL_LIBRARY', 'TK_LIBRARY', 'TCLLIBPATH', 'PYTHONPATH'):
        environment.pop(key, None)
    if system == 'darwin':
        environment.update(CFLAGS='-O2 -arch arm64', MACOSX_DEPLOYMENT_TARGET='11.0')
    if system == 'linux':
        execute(['pkg-config', '--exists', 'atk', 'atk-bridge-2.0'], cwd=build_root,
                environment=environment, log=logs / 'atk-voraussetzung.log')
    for kind in ('tcl', 'tk'):
        if system == 'win32':
            directory = sources / kind / 'win'
            common = ['nmake', '-nologo', '-f', 'makefile.vc', 'OPTS=msvcrt', f'INSTALLDIR={prefix}']
            if kind == 'tk':
                common.append(f'TCLDIR={sources / "tcl"}')
            execute([*common, 'release'], cwd=directory, environment=environment, log=logs / (kind+'-make.log'))
            execute([*common, 'install'], cwd=directory, environment=environment, log=logs / (kind+'-install.log'))
        else:
            directory = build_root / kind
            directory.mkdir()
            configure = [sources / kind / 'unix/configure', f'--prefix={prefix}', '--enable-shared']
            if system == 'darwin':
                configure.append('--disable-framework')
            if kind == 'tk':
                configure.append(f'--with-tcl={build_root / "tcl"}')
                if system == 'darwin':
                    configure.append('--enable-aqua=yes')
            execute(configure, cwd=directory, environment=environment, log=logs / (kind+'-configure.log'))
            if system == 'linux' and kind == 'tk':
                require_atk((directory / 'Makefile').read_text(encoding='utf-8'))
            execute(['make', '-j2'], cwd=directory, environment=environment, log=logs / (kind+'-make.log'))
            execute(['make', 'install'], cwd=directory, environment=environment, log=logs / (kind+'-install.log'))
    target = extension / ('_tkinter' + sysconfig.get_config_var('EXT_SUFFIX'))
    python_library = Path(sys.base_prefix) / 'libs/python314.lib' if system == 'win32' else None
    command = extension_command(system, machine, include=include, prefix=prefix,
                                modules=sources / 'python/Modules', output=target, python_library=python_library)
    execute(command, cwd=extension, environment=environment, log=logs / 'tkinter-extension.log')
    if system == 'win32':
        # Python lädt abhängige DLLs aus dem pyd-Ordner; PATH genügt seit 3.8 nicht.
        for name in ('tcl91.dll', 'tcl9tk91.dll'):
            shutil.copy2(prefix / 'bin' / name, extension / name)
    probe_environment = dict(environment, PYTHONPATH=str(extension))
    code = ('import _tkinter,tkinter,json; t=tkinter.Tcl(); print(json.dumps(dict('
            'extension=_tkinter.__file__,tcl=t.eval("info patchlevel"),'
            'tcl_library=t.eval("info library"),tk_compiled=_tkinter.TK_VERSION)))')
    result = json.loads(subprocess.check_output([sys.executable, '-B', '-c', code], env=probe_environment, text=True))
    if (Path(result['extension']).resolve() != target.resolve() or result['tcl'] != '9.1.0'
            or result['tk_compiled'] != '9.1'):
        raise ValueError('Probe hat die falsche _tkinter-/Tcl-/Tk-Laufzeit geladen.')
    files = {path.relative_to(destination).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
             for folder in (prefix, extension) for path in folder.rglob('*') if path.is_file()}
    proof = dict(python=version, platform=system, machine=machine, quellpins={**PINS, 'python': python_commit},
                 runtime_patches=patches,
                 runtime=str(prefix), extension=str(target), sha256=files, tcl_probe=result,
                 native_backend='ATK/AT-SPI' if system == 'linux' else 'Aqua' if system == 'darwin' else 'MSAA',
                 gui_reader_abnahme='offen; Tcl-Konsole ersetzt keine GUI-/Readerprobe')
    (destination / 'runtime-bau.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    print('Eigene Laufzeit gebaut; native GUI-/Readerprobe bleibt offen.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for kind in ('tcl', 'tk', 'python'):
        parser.add_argument('--'+kind+'-quelle', type=Path, required=True)
    parser.add_argument('--ziel', type=Path, required=True)
    args = parser.parse_args()
    build(args.tcl_quelle, args.tk_quelle, args.python_quelle, args.ziel)


if __name__ == '__main__':
    main()
