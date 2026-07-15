# 06 雙向耦合 — 執行版整合策略（2026-07-12 深夜，Fable；Wade 開工指令）

> **建置狀態（07-14）**：§7 全部檔案已建置完成。FLAC 腳本由 build_06_scripts.py 自
> 05 原始碼標記切片生成（零手抄）；make_cpl_resid06 對 05 產線資料逐位一致；
> make_damage_map_v2/make_shellE 合成資料單元測試全過（分箱/合併/護帶/單調/E表）。
> 執行順序：run_t5.py smoke → stage0 → ticks 26（斷點續跑靠 manifest）。
> 與 §2 的一處落差：小模 F_0 直接取 04 的 Small_Initial、s1 亦重跑（t01–t06 為
> 06 自身鏈，含 T=1.0 覆寫），確保前傳鏈全程自洽，不接 05 的 ss_01。

> 整合三份來源：Wade 07-12 開工指令（最高權重）、METHOD_TWO_WAY.md v1（Fable 07-07）、
> SOLAR.md 審查（GPT5.6_SOL 07-11）。凡三者衝突，Wade 指令優先，其次 SOLAR 數值安全建議。

## 0. Wade 指令與其實作對應

| Wade 指令 | 實作 |
|---|---|
| 只有小模／耦合模需要雙向，大模不重跑 | 大模驅動沿用 05 v6 定版檔（lg_disp_resid_s01 + s02-11），僅作小模邊界輸入 |
| 交替傳遞時機＝**每 5 天一次** | 11 階段拆成 **26 個 5 天 tick**：s1(30d)=t01–t06、s2–s5=t07–t10、s6(30d)=t11–t16、s7–s10=t17–t20、s11(30d)=t21–t26。30 天階段內水位面與大模邊界速度不變，逐 tick 推進 |
| 小模圍岩變形 → 耦合模「襯砌外力」 | 05 成熟前傳鏈：洞周累積位移 → Kabsch 剛體扣除 → ×f=0.25 → 耦合模邊界位移目標（位移驅動＝圍岩對襯砌之外力來源；增量 Δd=f(R_t−R_{t−1})，不重複載入） |
| 耦合模襯砌變形 → 小模「圍岩反力」 | **D→E secant 勁度回饋**：耦合模襯砌損傷場 D(s,y)（襯砌變形/開裂之狀態量）→ 小模殼元素 E=E0(1−D)^m 分區折減 → 小模圍岩感受的支撐反力隨之改變。此即「襯砌變形決定圍岩反力」之力學實現；**不做原始力回饋**（METHOD/SOLAR 一致：同介面同給位移+力＝過定，舊樹 Picard 發散實證），力回饋僅保留檔案介面作對照組 |
| 持續監控 CPU 與階段性成果 | orchestrator 逐 tick gate＋manifest；外掛 log 監視器＋CPU 看門狗 |

**5 天 tick 對耦合層級的意義**：Wade 的細時距交替＝把 METHOD 的 L1 交錯滯後由「一整個階段
（5–30 天）」縮到固定 5 天——顯式算子分裂的步長細化。SOLAR 的 L2 階段內 Picard 之必要性
因此下降；本執行版以 **T5（5-day staggered）為主線**，L2 降級為後續敏感度選項。

## 1. 鏈定義（狀態機依 SOLAR §3）

每 tick t（1…26）兩個 committed 狀態：F_t（小模 f3sav）、P_t（耦合 f3sav）＋ D_t（損傷圖）。

```
tick t：
  restore F_{t-1} → 套用 D_{t-1}→E 殼勁度（階段邊界單次寫入＋struct.force.update；t=1 用 E0）
              → 依 tick 所屬階段設定水位面/T 值/大模邊界速度 → 推進恰 5 天 creep
              → save F_t → 匯出洞周累積位移 u_t
  python：Kabsch(u_t) → R_t → 目標 d_t = f·R_t → 寫 drive_t06.txt
  restore P_{t-1} → 驅動至累積目標 d_t（ramp+calm 配方）→ save P_t
              → dump cracks/pmap/cwall → make_damage_map_v2 → D_t（供 t+1）
  gates 全過 → commit（manifest 原子寫入）
```

