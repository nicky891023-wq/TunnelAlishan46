# RUN_STATUS — 05 一單向管線 執行現況與交接（live 文件）

> **⚠ 2026-07-05 交接**：接手者先讀 **`../HANDOFF_20260705.md`**（現況/正在跑的東西/決策樹/判準/鐵則）。
> 接手者只監控回報，**所有決策給 Wade 裁決**。本檔為完整戰史，交接文件為行動指南。
> **07-07 起 Wade 全權授權 Fable 執行**（監控/檢核/修正/完成）；方法級變更仍回報 Wade。

## ★ 一頁現況摘要（2026-07-07 下午）

**三尺度**：大模 ✅ 驗收過｜小模 ✅ 驗收過（低水位平/高水位增/退水凍結）｜耦合模 🟡 初始態最後一步（STEP I 重澆）跑步中。

**耦合初始態生產鏈**（04/process/couple_solve/README.md）：
`Couple_Initial`(free2, 岩凍結) → STEP G v5 → `G3`(彈性傳遞介質) → **STEP I v2 → `G4`(無應力重澆環)＝staged 正式起點**

**三個已定案的關鍵認知**（各有量化證據，見 C1/C2 與兩個 _diag 資料夾）：
1. **wall-zone 介面積分不穩定**（軟岩+硬介面，calm 腿 vs 裸窗斷鍵率差 150-350×）→ 解法：介面勁度=zone E＋calm 節奏＋bf 膠合僅 bf_couple 組。
2. **安裝鎖入力網的預拉尾收割**（0.003% 應變仍產 5k 假裂縫；劑量反應 f0.25→38k/f0.05→5k）→ 解法：STEP I 零重力原位重澆。
3. **E_eq=1.6 GPa＝Wade 核准定案**（隧道幾乎全在 l4=1.5GPa 弱層；位移驅動下軟岩傳得少＝對襯砌友善）。

**接下來**：G4 落地 → staged 改指 G4（f=0.25 起、無應力環量真物理）→ stage-1 在線判讀（適度開裂→直接續跑 11 階段；過猛降 f/過靜升 f）→ G1/G2/G4 gate＋NO46 對照 → 成果圖 → 方法文件 → GitHub。<br>**✅ STEP I v2 完成（07-07 16:0x，Couple_Initial_G4 落地）**：重澆 2,268,301 全新零力鍵；自診斷實抓長期異常點 (1299.7,902.3) 卡力 307kN→準靜態放電 755 鍵（一次性）；重力五階爬回全程受控（0.1g 坐床 2,254→304 衰減、1.0g 末腿僅 17）；**GATE：重澆後總斷鍵 6,377（0.28%）、環帶均值 −0.0004mm≈0、gp 3.70mm 鎖定、全程零 Illegal**。全案第一個「無應力、自重平衡、材料定案（E_eq 1.6 烘入）」初始態。**staged 已改指 G4＋清 A′ 覆寫、f=0.25、16:1x launch**（第 5 次 staged 啟動——前四次死因均已逐一構造性排除）。

