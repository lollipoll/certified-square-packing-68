#!/usr/bin/env python3
"""Independent square verifier. Standard library only; no search-code imports.

Each square is reconstructed as four cyclic vertices. We check all edge lengths,
right angles, opposite edges, all wall inequalities, and all unordered pairs by
projection onto four candidate edge-normal directions (two per square).
Fraction mode is a zero-tolerance proof. Decimal mode is numerical screening.
"""
import argparse
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def rational(value):
    if isinstance(value, dict):
        if int(value['denominator']) <= 0:
            raise ValueError('Nonpositive denominator')
        return F(int(value['numerator']), int(value['denominator']))
    return F(value)


def dec(value):
    if isinstance(value, F):
        return D(value.numerator) / D(value.denominator)
    return D(value)


def atan(x):
    """Decimal arctangent, with half-angle reduction and a convergent series."""
    factor = 1
    while abs(x) > D('0.05'):
        x = x / (1 + (1 + x*x).sqrt())
        factor *= 2
    term = total = x
    k = 1
    while True:
        term *= -x*x
        new = total + term / (2*k+1)
        if new == total:
            return total * factor
        total = new
        k += 1


def pi():
    return 16*atan(D(1)/5) - 4*atan(D(1)/239)


def sincos(x):
    """Decimal Taylor series; used only for nonrigorous angle-based screening."""
    p = pi()
    x %= 2*p
    if x > p:
        x -= 2*p
    if x < -p:
        x += 2*p
    st = s = x
    ct = c = D(1)
    k = 1
    while True:
        st *= -x*x / ((2*k)*(2*k+1))
        ct *= -x*x / ((2*k)*(2*k-1))
        ns, nc = s+st, c+ct
        if ns == s and nc == c:
            return s, c
        s, c = ns, nc
        k += 1


def canonical(data, expected_n):
    """Read authoritative fields only; reject inconsistent inventory/container."""
    if type(expected_n) is not int or expected_n <= 0:
        raise ValueError('An external positive expected count is required')
    schema = data.get('schema')
    if schema == 'square-packing-candidate-export/v1':
        box = data['container']
        side = F(box['side_length'])
        if (box['shape'] != 'square' or F(data['unit_square_side_length']) != 1
                or F(box['rotation_radians']) != 0
                or any(F(v) != 0 for v in box['center'].values())):
            raise ValueError('Unexpected unit size or container frame')
        expected_bounds = dict(x_min=-side/2, y_min=-side/2,
                               x_max=side/2, y_max=side/2)
        if {k:F(v) for k,v in box['bounds'].items()} != expected_bounds:
            raise ValueError('Inconsistent container bounds')
        if F(box['original_side_literal']) != side:
            raise ValueError('Inconsistent side literal')
        count = data['square_count']
        squares = []
        for i, q in enumerate(data['squares']):
            if q['index'] != i or q['rotation']['representation'] != 'rational_half_angle_tangent':
                raise ValueError('Bad square index or rotation encoding')
            values = [q['center']['x'], q['center']['y'], q['rotation']['t']]
            for value in values:
                if rational(value) != F(value['original_literal']):
                    raise ValueError('Inconsistent exact literals')
            squares.append(tuple(map(rational, values)))
    elif schema in ('independent-square-certificate/v1', 'packing-n/exact-v1'):
        side = F(data['container_side'])
        count = data['n']
        squares = [tuple(F(q[k]) for k in ('x','y','t')) for q in data['squares']]
    else:
        raise ValueError('Unknown exact schema')
    if type(count) is not int or count != expected_n or len(squares) != expected_n:
        raise ValueError(f'Count mismatch: expected {expected_n}, declared {count}, actual {len(squares)}')
    if side <= 0:
        raise ValueError('Container side must be positive')
    return side, squares


def vertices(x, y, c, s):
    return [(x+(a*c-b*s)/2, y+(a*s+b*c)/2)
            for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]


def rational_polygons(squares, convert=lambda x:x):
    result = []
    for x,y,t in squares:
        x,y,t = map(convert, (x,y,t))
        c, s = (1-t*t)/(1+t*t), 2*t/(1+t*t)
        result.append(vertices(x,y,c,s))
    return result


def sub(a,b):
    return a[0]-b[0], a[1]-b[1]


def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]


def projection(poly, axis):
    vals = [dot(v, axis) for v in poly]
    return min(vals), max(vals)


