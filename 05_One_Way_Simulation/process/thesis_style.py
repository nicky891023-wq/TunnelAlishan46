#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
thesis_style.py -- journal-grade figure conventions for thesis Ch.5, benchmarked against
IJRMMS_CHFT.docx figures (07-10 visual audit):
  * Times New Roman serif everywhere, math italic symbols (mathtext stix)
  * curves: white bg, light-gray grid, thick saturated lines, boxed legend w/ symbols,
    dual axes when relating quantities, shaded band for derived ranges
  * field/state maps: VISIBLE MESH, discrete state colors (viscoelastic blue / viscoplastic
    red / elastic pale-yellow), top legend with color swatches + bold text, stage panels
    left->right with arrows
Figures saved to 00_Document/result with thesis numbering (圖5-xx_...).
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULT = Path(r"C:\Users\Wade\Desktop\Tunnel_TX\00_Document\result")
RESULT.mkdir(exist_ok=True)

def apply(scale=1.0):
    matplotlib.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 26 * scale,
        "axes.titlesize": 28 * scale,
        "axes.labelsize": 28 * scale,
        "xtick.labelsize": 23 * scale,
        "ytick.labelsize": 23 * scale,
        "legend.fontsize": 22 * scale,
        "figure.titlesize": 30 * scale,
        "axes.linewidth": 1.5,
        "lines.linewidth": 3.0,
        "lines.markersize": 9,
        "grid.color": "0.85",
        "grid.linewidth": 0.8,
        "axes.grid": True,
        "axes.axisbelow": True,
        "legend.framealpha": 1.0,
        "legend.edgecolor": "0.2",
        "savefig.bbox": "tight",
        "savefig.dpi": 300,
    })

# IJRMMS-style discrete state colors (image20 benchmark)
C_ELASTIC   = "#f5f0a0"   # pale yellow  : elastic / inactive
C_VISCO     = "#29abe2"   # blue         : viscoelastic (threshold ON, no failure)
C_PLASTIC   = "#e0231c"   # red          : viscoplastic / plastic (yield)
C_WATER     = "#2166ac"   # water table line
C_MESHLINE  = "0.55"      # mesh edge gray

# stage tags (11-stage water cycle, D5)
WATER = ["W-110","W-90","W-70","W-50","W-30","W-10","W-30","W-50","W-70","W-90","W-110"]
PHASE = ["dry1","rise","rise","rise","rise","wet","fall","fall","fall","fall","dry2"]
LEVEL = [-110,-90,-70,-50,-30,-10,-30,-50,-70,-90,-110]

def water_steps():
    """staircase water-level line (level HELD constant within each stage, jump between):
    returns xs, ys for plot() on a stage-index axis (Wade review 07-10: 水位線應為階梯狀)."""
    import numpy as np
    xs, ys = [], []
    for k in range(1, 12):
        xs += [k - 0.5, k + 0.5]
        ys += [LEVEL[k - 1], LEVEL[k - 1]]
    return np.array(xs), np.array(ys)

def stage_label(k, zh=False):
    if zh:
        ph = {"dry1":"乾季(初)","rise":"升水","wet":"雨季(峰)","fall":"退水","dry2":"乾季(末)"}[PHASE[k-1]]
        return f"s{k} {WATER[k-1]} {ph}"
    return f"Stage {k}  {WATER[k-1]} ({PHASE[k-1]})"
