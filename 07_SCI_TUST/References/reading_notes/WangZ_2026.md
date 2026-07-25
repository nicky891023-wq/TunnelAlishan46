# Wang, Z. et al. (2026) TUST — 寫作工藝精讀筆記（全文版）

- **全題**：Coupled thermo-mechanical simulation of lining cracking evolution and sealing system mechanical response in CAES lined rock caverns using finite-discrete element method
- **出處**：Tunnelling and Underground Space Technology incorporating Trenchless Technology Research, Vol. 172 (2026), Art. 107460；DOI: 10.1016/j.tust.2026.107460
- **特刊**：屬 TUST 特刊 **'Underground Energy Storage'**（題名頁星號註）。⚠️ 這改變了對它的定位判讀：不是一般投稿，是特刊邀稿/組稿脈絡，審稿速度與主題偏好都不同。
- **時程**：Received 2025-11-05 → Revised 2025-12-31 → Accepted 2026-01-07 → Online 2026-02-03。**收稿到接受 63 天**，改一輪即過。
- **作者群**：Zhangxing Wang^a,b、Jiao Wang^a,b、**Guanhua Sun**^a,b,*（通訊，ghsun@whrsm.ac.cn）、Shan Lin^c、Zhijun Liu^d,e、Hong Zheng^c
  - a 中科院武漢岩土力學所 岩土力學與工程安全國家重點實驗室；b 中國科學院大學；c 北京工業大學 城市安全與防災工程教育部重點實驗室；d 蘭州大學土木工程與力學學院；e 蘭州大學西部災害與環境力學教育部重點實驗室
- **取得狀態**：**`access = full-pdf`**。本機 PDF 全文 26 頁（正文 p.1–23、附錄 A/B/C p.23–25、參考文獻 p.26），已逐頁讀完。本筆記全部依據全文，**無推測標記**。
- **基金**：NSFC 42572366、52508463；國重室自主課題 SKLGME-JBGS2404；山東大學智能製造先進建設機械國重室開放課題 ACMKF2024-16。
- **規模**：**22 圖、5 表、23 式、3 附錄、56 篇參考文獻**。
- **筆記日期**：2026-07-25（全文覆寫，取代 2026-07-21 的 abstract-only 版）

---

## (a) 題目解剖

**構式（四段式方法三明治）**：〔耦合物理場＋模擬詞〕of〔現象A **evolution** and 現象B **response**〕in〔工程場景〕using〔方法全名〕

| 元素 | 內容 | 位置 |
|---|---|---|
| 開頭元素 | **方法／物理耦合**：Coupled thermo-mechanical simulation | 題首 |
| 現象（雙） | lining cracking **evolution** ＋ sealing system mechanical **response** | 題中，and 並列 |
| 場景 | CAES lined rock caverns（CAES 縮寫直接入題，未展開） | 題後段 |
| 方法詞 | using **finite-discrete element method**（全名，不縮寫成 FDEM） | 題尾 |

全文核對後的確認與修正：

1. **方法詞前後包夾成立**：simulation 開場、finite-discrete element method 收尾，中間夾兩個工程對象。題目 20 個實詞，偏長，但每段都是檢索關鍵字（thermo-mechanical / lining cracking / sealing / CAES / lined rock cavern / finite-discrete element method）。
2. **方法全名入題尾、縮寫留給關鍵詞欄**：Keywords 欄才出現 `FDEM`。Keywords 共 6 個：CAES、LRCs、Crack distribution、**Crack width**、Thermo-mechanical coupling、FDEM。⚠️ 值得學：**把「Crack distribution」與「Crack width」兩個「量」單獨列為關鍵詞**，等於宣告「本文賣的是這兩個可量化的輸出」，不是賣現象。
3. `using finite-discrete element method` 前**無定冠詞 the**（原文如此），Elsevier 未改——題尾方法片語傾向裸名詞片語。
4. 現象用 evolution / response 兩個過程性名詞，暗示動態全歷程；但全文其實只算了**第一個 40 h 工作循環**（見 (f)）——題目的 evolution 是「單循環內的演化」而非「長期演化」，這是題目與內容之間刻意留白的一步。

**可移植骨架**：`Coupled [場A]-mechanical simulation of [對象1 evolution] and [對象2 response] in [場景] using [方法全名]`

## (b) 文章架構與各節比重

實際節序（頁碼為 PDF 實頁）：

