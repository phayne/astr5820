#!/usr/bin/env python3
"""
Problem Set 1, stage A -- the "then apply to" figure.

Sweep the core rotation rate over the observed range of dense-core velocity
gradients and compare the resulting distribution of centrifugal radii against
measured Class II disk radii.

    python ps1/ps1a_sweep.py

The plotting boilerplate is written for you. What you supply is the physics (via
cloud/collapse.py), the choice of what else to vary, and the answer to the
question the set actually asks: which input dominates the spread?

Hand in the figure and two or three sentences. Say where each dataset came from.
"""

import os

import matplotlib.pyplot as plt
import numpy as np

from astrotools import constants as c
from astrotools import data
from astrotools.cloud import collapse

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")


def main():
    os.makedirs(FIGDIR, exist_ok=True)

    # --- observed inputs -------------------------------------------------
    gradients = data.load_core_velocity_gradients()      # km s^-1 pc^-1
    omegas = c.omega_from_velocity_gradient(gradients)   # s^-1
    observed_radii = data.load_class2_disk_radii()       # AU

    # --- predicted disk radii --------------------------------------------
    # TODO: R_c also depends on R_0 and M, and Lecture 3 showed it goes as
    # R_0^4. Holding those fixed at the fiducial values is a choice, not a
    # result. Vary them and find out which one dominates.
    r_c = collapse.centrifugal_radius(omegas, c.R_CORE, c.M_CORE) / c.AU

    # --- figure -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    bins = np.logspace(0, 4, 30)
    ax.hist(r_c, bins=bins, alpha=0.65, label="Predicted $R_c$ (this work)")
    ax.hist(observed_radii, bins=bins, alpha=0.65, label="Observed Class II gas radii")
    ax.set_xscale("log")
    ax.set_xlabel("Disk radius [AU]")
    ax.set_ylabel("Number")
    ax.legend(frameon=False)
    fig.tight_layout()

    path = os.path.join(FIGDIR, "ps1a_disk_radii.png")
    fig.savefig(path, dpi=150)
    print(f"wrote {path}")

    # --- numbers to quote in your write-up --------------------------------
    for label, sample in (("predicted", r_c), ("observed", observed_radii)):
        lo, med, hi = np.percentile(sample, [16, 50, 84])
        print(f"{label:>10s}: median {med:7.1f} AU, 16-84% {lo:7.1f} - {hi:7.1f} AU, "
              f"spread {hi / lo:5.1f}x")


if __name__ == "__main__":
    main()
