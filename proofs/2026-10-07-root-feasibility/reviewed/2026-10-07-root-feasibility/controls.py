"""Adversarial controls; each must actually be rejected by the indicated check."""
import copy,json,time
from pathlib import Path
from geometry import *
from verify_certificate import verify,check_identity,verify_root
from verify_secondary import verify as secondary,identity as second_identity,P

ROOT=Path(__file__).resolve().parent
def main():
    start=time.monotonic();base=json.loads((ROOT/'certificate.json').read_text());records=[]
    def reject(label,fn):
        try:fn()
        except (AssertionError,ValueError):records.append(dict(control=label,rejected=True));return
        raise AssertionError('CONTROL ACCEPTED: '+label)
    def both(label,mutate):
        candidate=copy.deepcopy(base);mutate(candidate)
        reject(label+' / primary',lambda:verify(candidate,root_check=False))
        reject(label+' / secondary',lambda:secondary(candidate,replay_root=False))
    def coefficient(d):
        p=next(p for e in d['pairs'] for p in e['vertices'] if p.get('identity'))
        p['identity'][0][1]=str(Q(p['identity'][0][1])+1)
    both('changed contact identity coefficient',coefficient)
    both('missing unordered pair',lambda d:d['pairs'].pop(42))
    both('duplicate pair replacing another',lambda d:d['pairs'].__setitem__(12,copy.deepcopy(d['pairs'][11])))
    both('missing wall predicate',lambda d:d['walls'].pop(0))
    both('mismatched root hash',lambda d:d['input_sha256'].__setitem__('released/campaign/results/reduced/root_witness.json','0'*64))
    def invalid_frame(d):d['frames'][8]['u'][0][0][1]='2'
    both('altered declared unit frame',invalid_frame)
    def bad_bound(d):
        p=next(p for e in d['pairs'] for p in e['vertices'] if 'positive' in p);p['positive']=10**50
    both('inflated positive interval bound',bad_bound)
    def fake_zero(d):
        p=next(p for e in d['pairs'] for p in e['vertices'] if 'positive' in p);p.clear();p['identity']=[]
    both('false zero replacing a strict gap',fake_zero)
    path=ROOT/'released/campaign/results/reduced'
    s=json.loads((path/'system.json').read_text());w=json.loads((path/'root_witness.json').read_text())
    bad=copy.deepcopy(w);bad['center'][136]=str(Q(w['center'][136])+Q(1,1000))
    reject('mismatched actual root center / contraction',lambda:verify_root(s,bad))
    bads=copy.deepcopy(s);bads['polynomials'][0].append([[], '1/10'])
    reject('changed actual selected system / geometric binding',lambda:Geometry(bads).bind())
    # Check unit length rejection itself, independently of frame-to-model binding.
    polys=list(map(read,s['polynomials']));c,sn=var(137),var(138)
    invalid=sub(add(scale(mul(c,c),4),mul(sn,sn)),const(1))
    proof=base['frames'][8]['identities'][0]
    reject('nonunit norm (2c,s) / primary identity',lambda:check_identity(invalid,proof,polys))
    pc,ps=P.variable(137),P.variable(138)
    reject('nonunit norm (2c,s) / integer identity',lambda:second_identity(4*pc*pc+ps*ps-1,proof,polys))
    print(json.dumps(dict(valid=True,controls=records,count=len(records),seconds=time.monotonic()-start),indent=2))
if __name__=='__main__':main()
