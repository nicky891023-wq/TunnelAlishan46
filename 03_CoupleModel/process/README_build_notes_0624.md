# 03_CoupleModel — 阿里山 #46 耦合模（結構化 hex 圍岩 + PFC 襯砌）

斷面域 40×40（隧道中心 ±20m）× y[860,910]，圍岩結構化全 hex（mb3 法）+ wall-zone 耦合球↔圍岩 + 剛性端牆 + PFC 襯砌球。**建模階段，未解算**（解算在 04_InitialBalance）。

## 輸入（Wade 的襯砌幾何 STL，首要鐵則）
- `wallzone_outter.stl` — 襯砌**外牆**＝圍岩開挖面（驅動圍岩 zone、wall-zone、ball 外緣）。**是開放馬蹄拱，底部平底 z≈1744.85**。
- `wall_inner.stl` — 內側淨空（剛性牆）。
- `wall_860.stl` / `wall_910.stl` — 兩端洞口端牆（剛性牆）。
- `tunnel_860_910_closed.stl` — 封閉襯砌環，球填充範圍。
- `tunnel_full_closed_SOURCE.stl` — 完整隧道閉合面（早期來源，**未被本管線使用**，僅保留備查；確認別處有備份即可刪）。

## 過程（建模順序）
1. **`build_couple_hex.py`** → `couple_hex.inp`：結構化全 hex 圍岩（**424,908 hex**、layer2-6）。內環 **116 節點**按原始 `wallzone_outter.stl` 弧長取樣（節點到 STL 0.00000m、零扭曲）；外圍徑向 24 圈漸變加密；cell 平衡周向/y/徑向 → **aspect median 1.84 / p99 3.31 / max 3.75**（近立方）。
2. **`build_Couple_mb3.f3dat`** → `Couple_Model.f3sav`：FLAC 組裝＝import `couple_hex.inp` + `wall-zone create wz_outter`（包圍岩隧道壁、含兩洞口、排除 XZ 端蓋）+ 剛性牆 + 球填 `tunnel_860_910_closed` 後對**真實牆(wallzone_outter+wall_inner) gap 0.040 內縮**（球緊貼牆、max 凸 ≤0.004m、0 外漏，**456,302 顆**）。**最終交付，不解算**。
3. **`build_wall_ball.f3dat`** → `WallBall_Only.f3sav`：純牆+球（無 zone）驗證 STL 幾何用。
4. **`verify_couple_render.f3dat`**：restore Couple_Model 匯出球+牆座標供獨立渲染驗證。

## 輸出
- **`Couple_Model.f3sav`** — 最終耦合模（圍岩+wall-zone+牆+球，未解算）。
- `WallBall_Only.f3sav` — 牆+球幾何驗證檔。

## 驗證渲染（已逐一睜眼確認）
- `couple_bore_vs_stl.png` — 圍岩內環精準疊合原始 wallzone_outter.stl（0.00000m）。
- `nogap_check.png` — wz_outter 耦合面＝STL、無縫。
- `final_check.png` — 兩洞口外圈封閉 + 外圍徑向密度。
- `couple_outer_density.png` — 外圍 24 圈加密。
- `couple_cubic_cells.png` — cell 近立方（aspect 分布）。
- `ball_touch_final.png` — 球緊貼內外牆、微凸 ≤0.004m。
- `couple_hex_notwist_long.png` — 零扭曲（縱向）。
