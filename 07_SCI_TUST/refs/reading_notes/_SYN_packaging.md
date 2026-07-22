# _SYN_packaging — 不完美的包裝目錄（interim）

> **目的**：彙整 reading_notes 全部筆記中「論文如何處理自身弱點」的實證手法（縮尺、參數無實測、單案例、驗證薄弱等），
> 逐項對照我們的弱點清單（f=0.25 縮尺、100 m 情境擺幅 vs 實測 ~30 m、單案例、素混凝土 BPM、現地裂縫型態差異、K0=0.7），給出可直接落筆的包裝句式。
> **樣本**：37/56（interim）——全文級 (f) 證據 25 篇＋摘要層可觀察 12 篇；其餘 19 篇 metadata-only 不計入。
> **建檔**：2026-07-22。所有範例均為對各篇筆記之轉述，非原文引語；落筆引用前請回查對應筆記與原文。

---

## Part A｜包裝手法總目錄（十式，附範例論文）

樣本中的第一個大發現：**「無獨立 Limitations 節」是常態而非例外**。25 篇全文樣本中，設獨立 limitations 節者僅 2 篇（Zhang S. 2025、（半個）Ma 2023——後者甚至不掛標題）；其餘 23 篇全部用下列十式把弱點「就地消化」。TUST/IJRMMS/EFA 審稿實務對此的容忍度有大量刊出證據。

### A1. 假設條款前置法（assumption-as-setting）
把簡化寫成「建模設定」而非「弱點自白」，集中放在方法節開頭，**每條掛 1–4 篇前例文獻當護盾，之後全文不再回顧**。
- **Yan 2023（TUST）**：2D 平面應變、地應力取 Mont Terri 資料、斷層厚 2 m、模型域大小——全部塞在模型設定節、逐項配引文，正文與結論零遲疑；連「域夠大」都只自我宣告、不展示收斂測試。
- **Wu 2024（IJNAMG）**：§3.1「General consideration」一次講清靜水壓、均質等向、廣義 Kelvin 等假設，每項掛 3–4 篇文獻示範「前人也這麼做」，並附一句坦誠「雖可能引入誤差」後即前行。
- **Fahimifar 2009（TUST）**：假設以編號 bullet 條列前置（軸對稱、穩態、水面不動…），「先講清楚，之後不再道歉」。
- **Wang 2023（EFA）**：所有簡化打包成 3.3 節末的編號「建模假設」清單（均質、無地下水、僅自重場），放在結果之前，讀起來是設定不是懺悔。

### A2. Scope 限定／缺陷改寫成「適用範圍」
把「做不到」翻譯成「本法適用若…」，語氣從防守變服務；甚至在題目就完成限定。
- **Cai 2004（IJRMMS）**：結論明寫僅適用低圍壓（<5 MPa）、不適用塑性降伏岩體——限制寫成「定義域」，全文不出現 limitation 字眼。
- **Fahimifar 2009**：驗證算例直接產出兩條編號適用條件（r_e/h_1 < 1/3、埋深 ≥ 5–10 倍洞徑）——限制變使用手冊。
- **Tsang 2023（RMRE）**：FJM 對孔隙率的表徵缺陷寫成「對中等孔隙率砂岩足夠泛用；低孔隙率高脆性岩應改用他型模型」——缺陷＝適用範圍聲明。
- **題目級 scope**：Wang X. 2021 把 "the west section" 寫進題目，先天免疫「為何不含全隧道」；Yoon 2007 以 "in uniaxial compression simulation" 收尾框死適用域；Nitka 2015 把載重條件寫進題目兼作 scope statement。

