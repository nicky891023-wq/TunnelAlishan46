# _SYN｜Q1 題目解剖統計（跨篇綜合）

> **建檔**：2026-07-22。**樣本狀態**：任務書載明「樣本=37/56（interim）」；實際執行時 `reading_notes/` 已有 **56 份筆記、全數納入統計（56/56）**，與 REFS_MASTER 56 篇一一對應（本統計 TUST 佔 31/56 ≈ 55%，恰合主庫「TUST 55%」記錄）。仍標 **interim**：約半數筆記 access=abstract-only/metadata-only，但題目解剖 (a) 節以「題目本身」為證據，不受全文缺席影響。
> **方法**：Glob 全部 `*.md`（跳過 `_SYN` 開頭）→ 彙整各筆記「(a) 題目解剖」節之開頭元素、方法詞、構式判讀；期刊由各筆記書目節核實。逐篇分類見附錄，可回溯查核。
> **定位**：依交接鐵則，本檔只做統計、評分與**建議**；題目定稿由 Wade 決定。

---

## 1. 開頭元素分佈（題目第一個實質元素）

分類口徑：案例（地名/工程專名起手）｜現象（病害/響應/場量/屬性起手，含「現象+analysis」）｜機制（mechanism/interaction/effects of X on Y/門檻概念起手）｜方法（方法名、模型名、解型、試驗/解析體裁宣告起手）｜應用端（對策/交付物/願景/預測任務起手）。

| 開頭元素 | 全樣本 n=56 | TUST n=31 | 其他期刊 n=25 |
|---|---|---|---|
| **方法** | 24（42.9%） | 12（38.7%） | 12（48.0%） |
| **現象** | 16（28.6%） | **11（35.5%）** | 5（20.0%） |
| **機制** | 10（17.9%） | 3（9.7%） | 7（28.0%） |
| **應用端**（對策/交付物/願景/預測） | 5（8.9%） | 4（12.9%） | 1（4.0%） |
| **案例**（地名起手） | 1（1.8%） | 1（3.2%） | 0 |

**判讀（含樣本偏誤校正）**：
- 「其他期刊」子樣本刻意收了大量 DEM/BPM 方法經典（Potyondy 2004/2015、Cho 2007、Yoon 2007、Nitka 2015、Peng 2017、Tsang 2023、Bai 2025、Lisjak 2015…），**方法開頭 48% 是被方法期刊灌高的**，不能直接當投稿基準。
- **TUST 內部**：方法開頭（38.7%）與現象開頭（35.5%）雙主流；但拆開看，TUST 的方法開頭一半是「體裁宣告」（Experimental investigation / Analytical study / Simulation of），真正以數值方法名領頭的（Zhou 2024、Wang 2020、WangZ 2026、Rasmussen 2024、Liu 2019、Yan 2023）**全是方法貢獻型論文**。
- **案例地名起手在 TUST 只有 1/31**（Moradi 2021，且自貼 "A case study" 標籤）——案例匿名化（"an operating/operational tunnel"、"a deep-buried tunnel"）是壓倒性慣例；專名頂多進冒號副標（3/31）。
- 機制開頭在 TUST 反而少（9.7%），但 2024–2026 卷有升溫跡象（Xin 2024、TianY 2026）。

## 2. 方法詞入題比例（依期刊分層）

| 分層 | 有方法詞 | 領頭 | 掛尾/副標 | 無方法詞 |
|---|---|---|---|---|
| **TUST（n=31）** | 23（74.2%） | 12（38.7%） | 11（35.5%） | 8（25.8%） |
| **其他（n=25）** | 18（72.0%） | — | — | 7（28.0%） |

表面上 TUST 七成有方法詞，但**決定因素是「賽道」不是期刊**：

