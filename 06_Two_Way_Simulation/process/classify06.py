#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""classify06.py -- three-track crack-length statistics for the 06 two-way final state,
on EXACTLY the 05 convention (crack_classify.py is the single source of truth for all
clustering parameters; this script adds per-cluster length accumulation and runs both
the 05 s11 calibration case and the 06 t26 case).

Convention (matches thesis Ch5 numbers 環199/斜19/縱3 m):
  * water-cycle-induced breaks only: age > end-of-stage-1 cutoff
    (05: AGE1=25855.0; 06: max age present in the t06 dump = end of the 06 s1)
  * ends trimmed 2 m: 862 <= y <= 908
Run from 06/process:  python classify06.py
"""
import io
import sys
from pathlib import Path

import numpy as np
from scipy.spatial import cKDTree  # noqa: F401  (via crack_classify)
from sklearn.cluster import DBSCAN

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
P05 = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process")
OUT5 = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/06_Two_Way_Simulation/output/t5")
RES = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/06_Two_Way_Simulation/result")
sys.path.insert(0, str(P05))
import crack_classify as cc  # noqa: E402
import tunnel_frame as tf    # noqa: E402


def sum_lengths(P):
    """classify_breaks logic with per-cluster length accumulation by type (m)."""
    X, Y, Z = P[:, 0], P[:, 1], P[:, 2]
    U = tf.station(X, Y, Z)
    coh = cc._coherence(U, Y)
    D = np.column_stack([U, Y])
    typ = np.full(len(P), -1, int)
    used = np.zeros(len(P), bool)
    L = {0: 0.0, 1: 0.0, 2: 0.0}
    sel = np.where(coh >= cc.COH_MIN)[0]
    if len(sel) >= cc.MIN_DIR:
        lab = DBSCAN(eps=cc.EPS_DIR, min_samples=cc.MIN_DIR).fit_predict(D[sel])
        for k in set(lab) - {-1}:
            sub = sel[lab == k]
            d = D[sub]
            axis = np.linalg.svd(d - d.mean(0), full_matrices=False)[2][0]
            proj = (d - d.mean(0)) @ axis
            length = proj.max() - proj.min()
            beta = abs(np.degrees(np.arctan2(abs(axis[1]), abs(axis[0]))))
            if beta < cc.BETA_LO:
                continue
            t = 1 if beta <= cc.BETA_HI else 2
            if length < (cc.LMIN_OBL if t == 1 else cc.LMIN_LONG):
                continue
            typ[sub] = t
            used[sub] = True
            L[t] += length
    for y0 in np.arange(cc.YMIN, cc.YMAX, cc.YSTEP):
        idx = np.where((~used) & (Y >= y0) & (Y < y0 + cc.YSTEP))[0]
        if len(idx) < cc.MIN_RING:
            continue
        lab = DBSCAN(eps=cc.EPS_RING, min_samples=cc.MIN_RING).fit_predict(
            np.column_stack([X[idx], Z[idx]]))
        for k in set(lab) - {-1}:
            sub = idx[lab == k]
            length = U[sub].max() - U[sub].min()
            if length < cc.LMIN_CIRC:
                continue
            typ[sub] = 0
            used[sub] = True
            L[0] += length
    return typ, L


def run_case(tag, path, age_min, trim=2.0):
    cs = np.loadtxt(path, skiprows=1, ndmin=2)
    w = (cs[:, 5] > age_min) & (cs[:, 1] >= 860 + trim) & (cs[:, 1] <= 910 - trim)
    P = cs[w, :3]
    typ, L = sum_lengths(P)
    n = len(P)
    print(f"\n== {tag} ==  breaks(in-window)={n}")
    for t in (0, 1, 2, -1):
        nt = int((typ == t).sum())
        ll = f"  len={L[t]:7.1f} m" if t in L else ""
        print(f"  {cc.TYPE_NAME[t]:14s}: {nt:7d} ({100*nt/max(n,1):5.1f}%){ll}")
    return L


# --- calibration: 05 s11 must reproduce ~199/19/3 m ---
L05 = run_case("05 one-way s11 (calibration)", P05 / "cs_s11_cracks.txt", cc.AGE1)

# --- 06: age cutoff = end of two-way s1 = max age in the t06 dump ---
t06 = np.loadtxt(OUT5 / "cs06_t06_cracks.txt", skiprows=1, ndmin=2)
AGE06 = t06[:, 5].max()
print(f"\n06 age cutoff (end of s1, from t06 dump): {AGE06}")
L06 = run_case("06 two-way t26 (water-cycle only)", OUT5 / "cs06_t26_cracks.txt", AGE06)
L06f = run_case("06 two-way t26 (full incl s1)", OUT5 / "cs06_t26_cracks.txt", 0.0)

with open(RES / "T06_crack_classification.txt", "w", encoding="utf-8") as fh:
    fh.write("three-track crack lengths (m), ends trimmed 2 m\n")
    fh.write(f"05 one-way s11 (age>AGE1): circ={L05[0]:.1f} obl={L05[1]:.1f} long={L05[2]:.1f}\n")
    fh.write(f"06 two-way t26 (age>{AGE06:.0f}): circ={L06[0]:.1f} obl={L06[1]:.1f} long={L06[2]:.1f}\n")
    fh.write(f"06 two-way t26 (full): circ={L06f[0]:.1f} obl={L06f[1]:.1f} long={L06f[2]:.1f}\n")
print("\nsaved ->", RES / "T06_crack_classification.txt")
