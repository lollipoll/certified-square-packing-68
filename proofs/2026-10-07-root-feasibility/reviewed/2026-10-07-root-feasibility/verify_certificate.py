#!/usr/bin/env python3
"""Exact all-inequality verifier: sparse coefficient identities and Fraction boxes."""
import hashlib,json,sys,time
from pathlib import Path
from itertools import combinations
from collections import Counter
from geometry import *

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'released/campaign/src'))
from verify_root import verify as verify_root

EXPECTED={
 'released/n68.json':'6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9',
 'released/campaign/results/reduced/system.json':'0bc2c2deea9f63d4ed1a3473ed50f71327ce33676bfd7ee1f43c371d13e481de',
 'released/campaign/results/reduced/root_witness.json':'fa234967c8496538ee67614a7d8b68c58022f34bcc698b48eda00eb7282fe824',
 'released/campaign/results/reduced/elimination_witness.json':'512b6a0c06b28478482b4b03c519b70f1f716dfe249bcbd5beff10df7112e807'}

def check_identity(target,proof,polys):
    result={};seen=set()
    for j,c in proof:
        assert isinstance(j,int) and 0<=j<len(polys) and j not in seen
        seen.add(j);c=Q(c);assert c
        result=add(result,scale(polys[j],c))
    assert result==target,'coefficient identity failed'

def verify(data,root_check=True):
    assert not sys.flags.optimize,'Assertions must be enabled'
    assert data['schema']=='n68-all-inequality-v1'
    assert data['input_sha256']==EXPECTED
    for f,h in EXPECTED.items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h
    p=ROOT/'released/campaign/results/reduced'
    s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text())
    g=Geometry(s);allp=g.bind();polys=list(map(read,s['polynomials']))
    root=verify_root(s,w) if root_check else None
    x=list(map(Q,w['center']));r=Q(w['radius']);box=[(v-r,v+r) for v in x]
    assert x[136]-r>0 and data['vertex_signs']==[list(v) for v in SIGNS]
    published=Q(json.loads((ROOT/'released/n68.json').read_text())['container_side'])
    comparison=json.loads((ROOT/'side-comparison.json').read_text())
    assert Q(comparison['rational_side'])==published
    assert Q(comparison['root_center_side'])==x[136] and Q(comparison['root_radius'])==r
    assert list(map(Q,comparison['rational_minus_root_interval']))==[published-x[136]-r,published-x[136]+r]
    assert published-x[136]-r>0
    scale_=data['positive_scale'];assert isinstance(scale_,int) and scale_>0
    counts=Counter();margins=[];minimum_label=None;minimum_bound=None
    def check(p,proof,label):
        nonlocal minimum_label,minimum_bound
        if set(proof)=={'identity'}:
            check_identity(p,proof['identity'],polys);counts['exact_contacts']+=1
        else:
            assert set(proof)=={'positive'} and isinstance(proof['positive'],int)
            bound=Q(proof['positive'],scale_);assert bound>0
            lo,hi=interval(p,box);assert lo>=bound,'positive bound failed'
            if minimum_bound is None or bound<minimum_bound:minimum_label=label;minimum_bound=bound
            margins.append(bound);counts['strict_predicates']+=1
    assert len(data['frames'])==68
    for i,frame in enumerate(data['frames']):
        assert frame['square']==i
        u=tuple(map(read,frame['u']));v=tuple(map(read,frame['v']))
        assert len(u)==len(v)==2
        assert u==g.axis(i,0,1) and v==g.axis(i,1,1),'frame differs from declared geometry'
        assert len(frame['identities'])==3
        for target,proof in zip((sub(dot(u,u),const(1)),sub(dot(v,v),const(1)),dot(u,v)),frame['identities']):check_identity(target,proof,polys)
        if i in g.denominators:assert Q(frame['fixed_denominator'])==g.denominators[i]>0
        else:assert frame['fixed_denominator'] is None
    assert len(data['pairs'])==2278
    for expected,entry in zip(combinations(range(68),2),data['pairs']):
        assert entry['pair']==list(expected),'pair coverage failed'
        owner,axis,sign=entry['edge'];assert owner in expected and axis in (0,1) and sign in (-1,1)
        other=expected[1] if owner==expected[0] else expected[0]
        assert len(entry['vertices'])==4
        for v,proof in enumerate(entry['vertices']):check(g.gap(owner,other,axis,sign,v),proof,['pair',*expected,'vertex',v])
    assert len(data['walls'])==1088
    for expected,entry in zip(product(range(68),range(4),range(2),(-1,1)),data['walls']):
        assert [entry[k] for k in ('square','vertex','axis','sign')]==list(expected),'wall coverage failed'
        check(g.wall(*expected),entry['proof'],['wall',*expected])
    assert len(data['proposed_identities'])==437
    for f,pr in zip(allp,data['proposed_identities']):check_identity(f,pr,polys)
    return dict(valid=True,pairs=2278,wall_predicates=1088,unit_frames=68,unit_identities=204,
                proposed_equations_implied=437,**dict(counts),minimum_certified_positive_margin=str(min(margins)),minimum_label=minimum_label,
                root_verified=root_check,root_radius=w['radius'],side_interval=root['side_interval'] if root else None)

def main():
    start=time.monotonic();data=json.loads((ROOT/'certificate.json').read_text());r=verify(data)
    r['seconds']=time.monotonic()-start;print(json.dumps(r,indent=2))
if __name__=='__main__':main()
