# Vazaios, Vlachopoulos & Diederichs (2019) — 閱讀筆記

**書目**：Vazaios, I., Vlachopoulos, N., Diederichs, M.S. (2019). Assessing fracturing mechanisms and evolution of excavation damaged zone of tunnels in interlocked rock masses at high stresses using a finite-discrete element approach. *Journal of Rock Mechanics and Geotechnical Engineering*, 11(4), 701–722. DOI: 10.1016/j.jrmge.2019.02.004

**取得狀態**：`access = full-pdf`（本機 PDF 全文 22 頁逐頁精讀；筆記全面覆寫 abstract-only 舊版）。**筆記日期：2026-07-22**。Full Length Article；收稿 2018-07-09、修回 2018-12-30、接受 2019-02-18、上線 2019-04-19；CC BY-NC-ND 開放取用。關鍵詞：EDZ、brittle failure、FDEM、tunnelling、DFN。P4 系譜最高引文獻。

---

## (a) 題目解剖

原題：*Assessing fracturing mechanisms and evolution of excavation damaged zone of tunnels in interlocked rock masses at high stresses using a finite-discrete element approach*

- **開頭元素**：動名詞「Assessing」起手＋**機制對象**（fracturing mechanisms、EDZ evolution）——不是案例、不是方法開頭；機制/現象佔題目主位。
- **有無方法詞**：有，但**置於句尾**（"using a finite-discrete element approach"），用全稱＋泛稱 "approach" 而非縮寫 FDEM（FDEM 留給關鍵詞與摘要），方法退居工具位。
- **構式拆解**（六段套疊，由核心向外加限定）：
  1. `Assessing`（動名詞動作）
  2. `fracturing mechanisms and evolution of excavation damaged zone`（雙機制對象，and 並列；「evolution」點出時間維度）
  3. `of tunnels`（工程對象）
  4. `in interlocked rock masses`（地質條件——正文對應詞是 non-persistent joints／interlocked hard rock，題目選了較形象的 interlocked）
  5. `at high stresses`（荷載/環境條件）
  6. `using a finite-discrete element approach`（方法，尾位）
- **題目與內文的對應檢核**（全文後驗證）：題目未提的第三自變數「節理強度」與第四變數「K 值（σH/σv）」都藏在正文；題目只承諾機制與演化，把參數矩陣留給摘要——**題目賣現象、摘要賣矩陣**的兩級遞進。
- **可複製模板**：`[Assessing/Evaluating] + [機制A and 演化B] + of [工程對象] + in [材料/地質條件] + at/under [荷載條件] + using [方法] approach`。長題目但每段都是檢索關鍵詞。

## (b) 文章架構與比重

7 節主幹＋致謝/參考文獻，22 頁（含圖表）。逐節頁距與比重：

| 節 | 頁距 | 佔比（約） | 角色 |
|---|---|---|---|
| 1. Introduction | 701–702 | ~0.8 頁 | 問題＋EDZ 分類＋貢獻宣告（僅 4 段，極精簡） |
| 2. Geological setting & rock mass properties | 702 | ~0.3 頁 | URL Test Tunnel（Pinawa, Manitoba，深 420 m）＋Lac du Bonnet 花崗岩性質（Table 1） |
| 3. Brittle failure in tunnels at high stresses | 702–703 | ~0.4 頁 | 脆性破壞力學背景（spalling＝extensile 微裂、抗張控制、非剪力準則） |
| 4. Numerical model (FDEM) | 703–708 | ~4.5 頁 | 4.1 FDEM 原理→4.2.1 幾何/網格/DFN/開挖模擬→4.2.2 應力邊界→4.2.3 校準＋參數→4.2.4 節理參數 |
| 5. Simulating the EDZ | 708–714 | ~5 頁 | 四組結果：5.1 裂隙強度 P21、5.2 延續性 Lt、5.3 節理強度、5.4 低圍壓（K 值）×構造 |
| 6. Discussion of results | 714–720 | ~5 頁 | 6.1–6.4 **與結果四小節一一鏡像**，升一層抽象重述機制 |
| 7. Conclusions | 720–721 | ~0.7 頁 | 3 段：目的重述→主發現→限制併未來工作 |

