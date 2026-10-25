# Reproducibility workflow

## Execution order

Run the frozen analytical notebooks in this order:

```text
01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb
02_PCA_UMAP_DOMAIN_SHIFT.ipynb
03_INNER_LOEO_MODEL_SELECTION.ipynb
04_OUTER_LOEO_EVALUATION.ipynb
05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb
06_CALIBRATION_RELIABILITY_ORDINAL.ipynb
06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb
07_FINAL_STATISTICAL_INFERENCE.ipynb
08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb
```

`06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb` is authoritative for final manuscript temperature-scaling values. NB06 is retained to document the original temperature range and subsequent numerical correction. The correction does not alter classifier training, outer predictions, model selection, or class labels.

## Source archives

Download the original University of Bath dataset identified by DOI `10.15125/BATH-01459`.

NB01 expects:

```text
ds_34.zip
Spect.zip
TPHiS.zip
VOC.zip
```

Place them under the project `01_RAW_ZIPS/` directory before running NB01. Raw archives are intentionally not redistributed here.

## Frozen notebook provenance

NB01 is committed directly in `notebooks/`.

Exact source-clean NB02–NB08 bytes are stored under:

`archive/frozen_notebook_payloads/`

Materialize all nine notebooks and text-readable Python mirrors with:

```bash
python scripts/rebuild_analysis_mirrors.py
```

The utility verifies frozen SHA-256 and byte size before writing generated local files.

## Leakage-safe rules

For every outer LOEO fold:

1. The external experiment is isolated before any model-development operation.
2. Scaling and feature transformations are fit only on development data.
3. Hyperparameters and model ranks are determined by inner experiment-disjoint validation.
4. SMOTE, when evaluated, is applied only to training data.
5. Class weighting is used only where the estimator genuinely supports weighting.
6. Probability calibration is fitted from development-only cross-fitted predictions.
7. The external experiment is used only for final evaluation of frozen decisions.
8. No model is selected from outer-test performance.

## Analytical roles

- NB01: source audit, original-block reconstruction, experiment mapping and frozen split protocol.
- NB02: descriptive experiment-shift characterization.
- NB03: leakage-safe internal hyperparameter/model selection.
- NB04: confirmatory external predictive evaluation.
- NB05: pre-specified imbalance-treatment sensitivity.
- NB06-v1.1: final probabilistic calibration analysis.
- NB07: final statistical synthesis.
- NB08: frozen evidence packaging/presentation; no new model-development decision.

## Statistical hierarchy

Only the four held-out experiments are independent generalization units. Row-level paired/bootstrap analyses quantify uncertainty conditional on each experiment; they are not population-level inference over future experiments.

The NB07 factorial OLS/ANOVA is retained only as structural effect-size decomposition. Conventional ANOVA p-values are not interpreted as confirmatory evidence because the 60 model × modality × experiment cells are not 60 independent experiments.

The manuscript uses per-experiment observed-class Macro-F1 as its primary fold-specific external endpoint. Fixed-label 1–5 Macro-F1 remains available as a sensitivity/summary metric.

## Known NB02 exclusion

Do not use `external_support_distance_ratio` in the manuscript. Exact duplicate spectral feature vectors caused a zero denominator in several folds. PCA, UMAP, stage-matched domain AUC and MMD remain valid.

## Reviewer-requested post-freeze additions

Peer-review/audit requests produced a separate explanatory layer without modifying the frozen confirmatory pipeline (numbering of the current submission):

- reconstruction count audit (Table S1);
- explicit stage-matched effective sample sizes (Table S2);
- development-majority no-skill baseline (Table S3);
- repeated-CV variability shown with domain AUC (Figure 2);
- direct selected-vs-post-hoc-best selection-loss panel (Figure 3);
- post-hoc TreeSHAP explanation of frozen spectral tree-model fits (Figure S1).

Tables S1–S3 are in `results/reviewer_revision/` and can be regenerated directly from the original TPHiS archive with:

```bash
python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/reviewer_revision
```

TreeSHAP is explanatory only and uses already-frozen NB03 spectral Random Forest/XGBoost hyperparameters; it has no role in preprocessing, tuning, model selection, calibration or confirmatory external performance estimation.

The previous-submission numbering is preserved, for provenance only, in `results/manuscript_current/`.

