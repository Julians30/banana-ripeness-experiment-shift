"""Publication figures for the Chemometrics and Intelligent Laboratory Systems submission (Figs. 1, 2, 7-11; S8-S10, S12-S15).

Redraws every figure from the exported result tables in results/post_hoc/ (NB14, NB15) and from the values of manuscript
Table 3; no model, calibrator or embedding is refitted. Common style: no in-figure titles (titles belong in the captions),
Okabe-Ito colour-blind-safe palette, panel labels (a), (b)..., vector PDF plus 600-dpi PNG, 90/190 mm widths.

Usage:  python scripts/make_publication_figures.py --out figures_out
"""
import argparse, os
from pathlib import Path
import numpy as np, pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(); ap.add_argument('--out', default='figures_out'); OUT = ap.parse_args().out
os.makedirs(OUT, exist_ok=True)
N14 = str(ROOT / 'results/post_hoc/nb14_prospective_domain_z') + '/'
N15 = str(ROOT / 'results/post_hoc/nb15_spectral_error_audit') + '/'

plt.rcParams.update({'font.family': 'DejaVu Sans', 'text.hinting': 'no_hinting', 'font.size': 8, 'axes.titlesize': 8.5, 'axes.labelsize': 8,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'legend.fontsize': 7, 'axes.spines.top': False,
    'axes.spines.right': False, 'axes.linewidth': 0.7, 'lines.linewidth': 1.2, 'pdf.fonttype': 42,
    'savefig.bbox': 'tight', 'savefig.pad_inches': 0.03})
MM = 1 / 25.4; W1, W2 = 90 * MM, 190 * MM
OI = dict(blue='#0072B2', orange='#E69F00', green='#009E73', verm='#D55E00', sky='#56B4E9', purple='#CC79A7', yellow='#F0E442', grey='#7F7F7F', black='#000000')
TEST_C = {2: OI['blue'], 3: OI['verm'], 4: OI['green'], 5: OI['purple']}
ARM = {'RAW': ('Raw spectra', OI['grey']), 'SNV': ('SNV', OI['green']), 'PREFIX': ('Initial-window DOMAIN_Z', OI['blue']), 'FULL_TARGET': ('Complete-target DOMAIN_Z', OI['orange'])}
def lab(ax, s, x=-0.14, y=1.04): ax.text(x, y, s, transform=ax.transAxes, fontweight='bold', fontsize=9, va='bottom')
def save(fig, name):
    fig.savefig(f'{OUT}/{name}.pdf'); fig.savefig(f'{OUT}/{name}.png', dpi=600); plt.close(fig); print('saved', name)