- **營運隧道病害/案例—機制賽道（我們的賽道）：方法詞 0/11**。TUST 8 篇（Ya-Chu 2017、WangX 2021、TianX 2021、TianY 2026、An 2026、Moradi 2021、Chen 2024、Lionel 2015）＋ EFA 3 篇（Sulei 2022、Wang 2023、Zheng 2024）**全部不放分析方法詞**——數值模擬/模型試驗一律降格為摘要裡的證據來源。TianX 2021 連 highlights 都不提 numerical simulation。
- **方法貢獻賽道**：方法詞領頭且極重（Zhou 2024 一題四個方法詞；Bai 2025 方法詞佔題目一半以上）。
- **中間帶**：機制/現象開頭＋方法掛尾（based on / using / by utilizing…），TUST 11/31——方法當「定錨尾巴」，不搶頭位（Sharifzadeh 2013、Paraskevopoulou 2018、Kovacevic 2021、Jingqi 2023…）。
- **結論**：我們的論文是「病害案例×機制歸因」文，FDM-DEM 是工具不是賣點主體——**題目不放方法詞是本賽道 11/11 的一致慣例**；三個候選題全無方法詞，方向正確。

## 3. 常見構式排行

| 排名 | 構式 | 出現數（/56） | TUST 內 | 代表例 |
|---|---|---|---|---|
| 1 | **情境限定 in/under〔地質/荷載/水文〕** | ≈45（80%+） | 幾乎全數 | in weak rock strata；under bias pressure；**under the groundwater level fluctuation**（Weixin 2023, TUST） |
| 2 | **方法掛尾 based on / using / by / with** | 16（28.6%） | 10/31 | based on displacement back analysis（Sharifzadeh）；using the CCM（Paraskevopoulou） |
| 3 | **雙並聯 A and B**（雙現象/雙過程/雙手段） | ≈13（23.2%） | 7/31 | EDZ formation **and** sealing（Lisjak）；water pressure **and** lining response（An 2026） |
| 4 | **依時詞入題 time-dependent / long-term / evolution** | 14（25.0%） | 7/31 | time-dependent floor heave（Chang 2024）；lining crack **evolution**（Ya-Chu 2017） |
| 5 | **冒號雙層〔主標：副標〕** | 12（21.4%） | 6/31（19%） | 副標類型：case study 標籤(5)、insights/價值(Xin、ZhangS)、貢獻物(Tsai)、方法鏈(Bai 2022)、example(Tarifard) |
| 6 | **因果尾綴 induced by / caused by / influenced by / subjected to** | 9（16.1%） | 6/31（19%） | induced by humidification（Chang）；influenced by slope instability（Ya-Chu）；caused by drainage system deterioration（Sulei） |
| 7 | **A case study 文體標籤** | 6（10.7%） | 3/31 | : A case study of Liwaiao Tunnel, Ningbo, China（Sulei，三級地名格式） |
| 8 | **案例/地層專名入題** | 6（10.7%） | 3/31 | Tawarazaka（WangX）、Xiamaixi（TianX）、Opalinus Clay（Lisjak） |
| 9 | **considering〔增量變數〕**（「別人沒考慮我考慮了」標記） | 4（7.1%） | 1/31 | considering interlayer effect（Zheng）；considering 雙災害（Ma） |
| 10 | **Study on / Investigation of 綴詞起手** | 4（7.1%） | 1/31 | 中式公式化開頭，TUST 樣本僅 Chen 2024 用 |

補充觀察：
- 因果連接詞頻譜：induced by（6）＞ caused by（1）＝ influenced by（1）＝ subjected to（1）；**"driven by" 在 56 篇樣本中零出現**——用它有微差異化效果，但也無前例背書。
- 題長分佈約 6–24 個英文詞；TUST 常態 12–20 詞，24 詞（Ma 2023、Tarifard 2022）仍過關，條件是「長而不虛」（每個詞都是檢索詞）。
- 術語佔位策略：把自創機制詞寫進題目搶定義權（non-Darcy、pipeline-type karst、clumped particle model）——**「intermittent time-dependent deformation」正是我們可佔位的詞**（已由 Tsai in-review IJRMMS 稿建立系列）。

---

## 4. 三個題目候選對照評分

