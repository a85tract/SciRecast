# Contributing to SciRecast

Thank you for your interest in SciRecast — an open-source, agentic ecosystem for modernizing
legacy scientific software. This guide explains how to reach us, report problems, and
contribute.

> **SciRecast works differently from a typical open-source project.** The modernized software
> in the **Product Layer** is maintained by an LLM agent (**Pika**), not by direct human
> edits. When you hit a problem, you **open an issue** — Pika generates, tests, and (after
> passing validation and security checks) merges the fix. Human contributors work on the
> inner layers: the agent engine (**Core**) and the validation & security infrastructure
> (**Support**).

## Getting help, giving feedback, reporting bugs

The main channel is **GitHub issues** on the relevant repository:

| You want to… | Where to go |
|---|---|
| Report a bug / wrong result in a modernized product (PyCAM5, JaxCAM6, …) | Open an issue on that product's repository, with a reproducer |
| Suggest a feature or give general feedback | Open an issue on the relevant repository, or on the [SciRecast hub](https://github.com/a85tract/SciRecast) |
| Ask a question or propose a collaboration | Email the PI (see **Contact** below) |
| Report a **security vulnerability** | **Do not open a public issue** — see **Security & responsible disclosure** below |

**A good bug report includes:** what you ran (command / case / configuration), the environment
(machine, compiler, library versions), what you expected, what actually happened (error text
or output), and a minimal way to reproduce it. For scientific-correctness issues, include the
reference you compared against and the size of the discrepancy.

## Ways to contribute

SciRecast has three contribution paths, matched to who you are:

1. **Users of the modernized software.** You run the software and hit issues. Open an issue
   describing the problem (and a proposed fix, if you have one). This path is lightweight —
   participate as much or as little as you like.
2. **Domain scientists & engineers.** You bring the domain expertise to judge correctness
   (e.g., what floating-point discrepancy is acceptable). You contribute **benchmark suites
   and validation workflows** to the Support layer
   ([CESM-CC-Test](https://github.com/a85tract/CESM-CC-Test)), following the ecosystem's
   validation conventions.
3. **Agentic-system developers.** You extend **Pika**, the modernization engine, with new
   formal methods and agentic designs to close capability gaps.

Because the Product Layer is agent-maintained, please **do not send pull requests that
hand-edit modernized product code** — file an issue instead, so the change flows through Pika
and the validation & security gates. Contributions to the **Core** and **Support** layers are
made through normal pull requests to those repositories.

## Security & responsible disclosure

Security findings are handled privately. **Do not report vulnerabilities in public issues.**
Instead:

- Open a **private security advisory** on the affected repository
  (GitHub → *Security* → *Report a vulnerability*), or
- Email the PI directly (see **Contact**).

Confirmed and responsibly-disclosed vulnerabilities are tracked in **Sec-Track**
([CESM-Sec-Track](https://github.com/a85tract/CESM-Sec-Track)), whose access is restricted to
the PI's group to reduce the risk of malicious exploitation. Please give us reasonable time to
remediate before any public disclosure.

## Licensing

SciRecast is licensed under the **Apache License 2.0** (see [`LICENSE`](LICENSE) and
[`NOTICE`](NOTICE)). By contributing, you agree that your contributions are licensed under the
same terms. Legacy code retained inside modernized software keeps its original license, as
documented in each component's `NOTICE` file.

## Governance

SciRecast is transitioning from a research prototype to a community-governed ecosystem.
Governance — a cross-institution steering committee, per-layer working groups, and an RFC
process for major changes — is being established and will be documented here as it takes shape.

## Contact

- **Lead PI:** Yueqi Chen, University of Colorado Boulder — <yuch8134@colorado.edu>
- **Issue trackers:** on each component repository (see the [README](README.md) for the map)
