# Zhang Sulei et al. (2022) — Liwaiao Tunnel 襯砌裂損機制（排水系統劣化）

**書目（PDF 首頁核對）**：Sulei Zhang; Qing Xu; Chungsik Yoo*; Bo Min; Chang Liu; Xiaoming Guan; Pengfei Li (2022). Lining cracking mechanism of old highway tunnels caused by drainage system deterioration: A case study of Liwaiao Tunnel, Ningbo, China. *Engineering Failure Analysis*, 137, 106270. https://doi.org/10.1016/j.engfailanal.2022.106270
機構：青島理工大學／成均館大學（Yoo 通訊）／北京交通大學／北京工業大學。投稿時程：收 2021-08-24 → 修 2022-02-25 → 收錄 2022-03-21 → 上線 2022-03-23（約 7 個月）。
Keywords: Highway tunnels; Drainage system; Clogging; Lining crack; Water leakage; Finite element analysis.

**access = full-pdf**（本機 PDF 全文精讀，14 頁全讀）
精讀日期：2026-07-22。PDF：`07_SCI_TUST/References/PDF/1-s2.0-S1350630722002448-main.pdf`
（前版筆記為 abstract-only 佔位，本版全文覆寫 (a)–(h)。）

---

## (a) 題目解剖

原題：*Lining cracking mechanism of old highway tunnels caused by drainage system deterioration: A case study of Liwaiao Tunnel, Ningbo, China*

- **開頭元素**：機制先行——「Lining cracking mechanism」（失效現象＋機制詞）打頭，不是案例、不是方法。
- **構式拆解**（四段式）：
  1. `[失效現象+mechanism]` Lining cracking mechanism
  2. `[對象母體]` of old highway tunnels ——用「old」點出營運中/老化情境，把單案例上升為一類隧道
  3. `[成因歸屬]` caused by drainage system deterioration ——因果鏈直接寫進題目（排水劣化→裂縫）
  4. `[冒號+案例錨定]` A case study of Liwaiao Tunnel, Ningbo, China ——「隧道名, 城市, 國家」三級地名格式
- **有無方法詞**：**無**。全文主力其實是 ABAQUS 流固耦合＋XFEM 裂縫擴展，但題目一字不提；方法退居摘要（"fracture-based numerical models"）與 3.2 節。賣點是機制與成因。
- **題文對應（全文驗證）**：題目的三個承諾全文各有一節兌現——cracking mechanism→§3.3、drainage deterioration→§3.2.3 堵塞模擬＋§2.3 現場堵塞觀測、case study→§2＋§3.1。題目即目錄。
- **可複製模板**：`[Failure mechanism] of [old/operating + 隧道類別] caused by / induced by [驅動因子]: A case study of [隧道名], [城市], [國家]`

## (b) 文章架構與比重

正文 5 節、14 頁（含文獻 1.5 頁），**數值分析獨大**：

| 節 | 內容 | 約略篇幅 | 佔比 |
|---|---|---|---|
| 1. Introduction | 背景統計＋文獻回顧＋缺口＋貢獻 | 1 頁 | ~9% |
| 2. Crack and leakage distribution（11 隧道普查） | 檢測方法、634 條裂縫統計、387 處滲漏統計 | 2.5 頁 | ~22% |
| 3. Numerical investigation | 工程背景、FE 建模、堵塞過程模擬、水壓/內力/裂縫結果 | 5.5 頁 | ~48% |
| 4. Seepage water treatment measures（虹吸排水管） | 對策：拱腳鑽孔＋虹吸排水管構造與現場安裝 | 2 頁 | ~17% |
| 5. Conclusions | 5 條編號結論 | 0.5 頁 | ~4% |

- 敘事鏈＝EFA 典型案例文體：**現場失效觀測（統計化）→ 代表案例 → 數值重現機制 → 模型-現場對照 → 治理對策**。
- §2 的普查（11 隧道）與 §3 的單案例（Liwaiao）是「母體→樣本」設計：先用 634 條裂縫的統計建立「縱向裂縫為主、裂縫即滲漏弱點」的母體規律，再挑一條隧道做機制解剖——題目中 old highway tunnels（複數）與 case study（單數）的兩層結構在正文有實體對應。
- 參考文獻 27 篇，TUST 約 7 篇最多；含共同作者自引 4–5 篇（Liu/Zhang EFA 2021、Min、Li、Yoo 各系列）。

## (c) 前言手法

**共 3 段**，短而密（僅 1 頁）：

1. **段 1（宏觀＋問題界定）**：以全國統計開場——2020 年底中國公路隧道 21,316 座/21,999 km——立即接「老隧道長期營運後大量出現裂縫滲漏」；再給概念框架：排水系統狀態三分類（fully clogged / fully draining / limited drainage，多數山嶺隧道處於後兩態）、堵塞為物理/化學/生物過程（泥砂沉積、鈣質結晶、材料老化、圍岩壓力）。一段之內完成「大→問題→機制詞彙表」。
2. **段 2（文獻回顧＋缺口 staging）**：單段塞入約 12 組文獻，全用「人名＋動詞」句式（established / introduced / investigated / conducted / adopted / designed / discovered）逐一點名，每組一句。段尾三步缺口 staging：
   - 讓步肯定：前人已考慮圍岩-地下水-襯砌的水力-力學互制、"provide important constraints"；
   - 轉折限縮：However——既有研究多聚焦**堵塞後**的水壓分佈與應力狀態之局部規律；
   - 空缺宣告＋需求句：尚無關於**堵塞過程中**襯砌損傷的 comprehensive studies；"Additional studies are needed to" 揭示排水劣化導致的破壞型態與開裂機制。
   缺口的槓桿點是**時間維度**（after → during），不是方法維度。
