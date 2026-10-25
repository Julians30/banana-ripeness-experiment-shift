# Repository scripts

## `audit_repository.py`

Read-only integrity audit used by GitHub Actions and available locally:

```bash
python scripts/audit_repository.py
```

It uses only the Python standard library. It decodes the frozen NB02–NB08 provenance payloads in memory, verifies the exact notebook hashes and syntax, checks the nested-LOEO protocol and frozen numerical evidence, confirms the frozen, reviewer-revision and post-hoc evidence layers, verifies reviewer-requested Tables S1–S3, checks environment metadata and the three-author citation metadata, checks that every relative Markdown link resolves, enforces repository file policy, and verifies that all 26 submitted figures match the SHA-256 of the images embedded in the manuscript.

**CI does not modify or push repository files.**

## `rebuild_analysis_mirrors.py`

Local reviewer convenience tool:

```bash
python scripts/rebuild_analysis_mirrors.py
```

It reconstructs NB02–NB08 from `archive/frozen_notebook_payloads/`, verifies all nine frozen notebook SHA-256 values, and generates readable Python mirrors from the notebook code cells.

The generated notebooks and mirrors are convenience artifacts. The frozen archive payloads remain the integrity source checked by CI.

## `09_REVIEWER_REQUESTED_AUDITS.py`

Regenerates the compact supplementary audits added during peer review from the original Bath `TPHiS.zip`:

```bash
python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
  --tphis-zip /path/to/TPHiS.zip \
  --output-dir results/reviewer_revision
```

It reproduces:

- Table S1 — inferred-original block versus balancing-tail counts;
- Table S2 — development-majority no-skill baseline;
- Table S3 — stage-matched effective sample sizes.

This script does **not** retrain or reselect the manuscript classifiers and does not change frozen NB01–NB08 evidence.

## `make_publication_figures.py`

Redraws Figures 1, 2, 7–11, S8–S10 and S12–S15 from tracked result tables (`results/post_hoc/`, manuscript Table 3 values); no model, calibrator or embedding is refitted:

```bash
pip install -r requirements-figures.txt
python scripts/make_publication_figures.py --out figures_out
```

## `postprocess_legacy_figures.py`

Produces Figures 3–6, S1–S7 and S11 from figures written by the analytical notebooks (`results/chemolab_submission/figure_sources/`): removes in-figure titles (journal rule) and replaces notebook-style labels with publication labels. Plot pixels are not modified; NB16 PDFs are cropped through the PDF CropBox and stay vector.

```bash
python scripts/postprocess_legacy_figures.py --out figures_out
```

## `verify_figures.py`

Compares regenerated PNGs with the submitted figures in `results/chemolab_submission/figures/` (byte identity, then pixel identity):

```bash
python scripts/verify_figures.py figures_out
```

CI runs the two figure scripts and this check on every push and pull request.