### A3. Future work 收納／限制-未來 1:1 鏡像
每個弱點立即配一個「已規劃的解方」，缺陷改寫成 roadmap。
- **Zhang S. 2025（TUST）**：教科書級示範——limitations 獨立成節但**放在結論之後**（結論保持零瑕疵）；先揚後抑開場（先稱已取得重大進展才認限制）；每條用 "may reduce / could affect" 假設語氣；三條限制與三條 future work 完全 1:1 鏡像（只做 flysch→未來擴岩類；未含支撐→未來納入）。且**只挑 scope 類限制講**，迴避方法論硬傷（16 參數反算非唯一性隻字未提）。
- **Ma 2023（C&G）**：結論後、CRediT 前的無標題小段："can be further enhanced by improving…"——弱點被說成升級空間；工具限制歸給 FLAC3D（軟體的錯不是設計的錯）；漏掉的因素 spin 成「使結果偏安全側」。
- **Wang T.-T. 2024（TUST）**：指標「可透過更多案例或數值模擬進一步驗證修正」——單案例的外推問題一句轉嫁給 future work（還順便把我們這種後續模擬論文寫成它的驗證者）。
- **Tsai in-review（IJRMMS）**：Discussion 末以三個開放問句收尾＋"warranting further research"——限制翻譯成研究前景。

### A4. Trend-level 措辭／「平均反應」免責框架
預先宣告模型目標是抓「平均／代表性／主導趨勢」，把打不到的散布定義成界外球。
- **Barla 2012（IJoG）**：先聲明監測數據因不均質、異向性、非靜水應力而大幅散射（軸對稱模型本就無法表現），再宣告目標是 capture the **average** response——模型與數據不合的部分預先劃出戰場。
- **Wu 2024**：解析模型的目的本來就是抓 mean response，實測散布反映問題本身的非對稱性，不是模型錯。
- **Vazaios 2019（JRMGE）**：反直覺發現緊跟 "under specific conditions" 圈住普適性風險；不確定性用 "may lead to / potentially minor" 情態詞內嵌於發現句，不設獨立缺陷段。

### A5. 沉默不提（silent boundary）
最高頻的一招——明顯弱點完全不寫，賭審稿人不逼問。**但有紅線**（見 Part C）。
- **Yin 2022（TUST）**：每級荷載僅 12 h 的短時潛變試驗外推 20 年——全文沉默；審稿一輪過。
- **Sharifzadeh 2013（TUST）**：地質節明寫某區段 high water inflows，模型完全無水——沉默；後來同團隊 Tarifard 2022 自己補這個洞（示範「留一手當續集」）。
- **Chen 2024（TUST）**：無地下水、無時間相依、每工況僅 1 試體、無真實案例——全部不提，結論零保留。
- **TianX 2021（TUST）**：「僅由外力造成」的單因強歸因如何排除他因——摘要與 highlights 均迴避。

### A6. 弱點反轉成賣點（reframe-as-asset）
- **Potyondy 2004（IJRMMS）**：DEM 最常被打的「粒徑怎麼選」被反轉成物理發現（粒徑與斷裂韌度連動）——把方法的最大質疑點改寫成方法的物理內涵。
- **Wang T.-T. 2024／Chiu 2017（TUST）**：稀缺性反轉——單案例長期監測「非常罕見」，n=1 從缺陷翻成資料價值；缺口與資料價值同一句完成。
- **Tsang 2023**：計算昂貴→直接給出每迭代耗時、總時數、容差-成本曲線，收束成「建議操作區間」——弱點改寫成使用指南。
- **Kovacevic 2021（TUST）**：單次模擬 50 分鐘的成本不當弱點寫，反而當 NN 代理模型的存在理由——痛點改寫成動機。
- **Yin 2022**：FLAC3D 不能模擬不連續面→順勢轉向規範安全係數法——工具限制變成引入新評估方法的理由。
- **TianY 2026（TUST）**：模型箱邊界反射波（試驗 artifact）寫成「反射波與夾層滑移疊加產生斜裂縫」的觀察結果——瑕疵就地轉化為發現（高風險招，慎用）。

### A7. 互證即免責（triangulation-as-shield）
建立「試驗—數值—理論」或「理論—試驗—數值」互證閉環＋專設互證小節，用一致性當可靠度盾牌，暗示無需自曝侷限。
- **TianY 2026**：三法互證＋7.3 專節四方一致（含真實震害）→ 全文零 limitations、零 future work，TUST 照收。
- **Chen 2024**：4.6 節理論 vs 數值、試驗 vs 數值兩張誤差對比表（±10% 內）取代討論節，作為全文合法性收束。
- **Sharifzadeh 2013／Tarifard 2022**：驗證階梯（解析解 benchmark → 監測比對 → 長期外推）——「先取信、後預測」。

