#!/usr/bin/env python3
"""One offline command; standard library; sequential checks; inputs never written."""
import contextlib,hashlib,io,json,os,runpy,shutil,sys,tempfile,time
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def run(path,args=(),cwd=None):
    old_args=sys.argv[:];old_cwd=Path.cwd();capture=io.StringIO();start=time.monotonic()
    try:
        sys.argv=[str(path),*args]
        if cwd:os.chdir(cwd)
        with contextlib.redirect_stdout(capture),contextlib.redirect_stderr(capture):
            try:runpy.run_path(str(path),run_name='__main__')
            except SystemExit as e:
                if e.code not in (None,0):raise
    finally:sys.argv=old_args;os.chdir(old_cwd)
    print(path.name+': PASS',flush=True)
    return dict(script=path.name,seconds=time.monotonic()-start,output=capture.getvalue())

def main():
    if sys.flags.optimize:raise RuntimeError('Run Python with assertions enabled; no -O/-OO.')
    sys.dont_write_bytecode=True
    start=time.monotonic();manifest=json.loads((ROOT/'MANIFEST.json').read_text())
    for name,h in manifest.items():
        assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==h,'hash mismatch: '+name
    print('Study manifest:',len(manifest),'hashes PASS',flush=True)
    logs=[];released=ROOT/'released'
    logs.append(run(released/'check_hashes.py'))
    logs.append(run(released/'verify.py',[str(released/'n68.json'),'--n','68']))
    logs.append(run(released/'independent_support_check.py',[str(released/'n68.json'),'--n','68']))
    logs.append(run(released/'check_polynomial_binding.py'))
    # Original scripts write receipts relative to cwd. Run only in a fresh copy.
    with tempfile.TemporaryDirectory(prefix='n68-geometry-baseline-') as temporary:
        work=Path(temporary);shutil.copytree(released/'campaign',work/'campaign')
        sys.path.insert(0,str(work/'campaign/src'))
        for name in ('verify_root','verify_elimination','verify_family_minimum','verify_fixed_angle','test_verifiers'):
            logs.append(run(work/'campaign/src'/f'{name}.py',cwd=work))
        # Retain root/elimination receipts in the returned replay log, not inputs.
        for name in ('root_verification','elimination_verification','family_minimum_verification'):
            logs.append(dict(receipt=name,data=json.loads((work/'campaign/results/reduced'/f'{name}.json').read_text())))
        sys.path.pop(0)
    sys.path.insert(0,str(ROOT))
    for name in ('verify_certificate','verify_secondary','controls'):
        logs.append(run(ROOT/f'{name}.py'))
    out=dict(valid=True,total_seconds=time.monotonic()-start,checks=logs,network=False,simultaneous_computation_processes=1)
    # Optional output is outside the sealed inputs; default is a new temp file.
    if len(sys.argv)>1:destination=Path(sys.argv[1]).resolve()
    else:
        fd,name=tempfile.mkstemp(prefix='n68-all-inequality-replay-',suffix='.json');os.close(fd);destination=Path(name)
    assert destination not in [(ROOT/name).resolve() for name in manifest]
    destination.write_text(json.dumps(out,indent=2)+'\n')
    print('ALL CHECKS PASS; seconds:',round(out['total_seconds'],3),'; receipt:',destination)
if __name__=='__main__':main()
