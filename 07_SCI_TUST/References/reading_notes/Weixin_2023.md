# Sun Weixin et al. (2023) — Experimental assessment of structural responses of tunnels under the groundwater level fluctuation

- **書目**：Sun Weixin; Han Fucheng; Zhang Yanmei; Zhang Wengang; Zhang Runhong; Su Weijia (2023). *Tunnelling and Underground Space Technology*, 137, 105138. https://doi.org/10.1016/j.tust.2023.105138
- **access = full-pdf**（本機 PDF 全文精讀：`07_SCI_TUST/References/PDF/1-s2.0-S088677982300158X-main.pdf`，15 頁含 2 頁參考文獻；精讀日期 2026-07-22，本筆記全面覆寫先前 metadata-only 版）
- **單位/通訊**：重慶大學土木工程學院；通訊作者 Wengang Zhang。審稿時程：收稿 2022-05-16 → 修回 2023-02-09 → 接受 2023-04-02（歷時約 11 個月，一輪大修）。
- **Keywords**：Groundwater level; Tunnel; Model test; Structural response; Buoyancy reduction; Time lag effect
- **主庫定位**：REFS_MASTER L1「水文→襯砌載重與劣化」；用途＝水位升降結構響應實驗證據，正當化我們模型的暫態外水載重循環邊界條件。
- **一句話**：1g 縮尺模型箱（砂/黏土兩種地層 × 圓形交通隧道/矩形共同溝兩種斷面，共 4 組試驗），量測單次水位升—停—降全程的接觸壓力、彎矩、孔壓、浮力、垂直位移；核心發現＝黏土浮力折減（0.75–0.78）受時滯效應控制、結構經一次水位循環後內力高於初始且產生殘餘沉陷。

## (a) 題目解剖（全文確認）

- **開頭元素**：**方法**（"Experimental assessment"）——研究行動名詞化開場，非案例、非現象。
- **有無方法詞**：有（"Experimental"）。
- **構式**：`[方法行動] of [響應對象] under [外部驅動條件]`
  - "Experimental assessment | of structural responses of tunnels | under the groundwater level fluctuation"
  - 受詞是 *responses*（把「響應」名詞化為評估對象），"under + 水文驅動" 收尾。
  - 文法瑕疵："the groundwater level fluctuation"（單數＋定冠詞，母語者慣寫 fluctuations）——全文另見 "stared to float"（conclusions 錯字）、Eq (3) 重複編號為 (2)、Fig. 20 圖說誤植 "in Fig. 14"，顯示 TUST 對語言瑕疵容忍度確實不低。
- 無地名、無案例名、無定量詞——一般化實驗研究路線。**題目未透露** tunnels 實為淺埋圓形＋矩形兩種、地層為砂/黏土——題目刻意最大化一般性。

## (b) 文章架構（節序與比重；正文 13 頁）

| 節 | 內容 | 篇幅 | 佔比 |
|---|---|---|---|
| 1. Introduction | 4 段 | ~0.9 頁 | ~7% |
| 2. Model test design and experimental setup | 2.1 材料（砂/黏土、模型製作）＋2.2 裝置量測（模型箱、監測項目） | ~2 頁 | ~15% |
| 3. Test procedure and program | 4 組試驗系列、分層填築/固結/注排水程序 | ~0.7 頁 | ~5% |
| 4. Test results and data analysis | 4.1 圓形隧道 ×（接觸力/孔壓/彎矩/浮力/垂直位移）→ 4.2 矩形隧道 × 同五項 | ~8 頁 | ~62% |
| 5. Conclusions | 3 條編號結論 | ~0.5 頁 | ~4% |

- **骨架特徵**：結果節採「2 斷面 × 5 響應量」平行矩陣，每一響應量固定配「時程曲線圖＋特徵水位包絡圖」，砂/黏土成對敘述——高度模板化、可複製。
- 第 4 節開頭先放**受力分析示意圖（Fig. 9，含膨脹角滑動面抗浮機構）**當詮釋框架，數據才進場——「先給力學透鏡、再看數據」的安排值得學。
- 無獨立 Discussion 節：機制詮釋全部內嵌於結果小節；無 Limitations 節。

## (c) 前言手法（4 段）

