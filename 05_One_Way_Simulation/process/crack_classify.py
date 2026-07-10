#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
crack_classify.py -- shared bond-break ORIENTATION classifier (single source of truth for
the crack-evolution GIF, the y=885 cross-section figure and the developed-lining map).

Three-track method (see make_crack_normal_gif.py for the full rationale):
  * OBLIQUE / LONGITUDINAL: on the developed surface (hoop-arc U, axial y) a smoothed local-
    orientation field (structure tensor + anisotropy-weighted double-angle averaging) marks
    DIRECTIONAL breaks; these are clustered and each cluster is classified by its OWN shape
    (PCA angle from the hoop): 25-65deg -> oblique, >65deg -> longitudinal.
  * CIRCUMFERENTIAL: every remaining break connects within its 1 m XZ cross-section slab into
    an arc = circumferential (the dominant bulk).

classify_breaks() returns per-break labels typ in {-1 unclassified, 0 circ, 1 oblique, 2 long}.
"""
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
from sklearn.cluster import DBSCAN
import tunnel_frame as tf

HERE = Path(__file__).parent
CX, CZ = 1298.85, 1747.5   # ring centre verified from xsec_G4 (07-10)
AGE1 = 25855.0            # stage-1 baseline cutoff (water-cycle-induced breaks only)
# --- circumferential (per XZ slab) ---
YMIN, YMAX, YSTEP = 860.0, 910.0, 1.0
EPS_RING, MIN_RING, LMIN_CIRC = 0.35, 4, 0.8
# --- oblique / longitudinal (developed-surface orientation field) ---
KORI, COH_MIN = 30, 0.28
EPS_DIR, MIN_DIR = 0.60, 6
BETA_LO, BETA_HI = 25.0, 65.0
LMIN_OBL, LMIN_LONG = 1.0, 3.0

TYPE_COL  = {0: "#e00000", 1: "#1f6fe0", 2: "#2ca02c", -1: "#c9c9c9"}
TYPE_NAME = {0: "circumferential", 1: "oblique", 2: "longitudinal", -1: "unclassified"}


def load_breaks(stage=11, age_min=AGE1):
    """water-cycle-induced break cloud at a stage: returns P(N,3), AGE(N)."""
    cs = np.loadtxt(HERE / f"cs_s{stage}_cracks.txt", skiprows=1, ndmin=2)  # x y z type diam age
    w = cs[:, 5] > age_min
    return cs[w, :3], cs[w, 5]


def _coherence(U, Y):
    D = np.column_stack([U, Y])
    _, idx = cKDTree(D).query(D, k=KORI + 1)
    nb = D[idx[:, 1:]]; q = nb - nb.mean(1, keepdims=True)
    cxx = (q[:, :, 0]**2).mean(1); cyy = (q[:, :, 1]**2).mean(1); cxy = (q[:, :, 0]*q[:, :, 1]).mean(1)
    tr = cxx + cyy; det = cxx*cyy - cxy**2; disc = np.sqrt(np.maximum((tr/2)**2 - det, 0))
    aniso = (disc * 2) / (tr + 1e-12)
    ap = 0.5 * np.arctan2(2*cxy, cxx - cyy)
    c2 = (aniso*np.cos(2*ap))[idx[:, 1:]].mean(1)
    s2 = (aniso*np.sin(2*ap))[idx[:, 1:]].mean(1)
    return np.sqrt(c2**2 + s2**2)


def classify_breaks(P):
    """label every break: -1 unclassified / 0 circ / 1 oblique / 2 longitudinal.
    Returns (typ, ST perimeter station m, R m). Curved-frame unrolling (07-10)."""
    X, Y, Z = P[:, 0], P[:, 1], P[:, 2]
    THETA = tf.theta_local(X, Y, Z)                  # local centre (curved axis)
    R = np.sqrt((X - tf.cx_of(Y))**2 + (Z - tf.z0_of(Y))**2)
    U = tf.station(X, Y, Z)                          # perimeter arc length (m)
    coh = _coherence(U, Y)
    D = np.column_stack([U, Y])
    typ = np.full(len(P), -1, int)
    used = np.zeros(len(P), bool)
    # 1. directional clusters -> oblique / longitudinal by cluster shape
    sel = np.where(coh >= COH_MIN)[0]
    if len(sel) >= MIN_DIR:
        lab = DBSCAN(eps=EPS_DIR, min_samples=MIN_DIR).fit_predict(D[sel])
        for L in set(lab) - {-1}:
            sub = sel[lab == L]
            d = D[sub]; axis = np.linalg.svd(d - d.mean(0), full_matrices=False)[2][0]
            proj = (d - d.mean(0)) @ axis
            length = proj.max() - proj.min()
            beta = abs(np.degrees(np.arctan2(abs(axis[1]), abs(axis[0]))))
            if beta < BETA_LO:
                continue
            t = 1 if beta <= BETA_HI else 2
            if length < (LMIN_OBL if t == 1 else LMIN_LONG):
                continue
            typ[sub] = t; used[sub] = True
    # 2. everything else -> circumferential arcs within each 1 m XZ slab
    for y0 in np.arange(YMIN, YMAX, YSTEP):
        idx = np.where((~used) & (Y >= y0) & (Y < y0 + YSTEP))[0]
        if len(idx) < MIN_RING:
            continue
        lab = DBSCAN(eps=EPS_RING, min_samples=MIN_RING).fit_predict(np.column_stack([X[idx], Z[idx]]))
        for L in set(lab) - {-1}:
            sub = idx[lab == L]
            length = U[sub].max() - U[sub].min()     # true perimeter arc length
            if length < LMIN_CIRC:
                continue
            typ[sub] = 0; used[sub] = True
    return typ, U, R


if __name__ == "__main__":
    P, _ = load_breaks()
    typ, TH, R = classify_breaks(P)
    n = len(P)
    for t in (0, 1, 2, -1):
        print(f"  {TYPE_NAME[t]:14s}: {int((typ==t).sum()):6d}  ({100*(typ==t).mean():5.1f}%)")
    cm = (np.abs(TH) < 30) & (P[:, 1] >= 860) & (P[:, 1] < 880)
    print("CROWN y860-880:", {TYPE_NAME[t]: int(((typ == t) & cm).sum()) for t in (0, 1, 2)})
