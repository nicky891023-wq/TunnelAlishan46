# SOLAR — 06 雙向耦合 Workflow 架構審查與修正建議

> 審查日期：2026-07-11  
> 審查範圍：`06_Two_Way_Simulation` 的方法文件、損傷映射骨架、總指揮骨架，以及其與 05 單向鏈的資料契約  
> 技術基準：FLAC3D 6.00、PFC 6.0 與本專案現行 05 v6 工作流  
> 文件性質：設計審查與後續討論依據；不是開跑授權，也不代表已實作

## 0. 執行結論

06 的核心方向正確，建議保留：

- 小模向耦合模傳遞剛體扣除後的邊界位移；
- 耦合模向小模回傳襯砌損傷／等效勁度；
- 避免在同一組自由度同時完整指定力與位移；
- 先做低成本交錯式，再以濕峰階段的固定點迭代檢驗；
- 殼勁度只在階段邊界單次更新；
- CONTROL-0、品質 gate、manifest 與斷點續跑的設計方向。

但目前 06 仍是「可行的概念架構＋不可執行骨架」，不宜在現階段稱為「架構已定案的雙向強耦合」。真正需要補齊的不是交換量方向，而是：

1. 階段起點、trial 與 commit 的狀態管理；
2. 曲線／縱坡隧道下的一致座標與損傷分箱；
3. 初始可斷鍵分母與 CONTROL-0 基線；
4. `D → E` 的物理率定及與既有 shell cap 的關係；
5. 固定點殘差、收斂判定與未收斂處置；
6. PFC timestep scaling 對路徑相依破壞的適用性；
7. 05 成果凍結、輸入雜湊與可重現簿記。

SOLAR 的建議定位是：

> 先完成「趨勢級的跨尺度雙向互制放大研究」，以 L1 為主線、stage 6 的收斂 L2 為驗證；待 `DRIVE_SCALE`、`D → E` 與 timestep 路徑敏感度通過後，再決定是否升級為量值級預測。

## 1. 建議保留與重新命名

| 現行項目 | SOLAR 判斷 | 建議用語 |
|---|---|---|
| 位移前傳、損傷／勁度回傳 | 保留 | 跨尺度狀態交換 |
| L1 階段間回饋 | 保留，但不是強耦合 | 顯式交錯耦合／弱耦合 |
| L2 階段內 Picard | 保留並重構 | 迭代式分割耦合／固定點耦合 |
| 收斂後的 L2 | 可稱較強形式 | 收斂的階段內強耦合 |
| 整個 06 | 不建議直接稱強耦合 | 跨尺度雙向分割耦合框架 |

本案是兩個重疊尺度模型間的狀態回饋，不是典型的單一域 monolithic coupling，也不是標準非重疊域分解。論文中使用「雙向耦合」合理，但應清楚限定其為 partitioned／staggered multiscale feedback。

## 2. L1 滯後的物理意義必須改寫

`docs/METHOD_TWO_WAY.md` 目前以「水位階段 5–30 天遠大於開裂瞬時」支持一階段滯後。這個推論不足：若開裂相對瞬時，反而表示損傷造成的勁度改變應在同一水位階段內影響收斂，而不是等到下一階段。

因此：

- L1 的一階段滯後應被定義為顯式算子分裂近似；
- L1 可因成本、穩定性與工程時程成為主線；
- L1 的合理性必須由收斂 L2 的差異量化支持；
- 只有在 L2 使用相同初始狀態、相同映射律、相同求解設定且真正收斂時，L1–L2 的差才可解釋為分裂／滯後誤差；
- 若 L2 在迭代上限內未收斂，不能把最後一次 trial 當成強耦合真值。

成本敘述也應釐清：L1 本身所需的小模與耦合模階段數，與重新跑一條單向鏈大致同階；「約 2×」只有在把既有 05 baseline 加上新增 06 L1 一起計算時才成立。

## 3. 正確的 stage-start／trial／commit 狀態機

### 3.1 必要狀態

每個 stage `k` 的起點至少必須固定三份不可變狀態：

- `F_{k-1}`：小模 FLAC 狀態，包括 zone stress、pore pressure、creep state、shell property、shell force 與物理累積時間；
- `P_{k-1}`：耦合模 PFC 狀態，包括 ball／contact state、既有斷鍵、位移基準與邊界狀態；
- `D_{k-1}`：上一個已提交的損傷場。

