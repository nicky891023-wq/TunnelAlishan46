# 小模/耦合模 數值方法架構提案（討論稿）

日期：2026-07-02。狀態：**討論稿，等 Wade 裁示 D1–D7 後定版**。
本文所有 FLAC3D/PFC 技術主張均經官方手冊逐條查證（FLAC3D 6.00 chm + PFC 6.0 chm + 官方範例），引用以〔〕標示。掛載 skill：flac3d-600、pfc-itasca。

---

## 1. 機制與職責分工（總架構）

研究機制鏈：**地下水位升降 → 有效應力/門檻啟閉 → 圍岩依時變形 → 襯砌受力/開裂**。

| 模型 | 職責 | 網格 | 本構 | 時間 | 水 |
|---|---|---|---|---|---|
| 大模（坡地） | 區域有效應力場+坡地潛移，產生驅動 | tet 分層 | Burgers-Mohr+門檻 | creep 真時間 | 水位面 STL、穩態流 |
| 小模（隧道） | 隧道**擠壓**：精確地質分層下的依時收斂 | tet 共形 6 層 | Burgers-Mohr+門檻 | creep 真時間 | 水位+洞周洩降 |
| 耦合模（支撐） | 圍岩-襯砌**互制**：襯砌外力/內力/裂縫/反力 | hex O-grid + PFC 球 | 圍岩=等效彈性（D2）；襯砌=linearpbond BPM | **無 creep**（階段準靜態） | 不進水（效應由驅動攜帶） |

時間依存性**只在大模與小模**發生；耦合模是「每階段的準靜態載重傳遞與破壞解析裝置」，水位與潛變的效應全部由小模的階段位移場攜帶進來。這與「耦合模不跑 creep（timestep 落差）」的既定方向一致——官方耦合例 PunchIndentation 也正是純準靜態staged loading〔datafiles\ExampleApplications\PunchIndentation\PunchIndentation.f3dat〕。

```
大模 staged creep ──位移場(單向)──▶ 小模 driven creep ──階段位移場(單向)──▶ 耦合模 staged 準靜態
                                          ▲                                        │
                                          └── 06 雙向：襯砌支撐勁度/壓力回饋 ◀─────┘
```

## 2. 小模襯砌：shell 現狀評估與 liner 選項（D1）

**官方查證事實**：
- `structure shell create by-face`＝node-to-zone link，平移三 DOF **rigid**、轉動 free → **不能分離、不能滑移、無界面彈簧**。官方明文對照：「shell 提供剛性連結；liner 提供彈性連結，允許開縫與滑移」〔sel_manual\shells\shells.html；zonesel\test3d\Liner\AdvancingLinedTunnel〕。
- `structure liner`＝每節點法向彈簧（有抗拉強度、可開縫再閉合）+ 切向彈簧-滑塊（c、φ、殘餘 c）。關鍵字：`coupling-stiffness-normal / coupling-yield-normal / coupling-stiffness-shear / coupling-cohesion-shear(-residual) / coupling-friction-shear`；勁度經驗式 k=10×max[(K+4/3G)/Δz_min]，曲面再乘 10–100〔sel_manual\liners\liners.html〕。
- 內力讀法（兩者通用，liner 即 shell-type 元素）：`structure liner recover surface (0,1,0)` → `recover resultants` → FISH `struct.shell.resultant(sp,0,5)`＝Ny（環向推力 N）、`(sp,0,2)`＝My（環向彎矩 M）。**官方驗證題 LinedCircularTunnel 用 Einstein & Schwartz (1979) 解析解對 N/M 做基準**——可直接當我們讀法的 QA 錨點〔datafiles\VerificationProblems\LinedCircularTunnel\liner-check.f3dat L122-145〕。
- 殼性質可 mid-run 分區改：`structure shell property isotropic (E,ν) range ...`；FISH `struct.shell.young(p)=f` 可寫（官方警語「cycling 中修改可能有風險」），改完呼叫 `struct.force.update()`〔cmd_structure.shell.property.html；fish_sel.shell.young.html〕。
- creep 區 + liner/shell：官方**無**任何範例與明文限制（搜遍 Creep 資料夾與 SEL 手冊）——我們的 Burgers-Mohr+殼組合沒有 Itasca 基準可靠，只能用 LinedCircularTunnel 彈性基準驗讀法。

