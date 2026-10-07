"""Adversarial proof-checker tests; run from the project root with normal Python."""
import json, unittest, copy
from fractions import Fraction as F
from pathlib import Path
from independent_verify import exact_check
from published_verify import verify
from verify_root import verify as root_check
from verify_fixed_angle import verify as dual_check
ROOT=Path('campaign/results')
class VerificationTests(unittest.TestCase):
 def small(self):
  return dict(schema='packing-n/exact-v1',n=2,container_side='2',squares=[dict(x='-1/2',y='0',t='0'),dict(x='1/2',y='0',t='0')])
 def test_exact_touching(self):
  d=self.small();self.assertTrue(exact_check(d,2)['valid']);self.assertTrue(verify(d,2)['valid_exact'])
 def test_tiny_overlap_rejected(self):
  d=self.small();d['squares'][1]['x']=str(F(1,2)-F(1,10**100));self.assertFalse(exact_check(d,2)['valid']);self.assertFalse(verify(d,2)['valid_exact'])
 def test_tiny_wall_violation_rejected(self):
  d=self.small();d['squares'][1]['x']=str(F(1,2)+F(1,10**100));self.assertFalse(exact_check(d,2)['valid']);self.assertFalse(verify(d,2)['valid_exact'])
 def test_inventory_rejected(self):
  d=self.small();d['n']=68
  with self.assertRaises(ValueError):exact_check(d,68)
  with self.assertRaises(AssertionError):verify(d,68)
 def test_bad_root_witness_rejected(self):
  s=json.loads((ROOT/'reduced/system.json').read_text());w=json.loads((ROOT/'reduced/root_witness.json').read_text());w['radius']='1/1'+'0'*140
  with self.assertRaises(AssertionError):root_check(s,w)
 def test_negative_dual_rejected(self):
  d=json.loads((ROOT/'best_exact.json').read_text());w=json.loads((ROOT/'fixed_angle/witness.json').read_text());w['dual_weights'][0]=str(-F(w['dual_weights'][0]))
  with self.assertRaises(AssertionError):dual_check(d,w)
 def test_polynomials_match_geometry(self):
  system=json.loads((ROOT/'reduced/system.json').read_text());z=list(map(F,json.loads((ROOT/'reduced/root_witness.json').read_text())['center']));group={i:g for g,ids in enumerate(system['groups']) for i in ids}
  for probe in range(3):
   point=[v+F(((i+11*probe)%17)-8,10**(3+probe)) for i,v in enumerate(z)]
   cs={}
   for i in range(68):
    if i in group:g=group[i];cs[i]=(point[137+2*g],point[138+2*g])
    else:
     t=F(system['fixed_t'][str(i)]);cs[i]=((1-t*t)/(1+t*t),2*t/(1+t*t))
   def vertex(i,v):
    a,b=v;c,s=cs[i];return (point[i]+(a*c-b*s)/2,point[68+i]+(a*s+b*c)/2)
   for poly,desc in zip(system['all_polynomials'],system['all_descriptions']):
    value=F(0)
    for inds,coef in poly:
     v=F(coef)
     for i in inds:v*=point[i]
     value+=v
    kind=desc['kind']
    if kind=='circle':
     g=desc['group'];expected=point[137+2*g]**2+point[138+2*g]**2-1
    elif kind=='gauge':expected=point[desc['variable']]-F(desc['value'])
    elif kind=='vertex_wall':
     w=desc['wall'];v=vertex(desc['square'],desc['vertex']);expected=(1 if w in ['top','right'] else -1)*v[0 if w in ['left','right'] else 1]-point[136]/2
    elif kind=='vertex_edge':
     j=desc['edge_square'];v=vertex(desc['vertex_square'],desc['vertex']);c,s=cs[j];a,b=(c,s) if desc['edge'][1]=='u' else (-s,c);sign=1 if desc['edge'][0]=='+' else -1;expected=sign*((v[0]-point[j])*a+(v[1]-point[68+j])*b)-F(1,2)
    else:raise ValueError(desc)
    self.assertEqual(value,expected)
if __name__=='__main__':unittest.main()
