#!/usr/bin/env python3
"""Regenerate reviewer-requested count, no-skill, and stage-matching audits.

This script does not train or select manuscript classifiers. It reconstructs
three reviewer-requested supplementary tables directly from the original TPHiS
release while preserving the frozen experiment boundaries used in NB01.

Usage:
    python scripts/09_REVIEWER_REQUESTED_AUDITS.py \
        --tphis-zip /path/to/TPHiS.zip \
        --output-dir results/reviewer_revision

The script requires pandas, numpy and scikit-learn from requirements.txt.
"""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score

CUTOFF = 17662
OUTERS = (2, 3, 4, 5)
ALL_STAGES = (1, 2, 3, 4, 5)
MATCH_CAP = 600


def load_original_tphis(zip_path: Path) -> pd.DataFrame:
    parts = []
    with zipfile.ZipFile(zip_path) as zf:
        for split in ("train", "test"):
            x = pd.read_csv(zf.open(f"TPHiS_x_{split}.csv")).rename(
                columns={"Unnamed: 0": "source_index"}
            )
            y = pd.read_csv(zf.open(f"TPHiS_y_{split}.csv")).rename(
                columns={"Unnamed: 0": "source_index", "0": "stage"}
            )
            if not np.array_equal(x["source_index"].to_numpy(), y["source_index"].to_numpy()):
                raise ValueError(f"X/Y source indices differ in {split}")
            x["stage"] = y["stage"].to_numpy(dtype=int)
            x["provided_split"] = split
            parts.append(x)

    released = (
        pd.concat(parts, ignore_index=True)
        .sort_values("source_index")
        .reset_index(drop=True)
    )
    if released["source_index"].nunique() != len(released):
        raise ValueError("source_index is not unique in released TPHiS data")

    original = released.loc[released["source_index"] < CUTOFF].copy()
    if len(original) != CUTOFF:
        raise ValueError(f"Expected {CUTOFF} inferred-original rows, found {len(original)}")

    original["test_id"] = np.select(
        [
            original["source_index"].between(0, 1719),
            original["source_index"].between(1720, 6496),
            original["source_index"].between(6497, 12629),
            original["source_index"].between(12630, 17661),
        ],
        [2, 3, 4, 5],
        default=-1,
    ).astype(int)
    if (original["test_id"] == -1).any():
        raise ValueError("Unassigned original rows remain after experiment mapping")
    return released, original


def count_audit(released: pd.DataFrame) -> pd.DataFrame:
    original = released.loc[released["source_index"] < CUTOFF]
    tail = released.loc[released["source_index"] >= CUTOFF]
    rows = []
    for stage in ALL_STAGES:
        n0 = int((original["stage"] == stage).sum())
        nt = int((tail["stage"] == stage).sum())
        total = int((released["stage"] == stage).sum())
        rows.append(
            {
                "Stage": stage,
                "Inferred original block": n0,
                "Inferred balancing tail": nt,
                "Released balanced total": total,
                "Deficit to 6,533": 6533 - n0,
            }
        )
    out = pd.DataFrame(rows)
    out.loc[len(out)] = {
        "Stage": "Total",
        "Inferred original block": int(out["Inferred original block"].sum()),
        "Inferred balancing tail": int(out["Inferred balancing tail"].sum()),
        "Released balanced total": int(out["Released balanced total"].sum()),
        "Deficit to 6,533": int(out["Deficit to 6,533"].sum()),
    }
    return out


def no_skill_baseline(original: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for outer in OUTERS:
        dev = original.loc[original["test_id"] != outer]
        ext = original.loc[original["test_id"] == outer]
        dev_majority = int(dev["stage"].value_counts().idxmax())
        y = ext["stage"].to_numpy(dtype=int)
        pred = np.full(len(ext), dev_majority, dtype=int)
        observed = sorted(np.unique(y).tolist())
        rows.append(
            {
                "Outer": outer,
                "Dev. majority stage": dev_majority,
                "External stages": ",".join(map(str, observed)),
                "External n": len(ext),
                "Accuracy": float(np.mean(y == pred)),
                "Macro-F1": float(
                    f1_score(y, pred, labels=observed, average="macro", zero_division=0)
                ),
                "Balanced acc.": float(balanced_accuracy_score(y, pred)),
            }
        )
    return pd.DataFrame(rows)


def stage_match_sizes(original: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for outer in OUTERS:
        dev = original.loc[original["test_id"] != outer]
        ext = original.loc[original["test_id"] == outer]
        for stage in ALL_STAGES:
            nd = int((dev["stage"] == stage).sum())
            ne = int((ext["stage"] == stage).sum())
            nm = min(nd, ne, MATCH_CAP)
            rows.append(
                {
                    "Outer": outer,
                    "Stage": stage,
                    "Development n": nd,
                    "External n": ne,
                    "Matched n / domain": nm,
                    "Total classifier n": 2 * nm,
                }
            )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tphis-zip", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("results/reviewer_revision"))
    args = parser.parse_args()

    released, original = load_original_tphis(args.tphis_zip)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    t1 = count_audit(released)
    t2 = no_skill_baseline(original)
    t3 = stage_match_sizes(original)

    t1.to_csv(args.output_dir / "Table_S1_reconstruction_count_audit.csv", index=False)
    t2.to_csv(
        args.output_dir / "Table_S3_development_majority_no_skill_baseline.csv",
        index=False,
        float_format="%.3f",
    )
    t3.to_csv(args.output_dir / "Table_S2_stage_matched_effective_sample_sizes.csv", index=False)

    # Hard assertions for the audited public release.
    assert t1.loc[t1["Stage"] == "Total", "Inferred original block"].item() == 17662
    assert list(t2["Macro-F1"].round(3)) == [0.000, 0.073, 0.070, 0.075]
    assert int(t3.query("Outer == 2 and Stage == 2")["Matched n / domain"].item()) == 17
    assert int(t3.query("Outer == 5 and Stage == 1")["Matched n / domain"].item()) == 2

    print("PASS: reviewer-requested Tables S1-S3 regenerated.")
    print(f"Wrote outputs to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
