# Certified refinement for 68 unit squares — v1.1.0

This certificate proves the feasible upper bound

**s(68) ≤ 8.798795237218283902576680967021394083521019030227879263240370**

The displayed number is the exact terminating decimal in the certificate. A shorter upward-rounded bound is **s(68) ≤ 8.798795237218283903**.

The improvement over v1.0.0's exact side 8.798795237221 is approximately **2.716097423319033 × 10⁻¹²**.

## Attribution and status

The refinement and certificate were prepared by **Seth Rehwaldt with assistance from OpenAI Codex**. This is a refinement of the existing n=68 packing family. The earlier construction and its development are credited in the [Kingbird table](https://kingbird.myphotos.cc/packing/squares_in_squares.html), including Jake Loyd's September 2026 improvement.

The source comparison identifies the tighter contact branch in **Francisco Couzo's earlier public coordinates** ([franciscouzo](https://github.com/franciscouzo/square-packing/blob/3bfc47e4f53ab474cd7702cb81f831faf2f5846a/n68.txt)). That contribution should retain its attribution. Our work supplies a tighter exact feasible certificate and an enclosed algebraic contact system for this branch. Discovery priority for a new arrangement is not claimed. Table acceptance and priority relative to other submissions remain for the maintainer to assess.

## Exact verification

Use normal Python 3.9 or newer, without `-O` or `-OO`. The checks use the Python standard library and require no optimizer, network access, or third-party packages. Python 3.12 was used for this review.

Run these commands from this directory:

```bash
python3 check_hashes.py
python3 -B verify.py n68.json --n 68 --reference-side 8.798795237221
python3 -B independent_support_check.py n68.json --n 68
python3 -B verify_analytic.py
```

The two direct geometry commands must report `valid_exact: true` and `valid: true`, respectively, and `pairs_checked: 2278`. Both use exact fractions and zero acceptance tolerance. The analytic launcher checks the root, elimination, restricted bounds, and seven supplied verifier tests in a temporary directory. It preserves the delivered files.

An additional supplied geometry implementation was replayed during review; its result is in `review-evidence/geometry_independent_check.json`. All three geometry implementations passed. The independently written support checker also accepted exact touching and rejected overlap and wall protrusion of size 10⁻¹⁰⁰.

The authoritative certificate is `n68.json`, SHA-256:

```text
6d4f72debae83b5825e91f7b090e0cee08851ad7b85400343c0dee52f468dff9
```

Squares have rational centers and rational half-angle parameters t. Reconstruct directions as c=(1−t²)/(1+t²), sinθ=2t/(1+t²). These formulas make the side length exactly one. All 68 squares are contained and all 2,278 unordered pairs have nonoverlapping interiors. Minimum wall clearance is about 2.29019 × 10⁻⁶¹; minimum separating margin is about 9.999999999 × 10⁻⁷¹. Their tiny size is handled by exact arithmetic.

## Scope of the analytic results

An exact contraction argument encloses a unique root of the selected, gauge-fixed quadratic contact system in a box of radius 10⁻¹⁰⁰. All 437 descriptive polynomials were reconstructed coefficient by coefficient in this review and the 153 selected equations checked against that reconstruction.

The certificate side is approximately 4.58039 × 10⁻⁶¹ above the enclosed contact-system side. The rational certificate supplies the proven packing bound; the algebraic contact root is not itself presented as an independently certified all-pairs packing.

The fixed-orientation result is a lower bound for the family with those orientations and the chosen pair separators. It is within about 4.58039 × 10⁻⁶¹ of the certificate. The eight-angle result is a local lower bound within the explicitly constrained contact relaxation, with orientation groups, held contacts, and coordinate gauges. Neither proves unrestricted variable-angle local optimality or global optimality.

See `REVIEW.md`, `ANALYTIC_DERIVATION.txt`, and the exact witnesses under `campaign/results/`. The separate `n68-refinement-campaign-20261007.tar.gz` release asset preserves the original complete optimization campaign and report. The small verification ZIP is self-contained for the exact claims; it does not require the original project's baseline files or a separate candidate-export ZIP.

`n68.svg` and `load_bearing.svg` are approximate illustrations. The rational coordinates in `n68.json` define the construction.
