---
title: Validation & Security
parent: CESM Case
parent_url: cesm
---

Shared by both pipelines: the gates every artifact has to pass, and the record of what was found.

## Validation & Security (shared by both pipelines)

### [CC-Test/](https://github.com/a85tract/CESM-CC-Test) → `CESM-CC-Test`
The CESM case's instance of SciRecast's Support Layer. Its Cyber half is built today: a
reusable local + CI DevSecOps gate for the modernization repos. Runs the same checks
locally (before `git push`) that the cloud CI runs on every PR, reusing each target repo's
own config so local and cloud never drift. Two planes:
- **Pre-push gate** (`tools/devsecops-local.sh` + `hooks/pre-push`): secret scan
  (gitleaks), SBOM+CVE+VEX (syft -> grype), and Claude AI code audit; blocks the push on
  secrets / Critical CVEs / high AI findings.
- **Sanitizer plane** (`tools/asan.sh`, `hpc/asan-cam.pbs`): builds + runs Fortran/C under
  `ifx -fsanitize=address` for heap-OOB / use-after-free with exact `file:line`. Verified
  on Derecho: ifx 2025.2.1 catches Fortran heap-buffer-overflow.

### Sec-Track → [`CESM-Sec-Track`](https://github.com/a85tract/CESM-Sec-Track) (restricted)
The CESM case's vulnerability record: N-day and responsibly disclosed 0-day findings spanning
the modernized software, its supply-chain dependencies, and the runtime environment. Access
is restricted to reduce the risk of malicious exploitation.

**Listed, never counted.** Access is granted per person, so no public run of
`tools/refresh_dashboard.py` can clone it, and a figure nobody outside can re-derive would be
a claim rather than evidence. It appears on these pages by name and by what it is for, and
nowhere as a number. Request access if you need it.

---
