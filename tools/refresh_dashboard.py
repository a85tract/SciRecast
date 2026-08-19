#!/usr/bin/env python3
"""Regenerate the counted parts of README.md from the submodules themselves.

The dashboard used to be hand-copied, which is why it carried a date and why
the date kept aging past the work. This tool replaces the parts that are
*countable* with counts taken from the checked-out submodules, and stamps each
with the revision it counted -- a number without the revision it was measured
at is not reproducible, and a dashboard nobody can reproduce is decoration.

What it deliberately does NOT touch: the per-scheme progress table, the bug
counts, the run archive, the work items. Those are human judgements ("CLUBB
45%", "root cause is likely rrtthl") and no scan produces them. They stay
hand-maintained, outside the generated markers, and the report says so rather
than implying the whole file is derived.

Usage:
    git submodule update --init            # counts need the trees present
    python tools/refresh_dashboard.py      # rewrites the marked blocks
    python tools/refresh_dashboard.py --check   # CI: fail if stale
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
PAGE = ROOT / "cesm-status.md"
"""Two targets, and the split is the point. ``cesm-status.md`` is the CESM
case's status tab -- the inventory and the gate conclusions in full.
``README.md`` is the thirty-second version and carries one generated line, not a second copy of the
tables: a table maintained in two places is a table that will disagree with
itself, which is the failure this tool exists to end."""

# One entry per submodule: how to describe it, and what is worth counting.
# A component whose tree is absent is reported as absent rather than skipped:
# a missing count and a zero count are different facts.
COMPONENTS: list[dict[str, object]] = [
    {
        "path": "cesm/PyCAM5",
        "pipeline": 1,
        "counts": [
            ("runtime selectors", "selectors"),
            ("Codon modules", "codon_files"),
            ("exported routines", "codon_exports"),
        ],
    },
    {"path": "cesm/freeCAM", "pipeline": 1, "counts": [("Python files", "py_files")]},
    {"path": "cesm/PyCCPP", "pipeline": 1, "counts": [("Fortran files", "f90_files")]},
    {
        "path": "cesm/JaxCAM6",
        "pipeline": 2,
        "counts": [
            ("schemes", "schemes"),
            ("kernel lines", "kernel_lines"),
            ("test files", "test_files"),
        ],
    },
    {
        "path": "cesm/NumbaCAM6",
        "pipeline": 2,
        "counts": [
            ("schemes", "schemes"),
            ("kernel lines", "kernel_lines"),
            ("test files", "test_files"),
        ],
    },
    {"path": "cesm/CC-Test", "pipeline": 0, "counts": [("tools", "tool_files")]},
]

SCHEME_DIRS_IGNORED = {"tests", "utils", "__pycache__", "docs"}


def git(args: list[str], cwd: Path) -> str:
    out = subprocess.run(  # noqa: S603 -- git, on a path we control
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )
    return out.stdout.strip() if out.returncode == 0 else ""


def revision(path: Path) -> tuple[str, str]:
    """``(short sha, commit date)`` of a checked-out submodule.

    The length is pinned rather than left to ``--short``, whose default follows
    each repository's ``core.abbrev`` -- a developer and a CI runner would
    otherwise disagree about the same commit and the dashboard would flap.
    """
    return git(["rev-parse", "HEAD"], path)[:7], git(["log", "-1", "--format=%cs"], path)


def python_files(path: Path) -> list[Path]:
    return [p for p in path.rglob("*.py") if ".git" not in p.parts]


def lines_in(paths: list[Path]) -> int:
    total = 0
    for p in paths:
        try:
            total += len(p.read_text(errors="replace").splitlines())
        except OSError:
            continue
    return total


def measure(path: Path) -> dict[str, int]:
    """Every count this tool knows how to take, for one component."""
    source = path / "src" if (path / "src").is_dir() else path
    fortran = [p for p in source.rglob("*.F90") if ".git" not in p.parts]
    pys = python_files(path)
    codon = [p for p in pys if p.name.endswith("_codon.py")]
    tests = [p for p in pys if p.name.startswith("test_") or p.name.endswith("_test.py")]
    kernels = [p for p in pys if p not in tests and "test" not in p.parts]

    selectors: set[str] = set()
    exports = 0
    for f in fortran:
        text = f.read_text(errors="replace")
        selectors |= set(re.findall(r"'([A-Z0-9_]+_IMPL)'", text))
    for c in codon:
        exports += len(re.findall(r"^@export\s*$", c.read_text(errors="replace"), re.M))

    schemes = sorted(
        d.name
        for d in path.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name not in SCHEME_DIRS_IGNORED
    )
    return {
        "selectors": len(selectors),
        "codon_files": len(codon),
        "codon_exports": exports,
        "py_files": len(pys),
        "f90_files": len(fortran),
        "schemes": len(schemes),
        "kernel_lines": lines_in(kernels),
        "test_files": len(tests),
        "tool_files": len([p for p in (path / "tools").glob("*") if p.is_file()])
        if (path / "tools").is_dir()
        else 0,
    }


def verifications(path: Path) -> list[dict[str, object]]:
    """Every gate conclusion a component has committed.

    Read from ``verification.json`` files -- the *current state* record the
    engine's runner writes: one entry per unit and comparison, regenerated
    rather than appended, no timestamps or paths, so it is committable and a
    diff in it means a verdict moved. The manifests under ``evidence/`` are the
    other record, one immutable document per verdict per run, and they are
    deliberately not committed anywhere, so nothing here looks for them.

    A component with no such file contributes nothing rather than a zero: the
    absence means "these gates have not been wired up here", which is a
    different claim from "they were run and found nothing".
    """
    found: list[dict[str, object]] = []
    for summary in sorted(path.rglob("verification.json")):
        if ".git" in summary.parts or "work" in summary.parts:
            continue
        try:
            record = json.loads(summary.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        rows = record.get("routines") or record.get("units") or []
        for row in rows:
            entry = dict(row)
            entry["_component"] = path.name
            entry["_revision"] = record.get("source_revision", "")
            found.append(entry)
    return found


def previous_rows(text: str) -> dict[str, str]:
    """The rows already in the README, by component.

    A component this checkout cannot read must not have its counts erased --
    several of them are private repositories, and a CI run holding fewer keys
    than a developer would otherwise overwrite real numbers with blanks. The
    previous row is carried forward verbatim and the footnote says which ones
    were not re-counted.
    """
    start = text.find("<!-- generated:inventory -->")
    end = text.find("<!-- /generated:inventory -->")
    if start < 0 or end < 0:
        return {}
    rows = {}
    for line in text[start:end].splitlines():
        match = re.match(r"\|\s*`([^`]+)`\s*\|", line)
        if match:
            rows[match.group(1)] = line.rstrip()
    return rows


def inventory_block(text: str) -> str:
    carried_from = previous_rows(text)
    rows = [
        "| Component | Pinned revision | Last commit | Counted |",
        "|---|---|---|---|",
    ]
    missing, carried = [], []
    for entry in COMPONENTS:
        path = ROOT / str(entry["path"])
        name = path.name
        readable = path.is_dir() and any(path.iterdir())
        if not readable:
            if name in carried_from:
                rows.append(carried_from[name])
                carried.append(name)
            else:
                missing.append(name)
                rows.append(f"| `{name}` | — | — | not checked out |")
            continue
        sha, date = revision(path)
        numbers = measure(path)
        counted = ", ".join(
            f"{numbers[key]:,} {label}" for label, key in entry["counts"]  # type: ignore[union-attr]
        )
        gates = verifications(path)
        if gates:
            by_confidence: dict[str, int] = {}
            for gate in gates:
                key = str(gate.get("confidence", "unknown"))
                by_confidence[key] = by_confidence.get(key, 0) + 1
            counted += "; gated: " + ", ".join(
                f"{n} {c}" for c, n in sorted(by_confidence.items())
            )
        rows.append(f"| `{name}` | `{sha}` | {date} | {counted} |")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    note = [
        "",
        f"*Counted by `tools/refresh_dashboard.py` at {stamp}, from the submodule "
        "revisions above. Re-run it after `git submodule update --remote`; every "
        "number here is reproducible from the pinned revision beside it.*",
    ]
    if carried:
        note.append("")
        note.append(
            "*Carried forward, not re-counted here: "
            + ", ".join(f"`{c}`" for c in carried)
            + " — those trees were not readable in this checkout (several component "
            "repositories are private), so their previous counts and revisions stand.*"
        )
    if missing:
        note.append("")
        note.append(
            "*Never counted: "
            + ", ".join(f"`{m}`" for m in missing)
            + " — run `git submodule update --init --recursive` and re-run.*"
        )
    return "\n".join(rows + note)


def gates_block() -> str:
    """Every committed gate conclusion, across components.

    This is the table the front page could not previously carry at all: not
    "ZM is 95% done" -- a judgement -- but "this routine was compared against
    the compiled original at this confidence, over this many points, under this
    oracle". Absent components contribute nothing; a component that has not
    wired up a gate simply does not appear, which is honest and visibly
    different from appearing with a failure.
    """
    rows = [
        "| Component | Routine | Comparison | Confidence | Points bit-exact | Oracle |",
        "|---|---|---|---|---|---|",
    ]
    total = 0
    for entry in COMPONENTS:
        path = ROOT / str(entry["path"])
        if not (path.is_dir() and any(path.iterdir())):
            continue
        for gate in verifications(path):
            total += 1
            points, exact = gate.get("points"), gate.get("bit_exact")
            coverage = (
                f"{exact:,}/{points:,}" if isinstance(points, int) and isinstance(exact, int)
                else str(gate.get("detail", "—"))[:44]
            )
            oracle = str(gate.get("oracle") or "—")
            rows.append(
                f"| `{gate['_component']}` | `{gate.get('routine') or gate.get('unit')}` "
                f"| {gate.get('comparison', '—')} | **{gate.get('confidence')}** "
                f"| {coverage} | `{oracle}` |"
            )
    if total == 0:
        return (
            "*No component has committed gate conclusions yet. A component wires this up by "
            "running the engine's gates and committing the `verification.json` they write; "
            "see [RecastEngine's examples](https://github.com/a85tract/RecastEngine/tree/main/examples).*"
        )
    return "\n".join(rows)


def headline_block() -> str:
    """One line for the README: how much is pinned, and what has been gated.

    Deliberately not a table. The README's job is to point at the page, and a
    summary that grows into a second inventory is how the two drift apart.
    """
    pinned = sum(
        1 for e in COMPONENTS if (ROOT / str(e["path"])).is_dir() and any((ROOT / str(e["path"])).iterdir())
    )
    gates = [g for e in COMPONENTS for g in verifications(ROOT / str(e["path"]))]
    by_confidence: dict[str, int] = {}
    for gate in gates:
        key = str(gate.get("confidence", "unknown"))
        by_confidence[key] = by_confidence.get(key, 0) + 1
    if gates:
        conclusions = ", ".join(f"{n} {c}" for c, n in sorted(by_confidence.items()))
        verdicts = f"{len(gates)} recorded gate conclusion(s): {conclusions}"
    else:
        verdicts = "no gate conclusions committed yet"
    return (
        f"**{pinned} of {len(COMPONENTS)} components checked out here; {verdicts}.** "
        "See the page for the inventory, the per-scheme progress, and what each figure "
        "was measured against."
    )


def rewrite(text: str, name: str, body: str) -> str:
    start, end = f"<!-- generated:{name} -->", f"<!-- /generated:{name} -->"
    if start not in text or end not in text:
        raise SystemExit(f"README.md has no {start} ... {end} block to fill")
    head, rest = text.split(start, 1)
    _stale, tail = rest.split(end, 1)
    return f"{head}{start}\n{body}\n{end}{tail}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument(
        "--check",
        action="store_true",
        help="do not write; exit non-zero if the generated blocks are out of date",
    )
    ns = ap.parse_args()

    page_before = PAGE.read_text()
    page_after = rewrite(page_before, "inventory", inventory_block(page_before))
    page_after = rewrite(page_after, "gates", gates_block())

    readme_before = README.read_text()
    readme_after = rewrite(readme_before, "headline", headline_block())

    if ns.check:
        # Compare the page's table rows only. The timestamp moves every run and
        # the provenance footnote describes *this checkout's* visibility -- a CI
        # runner holding fewer keys than a developer says so in the footnote and
        # would otherwise report a stale dashboard on every pull request. The
        # README's headline is compared whole, being one line with no clock in it.
        stale = []
        if previous_rows(page_before) != previous_rows(page_after):
            stale.append("index.md")
            for name, row in previous_rows(page_after).items():
                if previous_rows(page_before).get(name) != row:
                    print(f"  {name}:", file=sys.stderr)
                    print(
                        f"    recorded: {previous_rows(page_before).get(name, '(absent)')}",
                        file=sys.stderr,
                    )
                    print(f"    measured: {row}", file=sys.stderr)
        if readme_before != readme_after:
            stale.append("README.md")
        if not stale:
            print("dashboard is current")
            return 0
        print(f"stale: {', '.join(stale)} -- run tools/refresh_dashboard.py", file=sys.stderr)
        return 1

    written = []
    for target, before, after in (
        (PAGE, page_before, page_after),
        (README, readme_before, readme_after),
    ):
        if after != before:
            target.write_text(after)
            written.append(target.name)
    print(f"regenerated: {', '.join(written)}" if written else "dashboard unchanged")
    return 0


if __name__ == "__main__":
    sys.exit(main())
