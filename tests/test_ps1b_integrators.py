"""
Problem Set 1, stage B -- nbody/integrators.py.

The convergence test is the one that matters. Integrating exactly one orbital
period, the exact final state is the initial state, so the distance between them
is the global error with no reference solution required. Halve the step and a
first-order scheme improves by 2; a fourth-order scheme improves by 16.

    pytest tests/test_ps1b_integrators.py -v
"""

import numpy as np
import pytest

from astrotools import constants as c
from astrotools.nbody import integrators, twobody

A_TEST = 1.0 * c.AU
E_TEST = 0.3
PERIOD = twobody.orbital_period(A_TEST)


def _global_error(stepper, n_steps):
    """Position error after exactly one orbit, in units of the semi-major axis."""
    y0 = twobody.initial_conditions(A_TEST, E_TEST)
    _, y = integrators.integrate(
        stepper, twobody.kepler_derivs, y0, (0.0, PERIOD), PERIOD / n_steps
    )
    return np.linalg.norm(y[-1, :2] - y0[:2]) / A_TEST


def _convergence_ratio(stepper, n_steps=2000):
    return _global_error(stepper, n_steps) / _global_error(stepper, 2 * n_steps)


# ------------------------------------------------- the scheme is right


def test_rk4_step_matches_the_exponential_through_fourth_order():
    """Apply the scheme to y' = lambda*y and recover R(z) = 1+z+z^2/2+z^3/6+z^4/24.

    This is the amplification factor you inferred in Lecture 7, tested directly.
    """
    z = 0.1
    y_new = integrators.rk4_step(lambda t, y: y, 0.0, np.array([1.0]), z)
    expected = 1 + z + z ** 2 / 2 + z ** 3 / 6 + z ** 4 / 24
    assert abs(y_new[0] - expected) < 1e-12


def test_rk4_step_is_exact_for_a_constant_slope():
    y_new = integrators.rk4_step(lambda t, y: np.array([2.0]), 0.0, np.array([0.0]), 3.0)
    assert abs(y_new[0] - 6.0) < 1e-12


def test_rk4_step_does_not_mutate_its_input():
    """A stepper that writes into y in place will silently corrupt the driver."""
    y = np.array([1.0, 2.0, 3.0, 4.0])
    y_copy = y.copy()
    integrators.rk4_step(twobody.kepler_derivs, 0.0, y * c.AU, 1.0)
    assert np.array_equal(y, y_copy)


# --------------------------------------------------- order of accuracy


def test_euler_is_first_order():
    """The comparator. Halving dt should roughly halve the error."""
    ratio = _convergence_ratio(integrators.euler_step)
    assert 1.7 < ratio < 2.3, f"Euler convergence ratio {ratio:.2f}, expected ~2"


def test_rk4_is_fourth_order():
    """THE test for this set: sixteenfold error reduction per halving of dt."""
    ratio = _convergence_ratio(integrators.rk4_step)
    assert 13.0 < ratio < 19.0, (
        f"RK4 convergence ratio {ratio:.2f}, expected ~16. A ratio near 8 means "
        "one stage is misweighted; near 2 means the scheme has collapsed to Euler."
    )


def test_rk4_beats_euler_at_equal_cost():
    """Four times as many Euler steps, for the same number of force evaluations,
    still loses -- and by a wide margin."""
    assert _global_error(integrators.rk4_step, 500) < _global_error(
        integrators.euler_step, 2000
    )


# ------------------------------------------------------ conserved quantities


def test_rk4_conserves_angular_momentum_to_machine_precision():
    """Angular momentum is conserved by the geometry of a central force, not by
    the scheme, so RK4 holds it far better than it holds energy. Noticing this
    asymmetry is the point of the Week 4 diagnostics."""
    y0 = twobody.initial_conditions(A_TEST, E_TEST)
    _, y = integrators.integrate(
        integrators.rk4_step, twobody.kepler_derivs, y0, (0.0, 20 * PERIOD), PERIOD / 2000
    )
    drift = twobody.relative_drift(twobody.specific_angular_momentum(y))
    assert np.max(np.abs(drift)) < 1e-10


def test_rk4_energy_error_grows_with_time():
    """RK4 is accurate but not symplectic: its energy error accumulates rather
    than oscillating. Ten times the integration is more than ten times the error.
    This is the observation that motivates leapfrog in Week 9."""
    y0 = twobody.initial_conditions(A_TEST, E_TEST)
    errors = []
    for n_orbits in (10, 100):
        _, y = integrators.integrate(
            integrators.rk4_step,
            twobody.kepler_derivs,
            y0,
            (0.0, n_orbits * PERIOD),
            PERIOD / 200,
            store_every=200,
        )
        errors.append(abs(twobody.relative_drift(twobody.specific_energy(y))[-1]))
    assert errors[1] > 5 * errors[0]
