#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_damage_map.py -- 耦合模裂縫/鍵結普查 → 襯砌損傷圖 D(θ,y)（06 介面規格）
輸入：耦合階段的 cracks dump（x y z type ...）＋鍵結總數普查（或用 05 的
     crack_sectors/pmap 輸出重分箱）
輸出：dmg_map_sNN_iK.txt：theta_lo theta_hi y_lo y_hi D n_broken n_bond
分箱：θ 24×15°（中心 1297,1747.5）；y 5 帶×10m（860-910）
夾限：D ∈ [0, 0.9]；拱腳帶（z<=1745.30，不可斷）恆 D=0
⚠ 可先離線對 05 成果試算（METHOD §7 checklist 項目），不用等 06 開工。
"""
import sys
import numpy as np

CX, CZ = 1297.0, 1747.5
TH_BINS = np.arange(0, 361, 15)
Y_BINS  = np.arange(860, 911, 10)
D_CAP   = 0.9

def main(cracks_txt, nbond_sector_txt, out_txt):
    d = np.loadtxt(cracks_txt, skiprows=1)
    x, y, z = d[:, 0], d[:, 1], d[:, 2]
    th = np.degrees(np.arctan2(z - CZ, x - CX)) % 360
    feet = z <= 1745.30                       # 不可斷帶，排除
    nb = np.loadtxt(nbond_sector_txt)         # 同分箱的可斷鍵總數（耦合模一次性普查）
    rows = []
    for i in range(len(TH_BINS) - 1):
        for j in range(len(Y_BINS) - 1):
            m = (~feet & (th >= TH_BINS[i]) & (th < TH_BINS[i+1]) &
                 (y >= Y_BINS[j]) & (y < Y_BINS[j+1]))
            n_broken = int(m.sum())
            n_bond = int(nb[i, j]) if nb.ndim == 2 else 1
            D = min(D_CAP, n_broken / max(n_bond, 1))
            rows.append((TH_BINS[i], TH_BINS[i+1], Y_BINS[j], Y_BINS[j+1],
                         D, n_broken, n_bond))
    with open(out_txt, "w") as f:
        f.write("theta_lo theta_hi y_lo y_hi D n_broken n_bond\n")
        for r in rows:
            f.write(f"{r[0]} {r[1]} {r[2]} {r[3]} {r[4]:.4f} {r[5]} {r[6]}\n")
    print(f"DMGMAP {out_txt} sectors={len(rows)} "
          f"Dmax={max(r[4] for r in rows):.3f}")

if __name__ == "__main__":
    main(*sys.argv[1:4])
