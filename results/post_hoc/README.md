# Post-hoc robustness evidence

These analyses were run **after** the frozen confirmatory pipeline (NB01–NB08). They do not modify frozen outer predictions, model rankings, calibration fits or confirmatory estimates, and they are reported in the manuscript as robustness and mechanism-oriented evidence.

| Notebook | Question | Manuscript | Exported evidence |
|---|---|---|---|
| NB09 | Uniform and development-prevalence references; calibration skill; random-selection null for model ranking | 2.11, 3.2, Table 5 | `nb09_random_references/` |
| NB10 | Spectral normalization (SNV, complete-target DOMAIN_Z) under nested LOEO | 2.11, 3.7, Fig. 6 | `nb10_spectral_normalization/` |
| NB11 | Duplicate-aware analysis (unique spectral vectors) | 2.11, 3.7, Fig. S11 | `nb11_duplicate_aware/` |
| NB12 | Removal of spectral signatures shared across experiments | 2.11, 3.7, Fig. S11 | `nb12_shared_signature_removal/` |
| NB14 | Prospective initial-window DOMAIN_Z (N = 10, 25, 50), paired ordinal errors, composition stress | 2.12, 3.8, Table 6, Figs. 8–9, 11, Tables S4–S5 | `nb14_prospective_domain_z/` |
| NB15 | Feature displacement, PCA loadings, PCA/UMAP projections, error localization, leave-one-experiment-out and conditional resampling | 2.12, 3.7–3.8, Figs. 7–8, 10, S8–S10, S12–S15 | `nb15_spectral_error_audit/` |
| NB16 | Reliability diagrams with bin support (no refitting) | 3.5, Figs. 4–5, S4–S7 | `nb16_reliability_diagrams/` |
| NB17 | Positive control (random vs experiment-disjoint splits), MSC sensitivity, alternative calibrators | 2.13, 3.9, Table 7, Table S6 | `nb17_reviewer_shield/` |

All eight notebooks are in [`../../notebooks/post_hoc/`](../../notebooks/post_hoc/README.md), with the SHA-256 of each executed notebook in `notebook_provenance.csv`.

## Files

`nb09_random_references/`, `nb10_spectral_normalization/`, `nb11_duplicate_aware/`, `nb12_shared_signature_removal/` — the `tables/`, `metadata/` and `README_RESULTS.md` exported by each run (run IDs `20260928_015307`, `…_020934`, `…_030710`, `…_032519`). Key values are in the numbered `*_key_results*.json` file of each folder: NB09 `11_key_results_reviewer1.json` (random-selection null: observed mean selection loss 0.1147 vs null 0.0926, p = 0.12; winner agreement 1 vs 2.4 expected, p = 0.28); NB10 `09_selected_model_performance_raw_snv_domainz.csv` (Spectral: RAW 0.131, complete-target DOMAIN_Z 0.418); NB11 `16_key_results_reviewer2_duplicates.json` (DOMAIN_Z with unique-signature statistics 0.440); NB12 `14_key_results_reviewer2_remove_shared.json` (0.439 after removing the 278 rows in the two shared signatures). NB12's list of removed rows (`02_removed_shared_spectral_rows.csv.gz`) is omitted because it contains raw spectral values; it is reproduced by running NB12. The notebook figures of these runs were presentation drafts and are not included; the corresponding manuscript figures are Figure 6 and Figure S11.

`nb14_prospective_domain_z/` — numbered tables `01`–`12` follow the NB14 execution order; `paired_error_outcomes.csv.gz` and `selected_predictions_paired_diagnostics.csv.gz` hold record-level paired predictions on duplicate-collapsed spectral records (no raw sensor values); `NB14_run_manifest.json` records seed, windows, fit counts, package versions and key results.

`nb15_spectral_error_audit/` — `projection_coordinates.csv.gz` stores development-fitted PCA/UMAP coordinates (no raw sensor values); `pca_coefficients.csv` and `pca_explained_variance.csv` give loadings per fold and representation; `feature_displacement.csv`, `conditional_resampling_sensitivity.csv`, `leave_one_experiment_out_summary.csv` and `metrics_by_experiment.csv` support Table 6 and Fig. 8.

`nb16_reliability_diagrams/` — `figure_reliability_metrics.csv` (n, ECE, Brier and NLL per selected model, raw and temperature-scaled), `reliability_numerical_audit.csv` (per-bin support, confidence and accuracy behind each diagram) and `run_manifest.json` (source hashes; 0 classifier, calibrator or embedding refits). The figure files are in `../chemolab_submission/figure_sources/nb16_reliability/`.

`nb17_reviewer_shield/` — `A_*.csv` (pooled random, within-experiment and nested LOEO arms per modality; `A_summary.csv`), `A_check_vs_table4.csv` (LOEO arm versus manuscript Table 4: same selected model in 11/12 scenarios, identical Macro-F1 in 10/12), `B_*.csv` (RAW, SNV and MSC under nested LOEO), `C_calibrators.csv` (temperature, vector scaling and one-vs-rest isotonic calibration). NB17 coded its own candidate grid; its random-forest and XGBoost candidates differ from NB03 (`../../config/PROTOCOL_V1.md`), and both scenarios that differ from Table 4 are tree-ensemble scenarios.

## Scope

- No raw timestamps were released; acquisition order is approximated by the original source index.
- The composition stress test uses target labels to build calibration windows; it measures composition sensitivity and is not a deployable procedure.
- Row and signature-cluster resampling intervals are conditional on frozen predictions; spectral signatures are not established independent biological units.
- Only the four acquisition experiments are independent generalization units.
