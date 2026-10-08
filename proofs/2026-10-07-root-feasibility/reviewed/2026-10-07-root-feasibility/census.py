"""First checkpoint: exact root-box gap census and constant row identities."""
import json,time
from pathlib import Path
from collections import Counter
from itertools import combinations
from geometry import *

ROOT=Path(__file__).resolve().parent
def main():
    start=time.monotonic();p=ROOT/'released/campaign/results/reduced'
    s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text())
    g=Geometry(s);allp=g.bind();polys=list(map(read,s['polynomials']))
    x=list(map(Q,w['center']));r=Q(w['radius']);box=[(v-r,v+r) for v in x]
    span=Span()
    for j,f in enumerate(polys):span.insert(f,{(j,):Q(1)})
    counts=Counter();unresolved=[];identities={};positive=[]
    def classify(p,label):
        lo,hi=interval(p,box)
        if lo>0:counts['strict']+=1;positive.append(lo);return 'strict'
        if hi<0:counts['negative']+=1;unresolved.append(dict(label=label,status='negative',polynomial=dump(p),interval=[str(lo),str(hi)]));return 'negative'
        rem,proof=span.reduce(p)
        if not rem:
            counts['identity']+=1;identities[str(label)]=dump(proof);return 'identity'
        counts['unresolved']+=1;unresolved.append(dict(label=label,status='unresolved',polynomial=dump(p),interval=[str(lo),str(hi)],remainder=dump(rem)));return 'unresolved'
    pairs=[]
    # Rational evaluation proposes axes; every candidate is evaluated exactly.
    for i,j in combinations(range(68),2):
        choices=[]
        for owner,other in ((i,j),(j,i)):
            for axis,sign in product(range(2),(-1,1)):
                gaps=[g.gap(owner,other,axis,sign,v) for v in range(4)]
                score=min(evaluate(p,x) for p in gaps)
                choices.append((score,owner,other,axis,sign,gaps))
        choices.sort(key=lambda z:z[0],reverse=True)
        score,owner,other,axis,sign,gaps=choices[0]
        states=[classify(p,['pair',i,j,owner,axis,sign,v]) for v,p in enumerate(gaps)]
        pairs.append(dict(pair=[i,j],owner=owner,axis=axis,sign=sign,states=states))
    walls=[]
    for i,v,axis,sign in product(range(68),range(4),range(2),(-1,1)):
        state=classify(g.wall(i,v,axis,sign),['wall',i,v,axis,sign]);walls.append([i,v,axis,sign,state])
    proposed=[]
    for k,p in enumerate(allp):
        rem,pr=span.reduce(p);lo,hi=interval(p,box)
        proposed.append(dict(row=k,status='identity' if not rem else 'positive' if lo>0 else 'negative' if hi<0 else 'unresolved',interval=[str(lo),str(hi)],proof=dump(pr) if not rem else None))
    out=dict(counts=dict(counts),minimum_positive=str(min(positive)),pairs=pairs,walls=walls,unresolved=unresolved,identities=identities,proposed=proposed,seconds=time.monotonic()-start)
    (ROOT/'census.json').write_text(json.dumps(out,indent=2)+'\n')
    print('counts',counts,'minimum positive',float(min(positive)),'seconds',out['seconds'],flush=True)
    print('unresolved pair/wall labels',[u['label'] for u in unresolved],flush=True)
    print('proposed',Counter(p['status'] for p in proposed),flush=True)
if __name__=='__main__':main()