# ------------------------------------------------------------------ Fig. 1 design schematic
def fig_design():
    """Study design in black and white; millimetre coordinates on a 190 x 128 mm canvas.
    Every label is checked to lie inside its panel and not to overlap another label."""
    W, H = 190.0, 128.0
    K, D, M, L = '#000000', '#404040', '#8c8c8c', '#dcdcdc'
    FT, FB, FS = 7.6, 6.6, 6.0          # title, body, small (pt)

    fig = plt.figure(figsize=(W / 25.4, H / 25.4))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.set_aspect('equal'); ax.axis('off')
    TEXTS = []

    def txt(x, y, s, panel, size=FS, **kw):
        kw.setdefault('va', 'center'); kw.setdefault('zorder', 7)
        t = ax.text(x, y, s, fontsize=size, color=kw.pop('color', K), **kw); TEXTS.append((t, panel)); return t

    def rect(x, y, w, h, fc, lw=0.6, z=4):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=K, lw=lw, zorder=z))

    def panel(x, y, w, h, num, title):
        rs = 1.6
        ax.add_patch(FancyBboxPatch((x, y + h - 7.0), w, 7.0, boxstyle=f'round,pad=0,rounding_size={rs}', fc=L, ec='none', zorder=1))
        ax.add_patch(Rectangle((x, y + h - 7.0), w, 3.0, fc=L, ec='none', zorder=1.1))
        ax.plot([x, x + w], [y + h - 7.0] * 2, color=K, lw=0.6, zorder=2)
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={rs}', fc='none', ec=K, lw=0.85, zorder=3))
        ax.add_patch(Circle((x + 4.3, y + h - 3.5), 2.4, fc=K, ec=K, zorder=4))
        box = (x, y, w, h)
        txt(x + 4.3, y + h - 3.55, str(num), box, size=FT, color='white', fontweight='bold', ha='center')
        txt(x + 8.3, y + h - 3.5, title, box, size=FT, fontweight='bold')
        return box

    def arrow(x0, y0, x1, y1, lw=1.0, ms=10):
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle='-|>', mutation_scale=ms, lw=lw, color=K, shrinkA=0, shrinkB=0, zorder=6))

    def bullet(x, y, box, lines, size=FB, dy=3.5):
        ax.add_patch(Rectangle((x, y - 0.6), 1.2, 1.2, fc=K, ec='none', zorder=5))
        for k, s in enumerate(lines):
            txt(x + 2.6, y - k * dy, s, box, size=size)

    TOP_Y, TOP_H = 66.0, 58.0
    BOT_Y, BOT_H = 3.0, 55.0
    X1, W1 = 2.0, 44.0
    X2, W2 = 52.0, 86.0
    X3, W3 = 144.0, 44.0

    # ---------------------------------------------------------------- 1 data
    p1 = panel(X1, TOP_Y, W1, TOP_H, 1, 'Open data and audit')
    x = X1 + 3.0
    txt(x, TOP_Y + 45.5, 'Bath multisensor data set', p1, size=FB, fontweight='bold')
    txt(x, TOP_Y + 41.8, 'Original observations per experiment', p1, color=D)
    for i, (n, c) in enumerate([('Test 2', 1720), ('Test 3', 4777), ('Test 4', 6133), ('Test 5', 5032)]):
        yy = TOP_Y + 37.0 - i * 4.3
        txt(x, yy, n, p1)
        bw = 19.0 * c / 6133
        rect(x + 10.0, yy - 1.25, bw, 2.5, M, lw=0.5)
        txt(x + 10.0 + bw + 1.0, yy, f'{c:,}', p1)
    txt(x, TOP_Y + 18.8, 'Total 17,662 after removing the', p1)
    txt(x, TOP_Y + 15.6, 'inferred class-balancing tail', p1)
    ax.plot([x, X1 + W1 - 3.0], [TOP_Y + 12.6] * 2, color=M, lw=0.5, zorder=4)
    txt(x, TOP_Y + 9.4, 'TPH (3), Spectral (18), fused (21)', p1)
    txt(x, TOP_Y + 4.6, 'Data and protocol frozen', p1, size=FB, fontweight='bold')

    # ---------------------------------------------------------------- 2 nested LOEO
    p2 = panel(X2, TOP_Y, W2, TOP_H, 2, 'Nested leave-one-experiment-out')
    cw, ch, gap = 7.4, 4.2, 1.0
    gx, gy = X2 + 15.0, TOP_Y + 38.0          # outer grid: left edge, centre of row 1
    txt(gx + 2 * cw, TOP_Y + 47.0, 'Outer loop: 4 folds', p2, color=D, ha='center')
    for j, t in enumerate(['T2', 'T3', 'T4', 'T5']):
        txt(gx + j * cw + cw / 2, gy + ch / 2 + 2.4, t, p2, ha='center')
    for i in range(4):
        yy = gy - i * (ch + gap)
        txt(gx - 1.6, yy, f'Fold {i + 1}', p2, ha='right')
        for j in range(4):
            rect(gx + j * cw + 0.4, yy - ch / 2, cw - 0.8, ch, K if i == j else 'white')
    icw = 6.6
    ix = X2 + W2 - 4.0 - 3 * icw                # inner grid right-aligned in the panel
    txt(ix + 1.5 * icw, TOP_Y + 47.0, 'Inner loop, fold 1', p2, color=D, ha='center')
    for j, t in enumerate(['T3', 'T4', 'T5']):
        txt(ix + j * icw + icw / 2, gy + ch / 2 + 2.4, t, p2, ha='center')
    for i in range(3):
        yy = gy - i * (ch + gap)
        for j in range(3):
            rect(ix + j * icw + 0.4, yy - ch / 2, icw - 0.8, ch, M if i == j else 'white')
    arrow(gx + 4 * cw + 1.5, gy, ix - 1.5, gy, lw=0.8, ms=8)
    txt((gx + 4 * cw + ix) / 2, gy + 2.3, 'development', p2, ha='center', color=D)
    ax.plot([X2 + 3.0, X2 + W2 - 3.0], [TOP_Y + 18.6] * 2, color=M, lw=0.5, zorder=4)
    for k, (fc, lab) in enumerate([(K, 'Held out until scoring'), ('white', 'Development'), (M, 'Inner validation')]):
        yy = TOP_Y + 14.6 - k * 4.0
        rect(X2 + 4.0, yy - 1.2, 3.6, 2.4, fc)
        txt(X2 + 9.4, yy, lab, p2)
    cx = X2 + 42.0
    txt(cx, TOP_Y + 14.6, 'Inside development data only', p2, fontweight='bold')
    txt(cx, TOP_Y + 10.6, 'scaling, 5 algorithms, compact grids,', p2)
    txt(cx, TOP_Y + 6.6, 'model and hyperparameter selection', p2)
    txt(cx, TOP_Y + 2.6 + 0.0, '12 frozen selection scenarios', p2)

    # ---------------------------------------------------------------- 3 external evaluation
    p3 = panel(X3, TOP_Y, W3, TOP_H, 3, 'External evaluation')
    for i, (a, b) in enumerate([('Classification', 'Macro-F1, balanced accuracy, MCC'),
                                ('Ordinal', 'QWK, MAE, errors of ≥ 2 stages'),
                                ('Probabilistic', 'NLL, Brier, RPS, ECE'),
                                ('References', 'no-skill and random selection'),
                                ('Inference', 'exact sign-flip test, n = 4')]):
        yy = TOP_Y + 45.6 - i * 8.9
        txt(X3 + 3.0, yy, a, p3, fontweight='bold')
        txt(X3 + 3.0, yy - 3.4, b, p3)
    arrow(X1 + W1, TOP_Y + 29.0, X2, TOP_Y + 29.0)
    arrow(X2 + W2, TOP_Y + 29.0, X3, TOP_Y + 29.0)

    # ---------------------------------------------------------------- 4 development-only sensitivities
    X4, W4 = 2.0, 76.0
    p4 = panel(X4, BOT_Y, W4, BOT_H, 4, 'Development-only sensitivity analyses')
    bullet(X4 + 4.0, BOT_Y + 41.0, p4, ['Class weighting and training-only SMOTE'])
    bullet(X4 + 4.0, BOT_Y + 34.0, p4, ['Temperature scaling fitted on cross-fitted', 'development predictions'])
    bullet(X4 + 4.0, BOT_Y + 23.5, p4, ['Stage-matched domain classifier and MMD²'])
    bullet(X4 + 4.0, BOT_Y + 16.5, p4, ['PCA and UMAP fitted on development data;', 'held-out records projected'])
    ax.plot([X4 + 3.0, X4 + W4 - 3.0], [BOT_Y + 7.4] * 2, color=M, lw=0.5, zorder=4)
    txt(X4 + 4.0, BOT_Y + 3.9, 'Run inside every outer fold; the held-out experiment is never used', p4, color=D)

    # ---------------------------------------------------------------- 5 post-hoc normalization
    X5, W5 = 86.0, 102.0
    p5 = panel(X5, BOT_Y, W5, BOT_H, 5, 'Post-hoc spectral normalization (design unchanged)')
    txt(X5 + 4.0, BOT_Y + 42.2, 'Experiment-wise z-score; each bar is one target experiment in acquisition order', p5, color=D)
    bx, bw, bh = X5 + 30.0, W5 - 34.0, 5.0
    yT, yP = BOT_Y + 32.5, BOT_Y + 21.0
    txt(X5 + 4.0, yT + 1.6, 'Transductive', p5, size=FB, fontweight='bold')
    txt(X5 + 4.0, yT - 1.9, 'complete target', p5)
    rect(bx, yT - bh / 2, bw, bh, '#5a5a5a')
    txt(bx + bw / 2, yT, 'statistics from all records; all records scored', p5, color='white', fontweight='bold', ha='center')
    txt(X5 + 4.0, yP + 1.6, 'Prospective', p5, size=FB, fontweight='bold')
    txt(X5 + 4.0, yP - 1.9, 'initial window', p5)
    wN = 13.0
    rect(bx, yP - bh / 2, wN, bh, K)
    rect(bx + wN, yP - bh / 2, bw - wN, bh, 'white')
    txt(bx + wN / 2, yP, 'first N', p5, color='white', fontweight='bold', ha='center')
    txt(bx + wN + (bw - wN) / 2, yP, 'statistics from the window; later records scored', p5, ha='center')
    txt(bx, yP - 5.4, 'N = 10, 25 or 50 unique spectra', p5)
    arrow(bx + 40.0, yP - 5.4, bx + bw, yP - 5.4, lw=0.7, ms=7)
    txt(bx + bw - 1.0, yP - 8.3, 'acquisition order', p5, ha='right', color=D)
    ax.plot([X5 + 3.0, X5 + W5 - 3.0], [BOT_Y + 7.4] * 2, color=M, lw=0.5, zorder=4)
    txt(X5 + 4.0, BOT_Y + 3.9, 'Controls: duplicate-aware statistics, shared-signature removal, composition stress test', p5, color=D)

    arrow(X2 + 20.0, TOP_Y, X2 + 20.0, BOT_Y + BOT_H)
    arrow(X3 + W3 / 2, TOP_Y, X3 + W3 / 2, BOT_Y + BOT_H)

    # ---------------------------------------------------------------- overlap check
    fig.canvas.draw(); r = fig.canvas.get_renderer(); inv = ax.transData.inverted()
    bbs, bad = [], 0
    for t, (x0, y0, w, h) in TEXTS:
        bb = t.get_window_extent(r).transformed(inv)
        if not (bb.x0 >= x0 + 1.0 and bb.x1 <= x0 + w - 1.0 and bb.y0 >= y0 + 0.8 and bb.y1 <= y0 + h - 0.3):
            print('Figure 1 label outside its panel:', repr(t.get_text()), [round(float(v), 1) for v in (bb.x0, bb.x1, bb.y0, bb.y1)], (x0, x0 + w)); bad += 1
        bbs.append((t.get_text(), bb))
    for i in range(len(bbs)):
        for j in range(i + 1, len(bbs)):
            a, b = bbs[i][1], bbs[j][1]
            if a.x0 < b.x1 - 0.1 and b.x0 < a.x1 - 0.1 and a.y0 < b.y1 - 0.1 and b.y0 < a.y1 - 0.1:
                print('Figure 1 overlapping labels:', repr(bbs[i][0]), '<->', repr(bbs[j][0])); bad += 1
    assert bad == 0, f'Figure 1 layout: {bad} overlapping or clipped labels'
    save(fig, 'Figure_1')

