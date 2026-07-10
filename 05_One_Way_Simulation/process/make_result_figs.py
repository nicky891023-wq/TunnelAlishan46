#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_result_figs.py -- coupled-model result figures FIG-A..G + quant_summary.json
Spec: 05/docs/RESULTS_FIGURE_SPEC.md (quantitative standard S0).
Inputs: cs_s1..11_cracks.txt / cs_s*_cwall.txt / cs_s*_pmap.txt /
        couple_staged_v2.log (CS-CHK, MID-CONV, QA-WALL) / bond_census_G4.txt
Run:    python make_result_figs.py   (cwd = 05/process; output -> ../result/)

Styling (Wade 2026-07-08): ALL labels English, Times New Roman (serif),
fonts enlarged ~3-4x over matplotlib defaults; figure sizes scaled to fit.
"""
import json, re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# light-gray (empty) -> red (high) colormap for lining distribution maps
GRAYRED = LinearSegmentedColormap.from_list(
    "grayred", ["#e3e3e3", "#f7c9b8", "#f08a63", "#e03020", "#8a0000"])

# ---- global style: Times New Roman, fonts ~3-4x default ----
matplotlib.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",      # serif math for theta / Delta
    "font.size": 30,                 # base ~3x default (10)
    "axes.titlesize": 34,
    "axes.labelsize": 32,
    "xtick.labelsize": 26,
    "ytick.labelsize": 26,
    "legend.fontsize": 26,
    "figure.titlesize": 38,
    "axes.linewidth": 1.6,
    "lines.linewidth": 3.0,
    "lines.markersize": 11,
    "savefig.bbox": "tight",
})

HERE = Path(__file__).parent
OUT  = HERE.parent / "result"
CX, CZ = 1297.0, 1747.5
TH_BINS = np.arange(0, 361, 15)          # 24 x 15deg
Y_BINS  = np.arange(860, 911, 10)        # 5 x 10m
FEET_Z  = 1745.30
STAGES  = list(range(1, 12))
WATER   = ["W-110","W-90","W-70","W-50","W-30","W-10","W-30","W-50","W-70","W-90","W-110"]
DAYS    = [30, 5, 5, 5, 5, 30, 5, 5, 5, 5, 30]
PHASE   = ["dry1","rise","rise","rise","rise","wet","fall","fall","fall","fall","dry2"]
PHASE_C = {"dry1":"0.6","rise":"#4a7fb5","wet":"#c0392b","fall":"#7fb3d5","dry2":"0.6"}
BAND_ABS = 0.02                          # damage-band absolute threshold floor

def load_cracks(k):
    return np.loadtxt(HERE / f"cs_s{k}_cracks.txt", skiprows=1, ndmin=2)  # x y z type diam age

def sector_counts(d):
    x, y, z = d[:,0], d[:,1], d[:,2]
    th = np.degrees(np.arctan2(z-CZ, x-CX)) % 360
    keep = z > FEET_Z
    H, _, _ = np.histogram2d(th[keep], y[keep], bins=[TH_BINS, Y_BINS])
    return H  # 24 x 5

# ---- crown-centred "developed lining" mapping (crown=0, right foot=+, left foot=-) ----
PHI_BINS = np.arange(-150, 150.001, 1.0)     # fine: 1 deg
YF_BINS  = np.arange(860, 910.001, 0.5)      # fine: 0.5 m
def crown_phi(x, z):
    return np.degrees(np.arctan2(x - CX, z - CZ))   # 0=crown, +90=R spring, -90=L spring
def crown_hist(d):
    phi = crown_phi(d[:, 0], d[:, 2])
    H, _, _ = np.histogram2d(phi, d[:, 1], bins=[PHI_BINS, YF_BINS])
    return H
def annotate_ring(ax):
    ax.axvline(0,  color="0.45", ls="--", lw=1.4)     # crown
    ax.axvline(90, color="0.6",  ls=":",  lw=1.2)     # right springline
    ax.axvline(-90,color="0.6",  ls=":",  lw=1.2)     # left springline

def main():
    OUT.mkdir(exist_ok=True)
    census = np.loadtxt(HERE / "bond_census_G4.txt")          # 24x5 breakable-bond census
    cum   = {k: load_cracks(k) for k in STAGES}
    Ncum  = {k: len(cum[k]) for k in STAGES}
    Hcum  = {k: sector_counts(cum[k]) for k in STAGES}
    D     = {k: np.clip(Hcum[k] / np.maximum(census, 1), 0, 1) for k in STAGES}
    dN    = {k: Ncum[k] - (Ncum[k-1] if k > 1 else 0) for k in STAGES}
    rate  = {k: dN[k] / DAYS[k-1] for k in STAGES}
    floor = min(rate[k] for k in STAGES if PHASE[k-1] in ("fall", "dry2"))
    A_wet = rate[6] / max(np.mean([rate[k] for k in (2,3,4,5)]), 1e-9)
    A_frz = np.mean([rate[k] for k in (8,9,10,11)]) / max(rate[6], 1e-9)

    # ---------- FIG-A : damage-evolution history (money plot) ----------
    fig, ax = plt.subplots(figsize=(19, 11))
    ks = STAGES[1:]                                            # trend stats exclude stage 1
    ax.bar(ks, [dN[k] for k in ks], color=[PHASE_C[PHASE[k-1]] for k in ks],
           edgecolor="k", lw=0.8)
    ax.set_xlabel("Stage (water level)")
    ax.set_ylabel(r"Damage increment $\Delta N$ (bond breaks)")
    ax.set_xticks(ks); ax.set_xticklabels([f"{k}\n{WATER[k-1]}" for k in ks])
    ax2 = ax.twinx()
    lv = [-110,-90,-70,-50,-30,-10,-30,-50,-70,-90,-110]
    ax2.plot(STAGES, lv, "b-o", ms=10, alpha=.7)
    ax2.set_ylabel("Water level (m)", color="b"); ax2.tick_params(axis="y", colors="b")
    Dtot = [100*Ncum[k]/census.sum() for k in STAGES]
    ax3 = ax.twinx(); ax3.spines.right.set_position(("axes", 1.14))
    ax3.plot(STAGES, Dtot, "r--", lw=3)
    ax3.set_ylabel("Cumulative damage density (%)", color="r"); ax3.tick_params(axis="y", colors="r")
    ax.set_title(f"Lining damage evolution (f=0.25, trend)   "
                 f"$A_{{wet}}$={A_wet:.2f}   $A_{{frz}}$={A_frz:.2f}")
    fig.savefig(OUT / "FIG_A_damage_history.png", dpi=200); plt.close(fig)

    # ---------- FIG-B : crack distribution, crown-centred fine map (6 selected) ----------
    sel = [1, 3, 5, 6, 8, 11]
    Hs = {k: crown_hist(cum[k]) for k in STAGES}
    allnz = np.concatenate([Hs[k][Hs[k] > 0].ravel() for k in sel]) if sel else np.array([1])
    vmax = np.percentile(allnz, 98) if allnz.size else 1
    fig, axs = plt.subplots(2, 3, figsize=(26, 13), sharex=True, sharey=True)
    for ax_, k in zip(axs.flat, sel):
        im = ax_.pcolormesh(PHI_BINS, YF_BINS, Hs[k].T, vmin=0, vmax=vmax,
                            cmap=GRAYRED, shading="flat")
        ax_.set_facecolor("#e3e3e3"); annotate_ring(ax_)
        ax_.set_title(f"s{k}  {WATER[k-1]} ({PHASE[k-1]})")
    for ax_ in axs[-1, :]:
        ax_.set_xlabel("Angle from crown (deg)")
        ax_.set_xticks([-135,-90,0,90,135])
        ax_.set_xticklabels(["L foot","L spr","Crown","R spr","R foot"], fontsize=20)
    for ax_ in axs[:, 0]:
        ax_.set_ylabel("y (m)")
    fig.colorbar(im, ax=axs, label="Crack count / cell", shrink=.85, extend="max")
    fig.suptitle("Crack distribution - developed lining (crown at centre, feet at edges)")
    fig.savefig(OUT / "FIG_B_damage_maps.png", dpi=220); plt.close(fig)

    # ---------- FIG-D : sectional chronology + radial fiber ----------
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(23, 10), constrained_layout=True)
    d11 = cum[11]; t = d11[:, 5]
    births = np.searchsorted([np.max(cum[k][:, 5]) for k in STAGES], t) + 1
    mid = (d11[:, 1] > 870) & (d11[:, 1] < 900)
    sc = a1.scatter(d11[mid, 0], d11[mid, 2], c=births[mid], s=10, cmap="coolwarm")
    fig.colorbar(sc, ax=a1, label="Birth stage", fraction=0.046, pad=0.04)
    a1.set_aspect("equal")
    a1.set_xlabel("x (m)"); a1.set_ylabel("z (m)")
    a1.set_title("Sectional damage chronology (y 870-900)")
    r = np.sqrt((d11[:,0]-CX)**2 + (d11[:,2]-CZ)**2)
    grp = {"Dry/rise (1-5)": births <= 5, "Wet (6)": births == 6, "Retreat/dry (7-11)": births >= 7}
    w = 0.25
    for i, (lab, m) in enumerate(grp.items()):
        fr = [np.mean(r[m] < 1.55), np.mean((r[m] >= 1.55) & (r[m] <= 1.85)), np.mean(r[m] > 1.85)]
        a2.bar(np.arange(3)+i*w, fr, w, label=lab)
    a2.set_xticks(np.arange(3)+w); a2.set_xticklabels(["Inner", "Mid", "Outer"])
    a2.set_ylabel("Fraction"); a2.legend()
    a2.set_title("Radial fiber distribution (flexural tension)")
    fig.savefig(OUT / "FIG_D_section.png", dpi=200); plt.close(fig)

    # ---------- FIG-E : lining-rock interaction history ----------
    log = (HERE / "couple_staged_v2.log").read_text(errors="ignore")
    mwf = re.findall(r"^MID-WALL cs_s(\d+) .*?abs_normal=([-\d.eE+]+)MN", log, re.M)
    mc  = re.findall(r"^MID-CONV cs_s(\d+) .*?radial_inward mean=([-\d.eE+]+)mm", log, re.M)
    qw  = re.findall(r"^QA-WALL cs_s(\d+) .*?wz_outter=([-\d.eE+]+)MN", log, re.M)
    fig, axs = plt.subplots(1, 3, figsize=(24, 8))
    for ax_, data, title in [
            (axs[0], mc,  "Mid-band bore convergence (mm)"),
            (axs[1], mwf, "Mid-band lining normal |F| (MN)"),
            (axs[2], qw,  "wz_outter total reaction (MN)")]:
        if data:
            kk = [int(a) for a, _ in data]; vv = [float(b) for _, b in data]
            ax_.plot(kk, vv, "k-o", ms=11)
        ax_.set_title(title); ax_.set_xlabel("Stage")
    fig.savefig(OUT / "FIG_E_interaction.png", dpi=200); plt.close(fig)

    # ---------- FIG-B appendix : all 11 stages, crown-centred fine map ----------
    allnz2 = np.concatenate([Hs[k][Hs[k] > 0].ravel() for k in STAGES])
    vmax_all = np.percentile(allnz2, 98) if allnz2.size else 1
    fig, axs = plt.subplots(3, 4, figsize=(30, 17), sharex=True, sharey=True)
    for ax_, k in zip(axs.flat, STAGES):
        im = ax_.pcolormesh(PHI_BINS, YF_BINS, Hs[k].T, vmin=0, vmax=vmax_all,
                            cmap=GRAYRED, shading="flat")
        ax_.set_facecolor("#e3e3e3"); annotate_ring(ax_)
        ax_.set_title(f"s{k}  {WATER[k-1]}")
    axs.flat[-1].axis("off")
    for ax_ in axs[-1, :]:
        ax_.set_xlabel("Angle from crown (deg)")
    for ax_ in axs[:, 0]:
        ax_.set_ylabel("y (m)")
    fig.colorbar(im, ax=axs, label="Crack count / cell", shrink=.8, extend="max")
    fig.suptitle("Crack distribution - developed lining, all 11 stages (crown centre, feet edges)")
    fig.savefig(OUT / "FIG_B_damage_maps_all11.png", dpi=220); plt.close(fig)

    # ---------- FIG-G : lining external pressure, crown-centred (all stages) ----------
    # pmap native resolution = 24 sectors x 5 y-bands (coarser than cracks; finer needs re-export)
    try:
        phic = ((90 - np.arange(0, 360, 15) + 180) % 360) - 180   # 24 sector centres -> crown-centred
        order = np.argsort(phic); phis = phic[order]
        edges = np.concatenate([[phis[0]-7.5], (phis[:-1]+phis[1:])/2, [phis[-1]+7.5]])
        def pgrid(k):
            pm = np.loadtxt(HERE / f"cs_s{k}_pmap.txt", skiprows=1)
            g = np.full((5, 24), 0.0)
            for s, b, v in zip(pm[:, 0], pm[:, 1].astype(int), pm[:, 2]):
                g[b-1, int(s)//15] = v / 1000.0                   # kN
            return g[:, order]
        G = {k: pgrid(k) for k in STAGES}
        vmaxp = np.percentile(np.concatenate([np.clip(G[k], 0, None).ravel() for k in STAGES]), 97)
        fig, axs = plt.subplots(3, 4, figsize=(30, 17), sharex=True, sharey=True)
        for ax_, k in zip(axs.flat, STAGES):
            im = ax_.pcolormesh(edges, Y_BINS, np.clip(G[k], 0, None), cmap=GRAYRED,
                                vmin=0, vmax=vmaxp, shading="flat")
            ax_.set_facecolor("#e3e3e3"); ax_.set_xlim(-150, 150); annotate_ring(ax_)
            ax_.set_title(f"s{k}  {WATER[k-1]}")
        axs.flat[-1].axis("off")
        for ax_ in axs[-1, :]:
            ax_.set_xlabel("Angle from crown (deg)")
        for ax_ in axs[:, 0]:
            ax_.set_ylabel("y (m)")
        fig.colorbar(im, ax=axs, label="Radial pressure (kN/sector)", shrink=.8, extend="max")
        fig.suptitle("Lining external pressure - developed lining, all 11 stages "
                     "(native 24x5 sectors; crown centre, feet edges)")
        fig.savefig(OUT / "FIG_G_pressure_maps.png", dpi=220); plt.close(fig)
    except Exception as e:
        print("FIG-G skipped (check cs_s*_pmap.txt format):", e)

    json.dump({"A_wet": A_wet, "A_frz": A_frz, "floor_per_day": floor,
               "N_cum": Ncum, "dN": dN, "rate_per_day": rate,
               "D_total_pct": Dtot[-1]},
              open(OUT / "quant_summary.json", "w"), indent=2)
    print("FIGS done ->", OUT)

if __name__ == "__main__":
    main()
