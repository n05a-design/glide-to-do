"""Synthetische Blockmessung mit Format-/Linkerhalt; keine Tk-/Nutzerdatenzugriffe."""
import hashlib
import json
from pathlib import Path
import platform
import statistics
import sys
import time

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / 'src/glide'))
import page_features as pages


def run():
    report = {'version': '3.50.0', 'datum': '2026-11-02', 'python': platform.python_version(),
              'plattform': sys.platform, 'maschine': platform.machine(),
              'modul_sha256': hashlib.sha256((REPO/'src/glide/page_features.py').read_bytes()).hexdigest(),
              'kuenstliche_daten': True, 'messungen': []}
    for count in (100, 1000, 5000, 10000):
        rows = [f'Block {i:05d} · Text mit Umlaut ä und Emoji 😀' for i in range(count)]
        text = '\n'.join(rows)
        start, spans = 0, []
        for index, row in enumerate(rows):
            spans.append({'tag': f'link:{index}', 'start': start, 'end': start+len(row)})
            start += len(row)+1
        document = {'text': text, 'spans': spans,
                    'links': {f'link:{i}': f'glide://list/id{i}' for i in range(count)}}
        samples = []
        for attempt in range(11):
            began = time.perf_counter()
            result, caret = pages.move_document_block(document, count//4, count//4+1, count*3//4)
            duration = (time.perf_counter()-began)*1000
            assert result['links'] == document['links'] and len(result['spans']) == count
            assert result['text'][caret:caret+len(rows[count//4])] == rows[count//4]
            for span in result['spans']:
                index = int(span['tag'].split(':')[1])
                assert result['text'][span['start']:span['end']] == rows[index]
            assert document['text'] == text
            if attempt >= 2:
                samples.append(duration)
        # Eine große Aufklappgruppe bleibt in einem linearen Durchlauf zusammen.
        toggle = {'text': text, 'spans': [{'tag':'toggle','start':0,'end':len(rows[0])},
                  {'tag':'indent1','start':len(rows[0])+1,'end':len(text)}]}
        began = time.perf_counter()
        assert pages.block_lines(toggle, 0) == (0, count)
        group_ms = (time.perf_counter()-began)*1000
        report['messungen'].append({'zeilen':count,'spans':count,'zeichen':len(text),'proben':len(samples),
            'median_ms':round(statistics.median(samples),3),'p95_ms':round(sorted(samples)[-1],3),
            'aufklappgruppe_ms':round(group_ms,3),'format_link_text_erhalten':True})
    report['exitcode'] = 0
    return report


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2))
