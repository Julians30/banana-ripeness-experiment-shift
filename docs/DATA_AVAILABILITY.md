# Data availability

The raw banana multisensor dataset analyzed in this study is publicly available from the University of Bath Research Data Archive:

**Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”**

DOI: https://doi.org/10.15125/BATH-01459

License: CC BY 4.0

This repository does not redistribute the raw dataset. It provides the analysis notebooks, frozen validation protocol, software environment, manuscript-facing numerical outputs, and provenance information required to reconstruct the study after downloading the source data from the original archive.

The audited master file generated during the project had SHA-256:

`0a06fb3773f85dacee42e18eecf17e5e2a8e7f5e9508cd3d60bd4b66757e8ea8`

The frozen LOEO protocol has SHA-256:

`86731ff9a292f1afd35a215105b14c4af3aa2bda5e8c4dad4df639d4d82ad930`

Post-hoc robustness evidence (NB14–NB17) is versioned in `results/post_hoc/`. Record-level files there contain development-fitted projection coordinates, predictions and error outcomes, not raw sensor values. The 26 figures embedded in the submitted manuscript are versioned in `results/chemolab_submission/figures/` together with the files needed to regenerate them.

Large intermediate prediction files are not required for understanding the manuscript results and are not duplicated in the Git repository. A versioned archival snapshot of this repository (for example a Zenodo DOI linked to a GitHub release) can be created at acceptance and cited in the data availability statement.
