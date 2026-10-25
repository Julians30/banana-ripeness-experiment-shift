# Manuscript evidence map

## Current submission (Chemometrics and Intelligent Laboratory Systems)

The table and figure numbering of the submitted manuscript, with the source file of every item and the SHA-256 of every embedded figure, is in [`../results/chemolab_submission/README.md`](../results/chemolab_submission/README.md) and `../results/chemolab_submission/figure_provenance.csv`. Key correspondences with the numbering used below:

| Previous submission | Current submission |
|---|---|
| Figure 1 (domain AUC) | Figure 2 (AUC and MMD²) |
| Figure 2 (selected-model heatmap) | removed; values in Table 4 |
| Figure 3 | Figure 3 |
| Figure 4 (ECE) | Figures 4–5 (reliability diagrams with bin support) |
| Figure 5 (partial η²) | removed; values in Table 5 |
| Figure S1 / S2 / S3 | Figure S2 / S3 / S1 |
| Table S2 (no-skill baseline) | Table S3 |
| Table S3 (stage-matched n) | Table S2 |
| — | Figures 1, 6–11, S4–S15; Tables 6, S4, S5 (post-hoc layer, `../results/post_hoc/`) |

The remainder of this document records claim-level traceability using the **previous-submission numbering** and is retained for provenance.

---

This document links the **current revised manuscript** to frozen analytical evidence and reviewer-requested explanatory additions. It is a traceability layer; it does not introduce new confirmatory analysis.

## Evidence layers

The repository deliberately separates two layers:

1. **Frozen analytical evidence** — NB01–NB08, the frozen LOEO protocol, `results/main_tables/`, and `results/frozen_numeric_facts_nb08.json`.
2. **Current revised-manuscript presentation/reviewer evidence** — `results/manuscript_current/` and `results/reviewer_revision/`.

Reviewer-requested additions never replace or modify frozen outer predictions, model rankings, calibration fits, or confirmatory numerical values.

## Scope and data reconstruction

| Current manuscript claim | Current presentation artifact | Frozen / source evidence | Interpretation constraint |
|---|---|---|---|
| Confirmatory analysis uses 17,662 inferred-original TPHiS observations from four experiments. | current Table 1; mapping in `results/table_manifest.csv` | NB01; `results/frozen_numeric_facts_nb08.json` | Counts describe the audited original block only. |
| The inferred balancing tail exactly fills class deficits to 6,533 per stage. | `results/reviewer_revision/Table_S1_reconstruction_count_audit.csv` | NB01 source-index reconstruction; `scripts/09_REVIEWER_REQUESTED_AUDITS.py` | Source ordering supports the inference but is not a demonstrated time variable or author-provided synthetic flag. |
| Nested LOEO isolates a complete acquisition experiment from development. | `config/nested_loeo_protocol_v1.json`; `docs/REPRODUCIBILITY.md` | NB01, NB03, NB04 | External rows cannot influence preprocessing, tuning, resampling, calibration, or algorithm selection. |

## Experiment shift

| Current manuscript claim | Current presentation artifact | Frozen / source evidence | Interpretation constraint |
|---|---|---|---|
| Experiment identity remains strongly recoverable after matching on ripeness stage. | current Table 3; mapping in `results/table_manifest.csv`; current Figure 1; checksum in `results/manuscript_current/figures/README.md` | NB02; frozen analytical `Table_2_experiment_shift_diagnostics.csv` | Error bars are repeated-CV variability, not confidence intervals over independent experiments. |
| Actual matched sample sizes vary substantially by stage. | `results/reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv` | source-index experiment mapping; `scripts/09_REVIEWER_REQUESTED_AUDITS.py` | `matched n/domain = min(n_dev, n_external, 600)`; matching precedes modality construction. |
| The preliminary nearest-neighbor support-ratio diagnostic is excluded. | documentation only | NB02 | Do not use `external_support_distance_ratio` because duplicate spectral vectors generated zero denominators. |

## Confirmatory predictive transportability

| Current manuscript claim | Current presentation artifact | Frozen evidence | Interpretation constraint |
|---|---|---|---|
| Internally selected models frequently lose external performance. | current Table 4; mapping in `results/table_manifest.csv`; Figure 2 | frozen `Table_3_confirmatory_external_selected_models.csv`; NB04 | Post-hoc external best models are descriptive comparators only. |
| Internal winner = post-hoc external winner in 1/12 scenarios. | Current Table 4; current Figure 3 | frozen `Table_4_model_selection_instability_summary.csv`; `frozen_numeric_facts_nb08.json` | This is observed model-selection transportability, not a population probability over future experiments. |
| Mean selection loss = 0.114728 Macro-F1; max = 0.214790. | Current Table 4; current Figure 3 | frozen `Table_4_model_selection_instability_summary.csv`; NB04/NB07 | Selection loss is defined relative to the post-hoc external best model. |
| Mean inner–external rank association is approximately null. | Current Table 5 synthesis | frozen `Table_4_model_selection_instability_summary.csv` | Descriptive across 12 experiment × modality scenarios. |

