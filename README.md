# Banana Ripeness Experiment Shift

[![repository-audit](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml)

Reproducible code and frozen manuscript evidence for:

**Model-Selection Instability and Loss of Probabilistic Reliability under Experiment Shift in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation**

## Research question

To what extent do machine-learning models for multisensor banana-ripeness classification preserve predictive performance, model-selection decisions, and probabilistic reliability when evaluated on acquisition experiments completely excluded from model development?

## Data source

The study uses the University of Bath public dataset **Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”**.

- DOI: `10.15125/BATH-01459`
- License: CC BY 4.0
- Raw data are not redistributed in this repository.
- Frozen source archives used by NB01: `ds_34.zip`, `Spect.zip`, `TPHiS.zip`, and `VOC.zip`.

The primary four-experiment analysis uses the TPHiS data and three sensor representations: **TPH**, **Spectral**, and **TPH + Spectral**.

## Leakage-safe design

The confirmatory evaluation uses nested **Leave-One-Experiment-Out (LOEO)** validation. In every outer fold, one complete experiment is excluded from preprocessing, hyperparameter selection, algorithm selection, resampling and calibration fitting until the final external evaluation.

Five algorithms are studied: Ordinal Logistic Regression, PLS-DA, SVM-RBF, Random Forest and XGBoost.

## Frozen analytical pipeline

```text
01 Data audit and frozen LOEO protocol
        ↓
02 PCA / UMAP / experiment-shift diagnostics
        ↓
03 Inner experiment-disjoint model selection
        ↓
04 Confirmatory outer LOEO evaluation
        ↓
05 Imbalance-treatment sensitivity
        ↓
06 Probabilistic reliability and ordinal analysis
        ↓
06-v1.1 Wide-range temperature-scaling correction
        ↓
07 Final statistical inference
        ↓
08 Final manuscript tables and figures
```

NB06-v1.1 supersedes NB06 **only for final temperature-scaling values**. The original NB06 is retained for provenance.

## Frozen main results

Across **17,662** original TPHiS observations, four independent external experiments, three sensor modalities and five algorithms:

- external model cells: **60**;
- outer-experiment × modality model-selection scenarios: **12**;
- internal winner = external winner: **1/12 (8.3%)**;
- mean selection loss: **0.1147 Macro-F1**;
- maximum selection loss: **0.2148 Macro-F1**;
- mean inner-vs-external Spearman rank correlation: **−0.0754**;
- partial η² for held-out experiment on external Macro-F1: **0.4661**;
- partial η² for algorithm: **0.0531**;
- mean ECE of internally selected models: **0.4387 → 0.2568** after development-only temperature scaling;
- class weighting and training-only SMOTE each changed Macro-F1 by only about **+0.004 on average**, with heterogeneous effects across experiments.

The central result is therefore not a universal winning classifier. Experiment-specific distribution shift can dominate algorithm choice, destabilize model selection and reduce the transportability of probability estimates.

## Statistical scope

Only the **four held-out experiments** are treated as independent generalization units. Row-level bootstrap intervals quantify uncertainty conditional on each held-out experiment and are not interpreted as confidence intervals over a population of independent experiments.

The factorial ANOVA in NB07 is used for **descriptive structural effect-size decomposition**. Conventional ANOVA p-values are not used as confirmatory population inference.

## Reviewer-facing code and exact reconstruction

The repository preserves the frozen analysis in two layers:

1. **Canonical reviewer-facing files.** NB01 is stored directly in `notebooks/`. A single deterministic command materializes the remaining source-clean notebooks NB02–NB08 and one text-diff-friendly Python mirror per notebook.
2. **Immutable provenance payloads.** `archive/frozen_notebook_payloads/` contains compact Base85+gzip payloads for NB02–NB08. They are not alternative analyses; they exist only to reconstruct the exact frozen notebook bytes from a fresh clone.

Run:

```bash
python scripts/rebuild_analysis_mirrors.py
python scripts/audit_repository.py
```

The first command reconstructs any missing notebook, verifies the expected SHA-256 and byte count, validates notebook JSON, and generates deterministic `.py` mirrors. The second command verifies notebook bytes, script–notebook equivalence, the frozen LOEO protocol, numerical manuscript evidence, traceability safeguards and repository file policy.

Executed-Colab hashes and source-clean hashes are linked in `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`. The notebooks remain the canonical execution record; generated `.py` mirrors exist to simplify code search, static review and text-based diffing.

## Repository structure

```text
notebooks/                         canonical source-clean notebooks after materialization
scripts/                           deterministic mirror generator + integrity audit
archive/frozen_notebook_payloads/  immutable NB02–NB08 reconstruction payloads
config/                            frozen nested-LOEO protocol
results/main_tables/               seven frozen manuscript tables
results/SUPPLEMENTARY_EVIDENCE_MANIFEST.md  S1–S14 inventory and SHA-256
results/                           frozen numerical facts and figure/table manifests
docs/                              data, statistics, provenance and reproducibility documentation
.github/workflows/                 repository-integrity audit
```

The technical payload archive is intentionally isolated from the reviewer-facing root and never participates in scientific inference. It is a provenance/recovery mechanism only.

## Reproduce or inspect the analysis

1. Download the original Bath dataset using DOI `10.15125/BATH-01459`.
2. Place the four source archives under the project's `01_RAW_ZIPS/` directory as documented in `docs/REPRODUCIBILITY.md`.
3. Install the environment from `requirements.txt` or `environment.yml`.
4. Run `python scripts/rebuild_analysis_mirrors.py` to materialize and verify the frozen source code.
5. Run `python scripts/audit_repository.py` before executing any analysis.
6. Execute NB01–NB08 in the frozen order shown above when full computational reproduction is required.
7. Compare manuscript claims against `docs/MANUSCRIPT_EVIDENCE_MAP.md`, `results/main_tables/`, and `results/SUPPLEMENTARY_EVIDENCE_MANIFEST.md`.

## Important exclusions and safeguards

- The known NB02 `external_support_distance_ratio` diagnostic is **not used as manuscript evidence** because exact duplicate spectral feature vectors produced a zero denominator in several scenarios.
- External post-hoc best models are descriptive and are never presented as leakage-safe deployment selections.
- SMOTE is applied only inside training data.
- Probability calibration is fitted from development-only cross-fitted predictions; NB06-v1.1 changes calibration values only, not classifier training or outer predictions.
- Raw data archives and large row-level prediction dumps are intentionally not committed to Git.
- The repository audit treats the nine source-clean notebook SHA-256 values as frozen provenance checks; an unintended analytical-code change therefore fails the audit.

## Data and code availability

See `docs/DATASET.md`, `docs/DATA_AVAILABILITY.md`, `docs/REPRODUCIBILITY.md`, `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`, `docs/MANUSCRIPT_EVIDENCE_MAP.md` and `docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md`.

## Citation

Citation metadata are provided in `CITATION.cff`. A versioned release and archival DOI can be added before journal submission.

## License

The analysis code is distributed under the MIT License. The source dataset retains its original CC BY 4.0 license and is not relicensed by this repository.
