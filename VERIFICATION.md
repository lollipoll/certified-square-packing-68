# Verification review — 2026-10-07

Review runtime: Python 3.12.14.

The supplied `independent-audit.zip` was extracted into a separate directory.
The supplied ZIP and its audit files were not modified. Its SHA-256 is
`4edf42a7ad5f1f17363fc728c6e08cd7614d4cc1dd74b6515bf5c25b7d07215b`.

All **154** entries in the audit's hash manifest matched. All **16** original
verifier tests passed when rerun. The supplied exact verifier accepted all three
final certificates, checking 2,278, 5,253, and 5,460 pairs for n=68, 103, and 105
respectively: **12,991 pairs** in total.

A second checker was implemented for this review without importing the supplied
verifier. It uses center differences and exact projection half-widths rather than
constructing polygon vertices and projecting them. It also accepted all three
certificates at zero tolerance, with matching minimum margins. Its nine
regression tests and the original sixteen tests pass: **25 tests** in this
publication package.

For each n, the certificate's side, centers, and rotation parameters exactly
match the corresponding exported input inside the audit bundle. Those input
files also match the source SHA-256 values recorded in certificate provenance.
The separate original `candidate-export.zip` was absent, so the report's
full-workflow reproduction requiring that archive was not replayed in this review.

## Exact n=68 result

- Certificate SHA-256:
  `00e402139c76663a4bac8dbaed8705d1b8a04ccfd32f2945065f70ade5d6eb19`
- Enclosing side: `8798795237221/1000000000000`, exactly `8.798795237221`.
- Number of unit squares: 68.
- All 2,278 unordered pairs have nonoverlapping interiors.
- All squares lie inside the closed enclosing square.
- Minimum wall clearance:
  `94528211535083/1873109104598046000000000000`
  (approximately `5.046593991937698e-14`).
- Minimum pair separating margin:
  `2648882995461292/129668570340299116873757826843`
  (approximately `2.042810365310288e-14`).
- Both minima are strictly positive exact rational numbers.

The unchanged output of the supplied checker is in `supplied-check.json`.
The separately implemented checker's output is in `independent-check.json`.

## Why the arithmetic certifies the geometry

For a rational parameter t, define

```text
c = (1 - t*t) / (1 + t*t)
s = 2*t / (1 + t*t)
u = (c, s)
v = (-s, c)
```

Then `u.u = v.v = 1` and `u.v = 0` exactly. Center `(x,y)` with vertices
`(x,y) + (a*u + b*v)/2`, for a,b in {-1,+1}, defines a true unit square.
Containment follows from its exact coordinate projection bounds.

On an axis A, its projection half-width is
`(|u.A| + |v.A|)/2`. A pair separates on that axis if the absolute projected
center difference is at least the sum of the two half-widths. The separating
axis theorem for convex polygons reduces the search to edge normals of both
polygons. For squares these are their edge directions up to sign, so checking
u and v from each square suffices. The supplied checker instead computes
vertex projection endpoints on those axes. Both methods use exact rational
arithmetic for every geometric comparison.

These computations establish a feasible upper bound. They do not establish
global optimality or discovery priority. Both checkers were developed with AI
assistance; “separately implemented” refers to the code and formulation, not to
independent human peer review.

The n=103 and n=105 certificates are valid but have larger sides than the earlier
franciscouzo claims recorded in the audit. This publication package therefore
focuses on n=68.
