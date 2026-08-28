#!/usr/bin/env python3
"""Convert the VizieR download of Konyves et al. (2015) Table A.2 into the
course CSV read by astrotools.data.load_herschel_cores.

    python data/raw/make_herschel_catalog.py

Input   data/raw/J_A+A_584_A91_tablea2.dat.txt   (VizieR, pipe-separated)
Output  data/herschel_core_catalog.csv

The VizieR file is pipe-separated with a four-line header in which the column
names are split across two rows, so no header-aware reader gets the names right.
This script writes a plain comma-separated file with one header line, expands
VizieR's scale factors (10^21 cm^-2, 10^4 cm^-3) so that every column is in the
unit its name states, and turns the free-text comment field into three flags.
Published units (Msun, pc, K, cm^-2, cm^-3) are kept: converting them to SI is
part of the assignment.
"""

import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "J_A+A_584_A91_tablea2.dat.txt")
DST = os.path.join(HERE, os.pardir, "herschel_core_catalog.csv")

HEADER = [
    "seq", "name",
    "R_deconv_pc", "R_obs_pc",
    "M_core_msun", "M_core_err_msun",
    "T_dust_K", "T_dust_err_K",
    "N_H2_peak_cm2", "N_H2_av_cm2", "N_H2_avd_cm2",
    "n_H2_peak_cm3", "n_H2_av_cm3", "n_H2_avd_cm3",
    "alpha_BE", "core_type",
    "no_sed_fit", "tentative_bound", "co_high_vlsr",
]


def main():
    rows = []
    for line in open(SRC):
        f = [x.strip() for x in line.rstrip("\n").split("|")]
        if len(f) != 18 or not f[0].isdigit():
            continue                      # header, rule, or comment line
        com = " ".join(f[17].split())
        rows.append([
            int(f[0]), f[1],
            float(f[3]), float(f[4]),
            float(f[5]), float(f[6]),
            float(f[7]), float(f[8]),
            float(f[9]) * 1e21, float(f[10]) * 1e21, float(f[11]) * 1e21,
            float(f[12]) * 1e4, float(f[13]) * 1e4, float(f[14]) * 1e4,
            float(f[15]), f[16],
            int("no SED fit" in com),
            int("tentative bound" in com),
            int("CO high-V_LSR" in com),
        ])

    assert len(rows) == 749, f"expected 749 cores, parsed {len(rows)}"
    fmt = lambda v: f"{v:.6g}" if isinstance(v, float) else v
    with open(DST, "w", newline="\n") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(HEADER)
        w.writerows([fmt(v) for v in row] for row in rows)
    print(f"wrote {DST}: {len(rows)} cores")


if __name__ == "__main__":
    main()
