---
title: RecastEngine
nav_order: 2
---

# RecastEngine

**The modernization engine — the reusable, domain-independent part of SciRecast.**

The engine produces nothing on its own. A product is what comes out when the
engine is combined with the domain knowledge a particular effort needs and the
source being modernized; see [Architecture](.) for why that separation is the
whole design. What the engine contributes is the spine every workload walks and
the gates nothing gets past:

```
discover  ->  analyze  ->  transform  ->  verify  ->  record
  Unit        Facts        Candidate     Verdict    Evidence
```

Four recipes, one spine, different plugins in the slots: `translate` (Fortran →
NumPy/Numba/CUDA), `refactor` (carve a Python control plane into a monolith),
`port` (retarget a kernel to an accelerator), `audit` (secret scan, SBOM+CVE+VEX,
LLM source audit, sanitizer builds).

## What is registered

Every capability arrives through an entry point, including the engine's own —
there is no privileged built-in path, which is what makes a domain package like
`recast-cesm` a first-class extension rather than a patch.

<!-- generated:plugins -->
| Kind | Registered |
|---|---|
| frontend | `fortran` |
| transform | `translate.numpy` |
| oracle | `f2py-golden` |
| verifier | `differential.bitexact`, `static.rwset`, `symbolic.notary` |
| executor | `local` |
| store | `fs-evidence`, `fs-findings` |
| recipe | `audit`, `port`, `refactor`, `translate` |

*Read from `RecastEngine`'s `pyproject.toml` at `6333399`. A domain package adds to this list by declaring the same entry-point groups -- `recast-cesm` supplies the `cesm` frontend, the `translate.cam` transform and the `translate-cam` recipe that way, with no change to the engine.*
<!-- /generated:plugins -->

## What the gates concluded, on the engine's own example

`recast run translate examples/toy_physics` walks the whole chain: translate the
module, cross-check its dataflow against the source's, compile the untouched
Fortran as the reference, compare every output bit for bit, notarize any
rewrites, write the evidence. The verdicts below are read from the summary the
example commits, so they are what a clean run concludes rather than what a
README claims.

<!-- generated:engine-verdicts -->
| Unit | Verifier | Confidence | Metrics |
|---|---|---|---|
| `fortran:toy_physics` | `static.rwset` | **sampled** | blocks_checked=4 |
| `fortran:toy_physics` | `differential.bitexact` | **bit_exact** | bit_exact=85, max_ulp=0, points=85 |
| `fortran:toy_physics` | `symbolic.notary` | **symbolic** | rewrites=0 |

*Read from the summaries committed in `RecastEngine` at `6333399`. The engine's CI regenerates them on a clean machine and fails on any difference, so a verdict here is what a fresh run concludes rather than what was true once.*
<!-- /generated:engine-verdicts -->

## Reading further

| | |
|---|---|
| [`README`](https://github.com/a85tract/RecastEngine#readme) | quick start, and a run you can reproduce |
| [`docs/architecture.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/architecture.md) | the spine, the ten interfaces, where the boundaries fall |
| [`docs/splitting-the-translator.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/splitting-the-translator.md) | how a 2,883-line translator became reusable parts, and what held it honest |
| [`docs/writing-a-plugin.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/writing-a-plugin.md) | how to extend it |
| [`docs/roadmap.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/roadmap.md) | phases P0–P6 |
| [`conformance/`](https://github.com/a85tract/RecastEngine/tree/main/conformance) | what a plugin must satisfy |
