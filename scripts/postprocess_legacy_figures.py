"""Post-processing of figures carried over from the previous submission (Figs. 3, 6, S1-S3, S11) and of the NB16
reliability diagrams (Figs. 4, 5, S4-S7) for the Chemometrics and Intelligent Laboratory Systems submission.

Inputs (tracked): results/chemolab_submission/figure_sources/previous_submission/ (figures exactly as produced by
NB04/NB07, NB05/NB08, NB06-v1.1/NB08, the TreeSHAP analysis and NB10-NB12 for the previous submission) and
results/chemolab_submission/figure_sources/nb16_reliability/ (NB16 outputs).

Usage:  python scripts/postprocess_legacy_figures.py --out figures_out
        python scripts/verify_figures.py figures_out          # byte/pixel comparison with the submitted figures

Legacy figures: remove the in-figure title (journal rule) and replace
notebook-style labels (snake_case, notebook IDs, 'A.' panel labels) with publication labels. Pixel data of the plots
are untouched; text is re-typeset in DejaVu Sans (matplotlib's default font, used to draw the originals).
NB16 reliability PDFs are cropped through the PDF CropBox, so they remain vector."""
import argparse, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'results' / 'chemolab_submission' / 'figure_sources'
ap = argparse.ArgumentParser(); ap.add_argument('--out', default='figures_out'); OUT = ap.parse_args().out
os.makedirs(OUT, exist_ok=True)
P3 = str(SRC / 'previous_submission') + '/'
P16 = str(SRC / 'nb16_reliability') + '/'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
if not os.path.exists(FONT):
    import matplotlib; FONT = os.path.join(os.path.dirname(matplotlib.__file__), 'mpl-data/fonts/ttf/DejaVuSans.ttf')

def ink_bbox(a, box, thr=200):
    x0, y0, x1, y1 = box; sub = a[y0:y1, x0:x1] < thr
    ys, xs = np.where(sub)
    return x0 + xs.min(), y0 + ys.min(), x0 + xs.max() + 1, y0 + ys.max() + 1

def fit_size(old, width):
    lo, hi = 5, 200
    while hi - lo > 0.25:
        m = (lo + hi) / 2; f = ImageFont.truetype(FONT, int(round(m)))
        b = f.getbbox(old, anchor='ls'); (lo, hi) = (m, hi) if b[2] - b[0] < width else (lo, m)
    return int(round(lo))

def patch(im, box, old, new, align='center'):
    a = np.asarray(im.convert('L'))
    x0, y0, x1, y1 = ink_bbox(a, box)
    size = fit_size(old, x1 - x0); f = ImageFont.truetype(FONT, size)
    ob = f.getbbox(old, anchor='ls')           # glyph box relative to baseline
    baseline = y0 - ob[1]                      # top of old ink = baseline + ob[1]
    d = ImageDraw.Draw(im); d.rectangle((x0 - 4, y0 - 4, x1 + 4, y1 + 4), fill='white')
    if align == 'center':
        d.text(((x0 + x1) / 2, baseline), new, font=f, fill='black', anchor='ms')
    else:
        d.text((x0 - ob[0], baseline), new, font=f, fill='black', anchor='ls')

def crop_top(im, y): return im.crop((0, y, im.width, im.height))

def legacy(src, dst, crop_y, patches):
    im = Image.open(P3 + src).convert('RGB')
    for p in patches: patch(im, *p)
    im = crop_top(im, crop_y); im.save(f'{OUT}/{dst}.png', dpi=(300, 300)); print(dst, im.size)

H3 = (300, 160, 1750, 218); H3b = (1800, 160, 3419, 218)
legacy('Figure_3.png', 'Figure_3', 150, [
    (H3, 'A. Transport of the internal #1 vs #2 decision', '(a) Transport of the internal #1 vs #2 decision'),
    (H3b, 'B. Selection loss under experiment shift', '(b) Selection loss under experiment shift')])
legacy('Figure_6.png', 'Figure_6', 190, [
    ((0, 200, 1785, 262), 'Spectral', '(a) Spectral'),
    ((1785, 200, 3570, 262), 'TPH_Spectral', '(b) TPH + Spectral')])
legacy('Figure_S1.png', 'Figure_S1', 210, [
    ((0, 222, 1514, 275), 'RandomForest', '(a) Random forest'),
    ((1514, 222, 3029, 275), 'XGBoost', '(b) XGBoost')])
legacy('Figure_S2.png', 'Figure_S2', 162, [
    ((3255, 245, 4140, 330), 'class_weight_balanced', 'Class weighting', 'left'),
    ((3255, 357, 4140, 440), 'smote_training_only', 'Training-only SMOTE', 'left')])
legacy('Figure_S3.png', 'Figure_S3', 162, [])
legacy('Figure_S4.png', 'Figure_S11', 190, [
    ((0, 200, 1785, 250), 'RAW', '(a) RAW'), ((1785, 200, 3570, 250), 'SNV', '(b) SNV'),
    ((0, 1352, 1785, 1412), 'DOMAIN_Z_ROW', '(c) DOMAIN_Z, row-level statistics'),
    ((1785, 1352, 3570, 1412), 'DOMAIN_Z_UNIQUE', '(d) DOMAIN_Z, unique-signature statistics'),
    ((1030, 2700, 1800, 2752), 'NB11: shared signatures retained', 'Shared signatures retained', 'left'),
    ((1925, 2700, 2700, 2752), 'NB12: shared signatures removed', 'Shared signatures removed', 'left')])

# NB16 reliability diagrams: drop suptitle (rows 72-190 of 5863); keep vector PDF via CropBox
REL = [('Spectral_Raw', 'Figure_4'), ('Spectral_Calibrated', 'Figure_5'), ('TPH_Raw', 'Figure_S4'), ('TPH_Calibrated', 'Figure_S5'),
       ('TPH_Spectral_Raw', 'Figure_S6'), ('TPH_Spectral_Calibrated', 'Figure_S7')]
CUT = 330
for src, dst in REL:
    im = Image.open(P16 + f'F16_Reliability_{src}.png').convert('RGB'); H = im.height
    crop_top(im, CUT).save(f'{OUT}/{dst}.png', dpi=(600, 600))
    r = PdfReader(P16 + f'F16_Reliability_{src}.pdf'); w = PdfWriter()
    for pg in r.pages:
        x0, y0, x1, y1 = [float(v) for v in pg.mediabox]
        new_top = y1 - (y1 - y0) * CUT / H
        pg.cropbox.lower_left = (x0, y0); pg.cropbox.upper_right = (x1, new_top)
        pg.mediabox.lower_left = (x0, y0); pg.mediabox.upper_right = (x1, new_top)
        w.add_page(pg)
    with open(f'{OUT}/{dst}.pdf', 'wb') as fh: w.write(fh)
    print(dst, 'cropped')
