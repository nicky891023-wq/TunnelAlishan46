# REDO SYNC — 力平衡重做後的現況同步（Claude→Codex）

日期 2026-07-01。Wade 指示：把「力平衡重做」這一輪的**現況**完整同步給 Codex，讓 Codex 是對**現在**的模型審查，不是 6/28–6/29 那批舊的 couple_drive Phase-2 資訊（那些 CODEX_*_REVIEW / *_PACKET 全部 stale，發生在本輪重做之前）。

---

## A. 為什麼重做（本輪起因）
Wade 檢核 04 初始狀態後判定**先前的力平衡做錯**（量級/邊界驅動不對），下令：回到 initial、從**大模往下**慢慢重做（討論→修正→重跑），逐尺度交付三個「initial」力平衡供檢核。**鐵則不變**：本構維持 Burgers-Mohr；換模型或降參湊量級=作弊；量級不對要當數值設定問題耐心處理，不可作弊。

## B. 三尺度現況（重做後）
- **大模（邊坡）**：4 階段水位+threshold creep，產出區域應力/位移場（endmember，已知過驅動；每階段 box 邊界位移 `lg_bc_s1–4.txt`）。**未改動**。
- **小模（隧道 submodel，6 盒面 fix）**：本輪**重做重點**。
  - **兩段式 in-situ**（`small_insitu_2stage.f3dat` → `04/Small_Initial`）：
    1. 裸岩（襯砌 null、無殼）+ 大模應力 IDW + BC → `solve ratio-local 1e-4`（開挖鬆弛，塑性區長全）；
    2. 在鬆弛後的洞壁上 `structure shell create by-face`（D 形貼附襯砌，position-range 跟隨彎曲隧道，全覆蓋含兩洞口 y850.05–949.95，69828 shells）→ `solve ratio-local 1e-5`。
  - 成果：塑性區 38.7%（**經 Wade GUI 校正：100% 剪力破壞、非拉力**；state bit 修正 shear=&5, tension=&10）；殼裝在鬆弛態上僅 0.18MPa（**無 wished-in-place 過應力**）；day-0 in-situ 收斂保留（datum 非零、Wade 鐵則）。
  - 拉力塑性抑制：每層 tension 設 MC 頂點 c/tanφ（取代舊 0.1MPa 均一低值）。
- **耦合模（結構）**：**尚未做本輪 initial**（couple_bnd_disp 需由小模新的 sd_s1–4 位移場重新產出）。這是下一步。

## C. 潛變參數調校（本輪核心數值工作）
`do_threshold`：`q_th = threhold·(c·cosφ + p'·sinφ)`，`q≥q_th` 才開 creep（高門檻→少 creep）。effective p' 含孔隙水壓 → 高水位降 p' → 降 q_th → 多 creep（水位敏感的機制根源）。
- eta_m 掃描（eta_k=2.4e13 固定、threhold=0.6 全階段）：
  - **6e15**：too slow（~4mm creep，門檻飢餓）。
  - **1e14**：HIGH 水位 STAGE2 **發散**（dmax 跳 244mm，vclose 反號）。
  - **1e15**（採用）：四階段全受控、無發散。**Wade 判斷驗證成立**——先前力平衡做錯才使 creep 不回應 eta；修對後 creep 對 eta 有反應。

## D. 交付結果：eta=1e15 四階段依時模擬（`small_driven.f3dat`，圖 `qa_convergence_history.png`）
洞周 y860–910 哨兵斷面 y885 的**對向監測點對淨空收斂**（負=內收）；dmax=全 box 最大位移（含邊界被大模驅動點，故 > 收斂）：

| 階段 | 水位 | 天 | vclose 頂↔仰 | hclose 左↔右側牆 | dmax | Δdmax | active(creep) |
|---|---|---|---|---|---|---|---|
| in-situ | — | 0 | −13.97 | −10.99 | 22.2mm | — | 0 |
| S1 | 低 z1724 | 30 | −14.99 | −13.96 | 24.5mm | +2.3 | 21.7萬 |
| S2 | **高 z1807** | 60 | −15.06 | −16.27 | 34.9mm | **+10.4** | 79.2萬 |
| S3 | 低 z1724 | 90 | −15.05 | −16.29 | 34.96mm | +0.06 | 11（凍結）|
| S4 | **高 z1807** | 120 | −15.00 | −17.01 | 35.17mm | +0.21 | 14萬 |

- **物理站得住**：(1) 水位敏感（高快低慢，S3 凍結 vs S2 +10.4mm）；(2) 非瞬跳主導（S2 day35 衝 36.5→day40 收斂回 34.3 再緩增）；(3) 首輪吃損傷、次輪 shakedown（S2 +10.4 vs S4 +0.21）。
- 最終收斂 ≈ 垂直 15mm / 水平 17mm，box 最大變形 ≈ 35mm；落在淺埋低應力（0.3–1.7MPa、~100–200m 覆蓋）輕微擠壓段的合理範圍。Wade 已**接受量級**、要求微調。
- **殼**：shellMaxT 升到 22MPa（噴凝土抗拉 4.12MPa 的 5 倍）、記錄型張裂 0→3657。**小模殼是共節點連續體、力控無法反映真實開裂**，故僅 record-only 記錄裂縫熱點——真正襯砌受力/裂縫型態**必須靠耦合 PFC 鍵結襯砌模型**。

## E. 下一步（Wade 已定調，供 Codex 審）
1. **各階段 threshold 微調**（Wade 新指示，**不重作力平衡**）：threhold 改逐階段 = **S1 0.6 / S2 0.4 / S3 0.4 / S4 0.2或0.3**。方向＝逐階段降門檻→逐階段更易 creep→模擬長期漸進弱化，使後段不再 plateau（現況 S3 凍結、S4 shakedown）而持續累積。實作＝在四個 `drive_and_creep` 呼叫前各設 `[global threhold=X]`，改動 4 行、不動 Small_Initial/drive/eta。
2. **耦合 initial**：圍岩統一單一彈性、取小模 sd_s1–4 各階段位移場 → `couple_idw.py`（含扣全剛體 residual）→ `couple_bnd_disp.txt` → Control-0 gate（沿用 Codex P2 準則：Δcrack=0、drift<0.05mm、力漂<2%）→ 各階段襯砌受力+裂縫。

## F. 想請 Codex 裁決/檢查
1. **eta=1e15 四階段結果的正確性**：量級（收斂 15–17mm、dmax 35mm）+ 水位敏感 + shakedown，物理與數值上是否成立？有無被忽略的紅旗（如 shellMaxT 22MPa 記錄型過應力是否影響 rock 場的可信度）？
2. **逐階段 threshold 方案**：0.6/0.4/0.4/0.2~0.3 的漸進降門檻，作為「長期漸進弱化」代理是否合理？S4 取 0.2 vs 0.3 的取捨（0.2 更多變形但更靠近發散帶、eta 不變）？有無發散風險需預設 abort 準則？
3. **收斂指標**：目前用哨兵斷面 y885 單點對淨空收斂 + y860–910 band 平均（band_vert −13.47 與單斷面 vclose −15 一致）。作為交付指標是否足夠、或需沿隧道軸向剖面/展開圖？
4. **耦合驅動**：小模→耦合的位移傳遞（扣全剛體 residual、速度邊界）沿用舊 couple_drive 架構是否仍適用於新的 sd_s1–4？Control-0 準則是否沿用 P2 那版？
