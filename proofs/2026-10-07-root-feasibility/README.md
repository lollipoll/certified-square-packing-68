# Exact algebraic n=68 packing: certified root feasibility

Publication update: **7 October 2026, America/Chicago (8 October UTC)**.
Seth Rehwaldt, with OpenAI Codex assistance.

**Theorem: s(68) ≤ L\*.** The previously missing exact-root feasibility obligation is now proved: the enclosed root defines 68 unit squares, contained in its square container, with pairwise disjoint interiors. Boundary contact is allowed.

Let F = (F₀,…,F₁₅₂) be the ordered rational polynomials in [system.json](reviewed/2026-10-07-root-feasibility/released/campaign/results/reduced/system.json). Let z\* be their unique zero in the closed infinity-norm box centered at the rational vector `center` in [root_witness.json](reviewed/2026-10-07-root-feasibility/released/campaign/results/reduced/root_witness.json), with its original radius **10⁻¹⁰⁰**. Define **L\* = z\*₁₃₆**, using zero-based coordinates. These files define the number exactly:

| File | SHA256 |
| --- | --- |
| `system.json` | `0bc2c2deea9f63d4ed1a3473ed50f71327ce33676bfd7ee1f43c371d13e481de` |
| `root_witness.json` | `fa234967c8496538ee67614a7d8b68c58022f34bcc698b48eda00eb7282fe824` |

The nonsingular isolated root is algebraic. Its side has the **approximate** decimal expansion

```text
8.798795237218283902576680967021394083521019030227879263240369541961...
```

The displayed prefix is not an exact rational upper bound. The unchanged v1.1.0 rational-coordinate witness has exact side `8.798795237218283902576680967021394083521019030227879263240370`; it exceeds L\* by approximately **4.58038746818 × 10⁻⁶¹**. The launcher recomputes the exact rational interval `[center[136] − 10^-100, center[136] + 10^-100]` and the difference interval in its `binding.json` receipt. Its upper endpoint is a rational upper bound on the root side; it is distinct from the side of the rational-coordinate witness.

## Proof and reproduction

The unchanged [PROOF.txt](reviewed/2026-10-07-root-feasibility/PROOF.txt) specifies every center, orientation, square and predicate. Its exact contraction proof gives the unique root in the original box. The [construction ledger](reviewed/2026-10-07-root-feasibility/construction.json), [certificate](reviewed/2026-10-07-root-feasibility/certificate.json) and [readable coverage](reviewed/2026-10-07-root-feasibility/coverage.tsv) supply the complete geometry.

From the repository root at v1.2.0, one offline command runs the proof, supplementary support check, and root/family binding:

```sh
python3 -B proofs/2026-10-07-root-feasibility/reproduce.py
```

For the supplementary release archive, extract it and run:

```sh
python3 -B 2026-10-07-root-feasibility/reproduce.py
```

Use ordinary Python 3.9+ with assertions enabled (no `-O` or `-OO`); the publication replay used Python 3.12.3. Only the standard library is needed, with no network, optimizer, or third-party packages. Fresh receipts go to a new `/tmp/n68-publication-replay-*` directory, printed on success. The support script runs in a temporary copy to preserve its supplied ledger. The full command checks the publication and review manifests before and after replay.

The original commands remain available inside `reviewed/`:

```sh
python3 -B 2026-10-07-root-feasibility/reproduce.py
python3 -B support_audit.py
```

The second original command writes `support-audit.json` next to itself; the publication launcher above preserves that supplied review receipt. Both original commands passed freshly before publication. Their fresh [proof receipt](receipts/fresh-replay.json) and [support ledger](receipts/fresh-support-audit.json) are retained alongside the original review's receipts.

The exact checks establish:

- All **68 unit frames**, including 204 norm/orthogonality identities; containment of every corner against every wall (**1,088 predicates**).
- All **2,278 unordered pairs**, each covered by four corner predicates beyond a supporting edge, with no pair culling (**9,112 predicates**). Convexity proves interior nonoverlap.
- **255 exact-zero predicates** (208 pair and 47 wall) and **9,945 strictly positive predicates**. Zero claims are coefficient identities, never small numerical residuals.
- All **437 proposed equations**, including the 284 unselected rows, as exact constant rational linear combinations of the 153 selected equations.
- **20 rejection controls**, as well as the seven earlier verifier tests, original root enclosure, elimination, restricted-family bound, fixed-angle bound, and both rational-certificate geometry checks.

The minimum certified positive predicate margin is exactly `16598222465128834048351 / 100000000000000000000000000000`, approximately 1.6598222465 × 10⁻⁷.