# ------------------------------------------------------------------ Fig. 2 domain diagnostics (values = manuscript Table 3)
def fig_domain():
    T3 = {'TPH': ([0.987, 0.874, 0.884, 0.774], [0.003, 0.012, 0.014, 0.019], [0.662, 0.306, 0.303, 0.105]),
          'Spectral': ([1.000, 0.979, 0.979, 1.000], [0.000, 0.004, 0.005, 0.000], [0.515, 0.151, 0.236, 0.904]),
          'TPH + Spectral': ([1.000, 1.000, 1.000, 1.000], [0.000, 0.001, 0.000, 0.000], [0.519, 0.253, 0.317, 0.884])}
    col = {'TPH': OI['orange'], 'Spectral': OI['blue'], 'TPH + Spectral': OI['green']}; mk = {'TPH': 'o', 'Spectral': 's', 'TPH + Spectral': '^'}
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.5)); x = np.arange(4)
    for i, (m, (auc, sd, mmd)) in enumerate(T3.items()):
        off = (i - 1) * 0.16
        axs[0].errorbar(x + off, auc, yerr=sd, fmt=mk[m], color=col[m], ms=4.5, capsize=2, lw=0.9, label=m)
        axs[1].bar(x + off, mmd, width=0.16, color=col[m], label=m)
    axs[0].axhline(0.5, ls='--', lw=0.8, color=OI['grey']); axs[0].text(-0.3, 0.51, 'chance', fontsize=6.5, color=OI['grey'], ha='left', va='bottom')
    axs[0].set_ylim(0.45, 1.03); axs[0].set_ylabel('Stage-matched domain ROC-AUC')
    axs[1].set_ylabel('Stage-matched MMD²')
    for a, l in zip(axs, ['(a)', '(b)']):
        a.set_xticks(x); a.set_xticklabels(['Test 2', 'Test 3', 'Test 4', 'Test 5']); a.set_xlabel('Held-out experiment'); lab(a, l)
    axs[0].legend(frameon=False, loc='lower right', bbox_to_anchor=(1, 0.08))
    save(fig, 'Figure_2')

