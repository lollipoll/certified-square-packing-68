"""Exact sparse polynomials and geometry; no numerical dependencies."""
from fractions import Fraction as Q
from itertools import product

SIGNS = list(product((-1, 1), repeat=2))

def clean(p): return {k:v for k,v in p.items() if v}
def const(q): return clean({():Q(q)})
def var(i): return {(i,):Q(1)}
def add(p,q):
    r=p.copy()
    for m,c in q.items(): r[m]=r.get(m,Q(0))+c
    return clean(r)
def scale(p,a): return clean({m:c*a for m,c in p.items()})
def sub(p,q): return add(p,scale(q,-1))
def mul(p,q):
    r={}
    for m,c in p.items():
        for n,d in q.items():
            k=tuple(sorted(m+n));r[k]=r.get(k,Q(0))+c*d
    return clean(r)
def dot(a,b): return add(mul(a[0],b[0]),mul(a[1],b[1]))
def read(p):
    r={}
    for m,c in p:
        assert tuple(m)==tuple(sorted(m)) and all(0<=i<153 for i in m)
        assert tuple(m) not in r
        r[tuple(m)]=Q(c)
    return clean(r)
def dump(p): return [[list(m),str(c)] for m,c in sorted(p.items())]
def interval(p,box):
    lo=hi=Q(0)
    for m,c in p.items():
        a=b=c
        for i in m:
            x,y=box[i];v=(a*x,a*y,b*x,b*y);a,b=min(v),max(v)
        lo+=a;hi+=b
    return lo,hi
def evaluate(p,x):
    total=Q(0)
    for m,c in p.items():
        for i in m:c*=x[i]
        total+=c
    return total

class Geometry:
    def __init__(self,s):
        assert s['variable_order']=='x[68],y[68],L,c0,s0,...,c7,s7'
        assert len(s['groups'])==8
        members=[i for g in s['groups'] for i in g]
        assert len(members)==len(set(members))
        fixed={int(i) for i in s['fixed_t']}
        assert not fixed.intersection(members) and fixed.union(members)==set(range(68))
        self.s=s; self.centers=[(var(i),var(i+68)) for i in range(68)]
        self.frames={};self.denominators={}
        for g,ids in enumerate(s['groups']):
            for i in ids:self.frames[i]=(var(137+2*g),var(138+2*g))
        for key,value in s['fixed_t'].items():
            i=int(key);t=Q(value);d=1+t*t;assert d>0
            self.denominators[i]=d
            self.frames[i]=(const((1-t*t)/d),const(2*t/d))
        self.vertices={i:[self.vertex(i,a,b) for a,b in SIGNS] for i in range(68)}
    def vertex(self,i,a,b):
        c,s=self.frames[i];x,y=self.centers[i]
        return add(x,scale(sub(scale(c,a),scale(s,b)),Q(1,2))),add(y,scale(add(scale(s,a),scale(c,b)),Q(1,2)))
    def axis(self,i,axis,sign):
        c,s=self.frames[i];u=(c,s) if axis==0 else (scale(s,-1),c)
        return tuple(scale(p,sign) for p in u)
    def gap(self,owner,other,axis,sign,v):
        p=self.vertices[other][v];o=self.centers[owner]
        return sub(dot(self.axis(owner,axis,sign),tuple(sub(a,b) for a,b in zip(p,o))),const(Q(1,2)))
    def wall(self,i,v,axis,sign):
        return sub(scale(var(136),Q(1,2)),scale(self.vertices[i][v][axis],sign))
    def description(self,d):
        k=d['kind']
        if k=='circle':
            c,s=var(137+2*d['group']),var(138+2*d['group'])
            return sub(add(mul(c,c),mul(s,s)),const(1))
        if k=='gauge':return sub(var(d['variable']),const(d['value']))
        if k=='vertex_edge':return self.gap(d['edge_square'],d['vertex_square'],int(d['edge'][1]=='v'),1 if d['edge'][0]=='+' else -1,SIGNS.index(tuple(d['vertex'])))
        if k=='vertex_wall':return scale(self.wall(d['square'],SIGNS.index(tuple(d['vertex'])),int(d['wall'] in ('top','bottom')),1 if d['wall'] in ('top','right') else -1),-1)
        raise ValueError(k)
    def bind(self):
        s=self.s;allp=list(map(read,s['all_polynomials']));basis=s['basis_rows']
        assert len(allp)==len(s['all_descriptions'])==437
        assert all(self.description(d)==p for d,p in zip(s['all_descriptions'],allp))
        assert len(basis)==len(set(basis))==153
        assert basis==s['linear_rows']+s['closure_rows'] and len(s['linear_rows'])==137
        assert basis[137:145]==list(range(8))
        assert [allp[i] for i in basis]==list(map(read,s['polynomials']))
        return allp

class Span:
    """Sparse rational row reduction, retaining exact F-row combinations."""
    def __init__(self):self.rows={}
    @staticmethod
    def key(m):return len(m),m
    def reduce(self,p):
        p=p.copy();representation={}
        while p:
            lead=max(p,key=self.key)
            if lead not in self.rows:break
            row,proof=self.rows[lead];a=p[lead]
            p=sub(p,scale(row,a));representation=add(representation,scale(proof,a))
        return p,representation
    def insert(self,p,proof):
        remainder,used=self.reduce(p)
        if not remainder:return False
        lead=max(remainder,key=self.key);a=1/remainder[lead]
        self.rows[lead]=(scale(remainder,a),scale(sub(proof,used),a))
        return True
