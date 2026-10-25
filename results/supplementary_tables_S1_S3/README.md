# Supplementary Tables S1–S3

This directory contains supplementary Tables S1–S3. They were added after the confirmatory pipeline was frozen, to document the data reconstruction, the stage-matching sample sizes and a trivial baseline; they do not alter the frozen NB01–NB08 confirmatory model-selection/evaluation pipeline.

## Files

- `Table_S1_reconstruction_count_audit.csv` — original inferred block versus balancing tail counts by stage.
- `Table_S2_stage_matched_effective_sample_sizes.csv` — actual development/external counts and matched `n` per experiment × stage used to interpret domain discrimination.
- `Table_S3_development_majority_no_skill_baseline.csv` — leakage-safe trivial baseline; the majority stage is selected from development experiments only.
- `manifest.csv` — hashes, provenance and scope of the three tables.

## Reproduction

With the original Bath `TPHiS.zip` downloaded locally:

```bash
python scripts/make_supplementary_tables_S1_S3.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/supplementary_tables_S1_S3
```

## TreeSHAP scope

The manuscript also includes (Figure S1) a **post-hoc explanatory** TreeSHAP analysis for spectral Random Forest and XGBoost models. It uses the **frozen NB03 hyperparameters** within each outer fold and is not used for model selection, hyperparameter tuning, or confirmatory inference. SHAP attribution is interpreted as model dependence/importance, **not causal biochemical evidence**. The submitted figure is `../chemolab_submission/figures/Figure_S1.png` (SHA-256 in `../chemolab_submission/figure_provenance.csv`).

## Inferential scope

- The no-skill baseline is descriptive per held-out experiment.
- Stage-matching counts expose sparse-support cases rather than hiding them.
- None of these files increases the number of independent generalization units beyond the four held-out experiments.
