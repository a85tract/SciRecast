# SciRecast

**An open-source, agentic ecosystem for modernizing legacy scientific software.**

LLM agents do the labor-intensive porting work under human oversight; every artifact ships
only after passing correctness validation and security review.

## 📊 <https://a85tract.github.io/SciRecast/>

| Tab | What is on it |
|---|---|
| [Architecture](https://a85tract.github.io/SciRecast/) | the three layers, why the boundaries fall where they do, how a case attaches |
| [CESM · Status](https://a85tract.github.io/SciRecast/cesm-status) | component inventory and gate conclusions, generated from the submodules |
| [CESM · CAM5 → Python](https://a85tract.github.io/SciRecast/cesm-cam5) | PyCAM5, freeCAM, PyCCPP |
| [CESM · CAM6 → GPU](https://a85tract.github.io/SciRecast/cesm-cam6) | per-scheme progress, kernels, deployment, run archive, open items |
| [CESM · Validation](https://a85tract.github.io/SciRecast/cesm-validation) | CC-Test and Sec-Track |

This README is the thirty-second version and links onward rather than restating. Each section
lives in exactly one page source (`index.md`, `cesm-status.md`, …); the counted half of the
Status tab is generated from the submodules by
[`tools/refresh_dashboard.py`](tools/refresh_dashboard.py), so a figure there is never older
than the revision printed beside it.

<!-- generated:headline -->
**6 of 6 components checked out here; no gate conclusions committed yet.** See the page for the inventory, the per-scheme progress, and what each figure was measured against.
<!-- /generated:headline -->

## What is here

```bash
git submodule update --init --recursive
```

| | |
|---|---|
| [`RecastEngine`](https://github.com/a85tract/RecastEngine) | the engine — domain-independent: contracts, recipes, gates |
| `cesm/` | the first case's components, each its own submodule |

**CESM · Pipeline 1 (CAM5 → Python):** [`PyCAM5`](https://github.com/a85tract/PyCAM5) ·
[`freeCAM`](https://github.com/a85tract/freeCAM) · [`PyCCPP`](https://github.com/a85tract/PyCCPP)

**CESM · Pipeline 2 (CAM6 → GPU):** [`JaxCAM6`](https://github.com/a85tract/CESM-jax-kernels) ·
[`NumbaCAM6`](https://github.com/a85tract/CESM-numba-kernels)

**CESM · Shared:** [`CC-Test`](https://github.com/a85tract/CESM-CC-Test) ·
[`Sec-Track`](https://github.com/a85tract/CESM-Sec-Track) (restricted — linked, never
submoduled, because one unreadable submodule takes a recursive clone down with it)

Components sit under `cesm/` rather than at the top level so that the case grouping survives
in the tree: a second case is a second directory, not more names in a flat bag.

## Why a repository and not only a site

Because the submodule pointers are a record, not decoration. This repository at a given commit
pins one revision of the engine and one of every component, so a result is reproducible from a
single hash: `git submodule update --init --recursive` and you have the tree that produced it.
The `Advance <component> to <sha>` commits in the history are that record over time, and the
hooks in [`hooks/`](hooks/) (install with [`tools/install-hooks.sh`](tools/install-hooks.sh))
keep the pointers from silently falling behind the work. A site cannot hold any of that; it is
the same facts, rendered for reading.

## License

Apache License 2.0 — see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE). Two exceptions: legacy
code retained inside modernized software keeps its original license (documented in each
component's `NOTICE`), and Sec-Track access is restricted to reduce exploitation risk.
