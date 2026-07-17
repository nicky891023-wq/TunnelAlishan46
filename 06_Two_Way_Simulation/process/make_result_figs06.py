#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_result_figs06.py -- journal-grade result figures for the 06 two-way T5 chain.

Idempotent + tick-aware: plots whatever ticks are committed in output/t5/manifest.json,
so it can run mid-chain (progress check) and re-run at t26 for the final set.
Style follows 05/process/thesis_style.py (IJRMMS_CHFT benchmark conventions).

Outputs -> 06_Two_Way_Simulation/result/
  FIG06-01_cracks_timeline.png   cumulative + per-tick increments vs the v6 one-way chain
  FIG06-02_damage_map.png        D-hat(s,y) heatmap panels at milestone ticks
  FIG06-03_feedback_E.png        shell-E feedback trajectory (minE ratio, reduced cells)
  FIG06-04_drive_residual.png    per-tick drive residual magnitude vs 05 stage values
  FIG06-05_convergence.png       small-model vclose/hclose vs 05 hybrid baseline
  FIG06-06_active_zones.png      creep-active zone count vs day
  FIG06-07_sector_rose.png       final crack sector distribution vs v6 s11
  T06_tick_summary.csv           per-tick numbers table
Run from 06/process:  python make_result_figs06.py
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

P05 = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process")
P06 = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/06_Two_Way_Simulation/process")
OUT5 = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/06_Two_Way_Simulation/output/t5")
RES = Path(r"C:/Users/Wade/Desktop/Tunnel_TX/06_Two_Way_Simulation/result")
RES.mkdir(exist_ok=True)

sys.path.insert(0, str(P05))
import thesis_style as TS  # noqa: E402  (apply() + palette; output path is ours)
import matplotlib.pyplot as plt  # noqa: E402

TS.apply(scale=0.62)

# ---- chain constants (must match run_t5.py) ----
STAGE_OF_TICK = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 7, 8, 9, 10,
                 11, 11, 11, 11, 11, 11]
STAGE_END_DAY = {1: 30, 2: 35, 3: 40, 4: 45, 5: 50, 6: 80, 7: 85, 8: 90, 9: 95,
                 10: 100, 11: 130}
LEVEL_OF_STAGE = dict(zip(range(1, 12), TS.LEVEL))
CTRL0_06 = 42          # 06 CONTROL-0 crack baseline
CTRL0_05 = 28          # v6 CONTROL-0 crack baseline
C1, C2, C3 = "#e0231c", "#29abe2", "0.35"   # two-way red, one-way blue, aux gray


def water_day_steps():
    xs, ys = [], []
    d0 = 0
    for s in range(1, 12):
        d1 = STAGE_END_DAY[s]
        xs += [d0, d1]
        ys += [LEVEL_OF_STAGE[s], LEVEL_OF_STAGE[s]]
        d0 = d1
    return np.array(xs), np.array(ys)


# ---- load 06 manifest ----
m = json.loads((OUT5 / "manifest.json").read_text(encoding="utf-8"))
ticks = sorted(int(k) for k, v in m["ticks"].items() if v.get("state") == "committed")
if not ticks:
    sys.exit("no committed ticks")
T = {}
for t in ticks:
    e = m["ticks"][f"{t:02d}"]
    dm = re.search(r"maxDhat=([\d.]+)", e.get("damage", ""))
    se = re.search(r"reduced_cells=(\d+) minE=([\deE.+-]+) minE_ratio=([\d.]+)",
                   e.get("shellE", ""))
    rr = re.search(r"resid_med=([\d.]+)mm resid_max=([\d.]+)mm", e["resid"]["line"])
    T[t] = dict(day=e["small"]["day"], vclose=e["small"]["vclose"],
                hclose=e["small"]["hclose"], active=e["small"]["active"],
                cum=e["coupled"]["cracks_cum"] - CTRL0_06, inc=e["coupled"]["cracks_inc"],
                gp=e["coupled"]["gp_dmax"], ball=e["coupled"]["ball_dmax"],
                dhat=float(dm.group(1)) if dm else np.nan,
                ncell=int(se.group(1)) if se else 0,
                eratio=float(se.group(3)) if se else 1.0,
                rmed=float(rr.group(1)) if rr else np.nan,
                rmax=float(rr.group(2)) if rr else np.nan)
