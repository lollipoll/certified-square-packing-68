# A certified refinement of the 68-unit-square packing

## Latest result: v1.2.0 — exact algebraic root feasibility

**Update, 7 October 2026 (America/Chicago; 8 October UTC): s(68) ≤ L\*.** The previously missing all-pairs feasibility obligation for the enclosed algebraic root is now proved. L\* is coordinate 136 (zero-based) of the unique zero of the specified 153-equation rational polynomial system in its original radius-10⁻¹⁰⁰ box. Its approximate decimal begins `8.798795237218283902576680967021394083521019030227879263240369541961...`; the system and box, identified by hashes in the [theorem note](proofs/2026-10-07-root-feasibility/README.md), define it exactly.

The [new supplementary release](https://github.com/lollipoll/certified-square-packing-68/releases/tag/v1.2.0) preserves v1.1.0 and supplies the unchanged proof archive, computational review, fresh support-function check and receipts. It proves all 68 unit frames, containment and all 2,278 pairs: 255 exact-zero and 9,945 strictly positive predicates, all 437 implied equations, and 20 rejection controls. The root side is approximately 4.58039 × 10⁻⁶¹ below the unchanged rational certificate.

One command from this repository, using the Python standard library with assertions enabled:

```sh
python3 -B proofs/2026-10-07-root-feasibility/reproduce.py
```

Attainment is also established within the earlier fully restricted contact family; every restriction and the same-root binding are stated in the theorem note. There is no unrestricted local/global optimality claim or lower-bound update. These computational checks are not independent human peer review or proof-assistant formalization. Seth Rehwaldt's work used OpenAI Codex assistance; Francisco Couzo's earlier tighter branch, Jake Loyd and the preceding contributors retain their credit. Evan Daniel's related algebraic work is acknowledged; this multivariate specification does not supply his minimal-polynomial format. No new arrangement or worldwide priority is claimed. Review remains pending on [#428](https://github.com/jlevy/squares/issues/428) and [#4](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/4).

## Preserved rational refinement: v1.1.0

An updated certificate proves **s(68) ≤ 8.798795237218283902576680967021394083521019030227879263240370** (the full exact terminating decimal). It improves the v1.0.0 side by approximately 2.716097423319033 × 10⁻¹². See the [certificate and verification instructions](refinement-v1.1.0/README.md) and [v1.1.0 release](https://github.com/lollipoll/certified-square-packing-68/releases/tag/v1.1.0).

**Registration requested, 7 October 2026:** [jlevy/squares issue #428](https://github.com/jlevy/squares/issues/428). The [dated exact comparison and fresh replay receipts](publication/20261007/README.md) show an improvement of exactly `8798795237260591647898096977212073675963/100000000000000000000000000000000000000000000000000000000000` (about `8.79879523726059e-20`) over Daniel's smallest verified retrieved n68 certificate. The shorter upward-rounded display `8.798795237218283903` is larger than Daniel's bound and is not the improving ceiling requested. Review is pending; no register acceptance is claimed. The [existing submission to David Ellsworth](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/4) remains linked, and the priority/comparison caveat for [earlier issue #2](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/2) remains unresolved.

This is a certified refinement of the existing packing family. The tighter contact branch is present in Francisco Couzo's earlier public coordinates; the starting construction and earlier contributors retain their attribution. Unrestricted local and global optimality remain unproved. Material below describes the earlier v1.0.0 certificate unless otherwise labeled.

This repository gives an exact construction of 68 nonoverlapping unit squares
inside a square of side

**8.798795237221 = 8798795237221 / 1000000000000.**

Every center and rotation parameter is rational. Two separately implemented
Python checkers verify containment and all **2,278 unordered pairs** using exact
fraction arithmetic and zero acceptance tolerance. Both return `valid: true`.

![The certified 68-square packing](n68.svg)

The drawing is an approximate rendering. The authoritative geometry is
[n68.json](n68.json), whose SHA-256 is
`00e402139c76663a4bac8dbaed8705d1b8a04ccfd32f2945065f70ade5d6eb19`.

## Reproduce the verification

Use Python 3.9 or newer with its standard library; no optimizer, network access, or
third-party packages are needed. From this repository's directory:

```bash
python3 check_hashes.py
python3 verify.py n68.json --n 68
python3 independent_support_check.py n68.json --n 68
python3 -m unittest discover -s . -p 'test_*.py' -v
```

The final command runs 25 tests, including deliberate overlaps and wall
protrusions of size `1e-30`, boundary contacts, rational rotations, and a pair
that requires a separating direction from the second square.

## Comparison and scope

The following comparison was checked on **2026-10-07**. Smaller sides are better.

| Construction / claim | Reported enclosing side | Difference from this certificate |
|---|---:|---:|
| This exact certificate | 8.798795237221 | 0 |
| franciscouzo's posted coordinate-file header | 8.798795237222592 | +0.000000000001592 |
| Kingbird's listed 68-square packing | 8.7987961402601 | +0.0000009030391 |

Sources:

- [Kingbird's table](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
- [franciscouzo's n68 file, pinned to the audit's reviewed revision](https://github.com/franciscouzo/square-packing/blob/6042c56b43b64c09fe5a32c64879e698f399beaf/n68.txt)
- [Earlier pending n68 submission by dorfuchs93](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/2)

The certified side is smaller than the two stated numerical values. The earlier
pending submission supplies no side or coordinates in its public issue, so it
cannot be compared. Record recognition and historical priority remain unresolved.
The comparison does not establish a global minimum, a novel packing arrangement,
or superiority to every unpublished or unindexed construction.

## Attribution and provenance

Refinement and certification: Seth Rehwaldt, assisted by Codex.

The supplied provenance identifies
[Jake Loyd's September 19, 2026 packing](https://kingbird.myphotos.cc/packing/square-68.svg)
as the starting construction. The earlier contributors and construction history
are credited in the linked Kingbird page and SVG. This contribution is a
refinement of that published construction.

The supplied method used constrained numerical optimization and finite seeded
perturbations, followed by rational repair before export. This small publication
package reproduces the final certificate verification. Reproducing the complete
search requires the original search project and its inputs.

The original `independent-audit.zip` can be attached unchanged to a GitHub release
as supporting material. Its full-workflow replay additionally requires a separate
`candidate-export.zip`, which was not included in the supplied audit ZIP. The
standalone certificate checks above do not require that original archive.

See [VERIFICATION.md](VERIFICATION.md) for exact margins and review details.
