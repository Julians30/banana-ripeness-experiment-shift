# Banana Ripeness Experiment Shift

[![repository-audit](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml)

Reproducible code, frozen analytical evidence, and reviewer-facing presentation artifacts for:

**Experiment Shift, Composition-Dependent Domain Normalization, and Probabilistic Reliability in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation**

Submitted to *Chemometrics and Intelligent Laboratory Systems*. The complete table/figure map of the submitted manuscript is in [`results/chemolab_submission/README.md`](results/chemolab_submission/README.md).

## Research question

To what extent do machine-learning models for multisensor banana-ripeness classification preserve predictive performance, model-selection decisions, and probabilistic reliability when evaluated on acquisition experiments completely excluded from model development, and can unlabeled domain normalization correct the shift without borrowing information from the future of the target experiment?

## Data source

University of Bath Research Data Archive:

**Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”**

- DOI: `10.15125/BATH-01459`
- License: CC BY 4.0
- Raw data are not redistributed in this repository.

The primary analysis uses the TPHiS release because it provides the common four-experiment basis required for nested Leave-One-Experiment-Out validation.

## Leakage-safe design

The confirmatory evaluation uses nested **Leave-One-Experiment-Out (LOEO)** validation. For each outer fold, one complete experiment is excluded from preprocessing, hyperparameter selection, algorithm selection, resampling and calibration fitting until final external evaluation.

Five algorithms are evaluated:

- Ordinal Logistic Regression
- PLS-DA
- SVM-RBF
- Random Forest
- XGBoost

Three sensor representations are evaluated:

- TPH
- Spectral
- TPH + Spectral

## Frozen analytical pipeline

```text
01 Data audit and frozen LOEO protocol
        ↓
02 PCA / UMAP / experiment-shift diagnostics
        ↓
03 Inner experiment-disjoint model selection
        ↓
04 Confirmatory outer LOEO evaluation
        ↓
05 Imbalance-treatment sensitivity
        ↓
06 Probabilistic reliability and ordinal analysis
        ↓
06-v1.1 Wide-range temperature-scaling correction
        ↓
07 Final statistical inference
        ↓
08 Final frozen manuscript-evidence packaging
```

NB06-v1.1 supersedes NB06 **only for final temperature-scaling values**. NB06 is retained for provenance.

### Post-hoc robustness layer

```text
09 Random references and random-selection null
10 Spectral normalization (SNV, complete-target DOMAIN_Z)
11 Duplicate-aware analysis        12 Shared-signature removal
14 Prospective initial-window DOMAIN_Z and composition stress
15 Feature displacement, PCA loadings, projections, error localization
16 Reliability diagrams            17 Reviewer-requested sensitivity analyses
```

These notebooks never modify frozen outer predictions, rankings or calibration fits. Exported evidence: `results/post_hoc/`; NB17: `notebooks/post_hoc/`.

## Frozen main results

Across **17,662** inferred-original TPHiS observations, four independent external experiments, three modalities and five algorithms:

- external model cells: **60**;
- outer experiment × modality model-selection scenarios: **12**;
- internal winner = external winner: **1/12 (8.3%)**;
- mean selection loss: **0.1147 Macro-F1**;
- maximum selection loss: **0.2148 Macro-F1**;
- mean inner-vs-external Spearman rank correlation: **−0.0754**;
- partial η² for held-out experiment on external Macro-F1: **0.4661**;
- partial η² for algorithm: **0.0531**;
- mean selected-model ECE: **0.4387 → 0.2568** after development-only temperature scaling;
- class weighting and training-only SMOTE each changed Macro-F1 by only about **+0.004 on average**, with heterogeneous effects across experiments.

The ECE above averages all 12 selected models, including softmax surrogates; the manuscript reports **0.497 → 0.257** for the 10 scenarios with native probabilities.

## Post-hoc results

- Complete-target (transductive) DOMAIN_Z raised mean selected spectral Macro-F1 from **0.131 to 0.418** (0.440 with unique-signature statistics; 0.439 after removing shared signatures).
- Estimated prospectively from the first 25 unique spectra, it raised Macro-F1 only from **0.125 to 0.175**, improving 2 of 4 experiments; window sizes 10 and 50 gave no consistent improvement.
- Acquisition order followed ripening, so initial windows contained almost only unripe fruit; the stage composition of the calibration window alone changed Macro-F1 by up to **0.19**.
- Raw spectral PC1 is a nearly uniform intensity/baseline axis (92.6% of variance in the Test 3 fold); experiment-wise z-scoring removes between-experiment offsets only.

The central result is not a universal winning classifier. Experiment-specific distribution shift can dominate algorithm choice, destabilize model selection and reduce probability transportability.

## Statistical scope

Only the **four held-out experiments** are independent generalization units.

Row-level paired/bootstrap intervals quantify uncertainty conditional on a held-out experiment and are not interpreted as confidence intervals over a population of independent experiments.

The factorial OLS/ANOVA representation is used for **descriptive structural effect-size decomposition**. Conventional ANOVA p-values are not used as confirmatory population inference.

## Two evidence layers

The repository separates the frozen confirmatory pipeline from presentation/reviewer additions.

### 1. Frozen analytical evidence

- frozen notebook provenance: `archive/frozen_notebook_payloads/`;
- frozen validation protocol: `config/nested_loeo_protocol_v1.json`;
- frozen analytical tables: `results/main_tables/`;
- frozen numerical facts: `results/frozen_numeric_facts_nb08.json`;
- executed/source-clean notebook linkage: `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`.

### 2. Previous-submission presentation evidence

- revised-manuscript figure provenance (logical filenames, exact manuscript-embedded SHA-256 values and analytical sources): `results/manuscript_current/figures/README.md`;
- reviewer-requested Tables S1–S3: `results/reviewer_revision/`;

### 3. Current submission (Chemometrics and Intelligent Laboratory Systems)

- table/figure map and SHA-256 of every embedded figure: `results/chemolab_submission/`;
- post-hoc exported evidence: `results/post_hoc/`;
- publication figures: `python scripts/make_publication_figures.py --out figures_out` regenerates Figs. 1, 2, 7–11, S8–S10 and S12–S15 from tracked files.

Reviewer-requested additions include repeated-CV uncertainty for domain AUC, direct selection-loss visualization, the reconstruction-count audit, a development-majority no-skill baseline, explicit stage-matched sample sizes, and post-hoc TreeSHAP explanation. These additions **do not modify frozen outer predictions, model rankings, calibration fits, or confirmatory numerical estimates**.

## Reviewer-facing reproducibility

NB01 is directly browsable in `notebooks/`. Exact source-clean NB02–NB08 bytes are preserved as immutable base85+gzip provenance payloads in `archive/frozen_notebook_payloads/`.

To materialize all nine notebooks and readable Python mirrors locally:

```bash
python scripts/rebuild_analysis_mirrors.py
```

To regenerate the reviewer-requested Tables S1–S3 from the original TPHiS archive:

```bash
python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/reviewer_revision
```

The repository audit is read-only:

```bash
python scripts/audit_repository.py
```

It uses only the Python standard library and verifies frozen notebook provenance, LOEO semantics, key numerical evidence, current manuscript tables/figures, reviewer additions, environment metadata, citation metadata, evidence traceability and repository file policy.

## Repository structure

```text
.github/workflows/               read-only CI integrity audit
archive/
  frozen_notebook_payloads/     immutable NB02–NB08 source-clean provenance
config/                          frozen nested-LOEO protocol
docs/                            data, statistics, provenance and evidence maps
notebooks/
  01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb
  README.md
  post_hoc/                      NB17 reviewer-requested sensitivity notebook
results/
  main_tables/                   original frozen analytical evidence
  manuscript_current/
    README.md                    mapping from frozen evidence to revised manuscript
    figures/README.md           hashes/sources for figures embedded in the revised manuscript
  reviewer_revision/             Tables S1–S3 (count audit, stage-matched n, no-skill baseline)
  chemolab_submission/           current table/figure map and figure SHA-256
  post_hoc/                      NB14 and NB15 exported evidence
  frozen_numeric_facts_nb08.json
  table_manifest.csv
  figure_manifest.csv
scripts/
  audit_repository.py
  rebuild_analysis_mirrors.py
  09_REVIEWER_REQUESTED_AUDITS.py
  make_publication_figures.py
  postprocess_legacy_figures.py
requirements.txt
environment.yml
CITATION.cff
LICENSE
```

## Reproduce the analysis

1. Download the original Bath dataset using DOI `10.15125/BATH-01459`.
2. Place the four source archives documented in `docs/REPRODUCIBILITY.md` under the expected raw-data folder.
3. Run `python scripts/audit_repository.py`.
4. Run `python scripts/rebuild_analysis_mirrors.py`.
5. Install the pinned environment from `requirements.txt` or `environment.yml`.
6. Execute the notebooks in the documented order.
7. Compare generated evidence with `results/main_tables/`, `results/frozen_numeric_facts_nb08.json`, and `docs/MANUSCRIPT_EVIDENCE_MAP.md`.
8. Reproduce Tables S1–S3 with `scripts/09_REVIEWER_REQUESTED_AUDITS.py`.
9. Regenerate the publication figures with `scripts/make_publication_figures.py`.

## Important exclusions and safeguards

- `external_support_distance_ratio` from exploratory NB02 work is **excluded from manuscript evidence** because duplicate spectral vectors produced a zero denominator in several scenarios.
- External post-hoc best models are descriptive comparators and are never presented as leakage-safe deployment selections.
- SMOTE is applied only inside training data.
- Calibration is learned from development-only cross-fitted predictions.
- Raw archives and large row-level prediction dumps are intentionally not committed to Git.
- TreeSHAP is post-hoc explanatory evidence and is not interpreted causally.
- NB06-v1.1 supersedes NB06 only for final temperature-scaling values.
- NB08's corrected source-clean serialization provenance is documented in `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`.

## Environment

The final analytical environment used Python **3.13.15**. Package versions are pinned in `requirements.txt` and `environment.yml`; `shap==0.50.0` is included for the reviewer-requested explanatory analysis.

## Data and code availability

See:

- `docs/DATASET.md`
- `docs/DATA_AVAILABILITY.md`
- `docs/REPRODUCIBILITY.md`
- `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`
- `docs/STATISTICAL_ANALYSIS.md`
- `docs/MANUSCRIPT_EVIDENCE_MAP.md`
- `docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md`

## Citation

`CITATION.cff` contains all four manuscript authors and the current repository/software metadata. Update the preferred citation with the journal DOI after publication.

## License

Analysis code: **MIT License**.

Source dataset: **CC BY 4.0**, retained under the original University of Bath terms and not relicensed by this repository.
