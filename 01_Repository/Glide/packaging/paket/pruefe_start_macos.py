"""Native Paketprobe mit ausschließlich im Kindprozess gesperrtem externem Python."""
import argparse
import json
from pathlib import Path
import subprocess
import sys


def quoted_path(path):
    value = str(Path(path).resolve())
    if any(ord(char) < 32 for char in value):
        raise ValueError('Unzulässiger Pfad in der lokalen Sandboxregel.')
    return '"'+value.replace('\\', '\\\\').replace('"', '\\"')+'"'


def profile_for(package, forbidden):
    package = Path(package).resolve()
    paths = sorted({Path(value).resolve() for value in forbidden}, key=str)
    if not paths or any(package.is_relative_to(p) or p.is_relative_to(package) for p in paths):
        raise ValueError('Die Laufzeitsperre darf das Paket nicht überdecken.')
    return '(version 1)\n(allow default)\n'+''.join(
        '(deny file-read* (subpath '+quoted_path(p)+'))\n' for p in paths)


def run(package, report, forbidden, *, timeout=120):
    if sys.platform != 'darwin':
        raise RuntimeError('Diese tatsächliche Prozesssperre ist ausschließlich für macOS.')
    package = Path(package).resolve()
    executable = package/'Contents/MacOS/Glide'
    if not executable.is_file():
        raise ValueError('Gebautes eigenständiges Glide.app fehlt.')
    report = Path(report).resolve()
    if report.exists():
        raise ValueError('Neue Probe braucht einen eigenen noch nicht vorhandenen Bericht.')
    profile = profile_for(package, forbidden)
    prefix = ['/usr/bin/sandbox-exec', '-p', profile]
    allowed = subprocess.run(prefix+['/usr/bin/true'], capture_output=True, text=True, timeout=15)
    if allowed.returncode:
        raise RuntimeError('Lokale Prozess-Sandbox nicht verfügbar: '+allowed.stderr)
    blocked = subprocess.run(prefix+[sys.executable, '-B', '-c', 'raise SystemExit(0)'],
                             capture_output=True, text=True, timeout=15)
    if blocked.returncode == 0:
        raise RuntimeError('Gegenprobe rot erforderlich: das externe Prüf-Python blieb ausführbar.')
    report.parent.mkdir(parents=True, exist_ok=True)
    smoke = report.with_name(report.stem+'-paket.json')
    if smoke.exists():
        raise ValueError('Unverbrauchter Paketbericht erforderlich.')
    # Arbeitsverzeichnis neben dem Paket: Der Aufrufer darf in einer gesperrten
    # Quelle stehen; Tcl liest beim Start das Arbeitsverzeichnis.
    launched = subprocess.run(prefix+[str(executable), '--paket-pruefen', str(smoke)],
                              capture_output=True, text=True, timeout=timeout, cwd=str(package.parent))
    result = {'plattform': 'macOS arm64', 'nur_kindprozess_gesperrt': True,
              'system_installationen_unveraendert': True,
              'sandbox_positive_kontrolle_exitcode': allowed.returncode,
              'externes_python_gegenprobe_exitcode': blocked.returncode,
              'paketprozess_exitcode': launched.returncode,
              'ausgabe': launched.stdout+launched.stderr,
              'gesperrte_orte': ['externe Python-Laufzeit/Bauumgebung/Projektquelle; nur lokale Prozessregel'],
              'exitcode': 1}
    if smoke.exists():
        result['paket'] = json.loads(smoke.read_text())
        if launched.returncode == 0 and result['paket'].get('exitcode') == 0:
            result['exitcode'] = 0
    else:
        result['fehler'] = 'Paketprozess hat keinen eigenen Prüfbericht geschrieben.'
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print('Isolierte Paketprobe Exit', result['exitcode'], '; externes Python blockiert, Installationen unverändert.')
    return result['exitcode']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--paket', type=Path, required=True)
    parser.add_argument('--bericht', type=Path, required=True)
    parser.add_argument('--sperren', type=Path, action='append', required=True)
    args = parser.parse_args()
    raise SystemExit(run(args.paket, args.bericht, args.sperren))
