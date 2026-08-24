# Notebooks

These notebooks are the authoritative analysis record for the manuscript. They are preserved in analytical order.

1. `01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb` - source audit and frozen nested LOEO protocol.
2. `02_PCA_UMAP_DOMAIN_SHIFT.ipynb` - PCA, UMAP, stage-matched domain AUC and MMD diagnostics.
3. `03_INNER_LOEO_MODEL_SELECTION.ipynb` - experiment-disjoint inner model/hyperparameter selection.
4. `04_OUTER_LOEO_EVALUATION.ipynb` - confirmatory external LOEO evaluation.
5. `05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb` - imbalance sensitivity; SMOTE is training-only.
6. `06_CALIBRATION_RELIABILITY_ORDINAL.ipynb` - original calibration/reliability analysis retained for provenance.
7. `06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb` - corrected wide-range temperature scaling. This supersedes NB06 only for final calibration values.
8. `07_FINAL_STATISTICAL_INFERENCE.ipynb` - conditional paired bootstrap and structural synthesis.
9. `08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb` - presentation-only generation of frozen manuscript tables and figures.

## Provenance

The canonical GitHub filename for NB06-v1.1 omits the temporary `_FIXED` suffix used during debugging. Its content is the corrected notebook that generated the final audited NB06-v1.1 results.

GitHub tracks source-clean notebooks with bulky execution outputs removed. Analytical code is unchanged. The executed-file hashes are documented in `docs/EXECUTED_NOTEBOOK_PROVENANCE.md`.

The notebooks were executed in Google Colab with project artifacts stored in Google Drive. Exact input data are not redistributed here; see `docs/DATASET.md` and `docs/DATA_AVAILABILITY.md`.
