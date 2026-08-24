#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, hashlib, json, math, pathlib

ROOT=pathlib.Path(__file__).resolve().parents[1]
REQUIRED_NOTEBOOKS=[
'01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb',
'02_PCA_UMAP_DOMAIN_SHIFT.ipynb',
'03_INNER_LOEO_MODEL_SELECTION.ipynb',
'04_OUTER_LOEO_EVALUATION.ipynb',
'05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb',
'06_CALIBRATION_RELIABILITY_ORDINAL.ipynb',
'06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb',
'07_FINAL_STATISTICAL_INFERENCE.ipynb',
'08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb']
EXPECTED_PROTOCOL_SHA='86731ff9a292f1afd35a215105b14c4af3aa2bda5e8c4dad4df639d4d82ad930'
EXPECTED={'n_original_observations':17662,'n_outer_experiments':4,'n_modalities':3,'n_models':5,'n_outer_model_cells':60,'n_outer_modality_selection_scenarios':12,'internal_external_winner_matches':1,'internal_external_winner_agreement_rate':1/12,'mean_selection_loss_macro_f1':0.114728,'max_selection_loss_macro_f1':0.214790,'mean_inner_external_spearman':-0.075414}

def fail(msg): raise SystemExit('FAIL: '+msg)
def sha256(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def notebook_bytes(name):
    direct=ROOT/'notebooks'/name
    if direct.exists(): return direct.read_bytes()
    packed=ROOT/'notebooks_packed'/f'{name}.b85gz'
    if not packed.exists(): fail(f'missing notebook source or packed source: {name}')
    try: return gzip.decompress(base64.b85decode(packed.read_bytes()))
    except Exception as e: fail(f'cannot reconstruct {name}: {e}')

for name in REQUIRED_NOTEBOOKS:
    try: nb=json.loads(notebook_bytes(name).decode('utf-8'))
    except Exception as e: fail(f'invalid notebook JSON {name}: {e}')
    for i,cell in enumerate(nb.get('cells',[])):
        if cell.get('cell_type')!='code': continue
        src=cell.get('source','')
        if isinstance(src,list): src=''.join(src)
        cleaned='\n'.join(line for line in src.splitlines() if not line.lstrip().startswith(('!','%')))
        try: compile(cleaned,f'{name}:cell{i}','exec')
        except SyntaxError as e: fail(f'python syntax error in {name} cell {i}: {e}')

protocol=ROOT/'config'/'nested_loeo_protocol_v1.json'
if not protocol.exists(): fail('missing frozen protocol JSON')
json.loads(protocol.read_text(encoding='utf-8'))
if sha256(protocol)!=EXPECTED_PROTOCOL_SHA: fail('frozen protocol SHA-256 changed')

facts_path=ROOT/'results'/'frozen_numeric_facts_nb08.json'
if not facts_path.exists(): fail('missing frozen NB08 facts')
facts=json.loads(facts_path.read_text(encoding='utf-8'))
for k,v in EXPECTED.items():
    if k not in facts: fail(f'missing frozen fact: {k}')
    got=facts[k]
    if isinstance(v,float):
        if not math.isclose(float(got),float(v),rel_tol=1e-4,abs_tol=1e-6): fail(f'frozen fact mismatch: {k}')
    elif got!=v: fail(f'frozen fact mismatch: {k}')

main_tables=list((ROOT/'results'/'main_tables').glob('*.csv'))
if len(main_tables)!=7: fail(f'expected 7 main tables, found {len(main_tables)}')

for p in ROOT.rglob('*'):
    if not p.is_file(): continue
    rel=p.relative_to(ROOT)
    if p.suffix.lower() in {'.zip','.7z','.rar'}: fail(f'archive should not be tracked: {rel}')
    if p.stat().st_size>10*1024*1024: fail(f'file exceeds 10 MiB policy: {rel}')

readme=(ROOT/'README.md').read_text(encoding='utf-8')
for phrase in ['10.15125/BATH-01459','Leave-One-Experiment-Out','1/12','0.1147']:
    if phrase not in readme: fail(f'README missing required phrase: {phrase}')

print('PASS: repository structure and frozen evidence are internally consistent.')
print(f'PASS: {len(REQUIRED_NOTEBOOKS)} notebooks reconstruct, parse and syntax-check.')
print('PASS: frozen protocol SHA-256 matches audited protocol.')
print('PASS: seven main manuscript tables are present.')
