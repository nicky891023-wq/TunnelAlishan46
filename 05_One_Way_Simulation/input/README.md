# 00_geometry_water — 水位面幾何庫（純 input）

12 支 W-NN.stl 地下水位面（W-00 最高，每 10m 遞減至 W-110），byte 級複製自 260529 驗證過的原檔（`ClassPhD\test\TX\260529\02_small_model\geometry\`）。
05 內以 `geometry import 'input/W-XX.stl'`、04 以 `'../05_One_Way_Simulation/input/W-XX.stl'` + `zone water set 'W-XX'` 引用——**檔案位置與檔名不可動**。

- 現行使用：W-110（初始平衡+乾態）、W-90/70/50/30/10（05 的 11 階段升退水）。
- W-00/20/40/60/80/100 未被任何腳本引用（保留備用）。
- 平面外延覆蓋整個大模 footprint；W-NN = W-00 垂直下移 NN 公尺（已驗證位元一致）。
