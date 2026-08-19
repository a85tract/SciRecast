---
title: Architecture
nav_order: 1
---

# SciRecast

**An open-source, agentic ecosystem for modernizing legacy scientific software.**

LLM agents do the labor-intensive porting work under human oversight; every artifact ships
only after passing correctness validation and security review. This tab is the architecture:
what the three layers are, why the boundaries fall where they do, and how a case attaches.
The CESM tabs are the first case, in detail.

## The Three Layers, Seen Through the CESM Case

SciRecast is organized into three layers. **Humans maintain the inner two** (the engine, and
the validation & security infrastructure); **the agent produces the outermost one** — and only
after the artifact passes the gates.

```mermaid
flowchart TB
    subgraph Product["🟦 Product Layer — modernized software (CESM case)"]
        PyCAM5["PyCAM5 · freeCAM · PyCCPP"]
        JaxCAM6["JaxCAM6 · NumbaCAM6"]
    end
    subgraph Support["🟩 Support Layer — Validation &amp; Security"]
        CCTest["CC-Test"]
        SecTrack["Sec-Track"]
    end
    subgraph Core["🟥 Core Layer — RecastEngine"]
        Engine["multi-LLM-agent, neuro-symbolic"]
    end

    Engine -- "translate · refactor · port to accelerators" --> Product
    Engine -- "retrieve for correctness validation" --> CCTest
    Engine -- "store security analyses" --> SecTrack
    CCTest -- "gate" --> Product
    SecTrack -- "gate" --> Product
```

**🟥 Core Layer — [`RecastEngine`](https://github.com/a85tract/RecastEngine).** A multi-LLM-agent
engine that combines the generative power of LLMs with the rigor of formal methods
(neuro-symbolic). It translates languages, refactors architectures, ports code to
accelerators, and gates every result against the original. The engine knows nothing about any
particular model: domain knowledge attaches through its published plugin contract, which is
what makes a second case possible without rebuilding anything. Its own
[`docs/architecture.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/architecture.md)
carries the spine, the ten interfaces, and where the boundaries fall.

**🟩 Support Layer — the trust foundation.** *CC-Test* is the CI/CD workflow covering both
**C**orrectness and **C**yber testing; *Sec-Track* is the restricted-access record of N-day and
responsibly disclosed vulnerabilities across the software, its supply chain, and its runtime.
This is a separate layer because a gate the gated thing can influence is not a gate — what
these two check, and how strictly, is deliberately not the engine's decision to make. The CESM
case's instances of both, with their operational detail, are in the case repository.

**🟦 Product Layer — the modernized software itself.** Modernized artifacts are *outputs*, not
components: what comes out when the engine, the domain knowledge, and the legacy source are
put together. Humans do not hand-maintain this layer. For CESM, the products and their
per-scheme status are tracked in the case repository.

**Where the case lives.** Component repositories, pipeline structure, per-scheme progress, and
validated-run evidence are all in
**[`CESM-modernization-overview`](https://github.com/a85tract/CESM-modernization-overview)** —
the only place any of it is maintained.

**Contribution model.** Human developers do **not** directly modify the Product Layer. When end
users open issues, RecastEngine generates, tests, and merges the fixes. Humans contribute to the
Core Layer (new formal methods and agentic designs) and to the Support Layer (benchmark suites,
validation workflows, vulnerability reports).

---

## Why an umbrella repository at all

Because the submodule pointers are a record, not decoration. This repository at a given commit
pins one exact revision of the engine and one of the case, so a result can be reproduced from a
single hash: `git submodule update --init --recursive` and you have the tree that produced it.
The `Advance <component> to <sha>` commits in the history are that record over time, and the
hooks in [`hooks/`](hooks/) (install with [`tools/install-hooks.sh`](tools/install-hooks.sh))
are what keep the pointers from silently falling behind the work.

---

## Contribution model

Human developers do **not** directly modify the Product Layer. When end users open issues,
RecastEngine generates, tests, and merges the fixes. Humans contribute to the Core Layer (new
formal methods and agentic designs) and to the Support Layer (benchmark suites, validation
workflows, vulnerability reports).

See [`CONTRIBUTING.md`](https://github.com/a85tract/SciRecast/blob/main/CONTRIBUTING.md).
**Security vulnerabilities:** please do *not* open a public issue — use a private GitHub
security advisory or email **Yueqi Chen** (University of Colorado Boulder),
<yueqi.chen@colorado.edu>.
