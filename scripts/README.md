# Analysis scripts

This directory exposes one deterministic, text-diff-friendly Python mirror for each authoritative notebook. The mirrors are intended for **code review, searching, static inspection, and reproducibility auditing**. The Jupyter notebooks in `../notebooks/` remain the canonical execution record.

| Notebook | Python mirror |
|---|---|
| `01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb` | `01_DATA_AUDIT_AND_FROZEN_LOEO.py` |
| `02_PCA_UMAP_DOMAIN_SHIFT.ipynb` | `02_PCA_UMAP_DOMAIN_SHIFT.py` |
| `03_INNER_LOEO_MODEL_SELECTION.ipynb` | `03_INNER_LOEO_MODEL_SELECTION.py` |
| `04_OUTER_LOEO_EVALUATION.ipynb` | `04_OUTER_LOEO_EVALUATION.py` |
| `05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb` | `05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.py` |
| `06_CALIBRATION_RELIABILITY_ORDINAL.ipynb` | `06_CALIBRATION_RELIABILITY_ORDINAL.py` |
| `06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb` | `06_v1_1_CALIBRATION_WIDE_TEMPERATURE.py` |
| `07_FINAL_STATISTICAL_INFERENCE.ipynb` | `07_FINAL_STATISTICAL_INFERENCE.py` |
| `08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb` | `08_FINAL_MANUSCRIPT_TABLES_FIGURES.py` |

`rebuild_analysis_mirrors.py` verifies the frozen notebook byte hashes before regenerating these scripts. Notebook-only `!` shell commands and `%` magics are retained as comments so the mirrors remain syntactically valid Python; all other code-cell text is preserved.

`audit_repository.py` verifies that:
- all nine notebooks are directly present and byte-identical to the frozen GitHub sources;
- all nine Python mirrors exactly match deterministic extraction from those notebooks;
- the frozen LOEO protocol and numerical manuscript evidence remain unchanged;
- the manuscript evidence map, main tables, README safeguards, and repository file policy remain internally consistent.

Do not edit generated analysis mirrors manually. Edit the authoritative notebook only when a scientifically justified change is required, then deliberately update provenance and regenerate the mirror.
