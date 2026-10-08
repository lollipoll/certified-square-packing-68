"""Untrusted certificate producer. Verifiers do not call this file."""
import hashlib,json,time
from pathlib import Path
from geometry import *

ROOT=Path(__file__).resolve().parent
BOUND_SCALE=10**30
INPUTS=['released/n68.json','released/campaign/results/reduced/system.json',
        'released/campaign/results/reduced/root_witness.json',
        'released/campaign/results/reduced/elimination_witness.json']
def main():
    start=time.monotonic();p=ROOT/'released/campaign/results/reduced'
    s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text())
    census=json.loads((ROOT/'census.json').read_text())
    g=Geometry(s);allp=g.bind();polys=list(map(read,s['polynomials']))
    x=list(map(Q,w['center']));r=Q(w['radius']);box=[(v-r,v+r) for v in x]
    span=Span()
    for j,f in enumerate(polys):span.insert(f,{(j,):Q(1)})
    def identity(p):
        rem,proof=span.reduce(p);assert not rem
        return [[m[0],str(c)] for m,c in sorted(proof.items())]
    def witness(p):
        lo,hi=interval(p,box)
        if lo>0:
            a=lo*BOUND_SCALE;v=a.numerator//a.denominator;assert v>0
            return dict(positive=v)
        return dict(identity=identity(p))
    pairs=[]
    for entry in census['pairs']:
        i,j=entry['pair'];owner=entry['owner'];other=j if owner==i else i
        axis,sign=entry['axis'],entry['sign']
        pairs.append(dict(pair=[i,j],edge=[owner,axis,sign],vertices=[witness(g.gap(owner,other,axis,sign,v)) for v in range(4)]))
    walls=[]
    for i,v,axis,sign in product(range(68),range(4),range(2),(-1,1)):
        walls.append(dict(square=i,vertex=v,axis=axis,sign=sign,proof=witness(g.wall(i,v,axis,sign))))
    frames=[]
    for i in range(68):
        u=g.axis(i,0,1);v=g.axis(i,1,1)
        frames.append(dict(square=i,u=[dump(p) for p in u],v=[dump(p) for p in v],
                           identities=[identity(sub(dot(u,u),const(1))),identity(sub(dot(v,v),const(1))),identity(dot(u,v))],
                           fixed_denominator=str(g.denominators[i]) if i in g.denominators else None))
    data=dict(schema='n68-all-inequality-v1',input_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in INPUTS},
              positive_scale=BOUND_SCALE,vertex_signs=SIGNS,pairs=pairs,walls=walls,frames=frames,
              proposed_identities=[identity(p) for p in allp])
    (ROOT/'certificate.json').write_text(json.dumps(data,indent=2)+'\n')
    print('certificate written in',time.monotonic()-start,'seconds')
if __name__=='__main__':main()
