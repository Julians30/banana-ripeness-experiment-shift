# Manuscript evidence map

This document links the principal manuscript claims to frozen repository evidence. It is intended as a reviewer-facing traceability layer and does not introduce new analysis.

## Scope and design

| Manuscript claim | Frozen evidence | Analytical source | Interpretation constraint |
|---|---|---|---|
| The confirmatory analysis uses 17,662 original observations from four external experiments, three sensor representations and five algorithms. | `results/frozen_numeric_facts_nb08.json`; `results/main_tables/Table_1_dataset_stage_distribution.csv` | NB01, NB08 | Counts describe the audited TPHiS analysis set. |
| Model development and external evaluation are separated by nested Leave-One-Experiment-Out validation. | `config/nested_loeo_protocol_v1.json`; `docs/REPRODUCIBILITY.md` | NB01, NB03, NB04 | The held-out experiment must remain isolated from preprocessing, hyperparameter selection, algorithm selection, resampling and calibration fitting. |
| The experiments exhibit substantial measurable distribution shift. | `results/main_tables/Table_2_experiment_shift_diagnostics.csv`; `results/figure_manifest.csv` Figure 2 | NB02, NB08 | Use stage-matched domain AUC, MMD, PCA and UMAP evidence. Do not use `external_support_distance_ratio`. |

## Confirmatory predictive transportability

| Manuscript claim | Frozen evidence | Analytical source | Interpretation constraint |
|---|---|---|---|
| Internally selected models frequently lose performance on completely unseen experiments. | `results/main_tables/Table_3_confirmatory_external_selected_models.csv`; Figure 3 | NB04, NB08 | External post-hoc best models are descriptive comparators only. |
| The internally selected winner matches the external post-hoc winner in only 1 of 12 experiment × modality scenarios (8.3%). | `results/main_tables/Table_4_model_selection_instability_summary.csv`; `results/frozen_numeric_facts_nb08.json` | NB04, NB07, NB08 | This is model-selection transportability, not an estimate of a population probability over future experiments. |
| Mean selection loss is 0.114728 Macro-F1 and the maximum observed loss is 0.214790. | `results/main_tables/Table_4_model_selection_instability_summary.csv`; `results/frozen_numeric_facts_nb08.json` | NB04, NB07, NB08 | Selection loss is defined relative to the post-hoc external best model and therefore quantifies the cost of internal model selection under shift. |
| Mean inner-versus-external model-rank agreement is approximately null (Spearman = -0.075414; Kendall = -0.069097). | `results/main_tables/Table_4_model_selection_instability_summary.csv` | NB07, NB08 | Treat these as descriptive summaries across the 12 outer experiment × modality scenarios. |

## Probabilistic reliability

| Manuscript claim | Frozen evidence | Analytical source | Interpretation constraint |
|---|---|---|---|
| Probability estimates lose reliability under experiment shift. | `results/main_tables/Table_6_probabilistic_calibration_selected_models.csv`; Figure 5 | NB06-v1.1, NB08 | NB06-v1.1 is authoritative for final temperature-scaling values. |
| Development-only temperature scaling reduces mean ECE from 0.438699 to 0.256772 and mean NLL from 4.616133 to 1.768828. | `results/frozen_numeric_facts_nb08.json`; `results/main_tables/Table_6_probabilistic_calibration_selected_models.csv` | NB06-v1.1, NB08 | Calibration improves average reliability but does not establish reliable probability transfer in every experiment/modality cell. |
| Three selected temperature fits reached the predefined upper bound. | `results/frozen_numeric_facts_nb08.json`; `results/main_tables/Table_6_probabilistic_calibration_selected_models.csv` | NB06-v1.1, NB08 | Report this as evidence of severe calibration mismatch in specific development folds, not as a numerical optimization failure. |

## Structural dominance of experiment shift

| Manuscript claim | Frozen evidence | Analytical source | Interpretation constraint |
|---|---|---|---|
| Held-out experiment explains substantially more external Macro-F1 variation than algorithm identity. | `results/main_tables/Table_7_structural_effect_sizes.csv`; Figure 6 | NB07, NB08 | Partial eta-squared: held-out experiment = 0.466088; algorithm = 0.053088. |
| The factorial model is used for structural effect-size decomposition, not confirmatory population inference. | `docs/REPRODUCIBILITY.md`; `docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md` | NB07 | Do not interpret conventional ANOVA p-values as evidence over a population of independent experiments. |

## Imbalance-treatment sensitivity

| Manuscript claim | Frozen evidence | Analytical source | Interpretation constraint |
|---|---|---|---|
| Class weighting and training-only SMOTE produce only small average Macro-F1 changes relative to the magnitude of experiment shift. | `results/main_tables/Table_5_imbalance_sensitivity.csv`; Figure S1 | NB05, NB08 | Mean delta Macro-F1 is about +0.004 for each strategy, with heterogeneous experiment-specific effects. |
| With only four independent outer experiments, exact experiment-level sign-flip inference has coarse resolution. | `results/main_tables/Table_5_imbalance_sensitivity.csv`; `docs/REPRODUCIBILITY.md` | NB05, NB07 | The minimum possible two-sided p-value is 0.125 for n = 4. |

## Manuscript-level conclusion supported by the frozen evidence

The repository supports a conclusion about **transportability**, not about a universal best classifier. Across the audited experiments, experiment-specific distribution shift is associated with unstable internal model ranking, substantial selection loss, and degraded probability reliability. Calibration can improve average reliability metrics, but it does not remove experiment-specific failures. Accordingly, manuscript wording should emphasize leakage-safe external validation, model-selection instability and probabilistic transportability rather than presenting any single algorithm as globally superior.

## Evidence exclusions and provenance safeguards

- Do not use the NB02 `external_support_distance_ratio` diagnostic as manuscript evidence.
- Do not present external post-hoc winners as leakage-safe deployment selections.
- Preserve NB06 for provenance, but use NB06-v1.1 for final temperature-scaling values.
- Treat row-level bootstrap intervals as conditional within each held-out experiment.
- Treat only the four held-out experiments as independent generalization units.
- Do not modify frozen numerical values in `results/frozen_numeric_facts_nb08.json` outside a formally rerun and re-audited analysis.
