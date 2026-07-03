# POST_REVIEW — production SMOKE stage-1: MID intact, y-end artifact persists (Option A insufficient)

日期 2026-06-29。BC fix A(排除 r<6m y-cap、23530 gp)後跑全 stage-1。

## 結果（全 stage-1 ramp 30×10、breaker 看中段）
- **MID-TUNNEL(y866-904)：全程 0 裂縫**(j=1→30、0→100% 驅動皆 dmid=0)。中段襯砌在 stage-1 載荷下**完整不裂** = 交付區明確結果。
- **END-BAND：11573 裂縫**(7032@y<866 + 4541@y>904)、99% 拉伸。r 分布 **r0-2m=4133/r2-4m=6107/r4-6m=1333 → 全在 r<6m、NOT 在 r≈6m cutoff**。
- wz_outter 1.838→**59.25MN(32×)**、w_inner 1.297→**37.57MN(29×)**——**total 被過驅動端帶污染、非中段真值**。
- pattern 圖：兩 y 端蓋密集馬蹄弧、中段 y=885 切片 0 裂。

## 診斷：Option A 不足、根因 = y-cap 軸向位移強加
- 端裂在 r<6m（已從 driven set 排除、未被直接驅動）→ 是**相鄰 r 6-8m y-cap driven gp 把未驅動的端部襯砌軸向過載**。
- ∴ 不論排除半徑多大，**y-cap 軸向強加小模位移在 cut 面**是本質問題（端部襯砌被軸向擠壓、與自然響應不符）。
- 但**中段離端遠、artifact 限端部、中段 0 裂穩健成立**。

## 候選修法（需 Codex 裁）
- **B**：y-cap roller(uy=0)、只用小模殘餘驅動側向 x/z 面。移除軸向強加。**疑慮**：小模是 submodel(6 面 fix)、耦合盒 y-cap 在小模內部會動(非 fix)→ roller 改變軸向 BC、與 submodel 不完全一致。
- **B'(hybrid)**：y-cap 只驅動**徑向分量(ux,uz)**、軸向(uy) roller。保留徑向 submodel 一致、移除軸向擠壓。較物理？
- **D(更大排除)**：排除 r<10-12m y-cap gp(端部襯砌+更多 rock 緩衝不被相鄰驅動)。但軸向強加本質還在。
- **C(接受+排除)**：保留現驅動、中段(y870-900)為交付、端帶 boundary-affected 排除。中段已證 0 裂、穩健。

## 需 Codex 裁決
- **Q1**：哪個修法？(B/B'/D/C)。我傾向 **B'(radial-only y-cap drive)** 最物理（保徑向 submodel、去軸向擠壓）；C 最省（中段已穩健 0 裂可直接交付）。
- **Q2**：中段 0 裂是否需確認「中段確實被載荷」（非 under-driven）？需抽 **mid-only wz_outter 力**（bf_couple 接觸在 y866-904 帶積分），現 total 59MN 被端污染、無法報中段襯砌反力。
- **Q3**：若中段 stage-1 0 裂成立，全 4 階段累積後中段是否最終開裂（裂縫 pattern 交付）？續驅動 s2-4。

附圖 sm_s1_rampend_crack_pattern.png。