三案共同底盤（皆合規）：現象開頭（TUST 35.5% 主流之一）、案例匿名化（"an operating mountain railway tunnel"，合 30/31 慣例）、無方法詞（合病害機制賽道 11/11 慣例）、水文驅動情境詞（有 Weixin 2023 同刊前例）。差異在**機制賣點是否入題、因果構詞、可讀性**。

### N-A `Lining crack evolution of an operating mountain railway tunnel influenced by cyclic groundwater fluctuation`
- 構式：`[現象+evolution] of [匿名對象] influenced by [水文驅動]`——**Ya-Chu 2017（TUST, 被引 94+）同構迭代**：把 slope instability 換成 cyclic groundwater fluctuation，屬 TianY 筆記發現的「題名系譜迭代」戰法，審稿人一眼認出系列傳承。
- 強項：文法最乾淨、13 詞最短、evolution 自帶時間軸、系譜連結最強。
- 致命弱點：**核心賣點（間歇性依時變形機制）完全不入題**——讀起來是「又一篇病害追蹤案例」，與 2017 篇同構到增量感不足；influenced by 是樣本中最弱的因果詞（僅 1 例），對「機制歸因」型論文火力不夠。

### N-B `Lining cracking … driven by groundwater-fluctuation-induced intermittent time-dependent deformation`
- 構式：`[現象] driven by [X-induced Y 機制鏈]`——因果全鏈壓進一個介詞短語。
- 強項：機制詞入題、佔位 intermittent TDD。
- 弱點：**雙重因果標記疊加（driven by ＋ -induced）＋三連字號複合形容詞**，是 56 篇樣本中不存在的笨重構詞；連字號複合詞降低檢索命中（"groundwater fluctuation" 被焊死在複合詞裡）；母語審稿人觀感風險最高。

### N-C `… under cyclic groundwater fluctuation: intermittent time-dependent deformation as the driving mechanism`
- 構式：`[現象 of 對象] under [驅動情境]：[機制] as the driving mechanism`——冒號雙層（TUST 19% 合法且 2024–26 漸多），主標賣現象+情境（檢索熱詞全進），**副標=論文論點本身**（機制主張副標），與 Xin 2024「冒號後賣價值」、Tsai in-review「副標自帶貢獻聲明」同路但無撞型者。
- 強項：機制佔位＋因果乾淨（under 情境詞有 Weixin 2023 同刊前例；driving mechanism 呼應樣本高頻詞 mechanism）＋一題兩賣（案例讀者看主標、機制讀者看副標）。
- 風險：定冠詞 "the driving mechanism" 是強單因歸因主張，正文歸因閉環必須撐得住（TianX 筆記顯示 TUST 吃「單因歸因」這套，但要有證據鏈）。

### 評分表（每軸 0–5）

| 軸 | 權重依據 | N-A | N-B | N-C |
|---|---|---|---|---|
| TUST 構式合規（對 31 篇慣例） | §1–3 統計 | 5 | 3 | 5 |
| 機制/依時賣點入題（熱區對齊） | 依時詞 25%、2024–26 熱脈 | 1 | 5 | 5 |
| 檢索與關鍵詞密度 | 高頻詞、複合詞懲罰 | 4 | 3 | 4 |
| 文法與可讀性 | 樣本無 N-B 型前例 | 5 | 2 | 4 |
| 系譜連結與差異化 | Ya-Chu 2017→WangTT 2024 系列 | 4 | 4 | 4 |
| **總分（/25）** | | **19** | **17** | **22** |

---

## 5. 最終建議（供 Wade 定奪）

**首選：N-C 為基底，主標沿用 N-A 的 "crack evolution"**（繼承 2017 系譜與時間軸詞），即：

> **Lining crack evolution of an operating mountain railway tunnel under cyclic groundwater fluctuation: intermittent time-dependent deformation as the driving mechanism**

