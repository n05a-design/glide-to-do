"""Offizielle gepinnte Runtimequellen nur im vergänglichen CI-Prüfstand holen."""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sysconfig

from runtime_contract import PINS, python_pin


def prepare(destination):
    temporary = Path(os.environ['RUNNER_TEMP']).resolve()
    destination = destination.resolve()
    if (os.environ.get('GITHUB_ACTIONS') != 'true' or
            os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted' or
            destination == temporary or not destination.is_relative_to(temporary)):
        raise ValueError('Quellenabruf ausschließlich im eigenen Hosted-CI-Ziel unter RUNNER_TEMP.')
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError('Für den Quellenabruf ein neues leeres Ziel verwenden.')
    header = Path(sysconfig.get_path('include')) / 'patchlevel.h'
    pins = dict(PINS, python=python_pin(platform.python_version(), header.read_text(encoding='utf-8'),
                free_threaded=bool(sysconfig.get_config_var('Py_GIL_DISABLED')),
                debug=bool(sysconfig.get_config_var('Py_DEBUG'))))
    repositories = dict(tcl='tcltk/tcl', tk='tcltk/tk', python='python/cpython')
    for kind, repository in repositories.items():
        target = destination / kind
        target.mkdir()
        for command in (
                ['git', 'init', '-q'],
                ['git', 'fetch', '--depth=1', 'https://github.com/'+repository+'.git', pins[kind]],
                ['git', 'checkout', '--detach', 'FETCH_HEAD']):
            subprocess.run(command, cwd=target, check=True)
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=target, text=True).strip()
        if actual != pins[kind]:
            raise ValueError('Quellenabruf hat nicht den Originalpin geliefert.')
    (destination / 'quellpins.json').write_text(json.dumps(pins, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ziel', type=Path, required=True)
    prepare(parser.parse_args().ziel)
