# PFC 襯砌微觀參數律定紀錄（D7 律定＋v6 安裝驗證）

> 目的：耦合模襯砌（linearpbond BPM）的微觀參數要讓「球體襯砌」宏觀等效於 D7 定案的
> R.C. 襯砌：**E = 25 GPa、UCS(fc) = 41.2 MPa、ft = 4.12 MPa（fc/ft=10）、t = 0.4 m、ρ = 2400**。
> 微觀參數不是人為指定，是律定輸出。本檔＝律定方法、最終參數、與 v6 安裝時的驗證數字。

## 1. 律定方法（UCS/直接拉伸 rig，2026-06-14~17 完成）

- 試體：與襯砌同粒徑（r 0.036–0.044 m 均勻分布、不規則排列）、同鍵結模型（linearpbond）的圓柱試體。
- 試驗：UCS（平板壓縮，`wall.force.contact`/斷面積）＋直接拉伸（grip 球反向拉），量測宏觀 E、UCS、ft。
- 迭代：從 provisional 起手（emod 7.1e9 / pb_emod 4.3e9 / pb_ten 1.4e6 / pb_coh 1.6e7），對 D7 目標逐輪修正。
- 破壞模式檢核：張斷主導（≈96% 拉伸斷鍵），符合脆性混凝土。

## 2. 最終微觀參數（FINAL，寫入 `parameter.f3dat`，全案唯一來源）

| 參數 | 值 | 說明 |
|---|---|---|
| `pfc_emod`（linear emod） | 9.65e9 Pa | 線性接觸等效模數 |
| `pfc_kratio` | 1.0 | kn/ks |
| `pfc_pb_emod` | 5.88e9 Pa | 平行鍵結等效模數 |
| `pfc_pb_krat` | 0.6 | pb kn/ks |
| `pfc_pb_ten` | 2.10e6 Pa | 鍵結抗拉（**裂縫來源**，可斷） |
| `pfc_pb_coh` | 2.30e7 Pa | 鍵結凝聚 |
| `pfc_pb_fa` | 25° | 鍵結摩擦角 |
| `pfc_bondgap` | 0.03 m | 鍵結/proximity 間隙 |
| `pfc_ball_den` | 2400 kg/m³ | 密度 |
| `pfc_ball_damp` | 0.7 | 局部阻尼（平衡期） |
| `pfc_fric` | 0.5 | 線性摩擦係數 |
| `pfc_bf_strong` | 1.0e20 Pa | ball-facet 對 wz_outter 的不可斷耦合（**非材料**，是數值耦合） |

**律定結果 vs 目標**：E 24.85 GPa（−0.6%）、UCS 41.2 MPa（0%）、ft 4.04 MPa（−1.9%）→ 全部在 ±2%。

## 3. v6 安裝時的組態與驗證（2026-07-03，couple_servo_v6）

- 選擇性鍵結：ball-ball 全域 linearpbond 可斷（D7 值）；ball-facet **僅 wz_outter** 1e20 不可斷
  （bf_couple = 62,556）；剛性牆接觸（w_860/w_910）維持純摩擦 linear（bf_rigid = 55,752）。
- **拱角條帶（D4/D6 新增）**：襯砌無仰拱、環底緣 z≈1744.85；z ≤ 1745.30 的 ball-ball 鍵結
  改 1e100 不可斷（**185,044 個**，佔全環約 20%）＝左右拱角錨定（跟岩壁走、不散不踢入）。
  側壁→頂拱關注區維持可斷 D7 → 裂縫都在關注區發展。
- 力自由安裝（lin_mode 1）＋ servo 孔壁漸進洩壓 → 圍束平衡（Couple_Initial_v6，07-03 22:47）。
- **安裝品質驗證**：圍束態真實斷鍵 **376 / ~907,000（0.04%）**、球位移 13.5 mm（servo 收斂行程）——
  襯砌本質完好，鍵結「待載入開裂」＝正確的 staged 起點。
- 自由內面（STEP F）：刪 w_inner 後 gate＝新增斷鍵 0、球擾動 mm 級 →（結果待 STEP F 完成回填）。

## 4. 使用注意

- 微觀參數與**粒徑綁定**：換粒徑分布必須重律定（pb_kn/pb_ks 單位是 stress/disp，非 force/length）。
- `contact.force.normal` 等讀值＝linear+dashpot+pbond 總和；鍵結內力用 `pb_force/pb_moment/pb_sigma/pb_tau`。
- 裂縫判準：`pb_state`（0=從未鍵結、1=拉斷、2=剪斷、3=完好）＋ `bond_break` 事件 → DFN；
  1e20/1e100 的耦合與拱角鍵結永不顯示為裂縫，統計時本來就排除（它們不可斷）。
