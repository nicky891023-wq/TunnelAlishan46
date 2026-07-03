# 完整數值分析流程 — 阿里山 #46 隧道三尺度地下水依時變形研究

- **版本**：v1（Claude 草擬，送 Codex 共同設計/互相批評）
- **日期**：2026-06-28
- **流程**：Claude 草擬 → Codex 批評 → Claude 改進+回批 → 收斂 → 執行整套 → 全檢核 → 輸出
- **治理**：每階段長運算前 REVIEW_PACKET→Codex 批准；運算後 POST_REVIEW+Visual QA→Codex post-review 才進下一步。

---

## 1. 核心研究目標與假說

**目標**：量化季節性地下水升降如何驅動三尺度依時（creep）變形——(i) 區域邊坡潛移、(ii) 隧道圍岩收斂、(iii) 噴凝土襯砌經圍岩-襯砌 force-sharing 的開裂——並建立三尺度間的力學一致性。

**假說（待數值成果支持/否決）**：地下水位上升(HIGH)→弱/濕層有效應力下降→偏差應力超過門檻→creep onset→(邊坡)順向潛移 /(隧道)收斂→襯砌受載→裂縫；下降(LOW)抑制 creep。4 階段 **LOW-HIGH-LOW-HIGH（120 天）** 揭露季節性累積與襯砌損傷演化。

**判準**：每尺度的變形量級、空間分布、應力路徑、破壞區，需與(a)物理機制自洽、(b)三尺度間互相解釋、(c)現場錨點（若有）半定量相符。

---

## 2. 三尺度架構與各司其職

| 尺度 | 網格/材料 | 水位 | 求解 | 角色與輸出 |
|---|---|---|---|---|
| 大模(邊坡) | Burgers-Mohr 4 層 tet | STL 地形跟隨 z(地形) | `solve elastic`(Wade 鐵則、防走山) | 邊坡潛移位移場/階段 |
| 小模(隧道) | Burgers-Mohr 6 層共形 + 0.4m **彈性**襯砌環 | 水平 z1724/z1807 | ratio-average 1e-5 | 隧道收斂 + 襯砌反力/階段 |
| 耦合(襯砌) | FLAC3D 圍岩 zone + **PFC 鍵結球襯砌環** + wall-zone | (不跑 creep) | 接小模位移場驅動外圍岩、力平衡 | 襯砌裂縫 DFN + wz_outter 受力/階段 |

**尺度連結**：耦合域 x[1277,1317] y[860,910] z[1728,1768] 是小模子域（submodeling）。小模每階段累積位移→IDW→耦合外邊界 28304 gp。

---

## 3. 已驗證配方（這幾天測試）

1. **門檻 creep**：per-stage 評估（每水位階段一次、固定 active set）+ `zone water density [rho_w]` + 門檻 0.6 + `SetKStrains` 在(應力定案後)與(每次換水後)。**per-increment 翻 eta 會發散**（已排除）。
2. **大模水位**：STL 地形跟隨（`geometry import` + `zone water set`）；水平面在 36% 地形之上→不物理→走山（已排除）。
3. **大模求解**：`model solve elastic`（裸、非 only）——`only` 留人為高 cohesion 會毒害下游讀強度的程式（教訓 #76）。
4. **耦合驅動**：`model mechanical timestep scale`(dt=1) + 只驅外圍岩 gp(不碰球) + `ball attribute damp 0.8` + sub-step ramp+`model calm` + `zone gridpoint fix velocity`(先 fix 再設 gp.vel) + `fracture_track.fis`(zmax 已修)。依官方 PunchIndentation/SleevedTriaxial 範式。
5. **參數**：`04_InitialBalance/parameter.f3dat`（E/c/φ/den 分層、eta_m=6e15、eta_k=2.4e13、crp_dt=600、rho_w=1000、襯砌 shot_E=25e9/fc=41.2e6/ft=4.12e6）。

---

## 4. 教訓/gotcha（必避）

