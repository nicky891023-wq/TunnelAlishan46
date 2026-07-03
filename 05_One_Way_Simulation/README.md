# 05_One_Way_Simulation — 單向三尺度 staged 模擬（進行中）

**現況/進度/決策/坑 → 一律看 `RUN_STATUS.md`（live 文件）。方法定案 → `docs/COUPLING_METHOD_PROPOSAL.md`（D1–D7）。**

## 結構（07-03 定版）
- `process/`：兩支 staged 腳本+log、驅動場 txt（lg_disp_s* 全場/lg_disp_resid_s* 殘差）、make_resid.py、繪圖工具。重跑 cwd=05 root：`flac3d600_console processarge_staged.f3dat`（存檔自動落 output/）。
- `output/`：lgs_01-11（大模階段）、ss_01-11（小模階段）
- `result/`：成果圖

## 舊說明（路徑已改，內容仍有效）
- Phase A 大模：`large_staged.f3dat`（11 階段 W-110↔W-10，累積時鐘已修）→ `lgs_01–11.f3sav` + `lg_disp_s01–11.txt` → `make_resid.py`（Kabsch 扣剛體+應變 gate）→ `lg_disp_resid_s01–11.txt`
- Phase B 小模：`small_staged_v2.f3dat`（T=0.8、殘差驅動、每 1.25 天段界 shell cap、kinematic abort）→ `ss_01–11.f3sav` + log 內 SSv2-HIST 歷時線
- 繪圖工具：plot_convhist*.py、plot_slice.py、render_slice*.f3dat
- `result/`：成果圖輸出區（歷時曲線、門檻範圍、開裂殼分布…）
- `docs/`：COUPLING_METHOD_PROPOSAL.md（方法架構定案）、MAGNITUDE_DIAGNOSIS.md（量級誠實診斷）、REF_260529_workflow.md（260529 方法基準）

## `_archive/`＝隔離區（⚠ 內含錯誤過程，勿沿用，見其 README）
