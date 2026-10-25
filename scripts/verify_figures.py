"""Compare regenerated figures with the figures embedded in the submitted manuscript and supplementary file.

Usage:  python scripts/verify_figures.py figures_out

For every PNG in the given folder that also exists in results/chemolab_submission/figures/, reports whether the
files are byte-identical (SHA-256) and, if not, whether the decoded pixels are identical (requires Pillow + numpy).
PNG bytes can differ across matplotlib/Pillow versions even when the drawing is unchanged.
Exit status is 1 if any figure differs at pixel level.
"""
import hashlib, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REF = ROOT / "results" / "chemolab_submission" / "figures"
new_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "figures_out")
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
failed, checked = [], 0
for new in sorted(new_dir.glob("*.png")):
    ref = REF / new.name
    if not ref.exists():
        continue
    checked += 1
    if sha(new) == sha(ref):
        print(f"{new.name:16s} byte-identical")
        continue
    import numpy as np
    from PIL import Image
    a, b = np.asarray(Image.open(new).convert("RGB")), np.asarray(Image.open(ref).convert("RGB"))
    same = a.shape == b.shape and bool((a == b).all())
    if same:
        detail = "pixel-identical (different PNG encoding)"
    elif a.shape != b.shape:
        detail = f"DIFFERENT size {a.shape[1]}x{a.shape[0]} vs submitted {b.shape[1]}x{b.shape[0]}"
    else:
        diff = np.abs(a.astype(int) - b.astype(int)).max(axis=2)
        detail = f"DIFFERENT pixels: {100 * (diff > 0).mean():.3f}% differ, {100 * (diff > 32).mean():.3f}% by >32 levels"
    print(f"{new.name:16s} {detail}")
    if os.environ.get("GITHUB_ACTIONS") and not same:
        print(f"::warning title={new.name}::{detail}")
    if not same:
        failed.append(new.name)
print(f"checked {checked} figures; {len(failed)} differ")
sys.exit(1 if failed or checked == 0 else 0)
