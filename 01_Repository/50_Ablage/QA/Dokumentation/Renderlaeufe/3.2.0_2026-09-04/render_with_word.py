"""Run the document skill renderer with a supplied Word PDF conversion.

LibreOffice is unavailable on this Windows host. Word exports the PDF read-only;
the canonical renderer still handles rasterisation, naming and image sizing.
"""
import importlib.util
import shutil
import sys
from pathlib import Path

skill = Path(r'C:\Users\vontrostorff\.codex\plugins\cache\openai-primary-runtime\documents\26.903.11726\skills\documents')
spec = importlib.util.spec_from_file_location('canonical_render_docx', skill / 'render_docx.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
docx, pdf, output = map(Path, sys.argv[1:4])
def word_pdf(input_path, user_profile, convert_tmp_dir, stem, verbose=False):
    target = Path(convert_tmp_dir) / (stem + '.pdf')
    shutil.copy2(pdf, target)
    return str(target), 'PDF exported by installed Microsoft Word, read-only'
module.convert_to_pdf = word_pdf
module.rasterize(str(docx), str(output), 130, False, True)
print(output)