理由收束：
1. 病害機制賽道 11/11 無方法詞、30/31 案例匿名化——三案皆合規，但只有 N-C 把「間歇性依時變形」這個唯一差異化資產寫進題目；N-A 棄守賣點、N-B 構詞笨重。
2. 主標 "Lining crack evolution … an operating … tunnel" 對 Ya-Chu 2017 同構迭代（續作訊號）；副標對 Tsai in-review 的 intermittent 賣點跨刊佔位——一題同時鎖兩條團隊系譜。
3. "under + 水文驅動" 有同刊直接前例（Weixin 2023）；20 詞在 TUST 常態帶內；主標副標各自可獨立檢索。
4. 風險管理：若審稿階段對 "the driving mechanism" 單因強主張有疑慮，降級備案為副標改 "the role of intermittent time-dependent deformation"（弱化為角色探討）；不建議先自弱。

次選：N-A（安全牌，若正文機制證據鏈最終不足以撐單因歸因時退守）。不建議：N-B。

---

## 附錄｜56 篇逐篇分類（依筆記 (a) 節）

| 筆記 | 期刊 | 開頭元素 | 方法詞（位置） | 構式標記 |
|---|---|---|---|---|
| Chang_2024 | TUST | 方法（試驗平台） | 有（領頭，物理試驗詞） | A and B＋induced by |
| Mao_2026 | TUST | 現象（+analysis） | 有（based on 雙掛尾） | 雙支柱 based on |
| WangZ_2026 | TUST | 方法（耦合模擬） | 有（首尾各一） | of A and B＋using |
| Yan_2023 | TUST | 方法（分析型） | 有（multiscale＋based on） | induced by＋based on |
| LiuD_2022 | TUST | 現象 | 有（using 掛尾） | under 條件＋方法尾 |
| WangX_2021 | TUST | 現象 | 無 | 冒號 case study＋專名 |
| Xin_2024 | TUST | 機制 | 有（副標，證據級） | 冒號價值副標 |
| TianX_2021 | TUST | 應用端（對策） | 無（monitoring=工程行動詞） | induced by＋case study 副標＋專名 |
| ZhangS_2025 | TUST | 現象 | 有（副標，類別級） | 冒號 Insights from A and B |
| Ou_2025 | TUST | 應用端（願景 Towards） | 有（副標，資料源級） | 冒號交付物副標 |
| Moradi_2021 | TUST | 案例（地名 Ilam） | 無 | 冒號 case study |
| Chen_2024 | TUST | 機制（參數影響） | 無 | Study on the influence of X on Y |
| An_2026 | TUST | 現象（場量分佈） | 無 | A and B＋induced by |
| TianY_2026 | TUST | 機制 | 無 | 雙頭並聯＋subjected to |
| WangTT_2024 | TUST | 應用端（交付物 Index） | 有（量測詞，零模擬詞） | for assessing＋based on |
| Sharifzadeh_2013 | TUST | 現象 | 有（based on 掛尾） | 現象 of 對象 in 地質 based on 方法 |
| Paraskevopoulou_2018 | TUST | 現象 | 有（using 掛尾） | X of Y using Z |
| Fahimifar_2009 | TUST | 方法（解型） | 有（領頭） | considering 尾綴 |
| Kovacevic_2021 | TUST | 現象（任務綴詞） | 有（by utilizing 掛尾） | 五段介詞鏈 |
| Jun_2023 | TUST | 方法（Analytical） | 有（領頭） | on→of→for→in 介詞鏈 |
| Liu_2019 | TUST | 方法（Simulation of） | 有（首尾雙重） | during＋in＋based on |
| Yuqi_2018 | TUST | 應用端（Predicting） | 有（by measuring 掛尾） | 雙動名詞因果鏈 |
| Jingqi_2023 | TUST | 現象（+analysis） | 有（based on 掛尾，創新詞內嵌） | 對象雙限定詞 |
| Weixin_2023 | TUST | 方法（Experimental assessment） | 有（領頭） | **under the groundwater level fluctuation** |
| Zhou_2024 | TUST | 方法（FDM-DEM method） | 有（領頭，極重） | based on REV for 任務 |
| Rasmussen_2024 | TUST | 方法（Hybrid lattice/DEM） | 有（領頭） | 方法→現象→場域漏斗 |
| Lionel_2015 | TUST | 現象（互制） | 無 | 破折號副標＋time-dependent |
| Kunjie_2025 | TUST | 方法（Experimental investigation） | 有（領頭，體裁宣告） | 三重限定詞＋induced by |
| Wang_2020 | TUST | 方法（DEM-continuum） | 有（領頭，主詞） | 方法→現象→材料 |
| Yin_2022 | TUST | 方法（Modified Burgers model） | 有（領頭） | A and its B 雙節式 |
| Ya-Chu_2017 | TUST | 現象（crack evolution） | 無 | **influenced by＋匿名單數對象**（N-A 母版） |
| Tsang_2023 | RMRE | 方法（Automating） | 有（密集） | for 具名 Case Study |
| Lisjak_2015 | RMRE | 方法（Hybrid FDEM） | 有（領頭全拼） | 雙過程並聯＋地層專名 |
| Potyondy_2004 | IJRMMS | 方法（BPM） | 有（6 詞極簡） | A+[模型名]+for+[材料] |
| Cho_2007 | IJRMMS | 方法（clumped particle model） | 有 | 同上命名策略 |
| Yoon_2007 | IJRMMS | 方法（Application of） | 有（100% 方法詞） | of→to→in 介詞鏈 |
| Sulem_1987 | IJRMMS | 方法（Analytical Solution） | 有（領頭） | 解型→量→幾何 |
| Yan_2020 | IJRMMS | 方法（Modified Nishihara） | 有（模型+驗證雙詞） | under 情境收尾 |
| Peng_2017 | IJRMMS | 機制（Effects of X on Y） | 有（using 掛尾） | 無因次參數研究型 |
| Cai_2004 | IJRMMS | 機制（概念門檻） | 無 | Generalized＋of＋near 漏斗 |
| Tsai_inreview | IJRMMS(投) | 方法（雙動名詞） | 有（密集） | 冒號貢獻物副標＋intermittent 佔位 |
| Bai_2022 | C&G | 現象（視角化） | 有（副標極重，軟體名） | 冒號方法鏈副標 |
| Ma_2023 | C&G | 應用端（評估任務） | 無 | considering 雙災害 |
| Liu_2022 | IJMST | 現象（屬性） | 無 | 純名詞三層介詞鏈 |
| Wu_2024 | IJNAMG | 機制（Study on 綴詞） | 無 | between A and B |
| Wang_2023 | EFA | 現象（Investigation on 綴詞） | 無 | induced by＋case study 標籤 |
| Sulei_2022 | EFA | 機制（cracking mechanism） | 無 | caused by＋三級地名副標 |
| Zheng_2024 | EFA | 現象/機制（Damage evolution） | 無 | under＋considering＋in 四段 |
| Vazaios_2019 | JRMGE | 機制（Assessing） | 有（using approach 掛尾） | 六段套疊限定 |
| Tarifard_2022 | GGGG | 機制（評估+creep and water） | 有（using 佔 1/3） | 冒號 example from 副標 |
| Li_2021 | Nat. Hazards | 方法（Developing 模型） | 有（密集＋品牌詞） | based on 試驗資料源 |
| Barla_2012 | IJG-ASCE | 現象×方法複合 | 有（僅泛稱 Modeling） | 10 詞極簡 |
| Nitka_2015 | Granular Matter | 方法（Modelling） | 有（首尾包夾） | of X in Y with DEM |
| Bai_2025 | Comp. Part. Mech. | 方法（FDM–DEM 耦合） | 有（極重，佔半題） | considering＋for 收尾 |
| Potyondy_2015 | Geosystem Eng. | 方法（BPM as a tool） | 有（主詞） | 冒號綜述範疇副標 |
| Liu_2023 | TAFM | 機制（Investigation of 綴詞） | 有（using DEM 掛尾） | 機制+對象+缺陷限定+方法 |

*統計口徑備註：Barla 2012 開頭為「現象屬性×泛方法」複合，計入現象；Kovacevic 2021「任務+現象」計入現象；Ma 2023「評估任務」計入應用端。歸類異動不影響 §1 的量級結論。*