| 節 | 標題 | 頁 | 約略比重（正文 23 頁計） |
|---|---|---|---|
| — | Abstract（單段，約 210 字） | p.1 | — |
| 1 | Introduction | p.1(col2)–p.4(col1) | ~13% |
| 2 | Materials and methods | p.4(col2)–p.10(col1) | ~24% |
| 2.1 | Structural layout and material composition of LRC | p.4–5 | |
| 2.2 | Analytical model of temperature and pressure evolution for LRC | p.5 | |
| 2.3 | FPZ and cohesive zone model | p.5–9 | |
| 2.4 | Parameter calibration | p.9–10 | |
| 3 | FDEM numerical model | p.10(col2)–p.14(col2) | ~19% |
| 3.1 | Numerical model for LRC | p.10–11 | |
| 3.2 | Model validation | p.12–14 | |
| 4 | Results and discussion | p.14(col2)–p.23(col1) | ~36% |
| 4.1 | Influence of thermodynamic processes on lining cracking | p.14–17 | |
| 4.2 | Influence of surrounding rock deformation capacity on lining cracking | p.17–18 | |
| 4.3 | Influence of structural design parameters（4.3.1 配筋佈置／4.3.2 配筋率／4.3.3 襯砌厚度） | p.19–23 | |
| 5 | Conclusions | p.23(col1) | ~2%（僅 5 條編號） |
| — | CRediT／Declaration／Acknowledgments | p.23 | |
| A | Analytical model of temperature and pressure evolution for LRC | p.23–24 | ~4% |
| B | Theoretical formulation of the penalty contact algorithm（B.1 法向／B.2 切向） | p.24–25 | ~3% |
| C | **Definitions and calculation methods of crack cohesive element width and equivalent crack porosity**（C.1 裂縫體積／C.2 幾何反推裂縫寬／C.3 等效裂縫孔隙率） | p.25 | ~3% |
| — | Data availability（"Data will be made available on request."）＋ References | p.26 | |

**三個架構級的可學之處：**

1. **「Results and discussion」合併成一節**，不分開 Discussion。所有機制詮釋、設計建議都就地寫在結果裡，沒有獨立討論節去統整——這讓 Conclusions 可以壓到半頁。
2. **正文只留「做法＋結果」，把「怎麼算出來的」全部丟進附錄**。三個附錄分工乾淨：A＝借來的解析熱力模型（不是他們的貢獻，所以移出）、B＝接觸罰函數（標準做法，移出）、**C＝裂縫寬與孔隙率的後處理演算法（是他們的原創量化定義，卻也移到附錄）**。⚠️ 這是個有爭議但有效的選擇：正文專心講「裂縫寬 0.38 mm→0.29 mm」，讀者要追問「你怎麼定義裂縫寬」才翻附錄 C。我們可以照做，但**附錄 C 這種原創定義建議留在正文**，因為那正是方法貢獻。
3. **方法先、案例後、驗證夾在中間**：Section 2 建框架（含材料層次、解析溫壓、CZM 理論、參數標定）→ Section 3.1 工程尺度模型 → **Section 3.2 才做驗證**（用文獻 Yang 2020 的鋼襯 RC 管模型試驗）。驗證不是獨立一節，是掛在「數值模型」節底下的一個小節。這暗示：驗證被定位為「模型建立的一個步驟」，不是與結果並列的主張。

## (c) 前言手法

**七段結構**，每段角色分明：

| 段 | 角色 | 內容骨幹 | 收尾動作 |
|---|---|---|---|
| 1 | 能源大背景 | 再生能源轉型→中國 2024 底累計再生能源 18.89 億 kW、佔總裝機 56%（NEA 2025）→間歇性→需大規模儲能→抽蓄受地理限制、鋰電/飛輪受壽命與材料限制→**CAES 出線** | 「CAES has emerged as a critical alternative」 |
| 2 | 縮到場景 | CAES 可行性繫於儲氣庫氣密性與穩定→鹽穴最佳、枯竭氣藏次之→**無鹽層地區只能用人工襯砌岩洞 LRC**→以 **Fig. 1** 帶出整體系統圖→給硬參數（埋深 100–200 m、最大內壓 >10 MPa、壓力波動達 6 MPa、最短充放週期 1 天）→熱力荷載必然在混凝土產生拉應力 | 「lining cracks a critical failure mode」 |
| 3 | 鎖定問題並定義「所需的量」 | 襯砌的角色是傳遞內壓給圍岩＋支撐密封層→嚴重開裂會破壞這個支撐、在密封層造成應力集中與**變形協調失配（deformation coordination mismatch）**→提高局部破裂風險 | **「準確預測裂縫數量、分佈型態、與具體開度寬度，是 LRC 設計與安全評估的前提」**——⚠️ 這句是全篇的軸心：**缺口不是「沒人做」，而是「設計需要三個量：條數、分佈、開度」** |
| 4 | 既有知識 A：力學驅動 | 開裂由力學荷載、層間互制、熱力耦合共同驅動→Hori 2003（混凝土抗拉遠低於環拉應力，傳統配筋襯砌必然受拉損傷）→Okuno 2009（拉裂難完全避免，**焦點應轉向控制裂縫寬度而非完全防裂**） | 為「量開度」正名 |
| 5 | 既有知識 B：層間＋熱力 | Johansson 2003（開裂集中在岩石節理張開處，非均勻分佈）→Zhang 2024b（層間剪切互鎖與非光滑接觸加劇拉應力集中）→Geissbühler 2018／Becattini 2018（交變溫度場→熱疲勞與力學不穩定）→**Jiang 2024（熱膨脹部分抵銷環拉，但長期循環累積損傷使裂寬非線性成長後穩定）** | 把熱效應說成「雙面」，替自己的正面結論留伏筆 |
| 6 | **缺口 staging（雙缺口）** | 「Although the aforementioned studies have preliminarily revealed…」→缺口①：**工程尺度下的真實開裂模式、細緻裂縫特徵（裂寬與間距的時空分佈）、設計參數的定量影響，缺乏系統研究**→以 **Fig. 2** 展示自家正在做的大型室內物理模型試驗→承認**室內試驗受圍岩約束邊界與相似律限制，難外推到工程尺度**→轉向數值→缺口②：**FEM＋連續損傷（CDP／彌散裂縫／相場）把裂縫當成損傷變數或擴散場，不是實體不連續面**，可算整體承載力，但**解析不出循環熱力荷載下裂縫的離散張開/閉合與摩擦接觸**，而這正是評估襯砌–密封層力學協調的關鍵 | 缺口以「工具給不出設計所需的量」收束 |
| 7 | 方法＋目標宣告 | 「To overcome the limitations of continuum-based approximations…」→採 FDEM→定根（Munjiza 2004、Mahabadi 2012）→**明寫與 FEM 的差異**（FDEM 以 CZM 拓樸分離元素邊界，FEM 只是擴散式材料劣化）→列出 FDEM 能直接解析的四件事（**crack initiation, explicit propagation, stochastic bifurcation, frictional contact between fractured surfaces**，Lisjak 2020）→加入壓–溫耦合→**能精確量化裂縫開度**→三動詞目標句 | 見下 |

