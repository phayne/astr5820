"""
Loaders for the archival datasets used in the problem sets.

Every dataset lives in data/ as a CSV with a header line. Where each file came
from, and what units its columns are in, is recorded in data/README.md.
"""

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_herschel_cores():
    """Dense cores in Aquila from the Herschel Gould Belt Survey.

    Konyves et al. (2015), A&A 584, A91, Table A.2. Units are as published and
    are not uniform: masses in solar masses, radii in pc, temperatures in K,
    volume densities in 10^4 cm^-3, column densities in 10^21 cm^-2. See
    data/README.md for the full column list.

    Returns
    -------
    ndarray
        Structured array with one record per core. Access columns by name, for
        example cores["Mcore"], cores["Tdust"], cores["nH2avd"],
        cores["Coretype"].
    """
    path = os.path.join(DATA_DIR, "herschel_core_catalog.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Herschel core catalog not found at {path}.\n"
            f"See data/README.md for what this file should contain and where it "
            f"comes from. If it is missing from your clone, pull the latest "
            f"version of the repository."
        )
    return np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")
