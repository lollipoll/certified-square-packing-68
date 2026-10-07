"""Standard-library exact Krawczyk/contraction proof for a quadratic system.
Given center x, rational preconditioner R, and infinity radius r, prove
 ||R F(x)|| + (||I-R J(x)|| + ||R|| H r) r < r,
where H bounds the infinity-operator Lipschitz constant of the Jacobian.
This proves a unique zero in the box (and nonsingular Jacobian there), NOT
packing optimality or feasibility of other inequalities.
"""
from fractions import Fraction as F
from pathlib import Path
import json,sys,hashlib,time

def verify(system,witness):
 polys=[[(tuple(k),F(v)) for k,v in p] for p in system['polynomials']];x=list(map(F,witness['center']));R=[[F(v) for v in row] for row in witness['inverse']];r=F(witness['radius']);n=len(x)
 assert n==len(polys)==len(R) and all(len(row)==n for row in R) and r>0
 fs=[];J=[];hs=[]
 for p in polys:
  f=F(0);row={};h=F(0)
  for inds,c in p:
   assert len(inds)<=2 and all(0<=i<n for i in inds)
   t=c
   for i in inds:t*=x[i]
   f+=t
   for pos,i in enumerate(inds):
    t=c
    for j,k in enumerate(inds):
     if j!=pos:t*=x[k]
    row[i]=row.get(i,F(0))+t
   h+=abs(c)*len(inds)*max(0,len(inds)-1)
  fs.append(f);J.append(row);hs.append(h)
 normR=max(sum(map(abs,row)) for row in R);H=max(hs);defect=F(0);beta=F(0)
 for i,row in enumerate(R):
  beta=max(beta,abs(sum(a*b for a,b in zip(row,fs))));err={i:F(1)}
  for j,a in enumerate(row):
   if a:
    for k,b in J[j].items():err[k]=err.get(k,F(0))-a*b
  defect=max(defect,sum(map(abs,err.values())))
 contraction=defect+normR*H*r;image=beta+contraction*r
 assert contraction<1 and image<r
 return dict(valid=True,dimension=n,radius=str(r),residual_preconditioned=str(beta),residual_preconditioned_float=float(beta),jacobian_defect=str(defect),jacobian_defect_float=float(defect),inverse_norm=str(normR),hessian_bound=str(H),contraction_bound=str(contraction),image_radius=str(image),side_interval=[str(x[136]-r),str(x[136]+r)],meaning='Unique zero of the explicitly gauge-fixed polynomial system in the closed infinity-norm box. No optimality claim.')

def main():
 p=Path('campaign/results/reduced');s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text());start=time.monotonic();r=verify(s,w);r['seconds']=time.monotonic()-start;r['system_sha256']=hashlib.sha256((p/'system.json').read_bytes()).hexdigest();r['witness_sha256']=hashlib.sha256((p/'root_witness.json').read_bytes()).hexdigest();(p/'root_verification.json').write_text(json.dumps(r,indent=2)+'\n');print({k:r[k] for k in ['valid','dimension','radius','residual_preconditioned_float','jacobian_defect_float','seconds']})
if __name__=='__main__':main()
