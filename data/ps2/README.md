## satellites.csv

Semi-major axes, eccentricities and inclinations of the 451 known satellites of
Jupiter, Saturn, Uranus and Neptune.

**Source.** JPL Solar System Dynamics, Planetary Satellite Mean Elements,
https://ssd.jpl.nasa.gov/sats/elem/ (grouped tables), retrieved 2026-09-09.
Ephemerides: JUP365, JUP347, JUP348, JUP349 (Jupiter); SAT441, SAT415, SAT456,
SAT457, SAT455, SAT459 (Saturn); URA182, URA184, URA117 (Uranus); NEP097,
NEP105, NEP104 (Neptune). Epoch 2000-01-01.5 TDB, except the Uranian inner
satellites (2025-01-01.0) and the outer Uranian and Neptunian satellites
(2020-01-01.0).

**Units and conventions.** Semi-major axes converted from km to m; they are
planetocentric, so a/r_H is a direct division. Reference planes differ by group:
local Laplace plane or planet equator for the regular satellites, ecliptic for
the irregulars. `direction` is assigned as retrograde where the tabulated
inclination exceeds 90 degrees.

**Warning carried over from the source.** These are mean elements fitted to
numerically integrated orbits, not ephemerides. They describe the shape and
orientation of an orbit and nothing more.

## planet_elements.csv

Semi-major axes, eccentricities, masses and volumetric mean radii of the eight
planets. Source: JPL Solar System Dynamics planetary physical parameters and
orbital elements. Radii are volumetric mean radii, so that M / (4/3 pi R^3) is
the true mean density; ring and satellite distances quoted in "planet radii" in
the literature normally use the equatorial radius instead, which for Saturn is
3.5% larger.
