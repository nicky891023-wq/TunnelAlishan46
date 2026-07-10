#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_cracknormals.py -- classify bond-break crack ORIENTATION by mechanism.
Each break's contact normal = crack-opening direction; crack surface is perpendicular.
Decompose the normal against tunnel geometry (radial r, hoop theta, axial y):
  normal ~ axial  (n.y  large) -> CIRCUMFERENTIAL crack (surface in x-z plane, rings the tunnel)
  normal ~ hoop   (n.th large) -> LONGITUDINAL crack   (surface contains axis, runs along tunnel)
  normal ~ radial (n.r  large) -> RADIAL / delamination (surface tangent to lining shell)
Input: cracknormals_s11.txt (x y z nx ny nz state).  state 1=tension, 2=shear.
"""
from pathlib import Path
import numpy as np

HERE = Path(__file__).parent
CX, CZ = 1297.0, 1747.5
d = np.loadtxt(HERE / "cracknormals_s11.txt", skiprows=1, ndmin=2)
x, y, z = d[:, 0], d[:, 1], d[:, 2]
n = d[:, 3:6]
state = d[:, 6].astype(int)

# geometry basis per break
rx, rz = x - CX, z - CZ
rmag = np.sqrt(rx*rx + rz*rz); rmag[rmag == 0] = 1e-9
r_hat = np.stack([rx/rmag, np.zeros_like(rx), rz/rmag], axis=1)   # radial (x-z plane)
y_hat = np.tile([0.0, 1.0, 0.0], (len(d), 1))                    # axial
# hoop = y_hat x r_hat
th_hat = np.cross(y_hat, r_hat)

n = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
a_ax  = np.abs(np.einsum('ij,ij->i', n, y_hat))    # axial component  -> circumferential crack
a_hp  = np.abs(np.einsum('ij,ij->i', n, th_hat))   # hoop component   -> longitudinal crack
a_rad = np.abs(np.einsum('ij,ij->i', n, r_hat))    # radial component -> delamination

comp = np.stack([a_ax, a_hp, a_rad], axis=1)
klass = np.argmax(comp, axis=1)   # 0=circumferential, 1=longitudinal, 2=radial
names = ["CIRCUMFERENTIAL (env)", "LONGITUDINAL (zong)", "RADIAL/delamination"]

def report(mask, title):
    m = mask
    tot = m.sum()
    if tot == 0:
        print(f"\n{title}: none"); return
    print(f"\n{title}: {tot} breaks")
    for i, nm in enumerate(names):
        c = ((klass == i) & m).sum()
        print(f"   {nm:26s}: {c:7d}  ({100*c/tot:5.1f}%)")
    # 'oblique' = no dominant component (max < 0.6)
    obl = (comp.max(1) < 0.6) & m
    print(f"   (oblique / no dominant   : {obl.sum():7d}  ({100*obl.sum()/tot:5.1f}%))")

report(np.ones(len(d), bool), "ALL breaks")
report(state == 1, "TENSION breaks (state 1)")
report(state == 2, "SHEAR breaks (state 2)")

# mean components
print(f"\nmean |n.axial|={a_ax.mean():.3f}  |n.hoop|={a_hp.mean():.3f}  |n.radial|={a_rad.mean():.3f}")
print("(higher axial => more circumferential cracking; higher hoop => more longitudinal)")
