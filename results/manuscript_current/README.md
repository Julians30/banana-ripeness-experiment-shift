# Previous-submission presentation layer

> **Superseded numbering.** This directory documents the presentation layer of the previous submission. The current submission to *Chemometrics and Intelligent Laboratory Systems* is mapped in [`../chemolab_submission/README.md`](../chemolab_submission/README.md). Supplementary Tables S2 and S3 were renumbered to match the current manuscript (S2 = stage-matched sample sizes, S3 = no-skill baseline).

This directory documents the **post-review manuscript presentation layer**. It does not replace or modify the frozen analytical evidence in `results/main_tables/`, `results/frozen_numeric_facts_nb08.json`, or the NB01–NB08 provenance chain.

## Why this layer exists

Reviewer-requested revisions changed the manuscript presentation after the confirmatory analysis had been frozen. In particular, the revised paper added uncertainty to the domain-AUC figure, an explicit selection-loss panel, a no-skill baseline, sample-size audits, reconstruction-count evidence, and a post-hoc TreeSHAP explanation.

The repository therefore separates:

1. **Frozen analytical evidence** — the confirmatory model-selection/evaluation pipeline and its original tables; and
2. **Previous-submission presentation evidence** — presentation artifacts and reviewer-requested additions that do not alter the frozen predictions, rankings, calibration fits, or confirmatory estimands.

## Current manuscript table mapping

| Current manuscript item | Repository source | Status |
|---|---|---|
| Table 1 — dataset/stage composition | `../main_tables/Table_1_dataset_stage_distribution.csv` | frozen analytical evidence |
| Table 2 — physical stage characterization | source-study definitions summarized in manuscript | editorial/contextual; no invented °Brix or firmness thresholds |
| Table 3 — experiment-shift diagnostics | `../main_tables/Table_2_experiment_shift_diagnostics.csv`; reviewer uncertainty visualization in Figure 1 | frozen diagnostics + reviewer visualization |
| Table 4 — confirmatory external performance/selection transportability | `../main_tables/Table_3_confirmatory_external_selected_models.csv`; `../main_tables/Table_4_model_selection_instability_summary.csv`; `../reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv` | frozen evidence + reviewer baseline |
| Table 5 — integrated synthesis | `../main_tables/Table_5_imbalance_sensitivity.csv`; `../main_tables/Table_6_probabilistic_calibration_selected_models.csv`; `../main_tables/Table_7_structural_effect_sizes.csv` | frozen analytical evidence |
| Table S1 | `../reviewer_revision/Table_S1_reconstruction_count_audit.csv` | reviewer-requested audit |
| Table S2 | `../reviewer_revision/Table_S2_stage_matched_effective_sample_sizes.csv` | effective stage-matched sample sizes |
| Table S3 | `../reviewer_revision/Table_S3_development_majority_no_skill_baseline.csv` | development-majority no-skill baseline |

Previous-submission figure provenance is recorded in `figures/README.md`, including logical filenames, exact SHA-256 values of the images embedded in the previous submission, and analytical-source notes. The PNGs are presentation outputs and are not required by the frozen numerical audit.
