# Reviewer reproducibility checklist

## Data provenance
- [x] Public source dataset identified by DOI: `10.15125/BATH-01459`.
- [x] Raw dataset is not relicensed or redistributed by this repository.
- [x] Audited master-data SHA-256 documented.
- [x] Frozen LOEO-protocol SHA-256 documented.
- [x] Inferred original block versus balancing tail is explicitly audited in current Table S1.

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
- [x] Repeated-CV AUC variability is visible in current Figure 1.
- [x] Selection loss is directly visualized in current Figure 3.
- [x] Development-majority no-skill baseline is versioned as current Table S2.
- [x] Stage-matched effective n is versioned as current Table S3.
- [x] TreeSHAP Figure S3 is explicitly labeled post-hoc explanatory and non-causal.
- [x] `shap==0.50.0` is pinned in the environment used for the explanatory addition.

## Repository audit
- [x] NB01 and all eight reconstructed frozen notebooks parse as JSON and match frozen SHA-256 values.
- [x] Python code cells are syntax-checked by CI after excluding notebook magic/shell directives.
- [x] Frozen numerical results are checked against expected key values.
- [x] Seven frozen analytical evidence tables are checked automatically.
- [x] Current revised-manuscript table mappings are versioned; exact SHA-256 provenance is recorded for Figures 1–5 and Figures S1–S3.
- [x] Reviewer-requested Tables S1–S3 are versioned and hash-checked.
- [x] Raw archives and large prediction dumps are prohibited from the Git repository.
