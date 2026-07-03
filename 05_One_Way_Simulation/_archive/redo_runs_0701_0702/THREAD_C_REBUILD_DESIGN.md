# Thread C — 乾淨耦合重建設計（Wade 圍岩簡化 + Codex 重建裁決）

狀態：**設計中**（thread A 小模重跑運行時起草）。實作前需 REVIEW_PACKET→Codex APPROVED + 雙視覺基準。

## 目標（Wade 規格）
耦合模 = 結構尺度、圍岩影響範圍內、**襯砌聚焦**的運動學驅動結構模型。產出：襯砌**外力 / 內力(軸力·彎矩·剪力) / 反力(給圍岩) / 裂縫 pattern**。圍岩→**單一等值彈性**（僅傳遞介質、不解讀地質應力）。

## 現有耦合構造鏈（理解）
1. `build_Couple_mb3.f3dat` → `Couple_Model`：40×40×50m box(x[1277,1317] z[1728,1768] y[860,910])、結構化 hex 圍岩(層2-6 地質)、PFC 襯砌球(Wade STL、~456302)、wz_outter 牆-zone 耦合、w_inner 內背檔 + w_860/910 端板。
2. `Couple_Initial`(04)：bond 襯砌(linearpbond pb_ten=2.1MPa pb_coh=23MPa)+初始應力。
3. `couple_control0.f3dat` → `cb_control0`：載 box 驅動(28304 gp from couple_bnd_disp.txt)、零增量沉降檢核。
4. **零固定球**（襯砌靠 wz_outter 外 + w_inner 內 夾持）。

## 重建設計（重用幾何 + 乾淨新 BC）
**重用**（Codex 認可的 validated pieces）：`Couple_Initial` 的 bonded 襯砌幾何 + rock mesh + wz_outter + 端板牆；襯砌材料/裂縫律；界面位移場 `couple_interface_disp_s4.txt`；QA/繪圖腳本(`couple_qa_funcs.fis`、`couple_arch_qa_plot.py`、`fracture_track.fis`)。

**變更**：
1. **圍岩層2-6 → 單一等值彈性**：勁度用**柔度匹配**（校正使耦合重現小模 y860-910 局部柔度；小模 l4 砂頁岩 WET E=1.5GPa 為弱層、可能主導；非加權平均）。基準/軟/硬三組敏感度。
2. **驅動界面控制環**：把小模界面位移(residual、扣剛體)加在**緊鄰襯砌的圍岩側 gp(r4.7-5.3m)**、逐階段增量（非遠 box r20m）。需 IDW 映射小模場→耦合界面 gp（類 couple_idw.py 但目標=界面環）。
3. **釋放 w_inner**（內剛性背檔）→ 襯砌可向內變形；保留 wz_outter 耦合 + w_860/910 端板。
4. **最小 anti-drift 約束**（防剛體漂移、不約束變形）。
5. **逐階段增量、階段間不重置裂縫**（Codex）。

## 驗證（用裂縫前必過）
重現小模 y860-910 閉合（crown-invert≈0.75mm、springline≈1.07mm；s4_diam/band_conv 為 target）容差內。force balance：外力(圍岩→襯砌)、內力、反力閉合。

## Pilot 優先（Codex）
先小型/快速 pilot 驗證「界面驅動 + 閉合重現」可行 → 再放大全模。

## 視覺協定（Wade 鐵則：別改壞現有正確幾何）
每個幾何/BC 步驟：(a) Claude render+Read 自檢、(b) Codex 視覺複核、(c) 對照**你信任的現有 cb_control0 幾何基準**（先建立基準圖）。確認合理才下一步。

## 待決（下階段與 Codex 細談）
- 柔度匹配的具體程序（單次校正 run：對既有 layered Couple_Initial 施一組界面位移、量 closure → 反推等值 E）
- 界面驅動實作（IDW vs gp-ID；residual 扣剛體用 couple_idw 邏輯）
- anti-drift 約束的最小形式
- pilot 範圍（薄 y-slice？粗網格？或全幾何但先驗證流程）

## 開放風險
- 釋放 w_inner 後襯砌是否失穩（無內支承）→ 需 anti-drift + 漸進驅動 + 裂縫 breaker
- 單一彈性圍岩勁度若選不當 → 反力/裂縫失真（敏感度把關）
