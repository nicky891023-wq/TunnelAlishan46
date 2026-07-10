#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tunnel_frame.py -- curved-tunnel unrolling frame (Wade review 07-10: 依隧道線型與斷面
幾何修正展開圖).

Facts measured from ring3d_G4 (456k balls):
  * centreline cx(y) swings 1296.2 -> 1298.84 (y=885 curve apex) -> 1295.7 over y 860-910
    (the horizontal CURVE); crown apex z = 1750.2 and feet z = 1744.9 are y-invariant.
  * section: half-width 2.45 m (walls at cx +- 2.45), arch centre z0 = 1747.75,
    arch radius R = 2.45, legs 1744.9..1747.75.

API:
  theta_local(x, y, z) -> deg   angle about the LOCAL centre (cx(y), z0)
  station(x, y, z)     -> m     perimeter arc length from crown (signed, + right)
  ticks()              -> (positions, labels) for developed-map x axis
"""
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
Z0 = 1747.75          # arch centre elevation AT y=885 (grade-corrected via z0_of)
RARC = 2.45           # arch radius = half width
LEG = 2.85            # leg length (section is rigid: crown-feet distance constant)
GRADE = None          # z-apex linear fit coeffs (3.7% railway grade, measured 07-10)
QUART = RARC * np.pi / 2.0          # crown->springline arc length (3.848 m)
SFOOT = QUART + LEG                 # crown->foot station (6.698 m)

_C = None

def _fit():
    global _C, GRADE
    if _C is not None:
        return _C
    ring = np.loadtxt(HERE / "ring3d_G4.txt", skiprows=1, ndmin=2)
    x, y, z = ring[:, 0], ring[:, 1], ring[:, 2]
    ys, cxs, zas = [], [], []
    for y0 in np.arange(860.5, 910, 1.0):
        m = np.abs(y - y0) < 0.5
        za = z[m].max()                                  # crown apex (grade)
        mw = m & (np.abs(z - (za - RARC)) < 1.0)         # wall band at local arch centre
        if mw.sum() > 50:
            ys.append(y0); zas.append(za)
            cxs.append((x[mw].min() + x[mw].max()) / 2)
    _C = np.polyfit(ys, cxs, 4)
    GRADE = np.polyfit(ys, np.array(zas) - RARC, 1)      # arch-centre elevation, linear
    res = np.polyval(_C, ys) - cxs
    resz = np.polyval(GRADE, ys) - (np.array(zas) - RARC)
    print("tunnel_frame: cx fit rms=%.3f m, z0 grade=%.2f%% rms=%.3f m (%d slabs)" %
          (np.sqrt((res**2).mean()), GRADE[0] * 100, np.sqrt((resz**2).mean()), len(ys)))
    return _C

def z0_of(y):
    _fit()
    return np.polyval(GRADE, np.clip(y, 860.0, 910.0))

def cx_of(y):
    return np.polyval(_fit(), np.clip(y, 860.0, 910.0))

def theta_local(x, y, z):
    """deg from crown about the local centre (curve + grade); +x side positive."""
    return np.degrees(np.arctan2(x - cx_of(y), z - z0_of(y)))

def station(x, y, z):
    """signed perimeter arc length (m) from crown along the section contour.
    Arch points (z >= Z0): s = R * angle; leg points (z < Z0): s = quarter + drop."""
    dx = x - cx_of(y)
    dz = z - z0_of(y)
    s_arch = RARC * np.arctan2(np.abs(dx), dz)      # 0..pi*R/2 for dz>0 branch
    # on-leg: angle formula above approaches pi/2 as dz->0; use explicit branch
    on_leg = dz < 0
    s = np.where(on_leg, QUART + np.minimum(-dz, LEG), s_arch)
    return np.sign(dx) * s

def ticks():
    pos = [-SFOOT, -QUART, 0, QUART, SFOOT]
    lab = ["L foot", "L spr", "Crown", "R spr", "R foot"]
    return pos, lab

if __name__ == "__main__":
    _fit()
    for y0 in (860, 885, 910):
        print("cx(%d) = %.2f" % (y0, cx_of(np.array([y0]))[0]))
    print("stations: quarter=%.2f foot=%.2f" % (QUART, SFOOT))
