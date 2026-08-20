"""
Cloud collapse and disk formation.  ASTR 5820, Problem Set 1, stage A.

Three functions. Each one is a formula you derived in Lectures 2-3; the work here
is getting the units right, not inventing the physics.

    Jeans mass          M_J = (5 k_B T / (G mu m_H))^(3/2) * (3 / (4 pi rho))^(1/2)
    Free-fall time      t_ff = sqrt(3 pi / (32 G rho))
    Centrifugal radius  R_c = j^2 / (G M),  with j = Omega R^2 for equatorial material

Run the tests with:      pytest tests/test_ps1a_collapse.py -v

Two unit traps account for most of the failures on this set:
  1. Mass density is not number density: rho = n(H2) * mu * m_H. Dropping mu gives
     an M_J wrong by sqrt(2.33) -- close enough to look like rounding.
  2. Velocity gradients are quoted in km/s/pc; Omega is needed in s^-1. Use
     constants.omega_from_velocity_gradient.
"""

import numpy as np

from astrotools import constants as c


def number_density_to_mass_density(n_h2, mu=c.MU_CLOUD):
    """Convert H2 number density to mass density.

    Provided for you -- this is the conversion that trips up stage A, so it is
    written once, here, and imported everywhere else.

    Parameters
    ----------
    n_h2 : float or array_like
        H2 number density [m^-3].
    mu : float, optional
        Mean molecular weight per hydrogen-atom mass (2.33 for cloud material).

    Returns
    -------
    float or ndarray
        Mass density [kg m^-3].
    """
    return n_h2 * mu * c.M_H


def jeans_mass(temperature, density, mu=c.MU_CLOUD):
    """Jeans mass of a uniform, isothermal, self-gravitating sphere.

    Parameters
    ----------
    temperature : float or array_like
        Gas temperature [K].
    density : float or array_like
        MASS density [kg m^-3]. Use number_density_to_mass_density() if you are
        starting from n(H2).
    mu : float, optional
        Mean molecular weight per hydrogen-atom mass.

    Returns
    -------
    float or ndarray
        Jeans mass [kg].

    Notes
    -----
    Fiducial core (T = 10 K, n(H2) = 1e11 m^-3): M_J = 1.70 M_sun.
    The prefactor is convention-dependent; use the form given in Lecture 2 so
    your answer and the test agree.
    """
    raise NotImplementedError("PS1 stage A, question 1")


def free_fall_time(density):
    """Free-fall collapse time of a uniform sphere.

    Parameters
    ----------
    density : float or array_like
        MASS density [kg m^-3].

    Returns
    -------
    float or ndarray
        Free-fall time [s].

    Notes
    -----
    Fiducial core: t_ff = 1.066e5 yr. Note what the result does NOT depend on --
    the test checks that too.
    """
    raise NotImplementedError("PS1 stage A, question 2")


def specific_angular_momentum(omega, radius):
    """Specific angular momentum of equatorial material in solid-body rotation.

    Parameters
    ----------
    omega : float or array_like
        Angular frequency [s^-1].
    radius : float or array_like
        Cylindrical radius of the parcel [m].

    Returns
    -------
    float or ndarray
        Specific angular momentum [m^2 s^-1].
    """
    raise NotImplementedError("PS1 stage A, question 3")


def centrifugal_radius(omega, radius, mass, theta=np.pi / 2):
    """Radius at which infalling material is halted by centrifugal support.

    Parameters
    ----------
    omega : float or array_like
        Core angular frequency [s^-1].
    radius : float or array_like
        Initial (spherical) radius of the parcel [m].
    mass : float or array_like
        Enclosed mass [kg].
    theta : float, optional
        Polar angle of the parcel's starting position [rad]. The default,
        pi/2, is equatorial material, which lands farthest out and sets the
        disk's outer edge.

    Returns
    -------
    float or ndarray
        Landing radius [m].

    Notes
    -----
    Fiducial core (Omega = 3e-14 s^-1, R_0 = 0.05 pc, M = 1 M_sun):
    R_c = 257 AU (quoted as ~260 AU in Lecture 3).

    The sin^4(theta) dependence is what makes this a disk rather than a shell.
    Use GM_SUN rather than G * M_SUN when the mass is exactly one solar mass.
    """
    raise NotImplementedError("PS1 stage A, question 3")
