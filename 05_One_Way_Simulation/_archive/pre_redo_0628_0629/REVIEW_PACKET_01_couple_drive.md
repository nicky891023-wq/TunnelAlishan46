# REVIEW_PACKET #01 — 05 三尺度依時變形流程 + 耦合驅動 Run B

- **日期**：2026-06-28
- **角色**：Claude = 執行/提案 agent；Codex = 獨立 reviewer
- **狀態**：⏸ **AWAITING CODEX REVIEW** → 請回 `APPROVED` / `APPROVED WITH CONDITIONS` / `BLOCKED`
- **本 packet 要批准的「下一個長運算」**：`couple_drive.f3dat` 的 **SMOKE run**（耦合模 stage-1 驅動驗證）。在 Codex 批准前不啟動。

---

## 1. 研究宗旨與三尺度架構

阿里山林鐵 #46 隧道，地下水升降驅動的依時變形（creep）三尺度數值研究：

| 尺度 | 模型 | 角色（力學機制） |
|---|---|---|
| 大模 | 邊坡尺度 FLAC3D 連續體（4 層、tet） | 地下水升降→邊坡潛移（slope creep） |
| 小模 | 隧道近場 FLAC3D 連續體（6 層共形 + 0.4m 彈性襯砌環） | 地下水升降→圍岩依時收斂變形 |
| 耦合 | 隧道斷面 FLAC3D 圍岩(zone) + **PFC 球襯砌環**（wall-zone 耦合） | 圍岩-襯砌互制細節、襯砌**斷鍵開裂 pattern** |

水位情境：4 階段 **LOW-HIGH-LOW-HIGH（120 天）**。潛變模型 = Burgers-Mohr + MC + Threshold（門檻 0.6，per-stage 評估）。

---

## 2. 進度回報（已完成，供檢核）

### 2.1 小模（隧道收斂）✅
- 配方：burgers-mohr 6 層 + 門檻 0.6 + `zone water density` + 水平水位 z1724/z1807 + per-stage 門檻。
- 結果：4 階段累積 dmax **~3.7mm**；creep-active zone 數 s1=597909 / s2=430462 / **s3=105** / s4=215727（s3 LOW 幾無 creep）。
- 襯砌：保留 **elastic 0.4m 環**（Wade 定）。
- 存檔：`s4_s1..s4.f3sav`（各 1.07GB）。

### 2.2 大模（邊坡潛移）✅
- 破解「走山」：水平水位面在 36% 地形之上→不物理→改 **STL 地形跟隨水位**（`zone water set`）+ `model solve elastic`（Wade 鐵則）+ per-stage 門檻 0.6。
- 結果：4 階段累積 dmax **S1 42.3 / S2 64.1 / S3 66.5 / S4 81.0 cm**，全程有界、空間隨地形變化、高水位段 onset。
- 存檔：`lg_s1..s4.f3sav`（各 0.40GB）。

### 2.3 耦合（襯砌裂縫）🔧 提案中
- **排除**：耦合不能直接跑 creep（PFC dt≈2.5e-6 與 creep dt=600s 落差→不可解算）。Wade 定案：**耦合接收小模每階段位移場當邊界、解力平衡、襯砌 force-share 開裂**。
- 介面已備（見 §4）。本 packet 提議啟動驅動。

---

## 3. 三模型成果檢核框架 + 現有數據

### 3.1 尺度連結（submodeling）
- **小模→耦合**：耦合域 x[1277,1317] y[860,910] z[1728,1768]（隧道中心 ±20m 斷面 × 50m 軸向）是小模的**子域**。抽小模每階段累積 gp 位移（區域內 140694 gp）→ Python KDTree IDW（k=8、1/d²）映射到耦合**外邊界 28304 gp**（`couple_bnd_disp.txt`，gp.id 鍵）。
- **大模↔小模**：大模給區域邊坡潛移背景；小模給隧道近場細節。兩者同一水位情境、同門檻配方。

