# Paraskevopoulou & Diederichs (2018) — 寫作工藝精讀筆記

**書目**：Paraskevopoulou, C., Diederichs, M. (2018). Analysis of time-dependent deformation in tunnels using the Convergence-Confinement Method. *Tunnelling and Underground Space Technology*, 71, 62–80. DOI: 10.1016/j.tust.2017.07.001
**取得方式**：full-local（本機 PDF＝White Rose 典藏 Accepted Manuscript，CC-BY-NC-ND；路徑 `C:\Users\Wade\Desktop\Wade_TD_SCI\Reference\trash\time_dependent\files\Paraskevopoulou和Diederichs - 2018 - ....pdf`）
**主題一句話**：用 FLAC 軸對稱參數研究，把「開挖推進」與「潛變時間效應」同時放進 CCM/LDP 框架，量化忽略時間效應會低估多少收斂量。

---

## (a) 題目解剖

> Analysis of Time-dependent Deformation in Tunnels using the Convergence-Confinement Method

- **開頭元素**：現象（time-dependent deformation），前面掛一個中性分析名詞「Analysis of」——不是案例、不是方法起頭。
- **有無方法詞**：**有**，且是句尾壓軸——「Convergence-Confinement Method」全名入題（TUST 接受方法詞入題，甚至當賣點）。
- **構式**：`[分析名詞] of [現象] in [工程對象] using [方法]`——經典三段式「X of Y using Z」。現象給讀者釘子（掃過標題就知道講潛變變形），方法給審稿人定位（CCM 社群）。
- 沒有冒號、沒有副標、沒有問句；17 個字內解決。無新奇詞（novel/new 不入題），新意留給摘要句「a new yet simplified approach」。

## (b) 文章架構與比重

| 節 | 內容 | 佔主文比重（約） |
|---|---|---|
| 1 Introduction（含 1.1 GRC/LDP 教學小節） | 框架＋缺口 | ~20% |
| 2 Time-dependent Behaviour（2.1 流變模型、2.2 隧道依時變形、2.3 兩效應合併進 LDP） | 延伸背景＝半篇 review | ~28% |
| 3 Numerical Analysis | 模型設定（FLAC 軸對稱、D&B vs TBM、62 組模型） | ~10% |
| 4 Numerical Results（4.1 對解析解驗證、4.2 Kelvin-Voigt 一次潛變、4.3 Burgers 一二次潛變） | 結果 | ~20% |
| 5 Discussion | 應力路徑、臨界偏差應力 q_cr、Saint Martin La Porte 現場案例對照 | ~12% |
| 6 Conclusions | 量化收尾＋future work | ~10% |

特點：**背景（§1+§2）合計近半篇**——TUST 容忍甚至歡迎教學型長背景，用 3 張文獻整理表（Table 1–3）撐起來。方法極短，結果靠圖說話。

## (c) 前言手法

- **段落結構**：§1 本體只有 1 段超長段＋§1.1 約 5 段，合計約 6 段。
- **§1 首段角色**（一段完成三件事）：
  1. 權威開場——首句即引 Panet (1993) 定調「理解變形要靠支撐互制＋現場資料」；
  2. 廣度轟炸——一句話串 15+ 篇引文（1938–2015）證明掃過全場，然後收斂到「這些多半基於 CCM」；
  3. 缺口＋後果——CCM 簡化式「未顯式捕捉時間依存分量」→ 後果放大（unexpected failures、safety issues、cost overruns、delivery delays）→ 收尾一句「本文處理此適用性問題」。
- **缺口 staging＝「常用工具忽略因素 Y → 工程後果」句型，且全文重複三次**：摘要一次、§1 段尾一次、§1.1 段尾再補刀一次（「表 1 所有 LDP 公式皆未考慮依時變形→套用必低估位移與支撐需求」）。每個背景區塊都以缺口句收尾，是刻意的迴聲設計。
- **貢獻句式**：低調、過程導向、實務者取向——不列編號貢獻清單、不喊 novelty；摘要用「proposing a new yet simplified approach」（全文唯一值得引的自我定位語，<15 字），強調 practitioners 可直接用。
- §1.1 是 GRC/LDP 的 mini-tutorial：先教會讀者工具，再指出工具缺陷——「先給糖再抽走」的缺口鋪陳。

## (d) 結果敘事