days = np.array([T[t]["day"] for t in ticks])
last = ticks[-1]
print(f"committed ticks: {len(ticks)} (through t{last:02d}, day {days[-1]:.0f})")

# ---- v6 one-way baseline (coupled) ----
v6 = []
for ln in (P05 / "couple_staged_v6.log").read_text(errors="ignore").splitlines():
    mm = re.match(r"CS-CHK stg(\d+) cracks_t=(\d+) cracks_s=(\d+)", ln)
    if mm:
        v6.append((int(mm.group(1)), int(mm.group(2)) + int(mm.group(3)) - CTRL0_05))
v6days = np.array([STAGE_END_DAY[s] for s, _ in v6])
v6cum = np.array([c for _, c in v6])

# ---- 05 small-model hybrid baseline (s1 rerun T=1.0 + old chain s2-11) ----
def hist_lines(path, pat):
    out = []
    for ln in Path(path).read_text(errors="ignore").splitlines():
        mm = re.match(pat, ln)
        if mm:
            out.append(tuple(float(g) for g in mm.groups()))
    return out

H_PAT = (r"SSv2-HIST stg=(\d+) day=([\d.]+) vclose=([-\d.eE+]+) hclose=([-\d.eE+]+) "
         r"dmax=([-\d.eE+]+) active=(\d+)")
h05 = hist_lines(P05 / "small_s1_rerun.log", H_PAT)
h05 += [h for h in hist_lines(P05 / "small_staged_v2.log", H_PAT) if h[0] >= 2]
h05 = np.array(h05)
H06_PAT = (r"SS06-HIST stg=(\d+) day=([\d.]+) vclose=([-\d.eE+]+) hclose=([-\d.eE+]+) "
           r"dmax=([-\d.eE+]+) active=(\d+)")
h06 = []
for t in ticks:
    h06 += hist_lines(P06 / f"ss06_t{t:02d}.log", H06_PAT)
h06 = np.array(h06)

# ============================ FIG06-01 cracks timeline ============================
fig, (a, b) = plt.subplots(2, 1, figsize=(12, 9), sharex=True,
                           gridspec_kw={"height_ratios": [3, 2]})
a.plot(days, [T[t]["cum"] for t in ticks], "-o", color=C1, label="Two-way (T5, 5-day ticks)")
a.plot(v6days, v6cum, "--s", color=C2, label="One-way (v6, stage-wise)")
aw = a.twinx()
xs, ys = water_day_steps()
aw.plot(xs, ys, color=TS.C_WATER, lw=1.6, alpha=0.6)
aw.set_ylabel("Water level (m)", color=TS.C_WATER)
aw.tick_params(axis="y", colors=TS.C_WATER)
aw.grid(False)
a.set_ylabel("Cumulative bond breaks (net)")
a.legend(loc="upper left")
a.set_title("(a) Cumulative lining damage: two-way vs one-way", loc="left")
b.bar(days, [T[t]["inc"] for t in ticks], width=3.6, color=C1, alpha=0.85,
      label="Two-way per-tick")
v6inc = np.diff(np.concatenate([[0], v6cum]))
b.step(np.concatenate([[0], v6days]), np.concatenate([v6inc, [v6inc[-1]]]),
       where="post", color=C2, lw=2.0, label="One-way per-stage")
b.axhline(30000, color=C3, ls=":", lw=1.5)
b.text(days[-1], 30500, "stop gate 30k", ha="right", fontsize=13, color=C3)
b.set_xlabel("Time (days)")
b.set_ylabel("Breaks per step")
b.legend(loc="upper right")
b.set_title("(b) Damage increments", loc="left")
fig.savefig(RES / "FIG06-01_cracks_timeline.png")
plt.close(fig)