### 3.2 現有一致性數據
- 耦合 in-situ wz_outter 反力 = **1.88 MN**（Fx -0.22 / Fy 0.41 / Fz **-1.82** MN，覆土主導）。
- 耦合 in-situ **w_inner 反力 = 1.38 MN**（Fz -1.32）→ 襯砌被 wz_outter(岩) + 剛性 w_inner(內) 完全圍束（"no free face"，建模設計）。
- w_860/w_910（端牆）≈ 0 MN（僅邊界、不承載）。
- 球半徑 [0.036, 0.044] m；球數 456302；zone 數 424908。
- **待補**：小模 elastic 襯砌對圍岩的反力（供與耦合 wz_outter 對應檢核）—— Wade 指定的核心一致性檢核，需在小模另抽（提議列入後續步）。

### 3.3 邊界位移量級（IDW 映射結果，已算）
| 階段 | 邊界位移 mag (mm) min / mean / max |
|---|---|
| s1 | 0.046 / 1.509 / 3.909 |
| s2 | 0.060 / 1.513 / 3.489 |
| s3 | 0.062 / 1.513 / 3.491 |
| s4 | 0.051 / 1.543 / 3.523 |

**逐階段增量（實際驅動量）**：insitu→s1 mean **1.51mm**（主導）、s1→s2 mean 0.22mm、s2→s3 mean **0.001mm**、s3→s4 mean 0.04mm。
→ 變形集中在 s1，後階微調，反映小模收斂飽和。（y 端斷面含近洞 gp 故 max 達 3.9mm；x/z 徑向面 ~0.05–1mm。）

---

## 4. 提議的下一步：Run B 耦合驅動（先 SMOKE）

### 4.1 假說（待 Codex 確認可否被結果支持）
驅動耦合**外圍岩盤邊界**到小模每階段位移→圍岩收斂→經 wz_outter 力傳遞給 PFC 襯砌→襯砌在過應力處**斷鍵開裂**。產出：每階段裂縫 pattern（DFN）+ wz_outter 受力 + 內部收斂。一致性：耦合 wz_outter vs 小模襯砌反力應可相互解釋。

### 4.2 方法（依官方範式，非臆測）
依 design workflow（5 agent、查官方 datafiles）綜整，採 **PunchIndentation.f3dat + SleevedTriaxialTest.f3dat** 範式：
1. `model mechanical timestep scale` → **dt=1 精確恆定**（兩個官方耦合例都這樣，使 vel=Δdisp/Ncyc 精確）。
2. **只驅動外圍岩 gp（28304 個），絕不碰球**（lesson #69：直接位移控制襯砌球曾過裂 214k）。襯砌僅經 wz_outter 力響應 = force-sharing。
3. `ball attribute damp 0.8`（Sleeved 值，抑制慣性過衝破鍵）。
4. **sub-step ramp**（Nsub 增量、每 sub-step 後 `model calm`）= SleevedTriaxial rampUp「分增量避免 bonded 載入中破裂」紀律。
5. `zone gridpoint fix velocity range group 'driven'`（必須先 fix 否則 solver 覆寫 gp.vel）→ FISH 設 gp.vel = Δdisp/(Nsub·Ncyc_sub·dt)。
6. solve：圍岩 `model solve ratio-average 1e-4`（注意 PFC 球不在 ratio 內）+ 監看 max ball vel。
7. **w_inner 維持剛性**（Wade 定）。

### 4.3 腳本版本
- `couple_drive.f3dat`（4632 B，已 parse-check 過：`parse_check2.f3dat` → nn=28305 讀檔/string.token 解析正確、所有 FISH define 編譯成功、PARSE-OK）。
- `couple_idw.py`（IDW 映射，已跑）、`couple_bnd_disp.txt`（28304 gp×4 階段目標位移）、`fracture_track.fis`（官方 bond_break→DFN 裂縫追蹤）。

