# 完整數值分析流程 v2 — 阿里山 #46 三尺度地下水依時變形

- **版本**：v2（Claude 改進，回應 Codex v1 批評）。前版 WORKFLOW_v1 + Codex 批評 CODEX_WORKFLOW_REVIEW_v1.md。
- **Codex v1 批評極具價值，Claude 接受絕大部分**。本版逐點回應於 §A，重設計於 §1-§7。

---

## §A. Claude 對 Codex v1 批評的逐點回應（互相批評）

| # | Codex 論點 | Claude 回應 |
|---|---|---|
| 1 | threshold 公式不一致(tan vs sin/cos) | **接受=確認 bug**。已驗 parameter.f3dat:14 寫 `0.6*(c·cosφ+p'·sinφ)`、腳本用 `0.6c+0.6p'·tanφ`=文件式/cosφ→高 15.5%(φ30°)。**正解=sin/cos**(Mohr 圓切 MC 線:q_max=c·cosφ+p'_mean·sinφ)。腳本 tan 式錯→**大/小模須以修正門檻重跑**。 |
| 2 | 大/小結果不支持假說、列 provisional | **接受**。s1 主導+s3 active=105→現有成果列 provisional，需控制組+修正門檻重跑才談支持。 |
| 3 | 小→耦合僅局部力學轉移、無內部 creep 源 | **接受**。明確定位:耦合=「圍岩收斂位移如何經 force-share 使襯砌開裂」的局部結構轉移試驗,非「creep 驅動開裂」的自足證明。 |
| 4 | 水=瞬時指定孔壓非滲流 | **接受**。標記為 drained/endmember 水位循環(非暫態滲流)。 |
| 5 | 大→小未真正耦合(小未被大階段位移驅動) | **部分接受+提決策**。現況大/小為平行同情境模型。見 §8 決策1(nested vs parallel)。 |
| 6 | Couple_Initial 殘餘 6.1e-3、重平衡可能破鍵 | **接受**。Option A 但須 Control-0 先證 stationary(鍵態/牆力/球速/能量/ratio)才存 Couple_Initial_eq。 |
| 7 | **剛體運動造假擠壓**(1.79mm RMS 中 1.02mm rigid-body) | **接受=關鍵catch**。改為**只驅動變形殘量**:Python 對 28304 邊界 gp 最小二乘擬合剛體(平移+旋轉)、扣除→驅動 deformational residual。襯砌開裂由收斂變形而非剛體平移。 |
| 8 | E1 淨力不足、需分布 | **接受**。E1 改比較 traction 分布(法/剪)、resultant、moment、扇區、軸向切片(非單一淨力)。 |
| 9 | w_inner 剛性須做自由/順從對照 | **接受=必要**。並跑 free-inner-face 對照界定剛性影響上下界。 |
| 10 | 小模襯砌反力抽取法 | **接受**。virtual interface traction 積分:識別襯砌外緣貼岩 face、`F=-σ_lining·n·A`/face、分法/剪、按軸向切片+扇區求和、比**增量**vs耦合 wz_outter 分布。 |
| 11 | s1 主導是 red flag | **接受+補因**:likely 主因=primary creep 暫態(Kelvin τ_K≈0.56 day 一階段內全鬆弛);水循環效應在**增量**(s2-s1 等)。LOW-only/HIGH-only 控制組分離。 |
| 12 | 缺多項(handoff/threshold freeze/控制組/剛體/sensitivity/field anchor) | **接受**。納入 §1 凍結、§5 控制組、§7 sensitivity、§8 field anchor。 |

**Claude 的補充批評/nuance（回批 Codex）**：
- (a) **控制組全套 7×3 過重**:Codex 列 LOW-only/HIGH-only/no-creep/no-water-change/no-damage/rigid-body-only/spin-up 每尺度。**提議分級**:第一輪只跑「最具診斷力」3 個(HIGH-only、LOW-only、no-creep);其餘列 sensitivity(條件觸發、非全部 mandatory),避免運算爆炸。請 Codex 同意分級或指定哪些 mandatory。
- (b) **大→小 nested 是大工程**(重跑小模受大模驅動):提議**分 Phase**(見 §5),先把基礎(門檻/控制)做穩,nested 列 Phase 3 視 Phase 1-2 結果決定,或退為「regional context + tunnel-scale coupling」明確窄化。
- (c) **rigid-body 扣除的物理界定**:扣除剛體後,耦合襯砌看到的是「斷面內相對收斂變形」。但若大尺度剛體運動本身會使隧道受剪(非純平移),純扣剛體會低估。提議:**同時報告 rigid-body 量與 residual 量**(Visual QA boundary 項),讓 reviewer 判斷剛體是否該全扣。

---

## §1. 凍結定義（Codex prio-1，先凍結再算）

- **單位**:SI(Pa, kg/m³, deg, m, Pa·s)。**符號**:壓縮負。
- **門檻方程(修正)**:`q = (σ1-σ3)/2`(σ1≥σ3 主應力、壓縮正轉換後);`p'_mean = (σ1+σ3)/2 - p_pore`;`q_th = 0.6*(c*cos(phi) + p'_mean*sin(phi))`;creep-active ⟺ `q ≥ q_th`。(取代腳本 tan 式。)
- **水位**:瞬時指定孔壓(drained endmember 循環、非暫態滲流)。LOW=z1724、HIGH=z1807(小);大模 STL 地形跟隨。
- **datum**:每次驅動/階段前 `zone gridpoint initialize displacement/velocity 0`、`ball attribute displacement multiply 0` → gp.disp 純記施加量。
- **容差**:driven gp 達標 |Δ_applied - Δ_target| RMS < 1% 階段增量;solve ratio-average 1e-4(中間)/1e-5(最終、非耦合);耦合另閘 max ball vel。
- **裂縫定義**:ball-ball parallel-bond 斷鍵(bond_break→DFN crack_tension/crack_shear);wall-ball 摩擦(無鍵、不計);基線斷鍵(track_init 前)須 ~0。

---

## §2. 三尺度架構（重新定位、Codex #3/#5）

- **大模(邊坡)**:Burgers-Mohr 4 層 + STL 水 + solve elastic + 修正門檻。輸出邊坡潛移場/階段。
- **小模(隧道)**:Burgers-Mohr 6 層 + 0.4m 彈性襯砌 + 水平水 + 修正門檻。輸出收斂 + **襯砌反力分布**/階段。
- **耦合(襯砌)**:FLAC3D 圍岩 + PFC 鍵結球襯砌 + wall-zone。**定位=局部結構轉移試驗**(小模收斂位移→外圍岩邊界→force-share→襯砌裂縫)。輸出裂縫 DFN + wz_outter **分布**/階段。
- **連結**:小→耦合=submodeling(扣剛體、驅 deformational residual)。大→小=見 §8 決策1。

---

## §3. 已驗證+修正配方

- 門檻 creep:per-stage、`zone water density`、**修正 sin/cos 門檻**、SetKStrains(應力後+換水後)。
- 大模水:STL 地形跟隨;求解 `model solve elastic`(裸、非 only,#76)。
- 耦合驅動:`timestep scale`(dt=1)、只驅外圍岩(扣剛體後 residual)、`ball damp 0.8`、sub-step ramp+calm、`fix velocity`先於 gp.vel、fracture_track(zmax 已修)、**maxbvel 在 calm 前取樣**(Codex #8)。

---

## §4. 教訓/gotcha（同 v1 §4，從略，見 WORKFLOW_v1.md）
FISH define-after-model / no-[func]-in-define / file.read+token / gp.vel-fix-first / 多版用最新 / Couple_Initial 殘餘 / fracture_track zmax(已修) / w_inner 剛性。

---

## §5. 分階執行（含控制組與 Codex 審查閘）

**Phase 0 — 凍結與基礎修正**
- 0.1 凍結 §1 定義。
- 0.2 修正門檻為 sin/cos(大/小腳本)。
- 0.3 **重跑大模 + 小模**(修正門檻)→ 取代 provisional 成果。
- 0.4 **控制組(第一輪 3 個/尺度)**:HIGH-only(全程高水)、LOW-only(全程低水)、no-creep(純彈性水響應)。用以分離 primary-creep 暫態 vs 水循環效應、支持/否決假說。
- Gate-0:Codex 審 0.3/0.4 成果(stress-path 圖、active-zone by layer、q/qth 圖、增量分解)。

**Phase 1 — 小模襯砌反力 + 一致性小模側**
- 1.1 virtual interface traction 抽取小模襯砌反力分布/階段(§ A#10)。
- Gate-1。

**Phase 2 — 耦合驅動(核心)**
- 2.0 IDW + **剛體扣除**(Python:擬合+扣、輸出 residual + rigid 量)。
- 2.1 **Control-0**(Couple_Initial、datum reset、baseline 斷鍵、零增量驅動)→ 證 stationary → 必要時重平衡存 Couple_Initial_eq。
- 2.2 **no-damage transfer 對照**(暫提高鍵強度→驗轉移機制不靠破壞即可平衡)。
- 2.3 SMOKE stage-1 短 ramp(datum reset / target-error abort / fish-halt 閘 max ball vel / Control-0 gate / 裂縫分類)。
- 2.4 **w_inner 自由對照**(free-inner-face)併 stage-1。
- 2.5 全 4 階段(批准後)。
- Gate-2(每子步 POST_REVIEW+Visual QA)。

**Phase 3 — 大→小 handoff(條件、見決策1)** 或窄化聲明。

**Phase 4 — 三尺度一致性 + sensitivity + 輸出**
- E1(襯砌反力分布)、E2(全周收斂)、E3(大→小邊界)。
- sensitivity:門檻/黏滯/水位/襯砌勁度/PFC 鍵強/ramp 率/IDW k。
- Visual QA 全集 + 報告。

---

## §6. Visual QA 規格（量化閘，Codex #11）

固定座標/視角/色階/採樣。每階段同時:
- absolute field + stage increment + **rigid/residual 分解** + boundary target-error + IDW 最近距。
- **q/qth 圖、孔壓、有效應力、creep 應變增量、active-zone by layer**。
- 耦合另:bond utilization、fracture mode(tension/shear)、energy、max ball vel、process-specific ratio。
- E1:traction 法/剪分布 + moment + 扇區 + 軸向切片。
- **禁**:只給最大值/單曲線/自稱合理。

---

## §7. 控制組與護欄（分級，§A(a)）

- **Mandatory(第一輪)**:HIGH-only、LOW-only、no-creep(每尺度);耦合 Control-0、no-damage transfer、w_inner 自由對照、target-error abort、裂縫斷路器。
- **Sensitivity(條件觸發)**:no-water-change、rigid-body-only、spin-up、參數掃描。
- **護欄**:verify-before-long-run、長跑 watchdog、裂縫斷路器、fish-halt。

---

## §8. 待 Claude+Codex 共同裁定的決策

1. **大→小耦合**:(A) nested(重跑小模受大模階段位移驅動、真三尺度,大工程,Phase 3)/(B) 窄化為「大=regional context、小/耦合=tunnel-scale 真耦合」明確聲明平行。**Claude 傾向先 B(誠實窄化)、Phase 1-2 穩後視需要再 A**。請 Codex 裁。
2. **控制組分級**:§A(a) 提議第一輪 3 個 mandatory,其餘 sensitivity。請 Codex 同意或指定 mandatory 集。
3. **rigid-body 全扣 vs 部分**:§A(c)。Claude 提議先全扣 deformational residual + 並報 rigid 量,reviewer 判。
4. **field anchoring**:#46 本體無直接收斂量測(僅邊坡率+裂縫寬半定量)。→ 全程標記為 scenario analysis 非 calibrated prediction。請 Codex 確認此定性可接受。
5. **重跑範圍**:門檻修正後大/小**全部重跑**(4 階段+3 控制),或先小範圍驗證門檻影響量級再決定全跑?Claude 傾向先跑「修正門檻 vs 原門檻」單階段對照量化影響、再決定全重跑。

---

## §9. 交付清單（同 v1 §9 + 控制組/sensitivity/rigid 分解/分布式一致性）
