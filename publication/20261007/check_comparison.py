"""Replay pinned Daniel n68 after an exact coordinate translation; no search."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile

if not __debug__:
    raise RuntimeError('Assertions must be enabled')
here = Path(__file__).resolve().parent
release = here.parents[1] / 'refinement-v1.1.0'
raw = (here / 'sources/daniel-n68.cert').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '871fb854b07417fa2178c14e933f5c1ccf8f35d8280b93394b2109aebc8b2c68'
lines = [line for line in raw.decode().splitlines() if line and not line.startswith('#')]
n, side = lines[0].split()
n, side = int(n), F(side)
assert n == 68 and len(lines) == n+1
data = dict(schema='packing-n/exact-v1', n=n, container_side=str(side), squares=[])
for line in lines[1:]:
    x, y, t = map(F, line.split())
    # Source box [0,S]^2 -> centered box [-S/2,S/2]^2. No rounding.
    data['squares'].append(dict(x=str(x-side/2), y=str(y-side/2), t=str(t)))
ours_raw = (release / 'n68.json').read_bytes()
assert hashlib.sha256(ours_raw).hexdigest() == '6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9'
ours = F(json.loads(ours_raw)['container_side'])
with tempfile.TemporaryDirectory(prefix='n68-publication-comparison-') as temporary:
    converted = Path(temporary) / 'daniel-centered.json'
    converted.write_text(json.dumps(data, indent=2)+'\n')
    for checker, key in [('verify.py', 'valid_exact'), ('independent_support_check.py', 'valid')]:
        cmd = [sys.executable, '-B', str(release/checker), str(converted), '--n', str(n)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        assert report[key] and report['pairs_checked'] == 2278
        print(checker, 'PASS', json.dumps(report), flush=True)
delta = side-ours
assert delta == F('8798795237260591647898096977212073675963/100000000000000000000000000000000000000000000000000000000000') > 0
print(json.dumps(dict(our_side=str(ours), daniel_side=str(side), improvement_exact=str(delta)), indent=2))
