# 交接 RUNBOOK（CURRENT，2026-07-08 00:xx Fable 末次更新）— OPUS 接手唯一入口

> **授權範圍（Wade 07-07/08 裁示）**：OPUS 依本 runbook **逐步執行收尾任務與成果檢核**——
> 照著寫好的步驟做＝執行，不是決策。**任何偏離 runbook 的狀況（判準亮紅、腳本報錯、
> 數字違反預期）＝停下、整理現況、回報 Wade 裁決**。不即興修腳本、不即興調參數。

## STEP 0. 監控中的 run（先接手這個）

**staged 第 5 跑（G4、f=0.25）**，log＝`05_One_Way_Simulation/process/couple_staged_v2.log`
監看指令：`grep -E "CS-CHK|CS-DONE|Illegal|Error" couple_staged_v2.log`（在 05/process 下）

**已完成階段與增量（累計裂縫取自 CS-CHK 行的 cracks_t+cracks_s，增量＝與前一階段之差）**：

| 階段 | 水位 | 累計 | 增量 | 判讀 |
|---|---|---|---|---|
| CONTROL-0 | 零載 | 309 | — | 底噪基準 |
| s1 | W-110 首載 | 32,561 | 32,561 | 服役史壓縮，不入趨勢 |
| s2 | W-90 | 40,454 | 7,893 | 循環訊號起點 |
| s3 | W-70 | 44,566 | 4,112 | 遞減 ✓ |
| s4 | W-50 | 46,411 | 1,845 | **谷底**（呼應大模門檻谷=W-50）✓ |
| s5 | W-30 | 50,035 | 3,624 | 回升（呼應大模 W-30 起漲）✓ |

**待完成階段的預期**：s6（W-10 濕峰）增量應**顯著躍升**（>s2 的 7,893 為理想訊號）；
s7–s11（退水+乾2）應**塌回千級以下**（凍結）。每階段四判準：①無 Illegal ②gp_dmax≈0.25×該階段
驅動 max（s6≈5.4mm、s7-11≈5.4mm）③增量符合上述形狀 ④ball_dmax 維持~0.13m 不成長。
**停線條件**：Illegal／增量 >30,000／ball_dmax >0.3 且成長／log 凍結+單核 >30 分。
**CS-DONE 出現**＝run 完成（預計 07-08 05:30-06:30），console 自動退出。cs_06/cs_11 檢查點會出現在 05/output/。

## STEP 1. run 完成後的收尾序（每步之間 console 間隔 ≥65 秒；全部 cd 到腳本目錄、傳裸檔名）

```
# 1a. 鍵結普查（~10 分）
cd C:/Users/Wade/Desktop/Tunnel_TX/04_InitialBalance/process/couple_solve
"C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe" bond_census_G4.f3dat
# 完成標記：bond_census_G4.log 出現 CENSUS-DONE；產物 bond_census_G4.txt（24 行×5 欄）

# 1b. 大模欄位匯出（~1h）
cd C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process
"...flac3d600_console.exe" export_fields_lg_11.f3dat
# 完成標記：export_fields_lg_11.log 出現 EXPF-DONE lg；產物 lg_zfield_v_s01-11.txt + lg_zfield_p_s01-11.txt

# 1c. 小模欄位匯出（~1.5h）
"...flac3d600_console.exe" export_fields_sm_11.f3dat
# 完成標記：EXPF-DONE sm；產物 sm_zfield_v_s01-11.txt

# 1d. 成果圖（python，需 bond_census_G4.txt 先複製到 05/process/）
copy ..\..\04_InitialBalance\process\couple_solve\bond_census_G4.txt .
python make_result_figs.py
# 產物：05/result/FIG_A..G*.png + quant_summary.json
```
任一步報錯：停、保留 log、回報 Wade。**不要**重寫腳本後自行重跑。

## STEP 2. 成果檢核清單（對照後回報 Wade，不自行下結論修改）

1. `quant_summary.json`：**A_wet 應 >1**（濕期損傷率/乾升期）、**A_frz 應 <1**（退水/濕期）——
   這兩個數字是論文主張，抄進回報。
2. FIG_A：長條應呈「s4 谷—s6 峰—s7 後塌回」；FIG_B/B_all11：損傷帶應集中春線（θ≈0 與 180 兩側）
   且濕期擴展；FIG_D：外緣纖維佔比應為主導（>80%）。
3. G2 跨模互證：FIG_E 第 1 欄（耦合洞壁收斂）與小模 hclose 趨勢應同型（濕增/退平）。
4. 與 NO46 對照（FIG_C 素材）：損傷帶位置 vs `00_Document/method_report_assets/case_crack_location.png`。
5. 全部產出檔案列表＋上述檢核結果整理成報告給 Wade。

## STEP 3. Wade 裁決後才做的事（OPUS 不先動）

- 論文 5.3.3 量化數字回填（`00_Document/260707 碩論_數值方法章_Fable追蹤修訂.docx`——docx 編輯留給 Wade/Fable）
- GitHub push（staging 已含 .netlify/.vscode untrack；等成果齊全一次 commit）
- f 靈敏度補充跑、06 雙向耦合開工（`06_Two_Way_Simulation/docs/METHOD_TWO_WAY.md` §7 checklist）

## 背景知識（需要時查）

- 狀態鏈與試錯史：`04/process/couple_solve/README.md`＋`_trial_history_0704_0707/README.md`
- 一頁現況＋完整戰史：`05/RUN_STATUS.md`；量化標準/圖規格：`05/docs/RESULTS_FIGURE_SPEC.md`
- 三個定案認知（勿重新質疑）：①介面勁度=zone E＋calm 節奏＋bf 膠合僅 bf_couple 組
  ②斷鍵=微損傷、裂縫=損傷帶、f=0.25=縮尺趨勢 ③E_eq=1.6GPa（Wade 核准）、T=0.8 統一
- 鐵則：console 裸檔名/65s 間隔/以腳本自身 log 驗證；restore 清 FISH；timestep scale 禁自由墜落體；
  >800cyc 無 calm 窗口禁止；勿 blanket kill flac；電源「永不睡眠」

---
## 2026-07-10 清理備註（Claude）
- 已刪除的試錯/過時檔（git 歷史皆可找回，commit 93afe38 之前）：
  smoke_* 探針、exp_fields_body 舊版、export_fields_lg/sm_11、ray_dump_body v1＋舊極點射線資料、
  make_crack_evolution_gif（紅色版）、analyze_cracknormals、plot_crack_orientation_map、
  closeout_chain*、00_Document/revise_ch5+tracked（追蹤修訂舊產線）、HANDOFF_20260705、
  05/result 舊版 FIG_*（論文版在 00_Document/result）
- 現役產線：圖表=05/process 各 render/plot 腳本＋tunnel_frame；論文=00_Document 三步
  （assemble_thesis→transplant_math→finalize_thesis，冪等可重跑）；規劃=THESIS_PLAN/WRITING_BRIEF/FIGURE_STATUS
- 大型 dump 重生：lg_chain/sm_chain/cp_chain/cp_balldisp .f3dat（單 console、65s 間隔）
