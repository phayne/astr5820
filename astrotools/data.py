"""
Loaders for the archival datasets used in the problem sets.

Every dataset lives in data/<set>/ as a CSV with a header line. Where each file
came from, and what units its columns are in, is recorded in the README beside
it.
"""

import os

import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")


def load_herschel_cores():
    """Dense cores in Aquila from the Herschel Gould Belt Survey.

    Konyves et al. (2015), A&A 584, A91, Table A.2. Units are as published and
    are not uniform: masses in solar masses, radii in pc, temperatures in K,
    volume densities in 10^4 cm^-3, column densities in 10^21 cm^-2. See
    the README beside it for the full column list.

    Returns
    -------
    ndarray
        Structured array with one record per core. Access columns by name, for
        example cores["Mcore"], cores["Tdust"], cores["nH2avd"],
        cores["Coretype"].
    """
    path = os.path.join(DATA_DIR, "ps1", "herschel_core_catalog.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Herschel core catalog not found at {path}.\n"
            f"See the README beside it for what this file should contain and "
            f"where it comes from. If it is missing from your clone, pull the "
            f"latest version of the repository."
        )
    return np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")


def _load_table(filename, description):
    """Load a CSV with a header line into a structured array."""
    path = os.path.join(DATA_DIR, *filename.split("/"))
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"{description} not found at {path}.\n"
            f"See the README beside it for what this file should contain and "
            f"where it comes from. If it is missing from your clone, pull the "
            f"latest version of the repository."
        )
    return np.genfromtxt(path, delimiter=",", names=True, dtype=None, encoding="utf-8")


def load_planet_elements():
    """Orbital elements and bulk properties of the eight planets.

    JPL Solar System Dynamics. Columns: name, a_au, e, mass_kg, radius_m.

    Returns
    -------
    ndarray
        Structured array, one record per planet.

    Notes
    -----
    radius_m is the VOLUMETRIC MEAN radius, so a mean density computed as
    M / (4/3 pi R^3) is the true mean density. Ring and satellite distances are
    conventionally quoted in equatorial radii instead, which for Saturn is 3.5%
    larger; convert those to metres before using them.
    """
    return _load_table("ps2/planet_elements.csv", "Planetary elements")


def load_satellites():
    """Mean elements of the 451 known satellites of the giant planets.

    JPL Solar System Dynamics, Planetary Satellite Mean Elements. Columns:
    planet, name, a_m, e, i_deg, direction. Semi-major axes are planetocentric
    and in metres, so a_m divided by a Hill radius needs no conversion.

    Returns
    -------
    ndarray
        Structured array, one record per satellite.

    Notes
    -----
    direction is retrograde where the tabulated inclination exceeds 90 degrees.
    The reference plane is not the same for every satellite: regular satellites
    are referred to the local Laplace plane or the planet's equator, irregular
    satellites to the ecliptic. Prograde and retrograde are therefore measured
    against the planet's spin for the regulars and against its heliocentric
    orbit for the irregulars, which is the sense that matters for each. It does
    mean the Uranian regulars come out prograde even though Uranus is tipped by
    98 degrees.

    These are mean elements fitted to integrated orbits, not an ephemeris. Many
    irregulars have apoapsis a(1 + e) well beyond a.
    """
    return _load_table("ps2/satellites.csv", "Satellite catalog")

