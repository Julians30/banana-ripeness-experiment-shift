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

Across the 12 frozen scenarios, the internal winner matched the external winner in 1/12 cases.

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