- **tick 所屬階段對照**：STAGE_OF_TICK=[1×6,2,3,4,5,6×6,7,8,9,10,11×6]；
  水位面/歷時/T 值（s1:T=1.0，s2–11:T=0.8）/大模驅動檔均由所屬階段決定
- 大模 30 天階段之邊界速度＝該階段平均速度（05 既有定義），6 個子 tick 沿用同一速度 ✓ 自洽

## 2. stage-0 重建（SOLAR §5.2/§5.4）

06 不沿用 05 的 cs_01（其已含 s1 載入）。專屬 stage-0：
```
restore Couple_Initial_G4 → v6 REBAND（隨縱坡錨定＋6階退火＋drift cleanup＋quiet）
  → CONTROL-0（零目標 ramp，收 D_control0 基線）→ save cs06_t00（committed P_0）
  → bond registry dump（可斷鍵：id、位置、s-y cell、anchored flag）＝損傷分母，全鏈固定
```
小模 F_0＝05 的 Small_Initial（開挖+殼+排水+位移歸零之平衡態，未被 06 改動、視為 immutable）。

## 3. 損傷映射 v2（SOLAR §5）

- 座標：tunnel_frame 局部框架，D(s,y)；分箱 s=周長站位 24 格 × y 5 帶（860–910）
- 分母：stage-0 bond registry（固定，不動態重算）；n_bond=0 → invalid（不回饋）；
  n_bond<8 → 併鄰格；y 首尾帶＝guard band（D 強制 0，端部效應不回饋）
- CONTROL-0 逐格基線扣除：n_net = n_total − n_control0
- D_raw 與 D_reg（鄰域 3 格滑動平均）並存，回饋用 D_reg；夾限 [0, 0.9]
- 不可逆：D̂_t ≥ D̂_{t−1}（逐格 max）——T5 無迭代，此即單調保證
- E 映射：E=E0(1−D)^m，m=1，樓地板 2.5 GPa；05 原 secant cap 改為**監測＋abort gate**
  （E_cap 記錄但不折減——單一損傷來源，SOLAR §7）
- 定位（SOLAR §8）：f=0.25 保留 → **趨勢級互制放大研究**；所有輸出標 f=0.25 trend

## 4. Gates（逐 tick，AND 制）

小模 tick：solve 完成 marker＋creep 時間恰 +5d＋殼 E 寫入筆數＝預期
耦合 tick：零 Illegal＋gp_dmax≈驅動增量量級＋斷鍵淨增 < 30,000（停線閾，沿用 v6）＋
ball_dmax 不失控成長；CONTROL-0 專屬：cracks≈基線量級、drift 有界
鏈級：t01（D=0）之小模行為 ≡ 單向 5 天切片（identity 檢查）；
manifest 記錄 parent/hash/gate 數字，failed tick 不得為 parent（fail closed）

## 5. 成本與排程

單 tick ≈ 小模 restore(1–2m)+5d creep(10–15m)+save/export(3m) ＋ python(1m) ＋
耦合 restore(3m)+drive(15–25m)+save/dump(4m) ≈ **40–55 min** → 26 ticks ≈ **18–24 h**
單 console 串行（鐵則），tick 內兩次啟動各留 65s 授權緩衝。
里程碑檢核點：t01（identity）、t06（s1 末=乾季基線）、t11–t16（雨峰、損傷主升段）、
t26（末態）→ 與 05 單向對照（放大係數）。

## 6. 對照組（後續，非本輪）

L0 feedback-off 26-tick 鏈（單雙向放大係數之嚴格分母）→ U1 均勻折減 → 敏感度（m、floor、f）。

## 7. 檔案介面

```
06/output/t5/   ss06_tNN.f3sav / cs06_tNN.f3sav（committed）
                cpl_bnd_tNN.txt / cpl_resid_tNN.txt（前傳）
                cs06_tNN_cracks/pmap/cwall.txt（耦合 dump）
                dmg_map_tNN.txt / shellE_tNN.txt（回饋）
                manifest.json（原子寫入；planned→running→produced→validated→committed）
06/process/     small_tick.f3dat.tpl / coupled_tick.f3dat.tpl（參數側檔生成）
                stage0_rebuild.f3dat / bond_registry_body.f3dat
                make_cpl_resid06.py / make_damage_map_v2.py / make_shellE.py
                run_t5.py（總指揮）
```
