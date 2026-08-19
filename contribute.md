---
title: Contributing
nav_order: 4
---

# Contributing

## Where to send what

| What you have | Where it goes |
|---|---|
| A bug or a feature idea in a component | that component's own repository — [`PyCAM5`](https://github.com/a85tract/PyCAM5), [`freeCAM`](https://github.com/a85tract/freeCAM), [`JaxCAM6`](https://github.com/a85tract/CESM-jax-kernels), [`NumbaCAM6`](https://github.com/a85tract/CESM-numba-kernels), [`CC-Test`](https://github.com/a85tract/CESM-CC-Test), [`Sec-Track`](https://github.com/a85tract/CESM-Sec-Track) |
| A translation that is wrong, or a rule that should exist | [RecastEngine issues](https://github.com/a85tract/RecastEngine/issues) |
| **A security vulnerability** | **never a public issue** — a private GitHub security advisory, or the address below |
{: .route}

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

**Security vulnerabilities, collaboration, and licensing** — **Yueqi Chen**, University of
Colorado Boulder, <yueqi.chen@colorado.edu>. For a vulnerability, please do *not* open a
public issue: use a private GitHub security advisory, or this address.
