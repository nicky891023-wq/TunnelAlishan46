# 交接 RUNBOOK（CURRENT，2026-07-12 Fable 末次更新）— 接手者唯一入口

> **授權範圍（Wade 裁示，恆常有效）**：接手者**只監控回報，決策全給 Wade**。
> 照著寫好的步驟做＝執行，不是決策。任何偏離（判準亮紅、腳本報錯、數字違反預期）
> ＝停下、整理現況、回報 Wade 裁決。不即興修腳本、不即興調參數。

## 現況一覽（2026-07-12）

**v6 重跑（兩問題修正版）已全部完成、下游全部更新完畢。**無運轉中之 FLAC 作業。

- 問題1（s1 門檻過廣）：大/小模 s1 以 T=1.0 重跑完成（大模活化 117,621→3,315；小模 422,854→24,935）；
  s2-11 驅動檔以接縫平移法保留增量（原檔備份於 05/process/_backup_T08run/）
- 問題2（拱腳錨定）：耦合模 v6 以隨縱坡錨定帶（z≤rim(y)+0.41，rim=1743.97+0.0372(y-860)）
  ＋6階退火重跑 11 階段完成（couple_staged_v6.f3dat / .log），CONTROL-0=28 裂縫（同 v5 基準）
- 圖5-19 之 y860-895 三角形假象已消失（驗收通過）

**v6 各階段 CS-CHK（累計/增量）**：
CONTROL-0 28 / — ｜ s1 2,751 / +2,723 ｜ s2 5,772 / +3,021 ｜ s3 11,070 / +5,298 ｜
s4 17,838 / +6,768 ｜ s5 20,391 / +2,553 ｜ **s6 34,961 / +14,570（雨峰）** ｜
s7 36,470 / +1,509 ｜ s8 37,023 / +553 ｜ s9 37,503 / +480 ｜ s10 37,892 / +389 ｜ s11 37,980 / +88

**新關鍵數字（quant_summary.json 已重建）**：A_wet=0.551、A_frz=0.148、總損傷密度 1.83%
（水循環分量 1.70%）、裂縫 環199/斜19/縱3 m、左肩推力峰 1,029 kN/m（s6≈s11、s1 約 260）、
兩腰內擠均值 0.15 mm、外壓峰值 946 kPa、小模斷面(y885)活化 172/837/4,919/154/35。

## 已完成的下游更新（07-12）

1. 全部 dump 重匯：cs_s1-11 cracks/cwall/pmap（v6 內建）＋ cp_cforce/cp_balldisp s01/06/11
   ＋ pf_s01/06/11 ＋ lg/sm s01 場量與射線（s01_refresh.f3dat，新腳本）
   ⚠️ 教訓：FLAC 由上層 caller 啟動時 FISH file.open 以啟動 cwd 解析——dump 會寫到上層；
   正確作法＝cd 到 process/ 傳裸檔名（export_pf_3ckpt 頭註之原始模式）
2. 全部圖表重建：圖5-08/5-12/5-14/5-15/5-16/5-17/5-18/5-19＋表5-1~5-5（在 00_Document/result/）
   - 圖5-14 修正 blocker：門檻線 λ=0.6→0.8＋s1 T=1.0 說明（plot_sm_rays.py）
   - 圖5-19 錨定帶陰影改隨縱坡等寬帶（plot_cp_cracks.py，舊常數 1745.30 公式已移除）
   - 圖5-18 註記/圖例重疊、負值標籤脫節已修（plot_cp_deform.py）
3. 論文全文：**260711_TX碩論_Wade.docx**（00_Document/，Wade 核可之新摘要＋新第一章架構＋
   全部新數字；驗證 7 標記齊、零舊數殘留；產線 assemble→transplant_math→finalize 冪等）

## 等 Wade 裁決的事項（勿自行決定）

1. **A_wet 定義**：式(5-1)原定義下新值=0.55（雨峰日速率<升水短脈衝平均）。現行文稿保留原式、
   詮釋段改為事實敘述＋濕乾對比（644 vs 2.9 條/日，>200 倍）。是否改定義（如濕/乾季均速率比）由 Wade 定。
2. GitHub push（等 Wade 說 push 再 push）
3. f 靈敏度補充跑、06 雙向耦合開工

## 背景知識（需要時查）

- 一頁現況＋完整戰史：`05/RUN_STATUS.md`；狀態鏈：`04/process/couple_solve/README.md`
- 三個定案認知（勿重新質疑）：①介面勁度=zone E＋calm 節奏 ②斷鍵=微損傷、f=0.25=縮尺趨勢
  ③E_eq=1.6GPa、T=0.8（s2-11）＋T=1.0（s1 初始基準，07-11 定案）
- 鐵則：單 console／cd 到 process 傳裸檔名／65s 授權間隔／以腳本自身 log 驗證／restore 清 FISH／
  勿 blanket kill flac／電源永不睡眠
- 現役產線：圖表=05/process 各 render/plot 腳本＋tunnel_frame（勿改 thesis_style/tunnel_frame/
  f3grid_io/crack_classify）；論文=00_Document 三步產線；規劃=THESIS_PLAN/WRITING_BRIEF/FIGURE_STATUS