trial 不可覆寫 stage-start，只有通過 gate 的成對 FLAC／PFC 結果才能 commit。

### 3.2 L1 正確流程

```text
restore F_{k-1}
  → 在階段邊界套用 D_{k-1}
  → 只推進一次實際階段 Δt_k
  → 產生 F_k 與邊界位移 u_k

restore P_{k-1}
  → 由既有累積位移推至新的累積目標 u_k
  → 準靜態平衡一次
  → 產生 P_k 與 D_k

通過 gates
  → commit (F_k, P_k, D_k)
  → D_k 於 stage k+1 回饋
```

### 3.3 L2 正確流程

```text
stage-k 起點固定：F_{k-1}, P_{k-1}, D_{k-1}

for iteration i:
    restore F_{k-1}
    apply D_hat_i once
    advance exactly Δt_k once
    export u_i

    restore P_{k-1}
    drive to u_i once
    extract D_raw_i

    evaluate fixed-point residuals
    relax D_hat_(i+1)

    if all convergence gates pass:
        commit the paired FLAC/PFC trial
        advance to stage k+1
```

兩項禁止事項：

1. 不可從前一次 FLAC trial 繼續推進，否則 3 次 Picard 會變成 3 倍潛變時間；
2. 不可從前一次 PFC trial 繼續斷鍵，否則數值迭代會被誤算成多次實際載入。

`run_twoway.py` 實作時應把 `stage_start`、`trial_i`、`commit` 做成明確狀態，而不是只用檔名慣例隱含判斷。

## 4. 收斂判準必須從 OR 改為 AND

目前文件使用：

```text
洞壁位移變化 < 5% OR 裂縫數變化 < 10% OR max 3 iterations
```

這會造成其中一個總量暫時穩定、另一個空間場仍漂移時提前停止。建議至少使用：

```text
r_u = ||u_i - u_(i-1)|| / max(||u_i||, u_floor)
r_D = ||D_raw_i - D_hat_i||_w / max(||D_hat_i||_w, D_floor)

converged = (r_u < eps_u) AND (r_D < eps_D)
```

其中：

- `u` 應是洞壁位移場，不只是單一最大值；
- `D` 應是空間損傷向量，不只是總裂縫數；
- `w` 宜以初始可斷鍵數或代表面積加權；
- 分母必須有 floor，避免初始小量時相對誤差爆大；
- 既有 5% 與 10% 可先作 pilot 初值，但最終門檻應由 stage-6 收斂歷程決定；
- 反力／支撐力場可作第三個監測量，但不應取代 `r_u` 與 `r_D`。

`MAX_ITER=3` 是計算預算，不是收斂條件。三次未通過應標記 `non_converged`，停止該分支或退回 L1，不可自然提交最後一次 trial。

損傷不可逆性只相對於已提交的前一階段成立。欠鬆弛可允許 trial 間上下修正，但必須滿足：

```text
D_hat_(i+1) >= D_{k-1}
```

避免數值迭代造成跨階段癒合。

## 5. 損傷座標、分箱與分母必須重建

### 5.1 固定圓心已不符合現行模型

`process/make_damage_map.py` 仍使用：

```text
CX = 1297.0
CZ = 1747.5
feet = z <= 1745.30
```

但 05 已確認：

- 隧道中心線在平面內彎曲；
- 隧道有約 3.7% 縱坡；
- v6 拱腳錨定帶已改為隨 `y` 變化；
- `05/process/tunnel_frame.py` 已建立局部中心與展開周長座標。

建議將正式損傷場由 `D(theta_global,y)` 改為 `D(s,y)`：

- `s`：由參考構形計算的襯砌展開周長座標；
- `y`：隧道軸向座標；
- crown、springline、foot 由同一局部 frame 定義；
- PFC bond、crack event 與 FLAC shell element 共用同一個 reference registry；
- element／bond 的 cell assignment 一旦建立就固定，不應隨變形重新跳格。

### 5.2 分母必須來自實際 stage-0 committed state

現有 `bond_census_G4.txt` 是從原始 G4 狀態建立；但 v6 已在 crack tracking 前進行 grade-following re-band、退火與 drifter cleanup。這會改變哪些 bond 屬於可斷集合，也可能改變接觸總數。

因此 06 的正式分母應從：