**貢獻/目標句式（第7段末，三動詞排比，轉述）**：本研究旨在（i）提供一個能真實模擬高內壓下 LRC 襯砌開裂特徵的**不連續數值方法**、（ii）**系統評估**襯砌結構設計參數對開裂行為的影響、（iii）為 CAES 人工地下 LRC 的**密封完整性評估提供依據**。
→ `provide a [method] to realistically simulate … , systematically evaluate … , and provide a basis for assessing …`

**四個可直接偷的前言戰術：**

1. **把缺口畫成圖（Fig. 2）**：一張綠底橫幅圖，左半是自家室內模型試驗照片（試驗平台／試體／已裂內襯／環向裂縫特寫），右半是連續體 FEM 的網格與損傷雲圖，圖下用兩個標了 **"Issue 1"／"Issue 2"** 的方框直接寫出缺口文字（Issue 1：無法考慮完整地質模型、結果不能直接縮放到工程尺度；Issue 2：難以確定破裂形態、連續模型無法精確捕捉不連續）。⚠️ **缺口不只用寫的，用畫的**——這是我看過最直接的 gap 圖示化。強烈建議我們照做。
2. **拿自家的實驗當缺口證據**：Fig. 2 左半是「本研究團隊正在進行的」試驗，然後親口說它外推不到工程尺度。**自曝其短來論證數值方法的必要性**，比批評別人安全得多。我們有現地裂縫調查資料，可以同樣操作：「現地量測給了真實裂縫，但給不出機制與參數敏感度」。
3. **缺口句終結在「設計需要的物理量」**：第3段就把「條數／分佈／開度」立為設計前提，第6段再說既有工具給不出開度，第7段說 FDEM 能給。**三段一條線，缺口是量的缺口不是題目的缺口**。
4. **引文雙錨已證實**：一手拉破壞力學經典（**Irwin 1957、Barenblatt 1962、Hillerborg 1976**）＋方法經典（**Munjiza 2004、Mahabadi 2012（Y-Geo）、Lisjak 2020（GPU-FDEM）**）＋本構經典（Lee & Fenves 1998、Menegotto 1973）；另一手拉同刊近文（TUST：Wan 2024、Wang H. 2026、Geng 2025、Jiang 2024、Zhou 2025）。56 篇中**自引群極重**：Zhou ×4（2015/2017/2020/2025）、Sun ×4、Xia ×2、Zhu ×2、Geng ×2、Jiang ×2、Kushnir ×3、Kim ×4——武漢岩土所自家系譜約佔 1/3。

**引語（全文唯一，<15字）**：`"thicker linings generate fewer but wider cracks"`

## (d) 結果敘事

**核心發現是「模板化重複」**：五個參數組（熱力／圍岩勁度／配筋佈置／配筋率〔直徑＋間距〕／襯砌厚度）**共用同一套五步敘事與同一套兩張圖**。

### 每組的固定五步

1. **機制導言**（此參數為何影響力學路徑，1–2 句，不引圖）
2. **裂縫分佈圖定性描述**（`As illustrated in Fig. N` / `As shown in Fig. N` 開頭）——講疏密、貫穿與否、對稱性
3. **兩個裂縫指標定量**：**最大裂縫寬（mm）** ＋ **等效裂縫孔隙率（%）**，一律配「變化百分比」
4. **密封層鋼襯應力**：沿 **NDP（正規化圓周路徑）** 展開的 von Mises **平均應力** ＋ **應力幅值**，兩個數字並報
5. **`Taken together` / `In summary` / `In conclusion` 收束段 → 直接落到設計建議**

### 圖領句：壓倒性

幾乎每個結果段的第一或第二句就是 `As shown in Fig. N` / `As illustrated in Fig. N` / `As shown in Figs. 17 to 18`。文字是圖的說明文，不是獨立論述。**沒有任何一段結果是無圖裸述的。**

### 量化方式：一律「兩數字＋百分比變化」

這是全篇最一致的修辭。實測清單：

