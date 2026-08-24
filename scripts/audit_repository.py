#!/usr/bin/env python3
"""Read-only integrity audit for the frozen banana experiment-shift repository.

The audit is deliberately side-effect free: CI never rewrites notebooks, commits
generated files, or pushes back to the repository. Frozen NB02–NB08 notebooks are
stored as immutable base85+gzip provenance payloads and are decoded only in memory.
"""
from __future__ import annotations

import base64
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "notebooks"
ARCHIVE_DIR = ROOT / "archive" / "frozen_notebook_payloads"
SCRIPT_DIR = ROOT / "scripts"

NOTEBOOKS = [
    "01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb",
    "02_PCA_UMAP_DOMAIN_SHIFT.ipynb",
    "03_INNER_LOEO_MODEL_SELECTION.ipynb",
    "04_OUTER_LOEO_EVALUATION.ipynb",
    "05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb",
    "06_CALIBRATION_RELIABILITY_ORDINAL.ipynb",
    "06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb",
    "07_FINAL_STATISTICAL_INFERENCE.ipynb",
    "08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb",
]

EXPECTED_NOTEBOOK_SOURCE = {
    "01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb": ("02356fe8a51e6ae61b93b5289f1becbdbd99021418922a287a8df2a6776c75a8", 9170),
    "02_PCA_UMAP_DOMAIN_SHIFT.ipynb": ("4c18bdc8ed0cf39afc474e72f1237a4017bb4996bb3811bcd3cf916db7240f9c", 36504),
    "03_INNER_LOEO_MODEL_SELECTION.ipynb": ("7b11ba55fd472c8955a1d8b3077d2a653810b5f27ffc54f98d6735fd5f86c5fe", 31265),
    "04_OUTER_LOEO_EVALUATION.ipynb": ("29e3bcb96a4dfae3c5749f1c3e3988caf57fd7f3bee4f3bd447e3d53478c4d4e", 29995),
    "05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb": ("20c7b95995c417fc4e00f35af11fc3a11baf6cea0c127fbbee5cc6a6702383f9", 40388),
    "06_CALIBRATION_RELIABILITY_ORDINAL.ipynb": ("21cc97bac89b13a910e5a7a4009de0a5713ed3b7364239db678edfac32484eca", 42401),
    "06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb": ("d8999076c4c067be8aba6a83f3ad2b5351c784ac7646f879c1055aa024f496bd", 33826),
    "07_FINAL_STATISTICAL_INFERENCE.ipynb": ("3232477307baea128472ecd12fee0346168a548cf6b117a99ca7f8e1878b674b", 35257),
    "08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb": ("8efd3456de3bf2ee2eb6c78a2a60721c582937232b1fe8e2b8363e5a601f32d3", 47560),
}

EXPECTED_PAYLOAD_GIT_BLOBS = {
    "02_PCA_UMAP_DOMAIN_SHIFT.ipynb.b85gz": "9341dcdf1f4c99105ac406da6c49f7f41ce73033",
    "03_INNER_LOEO_MODEL_SELECTION.ipynb.b85gz": "e3c99cc16892c938fa65ded968df033d37729a75",
    "04_OUTER_LOEO_EVALUATION.ipynb.b85gz": "90712a56f078a0927ab40f47ee716f1537ecc2ef",
    "05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb.b85gz": "b8052a7632b7f80954c6f92137ab3289ffbbfd15",
    "06_CALIBRATION_RELIABILITY_ORDINAL.ipynb.b85gz": "e559848f3a895c301d2ba2260920ed2c3add2727",
    "06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb.b85gz": "caf7113466f936e70e5f36c4acf0fc798e48d29a",
    "07_FINAL_STATISTICAL_INFERENCE.ipynb.b85gz": "b6ad61c3198d1b704c5d4bce6cb1efd6dabb7d4b",
    "08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb.b85gz": "0d9a28cc71ada25e537c08ad6bce622a9718f490",
}

EXPECTED_PROTOCOL_CANONICAL_SHA = "df508d709559fa48c28e580329b1dfe2790251183a176897fc4ced708a808f42"
ORIGINAL_PROTOCOL_RAW_SHA = "86731ff9a292f1afd35a215105b14c4af3aa2bda5e8c4dad4df639d4d82ad930"

