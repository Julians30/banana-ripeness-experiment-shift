# Repository scripts

## `audit_repository.py`

Read-only integrity audit used by GitHub Actions and available locally:

```bash
python scripts/audit_repository.py
```

It uses only the Python standard library. It decodes the frozen NB02–NB08 provenance payloads in memory, verifies the exact notebook hashes and syntax, checks the nested-LOEO protocol and frozen numerical evidence, confirms both frozen and revised-manuscript evidence layers, verifies reviewer-requested Tables S1–S3, checks environment/citation metadata and evidence traceability, and enforces repository file policy.

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
