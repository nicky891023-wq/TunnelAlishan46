#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_hydro_schedule.py -- 簡報用 11 階段水文排程圖（07-12，比照 result/ 論文圖風格）。
Out: 00_Document/method_report_assets/hydro_schedule.png（覆蓋舊 CJK-sans 版）
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS

TS.apply()
HERE = Path(__file__).parent
OUT = HERE.parent.parent / "00_Document" / "method_report_assets" / "hydro_schedule.png"

DAYS = [30, 5, 5, 5, 5, 30, 5, 5, 5, 5, 30]
LEVEL = [-110, -90, -70, -50, -30, -10, -30, -50, -70, -90, -110]
PHASE = ["dry1", "rise", "rise", "rise", "rise", "wet", "fall", "fall", "fall", "fall", "dry2"]
PHASE_C = {"dry1": "0.62", "rise": "#4a7fb5", "wet": "#c0392b", "fall": "#7fb3d5", "dry2": "0.62"}

t0 = np.cumsum([0] + DAYS)
fig, ax = plt.subplots(figsize=(19, 7))
for k in range(11):
    ax.fill_between([t0[k], t0[k + 1]], LEVEL[k], -120,
                    color=PHASE_C[PHASE[k]], alpha=0.28, lw=0)
    ax.plot([t0[k], t0[k + 1]], [LEVEL[k]] * 2, color="#0b5394", lw=3.4)
    if k < 10:
        ax.plot([t0[k + 1]] * 2, [LEVEL[k], LEVEL[k + 1]], color="#0b5394", lw=3.4)
    xc = (t0[k] + t0[k + 1]) / 2
    ax.annotate(f"s{k+1}", xy=(xc, -131), ha="center", va="bottom",
                fontsize=19, color="0.25")
    if DAYS[k] == 30:                                   # wide stages: W label in-band
        ax.annotate(f"W{LEVEL[k]}", xy=(xc, -116), ha="center", fontsize=19,
                    color="0.35")
    ax.annotate(f"{DAYS[k]} d", xy=(xc, LEVEL[k] + 2.5), ha="center", fontsize=17,
                color="#0b5394")
ax.annotate("wet peak (30 d)", xy=(t0[5] + 15, -10), xytext=(t0[5] + 15, 2),
            ha="center", fontsize=21, color="#7a1d12")
ax.set_xlabel("Creep time (days)")
ax.set_ylabel("Water table (m, relative to W-00)")
ax.set_xlim(0, 130); ax.set_ylim(-134, 8)
ax.set_title("11-stage water-level cycle: dry(30 d) - rise(4x5 d) - wet(30 d) - "
             "fall(4x5 d) - dry(30 d);  s1 threshold T=1.0 (baseline), s2-s11 T=0.8")
fig.savefig(OUT, dpi=190, bbox_inches="tight")
print("saved", OUT)