> 完成 re-band、conditioning、CONTROL-0 基線處理後，實際要進入 stage 1 的 committed PFC state

建立一次性 bond registry，而不是繼續沿用 pristine G4 census。

每一條初始可斷 bond 至少應保存：

- stable bond／end IDs；
- reference cell ID；
- reference position；
- bond size／代表面積；
- breakable／anchored flag；
- 初始狀態版本與 run hash。

分母在整個兩向鏈中固定，不能用當前仍存在的 contacts 動態重算，否則接觸分離或刪除會讓分母縮小並虛增損傷率。

### 5.3 低樣本格不能直接相除

目前 24×5 census 共 120 格，其中可見：

- 15 格分母為 0；
- 最低非零格只有 4 條 bond；
- 多個拱腳／無仰拱區格子的樣本數極低。

因此不能只用：

```text
D = n_broken / max(n_bond, 1)
```

這會把零分母悄悄改成 1，造成一條事件就接近完全損傷。正式版本應：

- 強制檢查 census shape 必須為預期格數；
- `n_bond=0` 標成 invalid，不得假設為 1；
- 低於最低樣本數的 cell 合併、遮罩或以鄰域正則化；
- 保存 raw 與 regularized 兩套 D；
- 檢查 `sum(n_broken_cell)` 與基線扣除後的 crack event 總數守恆；
- 第一與第五軸向帶需視為端部 guard band，避免把耦合模型端部效應直接餵回小模；
- 中段結果可保留，端部以平滑 taper 過渡到未損傷區。

### 5.4 CONTROL-0 基線

現行 crack tracking 在 CONTROL-0 前啟動，因此後續累積裂縫可能包含數值坐床／conditioning 底噪。雙向回饋不能把這些事件直接解讀為服役損傷。

建議二擇一：

1. 建立通過 CONTROL-0 後的正式 stage-0 checkpoint，並從該基線重新開始事件統計；或
2. 保存 `D_control0(s,y)`，正式回饋使用 cell-wise 基線扣除。

不建議只扣除全域總數，因為底噪可能集中在局部區域。

### 5.5 建議資料格式

正式損傷介面宜至少包含：

```text
run_id stage iteration cell_id
s_lo s_hi y_lo y_hi
n_bond0 n_broken_control n_broken_total n_broken_net
D_raw D_regularized E_ratio
valid_cell guard_band flags
```

若 ball size 有明顯差異，建議另保留以 bond area 加權的損傷指標，避免一條小 bond 與一條大 bond 被視為完全等價。第一版仍可使用 count-based D，但必須在論文中說明這是一個微損傷代理量。

## 6. `D → E` 不是已率定的本構律

現行公式：

```text
E = E0 * (1 - D)^m
```

可作為第一版 surrogate，但不能直接稱為真實 RC 損傷本構，原因包括：

- BPM 斷鍵率不等於巨觀 Young's modulus 降幅；
- 斷鍵具有方向性、張剪模式與厚度位置差異；
- FLAC shell 的單一 isotropic `E` 同時改變膜與彎曲剛度；
- 真實鋼筋混凝土開裂後的彎曲與膜行為不會按同一比例下降；
- 現有 PFC 襯砌未明確表現配筋延性。

建議用語：

> 等效各向同性 secant 損傷映射

### 6.1 建議率定方式

至少做其中一種：

- PFC 襯砌 segment／coupon 的載入—卸載或小擾動 secant stiffness；
- PFC 環體局部區段的力—位移反算；
- 以相同邊界條件比較 PFC 受損區段與 FLAC shell strip 的等效剛度；
- 對 `m`、E floor 與空間平滑尺度做敏感度，而不是只跑單一值。

若尚未完成率定，論文主張應限於回饋趨勢與相對放大，不應把 E 降幅當成量值驗證。

## 7. 既有 shell cap 與映射 D 會形成雙重損傷源

`05/process/small_staged_v2.f3dat` 的 shell cap 會直接且永久降低 shell Young's modulus，並透過 `struct.force.update()` 影響下一個 solve。若 06 又在階段邊界施加映射 E，必須明確決定：

- 是覆寫既有 E；
- 是取 `min(E_map, E_cap)`；
- 還是允許 E 回升。

否則可能出現：

