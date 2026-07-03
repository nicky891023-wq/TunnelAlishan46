# 03_CoupleModel — 耦合模（襯砌尺度）建模 ✅ 完成凍結（2026-06-24）

**交付物**：`output/Couple_Model.f3sav`（424,908 hex 圍岩 O-grid + 456,302 PFC 球襯砌 + wz_outter 耦合牆 + 3 剛性牆，未解算）。
下游：04/process/couple_solve/couple_servo_v5.f3dat restore `../../../03_CoupleModel/output/Couple_Model`。

## 結構
- `input/`：wallzone_outter.stl（**首要鐵則幾何**＝襯砌外牆＝圍岩開挖面，開放馬蹄拱、底緣 z≈1744.85 平底）、wall_inner.stl（淨空）、wall_860/910.stl（端蓋）、tunnel_860_910_closed.stl（佈球包絡）
- `process/`：build_couple_hex.py（mb3 結構化 hex，--solid/--clearance 兩個變體 inp 已產出備用）、build_Couple_mb3.f3dat（組裝：import+wall-zone+剛性牆+佈球）、build_wall_ball.f3dat、verify_couple_render.f3dat、README_build_notes_0624.md（原建模筆記）
- `output/`：Couple_Model.f3sav；`output/qc/` 驗收渲染圖 10 張（bore貼STL 0.000m、球貼牆≤0.004m…）

## 坑（血淚）
- 圍岩內環必須逐斷面切原始 STL 精確落點（不平滑重採樣），wall-zone 才無縫。
- `ball distribute box` 要涵蓋整條彎曲隧道 bbox。
- 球內縮要對真實牆（wallzone_outter+wall_inner）做 geometry-distance gap 刪球。
- 已刪：WallBall_Only.f3sav（驗證用，可由 build_wall_ball.f3dat 重生）、tunnel_full_closed_SOURCE.stl（未使用）。
