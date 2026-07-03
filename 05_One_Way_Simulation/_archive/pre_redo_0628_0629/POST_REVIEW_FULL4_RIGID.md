# POST_REVIEW — FINAL 4-stage production (rigid w_inner) COMPLETE

日期 2026-06-29。Codex SMOKE-BP-VERDICT 後執行全 4 階段累積生產（Option C、交付中段 y870-900、端帶排除）。

## 中段交付結果（rigid w_inner、累積 s1-4）
| 量 | s1 | s2 | s3 | s4 |
|---|---|---|---|---|
| **中段裂縫** | 0 | 2 | 5 | 5 |
| 中段反力 sum_normal (MN) | 6.00 | 6.03 | 5.86 | — |
| 中段反力 abs_normal (MN) | 7.32 | 7.34 | 7.17 | 7.17 |
| 中段收斂 max (mm) | 0.045 | 0.061 | 0.085 | 0.147 |
| 中段收斂 mean (mm) | ~0 | ~0 | ~0 | ~0 |
| wz_total (端污染) | 52.2 | 61.9 | 61.6 | 64.7 |
| w_inner | 40.4 | 51.2 | 51.1 | 55.8 |
| 端帶裂縫(排除) | 12698 | 14476 | 14527 | 16925 |

- final_abort=0（4 階段全跑完、中段 breaker 未觸、guard PASS）。每階段存 cb_full_s{1-4}。
- **中段裂縫 pattern**：5 個全 tension、緊密 cluster 在 **y~880.6、z=1745(仰拱、低於中心 z1747.5)、r~2.5m、ang 260-265°**。= 中段襯砌**一處局部仰拱拉伸裂縫**、onset s2、s4 飽和 5。
- 圖：couple_evolution.png（中段裂縫/反力/收斂 vs 階段、端帶 twin 軸排除）、full_s4_crack_pattern.png（端帶主導、中段需專屬圖）。

## 詮釋
- 中段襯砌在 stage-1-4 累積載荷下 **largely intact、僅一處局部仰拱拉伸開裂(5 鍵)**。
- 中段確被驅動：收斂漸增 0.045→0.147mm（接近小模隧道壁 0.22mm）、反力 ~7MN(6× in-situ)。
- 仰拱先裂物理合理（隧道仰拱常為拉應力集中處）。

## 🚨 需 Codex 確認的 caveat
- **中段反力 plateau(~7MN) 而 total wz 增(52→65MN)**：s3→s4 增量(0.46mm)主要被端帶吸收(端裂+2400)、中段反力幾乎不變。但中段收斂仍增(0.085→0.147mm)、裂縫 0→2→5→5 漸增。
- **問題**：中段是否 partly under-driven（端帶 cascade 吸收驅動）？或這是剛性襯砌+局部仰拱破壞的合理表現（收斂+裂縫漸增證被驅動、反力 plateau 因襯砌軟化/界面力上限）？
- **Q1**：接受 rigid 中段結果（5 仰拱拉伸裂、robust）為交付？
- **Q2**：中段反力 plateau 是否需查（如比較 cb_control0 的中段 in-situ 反力、確認 drive-induced 增量）？
- **Q3**：進 free w_inner 敏感度案（界定 w_inner 剛性影響上下界）？

附 couple_evolution.png。
