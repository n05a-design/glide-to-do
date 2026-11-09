# SPDX-License-Identifier: MPL-2.0
"""Bau-Pins erhalten und SHA-256 der nicht zurückgezogenen PyPI-Dateien erneuern."""
import json
from pathlib import Path
import re
import ssl
import urllib.request


def main():
    root = Path(__file__).resolve().parents[2]
    context = ssl.create_default_context()
    for path in sorted((root / 'requirements').glob('build-*.txt')):
        pins = re.findall(r'^([A-Za-z0-9_.-]+)==([^\s]+)', path.read_text(), re.M)
        if not pins:
            raise ValueError('Keine festen Bauversionen in ' + path.name)
        lines = ['# Glide · feste Bauabhängigkeiten mit Original-SHA-256 von PyPI.',
                 '# Erneuern: python3 -B scripts/pflege/bauhashes.py', '--require-hashes']
        for name, version in pins:
            with urllib.request.urlopen(f'https://pypi.org/pypi/{name}/{version}/json',
                                        context=context, timeout=60) as response:
                data = json.load(response)
            hashes = sorted({entry['digests']['sha256'] for entry in data['urls']
                             if not entry.get('yanked')})
            if not hashes or any(not re.fullmatch('[0-9a-f]{64}', digest) for digest in hashes):
                raise ValueError('Keine gültigen Originalhashes für ' + name)
            lines.append(name + '==' + version + ' \\\n' + ' \\\n'.join(
                '    --hash=sha256:' + digest for digest in hashes))
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(path.name + ': ' + str(len(pins)) + ' feste Versionen geprüft')


if __name__ == '__main__':
    main()
