# 雙向強耦合數值方法（小模 ↔ 耦合模）— 架構定案 v1（2026-07-07，Fable）

> 本文件把 01–05 全部實戰經驗（含 12 次失敗的教訓）整合成 06 的可執行架構。
> 前置條件未滿足前**不開工**（見 §7 checklist）。設計原點：Wade 的構想
> 「小模圍岩變形＝耦合模襯砌外力；耦合模襯砌狀態＝小模圍岩所感受的支撐」＋
> 05/docs/COUPLING_METHOD_PROPOSAL.md §8 的定向（交換勁度/損傷、非力）。

## 1. 為什麼要雙向（物理動機）

單向鏈漏掉的物理＝**漸進互制**：襯砌開裂 → 環勁度下降 → 圍岩失去支撐、收斂加大 →
驅動變形加大 → 更多開裂。這個正回饋在濕水位階段（開裂活躍期）最重要；單向鏈的
小模殼永遠用「未損傷（或 secant 上限折減）」的勁度抵抗圍岩，會**低估**濕期收斂與
裂縫發展。雙向的目的＝把「耦合模量到的真實損傷」餵回小模的支撐勁度。

## 2. 交換量設計（定案）

| 方向 | 物理量 | 載體 | 理由 |
|---|---|---|---|
| 小模 → 耦合模 | 各階段箱邊界殘差位移（Kabsch 扣剛體） | `cpl_resid_sNN.txt`（05 成熟鏈） | 已驗證；位移驅動良態 |
| 耦合模 → 小模 | **襯砌損傷場 D(θ,y)** → 殼分區 E 折減 | `dmg_map_sNN_iK.txt`（新） | 勁度交換數值良態；**力回饋在同一介面同時給位移+力＝過定，且舊樹 Picard 發散實證**——力回饋僅留對照組 |

**損傷映射公式**（用 05 已建好的扇區機制：24×15° × 5 個 y 帶）：
- `D_s = N_broken_s / N_bond_s`（該扇區可斷鍵的斷裂比率），夾限 [0, 0.9]
- 殼元素勁度：`E_el = E0 × (1 − D_s(θ_el, y_el))^m`，初版 m=1；下限 2.5 GPa（沿用 Wade secant 樓地板）
- 施加時機＝**階段邊界、單次寫入＋`struct.force.update`**（Wade secant 實戰驗證的殼勁度更新模式；
  嚴禁 cycling 中反覆改殼勁度——T4 能量注入失穩教訓）
- 小模原 secant cap **保留**作階段內數值保險（樓地板抬高為 5 GPa），跨階段損傷唯一來源＝映射 D
  （單一損傷源，避免雙重折減）

## 3. 兩個耦合層級（L1 主線、L2 驗證）

### L1 交錯式（staggered，主線，建議先做）
第 k 階段的耦合模損傷 → 第 k+1 階段小模的殼勁度。**無階段內迭代。**
- 物理正當性：水位階段歷時 5–30 天 >> 開裂瞬時 → 損傷在階段時間尺度上演化，一階段滯後可接受
- 成本 ≈ 2× 單向鏈（~30–40 小時整鏈）
- 流程（k = 1…11）：
  1. 小模階段 k（殼 E 用 `dmg_map_s{k-1}` 映射；k=1 用未損傷 E0）→ ss_k'
  2. 匯出邊界位移（exp_body 模式）→ make_cpl_resid → cpl_resid_sk'
  3. 耦合模階段 k（G4 系初始態、calm 節奏配方）→ 7 種輸出 → make_damage_map → dmg_map_sk
  4. k+1

### L2 階段內 Picard（嚴謹版，只對濕峰階段 5–7 做，驗證 L1 滯後誤差）
同一階段內迭代：小模(i) → 耦合(i) → D(i) → **欠鬆弛 D̂(i) = D̂(i−1) + 0.5·(D(i) − D̂(i−1))** →
小模重跑階段 → 收斂判準：`‖Δu_cavity‖ < 5%` 或 `|ΔN_crack|/N < 10%` 或 max 3 迭代。
- 成本：每迭代 ≈ 小模階段(30–40min) + 傳遞(10min) + 耦合階段(1.5–2h)；3 階段 × 3 迭代 ≈ +15–20h
- 產出：L1 vs L2 的濕峰差異量化 ＝「滯後誤差」＝論文的方法論貢獻點

