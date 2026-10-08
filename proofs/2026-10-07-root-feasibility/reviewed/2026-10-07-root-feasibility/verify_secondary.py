#!/usr/bin/env python3
"""Separate arithmetic path: integer coefficient checks and dyadic vertex boxes.

Shares certificate, system, root witness and RELEASED root/binding checker.
Does not import geometry.py, census.py or verify_certificate.py.
This is a second implementation by the same Codex-assisted project, not a
second human review or a proof-assistant formalization.
"""
import hashlib,json,sys,time
from pathlib import Path
from fractions import Fraction
from math import gcd
from itertools import product,combinations

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'released'))
from check_polynomial_binding import Polynomial as P,verify as bind
sys.path.insert(0,str(ROOT/'released/campaign/src'))
from verify_root import verify as check_root

Q=Fraction
D=2**420
class Box:
    """Endpoints are integers in units of 2^-420; every operation rounds out."""
    def __init__(self,a,b=None):self.a=a;self.b=a if b is None else b
    @classmethod
    def rational(cls,q):
        q=Q(q)*D;return cls(q.numerator//q.denominator,-((-q.numerator)//q.denominator))
    def __add__(self,y):return Box(self.a+y.a,self.b+y.b)
    def __neg__(self):return Box(-self.b,-self.a)
    def __sub__(self,y):return self+-y
    def __mul__(self,y):
        v=[a*b for a in (self.a,self.b) for b in (y.a,y.b)]
        return Box(min(v)//D,-((-max(v))//D))

def stripped(p):return {m:c for m,c in p.terms.items() if c}
def serialized(p):return {tuple(m):Q(c) for m,c in p if Q(c)}
def identity(p,weights,equations):
    """Clear denominators, then check each integer coefficient exactly."""
    terms={m:[-c] for m,c in stripped(p).items()};seen=set()
    for j,a in weights:
        assert type(j) is int and 0<=j<153 and j not in seen
        seen.add(j);a=Q(a);assert a
        for m,c in equations[j].items():terms.setdefault(m,[]).append(a*c)
    for values in terms.values():
        denominator=1
        for c in values:denominator=denominator*c.denominator//gcd(denominator,c.denominator)
        assert sum(c.numerator*(denominator//c.denominator) for c in values)==0,'integer coefficient check failed'

def verify(cert=None,replay_root=True):
    assert not sys.flags.optimize
    start=time.monotonic()
    if cert is None:cert=json.loads((ROOT/'certificate.json').read_text())
    assert cert['schema']=='n68-all-inequality-v1'
    hashes={
      'released/n68.json':'6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9',
      'released/campaign/results/reduced/system.json':'0bc2c2deea9f63d4ed1a3473ed50f71327ce33676bfd7ee1f43c371d13e481de',
      'released/campaign/results/reduced/root_witness.json':'fa234967c8496538ee67614a7d8b68c58022f34bcc698b48eda00eb7282fe824',
      'released/campaign/results/reduced/elimination_witness.json':'512b6a0c06b28478482b4b03c519b70f1f716dfe249bcbd5beff10df7112e807'}
    assert cert['input_sha256']==hashes
    for name,h in hashes.items():assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h
    path=ROOT/'released/campaign/results/reduced'
    s=json.loads((path/'system.json').read_text());w=json.loads((path/'root_witness.json').read_text())
    assert bind(s)==437
    if replay_root:check_root(s,w)
    rows=[serialized(row) for row in s['polynomials']]
    values=list(map(Q,w['center']));radius=Q(w['radius'])
    z=[Box(Box.rational(a-radius).a,Box.rational(a+radius).b) for a in values]
    variables=[P.variable(i) for i in range(153)];symbols=[];directions=[];denominators={}
    groups={i:g for g,ids in enumerate(s['groups']) for i in ids}
    for i in range(68):
        if i in groups:
            k=137+2*groups[i];symbols.append((variables[k],variables[k+1]));directions.append((z[k],z[k+1]))
        else:
            t=Q(s['fixed_t'][str(i)]);d=1+t*t;assert d>0;denominators[i]=d
            c=(1-t*t)/d;sn=2*t/d;assert c*c+sn*sn==1
            symbols.append((P(c),P(sn)));directions.append((Box.rational(c),Box.rational(sn)))
    signs=list(product((-1,1),repeat=2));assert cert['vertex_signs']==[list(v) for v in signs]
    points=[];spoints=[];half=Box.rational(Q(1,2))
    for i in range(68):
        c,sn=directions[i];pc,ps=symbols[i];pv=[];sv=[]
        for a,b in signs:
            aa=Box.rational(a);bb=Box.rational(b)
            pv.append((z[i]+half*(aa*c-bb*sn),z[68+i]+half*(aa*sn+bb*c)))
            sv.append((variables[i]+Q(1,2)*(a*pc-b*ps),variables[68+i]+Q(1,2)*(a*ps+b*pc)))
        points.append(pv);spoints.append(sv)
    # Frames must be the declared frames, and genuinely orthonormal at F=0.
    assert len(cert['frames'])==68
    for i,frame in enumerate(cert['frames']):
        assert frame['square']==i;c,sn=symbols[i]
        assert [serialized(p) for p in frame['u']]==[stripped(c),stripped(sn)]
        assert [serialized(p) for p in frame['v']]==[stripped(-sn),stripped(c)]
        assert len(frame['identities'])==3
        for p,pr in zip((c*c+sn*sn-1,sn*sn+c*c-1,c*(-sn)+sn*c),frame['identities']):identity(p,pr,rows)
        if i in denominators:assert Q(frame['fixed_denominator'])==denominators[i]>0
        else:assert frame['fixed_denominator'] is None
    scale=cert['positive_scale'];assert type(scale) is int and scale>0
    contacts=strict=0;minimum=None
    def check(p,box,proof):
        nonlocal contacts,strict,minimum
        if set(proof)=={'identity'}:identity(p,proof['identity'],rows);contacts+=1
        else:
            assert set(proof)=={'positive'} and type(proof['positive']) is int and proof['positive']>0
            assert box.a*scale>=proof['positive']*D,'direct vertex interval check failed'
            margin=Q(proof['positive'],scale);minimum=margin if minimum is None else min(minimum,margin);strict+=1
    assert len(cert['pairs'])==2278
    for (i,j),entry in zip(combinations(range(68),2),cert['pairs']):
        assert entry['pair']==[i,j]
        owner,axis,sign=entry['edge'];assert owner in (i,j) and axis in (0,1) and sign in (-1,1)
        other=j if owner==i else i;c,sn=directions[owner];pc,ps=symbols[owner]
        nx,ny=(c,sn) if axis==0 else (-sn,c)
        px,py=(pc,ps) if axis==0 else (-ps,pc)
        eps=Box.rational(sign);assert len(entry['vertices'])==4
        for v,proof in enumerate(entry['vertices']):
            x,y=points[other][v];sx,sy=spoints[other][v]
            gap=eps*(nx*(x-z[owner])+ny*(y-z[68+owner]))-half
            poly=sign*(px*(sx-variables[owner])+py*(sy-variables[68+owner]))-Q(1,2)
            check(poly,gap,proof)
    assert len(cert['walls'])==1088
    for (i,v,axis,sign),entry in zip(product(range(68),range(4),range(2),(-1,1)),cert['walls']):
        assert [entry[k] for k in ('square','vertex','axis','sign')]==[i,v,axis,sign]
        check(Q(1,2)*variables[136]-sign*spoints[i][v][axis],half*z[136]-Box.rational(sign)*points[i][v][axis],entry['proof'])
    assert len(cert['proposed_identities'])==437
    for p,pr in zip(s['all_polynomials'],cert['proposed_identities']):identity(P(terms=serialized(p)),pr,rows)
    return dict(valid=True,method='integer-cleared identities and direct dyadic vertex intervals',
      pairs=2278,walls=1088,unit_frames=68,exact_contacts=contacts,strict_predicates=strict,
      proposed_equations_implied=437,minimum_certified_positive_margin=str(minimum),dyadic_bits=420,
      shared_checks='released root contraction and descriptive polynomial binding',seconds=time.monotonic()-start)

if __name__=='__main__':print(json.dumps(verify(),indent=2))
