# 01_LargeModel — 大模（坡地尺度）建模 ✅ 完成凍結（2026-06-22）

**交付物**：`output/Large_Model.f3sav`（511,988 tet、4 地質層共形、無隧道、elastic 佔位無參數/BC）。
下游：04/process/large_init.f3dat 以 `../01_LargeModel/output/Large_Model` restore。

## 結構
- `input/`：DEM.stl、F01(崩積層封閉體，取底片)、F02(Ssh頂)、F03(bedrock-up)、geo_surfaces_v2.npz(交叉檢核基準)
- `process/`：gen_large_geo.py(裁剪地質場+fragment面+尺寸場) → build_large_tet.py(gmsh OCC→large_tet.inp) → Large_Model.f3dat(FLAC import+分群+skin) ＋各中間檔/log
- `output/`：Large_Model.f3sav

## 重跑（一般不需要）
cwd = `process/`，依序跑三支腳本（python×2 → flac3d console×1）。路徑已改為 ../input/ 與 ../output/（2026-07-03 重整）。

## 坑
- F01 是封閉體，取樣要用 bottom sheet（geo_sampler sheet='bottom'）。
- 層標記用 band-median hybrid 修 jitter；export box 內網格 ≤~20m（p95 20.6 已接受）。
- geo_sampler.py 是 qc_geo_v2 改名複本，standalone main() 不能跑（只 import Surf class）。