## Post-hoc robustness layer (NB09–NB17)

| Notebook | Analysis (manuscript section) | Evidence in this repository |
|---|---|---|
| NB09 | uniform/development-prevalence references; random-selection null (2.11) | `results/post_hoc/nb09_random_references/` |
| NB10 | SNV and complete-target DOMAIN_Z under nested LOEO (2.11, 3.7) | `results/post_hoc/nb10_spectral_normalization/`; Figure 6 |
| NB11–NB12 | duplicate-aware statistics; removal of shared spectral signatures (2.11, 3.7) | `results/post_hoc/nb11_duplicate_aware/`, `results/post_hoc/nb12_shared_signature_removal/`; Figure S11 |
| NB14 | prospective initial-window DOMAIN_Z, window sensitivity, composition stress (2.12, 3.8) | `results/post_hoc/nb14_prospective_domain_z/` |
| NB15 | feature displacement, PCA loadings, PCA/UMAP projections, error localization (2.12, 3.7–3.8) | `results/post_hoc/nb15_spectral_error_audit/` |
| NB16 | reliability diagrams with bin support, no refitting (3.5) | `results/post_hoc/nb16_reliability_diagrams/` |
| NB17 | positive control, MSC, alternative calibrators (2.13, 3.9) | `notebooks/post_hoc/`, `results/post_hoc/nb17_reviewer_shield/` |

All post-hoc notebooks (NB09–NB12, NB14–NB17) are in `notebooks/post_hoc/`, linked to the executed notebooks by SHA-256 in `notebooks/post_hoc/notebook_provenance.csv`. NB17 runs in Colab or locally (set `NB17_MASTER_CSV`). NB17 coded its own candidate grid; its tree-ensemble candidates differ from NB03 (see `config/PROTOCOL_V1.md`), which explains the two scenarios in which it does not reproduce manuscript Table 4 exactly.

## Publication figures

All 26 figures embedded in the submitted manuscript and supplementary file are in `results/chemolab_submission/figures/` (PNG as embedded, plus vector PDF where available); their SHA-256 values are listed in `results/chemolab_submission/figure_provenance.csv` and checked by the audit. They can be regenerated from tracked files:

```bash
pip install -r requirements-figures.txt
python scripts/make_publication_figures.py --out figures_out      # Figs. 1, 2, 7-11, S8-S10, S12-S15
python scripts/postprocess_legacy_figures.py --out figures_out    # Figs. 3-6, S1-S7, S11
python scripts/verify_figures.py figures_out
```

With the versions in `requirements-figures.txt` all 26 PNGs are byte-identical to the submitted files; other matplotlib/Pillow versions may change PNG encoding or anti-aliasing. `postprocess_legacy_figures.py` only removes in-figure titles and re-typesets labels of figures produced by the analytical notebooks (inputs in `results/chemolab_submission/figure_sources/`); plot pixels are not modified.

## Repository integrity audit

Run:

```bash
python scripts/audit_repository.py
```

The audit is read-only and uses only the Python standard library. It verifies:

- frozen notebook provenance and code-cell syntax;
- frozen nested-LOEO semantic hash;
- frozen numerical evidence;
- analytical table inventory;
- previous-submission table mappings and figure SHA-256 provenance (kept for provenance);
- reviewer-requested Tables S1–S3 and explanatory-scope documentation;
- pinned Python/package metadata and the three-author `CITATION.cff`;
- manuscript-evidence traceability;
- repository file policy;
- post-hoc evidence (NB14 key values, NB15 files, NB17 notebook syntax and outputs) and the SHA-256 of all 26 submitted figures.

GitHub Actions runs the same read-only audit, and a second job that regenerates all 26 figures and compares them with the submitted files, on pushes and pull requests. It does not create commits or push generated files back to the repository.

## Environment

Final analytical runs used **Python 3.13.15** in Google Colab.

Pinned package versions are recorded in `requirements.txt` and `environment.yml`. `shap==0.50.0` is included for the reviewer-requested explanatory analysis.

## Data path adaptation

The notebooks were developed in Google Colab with the project rooted at:

`/content/drive/MyDrive/Paper3_Banano/BANANA_RIPENESS_MULTISENSOR_Q1`

For execution outside that workspace, change only the project-root variable while preserving the documented folder hierarchy, source archives and frozen protocol.
