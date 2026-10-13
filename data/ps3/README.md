## lupus_disks.csv

Class II stars in the Lupus clouds that have both an ALMA 890 μm continuum
measurement and an X-shooter accretion rate: 66 stars, one per row.

**Sources.**
- ALMA continuum fluxes at 890 μm and distances: Ansdell et al. 2016, ApJ 828,
  46, VizieR J/ApJ/828/46, tables 1 and 2.
- Accretion rates, stellar masses and notes: Alcalá et al. 2017, A&A 600, A20,
  VizieR J/A+A/600/A20, tables A.2 and A.3. These tables cover the full Lupus
  X-shooter sample, including the stars first published in Alcalá et al. 2014.

The four tables and both ReadMe files are in `raw/`, as distributed by CDS and
retrieved 2026-10-12. `build_lupus.py` regenerates this file from them.

**Matching.** Most stars are matched by name. Where the two papers use
different designations, the match is by position, to within 1.2″ in every case.
Positions come from the ALMA table, from the coordinates encoded in 2MASS and
c2d names, or from Alcalá et al. 2014, Table 1. Fifteen Alcalá stars have no
ALMA counterpart: they were not observed, fall below the survey's
0.1 M☉ cut, or lie off the Lupus I–IV clouds.

**Columns.**

| column        | units       | meaning |
|---------------|-------------|---------|
| `name`        | —           | as in Ansdell et al. 2016 |
| `name_alcala` | —           | as in Alcalá et al. 2017 |
| `distance_pc` | pc          | 150 (Lupus I, II, IV) or 200 (Lupus III). Both papers adopt the same value for every star. |
| `F890_mJy`    | mJy         | integrated 890 μm flux; for non-detections, the 3σ upper limit, 3 × `e_F890` |
| `e_F890_mJy`  | mJy         | uncertainty; blank for upper limits |
| `F890_limit`  | 0/1         | 1 if the source is undetected, F890 < 3 × e_F890 (62 of the 89 survey disks are detected) |
| `M_star_msun` | M☉          | stellar mass from Baraffe et al. 2015 tracks |
| `log_mdot`    | log M☉ yr⁻¹ | mass accretion rate, with the same tracks |
| `flag`        | —           | blank, or one or more of the following, separated by semicolons |

**Flags.**
- `chromospheric`: accretion luminosity comparable to chromospheric emission (Alcalá note a), so the accretion rate is uncertain.
- `mdot_upper_limit`: the accretion rate is an upper limit.
- `subluminous`: the star appears underluminous for its spectral type (notes sl, bz, c). This usually means a nearly edge-on disk seen in scattered light, which makes the luminosity and accretion rate underestimates.
- `transitional`: a disk with a cleared inner cavity (note td).

**Conventions carried over from the sources.** The survey's dust-mass recipe
uses κ = 10 (ν/1000 GHz) cm² g⁻¹ of dust (3.37 cm² g⁻¹ at 890 μm) and
T_dust = 20 K. Problem Set 3 asks you to apply that recipe; it is not applied
here.
