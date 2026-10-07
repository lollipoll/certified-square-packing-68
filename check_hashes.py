#!/usr/bin/env python3
"""Check the publication kit's certificate/code/results manifest."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent
count = 0
for line in (root / 'SHA256SUMS.txt').read_text().splitlines():
    expected, name = line.split('  ', 1)
    path = root / name
    if not path.resolve().is_relative_to(root):
        raise SystemExit(f'Unsafe manifest path: {name}')
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise SystemExit(f'FAIL: {name}')
    count += 1
print(f'PASS: {count} certificate/code/result hashes match')
