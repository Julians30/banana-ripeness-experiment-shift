# Statistical analysis hierarchy

## Primary endpoint

The primary predictive endpoint is **Macro-F1**.

For each held-out experiment, fold-specific Macro-F1 is computed over the classes actually observed in that external experiment. A fixed-label 1–5 Macro-F1 is retained as a sensitivity analysis because stage support differs across experiments.

## Secondary predictive metrics

- Balanced accuracy
- Matthews correlation coefficient (MCC)
- Quadratic weighted kappa (QWK)
- Ordinal mean absolute error
- Within ±1-stage accuracy
- Severe error rate (absolute stage error >=2)

## Probabilistic metrics

ECE uses 15 equal-width confidence bins. Temperature scaling is fitted on development-only cross-fitted predictions (NB06-v1.1 is authoritative). Mean selected-model ECE is 0.497 → 0.257 for the 10 scenarios with native probabilities (manuscript) and 0.4387 → 0.2568 over all 12 selected models including softmax surrogates (`results/frozen_numeric_facts_nb08.json`).


- Negative log-likelihood (NLL)
- Brier score
- Expected calibration error (ECE)
- Ranked probability score (RPS)
- Risk–coverage / selective classification diagnostics

## Model-selection transportability

For each outer experiment × modality scenario, NB03 freezes the internal model ranking before the outer test is opened. NB04 then quantifies:

- whether the internal winner equals the post-hoc external winner;
- selection loss in Macro-F1;
- Spearman correlation between internal and external model ranks;
- Kendall correlation between internal and external model ranks.

Across the 12 frozen scenarios, the internal winner matched the external winner in 1/12 cases. NB09 compares this agreement rate and the mean selection loss with a random-selection null; neither is independently unusual under that null, so the manuscript interprets selection instability as a consequence of the loss of transferable signal rather than of a defective selection rule.

## Planned paired bootstrap

NB07 compares the internal rank-1 and rank-2 models on the same external observations using paired, stage-stratified bootstrap resampling (2,000 replicates per planned contrast).

These confidence intervals are **conditional within the held-out experiment**. They are not confidence intervals over a population of independent experiments.

## Structural effect-size decomposition

A factorial OLS/ANOVA representation is used descriptively to decompose external Macro-F1, QWK and ordinal MAE into contributions from:

- held-out experiment;
- sensor modality;
- algorithm;
- modality × algorithm interaction.

Partial eta-squared values are interpreted as descriptive structural effect sizes. Conventional ANOVA p-values are not used as primary confirmatory evidence.

For external Macro-F1, the frozen partial eta-squared estimates are approximately:

- Held-out experiment: 0.466
- Modality: 0.035
- Algorithm: 0.053
- Modality × algorithm: 0.091

## Experiment-level exact tests

Because there are only four independent outer experiments, NB07 uses exact two-sided sign-flip tests as a conservative experiment-level summary for imbalance and calibration effects. With n=4, the minimum attainable two-sided p-value is 0.125; these tests are therefore interpreted primarily through effect magnitude, sign consistency and heterogeneity rather than significance thresholds.

## Multiplicity and scope

The study emphasizes pre-specified contrasts, effect sizes and cross-experiment consistency. It does not treat the 60 external model cells or the 17,662 rows as independent generalization replicates.

## Post-hoc analyses and their inferential status

All post-hoc analyses are reported as robustness or mechanism-oriented evidence; none changes the confirmatory estimates.

- **Reference forecasts (NB09).** Uniform and development-prevalence probability forecasts give the non-informative NLL/Brier references used to read calibrated scores.
- **Spectral normalization (NB10–NB12).** SNV and complete-target DOMAIN_Z are evaluated under the same nested LOEO procedure. Complete-target DOMAIN_Z uses statistics of the whole target experiment and is therefore transductive.
- **Prospective initial-window normalization (NB14).** DOMAIN_Z statistics are estimated from the first N = 10, 25 or 50 unique target spectra (acquisition order approximated by the source index) and models are scored only on later records. With four experiments, exact sign-flip tests cannot reach p < 0.125; results are read through effect size and sign consistency.
- **Composition stress (NB14).** Calibration windows of fixed size are resampled with controlled stage composition; this uses target labels and is a diagnostic of composition sensitivity, not a deployable procedure.
- **Displacement and localization (NB15).** Development-fitted PCA/UMAP projections, loadings and per-record errors; row and signature-cluster resampling intervals are conditional on frozen predictions.
- **Positive control (NB17).** The same model families are evaluated under pooled stratified random 5-fold CV (inner random 3-fold selection) and stratified 5-fold CV within each experiment. These splits place near-identical repeated readings in training and test partitions and are reported only to show that ripeness is separable within an acquisition experiment.
- **MSC and alternative calibrators (NB17).** MSC (training-partition mean reference) is compared with RAW and SNV under nested LOEO; vector scaling and one-vs-rest isotonic regression are fitted to the same cross-fitted development probabilities as temperature scaling.