# ------------------------------------------------------------------ loadings (Fig. 7 and supplementary)
def fig_loadings(test, name):
    c = pd.read_csv(N15 + 'pca_coefficients.csv'); v = pd.read_csv(N15 + 'pca_explained_variance.csv')
    fig, axs = plt.subplots(2, 2, figsize=(W2, 4.2), sharex=True, sharey=True)
    pcc = {1: OI['blue'], 2: OI['verm'], 3: OI['green']}; pmk = {1: 'o', 2: 's', 3: '^'}
    for a, arm, l in zip(axs.flat, ['RAW', 'SNV', 'PREFIX', 'FULL_TARGET'], ['(a)', '(b)', '(c)', '(d)']):
        for pc in (1, 2, 3):
            d = c[(c.external_test == test) & (c.arm == arm) & (c.PC == pc)].sort_values('wavelength_nm')
            ev = v[(v.external_test == test) & (v.arm == arm) & (v.PC == pc)].explained_variance_ratio.iloc[0]
            a.plot(d.wavelength_nm, d.coefficient_standardized_space, marker=pmk[pc], ms=2.8, color=pcc[pc], lw=1.0, label=f'PC{pc} ({ev*100:.1f}%)')
        a.axhline(0, lw=0.6, color=OI['grey'], ls=':'); a.legend(frameon=False, loc='upper center', ncol=3, fontsize=6.4, columnspacing=1.0, handlelength=1.6)
        a.set_title(ARM[arm][0], loc='left', fontsize=8); lab(a, l, x=-0.12, y=1.06)
        a.set_xticks([410, 535, 680, 810, 940])
    for a in axs[1]: a.set_xlabel('Wavelength (nm)')
    for a in axs[:, 0]: a.set_ylabel('PCA coefficient')
    axs[0, 0].set_ylim(-1.0, 1.22)
    save(fig, name)

