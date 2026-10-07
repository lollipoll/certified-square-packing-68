#!/usr/bin/env python3
"""Exact unit-square packing check using centers and projection half-widths.

This implementation does not import the supplied verifier or construct vertices.
For an axis a, a square's projection half-width is
    (abs(u dot a) + abs(v dot a)) / 2,
where u,v are its orthogonal unit edge directions. Two square interiors are
disjoint iff their projection intervals have disjoint interiors on at least
one edge-normal direction of either square (the separating-axis theorem).
For squares those directions are also their edge directions, up to sign.
All arithmetic and comparisons below use fractions.Fraction, with no tolerance.
"""
import argparse
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]


def inspect(data, expected_n):
    if data.get('schema') != 'independent-square-certificate/v1':
        raise ValueError('Expected independent-square-certificate/v1')
    if type(expected_n) is not int or expected_n < 1:
        raise ValueError('Expected a positive external square count')
    if type(data.get('n')) is not int or data['n'] != expected_n:
        raise ValueError('Declared square count disagrees with external count')
    if len(data['squares']) != expected_n:
        raise ValueError('Actual square count disagrees with external count')
    side = Fraction(data['container_side'])
    if side <= 0:
        raise ValueError('Container side must be positive')
    squares = []
    minimum_wall = None
    wall_witness = None
    wall_failures = []
    for i, raw in enumerate(data['squares']):
        x, y, t = (Fraction(raw[k]) for k in ('x', 'y', 't'))
        denominator = 1 + t * t
        c, s = (1 - t * t) / denominator, 2 * t / denominator
        u, v = (c, s), (-s, c)
        if dot(u, u) != 1 or dot(v, v) != 1 or dot(u, v) != 0:
            raise ValueError('Edge directions are not an orthonormal basis')
        extent = (abs(c) + abs(s)) / 2
        gaps = (side / 2 + x - extent, side / 2 - x - extent,
                side / 2 + y - extent, side / 2 - y - extent)
        for name, gap in zip(('left', 'right', 'bottom', 'top'), gaps):
            if minimum_wall is None or gap < minimum_wall:
                minimum_wall, wall_witness = gap, [i, name]
            if gap < 0:
                wall_failures.append([i, name, str(gap)])
        squares.append(((x, y), u, v))
    minimum_pair = None
    pair_witness = None
    overlaps = []
    pair_count = 0
    for i, j in itertools.combinations(range(expected_n), 2):
        center_i, u_i, v_i = squares[i]
        center_j, u_j, v_j = squares[j]
        delta = tuple(a - b for a, b in zip(center_i, center_j))
        gaps = []
        for axis in (u_i, v_i, u_j, v_j):
            radius_i = (abs(dot(u_i, axis)) + abs(dot(v_i, axis))) / 2
            radius_j = (abs(dot(u_j, axis)) + abs(dot(v_j, axis))) / 2
            gaps.append(abs(dot(delta, axis)) - radius_i - radius_j)
        margin = max(gaps)
        pair_count += 1
        if minimum_pair is None or margin < minimum_pair:
            minimum_pair, pair_witness = margin, [i, j]
        if margin < 0:
            overlaps.append([i, j, str(margin)])
    return {
        'valid': not wall_failures and not overlaps,
        'method': 'exact rational center/projection-half-width check',
        'acceptance_tolerance': '0',
        'n': expected_n,
        'container_side': str(side),
        'pairs_checked': pair_count,
        'minimum_wall_gap': str(minimum_wall),
        'wall_witness': wall_witness,
        'minimum_pair_gap': str(minimum_pair) if minimum_pair is not None else None,
        'pair_witness': pair_witness,
        'wall_failures': wall_failures,
        'overlaps': overlaps,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('certificate', type=Path)
    parser.add_argument('--n', type=int, required=True)
    args = parser.parse_args()
    payload = args.certificate.read_bytes()
    data = json.loads(payload, parse_float=str)
    result = inspect(data, args.n)
    result['certificate_sha256'] = hashlib.sha256(payload).hexdigest()
    print(json.dumps(result, indent=2))
    return 0 if result['valid'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
