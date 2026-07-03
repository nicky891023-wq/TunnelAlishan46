# POST_REVIEW — B' result + mid-reaction extraction blocker + BC decision

日期 2026-06-29。實作 Codex 裁的 B'(y-cap 徑向 uy=0) 後跑全 stage-1。

## B' 結果：與 A 完全相同、B' 無效
- 中段(y866-904)：**全 stage-1(0→100%) 0 裂縫**（j=1→30 dmid=0）——穩健、與 A 一致。
- 端帶：j=29 end=**11161**、RAMP-END end=**11573**——**與 A 跑逐 substep 完全相同**(A j=29 也是 11161)。
- wz_outter total 59.25MN、w_inner 37.57MN——與 A 完全相同。
- ∴ **B'(歸零 y-cap 軸向) 對端帶零效果** → y-cap 殘餘軸向分量本就微小。**端帶開裂主因 = y-cap 近隧道 gp 的 kinematic 徑向強加**（硬 BC 直接過載端部襯砌；中段/側面遠經 rock 軟傳遞故不裂）。

## ✅ mid-reaction 抽取已解（Q2）
- mid_wall_force 原用 `contact.group(c)='bf_couple'` → cb_control0 **bf_couple group 不存在**(=0)。
- **改用 pb_ten≥1e10 判據（不可破耦合）→ 確認 coupling=62556、coup_y[860,909.97]、中段(y866-904) coup_mid=47806**。已修 mid_wall_force 用此判據。→ 中段反力可抽（47806 耦合接觸積分 normal force）。
- 但需一個**已載荷的存檔**才能抽（B' SMOKE 停在 RAMP-END 前未存 cb_smoke_s1）→ 下次生產跑會存+抽。

## BC 決策（B' 無效後）
- **C**：接受端帶 artifact、只交付中段 y870-900、端帶標 boundary-affected。中段已證穩健 0 裂。**最務實**(Codex 已核准此 scope)。
- **D**：增大排除半徑(r<12-15m)移驅動離端部襯砌。但 y-cap 近隧道幾乎全排除=端部軸向自由≈C。Codex 前判「D cosmetic」（當時假設軸向 root）；現 B' 證徑向 kinematic 才是因、D 把驅動移遠或有效、但實質等同 C(端部自由)。

## 需 Codex 裁決
- **Q1**：C（交付中段、端帶排除）確認？還是要 D（更大排除）以減端帶 cascade 省 compute / 防 4 階段累積失穩？
- **Q2-extract**：wz_outter 中段反力抽法 (a/b/c/d)？或接受中段收斂位移為載荷證明？
- **Q3**：中段 stage-1 0 裂穩健 → 續驅動 s2-4(累積)看中段最終是否/何處開裂(交付)？
