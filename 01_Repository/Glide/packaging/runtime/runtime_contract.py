"""Feste Quellen und ABI-Verträge der eigenen Tcl/Tk-9.1-Laufzeit."""
from pathlib import Path
import re


PINS = {
    'tcl': '0c6bad08d91fa2ad51f05a50a41f8c1ea82ce985',
    'tk': '3f45110c0a568b70f2ebd5412f215e87d199bc7d',
}
PYTHON_PINS = {
    '3.14.5': '5607950ef232dad16d75c0cf53101d9649d89115',
    '3.14.7': '823f0323ee6ec1402088b73bce1a38473cac36dc',
    '3.14.8': '8e6e75d9102e39bed2a2b279203a396741180f12',
}


def export_identity(header, pin):
    if header != b'git-' or pin not in PINS.values():
        raise ValueError('Buildkennung benötigt den Originalpräfix und einen verifizierten Tcl-/Tk-Pin.')
    return header + pin.encode('ascii') + b'\n'


def python_pin(version, header, *, free_threaded=False, debug=False):
    if free_threaded or debug:
        raise ValueError('Nur die reguläre CPython-3.14-Release-ABI ist geprüft.')
    match = re.search(r'^#define\s+PY_VERSION\s+"([^" ]+)"', header, re.M)
    if version not in PYTHON_PINS or match is None or match[1] != version:
        raise ValueError('Python-Laufzeit, installierte Header und Quellpin müssen dieselbe Patchversion tragen.')
    return PYTHON_PINS[version]


def build_destination(destination, sources):
    destination = Path(destination).resolve()
    if any('onedrive' in part.casefold() for part in destination.parts):
        raise ValueError('Runtime-Bau muss außerhalb OneDrive liegen.')
    for source in sources:
        source = Path(source).resolve()
        if destination == source or destination.is_relative_to(source) or source.is_relative_to(destination):
            raise ValueError('Bauziel und Eingabequellen müssen getrennt sein.')
    return destination


def require_atk(makefile):
    # configure ermittelt ATK automatisch. Ein erfolgreiches Tk ohne ATK
    # enthält nur gleichnamige Accessibility-Stubs und ist hier unzulässig.
    if not re.search(r'(?:^|\s)-DHAVE_ATK=1(?:\s|$)', makefile):
        raise ValueError('Linux-Tk wurde ohne echtes ATK-/AT-SPI-Backend konfiguriert.')


def extension_command(system, machine, *, include, prefix, modules, output, python_library=None):
    include, prefix, modules, output = map(Path, (include, prefix, modules, output))
    includes = [include, include / 'internal', prefix / 'include', modules]
    if system == 'win32' and machine == 'x86_64' and python_library is not None:
        return ['cl', '/nologo', '/LD', '/MD', '/O2', '/DTCL_WITH_EXTERNAL_TOMMATH'] + [f'/I{path}' for path in includes] + [
            str(modules / '_tkinter.c'), f'/Fo{output.with_suffix(".obj")}', '/link',
            f'/OUT:{output}', '/MACHINE:X64', str(python_library),
            str(prefix / 'lib/tcl91.lib'), str(prefix / 'lib/tcl9tk91.lib'), str(prefix / 'lib/tommath.lib')]
    if system == 'darwin' and machine == 'arm64':
        flags = ['-bundle', '-undefined', 'dynamic_lookup', '-arch', 'arm64']
        libraries = ['libtcl9tk9.1.dylib', 'libtcl9.1.dylib']
    elif system == 'linux' and machine == 'x86_64':
        flags = ['-shared', '-fPIC']
        libraries = ['libtcl9tk9.1.so', 'libtcl9.1.so']
    else:
        raise ValueError('Nicht geprüfte native Zielplattform oder Python-Importbibliothek fehlt.')
    return ['cc', *flags, '-O2', *[f'-I{path}' for path in includes], str(modules / '_tkinter.c'),
            *[str(prefix / 'lib' / name) for name in libraries],
            f'-Wl,-rpath,{prefix / "lib"}', '-o', str(output)]