**評估**：
- 現狀 shell（rigid link、25GPa、record-only 應力）＝**未開裂上界拘束**：高估襯砌拘束→小模擠壓（=下游驅動）偏低；殼應力 22–46MPa 超抗拉 5–11 倍不物理，只能當「開裂熱點指標」。
- 選項 liner：物理上更正確（噴凝土-圍岩界面可脫開/滑移），讀 N/M 同管線；代價=界面參數 3–6 個要定、curved surface 勁度要調。
- **建議（05 版）**：**維持 shell** 但把「control stress」升級成**真實分區損傷折減**：每階段末，把 σ_recover > ft 的殼分組降 E（25→有依據的開裂 RC 有效模數，地板 ~2.5–5GPa，官方 command path 支援）→ 下一階段小模拘束隨開裂鬆弛，驅動才不被系統性低估，且與耦合模「會開裂的襯砌」自洽。liner 留作 06 或敏感度（若 Wade 要界面滑移物理）。
- 移除建模預留 liner elastic zone（null）→ 裸岩鬆弛 → 裝殼：**維持現狀，正確**（避免雙重襯砌+wished-in-place 過應力；已驗證安裝應力僅 0.26MPa）。

## 3. 耦合模圍岩本構：建議「單一等效彈性」（D2）

**建議：彈性，單一材料**，理由：

1. **職責分離、避免物理重複計算**：分層、塑性、潛變、水的效應已全部發生在小模、並包含在傳入的邊界位移場中。耦合模若再放 MC/塑性，位移驅動下圍岩自己降伏消耗驅動→同一份塑性變形被算兩次，襯砌受力反而失真且載重路徑依賴、不可唯一。
2. **數值穩定**：wall-zone facet 是 zone 面的奴隸副本〔pfcplugin.html「PFC walls are slaved to FLAC3D zone faces」〕，zone 降伏大變形是 facet 退化（solveForX 系列崩潰）的根源之一；彈性圍岩下 facet 幾何最穩。這與 8+ 次耦合失敗的教訓一致。
3. **E_eq 不是拍腦袋、是可率定的傳遞函數**：校準準則＝「**只有 in-situ、無驅動時，耦合模洞壁位移 ≈ 小模同窗洞壁位移**；驅動後每階段，耦合模洞壁位移 vs 小模洞壁位移偏差 < 容差（建議 15%）」。起點值用小模近隧道層（layer4 為主）體積加權 E，再依 gate 微調。這是 submodel 一致性校準，不是湊量級。
4. **誠實的界定**：彈性圍岩把驅動全額傳給襯砌（無塑性洩壓）→ 襯砌荷載偏保守上界；小模 elastic shell 拘束偏強 → 驅動偏下界。兩端夾出誠實區間，論文可以此論述。
5. **敏感度對照（選配）**：跑一版圍岩=layer4 MC 對照，確認裂縫 pattern 結論穩健，放論文附錄。

## 4. 小→耦合傳遞：位移邊界驅動 + 殘差定論（D3）

**不要**把「力」直接拿去解 PFC（舊 260529 假耦合的問題——襯砌受力變成輸入而非輸出）。**建議維持位移邊界驅動圍岩外邊界**，互制（襯砌抵抗→圍岩應力重分配→接觸力更新）由 wall-zone 在 box 內自然發生：

- **驅動面**：耦合 box 外表面全部 gridpoints（含 y 端蓋，y 端蓋處理沿用 codex_bc_reconcile 定論：全驅動、解讀時排除端蓋 artifact）。
- **驅動量**：小模該階段**增量**位移場，IDW 映射（沿用 couple_idw.py 機件）。
- **剛體定論**：**扣除剛體（Kabsch 最佳擬合平移+旋轉）後的殘差場驅動**。力學依據：剛體運動不產生應變、對襯砌內力零貢獻；保留只會擴大 PFC domain 行程與數值行程。「殘差只有母模位移的 1%」不是傳遞失敗——若母場 99% 是剛體平移，1% 就是全部的變形內容。**必設 gate**：殘差場與 full 場在 box 上的平均應變張量必須一致（數學恆等，逐階段驗證印出）→ 這一條把 codex_overturn 的疑慮轉成可證偽的檢核，也解決 small_idw.py docstring 與 f3dat 實作矛盾（文件同步改）。
- **載入配方（官方例句式）**：per-stage `zone gridpoint fix velocity` + FISH ramp（`gp.vel` 可寫〔fish_gp.vel.html〕）分 N 子步 → 每子步 `model cycle n` + `model calm`（SleevedTriaxialTest rampUp 同款：每增量 cycle 200 + calm〔DataFiles3D\PFC\Examples\SleevedTriaxialTest\SleevedTriaxialTest.dat〕）→ 增量施加完，邊界速度歸零 hold → `model solve ratio-average 1e-4`（官方兩個耦合例一致用 ratio-average；PunchIndentation 用 1e-4〔PunchIndentation.f3dat〕）。
- **timestep**：`model mechanical timestep scale` 在 zone 側官方明文 no-op、PFC 側=密度縮放使每球 dt=1（僅限準靜態）〔cmd_model.mechanical.html；timestep_constraints.html〕。官方耦合例用 scale；我們 v5/servo 也是。若沿用 automatic 路線，PFC 載入時 safety-factor 預設 0.8、我們驗證過 0.5 穩定——**兩條路都有官方依據，建議沿用已驗證的 v5 配方不動**。
- **阻尼**：`ball attribute damp` 官方模式＝平衡期 0.7、載重期 0.1（RockTest ucs.dat「apply a small amount of damping」）；我們既有 0.7–0.8。建議驅動期試 0.3–0.5 折衷（載重期太高的 local damping 會人工抑制脆性斷鍵的動態釋放，影響裂縫 pattern）——短測後定。
- **largestrain on** 全程（wall-zone 啟用必要條件〔pfcplugin.html〕）。

