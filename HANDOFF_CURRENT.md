# 交接 RUNBOOK（CURRENT，2026-07-14 Fable 末次更新）— 接手者唯一入口

> **授權範圍（Wade 裁示，恆常有效）**：接手者**只監控回報，決策全給 Wade**。
> 照著寫好的步驟做＝執行，不是決策。任何偏離（判準亮紅、腳本報錯、數字違反預期）
> ＝停下、整理現況、回報 Wade 裁決。不即興修腳本、不即興調參數。

## 🔴 進行中：06 雙向耦合 26-tick 鏈（2026-07-14 起跑）

Wade 指令：小模/耦合模雙向、每 5 天交替傳遞（小模圍岩變形→耦合模襯砌外力；
耦合模襯砌變形→小模圍岩反力=D→E 殼勁度折減）。大模不重跑（沿用 05 v6 驅動檔）。

**管線（全在 06/process，一律 cd 到該目錄操作）**：
- 總指揮 `run_t5.py`：`python run_t5.py status`（看進度）→ `smoke` → `stage0` →
  `ticks [N]`（斷點續跑：manifest=06/output/t5/manifest.json，committed tick 自動跳過）
- FLAC 腳本由 `build_06_scripts.py` 從 05 原始碼切片生成（cs06_stage0 / cs06_kernel /
  ss06_kernel / ss06_t1_init / exp06_body / track_reattach）；逐 tick 側檔由 run_t5 生成
- 資料工具：make_cpl_resid06（Kabsch，已驗證與 05 產線逐位一致）→
  make_damage_map_v2（24×5 格損傷圖：registry 分母/CONTROL-0 扣除/護帶/單調）→
  make_shellE（E=E0(1−D)，地板 2.5 GPa）
- **fail-closed**：任何 gate 亮紅→鏈自動停、manifest 記 failed_*→整理現況回報 Wade，
  不重跑不調參。裂縫單 tick 增量 ≥30,000（v6 shatter 規則）由 Wade 裁 DRIVE_SCALE
- 06 專屬鐵則：tick 腳本**不可**呼叫 track_init（會清累積裂縫 DFN；用 track_reattach）；
  **不可**在 tick 間重呼 apply_vel_idw / tag_driven（毀掉恆定邊界速度）；
  位移歸零只在 stage-0；存檔滾動保留（keep={t00,1,6,10,11,16,20,21,26}+最新2）
- ⚠️ log 判讀教訓（07-15）：FLAC 對 call 進來的檔案**逐行回顯定義**（"Def> io.out('SS06-ABORT…')"），
  對 log 做子字串搜尋會誤中定義文字（誤殺）或被定義文字誤放行（漏檢）。gate 一律用
  「行首錨定 / 帶數字」的 regex 比對**執行輸出**；另外耦合模單一 cycle 區塊靜默可達
  ~70 分鐘（1.35 s/cyc），staleness 看門狗已分級（stage0/耦合/小模=150/120/60 分）
- tick 內斷點續跑：小模或耦合任一段已有「自身 log marker＋存檔」即自動重用不重跑（maybe_done）
- 預估：每 tick ≈ 45–60 分（小模+耦合各一次 console，中間 65s 授權緩衝）→ 全鏈 20–26 h
- 里程碑回報點：t01（identity 對 05 s1 前 5 天）、t06（乾季末）、t11–t16（雨峰）、t26

## 現況一覽（2026-07-12 基線）

**v6 重跑（兩問題修正版）已全部完成、下游全部更新完畢。**

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

## 進行中（2026-07-12 下午，Wade 四項指令依序執行）

1. ✅ A_wet 改定義（Wade 核定）：A_wet=r_wet(s2-6)/r_dry1(s1)=7.0、A_frz=r_dry2(s11)/r_wet=0.0046；
   圖5-15/FIG_A/quant_summary/論文（260711 同檔）已全部更新
2. ✅ 清理＋說明檔＋GitHub push（commit 06077ab；刪 couple_staged_v3-v5 等失敗變體；
   RUN_STATUS/FIGURE_STATUS/WRITING_BRIEF/HANDOFF 均更至 v6 里程碑）
3. ✅ **Ch5 深度審閱完成**：Codex（gpt-5.6-sol＋ultra；主程式 C:/Users/Wade/Tools/codex/
   codex-x86_64-pc-windows-msvc.exe）審出 3 blocker＋~30 major（報告=draft/_CODEX_REVIEW_CH5.md），
   Fable 已全章改寫 ch5.md（λ≡T 閉合、載入增量公式 v_i/d_i/Δd_i、方位序列改正、S3賣點刪除、
   f=0.25 解讀範圍前置、A_wet 合成詮釋、三軌法/BPM標定/208萬分母、侷限拆模型簡化+推論範圍）
   ＋跨章修正（ch1 水壓傳遞/水文年/鍵結顆粒；ch6 貢獻標題10字/315mm/221m/驗證→支持；摘要同）。
   自檢 11/11 通過、docx 重建驗證（68圖/13數學段）。
   ✅ Codex 複驗完成（16:36，draft/_CODEX_VERIFY_CH5.md）：0 ❌、核心修正全數確認；
   它再抓 7 個新問題（130日≠100日算術錯、「不失真」「全域」「直接減緩」過強措辭、
   3.2→3.0回彈矛盾、199m時點誤植、ch1滲流尺度限定）→ 已全數修掉並重建 docx。
   殘餘 ⚠️（已知、屬補充深度非錯誤）：BPM標定細節/IDW參數/100×環帶厚度未列規格、
   圖5-13分向逐階數值未擴、946kPa階段差值未列、段長個別超標；
   180 kN/m 與 2.7 mm 兩值已由 v6 dump 代理精算驗證（wf_20a71150 journal），非臆造。
