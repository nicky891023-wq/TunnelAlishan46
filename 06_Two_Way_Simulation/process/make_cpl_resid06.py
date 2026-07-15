#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_cpl_resid06.py -- per-tick rigid-body removal for the 06 two-way chain.

Same linearized-Kabsch fit + strain-consistency gate as 05/process/make_cpl_resid.py
(functions copied verbatim), applied to one tick file:
    cpl_bnd_tNN.txt  ->  cpl_resid_tNN.txt
Always operates on the CUMULATIVE displacement field (the coupled drive law
vel=(target-gp.disp)/steps requires absolute targets; never Kabsch an increment).

Usage: python make_cpl_resid06.py NN         (run from 06/process)
Exit 0 + 'RESID06-OK' line on success; exit 1 + 'RESID06-FAIL' otherwise (fail closed).
"""
import sys
from pathlib import Path

import numpy as np

MIN_ROWS = 9000          # 05 reference: 10,109 boundary-band gps
GATE_MAX = 1e-9          # strain-consistency hard gate (05-proven threshold)
WARN_RESID_MAX = 0.05    # m; sanity warning only


def fit_rigid(X, U):
    rc = X.mean(axis=0)
    R = X - rc
    n = len(X)
    A = np.zeros((3 * n, 6))
    for i, (rx, ry, rz) in enumerate(R):
        A[3*i:3*i+3, 0:3] = np.eye(3)
        A[3*i:3*i+3, 3:6] = np.array([[0.0, rz, -ry], [-rz, 0.0, rx], [ry, -rx, 0.0]])
    sol, *_ = np.linalg.lstsq(A, U.reshape(-1), rcond=None)
    t, om = sol[:3], sol[3:]
    return U - (t + np.cross(np.broadcast_to(om, R.shape), R))


def mean_strain(X, U):
    rc = X.mean(axis=0)
    R = X - rc
    G = np.zeros((3, 3))
    M = np.linalg.pinv(R.T @ R)
    for j in range(3):
        G[j] = M @ (R.T @ (U[:, j] - U[:, j].mean()))
    return 0.5 * (G + G.T)


def main():
    nn = f"{int(sys.argv[1]):02d}"
    src = Path(f"cpl_bnd_t{nn}.txt")
    out = Path(f"cpl_resid_t{nn}.txt")
    if not src.exists():
        print(f"RESID06-FAIL t{nn} missing {src}")
        return 1
    d = np.loadtxt(src, skiprows=1)
    if d.ndim != 2 or d.shape[0] < MIN_ROWS or d.shape[1] != 6:
        print(f"RESID06-FAIL t{nn} bad shape {d.shape} (need >= {MIN_ROWS} x 6)")
        return 1
    X, U = d[:, 0:3], d[:, 3:6]
    resid = fit_rigid(X, U)
    gate = np.abs(mean_strain(X, U) - mean_strain(X, resid)).max()
    if not np.isfinite(gate) or gate >= GATE_MAX:
        print(f"RESID06-FAIL t{nn} strain gate {gate:.3e} >= {GATE_MAX:.0e}")
        return 1
    mf = np.linalg.norm(U, axis=1) * 1000.0
    mr = np.linalg.norm(resid, axis=1) * 1000.0
    rigid_frac = 1.0 - (np.median(mr) / np.median(mf) if np.median(mf) > 0 else 0.0)
    with open(out, "w") as fh:
        fh.write("x y z dx dy dz  # rigid-removed residual (small->coupled, 06 two-way)\n")
        for (x, y, z), (ux, uy, uz) in zip(X, resid):
            fh.write(f"{x:.8e} {y:.8e} {z:.8e} {ux:.8e} {uy:.8e} {uz:.8e}\n")
    if mr.max() / 1000.0 > WARN_RESID_MAX:
        print(f"RESID06-WARN t{nn} resid_max {mr.max():.1f} mm > {WARN_RESID_MAX*1000:.0f} mm")
    print(f"RESID06-OK t{nn} n={len(X)} full_med={np.median(mf):.3f}mm full_max={mf.max():.3f}mm "
          f"resid_med={np.median(mr):.3f}mm resid_max={mr.max():.3f}mm "
          f"rigid_frac={rigid_frac:.3f} gate={gate:.2e}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
