# Fahimifar & Zareifard (2009) — 寫作工藝精讀筆記

**書目**：Fahimifar, A.; Zareifard, M.R. (2009). A theoretical solution for analysis of tunnels below groundwater considering the hydraulic-mechanical coupling. *Tunnelling and Underground Space Technology*, 24, 634–646. DOI: 10.1016/j.tust.2009.06.002
**取得方式**：full-local（本機 PDF：`C:\Users\Wade\Desktop\Wade_TD_SCI\Reference\2020_2025\analyze\2009 水力解析解_A theoretical solution for analysis of tunnels below groundwater considering hydraulic-mechanical .pdf`）
**稿件時程**：收稿 2009-02-07 → 修訂 2009-06-17 → 接受 2009-06-19（一輪修訂約 4 個月，TUST 當年節奏）

---

## (a) 題目解剖

> A theoretical solution for analysis of tunnels below groundwater considering the hydraulic-mechanical coupling

- **開頭元素＝方法（解的類型）**：以 "A theoretical solution" 領頭，不是案例、不是現象。屬「解法宣告型」題目。
- **有方法詞**：theoretical solution、hydraulic-mechanical coupling 皆是方法／機制詞。
- **構式**：`A/An [解的類型] + for [分析對象] + considering [關鍵耦合機制]`
  - 三段式：解型（theoretical solution）→ 對象（tunnels below groundwater）→ 差異化賣點（考慮水力–力學耦合）。
  - "considering ..." 尾綴是本題目的差異化引擎——同類解多不考慮耦合，題目直接把缺口的補法寫進去。
- **題目與前言互為鏡像**：前言貢獻句同樣用一串現在分詞（considering...、applying...、using...）堆疊差異點，題目只保留最大的一個（coupling）。

## (b) 文章架構（13 頁，TUST 雙欄）

| 節 | 內容 | 約略比重 |
|---|---|---|
| 1. Introduction | 缺口鋪陳＋方法路線圖 | 1 頁（8%） |
| 2. Rock mass behavior | Hoek–Brown 強度準則＋應變軟化模型 | 1 頁（8%） |
| 3. Model assumptions and governing equations | 假設條列＋平衡／幾何方程 | 1 頁（8%） |
| 4. Hydraulic analysis | 滲流假設、變形相依滲透率、孔壓分布（共形映射解） | 2 頁（15%） |
| 5. Analysis of stresses and strains | 初始態→塑性區→彈性區→洞壁邊界條件 | 2 頁（15%） |
| 6. Computation procedure | 六步驟數值流程（編號清單） | 0.5 頁（4%） |
| 7. Computer program and examples | 五個算例（7.1–7.5） | 3 頁（23%） |
| 8. Conclusions | 結論 | 0.5 頁（4%） |
| Appendix A/B/C | 塑性區應力 FDM、塑性區應變、彈性區疊加解 | 3 頁（23%） |

- **推導藏進附錄**：主文只留控制方程與物理論述，逐式代數全部下放 Appendix A–C，讓正文維持「可讀的敘事線」。附錄比重高達近 1/4，是解析解論文的典型配置。
- **理論（§2–6）：算例（§7）≈ 5.5:3**——驗證與應用佔近 1/4 正文，不是點綴。

## (c) 前言手法（§1，共 7 段）