**鐵則清單**：見 ../HANDOFF_CURRENT.md ＋ 04/…/couple_solve/_trial_history_0704_0707/README.md（12 次嘗試對照表）。
**實務**：長跑期間電源設「永不睡眠」（07-06 夜實測睡眠凍結 run 8 小時）。
**✅✅ CS-DONE（07-08 04:1x，staged 第 5 跑完整跑通）**——耦合模 11 階段完成，**D7 驗收訊號完整**：增量序列（循環訊號）s2=7,893→s3=4,112→**s4=1,845（谷=W-50，呼應大模門檻谷）**→s5=3,624（W-30 回升）→**s6=38,793（W-10 濕峰爆發，前階段 10.7×，超過首載）**→s7=8,835（退水回落）→s8-10=862/643/679（地板）→**s11=43（乾2 三十天死平，凍結比 ~1000×）**。s1 首載 32,561 單獨呈現。品質：gp_dmax 全程精確貼 0.25×驅動、ball_dmax 殘屑靜止 0.128m、**全程零 Illegal**；cs_01/06/11 檢查點齊。「乾遞減—濕爆發—退水凍結」三尺度互證成立。**收尾自走鏈已啟動**（closeout_chain.sh：census→lg/sm 欄位匯出→make_result_figs → 05/result/FIG-A~G＋quant_summary.json；狀態檔 process/closeout_chain.status；runbook=../HANDOFF_CURRENT.md）。

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
| C1 耦合 initial 重做 | ✅ **完成**（07-04 → `04/output/Couple_Initial.f3sav`＝free2 定版）：v6 圍束平衡 ✅（servo 全程無 solveForX，斷鍵 376/907k=0.04%）→ STEP F 刪內牆首驗未過（新斷鍵48、球位移0.284m）→ **診斷=散球非下垂**（movers 72/456k=0.016%、blue-line 環收斂平均 0.005mm、拱角帶 0.065mm）→ 處置：刪 46 顆 >20mm 散球＋重收斂 → 重驗 dmax 0.6mm ✅；殘餘斷鍵涓流=**真實拱肩張性微裂**（97% 拉、拱角/端部零）→ gate 重定義「運動學安靜＋CONTROL-0 定量底噪、各階段裂縫增量淨額解讀」。<br>**07-04 console 事件（教訓）**：半夜 03:23 起 console 卡死→重開機後其實已恢復，但我用「flac3d.log 必存在」當驗證判準造成連環誤判（正確判準=腳本自己的 program log-file/存檔產物）；卡死根因=v6 退出後 10 秒內搶跑下支 console 的授權殘留。**鐵則：①console 接 console 隔 ≥60s；②驗證用腳本自身產物；③勿 blanket kill flac（會誤殺 GUI）**（v6 原始腳本：07-03 ~14:00 啟動，6-9hr） | =v5 配方+三修改：①圍岩單一等效彈性 E_eq=2.31GPa（zone 數加權，G2 gate 校準）②拱角條帶（z≤1745.30 的 ball-ball）1e100 不可斷 ③平衡後刪 w_inner→gate（新斷鍵=0、球擾動 mm 級）→ `Couple_Initial_free`。in-situ=07-02 新大模場（三尺度一致性恢復） |
| C2 耦合各階段驅動 | 🔴→🟡 **首launch無效已中止、STEP G 修復中**（07-04）。首 launch（17:20-19:24）stage 1 CHK 揭露**凍結岩箱事故**：cracks 18,725、但 (a) log 收斂行 `mech Zone Main (0.0000e+00)`＝zone 殘差恆零＝gp 全固定（couple_servo_v6:47 球安裝期全域凍岩、從未解凍，free2 繼承）；(b) 解讀帶(y870-900)洞壁 |u|=0.000mm vs 小模 med 3.56mm（G2 全敗）；(c) 18,683 新裂縫 100% 在兩端環（8412/10271）＝被驅動端面岩壁 vs 不動端平台的剪切假象；解讀帶零新增。→ 19:24 kill、產物隔離 `_diag_frozenrock_0704/`（含 README）、cs_01.f3sav 刪。**處置 STEP G**（04/process/couple_solve/couple_stepG_freerock.f3dat，19:29 啟動）：G1 岩箱轉增量彈性傳遞介質（zone 應力歸零＋density→1 去自重＋全域解凍＋僅重固定 6 外邊界帶；絕對應力/重力歷史由小模承載，耦合箱只傳增量——論文可交代）→ G2 刪端平台 w_860/w_910（端環改跟岩走）→ 各相 gate（新斷鍵~底噪、位移 mm 級）→ Couple_Initial_G → staged 重跑（腳本已改 restore 路徑＋CS-CHK 加 gp_dmax 監測欄）。**CONTROL-0 首輪參考值**：42 crack 全集中右側壁腰單點簇（y≈888、38拉4剪）＝既知應力集中核。<br>**STEP G 首跑失敗（22:58）**：G1 solve 9,474 cycles ratio 卡 1.6e-1 不收斂（持續運動非沉降）→ `Illegal geometry in zone 260648`＝**右拱角腳旁岩體 (1301.3, 877.8, 1745.0)**，位於 servo 洞周 apply 帶（v6:482/502 `stress-normal −1.4MPa`，x1292-1303 z1743-1752）內的凹角應力集中點。**H-apply 假說**：v6:533 的 `stress-normal 0` 未必取代 servo apply 物件→ 存檔殘留 1.4MPa 恆定推力 × 零應力柔軟岩體 = 失控。短測診斷 couple_stepG_diag（23:05→00:25）**判決：H-apply 確認**——D1 重現（底板/腳部被推、球被擠鬆）；D2 apply-remove 後岩體靜（2000 cyc 僅 6/441,728 gp >1mm、max 2.24mm、減速中）。殘餘 240mm 位移者＝洞膛內鬆散球自由落體（r≈0.7m，free2 清理漏網——當年只刪已動 >20mm 者；D4「球不能一直掉」要求本來就該清）。**STEP G v2（00:3x）也失敗（03:44 Illegal zone 84170）**：G1 6000cyc 斷 29,491 鍵、標記 295 顆 >20mm；刪後 G1b 又 ~4000cyc 再翻 zone。**根因 2＝timestep scale 制式下墜落物是質量放大破城錘**（慣性質量 stiffness-scaled ~1e9 kg；散球長距墜落後撞柔軟無自重岩面，逐撞 ratchet 至 zone 翻轉）——「先讓它掉再清」策略在此制式下根本錯誤。**STEP G v3（03:5x）关键進展後仍敗（06:45 Illegal zone 274267）**：孤兒預清除僅 38 顆（→散球主要是解凍「新製造」的）；8×800 掃除短腿全存活（gp_dmax 成長 leg8 已減速 25.5mm、掃除個位數）——**但 4000-cycle 無掃除 polish 第 1,329 cycle 翻 zone**；斷鍵率 ~5k/腿恆定不衰減。**根因 3（最終）＝安裝鎖入力庫**：球格架在剛性模具內 settle+servo 成形，格架鎖著大量自平衡接觸力（剛模平衡→穩定、STEP F 才會安靜）；岩模一步軟化＝全庫同時重分配→斷鍵能量級聯（timestep scale 質量放大更兇），任何長無掃除窗口必死。**STEP G v4（06:5x 啟動，退火版）→ ✅ 12:2x DONE（Couple_Initial_G 落地）**：P 孤兒清除 → apply-remove+零應力+density 1 → **E_zone 六階梯 1000×→100×→30×→10×→3×→1×E_eq**（每階只釋放一小部分失衡；印證 _archive 教訓#7「耦合模需漸進釋放」）→ 每階梯 600-cycle 掃除短腿 → 「短 solve 1500↔掃除」交替 → G2 刪端平台+短腿 → Couple_Initial_G。**實測**：退火階梯全程近乎無聲（A1000→A1 累計斷鍵僅 205、gp µm 級——v3 同進度 25,547 且死）；最終 solve 相釋放 15.6k（G1 gate：環帶均值 −0.002mm、gp 7.3mm）；平台移除一次性釋放 17.5k、底板 gp 38.6→32.8mm 回彈趨衡。**總轉換成本 33,259 斷鍵（1.47%）、刪球 204 顆、無任何 Illegal**。G2 gate：環帶均值 −0.05mm≈0、max 11.2mm（既知右肩核）。→ post-mortem 空間掃描（couple_stepG_pm）：冠部完好、損傷集中腳帶邊界＋右春線（與 NO46 春線縱裂同型態）、洞內漂球僅 1 → 放行 staged。<br>**但 staged 重跑（12:45）CONTROL-0 又翻 zone 273817（14:0x）**——回查 v4 數據：F1 solve2 −8,986、G2 末 solve −5,921＝**級聯未流盡**，Couple_Initial_G 是「仍在排水中」的快照，每個無掃除 1500-3000 cyc 窗口仍斷 4-6k 鍵。**STEP H（14:2x 啟動）＝排水＋原位再鍵結**：6 條掃除排水腿（坐床）→ **以不變的 D7 微觀參數在坐床幾何上重新形成全部 ball-ball 鍵結**（新 pb 鍵零初始鍵力＝鎖入力庫歸零、轉換損傷歸零；腳帶 1e20 重覆寫）→ 驗證（掃除腿+solve 2000+GATE：re-bond 後新斷鍵須 <500）→ **Couple_Initial_G2**（G 留作 fallback）。**物理正當性**：鎖入力是「剛模組裝」人工產物；真實襯砌是原位無應力澆築固化再受載——re-bond＝原位固化的數值類比，比拖著人工預應力的環正確。staged restore 路徑已改 G2。<br>**STEP H 三連敗（v1 排水/v2 re-bond/v3 全力歸零重澆）→ 真兇定案：wall-zone 介面積分不穩定**。歷程：v1 排水腿顯示兩拱腳線等速 ~20mm/腿犁入（誤判為拱腳外撐機構）；v2 立即 re-bond 後驗證腿仍斷 12k（誤判為環向預壓 lin 力網）；v3 unbond+lin_force 0+重澆＝墜落試驗（39.7k burst，把 6MN 承重內力一次歸零、內面無支撐）後仍死於 solve 窗（Illegal zone 62528，第四翻）。**決定性數值特徵**：A1 全軟下「600-cycle 腿＋calm」每腿僅斷 10-45 鍵，「>1000-cycle 無 calm solve 窗」每窗斷 3.7k-8.9k——**每 cycle 斷鍵率差 150-350×**。物理過程不在乎 calm 節奏；**積分不穩定需要數百 cycle 振幅 e-折疊**——calm 截斷成長、長窗長到斷鍵振幅。佐證：退火 A1000-A10 全靜、A3/A1 發病＝k_zone 降至球-壁面接觸勁度量級的門檻；物理帳（環自重在 E_eq 床的沉降 ~0.1mm）證明 20mm/腿非物理。假說：gp 慣性質量縮放只計 zone 勁度、不計 ball-facet 接觸勁度 → 軟岩處介面局部超出 dt=1 穩定界。**16:5x 派 5+1 文件代理查官方 doc → 17:4x 裁決（引文為據）**：①機制修正——接觸勁度「有」傳給 gp 但**僅在 zone update 事件時**（wall-zone update-tolerance 觸發），且兩側積分都**貼著 dt=1 穩定邊界零餘裕**（scale 模式球質量恰=k·dt²；FLAC gp 質量恰≥勁度），pbond 轉動勁度換算/腳部多邊接觸/更新間隙的任何局部低估即越界；calm 靠截斷指數成長存活（解釋 150-350× 差）。②**最佳補救（官方範例先例）＝介面勁度一致化**：唯一 wall-zone 官方例 PunchIndentation 刻意讓 zones 與 cmat 用同一模數（“use this as the Young's modulus of the bed of zones as well”）、對比時只讓 zone 更硬；v7 新增的 compute-stiffness 修正也以勁度一致為前提（6.0 無此指令）。③附註：PFC doc 明示 timestep scale「不適用路徑相依解」（本案破壞路徑相依＝已知妥協，靠 calm 節奏管理）；FLAC 側 scale f/safety-factor 對靜態零作用。④官方例配方：ball damp 0.7＋`model cycle N calm M`（**cycle 指令內建週期 calm**）。**17:5x 探針啟動（couple_ifx_probe）**：bf 介面（全部 ball-facet=wz）emod/pb_emod→2.31e9、強度 1e20 不動、cmat default 同步——G 存檔在裸窗 >1500cyc 四連死＝現成必死測試台，補救後須連活 2×2500 裸窗。過→重建乾淨初始（從 Couple_Initial 一步解凍+介面一致化）；staged 長 solve 改「cycle+calm 節奏＋短 ratio 檢查窗」。介面軟化的物理詮釋＝背填層，G2 gate 後續吸收。<br>**探針結果（07-05 19:01，OPUS 記錄，待 Wade 裁決）**：起 intact=2,234,087 → A 窗(2500 裸 cyc) 2,230,817（斷 3,270、gp_dmax 18.75mm@右腳、ball_dmax 256mm）→ B 窗(再 2500 裸 cyc) 2,230,684（**斷 133**、gp_dmax 19.40mm 同點＝**幾乎持平**、ball_dmax 605mm）→ IFX-DONE 乾淨退出。**判讀**：①**無任何 Illegal geometry**——同一軟岩組態先前裸窗四連死，此次連活 2×2500 裸窗＝介面不穩定治癒的決定性證據；②B 窗斷鍵 133（<200 判準）、gp 增幅 +3.4%＝收斂非發散（runaway 特徵是倍增）；③A 窗 3,270（>2000）＝殘留鎖入力庫＋散球一次性釋放（探針刻意未做孤兒清除/退火，裸測介面補救）；④ball_dmax 256→605mm＝單顆散球續墜（探針未清孤兒；STEP G v5 有孤兒預清除故不會殘留）。**結論：介面補救成立，A 窗大斷鍵屬探針未處理的殘留源、非介面失穩。** 決策點 A 回報 Wade。<br>**Wade 裁決＝選項 1（07-05 晚）**：launch STEP G v5，過 gate 才跑 11 階段；綠燈自動前進、紅燈停線討論。**STEP G v5 已 launch**（OPUS 執行，restore 乾淨 Couple_Initial→存 Couple_Initial_G3）。gate 判準：無 Illegal、new_broken ≲2000、midband ur mean <0.5mm、gp_dmax <10mm。過→自動 launch staged（`couple_staged_v2.f3dat` 已指 G3、全 calm 節奏）；不過→停線。<br>**STEPG v5 GATE ✅ 全過（07-05 23:51，Couple_Initial_G3 存檔）**：new_broken=**91**（v4 是 33,259——介面一致化幾乎消除轉換損傷）、midband ur mean −0.00003mm≈0、gp_dmax 0.059mm、ball_dmax 1.08mm、**無 Illegal**。退火階梯全程近乎無聲（累計~57）、刪端平台從 v4 的 12k 斷鍵災難變成 gp 44µm 無事件、calm settle 窗（v4 致命窗）安然度過。**耦合模初始態確立＝Couple_Initial_G3（一致介面彈性傳遞介質、自由內面、無端平台、拱腳錨定）**。→ OPUS 自動 launch 11 階段 staged。<br>**staged 第三跑（07-05 23:5x 從 G3）**：CS-0 balls=456,218（=G3）✓、20,648 驅動 gp ✓。**CONTROL-0 底噪基準（綠燈）**：cracks=**49**、ball_drift=**0.28mm**（嚴格判準<0.5mm ✅，比凍岩版 2.47mm 好 9×）。49＝全跑裂縫基準線（自由內面真實拱肩微裂+重坐床），各階段裂縫扣 49 解讀。自動接 stage 1。**各階段 CS-CHK 判準**：gp_dmax 須 mm 級（岩體傳遞）、裂縫淨增量、ball_dmax 貼驅動(~10mm)；停線＝Illegal/裂縫爆量/dmax runaway。<br>**stage 1 停線（07-06 03:2x，Illegal zone 263384）**：診斷發現＝**物理性環體碎裂、非數值問題**。ramp(10×150 calm)＋2400-calm settle 皆存活，死在最後 800-solve；但碎片數在**有 calm 的載入全程穩定累積**（calm 相 2,180 fragment 事件 vs 無 calm solve 僅 51）→ 373→2,573 碎片＝環失去結構連續性。驅動證實乾淨（中位 4.78mm、max 15.7mm、無 IDW 尖峰）。**旁證**：小模真實分層岩＋shell 襯砌同物理只受控損傷不碎裂 → 問題在耦合端襯砌強度/軟岩剛度/介面軟化副作用。**Wade 裁示：先診斷再考慮調參。** couple_load_diag（07-06 10:2x）：從 G3 施 25/50/75/100% 驅動、calm ramp 無終末 solve、各級 census 斷鍵數＋空間分布（feet/spring/crown）。判讀：線性且集中結構位置＝物理對（查 E_eq/細分 sub-step）；25% 就爆或均勻散布＝強度/軟岩。**耦合初始態 Couple_Initial_G3 有效、保留；G(v4)/v6_confined 為試錯可刪（待 Wade）。**<br>**stage-1 載入診斷結果（07-06）**：新增裂縫 96→4,388→17,123→36,415（超線性、25-50% 間門檻）；**92% 集中兩腿 springline、拱腳 0（1e100 完好）、拱頂少**＝無仰拱馬蹄環的「腿部彎裂」，位置符合 NO46＋邊坡右推。驅動乾淨（中位 4.78mm 無 IDW 尖峰）。**一度誤判「實心球柱 build bug」→ 出橫截面圖自我更正**：模型是正確馬蹄環（見 result/coupled_xsection_and_cracks.png），我的徑向直方圖用錯圓心（無仰拱環的假圓心貼近左壁）。**真因＝襯砌太脆＋軟岩不圍束**：~5mm 收斂＝0.06% 應變 >> 開裂應變 0.016%，球襯砌一裂就脆性碎裂無殘餘（缺配筋延性）。**Wade 裁示：先試「改材料參數（不用重做力平衡：強度/零應力態剛度都不影響零內力初始態）」，參數若超出真實範圍再加折減驅動。目標＝跑完 11 階段看階段差異趨勢、量值合理更好。** couple_matcal_diag set1（×2 襯砌、×2 岩/介面）：f100=24,363（原始 36,415、只降 33% 仍碎裂），且調硬岩/介面在位移驅動下幫倒忙（更硬傳遞=更多力給襯砌）→真實範圍材料參數壓不住（需 ×4 ft16 才行、不真實）。**方案定案＝A（Wade 07-06）**：材料全物理不動（圍岩 E_eq 2.31、襯砌 D7 ft4）＋施加變形折減 **f=0.25**（load_diag 校準 1.2mm→~100 裂縫/2.4mm→碎裂；11 階段 4.78-7.40mm×0.25=1.2-1.85mm→乾~100/濕~800、15× 趨勢無碎裂）。物理依據：5-7mm 收斂=0.06% 應變>>開裂 0.016%，球鍵脆性碎散（缺配筋延性），折減使停在離散裂縫發展區間。**交付＝pattern/相對趨勢，非絕對值。** couple_staged_v2 加 DRIVE_SCALE=0.25，07-06 從 G3 啟動全 11 階段（成功且合理後結合 Fable 成果寫方法紀錄）。<br>**Contingency（Wade 07-06 共識，成果不佳時依序）**：①**優先降 E_eq 2.31→1.6-1.8 GPa**（隧道幾乎全在 l4=1.5GPa 主導層，互制看洞周局部岩＝l4；且位移驅動下軟岩少傳力給襯砌＝減少開裂；改 E_eq 不用重做平衡、**介面剛度須同步降到同值維持一致化**）②其次 **f 0.25→0.20**。順序：先看 f=0.25/E_eq2.31 結果→不佳先調 E_eq→仍不佳再調 f。<br>**效能修復 v3（07-06 22:xx）**：f=0.25 首跑卡在 track_init 的 `fragment register ball-ball` 28 分鐘（2.27M 鍵註冊 fragment 追蹤，1 核、log 凍結）；且追蹤函式每 50 裂縫對全 456k 球跑 `fragment compute`＝各階段爬行。→ 做 **fracture_track_v3.fis 移除全部 fragment 操作**（只留每斷鍵建 crack DFN；dump_cracks 讀 DFN 照常、只失 mm 級裂縫位置微調）。staged 改 call v3、重跑：track_init 即時通過、CONTROL-0 進 20 核全平行 cycling。**CPU 判準**：設定/tag=1 核 4%（短暫正常）、cycling=~20 核（主運算）；長時間卡 1 核+log 凍結=異常。<br>**f=0.25 stage1 又碎裂（38,428 裂縫、ball_dmax 37.6mm）——校準方法有誤**：驅動確實折減（gp_dmax 3.9mm=0.25×15.7max），但**ramp-only 診斷嚴重低估**——f=0.25 只 ramp=514 裂縫，但 staged 的 ramp+settle2400+solve800 讓裂縫暴增到 38k（~75×）。機制＝**脆性襯砌在持載平衡階段逐圈級聯**（held-load、cycle 3200 圈、每斷鍵→重分配→再斷→全碎；ball_dmax 37.6mm=驅動 10× 環崩塌）＝無配筋脆性球襯砌的模型特性（真實 RC 有鋼筋止裂不會這樣）。**校準必須用完整階段流程、非 ramp-only**。<br>**方案 A′（Wade 07-07 裁示）**：①E_eq **2.31→1.6 GPa**＋介面同步 1.6（隧道幾乎全在 l4=1.5GPa；軟岩少傳力；G3 零應力態不用重做平衡；介面=zone E 維持一致化）②f **0.25→0.05**（壓到穩定裂縫門檻下）。完整 stage-1 測試通過（裂縫止裂於適度、非級聯全碎、ball_dmax mm 級）→自動接 11 階段。couple_staged_v2 已改（young 1.6e9+iface 1.6e9+DRIVE_SCALE 0.05），07-07 啟動。判準：stage1 裂縫數百~低千（非 38k）、ball_dmax<~5mm、gp_dmax~0.8mm(0.05×15.7)。<br>**Fable 深度診斷（07-07 上午，f=0.25 殘留證據 post-mortem）——修正「襯砌太弱/圍岩太軟」判讀**：①裂縫出生時間曲線（age 欄重建）：CONTROL-0+ramp 前半 3000cyc 僅 95 條→**點火於 ramp 中段等效 0.13× 驅動（0.6mm≈0.008% 應變，不到開裂應變一半——真材料不可能）**→峰值 5,009/200cyc 在 ramp 剛結束→單調衰減至 328/200cyc＝**水庫洩流形狀**，非崩塌加速形。②洞壁位移場（cs_s1_cwall 22,537 顆）：|u| max **1.34mm、>10mm 零顆、86%<1mm**、hclose −0.14mm——**38,428 鍵斷時環體紋絲不動＝非結構破壞**。**機制定案＝安裝鎖入力網的預拉尾端收割**：G3 球-球接觸力網從未歸零（揹著 servo 力鏈，預拉尾貼著 pb_ten），微小附加變形即開始收割尾巴（斷→改道→再斷→衰減洩流）；位置＝春線/腳帶邊（STEP G v4 PM 的鎖入應力帶）。07-05「鎖入力庫」診斷正確——當時與介面不穩定並存，修了介面沒排力庫（G3 gate 無載故尾巴沉默）。**大部分「裂縫」是安裝殘留假損傷，非階段荷載的物理開裂。**<br>**Wade 07-07 全權授權 Fable 執行到底；E_eq=1.6GPa 為 Wade 親自核准定案值（隧道幾乎全在 l4 弱層）**。工作流程：①A′ 跑完 stage-1（免費驗證診斷：預測數百~低千衰減式假裂縫、無結構位移）→kill、資料留存 ②**STEP I 零重力原位重澆**（STEP H v3 敗因僅在 1g 墜落；0g 下 unbond+lin_force 0+重鍵→死寂→重力 0.1→1g 五階爬回，全指令已實跑驗證；E_eq/介面 1.6 烘入）→ **Couple_Initial_G4**＝真無應力原位澆築環（只揹自重 kN 級，遠離強度尾）③f 重校準（全流程 stage-1、從 0.25 起——無預應力環量到的才是真物理）④全 11 階段→成果檢核（G1/G2/G4 gate、NO46 對照）→方法文件（結合 Fable 前期架構）→GitHub。<br>**A′ stage-1 判決（07-07 11:4x）＝診斷確證**：CONTROL-0 過（58 底噪、drift 0.23mm）；stage-1 f=0.05（施加 0.24mm≈0.003% 應變，物理不可能開裂）仍斷 **~4,956 條**（gp 1.17mm 岩正常、ball_dmax 75mm=鬆球滾遠）。**劑量反應 f=0.25→38.4k / f=0.05→5.0k ＝尾巴任何擾動都收割、不存在可用 f 窗口**。A′ 路線關閉；證據庫歸檔 `_diag_prestress_harvest_0707/`（含 README：時間曲線/位移場/劑量反應三證據）。**STEP I v1 敗（11:55，Illegal zone 260104@右腳角、0g 零力態 cycle 313）**：log 證實重澆鏈全數執行（unbond 4.36M+377k、lin_force 歸零 4,735,479、重鍵全套）——零力+零重力下仍爆＝**v1 的 bf 重鍵用了 type 全綁（377,610 個＝原 bf_couple 組 62,556 的 6 倍，多邊接觸次級全上 1e20 鍵）**→每顆表面球揹 6 條轉動勁度 pb 鍵→gp 質量縮放低估被 6 倍放大→介面積分不穩定重越界（零力態＝不穩定平衡點，roundoff 種子 e-折疊 313 cycle 爆在 facet 最密的右腳角）。佐證：v6→G3→A′ 全部穩定組態都是 bf_couple 組 62k。**STEP I v2（12:0x 重啟）**：bf 重鍵退回 `range contact group 'bf_couple'`＋內建自診斷（重澆後 max|F| 掃描全接觸＋3×100cyc 微腿 max 速度/argmax——零力態不靜立即現形）→V0G→重力五階爬回→gate→**Couple_Initial_G4**。預計 ~15:30。**教訓：①狀態手術先短測（代價 3.5hr）②servo/apply BC 物件活在存檔裡，轉用前 `zone face apply-remove` ③timestep scale 下不可放任自由墜落體（質量放大成破城錘）④剛性約束下成形的顆粒系統，其約束軟化必須退火式漸進（鎖入力庫級聯）** | `process/couple_staged_v2.f3dat`：控制-0 底噪定量→11 階段（cpl_resid 驅動、10×150 ramp+calm、solve ratio-average 1e-4）→每階段輸出：裂縫 DFN dump/wz_outter 反力/mid-band 襯砌力/blue-line vs corner 收斂/裂縫扇區/p(θ,y) map/洞壁位移(G2)。檢查點存 cs_01/06/11。傳遞鏈：`couple_export_bnd_v2.f3dat`（ss_NN→box 邊界帶+洞壁帶匯出）→`make_cpl_resid.py`（Kabsch+應變 gate）→cpl_resid_sNN.txt。裂縫追蹤沿用實跑驗證過的 fracture_track（bond_break→crack_tension/crack_shear DFN）與 couple_qa 函式庫（v2 加 pmap/cwall 匯出） |
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

### 3d. 04 整理定版（07-04 晚，Wade 指示）
- ★ 產出 sav 全部移入 `04/output/`：Large_Initial、Small_Initial、**Couple_Initial（=free2 定版）**、Couple_Initial_v6_confined（備援）。舊 v5/free/v6 三檢查點刪除（~21GB）。
- 重跑路徑同步修補（大小 init 存到 output/；05 兩支 staged 改 process-cwd 慣例：cd process/ 傳裸名）。
- ⚠ 待辦：couple_staged_v2.f3dat 的 restore 路徑（現指 couple_solve/Couple_Initial_free2，檔已移至 output/Couple_Initial）**等本輪跑完再改**（live 中不動檔）。