- **驗證先行**：§4.1 先拿數值對彈性解與 Kelvin-Voigt 解析解（Panet 1979）對標，一句話轉場——「這些結果驗證了模型。真正的問題是兩個極端之間黏滯行為如何影響 LDP」——從 credibility 直接切入 research question，是漂亮的樞紐句。
- **界限案例修辭**：彈性解＝瞬時開挖（cycle time→0）、零黏度 KV＝無限循環時間，所有參數結果都框在兩極端之間讀——給讀者天然座標系。
- **圖領句**：每小節先報圖號（「結果示於 Figures 7 and 8」），下一段「Figures 7 and 8 show similar trends…」，觀察→機制解釋的節奏固定：每個觀察後跟「This was expected as…」「This is also reasonable as…」。
- **量化方式**：以相對化為主——位移全部正規化到 KV 參考模型最大位移 u_r∞max（雙軸呈現，左正規化、右絕對值）；絕對數字很省，關鍵錨點只有三個：一次潛變可多貢獻 50%（放在結論）、時間效應可佔總變形 70%（引 Sulem 1987）、現場 166 天 60 cm（Saint Martin La Porte）。
- **機制詮釋升級**：Discussion 換「應力路徑」鏡頭——潛變由偏差應力 q 驅動、存在臨界值 q_cr、且在一個開挖步之後即達到（D&B 3 m、TBM 1 m）——把參數觀察抬升成可移植的機制敘述。
- **現場案例收尾**：Discussion 末端放唯一一個真實隧道（Barla 2016 的 Saint Martin La Porte 監測曲線），把數值故事釘到工程現實。

## (e) 貢獻凸顯

- **位置**：三處——摘要尾句（簡化方法、實務者可用）、§1 尾（本文處理缺口）、結論（量化收割）。
- **措辭**：結論才給最強數字——「僅一次潛變即可造成 50% 位移增量」「二次潛變下無理論上限（除全斷面閉合）」「開挖工法控制總位移，可輔助 D&B vs TBM 選擇」。貢獻全部包裝成**工程含意/決策價值**，不是方法論創新宣言。
- 結論還做了一次全文流程重述（overview→指出限制→參數研究→發現），方便只讀結論的審稿人。

## (f) 缺陷包裝

**沒有獨立 Limitations 節**。淡化手法四招：
1. **前置 scope 宣告**：§2.1 就講明「本文聚焦黏彈性、不考慮塑性降伏」——限制被翻譯成「刻意簡化」，放在背景不放結尾。
2. **假設嵌入方法**：CVISC 的凝聚力/抗拉設超高以禁止降伏、無支撐、等向應力——在 §3 平鋪直敘，不辯解。
3. **預防性拆彈**：數值上偏差應力達不到理論值，主動解釋為網格平均效應、「元素夠小即趨近」——先替審稿人把問題回答掉。
4. **現實對沖＋future work 轉向**：TBM 結果「未必代表真實工況」用工程常識緩衝；結論把「缺完整現場資料回饋分析」寫成對科學與實務都有貢獻的未來邀請，掩護本文無現場驗證的事實。

## (g) 圖表數與類型

- **16 圖、5 表**。
- 圖：概念示意 4（GRC-LDP 關係、潛變三階段曲線、兩種介質的 LDP 示意）＋模型設定 1（含鑽堡/TBM 廠商圖）＋驗證圖 1＋參數結果 LDP 圖 5＋應力路徑 2＋q-位移關係 2＋現場資料對照 1。
- 表：文獻整理表 3（LDP 解析解、流變模型/力學類比、黏彈解析解——整理表兼當「缺口證據」用）＋參數表 1＋模型矩陣/命名表 1。
- **固定版式慣例**：8 張結果圖全用「(Left) 全景 / (Right) 面附近放大」雙欄配置——同一縮放慣例重複使用，降低讀圖成本。

## (h) 對我們（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）的啟示

1. **題目直接套模板**：`[現象] in [營運鐵路隧道] using [跨尺度 FDM-DEM]`——TUST 明確接受方法詞壓軸入題；現象詞放最前（如 lining crack evolution under cyclic groundwater level），不需冒號副標。
2. **缺口用「常用工具忽略因素→安全/成本後果」句型，並在摘要、前言尾、背景尾迴聲三次**：我們的版本＝現行襯砌評估/收斂量測忽略地下水位循環驅動的裂縫擴展→維管成本與行車安全後果。每個背景區塊以缺口句收尾。
3. **背景做成文獻整理表＋教學小節**：仿 Table 1–3，做「裂縫/滲流/依時模型」synthesis 表，最後一欄留「皆未考慮水位循環×跨尺度」當缺口證據；TUST 審稿文化吃這套長背景。
4. **結果敘事三件套可整組移植**：(i) 驗證先行＋「真正的問題是…」樞紐句；(ii) 界限案例（恆高水位/恆低水位兩極端夾住季節循環情境）＋正規化到參考模型；(iii) Discussion 末端放單一真實監測斷面（我們的營運隧道裂縫監測段）把數值釘到現實——同時用「前置 scope 宣告」（如：聚焦水力-力學循環、不含熱/化學劣化）在方法區先拆限制的彈。
