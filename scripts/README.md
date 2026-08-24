# Repository scripts

## `audit_repository.py`

Read-only integrity audit used by GitHub Actions and available locally:

```bash
python scripts/audit_repository.py
```

It uses only the Python standard library. It decodes the frozen NB02–NB08 provenance payloads in memory, verifies the exact notebook hashes and syntax, checks the nested-LOEO protocol and frozen numerical evidence, confirms the manuscript-table inventory and evidence map, and enforces repository file policy.

**CI does not modify or push repository files.**

## `rebuild_analysis_mirrors.py`

Local reviewer convenience tool:

```bash
python scripts/rebuild_analysis_mirrors.py
```

It reconstructs NB02–NB08 from `archive/frozen_notebook_payloads/`, verifies all nine frozen notebook SHA-256 values, and generates readable Python mirrors from the notebook code cells.

The generated notebooks and mirrors are convenience artifacts. The frozen archive payloads remain the integrity source checked by CI.
