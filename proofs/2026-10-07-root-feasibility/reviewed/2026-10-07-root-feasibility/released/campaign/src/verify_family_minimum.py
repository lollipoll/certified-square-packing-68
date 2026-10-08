"""Exact restricted local minimum proof using a uniform inverse-Jacobian bound.
The 137 chosen linear-in-centers equations and the eight circles stay equalities.
Only the final eight contact equations may open (with their geometric signs).
Every genuine packing in this explicitly restricted family and box has L>=L*.
For quadratics, F(z)-F(z*)=J((z+z*)/2)(z-z*) exactly. Positivity of the last
8 entries of e_L^T J^{-1}, with wall signs corrected, proves the inequality.
"""
import json
from fractions import Fraction as F
from pathlib import Path
from verify_root import verify as verify_root

def main():
 p=Path('campaign/results/reduced');s=json.loads((p/'system.json').read_text());w=json.loads((p/'root_witness.json').read_text());root=verify_root(s,w);R=[[F(v) for v in row] for row in w['inverse']];base=F(root['jacobian_defect']);norm=F(root['inverse_norm']);H=F(root['hessian_bound']);signs=[]
 for idx in s['basis_rows'][-8:]:
  e=s['all_descriptions'][idx];assert e['kind'] in ['vertex_edge','vertex_wall'];signs.append(-1 if e['kind']=='vertex_wall' else 1)
 minimum=min(sign*a for sign,a in zip(signs,R[136][-8:]));assert minimum>0
 choices=[]
 for k in range(5,16):
  rho=F(1,10**k);delta=base+norm*H*rho
  if delta>=1:continue
  error=delta/(1-delta)*norm
  if error<minimum:choices.append((rho,delta,error))
 assert choices
 rho,delta,error=choices[0];assert F(w['radius'])<rho
 result=dict(valid=True,dimension=153,variable_order=s['variable_order'],box_center=w['center'],box_radius=str(rho),root_box_radius=w['radius'],equality_rows=list(range(145)),inequality_rows=list(range(145,153)),inequality_signs=signs,minimum_signed_inverse_coefficient=str(minimum),minimum_signed_inverse_coefficient_float=float(minimum),inverse_uncertainty_bound=str(error),inverse_uncertainty_bound_float=float(error),jacobian_defect_bound=str(delta),root_unique=True,conclusion='The enclosed algebraic root is the unique minimum of the specified contact relaxation in the stated box; its side is a local lower bound for actual packings satisfying the held equalities.',scope='Eight orientation groups as encoded; all other orientations fixed. The first 137 selected center/side equations (including 22 coordinate gauges) and eight unit circles are equalities. The remaining eight chosen contacts are feasible inequalities. Additional genuine-packing inequalities only shrink this family. Attainment by an exact algebraic packing is not asserted: exact all-pairs feasibility is proved for the separately rounded rational certificate. This does not prove unrestricted variable-angle local optimality, nor excludes opening the held contacts or changing supporting edges.')
 (p/'family_minimum_verification.json').write_text(json.dumps(result,indent=2)+'\n');print({k:result[k] for k in ['valid','box_radius','minimum_signed_inverse_coefficient_float','inverse_uncertainty_bound_float']})
if __name__=='__main__':main()
