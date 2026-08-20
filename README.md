# ASTR 5820 — Origin and Evolution of Planetary Systems

Course code repository, Fall 2026. Prof. Paul O. Hayne, University of Colorado Boulder.

**Start with [SETUP.md](SETUP.md).** Thirty minutes, once, before Week 2.

`astrotools` is a single toolbox built up over the semester: each problem set adds
functions to it, and later sets import what earlier ones wrote. The tests in
`tests/` are the specification for each coding exercise — read them before writing
any code.

```bash
conda env create -f environment.yml
conda activate astr5820
pip install -e .
python check_setup.py
```

| Set | Weeks | Module | Physics |
|---|---|---|---|
| 1 | 2, 4 | `cloud/collapse.py`, `nbody/integrators.py` | Jeans collapse, the centrifugal radius, integrator accuracy |
| 2 | 5, 6 | `disk/structure.py`, `disk/viscous.py` | MMSN, vertical structure, SEDs, viscous spreading |
| 3 | 7, 8 | `dust/drift.py`, `dust/settling.py` | Condensation fronts, radial drift, settling, streaming instability |
| 4 | 9, 10 | `nbody/diagnostics.py`, `nbody/accretion.py` | Resonance widths, leapfrog, isolation mass |
| 5 | 11, 12 | `chronology/isochron.py`, `interiors/thermal.py` | Radiometric ages, interiors, the radius valley |
| 6 | 13, 14 | `giants/growth.py` | Pebble accretion, critical core mass, migration |