| 段 | 角色 |
|---|---|
| 1 | 領域級缺陷：文獻回顧顯示「有效應力＋滲流」受關注不足，多數解建立在總應力上；即使湧水可忽略，強度仍受有效應力控制。 |
| 2 | 物理機制動機：滲流體積力↔水力梯度↔破裂區滲透率隨變形改變 → 力學–水力耦合「必須」納入。先講物理必然性，再談文獻。 |
| 3 | 文獻枚舉＋分類：一句點名五組作者（Brown & Bray 1982；Fazio & Ribacchi 1984；Carosso & Giani 1989；Bobet & Nam 2006；Lee et al. 2007），隨即分層——多數不含耦合／兩組「近似地」考慮（滲透率比值固定、無決定方法）／Brown & Bray 只在破裂區考慮。 |
| 4 | 鎖定最近對手拆解：明指 Brown & Bray 解的「主要困難」——彈性區用總應力、忽略滲流對彈性區作用；假設徑向流僅適用極深隧道，臨界淺埋情況實際流場「差異顯著」。缺口 staging 的教科書式打法：點名最強前作→逐一擊破其兩項假設。 |
| 5 | 貢獻句：「In the present study, ... a new analytical solution is presented.」以一長串分詞片語（plane strain axisymmetric、strain-softening、effective stresses、Hoek–Brown、coupling、修正孔壓方程）把所有差異點一次堆滿，動詞維持被動低調（is presented）。 |
| 6–7 | 方法路線圖：編號清單（1. 力學分析軸對稱；2. 水力分析非軸對稱）＋收尾段講兩者交替迭代（successive approximations）至收斂。前言結尾就是計算架構預告，讀者帶著框架進入正文。 |

- **引語規範**：全文轉述、無直接引語。
- **缺口→貢獻的映射是一對一**：對手的每一條缺陷（總應力、無耦合、徑向流假設、線彈性）都能在貢獻句找到對應解法，讀者可逐項打勾。

## (d) 結果敘事（§7 五算例，各司其職的「驗證階梯」）

1. **Example 1（vs 前作）**：與 Brown & Bray 對比。圖領句「Fig. 5 shows the calculated ground reaction curves...」；先說 "the results are close to each other" 給足面子，隨即 "However, ..." 轉折，解釋前作因滲流影響半徑不確定、彈性區忽略滲流而「gives inexact results」——用對比結果重申前言缺口。
2. **Example 2（自洽視覺化）**：畫出偏心圓等勢線（Fig. 6），證明「洞壁、彈塑性邊界、地下水面皆為等勢面」的假設自洽。
3. **Example 3（vs FLAC 數值）**：量化到小數——塑性半徑解析 6.50 m vs FLAC 冠/壁/底 6.51/6.49/6.53 m；Table 2 逐點比對。隨後把驗證轉化為**兩條編號適用條件**（r_e/h_1 < 約 1/3；埋深 ≥ 5–10 倍洞徑），並順帶踩 FLAC 一腳：需極細網格、大範圍模型、「very time consuming」→ 反襯解析法價值。
4. **Example 4（參數物理）**：有滲流／無滲流／水位以上三情境（Fig. 10），給出全文最漂亮的機制詮釋句——**孔壓使有效應力下降（趨穩定），滲流力施加向內體積力（趨不穩定）**，雙向機制一句話收束，並在結論重現。
5. **Example 5（敏感度）**：耦合參數 η 掃描 16 個量級（Fig. 11 半對數），給滲流量上下界（1.544e-4 與 8.29e-5 m³/ms），結論式收尾：η 對力學結果影響可忽略（2.02→1.93 MPa）→「純力學分析時可略去應變相依滲透率」。把難以標定的參數轉化為設計上下界建議。

- **敘事模板**：圖領句（Fig. X shows...）→ 量化數字 → 機制詮釋 → 設計含義。每個算例結尾都落在「對使用者的意義」。

## (e) 貢獻凸顯

- **位置**：摘要首句、前言第 5 段、結論首句，三處同構。
- **措辭**：一貫低調被動——"is presented" / "was presented"。結論首句誠實標註 "An analytical **unclosed form** solution ... was presented"，緊接唯一一處自誇："to indicate the **integrity and power** of the proposed method"。
- **間接凸顯**：不靠形容詞，靠對比——Example 1 證前作 inexact、Example 3 證 FLAC 費時，貢獻由對手襯托。
- **實務落點**：結論用排水設計（sealed vs pervious lining、排水系統減壓）收尾，把理論貢獻接到工程決策。

