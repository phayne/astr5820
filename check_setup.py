#!/usr/bin/env python3
"""
ASTR 5820 environment check.

Run this once you have followed SETUP.md:

    python check_setup.py

It verifies your Python version, your packages, that the course toolbox imports,
and that plotting and file output work. If every line reads OK, you are set up
for the semester. Bring any FAIL to office hours or contact the instructor with
the full output pasted in -- do not spend an hour on it alone.
"""

import contextlib
import importlib
import os
import platform
import sys
import traceback

MIN_PYTHON = (3, 10)

# (import name, minimum version, why the course needs it, required?)
PACKAGES = [
    ("numpy", "1.24", "arrays and linear algebra; used in every problem set", True),
    ("scipy", "1.10", "integration, optimisation, special functions", True),
    ("matplotlib", "3.7", "every figure you hand in", True),
    ("astropy", "5.3", "units, constants, FITS and VOTable archive files", True),
    ("pandas", "2.0", "reading the archival catalogues from Week 5 onward", True),
    ("pytest", "7.4", "runs the tests that define each coding exercise", True),
    ("rebound", "3.28", "N-body integrator; install in Week 9 with pip install -e '.[nbody]'", False),
]

results = []


def report(name, ok, detail=""):
    results.append((name, ok))
    status = "OK  " if ok else "FAIL"
    print(f"  [{status}] {name}" + (f" -- {detail}" if detail else ""))


def _version_tuple(v):
    parts = []
    for piece in str(v).split(".")[:3]:
        digits = "".join(ch for ch in piece if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def check_python():
    print("\nPython")
    v = sys.version_info
    ok = (v.major, v.minor) >= MIN_PYTHON
    report(
        f"Python {v.major}.{v.minor}.{v.micro}",
        ok,
        "" if ok else f"need {MIN_PYTHON[0]}.{MIN_PYTHON[1]} or later",
    )
    print(f"         {platform.platform()}")
    print(f"         interpreter: {sys.executable}")
    in_named_env = (
        bool(os.environ.get("VIRTUAL_ENV"))
        or os.environ.get("CONDA_DEFAULT_ENV") == "astr5820"
        or bool(os.environ.get("CODESPACES"))
        or os.path.exists("/.dockerenv")
    )
    if not in_named_env:
        print("         note: this does not look like the course environment.")
        print("         Did you run 'source .venv/bin/activate'?")


def check_packages():
    print("\nPackages")
    for name, minimum, purpose, required in PACKAGES:
        try:
            module = importlib.import_module(name)
        except ImportError:
            if required:
                report(name, False, f"not installed -- needed for {purpose}")
            else:
                print(f"  [--  ] {name} -- not installed; not needed until Week 9")
            continue
        version = getattr(module, "__version__", "unknown")
        if version != "unknown" and _version_tuple(version) < _version_tuple(minimum):
            report(name, False, f"{version} installed, need {minimum} or later")
        elif required:
            report(f"{name} {version}", True)
        else:
            print(f"  [OK  ] {name} {version} -- optional until Week 9")


def check_toolbox():
    print("\nCourse toolbox")
    try:
        from astrotools import constants as c
    except ImportError:
        report(
            "import astrotools",
            False,
            "run 'pip install -e .' from the repository root",
        )
        return
    report("import astrotools", True)

    # A constant that is easy to get wrong and easy to check.
    au_ok = abs(c.AU - 1.495978707e11) < 1.0
    report("constants load", au_ok, f"1 AU = {c.AU:.6e} m")

    try:
        from astrotools.nbody import integrators, twobody

        period = twobody.orbital_period(c.AU)
        y0 = twobody.initial_conditions(c.AU, 0.0)
        _, y = integrators.integrate(
            integrators.euler_step, twobody.kepler_derivs, y0, (0.0, period), period / 5000
        )
        drift = abs(twobody.relative_drift(twobody.specific_energy(y))[-1])
        report(
            "Euler integration runs",
            y.shape == (5001, 4),
            f"one orbit, {len(y) - 1} steps, energy drift {drift:.2e}",
        )
    except Exception:
        report("Euler integration runs", False, "traceback below")
        traceback.print_exc()


def check_plotting_and_io():
    print("\nPlotting and file output")
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        fig, ax = plt.subplots(figsize=(3, 2))
        ax.plot(np.linspace(0, 1, 10), np.linspace(0, 1, 10) ** 2)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_setup_check.png")
        fig.savefig(path, dpi=60)
        plt.close(fig)
        ok = os.path.exists(path) and os.path.getsize(path) > 0
        if ok:
            os.remove(path)
        report("matplotlib writes a figure", ok)
    except Exception:
        report("matplotlib writes a figure", False, "traceback below")
        traceback.print_exc()


class _Tally:
    """Counts test outcomes without letting pytest print over the setup report."""

    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1


def report_problem_set_progress():
    """Informational only. Failing tests here are the assignment, not a setup problem."""
    print("\nProblem Set 1")
    try:
        import pytest
    except ImportError:
        print("  pytest not installed; skipping")
        return

    root = os.path.dirname(os.path.abspath(__file__))
    tally = _Tally()
    with open(os.devnull, "w") as devnull, contextlib.redirect_stdout(devnull):
        pytest.main(
            ["-q", "--no-header", "--tb=no", os.path.join(root, "tests"),
             "-p", "no:cacheprovider"],
            plugins=[tally],
        )

    total = tally.passed + tally.failed
    print(f"  {tally.passed} of {total} tests passing.")
    if tally.failed:
        print("  The rest are the assignment, not a setup problem. Run")
        print("      pytest tests/ -v")
        print("  to see what each one is asking for.")


def main():
    print("=" * 68)
    print("ASTR 5820: Origin and Evolution of Planetary Systems")
    print("Environment check")
    print("=" * 68)

    check_python()
    check_packages()
    check_toolbox()
    check_plotting_and_io()

    failures = [name for name, ok in results if not ok]
    print("\n" + "=" * 68)
    if failures:
        print(f"{len(failures)} check(s) failed:")
        for name in failures:
            print(f"  - {name}")
        print("\nSee the Troubleshooting section of SETUP.md. If that does not")
        print("resolve it, send this entire output to the instructor.")
    else:
        print("All checks passed. Your environment is ready.")
    print("=" * 68)

    report_problem_set_progress()
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