# ------------------------------------------------------------------ Fig. 8 prospective synthesis
def fig_prospective():
    t8 = pd.read_csv(N14 + '08_source_order_prefix_vs_raw_and_oracle.csv')
    cr = pd.read_csv(N15 + 'conditional_resampling_sensitivity.csv'); lo = pd.read_csv(N15 + 'leave_one_experiment_out_summary.csv')
    fig, axs = plt.subplots(2, 2, figsize=(W2, 4.6)); tests = [2, 3, 4, 5]; x = np.arange(4)
    a = axs[0, 0]; d = t8[t8.N_prefix == 25].set_index('outer_test').loc[tests]
    for i, (colname, key, m) in enumerate([('raw_macro_f1_observed', 'RAW', 'o'), ('dz_prefix_macro_f1_observed', 'PREFIX', 's'), ('dz_oracle_macro_f1_observed', 'FULL_TARGET', '^')]):
        a.scatter(x + (i - 1) * 0.18, d[colname], marker=m, s=26, color=ARM[key][1], label={'RAW': 'Raw spectra', 'PREFIX': 'Initial window (N = 25)', 'FULL_TARGET': 'Complete-target diagnostic'}[key], zorder=3)
    for xi in x: a.plot([xi - 0.18, xi], [d.iloc[xi].raw_macro_f1_observed, d.iloc[xi].dz_prefix_macro_f1_observed], color='#BBBBBB', lw=0.8, zorder=1)
    a.set_ylabel('External Macro-F1'); a.set_ylim(-0.02, 0.4); a.legend(frameon=False, loc='upper center', ncol=1, fontsize=6.6)
    a = axs[0, 1]
    for i, (n, m) in enumerate([(10, 'v'), (25, 's'), (50, 'D')]):
        dd = t8[t8.N_prefix == n].set_index('outer_test').loc[tests]
        a.scatter(x + (i - 1) * 0.2, dd.delta_prefix_vs_raw_observed, marker=m, s=24, color=[OI['sky'], OI['blue'], OI['black']][i], label=f'N = {n} (mean {dd.delta_prefix_vs_raw_observed.mean():+.3f})', zorder=3)
    a.axhline(0, lw=0.8, color=OI['grey'], ls='--'); a.set_ylabel('Δ Macro-F1 vs raw'); a.legend(frameon=False, fontsize=6.6, loc='upper center')
    a = axs[1, 0]
    for i, (meth, labm, colr) in enumerate([('stage_stratified_rows', 'Stage-stratified rows', OI['grey']), ('signature_clusters', 'Spectral-signature clusters', OI['blue'])]):
        dd = cr[(cr.metric == 'delta_macro_f1') & (cr.method == meth)].set_index('outer_test').loc[tests]
        a.errorbar(x + (i - 0.5) * 0.25, dd.point, yerr=[dd.point - dd.q025, dd.q975 - dd.point], fmt='o', ms=4, capsize=2, color=colr, label=labm, lw=0.9)
    a.axhline(0, lw=0.8, color=OI['grey'], ls='--'); a.set_ylabel('Δ Macro-F1 (95% interval)'); a.set_ylim(-0.22, 0.47); a.set_yticks([-0.2, -0.1, 0, 0.1, 0.2, 0.3]); a.legend(frameon=False, fontsize=6.6, loc='upper center', ncol=2)
    a = axs[1, 1]; dd = lo.set_index('omitted_test').loc[tests]
    a.bar(x, dd.mean_delta_f1, width=0.5, color=[TEST_C[t] for t in tests])
    for xi, val in zip(x, dd.mean_delta_f1): a.text(xi, val + (0.004 if val >= 0 else -0.004), f'{val:+.3f}', ha='center', va='bottom' if val >= 0 else 'top', fontsize=6.8)
    a.axhline(0, lw=0.8, color=OI['grey']); a.set_ylabel('Mean Δ Macro-F1, other three'); a.set_ylim(-0.04, 0.14)
    for a, l in zip(axs.flat, ['(a)', '(b)', '(c)', '(d)']):
        a.set_xticks(x); a.set_xticklabels([f'Test {t}' for t in tests]); lab(a, l)
    axs[1, 0].set_xlabel('Held-out experiment'); axs[1, 1].set_xlabel('Omitted experiment'); fig.subplots_adjust(wspace=0.32, hspace=0.38)
    save(fig, 'Figure_8')

