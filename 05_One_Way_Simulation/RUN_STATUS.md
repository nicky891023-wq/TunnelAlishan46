# RUN_STATUS — 05 一單向管線 執行現況與交接（live 文件）

> 維護人：Claude（2026-07-02 起接手全管線，OPUS 版已停用）。每完成一段就更新本檔。
> 方法依據：`docs/COUPLING_METHOD_PROPOSAL.md`（D1–D7 已由 Wade 裁示定版）。

## 0. 已定版決策（Wade 2026-07-02 晚）

| # | 決策 | 內容 |
|---|---|---|
| D1 | 小模襯砌 | structure shell 維持＋**分區損傷折減 E**（Wade secant 法，見 §2） |
| D2 | 耦合圍岩 | 單一等效彈性 E_eq，洞壁位移 gate（±15%）校準；MC 對照放附錄 |
| D3 | 大→小驅動 | 扣剛體殘差（make_resid.py，內建應變一致性 gate） |
| D4 | 耦合內牆 | **刪 w_inner**（自由內面）；拱角固定=底部條帶 ball-ball 鍵結不可斷(1e100)+既有 ball-facet 1e20 黏 wz_outter（跟岩壁走）；襯砌無仰拱、關注側壁→頂拱 |
| D5 | 階段制 | 11 階段 W-110↔W-10（dry1 30d / raise 5d×4 / wet 30d / drop 5d×4 / dry2 30d），260529 crp_process_n_wp 法 |
| D6 | 門檻 | **T=0.8 全階段統一、大小模同值**（parameter.f3dat 已改，含理由註記）。「遇水軟化→T 降」保留為機制解釋彈性，不做逐階段調值 |
| D7 | 驗收 | 隧道歷時曲線：低水位≈平、高水位隨時間增；耦合模輸出襯砌外力/內力/裂縫/反力 |

其他固定參數：eta_m=1.2e15、eta_k=2.4e13、crp_dt=600s、K0=0.7、D7 襯砌（E25GPa/t0.4/fc41.2/ft4.12）、PFC 微觀=D7 律定值（parameter.f3dat）。

## 1. OPUS 失敗診斷（為什麼重做，勿重蹈）

小模 stage 1（W-110）：`SS-CHK stg1 ... dmax=0.838 active=1098455 shellMaxC=395230MPa`
- **shell cap 無效**：`struct.shell.young()` 在 cycling 中寫入不觸發元素勁度重組（官方 doc：需 geometry update / `struct.force.update()`；小應變下更新只在 solve 啟動時）→ callback 12 等於沒作用。
- **內部 runaway 真因（07-03 短測抓到，修正先前歸因）**：phase 3 `zone cmodel assign burgers-mohr` **重置全部屬性**，OPUS 的重設清單漏了 cohesion/friction/tension → c=φ=0 → q_th=0 → **active=1,098,455＝rock 總數 100%**（非「T=0.6 的 77%」）＋ MC 零強度塑性崩壞。260529 原版 crp_process_n_wp 與大模腳本都有帶強度參數、只有小模移植漏掉。v2 已修（phase 3 補回 per-layer cohesion/friction/tension）。T=0.8 統一決策不變（track E 驗證依據）。
- 大模 11 階段有 **time-total 累積 bug**（stage2-11 各只跑 600s creep）→ lg_disp_s02-11/resid_s02-11（07-02 19:06 版）內容無效。

## 2. 修法要點（新版腳本的關鍵差異）

1. **large_staged.f3dat**：`cum_days` 累積計數器 → `model solve creep time-total [cum_days*86400]`（已修，07-02 晚重跑中）。
2. **T=0.8**：parameter.f3dat `crp_threshold=0.8`（大小模統一）。
3. **小模 shell cap（段界強制版，待寫 small_staged_v2.f3dat）**：每階段 creep 拆 2.5 天子段；子段之間（solve 外）做 Wade secant 折減：`scale=min(fc/max壓應力, ft/max拉應力, 1)`、`E_new=max(E*scale, 2.5GPa)`、寫入後 `struct.force.update()`；下一子段 solve 啟動時勁度必然重組。**硬 gate：折減後子段末 shellMaxC ≤ 1.1×fc，否則 abort 報告**。
4. 小模流體相 `or cycles 20000` → `500`（260529 n_wp 原值；小模流體 dt~1e-11 本來就到不了穩態，pp 主要由 water set 初始化決定=準穩態假設）。
5. 門檻**每階段評估一次**（固定 active set，06-27 驗證的穩定配方），不用 interval callback。
6. 先跑 **1 階段短測**（5 天）驗證：active 量級、cap 真的鎖住、無 runaway → 才放整跑（長跑前先驗證鐵則）。

