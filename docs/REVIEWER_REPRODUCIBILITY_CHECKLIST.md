# Reviewer reproducibility checklist

## Data provenance
- [x] Public source dataset identified by DOI: `10.15125/BATH-01459`.
- [x] Raw dataset is not relicensed or redistributed by this repository.
- [x] Audited master-data SHA-256 documented.
- [x] Frozen LOEO-protocol SHA-256 documented.

## Leakage control
- [x] Complete experiments are held out in outer LOEO evaluation.
- [x] Preprocessing, model selection, hyperparameter decisions and calibration fitting use development experiments only.
- [x] SMOTE is restricted to training data.
- [x] External post-hoc winners are labeled descriptive and are never presented as leakage-safe selected models.

## Statistical scope
- [x] Four held-out experiments are the independent generalization units.
- [x] Row-level bootstrap intervals are explicitly conditional within experiment.
- [x] Factorial ANOVA is used as descriptive effect-size decomposition, not population-level confirmatory inference.
- [x] Exact experiment-level sign-flip tests acknowledge the minimum possible bilateral p-value with n=4.

## Provenance corrections
- [x] Original NB06 is retained.
- [x] NB06-v1.1 supersedes NB06 only for final temperature-scaling values.
- [x] The known NB02 `external_support_distance_ratio` defect is excluded from manuscript evidence.

## Repository audit
- [x] Every tracked notebook parses as JSON.
- [x] Python code cells are syntax-checked by CI after excluding notebook magic/shell directives.
- [x] Frozen results are checked against expected key values.
- [x] Required manuscript tables are checked automatically.
- [x] Raw archives and large prediction dumps are prohibited from the Git repository.
