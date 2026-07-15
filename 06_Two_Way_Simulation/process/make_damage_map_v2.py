#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_damage_map_v2.py -- per-tick lining damage map D(s,y) for the 06 two-way chain.

SOLAR §5 compliant:
  * cells: 24 x 15 deg sectors x 5 y-bands (860-910, 10 m each), straight-tunnel frame
    theta = atan2(x-1297, z-1747.5) in deg wrapped to [0,360); isec = int(theta/15)+1;
    iband = int((y-860)/10)+1 clamped [1,5]
    -- EXACTLY the formula in ss06_kernel.f3dat apply_shellE (FISH side). Do not change
       one without the other.
  * denominator: stage-0 bond registry (breakable=1 rows of cpl_bond_registry.txt),
    FROZEN for the whole chain. n_bond=0 -> invalid; n_bond<8 -> merged clockwise.
  * numerator: cumulative crack count from cs_s{t}_cracks.txt MINUS the per-cell
    CONTROL-0 baseline (cs_control0_cracks.txt), floored at 0.
  * guard bands: iband 1 and 5 forced D=0 (end effects are not fed back).
  * D_reg = circular 3-sector moving average (valid cells only) of D_raw, clamped
    to [0, 0.9]; D_hat = max(D_reg, previous tick's D_hat)  (monotonic damage).

Usage: python make_damage_map_v2.py NN     (run from 06/process)
Reads : cpl_bond_registry.txt, cs_control0_cracks.txt, cs_s{N}_cracks.txt,
        dmg_map_t{NN-1}.txt (if NN>1)
Writes: dmg_map_tNN.txt
Prints 'DMG-OK ...' on success; 'DMG-FAIL ...' + exit 1 otherwise.
"""
import sys
from pathlib import Path

import numpy as np

CX, CZ = 1297.0, 1747.5
Y0 = 860.0
NSEC, NBAND = 24, 5
MIN_BOND = 8
D_CAP = 0.9
GUARD_BANDS = (1, NBAND)


def cells_of(x, y, z):
    th = np.degrees(np.arctan2(x - CX, z - CZ)) % 360.0
    isec = np.minimum((th / 15.0).astype(int) + 1, NSEC)
    ib = np.clip(((y - Y0) / 10.0).astype(int) + 1, 1, NBAND)
    return isec, ib


def bincount2d(x, y, z):
    isec, ib = cells_of(x, y, z)
    n = np.zeros((NSEC + 1, NBAND + 1), dtype=int)   # 1-based
    np.add.at(n, (isec, ib), 1)
    return n


def load_xyz(path, what):
    p = Path(path)
    if not p.exists():
        print(f"DMG-FAIL missing {what}: {path}")
        sys.exit(1)
    try:
        d = np.loadtxt(p, skiprows=1, usecols=(0, 1, 2), ndmin=2)
    except Exception:
        d = np.zeros((0, 3))
    return d


def main():
    t = int(sys.argv[1])
    nn = f"{t:02d}"

    reg = np.loadtxt("cpl_bond_registry.txt", skiprows=1, ndmin=2)
    brk = reg[reg[:, 3] > 0.5]
    n_bond = bincount2d(brk[:, 0], brk[:, 1], brk[:, 2])

    ctrl = load_xyz("cs_control0_cracks.txt", "control-0 baseline")
    n_ctrl = bincount2d(ctrl[:, 0], ctrl[:, 1], ctrl[:, 2]) if len(ctrl) else \
        np.zeros((NSEC + 1, NBAND + 1), dtype=int)

    cr = load_xyz(f"cs_s{t}_cracks.txt", f"tick {t} cumulative cracks")
    n_cum = bincount2d(cr[:, 0], cr[:, 1], cr[:, 2]) if len(cr) else \
        np.zeros((NSEC + 1, NBAND + 1), dtype=int)

    n_net = np.maximum(n_cum - n_ctrl, 0)

    # --- clockwise merge of deficient cells (deterministic, registry-only => stable) ---
    # group id per (isec, iband); deficient cells chain onto the next sector's group.
    D_raw = np.zeros((NSEC + 1, NBAND + 1))
    valid = np.zeros((NSEC + 1, NBAND + 1), dtype=int)
    for ib in range(1, NBAND + 1):
        nb = n_bond[1:NSEC + 1, ib].astype(float)
        nn_ = n_net[1:NSEC + 1, ib].astype(float)
        if nb.sum() < MIN_BOND:
            continue                       # whole band invalid
        grp = np.arange(NSEC)              # start: each sector its own group
        # chain deficient (0 < group bonds < MIN_BOND) groups onto the next sector's
        # group, clockwise, until none left or a group wraps the full ring.
        for _ in range(2 * NSEC):
            gb = np.bincount(grp, weights=nb, minlength=NSEC)
            deficient = [s for s in range(NSEC) if 0 < gb[grp[s]] < MIN_BOND]
            if not deficient:
                break
            s = deficient[0]
            tgt = grp[(s + 1) % NSEC]
            if tgt == grp[s]:
                break                      # group wrapped the whole ring
            grp[grp == grp[s]] = tgt
        gb = np.bincount(grp, weights=nb, minlength=NSEC)
        gn = np.bincount(grp, weights=nn_, minlength=NSEC)
        for s in range(NSEC):
            if gb[grp[s]] >= MIN_BOND:
                D_raw[s + 1, ib] = gn[grp[s]] / gb[grp[s]]
                valid[s + 1, ib] = 1

    # --- circular 3-sector smoothing (valid-aware), clamp, guard bands ---
    D_reg = np.zeros_like(D_raw)
    for ib in range(1, NBAND + 1):
        for s in range(1, NSEC + 1):
            idxs = [((s - 2) % NSEC) + 1, s, (s % NSEC) + 1]
            vals = [D_raw[i, ib] for i in idxs if valid[i, ib]]
            if valid[s, ib] and vals:
                D_reg[s, ib] = float(np.mean(vals))
    D_reg = np.clip(D_reg, 0.0, D_CAP)
    for ib in GUARD_BANDS:
        D_reg[:, ib] = 0.0
        valid[1:, ib] = np.where(n_bond[1:, ib] > 0, 1, valid[1:, ib])

    # --- monotonic vs previous tick ---
    D_hat = D_reg.copy()
    prev = Path(f"dmg_map_t{t-1:02d}.txt")
    if t > 1:
        if not prev.exists():
            print(f"DMG-FAIL missing previous map {prev} (monotonic guarantee)")
            return 1
        pd = np.loadtxt(prev, ndmin=2)
        for row in pd:
            D_hat[int(row[0]), int(row[1])] = max(D_hat[int(row[0]), int(row[1])], row[8])
        D_hat = np.clip(D_hat, 0.0, D_CAP)
        for ib in GUARD_BANDS:                       # guards stay 0 forever
            D_hat[:, ib] = 0.0

    with open(f"dmg_map_t{nn}.txt", "w") as fh:
        fh.write("# isec iband n_bond n_cum n_ctrl n_net D_raw D_reg D_hat valid  "
                 f"(tick {t}; frame atan2(x-{CX}, z-{CZ}); guards iband 1,{NBAND})\n")
        for s in range(1, NSEC + 1):
            for ib in range(1, NBAND + 1):
                fh.write(f"{s} {ib} {n_bond[s, ib]} {n_cum[s, ib]} {n_ctrl[s, ib]} "
                         f"{n_net[s, ib]} {D_raw[s, ib]:.6f} {D_reg[s, ib]:.6f} "
                         f"{D_hat[s, ib]:.6f} {valid[s, ib]}\n")

    core = D_hat[1:, 2:NBAND]        # non-guard bands
    print(f"DMG-OK t{nn} cracks_cum={len(cr)} ctrl={len(ctrl)} net={int(n_net.sum())} "
          f"bonds={int(n_bond.sum())} valid_cells={int(valid[1:, 1:].sum())}/120 "
          f"maxDraw={D_raw.max():.4f} maxDhat={D_hat.max():.4f} coreMaxD={core.max():.4f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