# ============================ FIG06-02 damage map panels ============================
mile = [t for t in (6, 11, 16, 26) if t in ticks]
if len(mile) < 4:
    mile = sorted(set(ticks[:: max(1, len(ticks) // 4)][-4:]))
fig, axs = plt.subplots(1, len(mile), figsize=(4.2 * len(mile) + 1.6, 4.4), sharey=True)
axs = np.atleast_1d(axs)
vmax = max(0.05, max(T[t]["dhat"] for t in ticks))
for ax, t in zip(axs, mile):
    d = np.loadtxt(P06 / f"dmg_map_t{t:02d}.txt", ndmin=2)
    G = np.full((24, 5), np.nan)
    for row in d:
        G[int(row[0]) - 1, int(row[1]) - 1] = row[8] if row[9] > 0 else np.nan
    pc = ax.pcolormesh(np.arange(0, 361, 15), np.arange(860, 911, 10), G.T,
                       cmap="YlOrRd", vmin=0, vmax=vmax, edgecolors="0.8", lw=0.3)
    ax.set_facecolor("0.75")
    ax.set_xticks([0, 90, 180, 270, 360])
    ax.set_xlabel(r"$\theta$ from crown ($^\circ$)")
    ax.set_title(f"day {T[t]['day']:.0f} (t{t:02d})", fontsize=15)
axs[0].set_ylabel("y (m)")
cb = fig.colorbar(pc, ax=axs, fraction=0.025, pad=0.02)
cb.set_label(r"$\hat{D}$ (regularized, monotonic)")
fig.suptitle("Lining damage map evolution (gray = invalid / no denominator)",
             y=1.04, fontsize=17)
fig.savefig(RES / "FIG06-02_damage_map.png")
plt.close(fig)

# ============================ FIG06-03 feedback E trajectory ============================
fig, a = plt.subplots(figsize=(11, 5.5))
a.plot(days, [100 * (1 - T[t]["eratio"]) for t in ticks], "-o", color=C1,
       label="max shell-E reduction (%)")
a.set_ylabel("Max E reduction (%)", color=C1)
a.tick_params(axis="y", colors=C1)
a2 = a.twinx()
a2.plot(days, [T[t]["ncell"] for t in ticks], "-s", color=C2, label="cells fed back")
a2.set_ylabel("Cells with E < E$_0$ (of 120)", color=C2)
a2.tick_params(axis="y", colors=C2)
a2.grid(False)
a.set_xlabel("Time (days)")
a.set_title("D→E feedback trajectory (E = E$_0$(1$-$$\\hat{D}$), floor 2.5 GPa)",
            loc="left")
fig.savefig(RES / "FIG06-03_feedback_E.png")
plt.close(fig)

# ============================ FIG06-04 drive residual ============================
r05 = []
for s in range(1, 12):
    f = P05 / f"cpl_resid_s{s:02d}.txt"
    if f.exists():
        d = np.loadtxt(f, skiprows=1)
        r = np.linalg.norm(d[:, 3:6], axis=1) * 1000
        r05.append((STAGE_END_DAY[s], np.median(r), r.max()))
r05 = np.array(r05)
fig, a = plt.subplots(figsize=(11, 5.5))
a.plot(days, [T[t]["rmed"] for t in ticks], "-o", color=C1, label="Two-way median")
a.plot(days, [T[t]["rmax"] for t in ticks], "--o", color=C1, alpha=0.5,
       label="Two-way max", ms=5)
a.plot(r05[:, 0], r05[:, 1], "s", color=C2, label="One-way median (stage)")
a.plot(r05[:, 0], r05[:, 2], "s", color=C2, alpha=0.45, label="One-way max (stage)")
a.set_xlabel("Time (days)")
a.set_ylabel("Rigid-removed boundary residual (mm)")
a.set_title("Coupling drive magnitude (cumulative field)", loc="left")
a.legend(loc="upper left", fontsize=13)
fig.savefig(RES / "FIG06-04_drive_residual.png")
plt.close(fig)

# ============================ FIG06-05 convergence ============================
fig, a = plt.subplots(figsize=(12, 5.8))
a.plot(h06[:, 1], h06[:, 2], "-", color=C1, label="Two-way $v_{close}$")
a.plot(h06[:, 1], h06[:, 3], "--", color=C1, alpha=0.6, label="Two-way $h_{close}$")
a.plot(h05[:, 1], h05[:, 2], "-", color=C2, lw=1.6, label="One-way $v_{close}$ (hybrid)")
a.plot(h05[:, 1], h05[:, 3], "--", color=C2, lw=1.6, alpha=0.6,
       label="One-way $h_{close}$ (hybrid)")
aw = a.twinx()
aw.plot(*water_day_steps(), color=TS.C_WATER, lw=1.5, alpha=0.55)
aw.set_ylabel("Water level (m)", color=TS.C_WATER)
aw.tick_params(axis="y", colors=TS.C_WATER)
aw.grid(False)
a.set_xlabel("Time (days)")
a.set_ylabel("Tunnel closure (mm)")
a.set_title("Small-model convergence at y = 885 m", loc="left")
a.legend(loc="lower left", fontsize=13, ncol=2)
fig.savefig(RES / "FIG06-05_convergence.png")
plt.close(fig)

# ============================ FIG06-06 active zones ============================
fig, a = plt.subplots(figsize=(11, 5.2))
a.semilogy(days, [T[t]["active"] for t in ticks], "-o", color=C1, label="Two-way")
o5 = {1: 24935, 2: 152991}   # s1 = v6 rerun (T=1.0); s2 = old chain log
for ln in (P05 / "small_staged_v2.log").read_text(errors="ignore").splitlines():
    mm = re.match(r"   SSv2-stg(\d+) creep start: active=(\d+)", ln)
    if mm and int(mm.group(1)) >= 2:
        o5[int(mm.group(1))] = int(mm.group(2))
a.semilogy([STAGE_END_DAY[s] for s in sorted(o5)], [o5[s] for s in sorted(o5)],
           "s", color=C2, label="One-way (hybrid, stage)")
a.set_xlabel("Time (days)")
a.set_ylabel("Creep-active zones")
a.set_title("Threshold-activated zone population (T=1.0 in s1, 0.8 after)", loc="left")
a.legend()
fig.savefig(RES / "FIG06-06_active_zones.png")
plt.close(fig)

# ============================ FIG06-07 sector rose (final vs v6 s11) ============================
def sector_counts(path):
    d = np.loadtxt(path, skiprows=1, usecols=(0, 1, 2), ndmin=2)
    th = np.degrees(np.arctan2(d[:, 0] - 1297.0, d[:, 2] - 1747.5)) % 360
    return np.histogram(th, bins=np.arange(0, 361, 15))[0]

f06 = OUT5 / f"cs06_t{last:02d}_cracks.txt"
f05 = P05 / "cs_s11_cracks.txt"
if f06.exists() and f05.exists():
    c06, c05 = sector_counts(f06), sector_counts(f05)
    ang = np.radians(np.arange(7.5, 360, 15))
    fig = plt.figure(figsize=(11, 5.8))
    for i, (cc, tag, col) in enumerate([(c06, f"Two-way day {days[-1]:.0f}", C1),
                                        (c05, "One-way final (s11)", C2)]):
        ax = fig.add_subplot(1, 2, i + 1, projection="polar")
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.bar(ang, cc, width=np.radians(13), color=col, alpha=0.85)
        ax.set_title(tag, fontsize=15)
        ax.tick_params(labelsize=11)
    fig.suptitle(r"Crack count by sector ($\theta$ from crown, clockwise)", fontsize=17)
    fig.savefig(RES / "FIG06-07_sector_rose.png")
    plt.close(fig)

# ============================ table ============================
with open(RES / "T06_tick_summary.csv", "w", encoding="utf-8") as fh:
    fh.write("tick,stage,day,vclose_mm,hclose_mm,active,cracks_net_cum,cracks_inc,"
             "gp_dmax_m,ball_dmax_m,maxDhat,cells_fed,minE_ratio,resid_med_mm,resid_max_mm\n")
    for t in ticks:
        e = T[t]
        fh.write(f"{t},{STAGE_OF_TICK[t-1]},{e['day']:.0f},{e['vclose']:.4f},"
                 f"{e['hclose']:.4f},{e['active']},{e['cum']},{e['inc']},{e['gp']:.2e},"
                 f"{e['ball']:.4f},{e['dhat']:.4f},{e['ncell']},{e['eratio']:.4f},"
                 f"{e['rmed']:.3f},{e['rmax']:.3f}\n")
print("FIGS06 OK ->", RES)
for p in sorted(RES.glob("FIG06-*.png")):
    print("  ", p.name)