def check_polygons(polygons, side, expected_n, tolerance=0, witnesses=False):
    """All-pairs polygon SAT. No neighbor culling; touching is accepted.

    Gap on axis a = max(min(B.a)-max(A.a), min(A.a)-max(B.a)).
    Pair margin = max of those gaps over all four axes. Negative means overlap.
    Exact axes have unit norm after the independent geometry checks.
    """
    if not polygons or side <= 0 or tolerance < 0:
        raise ValueError('Empty packing, invalid side, or negative tolerance')
    numeric = isinstance(side, D)
    axes = []
    wall_min, wall_witness = None, None
    unit_error = angle_error = opposite_error = 0
    side_length_error = 0
    outside = []
    for i,poly in enumerate(polygons):
        if len(poly) != 4:
            raise ValueError('Every square must have four cyclic vertices')
        edges = [sub(poly[(k+1)%4],poly[k]) for k in range(4)]
        for k,e in enumerate(edges):
            length2 = dot(e,e)
            unit_error = max(unit_error, abs(length2-1))
            if numeric:
                side_length_error = max(side_length_error, abs(length2.sqrt()-1))
            angle_error = max(angle_error, abs(dot(e,edges[(k+1)%4])))
            opposite_error = max(opposite_error, *(abs(e[d]+edges[(k+2)%4][d]) for d in (0,1)))
        normals = [(-e[1],e[0]) for e in edges[:2]]
        if numeric:
            normals = [(a/dot((a,b),(a,b)).sqrt(), b/dot((a,b),(a,b)).sqrt()) for a,b in normals]
        axes.append(normals)
        for k,(x,y) in enumerate(poly):
            for name,gap in [('left',x+side/2),('right',side/2-x),
                             ('bottom',y+side/2),('top',side/2-y)]:
                if wall_min is None or gap < wall_min:
                    wall_min,wall_witness = gap,[i,k,name]
                if gap < -tolerance:
                    outside.append({'square':i,'vertex':k,'wall':name,'gap':str(gap)})
    pair_min, pair_witness = None,None
    overlaps, all_witnesses = [],[]
    pairs = 0
    for i in range(len(polygons)):
        for j in range(i+1,len(polygons)):
            best, which, order = None,None,None
            for k,axis in enumerate(axes[i]+axes[j]):
                a0,a1 = projection(polygons[i],axis)
                b0,b1 = projection(polygons[j],axis)
                forward,reverse = b0-a1,a0-b1
                gap = max(forward,reverse)
                if best is None or gap > best:
                    best,which,order = gap,k,('i_before_j' if forward >= reverse else 'j_before_i')
            pairs += 1
            witness = {'i':i,'j':j,'axis_owner':i if which<2 else j,
                       'edge':which%2,'order':order}
            if pair_min is None or best < pair_min:
                pair_min,pair_witness = best,witness
            if best < -tolerance:
                overlaps.append(dict(witness, gap=str(best)))
            if witnesses:
                all_witnesses.append(witness)
    shape_ok = max(unit_error,angle_error,opposite_error) <= tolerance
    result = {'valid':len(polygons)==expected_n and shape_ok and not outside and not overlaps,
              'count_expected':expected_n,'count_actual':len(polygons),
              'pairs_checked':pairs,'wall_inequalities_checked':16*len(polygons),
              'acceptance_tolerance':str(tolerance),'unit_squared_error':str(unit_error),
              'right_angle_dot_error':str(angle_error),'opposite_edge_error':str(opposite_error),
              'minimum_wall_gap':str(wall_min),'wall_witness':wall_witness,
              'minimum_pair_gap':str(pair_min) if pair_min is not None else None,
              'pair_witness':pair_witness,
              'max_boundary_violation':str(max(0,-wall_min)),
              'max_pair_penetration':str(max(0,-pair_min)) if pair_min is not None else '0',
              'violating_wall_inequalities':outside,'overlapping_pairs':overlaps}
    if numeric:
        result['max_side_length_error'] = str(side_length_error)
    if witnesses:
        result['separators'] = all_witnesses
    return result


def exact_check(data,n,witnesses=False):
    side,squares = canonical(data,n)
    result = check_polygons(rational_polygons(squares),side,n,witnesses=witnesses)
    result.update(mode='exact Fraction, zero tolerance',container_side=str(side))
    return result


def numerical_check(data,n,precision=80,tolerance='1e-60'):
    with localcontext() as ctx:
        ctx.prec = precision
        if 'arrays' in data:
            arrays = data['arrays']
            if arrays['q']['shape'] != [n,3] or arrays['side']['shape'] != []:
                raise ValueError('Bad checkpoint shape')
            vals = list(map(D,arrays['q']['values_decimal']))
            if len(vals) != 3*n or len(arrays['side']['values_decimal']) != 1:
                raise ValueError('Bad checkpoint inventory')
            side = D(arrays['side']['values_decimal'][0])
            polys = []
            for i in range(n):
                x,y,angle = vals[3*i:3*i+3]
                s,c = sincos(angle)
                polys.append(vertices(x,y,c,s))
        else:
            side,squares = canonical(data,n)
            side,polys = dec(side),rational_polygons(squares,dec)
        result = check_polygons(polys,side,n,D(tolerance))
        result.update(mode='Decimal numerical screening, not interval arithmetic',
                      precision=precision,container_side=str(side))
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('file',type=Path)
    parser.add_argument('--n',required=True,type=int)
    parser.add_argument('--numeric',action='store_true')
    parser.add_argument('--precision',type=int,default=80)
    parser.add_argument('--tolerance',default='1e-60')
    parser.add_argument('--witnesses',action='store_true')
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    raw = args.file.read_bytes()
    data = json.loads(raw,parse_float=str)
    result = (numerical_check(data,args.n,args.precision,args.tolerance) if args.numeric
              else exact_check(data,args.n,args.witnesses))
    result['input_sha256'] = sha256(raw)
    out = json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(out)
    else:
        print(out,end='')
    raise SystemExit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()