### A8. 位置戰術（burial & sequencing）
弱點放在讀者注意力最低處；結論版面保持全正面。
- **Zhang S. 2025**：limitations 放結論**之後**。
- **Ma 2023**：結論後無標題段。
- **Kovacevic 2021**：全文最誠實的一句藏在 4.1 場址描述末段（非結論），且前面先鋪「換斷面只需重跑、方法論不變」的緩衝——先給解方再認限制。
- **Chiu 2017**：精度損失（補強遮蔽基準點）只在方法節一句帶過，不量化、不討論對結論的影響。

### A9. 誠實但限定框（admit-with-containment）
主動承認誤差，但立刻用時間框／成因歸屬把它圈進無害區。
- **Wang 2023**：反算相對誤差最大 31.01% 全表列出，一句 "誤差大者集中在開挖後短期" 收納，整體仍宣稱 in good agreement。
- **Yin 2022**：模擬 vs 600 天監測前 6 個月不吻合——主動歸因「監測從新襯砌才開始、初期變形被漏計」，差異外部化為量測時機問題；第 14 個月起吻合→宣告能反映長期特性。
- **Wu 2024**：前 30 天預測與實測落差先坦承並歸因（起測時間不同、非靜水壓），再主張整體趨勢吻合，最後打出「事件級命中」王牌（讓壓元件降伏 0.282 vs 實測 0.283 MPa）——一個銳利數字勝過十條大致吻合的曲線。

### A10. 讓步-反轉句式（concession–reversal）
"Although…" 讓步子句一行帶過，緊接正面收束，不展開。
- **Sulem 1987（IJRMMS）**：結論 "although valid for simple tunnel geometry and field stress conditions" 一行，緊接 "can give a reasonable estimate"。
- **Li 2021（Nat. Hazards）**：唯一認錯藏在驗證段："Although the attenuation creep stage slightly deviates" → 立接 overall effect is good、high reliability。
- **Zhang S. 2025**：先揚（重大進展）後抑（certain limitations remain）。

### 驗證薄弱的專用三招（跨 A4/A7/A9 的組合技）
1. **定性一致升格為驗證**：Yan 2023 僅「震源集中位置與微震觀測定性一致」，結論即升格為 "validate the efficiency"；An 2026 僅滲流路徑順序一致，一句「高度一致」帶過，無逐點誤差。→ TUST 對「位置／順序／型態級」的定性比對當驗證，有大量先例。
2. **借文獻區間當標尺**：Tsang 2023 把 σci/σc=0.46、σcd/σc=0.83 與文獻經驗區間（0.42–0.47、0.78–0.90）並排——單一數字升級成「真實性證據」。
3. **借他人案例背書空間分佈**：Tarifard 2022 引 Xu 2019「Dujia 隧道裂縫先出現在 spring-line」替自己模擬的危險位置背書——用別人的實測幫自己的模式驗證。

---

## Part B｜逐項對照：我們的六個弱點 × 包裝方案

> 通則：每個弱點選 2–3 式組合（**前置假設＋一個主動防禦動作＋一句收束措辭**），全文只在一處處理、不重複道歉。英文句式為可直接改寫的骨架（〔〕內代填）。

### B1. f=0.25 縮尺（模型縮尺／縮尺參數設定，非現地實測值）

**風險**：審稿人問「f=0.25 怎麼來的？縮尺後與原型行為的相似性何在？」
**主打**：A1 假設條款＋前例護盾 → A6 敏感度自我拆彈 → A2 scope 收束。