## (f) 缺陷包裝

- **無 Limitations 專節、無 Future work 節**。缺陷以四種方式消化：
  1. **前置為假設條列**（§3、§4.1 的 bullet 清單）：軸對稱、塑性區徑向流、穩態、水面不動、r_e/h_1 需小——先講清楚，之後不再道歉。
  2. **轉化為適用條件**（Example 3）：「The proposed method gives the appropriate results **if**: 1. ... 2. ...」——把限制改寫成使用手冊，語氣從防守變服務。
  3. **軟化詞**：r_e/h_1 > 1/2 時徑向流假設 "may result in an **acceptable** error"——承認誤差但預貼「可接受」標籤。
  4. **參數難標定的自我拆彈**：§4.2 承認 η 需大量室內率定（對應力路徑、尺寸、異向性敏感），但 Example 5 隨即證明 η 對力學結果不敏感、滲流量有上下界可供設計——缺陷在同一篇內被實驗性中和。
- 「unclosed form」（需數值求解）之弱點以 FORTRAN 程式一句帶過，框架成「已解決的工程問題」。

## (g) 圖表數與類型

- **圖 12 張**（正文 Fig. 1–11＋附錄 Fig. A1）＋**表 2 張**：
  - 概念／示意 5：Fig. 1 本構模型三聯圖、Fig. 2 分區模型、Fig. 3 滲流網、Fig. 4 初始態、Fig. A1 元素受力。
  - XY 曲線 6：Fig. 5/8/10 GRC 對比、Fig. 7 孔壓徑向分布（解析 vs FLAC 點線疊圖）、Fig. 6 等勢線圖、Fig. 11 η 敏感度（半對數）。
  - 數值軟體截圖 1：Fig. 9 FLAC 等勢線雲圖（未重繪，原樣貼入，2009 年代風格）。
- **表**：Table 1 兩法六量對比、Table 2 FLAC vs 程式在 crown/bottom/wall 三位置四量對比——驗證用表都做成「逐量並排」格式，讀者一眼比差。
- 驗證圖固定語法：解析＝實線、數值＝離散符號點。

## (h) 對我們的啟示（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）

1. **題目構式可直接沿用**：`[解型/框架] for [營運鐵路隧道襯砌] considering [groundwater-level cycling / hydro-mechanical coupling]`。TUST 顯然接受「considering + 耦合機制」尾綴作為差異化訊號；我們的 cross-scale FDM-DEM 可放解型位置，水位循環放 considering 位置。
2. **三層驗證階梯**照搬：先 vs 最近解析前作（本篇即可當我們的 benchmark 對象——含水隧道解析解）、再 vs 成熟數值/實測、最後參數掃描給設計含義。每個算例賦予單一修辭任務，結尾都落到工程決策（我們的對應：排水劣化、裂縫演化門檻）。
3. **缺陷改寫為適用條件**：不設 Limitations 節，把 2D/軸對稱、耦合簡化、尺度橋接假設寫成編號的「本法適用若…」條件；難標定參數（如 DEM 微觀參數）仿 Example 5 做量級掃描證明不敏感或給上下界，於同篇內自我拆彈。
4. **雙向機制金句**：本篇「孔壓趨穩、滲流力趨不穩」一句貫穿摘要–算例–結論。我們應提煉對應句——例如「水位上升抬升孔壓卸載襯砌有效應力、水位驟降反向滲流力加載裂縫尖端」之類的循環雙向機制句，作為全文記憶點反覆出現。
5. **引用價值**：本篇是「隧道×地下水×力學耦合」解析解的 TUST 正典，可在前言作為「穩態、單次水位、無襯砌劣化」一類解的代表——我們的缺口（**循環**水位、**營運期**襯砌裂縫、**跨尺度**離散破裂）恰好是它 considering 之外的三個維度。
