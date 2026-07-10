# 04_InitialBalance — 三尺度初始力平衡 ✅（大/小 07-02 重建版；耦合 06-27 v5）

**root 介面**：`parameter.f3dat`（全案統一參數，改參數只改這裡）＋本 README＋PFC_CALIBRATION.md。

**★ 產出 sav 一律在 `output/`（2026-07-04 整理定版）**：
- `output/Large_Initial.f3sav`（07-02，260529 法：W-110 流體穩態→fluid off→K0 0.7→solve elastic→datum 歸零）
- `output/Small_Initial.f3sav`（07-02，兩段式：null 襯砌→IDW→W-110+洞周洩水→裸岩鬆弛→69,828 殼→1e-5）
- `output/Couple_Initial.f3sav`（=v6 free2：球環安裝完成、自由內面，**岩仍凍結**＝重澆鏈的根基底本）
- `output/Couple_Initial_G3.f3sav`（STEP G v5，07-05：岩解凍成增量彈性傳遞介質、一致介面、無端平台）
- `output/Couple_Initial_G4.f3sav`（**STEP I v2，07-07：零重力原位重澆、E_eq=1.6GPa Wade 核准、無應力環——staged 正式起點**）
- `output/Couple_Initial_v6_confined.f3sav`（圍束態深備援）
- 已刪：v5 舊 initial、free、v6 中間檢查點、**G(v4 退火版，被 G3 取代)**（皆可由 process/couple_solve 生產鏈重生）
- 生產鏈與三天試錯史：`process/couple_solve/README.md` 與其 `_trial_history_0704_0707/`

## 結構
- `process/`：large_init / small_init（現行版腳本+log）、idw_map.f3dat（IDW 映射 FISH）、export_large_stress.f3dat、render/plot QA 工具、`couple_solve/`（v5 全套+驗證）、`_superseded/`（06-22/23 無流體舊版，勿用）
- `output/`：流體檢查點（*_fld）、大模近場應力匯出（large_stress_for_small/coarse.dat＝小模與耦合模 IDW 源）、`qa/` 驗證圖

## ⚠ 待辦（Phase C 前必做）
（已完成 07-04：output/Couple_Initial.f3sav=free2。歷程與 gate 全記錄見 05/RUN_STATUS.md。）

## 重跑
cwd = 04 root：`flac3d600_console process\large_init.f3dat`（★ 存檔落在 root）。小模流體相會撞 20000 cycle 上限（pp≈初始靜水壓＝準穩態假設，已知非 bug）。

## 坑
- 初始平衡一律 `model solve elastic`（Wade 鐵則）。
- `zone water density` 漏設會讓 pp 全 0、門檻機制靜默失效。
- v5 耦合解必須 servo 漸進洩壓（一次性釋放→wall-zone facet 退化 solveForX 崩潰，8 次失敗教訓）。
