# Banana Ripeness Experiment Shift

[![repository-audit](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml/badge.svg)](https://github.com/Julians30/banana-ripeness-experiment-shift/actions/workflows/repository-audit.yml)

Code, frozen analytical evidence, post-hoc robustness evidence and the submitted figures for:

**Experiment Shift, Composition-Dependent Domain Normalization, and Probabilistic Reliability in Multisensor Banana Ripeness Classification: A Leakage-Safe Evaluation**

Julián Coronel-Reyes¹ \*, Alexander Haro-Sarango², Johnny Javier Triviño Sanchez³

¹ Facultad de Ciencias Agropecuarias, Universidad Técnica de Machala, Machala, Ecuador · ² Escuela Profesional de Contabilidad, Universidad Peruana Unión, Lima, Peru · ³ Instituto Superior Universitario Bolivariano de Tecnología (ITB), Guayaquil, Ecuador
\* Corresponding author: jcoronel1@utmachala.edu.ec

Submitted to *Chemometrics and Intelligent Laboratory Systems*.

## Reviewer quick guide

| If you want to… | Go to |
|---|---|
| find the source of any table or figure of the manuscript | [`results/chemolab_submission/README.md`](results/chemolab_submission/README.md) |
| check a specific claim and its interpretation limits | [`docs/MANUSCRIPT_EVIDENCE_MAP.md`](docs/MANUSCRIPT_EVIDENCE_MAP.md) |
| see the exact validation design, leakage rules and candidate grids (Table 2) | [`config/PROTOCOL_V1.md`](config/PROTOCOL_V1.md), `config/nested_loeo_protocol_v1.json` |
| inspect the submitted figures | [`results/chemolab_submission/figures/`](results/chemolab_submission/figures/) (byte-identical to the images in the Word files) |
| read the analysis code | NB01 in `notebooks/`; NB02–NB08 via `python scripts/rebuild_analysis_mirrors.py`; post-hoc NB09–NB12 and NB14–NB17 in `notebooks/post_hoc/` |
| verify integrity in one command | `python scripts/audit_repository.py` (standard library only; also run by CI) |
| regenerate all 26 figures | `pip install -r requirements-figures.txt`, then the commands under [Regenerate the figures](#regenerate-the-figures) |
| see what is confirmatory and what is post-hoc | [Evidence layers](#evidence-layers) below |
| check statistical scope (n = 4 experiments) | [`docs/STATISTICAL_ANALYSIS.md`](docs/STATISTICAL_ANALYSIS.md) |
| obtain the data | DOI [10.15125/BATH-01459](https://doi.org/10.15125/BATH-01459); [`docs/DATASET.md`](docs/DATASET.md) |

## Research question

To what extent do machine-learning models for multisensor banana-ripeness classification preserve predictive performance, model-selection decisions and probabilistic reliability when evaluated on acquisition experiments completely excluded from model development, and can unlabeled domain normalization correct the shift without borrowing information from the future of the target experiment?

## Data source

University of Bath Research Data Archive, **Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”**, DOI `10.15125/BATH-01459`, licence CC BY 4.0. Raw data are not redistributed here.

The primary analysis uses the TPHiS release (temperature, pressure, humidity and 18 spectral channels, 410–940 nm), which provides the common basis for the four acquisition experiments (Tests 2–5) required by nested Leave-One-Experiment-Out validation. After removing the inferred balancing tail of the released files, 17,662 original observations remain (Table 1, Table S1).

## Leakage-safe design

The confirmatory evaluation uses nested **Leave-One-Experiment-Out (LOEO)** validation. In each outer fold one complete experiment is excluded from scaling, hyperparameter selection, algorithm selection, resampling and calibration fitting until final external evaluation; inner folds also leave one development experiment out.

- Algorithms: ordinal logistic regression, PLS-DA, SVM-RBF, random forest, XGBoost.
- Sensor representations: TPH, Spectral, TPH + Spectral.

## Evidence layers

| Layer | What it contains | Where |
|---|---|---|
| **1. Frozen confirmatory pipeline** (NB01–NB08) | data audit and LOEO protocol, experiment-shift diagnostics, inner selection, outer evaluation, imbalance sensitivity, calibration (NB06-v1.1 authoritative), statistical inference, table packaging | `notebooks/01_…ipynb`, `archive/frozen_notebook_payloads/`, `config/`, `results/main_tables/`, `results/frozen_numeric_facts_nb08.json` |
| **2. Explanatory additions** (after freezing) | count audit, stage-matched n, no-skill baseline (Tables S1–S3); TreeSHAP (Figure S1) | `results/supplementary_tables_S1_S3/` |
| **3. Post-hoc robustness** (NB09–NB12, NB14–NB17) | random references; SNV and DOMAIN_Z; duplicate-aware and shared-signature analyses; prospective initial-window normalization and composition stress; displacement, loadings, projections, error localization; reliability diagrams; positive control, MSC, alternative calibrators | `results/post_hoc/`, `notebooks/post_hoc/` |
| **Submission package** | table/figure map, the 26 submitted figures, their SHA-256 and their sources | `results/chemolab_submission/` |

Layers 2 and 3 never modify frozen outer predictions, model rankings, calibration fits or confirmatory estimates.

```text
Frozen pipeline
01 Data audit and frozen LOEO protocol → 02 PCA / UMAP / experiment-shift diagnostics
→ 03 Inner experiment-disjoint model selection → 04 Confirmatory outer LOEO evaluation
→ 05 Imbalance sensitivity → 06 / 06-v1.1 Probabilistic reliability (v1.1 authoritative for temperature scaling)
→ 07 Statistical inference → 08 Frozen evidence packaging

Post-hoc layer
09 Random references and random-selection null      10 SNV and complete-target DOMAIN_Z
11 Duplicate-aware analysis                          12 Shared-signature removal
14 Prospective initial-window DOMAIN_Z, composition stress
15 Displacement, PCA loadings, projections, error localization
16 Reliability diagrams                              17 Positive control, MSC, alternative calibrators
```

## Main results

Frozen confirmatory analysis (17,662 observations, four external experiments, three modalities, five algorithms; 60 external model cells; 12 outer experiment × modality selection scenarios):

- internal winner = external winner: **1/12**;
- mean selection loss: **0.1147 Macro-F1** (maximum 0.2148);
- mean inner-vs-external Spearman rank correlation: **−0.0754**;
- partial η² on external Macro-F1: held-out experiment **0.4661**, algorithm **0.0531**;
- development-only temperature scaling: mean ECE **0.497 → 0.257** for the 10 scenarios with native probabilities (0.4387 → 0.2568 over all 12 selected models including softmax surrogates);
- class weighting and training-only SMOTE: about **+0.004** Macro-F1 on average, heterogeneous across experiments.

Post-hoc analyses:

- complete-target (transductive) DOMAIN_Z raised mean selected spectral Macro-F1 from **0.131 to 0.418**;
- estimated prospectively from the first 25 unique spectra, it raised Macro-F1 only from **0.125 to 0.175**, improving 2 of 4 experiments; windows of 10 and 50 gave no consistent improvement;
- initial windows contained almost only unripe fruit, and window stage composition alone changed Macro-F1 by up to **0.19**;
- raw spectral PC1 is a nearly uniform intensity/baseline axis (92.6% of variance in the Test 3 fold);
- positive control: the same model families reach Macro-F1 **0.962–0.995** under pooled random 5-fold CV and **0.958–0.994** within single experiments, versus **0.108–0.158** under nested LOEO;
- MSC (0.203) behaves like SNV (0.211); vector scaling and isotonic calibration do not transfer better than temperature scaling.

The central result is not a universal winning classifier: experiment-specific distribution shift dominates algorithm choice, destabilizes model selection and reduces probability transportability.

## Statistical scope

Only the **four held-out experiments** are independent generalization units. Row-level bootstrap intervals are conditional on a held-out experiment. The factorial OLS/ANOVA is a descriptive effect-size decomposition. With four experiments the smallest attainable two-sided exact sign-flip p-value is 0.125. Details: [`docs/STATISTICAL_ANALYSIS.md`](docs/STATISTICAL_ANALYSIS.md).

## Reproduce

### Integrity audit (no data needed)

```bash
python scripts/audit_repository.py
```

Read-only, standard library only. It checks the frozen notebook hashes and syntax, the LOEO protocol, frozen numerical evidence, all evidence tables, Tables S1–S3, post-hoc notebooks and evidence, citation metadata (three authors), Markdown links, file policy, and that each of the 26 submitted figures is byte-identical to the image embedded in the manuscript.

### Analysis notebooks

1. Download the Bath dataset (DOI `10.15125/BATH-01459`) and place `ds_34.zip`, `Spect.zip`, `TPHiS.zip` and `VOC.zip` as described in [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md).
2. Install `requirements.txt` or `environment.yml` (Python 3.13.15).
3. Materialize NB02–NB08 and readable Python mirrors: `python scripts/rebuild_analysis_mirrors.py`.
4. Run NB01–NB08 in order and compare with `results/main_tables/` and `results/frozen_numeric_facts_nb08.json`.
5. Tables S1–S3: `python scripts/make_supplementary_tables_S1_S3.py --tphis-zip /path/to/TPHiS.zip --output-dir results/supplementary_tables_S1_S3`.
6. Post-hoc notebooks: `notebooks/post_hoc/` (NB09–NB12 and NB14–NB16 read frozen outputs or the master file; NB17 runs in Colab or locally, CPU, about 4 h).

### Regenerate the figures

```bash
pip install -r requirements-figures.txt
python scripts/make_publication_figures.py --out figures_out     # Figs. 1, 2, 7-11, S8-S10, S12-S15
python scripts/postprocess_notebook_figures.py --out figures_out   # Figs. 3-6, S1-S7, S11
python scripts/verify_figures.py figures_out                     # compare with the submitted figures
```

All 26 PNGs are byte-identical to the submitted files with these versions; CI repeats this check on every push and pull request.

## Repository structure

```text
.github/workflows/             CI: integrity audit + figure regeneration check
archive/frozen_notebook_payloads/  immutable NB02–NB08 source-clean notebooks (base85+gzip)
config/                        frozen nested-LOEO protocol and exact candidate grids
docs/                          dataset, data availability, reproducibility, statistics, evidence map, checklist
notebooks/
  01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb
  post_hoc/                    NB09–NB12, NB14–NB17 post-hoc notebooks + notebook_provenance.csv
results/
  main_tables/                 frozen analytical tables (NB08)
  frozen_numeric_facts_nb08.json
  supplementary_tables_S1_S3/  Tables S1–S3
  post_hoc/                    NB09–NB12 and NB14–NB17 exported evidence
  chemolab_submission/         table/figure map, figures/, figure_sources/, figure_provenance.csv
  table_manifest.csv, figure_manifest.csv
scripts/
  audit_repository.py          read-only integrity audit
  rebuild_analysis_mirrors.py  materialize NB02–NB08 and Python mirrors
  make_supplementary_tables_S1_S3.py  Tables S1–S3 from TPHiS.zip
  make_publication_figures.py  Figs. 1, 2, 7–11, S8–S10, S12–S15
  postprocess_notebook_figures.py  Figs. 3–6, S1–S7, S11
  verify_figures.py            compare regenerated and submitted figures
requirements.txt, environment.yml, requirements-figures.txt, CITATION.cff, LICENSE
```

## Exclusions and safeguards

- `external_support_distance_ratio` (exploratory NB02) is excluded: duplicate spectral vectors produced zero denominators.
- Post-hoc external best models are descriptive comparators, never leakage-safe selections.
- SMOTE is applied only inside training data; calibration is learned from development-only cross-fitted predictions.
- Complete-target DOMAIN_Z is transductive; the prospective NB14 estimate is the deployable one.
- TreeSHAP is explanatory, not causal.
- NB17's tree-ensemble candidate grid differs from NB03; this is disclosed in `config/PROTOCOL_V1.md` and explains its two non-identical scenarios.
- Raw archives and large row-level dumps are not committed; files are limited to 10 MiB.
- NB08's corrected source-clean serialization is documented in [`docs/EXECUTED_NOTEBOOK_PROVENANCE.md`](docs/EXECUTED_NOTEBOOK_PROVENANCE.md).

## Data and code availability

[`docs/DATASET.md`](docs/DATASET.md) · [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md) · [`docs/REPRODUCIBILITY.md`](docs/REPRODUCIBILITY.md) · [`docs/EXECUTED_NOTEBOOK_PROVENANCE.md`](docs/EXECUTED_NOTEBOOK_PROVENANCE.md) · [`docs/STATISTICAL_ANALYSIS.md`](docs/STATISTICAL_ANALYSIS.md) · [`docs/MANUSCRIPT_EVIDENCE_MAP.md`](docs/MANUSCRIPT_EVIDENCE_MAP.md) · [`docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md`](docs/REVIEWER_REPRODUCIBILITY_CHECKLIST.md)

## Citation

`CITATION.cff` lists the three manuscript authors (Coronel-Reyes, Haro-Sarango, Triviño Sanchez) and the software metadata. The preferred citation will be updated with the journal DOI after publication.

## License

Analysis code: MIT License. Source dataset: CC BY 4.0, retained under the original University of Bath terms and not relicensed here.
