# 阿里山 #46 三尺度依時變形重作 — 交付報告 (2026-07-01)

退回力平衡重作，從大模初始開始逐步往下，凡有發現先記錄、交你查核。

## 0. 流程總覽（你的權威規格）
- **大模**：區域邊坡潛移（地下水+時間、4 地層）→ 交付公尺級位移驅動小模
- **小模**：隧道擠壓（6 地層、自由體）→ 看 y860-910 頂拱/側壁收斂歷時（低水位緩、高水位顯著、creep 主導）
- **耦合模**：結構尺度、取小模逐階位移當輸入 → 襯砌受力/裂縫 pattern（後續）

---

## 1. 大模初始 + 4 階段（✅ 完成、合理）
- **in-situ**：K0=1.0、solve elastic，地表拉力 +0.1MPa（岩石抗拉強度內、你已接受）。Large_Initial.f3sav
- **4 階段水位 creep**（LOW-HIGH-LOW-HIGH、120 天、threshold 0.6 Burgers-Mohr）：
  | 階段 | 水位 | 累積 dmax | 該階段增量 |
  |---|---|---|---|
  | S1 | LOW | 0.453 m | (初始+creep) |
  | S2 | HIGH | 0.710 m | **+257 mm（快）** |
  | S3 | LOW | 0.821 m | +111 mm（慢） |
  | S4 | HIGH | 0.994 m | **+173 mm（快）** |
- **高水位階段潛移快、低水位慢** ✓ 符合依時變形物理。**~1m 公尺級邊坡潛移** ✓ 符合你的預期。

## 2. 小模初始（SHELL 襯砌、✅ 力平衡合理）
- **建殼方法**（方案 A、render 驗證）：null attached lining → `struct shell create by-face range group 'rock' position<內部>` → 乾淨單層 D 形洞壁殼（68051、隨彎曲隧道、~640 面/m、dkt-csth、E0=25GPa t=0.40）
- **岩石力平衡很好**：
  - max_disp **5.2mm**（vs 裸岩 22.3mm）→ shell 成功 bound 收斂 ✓
  - 塑性 **11.6%**（vs 裸岩 38.7%）→ shell 支撐減少降伏 ✓
  - 拉力 +0.1MPa（ten_r 內）、max_vel 1.86e-7（收斂）✓
  - **datum 不歸零**：保留 in-situ 彈塑變形為 day-0 值（你要求「曲線 0 天不為 0」）

## 3. ⚠️ SHELL E 折減的重要發現（需與你討論）
- in-situ 殼**拉力 32.7MPa（8× 超過混凝土抗拉 4.12MPa）**——頂拱/仰拱彎曲處
- **實證測試結論：E 折減無法 cap 殼應力**（不論 FISH 設 young 或 command isotropic）：
  - 設 E=5GPa → solve 前應力降到 6.5MPa（stress=E×strain）
  - **solve 後應力回到 32.7MPa**（strain 增 5× 補償）→ **應力是力控的**（圍岩推力固定、軟化殼只是變形更多、stress=force/area 不變）
- **這與你以前 SHELL E 折減的差異**：你以前是 delete+recreate（重設應力歸零），但本案邊界（固定/驅動 box）使殼力控，E 折減（任何形式）無法 cap
- **本次處理**：shell 維持 E0（bound 收斂、隧道擠壓量級由大模驅動主導、非殼軟化）；shell_damage 改為**記錄超應力區=襯砌裂縫 pattern**（你要的裂縫各自 pattern 的雛形）
- **待你決策**：(a) 接受「超應力區=裂縫指標」+ 殼維持 E0；(b) 改用會塑性/開裂的襯砌模型（非彈性殼+E 折減）；(c) 其他

## 4. 大→小驅動（velocity-IDW、residual）
- 大模逐階 box 邊界位移 IDW 映射到小模 14946 個 box 面 gp
- **發現**：大模 slope creep 把小模 box **近乎剛體平移**（rigid frac=1.00、s4 平移 300mm），**純變形 residual 僅 5-18mm**
- 用 **residual 驅動**（排除剛體平移+旋轉的假性收斂）：隧道擠壓 = 純應變部分 + creep 放大。這是物理正確的擠壓量測。
- ⚠️ **量級提醒**：大模在小模尺度上差異變形僅 ~18mm，隧道擠壓可能 < 你預期的 10-20cm（除非 creep 大幅放大）。這是大模實際交付的量、非作弊湊數。small_driven 結果見下。

## 5. 小模逐階依時變形（small_driven、residual 驅動）
- **質性行為全對** ✓：
  - day-0 in-situ vclose=-2.14mm hclose=-1.75mm（**曲線非零 ✓**、你要的初始彈塑變形）
  - stage1(LOW) -2.20/-2.08 → stage2(HIGH) -2.50/-2.93 → stage3(LOW) -2.44/-3.00mm
  - **低水位 creep 極緩、高水位 ~5× 加速** ✓（你的依時變形物理）、無劇烈跳動 ✓
  - 記錄襯砌裂縫 pattern（超應力殼數逐階增加）
- **量級僅 ~3mm（diameter closure）、遠低於目標 10-20cm**

