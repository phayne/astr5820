"""
Build lupus_disks.csv from the published tables in raw/.

    python data/ps3/build_lupus.py

Inputs (fixed-width, as distributed by CDS; formats in the two ReadMe files):
    raw/ansdell2016_table1.dat   J/ApJ/828/46 table1  distance, stellar mass
    raw/ansdell2016_table2.dat   J/ApJ/828/46 table2  ALMA 890 um flux, coordinates
    raw/alcala2017_tablea2.dat   J/A+A/600/A20 tablea2  stellar parameters, notes
    raw/alcala2017_tablea3.dat   J/A+A/600/A20 tablea3  accretion rates

One row per star in the ALMA survey that also has an X-shooter accretion rate.
"""

import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# Coordinates of Alcala et al. sources whose names carry no position, from
# Alcala et al. 2014, A&A 561, A2, Table 1 (J2000).
GTO_COORDS = {
    "AKC2006-19": ("15:44:57.90", "-34:23:39.5"),
    "Lup713": ("16:07:37.72", "-39:21:38.8"),
    "Lup604s": ("16:08:00.20", "-39:02:59.7"),
    "Lup706": ("16:08:37.30", "-39:23:10.8"),
    "Lup818s": ("16:09:56.29", "-38:59:51.7"),
    "Par-Lup3-3": ("16:08:49.40", "-39:05:39.3"),
    "Par-Lup3-4": ("16:08:51.43", "-39:05:30.4"),
    "SST-Lup3-1": ("16:11:59.81", "-38:23:38.5"),
}


def sexa_to_deg(ra, dec):
    h, m, s = (float(x) for x in ra.split(":"))
    sign = -1 if dec.strip().startswith("-") else 1
    d, dm, ds = (abs(float(x)) for x in dec.split(":"))
    return 15 * (h + m / 60 + s / 3600), sign * (d + dm / 60 + ds / 3600)


def coords_from_name(name):
    """Position encoded in a 2MASS (Jhhmmssss-ddmmsss) or c2d (Jhhmmss.s-ddmmss) name."""
    if not re.match(r"^(2MASS|SSTc2d|J)", name.replace(" ", "")):
        return None
    m = re.search(r"J?(\d{2})(\d{2})(\d{2})\.?(\d+)([+-])(\d{2})(\d{2})(\d{2})(\d*)", name.replace(" ", ""))
    if not m:
        return None
    hh, mm, ss, sfrac, sg, dd, dm, ds, dfrac = m.groups()
    ra = f"{hh}:{mm}:{ss}.{sfrac}"
    dec = f"{sg}{dd}:{dm}:{ds}" + (f".{dfrac}" if dfrac else "")
    return sexa_to_deg(ra, dec)


def norm(name):
    """Comparable form of a star name: no spaces, no '(SW)'-type suffix, first alias only."""
    name = re.sub(r"\(.*?\)", "", name).split("/")[0]
    return name.replace("2MASS", "").replace(" ", "").strip()


def sep_arcsec(a, b):
    import math
    dra = (a[0] - b[0]) * math.cos(math.radians(0.5 * (a[1] + b[1])))
    return 3600 * math.hypot(dra, a[1] - b[1])


def fnum(s):
    s = s.strip()
    return float(s) if s else None


# ---------------------------------------------------------------- Ansdell
ans = {}
for line in open(os.path.join(RAW, "ansdell2016_table1.dat")):
    ans[line[0:17].strip()] = {"distance_pc": int(line[18:21]),
                               "M_star_ansdell": fnum(line[27:31])}
for line in open(os.path.join(RAW, "ansdell2016_table2.dat")):
    name = line[0:17].strip()
    ra = f"{line[18:20]}:{line[21:23]}:{line[24:29]}"
    dec = f"{line[30]}{line[31:33]}:{line[34:36]}:{line[37:42]}"
    ans[name].update(F890=float(line[43:49]), eF890=float(line[50:55]),
                     pos=sexa_to_deg(ra, dec))
alma = {k: v for k, v in ans.items() if "F890" in v}          # 89 observed

# ---------------------------------------------------------------- Alcala
alc = {}
for line in open(os.path.join(RAW, "alcala2017_tablea2.dat")):
    name = line[2:25].strip()
    alc[name] = {"sample": line[0], "distance_alcala": int(line[45:48]),
                 "M_star_B15": fnum(line[85:89]), "M_star_B15_limit": line[84].strip(),
                 "notes_a2": line[116:123].strip()}
for line in open(os.path.join(RAW, "alcala2017_tablea3.dat")):
    name = line[2:25].strip()
    alc[name].update(log_mdot=fnum(line[60:66]), mdot_limit=line[59].strip(),
                     note_a3=line[82:83].strip())

# ---------------------------------------------------------------- match
by_norm = {norm(k): k for k in alma}
matched, unmatched = {}, []
for name in alc:
    key = by_norm.get(norm(name))
    method = "name"
    if key is None:
        pos = coords_from_name(name)
        if pos is None and name in GTO_COORDS:
            pos = sexa_to_deg(*GTO_COORDS[name])
        if pos is not None:
            best = min(alma, key=lambda k: sep_arcsec(pos, alma[k]["pos"]))
            sep = sep_arcsec(pos, alma[best]["pos"])
            if sep < 3.0:
                key, method = best, f"position ({sep:.1f} arcsec)"
    if key is None:
        unmatched.append(name)
    else:
        assert key not in matched, (key, name)
        matched[key] = (name, method)

# ---------------------------------------------------------------- write
rows = []
for key in sorted(matched, key=lambda k: list(alma).index(k)):
    a, (aname, method) = alma[key], matched[key]
    b = alc[aname]
    assert a["distance_pc"] == b["distance_alcala"], (key, a["distance_pc"], b["distance_alcala"])
    detected = a["F890"] >= 3 * a["eF890"]
    flags = []
    if b["note_a3"] == "a":
        flags.append("chromospheric")
    if "sl" in b["notes_a2"] or "bz" in b["notes_a2"] or b["note_a3"] == "c":
        flags.append("subluminous")
    if "td" in b["notes_a2"]:
        flags.append("transitional")
    if b["mdot_limit"]:
        flags.append("mdot_upper_limit")
    if b["log_mdot"] is None:
        continue                     # no B15 accretion rate: outside the B15 track grid
    rows.append({
        "name": key,
        "name_alcala": aname,
        "distance_pc": a["distance_pc"],
        "F890_mJy": round(a["F890"] if detected else 3 * a["eF890"], 2),
        "e_F890_mJy": a["eF890"] if detected else "",
        "F890_limit": 0 if detected else 1,
        "M_star_msun": b["M_star_B15"] if b["M_star_B15"] is not None else "",
        "log_mdot": b["log_mdot"],
        "flag": ";".join(flags),
    })

out = os.path.join(HERE, "lupus_disks.csv")
with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

n_det = sum(a["F890"] >= 3 * a["eF890"] for a in alma.values())
print(f"ALMA sources: {len(alma)} ({n_det} detected at 3 sigma); Alcala sources: {len(alc)}")
print(f"matched: {len(matched)}; written: {len(rows)} -> {out}")
print("matched by position:", {k: v for k, v in matched.items() if v[1] != 'name'})
print("Alcala sources with no ALMA counterpart:", unmatched)
