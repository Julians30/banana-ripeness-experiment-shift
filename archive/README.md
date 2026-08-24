# Reproducibility archive

This directory contains **immutable provenance payloads**, not working analysis files.

`frozen_notebook_payloads/` stores compact Base85+gzip representations of the eight source-clean notebooks NB02–NB08. They are retained only so a fresh clone can reconstruct the exact notebook bytes even when GitHub Actions or a local environment has not yet materialized the reviewer-facing files.

Run:

```bash
python scripts/rebuild_analysis_mirrors.py
```

The script decodes each missing notebook, verifies its frozen SHA-256 and byte count, validates the JSON, and then generates a deterministic Python mirror from its code cells. NB01 is already stored directly in `notebooks/` because it defines the initial data audit and frozen LOEO protocol.

The archived payloads are **not analytical alternatives** and must never be edited independently. The expected source-clean hashes are frozen in `scripts/rebuild_analysis_mirrors.py`, `scripts/audit_repository.py`, and `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`.
