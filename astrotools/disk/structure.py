"""
Disk structure and the infrared SED.  ASTR 5820.

You implement two functions: scale_height and sed. Everything else here is
supplied: the power-law surface density and temperature of the fiducial disk,
the sound speed, the Planck function, and a power-law dust opacity.

CONVENTIONS
-----------
All quantities are SI. Radii are cylindrical radii in meters. Profiles that
depend on radius are passed around as callables, f(r) -> value, so that the same
sed() works for the minimum-mass nebula, a flat reprocessing disk, a flared
disk, or anything else you can write as a function of r.

Dust opacities are per kilogram of DUST, and dust surface densities are dust
only. The dust-to-gas ratio is applied by the caller, once.
"""

import numpy as np

from astrotools import constants as c


# =====================================================================
# Supplied
# =====================================================================

def surface_density(r, sigma_1au=c.SIGMA_GAS_1AU, slope=c.SIGMA_SLOPE):
    """Power-law surface density, Sigma = sigma_1au (r/AU)^slope. Supplied.

    Parameters
    ----------
    r : float or ndarray
        Cylindrical radius [m].
    sigma_1au : float, optional
        Surface density at 1 AU [kg m^-2]. Default: Hayashi MMSN gas.
    slope : float, optional
        Power-law index. Default -3/2.

    Returns
    -------
    float or ndarray
        Surface density [kg m^-2].
    """
    return sigma_1au * (np.asarray(r) / c.AU) ** slope


def temperature(r, t_1au=c.T_DISK_1AU, slope=c.T_DISK_SLOPE):
    """Power-law midplane temperature, T = t_1au (r/AU)^slope. Supplied.

    The defaults are the course fiducial, T = 280 (r/AU)^(-1/2) K. A flat
    reprocessing disk is temperature(r, 81.0, -0.75) and a flared one
    temperature(r, 160.0, -3/7), for a T Tauri star with T = 4000 K, R = 2 R_sun.

    Parameters
    ----------
    r : float or ndarray
        Cylindrical radius [m].
    t_1au : float, optional
        Temperature at 1 AU [K].
    slope : float, optional
        Power-law index, -q.

    Returns
    -------
    float or ndarray
        Temperature [K].
    """
    return t_1au * (np.asarray(r) / c.AU) ** slope


def sound_speed(T, mu=c.MU_DISK):
    """Isothermal sound speed, c_s = sqrt(k T / mu m_H). Supplied.

    Parameters
    ----------
    T : float or ndarray
        Temperature [K].
    mu : float, optional
        Mean mass per particle in units of m_H.

    Returns
    -------
    float or ndarray
        Sound speed [m s^-1].
    """
    return np.sqrt(c.K_B * np.asarray(T) / (mu * c.M_H))


def keplerian_omega(r, m_star=c.M_SUN):
    """Keplerian angular frequency, Omega = sqrt(G M / r^3). Supplied.

    Returns
    -------
    float or ndarray
        [s^-1].
    """
    return np.sqrt(c.G * m_star / np.asarray(r) ** 3)


def planck_nu(nu, T):
    """Planck specific intensity B_nu(T). Supplied.

    Safe at large h nu / k T, where it returns 0 rather than overflowing.

    Parameters
    ----------
    nu : float or ndarray
        Frequency [Hz].
    T : float or ndarray
        Temperature [K]. nu and T broadcast against each other.

    Returns
    -------
    ndarray
        B_nu [W m^-2 Hz^-1 sr^-1].
    """
    nu = np.asarray(nu, dtype=float)
    T = np.asarray(T, dtype=float)
    x = c.H_PLANCK * nu / (c.K_B * T)
    with np.errstate(over="ignore"):
        out = 2.0 * c.H_PLANCK * nu**3 / c.C_LIGHT**2 / np.expm1(np.minimum(x, 700.0))
    return np.where(x > 700.0, 0.0, out)


