# Frozen validation protocol V1 — Banana multisensor

**Primary design:** nested Leave-One-Experiment-Out (LOEO) on inferred-original observations only.

## Outer folds

| Outer test | Development experiments | External experiment |
|---|---|---|
| 2 | 3, 4, 5 | 2 |
| 3 | 2, 4, 5 | 3 |
| 4 | 2, 3, 5 | 4 |
| 5 | 2, 3, 4 | 5 |

Within each outer development set, hyperparameters are selected by leaving one development experiment out at a time.

## Leakage rules

- External test rows are never used to fit scalers, PCA, UMAP, feature selection, resampling, hyperparameters, calibration or thresholds.
- SMOTE, when tested, occurs only within inner-training data.
- Test 5 streams remain grouped; they are never split across development and external test.
- The provided random train/test columns are retained only for protocol-replication/sensitivity analyses and are not used as the primary validation design.

## Metrics and estimands

The frozen computational protocol produces both:

- **per-experiment Macro-F1 on classes observed in the held-out experiment**, used as the primary fold-specific external endpoint in the manuscript; and
- **pooled/fixed-label Macro-F1 on labels 1–5**, retained as a sensitivity/summary measure across out-of-experiment predictions.

This distinction is necessary because Test 2 contains no stage-5 observations and stage support differs across experiments.

Secondary metrics: balanced accuracy, MCC, QWK, ordinal MAE, ±1-stage accuracy, >=2-stage error rate, Brier, NLL, ECE and risk–coverage.

## Model candidates and frozen grids (manuscript Table 2)

Exact candidate configurations of NB03 (`candidate_grid()`; reconstruct NB03 with `python scripts/rebuild_analysis_mirrors.py`). Scaling is fitted on the training partition only.

| Algorithm | Preprocessing | Candidates |
|---|---|---|
| Ordinal logistic regression (`mord.LogisticAT`) | StandardScaler | alpha = 0.01, 0.1, 1, 10 |
| PLS-DA (`PLSRegression`, scale=False, one-hot targets) | StandardScaler | TPH: 1, 2, 3 components; Spectral and fused: 2, 4, 8 |
| SVM-RBF | StandardScaler | (C, gamma) = (0.5, scale), (2, scale), (8, scale), (8, 0.03) |
| Random forest | none | 400 trees; (max_depth, min_samples_leaf, max_features) = (None, 1, sqrt), (18, 1, sqrt), (None, 3, sqrt), (None, 1, 0.7) |
| XGBoost | none | subsample = colsample_bytree = 0.9; (n_estimators, max_depth, learning_rate) = (250, 3, 0.05), (350, 5, 0.05), (250, 3, 0.10), (500, 2, 0.03) |

Within each outer fold and modality, the configuration of each algorithm is chosen by mean inner-validation Macro-F1 over the three inner folds (ties broken by worst-fold Macro-F1, mean QWK, mean ordinal MAE, candidate order); the five algorithms are then ranked by the same criterion and the rank-1 algorithm is the internally selected model.

**NB17 re-implementation.** The post-hoc NB17 notebook (positive control, MSC, alternative calibrators) was coded independently. It uses the same algorithms, preprocessing and ordinal-logistic, PLS-DA and SVM candidates, but its tree-ensemble candidates differ: random forest uses the full 2 × 2 × 2 factorial of the values above (8 configurations) and XGBoost uses (250, 2, 0.10), (250, 3, 0.05), (500, 4, 0.03), (500, 5, 0.05). Its nested LOEO arm reproduced the frozen selected model in 11/12 scenarios and the external Macro-F1 to three decimals in 10/12 (`results/post_hoc/nb17_reviewer_shield/A_check_vs_table4.csv`); both differences (Test 2 with TPH and with Spectral) are scenarios in which a tree ensemble was selected. NB17 results are therefore reported as sensitivity analyses; confirmatory values come only from NB03/NB04.

## Exploratory structure

PCA and UMAP are descriptive. For held-out projections, the embedding/preprocessing is learned on development data only.

## Post-freeze additions

Added after the confirmatory pipeline, without altering frozen outer predictions, model rankings, calibration fits or confirmatory numerical evidence:

- reviewer-requested count audit, development-majority no-skill baseline, stage-matched sample sizes, repeated-CV uncertainty for domain AUC, selection-loss panel and TreeSHAP explanation (current Tables S1–S3, Figures 2, 3 and S1);
- post-hoc robustness notebooks NB09–NB12 (random references, spectral normalization, duplicate-aware and shared-signature analyses), NB14–NB15 (prospective initial-window DOMAIN_Z, composition stress, feature displacement, loadings, projections), NB16 (reliability diagrams) and NB17 (positive control, MSC, alternative calibrators). Evidence: `results/post_hoc/`; map: `results/chemolab_submission/README.md`.

**Status:** validation design frozen before confirmatory model comparison. The explanatory clarifications above document how the frozen outputs map to the manuscript; they do not change `nested_loeo_protocol_v1.json`.