- **範例做法轉述**：
  1. **Liu D. 2022（TUST，1/10 縮尺襯砌試驗）**——縮尺正當化完全靠先例背書：用原型材料、忽略自重，引 Yuan 1998 及三篇同做法先例（He 2009、Yashiro & Okano 2018、Ding 2020）把相似律缺陷「常規化」。做法：一句設定＋一串「他們也這樣」的引文，不辯論相似律本身。
  2. **Fahimifar 2009**——難標定參數 η 的自我拆彈：先承認需大量率定，隨即用 16 個量級的參數掃描證明其對力學結果不敏感（2.02→1.93 MPa）、給出上下界供設計——缺陷在同一篇內被實驗性中和。
  3. （反例警戒）**An 2026**——C_K=1 對上幾何比 1/40，時間相似比僅一語帶過、換算從未交代，全文沉默仍過刊——說明 TUST 行情容忍沉默，但這是可被後續論文攻擊的把柄，我們不宜全抄。

- **建議句式**：
  - 前置設定＋護盾：*"Following common practice in reduced-scale / calibrated DEM studies (〔refs〕), the friction coefficient was set to f = 0.25, consistent with 〔標定來源／相似律換算〕."*
  - 敏感度拆彈：*"A sensitivity scan over f = 〔0.15–0.35〕 confirmed that the simulated crack pattern and its cycle-dependence remain qualitatively unchanged, with peak crack width varying by less than 〔X〕%; f therefore acts as a second-order parameter within the studied range."*
  - scope 收束：*"The adopted value should be regarded as a calibrated model parameter rather than a field-measured property; the conclusions are framed in terms of relative (cycle-to-cycle) response, which is insensitive to this choice."*
  - 心法：把「f 的絕對值可信度」換成「結論只依賴相對趨勢」——這是 A4 trend-level 的參數版。

### B2. 100 m 情境擺幅 vs 實測 ~30 m

**風險**：「你模擬的水位擺幅是實測的三倍多，結論還算數嗎？」
**主打**：A2 情境化（scenario framing）＋界限案例論證＋把實測值放進掃描範圍內。

- **範例做法轉述**：
  1. **Tarifard 2022（G3 期刊）**——水位 10–60 m 是**假想情境**（assumed water tables），非實測序列；用 scenario 框架讓「沒有實測水位資料」變成研究設計而非缺陷。審稿人看到的是「界定清楚的範圍」，不是「承認的短板」。
  2. **Paraskevopoulou 2018（TUST）**——界限案例修辭：彈性解＝瞬時開挖、零黏度＝無限循環時間，所有參數結果框在兩極端之間讀，給讀者天然座標系。100 m 可比照定位為 upper-bound envelope。
  3. **An 2026**——五水準一次排列的參數掃描寫法（歷時、滲透比、淨距各 5 水準），把單一情境問題溶解在「敏感區間」的交付裡（滲透比 100–500 最敏感）。

- **建議句式**：
  - 情境宣告：*"Groundwater-level fluctuation amplitudes of 〔30, 50, 70, 100〕 m were considered as design scenarios, spanning the range from the monitored seasonal amplitude (~30 m at the study tunnel) to an upper-bound envelope representative of extreme recharge events / long-term hydrogeological change."*
  - 界限定位：*"The 100 m case is intended as a bounding scenario that brackets the plausible response envelope, rather than a prediction of the site condition."*
  - 交付轉向：*"Within this range, the crack-growth response was found to be most sensitive between 〔30–60〕 m, which covers the monitored amplitude"*——把重點從「100 m 真不真」移到「敏感區間涵蓋實測值」。
  - 心法：**實測 30 m 必須是掃描水準之一**（最好是基準工況），100 m 退居包絡角色；絕不能讓 100 m 單獨扛結論。

### B3. 單案例

**風險**：「n=1，外推性何在？」
**主打**：A6 稀缺性反轉＋單案例自造對照組＋A3 future work 轉嫁。

