"""
Viscous evolution of a thin disk.  ASTR 5820.

You implement one function: step. The grid, the boundary conditions, the
analytic reference solutions, the timestep limit and the driver all ship
complete, so the only thing you write is the finite-difference update itself.

THE EQUATION
------------
Mass and angular-momentum conservation in a thin Keplerian disk give

    dSigma/dt = (3/r) d/dr [ r^(1/2) d/dr ( nu Sigma r^(1/2) ) ].

Written for the mass in an annulus rather than for Sigma, the same equation
says that the mass in a cell changes only by what flows through its two faces,

    dM_i/dt = Mdot(i+1/2) - Mdot(i-1/2),
    Mdot    = 6 pi r^(1/2) d/dr ( nu Sigma r^(1/2) ),

with Mdot positive INWARD. Differencing that form conserves mass to roundoff
on any grid, which a direct difference of the first form does not.

THE GRID
--------
Cells are spaced evenly in log r between r_in and r_out. Each cell i has a
center grid.r[i], faces grid.r_face[i] and grid.r_face[i+1], and area
grid.area[i] = pi (r_face[i+1]^2 - r_face[i]^2). One ghost center sits beyond
each end, at the same logarithmic spacing: grid.r_pad holds all n + 2 centers.

THE BOUNDARY CONDITIONS
-----------------------
nu Sigma = 0 at both ghost centers. At the inner edge this is the zero-torque
condition: gas reaching r_in is accreted by the star and exerts no torque on the
disk outside it. At the outer edge it lets mass leave freely; put r_out far
enough out that none of consequence does. pad_with_boundaries() applies both.
"""

from collections import namedtuple

import numpy as np
from scipy.special import ive

from astrotools import constants as c


Grid = namedtuple("Grid", ["r", "r_face", "r_pad", "area", "n"])


# =====================================================================
# Supplied
# =====================================================================

def make_grid(r_in, r_out, n):
    """Log-spaced grid of n cells between r_in and r_out. Supplied.

    Returns
    -------
    Grid
        r (n,) cell centers; r_face (n+1,) faces; r_pad (n+2,) centers with one
        ghost at each end; area (n,) annulus areas [m^2]; n.
    """
    r_face = np.geomspace(r_in, r_out, n + 1)
    r = np.sqrt(r_face[1:] * r_face[:-1])
    ratio = r_face[1] / r_face[0]
    r_pad = np.concatenate(([r[0] / ratio], r, [r[-1] * ratio]))
    area = np.pi * (r_face[1:] ** 2 - r_face[:-1] ** 2)
    return Grid(r, r_face, r_pad, area, n)


def pad_with_boundaries(q):
    """Append the boundary values to a cell-centered array of nu*Sigma*r^(1/2).

    Supplied. Returns an array of length n + 2 matching grid.r_pad, with zeros
    in the two ghost cells.
    """
    return np.concatenate(([0.0], np.asarray(q, dtype=float), [0.0]))


def cfl_timestep(grid, nu, safety=0.5):
    """Largest stable explicit timestep, times a safety factor. Supplied.

    To leading order the equation is a diffusion equation in r with diffusion
    coefficient 3 nu, so an explicit scheme is stable only for
    dt < (Delta r)^2 / (6 nu) in every cell, roughly. On a log grid Delta r is
    smallest at the inner edge, which is where this limit is set. The estimate
    here uses the center-to-center spacing and is conservative: the true limit
    on a log grid lies somewhat above it.

    Parameters
    ----------
    grid : Grid
    nu : ndarray, shape (n,)
        Kinematic viscosity at the cell centers [m^2 s^-1].
    safety : float, optional
        Fraction of the limit to return.

    Returns
    -------
    float
        Timestep [s].
    """
    dr = np.diff(grid.r_pad)[:-1]           # spacing to the inner neighbor
    return safety * np.min(dr**2 / (6.0 * np.asarray(nu)))


def disk_mass(sigma, grid):
    """Total mass on the grid [kg]. Supplied."""
    return np.sum(sigma * grid.area)


def angular_momentum(sigma, grid, m_star=c.M_SUN):
    """Total angular momentum on the grid, sum of M_i sqrt(G M r_i). Supplied."""
    return np.sum(sigma * grid.area * np.sqrt(c.G * m_star * grid.r))


def alpha_viscosity(r, alpha, T_func, m_star=c.M_SUN, mu=c.MU_DISK):
    """Shakura-Sunyaev viscosity, nu = alpha c_s H = alpha c_s^2 / Omega. Supplied.

    For T proportional to r^(-1/2) this gives nu proportional to r.

    Returns
    -------
    ndarray
        [m^2 s^-1].
    """
    r = np.asarray(r, dtype=float)
    cs2 = c.K_B * T_func(r) / (mu * c.M_H)
    omega = np.sqrt(c.G * m_star / r**3)
    return alpha * cs2 / omega


