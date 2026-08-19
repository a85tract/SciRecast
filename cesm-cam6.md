---
title: CESM · CAM6 → GPU
nav_order: 4
---

The second pipeline: port CAM6's physics kernels to Python/JAX and Numba on GPUs, validated scheme by scheme against native CESM output.

## Pipeline 2 — CAM6 → Python/JAX + GPU

Ports the CAM6 physics parameterizations from Fortran to Python, accelerating the
computational kernels on NVIDIA GPUs via JAX and Numba (`@njit` / `@cuda.jit`), validated
scheme-by-scheme against native CESM/CAM output.

### Progress Dashboard

| Scheme | JAX | Numba CPU | Numba CUDA | CESM Validated | Overall |
|--------|-----|-----------|------------|----------------|---------|
| ZM (Deep Convection) | v3 DONE | DONE 280-300x | DONE 13.5x | 30yr 720/720 rc=0 | **95%** |
| MG (Microphysics) | DONE 1yr | DONE 38-340x | DONE | 3yr 72/72 rc=0 | **90%** |
| Kessler (Warm Rain) | DONE 1.4e-14 | standalone | via JAX GPU | HS94/TJ2016 pass | **100%** |
| CLUBB (Turbulence) | E2E done | Phase 3 | 10/12 fields | 30d bias unresolved | **45%** |
| Radiation (RTE only) | RTE solver written | - | - | Smoke + partial Fortran ref; **missing gas/cloud optics; CAM6 uses RRTMG, cannot deploy directly** | **20%** |
| Hack Shallow | Smoke pass | - | - | synthetic data passes; **CAM-SIMA CAM4 init crash blocks end-to-end validation** | **15%** |
| Held-Suarez | VERIFIED | - | - | 6-member ne16 500 steps, 1.24e-6 rel diff, **1.31x speedup** | **100%** |
| TJ2016 | VERIFIED | - | - | 6-member, 7.52e-3 rel diff (within ensemble spread) | **100%** |

**Cumulative bugs found and fixed**: 53+ (ZM 25, MG 15+, CLUBB 13)

### Kernels (submodules)

**[JaxCAM6/](https://github.com/a85tract/CESM-jax-kernels)** → `CESM-jax-kernels`
All JAX kernel implementations, organized by physics scheme.
- Schemes: ZM, MG, Kessler, CLUBB, Radiation, Shallow, HS94, TJ2016
- Sizes and test-file counts: see the generated inventory above.

**[NumbaCAM6/](https://github.com/a85tract/CESM-numba-kernels)** → `CESM-numba-kernels`
All Numba (`@njit` + `@cuda.jit`) kernel implementations.
- Schemes: ZM, MG, CLUBB (+Option C), Kessler; plus the Option C C/PTX launcher
- Sizes and test-file counts: see the generated inventory above.

### Bridge & Agent Tooling (related repos — not linked here as submodules)

**[CESM-pyphys-bridge](https://github.com/a85tract/CESM-pyphys-bridge)**
Fortran-Python bridge runtime, per-scheme adapters, CESM SourceMods, and deployment scripts.
- Architecture: Fortran -> C bridge (CPython embed) -> Python runtime -> kernel
- Supports JAX, Numba njit, Numba CUDA backends via env var switches

**[CESM-Agent-Produced-Scripts](https://github.com/a85tract/CESM-Agent-Produced-Scripts)**
Agent-produced scripts supporting the modernization workflow (extraction, wiring,
validation harnesses).

### Analysis Tools (local `/glade` dirs on Derecho — NOT linked repos)

- **cpg/** (`/glade/u/home/dai/cpg`) — Code Property Graph analysis. LLVM IR -> CFG/DFG,
  296K nodes / 1.56M edges. 847 GPU candidate functions identified. 43 tools, ~10K lines.
- **ast-comparison/** (`/glade/u/home/dai/ast_comparison`) — Fortran AST structural
  comparison tool (proc_isomorph). 9 modules, ~3K lines.
- **gpu-performance/** (`/glade/u/home/dai/GPU_PERFORMANCE`) — A100 benchmark harness, MPS
  multi-GPU config, performance profiling. ~2K lines.
- **bug-audit/** (`/glade/u/home/dai/safe-ose`) — Bug case files and audit reports
  (13 cases + CLUBB JAX 22-bug audit).

### CESM Deployment Quick Reference

| Configuration | Env Vars | SourceMods Needed |
|--------------|----------|-------------------|
| ZM Numba CPU | `USE_NUMBA_GPU_RUNTIME=1` | physpkg, zm_conv_intr, zm_convr_numba_mod, zm_numba_batch_mod |
| ZM Numba CUDA | `USE_NUMBA_CUDA=1` | same + jax_gpu_control |
| MG Numba | `USE_NUMBA_GPU_RUNTIME=1` | + micro_mg2_pyphys_mod |
| CLUBB Option C | `CLUBB_GPU_REPLACE=1` | clubb_intr + linked .so |
| CLUBB JAX | `CLUBB_JAX=1` | clubb_intr + clubb_jax_mod |

### Validated Run Archive (on scratch)

| Run | Path | Duration | Status |
|-----|------|----------|--------|
| ZM Numba 3yr | `fhist_f19_numba_test/` | 72/72 seg | PASS |
| ZM Numba 30yr (AOD fix) | scratch | 720/720 seg | Eng PASS |
| ZM Plan A 30yr | scratch | 720/720 seg | B-vs-D pending |
| MG CUDA 3yr | `fhist_f19_mg_cuda_3yr_h0/` | 72/72 seg | PASS |
| CLUBB GPU 30yr | `fhist_f10_numba_test_gpu_30yr_h0/` | 29.6yr | Env var trap |
| Ensemble v3 | `ensemble_v3/` | 11-case 2x5 | Complete |

### Active Work Items (as of 2026-06-29)

1. **ZM Plan A B-vs-D analysis** — 30yr chain completed 06-28, analysis script submitted (PBS 6590501)
2. **CLUBB JAX 22-bug fix** — `rrtthl` sub-plume correlation error is likely root cause of 3x TGCLDLWP
3. **CLUBB Numba buffer chain** — 11-launch chain intermediate buffers not threaded through
4. **MG SourceMods extraction** — `micro_mg2_pyphys_mod.F90` not yet copied to pyphys-bridge/sourcemods/mg/

---