- **範例做法轉述**：
  1. **Wang T.-T. 2024／Chiu 2017（TUST，同一系譜）**——稀缺性反轉：營運隧道位移＋裂縫＋剝落三合一長期紀錄「非常罕見」→單案例從缺陷翻成資料價值。且**單案例內自造對照組**：滑動體內外、補強範圍內外、補強前後（2024）；同型態×淺深覆蓋矩陣（2017）——一條隧道切出多組可比樣本。
  2. **WangX 2021（TUST）**——scope 內建於題目（"the west section"）＋摘要結果句反覆條件化（"For the WS of…"），臨界深度 100 m 明確綁定本案不外推。
  3. **Kovacevic 2021**——「換別的斷面只需重跑模擬、方法論不變」的緩衝句：單案例限制被「方法可移植性」對沖。
  4. **TianX 2021**——lessons-learned 收尾把 n=1 個案正當化為通則知識，預堵「只是個案」質疑。

- **建議句式**：
  - 稀缺反轉：*"Operating mountain railway tunnels with concurrent long-term records of lining cracks and groundwater level are exceedingly rare; the 〔案例名〕 tunnel therefore offers an uncommon opportunity to anchor a cross-scale model against decade-scale field evidence."*
  - 自造對照：*"Within the single case, contrasts are constructed along three axes — sections inside vs. outside the high-fluctuation reach, wet vs. dry seasons, and cracked vs. intact lining panels — providing internal replication in lieu of multiple cases."*
  - future work 轉嫁：*"Extension of the calibrated framework to tunnels in different lithologies and hydrogeological settings is straightforward and is left for future work; the methodology itself is case-independent."*
  - 心法：仿 Chiu/Wang 系譜——把「一個案例」寫成「一組內部對照矩陣」；情境矩陣（有/無水位循環、不同幅值）本身就是我們的對照組。

### B4. 素混凝土 BPM（DEM 襯砌無配筋）

**風險**：「真襯砌有鋼筋，素混凝土模型的開裂行為能代表嗎？」
**主打**：A1 假設條款＋A6 保守方向 spin＋A2 scope（聚焦混凝土基材開裂）＋工具歸因備援。

- **範例做法轉述**：
  1. **Liu D. 2022**——試體不配鋼筋，理由寫成「為便於設置不同工況裂縫」——把試驗能力上限包裝成**主動的範圍設定**（不是做不到，是設計選擇）。
  2. **Ma 2023**——雙重示範：(i) 工具歸因——鏽蝕鋼筋組成律粗糙歸咎於 FLAC3D 只能用 beam element（限制是軟體的，不是研究設計的）；(ii) 保守 spin——不考慮某因素時聲稱 "make the results become safer"。
  3. **TianY 2026**——微混凝土襯砌無配筋相似——全文沉默仍過 TUST（行情證據，但同樣是可攻擊點）。
  4. **Chen 2024**——模型試驗不配鋼筋＋只做 4 工況，理由寫成鐵片預製裂縫「切割埋設易產生較大誤差，故不再增設」——能力上限寫成主動取捨。

- **建議句式**：
  - 主動設定：*"The lining is represented as plain concrete in the DEM sub-domain, a deliberate simplification that isolates the crack initiation and propagation behaviour of the concrete matrix — the phase in which the observed field cracks originate — from reinforcement-related effects."*
  - 保守方向：*"Since reinforcement would restrain crack opening and delay coalescence, the plain-concrete idealization yields conservative (upper-bound) estimates of crack width and density under groundwater-level cycling."*
  - scope＋future work 鏡像：*"Explicit reinforcement, bond-slip and corrosion coupling are beyond the present scope and constitute a natural extension of the framework."*
  - 心法：三句剛好走 A1→A6→A3 的順序，一段內收束，全文不再回頭。注意與現地對照時，若實際裂縫型態受配筋控制（如裂縫間距），要先用 B5 的「型態級一致」策略框定比對層級，避免自打。

### B5. 現地裂縫型態差異（模擬 vs 巡檢實錄不完全吻合）

**風險**：「模擬裂縫圖案與現地展開圖對不上，驗證何在？」
**主打**：驗證三招（定性一致升格＋文獻區間標尺＋他人案例背書）＋A4 平均反應框架＋A9 誠實限定框。