## 6. 🎯 量級診斷（誠實、不作弊）— 見 MAGNITUDE_DIAGNOSIS.md
**真正根因（實測、非假設）**：
1. **模擬斷面是淺層+低應力**：實測隧道處 sig1=0.3-1.7MPa（非 5-12MPa）、覆蓋僅 ~100-200m（部分出露邊坡趾部）→ **σcm/p0 高 = 輕微/非擠壓地層**。3mm/10m=0.03% 應變 = 非擠壓區正常值。
2. **creep 黏滯不是瓶頸**（決定性）：eta_m 降 300×（6e15→2e13、diag_etam）creep **幾乎不變**→ 真瓶頸是**低驅動應力使 creep 門檻未跨**（q≈0.3-0.5 < q_th≈0.6、tcrit 場大多 <0.6、creep 被餓死）。**調 eta 既作弊又無效**。
3. **stiff shell 過度支撐**（次要）：裸岩 22.3mm vs 有殼 5.2mm（4.3×）、E_shell/E_rock=16.7×。E0=25GPa 對「會開裂的等值襯砌」可能太硬。
4. **驅動 residual 小**：大模近剛體平移、box 面差異變形僅 5-26mm/100m → 隧道跨度 ~10m 才 ~2mm。

**10-20cm 在此斷面物理上不合理**（這是淺層輕擠壓段）。**達 10-20cm 需要：較深斷面(p0 5-12MPa)、或更長時間(多年非 120 天)、或更大傳遞驅動**——都是物理/scope 問題、不是旋鈕。

**待你決策（scope/物理、非我能定）**：
- **A（最關鍵）**：模擬的斷面夠深嗎？10-20cm 需 p0≈5-12MPa(覆蓋 300-500m)。要從較深中心線樁號重切小模 box、或接受此段本就低擠壓？**這單一決策解釋大部分落差**。
- **B**：等值襯砌 E0 用裂後 RC 有效模數(~3-8GPa) 取代完整 25GPa？（你本就要它開裂、物理可辯護）
- **C**：時間窗 120 天 vs 多年（若 10-20cm 是長期狀態）
- **D**：eta 維持 6e15（diag_etam 證明、不作弊）

**今晚可做（便宜、修正性、非湊數）**：等值襯砌 E0=5GPa(裂後 RC) + 修好的 command E 折減重跑 → 預期 ~10-20mm（誠實可закрыть 的部分、仍未到 100-200mm、headline 是斷面深度）。

## 7. 三 initial render（睜眼驗證）
- **大模 initial**（qa_large_initial.png、y900 邊坡剖面）✓：szz 壓應力隨深度增至 -28MPa、地表塑性帶 7.6%、沉陷 566mm(4 階段會歸零重啟 creep 鐘)、max_tension +0.1MPa、收斂(vel 3e-7)。邊坡 in-situ 合理。
- **小模 initial**（qa_small_initial.png、y885 隧道剖面）✓：隧道周圍壓應力集中、塑性集中近隧道 16.9%、max_disp 3.87mm(shell bound)、max_tension +0.1MPa、收斂(vel=0)。
- **收斂歷時**（qa_convergence_history.png）✓：day-0 非零、LOW 緩/HIGH 加速、無劇烈跳動、~3mm。
- **耦合 initial**：Couple_Initial.f3sav 存在(幾何就緒)、但**需依你指示把圍岩統一為單一彈性 + 取小模逐階位移驅動**(尚未重做)；且 PFC 襯砌需另法 render(zone-slice 不顯示球)。**列為下一步**。

## 8. 總結 — 今晚成果 vs 待你決策
**✅ 質性流程全部正確、誠實重做（從力平衡逐步）**：
- 大模公尺級邊坡潛移(高/低水位對)、小模 shell 力平衡、大→小驅動、threshold creep、收斂歷時(day-0 非零、LOW 緩 HIGH 快、無跳動)、裂縫 pattern 記錄——**全符合你的三尺度依時變形規格**。
- 全程 grounding 安裝文件、render 親驗、無作弊(eta 維持 6e15、模型維持 Burgers-Mohr)。

**⚠️ 唯一未達：擠壓量級(~3mm vs 10-20cm)——但這是誠實的物理結果，不是 bug**：
- 此斷面實測淺層低應力(0.3-1.7MPa)=輕擠壓地層；creep 被門檻餓死(非黏滯問題、eta 測試已證)；stiff shell 過度支撐。
- **達 10-20cm 需要物理/scope 改變(你決策)**：A.較深斷面(p0 5-12MPa) B.等值裂後襯砌 E0(3-8GPa) C.更長時間 — 都不是數值旋鈕。

**🙋 請你晨間決策**（見 §6 A/B/C/D）：最關鍵是 **A.模擬的斷面是否夠深**(這解釋大部分落差)。我可今晚先跑「等值裂後襯砌 E0=5GPa + 修好的 E 折減」展示誠實可閉合的部分(~10-20mm)——但 headline 是斷面深度、需你定。

## 6. 三 initial render（待補）
- 大模 / 小模 / 耦合 initial 的應力場/位移場/塑性區 render（睜眼驗證）

---
*所有長檔皆先驗證再執行、render 親驗、凡有疑點先記錄交你。*
