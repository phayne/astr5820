"""
The two-body problem: right-hand side, initial conditions, and diagnostics.

You implement two functions, hill_radius and roche_density. Everything else here
is complete, so that the integration work is about the scheme and nothing else.

State vector convention, used by every integrator in this course:

    y = [x, y, vx, vy]

for a test particle orbiting a fixed mass at the origin, in the orbital plane.
Everything is SI.
"""

import numpy as np

from astrotools import constants as c


def kepler_derivs(t, y, gm=c.GM_SUN):
    """Time derivative of the two-body state vector.

    This is the ``func`` argument the steppers expect.

    Parameters
    ----------
    t : float
        Time [s]. Unused -- the potential is static -- but kept in the signature
        so that any right-hand side can be passed to any stepper.
    y : ndarray, shape (4,)
        State vector [x, y, vx, vy] in SI.
    gm : float, optional
        Gravitational parameter G*M of the central body [m^3 s^-2].

    Returns
    -------
    ndarray, shape (4,)
        [vx, vy, ax, ay].
    """
    r = np.sqrt(y[0] ** 2 + y[1] ** 2)
    return np.array([y[2], y[3], -gm * y[0] / r ** 3, -gm * y[1] / r ** 3])


def orbital_period(a, gm=c.GM_SUN):
    """Kepler's third law: P = 2 pi sqrt(a^3 / GM). Returns seconds."""
    return 2.0 * np.pi * np.sqrt(a ** 3 / gm)


def initial_conditions(a, e, gm=c.GM_SUN):
    """State vector at pericentre for an orbit of given a and e.

    Starting at pericentre puts the fastest, most demanding part of the orbit at
    step zero, which is what you want when testing an integrator. The particle
    returns to this exact state after one period, so the distance between the
    final and initial positions is the global error of a one-period run.

    Parameters
    ----------
    a : float
        Semi-major axis [m].
    e : float
        Eccentricity, 0 <= e < 1.
    gm : float, optional
        Gravitational parameter [m^3 s^-2].

    Returns
    -------
    ndarray, shape (4,)
        [x, y, vx, vy] with the particle on the +x axis moving in +y.
    """
    r_peri = a * (1.0 - e)
    v_peri = np.sqrt(gm * (2.0 / r_peri - 1.0 / a))   # vis-viva
    return np.array([r_peri, 0.0, 0.0, v_peri])


def specific_energy(y, gm=c.GM_SUN):
    """Specific orbital energy v^2/2 - GM/r [J kg^-1]. Accepts (4,) or (N, 4)."""
    y = np.atleast_2d(y)
    r = np.sqrt(y[:, 0] ** 2 + y[:, 1] ** 2)
    v2 = y[:, 2] ** 2 + y[:, 3] ** 2
    return np.squeeze(0.5 * v2 - gm / r)


def specific_angular_momentum(y):
    """Specific angular momentum x*vy - y*vx [m^2 s^-1]. Accepts (4,) or (N, 4)."""
    y = np.atleast_2d(y)
    return np.squeeze(y[:, 0] * y[:, 3] - y[:, 1] * y[:, 2])


def relative_drift(quantity):
    """Fractional departure of a conserved quantity from its initial value.

    Parameters
    ----------
    quantity : array_like, shape (N,)
        Time series of a quantity that ought to be conserved.

    Returns
    -------
    ndarray, shape (N,)
        (Q(t) - Q(0)) / |Q(0)|.
    """
    quantity = np.asarray(quantity)
    return (quantity - quantity[0]) / np.abs(quantity[0])


def hill_radius(a, m_planet, m_star=c.M_SUN, e=0.0):
    """Radius of the region in which a planet's gravity beats the star's tide.

    Parameters
    ----------
    a : float or array_like
        Semi-major axis of the planet's orbit about the star [m].
    m_planet : float or array_like
        Mass of the planet [kg].
    m_star : float or array_like, optional
        Mass of the star [kg].
    e : float or array_like, optional
        Eccentricity of the planet's orbit. The Hill radius is smallest at
        pericentre, which is what limits what the planet holds onto over many
        orbits; the default e = 0 gives the circular-orbit value.

    Returns
    -------
    float or ndarray
        Hill radius [m].

    Notes
    -----
    Earth gives r_H = 1.50e9 m = 0.0100 AU.

    Only the mass ratio matters, so both masses in kilograms and both in solar
    masses give the same answer. One of each does not.
    """
    raise NotImplementedError("PS2, section 1")


def roche_density(a, m_star=c.M_SUN):
    """Critical mean density for tidal disruption of a rigid satellite.

    A body of lower mean density than this, orbiting at distance a, is pulled
    apart: its own surface lies outside its Hill radius.

    Parameters
    ----------
    a : float or array_like
        Distance from the primary [m].
    m_star : float or array_like, optional
        Mass of the primary [kg]. For rings this is the planet, not the Sun.

    Returns
    -------
    float or ndarray
        Critical mean density [kg m^-3].

    Notes
    -----
    Saturn (M = 5.6834e26 kg) at the orbit of Mimas, a = 1.855e8 m, gives
    rho_R = 64 kg m^-3.

    There is no radius in this expression, and no property of the satellite
    other than the density being compared against.
    """
    raise NotImplementedError("PS2, section 1")
