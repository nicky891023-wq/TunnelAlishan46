# Kovacevic et al. (2021) 精讀筆記 — 寫作工藝萃取

**書目**：Kovačević, M.S., Bačić, M., Gavin, K., Stipanović, I. (2021). Assessment of long-term deformation of a tunnel in soft rock by utilizing particle swarm optimized neural network. *Tunnelling and Underground Space Technology*, 110, 103838. DOI: 10.1016/j.tust.2021.103838
**取得方式**：full-local（本機 PDF：Wade_TD_SCI/Reference/2020_2025/case/，TU Delft 機構典藏版，正文 15 頁）
**審稿時程**：收稿 2020-07-02 → 修訂 2020-12-28 → 接受 2020-12-29 → 上線 2021-01-22（一輪大修後極速接受）
**內容一句話**：以 FLAC 修正 Burgers-creep 黏塑性模型（HB 破壞準則）產生參數-變位資料庫 → 訓練 NetRHEO 類神經網路作代理模型 → PSO 反算最可能流變參數組 → 以克羅埃西亞 Pećine 公路隧道 15 年監測驗證，並預測鄰近百年 Brajdica 鐵路隧道改建後 30 年長期變形。

---

## (a) 題目解剖

> Assessment of long-term deformation of a tunnel in soft rock by utilizing particle swarm optimized neural network

- **開頭元素**：任務詞＋現象起頭——「Assessment of long-term deformation」（評估×長期變形）先行；不是案例名、不是機制、不是方法。
- **有無方法詞**：**有**，且放在句尾——"particle swarm optimized neural network"（PSO＋NN 兩個方法詞疊在一起當修飾語）。
- **構式**：`[任務動名詞] of [現象] of [對象] in [地質情境] by utilizing [方法]`。五段式：Assessment｜long-term deformation｜a tunnel｜soft rock｜PSO-NN。
- **觀察**：案例名（Pećine/Brajdica）完全不入題，用泛化的 "a tunnel in soft rock" 拉大適用性；方法詞收尾表明這是「方法論文包著案例」而非「案例論文」。TUST 明顯接受這種現象先行、方法收尾的題式。

## (b) 文章架構（節序與比重，正文約 13 頁）

| 節 | 標題 | 比重 | 角色 |
|---|---|---|---|
| 1 | Introduction | ~1.2 頁 | 動機＋缺口＋貢獻 |
| 2 | A constitutive representation of time-dependent deformations | ~2 頁 | 修正 Burgers＋HB 理論（Eq.1–7，Fig.2–3） |
| 3 | Estimation of rheological parameters by using the PSO algorithm | ~2.5 頁 | 方法：3.1 四步驟總覽／3.2 NetRHEO／3.3 PSO（Eq.8–15，Fig.4–5） |
| 4 | Validation of the methodology: long-term behavior of tunnels Pećine and Brajdica | ~5.5 頁 | 案例：4.1 場址→4.2 輸入參數→4.3 監測資料庫→4.4 NN 應用→4.5 PSO 估計→4.6 改建衝擊量化→4.7 30 年預測 |
| 5 | Conclusions | ~0.7 頁 | 重述貢獻＋資產管理意涵 |

- 比重核心在第 4 節（>40%）：**方法只佔 1/3，驗證與應用佔一半**——用案例的厚度撐起方法的可信度。
- 第 4 節內部是「漏斗式」：場址→參數→資料→代理模型→反算→兩個應用場景（鄰近開挖衝擊、30 年預測），一路由已知走向預測。
- 補充資料（Supplementary）放 NN 建構資料庫與 32 種架構試誤紀錄，正文只留結論——冗長的 trial-and-error 外移，保正文流暢。

## (c) 前言手法（5 段）

