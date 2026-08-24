"""
Loaders for the archival datasets used in the "then apply to" half of each set.

Every dataset lives in data/ as a CSV with a header line and a provenance block in
data/README.md. Recording where a number came from is part of the work on every
problem set, so read that file before you use anything here.
"""

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


# ---------------------------------------------------------------------------
# Counting constants for the Problem Set 1 lifetime estimate.
# Konyves et al. (2015), Sect. 5.1: the Aquila field contains 622 Class II
# young stellar objects identified by Spitzer, and a Class II lifetime of
# 2 Myr is adopted. See data/README.md.
# ---------------------------------------------------------------------------
N_CLASS_II_AQUILA = 622
T_CLASS_II_YR = 2.0e6


def load_herschel_cores():
    """Dense cores in Aquila from the Herschel Gould Belt Survey.

    Konyves et al. (2015), A&A 584, A91; VizieR J/A+A/584/A91, tablea2.

    Values are returned in the units the catalog publishes -- masses in solar
    masses, radii in parsecs, temperatures in kelvin, volume densities in
    10^4 cm^-3. Convert to SI before handing anything to cloud.collapse; the
    conversion is yours to get right, and the tests will not catch it for you.

    Returns
    -------
    numpy.ndarray
        Structured array with one row per core. Field names are the CSV column
        names, listed in data/README.md. Use the ``core_type`` field to select
        prestellar cores and ``co_contaminated`` to drop the 23 flagged
        contaminants, which reproduces the paper's science sample.

    Examples
    --------
    >>> cores = load_herschel_cores()
    >>> pre = cores[(cores["core_type"] == "prestellar")
    ...             & (cores["co_contaminated"] == 0)]
    >>> len(pre)
    446
    """
    path = os.path.join(DATA_DIR, "herschel_core_catalog.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Herschel core catalog not found at {path}.\n"
            f"See data/README.md for what this file should contain and where it "
            f"comes from. If it is missing from your clone, pull the latest "
            f"version of the repository."
        )
    return np.genfromtxt(
        path, delimiter=",", names=True, dtype=None, encoding="utf-8"
    )
