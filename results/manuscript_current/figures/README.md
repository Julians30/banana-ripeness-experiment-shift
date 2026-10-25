# Previous-submission figure provenance

> Superseded by `../../chemolab_submission/figure_provenance.csv` (current submission). Retained for provenance.

This file records the exact SHA-256 values of the PNG images embedded in the current revised manuscript, together with stable logical filenames and analytical sources. The hashes provide a submission-level provenance link without making the presentation PNGs part of the frozen numerical evidence.

| Manuscript figure | File | SHA-256 | Analytical source / scope |
|---|---|---|---|
| Figure 1 | `Figure_1_stage_matched_domain_auc.png` | `c9d447a9c11a0b3f2763e3757c86a7f08c008a0d609e3e5640fceef8ccc04330` | Stage-matched experiment discriminability with repeated stratified 5-fold CV ×3 uncertainty. NB02 diagnostics; reviewer-requested ±1 SD visualization. |
| Figure 2 | `Figure_2_selected_models_external_macro_f1.png` | `4e3c09ff01e10602b454a295076a038b75842606cd64dfd20540175c284ecb92` | External Macro-F1 of internally selected models. NB04/NB08 frozen selected-model evidence. |
| Figure 3 | `Figure_3_model_selection_transportability.png` | `8660e842aa40c7dfec8dce50b03e42537c25c2a6f4c2d1fcb9d87b792e80449d` | Internal rank-1 vs rank-2 and selected-vs-post-hoc-best transportability. NB04/NB07 plus reviewer-requested direct selection-loss panel. |
| Figure 4 | `Figure_4_ece_raw_vs_temperature_scaled.png` | `42725a5bced3feb40be9ef07c6954984aabc576af553e7e731d0807c5d65e782` | Raw versus development-fitted temperature-scaled ECE. NB06-v1.1; near-zero T2|TPH calibrated ECE explicitly labeled. |
| Figure 5 | `Figure_5_macro_f1_partial_eta_squared.png` | `acb9214549c571460932acb1fc12e236634544c10160fc24326ca703bd32e329` | Descriptive partial eta-squared decomposition of external Macro-F1. NB07/NB08; descriptive structural effect sizes only. |
| Figure S1 | `Figure_S1_balancing_effect_by_experiment.png` | `b913ec2489228cd58470085c9d9082e838b7bcb809e2a83fa5025353a0e98372` | External Macro-F1 sensitivity to imbalance treatment. NB05/NB08. |
| Figure S2 | `Figure_S2_calibration_transfer_by_experiment.png` | `601276fddffbd8930430629f12ad7eea09abfede868e3d4c2e0c7e4fabc03971` | Experiment-level calibration-transfer heterogeneity. NB06-v1.1/NB08. |
| Figure S3 | `Figure_S3_treeshap_spectral_tree_models.png` | `b45fe834e60a64c3bae4fe187b43f2bfb5fbb26289ac7c6444be51aec482cf97` | Post-hoc TreeSHAP attribution for spectral RF/XGBoost models. Reviewer-requested explanatory analysis using frozen outer-fold hyperparameters; not causal or used for selection. |

## Interpretation safeguards

- Figure S3 is **post-hoc explanatory** evidence; SHAP magnitude is not causal biochemical evidence.
- Figure 4 uses NB06-v1.1 for final temperature-scaling values.
- Figure 5 is descriptive because only four outer experiments are independent generalization units.
- `external_support_distance_ratio` is excluded from manuscript evidence.
