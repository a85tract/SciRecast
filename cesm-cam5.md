---
title: CESM · CAM5 → Python
nav_order: 3
---

The first pipeline: rewrite CAM5's physics into Python and decouple it, keeping bit-for-bit agreement with the native Fortran.

## Pipeline 1 — CAM5 → Python + Decoupling

Rewrites the CAM5 physics into Python while **decoupling** the tightly-woven Fortran into
modular, reusable components. The native Fortran path remains the reference; the Python
(Codon-compiled) path is selected at runtime and must stay bit-for-bit (BFB) with it.

### [PyCAM5/](https://github.com/a85tract/PyCAM5) → `PyCAM5` (product)
Python (Codon-compiled) port of CAM5 inside the isotope-enabled iCESM1.3/iHESP CAM
component. Runtime `*_IMPL` selectors pick native Fortran vs Codon per entry point; the
goal is BFB output against a pristine native baseline.
- Selector and Codon-module counts: see the generated inventory above.
- PI (pre-industrial) & MCO (Miocene) 6-month all-Codon runs compare
  `overall_numeric_equal=True` against matching native baselines (validation snapshot
  2026-06-16).

### [freeCAM/](https://github.com/a85tract/freeCAM) → `freeCAM` (product)
Python-owned CAM runtime: Python owns the model control path, clock, MPI-aware state,
coupling boundaries, and phase ordering, while the original Fortran supplies the numerics
through generated `bind(C)` adapters. Where PyCAM5 replaces the Fortran with Codon, freeCAM
keeps the original machine code and takes the **control path** instead — the decoupling goal
approached from the other end.
- Primary target: the CAM component of Feng Zhu's iCESM1.3.1 PI-atm case, replayed CAM-only
  against captured `x2a`/`a2x` boundaries; 134 active state fields in a Python `StatePool`.
- Decomposable devices: CCPP schemes and leaf kernels are compiled into separate device
  libraries and called individually (`cam.physics.dadadj.run()`, `cam.phases.cam_run3.run()`).
- Also retains a CAM-SIMA reference runtime whose gate covers 7 pinned suites at
  `ne3np4.pg3`, 24 ranks, 50 steps, BFB against an independent CAM-SIMA executable oracle.

### [PyCCPP/](https://github.com/a85tract/PyCCPP) → `PyCCPP` (product)
Python version of the Common Community Physics Package (CCPP), easing integration of
physics packages developed across NOAA, DOE, NASA, and the U.S. Air Force. Intended to
support the CAM5 decoupling goal by giving CAM5 physics a modular, framework-based
interface — **not yet integrated into the pipeline** (early stage).

---
