# Frozen notebook inventory

The analysis contains nine frozen notebook stages. NB01 is committed directly because it is small and is the entry point for raw-data auditing. NB02–NB08 are preserved byte-for-byte in `archive/frozen_notebook_payloads/` and can be materialized locally with:

```bash
python scripts/rebuild_analysis_mirrors.py
```

The repository audit decodes the archived notebooks in memory and verifies their frozen SHA-256 values and Python syntax.

| Stage | Notebook | Frozen SHA-256 |
|---|---|---|
| 01 | `01_DATA_AUDIT_AND_FROZEN_LOEO.ipynb` | `02356fe8a51e6ae61b93b5289f1becbdbd99021418922a287a8df2a6776c75a8` |
| 02 | `02_PCA_UMAP_DOMAIN_SHIFT.ipynb` | `4c18bdc8ed0cf39afc474e72f1237a4017bb4996bb3811bcd3cf916db7240f9c` |
| 03 | `03_INNER_LOEO_MODEL_SELECTION.ipynb` | `7b11ba55fd472c8955a1d8b3077d2a653810b5f27ffc54f98d6735fd5f86c5fe` |
| 04 | `04_OUTER_LOEO_EVALUATION.ipynb` | `29e3bcb96a4dfae3c5749f1c3e3988caf57fd7f3bee4f3bd447e3d53478c4d4e` |
| 05 | `05_BALANCING_SENSITIVITY_CLASSWEIGHT_SMOTE.ipynb` | `20c7b95995c417fc4e00f35af11fc3a11baf6cea0c127fbbee5cc6a6702383f9` |
| 06 | `06_CALIBRATION_RELIABILITY_ORDINAL.ipynb` | `21cc97bac89b13a910e5a7a4009de0a5713ed3b7364239db678edfac32484eca` |
| 06-v1.1 | `06_v1_1_CALIBRATION_WIDE_TEMPERATURE.ipynb` | `d8999076c4c067be8aba6a83f3ad2b5351c784ac7646f879c1055aa024f496bd` |
| 07 | `07_FINAL_STATISTICAL_INFERENCE.ipynb` | `3232477307baea128472ecd12fee0346168a548cf6b117a99ca7f8e1878b674b` |
| 08 | `08_FINAL_MANUSCRIPT_TABLES_FIGURES.ipynb` | `59b4f7e2dcc6cfb214536cf31736b50a2af9666b207387eb897ff6f994d58c9e` |

NB08's source-clean hash reflects the canonical output-stripped compact serialization preserved by the immutable archive payload; no analytical code or manuscript values were changed. NB06-v1.1 supersedes NB06 **only for the final temperature-scaling values**. NB06 remains part of the provenance chain.