3. **段 3（貢獻段）**："In this paper" 起手，流程敘事式貢獻句（investigated → selected → conducted → presented）：11 隧道普查 → Liwaiao 案例 → stress-pore-pressure-coupled＋fracture-based FE → 裂縫特徵/水壓分佈/應力狀態 → 治理建議；收尾一句用途承諾——結果將"helpful for the maintenance"（實用價值收束，不誇大理論貢獻）。

- **引語策略**：全文轉述、零直接引語；文獻只當墊腳石，一句帶過。
- 貢獻句式不用 novelty 詞（no "novel/first"），用「comprehensive／系統性流程」自證新意——與缺口宣告（no comprehensive studies）首尾互鎖。

## (d) 結果敘事

- **時間軸當敘事主線**：堵塞用「出水口滲透係數每 3 個月×3/4」離散化（k_n = k₀(3/4)ⁿ, n = t/90），此後所有結果都掛在 n 上講故事——"When n increased to 7 (after 21 months)..."。裂縫 1→4 依時序命名出場（21/30/33/36 個月），n=13 裂縫 1 近貫穿、結構喪失承載力——機制被寫成一部「失效編年史」。
- **圖領句範式**：每小節第一句必是 "Fig. X shows/gives..."，接讀圖句（"It can be seen that..."），再接詮釋句（"The results indicated that... / It can be inferred that..."）。圖→讀→釋三拍子貫穿 §3.3。
- **量化密度高**：關鍵數字直接入句——未堵塞時襯砌水壓僅 ~10 kPa 可忽略；末期側牆底 84 kPa vs 拱頂 52 kPa；n=6（18 個月）側牆底負彎矩 29 kN·m、側牆中正彎矩 23.2 kN·m、拱肩軸力 242 kN；裂縫 1 深 21 cm、裂縫 2 深 18 cm、皆呈 V 形。
- **空間×時間雙座標**：先按部位（拱頂/側牆/拱腳）比水壓增速，再按時間敘裂縫序列（拱腳→側牆中→拱肩內外），最後歸納「拱腳最危、縱向裂縫是弱點」呼應 §2 統計。
- **模型-現場閉環**：§3.3 收尾用 Fig. 21 把 FEM 開裂位置與現場照片並排，"consistent with the field survey results"——數值敘事以現場驗證封口，這是全文可信度的樞紐圖。
- 對照組寫法：二襯受水壓衝擊 vs 初支「透水、內外無壓差、幾乎不受影響」——用一個不受影響的構件反襯受影響構件，機制歸因更乾淨。

## (e) 貢獻凸顯

- **定位在「機制查明＋綜合流程」而非方法創新**：XFEM/耦合分析當工具寫，novelty 掛在（i）首次系統回答「堵塞**過程中**襯砌如何逐步開裂」（呼應缺口的 during vs after）；（ii）現場普查—數值—對策的完整閉環。
- **結論 5 條編號**，每條一個可攜帶的定量事實（縱向裂縫為主／側牆底水壓變化最大／內力增幅拱腳最劇／裂縫序列與現場一致／虹吸管建議推廣）——結論可被直接摘引，方便他人引用（也解釋其被引速度）。
- **對策當貢獻**：§4 虹吸排水管佔 2 頁，寫足構造細節（Ω 形虹吸孔、1 mm 孔、0.3 mm 溝槽、毛細+重力自動泥水分離），並以現場對照收尾（傳統管堵、虹吸管仍暢）——把 failure analysis 文體的「remedy」段做成第二賣點。
- 摘要與前言收尾句都押在實用價值（treatment / prevention / maintenance），與 EFA 讀者群（業主、養護單位）對頻。

## (f) 缺陷包裝

- **無 Limitations 專節、無 limitation 字眼**。弱點全部以「中性建模假設」姿態埋進 §3.2 方法段落，說完即走、不再回訪：
  - 2D 平面應變、圍岩襯砌均質連續體假設——一句帶過；
  - 地下水位全程固定於地表下 5 m（假設隧道排水量相對補給可忽略）——寫成 "Assuming that..." 的建模選擇；
  - 堵塞律 (3/4)ⁿ/每 3 個月為人為設定，未用現場堵塞速率率定——完全未討論其任意性；
  - 裂縫擴展方向假設垂直於最大主應力——以 XFEM 慣例姿態陳述。
