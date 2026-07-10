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
- **自由內面（STEP F，07-04 完成）**：刪 w_inner → 12k-cycle 再收斂後首驗未過（新斷鍵 48、球位移 0.284 m）。
  診斷＝**46 顆散球**（原本卡在內牆與環之間的自由球）飛脫，非環體下垂：movers 72/456k=0.016%、
  blue-line 環收斂平均 0.005 mm、拱角帶 0.065 mm。處置（couple_freeface_fix）：`>20mm` 散球刪除
  （46 顆）→ 再收斂 → 重驗 dmax 0.6 mm ✅ → **`output/Couple_Initial.f3sav`（=free2 定版）**。
  殘餘每段 +19/+23 斷鍵涓流經查為**真實拱肩張性微裂**（97% 拉斷、拱角/端部零）＝自由內面下的
  物理背景率；各階段裂縫增量一律**扣除 CONTROL-0 底噪**後解讀。
- **STEP G（07-05，staged 正式起點=`output/Couple_Initial_G.f3sav`）**：free2 的岩箱仍是剛性模具
  （servo 全域凍結未解除），STEP G v4 以**退火階梯**（E 1000×→1×E_eq 六階、掃除短腿、apply 清除、
  孤兒預清除、刪端平台）轉為增量彈性傳遞介質。一次性轉換成本：斷鍵 33,259（1.47%）、刪球 204。
  Post-mortem：冠部完好、損傷集中腳帶邊界與右春線（與 NO46 現場春線縱裂同型態）、洞內漂球僅 1。
  詳見 05/RUN_STATUS.md C1/C2 與 _diag_frozenrock_0704/。
- **STEP I（07-07，staged 最終起點=`output/Couple_Initial_G4.f3sav`）**：G3 力網仍揹 servo 鎖入力
  （預拉尾收割產生假裂縫，證據 05/…/_diag_prestress_harvest_0707/）→ **零重力原位重澆**：0g 下全
  unbond＋lin_force 歸零＋岩應力歸零 → D7 參數全新鍵結（微觀參數不變）、**bf 膠合僅 bf_couple 組
  62,556 個**（型別全綁 377k 會 6× 放大介面轉動勁度→積分不穩定，STEP I v1 實證）→ 重力五階爬回。
  E_eq=1.6GPa＝Wade 核准（l4 弱層）；介面勁度=zone E（穩定鐵則）。長期異常點 (1299.7,902.3,1748.4)
  卡力 307kN 於重澆時準靜態放電（一次性 ~755 鍵，計入 G4 基線）。

## 4. 使用注意

- 微觀參數與**粒徑綁定**：換粒徑分布必須重律定（pb_kn/pb_ks 單位是 stress/disp，非 force/length）。
- `contact.force.normal` 等讀值＝linear+dashpot+pbond 總和；鍵結內力用 `pb_force/pb_moment/pb_sigma/pb_tau`。
- 裂縫判準：`pb_state`（0=從未鍵結、1=拉斷、2=剪斷、3=完好）＋ `bond_break` 事件 → DFN；
  1e20/1e100 的耦合與拱角鍵結永不顯示為裂縫，統計時本來就排除（它們不可斷）。
