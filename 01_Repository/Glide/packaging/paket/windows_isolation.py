"""Grenzen einer Laufzeitsperre ausschließlich im vergänglichen Hosted-CI-Runner."""
from pathlib import PureWindowsPath


def absolute(value):
    path = PureWindowsPath(value)
    if not path.is_absolute() or not path.drive.endswith(':') or '..' in path.parts:
        raise ValueError('Eindeutiger lokaler absoluter Windows-Pfad erforderlich.')
    return path


def plan(environment, package, report, forbidden):
    required = {'GITHUB_ACTIONS':'true', 'CI':'true', 'RUNNER_ENVIRONMENT':'github-hosted', 'RUNNER_OS':'Windows'}
    if any(environment.get(key) != value for key,value in required.items()):
        raise ValueError('Laufzeitsperre ausschließlich im vergänglichen GitHub-Hosted-Windows-Prüfstand.')
    roots = {key:absolute(environment.get(key,'')) for key in
             ('RUNNER_TEMP','RUNNER_TOOL_CACHE','GITHUB_WORKSPACE','SystemRoot')}
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
        if any(path.is_relative_to(p) or p.is_relative_to(path) for p in (package,report,roots['SystemRoot'])):
            raise ValueError('Sperre darf Paket, Bericht und Windows-Systemverzeichnis nicht überdecken.')
        values.add(path)
    if not values:
        raise ValueError('Ausdrücklich benannte externe Laufzeit erforderlich.')
    values = sorted((path for path in values if not any(path != other and path.is_relative_to(other)
                     for other in values)),key=str)
    return {'package':str(package),'report':str(report),'forbidden':[str(path)for path in values]}
