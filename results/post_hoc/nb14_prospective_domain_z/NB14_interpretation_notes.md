# NB14 — prospective DOMAIN_Z reviewer analysis

## Data chronology
- No timestamp/date fields exist in the released raw feature CSV files.
- Therefore, this analysis uses the original source index as an acquisition-order proxy and does not claim hour/day timing.
- Primary calibration window: first 25 unique spectral signatures; sensitivity windows: [10, 25, 50].

## Primary N=25 result
- Mean RAW future-only Macro-F1: 0.1255.
- Mean prospective DOMAIN_Z Macro-F1: 0.1755.
- Mean full-target diagnostic Macro-F1 on the same future-only rows: 0.1624.
- Mean prospective DOMAIN_Z minus RAW: +0.0500.
- DOMAIN_Z better than RAW in 2/4 outer experiments.
- Mean oracle minus prospective prefix gap: -0.0130.
- Maximum absolute fold-specific oracle-prefix gap: 0.1429.
- With only four outer experiments, the minimum possible two-sided exact sign-test p for 4/4 changes in one direction is 0.125.

## Interpretation guardrail
If prefix-only DOMAIN_Z remains materially above RAW while the full-target diagnostic adds little, the normalization result is robust to future-target feature leakage under the available order proxy.
If the full-target diagnostic substantially exceeds prefix-only DOMAIN_Z, the earlier whole-target result should be described as optimistic/transductive and removed from the headline.

## Composition stress
The early/late calibration-mixture analysis is diagnostic only: target stage labels are used to construct stress-test calibration subsets and are not part of the deployable prospective pipeline.