EXPECTED_FACTS = {
    "n_original_observations": 17662,
    "n_outer_experiments": 4,
    "n_modalities": 3,
    "n_models": 5,
    "n_outer_model_cells": 60,
    "n_outer_modality_selection_scenarios": 12,
    "internal_external_winner_matches": 1,
    "internal_external_winner_agreement_rate": 1 / 12,
    "mean_selection_loss_macro_f1": 0.114728,
    "max_selection_loss_macro_f1": 0.214790,
    "mean_inner_external_spearman": -0.075414,
}

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()

def normalized_code(source: str) -> str:
    return "\n".join(
        line for line in source.splitlines()
        if not line.lstrip().startswith(("!", "%"))
    )

def parse_and_compile_notebook(name: str, data: bytes) -> dict:
    expected_sha, expected_size = EXPECTED_NOTEBOOK_SOURCE[name]
    if len(data) != expected_size:
        fail(f"{name}: byte size {len(data)} != frozen {expected_size}")
    got = sha256(data)
    if got != expected_sha:
        fail(f"{name}: SHA-256 {got} != frozen {expected_sha}")
    try:
        nb = json.loads(data.decode("utf-8"))
    except Exception as exc:
        fail(f"{name}: invalid notebook JSON: {exc}")
    if not isinstance(nb.get("cells"), list):
        fail(f"{name}: missing notebook cell list")
    for idx, cell in enumerate(nb["cells"]):
        if cell.get("cell_type") != "code":
            continue
        src = cell.get("source", "")
        if isinstance(src, list):
            src = "".join(src)
        try:
            compile(normalized_code(src), f"{name}:cell{idx}", "exec")
        except SyntaxError as exc:
            fail(f"{name}: Python syntax error in code cell {idx}: {exc}")
    return nb

print("AUDIT 1/8 — frozen notebook provenance")
nb01 = NOTEBOOK_DIR / NOTEBOOKS[0]
if not nb01.exists():
    fail("missing directly browsable NB01 notebook")
parse_and_compile_notebook(NOTEBOOKS[0], nb01.read_bytes())

if not ARCHIVE_DIR.exists():
    fail("missing archive/frozen_notebook_payloads")
for name in NOTEBOOKS[1:]:
    payload_name = f"{name}.b85gz"
    payload_path = ARCHIVE_DIR / payload_name
    if not payload_path.exists():
        fail(f"missing frozen notebook payload: {payload_name}")
    payload = payload_path.read_bytes()
    expected_blob = EXPECTED_PAYLOAD_GIT_BLOBS[payload_name]
    got_blob = git_blob_sha(payload)
    if got_blob != expected_blob:
        fail(f"{payload_name}: Git blob SHA changed: {got_blob}")
    try:
        notebook_bytes = gzip.decompress(base64.b85decode(payload))
    except Exception as exc:
        fail(f"{payload_name}: cannot decode base85+gzip payload: {exc}")
    parse_and_compile_notebook(name, notebook_bytes)
print("PASS: NB01 and eight immutable notebook payloads reproduce all nine frozen notebook sources.")

print("AUDIT 2/8 — repository layout")
if (ROOT / "notebooks_packed").exists():
    fail("obsolete notebooks_packed/ directory is present at repository root")
if (SCRIPT_DIR / "unpack_notebooks.py").exists():
    fail("obsolete scripts/unpack_notebooks.py is present")
for required in [
    ROOT / "archive" / "README.md",
    NOTEBOOK_DIR / "README.md",
    SCRIPT_DIR / "rebuild_analysis_mirrors.py",
]:
    if not required.exists():
        fail(f"missing reviewer-facing file: {required.relative_to(ROOT)}")
print("PASS: provenance payloads are archived and the reviewer-facing root is clean.")

print("AUDIT 3/8 — frozen LOEO protocol")
protocol_path = ROOT / "config" / "nested_loeo_protocol_v1.json"
if not protocol_path.exists():
    fail("missing config/nested_loeo_protocol_v1.json")
raw_protocol = protocol_path.read_bytes()
try:
    protocol = json.loads(raw_protocol.decode("utf-8"))
except Exception as exc:
    fail(f"invalid frozen protocol JSON: {exc}")
canonical = json.dumps(
    protocol, sort_keys=True, separators=(",", ":"), ensure_ascii=False
).encode("utf-8")
if sha256(canonical) != EXPECTED_PROTOCOL_CANONICAL_SHA:
    fail("frozen LOEO protocol semantic SHA-256 changed")
