# Reproducibility workflow

## Execution order

Run the notebooks in the following order:

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

## Version hierarchy

`06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb` is the authoritative calibration version for final manuscript values. The original NB06 is retained to document the initial temperature range and the subsequent numerical correction. The correction does not alter classifier training, outer predictions, model selection, or class labels.

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

- NB02: descriptive experiment-shift characterization.
- NB03: leakage-safe internal hyperparameter/model selection.
- NB04: confirmatory external predictive evaluation.
- NB05: pre-specified imbalance-treatment sensitivity.
- NB06-v1.1: final probabilistic calibration analysis.
- NB07: final statistical synthesis.
- NB08: presentation and packaging only; no new analytical decision.

## Statistical hierarchy

Only the four held-out experiments are independent generalization units. Row-level paired/bootstrap analyses quantify uncertainty conditional on each experiment. They are not population-level inference over new experiments.

The NB07 factorial ANOVA is retained only as a structural effect-size decomposition. Conventional ANOVA p-values are not interpreted as confirmatory evidence because the 60 model × modality × experiment cells are not 60 independent experiments.

## Known NB02 exclusion

Do not use `external_support_distance_ratio` in the manuscript. Exact duplicate spectral feature vectors caused a zero denominator in several folds. PCA, UMAP, stage-matched domain AUC and MMD remain valid.

## Environment

The final analytical runs used Python 3.13.15 in Google Colab. Tested package versions are recorded in `requirements.txt` and `environment.yml`.

## Data path adaptation

The notebooks were developed in Google Colab with the project rooted at:

`/content/drive/MyDrive/Paper3_Banano/BANANA_RIPENESS_MULTISENSOR_Q1`

For execution outside that workspace, change the project-root variable while preserving the documented folder hierarchy and frozen protocol.
