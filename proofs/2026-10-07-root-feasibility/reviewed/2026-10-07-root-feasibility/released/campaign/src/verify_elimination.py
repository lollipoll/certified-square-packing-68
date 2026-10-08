"""Certify that the 137 linear center/side equations can be eliminated."""
import json
from fractions import Fraction as F
from pathlib import Path

def main():
 p=Path('campaign/results/reduced');s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text());e=json.loads((p/'elimination_witness.json').read_text());x=list(map(F,w['center']));R=[[F(v) for v in r] for r in e['inverse']];J=[];H=F(0)
 for row in s['polynomials'][:137]:
  grad={};h=F(0)
  for inds,c in row:
   c=F(c);assert sum(i<137 for i in inds)<=1
   for pos,i in enumerate(inds):
    if i>=137:continue
    a=c
    for k,j in enumerate(inds):
     if k!=pos:a*=x[j]
    grad[i]=grad.get(i,F(0))+a
    if len(inds)==2:h+=abs(c)
  J.append(grad);H=max(H,h)
 n=137;defect=F(0)
 for i,row in enumerate(R):
  assert len(row)==n;err={i:F(1)}
  for j,a in enumerate(row):
   if a:
    for k,b in J[j].items():err[k]=err.get(k,F(0))-a*b
  defect=max(defect,sum(map(abs,err.values())))
 M=max(sum(map(abs,row)) for row in R);rho=F(e['radius']);bound=defect+M*H*rho;assert bound<1 and F(w['radius'])<rho
 out=dict(valid=True,dimension=n,box_radius=str(rho),inverse_defect=str(defect),inverse_defect_float=float(defect),uniform_defect_bound=str(bound),uniform_defect_bound_float=float(bound),meaning='The selected center/side coefficient matrix A is nonsingular throughout this box; the eight rational closure equations are a valid local elimination.')
 (p/'elimination_verification.json').write_text(json.dumps(out,indent=2)+'\n');print({k:out[k] for k in ['valid','dimension','box_radius','uniform_defect_bound_float']})
if __name__=='__main__':main()