# ------------------------------------------------------------------ Fig. 9 paired ordinal errors
def fig_errors():
    d = pd.read_csv(N14 + 'paired_error_outcomes.csv.gz'); d = d[d.N_prefix == 25]; tests = [2, 3, 4, 5]
    fig, axs = plt.subplots(1, 3, figsize=(W2, 2.3), gridspec_kw=dict(width_ratios=[1.1, 1.2, 0.9]))
    a = axs[0]; k = np.arange(5)
    for i, (col, key) in enumerate([('raw_abs_error', 'RAW'), ('prefix_abs_error', 'PREFIX')]):
        bal = d.groupby('outer_test')[col].value_counts(normalize=True).unstack(fill_value=0).reindex(columns=k, fill_value=0).mean() * 100
        a.bar(k + (i - 0.5) * 0.38, bal.values, width=0.38, color=ARM[key][1], label=['Raw spectra', 'Initial window'][i])
    a.set_xticks(k); a.set_xlabel('Absolute stage error'); a.set_ylabel('Records (%, experiment-balanced)'); a.set_ylim(0, 52); a.legend(frameon=False, loc='upper right', ncol=1)
    a = axs[1]; o = d.groupby('outer_test').outcome.value_counts(normalize=True).unstack().reindex(tests)[['Improved', 'Unchanged', 'Worsened']] * 100
    left = np.zeros(4)
    for c_, colr in zip(o.columns, [OI['blue'], '#BDBDBD', OI['verm']]):
        a.barh(np.arange(4), o[c_], left=left, color=colr, label=c_, height=0.6)
        for yi, (l_, v_) in enumerate(zip(left, o[c_])):
            if v_ >= 8: a.text(l_ + v_ / 2, yi, f'{v_:.0f}', ha='center', va='center', fontsize=6.6, color='white' if c_ != 'Unchanged' else 'black')
        left += o[c_].values
    a.set_yticks(np.arange(4)); a.set_yticklabels([f'Test {t}' for t in tests]); a.set_xlabel('Records (%)'); a.set_xlim(0, 100)
    a.legend(frameon=False, ncol=3, loc='upper center', bbox_to_anchor=(0.45, -0.25), fontsize=6.5, handlelength=1)
    a = axs[2]; dm = d.groupby('outer_test').delta_abs_error.mean().reindex(tests)
    a.scatter(np.arange(4), dm, color=[TEST_C[t] for t in tests], s=30, zorder=3)
    a.axhline(0, lw=0.8, color=OI['grey'], ls='--'); a.set_xticks(np.arange(4)); a.set_xticklabels([str(t) for t in tests])
    a.set_xlabel('Held-out experiment'); a.set_ylabel('Δ ordinal MAE (stages)')
    for a_, l in zip(axs, ['(a)', '(b)', '(c)']): lab(a_, l, x=-0.2)
    fig.subplots_adjust(wspace=0.5)
    save(fig, 'Figure_9')