- **P1（宏觀鋪陳）**：都市化→地下空間→交通隧道與共同溝是生命線，須確保安全。引用密度低（2 組引文）。
- **P2（問題 staging）**：災害威脅→鎖定地下水為最顯著風險因子；列舉水位波動的驅動（氣候變遷海平面上升、都市化、隧道施工降水、超抽）與後果（湧水湧泥、上浮、地表沉陷、縱向變形、滲漏與襯砌扭曲）。引用密集（~12 篇）。段尾第一層缺口："However, despite these efforts, the problem has not been completely resolved, and further research is necessary."（泛缺口）
- **P3（文獻回顧）**：逐篇點名式回顧——數值（Gattinoni & Scesi 監測反演、Shivaei 3D 雙隧道、Lu ABAQUS 黏土、Wu Timoshenko 梁）、解析（Zhang 複變函數）、少數實驗（Liu 2023 砂層自製裝置）、岩石隧道滲流穩定（Bhattacharya & Dutta）。段尾補一句共同溝研究尚少但需求漸增——為矩形斷面的納入預埋正當性。
- **P4（第二層缺口→貢獻）**：缺口收斂句式＝「現有分析 *primarily conducted through numerical simulations or theoretical derivations*，受限於對理論模型與模擬的依賴」→ 貢獻句式＝"In this study, the interaction law between [結構與土] during [水位升降] in [砂與黏土層] was studied through the scaled model experiments." → 量測項目清單句 → 收尾承諾實用價值："Constructive suggestions were put forward to prevent..."
- **缺口 staging 是兩層式**：P2 尾泛缺口（問題未解決）＋ P4 頭方法論缺口（實驗證據不足——與摘要首句 "researches...based on the experiments are still insufficient" 呼應）。摘要與前言的缺口口徑一致。
- 無 roadmap 段（"The remainder of this paper..."不存在）——TUST 不強制。

## (d) 結果敘事

- **圖領句起手**：每小節第一句幾乎都是「Fig. N shows the change of [響應量]...」或 "As shown in Fig. N, in the sand experiment, ..."——先錨定圖號，再展開。
- **敘事單元的固定節奏**：圖領句 → 以測點編號（A-11、C-9…）映射到結構部位（vault/spandrel/arch foot/bottom/四角）描述變化過程 → 給**臨界水位門檻**（砂中圓形 ~43 cm 起浮、黏土 ~50 cm；矩形砂 ~39 cm、黏土 ~48 cm）→ 機制詮釋子句（浮力、時滯、有效應力、濕化弱化承載力，常帶引文）→ 砂 vs 黏土、圓 vs 矩交叉對照。
- **量化方式**：以趨勢語言＋特徵數值為主——浮力折減係數（砂 0.95–0.99≈可忽略；黏土圓形 ~0.75、矩形 ~0.78）、最大上浮量（砂 0.53 mm vs 黏土 0.37 mm）、彎矩極值（矩形黏土 −1.37/0.92 N·m；75 cm 水位 1.20/−1.62 N·m）。無統計、無誤差棒；量測誤差以一句 "can be easily observed due to the experimental error and measurement error" 帶過。
- **機制詮釋深度**：黏土時滯效應追到微觀三因（低孔隙比、低飽和度氣泡堵孔、結合水膜）；起浮前「先隨土沉降（濕化弱化承載）→浮力超過自重起浮→退水殘餘沉陷」的三段式運動敘事貫穿全文。
- **內部交叉驗證修辭**：圓形與矩形量得的浮力折減係數 "essentially identical, thus validating the conclusion"——用兩幾何互證增強可信度，替代重複試驗。
- **結果→工程意涵橋接**（4.2.3 末）："The changes may lead to structural cracking, water seepage, and other related problems. Therefore, it is essential to pay attention to groundwater level changes during the planning, design, and construction..."——在結果節內直接下工程結論。

## (e) 貢獻凸顯

- **摘要**：新穎性掛在裝置與方法——"self-designed experimental equipment and innovative experimental methods"；結論性亮點三個（臨界位置、黏土浮力時滯折減、週期性沉浮＋末段大沉陷）。
- **前言 P4**：貢獻＝填補「實驗證據不足」的方法論缺口＋承諾 constructive suggestions。
- **結果節內**：即時貢獻句（見 (d) 末條）＋交叉驗證句。
- **結論**：先一句定位——本文可作為抗浮研究與實務建設的 "notable reference"——再列 3 條編號 key findings：(1) 臨界位置辨識（圓形＝vault/spandrel/arch foot/bottom；矩形＝四角、底板中央、側牆中央）；(2) 黏土浮力折減 0.75–0.78 獲確認、砂可忽略、受時滯控制，實務應納入 "to save cost and ensure safety"；(3) 沉—浮—沉序列與退水殘餘沉陷。
- 貢獻語言全程克制：無 "first/novel breakthrough" 等強詞，靠「self-designed／confirms／identified」等動詞堆疊。

## (f) 缺陷包裝

- **無 Limitations 節**；缺陷全部化整為零、就地消化：
  1. 土性不確定性不計——包裝成有引文背書的合理簡化："The testing soil...possessed great grading...went through well compaction. Therefore, the uncertainty in soil properties is not considered (Wang et al., 2023)."（第 3 節，一句帶過）
  2. 退水段浮力不討論——以量測原理限制為由的範圍排除："Since the measured pore water pressure cannot reflect the actual buoyancy during the groundwater level drop...were not discussed in this study."（4.1.4，陳述句口吻，無歉意）
  3. 低水位段係數波動——歸因儀器精度與時滯，一句附註化。
  4. 黏土固結超沉導致實際埋深偏離設計（31.2 vs 32 cm）——當事實報告，不評估其影響。
  5. 唯一 future work 放在 4.2.4 小節末（非結論）："the fitting relationship between groundwater buoyancy reduction coefficient and clay properties still needs further study."
