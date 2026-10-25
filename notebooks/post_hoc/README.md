# Post-hoc notebooks

Notebooks run after the frozen confirmatory pipeline. They read the audited master file produced by NB01 (`06_master_original_multisensor.csv`, 17,662 observations) and never overwrite frozen outputs.

| Notebook | Status |
|---|---|
| `17_REVIEWER_SHIELD_POSITIVE_CONTROL_MSC_CALIBRATORS.ipynb` | included and executed (outputs in `../../results/post_hoc/nb17_reviewer_shield/`); CPU runtime about 4 h; checkpoints after every modality/arm; verifies the master file against manuscript Table 1 before fitting |
| NB09–NB12, NB14–NB16 | exported evidence in `../../results/post_hoc/`; notebooks to be added |

NB17 re-implements the nested LOEO selection rule with the Table 2 algorithms and preprocessing; its LOEO arm is compared with manuscript Table 4 in the final cell (`A_check_vs_table4.csv`: same selected model in 11/12 scenarios, Macro-F1 identical to three decimals in 10/12). Its ordinal-logistic, PLS-DA and SVM candidates equal NB03, but its tree-ensemble candidates differ (random forest: full 2 × 2 × 2 factorial, 8 configurations; XGBoost: (250, 2, 0.10), (250, 3, 0.05), (500, 4, 0.03), (500, 5, 0.05)); both non-identical scenarios are ones in which a tree ensemble was selected. Exact NB03 grids: `../../config/PROTOCOL_V1.md`.

**Running NB17.** In Google Colab it finds the master file in Google Drive. Locally, install `requirements.txt` and set `NB17_MASTER_CSV=/path/to/06_master_original_multisensor.csv` (and optionally `NB17_OUT_DIR`). Cells 1–2 (environment and paths) were generalized after the executed run so that the notebook runs outside Colab, and cell 8 now also records the master-file SHA-256; the analysis code in cells 3–8 is the code that produced `../../results/post_hoc/nb17_reviewer_shield/`.
