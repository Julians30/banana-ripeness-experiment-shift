# Reviewer reproducibility checklist

## Data provenance
- [x] Public source dataset identified by DOI: `10.15125/BATH-01459`.
- [x] Raw dataset is not relicensed or redistributed by this repository.
- [x] Audited master-data SHA-256 documented.
- [x] Frozen LOEO-protocol SHA-256 documented.
- [x] Inferred original block versus balancing tail is explicitly audited in Table S1.

## Leakage control
- [x] Complete experiments are held out in outer LOEO evaluation.
- [x] Preprocessing, model selection, hyperparameter decisions and calibration fitting use development experiments only.
- [x] SMOTE is restricted to training data.
- [x] External post-hoc winners are labeled descriptive and are never presented as leakage-safe selected models.
- [x] Development-majority no-skill baseline derives its prediction class from development experiments only.

## Statistical scope
- [x] Four held-out experiments are the independent generalization units.
- [x] Row-level bootstrap intervals are explicitly conditional within experiment.
- [x] Factorial ANOVA is used as descriptive effect-size decomposition, not population-level confirmatory inference.
- [x] Exact experiment-level sign-flip tests acknowledge the minimum possible two-sided p-value with n=4.
- [x] Effective stage-matching sample sizes are disclosed, including sparse stage/domain cells.

## Provenance corrections
- [x] Original NB06 is retained.
- [x] NB06-v1.1 supersedes NB06 only for final temperature-scaling values.
- [x] The known NB02 `external_support_distance_ratio` defect is excluded from manuscript evidence.
- [x] NB08 source-clean serialization correction is documented without changing code/results.

## Reviewer-requested explanatory additions
- [x] Repeated-CV AUC variability is visible in Figure 2.
- [x] Selection loss is directly visualized in Figure 3.
- [x] Stage-matched effective n is versioned as Table S2.
- [x] Development-majority no-skill baseline is versioned as Table S3.
- [x] TreeSHAP (Figure S1) is explicitly labeled post-hoc explanatory and non-causal.
- [x] `shap==0.50.0` is pinned in the environment used for the explanatory addition.

## Repository audit
- [x] NB01 and all eight reconstructed frozen notebooks parse as JSON and match frozen SHA-256 values.
- [x] Python code cells are syntax-checked by CI after excluding notebook magic/shell directives.
- [x] Frozen numerical results are checked against expected key values.
- [x] Seven frozen analytical evidence tables are checked automatically.
- [x] Previous-submission table mappings and figure SHA-256 values are kept for provenance in `results/manuscript_current/`.
- [x] Reviewer-requested Tables S1–S3 are versioned and hash-checked.
- [x] Raw archives and large prediction dumps are prohibited from the Git repository.

## Post-hoc robustness layer (current submission)
- [x] Prospective initial-window normalization (NB14) evidence is versioned in `results/post_hoc/nb14_prospective_domain_z/`.
- [x] Feature displacement, PCA loadings, projections and error localization (NB15) are versioned in `results/post_hoc/nb15_spectral_error_audit/`.
- [x] All 26 figures of the current submission are versioned in `results/chemolab_submission/figures/`; the audit checks that each PNG is byte-identical (SHA-256) to the image embedded in the submitted Word files.
- [x] All 26 figures are regenerated from tracked files (`scripts/make_publication_figures.py`, `scripts/postprocess_legacy_figures.py`) and compared with the submitted files by `scripts/verify_figures.py` in CI.
- [x] The NB17 notebook (positive control, MSC, alternative calibrators) and its outputs are included (`notebooks/post_hoc/`, `results/post_hoc/nb17_reviewer_shield/`); its candidate-grid differences from NB03 are disclosed in `config/PROTOCOL_V1.md`.
- [x] NB16 reliability-diagram metrics and bin audit are versioned in `results/post_hoc/nb16_reliability_diagrams/`.
- [x] Exact NB03 candidate grids (manuscript Table 2) are listed in `config/PROTOCOL_V1.md`.
- [x] `CITATION.cff` lists exactly the three manuscript authors with affiliations.
- [x] All post-hoc notebooks (NB09–NB12, NB14–NB17) are included in `notebooks/post_hoc/` and linked by SHA-256 to the executed notebooks (`notebook_provenance.csv`); NB09–NB12 exported tables are in `results/post_hoc/nb09_…`–`nb12_…`.