4. ✅ 全文正式排版完成（formal_typeset.py，接在三步產線之後執行；產線現為四步：
   assemble→transplant_math→finalize→formal_typeset，之後用 Word COM 更新欄位）：
   A4＋範本邊界、H1-16pt/H2H3-14pt/行距對齊蔡承翰定稿、封面（郭婷軒/王泰典/115年7月）、
   目錄＋圖目錄＋表目錄（TOC欄位，已用 Word COM 更新）、分節頁碼（前文小寫羅馬、封面無頁碼、
   正文阿拉伯重編）、59圖+10表標題掛「圖標題/表標題」樣式、式(5-1)(5-2)轉真OMML分式＋右靠編號、
   37處內文符號斜體/上下標（T λ f c φ E τ x y z g、η_m η_k、A_wet A_frz、r_wet rk、E_eq K0
   fc ft、σ1′ σ3′ σθ′ p′、u_i v_i d_i R_i Δd_i、ΔN Δh Δpp ux dx dy dz、10^15/13）。
   全文 96 頁，PDF 抽驗（封面/摘要/目錄/公式頁）全過。
   ⚠️ 封面三項待 Wade 確認：英文題名（我擬）、Ting-Hsuan Kuo 英文拼名、日期115年7月。
   ⚠️ Codex 複驗已排 16:36 自動補跑（背景任務 bczgs48e2，輸出 draft/_CODEX_VERIFY_CH5.md）。

## 🆕 老師批改版到件（07-12 傍晚）

00_Document/TTW/ 收到王泰典老師直接改寫版（初稿8_TT，無追蹤修訂）＋手寫新摘要。
**已完成閱讀並記錄：TTW/TT批改閱讀紀錄_20260712.md**（架構對照/術語定版表/圖表重編對照/
摘要要點/各章批改要點/與v6落差清單/待裁決核取清單）。重點：跨尺度・坡地尺度・隧道尺度
等術語欽定、案例提前Ch3、摘要匿名化、Ch2恢復模型系譜圖、結論改條列式；
TT內數值仍為舊跑次（無 s1 T=1.0/v6 錨定帶/A_wet 新定義）→ 合稿時以 v6 成果回填。
**Wade 裁示（07-12 晚）：依老師版合稿。已完成 → 00_Document/260712_TX碩論_Wade.docx（98頁）：**
TT 為基底＋摘要換老師五段版＋英文摘要改寫對齊＋Ch5 回填 v6 定量（雙門檻/黏滯係數/
損傷14,570/密度1.70-1.83%/外壓946/推力1,030/內擠0.15/裂縫199-19-3）＋換圖17張
（照TT編號）＋圖5-21掛新獨立累積圖＋新增圖5-22三維演化。
合稿管線=00_Document/merge_260712.py（冪等，從TT原檔一鍵重建；換圖時清該繪圖srcRect、
其他章刻意裁切不動）。⚠️教訓：全域刪srcRect會毀檔，必須只動換圖的繪圖元素。
21:38 Codex(gpt-5.6-sol ultra) 合稿審完成（報告=TTW/_CODEX_REVIEW_260712.md）：
初判 NO-GO（1 blocker＋13 major）→ **全數修畢**（22:xx）：裂縫排序 blocker（TT 原生）、
s1 舊敘事、7.0 合成註記、密度分母 208 萬、130 日時程、增量載入說明、6.1 主詞、1.3 章名對齊、
術語全域統一（跨尺度/坡地/隧道尺度/資料傳遞）、圖目錄同步（5-22/4-15 入列）、
年份修正（盧碧颱風=2021，與 Codex 建議方向相反、以領域事實為準）、τ-p 與驗證措辭降階、
EN 三處、錯字六處。定版 99 頁；本文/圖目錄殘留掃描全 NONE；數學段 16/表 20/圖 84 完整。
⚠️ 慘痛教訓（已固化）：docx 內含 SEQ/REF 欄位的段落**不可用 set_text 或全文重排**——
會毀欄位（圖表號消失/目錄掉項）。安全作法=逐 w:t 替換（wt_replace）；跨 run 邊界殘留
用 fix_260712_fields.py（無欄位段才整段重寫；Caption 用鄰近複製保 SEQ）。
產線定版：merge_260712.py → fix_260712_fields.py → Word COM 欄位更新。

## 金蟬交接須知（Wade：Fable 額度緊時由 GPT5.6 SOL ULTRA 接手）

- Fable 額度每小時刷新；交接時把本檔＋draft/_CODEX_REVIEW_CH5.md＋WRITING_BRIEF.md 給接手者即可續作
- 論文產線冪等：改 draft/chN.md → assemble_thesis → transplant_math → finalize_thesis（皆在 00_Document）
- 鐵則不變：接手者只執行與回報，決策留 Wade

## 背景知識（需要時查）

- 一頁現況＋完整戰史：`05/RUN_STATUS.md`；狀態鏈：`04/process/couple_solve/README.md`
- 三個定案認知（勿重新質疑）：①介面勁度=zone E＋calm 節奏 ②斷鍵=微損傷、f=0.25=縮尺趨勢
  ③E_eq=1.6GPa、T=0.8（s2-11）＋T=1.0（s1 初始基準，07-11 定案）
- 鐵則：單 console／cd 到 process 傳裸檔名／65s 授權間隔／以腳本自身 log 驗證／restore 清 FISH／
  勿 blanket kill flac／電源永不睡眠
- 現役產線：圖表=05/process 各 render/plot 腳本＋tunnel_frame（勿改 thesis_style/tunnel_frame/
  f3grid_io/crack_classify）；論文=00_Document 三步產線；規劃=THESIS_PLAN/WRITING_BRIEF/FIGURE_STATUS
