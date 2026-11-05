"""
Gas drag in the frame rotating with a planet.  ASTR 5820.

You implement one function: hill_drag_derivs. The initial conditions and the
encounter driver are supplied.

UNITS AND FRAME
---------------
Everything here is dimensionless. Lengths are in units of the planet's Hill
radius r_H = a (M / 3 M_star)^(1/3), times in units of 1/Omega_K, and velocities
in units of Omega_K r_H. In these units GM = 3 for the planet.

The origin is on the planet, x points radially away from the star, and y points
in the direction of orbital motion. The state vector follows the course
convention,

    y = [x, y, vx, vy].

The gas moves with the Keplerian shear less the headwind dv (in units of
Omega_K r_H), u = (0, -1.5 x - dv), and its perturbation by the planet is
neglected. A pebble with Stokes number st feels a drag acceleration
-(v - u) / st.

STEPPER CONVENTION
------------------
hill_drag_derivs(t, y, st, dv) returns dy/dt. Wrap it in a lambda, for example
``func = lambda t, y: hill_drag_derivs(t, y, 0.1, 0.41)``, to pass it to any
stepper in integrators.py.
"""

import numpy as np

GM_HILL = 3.0      # GM of the planet in Hill units
L_START = 12.0     # pebbles start this many Hill radii upstream


def hill_drag_derivs(t, y, st, dv):
    """Time derivative of the state of a pebble near a planet, with gas drag.

    Parameters
    ----------
    t : float
        Time [1/Omega_K]. Unused, kept for the stepper convention.
    y : ndarray, shape (4,)
        State [x, y, vx, vy] in Hill units.
    st : float
        Stokes number of the pebble.
    dv : float
        Headwind in units of Omega_K r_H.

    Returns
    -------
    ndarray, shape (4,)
        [vx, vy, ax, ay].

    Notes
    -----
    With the planet removed, a pebble started with the velocity returned by
    initial_state keeps its radial velocity, the drift velocity
    -2 st dv / (1 + st^2), while its azimuthal velocity follows the shear.
    """
    raise NotImplementedError("PS4, section 1")


def initial_state(x0, st, dv):
    """State of a pebble entering the region upstream, drifting with the gas.

    The pebble starts at radial offset x0, L_START Hill radii upstream of the
    planet, with the steady drift velocity it has far from the planet. Pebbles
    outside the radius at which the gas moves with the planet start at +L_START
    and move in -y; those inside start at -L_START and move in +y.

    Returns
    -------
    ndarray, shape (4,)
    """
    vx = -2.0 * st * dv / (1.0 + st ** 2)
    vy = -1.5 * x0 - dv / (1.0 + st ** 2)
    y0 = L_START if vy < 0 else -L_START
    return np.array([x0, y0, vx, vy])


def encounter(stepper, func, y0, r_cap, t_max=None, dt_max=0.02):
    """Advance a pebble until it is captured or leaves the region.

    The step is dt = min(dt_max, 0.02 r^1.5), where r is the distance from the
    planet, so that it shrinks with the local orbital time near the planet.

    Parameters
    ----------
    stepper : callable
        Any stepper from integrators.py.
    func : callable
        func(t, y) -> dy/dt.
    y0 : ndarray, shape (4,)
        Initial state, usually from initial_state.
    r_cap : float
        Capture radius [r_H].
    t_max : float, optional
        Longest integration [1/Omega_K]. Defaults to the time needed to cross
        the region twice at the initial azimuthal speed, plus 40.
    dt_max : float, optional
        Largest step [1/Omega_K].

    Returns
    -------
    captured : bool
    t : ndarray
        Times of the stored states.
    states : ndarray, shape (N, 4)
        Stored states, one per step.
    """
    y = np.asarray(y0, dtype=float).copy()
    if t_max is None:
        t_max = 2.5 * L_START / max(abs(y[3]), 0.03) + 40.0
    t = 0.0
    ts, ys = [t], [y.copy()]
    while t < t_max:
        r = np.hypot(y[0], y[1])
        dt = min(dt_max, 0.02 * r ** 1.5)
        y = np.asarray(stepper(func, t, y, dt), dtype=float)
        t += dt
        ts.append(t)
        ys.append(y.copy())
        if np.hypot(y[0], y[1]) < r_cap:
            return True, np.array(ts), np.array(ys)
        if abs(y[1]) > L_START + 0.5:
            break
    return False, np.array(ts), np.array(ys)