- **架構特徵一**：前言極短，但緊接兩個**獨立的迷你背景節**（§2 場址、§3 脆性破壞理論）——把傳統前言的文獻鋪陳外包出去，前言只做缺口與貢獻。
- **架構特徵二**：Results 與 Discussion 分節且**四對四鏡像**（5.1↔6.1、5.2↔6.2、5.3↔6.3、5.4↔6.4），Results 只「描述模型現象」，Discussion 才做機制歸因與因子排序；重量級對比組圖（Figs. 19–23）竟放在 Discussion 節，讓討論自帶證據。
- **架構特徵三**：方法節近 1/4 篇幅，含完整校準流程圖（Fig. 4）與 7 張輸入參數表——可重現性當賣點。
- **模型量級**（Table 2/4）：60 m×60 m 域、四級網格（0.03→2.5 m）、23–67 萬三角元素、時步 ~4×10⁻⁸–9×10⁻⁸ s、350 萬步、單機（i7-4930K/16 GB）跑 30–144 h——誠實揭露算力成本。

## (c) 前言手法

**4 段**，逐段角色：

1. **普適問題起手**：開挖損傷改變圍岩性質、影響開挖反應→「準確且嚴謹評估 EDZ 深度與形狀是設計必要條件」；一句話帶過既有兩路徑（經驗法 vs. 數值法）＋整串文獻括號。
2. **分類學段**：EIZ／EDZ（內 EDZi／外 EDZo）／HDZ 三層損傷分區＋CDZ（施工損傷），配 Fig. 1 概念圖——用分類框架宣示本文談的是「應力重分布引致、不可避免」的那一類損傷。
3. **收窄至缺口**：深部硬岩脆性破壞由抗張強度主導（extensile fracturing at low confinement）→轉折句：若存在**先存節理、尤其非持續節理**，行為將進一步改變——缺口是「非持續節理互鎖岩體的 EDZ 機制」，介於無裂隙端元（已被 Diederichs 系列解決）與持續節理端元之間的空檔。**缺口 staging 只用一段**，靠 §2–§3 兩個背景節補強，不在前言堆文獻。
4. **貢獻宣告段**：句式「In this study, the excavation induced damage … is investigated by applying the FDEM」＋直述三自變數（節理幾何、節理強度、初始應力大小）與因變數（損傷及其演化）——參數矩陣在前言末預告，全文照表操課。
- 引語手法：通篇轉述＋括號群引；自我定位聚焦於考察 "the in situ stress-joint network interaction"（摘要語）。

## (d) 結果敘事

- **雙錨定量法**：所有監測應力路徑一律畫在 σ3/σci–σ1/σci 正規化平面上，同時疊 **Hoek-Brown 包絡（GSI=80）**與 **DISL 損傷起始/剝落極限模型**兩組準則（Figs. 8, 10, 12, 18）——把「裂縫圖好看」升級為「應力路徑落在哪個準則區間」的可檢驗量化主張。這是全文敘事的定量脊椎。
- **三階段敘事模板**：每個構型都用同一組四聯圖講故事——Stage I 起裂→Stage II 傳播＋新裂縫→Stage III 裂縫互制→(d) 崩落成 v 形 notch（Figs. 7, 9, 11 完全平行），讀者可逐格對照 intact vs. DFN3 vs. DFN5。
- **監測變數三件套**：應力路徑＋最小主應變 ε3＋體積應變 εvol（外加裂縫數）（Fig. 13）——體應變雲圖用來論證「圍壓在 notch 頂部重建→裂縫傳播停止」的自穩機制。
- **機制語言主導**：節理是「應力屏障」「應力集中/耗散/再導向實體」；裂縫被次垂直節理「圍束」；intact 模型 notch 沿 σ1 方向傾斜，DFN 模型 notch 被節理再導向為近垂直——每個現象都給力學因果。
- **反直覺發現特意留亮點**：(i) 純摩擦節理下 HDZ 深度與 intact 相近但位置改向；(ii) 節理幾何 > 節理強度（強度僅在極端值時才要緊）；(iii) K=2（初始應力較高）反而比 K=3 穩定——因 K=2 側壁能重建圍壓，K=3 側壁處於伸張狀態致災難性崩塌（§5.4/6.4）。
- 結果句尾均收在工程後果（開口整體穩定性、結構完整性喪失）。