| 主題 | 對比 | 百分比話術 |
|---|---|---|
| 熱效應→最大裂寬 | 0.38 mm → 0.29 mm | 「a reduction of about 34%」 |
| 熱效應→等效裂縫孔隙率 | 0.19% → 0.05% | 「a reduction of about 74%」 |
| 熱效應→鋼襯 von Mises | 242.4 MPa → 161.2 MPa | — |
| 熱效應→鋼襯應力幅 | 180.9 MPa → 99.7 MPa | 「a reduction of more than 30%」 |
| 圍岩勁度→塑性區深度 | 5.28 m(6GPa) / 4.29 m(12) / 3.45 m(16) / 2.86 m(20) | 「23% greater」「decreases by nearly 50%」 |
| 圍岩勁度→徑向位移 | 11.77 / 5.79 / 4.14 / 3.08 mm | — |
| 圍岩勁度→裂寬・孔隙率 | 0.65 mm・0.43%(6GPa) → <0.30 mm・0.07%(20GPa) | — |
| 圍岩勁度→鋼襯應力/幅 | 403.2/287.3 → 184.1/115.6 → 146.9/86.0 MPa | 「an overall reduction of more than 40%」 |
| 配筋佈置→裂寬・孔隙率 | 內單層 0.70 mm・0.26%；外單層 0.48・0.24%；**雙層 0.38・0.09%** | — |
| 鋼筋直徑 16→25 mm | 裂寬 0.45→0.35 mm；孔隙率 0.20→0.16% | 「about 20%」＋**「limited」** |
| 鋼筋間距 50→200 mm | 裂寬 0.35→0.44 mm；孔隙率 | 「increases by about 30%」 |
| 襯砌厚度 80→50 cm | 裂寬 0.70→0.30 mm；孔隙率 0.26→0.09% | 「approximately 55–65%」 |
| 襯砌厚度→鋼襯平均應力 | 242/240/244/238 MPa（幅 180/153/152/138） | **「weak sensitivity」** |

⚠️ 注意：**摘要只押一個 30%**（熱效應對裂寬與鋼襯應力幅），但正文有十幾個百分比。**摘要是「選一個最好記的數字」，正文才鋪滿**——這個層級落差要學。

### 機制詮釋：五段鏈，一次不跳

`參數 → 應力場/塑性區變化 → 裂縫指標（寬・孔隙率・貫穿性）→ 密封層應力與幅值 → 設計含義（疲勞/氣密性/選址）`

範例（4.1）：內壁溫度 290 K→319 K(4 MPa)→339 K(10 MPa)、外壁近初溫→形成 **30–40 K 徑向溫度梯度**→內側混凝土產生環向**壓**應力→抵銷部分內壓拉應力→裂縫數量與**連通性**同時下降→熱膨脹提供穩定約束、提升壓力上升期的變形協調性→鋼襯應力集中被緩解、循環應力波動變小→**延緩疲勞損傷**。

範例（4.2）：低勁度圍岩→側牆大範圍塑性擴張、幾乎形成連續塑性環→襯砌承擔大部分內壓（塑性主導破壞模式）→密集環向裂縫、最大裂寬 0.65 mm→鋼襯平均應力 403.2 MPa（**逼近 Q420 降伏**）與高幅值→局部降伏風險→**選址應優先高勁度地層，否則需圍岩加固**。

### 敢寫負結果與「弱敏感」，而且解釋原因

- 鋼筋直徑：加大直徑「對抑制裂縫擴展的貢獻有限」——並解釋原因（**改善受整體複合勁度與載重傳遞效率所限制**）。
- 襯砌厚度對鋼襯應力：「weak sensitivity」——並給機制上界：鋼襯應力主要由**內壓＋圍岩約束**共同決定，**經由裂縫傳遞的厚度影響不能超越這個力學邊界**。⚠️ 這句是頂級寫法：把 null result 轉成「我找到了一個力學邊界」。
- 相對地，凡是「有效」的參數都給出可操作結論（雙層配筋、縮小間距、優選高勁度圍岩）。

### 設計建議就地下錨，不留到結論

`preference should be given to formations with high stiffness…` / `a double-reinforcement configuration is therefore recommended…` / `The optimal thickness should balance crack control with economic efficiency.` —— 全部寫在 4.x 段末，Conclusions 只是再列一次。

## (e) 貢獻凸顯（位置與措辭）

**五處錨定，措辭一致：**

| 位置 | 措辭核心 |
|---|---|
| Abstract 第 2 句 | 「This study **proposes** a coupled thermo-mechanical numerical framework based on the finite-discrete element method, which **can effectively predict** the random cracking process and crack evolution patterns of the lining.」（先給工具＋工具能力） |
| Abstract 末句 | 「The **proposed framework provides a reliable theoretical and engineering basis** for safety assessment and design optimization of LRCs in CAES applications.」（賣用途） |
| **Fig. 2 圖內文字** | 綠底橫幅＋"Issue 1"／"Issue 2" 方框——**用圖宣告缺口，等於用圖宣告貢獻** |
| Intro 第7段（方法差異句） | 「FDEM **differs significantly from** conventional FEM, which models cracking as diffuse material degradation.」＋列舉 FDEM 能直接解析的四件事 |
| Intro 第7段末（目標三動詞） | provide a discontinuous numerical method / systematically evaluate / provide a basis for assessing sealing integrity |
| Conclusions 首句 | 「This study **developed** a coupled thermo-mechanical numerical framework based on FDEM to investigate…」 |

**關鍵觀察：貢獻詞是 framework，不是 finding。** 五個參數組的所有結果都被包裝成「框架的應用示範」，而非獨立發現。這讓論文即使結論偏工程直覺（勁度越高越好、雙層配筋較好），也不會被評為「無新意」——因為賣點在工具。