- **FISH**：(a) `fish define` 前必須先有 model(new/restore)，否則函式被當變數靜默失效(#78)；(b) define 內不可 `[func]`/bare-call，要 `string(func)` 表達式呼叫且函式設回傳值(#74)；(c) 函式參數在 model 存在後 OK；(d) 讀檔 `file.read`+`string.token`；(e) `gp.vel` 須先 `fix velocity` 否則被 solver 覆寫；(f) gp.fix/vel 在 local 系，須確認 global frame。
- **Couple_Initial 殘餘不平衡 ratio=6.0954e-03**（非 1e-4、撞 cycle cap、couple_servo_v5.log:604）→ 驅動前可能自帶假裂。**處理待定**（見 §8）。
- **fracture_track.fis zmax bug**（zmin 設兩次、zmax 未設→裂縫永遠 0）→ **已修** `global zmax = domain.max.z()`。
- **w_inner 剛性內牆承 1.38MN**（襯砌無自由面）→ Wade 定保留→ 視為 sensitivity 非 validation。
- **多版數據用最新**（mtime）。

---

## 5. 完整流程（逐步、含檢核閘）

### Stage A — 三尺度初始平衡 ✅(已完成，但耦合殘餘待處理)
- Large_Initial / Small_Initial / Couple_Initial 已建。
- **A-issue**：Couple_Initial ratio 6.1e-3。**提議**：先 `model solve ratio-average 1e-4`（必要時加 ball settle）重平衡存 Couple_Initial_eq，作為驅動基準（消除假裂源）。← 待 Codex 批。

### Stage B — 大模邊坡潛移 ✅(已完成)
- `large_creep_4stage.f3dat`：4 階段 LOW-HIGH-LOW-HIGH、STL 水、solve elastic、門檻 0.6。
- 結果 dmax S1 42.3/S2 64.1/S3 66.5/S4 81.0 cm（lg_s1..s4）。
- **B-QA(補)**：需建 Visual QA Pack（固定座標/色階、absolute+increment+unbalanced+邊界）。

### Stage C — 小模隧道收斂 ✅(已完成)
- `small_4stage_standalone.f3dat`：6 層、彈性襯砌、門檻 0.6。
- 結果 收斂 ~3.7mm（s4_s1..s4）。
- **C-補**：抽小模**襯砌對圍岩反力**/階段（一致性檢核小模側，尚未做）+ Visual QA Pack。

### Stage D — 耦合襯砌開裂（核心交付、進行中）
- D0 介面 ✅：抽小模 bc(140694gp×4)→Run A 耦合邊界(28304gp)→Python IDW→`couple_bnd_disp.txt`。
- **D1 控制組（Codex 條件）**：restore(Couple_Initial_eq)+datum reset+baseline 斷鍵+track_init+load_targets+fix driven → **零增量驅動**(target=0、同 cycle/solve)→報 新裂縫/wz/maxbvel/ratio。**Gate**：新裂縫 ≤ 門檻 才續；否則殘餘問題、回 §8。
- **D2 SMOKE stage-1**：`run_stage(1,Nsub=3,Ncyc=100,solve 1500)`；報 裂縫(ball-ball 分 tension/shear)/wz/maxbvel/內部收斂/**target-application audit**(driven gp 達標誤差)。
- **D3 全 4 階段**：批准後逐階段 LOW-HIGH-LOW-HIGH，每階段存檔+Visual QA+裂縫累積。
- 護欄：裂縫斷路器（單階躍升千級或與 push 同步爆→中止降速/升 Nsub）。

### Stage E — 三尺度一致性檢核
- E1 小↔耦合襯砌反力：小模襯砌反力 vs 耦合 wz_outter（每階段、向量+量級，可相互解釋、落差有界）。
- E2 耦合近洞收斂 vs 小模收斂（同階段、同位置）。
- E3 大↔小：大模在小模域邊界的位移趨勢 vs 小模邊界條件一致性。

### Stage F — Visual QA + 驗證 + 輸出
- 每模型每階段 Visual QA Pack（§6 規格）。
- 最終輸出：三尺度成果圖集 + 一致性檢核表 + 機制論證 + （pptx/報告）。

---

## 6. 驗證框架（Visual QA 規格，Codex 審查用）

每次運算後固定**座標/視角/色階/採樣位置**，每階段**同時**提供：
1. **absolute field**：位移場 + 應力場（斷面 y=885 中段 + 3D）。
2. **stage increment**：該階段新增變形/裂縫。
3. **unbalanced force**：mech.ratio 歷時 + 不平衡力場（+耦合 max ball vel）。
4. **boundary location**：被驅動/受約束的邊界位置 + 施加 vs 達成位移比對。
- **禁**：只給最大值/單曲線/自稱合理圖。
- 三尺度比較圖共用色階與採樣位置。

---

## 7. 控制組與護欄

- **C-ctrl-0**：耦合零增量驅動→應 ~0 新裂縫（隔離殘餘假裂）。
- **C-baseline**：track_init 前的既存斷鍵數（應 ~0）。
- **C-audit**：driven gp 達 stage target 誤差（容差內）。
- **C-crack-split**：裂縫分 ball-ball(襯砌鍵) vs wall-ball(摩擦、應無斷鍵) + tension/shear。
- **護欄**：裂縫斷路器、verify-before-long-run、長跑 watchdog（CPU 前進+產出）。

---

## 8. 待 Codex 共同裁定的開放決策

1. **Couple_Initial 殘餘 6.1e-3**：(A) 先重平衡到 1e-4 再驅動（推薦、消假裂源）/(B) 接受+靠零增量控制組監測。Claude 傾向 A。
2. **w_inner 剛性**（Wade 定）：作 sensitivity；是否需並跑「移除 w_inner 自由襯砌」對照組以界定剛性的影響上下界？
3. **增量 s1 主導、s2-s4 微小**（小模收斂飽和）：4 階段裂縫演化≈s1 單發+微調，是否符合季節敘事？或需檢視小模 4 階段是否真實反映水位循環（s3 active=105 是否過低）？
4. **小模襯砌反力抽取法**：彈性襯砌環對圍岩的反力如何定義/抽取以對應耦合 wz_outter？

---

## 9. 交付清單

- [ ] 三尺度 4 階段成果（位移/應力/裂縫）含 Visual QA Pack
- [ ] 三尺度一致性檢核表（E1/E2/E3）
- [ ] 核心機制論證（水位→有效應力→creep→變形→襯砌裂縫）
- [ ] 控制組與護欄紀錄
- [ ] 最終報告/簡報