## (e) 貢獻凸顯

- **三層堆疊**（摘要＝結論的縮印）："highlight the significance of…"（主發現：先存節理折減原位岩體強度＋延展潛能）→ "Furthermore…"（空間分布控制穩定性＋節理強度影響可能輕微）→ "Additionally…"（應力–節理網絡互制→不可控裂縫傳播）。
- **Discussion 鏡像重述**：6.1–6.4 每小節把對應結果重講一遍並升階為因子排序陳述——「節理網絡幾何、延續性、空間分布是主導因子，節理強度次之」；結論再第三次重申。同一發現全文出現三次（結果→討論→結論），每次抽象度遞增。
- **方法優勢靠對照襯托**：討論節開頭點名「傳統連續體技術受限、無法真實捕捉破壞機制」並引自家姊妹作（Vlachopoulos & Vazaios 2018）——FDEM 的賣點不是自誇而是襯托：能看見連續體看不見的應力誘發裂縫×先存節理互制。
- **措辭**：highlight / demonstrate / reveal / examined——「揭示機制」語系；方法是工具，洞見（因子層級＋互制機制）才是貢獻。校準品質用「模擬 UCS≈120 MPa，與前人 SRM 研究 105–175 MPa 一致」的區間對標背書。

## (f) 缺陷包裝

- **假設前置於方法節**：2D 平面應變＋面替換法（core modulus reduction）模擬 3D 掌子面推進、不計重力梯度（deep tunnel 均勻應力場假設）、out-of-plane 應力不影響裂縫成核——全部以「modelling assumption」語氣寫在 §4.2.2，不設獨立 limitations 節。
- **算力限制以權衡語包裝**：「捕捉破壞機制 vs. 計算時間需求之間的平衡」——元素不能太細是 trade-off 不是缺陷；Table 4 誠實列 runtime 反而加分。
- **缺陷→未來工作轉換**：討論 6.3 末把未檢驗項（更高節理強度、其他節理方位、節理 penalty 參數影響）一句話併入 "will be part of future work"（p. 718）；結論末段同法：需更多 DFN 幾何驗證、同組 DFN 參數需更多隨機實現（隱晦承認每組 DFN 只跑單一實現）。缺陷全數改寫為研究路線圖，位置固定在小節末與全文末。
- **範圍限定語**：反直覺發現（節理強度影響輕微）永遠掛條件狀語——"under specific conditions"、"unless increased at really high values that match the intact material"——先圈住適用範圍，普適性風險即除。

## (g) 圖表

**23 圖、7 表**，約每頁一圖，結果零表格——**結果全靠圖說話，表只放輸入**。

