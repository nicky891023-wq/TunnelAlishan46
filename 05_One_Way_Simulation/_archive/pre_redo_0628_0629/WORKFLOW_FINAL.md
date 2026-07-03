# 阿里山 #46 隧道 — 完整三尺度數值模擬流程（FINAL，Claude↔Codex 收斂版）

日期 2026-06-29。經 Claude（執行+提案）↔ Codex（獨立審查）五輪協商 + Phase 0-2 執行驗證後的最終定稿。
治理：任何模型修改/長運算/方向變更前提交 REVIEW_PACKET 停等 Codex（APPROVED / WITH CONDITIONS / BLOCKED）；執行後 POST_REVIEW；每次運算後建 Visual QA Pack。

---

## I. 研究核心目標 + 三尺度角色（Wade 定義）

**核心**：地下水位升降 + 依時變形（threshold creep）起閉機制下，阿里山 #46 隧道襯砌的受力與裂縫 pattern、圍岩互制。

| 尺度 | 範圍 | 模擬什麼 | 不做 |
|---|---|---|---|
| **大模** | 邊坡尺度（區域） | 水位升降 + creep 起閉下整個區域的**應力場、位移場**（endmember） | — |
| **小模** | 隧道尺度（submodel） | 隧道圍岩的**應力場、位移場**（每階段） | — |
| **耦合模** | 結構尺度 | 汲取小模各階段位移當外力 → **襯砌受力、裂縫 pattern + 圍岩互制** | **不做水流、不做 creep** |

資訊單向下傳：大模 → 小模（應力場 IDW 映射）→ 耦合模（位移場速度邊界驅動）。

---

## II. 完整流程（Phase 0-4）

### Phase 0：定義凍結 + 大/小模重跑 + 控制組（✅ 完成、Gate-0 PASS WITH CONDITIONS）
- **凍結 threshold creep 公式**：`q_th = 0.6·(c·cosφ + p'_mean·sinφ)`（修正前誤用 tan 式、高 15.5%）。
- **per-stage 評估**：`zone water density [rho_w]`、threshold 0.6、SetKStrains 在應力後 + 每次水位變動後。
- **重跑 8 run**：大/小 × {baseline, HIGH-water, LOW-water, no-creep}。
- **成果**：小模 mm 級強力支持假說（水位調制 creep-active set、creep 集中 layer4 濕弱砂頁岩）；大模過驅動（接受為 regional-context endmember、機制正確）。

### Phase 1：小模襯砌反力 + 收斂（✅ 收斂量完成）
- 隧道壁參考點（crown/spring/invert）radial inward ≈ 0.22mm（s4_s1），遠小於 global dmax 3.22mm → 確認襯砌剛、global dmax ≠ 隧道收斂。
- **小模 lining 結構議題**：小模「lining」= wished-in-place plug（與圍岩共節點、無空洞/界面、初始應力已超噴凝強度）→ **小模給位移/應力場 OK、但真實襯砌力/裂縫必須來自耦合 PFC**（Codex 裁定）。
- E1 一致性（小模虛擬切面反力 vs 耦合）延後（wz_outter 馬蹄形非圓柱、需重抽面幾何）。

### Phase 2：耦合驅動（🔴 執行中 = 核心交付）
**流程**：
1. restore Couple_Initial（PFC 襯砌 + zone 圍岩 + wz_outter wall-zone 耦合）。
2. **dt=1**：`model mechanical timestep scale`（官方 PunchIndentation 佐證 PFC 時步→1）。
3. 讀小模各階段位移 → **IDW 映射**到耦合外盒邊界 gp（k=8、1/d²）。
4. **扣全剛體**（best-fit 平移+旋轉）、只驅動 **deformational residual**（剛體佔 53-60%、不扣有假擠壓）。
5. **BC**（Codex 定 Option C + B'）：外盒邊界 23530 gp、**排除近隧道 y 端蓋 r<6m gp**、y 端蓋驅徑向 uy=0。
6. **驅動**：ball damp 0.8、`zone gridpoint fix velocity` 先於 gp.vel、30×10 sub-step ramp + model calm、datum reset。
7. **Gate（依序）**：Control-0（零增量、測 in-situ 不自帶假裂）→ pre-drive guard（每跑前零增量驗 stationary）→ 全 stage-1 → 累積 s2-4。
8. **裂縫追蹤**：fracture_track.fis（bond_break callback、entries(2)=mode {1=tension,2=shear}）→ crack_tension/crack_shear DFN。
9. **交付區 = 中段 y870-900**；端帶（y<870/>900）= y 端蓋 kinematic 強加 boundary artifact、**counted but EXCLUDED from interpretation**。
10. **w_inner**：rigid（Wade 主案）+ free（mandatory sensitivity）兩案、界定剛性上下界。