- **完全沒提的**：1g 縮尺的應力相似律失真（幾何 1/30 但無相似比推導）、模型箱邊界效應（1.5×0.8×1.2 m）、僅單次升降循環（非多循環）、微混凝土模型是否開裂未檢查、無重複試驗。**Conclusions 零缺陷字句**——缺陷永不進結論，是本文最鮮明的包裝策略。

## (g) 圖表數與類型

- **21 圖 + 3 表**（TUST 實驗文的高圖量端）。
- 表：土性參數（T1）、模型設計參數原型/模型對照（T2）、試驗系列矩陣（T3）——三張都是「一眼可查」的設定表。
- 圖分四類：
  1. 實物照片×5（材料、鋼筋籠/澆模、模型箱、感測佈設、完成填土）——實驗可信度背書；
  2. 示意圖×4（粒徑曲線、感測器佈點圖、3D 流程示意 Fig.7、受力分析 Fig.9）；
  3. 時程多線圖×4（接觸壓力 Fig.10/16、孔壓 Fig.12/18；上緣同步標水位刻度——**雙 x 軸「時間＋水位」設計**，把邊界條件直接印在數據圖上，值得抄）；
  4. 特徵水位包絡圖×4（圓形極座標 Fig.11/13、矩形展開包絡 Fig.17/19，各含升/降×砂/黏 4 分圖）＋係數/位移對水位曲線×4（Fig.14/20/15/21）。
- 每個響應量固定「時程圖＋包絡圖」成對出圖，砂/黏、升/降以子圖並列——圖版邏輯與文字敘事完全同構。

## (h) 對我們（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）啟示

1. **循環邊界條件的最強實驗背書**：本文實測「一次」水位升—停—降後，接觸壓力與彎矩即高於初始值且留下殘餘沉陷（砂/黏、圓/矩四組皆然）——即單循環已具不可逆性。我們前言可據此立論：既然單循環留殘餘內力增量，多循環（季節性/豐枯水年）之累積效應與裂縫襯砌之交互作用更不可忽視——這正是暫態循環外水載重邊界條件的實驗正當化，且把我們從「穩態水壓」區隔開。引用位置：前言水文段＋方法章邊界條件設定段。
2. **缺口 staging 的精準對接**：本文明說水位變化 "may lead to structural cracking, water seepage"（可引全文引語，8 字 <15 字上限），**點名裂縫為後果卻完全未研究裂縫**——淺埋土層、彈性未裂微混凝土模型、浮力主導機制。我們的缺口句可寫成：土層淺埋隧道之水位波動響應已有實驗刻畫（Sun et al., 2023），但「岩體深埋＋既有裂縫襯砌＋滲流—裂縫跨尺度力學」的響應機制仍空白——本文是我們的 experimental counterpart，我們補機制解析端（FDM-DEM）。
3. **可移植句式**：(i) 缺口收斂句 "the analysis is primarily conducted through [A] ... limited by its reliance on [A]"——我們鏡像反轉：實驗與現場觀測已有、跨尺度機制模型闕如；(ii) 貢獻句 "In this study, the interaction law between [X] and [Y] during [Z] was studied through [方法]"；(iii) 交叉驗證句 "essentially identical, thus validating..."——可移植為 FDM 與 DEM 在耦合界面/重疊區的互證修辭；(iv) 結果節奏「圖領句→部位映射→臨界門檻→機制子句→對照」直接套用於我們的裂縫擴展敘事（臨界水位門檻 ↔ 我們的裂縫起裂/貫通臨界水頭）。
4. **時滯效應的類比遷移**：本文把黏土低滲透性的孔壓時滯捧成關鍵字級發現（buoyancy reduction、time lag effect 皆入 keywords）。我們岩體裂隙網絡滲流同樣造成外水壓對水位變化的暫態滯後——可引本文為「時滯/暫態路徑相依性有實驗證據」，正當化我們用暫態滲流耦合而非瞬時靜水壓更新。
5. **差異化與撞型迴避**：本文題目以方法開頭（Experimental assessment）、無案例無地名；依 00 號檔題目方向（案例＋機制構式），我們應以案例/現象開頭（營運山岳鐵路隧道襯砌裂縫），"under cyclic groundwater level fluctuations"（用複數、避其文法瑕疵）收尾，並植入 cross-scale/FDM-DEM 方法詞——與本文自然錯開。另注意其包裝術的反面教訓：縮尺相似律與單循環限制隻字未提仍過稿，說明 TUST 審稿對實驗文的 limitations 要求鬆；但我們數值文的驗證鏈（vs 本文這類實驗數據）反而會被嚴查——可把本文的浮力折減係數/臨界水位當作我們土層退化情境子模型的獨立比對標的。
