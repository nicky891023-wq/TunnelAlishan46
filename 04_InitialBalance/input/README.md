# 04 的輸入不在本資料夾——直接取自上游 stage 的 output（勿複製、以固定路徑引用）

| 輸入 | 位置 | 用於 |
|---|---|---|
| 大模網格 | `../01_LargeModel/output/Large_Model.f3sav` | process/large_init.f3dat |
| 小模網格 | `../02_SmallModel/output/Small_Model.f3sav` | process/small_init.f3dat |
| 隧道淨空面 | `../02_SmallModel/input/tunnel_inner.stl` | small_init（洞周洩水區選取） |
| 耦合模 | `../03_CoupleModel/output/Couple_Model.f3sav` | process/couple_solve/couple_servo_v6.f3dat |
| 水位面 | `../05_One_Way_Simulation/input/W-110.stl`（2026-07-03 起，原 00_geometry_water） | 兩支 *_init 的流體相 |
| 材料參數 | `../parameter.f3dat`（04 root，全案唯一參數源） | 全部 |
