# POST_REVIEW — Control-0 gate result (Phase 2 coupled drive)

日期 2026-06-29。依治理：執行後提交 POST_REVIEW，等 Codex APPROVED / WITH CONDITIONS / BLOCKED 才進 SMOKE。

## 已落實的 Codex P2 條件
- ✅ **couple_idw.py 剛體 sign bug** 修正（`b += K@di` → `b -= K@di`）。驗證：residual RMS 1.21-1.56mm **< total RMS 1.43-1.95mm**（修前 residual>total）。剛體佔 53-60%（不扣會有 ~60% 假擠壓）。couple_bnd_disp.txt 重生為 deformational residual。
- ✅ **hard abort 計數**：Control-0 log 確認 driven=28304 / miss=0。
- ✅ **maxbvel 在 calm 前**取樣。
- ✅ **datum reset**（gp.disp/vel=0, ball disp×0）。
- ✅ **dt=1 已確認**：官方 PunchIndentation.f3dat 註解「so the PFC timestep will be 1」+ dt-check（restore cb_control0）DT0 after-restore mech.timestep=**1**。SMOKE 30×10→velocity 1.3e-5 m/s（比官方 punch 0.0001 m/s 更緩、準靜態）。

## Control-0 結果（零增量 gate）
| 量 | 值 | Codex 準則 | 判定 |
|---|---|---|---|
| new_cracks | **21** | ==0 | ✗ |
| driven_drift_max | **0.000mm** | <0.05mm | ✓ |
| maxbvel(終) | **8.98e-7** | 遞減/極低 | ✓ stationary |
| wz_outter | 1.882→**1.838MN** | drift<2% | ✗ (2.3%) |
| w_inner | 1.378→**1.297MN** | drift<2% | ✗ (5.9%) |

過程：sub-step 裂縫 2→13→14→15→21 緩增後**穩定**；maxbvel transient 後降至 9e-7。

## 我的詮釋 + 提案
1. **21 裂縫 = in-situ 一次性 settling**。Couple_Initial 組裝時殘餘 ratio 6.0954e-03（非 1e-4、cycle cap）。零增量再平衡把殘餘鬆弛掉 → 21 鍵斷（對襯砌數十萬鍵屬極微）+ 牆力降 2-6% 至真平衡。**maxbvel 9e-7 證明已 stationary、裂縫已穩、非持續破壞**。
2. **提案：SMOKE 從 cb_control0 驅動**（settled stationary 基準）、fracture_track **re-arm**（DFN baseline=0）→ 21 settling 裂縫已斷不重計、SMOKE 裂縫=**純驅動誘發**。牆力 baseline = cb_control0 settled（wz 1.838 / wi 1.297MN）。
3. driven_drift=0 證明速度邊界鎖定有效；驅動點不漂移。

## 需 Codex 裁決
- **Q1**：接受「SMOKE 從 cb_control0 驅動、21 裂縫視為 pre-drive settling」？或要求更深再平衡 / 第二次 Control-0（從 cb_control0 再零增量、驗 0 新裂縫=真 stationary）再進 SMOKE？（第二次 Control-0 約 +3hr）
- **Q2**：牆力 drift 2.3%/5.9% 是否可接受為「in-situ 鬆弛至真平衡」、以 cb_control0 settled 值為 SMOKE baseline？
- **Q3**：效能——耦合 ~2s/cycle、6000-cycle solve ~3hr。SMOKE/各階段 final solve 是否同意降至 ~2500-3000 cycle（ramp 已帶近平衡、耦合 plateau ~6e-3）以讓全 4 階段×2 w_inner 在合理時間完成？

SMOKE 腳本已備好+parse 驗過（從 cb_control0、dt assert、斷路器 30×10 / Δcrack_sub>50 / cum>200、maxbvel calm 前）。等 Codex 綠燈即跑。
