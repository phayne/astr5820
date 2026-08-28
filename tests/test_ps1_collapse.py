"""
Problem Set 1 -- astrotools/cloud/collapse.py.

Two kinds of test here. The value tests check that your fiducial numbers agree
with the lecture notes to 1%. The scaling tests check that the functions behave
correctly when the inputs change, which is what catches a dropped mu or a
mistaken power -- errors that a single value test can miss.

    pytest tests/test_ps1_collapse.py -v
"""

import numpy as np

from astrotools import constants as c
from astrotools.cloud import collapse

# The fiducial core: T = 10 K, n(H2) = 1e11 m^-3, M = 3 M_sun, Omega = 3e-14 s^-1.
# Density and radius are derived in constants.py, not chosen independently.
RHO_CORE = c.RHO_CORE

# Reference values for the fiducial core, computed from the constants in
# astrotools/constants.py. Each is quoted, rounded, in the Lecture 2 or
# Lecture 3 summary box. The tolerance is 1%, so the references below carry
# more digits than the lectures do.
#
#   rho   = n(H2) * MU_H2 * M_H                        = 4.6859e-16 kg m^-3
#   R_0   = (3M / 4 pi rho)^(1/3)                      = 1.4485e15 m = 0.0469 pc
#   M_J   = (5 k T / (G MU_CLOUD M_H))^(3/2)
#             * (3 / (4 pi rho))^(1/2)                 = 3.0835e30 kg = 1.551 M_sun
#   t_ff  = (3 pi / 32 G rho)^(1/2)                    = 9.724e4 yr
#   j     = Omega R_0^2                                = 6.294e16 m^2 s^-1
#   R_c   = j^2 / (G M)                                = 66.52 AU
#
# MU_H2 = 2.8 converts number density to mass density; MU_CLOUD = 2.33 enters
# the sound speed inside M_J. They are different quantities. Using 2.33 for the
# density conversion makes rho low by 17% and M_J high by 10% -- close enough to
# look like rounding, which is why these references are pinned.
RHO_REF = 4.6859e-16              # kg m^-3
R_0_REF = 0.04694 * c.PC          # m
M_J_REF = 3.0835e30               # kg  = 1.551 M_sun
T_FF_REF = 9.724e4 * c.YR         # s
J_REF = 6.294e16                  # m^2 s^-1
R_C_REF = 66.52 * c.AU            # m

TOL = 0.01


def _frac(value, reference):
    return abs(value - reference) / reference


# ---------------------------------------------------------------- values


def test_mass_density_of_reference_core():
    """rho = n(H2) * MU_H2 * m_H, with MU_H2 = 2.8, not MU_CLOUD and not 1."""
    rho = collapse.number_density_to_mass_density(c.N_H2_CORE)
    assert _frac(rho, RHO_REF) < TOL
    assert _frac(rho, RHO_CORE) < TOL


def test_radius_of_reference_core():
    """Mass, density and radius are not three independent choices."""
    assert _frac(c.R_CORE, R_0_REF) < TOL


def test_jeans_mass_fiducial():
    m_j = collapse.jeans_mass(c.T_CORE, RHO_CORE)
    ratio = m_j / M_J_REF
    assert _frac(m_j, M_J_REF) < TOL, (
        f"got {m_j / c.M_SUN:.3f} M_sun, expected {M_J_REF / c.M_SUN:.3f} "
        f"(ratio {ratio:.3f}). The density is supplied here, so the error is in "
        "jeans_mass itself. Common causes:\n"
        "  ratio ~ 0.76: the sound-speed term used MU_H2 = 2.8. It needs "
        "MU_CLOUD = 2.33.\n"
        "  ratio ~ 3.56: mu was left out of the sound-speed term altogether.\n"
        "  ratio ~ 1.02: the pi-based prefactor was used. These tests use the "
        "Lecture 2, Sec. 2.3 form, not the one in Armitage Sec. 2.1."
    )


def test_reference_core_is_marginally_unstable():
    """M / M_J = 1.93 -- unstable, but only just. That is the interesting regime."""
    ratio = c.M_CORE / collapse.jeans_mass(c.T_CORE, RHO_CORE)
    assert _frac(ratio, 1.935) < TOL, f"got M/M_J = {ratio:.2f}, expected 1.93"


def test_free_fall_time_fiducial():
    t_ff = collapse.free_fall_time(RHO_CORE)
    assert _frac(t_ff, T_FF_REF) < TOL, (
        f"got {t_ff / c.YR:.3e} yr, expected {T_FF_REF / c.YR:.3e}. "
        "The coefficient is sqrt(3 pi / 32) = 0.54."
    )


def test_specific_angular_momentum_fiducial():
    j = collapse.specific_angular_momentum(c.OMEGA_CORE, c.R_CORE)
    assert _frac(j, J_REF) < TOL, (
        f"got {j:.3e} m^2 s^-1, expected {J_REF:.3e}. "
        "Omega must be in s^-1; velocity gradients quoted in km/s/pc need "
        "constants.omega_from_velocity_gradient()."
    )


def test_centrifugal_radius_fiducial():
    r_c = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE)
    assert _frac(r_c, R_C_REF) < TOL, (
        f"got {r_c / c.AU:.1f} AU, expected {R_C_REF / c.AU:.1f}. "
        "Since R_c goes as Omega^2, an error in Omega is squared here."
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


def test_specific_angular_momentum_scales_as_r_squared():
    j1 = collapse.specific_angular_momentum(c.OMEGA_CORE, c.R_CORE)
    j2 = collapse.specific_angular_momentum(c.OMEGA_CORE, 3.0 * c.R_CORE)
    assert _frac(j2 / j1, 9.0) < TOL


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


def test_polar_material_falls_to_the_center():
    """The sin^4(theta) dependence is what makes this a disk, not a shell."""
    equatorial = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=np.pi / 2)
    mid = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=np.pi / 4)
    polar = collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE, theta=1e-3)
    assert _frac(mid / equatorial, 0.25) < TOL      # sin^4(pi/4) = 1/4
    assert polar < 1e-6 * equatorial


# ------------------------------------------------------------ array input


def test_functions_accept_arrays():
    """You will evaluate these over a whole catalog and over a range of
    thresholds. If they do not vectorize, you have a Python loop somewhere a
    NumPy expression should be."""
    temperatures = np.linspace(8.0, 20.0, 25)
    densities = np.logspace(-16.5, -14.5, 25)

    m_j = collapse.jeans_mass(temperatures, densities)
    assert m_j.shape == temperatures.shape

    t_ff = collapse.free_fall_time(densities)
    assert t_ff.shape == densities.shape
    assert np.all(np.diff(t_ff) < 0)

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
    assert 1e16 < collapse.specific_angular_momentum(c.OMEGA_CORE, c.R_CORE) < 1e17
    assert 1e12 < collapse.centrifugal_radius(c.OMEGA_CORE, c.R_CORE, c.M_CORE) < 1e14