raw_sha = sha256(raw_protocol)
if raw_sha == ORIGINAL_PROTOCOL_RAW_SHA:
    print("PASS: protocol semantic and raw-byte hashes match the archived protocol.")
else:
    print("PASS: protocol semantic hash matches; raw serialization differs but semantics are unchanged.")

print("AUDIT 4/8 — frozen numerical evidence")
facts_path = ROOT / "results" / "frozen_numeric_facts_nb08.json"
if not facts_path.exists():
    fail("missing results/frozen_numeric_facts_nb08.json")
facts = json.loads(facts_path.read_text(encoding="utf-8"))
for key, expected in EXPECTED_FACTS.items():
    if key not in facts:
        fail(f"missing frozen fact: {key}")
    got = facts[key]
    if isinstance(expected, float):
        if not math.isclose(float(got), float(expected), rel_tol=1e-4, abs_tol=1e-6):
            fail(f"frozen fact mismatch: {key}: {got} vs expected≈{expected}")
    elif got != expected:
        fail(f"frozen fact mismatch: {key}: {got} vs {expected}")
print("PASS: frozen NB08 numerical evidence matches audited values.")

print("AUDIT 5/8 — manuscript tables and manifests")
main_table_dir = ROOT / "results" / "main_tables"
main_tables = sorted(main_table_dir.glob("*.csv")) if main_table_dir.exists() else []
if len(main_tables) != 7:
    fail(f"expected 7 main manuscript tables, found {len(main_tables)}")
for required in [ROOT / "results" / "table_manifest.csv", ROOT / "results" / "figure_manifest.csv"]:
    if not required.exists():
        fail(f"missing {required.relative_to(ROOT)}")
print("PASS: seven main manuscript tables and both manifests are present.")

print("AUDIT 6/8 — documentation and reviewer safeguards")
readme_path = ROOT / "README.md"
if not readme_path.exists():
    fail("missing README.md")
readme = readme_path.read_text(encoding="utf-8")
for phrase in [
    "10.15125/BATH-01459",
    "Leave-One-Experiment-Out",
    "1/12",
    "0.1147",
    "archive/frozen_notebook_payloads",
    "rebuild_analysis_mirrors.py",
]:
    if phrase not in readme:
        fail(f"README missing required reproducibility phrase: {phrase}")
notebook_readme = (NOTEBOOK_DIR / "README.md").read_text(encoding="utf-8")
for name in NOTEBOOKS:
    if name not in notebook_readme:
        fail(f"notebooks/README missing pipeline stage: {name}")
print("PASS: README files document data provenance, reconstruction, and all nine analysis stages.")

print("AUDIT 7/8 — manuscript evidence traceability")
evidence_map_path = ROOT / "docs" / "MANUSCRIPT_EVIDENCE_MAP.md"
if not evidence_map_path.exists():
    fail("missing docs/MANUSCRIPT_EVIDENCE_MAP.md")
evidence_map = evidence_map_path.read_text(encoding="utf-8")
for phrase in [
    "Table_3_confirmatory_external_selected_models.csv",
    "Table_4_model_selection_instability_summary.csv",
    "Table_6_probabilistic_calibration_selected_models.csv",
    "Table_7_structural_effect_sizes.csv",
    "external_support_distance_ratio",
    "NB06-v1.1",
]:
    if phrase not in evidence_map:
        fail(f"manuscript evidence map missing: {phrase}")
print("PASS: manuscript claims remain linked to frozen evidence and explicit exclusions.")

print("AUDIT 8/8 — repository file policy")
for path in ROOT.rglob("*"):
    if not path.is_file():
        continue
    rel = path.relative_to(ROOT)
    if rel.parts and rel.parts[0] == ".git":
        continue
    if path.suffix.lower() in {".zip", ".7z", ".rar"}:
        fail(f"raw/archive bundle should not be tracked: {rel}")
    if path.stat().st_size > 10 * 1024 * 1024:
        fail(f"file exceeds 10 MiB policy: {rel}")
print("PASS: no raw archives or oversized research files are tracked.")

print("\nPASS: frozen notebook provenance, leakage-safe protocol, manuscript evidence, and repository structure are internally consistent.")
print("PASS: repository integrity audit completed successfully.")