### Phase 4：三尺度一致性 + Visual QA 全輸出（待）
- 三尺度應力/位移場連貫性檢核。
- 門檻/cohesion 敏感度（design-level claim 前必做）。
- 固定座標/視角/色階的比較圖：absolute field + stage increment + unbalanced force + boundary location。

---

## III. 耦合模執行細節（本輪定稿）

- **驅動點**：23530 外盒 gp（x±19.5/y[860.5,909.5]/z±19.5、排除 r<6m y 端蓋）。
- **速度 sizing**：gp.vel = (gp.extra(.,stg) − gp.disp)/(substeps_left × ncyc × dt)，dt=1 → velocity ~1.3e-5 m/s（準靜態、比官方 punch 0.0001 更緩）。
- **斷路器**：中段 dmid>50/substep 或 n_mid>300 → 停（abort_flag、存 _BREAK 名不誤標）。
- **adaptive solve**：ratio-average 1e-4 cap 3000、非穩態則延長（Control-0 需 4372 cycle 達 1e-4）。
- **襯砌微觀（D7 FINAL_CALIB）**：linearpbond、pb_ten=2.1 MPa（抗拉弱、tension 主導破壞）、pb_coh=23 MPa、pb_emod=5.88 GPa；耦合接觸 pb_ten≥1e10 不可破。
- **中段反力抽取**：pb_ten≥1e10 耦合接觸（中段 47806 個）積分 normal force（signed sum + abs sum）。
- **中段收斂**：中段襯砌球徑向 inward 位移（mean/max）= 載荷第二證明。

---

## IV. 治理 + Gate（Claude↔Codex）

- Claude = 執行+提案 agent；Codex = 獨立 reviewer（gpt-5.5 xhigh）。
- 每階段：REVIEW_PACKET → 停 → Codex 裁決 → 執行 → POST_REVIEW。
- 已過 gate：CONTROL0-VERDICT、SMOKE-DIAG-VERDICT、SMOKE-PROD-VERDICT、SMOKE-BP-VERDICT（皆 APPROVED WITH CONDITIONS）。
- **Workflow 對抗審查**（18-agent）= 額外正確性防線（抓到 crack-track CRITICAL bug）。

---

## V. Visual QA Pack（每次運算後）

- 裂縫 pattern：3D 散點（tension紅/shear藍）+ y 切片 + sector 直方圖（固定色階/視角）。
- 牆力：wz_outter total（端污染註明）+ 中段 mid_wall_force。
- 收斂：中段襯砌球徑向位移。
- 端帶分開報、明確標 boundary-affected。
- 禁止只給最大值/單曲線/自稱合理。

---

## VI. 驗證分層（誠實）

- ✅ **已驗**：threshold 公式（對文件）、dt=1（官方範例+實測）、剛體扣除（residual<total）、crack-track（對 PFC 文件）、中段 stage-1 0 裂（A+B' 逐 substep 一致）。
- 🔬 **執行中**：中段 s2-4 累積裂縫/力/收斂。
- ⏳ **待**：E1 三尺度一致性、門檻敏感度、free w_inner、Phase 4 全 QA。
- ⚠️ **已知限制**：大模過驅動（endmember）；耦合 y 端 boundary artifact（排除中段外）；小模 lining=plug（不提供薄襯砌力）。

---

## VII. 當前狀態（2026-06-29）

- 最終全 4 階段生產執行中（rigid w_inner、累積 s1-4、~8-16hr）。
- 核心結果已立：**中段隧道襯砌 stage-1 載荷下 0 裂、穩健**（兩獨立跑一致）。
- 下一步：4 階段完 → QA → POST_REVIEW → free w_inner 敏感度 → Phase 4。