### 4.4 參數與來源
| 參數 | 值 | 來源 |
|---|---|---|
| dt | 1.0（timestep scale）/ 2.52e-6（raw） | recon `couple_recon.log` |
| ball damp | 0.8 | synthesis（SleevedTriaxial line 98） |
| 球半徑 | [0.036,0.044] m | recon |
| 邊界目標位移 | `couple_bnd_disp.txt` | 小模 s4_s1..s4 → Python IDW |
| 門檻/材料 | `parameter.f3dat` | 04 既有 |
| Ncyc sizing | per-cycle move ≤ 1e-3·r_ball=3.6e-5 m | synthesis 準靜態準則 |

### 4.5 控制組（提議）
- **Control-0（零增量驅動）**：驅動邊界到**現位置（Δ=0）**、cycle 同樣步數 → 應得 **~0 新裂縫**。用以隔離「驅動機制本身的假裂」與「真實收斂裂縫」。建議在 smoke 前或併入 smoke 第 0 子步。
- **Baseline**：Couple_Initial 為 0 斷鍵（建模紀錄）。

### 4.6 護欄（over-crack 斷路器）
- 只驅外圍岩、timestep scale、Nsub sub-step + calm、ball damp 0.8。
- **裂縫斷路器**：若單一 sub-step 裂縫增量躍升至「千級」或與 push 同步爆發 → 中止、降 vel / 升 Nsub。
- **w_inner 剛性的幾何擠壓風險**：襯砌被內移岩盤與剛性背擋夾壓，應變 ≈ Δ收斂/襯砌厚 ~ mm/0.4m ~ 0.25% 可能超降伏應變(~0.16%) → 預期會裂；需 Codex 判定是「合理局部開裂」或「shatter」。
- verify-before-long-run：先 SMOKE 不全跑。

### 4.7 SMOKE 計畫（本 packet 要批准的長運算）
- 內容：`[run_stage(1, 3, 100, 1500)]` = stage-1、Nsub=3、Ncyc_sub=100（per-cycle move ≈ 6.5e-6 m << 3.6e-5 護欄）、末 solve cap 1500。
- 監看：每 sub-step 報 cracks + max ball vel；末報 cracks / wz_outter / max ball vel / 內部 dmax。
- 成本：約 1 次 restore(~10min) + ~1800 cycle。先用以**量每 cycle 成本**、驗機制、看裂縫趨勢（漸進 vs avalanche）。
- 產出存 `cb_smoke_s1.f3sav` + log。

---

## 5. 風險與未決（請 Codex 裁定）
1. **w_inner 剛性**（Wade 定）→ 幾何擠壓，是否導致非物理 shatter？閾值？
2. **Shell-only BC**：只驅 6 面外殼，耦合內部自解 BVP，近洞場是「耦合對邊界的響應」非小模內部場（可接受為設計意圖，但需驗證近洞 disp 不嚴重偏離小模映射值；若偏離則加厚驅動帶）。
3. **增量 s1 主導、s2-s4 微小**：4 階段裂縫演化≈ s1 單發 + 微調 → 是否符合「季節性」敘事？（物理上=小模收斂飽和）
4. 小模襯砌反力尚未抽取（一致性檢核的小模側）。

## 6. Visual QA 計畫（每次運算後建立，供 Codex 審）
固定座標/視角/色階/採樣位置，每階段同時提供：
- **absolute field**：耦合斷面（y=885 中段）裂縫 DFN + 圍岩位移場 + 應力場。
- **stage increment**：該階段新增裂縫 + 位移增量。
- **unbalanced force**：圍岩 mech.ratio / 不平衡力場 + max ball vel 歷時。
- **boundary location**：被驅動的 28304 邊界 gp 位置圖 + 施加 vs 達成位移比對。
- 小模 vs 耦合：近洞收斂、wz_outter vs 小模襯砌反力對應。
（不只給最大值/單曲線/自稱合理圖。）

## 7. 請 Codex 確認項目
- [ ] 幾何（耦合域、邊界帶、submodeling 切法）合理
- [ ] 應力路徑（in-situ→驅動→force-share）合理
- [ ] 變形位置（近洞收斂 vs 邊界驅動）合理
- [ ] 破壞區（w_inner 剛性下的裂縫機制）合理或需改 BC
- [ ] 控制組設計足夠
- [ ] 准予啟動 SMOKE（或條件/退回）
