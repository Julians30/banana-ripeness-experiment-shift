# Manuscript evidence map

Claim-level traceability for the manuscript submitted to *Chemometrics and Intelligent Laboratory Systems*:

**Experiment Shift, Composition-Dependent Domain Normalization, and Probabilistic Reliability in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation**

Table and figure numbers below are those of the submitted manuscript. The item-by-item source map (every table and figure, with the SHA-256 of every embedded figure) is in [`../results/chemolab_submission/README.md`](../results/chemolab_submission/README.md). The previous-submission numbering is kept only for provenance in [`../results/manuscript_current/`](../results/manuscript_current/README.md); the correspondence is given at the end of this document.

## Evidence layers

1. **Frozen confirmatory evidence**: NB01–NB08, the frozen LOEO protocol (`../config/`), `../results/main_tables/` and `../results/frozen_numeric_facts_nb08.json`.
2. **Reviewer-requested explanatory additions**: `../results/reviewer_revision/` (Tables S1–S3) and the TreeSHAP figure (Figure S1).
3. **Post-hoc robustness evidence**: NB09–NB12, NB14–NB17; exported tables in `../results/post_hoc/`.

Layers 2 and 3 never replace or modify frozen outer predictions, model rankings, calibration fits or confirmatory numerical values.

## Scope and data reconstruction

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| The confirmatory analysis uses 17,662 inferred-original TPHiS observations from four experiments (Tests 2–5). | Table 1 | NB01; `results/main_tables/Table_1_dataset_stage_distribution.csv` | Counts describe the audited original block only. |
| The inferred balancing tail fills class deficits to 6,533 per stage. | Table S1 | `results/reviewer_revision/Table_S1_reconstruction_count_audit.csv`; `scripts/09_REVIEWER_REQUESTED_AUDITS.py` | Source ordering supports the inference but is not a time variable or an author-provided synthetic flag. |
| Nested LOEO isolates a complete acquisition experiment from development. | Figure 1; Section 2.4 | `config/nested_loeo_protocol_v1.json`; `config/PROTOCOL_V1.md`; NB01, NB03, NB04 | External rows cannot influence preprocessing, tuning, resampling, calibration or algorithm selection. |
| Candidate algorithms and grids. | Table 2 | NB03 `candidate_grid()`; exact configurations in `config/PROTOCOL_V1.md` | Grids are compact by design (Section 2.5). |

## Experiment shift

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Experiment identity remains strongly recoverable after matching on ripeness stage (domain ROC-AUC, MMD²). | Table 3; Figure 2 | NB02; `results/main_tables/Table_2_experiment_shift_diagnostics.csv` | Error bars are repeated-CV variability, not confidence intervals over independent experiments. |
| Matched sample sizes vary substantially by stage. | Table S2 | `results/reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv` | `matched n/domain = min(n_dev, n_external, 600)`. |
| Raw spectral PC1 is a nearly uniform intensity/baseline axis (92.6% of variance in the Test 3 fold). | Figure 7; Figures S8–S10 | NB15 `pca_coefficients.csv`, `pca_explained_variance.csv` | PCA is fitted on development data only. |
| Held-out experiments occupy displaced regions of the development PCA space; UMAP is used only for neighbourhood structure. | Figure 10; Figures S12–S13 | NB15 `projection_coordinates.csv.gz` | UMAP maps new records through development neighbours and cannot extrapolate. |
| The NB02 nearest-neighbour support ratio is excluded. | not reported | NB02 | Duplicate spectral vectors generated zero denominators. |

## Confirmatory predictive transportability

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Internally selected models frequently lose external performance. | Table 4 | `results/main_tables/Table_3_confirmatory_external_selected_models.csv`; NB04 | Post-hoc external best models are descriptive comparators only. |
| Internal winner = post-hoc external winner in 1/12 scenarios; mean selection loss 0.1147, maximum 0.2148 Macro-F1. | Table 4; Figure 3 | `results/main_tables/Table_4_model_selection_instability_summary.csv`; `frozen_numeric_facts_nb08.json` | Not independently unusual under the NB09 random-selection null. |
| Mean inner–external rank association is approximately null (Spearman −0.075). | Table 5 | `results/main_tables/Table_4_model_selection_instability_summary.csv` | Descriptive across 12 scenarios. |
| Development-majority no-skill Macro-F1 is 0.000, 0.073, 0.070 and 0.075 for Tests 2–5. | Table S3 | `results/reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv` | Majority class from development experiments only. |

## Imbalance sensitivity

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Class weighting and training-only SMOTE change mean Macro-F1 by about +0.004. | Table 5; Figure S2 | `results/main_tables/Table_5_imbalance_sensitivity.csv`; NB05/NB07 | Heterogeneous across experiments; exact sign-flip p ≥ 0.125 with four experiments. |

