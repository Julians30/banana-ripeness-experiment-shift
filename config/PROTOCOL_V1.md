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

## Metrics

Primary pooled metric: Macro-F1 over all out-of-experiment predictions using labels 1–5.
Per-experiment Macro-F1: calculated over stages present in that target experiment; Test 2 contains no stage-5 observations.
Secondary: balanced accuracy, MCC, QWK, ordinal MAE, ±1-stage accuracy, >=2-stage error rate, Brier, NLL, ECE and risk–coverage.

## Model candidates

Ordinal Logistic Regression; PLS-DA; SVM-RBF; Random Forest; XGBoost.

## Exploratory structure

PCA and UMAP are descriptive. For held-out projections, the embedding/preprocessing is learned on development data only.

**Status:** frozen before confirmatory model comparison.