## 5. 耦合模四個輸出量的正確讀法（全部 doc-verified）

| 量 | 讀法 | 依據 |
|---|---|---|
| **外力**（圍岩→襯砌） | 總量：`wall.force.contact(w)`（wz_outter 上全接觸力合力）。分布 p(θ,y)：PFC6 **無** per-facet force intrinsic——官方替代法＝逐 facet `wall.facet.contactmap(f)` 取接觸 map，自己 Σ `contact.force.global(c)`，依 facet 形心 (θ,y) 分箱 | fish_wall.force.contact.html；fish_wall.facet.contactmap.html |
| **內力**（襯砌本體） | 主軌＝**斷面切割法**：沿 y 每隔 Δy、沿環每 Δθ 定義切割面，Σ 跨切割面 ball-ball contact 的 `contact.force.global`（=linear+dashpot+pbond 總力〔Eq.(1) cmlinearpbond.html〕）+ 對斷面形心取矩 → N、Q、M 分布。輔軌＝bond 層級熱點：`contact.prop(c,'pb_sigma'/'pb_tau')`（bond 周邊纖維最大正/剪應力，read-only）。measure 球（官方 in-material 唯一法〔RockTest tension.dat〕）在環內受限：環厚僅 ~5 顆球徑，精度有限，只作參考 | cmlinearpbond.html Eq.(1)(12)；fish_contact.prop.html |
| **裂縫** | 官方 `fracture.p3fis` 配方：`fish callback add @add_crack event bond_break`；entries(1)=contact、(2)=模式 1 拉/2 剪、(3)=破壞強度、(4)=應變能 → DFN `crack_tension`/`crack_shear`（位置/dip/dipdir/尺寸）。**quirk**：`fracture.create` disk 第三參數是「直徑」而官方腳本傳 pb_radius——沿用官方或自行 ×2，擇一並註明。普查軌：`pb_state`（0=從未鍵結、1=拉斷、2=剪斷、3=完好）雙軌互驗 | cmlinearpbond.html Table 3；fragmentationdatafiles.html（fracture.p3fis 全文）|
| **反力**（襯砌→圍岩） | 作用-反作用：wz_outter 傳入 zone gridpoints 的力＝球對 facet 接觸力之負值 → 同外力 map 取負即反力分布；圍岩側可用 `gp.force.unbal`（官方判例：velocity-fixed gp 平衡時 unbal=反力〔SquareFooting footing-load.f3dat〕）交叉驗 | pfcplugin.html；fish_gp.force.unbal.html |

注意：quad zone face 拆兩個三角 facet、力只分配到該三角的 3 個 gridpoints〔pfcplugin.html〕——解讀 gridpoint 力時記得。

## 6. 內牆 w_inner 剛性牆問題（D4，新發現的關鍵決策）

v5 現狀：`wall_inner` 剛性牆**全程保留**（防解凍彈跳）。但剛性內牆封住襯砌內面 → 環無法向內撓曲 → **彎拉開裂被系統性抑制**，只剩壓剪路徑——與「看到襯砌開裂」的目標直接衝突（真實噴凝土內面是自由面）。選項：

- **(a) 建議：進入 05 驅動前刪除 w_inner**。鍵結環自撐有官方鐵證（bonded-assembly 刪全牆不散；PunchIndentation 也刪 temporary lid）。與「解凍彈跳」教訓不同——當時是 install 瞬態、未平衡；現在環已 bonded+servo 平衡完成。程序：restore Couple_Initial → `wall delete` w_inner → `model solve ratio-average 1e-4` 再平衡 → **gate：額外斷鍵=0、球最大位移擾動 < 容差（mm 級）** → 存 Couple_Initial_free 作 05 起點。
- (b) 保險版：保留牆但把 bf_rigid 接觸 kn 降數個量級（近自由但防彈出）。
- (c) 維持剛性（不建議——裂縫模式失真，研究目標受損）。

