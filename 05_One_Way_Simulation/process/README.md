> **⚠ 2026-07-12 更新**：本 README 之「LIVE 主控」段落成文於 07-07，現況以
> `../RUN_STATUS.md` 頂部 v6 里程碑為準——staged 主控＝`couple_staged_v6.f3dat`
> （隨縱坡錨定帶＋接縫平移驅動）；s1 重跑鏈＝`gen_s1_reruns.py`＋`large/small_s1_rerun.f3dat`
> （T=1.0，診斷=diag_T1_sweep）；傳遞鏈＝`couple_export_bnd_v4.f3dat`＋`exp_body.f3dat`
> ＋`cpl_export_s01.f3dat`。v2 相關檔為 07-08 跑通戰史佐證，僅供追溯。

# 05/process — 檔案地圖（2026-07-07 盤點）

## LIVE（staged 主鏈，勿動）
- `couple_staged_v2.f3dat`：11 階段主控（restore 04/output 的耦合初始態；DRIVE_SCALE 折減；
  calm 節奏 solve；每階段 7 種輸出＋cs_01/06/11 檢查點）
- `fracture_track_v3.fis`：裂縫 DFN 追蹤（無 fragment 操作版——v2 會卡死大模型）
- `couple_qa_v2.fis`：七個 QA 輸出函式
- `cpl_resid_s01-11.txt`：**驅動檔**（小模→Kabsch 剛體扣除→殘差）
- `cpl_wall_s01-11.txt`：G2 gate 參考（小模洞壁位移）；`cpl_bnd_s01-11.txt`：邊界帶原始匯出

## 傳遞鏈（重演用）
`couple_export_bnd_v4.f3dat`＋`exp_body.f3dat`（restore 會清 FISH→逐階段重載定義的成熟模式）
→ `make_cpl_resid.py`（Kabsch＋應變一致性 gate ~1e-19）

## 上游完成跑（產物在 ../output）
`large_staged.f3dat`、`small_staged_v2.f3dat`（各自 +log；11 階段皆完成且驗收過）

## 診斷證據庫（⚠ 各自附 README，勿當成果）
- `_diag_frozenrock_0704/`：凍結岩箱事故（staged 首跑無效的證據）
- `_diag_prestress_harvest_0707/`：鎖入力網預拉尾收割（f=0.25/0.05 兩跑證據＝STEP I 重澆的依據）
