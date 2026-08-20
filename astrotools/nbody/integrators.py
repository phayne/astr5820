"""
Integration schemes.  ASTR 5820, Problem Set 1, stage B (and Set 4).

You implement one function: rk4_step. Euler ships complete as the comparator, and
the driver that loops over steps is provided, so the only thing you write is the
scheme itself.

    pytest tests/test_ps1b_integrators.py -v

STEPPER CONVENTION
------------------
Every stepper has the signature

    stepper(func, t, y, dt) -> y_new

where ``func(t, y)`` returns dy/dt. Week 9's leapfrog uses the same signature but
takes an ACCELERATION function instead, since a symplectic scheme has to see
positions and velocities separately. The driver below does not care which.

WHAT THE TEST IS CHECKING
-------------------------
Integrate exactly one orbital period and the exact answer is the initial
condition -- so the distance between the final and initial states IS the global
error, with no reference solution needed. Euler's global error should fall by 2
when dt is halved; a fourth-order scheme's should fall by 16. That factor of 16
is the inference you made in Lecture 7 from the Euler and midpoint amplification
factors, and this test is where it is checked.
"""

import numpy as np


def euler_step(func, t, y, dt):
    """One step of the forward Euler method. Complete -- your comparator.

    Amplification factor R(z) = 1 + z, matching exp(z) through the linear term.
    Local error O(dt^2), global error O(dt): first order.
    """
    return y + dt * np.asarray(func(t, y))


def rk4_step(func, t, y, dt):
    """One step of the classical four-stage Runge-Kutta method.

    Parameters
    ----------
    func : callable
        func(t, y) -> dy/dt, returning an array the same shape as y.
    t : float
        Current time [s].
    y : ndarray
        Current state vector.
    dt : float
        Step size [s].

    Returns
    -------
    ndarray
        State at t + dt.

    Notes
    -----
    Four stages: the slope at the start, twice at the midpoint, once at the end,
    combined with weights 1/6, 1/3, 1/3, 1/6. Amplification factor

        R(z) = 1 + z + z^2/2 + z^3/6 + z^4/24,

    matching exp(z) through z^4, so the global error is O(dt^4).
    """
    raise NotImplementedError("PS1 stage B")


def integrate(stepper, func, y0, t_span, dt, store_every=1):
    """Fixed-step integration driver. Complete -- provided.

    The number of steps is chosen so the integration lands exactly on t_end, and
    dt is adjusted by less than one part in n_steps to make it do so. Exact
    landing matters for the convergence test, which compares the state after a
    whole number of orbits.

    Parameters
    ----------
    stepper : callable
        One of euler_step, rk4_step, (later) leapfrog_step.
    func : callable
        Passed straight through to the stepper.
    y0 : array_like
        Initial state vector.
    t_span : tuple of float
        (t_start, t_end) [s].
    dt : float
        Requested step size [s]; rounded to divide the interval evenly.
    store_every : int, optional
        Store every Nth state. Use a large value for long integrations -- Week 9
        runs 1e5 orbits and you do not want all of it in memory.

    Returns
    -------
    t : ndarray, shape (M,)
        Times of the stored states [s].
    y : ndarray, shape (M, len(y0))
        Stored states.
    """
    t_start, t_end = t_span
    n_steps = max(1, int(round((t_end - t_start) / dt)))
    dt = (t_end - t_start) / n_steps

    y = np.asarray(y0, dtype=float).copy()
    t = float(t_start)

    t_out = [t]
    y_out = [y.copy()]

    for i in range(1, n_steps + 1):
        y = np.asarray(stepper(func, t, y, dt), dtype=float)
        t = t_start + i * dt
        if i % store_every == 0 or i == n_steps:
            t_out.append(t)
            y_out.append(y.copy())

    return np.array(t_out), np.array(y_out)


# Week 9 (Set 4) adds:
#
#     def leapfrog_step(accel, t, y, dt): ...
#
# Kick-drift-kick, second order, symplectic. It slots into integrate() unchanged.
