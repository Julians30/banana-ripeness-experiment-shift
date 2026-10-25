# Chemometrics and Intelligent Laboratory Systems submission — evidence map

This directory maps every table and figure of the manuscript **"Experiment Shift, Composition-Dependent Domain Normalization, and Probabilistic Reliability in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation"** to its source in this repository. It supersedes the numbering of the previous submission documented in `../manuscript_current/` (kept for provenance).

Layers:

- **Frozen confirmatory evidence** — NB01–NB08, `../main_tables/`, `../frozen_numeric_facts_nb08.json`.
- **Post-hoc robustness evidence** — NB09–NB12 (random references, spectral normalization, duplicate-aware and shared-signature analyses), NB14 (prospective initial-window normalization and composition stress), NB15 (feature displacement, loadings, projections, error localization), NB16 (reliability diagrams), NB17 (positive control, MSC and alternative calibrators; Section 2.13). Exported tables are in `../post_hoc/`.

None of the post-hoc layers modifies frozen outer predictions, model rankings, calibration fits or confirmatory estimates.

## Tables

| Manuscript | Content | Repository source |
|---|---|---|
| Table 1 | Stage composition of Tests 2–5 | `../main_tables/Table_1_dataset_stage_distribution.csv` |
| Table 2 | Candidate models and frozen grids | exact configurations in `../../config/PROTOCOL_V1.md`; NB03 `candidate_grid()` |
| Table 3 | Stage-matched experiment-shift diagnostics | `../main_tables/Table_2_experiment_shift_diagnostics.csv` |
| Table 4 | External performance of internally selected models | `../main_tables/Table_3_confirmatory_external_selected_models.csv`; `../main_tables/Table_4_model_selection_instability_summary.csv` |
| Table 5 | Integrated synthesis | `../main_tables/Table_4`–`Table_7`; NB09–NB12 values; NB17; `../post_hoc/nb14_prospective_domain_z/`; `../post_hoc/nb15_spectral_error_audit/` |
| Table 6 | Prospective initial-window DOMAIN_Z (N = 25) | NB14 `08_source_order_prefix_vs_raw_and_oracle.csv`, `03_prefix_and_future_stage_composition.csv`, `paired_error_summary_by_experiment.csv`; NB15 `feature_displacement.csv` |
| Table 7 | Positive control (random, within-experiment and nested LOEO splits) | NB17 `../post_hoc/nb17_reviewer_shield/A_*.csv` |
| Table S1 | Balancing-tail count audit | `../reviewer_revision/Table_S1_reconstruction_count_audit.csv` |
| Table S2 | Stage-matched effective sample sizes | `../reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv` |
| Table S3 | Development-majority no-skill baseline | `../reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv` |
| Table S4 | Window-size sensitivity (N = 10, 25, 50) | NB14 `08_source_order_prefix_vs_raw_and_oracle.csv`, `09_source_order_summary_by_window.csv` |
| Table S5 | Calibration-window composition stress | NB14 `11_stage_composition_stress_summary.csv` (replicates: `10_stage_composition_stress_replicates.csv.gz`) |
| Table S6 | Alternative calibrators | NB17 `../post_hoc/nb17_reviewer_shield/C_calibrators.csv` |

## Figures

All 26 submitted figures are in [`figures/`](figures/) (PNG exactly as embedded in the Word files; vector PDF where available). The audit checks each PNG against the SHA-256 in `figure_provenance.csv`.

Figures marked **script** are regenerated from tracked files (pixel-identical PNGs; verified for the submitted version) with `python scripts/make_publication_figures.py --out <folder>`. Figures marked **post-processed** were produced by NB04/NB07/NB10–NB12 or NB16 and only had their in-figure title removed or labels corrected with `scripts/postprocess_legacy_figures.py` (plot pixels unchanged; inputs in [`figure_sources/`](figure_sources/): `previous_submission/` holds the notebook-produced figures of the previous submission, where `Figure_S4.png` is the current Figure S11, and `nb16_reliability/` holds the NB16 outputs). `python scripts/verify_figures.py <folder>` compares regenerated PNGs with the submitted ones; with `requirements-figures.txt` all 26 are byte-identical.

| Manuscript | Content | Source | Production |
|---|---|---|---|
| Figure 1 | Leakage-safe study design | design schematic | script |
| Figure 2 | Domain ROC-AUC and MMD² | `../main_tables/Table_2_experiment_shift_diagnostics.csv` | script |
| Figure 3 | Model-selection transportability | NB04/NB07 | post-processed |
| Figures 4–5 | Spectral reliability before/after temperature scaling | NB16 (NB06-v1.1 probabilities); `../post_hoc/nb16_reliability_diagrams/` | post-processed |
| Figure 6 | Selected-model Macro-F1 after spectral normalization | NB10 | post-processed |
| Figure 7 | PCA loadings, Test 3 fold | NB15 `pca_coefficients.csv`, `pca_explained_variance.csv` | script |
| Figure 8 | Prospective normalization synthesis | NB14 `08`, `09`; NB15 `conditional_resampling_sensitivity.csv`, `leave_one_experiment_out_summary.csv` | script |
| Figure 9 | Paired ordinal errors | NB14 `paired_error_outcomes.csv.gz` | script |
| Figure 10 | PCA projections, Test 5 | NB15 `projection_coordinates.csv.gz` | script |
| Figure 11 | Composition stress | NB14 `10_stage_composition_stress_replicates.csv.gz` | script |
| Figure S1 | TreeSHAP spectral attribution | reviewer-requested post-hoc analysis (frozen NB03 hyperparameters) | post-processed |
| Figure S2 | Imbalance sensitivity by experiment | NB05/NB08 | post-processed |
| Figure S3 | Calibration transfer by experiment | NB06-v1.1/NB08 | post-processed |
| Figures S4–S7 | TPH and fused reliability diagrams | NB16 | post-processed |
| Figures S8–S10 | PCA loadings, Test 2, 4 and 5 folds | NB15 | script |
| Figure S11 | Removal of shared spectral signatures | NB11/NB12 | post-processed |
| Figure S12 | UMAP embeddings, Test 5 | NB15 `projection_coordinates.csv.gz` | script |
| Figure S13 | PCA projections, Test 3 | NB15 | script |
| Figures S14–S15 | Error localization, Tests 3 and 5 | NB15 `projection_coordinates.csv.gz`, `paired_predictions_with_signature.csv.gz` | script |

## Interpretation safeguards

- Complete-target DOMAIN_Z is transductive; the prospective analysis (NB14) is the deployable estimate.
- The acquisition-order proxy is the original source index; no timestamps were released.
- The composition stress test uses target labels to build calibration windows and is a diagnostic, not a procedure.
- PCA is used to display displacement and loadings because it is a linear map; UMAP maps new records through nearest development neighbours and is used only for neighbourhood structure and silhouettes.
- With four experiments, the smallest attainable two-sided exact sign-flip p-value is 0.125.
- Mean selected-model ECE is 0.4387 → 0.2568 across all 12 selected models (including softmax surrogates, `../frozen_numeric_facts_nb08.json`); the manuscript reports 0.497 → 0.257 for the 10 scenarios with native probabilities.