1. **段1｜通說鋪陳**：NATM 哲學假設「隧道完工後變形迅速穩定」——先立一個業界共識當靶子。
2. **段2｜However 反例轟炸**：軟岩/岩溶岩 squeezing 打破通說；連舉三個帶年份的實例（Lyon-Torino 施工中斷面縮減、日本公路隧道完工 17 年後隆起、挪威 Laerdal 開挖 4 年後噴凝土破壞），且直接把破壞照片放進前言（Fig.1）——用視覺證據強化「問題是真的」。
3. **段3｜社群已知但不夠**：長期監測文獻回顧，落點在「量測變形顯著大於計算值、趨勢也不同」→ 時間相依行為必須納入設計。
4. **段4｜缺口 staging**：預測難在「流變參數評估極複雜」→ 室內試驗昂貴費時 → 引 Boidy（室內參數不能直接用於預測）→ Eurocode 7 建議監測 10 年以上 → Ureshino 案例示範監測資料可反算參數。缺口收斂為：**如何從長期監測資料有效反算流變參數**。
5. **段5｜貢獻句＋方法概述**：以 "This paper presents an approach to predict the long-term behavior..."（轉述）開頭，接著兩句講 NN 估參數、PSO 選最可能組，末句點明克羅埃西亞案例驗證。無逐節 roadmap——用方法流程概述取代。
- **staging 邏輯鏈**：通說 → 反例（照片）→ 量測>計算 → 參數瓶頸 → 監測+代理模型+反算 = 本文。每一段都替下一段挖好洞。

## (d) 結果敘事

- **圖領句**：每個結果段落以「資料/結果示於 Fig. X」型句子開場，隨後緊接 "It is clearly visible that..." 式的判讀句——先指圖、再說圖會說話的那件事。
- **量化方式**：**百分比是主要修辭貨幣**——15 年間拱頂變位增加 70%、地表點增至 153%；水平位移 <8% 垂直位移（用來正當化只取垂直）；Brajdica 開挖後 Pećine 拱頂 +8%、地表 +10%（對照前一年僅 0.5%/1%）；2035 預測比 2020 大 39%（拱頂）/48%（地表）；Brajdica 30 年再增 125%；年增量衰減至 0.5%/年。絕對值（cm、mm）只當背景，百分比才是說服工具。
- **NN/PSO 成效量化**：R²=0.9979–0.9991、MSE~1e-8 四資料集並列；PSO vs GA 用 Table 2 對決（f_min 1.2597e-8 vs 1.7823e-8），文字宣稱 PSO 收斂效率顯著優於 GA——**方法優勢用同場對照實驗坐實，不空口**。
- **機制詮釋**：節制。把長期增量歸因於 "omnipresent long-term deformations in soft karstic rock"（岩溶軟岩潛變無所不在），不深入微觀機制——機制留在第 2 節本構層次，結果節只做現象級歸因。
- **驗證敘事骨架**：hindcast→forecast 兩段式。Fig.11 用反算參數重現 15 年監測（驗證），Fig.13 左半 hindcast＋右半 15 年 forecast、事件處加放大插圖（inset）——**同一張圖完成「我算得準」與「所以未來可信」的過渡**，是全文最強的一張敘事圖。

## (e) 貢獻凸顯

- **位置**：三明治式——摘要（proposes/demonstrates the potential）、前言末段（presents an approach + 案例驗證）、結論首尾（重述方法鏈＋收在管理意涵）。
- **措辭**：不用 novelty 大詞（無 "for the first time"）；改用「組合式貢獻」：修正 Burgers＋HB（承 Itasca/文獻）× NetRHEO 代理 × PSO 反算 × 15 年實測——每個元件都有出處，新意在**組裝與實證**。
- 3.1 節把方法論寫成**編號四步驟清單**，把「可複製的流程」本身當成貢獻展示。
- 把建模選擇翻轉成貢獻：採 5 個觀測點被寫成「比過去只用襯砌收斂量測的研究前進一步」（a step forward from previous studies）——選擇→優勢的措辭翻轉。
- 結論最後一段跳出技術層：告訴 tunnel managers 儀器化資產能換得長期韌性資訊——**以資產管理價值收尾**，貼合 TUST 讀者群。

## (f) 缺陷包裝