## 4. 從 05 直接繼承的機制（不重造）

- 傳遞鏈：exp_body.f3dat（restore 後重載 FISH 定義的成熟模式）、make_cpl_resid.py（Kabsch＋應變一致性 gate）
- 耦合階段配方：G4 系初始態、DRIVE_SCALE、10×150 ramp+calm、`cycle 2400 calm 300`+短 ratio 窗、
  fracture_track_v3（無 fragment）、couple_qa_v2 七輸出
- 扇區統計：export_pmap / crack_sectors → make_damage_map.py 只是重分箱
- 品質 gate：應變一致性（傳遞）、CONTROL-0（**零交換迴圈必須重現單向結果**——新增的 06 專屬 gate）、
  每階段 CS-CHK（gp_dmax 參與、裂縫淨增量、ball_dmax 貼驅動）

## 5. 數值鐵則（12 次失敗換來的，06 全部適用）

1. 介面勁度 = zone E（wall-zone 積分穩定）；bf 膠合僅 bf_couple 組
2. 全程 calm 節奏；>800 cycle 裸窗禁止
3. timestep scale 下嚴禁自由墜落體；BPM 環的約束/勁度變更須退火或 0g 操作
4. BC/servo 物件活在存檔裡——狀態轉用前盤點
5. restore 清空 FISH → 定義放側檔逐次 call；console 裸檔名/60s 間隔/以腳本產物驗證
6. 殼勁度更新只在階段邊界單次＋force.update（T4 教訓）
7. 長跑前先短測；每個新交換迴圈先跑 CONTROL-0（零交換）
8. 電源「永不睡眠」

## 6. 檔案介面規格

```
06/input/   ← 唯讀引用 05 產物：ss_01-11.f3sav（基線）、Couple_Initial_G4.f3sav、cpl_resid_s*（基線）
06/process/ run_twoway.py（總指揮）、make_damage_map.py、small_stage_dmg.f3dat（單階段殼E版）、
            couple_stage_one.f3dat（單階段耦合版）、exp_body.f3dat（沿用）
06/output/  ss_kk_iK.f3sav / cs_kk_iK.f3sav / dmg_map_skk_iK.txt / manifest.json（鏈狀態簿記）
```
- `dmg_map_sNN_iK.txt` 格式：`theta_lo theta_hi y_lo y_hi D n_broken n_bond`（24×5 列）
- `manifest.json`：每階段每迭代的輸入/輸出檔、gate 數字、收斂判定——**斷點續跑依據**

## 7. 開工前置 checklist（現況 2026-07-07）

- [ ] 05 staged 11 階段完整跑通＋三 gate（G1/G2/G4）評估完成 ← **進行中（G4 重澆中）**
- [ ] DRIVE_SCALE f 的物理意義定案（若 f<1，回饋的 D 是低估——需 f≈1 可行性或 D 放大校準；**開放項**）
- [ ] 小模「殼分區 E 寫入」單元測試（struct.shell.young 寫入＋force.update 於 restore 態）
- [ ] make_damage_map.py 對 05 stage 成果的離線試算（不用等 06 開工）
- [ ] run_twoway.py 乾跑測試（mock 檔案、驗證簿記與 console 排程邏輯）

## 8. 風險與對照組

- **主風險＝Picard 發散**（舊樹力回饋實證）：勁度交換＋欠鬆弛 0.5＋max 3 迭代已是保守設計；
  若仍振盪 → ω 降 0.3、或退回 L1 純交錯
- **對照組**：(a) 純單向（05 成果）＝下界；(b) 力回饋版留檔案介面但不做主線；
  (c) L1 vs L2 濕峰差＝滯後誤差量化
- 若 05 的 f 遠小於 1（趨勢研究），06 的定位同樣是**趨勢級的互制放大係數研究**
  （單向 vs 雙向的裂縫/收斂比值），論文表述照此校準