**第二層貢獻（藏在附錄 C）**：**裂縫寬與等效裂縫孔隙率的量化定義與後處理演算法**。這其實是最硬的方法貢獻，卻被放在附錄且沒在摘要點名。⚠️ 這是他們的失誤（或謙抑），我們不要學——**原創的量化指標定義應該進正文並在摘要點名**。

## (f) 缺陷包裝

**全文沒有「Limitations」小節，沒有「Future work」段落，Conclusions 只有 5 條編號findings 就直接接 CRediT。** 弱點採**分散就地埋設**策略——在每個技術主張的當下承認，然後立刻用一句話拆解。

### 五處明寫的弱點與拆解話術

1. **驗證誤差 50%，卻寫進正文（p.14）**——最精彩的一段：
   - 承認：模擬起裂壓力 1.16 MPa（Group A）／1.42 MPa（Group D），比 Yang (2020) 實測的 0.7／0.9 MPa **高約 50%**。
   - 拆解成三因子，其中**兩個把責任推給實驗與材料，只有一個是模型的**：(1) 材料理想化（忽略骨材–砂漿界面過渡區 ITZ，而 ITZ 才是真實起裂弱點）；(2) **試驗缺陷**（試體本身有澆置缺陷與微孔隙，數值幾何沒有，所以真實起裂門檻被拉低）；(3) 本構限制（雙線性內聚律對微觀應力集中的敏感度捕捉有限）。
   - 救援句：儘管量值有差，模型成功重現裂縫**擴展路徑與分佈型態**，因此「validating its reliability **for comparative analysis** of lining performance」——⚠️ **把模型用途從「絕對預測」降規為「比較分析」，一句話就讓 50% 誤差變得可接受。** 這是我們的模型必然會遇到的處境，這句是模板。
2. **CZM 本身的參數不可測（p.9）**：坦承峰值法向/切向 traction 無法由試驗直接得到，必須用數值反算——並直接寫成「an inherent limitation of the CZM」。**把限制歸給方法本身而非自己的實作**。
3. **解析熱力模型的五條假設（p.5）**：材料均質等向、洞內空氣溫壓密度空間均勻、圍岩外邊界定溫、忽略壓致體積變化、長徑比大故簡化為一維徑向熱傳。收尾：「儘管這些假設引入了理想化，Zhou et al. (2015) 的完整驗證研究已顯示……誤差在工程可接受範圍內」——**用他人的驗證替自己的假設背書**。
4. **熱效應可忽略的自我否定（p.17）**：他們最亮眼的發現（熱應力有利）被自己加上邊界：在保守設計、溫變適中、結構勁度足夠時，熱荷載可合理忽略，「這個簡化有助於精簡設計與分析而不損及結構安全與密封性能」。⚠️ 把「我的耦合可能沒必要」翻譯成「我證明了何時可以不做耦合」——**限制被改寫成設計指引**。
5. **厚度研究的範圍限制（p.22–23）**：「It is worth noting that…」承認厚度組只看了襯砌開裂與密封層響應、未同時調整配筋率，實務上厚度需與配筋率合併設計。放在 4.3.3 末，以實務忠告的語氣寫。

### 完全沒提的六件事（我們的機會）

1. **裂縫→漏氣率的閉環從未建立**。全篇不斷講 airtightness / impermeability，但「等效裂縫孔隙率」只是幾何代理量，**從頭到尾沒有換算成任何滲流量或漏氣率**，也沒有任何滲流計算。
2. **只算第一個工作循環（約 40 h）**。所有參數化圖的標題都是 "during the first working cycle"。前言引 Jiang (2024) 說長期循環累積損傷使裂寬非線性成長，自己卻沒做長期循環——**疲勞被反覆提及（fatigue risk / fatigue damage）卻從未被計算**。
3. **軸向厚度只有 0.6 m 的準二維切片**（模型平面尺寸 16×洞徑，軸向僅 0.6 m）。號稱 3D，實為薄片；**縱向裂縫、施工縫、環縫效應全部不在**。
4. **零厚度內聚元素的網格依賴性完全未討論**。這是 cohesive-element 插入法的經典弱點（裂縫路徑受網格拓樸限制、破壞能受元素尺寸影響），全文只在 2.4 提到「網格尺寸依幾何比例、敏感度分析與計算效率選定」，**沒有任何裂縫型態的網格收斂測試**。
5. **號稱 stochastic bifurcation / random cracking，卻只跑單一實現**。沒有多重隨機種子、沒有材料非均質性的統計分佈，「隨機」實際上只來自網格拓樸的非結構性。
6. **密封層沒有破壞準則**。鋼襯用 Q420 彈塑性，Case 1-1 平均 von Mises 已達 403.2 MPa（逼近 420 MPa 降伏），文字僅寫「potential risk of local yielding」，**沒有給出密封失效判準，也沒說裂縫寬到多少密封層就失效**——這正好是題目承諾的 sealing system response 的最後一哩，被留白了。

⚠️ 對我們最重要的一條：**第 1 與第 2 條（漏氣閉環、長期循環）正好是我們的水位循環題目天生要處理的**。我們若做「裂縫開度→導水度→孔隙壓→開度」的閉環＋多循環，直接就是對這篇的方法論增量。

## (g) 圖表數與類型

