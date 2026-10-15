"""Native Signaturgegenprobe auf vergänglichem Windows-CI, keine Systemänderung."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import traceback

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/'packaging/paket'))
from runtime_paths import authenticode, defender_provider


def run(report):
    if (sys.platform != 'win32' or os.environ.get('GITHUB_ACTIONS') != 'true' or
            os.environ.get('RUNNER_ENVIRONMENT') != 'github-hosted'):
        raise RuntimeError('Signaturgegenprobe nur im vergänglichen Windows-Hosted-CI.')
    temporary = Path(os.environ['RUNNER_TEMP']).resolve()
    report = report.resolve()
    if report == temporary or not report.is_relative_to(temporary) or report.exists():
        raise ValueError('Unbenutzter eigener Bericht unter RUNNER_TEMP erforderlich.')
    result = dict(exitcode=1, system_installationen_unveraendert=True)
    try:
        base = Path(os.environ['ProgramData'])/'Microsoft/Windows Defender/Platform'
        candidates = [path for path in base.glob('*/MpOAV.dll')
                      if defender_provider(str(path), os.environ['ProgramData']) is not None]
        if not candidates:
            raise RuntimeError('Bekannter Microsoft-Systemanbieter für die positive Gegenprobe fehlt.')
        original = max(candidates, key=lambda path: tuple(map(int,re.findall(r'\d+',path.parent.name))))
        data = original.read_bytes()
        started = time.monotonic()
        positive = authenticode(original, os.environ['SystemRoot'])
        result.update(positive=positive, verifikation_ms=round((time.monotonic()-started)*1000),
                      original_sha256=hashlib.sha256(data).hexdigest())
        assert positive['Status'] == 'Valid', positive
        assert re.search(r'(?:^|,\s*)O=Microsoft Corporation(?:,|$)', positive['Subject']), positive
        with tempfile.TemporaryDirectory(prefix='glide-signature-counter-', dir=temporary) as folder:
            # Nur die künstliche Kopie verändern: DOS-Stub gehört zum Hash,
            # PE-Header und Zertifikatsdaten bleiben weiterhin auswertbar.
            altered = bytearray(data)
            assert altered[:2] == b'MZ' and len(altered) > 0x40
            altered[0x40] ^= 1
            counter = Path(folder)/'manipulierte-kopie.dll'
            counter.write_bytes(altered)
            negative = authenticode(counter, os.environ['SystemRoot'])
            result['manipulierte_kopie'] = negative
            assert negative['Status'] != 'Valid', 'Manipulierte Microsoft-Kopie darf nicht gültig sein.'
            assert original.read_bytes() == data, 'Originalanbieter wurde verändert.'
        result['exitcode'] = 0
    except Exception as error:
        result.update(fehler=str(error),traceback=traceback.format_exc())
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('Native Windows-Signaturgegenprobe Exit',result['exitcode'])
    return result['exitcode']


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bericht',type=Path,required=True)
    args=parser.parse_args();raise SystemExit(run(args.bericht))