## 3. 執行進度

| 步驟 | 狀態 | 產物 / 驗收 |
|---|---|---|
| A1 大模 bug 修 + T=0.8 重跑（11 階段） | ✅ **完成**（07-02 21:26 → 23:59，exit 0，無錯誤） | 見下表；lgs_01-11.f3sav、lg_disp_s01-11.txt 全新 |
| A2 殘差重產 | ✅（07-03 00:0x，應變 gate 全過 ~1e-19） | lg_disp_resid_s01-11.txt |
| B1 small_staged_v2 短測 | ✅ **5 輪迭代後通過**（07-03 上午；debug 全記錄見 §1b） | dmax 全程貼驅動（30.9mm 收尾）、乾態 vclose≈0、maxC 凍住、abort=0 |
| B2 小模 11 階段整跑 | ✅ **完成**（07-03 08:45→13:3x，abort=0 無失穩） | ss_01-11.f3sav；`result/small_convergence_history_v2.png`。**驗收過**：dry2 30 天 Δhclose=0.00（平）、濕峰 W-10 30 天 −2.43mm（增）、退水凍結；active 乾谷 153k→濕峰 478k→dry2 44k；最終 hclose −7.77mm/vclose≈0（純水平橢圓化模態）、dmax 70mm 貼驅動。stg1 含首載瞬態 −4.8mm（與論文舊圖同款）。階段轉換有 MC 再平衡鋸齒（水位階躍＝載重步，物理性）；轉換相殼應力尖峰不在 cap 管轄（改進項：phase 2 後補跑一次 cap）。 |
| C1 耦合 initial 重做 | 🟡 **跑中**（07-03 ~14:00 啟動 couple_servo_v6，預估 6-9hr） | =v5 配方+三修改：①圍岩單一等效彈性 E_eq=2.31GPa（zone 數加權，G2 gate 校準）②拱角條帶（z≤1745.30 的 ball-ball）1e100 不可斷 ③平衡後刪 w_inner→gate（新斷鍵=0、球擾動 mm 級）→ `Couple_Initial_free`。in-situ=07-02 新大模場（三尺度一致性恢復） |
| C2 耦合各階段驅動 | ⬜ 腳本已備（等 C1 過 gate） | `process/couple_staged_v2.f3dat`：控制-0 gate（0 裂縫+0 漂移）→11 階段（cpl_resid 驅動、10×150 ramp+calm、solve ratio-average 1e-4）→每階段輸出：裂縫 DFN dump/wz_outter 反力/mid-band 襯砌力/blue-line vs corner 收斂/裂縫扇區/p(θ,y) map/洞壁位移(G2)。檢查點存 cs_01/06/11。傳遞鏈：`couple_export_bnd_v2.f3dat`（ss_NN→box 邊界帶+洞壁帶匯出）→`make_cpl_resid.py`（Kabsch+應變 gate）→cpl_resid_sNN.txt。裂縫追蹤沿用實跑驗證過的 fracture_track（bond_break→crack_tension/crack_shear DFN）與 couple_qa 函式庫（v2 加 pmap/cwall 匯出） |
| D 論文圖組 | ⬜ | 第五章三組圖 |

### 1b. 短測 debug 全紀錄（07-03 清晨，5 輪，各修一個真 bug）

1. **T1**：active=1,098,455＝rock 100% → 抓到 `cmodel assign` 屬性重置漏補強度（§1 更正）。
2. **T2**：vclose −152m 爆炸 → 我的 bug：`zone gridpoint free velocity` 之後、重固定放在 phase 3 → **phase 2 MC 平衡在無邊界浮動箱上解**。修：tag 時就地 fix+零速度。
3. **T3**：穩定 5 天（dmax 30.9mm 貼驅動）但 maxC ~100MPa——殼應力為**增量累積制**，cap 只能擋未來增長、不消既有應力（Wade 原法的實際作用機制；капped 殼應力值屬虛擬記錄，襯砌受力交付量以耦合模為準）。
4. **T4**：試「cap 迭代（creep off→cycle 200→re-cap ×5）」→ **能量注入型失穩**（dmax 7.8→290mm、隧道外脹）＝官方 SEL 警語情境（timestep 頻變+重複 force.update+程序開關）。棄。
5. **T5（定版）**：v3 流程＋1.25 天 chunk 單次 cap＋kinematic abort（dmax>0.2m）→ 4/4 chunk 穩定、與 T3 同點位逐位元一致、maxC 凍住。**cap 設計定版**。

### A1/A2 成果（大模 11 階段，T=0.8，07-02 夜）

