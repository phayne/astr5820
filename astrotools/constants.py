"""
Physical constants, the standard disk model, and unit conversions for ASTR 5820.

Everything in this course is in SI. Every module imports its numbers from here, so
that a result computed in Week 2 and a result computed in Week 13 refer to the same
Sun, the same AU, and the same minimum-mass solar nebula.

    from astrotools import constants as c
    print(c.AU, c.M_SUN)

Do not redefine constants locally. If you need a number that is not here, add it
here and say where it came from.
"""

# =====================================================================
# Fundamental constants (CODATA 2018; SI)
# =====================================================================
G           = 6.67430e-11        # gravitational constant       [m^3 kg^-1 s^-2]
K_B         = 1.380649e-23       # Boltzmann constant           [J K^-1]
H_PLANCK    = 6.62607015e-34     # Planck constant              [J s]
C_LIGHT     = 2.99792458e8       # speed of light               [m s^-1]
SIGMA_SB    = 5.670374419e-8     # Stefan-Boltzmann constant    [W m^-2 K^-4]
N_A         = 6.02214076e23      # Avogadro constant            [mol^-1]
R_GAS       = 8.314462618        # molar gas constant           [J mol^-1 K^-1]

M_H         = 1.67353e-27        # mass of the hydrogen ATOM    [kg]
M_P         = 1.67262192e-27     # mass of the proton           [kg]
M_E         = 9.1093837015e-31   # mass of the electron         [kg]

# Note: TWO mean molecular weights appear in this course and they are not the
# same quantity. MU_CLOUD = 2.33 is the mean mass per free PARTICLE in units of
# M_H, and belongs in the sound speed, c_s = sqrt(k T / (MU_CLOUD * M_H)).
# MU_H2 = 2.8 is the total gas mass per H2 MOLECULE, including helium, and is
# what converts an H2 number density into a mass density,
# rho = n(H2) * MU_H2 * M_H. Both appear in the Jeans mass. Using 2.33 for the
# density conversion makes rho low by 20% and M_J high by 10%.

# =====================================================================
# Astronomical units and bodies (IAU 2015 nominal values)
# =====================================================================
AU          = 1.495978707e11     # astronomical unit            [m]
PC          = 3.0856775814913673e16   # parsec                  [m]
LY          = 9.4607304725808e15 # light year                   [m]
YR          = 3.15576e7          # Julian year                  [s]
MYR         = 1.0e6 * YR
GYR         = 1.0e9 * YR
DAY         = 86400.0            # [s]

GM_SUN      = 1.32712440018e20   # solar gravitational parameter [m^3 s^-2]
M_SUN       = GM_SUN / G         # 1.9885e30                     [kg]
R_SUN       = 6.957e8            # [m]
L_SUN       = 3.828e26           # [W]
T_SUN       = 5772.0             # effective temperature         [K]

M_EARTH     = 5.97217e24         # [kg]
R_EARTH     = 6.371e6            # volumetric mean radius        [m]
M_JUP       = 1.89813e27         # [kg]
R_JUP       = 6.9911e7           # equatorial radius             [m]

# GM_SUN is measured far more precisely than either G or M_SUN separately.
# Use GM_SUN wherever the product is what you need -- it is the better number.

# =====================================================================
# Fiducial dense core (Lectures 2-3; Problem Set 1)
# =====================================================================
# A stake in the ground, not a claim about any particular object. Chosen so the
# core comes out marginally Jeans unstable, which is the interesting regime:
# M_CORE / M_J = 1.93. Note that T, n and M fix the radius -- R_CORE is not an
# independent choice, and 0.047 pc is what (3 M_CORE / 4 pi rho)^(1/3) returns.
T_CORE          = 10.0           # temperature                   [K]
N_H2_CORE       = 1.0e11         # H2 number density             [m^-3]
R_CORE          = 0.047 * PC     # radius (follows from M, n)    [m]
M_CORE          = 3.0 * M_SUN    # enclosed mass                 [kg]
OMEGA_CORE      = 3.0e-14        # angular frequency             [s^-1]
MU_CLOUD        = 2.33           # mean mass per particle / M_H (sound speed)
MU_H2           = 2.8            # gas mass per H2 molecule / M_H (density conversion)

# The fiducial Omega is a ROUNDED stand-in for a 1 km/s/pc velocity gradient;
# the exact conversion is 3.241e-14 s^-1 (see omega_from_velocity_gradient).
# Because R_c goes as Omega^2, the rounding is a ~17% difference in disk radius.
# Use OMEGA_CORE for the fiducial test value; use the converter for the sweep.

# =====================================================================
# Standard disk model: Hayashi minimum-mass solar nebula (Weeks 5 onward)
# =====================================================================
# Surface densities at 1 AU, each scaling as (r/AU)^SIGMA_SLOPE.
SIGMA_GAS_1AU       = 1.70e4     # gas                           [kg m^-2]
SIGMA_ROCK_1AU      = 71.0       # solids inside the snow line   [kg m^-2]
SIGMA_ROCKICE_1AU   = 300.0      # solids beyond the snow line   [kg m^-2]
SIGMA_SLOPE         = -1.5       # Sigma propto r^(-3/2)

T_DISK_1AU          = 280.0      # midplane temperature at 1 AU  [K]
T_DISK_SLOPE        = -0.5       # T propto r^(-1/2), passive, optically thin

R_SNOW              = 2.7 * AU   # where T = 170 K               [m]
T_SNOW              = 170.0      # water condensation temperature [K]
MU_DISK             = 2.34       # mean molecular weight, disk gas
DLNP_DLNR           = -3.25      # midplane pressure gradient index

# The two-branch solid surface density ALREADY contains the ice enrichment: the
# factor 4.2 step at 2.7 AU is what the MMSN augmentation returns. Do not apply a
# uniform metallicity on top of it.

# =====================================================================
# Unit conversions
# =====================================================================

def omega_from_velocity_gradient(grad_km_s_pc):
    """Convert an observed core velocity gradient to an angular frequency.

    Dense-core rotation is reported as a linear velocity gradient across the core
    in km/s/pc. For solid-body rotation the gradient equals Omega (up to the
    unknown inclination factor sin i, which is not corrected for here).

    Parameters
    ----------
    grad_km_s_pc : float or array_like
        Velocity gradient [km s^-1 pc^-1].

    Returns
    -------
    float or ndarray
        Angular frequency [s^-1]. 1 km/s/pc -> 3.241e-14 s^-1.
    """
    return grad_km_s_pc * 1.0e3 / PC


def au(x_metres):
    """Metres -> AU."""
    return x_metres / AU


def msun(x_kg):
    """Kilograms -> solar masses."""
    return x_kg / M_SUN


def yr(x_seconds):
    """Seconds -> years."""
    return x_seconds / YR
