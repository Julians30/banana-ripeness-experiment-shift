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

The revised manuscript uses per-experiment observed-class Macro-F1 as its primary fold-specific external endpoint. Fixed-label 1–5 Macro-F1 remains available as a sensitivity/summary metric.

## Known NB02 exclusion

Do not use `external_support_distance_ratio` in the manuscript. Exact duplicate spectral feature vectors caused a zero denominator in several folds. PCA, UMAP, stage-matched domain AUC and MMD remain valid.

## Reviewer-requested post-freeze additions

Peer-review/audit requests produced a separate explanatory layer without modifying the frozen confirmatory pipeline:

- reconstruction count audit (current Table S1);
- development-majority no-skill baseline (current Table S2);
- explicit stage-matched effective sample sizes (current Table S3);
- repeated-CV variability shown with domain AUC (current Figure 1);
- direct selected-vs-post-hoc-best selection-loss panel (current Figure 3);
- corrected near-zero calibrated-ECE visibility (current Figure 4);
- post-hoc TreeSHAP explanation of frozen spectral tree-model fits (current Figure S3).

Current presentation files are versioned under:

- `results/manuscript_current/`
- `results/reviewer_revision/`

Tables S1–S3 can be regenerated directly from the original TPHiS archive with:

```bash
python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/reviewer_revision
```

TreeSHAP is explanatory only and uses already-frozen NB03 spectral Random Forest/XGBoost hyperparameters; it has no role in preprocessing, tuning, model selection, calibration or confirmatory external performance estimation.

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
- current revised-manuscript table mappings and exact embedded-figure SHA-256 provenance;
- reviewer-requested Tables S1–S3 and explanatory-scope documentation;
- pinned Python/package metadata and four-author `CITATION.cff`;
- manuscript-evidence traceability;
- repository file policy.

GitHub Actions runs the same read-only audit on pushes and pull requests. It does not create commits or push generated files back to the repository.

## Environment

Final analytical runs used **Python 3.13.15** in Google Colab.

Pinned package versions are recorded in `requirements.txt` and `environment.yml`. `shap==0.50.0` is included for the reviewer-requested explanatory analysis.

## Data path adaptation

The notebooks were developed in Google Colab with the project rooted at:

`/content/drive/MyDrive/Paper3_Banano/BANANA_RIPENESS_MULTISENSOR_Q1`

For execution outside that workspace, change only the project-root variable while preserving the documented folder hierarchy, source archives and frozen protocol.
