# couple_solve — 耦合模初始態生產鏈（2026-07-07 盤點定版）

## 生產鏈（依序，全部可重演）
1. `couple_servo_v6.f3dat`（+log）：從 03 網格建球環——選擇性鍵結、力自由安裝（lin_mode 1）、
   servo 孔壁洩壓、拱腳帶 1e20、STEP F 刪內牆 → `output/Couple_Initial.f3sav`（=free2，岩仍凍結）
   （v5 為前代配方，留檔對照）
2. `couple_stepG_freerock.f3dat`（+couple_stepG.log）＝**STEP G v5**：岩箱解凍成增量彈性傳遞介質
   （apply 清除、應力歸零、density 1、**介面勁度一致化 bf emod=E_eq**、迷你退火 100×→1×、刪端平台、
   calm 節奏 settle）→ `output/Couple_Initial_G3.f3sav`（斷鍵僅 91）
3. `couple_stepI_recast0g.f3dat`（+couple_stepI.log）＝**STEP I v2**：零重力原位重澆（0g → 全 unbond
   ＋lin_force 歸零＋岩應力歸零 → D7 全新鍵結、bf 膠合僅 bf_couple 組 → 0g 自診斷 → 重力五階爬回）
   → `output/Couple_Initial_G4.f3sav`＝**無應力原位澆築環（E_eq=1.6GPa Wade 核准、只揹自重）＝staged 正式起點**

## 為什麼需要 STEP I（一句話）
G3 的球-球力網揹著 servo 安裝鎖入力（力鏈預拉尾貼強度），任何附加變形都會「收割」出上萬條假裂縫
（證據：05/process/_diag_prestress_harvest_0707/）。重澆＝把環變成真正無應力的原位澆築體。

## 子資料夾
- `servo_install_qa/`：v5/v6 安裝期的幾何/鍵結/位移驗證圖與 dump（生產鏈品保紀錄）
- `_trial_history_0704_0707/`：**三天除錯史的全部試錯腳本/ログ/dump（⚠勿當成果、先讀其 README）**

## 材料/參數
全案唯一參數源 `04/parameter.f3dat`；D7 襯砌微觀參數見 `04/PFC_CALIBRATION.md`；
E_eq=1.6 GPa＝Wade 核准定案（隧道幾乎全在 l4=1.5GPa 弱層）；介面勁度必須=zone E（數值穩定鐵則）。
