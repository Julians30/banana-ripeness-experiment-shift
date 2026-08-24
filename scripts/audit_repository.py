#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, hashlib, json, math, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
REQUIRED_NOTEBOOKS = [
    '01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb',
    '02_PCA_UMAP_DOMAIN_SHIFT.ipynb',
    '03_INNER_LOEO_MODEL_SELECTION.ipynb',
    '04_OUTER_LOEO_EVALUATION.ipynb',
    '05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb',
    '06_CALIBRATION_RELIABILITY_ORDINAL.ipynb',
    '06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb',
    '07_FINAL_STATISTICAL_INFERENCE.ipynb',
    '08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb',
]

# The scientific protocol is frozen semantically. This canonical hash is
# invariant to whitespace/indentation while still changing if any key/value,
# fold, or rule changes.
EXPECTED_PROTOCOL_CANONICAL_SHA = 'df508d709559fa48c28e580329b1dfe2790251183a176897fc4ced708a808f42'
ORIGINAL_PROTOCOL_RAW_SHA = '86731ff9a292f1afd35a215105b14c4af3aa2bda5e8c4dad4df639d4d82ad930'

EXPECTED = {
    'n_original_observations': 17662,
    'n_outer_experiments': 4,
    'n_modalities': 3,
    'n_models': 5,
    'n_outer_model_cells': 60,
    'n_outer_modality_selection_scenarios': 12,
    'internal_external_winner_matches': 1,
    'internal_external_winner_agreement_rate': 1/12,
    'mean_selection_loss_macro_f1': 0.114728,
    'max_selection_loss_macro_f1': 0.214790,
    'mean_inner_external_spearman': -0.075414,
}


def fail(msg: str) -> None:
    print(f'FAIL: {msg}', file=sys.stderr)
    raise SystemExit(1)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def notebook_bytes(name: str) -> bytes:
    direct = ROOT/'notebooks'/name
    if direct.exists():
        return direct.read_bytes()
    packed = ROOT/'notebooks_packed'/f'{name}.b85gz'
    if not packed.exists():
        fail(f'missing notebook source or packed source: {name}')
    try:
        return gzip.decompress(base64.b85decode(packed.read_bytes()))
    except Exception as exc:
        fail(f'cannot reconstruct {name}: {exc}')


print('AUDIT 1/5 — notebooks')
for name in REQUIRED_NOTEBOOKS:
    try:
        nb = json.loads(notebook_bytes(name).decode('utf-8'))
    except Exception as exc:
        fail(f'invalid notebook JSON {name}: {exc}')
    if not isinstance(nb.get('cells'), list):
        fail(f'notebook cells missing/invalid: {name}')
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') != 'code':
            continue
        src = cell.get('source', '')
        if isinstance(src, list):
            src = ''.join(src)
        cleaned = '\n'.join(
            line for line in src.splitlines()
            if not line.lstrip().startswith(('!', '%'))
        )
        try:
            compile(cleaned, f'{name}:cell{i}', 'exec')
        except SyntaxError as exc:
            fail(f'python syntax error in {name} cell {i}: {exc}')
print(f'PASS: {len(REQUIRED_NOTEBOOKS)} notebooks reconstruct, parse and syntax-check.')

print('AUDIT 2/5 — frozen LOEO protocol')
protocol_path = ROOT/'config'/'nested_loeo_protocol_v1.json'
if not protocol_path.exists():
    fail('missing frozen protocol JSON')
raw_protocol = protocol_path.read_bytes()
try:
    protocol_obj = json.loads(raw_protocol.decode('utf-8'))
except Exception as exc:
    fail(f'invalid frozen protocol JSON: {exc}')
canonical = json.dumps(
    protocol_obj,
    sort_keys=True,
    separators=(',', ':'),
    ensure_ascii=False,
).encode('utf-8')
canonical_sha = sha256_bytes(canonical)
raw_sha = sha256_bytes(raw_protocol)
if canonical_sha != EXPECTED_PROTOCOL_CANONICAL_SHA:
    fail(
        'frozen protocol semantic content changed: '
        f'canonical_sha={canonical_sha}'
    )
print('PASS: frozen protocol semantic SHA-256 matches audited protocol.')
if raw_sha == ORIGINAL_PROTOCOL_RAW_SHA:
    print('PASS: frozen protocol raw-byte SHA-256 also matches original archived file.')
else:
    print(
        'INFO: protocol raw-byte SHA differs only in serialization; '
        f'current={raw_sha}, archived={ORIGINAL_PROTOCOL_RAW_SHA}'
    )

print('AUDIT 3/5 — frozen numerical evidence')
facts_path = ROOT/'results'/'frozen_numeric_facts_nb08.json'
if not facts_path.exists():
    fail('missing frozen NB08 facts')
try:
    facts = json.loads(facts_path.read_text(encoding='utf-8'))
except Exception as exc:
    fail(f'invalid frozen facts JSON: {exc}')
for key, expected in EXPECTED.items():
    if key not in facts:
        fail(f'missing frozen fact: {key}')
    got = facts[key]
    if isinstance(expected, float):
        if not math.isclose(float(got), float(expected), rel_tol=1e-4, abs_tol=1e-6):
            fail(f'frozen fact mismatch: {key}: got={got}, expected≈{expected}')
    elif got != expected:
        fail(f'frozen fact mismatch: {key}: got={got}, expected={expected}')
print('PASS: frozen NB08 numerical evidence matches audited values.')

print('AUDIT 4/5 — manuscript tables and repository policy')
main_table_dir = ROOT/'results'/'main_tables'
if not main_table_dir.exists():
    fail('missing results/main_tables directory')
main_tables = sorted(main_table_dir.glob('*.csv'))
if len(main_tables) != 7:
    fail(f'expected 7 main tables, found {len(main_tables)}')
print('PASS: seven main manuscript tables are present.')

for path in ROOT.rglob('*'):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if rel.parts and rel.parts[0] == '.git':
        continue
    if path.suffix.lower() in {'.zip', '.7z', '.rar'}:
        fail(f'archive should not be tracked: {rel}')
    if path.stat().st_size > 10*1024*1024:
        fail(f'file exceeds 10 MiB policy: {rel}')
print('PASS: tracked research-file policy checks passed.')

print('AUDIT 5/5 — README safeguards')
readme_path = ROOT/'README.md'
if not readme_path.exists():
    fail('missing README.md')
readme = readme_path.read_text(encoding='utf-8')
for phrase in [
    '10.15125/BATH-01459',
    'Leave-One-Experiment-Out',
    '1/12',
    '0.1147',
]:
    if phrase not in readme:
        fail(f'README missing required phrase: {phrase}')
print('PASS: README contains dataset, validation, and frozen-result safeguards.')

print('\nPASS: repository structure and frozen evidence are internally consistent.')
print('PASS: CI reproducibility audit completed successfully.')