**22 圖、5 表、23 式**。圖表密度極高（正文 23 頁配 22 圖，約每頁一圖），且**六張同型裂縫圖＋六張同型指標圖**構成結果主體。

### 圖（22）

| 圖 | 類型 | 內容 |
|---|---|---|
| 1 | **3D 概念渲染圖（藝術級）** | CAES 系統全景：風光電站→變電→地面廠房→施工輔助隧道→硬岩層中的儲氣洞群；含資訊方塊（最大內壓 10–16 MPa、埋深 100–200 m、混凝土襯砌＋密封層、最短循環 1 天）＋放大插圖顯示圍岩/密封層/襯砌裂縫 |
| 2 | **缺口圖示（照片＋雲圖蒙太奇＋Issue 方框）** | 左：室內先導模型試驗（平台/試體/已裂內襯/環向裂縫）；右：連續體 FEM 網格＋損傷雲圖＋壓力時程；下：Issue 1／Issue 2 文字框 |
| 3 | **結構分層爆炸示意圖** | LRC 3D 剖切＋四層引線（密封/滑動/二次襯砌/初期支撐）＋每層的材料選項小圖（橡膠・鋼板／瀝青／RC・SFRC・PFRC／鋼筋網噴凝土・岩栓錨索） |
| 4 | **理論概念圖（7 面板 a–g）** | (a) 真實混凝土裂縫照片；(b) 三區破壞機制（traction-free／FPZ／彈性區）；(c) 黏結應力–張開位移關係；(d) FPZ 的離散數值表示（三角形彈性元素＋介面元素，三色標示完好/損傷/破斷）；(e)(f) 拉/剪雙線性 traction-separation；(g) **B-K 混合模式破壞能準則 3D 圖** |
| 5 | **標定模型＋曲線（8 面板）** | 單軸壓（100×200 mm 圓柱，91,686 solid＋176,787 cohesive）與拉（狗骨 100×100×600 mm，135,212 solid＋263,007 cohesive）的網格、C30/C40 破壞型態、應力–應變曲線（含標註點） |
| 6 | **工程模型＋荷載（4 面板）** | (a) 3D 圍岩–襯砌–密封系統含邊界約束（16R×16R）；(b) 網格細部（solid＋zero-thickness cohesive、內/外/噴層鋼筋三層）；(c) **循環氣壓時程**（初始循環 42 h、規則循環 24 h：充氣6h/高壓儲氣7h/放氣4h/低壓儲氣7h，4–10 MPa）；(d) **循環溫度時程**（初始 42 h→溫度響應期 120 h→初步穩定期） |
| 7 | **驗證模型（4 面板）** | (a) 鋼襯 RC 管模型試驗照片（電阻應變計、千分表）；(b) 設計圖（R200/R250、內外環筋）；(c) 邊界條件；(d) 網格類型（C3D8／C3D4／T3D2／COH3D6） |
| 8 | **驗證對比（含定量圖）** | (a.1–a.4)(b.1–b.4) 模擬裂縫發展與最大主應力雲圖；(c) 四張試體實測裂縫照片；(d) **雙 Y 軸圖：裂縫寬（線）＋裂縫條數（柱狀）對內壓**，標註起裂壓力 1.16／1.42 MPa、最大寬 0.083／0.094 mm、最大條數 1120／3255 |
| **9, 13, 15, 17, 18, 21** | **裂縫分佈剖面線圖（同一模板 ×6）** | 圓形斷面線畫圖，把離散裂縫畫成襯砌環上的短線段；Fig.9 另加溫度雲圖版本 |
| **10, 14, 16, 19, 20, 22** | **指標演化＋密封層應力多面板（同一模板 ×6）** | (a) 最大裂縫寬 vs 時間；(b) 等效裂縫孔隙率 vs 時間（兩圖都標出 Initial-charging／Storage／Discharging／Storage 四階段虛線）；(c)(e)(g) von Mises 沿 NDP 0–360°（含平均線與陰影帶、標 Tunnel Crown／Tunnel Invert）；(d)(f)(h) von Mises 應力幅值沿 NDP |
| 11 | **等效塑性應變 PEEQ 雲圖** | 四個勁度案例 × 開挖後/最大內壓兩列，標最大深度 |
| 12 | **極座標圖** | 圍岩徑向位移沿 0–360°，八條曲線（四勁度 × 開挖/最大壓），標 11.77/5.79/4.14/3.08 mm |

### 表（5）

| 表 | 內容 |
|---|---|
| 1 | C30/C40 內聚元素參數（E、ν、ρ、Mode-I/II 破壞能、法/切向勁度係數、法/切向峰值 traction） |
| 2 | **五個結構的材料本構總表**（風化層／圍岩粉砂岩 M-C／噴凝土 C25 CDP／混凝土襯砌 C40 CZM／鋼襯 Q420 彈塑性），最後一欄「Another constitutive parameter」用**交叉引用**（Refer to Lee and Fenves 1998／Refer to Table 1／Refer to Menegotto 1973）而非列數字 |
| 3 | **工況矩陣（16 案例）**：Case 0-0 基準＋五組（1-x 圍岩模數 6/16/20 GPa；2-x 內/外單層配筋；3-x 鋼筋直徑 16/22/25 mm；4-x 間距 50/150/200 mm；5-x 厚度 40/60/80 cm），最後一欄給換算配筋率。**用「/」符號表示「與基準案例相同」**，並在表註說明 |
| 4 | 驗證管模型配置（Group A/D：鋼板厚 1/1.5 mm、配筋率 1.286/2.288%、試驗壓力 1.3/2.1 MPa） |
| 5 | 驗證管模型的數值參數（C30 solid／C30 cohesive／Q235 鋼板／HRB300 鋼筋 四欄，不適用處填「/」） |

