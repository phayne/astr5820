"""
Loaders for the archival datasets used in the "then apply to" half of each set.

Every dataset lives in data/ as a CSV with a header line and a provenance block in
data/README.md. Recording where a number came from is part of the grade on every
problem set, so the loaders return the citation alongside the array.
"""

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def _load_column(filename, column, description):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{description} not found at {path}.\n"
            f"See data/README.md for what this file should contain and where it "
            f"comes from. If it is missing from your clone, pull the latest "
            f"version of the repository."
        )
    table = np.genfromtxt(path, delimiter=",", names=True)
    return np.asarray(table[column], dtype=float)


def load_class2_disk_radii():
    """Gas (CO-emitting) radii of Class II disks.

    Returns
    -------
    ndarray
        Disk radii [AU].
    """
    return _load_column("class2_disk_radii.csv", "R_gas_au", "Class II disk radii")


def load_core_velocity_gradients():
    """Velocity gradients of dense molecular cloud cores.

    Convert to Omega with constants.omega_from_velocity_gradient. No inclination
    correction is applied; these are projected gradients, so each is a lower
    bound on the true rotation rate.

    Returns
    -------
    ndarray
        Velocity gradients [km s^-1 pc^-1].
    """
    return _load_column(
        "core_velocity_gradients.csv", "grad_km_s_pc", "Dense-core velocity gradients"
    )
