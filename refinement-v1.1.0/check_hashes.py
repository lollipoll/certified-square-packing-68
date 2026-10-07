#!/usr/bin/env python3
"""Check the SHA-256 manifest and the duplicate certificate used by analytic checks."""
from pathlib import Path
import hashlib
root = Path(__file__).resolve().parent
count = 0
for line in (root/'SHA256SUMS.txt').read_text().splitlines():
    digest,name = line.split(maxsplit=1)
    path = root/name.lstrip('*')
    if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
        raise SystemExit('HASH MISMATCH: '+name)
    count += 1
if (root/'n68.json').read_bytes() != (root/'campaign/results/best_exact.json').read_bytes():
    raise SystemExit('The two certificate copies differ')
print('All '+str(count)+' file hashes match; certificate copies are identical.')