def dust_opacity(nu, kappa_0=0.23, lambda_0=1.3e-3, beta=1.0):
    """Power-law dust opacity per kilogram of dust. Supplied.

    kappa(nu) = kappa_0 (nu / nu_0)^beta, with nu_0 = c / lambda_0. The default,
    0.23 m^2 kg^-1 = 2.3 cm^2 g^-1 at 1.3 mm with beta = 1, is the value used by
    the millimeter disk surveys.

    Parameters
    ----------
    nu : float or ndarray
        Frequency [Hz].
    kappa_0 : float, optional
        Opacity at lambda_0 [m^2 per kg of dust].
    lambda_0 : float, optional
        Reference wavelength [m].
    beta : float, optional
        Opacity index.

    Returns
    -------
    float or ndarray
        Opacity [m^2 per kg of dust].
    """
    nu_0 = c.C_LIGHT / lambda_0
    return kappa_0 * (np.asarray(nu) / nu_0) ** beta


def radial_grid(r_in, r_out, n=2000):
    """Logarithmically spaced annulus EDGES from r_in to r_out. Supplied.

    A disk spans three or more decades in radius, and every decade contributes
    to some part of the spectrum, so the annuli are spaced evenly in log r.

    Returns
    -------
    ndarray, shape (n + 1,)
        Annulus edges [m].
    """
    return np.geomspace(r_in, r_out, n + 1)


# =====================================================================
# You implement these
# =====================================================================

def scale_height(r, T, m_star=c.M_SUN, mu=c.MU_DISK):
    """Vertical scale height of an isothermal disk, H = c_s / Omega_K.

    Parameters
    ----------
    r : float or ndarray
        Cylindrical radius [m].
    T : float or ndarray
        Midplane temperature at r [K].
    m_star : float, optional
        Stellar mass [kg].
    mu : float, optional
        Mean mass per particle in units of m_H.

    Returns
    -------
    float or ndarray
        Scale height H [m]. Divide by r for the aspect ratio.
    """
    raise NotImplementedError("PS3, section 1")


def sed(nu, r_edges, T_func, distance, sigma_dust=None, kappa=None, cos_i=1.0):
    """Flux density of a disk built from concentric annuli.

    Each annulus between r_edges[k] and r_edges[k+1] has area
    pi (r_{k+1}^2 - r_k^2), temperature T_func(r_mid) with r_mid the geometric
    mean of its edges, and emits from the face we see

        I_nu = (1 - exp(-tau_nu)) B_nu(T),      tau_nu = kappa(nu) Sigma_dust / cos i,

    so that the flux density is

        F_nu = (cos i / d^2) * sum_k  area_k * I_nu,k .

    If sigma_dust is None the disk is optically thick at every frequency and
    I_nu = B_nu(T): the sum of blackbody annuli.

    tau_nu here is the FULL vertical column, kappa Sigma_dust, because the light
    that leaves the disk has crossed all of it. The optical depth from the
    midplane to the surface, kappa Sigma_dust / 2, tells you whether the
    midplane itself is visible; it does not set I_nu. In the optically thin
    limit this sed() returns F_nu = kappa B_nu M_dust / d^2 exactly.

    Parameters
    ----------
    nu : float or ndarray, shape (M,)
        Frequencies [Hz].
    r_edges : ndarray, shape (N + 1,)
        Annulus edges [m], increasing. radial_grid() makes one.
    T_func : callable
        T_func(r) -> temperature [K].
    distance : float
        Distance to the disk [m].
    sigma_dust : callable or None, optional
        sigma_dust(r) -> DUST surface density [kg m^-2], summed over both
        halves of the disk. None for an optically thick disk.
    kappa : callable or None, optional
        kappa(nu) -> opacity [m^2 per kg of dust]. Required with sigma_dust.
    cos_i : float, optional
        Cosine of the inclination; 1 is face-on.

    Returns
    -------
    ndarray, shape (M,)
        F_nu [W m^-2 Hz^-1]. Multiply by nu for nu F_nu.
    """
    raise NotImplementedError("PS3, section 1")
