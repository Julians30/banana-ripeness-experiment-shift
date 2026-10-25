# NB15 interpretation



PCA/UMAP are exploratory, fitted only to development future-row records; external observations are transformed. All 18 channels are standardized using development data after the named representation.

PREFIX uses each domain initial 25 unique signatures; FULL_TARGET uses each domain complete unique-signature feature statistics and is transductive.

Classifiers were not refitted. Only RAW/PREFIX have NB14 predictions; SNV/FULL_TARGET are visual diagnostics here.

Vector-stage records can share a spectral state with conflicting labels; projections will coincide. No jitter is added to create artificial separation.

UMAP is an exploratory embedding; different fits have different coordinate systems. PCA coefficient sign is anchored only for display.

Row/signature resampling intervals are conditional sensitivity analyses on frozen predictions; signatures are not established independent biological units. Temporal and fruit-level dependence remain unresolved.

Leave-one-experiment-out summaries are descriptive across four outer folds with overlapping training sets. No population p-values are reported.

Use stage support and per-experiment predictions with all pooled summaries. Do not infer biochemical mechanisms from coefficients or causality from embeddings.



 outer_test   n  n_signatures   raw_f1  prefix_f1  delta_mae  delta_severe  delta_f1
          2 112           110 0.078947   0.309884  -0.116071      0.142857  0.230937
          3 666           632 0.228477   0.084629   0.905405      0.367868 -0.143848
          4 351           341 0.193828   0.096760  -0.398860     -0.122507 -0.097067
          5 666           658 0.000677   0.210587  -1.689189     -0.726727  0.209910



 omitted_test  retained_experiments  mean_delta_f1  mean_delta_mae  mean_delta_severe
            2                     3      -0.010335       -0.394215          -0.160455
            3                     3       0.114593       -0.734707          -0.235459
            4                     3       0.099000       -0.299952          -0.072001
            5                     3      -0.003326        0.130158           0.129406