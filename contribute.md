---
title: Contributing
nav_order: 4
---

# Contributing

## Who changes what

Human developers do **not** directly modify the Product Layer. When end users
open issues, RecastEngine generates, tests, and merges the fixes. Humans
contribute to the **Core Layer** — new formal methods, agentic designs, plugin
contracts — and to the **Support Layer** — benchmark suites, validation
workflows, vulnerability reports.

That division is not deference to the machine; it is what keeps the gates
meaningful. A human editing generated output by hand produces an artifact whose
provenance no longer matches its evidence, and the next regeneration silently
undoes the edit. If generated code is wrong, the rule that generated it is
wrong — fix that, in the engine, where the fix applies to every artifact rather
than to one.

## Where to send what

| | |
|---|---|
| A bug or a feature idea in a component | that component's own repository |
| A translation that is wrong, or a rule that should exist | [RecastEngine issues](https://github.com/a85tract/RecastEngine/issues) |
| A gate that passed something it should not have | RecastEngine issues — a gate that can be fooled is the more serious bug |
| **A security vulnerability** | **never a public issue** — a private GitHub security advisory, or email below |

## Extending the engine

Implement one of the ten interfaces in
[`src/recast/plugins/`](https://github.com/a85tract/RecastEngine/tree/main/src/recast/plugins)
and register an entry point;
[`docs/writing-a-plugin.md`](https://github.com/a85tract/RecastEngine/blob/main/docs/writing-a-plugin.md)
walks through it, and [`conformance/`](https://github.com/a85tract/RecastEngine/tree/main/conformance)
says what a plugin has to satisfy. Improving the engine improves it for everyone
using it: the contract a plugin you write uses is the same one the shipped
plugins use, so nothing you add is second-class.

Site-specific and domain-specific knowledge belongs in a plugin rather than in
the engine — a scheduler for your cluster, the conventions of your model. The
engine passing its tests with every domain package uninstalled is a standing
check, not an aspiration.

## Contact

Full guidelines: [`CONTRIBUTING.md`](https://github.com/a85tract/SciRecast/blob/main/CONTRIBUTING.md).

**Security vulnerabilities:** please do *not* open a public issue — use a private
GitHub security advisory or email **Yueqi Chen** (University of Colorado
Boulder), <yueqi.chen@colorado.edu>.

**Collaboration and licensing:** the same address.
