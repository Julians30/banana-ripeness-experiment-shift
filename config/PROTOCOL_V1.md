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

- **per-experiment Macro-F1 on classes observed in the held-out experiment**, used as the primary fold-specific external endpoint in the revised manuscript; and
- **pooled/fixed-label Macro-F1 on labels 1–5**, retained as a sensitivity/summary measure across out-of-experiment predictions.

This distinction is necessary because Test 2 contains no stage-5 observations and stage support differs across experiments.

Secondary metrics: balanced accuracy, MCC, QWK, ordinal MAE, ±1-stage accuracy, >=2-stage error rate, Brier, NLL, ECE and risk–coverage.

## Model candidates

Ordinal Logistic Regression; PLS-DA; SVM-RBF; Random Forest; XGBoost.

## Exploratory structure

PCA and UMAP are descriptive. For held-out projections, the embedding/preprocessing is learned on development data only.

## Post-freeze reviewer additions

Reviewer-requested count audits, the development-majority no-skill baseline, explicit stage-matching sample sizes, uncertainty visualization for domain AUC, the direct selection-loss panel, and TreeSHAP explanation were added after the confirmatory pipeline. They do not alter the frozen outer predictions, model rankings, calibration fits, or confirmatory numerical evidence.

**Status:** validation design frozen before confirmatory model comparison. The explanatory clarifications above document how the frozen outputs map to the revised manuscript; they do not change `nested_loeo_protocol_v1.json`.