| stg | 水位 | 天 | active | dmax(m) | Δdmax 速率 | box 殘差 med(mm) |
|---|---|---|---|---|---|---|
| 1 dry1 | W-110 | 30 | 117,621 | 1.267 | （含首載瞬態） | 18.2 |
| 2-4 raise | W-90→50 | 5×3 | 75k→38k | 1.454 | 8-22 mm/d | 19.0→20.4 |
| 5 raise | W-30 | 5 | 48,463 ↑ | 1.547 | 18.6 mm/d ↑ | 21.2 |
| 6 **wet** | W-10 | 30 | **80,165** | 2.100 | 18.4 mm/d | **24.9（+3.7）** |
| 7-10 drop | W-30→90 | 5×4 | 64k→5.3k | 2.166 | 12→0.07 mm/d | 25.2→25.1（平） |
| 11 dry2 | W-110 | 30 | 3,571 | 2.166 | **0.03 mm/d＝平** | 25.1（+0.0） |

機制訊號完整：active 在 W-50 谷底（鬆弛主導）→ W-30 起回升 → 濕峰 2.1×、退水快速關閉、dry2 全平。
殘差驅動「乾安靜、濕脈衝」：升段每階段 +0.5~0.9mm、濕峰 +3.7mm、退水後 ≈0。max 殘差 64.6mm。

## 3b. 全專案盤點重整（2026-07-03 上午，Wade 指示）

- 01/02/03/04 全部改為 `input/ | process/ | output/` 結構＋各自 README；**跨資料夾引用已同步修補**（04 scripts → 01/02/03 的 output 路徑；03 build py → 02/input；couple_servo_v5 → 03/output）。root 介面不變：04 root 的 parameter.f3dat＋三個 ★Initial、00 的 W-*.stl（下游固定路徑引用）。
- 已刪（可重生二進位，共 ~12GB）：05 的 lg_s1-4/sd_s1-4/_provisional_oldthreshold；02 的 rock.inp/lining.inp；03 的 WallBall_Only.f3sav/tunnel_full_closed_SOURCE.stl；04 的 stale small_stress_for_coupled/coarse.dat。
- 誤導性過程檔隔離：`05/_archive/`（pre_redo/redo_runs/opus/cap_tests 四區＋警告 README）；頂層 `_archive_05_testfiles/` 補警告 README。
- 05 新增 `result/`（成果圖輸出區）。05 的最終 input/process/output 細分**等整跑結束後再做**（live 檔案不動）。
- 重跑慣例：各 stage 資料夾腳本 cwd＝腳本所在目錄（01/02/03）或 stage root（04/05），README 有註明。

### 3c. 結構二次調整（07-03 晚，Wade 指示）
- 水位面 STL：`00_geometry_water/` → **`05/input/`**（04 與 05 的 4 支腳本引用已同步修補、grep 零殘留）。
- `04/input/README.md`：說明 04 輸入=01/02/03 的 output＋05/input 水位面＋root parameter。
- 頂層 `_archive_05_testfiles/` → `05/_archive/early_tests_0626_0701/`；`05/_archive/README.md` 擴寫為**八條試錯總結**（cmodel 屬性重置/邊界時機/殼增量制/toggle 失穩/累積時鐘/門檻與初始態/耦合漸進/殘差 gate）。
- 新增 `00_Document/`：論文初稿 docx＋**數值方法彙整簡報**（`數值方法簡報_跨尺度圍岩襯砌互制.html`＋assets，9 節，補論文數值方法章的完整架構與現有成果）。

## 4. 檔案地圖（本輪新增/有效）

- `large_staged.f3dat`（已修）＋ `large_staged.log`（新跑）
- `make_resid.py`（新寫：Kabsch 殘差＋應變 gate；OPUS 未留腳本）
- `small_staged.f3dat`＝OPUS 版**勿再跑**（cap 無效+T0.6）；v2 撰寫中
- 舊 `ss_*`/`sd_*` 混參數 sav：sd_s4 是 run2 舊檔與 sd_s1-3 不一致，皆屬歷史對照
- 方法/決策：`docs/COUPLING_METHOD_PROPOSAL.md`、本檔
- 參考：Wade shell cap 原法 `C:\Users\Wade\Desktop\Wade_TD_SCI\FLAC\code\CreepSupport\CreepFISH\WadeCreepSupport.f3dat`；260529 流程 `C:\Users\Wade\Desktop\ClassPhD\test\TX\260529\02_small_model\helpers\crp_process_v3.f3dat`

## 5. 接手須知

- console 跑法：`flac3d600_console.exe <f3dat>`、stdin 關閉、結尾 program quit；GUI 開著可能佔 license seat（07-02 實測 Wade 關 GUI 後 console 正常）。
- 長跑必掛看門狗（log grep stage 完成+Error）；短測先行；每步產物寫回本檔。
