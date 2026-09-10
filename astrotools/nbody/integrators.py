"""
Integration schemes.  ASTR 5820.

You implement one function: rk4_step. Euler ships complete as the comparator, and
the driver that loops over steps is provided, so the only thing you write is the
scheme itself.

STEPPER CONVENTION
------------------
Every stepper has the signature

    stepper(func, t, y, dt) -> y_new

where ``func(t, y)`` returns dy/dt and y is a 1-D state vector. The driver does
not know or care which stepper it is calling, so a new scheme written to this
signature works with everything here as soon as it exists.

HOW TO CHECK A SCHEME
---------------------
Integrate exactly one orbital period and the exact answer is the initial
condition, so the distance between the final and initial states IS the global
error, with no reference solution needed. Halving dt should divide Euler's
global error by 2 and a fourth-order scheme's by 16.
"""

import numpy as np


def euler_step(func, t, y, dt):
    """One step of the forward Euler method. Complete -- your comparator.

    Follows the slope at the current state for a whole step. Local error
    O(dt^2), global error O(dt): first order.

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
    combined with weights 1/6, 1/3, 1/3, 1/6. Global error O(dt^4).

    Return a new array rather than writing into y. The driver keeps the states
    you return, and an in-place update would leave every stored step pointing at
    the same array.
    """
    raise NotImplementedError("PS2, section 1")


def integrate(stepper, func, y0, t_span, dt, store_every=1):
    """Fixed-step integration driver. Complete -- provided.

    The number of steps is chosen so the integration lands exactly on t_end, and
    dt is adjusted by less than one part in n_steps to make it do so. Exact
    landing matters for the convergence test, which compares the state after a
    whole number of orbits.

    Parameters
    ----------
    stepper : callable
        Any function following the stepper convention above.
    func : callable
        Passed straight through to the stepper.
    y0 : array_like
        Initial state vector.
    t_span : tuple of float
        (t_start, t_end) [s].
    dt : float
        Requested step size [s]; rounded to divide the interval evenly.
    store_every : int, optional
        Store every Nth state. Set it to the number of steps per orbit to get
        one sample per orbit, which is all a long run needs and far less memory
        than keeping every step.

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
