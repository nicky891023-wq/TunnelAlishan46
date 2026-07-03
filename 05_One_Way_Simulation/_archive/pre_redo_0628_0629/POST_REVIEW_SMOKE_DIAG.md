# POST_REVIEW — SMOKE diagnostic: crack onset is a y-end-cap BOUNDARY ARTIFACT

日期 2026-06-29。SMOKE stage-1 在 j=2 觸發斷路器(151 裂縫)。診斷後送審。

## Workflow 對抗審查(18 agents)抓到的 bug（已處理）
- **CRITICAL fracture_track.fis:11** `entries(3)`(=bond 失敗強度 force) 誤當 mode → `if mode=1/2` 永遠 false → **crack_tension/crack_shear DFN 從未建立 → QA dump 空**。已修 `entries(2)`（對 PFC linearpbond cmlinearpbond.html Table3 + 官方 fracture.p3fis 驗證）。修後診斷 QA 非空(949 裂縫正確分類)。
- **major velocity-drive**: 斷路器設 abort_flag 但腳本不分支、照樣 solve/save 把破裂態存成「完成 stage-1」。待生產版修。
- minor: couple_idw.py 註解誤導(碼正確、已修防 regression)；QA header「axial band」未實作。

## 診斷結果（crack-track 修正後、高斷路器 cum>500 見演化）
- **949 純拉伸裂縫(0 剪切)**、加速 cascade：j1=0 → j2=151 → j3=465 → j4=949。
- **致命空間特徵**：裂縫 y 分布 = **763 @ y[860-865] + 186 @ y[905-910]、中段 y[865-905] 40m 完全 0 裂縫**。crack r=1.35-4.70m（襯砌/核心）。sectors 集中拱頂(90-120°)。
- **wz_outter 1.838→26.28MN(14×)**，且 **Fy=16.2MN 大軸向 + Fx=-20.1MN 不對稱**（非純徑向收斂）。
- guard PASS(0 裂縫零增量、cb_control0 真 stationary)——裂縫純驅動誘發。

## 診斷：y 端蓋驅動的 BOUNDARY ARTIFACT
- couple_bnd.txt 的 28304 driven gp = 外盒邊界(x±19.5/y[860.5,909.5]/z±19.5)。其中 **r<6m 的 4774 gp 全在 y 端蓋**（隧道斷面在 cut 面、含襯砌/核心相鄰 gp）。
- 用小模殘餘**直接驅動 y 端蓋的襯砌/核心 gp** → 過載端部襯砌 → 拉伸破壞集中 y 端 ±4.5m。
- **中段隧道（真正關注區）在 13% stage-1 驅動下 0 裂縫** → 物理上襯砌中段尚未破壞。
- wz_outter 大軸向力 Fy=16.2MN 直接證實 y 端軸向過驅動。

## 需 Codex 裁決：y 端 BC 修法
- **選項 A**：driven set 排除 y 端蓋 r<6m 的襯砌/核心 gp（只驅動 rock 邊界）。重生 couple_bnd.txt+IDW+targets。端部襯砌不被直接驅。
- **選項 B**：y 端蓋改 roller(uy=0、徑向自由)、只用小模殘餘驅動側向(x,z)面 = 標準隧道切片 plane-strain-ish BC。
- **選項 C**：保留驅動、但裂縫分析(breaker+QA)只取中段(y 870-900)、y 端視為 boundary-affected 排除。風險：端部 cascade 可能應力重分配污染中段。
- **Q1**：哪個 BC 修法？(A 最乾淨但需重抽；B 最物理；C 最快但有污染風險)
- **Q2（已查）**：小模是 submodel、6 盒面全 `fix velocity`(held at parent)、focus 區 y860-910 匯出。耦合盒(y860.5-909.5)在小模內部、用小模**內部位移場**驅動耦合盒邊界。根因：y 端蓋把小模位移場**硬加(kinematic)在端部襯砌/核心 gp** → 與脆性襯砌自然響應不符 → 應力集中開裂；中段襯砌經 rock 軟響應不裂。傾向**選項 A**(driven set 排除端部 r<6m 襯砌/核心 gp、襯砌只經 rock 受驅)。
- **Q3**：中段 13% 0 裂縫——是否續驅動全 stage-1 看中段是否最終開裂(中段才是襯砌受力/裂縫 pattern 的交付)？

附圖 smdiag_crack_pattern.png（3D 兩弧帶在 y 端、y=885 中段切片 0 裂縫、sectors 拱頂集中）。
