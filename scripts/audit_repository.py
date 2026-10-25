#!/usr/bin/env python3
"""Read-only integrity audit for the banana experiment-shift repository.

The audit is side-effect free. It verifies:
1) frozen notebook provenance;
2) clean repository layout;
3) frozen LOEO protocol;
4) frozen numerical evidence;
5) original analytical tables/manifests;
6) current revised-manuscript presentation artifacts;
7) reviewer-requested revision evidence;
8) environment/citation metadata;
9) manuscript-evidence traceability and documentation;
10) repository file policy;
11) post-hoc robustness evidence and current-submission traceability.

CI never rewrites notebooks, commits generated files, or pushes to the repository.
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
    "08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb": ("59b4f7e2dcc6cfb214536cf31736b50a2af9666b207387eb897ff6f994d58c9e", 46883),
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

CURRENT_ARTIFACT_SHA256 = {
    "results/reviewer_revision/Table_S1_reconstruction_count_audit.csv": "d0897be3128e001d7a91b313097d6e99b4319680b7660c25a7d88fe80e8bcc70",
    "results/reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv": "df88ec28798fa8b19442d18deb1d6308dce31aebb90088b46ca9f8c70b41dbf3",
    "results/reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv": "dab5bf76b28bef36dd97a2454b46747b093a40f5cbe888a776e0cfa5cd68a349",
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
    got = sha256(data)
    if len(data) != expected_size:
        fail(f"{name}: byte size {len(data)} != frozen {expected_size}; SHA-256={got}")
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


print("AUDIT 1/11 — frozen notebook provenance")
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
print("PASS: NB01 and eight immutable payloads reproduce all nine frozen notebook sources.")

print("AUDIT 2/11 — repository layout")
if (ROOT / "notebooks_packed").exists():
    fail("obsolete notebooks_packed/ directory is present at repository root")
if (SCRIPT_DIR / "unpack_notebooks.py").exists():
    fail("obsolete scripts/unpack_notebooks.py is present")
for required in [
    ROOT / "archive" / "README.md",
    NOTEBOOK_DIR / "README.md",
    SCRIPT_DIR / "rebuild_analysis_mirrors.py",
    SCRIPT_DIR / "09_REVIEWER_REQUESTED_AUDITS.py",
]:
    if not required.exists():
        fail(f"missing reviewer-facing file: {required.relative_to(ROOT)}")
print("PASS: provenance archive and reviewer-facing utilities are present.")

print("AUDIT 3/11 — frozen LOEO protocol")
protocol_path = ROOT / "config" / "nested_loeo_protocol_v1.json"
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
if sha256(raw_protocol) == ORIGINAL_PROTOCOL_RAW_SHA:
    print("PASS: protocol semantic and raw-byte hashes match the archived protocol.")
else:
    print("PASS: protocol semantic hash matches; raw serialization differs but semantics are unchanged.")

print("AUDIT 4/11 — frozen numerical evidence")
facts_path = ROOT / "results" / "frozen_numeric_facts_nb08.json"
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

print("AUDIT 5/11 — original analytical tables and manifests")
main_table_dir = ROOT / "results" / "main_tables"
main_tables = sorted(main_table_dir.glob("*.csv")) if main_table_dir.exists() else []
if len(main_tables) != 7:
    fail(f"expected 7 frozen analytical tables, found {len(main_tables)}")
for required in [ROOT / "results" / "table_manifest.csv", ROOT / "results" / "figure_manifest.csv"]:
    if not required.exists():
        fail(f"missing {required.relative_to(ROOT)}")
print("PASS: seven frozen analytical tables and both top-level manifests are present.")

print("AUDIT 6/11 — current revised-manuscript artifacts")
for rel, expected_sha in CURRENT_ARTIFACT_SHA256.items():
    path = ROOT / rel
    if not path.exists():
        fail(f"missing current manuscript/reviewer artifact: {rel}")
    got = sha256(path.read_bytes())
    if got != expected_sha:
        fail(f"current artifact changed: {rel}: SHA-256={got}")
for required in [
    ROOT / "results" / "manuscript_current" / "README.md",
    ROOT / "results" / "manuscript_current" / "figures" / "README.md",
    ROOT / "results" / "reviewer_revision" / "README.md",
    ROOT / "results" / "reviewer_revision" / "manifest.csv",
]:
    if not required.exists():
        fail(f"missing current manuscript traceability file: {required.relative_to(ROOT)}")
figure_provenance = (ROOT / "results/manuscript_current/figures/README.md").read_text(encoding="utf-8")
for figure_hash in [
    "c9d447a9c11a0b3f2763e3757c86a7f08c008a0d609e3e5640fceef8ccc04330",
    "4e3c09ff01e10602b454a295076a038b75842606cd64dfd20540175c284ecb92",
    "8660e842aa40c7dfec8dce50b03e42537c25c2a6f4c2d1fcb9d87b792e80449d",
    "42725a5bced3feb40be9ef07c6954984aabc576af553e7e731d0807c5d65e782",
    "acb9214549c571460932acb1fc12e236634544c10160fc24326ca703bd32e329",
    "b913ec2489228cd58470085c9d9082e838b7bcb809e2a83fa5025353a0e98372",
    "601276fddffbd8930430629f12ad7eea09abfede868e3d4c2e0c7e4fabc03971",
    "b45fe834e60a64c3bae4fe187b43f2bfb5fbb26289ac7c6444be51aec482cf97",
]:
    if figure_hash not in figure_provenance:
        fail(f"current figure provenance missing SHA-256: {figure_hash}")
print("PASS: current revised-manuscript mapping, figure provenance and reviewer additions are versioned.")

print("AUDIT 7/11 — reviewer-requested evidence semantics")
s1 = (ROOT / "results/reviewer_revision/Table_S1_reconstruction_count_audit.csv").read_text(encoding="utf-8-sig")
s3 = (ROOT / "results/reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv").read_text(encoding="utf-8-sig")
s2 = (ROOT / "results/reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv").read_text(encoding="utf-8-sig")
for phrase in ["17662", "15003", "32665"]:
    if phrase not in s1:
        fail(f"Table S1 missing audited count {phrase}")
for phrase in ["2,2,718,17,17,34", "5,1,1193,2,2,4"]:
    if phrase not in s2.replace("\r\n", "\n"):
        fail(f"Table S2 missing sparse stage-matching row {phrase}")
for phrase in ["0.073", "0.070", "0.075"]:
    if phrase not in s3:
        fail(f"Table S3 missing no-skill Macro-F1 {phrase}")
revision_readme = (ROOT / "results/reviewer_revision/README.md").read_text(encoding="utf-8")
for phrase in ["post-hoc explanatory", "frozen NB03 hyperparameters", "not causal biochemical evidence"]:
    if phrase not in revision_readme:
        fail(f"reviewer revision documentation missing phrase: {phrase}")
print("PASS: reviewer-requested count, baseline, sample-size and TreeSHAP scope are explicit.")

print("AUDIT 8/11 — environment and citation metadata")
requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
environment = (ROOT / "environment.yml").read_text(encoding="utf-8")
citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
if "shap==0.50.0" not in requirements or "shap==0.50.0" not in environment:
    fail("SHAP dependency used by the revised manuscript is not pinned")
if "python=3.13.15" not in environment:
    fail("environment.yml does not pin the analytical Python version")
AUTHORS = ["Coronel-Reyes", "Haro-Sarango", "Triviño Sanchez"]
for author in AUTHORS:
    if author not in citation:
        fail(f"CITATION.cff missing manuscript author: {author}")
n_entries = sum(1 for line in citation.splitlines() if line.lstrip().startswith("- family-names:"))
if n_entries != 2 * len(AUTHORS):  # software authors + preferred-citation authors
    fail(f"CITATION.cff lists {n_entries} author entries; expected exactly {len(AUTHORS)} in each author block")
print("PASS: Python/package environment and three-author citation metadata (manuscript author list) match the revised study.")

print("AUDIT 9/11 — documentation and manuscript-evidence traceability")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in [
    "10.15125/BATH-01459",
    "Leave-One-Experiment-Out",
    "1/12",
    "0.1147",
    "archive/frozen_notebook_payloads",
    "results/manuscript_current",
    "results/reviewer_revision",
]:
    if phrase not in readme:
        fail(f"README missing reproducibility phrase: {phrase}")
evidence_map = (ROOT / "docs" / "MANUSCRIPT_EVIDENCE_MAP.md").read_text(encoding="utf-8")
for phrase in [
    "Table_S1_reconstruction_count_audit.csv",
    "Table_S3_development_majority_no_skill_baseline.csv",
    "Table_S2_stage_matched_effective_sample_sizes.csv",
    "chemolab_submission/README.md",
    "config/PROTOCOL_V1.md",
    "nb17_reviewer_shield",
    "external_support_distance_ratio",
    "NB06-v1.1",
]:
    if phrase not in evidence_map:
        fail(f"manuscript evidence map missing: {phrase}")
import re
for md in sorted(ROOT.rglob("*.md")):
    if ".git" in md.parts:
        continue
    for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", md.read_text(encoding="utf-8")):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (md.parent / target).exists():
            fail(f"broken relative link in {md.relative_to(ROOT)}: {target}")
print("PASS: README and evidence map cover frozen, reviewer-revision and post-hoc evidence; all relative Markdown links resolve.")

print("AUDIT 10/11 — repository file policy")
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

print("AUDIT 11/11 — post-hoc robustness evidence and current-submission traceability")
nb14 = ROOT / "results" / "post_hoc" / "nb14_prospective_domain_z"
nb15 = ROOT / "results" / "post_hoc" / "nb15_spectral_error_audit"
for required in [
    nb14 / "08_source_order_prefix_vs_raw_and_oracle.csv",
    nb14 / "09_source_order_summary_by_window.csv",
    nb14 / "11_stage_composition_stress_summary.csv",
    nb14 / "12_key_results_nb14.json",
    nb15 / "feature_displacement.csv",
    nb15 / "pca_coefficients.csv",
    nb15 / "projection_coordinates.csv.gz",
    ROOT / "results" / "chemolab_submission" / "README.md",
    ROOT / "results" / "chemolab_submission" / "figure_provenance.csv",
    ROOT / "scripts" / "make_publication_figures.py",
    ROOT / "notebooks" / "post_hoc" / "17_REVIEWER_SHIELD_POSITIVE_CONTROL_MSC_CALIBRATORS.ipynb",
    ROOT / "results" / "post_hoc" / "nb17_reviewer_shield" / "A_summary.csv",
    ROOT / "results" / "post_hoc" / "nb17_reviewer_shield" / "C_calibrators.csv",
]:
    if not required.exists():
        fail(f"missing post-hoc/current-submission file: {required.relative_to(ROOT)}")
key = json.loads((nb14 / "12_key_results_nb14.json").read_text(encoding="utf-8"))
for name, expected in {
    "primary_window_unique_spectra": 25,
    "primary_tests_prefix_better_than_raw": 2,
    "primary_mean_raw_future_macro_f1": 0.125482,
    "primary_mean_domainz_prefix_macro_f1": 0.175465,
    "minimum_two_sided_exact_sign_p_for_4_of_4": 0.125,
}.items():
    got = key.get(name)
    if got is None or not math.isclose(float(got), float(expected), rel_tol=1e-4, abs_tol=1e-6):
        fail(f"NB14 key result mismatch: {name}: {got} vs {expected}")
provenance_rows = (ROOT / "results/chemolab_submission/figure_provenance.csv").read_text(encoding="utf-8").strip().splitlines()[1:]
if len(provenance_rows) != 26:
    fail(f"expected 26 current-submission figures (11 main + 15 supplementary), found {len(provenance_rows)}")
figure_dir = ROOT / "results" / "chemolab_submission" / "figures"
for row in provenance_rows:
    item, filename, expected_sha = row.split(",")[:3]
    png = figure_dir / filename
    if not png.exists():
        fail(f"submitted figure file missing: {png.relative_to(ROOT)} ({item})")
    if hashlib.sha256(png.read_bytes()).hexdigest() != expected_sha:
        fail(f"submitted figure does not match the SHA-256 embedded in the manuscript: {filename}")
parse_and_compile_post_hoc = json.loads((ROOT / "notebooks/post_hoc/17_REVIEWER_SHIELD_POSITIVE_CONTROL_MSC_CALIBRATORS.ipynb").read_text(encoding="utf-8"))
for idx, cell in enumerate(parse_and_compile_post_hoc["cells"]):
    if cell.get("cell_type") == "code":
        src = cell["source"] if isinstance(cell["source"], str) else "".join(cell["source"])
        try:
            compile(normalized_code(src), f"NB17:cell{idx}", "exec")
        except SyntaxError as exc:
            fail(f"NB17: Python syntax error in code cell {idx}: {exc}")
print("PASS: NB14/NB15 evidence, NB17 notebook and all 26 submitted figures (byte-identical to the manuscript/supplementary embeds) are versioned and consistent.")

print("\nPASS: frozen analysis and current revised-manuscript evidence are internally consistent.")
print("PASS: repository integrity audit completed successfully (11/11 stages).")
