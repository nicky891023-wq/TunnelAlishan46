# REVIEW_PACKET #02 — Phase 1 (lining reaction) + Phase 2 (coupled drive)

- 日期 2026-06-29。Gate-0 已 PASS WITH CONDITIONS。本 packet = Claude↔Codex 討論 + Phase 2 執行前審查。
- 角色 (Wade 再申明)：大模=區域應力/位移場(已完成、endmember)；小模=隧道圍岩應力/位移場(已完成)；**耦合=汲取小模各階段位移當外力(不水流/不潛變)、聚焦襯砌受力+裂縫 pattern+圍岩互制**(核心交付)。

## A. Phase 1 進度 + 一個需共識的問題

**收斂 (works, 遵 Gate-0 C6 從隧道壁參考點抽)**：crown/springR radial_inward ≈ **0.22mm**(s4_s1)、遠小於 global dmax 3.22mm → **確認 Codex item3:襯砌剛、global dmax≠隧道收斂**。✅

**🚨襯砌反力結構問題 (需 Codex 共識)**：小模「lining」群組(slot mat 與 type 皆='lining')= **335011 zone、徑向 r 0-9m**(hist peak 3-4m、外緣 ~5m、尾 9+m)、**非薄 0.4m 噴凝環**。run_small_init 確認 lining="wished-in-place"(與圍岩共節點、無開挖空洞、彈性襯砌與圍岩共置)。我用「per-lining-zone 最遠徑向面」做 virtual interface traction → **net|F| garbage (8.4e14MN、area 為負巨值)**，因外緣面在此模糊結構上無法乾淨識別。
**問題**：E1 一致性檢核(小模襯砌反力 vs 耦合 wz_outter 1.88MN)的「小模襯砌反力」該怎麼抽？選項：
- (a) 在固定徑向(~r5m 襯砌-圍岩界)做虛擬圓柱切面、積分通過該面的淨力(rock 側或 lining 側 traction);
- (b) 支撐壓力 = 襯砌外緣平均徑向應力 × 隧道壁面積;
- (c) 沿 y=885 斷面、在 r=4.5-5m 環帶積分 σ·n·A。
請 Codex 裁定哪個方法、或指出小模「lining」結構是否如預期(填滿 r<5m 無空洞)。

## B. Phase 2 (耦合驅動) — 執行前審查

**方法 (workflow synthesis + Gate-0 條件)**：
1. restore Couple_Initial + pfc/wallzone + largestrain on + **timestep scale (dt=1)**。
2. 讀小模每階段位移(已重抽 bc:修正門檻小模 s4_s1..4)→ IDW 映射耦合外圍岩邊界 28304 gp → **扣全剛體、驅動 deformational residual**(Codex A(c)、couple_idw.py 已加、報剛體量)。
3. **ball damp 0.8**、**zone gridpoint fix velocity** 先於 gp.vel、**sub-step ramp + model calm**。
4. **Control-0 (零增量驅動 gate)**:datum reset + baseline 斷鍵 + 零增量 → 應 ~0 新裂縫;若殘餘 6.1e-3 自帶假裂則先重平衡 Couple_Initial_eq(Codex REVIEW#01)。
5. **no-damage transfer 對照**(暫提鍵強→驗轉移機制不靠破壞即可平衡)。
6. **SMOKE stage-1 短 ramp** 先(target-error abort + fish-halt max ball vel + 裂縫斷路器) → 驗機制不過裂 → 全 4 階段。
7. fracture_track(zmax 已修)→ DFN crack_tension/crack_shear;每階段記 wz_outter + 裂縫 pattern。
8. **w_inner**:Wade 定**保留剛性=主案**;Codex/workflow 要 **free-inner 對照=mandatory sensitivity** → **兩案都跑**(rigid 主、free 界定剛性影響上下界)。

**需 Codex 共識**：(1) §A 的襯砌反力抽法;(2) 確認剛體 residual + Control-0 + no-damage 順序與 SMOKE-first;(3) over-cracking 斷路器門檻(單 sub-step 裂縫增量上限);(4) w_inner 雙案是否足夠。

## C. 待 Codex
GATE / CONSENSUS 回覆:Phase 1 反力抽法 + Phase 2 准予(SMOKE first) / 條件 / 退回。