- **表（全部前置於 §2–§4）**：T1 LdB 花崗岩實驗性質（E=69 GPa、UCS=213 MPa、CI=90/CD=172 MPa、σt=9.3 MPa）；T2 六構型網格/元素數；T3 DFN 參數（P21=1–2 m/m²、Lt=0.25–2 m、雙節理組 dip 80°/10°）；T4 時步/步數/runtime；T5 應力場（σxx=−58、σyy=−13、τxy=−9.2 MPa，即 σ1≈60/σ3≈11 MPa 斜交）；T6 校準後 FDEM 輸入（E=65 GPa、μ=1.7、c=50 MPa、ft=10 MPa、GI=300/GII=1900 N/m、penalty=650）；T7 四種節理強度 Case。
- **圖型五類**：
  1. 概念/原理圖（Fig. 1 EDZ 分區、Fig. 2 FDEM 內聚裂縫模型三聯、Fig. 4 **兩迴圈校準流程圖**——變形性迴圈對 Read(1994) 位移、強度迴圈對 URL 損傷剖面）；
  2. 模型設置（Fig. 3 四級網格域、Fig. 6 五個 DFN 實現）；
  3. **實測–模擬對照**（Fig. 5：URL 現場 notch 照片 vs. FDEM 損傷輪廓並排，1.3R vs 1.26R——全文唯一照片，校準可信度的視覺王牌）；
  4. 過程演化組圖（Figs. 7/9/11 四階段偏應力雲圖＋裂縫；Figs. 14–17 六步 (a)裂縫型態＋(b)體應變雲圖成對模板；Figs. 19/20 四強度情境×四步 σ3 雲圖矩陣；Figs. 21–23 K 值情境 Step 133–200 時序）；
  5. 定量詮釋圖（Figs. 8/10/12/18 正規化應力路徑 vs. 雙包絡；Fig. 13 ε3–εvol 路徑對比）。
- **圖說自足**：每張組圖圖說長達 5–8 行，內嵌顏色編碼定義（張裂紅/剪裂綠、軟化藍/粉）、參數提示、崩落區虛線標註——圖脫離正文可讀。
- **模板化重複**是最大特色：同版式雲圖跨構型重複 4 次以上，讓「比較」本身成為圖的功能。

## (h) 對我們的啟示（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）

1. **兩迴圈校準流程圖直接移植**：Fig. 4 的「先鎖變形性（對實測位移）→再鎖強度微觀參數（對實測損傷剖面）」雙迴圈＋Fig. 5 實測照片並排驗證，是審稿人建立信任的完整儀式。我們可複製為：FDM 遠場先對襯砌收斂/變位監測校準→DEM 近場對襯砌裂縫實測圖譜校準，並同樣畫成流程圖＋現場裂縫照片 vs. 模擬裂縫並排圖。
2. **「端元＋參數矩陣」架構**：無裂隙 intact 端元先立基準，再逐一疊加 P21、Lt、節理強度、K 值四因子，每因子一對「結果小節↔討論小節」鏡像。我們對應：完整襯砌×恆定水位端元→疊加裂縫密度×水位循環幅/頻×界面劣化，Results 描述、Discussion 排序因子，結構照抄。
3. **應力路徑×準則包絡的定量脊椎**：他們把每個情境的監測應力路徑疊在 DISL＋Hoek-Brown 雙包絡上，機制主張全部可檢驗。我們可將襯砌單元在水位循環下的應力路徑疊在混凝土開裂/疲勞包絡上，讓「裂縫隨循環演化」從雲圖敘述升級為準則交叉點的量化陳述——這是本文被高引的方法學核心，值得指名引用。
4. **製造一個「因子層級＋反直覺」亮點**：本文最響亮的可攜結論是「節理幾何/空間分布 > 節理強度」與「初始應力較高的 K=2 反而較穩（圍壓重建）」，且都掛條件狀語圈範圍。我們應預留同型亮點（例如「水位循環幅度 > 裂縫初始密度」或「某水位區間反而閉合裂縫」），並學其 "under specific conditions" 式的普適性防火牆。
5. **缺陷全數轉未來工作＋假設前置**：2D、單一 DFN 實現、penalty 未參數化——全在方法節以假設交代、在小節末以 future work 收束，不設 limitations 節。我們的 2D/3D 取捨、單一疲勞本構、有限循環數可循此法包裝；並學 Table 4 誠實揭露 runtime，把算力成本寫成嚴謹而非弱點。