- 同一損傷被 cap 與 D 重複折減；
- 下一階段套圖時數值癒合；
- cap floor 與 damage-map floor 互相矛盾；
- 無法判別收斂增加究竟來自 PFC 回饋還是小模自身 cap。

SOLAR 建議主線採用：

1. PFC 映射 D 作為唯一跨階段物理勁度退化來源；
2. 原 shell cap 改為超限監測與 abort gate；
3. 若為穩定性必須保留 cap，另設「D + cap 正則化」敏感度組，不能再宣稱 D 是唯一損傷來源。

殼勁度更新仍應只在 stage-start restore 後做一次；同一 trial 內不得反覆更新。單元測試必須檢查固定變形下降 E 後的力變化、能量反應與動力擾動，避免重現過去反覆 `force.update` 所造成的能量注入。

## 8. `DRIVE_SCALE f` 決定 06 是趨勢級或量值級

若 PFC 端持續使用 `DRIVE_SCALE = 0.25`，小模因回饋多產生的位移也只會有四分之一進入 PFC。此時整個 feedback loop 是刻意降低 loop gain 的 surrogate，而不是完整物理閉環。

這不代表研究不能做，但必須選定定位：

### A. 趨勢級互制研究（SOLAR 建議先做）

- 保留既有 f；
- 研究單向與雙向的相對放大；
- 研究損傷局部化位置與水位階段差異；
- 所有絕對位移、裂縫數與 E 降幅都標示為縮放模型結果；
- 不任意用另一個經驗係數放大 D 來抵銷 f。

### B. 量值級預測

至少需要：

- 讓前向位移比例具備可辯護的物理／率定依據，理想上接近完整傳遞；
- 補足 BPM 的巨觀力學率定與配筋／殘餘承載機制；
- 完成 `D → E` 等效率定；
- 完成 timestep 模式與網格／粒徑敏感度；
- 使用現地位移、裂縫或襯砌剛度資料做外部校核。

在上述條件未完成前，建議不要把 06 寫成量值級預測。

## 9. PFC timestep scaling 是關鍵方法風險

PFC 6.0 官方文件指出，timestep scaling 適合快速尋找靜態平衡，但其路徑與時間尺度不具物理意義；對 path-dependent 非線性／非彈性問題不應直接視為物理路徑。

本案的 bond break、損傷局部化與後續勁度回饋正是路徑相依量，因此：

- timestep scaling 可保留於 assembly conditioning 或純平衡準備；
- 正式破壞載入至少需要一個 automatic-timestep 代表性對照；
- 若全尺寸成本過高，可先用縮小段、代表性 stage 6 或局部環段做敏感度；
- 比較項目應包含總損傷、空間 D、張／剪比例、反力與洞壁位移；
- 若兩種 timestep 模式差異顯著，06 只能定位為數值趨勢探索；
- 若差異在預先定義的容許範圍內，可把對照結果列為方法可信度證據。

官方依據：

`C:\Users\Wade\.agents\skills\pfc-itasca\references\chm_extracted\pfc\docproject\source\manual\pfc_model_components\pfc_model_formulation\timestep_constraints.html`

## 10. `run_twoway.py` 的必要重構

目前下列函式仍未實作：

- `small_stage()`；
- `export_drive()`；
- `coupled_stage()`；
- `relax_damage()`；
- `converged()`。

即使補上函式，現有簿記仍不足以安全續跑。

### 10.1 現有 resume 問題

程式重啟時 `dmg_prev = None`。若 `tag in manifest["done"]` 就直接 `continue`，程式不會從 manifest 重建該 stage 的 committed damage path；跳過完成項後，後續 stage 可能從錯誤的 `None` 或錯誤 trial 繼續。

manifest 不能只保存 `done` 字串，至少要記錄：

- run ID 與 branch（L0／L1／L2）；
- stage、iteration、status；
- parent FLAC／PFC checkpoint；
- applied D map 與 forward displacement map；
- executable 路徑與 solver version；
- script、input、parameter、map 的 hash；
- log 路徑、啟動／結束時間與 process exit code；
- 所有 gates、殘差與 PASS／FAIL；
- committed output hash；
- failure reason 與是否允許 resume。

建議狀態：

```text
planned → running → produced → validated → committed
                         └────→ failed
```

只有 `committed` 可作下一步 parent。

### 10.2 manifest 必須原子寫入

