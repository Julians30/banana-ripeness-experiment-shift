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

## Repository structure

```text
notebooks/                  source-clean executable notebooks
config/                     frozen nested-LOEO protocol
results/main_tables/        frozen manuscript tables
results/supplementary_tables/ selected complete supplementary evidence
docs/                       data, statistics and reproducibility documentation
scripts/                    automated repository audit
.github/workflows/          CI reproducibility audit
```

The GitHub notebooks are source-clean copies with bulky execution outputs removed; analytical code is unchanged. Hashes linking them to the executed project notebooks are documented in `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`.

## Reproduce the analysis

1. Download the original Bath dataset using DOI `10.15125/BATH-01459`.
2. Reconstruct the project folders described in `docs/REPRODUCIBILITY.md`.
3. Verify the master-data and frozen-protocol hashes documented in `docs/DATA_AVAILABILITY.md`.
4. Install the environment from `requirements.txt` or `environment.yml`.
5. Execute the notebooks in the order shown above.
6. Run `python scripts/audit_repository.py`.

A matching GitHub Actions workflow executes the structural audit on every push and pull request.

## Important exclusions and safeguards

- The known NB02 `external_support_distance_ratio` diagnostic is **not used as manuscript evidence** because exact duplicate spectral feature vectors produced a zero denominator in several scenarios.
- External post-hoc best models are descriptive and are never presented as leakage-safe deployment selections.
- SMOTE is applied only inside training data.
- Raw data archives and large row-level prediction dumps are intentionally not committed to Git.

## Data and code availability

See `docs/DATASET.md`, `docs/DATA_AVAILABILITY.md`, `docs/REPRODUCIBILITY.md` and `docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md`.

## Citation

Citation metadata are provided in `CITATION.cff`. A versioned release and archival DOI can be added before journal submission.

## License

The analysis code is distributed under the MIT License. The source dataset retains its original CC BY 4.0 license and is not relicensed by this repository.
