---
title: CESM Case
nav_order: 3
---

# CESM Modernization

**SciRecast's first case.**

Two pipelines, one shared validation layer. Every component below is its own repository.

## Two modernization pipelines

<!-- HTML rather than a markdown table: the shared row has to span both
     pipeline columns, and kramdown's tables have no colspan. -->
<table class="compare">
  <thead>
    <tr><th></th><th>Pipeline 1</th><th>Pipeline 2</th></tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Target model</th>
      <td><strong>CAM5</strong></td>
      <td><strong>CAM6</strong></td>
    </tr>
    <tr>
      <th scope="row">Approach</th>
      <td>Rewrite to Python + <strong>decoupling</strong> (modularize physics; Codon-compiled)</td>
      <td>Rewrite to <strong>Python/JAX + Numba, GPU-accelerated</strong></td>
    </tr>
    <tr>
      <th scope="row">Primary goal</th>
      <td>Modular, reusable Python CAM5 that stays <strong>bit-for-bit</strong> with native Fortran</td>
      <td>GPU-accelerated physics kernels validated against native Fortran</td>
    </tr>
    <tr>
      <th scope="row">Core artifacts</th>
      <td><a href="#pycam5"><code>PyCAM5</code></a>,
          <a href="#freecam"><code>freeCAM</code></a></td>
      <td><a href="#jaxcam6"><code>JaxCAM6</code></a>,
          <a href="#numbacam6"><code>NumbaCAM6</code></a></td>
    </tr>
    <tr>
      <th scope="row">Status metric</th>
      <td>Runtime selector coverage + long-run BFB evidence</td>
      <td>Per-scheme progress against native CESM output (8 schemes)</td>
    </tr>
    <tr>
      <th scope="row">Validation &amp; Security</th>
      <td colspan="2"><a href="#cc-test"><code>CC-Test</code></a>,
          <a href="#sec-track"><code>Sec-Track</code></a> (restricted)</td>
    </tr>
  </tbody>
</table>

## Pipeline 1 — CAM5 → Python + decoupling

Rewrites the CAM5 physics into Python while **decoupling** the tightly-woven Fortran into
modular, reusable components. The native Fortran path remains the reference; the Python
(Codon-compiled) path is selected at runtime and must stay bit-for-bit (BFB) with it.

### [PyCAM5](https://github.com/a85tract/PyCAM5)
Python (Codon-compiled) port of CAM5 inside the isotope-enabled iCESM1.3/iHESP CAM
component. Runtime `*_IMPL` selectors pick native Fortran vs Codon per entry point; the
goal is BFB output against a pristine native baseline.

### [freeCAM](https://github.com/a85tract/freeCAM)
Python-owned CAM runtime: Python owns the model control path, clock, MPI-aware state,
coupling boundaries, and phase ordering, while the original Fortran supplies the numerics
through generated `bind(C)` adapters. Where PyCAM5 replaces the Fortran with Codon, freeCAM
keeps the original machine code and takes the **control path** instead — the decoupling goal
approached from the other end.

## Pipeline 2 — CAM6 → Python/JAX + GPU

Ports the CAM6 physics parameterizations from Fortran to Python, accelerating the
computational kernels on NVIDIA GPUs via JAX and Numba (`@njit` / `@cuda.jit`), validated
scheme-by-scheme against native CESM output.

### [JaxCAM6](https://github.com/a85tract/CESM-jax-kernels)
All JAX kernel implementations, organized by physics scheme: ZM, MG, Kessler, CLUBB,
Radiation, Shallow, HS94 and TJ2016.

### [NumbaCAM6](https://github.com/a85tract/CESM-numba-kernels)
All Numba (`@njit` + `@cuda.jit`) kernel implementations: ZM, MG, CLUBB (+Option C) and
Kessler, plus the Option C C/PTX launcher.

## Validation & security (shared by both pipelines)

### [CC-Test](https://github.com/a85tract/CESM-CC-Test)
The CESM case's instance of SciRecast's Support Layer, built out on the Cyber side today:
a reusable local + CI DevSecOps gate for the modernization repos. It runs the same checks
before a `git push` that the cloud CI runs on every PR — secret scan, SBOM+CVE+VEX, AI code
audit, sanitizer builds — reusing each target repo's own config so local and cloud never
drift.

### [Sec-Track](https://github.com/a85tract/CESM-Sec-Track)
The CESM case's vulnerability record: N-day and responsibly disclosed 0-day findings spanning
the modernized software, its supply-chain dependencies, and the runtime environment. Access
is granted per person, both to reduce the risk of malicious exploitation and because a
figure nobody outside can re-derive would be a claim rather than evidence — so it is listed
here by name and never as a number.

### Analysis tools
Code Property Graph analysis, Fortran AST comparison, A100 benchmarking, and bug case
files, kept under `/glade/u/home/dai/` on Derecho. They are working directories rather
than repositories, so nothing here links or counts them.
