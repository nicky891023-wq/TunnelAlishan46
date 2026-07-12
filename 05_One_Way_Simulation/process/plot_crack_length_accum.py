#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
plot_crack_length_accum.py -- TT 版 圖5-21：襯砌裂縫長度累積（獨立圖，07-12 合稿）。
內容＝圖5-19 面板(c) 之獨立放大版：三類裂縫長度 vs 階段＋階梯水位副軸。
Out: result/圖5-21_襯砌裂縫長度累積.png（供 260712 換圖）
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import thesis_style as TS
import crack_classify as cc
from plot_cp_cracks import build_lines   # reuse the proven trace builder

TS.apply()
HERE = Path(__file__).parent
OUT = TS.RESULT

ks = list(range(1, 12))
EV = {0: [], 1: [], 2: []}
for k in ks:
    Pk, _ = cc.load_breaks(k)
    Pk = Pk[(Pk[:, 1] > 862.0) & (Pk[:, 1] < 908.0)]
    if len(Pk) < 10:
        for t in (0, 1, 2):
            EV[t].append(0.0)
        continue
    typk, THk, Rk = cc.classify_breaks(Pk)
    _, totk = build_lines(Pk, typk, THk, Rk)
    for t in (0, 1, 2):
        EV[t].append(totk[t])

fig, ax = plt.subplots(figsize=(16, 9))
for t, nm in ((0, "circumferential"), (1, "oblique"), (2, "longitudinal")):
    ax.plot(ks, EV[t], "-o", color=cc.TYPE_COL[t], lw=3.4, ms=10, label=nm)
ax.axvspan(5.5, 6.5, color="#c0392b", alpha=0.10)
ax.text(6, max(EV[0]) * 0.94, "wet", ha="center", fontsize=20, color="#7a1d12")
axb = ax.twinx()
wx_, wy_ = TS.water_steps()
axb.plot(wx_, wy_, "b--", lw=2.2, alpha=0.65)
axb.set_ylabel("Water level (m)", color="b")
axb.tick_params(axis="y", colors="b"); axb.grid(False)
ax.set_xticks(ks)
ax.set_xticklabels([f"{k}\n{TS.WATER[k-1]}" for k in ks], fontsize=19)
ax.set_xlabel("Stage (water level)")
ax.set_ylabel("Total crack trace length (m)")
ax.set_title("Cumulative crack trace length by class (s1 baseline excluded; "
             "2 m end bands trimmed; f = 0.25 trend)")
ax.text(0.985, 0.03, "traces re-classified independently per stage;\n"
        "class totals may fluctuate slightly as traces grow",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=14,
        color="0.4", style="italic", bbox=dict(fc="white", alpha=0.8, lw=0, pad=1.5))
ax.legend(fontsize=20, loc="center left")
fig.savefig(OUT / "圖5-21_襯砌裂縫長度累積.png", dpi=180, bbox_inches="tight")
print("saved 圖5-21")
