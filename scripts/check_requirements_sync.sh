#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
from pathlib import Path
import re

pyproject_text = Path('pyproject.toml').read_text(encoding='utf-8')

# Read only [project].dependencies = [ ... ] entries pinned as name==version
in_project = False
in_deps = False
deps = []
for raw in pyproject_text.splitlines():
    line = raw.strip()
    if line.startswith('[') and line.endswith(']'):
        in_project = line == '[project]'
        if line != '[project]':
            in_deps = False
        continue
    if not in_project:
        continue
    if line.startswith('dependencies') and '[' in line:
        in_deps = True
        continue
    if in_deps:
        if ']' in line:
            in_deps = False
            continue
        m = re.match(r'"([A-Za-z0-9_.-]+)==([^"\s]+)"\s*,?$', line)
        if m:
            deps.append((m.group(1), m.group(2)))

pattern = re.compile(r'^\s*([A-Za-z0-9_.-]+)==([^\s#]+)\s*$')
req_bytes = Path('requirements.txt').read_bytes()
for enc in ('utf-8', 'utf-16', 'utf-16-le', 'utf-16-be'):
    try:
        req_text = req_bytes.decode(enc)
        break
    except UnicodeDecodeError:
        continue
else:
    raise SystemExit('Não foi possível decodificar requirements.txt (UTF-8/UTF-16).')

req_pins = {}
for line in req_text.splitlines():
    m = pattern.match(line)
    if m:
        req_pins[m.group(1).lower().replace('_', '-').replace('.', '-')] = m.group(2)

missing, mismatch = [], []
for name, exp in deps:
    key = name.lower().replace('_', '-').replace('.', '-')
    got = req_pins.get(key)
    if got is None:
        missing.append(name)
    elif got != exp:
        mismatch.append((name, exp, got))

if missing or mismatch:
    if missing:
        print('Dependências diretas ausentes em requirements.txt:', ', '.join(missing))
    for name, exp, got in mismatch:
        print(f'Versão divergente para {name}: pyproject={exp}, requirements={got}')
    raise SystemExit(1)

print('Dependências diretas de pyproject.toml estão sincronizadas em requirements.txt.')
PY