def ring_solution(r, t, m, r0, nu):
    """Lynden-Bell & Pringle Green's function for constant nu. Supplied.

    A ring of mass m placed at r0 at t = 0 has, at time t,

        Sigma = m / (pi r0^2 tau) x^(-1/4) exp(-(1 + x^2)/tau) I_{1/4}(2x/tau),

    with x = r / r0 and tau = 12 nu t / r0^2. The exponentially scaled Bessel
    function is used so that small tau does not overflow.

    Returns
    -------
    ndarray
        Sigma [kg m^-2].
    """
    x = np.asarray(r, dtype=float) / r0
    tau = 12.0 * nu * t / r0**2
    z = 2.0 * x / tau
    # I_{1/4}(z) = ive(1/4, z) * exp(z), folded into the exponent
    return (m / (np.pi * r0**2 * tau) * x**-0.25
            * np.exp(-(1.0 + x**2) / tau + z) * ive(0.25, z))


def similarity_solution(r, t, m0, r1, nu1, gamma=1.0):
    """Lynden-Bell & Pringle self-similar disk, nu = nu1 (r/r1)^gamma. Supplied.

    Normalized to an initial disk mass m0 rather than to Armitage's constant C,
    which is related by C = 3 (2 - gamma) nu1 m0 / (2 r1^2). With
    T = 1 + t/t_s and t_s = r1^2 / (3 (2 - gamma)^2 nu1),

        Sigma = C / (3 pi nu1 x^gamma) T^(-(5/2 - gamma)/(2 - gamma))
                * exp(-x^(2 - gamma) / T),            x = r / r1.

    Returns
    -------
    ndarray
        Sigma [kg m^-2].
    """
    x = np.asarray(r, dtype=float) / r1
    ts = r1**2 / (3.0 * (2.0 - gamma) ** 2 * nu1)
    T = 1.0 + t / ts
    C = 3.0 * (2.0 - gamma) * nu1 * m0 / (2.0 * r1**2)
    return (C / (3.0 * np.pi * nu1 * x**gamma)
            * T ** (-(2.5 - gamma) / (2.0 - gamma))
            * np.exp(-x ** (2.0 - gamma) / T))


def evolve(sigma0, grid, nu, t_end, dt, n_out=200):
    """Advance Sigma from t = 0 to t_end with your step(). Supplied.

    The number of steps is chosen so the run lands exactly on t_end, with dt
    reduced by less than one part in n_steps to make it do so.

    Parameters
    ----------
    sigma0 : ndarray, shape (n,)
        Initial surface density [kg m^-2].
    grid : Grid
    nu : ndarray, shape (n,)
        Viscosity at the cell centers [m^2 s^-1].
    t_end : float
        [s].
    dt : float
        Requested timestep [s].
    n_out : int, optional
        Number of evenly spaced snapshots after the initial one.

    Returns
    -------
    t : ndarray, shape (n_out + 1,)
        Snapshot times [s].
    sigma : ndarray, shape (n_out + 1, n)
        Surface density at each snapshot.
    mass : ndarray, shape (n_out + 1,)
        Disk mass at each snapshot [kg]. -d(mass)/dt is the accretion rate onto
        the star, provided nothing is lost through the outer boundary.
    """
    n_steps = max(1, int(np.ceil(t_end / dt)))
    dt = t_end / n_steps
    out_at = set(np.round(np.linspace(0, n_steps, n_out + 1)).astype(int))

    sigma = np.asarray(sigma0, dtype=float).copy()
    t_list, s_list = [0.0], [sigma.copy()]
    for k in range(1, n_steps + 1):
        sigma = step(sigma, grid, nu, dt)
        if k in out_at:
            t_list.append(k * dt)
            s_list.append(sigma.copy())

    s_arr = np.array(s_list)
    return np.array(t_list), s_arr, s_arr @ grid.area


# =====================================================================
# You implement this
# =====================================================================

def step(sigma, grid, nu, dt):
    """Advance the surface density by one explicit (forward Euler) step.

    Parameters
    ----------
    sigma : ndarray, shape (n,)
        Surface density at the cell centers [kg m^-2].
    grid : Grid
    nu : ndarray, shape (n,)
        Kinematic viscosity at the cell centers [m^2 s^-1].
    dt : float
        Timestep [s]. Must satisfy the CFL limit; see cfl_timestep().

    Returns
    -------
    ndarray, shape (n,)
        Surface density at t + dt.

    Notes
    -----
    1. Form q = nu Sigma r^(1/2) at the cell centers and pad it with the
       boundary values.
    2. At each of the n + 1 faces, difference q between the two neighboring
       centers to get Mdot = 6 pi r_face^(1/2) dq/dr.
    3. Update the mass in each cell by the difference of its two face fluxes,
       and divide by the cell area.

    Return a new array rather than writing into sigma.
    """
    raise NotImplementedError("PS3, section 1")
