"""
The two-body problem: right-hand sides, initial conditions, and diagnostics.

Complete -- nothing to implement here. This module exists so that Problem Set 1
stage B is about the integration scheme and nothing else.

State vector convention, used by every integrator in this course:

    y = [x, y, vx, vy]

for a test particle orbiting a fixed mass at the origin, in the orbital plane.
Week 9 generalises this to N bodies in 3D; the convention does not change.
"""

import numpy as np

from astrotools import constants as c


def kepler_acceleration(t, y, gm=c.GM_SUN):
    """Acceleration of a test particle in a fixed point-mass potential.

    Parameters
    ----------
    t : float
        Time [s]. Unused -- the potential is static -- but kept in the signature
        so that acceleration and derivative functions are interchangeable.
    y : ndarray, shape (4,)
        State vector [x, y, vx, vy] in SI.
    gm : float, optional
        Gravitational parameter G*M of the central body [m^3 s^-2].

    Returns
    -------
    ndarray, shape (2,)
        Acceleration [ax, ay] [m s^-2].
    """
    r_vec = y[:2]
    r = np.sqrt(r_vec[0] ** 2 + r_vec[1] ** 2)
    return -gm * r_vec / r ** 3


def kepler_derivs(t, y, gm=c.GM_SUN):
    """Time derivative of the two-body state vector.

    This is the ``func`` argument that euler_step and rk4_step expect.

    Returns
    -------
    ndarray, shape (4,)
        [vx, vy, ax, ay].
    """
    return np.concatenate((y[2:], kepler_acceleration(t, y, gm)))


def orbital_period(a, gm=c.GM_SUN):
    """Kepler's third law: P = 2 pi sqrt(a^3 / GM). Returns seconds."""
    return 2.0 * np.pi * np.sqrt(a ** 3 / gm)


def initial_conditions(a, e, gm=c.GM_SUN):
    """State vector at pericentre for an orbit of given a and e.

    Starting at pericentre puts the fastest, most demanding part of the orbit at
    step zero, which is what you want when testing an integrator.

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