⚠️ **Table 3 的「/」= 同基準** 是我們的工況表可以直接抄的排版慣例——16 個工況壓成半頁，且一眼看出是 OFAT（單因子輪動）設計。

## (h) 對我們的啟示（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）

### 1. 【最新做法·裂縫量化】直接照抄「兩指標＋一附錄演算法」的呈現體系

這篇的離散開裂量化用了**四種表徵，分工明確**：

- **開度（核心，唯一貫穿全文的量）**：`最大裂縫寬 w_max (mm)` 的**時程曲線**——隨充放氣循環上升、在放氣段回落（裂縫閉合），四階段以虛線分隔。這是他們唯一每組都畫的量。
- **總量（原創指標）**：`等效裂縫孔隙率 φe (%) = 累積裂縫體積 V_total / 襯砌環總體積 V_lining`（Eq. 23）。定位為「巨觀工程損傷指標」。
- **條數**：**只在驗證段用**（Fig. 8d，破斷 cohesive 元素數 1120 vs 3255，並換算成佔全部元素的 1.2% vs 3.5%）。工程尺度段**改用「密度／疏密／平均間距」定性＋一句定量（平均間距 <0.5 m）**。
- **長度／連通性**：**完全不量長度**，改用「貫穿 vs 非貫穿（through / non-through）」「連通性 connectivity」的**二分定性分級**。

**裂縫寬的演算法（附錄 C，可直接移植到我們的 DEM 後處理）**：不是量節點相對位移，而是**幾何反推**——
(i) 篩出 `SDEG > threshold` 的破壞內聚元素；
(ii) 取變形後節點座標 `x_i = X_i + u_i`，算幾何形心 C0（Eq.18）；
(iii) 把六面體六個面各切成兩個三角形，各與 C0 組成四面體，**一個 8 節點元素分解成 12 個四面體**，用向量純量三重積求體積（Eq.19–20）；
(iv) 全模型加總得 V_total（Eq.21）；
(v) **平均裂縫寬 = 該元素變形後體積 / 該元素未變形中面投影面積**（Eq.22，假設張開後形如以初始中面為底的稜柱）。

⚠️ **我們的行動**：把這套「**開度時程 + 等效孔隙率 + 貫穿性分級 + 條數僅用於驗證**」的四層量化直接搬過來，但要做三個升級：(a) 把 φe 換算成**滲透率/導水係數**（用 cubic law），補上他們沒做的滲流閉環；(b) 條數不要只用在驗證，工程尺度也報，因為我們有**現地裂縫調查的條數與間距**可以對；(c) 附錄 C 那種原創定義**放正文**並在摘要點名。

### 2. 【最新做法·與密封/防水系統互制】三個具體寫法

- **界面怎麼建**：層間用**硬接觸（法向罰函數，Kn = 1.0×10¹⁴ N/m³）＋庫倫摩擦**（岩–襯 μ=0.6、襯–密封 μ=0.3），並對**所有襯砌元素另加 general contact**，以免內聚元素破斷後新生裂面互相貫入導致計算發散。附錄 B 給完整公式（Eq.14–17，含 Kn = α·E/l_min，α≈10）。
- **指標怎麼抽**：定義 **NDP（Normalized Distance Path）**——以襯砌環中心為原點，自右側中點起**逆時針轉 360°**，沿此路徑抽鋼襯 von Mises 應力，展開成一維曲線。同時報 **平均應力（紅色虛線）** 與 **應力幅值（循環內波動）**，用**陰影帶**畫出波動範圍，並在橫軸標出 **Tunnel Crown／Tunnel Invert** 位置。核心術語是 **circumferential nonuniformity（圓周不均勻性）**。
- **論述鏈怎麼寫**：`裂縫在充放氣中的張開/閉合 → 密封層局部應力狀態 → 應力幅值 → 疲勞損傷風險`；關鍵術語 **deformation coordination mismatch（變形協調失配）**、**stress coordination（應力協調）**、**mechanical compatibility**。反向也敢寫：襯砌厚度對鋼襯「弱敏感」，因為鋼襯應力主由內壓與圍岩約束決定，**裂縫傳遞的影響不能越過這個力學邊界**。

⚠️ **我們的對應**：把「鋼襯 von Mises + NDP」換成「**防水膜/排水層界面的法向張開量 + 剪切位移沿 NDP 展開**」，或「二次襯砌與初期支撐界面的接觸應力沿 NDP」。**「平均值＋幅值＋陰影帶＋標示拱頂/仰拱」這套圖，是可以一比一複製的。**

### 3. 【對照差異句】熱力循環（他們）vs 水力循環（我們）——差異點就是我們的賣點

