#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_shellE.py -- D->E secant feedback table for the small model's lining shells.

E(cell) = max(E0 * (1 - D_hat), E_FLOOR); invalid / guard cells -> E0 (no feedback).
E0 is read from shell_registry.txt (must be uniform: single damage source rule).
Output shellE_tNN.txt is the 24x5 cell table consumed by apply_shellE in
ss06_kernel.f3dat ('isec iband E', 1 header line).

Usage:  python make_shellE.py NN           (needs dmg_map_tNN.txt)
        python make_shellE.py --identity   (all cells E0 -> shellE_identity.txt;
                                            smoke-test the FISH write path)
Prints 'SHELLE-OK ...' on success; 'SHELLE-FAIL ...' + exit 1 otherwise.
"""
import sys
from pathlib import Path

import numpy as np

NSEC, NBAND = 24, 5
E_FLOOR = 2.5e9          # cracked-RC residual stiffness (05 ruling, unchanged)
M_EXP = 1.0              # E = E0*(1-D)^m, m=1 (STRATEGY §3)


def read_e0():
    reg = Path("shell_registry.txt")
    if not reg.exists():
        print("SHELLE-FAIL missing shell_registry.txt (run smoke first)")
        sys.exit(1)
    y = np.loadtxt(reg, skiprows=1, usecols=(3,), ndmin=1)
    e0 = float(np.median(y))
    if (np.abs(y - e0) / e0).max() > 1e-6:
        print(f"SHELLE-FAIL shell young not uniform (min={y.min():.4e} max={y.max():.4e})")
        sys.exit(1)
    return e0, len(y)


def write_table(out, E):
    with open(out, "w") as fh:
        fh.write("isec iband E\n")
        for s in range(1, NSEC + 1):
            for ib in range(1, NBAND + 1):
                fh.write(f"{s} {ib} {E[s, ib]:.6e}\n")


def main():
    e0, nshell = read_e0()
    E = np.full((NSEC + 1, NBAND + 1), e0)

    if sys.argv[1] == "--identity":
        write_table("shellE_identity.txt", E)
        print(f"SHELLE-OK identity E0={e0:.6e} nshell={nshell} cells={NSEC*NBAND}")
        return 0

    t = int(sys.argv[1])
    nn = f"{t:02d}"
    dm = Path(f"dmg_map_t{nn}.txt")
    if not dm.exists():
        print(f"SHELLE-FAIL missing {dm}")
        return 1
    d = np.loadtxt(dm, ndmin=2)
    nred = 0
    for row in d:
        s, ib, dhat, valid = int(row[0]), int(row[1]), row[8], int(row[9])
        if valid and dhat > 0.0:
            e = max(e0 * (1.0 - dhat) ** M_EXP, E_FLOOR)
            if e < e0:
                E[s, ib] = e
                nred += 1
    write_table(f"shellE_t{nn}.txt", E)
    print(f"SHELLE-OK t{nn} E0={e0:.6e} nshell={nshell} reduced_cells={nred} "
          f"minE={E[1:, 1:].min():.6e} minE_ratio={E[1:, 1:].min()/e0:.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
