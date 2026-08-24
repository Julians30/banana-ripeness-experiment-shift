# Dataset provenance

## Source

University of Bath Research Data Archive

**Dataset for “Low-Cost, Multi-Sensor Non-Destructive Banana Ripeness Estimation Using Machine Learning”**

DOI: https://doi.org/10.15125/BATH-01459

License: **CC BY 4.0**

## Source archives used in the project

The study workspace contains four source archives from the Bath record:

- `ds_34.zip` — all-sensor data for Tests 3 and 4
- `Spect.zip` — spectral data for Tests 2, 3 and 5
- `TPHiS.zip` — temperature/pressure/humidity + spectral data for Tests 2, 3, 4 and 5
- `VOC.zip` — VOC sensor data for Tests 3 and 4

The primary confirmatory analysis uses the **TPHiS** representation because it provides the common four-experiment basis required for nested leave-one-experiment-out evaluation.

## Primary experiments

Tests 2, 3, 4 and 5 are treated as independent acquisition experiments for external validation.

Original TPHiS observations retained after audit: **17,662**.

Experiment counts:

- Test 2: 1,720
- Test 3: 4,777
- Test 4: 6,133
- Test 5: 5,032

Important target-support differences are retained rather than artificially harmonized: Test 2 has no stage-5 observations and Test 5 contains only two stage-1 observations.

## Data redistribution

Raw Bath data are **not redistributed in this repository**. Users should download the dataset from the original DOI and preserve its attribution/license requirements.

## Frozen master-file provenance

The audited project master file used by the analyses was:

`06_master_original_multisensor.csv`

SHA-256:

`0a06fb3773f85dacee42e18eecf17e5e2a8e7f5e9508cd3d60bd4b66757e8ea8`

The frozen nested LOEO protocol is stored in `config/nested_loeo_protocol_v1.json`.