# ------------------------------------------------------------------ projections
def fig_proj(test, coord, name, color_by='test'):
    p = pd.read_csv(N15 + 'projection_coordinates.csv.gz'); v = pd.read_csv(N15 + 'pca_explained_variance.csv')
    fig, axs = plt.subplots(1, 4, figsize=(W2, 2.1))
    for a, arm, l in zip(axs, ['RAW', 'SNV', 'PREFIX', 'FULL_TARGET'], ['(a)', '(b)', '(c)', '(d)']):
        d = p[(p.external_test == test) & (p.arm == arm)]
        X, Y = (('PC1', 'PC2') if coord == 'PCA' else ('UMAP1', 'UMAP2'))
        dev, ext = d[d.role == 'development'], d[d.role == 'external']
        a.scatter(dev[X], dev[Y], s=2.5, c=[TEST_C[t] for t in dev.test_id], alpha=0.35, linewidths=0, rasterized=True)
        a.scatter(ext[X], ext[Y], s=7, marker='^', c=[TEST_C[t] for t in ext.test_id], edgecolors='black', linewidths=0.25, rasterized=True)
        if coord == 'PCA':
            e1 = v[(v.external_test == test) & (v.arm == arm) & (v.PC == 1)].explained_variance_ratio.iloc[0] * 100
            e2 = v[(v.external_test == test) & (v.arm == arm) & (v.PC == 2)].explained_variance_ratio.iloc[0] * 100
            a.set_xlabel(f'PC1 ({e1:.1f}%)'); a.set_ylabel(f'PC2 ({e2:.1f}%)', labelpad=1)
        else:
            a.set_xlabel('UMAP 1'); a.set_ylabel('UMAP 2', labelpad=1)
        a.set_title(ARM[arm][0].replace(' DOMAIN_Z', '\nDOMAIN_Z'), loc='left', fontsize=7.2); lab(a, l, x=-0.25, y=1.16)
        a.tick_params(labelsize=6.5)
    h = [Line2D([], [], marker='o', ls='', color=TEST_C[t], ms=4, label=f'Test {t}') for t in [2, 3, 4, 5]]
    h += [Line2D([], [], marker='o', ls='', color='#777777', alpha=0.5, ms=4, label='Development'), Line2D([], [], marker='^', ls='', mfc='#777777', mec='black', ms=5, label=f'Held-out Test {test}')]
    fig.legend(handles=h, loc='lower center', ncol=6, frameon=False, bbox_to_anchor=(0.5, -0.2), fontsize=6.8)
    fig.subplots_adjust(wspace=0.45)
    save(fig, name)

