# n=68 registration evidence, 7 October 2026

[Registration issue #428](https://github.com/jlevy/squares/issues/428) requests review of the exact v1.1.0 refinement. It is pending; no acceptance is claimed. [Submitted text](registration.md), [exact comparison](comparison.json), and [full source commits, retrieval times and hashes](source-manifest.json) preserve the dated evidence.

The release tag resolves to `fded686668e29258dad2eb29d0482fa3fd51bd6b`. Its `refinement-v1.1.0` folder is unchanged. The authoritative certificate SHA256 remains `6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9`. All four documented release commands passed freshly with assertions enabled; [command/time receipt](receipts/n68-release-checks.json) and individual logs record the results. Both direct geometry commands accepted all 2,278 unordered pairs, exact unit sides/right angles and containment at zero tolerance. Analytic checks and all seven verifier tests passed.

From the repository root, reproduce the released checks:

```sh
cd refinement-v1.1.0
python3 check_hashes.py
python3 -B verify.py n68.json --n 68 --reference-side 8.798795237221
python3 -B independent_support_check.py n68.json --n 68
python3 -B verify_analytic.py
```

From the repository root, replay the pinned Daniel certificate and exact comparison:

```sh
python3 -B publication/20261007/check_comparison.py
```

Python 3.9+ standard library, no `-O`/`-OO`. The adapter translates `(x,y,t)` in `[0,S]^2` exactly to `(x-S/2,y-S/2,t)`, writes a temporary release-schema certificate, and invokes both released checkers. No decimal tolerance, approximate coordinate conversion or optimization is involved. The [original polygon receipt](receipts/daniel-n68-polygon.json) and [retained five-case support implementation's receipt](receipts/daniel-support-check.json) each cover all 2,278 pairs; that latter checker is reused, not newly authored. The command above additionally exercises the n68 release's own support implementation on Daniel's converted certificate. The checkers share Python Fraction arithmetic, the half-angle map and separating-axis theorem.

The exact improvement is `8798795237260591647898096977212073675963/100000000000000000000000000000000000000000000000000000000000`. The full side, not its coarser upward-rounded shorthand, is the requested bound. The rational witness proves feasibility; the enclosed contact-system root has not been certified against every packing inequality. Restricted analytic lower bounds do not change the unrestricted lower-bound column.

Seth Rehwaldt's refinement work was assisted by OpenAI Codex. Francisco Couzo's earlier tighter contact branch, Jake Loyd and the documented earlier contributors retain their credit. No new arrangement, worldwide priority or human peer review is claimed. David's earlier issue #2 still has no public side or coordinates; comparison and priority remain unresolved. All conclusions are limited to the pinned public sources and issues retrieved on 7 October 2026.
