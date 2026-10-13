"""Eingefrorenen Bytecode auf denselben Programmstand wie seine Quellen prüfen."""
import hashlib
import marshal
from pathlib import Path
from types import CodeType


def compare(sources, read_code):
    """Nur kompilieren und vergleichen, keinen Anwendungscode ausführen.

    Codeobjekt-Gleichheit schließt verschachtelte Funktionen ein. Baupfade in
    co_filename dürfen sich unterscheiden; Assertions/Optimierung und alle
    ausführbaren Konstanten müssen gleich bleiben.
    """
    records={}
    failures=[]
    for name,raw in sources.items():
        try:
            actual=read_code(name)
            expected=compile(raw,name+'.py','exec',dont_inherit=True,optimize=0)
            if not isinstance(actual,CodeType)or actual!=expected:
                failures.append(name)
            records[name]=hashlib.sha256(raw).hexdigest()
        except (KeyError,ValueError,TypeError,SyntaxError):
            failures.append(name)
    if failures:
        raise ValueError('Gepackter Code unterscheidet sich: '+', '.join(sorted(set(failures))))
    return records


def inspect_archive(executable, sources, *, entry=None):
    # Die Abhängigkeit bleibt beim Bauwerkzeug; weder App noch Unit-Tests
    # importieren PyInstaller.
    from PyInstaller.archive.readers import CArchiveReader
    archive=CArchiveReader(str(executable))
    embedded=[name for name,record in archive.toc.items()if record[-1]=='z']
    if len(embedded)!=1:
        raise ValueError('Kein eindeutiges Python-Modularchiv im Paket.')
    pyz=archive.open_embedded_archive(embedded[0])
    result=compare(sources,pyz.extract)
    if entry is not None:
        name,raw=entry
        compare({name:raw},lambda n:marshal.loads(archive.extract(n)))
    return result
