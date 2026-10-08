#!/usr/bin/env python3
"""Reconstruct all contact polynomials exactly from their geometric descriptions."""
from fractions import Fraction as Q
from pathlib import Path
import json


class Polynomial:
    def __init__(self,value=0,terms=None):
        self.terms = {():Q(value)} if terms is None else terms

    @classmethod
    def variable(cls,index):
        return cls(terms={(index,):Q(1)})

    def __add__(self,other):
        if not isinstance(other,Polynomial):
            other=Polynomial(other)
        terms=dict(self.terms)
        for key,value in other.terms.items():
            terms[key]=terms.get(key,Q(0))+value
        return Polynomial(terms={k:v for k,v in terms.items() if v})

    __radd__=__add__

    def __neg__(self):
        return Polynomial(terms={k:-v for k,v in self.terms.items()})

    def __sub__(self,other):
        return self+-other if isinstance(other,Polynomial) else self+Polynomial(-other)

    def __mul__(self,other):
        if not isinstance(other,Polynomial):
            other=Polynomial(other)
        terms={}
        for key,value in self.terms.items():
            for second,coefficient in other.terms.items():
                product=tuple(sorted(key+second))
                terms[product]=terms.get(product,Q(0))+value*coefficient
        return Polynomial(terms={k:v for k,v in terms.items() if v})

    __rmul__=__mul__


def verify(system):
    variables=[Polynomial.variable(i) for i in range(153)]
    groups={i:g for g,members in enumerate(system['groups']) for i in members}
    if len(system['groups']) != 8 or len(groups)!=sum(map(len,system['groups'])):
        raise ValueError('Invalid or repeated orientation groups')
    directions={}
    for i in range(68):
        if i in groups:
            g=groups[i]
            directions[i]=(variables[137+2*g],variables[138+2*g])
        else:
            t=Q(system['fixed_t'][str(i)])
            directions[i]=(Polynomial((1-t*t)/(1+t*t)),Polynomial(2*t/(1+t*t)))

    def vertex(i,signs):
        a,b=signs;c,s=directions[i]
        return (variables[i]+Q(1,2)*(a*c-b*s),variables[68+i]+Q(1,2)*(a*s+b*c))

    reconstructed=[]
    for description in system['all_descriptions']:
        kind=description['kind']
        if kind=='circle':
            g=description['group'];c,s=variables[137+2*g:139+2*g]
            expression=c*c+s*s-1
        elif kind=='gauge':
            expression=variables[description['variable']]-Q(description['value'])
        elif kind=='vertex_wall':
            x,y=vertex(description['square'],description['vertex'])
            wall=description['wall'];sign=1 if wall in ['top','right'] else -1
            expression=sign*(x if wall in ['left','right'] else y)-Q(1,2)*variables[136]
        elif kind=='vertex_edge':
            j=description['edge_square'];x,y=vertex(description['vertex_square'],description['vertex'])
            c,s=directions[j]
            nx,ny=(c,s) if description['edge'][1]=='u' else (-s,c)
            sign=1 if description['edge'][0]=='+' else -1
            expression=sign*((x-variables[j])*nx+(y-variables[68+j])*ny)-Q(1,2)
        else:
            raise ValueError('Unknown polynomial description')
        reconstructed.append(expression.terms)

    def read(polynomials):
        return [{tuple(indices):Q(value) for indices,value in row if Q(value)} for row in polynomials]

    actual=read(system['all_polynomials'])
    if reconstructed!=actual:
        raise ValueError('A polynomial differs from its geometric description')
    basis=system['basis_rows']
    if len(basis)!=153 or len(set(basis))!=153 or len(system['linear_rows'])!=137:
        raise ValueError('Invalid basis inventory')
    if [actual[i] for i in basis]!=read(system['polynomials']):
        raise ValueError('Selected polynomial basis differs')
    if basis[:137]!=system['linear_rows'] or basis[137:145]!=list(range(8)):
        raise ValueError('Unexpected linear and circle row ordering')
    if any(sum(i<137 for i in indices)>1 for row in system['polynomials'][:137] for indices,coefficient in row):
        raise ValueError('A held equation is nonlinear in center/side variables')
    return len(actual)


if __name__=='__main__':
    path=Path(__file__).resolve().parent/'campaign/results/reduced/system.json'
    count=verify(json.loads(path.read_text()))
    print(f'All {count} contact polynomials match the exact geometric reconstruction; selected basis verified.')
