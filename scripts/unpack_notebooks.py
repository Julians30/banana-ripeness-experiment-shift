#!/usr/bin/env python3
from pathlib import Path
import base64, gzip

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'notebooks_packed'
OUT=ROOT/'notebooks'
OUT.mkdir(exist_ok=True)

files=sorted(SRC.glob('*.ipynb.b85gz'))
if not files:
    raise SystemExit('No packed notebooks found.')

for src in files:
    name=src.name.removesuffix('.b85gz')
    data=gzip.decompress(base64.b85decode(src.read_bytes()))
    dst=OUT/name
    dst.write_bytes(data)
    print(f'Wrote {dst.relative_to(ROOT)} ({len(data)} bytes)')

print(f'Reconstructed {len(files)} source-clean notebooks.')