- **範例做法轉述**：
  1. **Yan 2023**——只做到「震源集中於隧道近旁與同深度，與 Husen 2012 觀測一致」的定性比對，結論即宣稱 validate the efficiency——TUST 買單「位置級一致＝驗證」。
  2. **An 2026**——驗證僅「滲流路徑順序一致」（右拱腰→右拱肩→仰拱→…），一句「高度一致」帶過——順序級一致也算。
  3. **Barla 2012**——散射免責框架：先聲明實測散布源自不均質與非對稱（模型本就不表現），target＝average response；模型間差異回溯到公式本質，寫成「模型內稟差異」而非缺陷。
  4. **Chiu 2017**——不一致處以「原因與環境的固有不確定性」一句吸收所有離群觀察。
  5. **Wu 2024**——「事件級命中」策略：全曲線不求吻合，選一個可精確對標的事件量釘死可信度。

- **建議句式**：
  - 比對層級宣告（先發制人）：*"Model performance is assessed at the pattern level — crack location, orientation, and the sequence of appearance — rather than crack-by-crack correspondence, which is neither expected nor meaningful given the inherent variability of lining heterogeneity and construction history."*
  - 一致性主張：*"The simulated cracks concentrate at 〔部位〕 and develop predominantly 〔縱向/環向〕, consistent with the mapped distribution in the inspection records; the predicted onset sequence 〔A→B→C〕 likewise matches the chronology inferred from successive inspections."*
  - 事件級命中（若有）：*"Notably, the model reproduces the surge in crack widening recorded after the 〔某年豪雨/驟降事件〕, with the simulated onset at cycle 〔N〕 corresponding to 〔實測日期/門檻〕."*
  - 離群吸收：*"Local deviations are attributed to construction joints and thickness variations not represented in the model, factors documented in the maintenance records."*
  - 心法：**先降級比對目標（型態/位置/順序），再全力命中降級後的目標**——這是樣本中驗證薄弱論文的共同生存法則；有一個銳利的事件級數字就足以升格全段。

### B6. K0=0.7（側壓係數假定值，無現地量測）

**風險**：「K0 哪來的？初始應力態直接控制襯砌內力分佈。」
**主打**：A1 假設＋區域資料/文獻護盾 → **升級招：把 K0 從假設轉成參數軸** → A2 基準綁定。

- **範例做法轉述**：
  1. **Yan 2023**——地應力「依 Mont Terri 資料」＋引兩篇文獻（Urpi 2019、Rinaldi & Urpi 2020）——一句設定＋引文護盾，不再討論。
  2. **Liu 2022（IJMST）**——側壓係數=1（靜水應力場）以「為簡化計算所作假設」名義在結論末段一次打包，配 "後續研究進一步考慮" 收尾；更早已在方法節前置消毒（先講假設、後不追究）。
  3. **WangX 2021**——**最強做法**：初始水平應力比不是假設而是**掃描參數**（參數研究五因子之一），並產出「應力比↑→收斂比↑」的可引用結果——弱點直接變成貢獻軸。
  4. **Wu 2024**——靜水壓假設掛 refs 36–42 示範慣例，再以「納入非對稱推導工作量極高、會使工具失去實用性」的成本效益論證正當化。

- **建議句式**：
  - 設定＋護盾：*"In the absence of site-specific stress measurements, K0 = 0.7 was adopted as the baseline, consistent with the regional stress regime reported for 〔台灣西部麓帶/相應地質區〕 (〔refs〕) and with values back-analysed for comparable metamorphic/sedimentary settings (〔refs〕)."*
  - 參數軸升級：*"To bound the influence of this assumption, K0 was varied over 〔0.5–1.2〕; the crack-relevant response (crown vs. sidewall stress redistribution) shifts systematically with K0, but the cycle-driven incremental damage — the focus of this study — remains governed by the groundwater fluctuation amplitude across the full K0 range."*
  - 心法：句式後半是關鍵——**證明「我們的主結論對 K0 不敏感」比「K0 準不準」更重要**；若敏感，就學 WangX 2021 把它升格為正式參數研究的一軸，弱點變第二貢獻。

---

## Part C｜佈局總表與紅線

### C1. 各弱點的「安放位置」建議（依樣本位置戰術歸納）

