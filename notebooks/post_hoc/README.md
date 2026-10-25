# Post-hoc notebooks

Notebooks run after the frozen confirmatory pipeline. They read the audited master file produced by NB01 (`06_master_original_multisensor.csv`, 17,662 observations) and never overwrite frozen outputs.

| Notebook | Status |
|---|---|
| `17_REVIEWER_SHIELD_POSITIVE_CONTROL_MSC_CALIBRATORS.ipynb` | included and executed (outputs in `../../results/post_hoc/nb17_reviewer_shield/`); CPU runtime about 4 h; checkpoints after every modality/arm; verifies the master file against manuscript Table 1 before fitting |
| NB09–NB12, NB14–NB16 | exported evidence in `../../results/post_hoc/`; notebooks to be added |

NB17 re-implements the Table 2 candidate grid and the nested LOEO selection rule; its LOEO arm is compared with manuscript Table 4 in the final cell.