（w_860/w_910 端蓋剛性牆建議保留：端部人工邊界本來就要截斷解讀。）

## 7. 05 單向管線定案流程（含 staging 與 gates）

**階段制（D5）**：三選一，需與論文第五章文字同步：
- (i) 論文現稿：低-高-雨後低 3 階段各 30 天；
- (ii) 現行程式：低-高-低-高 4 階段各 30 天（能展示第二輪 re-activation=「反覆觸發」主軸，**建議**）；
- (iii) 今日新做的 11 階段 W-110↔W-10（最細，但 creep bug 待修+小模端未改 11 階段制，成本最高）。

**流程**：
1. 大模 staged creep（修 time-total 累積 bug）→ 各階段 box 位移場
2. 小模 driven（同階段制；shell 分區損傷折減 per §2；門檻/η 用定版參數）→ 洞壁位移場 + 殼 N/M + 收斂曲線
3. 耦合 initial 重做：新大模場 IDW、圍岩單一等效彈性（E_eq 初值+校準）、（採 (a) 則）刪 w_inner 再平衡
4. 耦合 per-stage 驅動（§4 配方）→ 外力/內力/裂縫/反力（§5 配方）
5. **Gates**：G1 小模殼反力總量 vs 耦合 wz_outter 合力同量級可互釋（Wade 既定原則）；G2 耦合洞壁位移 vs 小模洞壁位移 <15%（E_eq 校準）；G3 殘差-full 應變一致性（§4）；G4 裂縫 pattern vs NO46 展開圖定性比對（縱向裂縫帶位態）；G5 Control-0（零驅動→零裂縫增量，沿用 Codex P2 準則）
6. 產論文第五章三組圖（坡地/隧道/支撐）

## 8. 06 雙向（1+2 尺度）設計

大模維持單向；小↔耦合每階段閉迴圈。**交換量建議用「勁度/損傷」而非「力」**（舊樹凍結反力 Picard 發散教訓 #63；力回饋無剛度、易失穩）：

```
stage k：小模(殼 E_k) → 洞壁/邊界位移 → 耦合驅動 → 裂縫密度 ρ(θ,y) + 支撐壓力 p(θ,y)
        → 折減映射 E_{k}^{new}(θ,y) = f(ρ)（分區 structure shell property isotropic range）
        → （Picard：小模 stage k 重跑一次，under-relaxation 0.5）→ 收斂判準：
           洞壁位移變化 <5% 或裂縫增量變化 <10% → 進 stage k+1
```

- 折減律 f(ρ)：開裂 RC 有效模數文獻區間 3–8GPa 為地板，按裂縫密度線性內插（後續可用四點彎率定，舊樹 D11 思路）。
- 強形式備選：把小模殼換成 `zone face apply stress-normal 1.0 fish-local @p_map`（官方 per-face 空間分布機制〔cmd_zone.face.apply.html fish-local〕）直接施加耦合實測支撐壓力——保留為研究性對照，不當主線（無剛度、發散風險）。
- 06 的全部機件（IDW、驅動、讀數、gates）與 05 完全共用，06=05+迴圈控制。

## 9. 決策點清單（等 Wade 裁示）

| # | 決策 | 我的建議 |
|---|---|---|
| D1 | 小模襯砌：shell 維持 + 分區損傷折減 E？或換 liner？ | shell+損傷折減（05）；liner 留 06/敏感度 |
| D2 | 耦合模圍岩：單一等效彈性？ | 是；E_eq 用洞壁位移 gate 校準；MC 對照放附錄 |
| D3 | 驅動場：殘差（扣剛體）？ | 是，配應變一致性 gate |
| D4 | w_inner 剛性內牆 | 刪除（短測 gate 通過後）；保險版=降 kn |
| D5 | 階段制 | 4 階段低高低高（論文文字同步改）；11 階段若要細化需同改小模端 |
| D6 | 載入配方 | v5 timestep/阻尼配方不動；驅動期 damp 短測 0.3–0.5 |
| D7 | live large_staged | 跑完後修 time-total bug 依 D5 重跑；stage2+ 產物棄用 |

---
（查證紀錄：本文件由 5 個文件查證 agent 的結構化輸出彙整，原始引用含行號存於 session 工作區 verify_full.md。）
