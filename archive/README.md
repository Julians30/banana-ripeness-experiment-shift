# Frozen notebook provenance archive

This directory preserves the immutable NB02–NB08 source-clean notebook payloads used by the repository integrity audit. The payloads are exact base85+gzip encodings of the frozen notebook bytes and are not an alternative analysis.

Use `python scripts/rebuild_analysis_mirrors.py` to reconstruct all notebooks locally. Any change to a payload will fail the integrity audit.
