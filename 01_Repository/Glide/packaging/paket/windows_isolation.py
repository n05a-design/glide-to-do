"""Grenzen einer Laufzeitsperre ausschließlich im vergänglichen Hosted-CI-Runner."""
import errno
from pathlib import PureWindowsPath


def access_denied(error):
    # FileIO meldet Windows-Zugriffsfehler über die C-Runtime als EACCES;
    # CreateProcess liefert dagegen den ursprünglichen WinError 5.
    return (getattr(error, 'winerror', None) == 5 or
            isinstance(error, PermissionError) and error.errno == errno.EACCES)


def acl_snapshot(raw):
    """icacls-/save-DACLs unabhängig von der Verzeichnisreihenfolge vergleichen."""
    lines = raw.decode('utf-16').splitlines()
    if not lines or len(lines) % 2:
        raise ValueError('Unvollständige icacls-ACL-Sicherung.')
    result = {}
    for name, dacl in zip(lines[::2], lines[1::2]):
        if not name or not dacl.startswith('D:') or name in result:
            raise ValueError('Ungültige oder doppelte icacls-ACL-Sicherung.')
        result[name] = dacl
    return result


def normalize_environment(environment):
    # os.environ ist unter Windows schreibungsunabhängig. Ein dict daraus
    # enthält dagegen SYSTEMROOT und verliert diese Nachschlage-Eigenschaft.
    result = {}
    for key, value in environment.items():
        name = key.upper()
        if name in result and result[name] != value:
            raise ValueError('Widersprüchliche Schreibvarianten der Windows-Umgebung.')
        result[name] = value
    return result


def absolute(value):
    path = PureWindowsPath(value)
    if not path.is_absolute() or not path.drive.endswith(':') or '..' in path.parts:
        raise ValueError('Eindeutiger lokaler absoluter Windows-Pfad erforderlich.')
    return path


def restoration_entries(source, snapshot):
    root = absolute(source)
    entries = []
    for name, dacl in snapshot.items():
        relative = PureWindowsPath(name)
        path = root.parent / relative
        if (relative.is_absolute() or relative.drive or '..' in relative.parts or
                not path.is_relative_to(root) or not dacl.startswith('D:')):
            raise ValueError('ACL-Restaurierung verlässt die gesicherte CI-Quelle.')
        entries.append((str(path), dacl))
    if not entries or not any(PureWindowsPath(path) == root for path, _ in entries):
        raise ValueError('Original-ACL des gesicherten Wurzelordners fehlt.')
    return sorted(entries, key=lambda entry: (len(PureWindowsPath(entry[0]).parts), entry[0].casefold()))


def plan(environment, package, report, forbidden):
    environment = normalize_environment(environment)
    required = {'GITHUB_ACTIONS':'true', 'CI':'true', 'RUNNER_ENVIRONMENT':'github-hosted', 'RUNNER_OS':'Windows'}
    if any(environment.get(key) != value for key,value in required.items()):
        raise ValueError('Laufzeitsperre ausschließlich im vergänglichen GitHub-Hosted-Windows-Prüfstand.')
    roots = {key:absolute(environment.get(key,'')) for key in
             ('RUNNER_TEMP','RUNNER_TOOL_CACHE','GITHUB_WORKSPACE','SYSTEMROOT')}
    package, report = absolute(package), absolute(report)
    if not package.is_relative_to(roots['RUNNER_TEMP']) or not report.is_relative_to(roots['RUNNER_TEMP']):
        raise ValueError('Paket und Bericht müssen im temporären CI-Prüfbereich liegen.')
    if report.is_relative_to(package) or package == roots['RUNNER_TEMP']:
        raise ValueError('Prüfbericht muss außerhalb des Paketverzeichnisses liegen.')
    values = set()
    for value in forbidden:
        path = absolute(value)
        python_cache = roots['RUNNER_TOOL_CACHE']/'Python'
        owned = path.is_relative_to(python_cache) or path.is_relative_to(roots['GITHUB_WORKSPACE']) or path.is_relative_to(roots['RUNNER_TEMP'])
        if not owned or path in (roots['RUNNER_TEMP'],roots['RUNNER_TOOL_CACHE']):
            raise ValueError('Sperre darf ausschließlich CI-Python, Projektquelle oder eigene temporäre Bauquellen betreffen.')
        if any(path.is_relative_to(p) or p.is_relative_to(path) for p in (package,report,roots['SYSTEMROOT'])):
            raise ValueError('Sperre darf Paket, Bericht und Windows-Systemverzeichnis nicht überdecken.')
        values.add(path)
    if not values:
        raise ValueError('Ausdrücklich benannte externe Laufzeit erforderlich.')
    values = sorted((path for path in values if not any(path != other and path.is_relative_to(other)
                     for other in values)),key=str)
    return {'package':str(package),'report':str(report),'forbidden':[str(path)for path in values]}
