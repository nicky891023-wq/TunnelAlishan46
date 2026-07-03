# 04_InitialBalance — 三尺度初始力平衡 ✅（大/小 07-02 重建版；耦合 06-27 v5）

**root 介面（下游以固定路徑引用，不可搬動）**：
- `parameter.f3dat` — 全案統一參數（材料/creep/門檻 T=0.8/襯砌/PFC 微觀）。**改參數只改這裡**。
- `Large_Initial.f3sav`（07-02，260529 法：W-110 流體穩態→fluid off→K0 0.7→solve elastic→datum 歸零）
- `Small_Initial.f3sav`（07-02，兩段式：null 襯砌→IDW 承接大模場→W-110+洞周洩水→裸岩 MC 鬆弛 1e-4→裝 69,828 片 dkt-csth 殼→1e-5；datum 歸零）
- `Couple_Initial.f3sav`（06-27 servo v5：選擇性鍵結+力自由安裝+servo 孔壁洩壓；**注意：承接的是 06-22 舊大模場**）

## 結構
- `process/`：large_init / small_init（現行版腳本+log）、idw_map.f3dat（IDW 映射 FISH）、export_large_stress.f3dat、render/plot QA 工具、`couple_solve/`（v5 全套+驗證）、`_superseded/`（06-22/23 無流體舊版，勿用）
- `output/`：流體檢查點（*_fld）、大模近場應力匯出（large_stress_for_small/coarse.dat＝小模與耦合模 IDW 源）、`qa/` 驗證圖

## ⚠ 待辦（Phase C 前必做）
Couple_Initial 與 07-02 新大模場**不一致**——耦合 initial 需以新場+單一等效彈性圍岩重做（並執行刪內牆+拱角鍵結設計），見 05/RUN_STATUS.md 與 05/docs/COUPLING_METHOD_PROPOSAL.md。

## 重跑
cwd = 04 root：`flac3d600_console process\large_init.f3dat`（★ 存檔落在 root）。小模流體相會撞 20000 cycle 上限（pp≈初始靜水壓＝準穩態假設，已知非 bug）。

## 坑
- 初始平衡一律 `model solve elastic`（Wade 鐵則）。
- `zone water density` 漏設會讓 pp 全 0、門檻機制靜默失效。
- v5 耦合解必須 servo 漸進洩壓（一次性釋放→wall-zone facet 退化 solveForX 崩潰，8 次失敗教訓）。
