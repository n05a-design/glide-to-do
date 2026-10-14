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