The two submitted implementations use different arithmetic paths: sparse `Fraction` polynomial intervals and coefficient identities; and direct dyadic vertex intervals with denominator-cleared integer coefficient identities. They share the selected system, root witness, supplied multipliers and released root theorem. The second implementation reuses the released polynomial/binding code, but does not import the first new geometry verifier.

The additional [computational review](reviewed/REVIEW.txt) and [support_audit.py](reviewed/support_audit.py) derive row relations afresh, read no supplied identity multipliers, import no submitted verifier or polynomial code, and select separating axes anew using center/support geometry. Its fresh calculation checks 68 frames, 437 equations, 2,278 pairs (122 touching; 2,156 strictly separated), and 272 full-square wall conditions (24 exact contacts; 248 strict). The different contact totals count full-square support conditions rather than individual vertices. This check shares the system, root witness and geometric principles, and relies on the separately replayed root theorem. All routes rely on Python and exact integer/rational arithmetic. Multiple scripts and computational review are **not independent human peer review or proof-assistant formalization**.

## Attainment in the precisely restricted contact family

The fresh [publication binding](receipts/publication-binding.json) identifies the earlier theorem's center and root witness with these same published inputs, replays its inverse-Jacobian proof, and checks that the radius-10⁻¹⁰⁰ root box lies inside its radius-10⁻¹¹ neighborhood. The root obeys all 153 equalities and is now proved feasible. Thus the earlier lower bound is **attained by a packing in that restricted family**.

Every restriction remains: **F₀,…,F₁₄₄ are held equalities** (including the selected contacts, eight unit-circle equations, and **22 coordinate gauges**); the final eight rows satisfy `sign[k] * F[145+k] ≥ 0`, with signs **[1,1,1,1,1,−1,1,1]**; the **eight shared-angle groups**, all other **fixed orientations**, gauges, and selected contact branches are those in `construction.json`; and the closed infinity-norm neighborhood has radius **10⁻¹¹ around the same rational center**. In this family L ≥ L\*, with equality forcing the same reduced-coordinate root. Intersecting with genuine packings preserves the lower bound and now contains its minimizer.

This corollary does not cover opening the held contacts, changing the gauges/orientations/groups, or choosing other separating branches. It proves neither unrestricted local nor global optimality and requests **no change to the unrestricted lower-bound column**. The sealed proof note's earlier conservative omission of attainment is preserved as historical text; this bound-and-attainment deduction is new supplementary material.

## Comparison, credit and publication history

See the [dated, limited comparison](COMPARISON.md) and its pinned sources. Daniel's retrieved rational certificate remains above the unchanged v1.1.0 rational side, hence above L\*. His exact-form table still marks n=68 open. This multivariate isolating specification does **not** complete his minimal-polynomial/number-field format; no univariate minimal polynomial was computed. Feasibility does not depend on worldwide record status.

Seth Rehwaldt's refinement, proof and publication work used OpenAI Codex assistance. Retain **Francisco Couzo's earlier tighter contact branch**, **Jake Loyd's** September 2026 contribution, and the documented preceding contributors, including the **Brendberg–Schadt–Ellsworth lineage** in the register and Kingbird history. **Evan Daniel's** exact rational certification and related algebraic work are acknowledged. Joshua Levy and the squares project maintain the register. No new arrangement or worldwide priority is claimed.

The public **v1.1.0** tag remains `fded686668e29258dad2eb29d0482fa3fd51bd6b`. All **37** files copied into the proof's `released/` folder match `refinement-v1.1.0/` at that tag byte for byte, including the system, root and elimination witnesses. The v1.1.0 rational `n68.json` SHA256 remains `6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9`. Earlier repository files and release assets are preserved; this directory and the README's dated latest-result notice are the publication additions.

The original `root-feasibility-proof-20261007.tar.gz` is unchanged: **767243 bytes**, SHA256 `c124d77e50a5dcd2b8b4e26c34bc0ae258d15dcb87cef84111eb26ea8ad8910c`. Its files match the extracted proof directory. The supplied review bundle was **1722472 bytes**, SHA256 `f3ac769a212dde944d2f3cfab21514f68b4013f8d1bcca44a7fac922c895c066`; all 77 review-manifest entries and 70 proof-manifest entries were checked. The new supplementary release archive packages this publication directory, including those preserved review files, fresh receipts, comparison snapshots and launcher. See the release for its size and SHA256.

[Release v1.2.0](https://github.com/lollipoll/certified-square-packing-68/releases/tag/v1.2.0) · [Existing register submission #428](https://github.com/jlevy/squares/issues/428) · [Existing Ellsworth submission #4](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/4). Review and registration remain pending; posting this evidence is not acceptance.