## Probabilistic reliability

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Development-only temperature scaling lowers mean ECE from 0.497 to 0.257 for the 10 scenarios with native probabilities. | Section 3.5; Figures 4–5, S3–S7 | `results/main_tables/Table_6_probabilistic_calibration_selected_models.csv`; NB06-v1.1; NB16 `results/post_hoc/nb16_reliability_diagrams/` | Over all 12 selected models (including softmax surrogates) the value is 0.4387 → 0.2568 (`frozen_numeric_facts_nb08.json`). Low ECE with near-uniform probabilities is not informative prediction (bin support shown). |
| Three selected temperature fits reached the upper bound. | Section 3.5 | NB06-v1.1 | Severe calibration mismatch, not an optimization failure. |
| Vector scaling and isotonic calibration do not transfer better than temperature scaling; none beats the uniform forecast. | Table S6; Section 3.9 | NB17 `results/post_hoc/nb17_reviewer_shield/C_calibrators.csv` | Post-hoc sensitivity analysis. |

## Structural effect-size decomposition

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Held-out experiment explains much more Macro-F1 variation than algorithm (partial η² 0.466 vs 0.053). | Table 5 | `results/main_tables/Table_7_structural_effect_sizes.csv`; NB07 | Descriptive decomposition; ANOVA p-values are not population inference. |

## Domain normalization (post-hoc)

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Complete-target DOMAIN_Z raises mean selected spectral Macro-F1 from 0.131 to 0.418 (0.440 unique-signature statistics; 0.439 after removing shared signatures). | Figure 6; Figure S11; Table 5 | NB10–NB12 | Transductive: uses the whole target experiment. |
| Estimated prospectively from the first 25 unique spectra, DOMAIN_Z raises Macro-F1 only from 0.125 to 0.175, improving 2 of 4 experiments. | Table 6; Figure 8; Table S4 | NB14 `08_source_order_prefix_vs_raw_and_oracle.csv`, `09_source_order_summary_by_window.csv`, `12_key_results_nb14.json` | Acquisition order approximated by the source index (no timestamps released). |
| Initial windows contain almost only unripe fruit; window composition alone changes Macro-F1 by up to 0.19. | Figures 8, 11; Table S5 | NB14 `03_prefix_and_future_stage_composition.csv`, `10_…replicates.csv.gz`, `11_stage_composition_stress_summary.csv` | The stress test uses target labels; it is a diagnostic, not a procedure. |
| Paired ordinal errors and error localization. | Figure 9; Figures S14–S15 | NB14 `paired_error_outcomes.csv.gz`; NB15 `paired_predictions_with_signature.csv.gz` | Resampling intervals are conditional on frozen predictions. |
| MSC (0.203) behaves like SNV (0.211) under nested LOEO (RAW 0.158). | Section 3.9 | NB17 `B_RAW.csv`, `B_SNV.csv`, `B_MSC.csv` | NB17 SNV reproduces NB10. |

## Positive control (post-hoc)

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| The same model families reach Macro-F1 0.962–0.995 under pooled random 5-fold CV and 0.958–0.994 within single experiments, versus 0.108–0.158 under nested LOEO. | Table 7; Section 3.9 | NB17 `A_*.csv`, `A_summary.csv` | Random and within-experiment splits place near-identical repeated readings in both partitions. |
| NB17's LOEO arm reproduces the frozen selected model in 11/12 scenarios and Macro-F1 to three decimals in 10/12. | Section 2.13 | NB17 `A_check_vs_table4.csv` | NB17's tree-ensemble candidates differ from NB03 (`config/PROTOCOL_V1.md`); both differences occur where a tree ensemble was selected. |

## Reviewer-requested TreeSHAP explanation

| Manuscript claim | Manuscript item | Evidence | Interpretation constraint |
|---|---|---|---|
| Spectral tree explanations emphasize visible-green and selected NIR bands. | Figure S1 | post-hoc TreeSHAP with frozen NB03 hyperparameters (`results/reviewer_revision/README.md`) | Explanatory only, not causal biochemical attribution. |

## Correspondence with the previous submission

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
| — | Figures 1, 6–11, S4–S15; Tables 6, 7, S4–S6 (post-hoc layer) |

## Evidence exclusions and safeguards

- Do not use `external_support_distance_ratio` as manuscript evidence.
- Do not present post-hoc external winners as deployable leakage-safe selections.
- NB06 is kept for provenance; NB06-v1.1 is authoritative for temperature scaling.
- Row-level bootstrap intervals are conditional within each held-out experiment.
- Only the four held-out experiments are independent generalization units.
- Complete-target DOMAIN_Z is transductive; the prospective NB14 estimate is the deployable one.
- TreeSHAP is post-hoc explanatory evidence, not confirmatory or causal evidence.
- Do not modify `results/frozen_numeric_facts_nb08.json` outside a formally rerun and re-audited analysis.
