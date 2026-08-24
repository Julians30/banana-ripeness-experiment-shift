# Reviewer-requested revision evidence

This directory contains compact evidence added in response to peer review. These files are **post-freeze reviewer additions** and do not alter the frozen NB01–NB08 confirmatory model-selection/evaluation pipeline.

## Files

- `Table_S1_reconstruction_count_audit.csv` — original inferred block versus balancing tail counts by stage.
- `Table_S2_development_majority_no_skill_baseline.csv` — leakage-safe trivial baseline; the majority stage is selected from development experiments only.
- `Table_S3_stage_matched_effective_sample_sizes.csv` — actual development/external counts and matched `n` per experiment × stage used to interpret domain discrimination.
- `manifest.csv` — hashes, provenance and scope of the three reviewer-requested tables.

## Reproduction

With the original Bath `TPHiS.zip` downloaded locally:

```bash
python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/reviewer_revision
```

## TreeSHAP scope

The revised manuscript also includes a **post-hoc explanatory** TreeSHAP analysis for spectral Random Forest and XGBoost models. It uses the **frozen NB03 hyperparameters** within each outer fold and is not used for model selection, hyperparameter tuning, or confirmatory inference. SHAP attribution is interpreted as model dependence/importance, **not causal biochemical evidence**. The exact manuscript-embedded image SHA-256 is recorded in `../manuscript_current/figures/README.md`.

## Inferential scope

- The no-skill baseline is descriptive per held-out experiment.
- Stage-matching counts expose sparse-support cases rather than hiding them.
- None of these files increases the number of independent generalization units beyond the four held-out experiments.
