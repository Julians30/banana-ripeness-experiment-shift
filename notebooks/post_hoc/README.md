# Post-hoc notebooks

Notebooks run after the frozen confirmatory pipeline (NB01–NB08). They read frozen NB01–NB08 outputs or the audited master file produced by NB01 (`06_master_original_multisensor.csv`, 17,662 observations, SHA-256 `0a06fb37…` in `docs/DATASET.md`) and never overwrite frozen outputs.

| Notebook | Analysis (manuscript) | Exported evidence |
|---|---|---|
| `09_NULL_BASELINES_CALIBRATION_SKILL.ipynb` | uniform/development-prevalence references, calibration skill, random-selection null for model ranking (2.11, 3.2, Table 5) | `../../results/post_hoc/nb09_random_references/` |
| `10_SPECTRAL_NORMALIZATION_SENSITIVITY.ipynb` | SNV and complete-target DOMAIN_Z under nested LOEO (2.11, 3.7, Fig. 6) | `../../results/post_hoc/nb10_spectral_normalization/` |
| `11_DUPLICATE_AWARE_SPECTRAL_SENSITIVITY.ipynb` | duplicate-aware statistics on unique spectral vectors (2.11, 3.7, Fig. S11) | `../../results/post_hoc/nb11_duplicate_aware/` |
| `12_REMOVE_CROSS_EXPERIMENT_EXACT_SPECTRAL_OVERLAP.ipynb` | removal of spectral signatures shared across experiments (2.11, 3.7, Fig. S11) | `../../results/post_hoc/nb12_shared_signature_removal/` |
| `14_INITIAL_WINDOW_DOMAIN_Z_ERROR_DIAGNOSTICS.ipynb` | prospective initial-window DOMAIN_Z (N = 10, 25, 50), paired ordinal errors, composition stress (2.12, 3.8, Table 6, Figs. 8–9, 11, Tables S4–S5) | `../../results/post_hoc/nb14_prospective_domain_z/` |
| `15_SPECTRAL_STRUCTURE_ERRORS_ROBUSTNESS.ipynb` | feature displacement, PCA loadings, PCA/UMAP projections, error localization, conditional resampling (2.12, 3.7–3.8, Figs. 7–8, 10, S8–S10, S12–S15) | `../../results/post_hoc/nb15_spectral_error_audit/` |
| `16_RELIABILITY_PUBLICATION_FIGURES.ipynb` | reliability diagrams with bin support, no refitting (3.5, Figs. 4–5, S4–S7) | `../../results/post_hoc/nb16_reliability_diagrams/` |
| `17_POSITIVE_CONTROL_MSC_CALIBRATORS.ipynb` | positive control, MSC, alternative calibrators (2.13, 3.9, Table 7, Table S6) | `../../results/post_hoc/nb17_positive_control_msc_calibrators/` |

## Provenance

`notebook_provenance.csv` links each notebook to the executed notebook kept in the authors' project workspace (SHA-256 and size of the executed file, SHA-256 and size of the file committed here) and states exactly how the two differ. NB09–NB16 are the executed notebooks with outputs, execution counts and Colab metadata removed. The repository audit checks the committed SHA-256 values and the Python syntax of every code cell.

- NB09–NB12 and NB14 were written in response to questions raised by colleagues who read a draft of the manuscript before submission. Labels referring to that internal reading (e.g. "Reviewer 1/2") were removed after execution from notebook titles, run-folder names and output file names (for example `11_key_results_reviewer1.json` → `11_key_results.json`), consistently in the notebooks and in `../../results/post_hoc/`. No computation, value or table content changed. The manuscript has not been submitted to any other journal.
- The executed NB14 is version 2 (run `20261025_133148`, the run recorded in `results/post_hoc/nb14_prospective_domain_z/NB14_run_manifest.json`). An earlier, unexecuted draft of NB14 is not used for any reported value and is not included.
- The narrative (markdown) cells of NB14–NB16 are in Spanish; code, outputs and exported tables are in English.
- NB17: markdown, comments and printed messages were translated to English; cells 1–2 (environment and paths) were generalized after the executed run so that it also runs outside Colab, and cell 8 now also records the master-file SHA-256. Analysis cells 3–7 are identical to the executed notebook apart from string literals.
- All notebooks were run in Google Colab with the project at `/content/drive/MyDrive/Paper3_Banano/BANANA_RIPENESS_MULTISENSOR_Q1`; to run elsewhere, change the project-root variable (NB17: set `NB17_MASTER_CSV`).

## NB17 candidate grid

NB17 re-implements the nested LOEO selection rule with the Table 2 algorithms and preprocessing; its LOEO arm is compared with manuscript Table 4 in the final cell (`A_check_vs_table4.csv`: same selected model in 11/12 scenarios, Macro-F1 identical to three decimals in 10/12). Its ordinal-logistic, PLS-DA and SVM candidates equal NB03, but its tree-ensemble candidates differ (random forest: full 2 × 2 × 2 factorial, 8 configurations; XGBoost: (250, 2, 0.10), (250, 3, 0.05), (500, 4, 0.03), (500, 5, 0.05)); both non-identical scenarios are ones in which a tree ensemble was selected. Exact NB03 grids: `../../config/PROTOCOL_V1.md`.

**Running NB17.** In Google Colab it finds the master file in Google Drive. Locally, install `requirements.txt` and set `NB17_MASTER_CSV=/path/to/06_master_original_multisensor.csv` (and optionally `NB17_OUT_DIR`). CPU runtime is about 4 h, with checkpoints after every modality and arm.
