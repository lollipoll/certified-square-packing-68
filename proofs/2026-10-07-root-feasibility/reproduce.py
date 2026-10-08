#!/usr/bin/env python3
"""Offline publication replay; writes only a fresh temporary receipt directory."""
import datetime
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REVIEW = ROOT / 'reviewed'
PROOF = REVIEW / '2026-10-07-root-feasibility'


def check_manifest(folder, name):
    entries = json.loads((folder / name).read_text())
    for relative, digest in entries.items():
        assert hashlib.sha256((folder / relative).read_bytes()).hexdigest() == digest, relative
    print(name, len(entries), 'hashes PASS', flush=True)


def main():
    if sys.flags.optimize:
        raise RuntimeError('Assertions must be enabled; do not use -O or -OO.')
    sys.dont_write_bytecode = True
    check_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    check_manifest(REVIEW, 'REVIEW_MANIFEST.json')
    out = Path(tempfile.mkdtemp(prefix='n68-publication-replay-'))
    subprocess.run([sys.executable, '-B', str(PROOF / 'reproduce.py'),
                    str(out / 'replay.json')], check=True)
    # The reviewed support script writes next to itself. Replay it in a temporary
    # copy so that its original supplied ledger and manifest remain unchanged.
    with tempfile.TemporaryDirectory(prefix='n68-support-replay-') as temporary:
        work = Path(temporary)
        shutil.copy2(REVIEW / 'support_audit.py', work / 'support_audit.py')
        shutil.copytree(PROOF / 'released', work / PROOF.name / 'released')
        subprocess.run([sys.executable, '-B', str(work / 'support_audit.py')], check=True)
        shutil.copy2(work / 'support-audit.json', out / 'support-audit.json')

    replay = json.loads((out / 'replay.json').read_text())
    assert replay['valid']
    family = next(item['data'] for item in replay['checks']
                  if item.get('receipt') == 'family_minimum_verification')
    released = PROOF / 'released'
    system = json.loads((released / 'campaign/results/reduced/system.json').read_text())
    witness = json.loads((released / 'campaign/results/reduced/root_witness.json').read_text())
    construction = json.loads((PROOF / 'construction.json').read_text())
    assert family['valid'] and family['root_unique']
    assert family['box_center'] == witness['center']
    radius = Q(witness['radius'])
    assert Q(family['root_box_radius']) == radius == Q(1, 10**100)
    assert Q(family['box_radius']) == Q(1, 10**11) > radius
    assert family['equality_rows'] == list(range(145))
    assert family['inequality_rows'] == list(range(145, 153))
    assert family['inequality_signs'] == [1, 1, 1, 1, 1, -1, 1, 1]
    assert construction['groups'] == system['groups'] and len(system['groups']) == 8
    assert construction['fixed_half_angle_parameters'] == system['fixed_t']
    assert len(construction['gauges']) == 22
    # The full polynomial/geometry binding and the restricted theorem were just
    # replayed on these same system and root-witness bytes.
    center = Q(witness['center'][136])
    rational = Q(json.loads((released / 'n68.json').read_text())['container_side'])
    low, high = center - radius, center + radius
    comparison = json.loads((PROOF / 'side-comparison.json').read_text())
    assert [Q(x) for x in comparison['rational_minus_root_interval']] == [rational-high, rational-low]
    assert high < rational
    # Date-limited comparison with the pinned, previously replayed certificate.
    count, side = (ROOT / 'sources/daniel-n68.cert').read_text().splitlines()[1].split()
    assert count == '68'
    daniel = Q(side)
    assert rational < daniel
    support = json.loads((out / 'support-audit.json').read_text())
    assert support['valid'] and support['pairs'] == 2278 and support['unit_frames'] == 68
    binding = dict(valid=True, checked_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   root_side_coordinate=136, root_box_radius=str(radius),
                   family_root_is_same=True, family_box_radius=family['box_radius'],
                   held_equalities=family['equality_rows'], inequalities=family['inequality_rows'],
                   inequality_signs=family['inequality_signs'], shared_angle_groups=8,
                   coordinate_gauges=22, fixed_orientations_unchanged=True,
                   root_side_interval=[str(low), str(high)],
                   rational_coordinate_witness_side=str(rational),
                   rational_minus_root_interval=[str(rational-high), str(rational-low)],
                   pinned_daniel_side=str(daniel), daniel_minus_rational=str(daniel-rational),
                   rational_upper_endpoint_is_not_rational_coordinate_witness_side=True)
    (out / 'binding.json').write_text(json.dumps(binding, indent=2)+'\n')
    check_manifest(REVIEW, 'REVIEW_MANIFEST.json')
    check_manifest(ROOT, 'PUBLICATION_MANIFEST.json')
    print('ALL PUBLICATION CHECKS PASS; fresh receipts:', out, flush=True)


if __name__ == '__main__':
    main()
