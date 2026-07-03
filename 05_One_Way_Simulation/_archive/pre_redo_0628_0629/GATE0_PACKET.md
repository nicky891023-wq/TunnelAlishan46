# GATE-0 PACKET — Phase 0 成果 (修正門檻重跑 + 控制組) 送 Codex 審

- **日期**：2026-06-28
- **依據**：WORKFLOW_v2 (Codex APPROVED FOR EXECUTION)。Phase 0 條件：凍結定義、修 sin/cos 門檻、舊成果列 provisional、修正門檻重跑大/小 baseline + HIGH-only/LOW-only/no-creep 控制組、Gate-0 含 stress path/q-qth/分層 active/增量分解。
- **狀態**：⏸ AWAITING CODEX GATE-0 REVIEW → 確認幾何/應力路徑/變形位置/破壞區合理 + 准進 Phase 1/2，或退回。

---

## 1. 已執行 (Phase 0)
- ✅ 凍結定義 (WORKFLOW_v2 §1)：q_th=0.6*(c·cosφ+p'·sinφ)、SI 壓縮負、datum reset、drained endmember 水位。
- ✅ 修 sin/cos 門檻 (large_creep_4stage.f3dat:48 / small_4stage_standalone.f3dat:39) + 小模 header 0.8→0.6。
- ✅ 舊門檻成果備份至 `_provisional_oldthreshold/`。
- ✅ 修正門檻重跑：大模 baseline、小模 baseline、大 HIGH-only/LOW-only、(進行中) 大 no-creep + 小 HIGH-only/LOW-only/no-creep。
- ✅ fracture_track.fis zmax bug 已修 (Codex REVIEW#01)。

## 2. 關鍵結果 (8 run 全完成：大/小 × baseline/HIGH-only/LOW-only/no-creep)

### 2.1 大模 (邊坡潛移) — 過驅動(creep 主導) + 水位效應明確
| 案例 | dmax/階段 (m) S1/S2/S3/S4 | 增量 |
|---|---|---|
| baseline (LOW-HIGH-LOW-HIGH) | 0.880/1.313/1.426/**1.630** | +0.88/+0.43/+0.11/+0.20 |
| HIGH-only (常高水) | 1.029/1.367/1.542/**1.686** | (最多) |
| LOW-only (常低水) | 0.880/1.171/1.305/**1.380** | (最少) |
| no-creep (彈性水響應) | 0/0.131/0.131/**0.131** | 純彈性=13cm |

- **水位效應確認**：HIGH-only(1.69) > 循環(1.63) > LOW-only(1.38)、增量 HIGH > LOW。**機制方向正確**。
- **⚠️過驅動 = creep 主導**：no-creep 僅 13cm，creep 加 ~1.5m。連 LOW-only 1.38m >> 現場(15-33mm/年→120天 5-11mm) = **~125-275×**。過驅動是 creep 參數本質、水位調制次要(~22%)。

### 2.2 小模 (隧道收斂) — mm 級、強烈支持假說
| 案例 | dmax/階段 (mm) S1/S2/S3/S4 | 增量 |
|---|---|---|
| baseline | 3.22/4.21/4.21/**4.42** | +3.22/**+0.99(H)**/**+0.005(L暫停)**/+0.21(H) |
| HIGH-only | 3.96/4.02/4.04/**4.05** | (快速飽和) |
| LOW-only | 3.22/3.24/3.25/**3.26** | (S1 後幾乎不動) |
| no-creep | 0/1.89/1.89/**1.89** | 彈性=1.89mm |

- mm 級隧道收斂合理。**no-creep 分離**：1.89mm 彈性 + 2.5mm creep ≈ 各半。
- **creep 集中 layer4** (濕弱砂頁岩 c=100kPa、S1 dump L4=612750/618771=99% active)。

### 2.3 🔑核心機制 — 水位直接調制 creep-active set (no-creep active-by-stage 最乾淨)
小模 active zones/階段 (no-creep 版、純門檻不含 creep 累積)：
**S1 LOW=662079 → S2 HIGH=868855 → S3 LOW=385633 → S4 HIGH=868855**
→ **HIGH 水位 → 有效應力降 → 更多 zone 偏差應力越過門檻 → active set 增 ~2.3×；LOW 反之**。
這是假說的核心力學：地下水升→有效應力降→越過 creep 門檻→依時變形。**乾淨重現、強力支持。**

## 3. Visual QA (已產出 + Claude 渲染檢視過，Codex 請審)
- **gate0_small_fields.png** (固定色階 y=885 切片、4 階段 ×3 列)：q/qth + creep-active + disp。**creep-active S1=14737 帶狀 → S3 LOW=364(帶幾乎消失) → S4 HIGH=10780(回復)** = 水位調制視覺鐵證;q/qth 高值集中 layer4 帶(z1740-1760)+隧道 EDZ;disp 隧道收斂型態 mm 級集中近洞。
- **gate0_small_trends.png**：cumulative + 增量;增量圖明確 HIGH(S2/S4)驅動、LOW(S3)暫停;no-creep 彈性階 1.89mm。
- **gate0_large_fields.png**：slope creep 集中上緣淺層/邊坡面;disp 切片 0.46-0.8m。
- **gate0_large_trends.png / gate0_*_overdrive.png**：大模 ~75-160× 現場率(over-driving)。
- slice active-by-layer (小模)：L4 S1=13512/13687(99%) → S3=356(LOW) → S4=9756(HIGH)。
- **Visual QA 限制 (誠實揭露)**：(a) 切片散點圖非插值場(zone centroid scatter);(b) overdrive 比較用「邊坡率 15-33mm/yr」對兩尺度,對小模(隧道)非恰當錨(隧道現場收斂錨稀疏);(c) 尚未做 stress-path(q-p')軌跡圖、rigid/residual 分解(那是 Phase 2 耦合驅動才需);(d) unbalanced/ratio 歷時未繪(可補)。請 Codex 指示 Gate-0 是否需補這些才放行。

## 4. 待 Codex Gate-0 裁定
1. **大模過驅動 (~150-280×)**：(A) 重新校正 creep 參數(eta/門檻)使量級對齊現場率 / (B) 接受為 endmember scenario(已標 scenario analysis 非 calibrated) 並聚焦「機制方向正確」/ (C) 其他。**Claude 傾向**：大模定位為 regional context scenario(B)，因核心交付是隧道尺度(小→耦合);但若要量化現場對應，需 (A) 校正。請 Codex 裁。
2. **小模成果**：是否確認合理 (mm 級、L4 主導、水位調制)、可進 Phase 1 (襯砌反力抽取) + Phase 2 (耦合驅動)？
3. **幾何/應力路徑/變形位置/破壞區** 合理性確認 (Wade 治理要求)。
4. **小模 s1 primary creep**：是否需 spin-up/baseline 扣除 (Codex 之前提)，或 S1 視為 primary 暫態、後續增量為水效應已足夠分離？

---
## 5. Gate-0 條件處理 (Codex PASS WITH CONDITIONS、2026-06-29)
- **C1 大模非單一 layer4**：大模 creep 跨 layer2-4(淺層/邊坡面主導)、不稱單層機制。已於 §2.1/§2.3 修正措辭。
- **C2 q/qth vs creep flag 時序**：dump 的 `creep`=該階段**潛變前**門檻 gate flag(do_threshold 當下)、`q/qth`=該階段**潛變後**應力狀態 → 圖上兩者不必逐一吻合(creep 後應力鬆弛、q 下降);active 帶與 q/qth 帶大致對應即合理。
- **C3 HIGH-only/LOW-only 標籤**：控制組由 baseline sed 衍生、io.out 仍帶 baseline 的 "S1 LOW/S2 HIGH" 字樣、但**實際水位恆定**(HIGH-only 全 HIGH、LOW-only 全 LOW)。階段標籤=時間階段(day30/60/90/120)、非水位;趨勢表已按此解讀。
- **C4 大模 endmember 標記**：大模成果**明確標為 non-calibrated regional-context endmember scenario**、不作定量現場率預測。大模**不驅動耦合**(耦合由小模驅動)、故不涉 item5 的 calibrated forcing 問題。
- **C5 小模 layer4 = threshold-sensitive weak-layer creep**：非校正破壞預測;設計級宣稱前須跑門檻/c 敏感度(列 Phase 4 sensitivity)。
- **C6 Phase 1 條件**：襯砌反力/收斂從**隧道壁參考點**(crown/side/invert)+ virtual interface traction 抽、**不用 global dmax**。→ Phase 1 遵此。
- **延後項(Codex 同意移至 Phase 1/2)**：插值/contour、stress-path(q-p')軌跡、rigid/residual 分解、unbalanced/ratio 歷時。