- **無獨立 limitations 節、無 future work 節**。
- 最誠實的一句藏在 4.1 場址描述末段（非結論）：只反算流變參數、其他影響因子（地質條件、覆蓋、支撐、鄰近振動）需另行數值分析，"poses certain limitation of the presented study"（原文，<15 字）。**位置淡化**：放在讀者注意力最低的案例描述段落，且前面先鋪「換別的斷面只需重跑模擬、方法論不變」的緩衝——先給解方再認限制。
- **scope 式淡化**：只用垂直位移 → 用「水平 <8%」的量化理由＋引 Xiang et al. (2018) 同行先例雙重護航；單一監測斷面 → 說明 Pećine 共 8 個斷面、其餘斷面照方法重跑即可。
- **成本轉化**：單次模擬 50 分鐘的計算負擔不當弱點寫，反而當成 NN 代理模型必要性的論據——把痛點改寫成動機。
- 量測誤差（4.3 節）主動交代：隨機誤差靠安裝工藝壓低、系統誤差用數學程序修正——先自曝再自答，堵審稿人的口。

## (g) 圖表數與類型（14 圖 2 表）

| 類型 | 圖號 | 用途 |
|---|---|---|
| 現場照片 | Fig.1（破壞照×2）、Fig.6a（時間軸照片帶） | 前言動機／案例歷史 |
| 概念示意 | Fig.2（彈簧-阻尼元件）、Fig.4（NN 架構）、Fig.5（PSO 更新示意） | 理論與方法視覺化 |
| 準則圖解 | Fig.3（MC vs HB，公式直接嵌入圖中） | 本構選擇正當化 |
| 平面/斷面 | Fig.6b（雙隧道平面）、Fig.7（監測儀器斷面） | 場址與量測布置 |
| 數值雲圖 | Fig.9、Fig.12（FLAC 垂直位移 contour） | 開挖/改建即時效應 |
| 時間序列 | Fig.8（15 年實測）、Fig.11（模擬 vs 實測）、Fig.13（hindcast+forecast＋inset）、Fig.14（30 年預測，雙軸：位移+年增率%） | 核心結果 |
| 迴歸散佈 | Fig.10（train/val/test/all 四宮格） | NN 成效 |
| 表 | Table 1（本構輸入值）、Table 2（PSO vs GA 對決） | 參數透明＋方法對照 |

- 特色：照片(3)＋示意(4)＋結果(7) 的節奏約 1:1:2；Fig.3 把公式塞進圖裡省正文篇幅；Fig.13 的 inset 放大與 Fig.14 的雙軸（絕對值+年增率）是「長期預測」的高效表達模板。

## (h) 對我們（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）的啟示

1. **題式可直接套用**：`[任務詞] of [長期現象] of [an operating mountain railway tunnel] under [地下水位循環] by [cross-scale FDM-DEM]`——本文證明 TUST 接受現象先行＋方法收尾、案例名不入題的構式；我們的「營運中鐵路隧道」比它的 "a tunnel" 更具體，是賣點不是包袱（它的案例恰好也是百年鐵路隧道改建，可引為同類先例）。
2. **hindcast→forecast 是長期敘事的黃金骨架**：先用監測資料（裂縫計/水位計時序）反算參數重現歷史，再同一張圖右延預測、事件點（豪雨/乾旱循環）加 inset 放大——複製 Fig.13 版式；預測結果用「相對增幅 %＋年增率衰減曲線」表達（Fig.14 雙軸），對 TUST 的資產管理讀者最有感，結論末段收在維管單位價值。
3. **昂貴正演模型的標準包裝**：跨尺度 FDM-DEM 單次計算成本高——照抄其三件套：(i) 明寫單次模擬耗時當代理模型動機；(ii) 參數資料庫→代理→反算→驗證寫成編號步驟清單；(iii) 冗長的收斂/試誤細節全放補充資料。另外它只掃 5^3=125 組參數就敢發 TUST，說明參數空間不必大、邏輯鏈完整即可。
4. **缺陷處理範本**：不設 limitations 節；把「只考慮單一因子」的限制用一句話埋進案例描述段、前面先鋪「方法論不變」緩衝；把建模取捨（如我們只取特定裂縫模式或簡化滲流路徑）寫成「比既有研究前進一步」的措辭翻轉；量測誤差主動交代處理方式，堵審稿口。