直接覆寫 `manifest.json` 可能在斷電或程序中止時留下半份 JSON。應使用 temporary file、flush、atomic replace，並保留上一版備份。

### 10.3 log 與 marker

目前 `run_console()` 可能讀到舊 log 的 done marker。正式版本應：

- 每個 run／stage／iteration 使用唯一 log；
- 驗證 log 建立時間晚於 process launch；
- 同時檢查 exit code、明確 PASS marker、必要產物與 hash；
- fail closed：沒有完整 PASS 證據就不得 commit；
- marker 出現後仍需確認 process 正常退出；
- error pattern 不應只限於 `Illegal geometry` 與 `*** An error`。

### 10.4 每個 trial 使用獨立工作目錄

禁止多個 trial 共用 `cs_s1_cracks.txt`、固定 log 或同名 sav。建議：

```text
output/<run_id>/
  l1/s06/i01/
  l2/s06/i01/
  l2/s06/i02/
```

這也能避免 Fable 與其他程序仍在調整 05 時互相覆寫。

### 10.5 solver host 必須鎖版並 smoke-test

技能資料對「FLAC3D 6 console 載入 PFC」提出 GUI-bound 風險；但本專案現行 log 又顯示 FLAC3D 6.00 Release 069 以 `program load module 'pfc'` 實際進入 cycling。兩者不能靠假設裁決。

建議：

- 不在 06 開工時任意切換 host；
- 把 small solver 與 coupled solver 分成兩個明確 profile；
- 鎖定已驗證的 executable、release、module load 方式與呼叫語法；
- 每個 profile 先做 restore／cycle／save／quit smoke test；
- smoke test 通過後才允許正式 run；
- manifest 保存實際 executable 與版本。

## 11. 05 輸入必須先凍結，不可直接引用 live 檔名

`input/README.md` 現在建議用符號連結或相對路徑直接引用 05。這在 05 仍由 Fable 重跑時有高度風險：同一資料夾中的 `cs_s1`、`cs_s6`、`cs_s11` 可能來自不同輪次，單看檔名無法辨認世代。

06 開工前應先建立唯一權威 baseline package：

```text
05/output/runs/<run_id>/
```

至少凍結：

- small／coupled stage-0 與各 committed checkpoints；
- 11 階段 forward displacement maps；
- CONTROL-0 與所有 gates；
- post-conditioning bond registry／census；
- scripts、parameter files 與 solver version；
- SHA-256 或等效內容 hash；
- 一份 machine-readable baseline manifest。

大型 sav 不一定要複製到 06，但被引用的 run 目錄必須視為 immutable，06 manifest 必須保存其絕對來源與 hash。不可只引用會持續被覆寫的通用檔名。

## 12. 建議的分階段落地順序

### Gate 0 — 凍結 05 authoritative baseline

- 05 主鏈完成；
- 所有接受的品質 gates 有明確 PASS；
- 不再混用不同輪次檔案；
- `DRIVE_SCALE` 與研究定位已書面定義；
- 輸入全部有 run ID 與 hash。

### Gate 1 — 離線 mapping contract

- 建立 local tunnel frame；
- 建立 post-conditioning bond registry；
- 建立 shell element reference registry；
- 完成 PFC cell → FLAC shell cell 對照；
- 通過 count／area 守恆；
- 處理零分母、低樣本與 guard bands；
- 不啟動 FLAC／PFC 長跑即可測試。

### Gate 2 — shell E 更新單元測試

至少包含：

1. `D=0`：stage-by-stage 版本必須重現 05 baseline；
2. uniform D：整體反力／剛度變化方向與預期一致；
3. localized D：局部軟化不造成非物理能量尖峰或格線跳變；
4. restore 相同 stage-start 重跑結果可重現；
5. 一個 trial 只推進一次指定物理時間。

### Gate 3 — orchestrator mock／dry run

- 不呼叫 solver；
- 驗證工作目錄、唯一檔名、manifest、hash 與 resume；
- 人為中斷後可以從最後 committed state 正確重啟；
- failed／non-converged trial 不會被誤當 parent。

### Gate 4 — stage 6 單階段 pilot

- 從固定的 stage-5 start 同時建立 FLAC／PFC trial；
- 先跑 feedback-off identity；
- 再跑一個 L1 pass；
- 再跑 L2，觀察 `r_u`、`r_D`、ω 與迭代歷程；
- 做至少一個 timestep-mode 對照或縮小模型驗證；
- 未收斂時停止，不直接擴張到 11 階段。

