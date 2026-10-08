# Limited public comparison, 7 October 2026 Chicago / 8 October UTC

Successful GitHub API reads during publication are pinned in [SOURCE_MANIFEST.json](sources/SOURCE_MANIFEST.json), with retrieval times, file sizes, SHA256 hashes and immutable source commits. The register head was `84881f214086bf5b8ce83a714c4fda6d7be7b2d1`; Evan Daniel's head was `6069054020e1c78a395aa90a689332b4a1e6e2cd`. Earlier comparison statements in preserved files describe their own dates.

| Inspected source | Observation at retrieval |
| --- | --- |
| [Register n=68 case](https://github.com/jlevy/squares/blob/84881f214086bf5b8ce83a714c4fda6d7be7b2d1/packing/frontier/n-068.md) | Both upper lanes retain Daniel's rational `4399397618609141951332334459697/500000000000000000000000000000`, exactly `8.798795237218283902664668919394`. The unrestricted lower bound remains `851/100`; this publication requests no change to it. |
| [Daniel's current n68 certificate](https://github.com/evand/square-packing/blob/6069054020e1c78a395aa90a689332b4a1e6e2cd/search/exact/batch/certs/n-68.cert) | SHA256 `871fb854b07417fa2178c14e933f5c1ccf8f35d8280b93394b2109aebc8b2c68`, byte-identical to the certificate previously replayed in this repository's dated rational comparison. |
| [Daniel's exact-form table](https://github.com/evand/square-packing/blob/6069054020e1c78a395aa90a689332b4a1e6e2cd/search/exact/EXACT_FORMS.md) and [submission #419](https://github.com/jlevy/squares/issues/419) | n=68 remains open after a timeout. Table SHA256 `bb07621b47e16229d74d9b3087d9a2a4d49876843f426929fac0ce5cfa5b04b7`. His deliverable is a univariate minimal polynomial, isolating interval and configuration over a number field. Our multivariate system/box feasibility result is a different representation and does not complete that format. |
| [#375](https://github.com/jlevy/squares/issues/375), [#399](https://github.com/jlevy/squares/issues/399), [#420](https://github.com/jlevy/squares/issues/420), [#422](https://github.com/jlevy/squares/issues/422), including available comments | Daniel's rational work and related pending submissions were inspected. The newer construction updates concern other counts. The local-minimum submission does not supply an n=68 result. No smaller comparable n=68 certificate was identified in these reads. |
| [Existing #428](https://github.com/jlevy/squares/issues/428) and [Davidebyzero #4](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/4) | Before this update, both were open: #428 had no comments; #4 had the earlier v1.1.0 comment. Neither had accepted this root-feasibility result. |
| [Earlier Davidebyzero #2](https://github.com/Davidebyzero/packing_squares_in_squares__tools/issues/2) | The fresh issue read still contains no public side or coordinates; there were no comments. There is no new comparable evidence, and no priority inference can be drawn. |

The exact rational improvement (Daniel minus preserved v1.1.0) is

```text
8798795237260591647898096977212073675963 /
100000000000000000000000000000000000000000000000000000000000
```

It is approximately `8.79879523726059e-20`; the newly feasible L\* is additionally about `4.58039e-61` smaller. The publication launcher recomputes these exact comparisons and proves the root-side enclosure lies below the preserved rational side. The coarse display `8.798795237218283903` is larger than Daniel's bound and must not replace the exact specification as an improving ceiling.

These are dated observations of the inspected sources, not an exhaustive worldwide survey, priority determination or claim of a new arrangement. Some retrieval routes failed; ordinary GitHub CLI/API reads succeeded and were pinned. No denied escalation was retried. The mathematical theorem is unaffected by comparison coverage. Review and registration of this submission remain pending.

Source attribution: register material is credited to Joshua Levy and the squares project (CC BY 4.0, as documented by the register and the prior submission). Daniel's source license is retained in [daniel-LICENSE.txt](sources/daniel-LICENSE.txt). These snapshots preserve evidence and its provenance; they are not newly authored proof inputs.
