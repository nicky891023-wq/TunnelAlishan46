#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_tables.py -- Tables 5-1..5-5 (CSV for Word + PNG previews), ALL-ENGLISH content
(Wade review 07-10: CJK glyphs tofu in Times New Roman renders).
Values from 04/parameter.f3dat (authoritative run inputs) + quant_summary.json.
"""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT

def _build_table_fig(figsize, cols, rows, fs, scale_y):
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    tb = ax.table(cellText=rows, colLabels=cols, loc="center", cellLoc="center")
    tb.auto_set_font_size(False)
    tb.set_fontsize(fs)
    tb.scale(1, scale_y)
    tb.auto_set_column_width(col=list(range(len(cols))))
    for j in range(len(cols)):
        tb[0, j].set_facecolor("#e8e2d0")
        tb[0, j].set_text_props(fontweight="bold")
    return fig, ax, tb

def render_table(name, title, cols, rows, fs=21, title_fs=25, scale_y=2.3):
    # pass 1: probe the pixel size the table/title actually need
    fig, ax, tb = _build_table_fig((16, 10), cols, rows, fs, scale_y)
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    inv_in = fig.dpi_scale_trans.inverted()
    tw = tb.get_window_extent(ren).transformed(inv_in)
    probe = fig.text(0.5, 0.5, title, fontsize=title_fs)
    fig.canvas.draw()
    ttw = probe.get_window_extent(ren).transformed(inv_in)
    plt.close(fig)
    # pass 2: rebuild sized to content so nothing clips at canvas edges
    fig_w = max(tw.width, ttw.width) + 1.0
    fig_h = tw.height + ttw.height + 1.2
    fig, ax, tb = _build_table_fig((fig_w, fig_h), cols, rows, fs, scale_y)
    fig.canvas.draw()
    ren = fig.canvas.get_renderer()
    tbb = tb.get_window_extent(ren)
    cx, top = ax.transAxes.inverted().transform(
        ((tbb.x0 + tbb.x1) / 2, tbb.y1))
    ttl = ax.set_title(title, fontsize=title_fs, x=cx, y=top, pad=12)
    fig.canvas.draw()
    bb = mtransforms.Bbox.union(
        [tbb, ttl.get_window_extent(ren)]).transformed(
        fig.dpi_scale_trans.inverted())
    bb = mtransforms.Bbox.from_extents(bb.x0 - 0.1, bb.y0 - 0.1,
                                       bb.x1 + 0.1, bb.y1 + 0.1)
    fig.savefig(OUT / f"{name}.png", dpi=180, bbox_inches=bb)
    plt.close(fig)
    with open(OUT / f"{name}.csv", "w", encoding="utf-8-sig") as f:
        f.write(",".join(cols) + "\n")
        for r in rows:
            f.write(",".join(str(x) for x in r) + "\n")
    print("saved", name)

# ---- Table 5-1 slope scale ----
render_table("表5-1_邊坡尺度模型參數",
    "Table 5-1  Slope-scale model rock parameters (Mohr-Coulomb + Burgers-Mohr "
    "threshold creep)",
    ["Layer", "E (GPa)", "v", "c (MPa)", "phi (deg)", "rho (kg/m3)",
     "sig_t (kPa)"],
    [["1 (colluvium)", "0.5", "0.25", "0.19", "29.1", "2150", "100"],
     ["2", "2.0", "0.25", "0.29", "35.1", "2630", "100"],
     ["3", "5.0", "0.25", "0.47", "44.3", "2600", "100"],
     ["4", "7.0", "0.25", "0.80", "51.5", "2600", "100"]])

# ---- Table 5-2 tunnel scale ----
render_table("表5-2_隧道圍岩擾動尺度模型參數",
    "Table 5-2  Tunnel-scale model rock and lining parameters",
    ["Layer", "E (GPa)", "c (MPa)", "phi (deg)", "rho (kg/m3)", "Note"],
    [["1", "1.0", "0.19", "29.1", "2600", ""],
     ["2", "2.0", "0.29", "35.1", "2630", ""],
     ["3", "3.5", "0.47", "44.3", "2630", ""],
     ["4 (tunnel host)", "1.5", "0.10", "30.0", "2630",
      "WET weathered SS/SH interbed"],
     ["5", "3.0", "0.80", "51.5", "2630", ""],
     ["6", "7.0", "2.06", "56.3", "2600", ""],
     ["Shell lining", "25", "fc=41.2 / ft=4.12 MPa", "-", "2400",
      "t=0.40 m, v=0.2"],
     ["Common", "v=0.25, sig_t=100 kPa", "eta_m=1.2e15, eta_k=2.4e13 Pa.s",
      "T=0.8", "k x100 annulus", "threshold T=0.8 unified"]])

# ---- Table 5-3 coupled scale ----
render_table("表5-3_圍岩襯砌互制尺度模型參數",
    "Table 5-3  Rock-lining interaction model parameters (FLAC3D elastic box + PFC "
    "linearpbond BPM)",
    ["Item", "Value", "Remark"],
    [["Rock equivalent modulus E_eq", "1.6 GPa",
      "tunnel hosted in layer-4 weak zone; interface stiffness unified"],
     ["PFC emod / kratio", "9.65 GPa / 1.0", "linear deformability"],
     ["pb_emod / kratio", "5.88 GPa / 0.6", "parallel-bond deformability"],
     ["pb_ten / pb_coh / pb_fa", "2.10 MPa / 23.0 MPa / 25 deg",
      "calibrated bond strength (D7)"],
     ["Balls / bonds", "456,163 / ~2.23M", "horseshoe, no invert, feet anchored"],
     ["Drive scale factor f", "0.25",
      "keeps lining in crack-development regime (trend-level)"],
     ["Initial state", "zero-gravity in-place recast (G4)",
      "stress-free ring, self-weight only"]])

# ---- Table 5-4 stage schedule ----
PH = {"dry1": "dry (initial)", "rise": "rising", "wet": "wet (peak)",
      "fall": "falling", "dry2": "dry (final)"}
rows4 = []
for k in range(1, 12):
    rows4.append([f"s{k}", TS.WATER[k-1], PH[TS.PHASE[k-1]],
                  "30" if TS.PHASE[k-1] in ("dry1", "wet", "dry2") else "5"])
render_table("表5-4_水位循環階段時程",
    "Table 5-4  11-stage water-level cycle schedule",
    ["Stage", "Water table", "Phase", "Duration (d)"], rows4)

# ---- Table 5-5 damage statistics ----
Q = json.loads((HERE.parent / "result" / "quant_summary.json").read_text())
rows5 = []
for k in range(1, 12):
    rows5.append([f"s{k}", TS.WATER[k-1], f"{Q['dN'][str(k)]:,}",
                  f"{Q['rate_per_day'][str(k)]:,.0f}",
                  f"{Q['N_cum'][str(k)]:,}"])
rows5.append(["Indices", "A_wet = 1.48", "A_frz = 0.085",
              f"D_total = {Q['D_total_pct']:.2f}%", "s1 = service baseline"])
render_table("表5-5_襯砌損傷統計",
    "Table 5-5  Stage-by-stage lining damage statistics (bond breaks)",
    ["Stage", "Water", "Delta N", "Rate (/day)", "Cumulative N"], rows5)