### Gate 5 — 完整 L1

- 11 階段皆使用 06 自己的 committed chain；
- 不 restore 回 05 的 `ss_k` 或原始 G4 來跳過歷史；
- 每階段保存 forward map、damage map、gates 與 commit manifest；
- feedback-off 分支可重現一單向結果。

### Gate 6 — L2／hybrid 驗證鏈

- stage 1–4 可由相同 L1 checkpoint 起始；
- stage 5–7 進行階段內迭代；
- stage 8–11 必須沿 L2 已改變的 committed state 繼續；
- 不可在 stage 7 後接回 L1 checkpoint；
- 量化 L1 與收斂 L2 的差異。

### Gate 7 — 敏感度與論文產出

最少檢查：

- `D → E` 指數／floor；
- 空間平滑尺度與 cell resolution；
- under-relaxation；
- `DRIVE_SCALE`；
- timestep mode；
- uniform degradation vs localized degradation。

## 13. 建議對照組

| 組別 | 回饋方式 | 目的 |
|---|---|---|
| L0 | feedback off | 重現 05 單向 baseline |
| U1 | 使用與 mapped D 相同平均值的均勻 E 折減 | 分離「平均軟化」與「空間局部化」效果 |
| L1 | 空間 D、階段間顯式交錯 | 低成本主線 |
| L2 | 空間 D、階段內固定點迭代 | 檢驗 L1 分裂／滯後誤差 |

若時間有限，優先順序為 L0 → L1 → stage-6 L2 → U1。

## 14. 建議主要量化指標

### 14.1 耦合反應

- 洞壁位移場與水平／垂直收斂；
- 襯砌反力／接觸力分布；
- 空間損傷 `D(s,y)`；
- stage damage increment 與 damage rate；
- 單向／雙向位移放大係數；
- 單向／雙向損傷放大係數。

### 14.2 數值可信度

- 每次 iteration 的 `r_u` 與 `r_D`；
- accepted／rejected trial；
- CONTROL-0 漂移與底噪；
- zero-feedback reproduction error；
- timestep-mode sensitivity；
- mapping 守恆誤差；
- stage-start restore reproducibility。

### 14.3 不建議單獨使用的指標

- 只看總 crack count；
- 只看最大位移；
- 只看全域平均 D；
- 只用最後一次 iteration 與 iteration 上限判定成功。

## 15. 論文建議寫法

### 15.1 建議章節名稱

> 跨尺度雙向分割耦合方法：由襯砌微損傷至連續體等效勁度回饋

### 15.2 建議方法敘事

可將貢獻寫成：

> 本研究建立重疊尺度模型間的 partitioned two-way feedback framework。連續體小尺度模型提供去除剛體運動後的邊界變形，離散體襯砌模型回傳空間分布的等效損傷指標，並轉換為連續體 shell 的等效 secant stiffness。研究以顯式交錯法作主要計算鏈，並在高損傷水位階段以固定點迭代評估分裂誤差與回饋放大效應。

### 15.3 建議研究問題

1. 襯砌損傷回饋是否顯著放大隧道收斂？
2. 放大主要發生在哪些水位階段與空間位置？
3. 均勻軟化與空間局部化軟化的差異多大？
4. L1 相對於收斂 L2 的分裂誤差是否可接受？
5. 結果對 `D → E`、f、平滑尺度與 timestep mode 是否穩健？

### 15.4 必須誠實揭露的界線

- `DRIVE_SCALE < 1` 時，結果是縮放後的互制趨勢；
- BPM 斷鍵是微損傷事件，不直接等同巨觀裂縫寬度；
- scalar shell E 是等效各向同性 surrogate；
- PFC 襯砌未完整表現配筋延性；
- timestep scaling 的破壞路徑不是實際時間歷程；
- L1 的一階段 lag 是數值分裂，不是自然物理延遲；
- 只有收斂 L2 才可作較強耦合參考。

### 15.5 建議成果圖

- 單向、L1、L2 的收斂歷時比較；
- `D(s,y)` 階段演化圖；
- Picard iteration residual 圖；
- 均勻軟化 vs 空間映射的對照；
- 單向／雙向位移與損傷放大係數；
- timestep-mode 與 mapping 參數敏感度；
- stage-start／trial／commit 方法示意圖。