# ------------------------------------------------------------------ Fig. 11 composition stress
def fig_composition():
    r = pd.read_csv(N14 + '10_stage_composition_stress_replicates.csv.gz'); tests = [2, 3, 4, 5]
    sc = [('early80_late20', '80% early / 20% late', OI['blue'], 'o'), ('balanced50_50', '50% / 50%', OI['grey'], 's'), ('early20_late80', '20% early / 80% late', OI['verm'], 'D')]
    fig, a = plt.subplots(figsize=(W1 * 1.45, 2.5)); x = np.arange(4)
    for i, (s, l_, colr, m) in enumerate(sc):
        g = r[r.scenario == s].groupby('outer_test').macro_f1_observed
        mean, lo, hi = g.mean().reindex(tests), g.quantile(0.025).reindex(tests), g.quantile(0.975).reindex(tests)
        a.errorbar(x + (i - 1) * 0.2, mean, yerr=[mean - lo, hi - mean], fmt=m, color=colr, ms=4.5, capsize=2, lw=0.9, label=l_)
    a.set_xticks(x); a.set_xticklabels([f'Test {t}' for t in tests]); a.set_xlabel('Held-out experiment')
    a.set_ylabel('External Macro-F1 (mean, 2.5–97.5%)'); a.set_ylim(0, 0.6)
    a.legend(frameon=False, title='Calibration-window stages (early 1–3 / late 4–5)', title_fontsize=6.8, loc='upper right')
    save(fig, 'Figure_11')

# ------------------------------------------------------------------ error maps (supplementary)
def fig_errmap(test, name):
    p = pd.read_csv(N15 + 'projection_coordinates.csv.gz'); e = pd.read_csv(N15 + 'paired_predictions_with_signature.csv.gz')
    d = p[(p.external_test == test) & (p.arm == 'PREFIX') & (p.role == 'external')].merge(e[e.outer_test == test][['master_id', 'stage_true', 'prefix_ae']], on='master_id', how='inner')
    d = d.drop_duplicates(['master_id', 'stage_true']) if 'stage_true' in d else d
    cls = np.where(d.prefix_ae == 0, 'Correct', np.where(d.prefix_ae == 1, 'One-stage error', 'Error ≥ 2 stages'))
    cmap = {'Correct': OI['green'], 'One-stage error': OI['orange'], 'Error ≥ 2 stages': OI['verm']}
    fig, axs = plt.subplots(1, 2, figsize=(W2, 2.6))
    for a, (X, Y, xl, yl), l in zip(axs, [('PC1', 'PC2', 'PC1', 'PC2'), ('UMAP1', 'UMAP2', 'UMAP 1', 'UMAP 2')], ['(a)', '(b)']):
        for k_, c_ in cmap.items():
            m = cls == k_; a.scatter(d[X][m], d[Y][m], s=9, color=c_, alpha=0.8, linewidths=0, label=f'{k_} (n = {m.sum()})')
        a.set_xlabel(xl); a.set_ylabel(yl); lab(a, l, x=-0.12)
    axs[0].legend(frameon=False, fontsize=6.6)
    save(fig, name)

fig_design(); fig_domain(); fig_loadings(3, 'Figure_7')
for t, n in [(2, 'Figure_S8'), (4, 'Figure_S9'), (5, 'Figure_S10')]: fig_loadings(t, n)
fig_prospective(); fig_errors(); fig_proj(5, 'PCA', 'Figure_10'); fig_composition()
fig_proj(5, 'UMAP', 'Figure_S12'); fig_proj(3, 'PCA', 'Figure_S13')
fig_errmap(3, 'Figure_S14'); fig_errmap(5, 'Figure_S15')
