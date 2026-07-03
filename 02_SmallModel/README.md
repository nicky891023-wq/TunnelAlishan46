# 02_SmallModel — 小模（隧道尺度）建模 ✅ 完成凍結（2026-06-23，Route C 共形版）

**交付物**：`output/Small_Model.f3sav`（1,433,466 tet、6 地質層+0.4m 實體襯砌環共形、內淨空挖空、elastic 佔位）。
下游：04/process/small_init.f3dat restore `../02_SmallModel/output/Small_Model`（該流程會先 null 襯砌 zone → 裸岩鬆弛 → 裝 structure shell）。

## 結構
- `input/`：S01–S05.stl（地質面）、tunnel_inner/outter.stl、centerline_model.csv（93 點中心線）
- `process/`：build_small_conformal.py(gmsh OCC 共形) → small_conformal.inp → Small_Conformal.f3dat(import+分群+skin)；verify_*.py（QC）
- `process/_superseded_routeB/`：⚠ 已棄用建法（attach 產生 zero-stiffness gp），勿參考，見其 README
- `output/`：Small_Model.f3sav、lining_xsection.png（襯砌環 QC 圖）

## 重跑（一般不需要）
cwd = `process/`：python build_small_conformal.py → flac console Small_Conformal.f3dat。

## 坑
- ⚠ 歷史同名陷阱：`_superseded_routeB/Small_Model.f3dat`（Route B 腳本）若誤跑會覆蓋共形版 f3sav——已隔離，勿移回。
- 隧道沿 y 斜貫多層（地層比隧道陡）是實際地質，網格「鋸齒」為真穿層非 bug。
