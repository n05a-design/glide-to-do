"""Original-Lizenzen statisch eingebundener Windows-CPython-Bibliotheken."""
import re


def dependency_version(externals, name):
    versions = set(re.findall(re.escape(name) + r'-(\d+\.\d+\.\d+)(?![\d.])', externals))
    if len(versions) != 1:
        raise ValueError('Abhängigkeitsversion im CPython-Bauskript nicht eindeutig: ' + name)
    return versions.pop()


def static_sources(externals, decimal_version, zlib_ng_version):
    """Die Versionsangabe der echten Erweiterung muss dem CPython-Pin entsprechen.

    LICENSE.txt wird von PCbuild/regen.targets zusammengesetzt. Es enthält
    libmpdec und zlib-ng nicht; ein Stichwort dort wäre kein Lizenznachweis.
    """
    records = []
    for component, dependency, actual, filename, output in (
            ('libmpdec', 'mpdecimal', decimal_version, 'COPYRIGHT.txt', 'libmpdec-COPYRIGHT.txt'),
            ('zlib-ng', 'zlib-ng', zlib_ng_version, 'LICENSE.md', 'zlib-ng-LICENSE.md')):
        version = dependency_version(externals, dependency)
        if actual != version:
            raise ValueError('Native Bibliothek weicht vom CPython-Quellpin ab: ' + component)
        tag = dependency + '-' + version
        source = 'https://github.com/python/cpython-source-deps/tree/' + tag
        records.append(dict(name=component, version=version, source=source, file=output,
                            url='https://raw.githubusercontent.com/python/cpython-source-deps/' + tag + '/' + filename))
    return records


def toolkit_references(tcl, tk_compiled, *, pins=None):
    """Eigene 9.1-Quellen über exakte Pins, installierte 9.0 über ihren Tag."""
    if re.fullmatch(r'9\.0\.\d+', tcl) and tk_compiled == '9.0' and pins is None:
        refs = dict(tcl='core-'+tcl.replace('.', '-'), tk='core-'+tcl.replace('.', '-'))
    elif tcl == '9.1.0' and tk_compiled == '9.1' and pins is not None:
        if any(re.fullmatch('[0-9a-f]{40}', pins.get(name, '')) is None for name in ('tcl', 'tk')):
            raise ValueError('Eigene Tcl/Tk-Lizenzbelege brauchen die verifizierten Originalpins.')
        refs = {name:pins[name] for name in ('tcl', 'tk')}
    else:
        raise ValueError('Tcl/Tk-Version und Lizenzherkunft passen nicht zusammen.')
    return {name:dict(raw='https://raw.githubusercontent.com/tcltk/'+name+'/'+ref,
                      source='https://github.com/tcltk/'+name+'/tree/'+ref)
            for name, ref in refs.items()}


def utf8proc_version(header):
    parts = []
    for name in ('MAJOR', 'MINOR', 'PATCH'):
        values = re.findall(r'^#define UTF8PROC_VERSION_'+name+r' (\d+)\s*$', header, re.MULTILINE)
        if len(values) != 1:
            raise ValueError('utf8proc-Version aus dem gepinnten Originalheader nicht eindeutig.')
        parts.append(values[0])
    return '.'.join(parts)