| 弱點 | 安放位置 | 手法組合 | 是否設 limitations 提及 |
|---|---|---|---|
| f=0.25 縮尺 | 方法節 DEM 標定小節（A1）＋敏感度小節（A6） | A1＋A6＋A4 | 不需 |
| 100 m 擺幅 | 情境矩陣表格所在的工況設計小節 | A2 情境化＋界限案例 | 不需 |
| 單案例 | 前言（稀缺反轉）＋案例節（對照矩陣）＋文末一句 future work | A6＋A3 | 可一句 |
| 素混凝土 BPM | 方法節建模假設清單一段收束 | A1＋A6 保守 spin＋A3 | 可一句 |
| 裂縫型態差異 | 驗證節開頭先宣告比對層級（先發制人） | A4＋驗證三招＋A9 | 不需 |
| K0=0.7 | 方法節一句＋參數研究一軸 | A1＋參數軸升級 | 不需 |

- **limitations 專節**：建議比照 Zhang S. 2025——若設，放結論之後、只收 scope 類 2–3 條、每條配 future work 鏡像、用 may/could 語氣；六個弱點中最多放「單案例」與「素混凝土」各一句，其餘已在正文就地消化，不重複。
- **摘要與結論**：零弱點詞（37 篇樣本無一例外——摘要層完全不見 limitation 蹤影是常態）。

### C2. 紅線（樣本中的反面教材）

1. **承諾了卻不交付**：Liu D. 2022 前言路線圖明說會討論 limitations，結論卻蒸發——雖過審，但這是給審稿人的免費把柄。要嘛不承諾，承諾就交付。
2. **root-cause 式自我矛盾**：Wang 2023 在 2.2 節明說地下水是病害 root cause，建模假設卻直接排除水、相隔 6 頁無任何解釋——正是被後續論文（含我們）點名攻擊的缺口。**我們的題目就是水**，因此任何在前文被賦予因果地位的因素（如配筋、溫度）都不可在模型中無聲排除——必須用 B4 式的「主動設定＋保守方向」明寫。
3. **假精度**：TianY 2026 縮尺試驗報兩位小數百分比、WangTT 2024 單位不一致與量級疑點——皆獲刊，但引用時要小心不要傳染；我們的 DEM 輸出量報值位數應與可信度相稱。
4. **瑕疵轉發現（A6 極端版）慎用**：TianY 把邊界反射波 artifact 寫成觀察結果——若被識破是誠信級風險，我們不用此招。
5. **沉默的前提是「不在自己的主軸上」**：Yin 2022 對短時外推沉默能活，因為外推不是它的賣點；我們對「水」相關的任何簡化（如未模擬滲流-裂縫雙向回饋）不能沉默，因為那正是主軸——主軸上的簡化只能用 A1＋A2 明寫。

### C3. 一段話總結（寫作時貼在螢幕邊）

> 樣本 37 篇的共同語法：**弱點不是用「承認」處理，是用「定義」處理**——定義成假設（A1）、定義成適用範圍（A2）、定義成未來工作（A3）、定義成研究目標（A4 的「本就只求平均反應」）、或定義成貢獻（A6 的敏感度/參數軸）。位置上前置不後置、集中不分散、一次不重複；驗證上先降級比對目標再全力命中；摘要與結論永遠零弱點詞。TUST 的刊出證據顯示這套語法的容忍度很高，但紅線是不可與自己的主軸敘事矛盾。

---

*來源：本目錄之全部手法均轉述自 reading_notes 各篇筆記之 (f) 缺陷包裝節；篇名縮寫對應筆記檔名。metadata-only 的 19 篇（Zheng 2024、Cho 2007、Yoon 2007（僅題目層計入 A2）、Jun 2023、Nitka 2015（僅題目層計入 A2）、Liu 2023、Peng 2017、Bai 2022、Sulei 2022、Yuqi 2018、Jingqi 2023、Weixin 2023、Lisjak 2015、Zhou 2024、Rasmussen 2024、Lionel 2015、Bai 2025 等）未計入手法統計；取得全文後應回填並更新本目錄（樣本升級 37→56）。*
