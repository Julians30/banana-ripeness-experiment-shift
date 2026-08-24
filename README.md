# Banana Ripeness Experiment Shift

Reproducible code and frozen evidence for the study:

**Model-Selection Instability and Loss of Probabilistic Reliability under Experiment Shift in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation**

## Research question

To what extent do machine-learning models for multisensor banana-ripeness classification preserve predictive performance, model-selection decisions, and probabilistic reliability when evaluated on acquisition experiments that were completely excluded from model development?

## Study design

The analysis uses the University of Bath public dataset **Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”** (DOI: `10.15125/BATH-01459`, CC BY 4.0).

The primary four-experiment analysis uses the TPHiS data and evaluates three sensor representations:

- TPH
- Spectral
- TPH + Spectral

Five machine-learning algorithms are evaluated:

- Ordinal Logistic Regression
- PLS-DA
- SVM-RBF
- Random Forest
- XGBoost

The confirmatory design is a nested **Leave-One-Experiment-Out (LOEO)** framework. For each outer fold, one complete experiment is held out from all preprocessing, hyperparameter selection, model selection, calibration fitting, and resampling decisions.

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
06-v1.1 Wide-range temperature scaling correction
        ↓
07 Final statistical inference
        ↓
08 Final manuscript tables and figures
```

NB06-v1.1 supersedes NB06 only for the **final temperature-scaling values**. NB06 is retained for auditability and provenance.

## Frozen main results

Across 17,662 original TPHiS observations, four independent external experiments, three sensor modalities, and five algorithms:

- External model cells: **60**
- Frozen outer-experiment × modality selection scenarios: **12**
- Internal winner = external winner: **1/12 (8.3%)**
- Mean model-selection loss: **0.1147 Macro-F1**
- Maximum model-selection loss: **0.2148 Macro-F1**
- Mean inner-vs-external Spearman rank correlation: **−0.0754**
- Partial η² for held-out experiment on external Macro-F1: **0.4661**
- Partial η² for algorithm: **0.0531**
- Mean ECE of internally selected models: **0.4387 → 0.2568** after development-only temperature scaling
- Mean imbalance-related Macro-F1 change: approximately **+0.004** for both class weighting and training-only SMOTE, with heterogeneous effects across experiments

These results indicate that experiment identity and distribution shift can dominate algorithm choice, destabilize model selection, and reduce the transportability of probabilistic confidence.

## Statistical scope

Only the **four held-out experiments** are treated as independent generalization units. Row-level bootstrap intervals quantify uncertainty conditional on each experiment and must not be interpreted as population-level confidence intervals over independent experiments.

The factorial ANOVA in NB07 is used for **descriptive structural effect-size decomposition**. Its conventional p-values are not treated as confirmatory population inference.

## Repository structure

```text
notebooks/       Executable analysis notebooks
config/          Frozen LOEO protocol and analysis configuration
docs/            Dataset, reproducibility, statistical and data-availability notes
results/         Frozen manuscript-facing numerical results
.github/         Automated repository audit
```

## Data availability

The raw dataset is **not redistributed in this repository**. Obtain it from the original University of Bath record:

- DOI: https://doi.org/10.15125/BATH-01459

The repository records the frozen analysis protocol, source provenance and key result artifacts required to reproduce the reported workflow.

## Known excluded diagnostic

The NB02 variable `external_support_distance_ratio` is intentionally excluded from manuscript evidence because exact duplicate Spectral feature vectors caused the development second-nearest-neighbor median to equal zero in several scenarios. PCA, UMAP, stage-matched domain-classifier AUC and MMD diagnostics are unaffected and retained.

## Reproducibility

Run notebooks in numerical order. See [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) for the exact execution hierarchy and methodological guardrails.

## License

Code in this repository is released under the MIT License. The original dataset retains its own CC BY 4.0 license and is not relicensed by this repository.

## Citation

Citation metadata is provided in [`CITATION.cff`](CITATION.cff). A versioned release and archival DOI can be added when the manuscript is frozen for submission.