## 16. 檔案層級審查摘要

### `README.md`

- 「架構已定案」建議改成「初版架構／待前置 gates 驗證」；
- 「雙向強耦合」建議改成「雙向分割耦合」；
- L1 的物理正當性改為數值近似並待 L2 量化；
- 成本敘述標明是「05 baseline + 06 rerun」或「單一 L1 run」。

### `docs/METHOD_TWO_WAY.md`

- 明確增加 stage-start／trial／commit；
- L2 每次 iteration restore 同一 stage-start；
- 收斂由 OR 改 AND；
- 總 crack count 改為空間 D residual；
- max iteration 改為 non-convergence gate；
- 新增 local tunnel frame、bond registry 與 post-conditioning census；
- 明確選擇 shell cap 與 mapped D 的唯一／雙重來源；
- 新增 trend-level／quantitative-level 的研究定位。

### `process/make_damage_map.py`

- 移除固定圓心／固定 feet z；
- 改用 reference `cell_id`；
- `np.loadtxt(..., ndmin=2)` 處理單筆／空檔；
- 強制驗證 census shape；
- 零分母不得設成 1；
- 加入 CONTROL-0 cell-wise baseline；
- 加入 low-count flag、guard-band flag、raw／regularized D；
- 加入 run ID、stage、iteration 與 input hash；
- 檢查事件數守恆。

### `process/run_twoway.py`

- 完成五個未實作函式前不可啟用；
- 重構成 immutable stage-start／trial／commit；
- manifest 原子寫入並保存 parent、hash、gate、solver version；
- resume 時由 committed manifest 重建 `dmg_prev`；
- 每個 trial 獨立工作目錄與 log；
- stale marker、exit code 與產物 hash 三重驗證；
- L1 與 L2 必須是明確分支，不能只靠 `WET_STAGES` 隱式混合；
- max iteration 未收斂不得自動進下一階段。

### `input/README.md`

- 不建議引用持續變動的 05 通用檔名；
- 改為引用 immutable baseline run ID 與 hash；
- 大型 sav 可不複製，但來源不得在 06 執行期間被覆寫。

## 17. 開工前硬性 checklist（SOLAR 版）

- [ ] 05 authoritative baseline 已凍結且不再混世代
- [ ] 所有 baseline scripts／parameters／saves／maps 有 hash
- [ ] post-conditioning stage-0 PFC checkpoint 已定義
- [ ] CONTROL-0 cell-wise baseline 已定義
- [ ] local tunnel frame 與 reference cell registry 已完成
- [ ] bond census 與 crack events 守恆
- [ ] 零分母與低樣本 cell 已處理
- [ ] PFC → FLAC shell element mapping 已單元測試
- [ ] `D=0` 可重現 05
- [ ] uniform-D 與 localized-D 測試通過
- [ ] shell cap 與 mapped D 的關係已定案
- [ ] `D → E` 定位為已率定或明確標註 surrogate
- [ ] `DRIVE_SCALE` 對應 trend／quantitative 定位已定案
- [ ] stage-start／trial／commit 狀態機已實作
- [ ] manifest resume／crash test 通過
- [ ] stale log marker 不會造成假 PASS
- [ ] stage-6 L2 pilot 的 `r_u`、`r_D` 同時收斂
- [ ] timestep-mode 代表性敏感度已完成或列為限制
- [ ] 未收斂 trial 會 fail closed

## 18. 最終建議

06 最值得保留的研究核心不是「把兩個模型互相接上」本身，而是：

1. 用可追溯的微損傷場回饋連續體支撐勁度；
2. 區分空間局部化軟化與均勻軟化；
3. 用 L2 收斂解檢驗低成本 L1 的分裂誤差；
4. 量化襯砌損傷—圍岩收斂的正回饋放大。

若先以趨勢級研究完成上述四點，06 已具有足夠清楚的方法論價值。若直接跳到量值級「強耦合預測」，目前的 f、`D → E`、shell cap、座標分箱與 timestep 路徑問題會同時成為審查弱點。

因此建議順序仍是：

> 凍結 05 → 離線 mapping contract → D=0 identity → stage-6 L2 pilot → 完整 L1 → hybrid L2 → 敏感度與論文定稿。

在上述前置 gates 未通過前，`run_twoway.py` 應維持不可執行狀態。
