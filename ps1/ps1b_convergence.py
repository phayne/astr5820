#!/usr/bin/env python3
"""
Problem Set 1, stage B -- the "then apply to" figure.

Two panels. Left: global error after one orbit against step size, for Euler and
RK4, with reference slopes. Right: fractional energy drift over 100 orbits for
both schemes.

    python ps1/ps1b_convergence.py

The left panel should show the slopes you predicted before writing any code.
The right panel is the one to look at hardest -- it is the reason Week 9 replaces
a fourth-order scheme with a second-order one.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from astrotools import constants as c
from astrotools.nbody import integrators, twobody

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")

A_TEST = 1.0 * c.AU
E_TEST = 0.3
PERIOD = twobody.orbital_period(A_TEST)
SCHEMES = {"Euler": integrators.euler_step, "RK4": integrators.rk4_step}


def global_error(stepper, n_steps):
    """Position error after exactly one orbit, in units of a."""
    y0 = twobody.initial_conditions(A_TEST, E_TEST)
    _, y = integrators.integrate(
        stepper, twobody.kepler_derivs, y0, (0.0, PERIOD), PERIOD / n_steps
    )
    return np.linalg.norm(y[-1, :2] - y0[:2]) / A_TEST


def main():
    os.makedirs(FIGDIR, exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    # --- convergence ------------------------------------------------------
    # Range chosen so both schemes sit in their asymptotic regime: coarser than
    # this and Euler's error saturates, finer and RK4 hits the roundoff floor
    # near 1e-13. Widen it and watch both fits degrade -- that is worth seeing.
    n_steps = 2 ** np.arange(8, 14)
    dt_over_p = 1.0 / n_steps
    for name, stepper in SCHEMES.items():
        errors = np.array([global_error(stepper, int(n)) for n in n_steps])
        ax1.loglog(dt_over_p, errors, "o-", label=name)
        # Measured order between successive points -- quote this, not the eyeball slope.
        order = np.polyfit(np.log(dt_over_p), np.log(errors), 1)[0]
        print(f"{name:>6s}: fitted order {order:.2f}")

    ax1.set_xlabel(r"$\Delta t / P$")
    ax1.set_ylabel("Position error after one orbit  [$a$]")
    ax1.legend(frameon=False)
    # TODO: overplot reference lines of slope 1 and slope 4 so the orders can be
    # read off rather than inferred.

    # --- energy drift -----------------------------------------------------
    y0 = twobody.initial_conditions(A_TEST, E_TEST)
    n_orbits = 100
    for name, stepper in SCHEMES.items():
        t, y = integrators.integrate(
            stepper, twobody.kepler_derivs, y0, (0.0, n_orbits * PERIOD),
            PERIOD / 500, store_every=50,
        )
        drift = twobody.relative_drift(twobody.specific_energy(y))
        ax2.semilogy(t / PERIOD, np.abs(drift), label=name)

    ax2.set_xlabel("Orbits")
    ax2.set_ylabel(r"$|\Delta E / E|$")
    ax2.legend(frameon=False)

    fig.tight_layout()
    path = os.path.join(FIGDIR, "ps1b_convergence.png")
    fig.savefig(path, dpi=150)
    print(f"wrote {path}")

    # TODO for the write-up: extrapolate the RK4 curve in the right-hand panel to
    # 1e5 orbits. State the timestep at which RK4 would need to run to match a
    # leapfrog integration there, and what that costs.


if __name__ == "__main__":
    main()
