# SciRecast

**An open-source, agentic ecosystem for modernizing legacy scientific software.**

LLM agents do the labor-intensive porting work under human oversight; every artifact ships
only after passing correctness validation and security review.

## 📊 <https://a85tract.github.io/SciRecast/>

| Tab | What is on it |
|---|---|
| [Architecture](https://a85tract.github.io/SciRecast/) | the three layers, why the boundaries fall where they do, how a case attaches |
| [RecastEngine](https://a85tract.github.io/SciRecast/engine) | the spine, what is registered, and what the engine's own gates conclude |
| [CESM Case](https://a85tract.github.io/SciRecast/cesm) | the first case: inventory, gate conclusions, and three pages of detail beneath it |
| [Contributing](https://a85tract.github.io/SciRecast/contribute) | who changes what, where to send it, how to extend the engine |

This README is the thirty-second version and links onward rather than restating. Each section
lives in exactly one page source (`index.md`, `engine.md`, `cesm.md`, …); the counted parts of
the engine and CESM pages are generated from the component repositories by
[`tools/refresh_dashboard.py`](tools/refresh_dashboard.py), so a figure there is never older
than the revision printed beside it.

<!-- generated:headline -->
**6 of 6 components counted; no gate conclusions committed yet.** See the page for the inventory, the per-scheme progress, and what each figure was measured against.
<!-- /generated:headline -->

## What is here

The pages, and the tool that fills in their counted parts. No component is checked out or
pinned here, so there is nothing to initialise — the tool clones what it needs, counts it, and
throws the clone away:

```bash
python tools/refresh_dashboard.py
```

| | |
|---|---|
| [`RecastEngine`](https://github.com/a85tract/RecastEngine) | the engine — domain-independent: contracts, recipes, gates |
| the `cesm/…` names below | the first case's components, each its own repository |

**CESM · Pipeline 1 (CAM5 → Python):** [`PyCAM5`](https://github.com/a85tract/PyCAM5) ·
[`freeCAM`](https://github.com/a85tract/freeCAM) · [`PyCCPP`](https://github.com/a85tract/PyCCPP)

**CESM · Pipeline 2 (CAM6 → GPU):** [`JaxCAM6`](https://github.com/a85tract/CESM-jax-kernels) ·
[`NumbaCAM6`](https://github.com/a85tract/CESM-numba-kernels)

**CESM · Shared:** [`CC-Test`](https://github.com/a85tract/CESM-CC-Test) ·
[`Sec-Track`](https://github.com/a85tract/CESM-Sec-Track) (restricted — listed but never
counted: access is granted per person, and a number nobody outside can re-derive is not
evidence)

Components are named `cesm/…` rather than by bare name so the case grouping survives: a second
case is a second prefix, not more names in a flat bag.

## Why a repository and not only a site

Because the numbers have to be re-derivable, and only a repository can hold what re-derives
them. The generator, the pages it writes into, and the markers it writes between all sit in one
tree, so `python tools/refresh_dashboard.py --check` says whether what is published still
matches what the components contain. Each row carries the revision it was measured at, and the
history records what the dashboard claimed and when. A site can show the numbers; it cannot
show that they were earned.

## License

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). Two exceptions: legacy
code retained inside modernized software keeps its original license (documented in each
component's `NOTICE`), and Sec-Track access is restricted to reduce exploitation risk.