- §2 的資料缺陷用「務實」語氣消化：裂縫深度僅對典型裂縫量測（"long operation time and low accuracy"），順勢宣告只統計長寬——把缺測寫成方法選擇。
- 結論起手一個限定子句 "at least for the tunneling considered in this study" ——全文唯一一處範圍自限，藏在結論導語裡，5 條結論本身不再帶任何 hedge。
- 可學：**用驗證圖（Fig. 21）替代 limitations 討論**——與現場一致性一旦成立，模型簡化的正當性就被默認，審稿人火力被引向已閉環的部分。

## (g) 圖表

**23 圖、1 表**（圖極多、表極少——EFA 案例文體典型）：

- 現場照片系（建可信度）：Fig.1 隧道外觀、Fig.2 裂縫/滲漏病害、Fig.3 智慧檢測車+人工檢測、Fig.8 裂縫滲漏與施工縫滲漏、Fig.21/22/23 內含現場照片。
- 統計圖系（§2 普查）：Fig.5 裂縫類型圓餅（287/208/139）、Fig.7 滲漏類型圓餅（252/117/18）、Fig.6 長寬雙軸長條、Fig.12 K3+190–290 裂縫展開圖（五測線）。
- 機制示意系：Fig.4 三類裂縫 3D 示意+照片、Fig.9 泥砂堵塞機制示意（引自前人）、Fig.10 斷面尺寸+支護標註、Fig.11 地質縱剖面（含照片內嵌）、Fig.13 地層-模型示意。
- 數值結果系：Fig.14 網格、Fig.15 孔壓雲圖 6 連格（n=0→16，時間演化一頁看盡）、Fig.16/17 孔壓演化折線（特徵點/內外差雙軸）、Fig.18 內力分佈玫瑰圖（M 左 N 右、n 疊線）、Fig.19 初支應力折線、Fig.20 開裂序列圖+裂深/裂寬演化折線（a/b/c 三聯）。
- 樞紐圖 **Fig.21**：FEM 損傷雲圖與現場裂縫照片逐部位（拱肩/側牆/拱腳）左右對照——一張圖完成驗證論證。
- 對策圖 Fig.22（虹吸管分解構造）、Fig.23（設計圖+安裝照片）。
- Table 1 唯一表：圍岩/支護/襯砌力學參數（密度、c、φ、E、ν、滲透係數、孔隙率）。
- 手法小結：**照片→統計→示意→雲圖→折線→照片對照**的圖序本身就是論證鏈；雲圖用多格時間序列而非單張；折線圖大量用雙軸與特徵點編號。

## (h) 對我們的啟示（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）

1. **缺口可直接疊在本篇肩上——時間結構升一階**：本篇把缺口打在「after → during」（堵塞過程中的損傷演化），驅動仍是**單調**水壓上升（(3/4)ⁿ 單向劣化）。我們的地下水位**循環/反覆**波動是下一階時間結構（monotonic → cyclic），可原樣沿用其三步 staging：肯定其查明單調堵塞下的開裂序列 → However 既有研究限於單向水壓上升 → 反覆升降下的裂縫累積擴展（疲勞式）尚無綜合研究。這是我們 P2 前言最順的接榫點。
2. **「普查母體→代表案例→數值機制→現場驗證→對策」五段敘事鏈可整套移植**：我們對應為——營運鐵路隧道檢測統計（裂縫型態比例）→ 代表斷面 → 跨尺度 FDM-DEM 重現水位循環下裂縫萌生擴展 → 與檢測影像對照（做我們的 Fig.21）→ 排水維護/監測建議。務必保留「模型-現場對照圖」這個樞紐：它同時完成驗證與缺陷免答。
3. **方法升級點有明確靶**：本篇用 XFEM 連續體＋「裂縫垂直最大主應力」假設，只能給裂深/裂寬/序列；其結果（V 形裂縫、裂 1 深 21 cm、拱腳先裂→側牆中→拱肩、n=13 近貫穿失承）可當我們 DEM 尺度的**基準重現目標**——跨尺度 FDM-DEM 能交代裂縫路徑曲折、粗糙度與骨材尺度機制，正是其方法交不出的層次。引用時以此立差異。
4. **可摘引的定量錨點**（供前言/討論用）：634 條裂縫中縱向 45.27% 為主；滲漏 68.48% 出自裂縫（裂縫=滲漏弱點的因果句）；未堵塞襯砌水壓僅 ~10 kPa、末期側牆底 84 kPa vs 拱頂 52 kPa（水壓沿深度分佈不均的案例數字）；首裂出現於堵塞 21 個月。這些是「單調水壓上升 baseline」的現成數據。
5. **題目與寫作工藝三件套照抄**：(i) 題目零方法詞、機制先行＋案例錨定（我們套 `Lining cracking mechanism of operating mountain railway tunnels induced by cyclic groundwater-level fluctuation: a case study of [○○] Tunnel, Taiwan`，FDM-DEM 留給摘要）；(ii) 前言只 3 段、文獻單段「人名+動詞」高密度掃射、貢獻句用流程敘事不用 novel；(iii) 無 limitations 節——用建模假設中性陳述＋驗證圖閉環＋結論導語一句範圍自限（"at least for..."句式）處理缺陷。另注意其結論 5 條每條一個可搬走的定量事實——為被引而寫。
