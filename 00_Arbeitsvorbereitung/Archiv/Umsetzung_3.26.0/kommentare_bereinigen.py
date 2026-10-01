"""Entfernt Arbeitsauftragsmarker ohne ausführbaren Code zu verändern."""
import ast
import io
from pathlib import Path
import re
import tokenize

p = Path(__file__).resolve().parents[2] / '01_Repository/Glide/src/glide/app.pyw'
s = p.read_text(encoding='utf-8')
lines = s.splitlines(keepends=True)
offsets = [0]
for line in lines:
    offsets.append(offsets[-1] + len(line))
pattern = re.compile(r'Punkt(?:e)?\s+\d+(?:\.\d+)?(?:\s*(?:und|bis|[–,])\s*\d+(?:\.\d+)?)*\s*\([^\n)]*3\.2[2-5](?:\.\d+)?[^\n)]*\):?\s*')
edits = []
for token in tokenize.generate_tokens(io.StringIO(s).readline):
    if token.type != tokenize.COMMENT:
        continue
    changed = pattern.sub('', token.string)
    if changed != token.string:
        start = offsets[token.start[0]-1] + token.start[1]
        end = offsets[token.end[0]-1] + token.end[1]
        edits.append((start, end, changed))
tree = ast.parse(s)
for node in ast.walk(tree):
    if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and node.body:
        first = node.body[0]
        if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
            token = first.value
            start = offsets[token.lineno-1] + len(lines[token.lineno-1].encode('utf-8')[:token.col_offset].decode('utf-8'))
            end = offsets[token.end_lineno-1] + len(lines[token.end_lineno-1].encode('utf-8')[:token.end_col_offset].decode('utf-8'))
            old = s[start:end]
            changed = pattern.sub('', old)
            if changed != old:
                edits.append((start, end, changed))
for start, end, changed in sorted(edits, reverse=True):
    s = s[:start] + changed + s[end:]
def runtime_tree(source):
    node = ast.parse(source)
    for item in ast.walk(node):
        if isinstance(item, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and item.body:
            first = item.body[0]
            if isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant) and isinstance(first.value.value, str):
                first.value.value = ''
    return ast.dump(node, include_attributes=False)
assert runtime_tree(p.read_text(encoding='utf-8')) == runtime_tree(s)
p.write_text(s, encoding='utf-8')
print(f'{len(edits)} historische Arbeitsauftragsmarker bereinigt; Laufzeit-AST unverändert.')
