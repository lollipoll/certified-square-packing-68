"""Review check: derive zero relations afresh and use center/support geometry.

Imports no submitted proof code and reads no submitted identity multipliers.
The separately reviewed and replayed contraction proof supplies the root.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json, time

ROOT=Path(__file__).resolve().parent
PACKAGE=ROOT/'2026-10-07-root-feasibility'
start=time.monotonic()
s=json.loads((PACKAGE/'released/campaign/results/reduced/system.json').read_text())
w=json.loads((PACKAGE/'released/campaign/results/reduced/root_witness.json').read_text())
center=[Q(x) for x in w['center']];radius=Q(w['radius'])
box=[(x-radius,x+radius) for x in center]

def constant(x):
    x=Q(x);return {():x} if x else {}
def variable(i):return {(i,):Q(1)}
def linear(*terms):
    result={}
    for p,a in terms:
        for m,c in p.items():result[m]=result.get(m,Q(0))+a*c
    return {m:c for m,c in result.items() if c}
def multiply(p,q):
    result={}
    for m,c in p.items():
        for n,d in q.items():
            key=tuple(sorted(m+n));result[key]=result.get(key,Q(0))+c*d
    return {m:c for m,c in result.items() if c}
def scalar_product(a,b):return linear((multiply(a[0],b[0]),1),(multiply(a[1],b[1]),1))
def read(row):return {tuple(m):Q(c) for m,c in row if Q(c)}
def value(p):
    total=Q(0)
    for m,c in p.items():
        for i in m:c*=center[i]
        total+=c
    return total
def enclosure(p):
    low=high=Q(0)
    for m,c in p.items():
        a=b=c
        for i in m:
            x,y=box[i];products=(a*x,a*y,b*x,b*y);a,b=min(products),max(products)
        low+=a;high+=b
    return low,high

# Fresh row reduction, without the submitted representations.
pivots={}
def remainder(p):
    p=p.copy()
    while p:
        lead=max(p,key=lambda m:(len(m),m))
        if lead not in pivots:return p
        p=linear((p,1),(pivots[lead],-p[lead]))
    return {}
for row in s['polynomials']:
    p=remainder(read(row))
    assert p
    lead=max(p,key=lambda m:(len(m),m))
    pivots[lead]=linear((p,1/p[lead]))
assert len(pivots)==153
assert len(s['all_polynomials'])==437
assert all(not remainder(read(row)) for row in s['all_polynomials'])

groups={i:g for g,ids in enumerate(s['groups']) for i in ids}
frames=[];centers=[]
for i in range(68):
    centers.append((variable(i),variable(68+i)))
    if i in groups:
        k=137+2*groups[i];c,sn=variable(k),variable(k+1)
    else:
        t=Q(s['fixed_t'][str(i)]);d=1+t*t;assert d>0
        c,sn=constant((1-t*t)/d),constant(2*t/d)
    u=(c,sn);v=(linear((sn,-1)),c)
    assert not remainder(linear((scalar_product(u,u),1),(constant(1),-1)))
    assert not remainder(linear((scalar_product(v,v),1),(constant(1),-1)))
    assert not remainder(scalar_product(u,v))
    frames.append((u,v))

def absolute(p):
    # Signs are exact on the root box, or the expression vanishes at the root.
    if not p or not remainder(p):return {}
    lo,hi=enclosure(p)
    if lo>0:return p
    if hi<0:return linear((p,-1))
    raise AssertionError('Unresolved absolute-value branch')
def support(other,n):
    return linear((absolute(scalar_product(n,frames[other][0])),Q(1,2)),
                  (absolute(scalar_product(n,frames[other][1])),Q(1,2)))
def gap(owner,other,axis,sign):
    n=tuple(linear((p,sign)) for p in frames[owner][axis])
    difference=tuple(linear((b,1),(a,-1)) for a,b in zip(centers[owner],centers[other]))
    return linear((scalar_product(n,difference),1),(constant(Q(1,2)),-1),(support(other,n),-1))

pair_records=[]
for i,j in combinations(range(68),2):
    candidates=[]
    for owner,other in ((i,j),(j,i)):
        for axis in (0,1):
            for sign in (-1,1):
                p=gap(owner,other,axis,sign)
                candidates.append((value(p),owner,axis,sign,p))
    candidates.sort(key=lambda entry:entry[0],reverse=True)
    for _,owner,axis,sign,p in candidates:
        if not remainder(p):
            pair_records.append({'pair':[i,j],'edge':[owner,axis,sign],'kind':'exact_zero'})
            break
        lo,hi=enclosure(p)
        if lo>0:
            pair_records.append({'pair':[i,j],'edge':[owner,axis,sign],'kind':'strict','lower':str(lo)})
            break
    else:raise AssertionError(('Unseparated pair',i,j))

wall_records=[]
for i in range(68):
    c,sn=frames[i][0]
    extent=linear((absolute(c),Q(1,2)),(absolute(sn),Q(1,2)))
    for axis in (0,1):
        for sign in (-1,1):
            p=linear((variable(136),Q(1,2)),(centers[i][axis],-sign),(extent,-1))
            if not remainder(p):kind='exact_zero';lo=None
            else:
                lo,hi=enclosure(p);assert lo>0,(i,axis,sign);kind='strict'
            wall_records.append({'square':i,'axis':axis,'sign':sign,'kind':kind,'lower':str(lo) if lo is not None else None})

assert len(pair_records)==2278 and len(wall_records)==272
out={'valid':True,'method':'fresh rational row reduction and center/support geometry; axes selected anew',
     'selected_row_rank':len(pivots),'proposed_equations_implied':437,'unit_frames':68,
     'pairs':2278,'pair_exact_contacts':sum(r['kind']=='exact_zero' for r in pair_records),
     'pair_strict':sum(r['kind']=='strict' for r in pair_records),
     'support_wall_conditions':272,'wall_exact_contacts':sum(r['kind']=='exact_zero' for r in wall_records),
     'wall_strict':sum(r['kind']=='strict' for r in wall_records),'seconds':time.monotonic()-start,
     'shares':'released system and root witness; prior contraction proof reviewed and replayed separately',
     'imports_submitted_verifier_code':False,'reads_submitted_identity_multipliers':False,
     'pairs_ledger':pair_records,'walls_ledger':wall_records}
(ROOT/'support-audit.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if not k.endswith('_ledger')},indent=2))
