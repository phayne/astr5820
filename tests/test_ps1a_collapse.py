"""
Problem Set 1, stage A -- cloud/collapse.py.

Two kinds of test here. The value tests check that your fiducial numbers agree
with the lecture notes to 1%. The scaling tests check that the functions behave
correctly when the inputs change, which is what catches a dropped mu or a
mistaken power -- errors that a single value test can miss.

    pytest tests/test_ps1a_collapse.py -v
"""

import numpy as np
import pytest

from astrotools import constants as c
from astrotools.cloud import collapse

RHO_CORE = collapse.number_density_to_mass_density(c.N_H2_CORE)

# Reference values for the fiducial core, computed from the constants in
# astrotools/constants.py. Lecture 2 quotes 1.7 M_sun and ~1.1e5 yr; Lecture 3
# quotes ~260 AU. The tolerance is 1%.
M_J_REF = 1.700 * c.M_SUN         # kg
T_FF_REF = 1.066e5 * c.YR         # s
R_C_REF = 257.0 * c.AU            # m

TOL = 0.01


def _frac(value, reference):
    return abs(value - reference) / reference


# ---------------------------------------------------------------- values


def test_mass_density_of_fiducial_core():
    """rho = n(H2) * mu * m_H, not n(H2) * m_H."""
    assert _frac(RHO_CORE, 3.899e-16) < TOL


def test_jeans_mass_fiducial():
    m_j = collapse.jeans_mass(c.T_CORE, RHO_CORE)
    assert _frac(m_j, M_J_REF) < TOL, (
        f"got {m_j / c.M_SUN:.3f} M_sun, expected {M_J_REF / c.M_SUN:.3f}. "
        "If you are off by a factor of about 1.5, check mu."
    )


def test_free_fall_time_fiducial():
    t_ff = collapse.free_fall_time(RHO_CORE)
    assert _frac(t_ff, T_FF_REF) < TOL, (
        f"got {t_ff / c.YR:.3e} yr, expected {T_FF_REF / c.YR:.3e}"
    )


def test_specific_angular_momentum_fiducial():
    j = collapse.specific_angular_momentum(c.OMEGA_CORE, c.R_CORE)
    assert _frac(j, 7.14e16) < TOL


def test_centrifugal_radius_fiducial():
    r_c = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE)
    assert _frac(r_c, R_C_REF) < TOL, (
        f"got {r_c / c.AU:.1f} AU, expected {R_C_REF / c.AU:.1f}"
    )


# --------------------------------------------------------------- scaling


def test_jeans_mass_scales_as_rho_to_the_minus_half():
    """M_J propto rho^(-1/2) at fixed T."""
    m1 = collapse.jeans_mass(c.T_CORE, RHO_CORE)
    m2 = collapse.jeans_mass(c.T_CORE, 100.0 * RHO_CORE)
    assert _frac(m1 / m2, 10.0) < TOL


def test_jeans_mass_scales_as_t_to_the_three_halves():
    m1 = collapse.jeans_mass(c.T_CORE, RHO_CORE)
    m2 = collapse.jeans_mass(4.0 * c.T_CORE, RHO_CORE)
    assert _frac(m2 / m1, 8.0) < TOL


def test_free_fall_time_depends_only_on_density():
    """t_ff carries no length scale -- that is why collapse is homologous."""
    t1 = collapse.free_fall_time(RHO_CORE)
    t2 = collapse.free_fall_time(4.0 * RHO_CORE)
    assert _frac(t1 / t2, 2.0) < TOL


def test_centrifugal_radius_scales_as_omega_squared():
    """A decade in rotation rate is two decades in disk radius -- the whole point
    of the Week 2 prediction."""
    r1 = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE)
    r2 = collapse.centrifugal_radius(10.0 * c.OMEGA_CORE, c.R_CORE, c.M_CORE)
    assert _frac(r2 / r1, 100.0) < TOL


def test_centrifugal_radius_scales_as_r0_to_the_fourth():
    r1 = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE)
    r2 = collapse.centrifugal_radius(c.OMEGA_CORE, 2.0 * c.R_CORE, c.M_CORE)
    assert _frac(r2 / r1, 16.0) < TOL


def test_polar_material_falls_to_the_centre():
    """The sin^4(theta) dependence is what makes this a disk, not a shell."""
    equatorial = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=np.pi / 2)
    mid = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=np.pi / 4)
    polar = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=1e-3)
    assert _frac(mid / equatorial, 0.25) < TOL      # sin^4(pi/4) = 1/4
    assert polar < 1e-6 * equatorial


# ------------------------------------------------------------ array input


def test_functions_accept_arrays():
    """The Omega sweep needs these to vectorise. If they do not, you have a
    Python loop somewhere a NumPy expression should be."""
    omegas = np.logspace(-14.5, -13.0, 25)
    radii = collapse.centrifugal_radius(omegas, c.R_CORE, c.M_CORE)
    assert radii.shape == omegas.shape
    assert np.all(np.diff(radii) > 0)


# ---------------------------------------------------------------- units


def test_units_are_si():
    """A wrong-units answer usually lands orders of magnitude away, so pin the
    magnitudes rather than the values."""
    assert 1e29 < collapse.jeans_mass(c.T_CORE, RHO_CORE) < 1e31
    assert 1e12 < collapse.free_fall_time(RHO_CORE) < 1e13
    assert 1e12 < collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE) < 1e14
