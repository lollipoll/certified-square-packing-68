#!/usr/bin/env python3
"""Replay all supplied proof checks in a temporary copy, preserving delivered files."""
from pathlib import Path
import shutil, subprocess, sys, tempfile

if sys.flags.optimize:
    raise RuntimeError('Run without -O or -OO; the supplied proof checks use assertions.')
root = Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(root/'check_polynomial_binding.py')],check=True)
with tempfile.TemporaryDirectory(prefix='n68-proof-replay-') as temporary:
    work = Path(temporary)
    shutil.copytree(root/'campaign',work/'campaign')
    for name in ['verify_root','verify_elimination','verify_family_minimum','verify_fixed_angle','test_verifiers']:
        print('\nChecking '+name,flush=True)
        subprocess.run([sys.executable,'-B',str(work/'campaign/src'/(name+'.py'))],cwd=work,check=True)
print('\nAll analytic and restricted-bound checks passed. Delivered files were not changed.')