## Trivial baseline

| Current manuscript claim | Current presentation artifact | Source evidence | Interpretation constraint |
|---|---|---|---|
| Development-majority no-skill Macro-F1 is 0.000, 0.073, 0.070 and 0.075 for Tests 2–5. | `results/reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv` | `scripts/09_REVIEWER_REQUESTED_AUDITS.py` | Majority class is determined from development experiments only; external labels are used only for scoring. |

## Imbalance sensitivity

| Current manuscript claim | Current presentation artifact | Frozen evidence | Interpretation constraint |
|---|---|---|---|
| Class weighting and training-only SMOTE change mean Macro-F1 by only about +0.004. | Current Table 5; Figure S1 | frozen `Table_5_imbalance_sensitivity.csv`; NB05/NB07 | Effects are heterogeneous across four experiments; sign-flip p-values have coarse resolution. |
| SMOTE can worsen ordinal error structure. | discussion + Figure S1 context | NB05 | Synthetic interpolation should not be interpreted as repairing experiment shift. |

## Probabilistic reliability

| Current manuscript claim | Current presentation artifact | Frozen evidence | Interpretation constraint |
|---|---|---|---|
| Development-only temperature scaling improves average ECE and NLL. | Current Table 5; `Figure_4_ece_raw_vs_temperature_scaled.png`; Figure S2 | frozen `Table_6_probabilistic_calibration_selected_models.csv`; NB06-v1.1 | NB06-v1.1 is authoritative for final temperature values. |
| Mean ECE 0.438699 → 0.256772; mean NLL 4.616133 → 1.768828. | Current Table 5 / Figure 4 | `frozen_numeric_facts_nb08.json` | Average improvement does not imply uniform calibration transfer. |
| Three selected temperature fits reached the upper bound. | frozen Table 6 / manuscript text | NB06-v1.1 | Indicates severe calibration mismatch in particular development folds, not an optimization crash. |

## Structural effect-size decomposition

| Current manuscript claim | Current presentation artifact | Frozen evidence | Interpretation constraint |
|---|---|---|---|
| Held-out experiment contributes much more Macro-F1 variation than algorithm identity. | Current Table 5; Figure 5 | frozen `Table_7_structural_effect_sizes.csv`; NB07 | partial eta-squared: experiment 0.466088, algorithm 0.053088. |
| Factorial OLS/ANOVA is descriptive. | manuscript text; `docs/STATISTICAL_ANALYSIS.md` | NB07 | Conventional ANOVA p-values are not population-level confirmatory inference. |
| Residual variation remains substantial. | manuscript discussion | NB07 model R² = 0.516 | Residual variation may contain unmodeled interactions, biological variability, sensor noise, and acquisition microconditions; these are plausible sources, not separately identified causal components. |

## Reviewer-requested TreeSHAP explanation

| Current manuscript claim | Current presentation artifact | Analytical basis | Interpretation constraint |
|---|---|---|---|
| Spectral tree explanations emphasize visible-green and selected NIR bands. | `Figure_S3_treeshap_spectral_tree_models.png` (checksum in `results/manuscript_current/figures/README.md`) | Post-hoc TreeSHAP using spectral RF/XGBoost and frozen NB03 hyperparameters | Explanatory only; no role in tuning/model selection; attribution may mix ripeness and experiment-specific signal. |
| TreeSHAP is not causal biochemical attribution. | `results/reviewer_revision/README.md` | manuscript discussion | Do not claim that a band's SHAP value proves a specific physiological mechanism. |

## Current manuscript presentation manifest

The exact current presentation layer is indexed by:

- `results/figure_manifest.csv`
- `results/table_manifest.csv`
- `results/reviewer_revision/manifest.csv`

## Evidence exclusions and safeguards

- Do not use `external_support_distance_ratio` as manuscript evidence.
- Do not present post-hoc external winners as deployable leakage-safe selections.
- Preserve NB06 for provenance; use NB06-v1.1 for final temperature-scaling values.
- Treat row-level bootstrap intervals as conditional within each held-out experiment.
- Treat only four held-out experiments as independent generalization units.
- Treat TreeSHAP as post-hoc explanatory evidence, not confirmatory or causal evidence.
- Do not modify `results/frozen_numeric_facts_nb08.json` outside a formally rerun and re-audited analysis.
