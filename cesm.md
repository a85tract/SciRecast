---
title: CESM Case
nav_order: 3
---

# CESM/CAM Modernization

SciRecast's first case: rewriting CESM/CAM's physics, with the native Fortran
kept as the reference and every artifact gated against it. Two pipelines, one
shared validation layer.

| | Read on |
|---|---|
| PyCAM5, freeCAM, PyCCPP — the CAM5 → Python pipeline | [CAM5 → Python](cesm-cam5) |
| JaxCAM6, NumbaCAM6 — the CAM6 → GPU pipeline, per-scheme progress | [CAM6 → GPU](cesm-cam6) |
| CC-Test and Sec-Track — the gates both pipelines pass | [Validation & Security](cesm-validation) |

Two halves across these pages, and the difference matters when you read a
number. The **inventory** and **gate conclusions** below are generated from the
submodules themselves by
[`tools/refresh_dashboard.py`](https://github.com/a85tract/SciRecast/blob/main/tools/refresh_dashboard.py),
each figure beside the revision it was counted at. Everything on the three pages
linked above is **human assessment** and carries its own date.

## Component Inventory

Counts and revisions below are taken from the checked-out submodules by
[`tools/refresh_dashboard.py`](tools/refresh_dashboard.py), not typed in. Each number sits
beside the revision it was counted at, so it can be re-derived rather than trusted.

<!-- generated:inventory -->
| Component | Pinned revision | Last commit | Counted |
|---|---|---|---|
| `PyCAM5` | `e8d6899` | 2026-08-10 | 831 runtime selectors, 55 Codon modules, 2,475 exported routines |
| `freeCAM` | `117f9ea` | 2026-08-15 | 96 Python files |
| `PyCCPP` | `d57889a` | 2026-04-23 | 1,079 Fortran files |
| `JaxCAM6` | `1b7c82b` | 2026-07-06 | 8 schemes, 12,444 kernel lines, 22 test files |
| `NumbaCAM6` | `c86638f` | 2026-07-06 | 4 schemes, 19,993 kernel lines, 62 test files |
| `CC-Test` | `49af867` | 2026-08-13 | 3 tools |

*Counted by `tools/refresh_dashboard.py` at 2026-08-19 06:14 UTC, from the submodule revisions above. Re-run it after `git submodule update --remote`; every number here is reproducible from the pinned revision beside it.*
<!-- /generated:inventory -->

### Gate conclusions

What has actually been compared against the original, and at what confidence.
These rows come from the `verification.json` files the components commit — not
progress estimates but recorded verdicts, each naming the oracle it was measured
against.

<!-- generated:gates -->
*No component has committed gate conclusions yet. A component wires this up by running the engine's gates and committing the `verification.json` they write; see [RecastEngine's examples](https://github.com/a85tract/RecastEngine/tree/main/examples).*
<!-- /generated:gates -->

**Judgements are not generated.** The per-scheme progress table, the bug tallies, the run
archive, and the work items further down are human assessments — no scan produces "CLUBB
45%" or "rrtthl is likely the root cause". They are maintained by hand and carry their own
date: **as of 2026-06-29** (layout last updated 2026-07-17). Treat that date as part of the
claim; a judgement older than the work it describes is a lead, not a result, and each
component repository is authoritative for its own state.



## Two Modernization Pipelines

| | **Pipeline 1** | **Pipeline 2** |
|---|---|---|
| Target model | **CAM5** | **CAM6** |
| Approach | Rewrite to Python + **decoupling** (modularize physics; Codon-compiled) | Rewrite to **Python/JAX + Numba, GPU-accelerated** |
| Primary goal | Modular, reusable Python CAM5 that stays **bit-for-bit** with native Fortran | GPU-accelerated physics kernels validated against native Fortran |
| Core artifacts | `PyCAM5`, `freeCAM`, `PyCCPP` | `JaxCAM6`, `NumbaCAM6` (+ `pyphys-bridge`) |
| Status metric | Runtime selector coverage + long-run BFB evidence | Per-scheme progress dashboard (8 schemes) |

Shared across both pipelines: **Validation & Security** infrastructure (`CESM-CC-Test`,
`CESM-Sec-Track`). Linked sub-projects are git submodules — run
`git submodule update --init --recursive` to populate them.

`CESM-Sec-Track` is **not** among them. It is linked but never vendored, because it
holds unpatched vulnerabilities and a submodule of a public repository has to be
publicly cloneable to be useful. See [Sec-Track](#sec-track--cesm-sec-track-restricted).

---

## Repository Layout

```
cesm-modernization-overview/   <- You are here (master tracker)

  # ── Pipeline 1: CAM5 → Python + decoupling (submodules) ──
  PyCAM5/           -> PyCAM5                     Python/Codon CAM5 port (BFB validated)
  freeCAM/          -> freeCAM                    Python-owned CAM control path + decomposable devices
  PyCCPP/           -> PyCCPP                     Python Common Community Physics Package

  # ── Pipeline 2: CAM6 → Python/JAX + GPU (submodules) ──
  JaxCAM6/          -> CESM-jax-kernels           JAX kernel implementations
  NumbaCAM6/        -> CESM-numba-kernels         Numba CPU+GPU kernels

  # ── Shared: validation & security (submodules) ──
  CC-Test/          -> CESM-CC-Test              CC-Test: CI/CD validation workflow (Cyber now, Correctness later)

  # ── Related repos (NOT linked here as submodules) ──
                       CESM-Sec-Track              Sec-Track: N-day/0-day vuln repo (restricted access)
                       CESM-pyphys-bridge          Fortran-Python bridge + CESM adapters
                       CESM-Agent-Produced-Scripts Agent-produced modernization scripts

  # ── Pipeline 2 analysis tools (local /glade dirs on Derecho, NOT linked repos) ──
  cpg/              -> /glade/u/home/dai/cpg              Code Property Graph analysis
  ast-comparison/   -> /glade/u/home/dai/ast_comparison  Fortran AST comparison tool
  gpu-performance/  -> /glade/u/home/dai/GPU_PERFORMANCE A100 benchmarks + MPS config
  bug-audit/        -> /glade/u/home/dai/safe-ose        Bug case files and audit reports
```