| 面向 | 本文：熱–力循環 | 我們：水力循環 |
|---|---|---|
| 驅動 | 內壓 4→10 MPa（1 天週期）＋內壁溫度 290→339 K，形成 30–40 K 徑向梯度 | 地下水位升降 → 襯砌背後孔隙水壓循環（季節/年週期） |
| 荷載方向 | 由內向外（內壓為主動荷載） | 由外向內（外水壓）／或降水造成有效應力重分佈 |
| 溫度/水的耦合性質 | **有利的負回饋**：熱膨脹→環向壓應力→抵銷內壓拉應力→裂寬 −34%、孔隙率 −74%、鋼襯應力幅 −30%；**熱效應自我抑制裂縫** | **不利的正回饋**：裂縫張開→導水度上升（cubic law, ∝w³）→孔隙壓進一步侵入→有效應力下降→裂縫再張開；**無任何抵銷機制** |
| 時間尺度 | 只算第一循環（40 h），並宣稱約 10 個循環後溫度趨近熱平衡 | 需算多年、多循環；疲勞與劣化是主體而非附註 |
| 溫度耦合的必要性 | 作者自己承認「保守設計下可合理忽略」 | 水力耦合**不可忽略**，因為它是正回饋 |

**可用的英文對照句草稿（自撰，非引用）**：
> "In CAES lined rock caverns, thermo-mechanical cycling is partly self-limiting: the thermally induced hoop compression offsets a portion of the internal-pressure tension and thereby narrows the crack aperture. Cyclic groundwater loading in an operating mountain railway tunnel offers no such counter-stress. Instead, an increment of aperture raises fracture transmissivity, which admits more pore pressure and reopens the crack — a positive hydro-mechanical feedback rather than a self-stabilizing one. The lining crack problem therefore has to be posed over many cycles, not one."

⚠️ 這段話同時做了三件事：致敬、劃界、宣告增量。**建議直接放在我們前言第 5–6 段之間當轉折段。**

### 4. 【架構與門檻】驗證只到「文獻的縮尺模型試驗」，誤差 50% 仍可過稿——但話術要學到位

他們的驗證鏈是：**別人 2020 年碩論的鋼襯 RC 管模型試驗（幾何比 26.25:1）→ 比對裂縫路徑與分佈型態（定性吻合）＋最大裂寬（0.083 vs 0.087 mm、0.094 vs 0.096 mm，很準）→ 但起裂壓力高估 50%（1.16 vs 0.7 MPa）**。處理方式是三因子歸因（兩個推給實驗與材料）＋**把模型用途降規為「comparative analysis」**。

⚠️ **我們的行動**：(a) 驗證用**現地裂縫調查／監測資料**比對「裂縫間距與開度分佈」即可，不必追求絕對起裂值；(b) 誤差要主動寫出並歸因（ITZ、既有施工缺陷、材料非均質、本構簡化）；(c) 一定要有那句「本模型的可靠性在於**比較分析與參數敏感度**，非絕對預測」。這句是我們的護城河。

### 5. 【方法標定與分區】FDEM 只給襯砌、其餘用連續體——這正是我們跨尺度 FDM-DEM 的先例

原文明說：襯砌域離散為**彈性 solid 元素 + 零厚度內聚介面元素**，破壞準則達到即劣化並刪除該內聚元素、拓樸上生成真實不連續面；而**圍岩與鋼襯用標準連續體有限元素、假設保持完整，理由是「把計算資源集中在襯砌的開裂行為上」**。元素型別為 C3D8／C3D4／COH3D6／COH3D8／T3D2（Abaqus 命名體系），本構含 CDP、Mohr-Coulomb、Menegotto 鋼筋——換言之，**這是「零厚度內聚元素插入的有限元」，掛上 FDEM 的品牌**（引 Munjiza 2004／Mahabadi 2012／Lisjak 2020 定根）。

⚠️ **兩個直接推論**：
- **分區賦予不同方法、並明講理由，是 TUST 接受的**。我們的「圍岩用 FDM 連續體、襯砌與節理帶用 DEM 離散」完全站得住，但**必須像他們一樣，用一句話交代「為何只在此區用離散法」**（集中算力於開裂區）。
- **方法命名有彈性但要有系譜**：他們把 cohesive-element FEM 稱作 FDEM，靠的是引三篇 FDEM 經典把系譜接上。我們稱「跨尺度 FDM-DEM」時，同樣要在方法系譜段接上 Cundall／Itasca 耦合的經典錨，別讓審稿人抓命名。

**另外三個立即可用的小抄**：
- **參數標定寫法（2.4 節）**：理論映射式給初值（Blal 2013 的 KnLmesh/E ≥ 19/(1−2ν)、Ks/Kn = 2(1−2ν)/(1+3ν)）→ 虛擬單軸壓/拉試驗 → **解耦三步標定**（先標微觀勁度對彈模、再調法/切向強度對峰值、最後微調破壞能對後峰值軟化）→ 敏感度分析確認「微勁度控彈模、微強度控峰值強度、破壞能控軟化」。並老實寫「迭代紀錄從略」。
- **工況表用「/」表示同基準**（Table 3），16 案例壓成半頁。
- **Conclusions 只寫 5 條編號 findings、半頁、無 future work**——TUST 允許。所有設計建議已在 4.x 就地下錨。

---
*筆記全文覆寫：2026-07-25；access = full-pdf（26 頁全讀）。全文直接引語僅一句（7 字，已標引號）。取代 2026-07-21 的 abstract-only 版本，原推測標記均已由全文證據替換或推翻。*
