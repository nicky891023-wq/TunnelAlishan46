# Tsai, Li & Wang (2026, in review, IJRMMS) — 寫作工藝精讀筆記

**題目**：Numerical Simulation and Mechanical Interpretation of Intermittent Time-Dependent Deformation in Tunnels: A Modified Mechanical Model Developed from a Case Study
**來源**：本機 docx（C:/Users/Wade/Desktop/Wade_TD_SCI/PaperWork/Claude/IJRMMS_01_Manuscript.docx）
**access**：full-local（全文本機手稿；圖表僅有 caption，正圖與參考文獻清單不在本檔）
**主題**：Burgers–Mohr 黏彈塑模型 + 黏性邊界面（viscous boundary surface）＋單一應力門檻參數，模擬曾文越域引水西隧道 4 年監測之「間歇性」潛變變形。

---

## (a) 題目解剖

- **開頭元素**：方法先行——「Numerical Simulation and Mechanical Interpretation」雙動名詞開場，先亮出「模擬＋力學詮釋」兩種手段，才接現象（Intermittent Time-Dependent Deformation）與場域（in Tunnels）。
- **有無方法詞**：有，且密度高——主標含 Numerical Simulation；副標含 Mechanical Model、Case Study。
- **構式**：`[方法A and 方法B] of [關鍵形容詞+現象] in [場域]: A [貢獻物] Developed from a [證據來源]`。
  - 關鍵形容詞 *Intermittent* 是全文賣點（間歇性），放在現象前面當鉤子。
  - 副標把「新東西是什麼（修正模型）」與「怎麼來的（案例發展）」一次講完，等於題目自帶貢獻聲明。
  - 案例（曾文/西隧道）不進題目——案例是驗證載具，不是主角。

## (b) 文章架構（節序與比重）

| 節 | 段數(約) | 角色 |
|---|---|---|
| 1. Introduction | 4 | 問題→文獻→缺口→本研究 |
| 2. Methodology | 5 | 失敗包絡線→黏性邊界面→修正 Burgers–Mohr→二維應力空間詮釋 |
| 3. Case Study（3.1 地質、3.2 施工與變形） | 7 | 案例背景＋監測曲線五型分類＋參數反算 |
| 4. Results | 7 | 五型曲線各一段模擬對照＋一段總結 |
| 5. Discussion（5.1 支撐反力、5.2 門檻參數敏感度、5.3 間歇機制） | 9 | 全文最重——結構層次→參數研究→應力路徑機制統整 |
| 6. Conclusions | 5（4 條編號） | 條列式結論 |

- 比重特徵：**Discussion > Results**，Discussion 佔比最大，把「機制詮釋」當成與模擬同等級的貢獻（呼應題目的 Mechanical Interpretation）。
- Case Study 獨立成節、插在 Methodology 與 Results 之間——監測曲線分類（Type I/IIA/IIB/IIIA/IIIB）在 §3 先建立，§4-§5 全部沿用同一分類當敘事骨架。

## (c) 前言手法（4 段）

1. **段1｜問題與後果**：時間相依變形是山岳隧道常見問題→施工期後果（支撐破壞、淨空不足）→營運期後果（襯砌載重累積、性能劣化）→拉到 resilience 高度→收在「只顧短期穩定的設計不足以掌握長期演化」。由小到大、由工程到韌性的階梯式升級。
2. **段2｜文獻總覽**：以 Table 1 承載案例文獻（正文不逐一敘述，表格代勞）；再用 (i)(ii)(iii) 三分法歸納研究途徑（潛變試驗／案例+數值模擬／解析解），最後點出趨勢：從材料層次延伸到結構層次。
3. **段3｜缺口 staging**：轉折詞 "Despite these advances" 起手，兩層缺口——(1) 既有模型只會「擬合材料行為」，缺乏判斷變形何時啟動/減速/停止/再活化的**顯式力學準則**，故無法重現多階段行為、無一致詮釋框架；(2) 變形受支撐型式與外部擾動間接影響，而其抑制取決於補強措施與時機。段末以 "Therefore, developing a mechanical model that can... is essential" 收束成需求句。
4. **段4｜本研究**："In this context, the present study introduces..." 直述貢獻物；緊接對比句「不同於增加阻尼元件或修改本構關係的作法，本模型在**保留原模型簡潔性**的同時建立間歇性機制」——用「簡單」當賣點防守審稿人；再交代驗證材料（4 年監測＋室內試驗）與價值（補強設計與長期穩定評估參考）。
   - 引語樣本（全文唯一引語）："preserving the simplicity of the original model"。

## (d) 結果敘事

- **圖領句**：每段固定以 "Fig. 6(x) shows the simulation result for the Type X curve." 開場——一型一段、一段一圖版，五段平行結構，讀者可預測節奏。
- **量化方式**：
  - 絕對值：黏塑/黏彈區厚度 0.6–0.7 m、4.7–4.8 m；監測天數 1579 d、1586 d。
  - 正規化：以隧道半徑無因次化（R_vp/R0 ≈ 1.24、1.28），跨案例可比。
  - 倍率變化：黏彈區在淹水事件後達初始值約 1.8 倍——用「倍數」講演化，比堆數字有力。
- **機制詮釋**：每個觀察後立即接 "indicating that / demonstrating that / confirming that" 子句，觀察與詮釋不分家；模擬-監測吻合處明說（consistent with the monitoring data），需調參數處也明說（reducing σ_t and η_M reproduced the curve）——把調參誠實化為「事件改變了材料狀態」的物理敘述。
- **節末總結段**："Figures 6–8 collectively demonstrate..." 把五個平行段落收攏成一句主張（統一框架、可描述多樣性、涵蓋外部擾動與補強效應），為 Discussion 鋪路。

## (e) 貢獻凸顯

- **位置**：五處疊加——摘要末三句、前言段4、Results 總結段、5.1 末段（"reveals that the modified model can describe not only... but also..."）、Conclusions 四條編號。
- **措辭**：反覆使用三個關鍵語塊——**"a single parameter"**（單一參數，強調精簡）、**"a unified mechanical framework"**（統一力學框架，強調一致性）、**"clear physical meaning and practical applicability"**（物理意義+實用性雙保險）。
- 最高階貢獻放在結論(4)：補強有效的機制「不只是提高勁度強度，更在於透過圍岩-支撐互制把應力狀態拉回黏性邊界面內」——把工程啟示上升為機制洞見，這是全文的 take-home message。

## (f) 缺陷包裝

- **無獨立 Limitations 節**。缺陷處理採三招：
  1. **化為未來工作**：5.3 最末段以三個開放問句收尾（參數在不同應力狀態下是否相似？關鍵影響因子？地質調查階段如何評估？）標註 "warranting further research"——限制被翻譯成研究前景。
  2. **化為假設聲明、順帶淡化**：淹水事件的弱化效應「可能也降低了岩體強度，但本研究以降低應力門檻來模擬」（5.1 一句帶過）；簡化以 "For practical applicability and simplicity" 正當化——把簡化說成優點。
  3. **誠實但不放大**：浸水泥質砂岩試體數小時內破壞、重複試驗失敗——只陳述事實一句、不做展開，隨即轉向可用的數據。
- 二次襯砌未納入：以「未來可納入以檢討全生命週期韌性」一句正面表述（5.1 末），缺件變成延伸方向。

## (g) 圖表數與類型

- **12 圖、5 表**。
- 圖：①概念模型圖（破壞包絡線+黏性邊界線+本構元件，Fig.1）②地質縱剖面+比值分布（Fig.2）③監測曲線五型（Fig.3）④參數反算示意（Fig.4）⑤潛變試驗（Fig.5）⑥模擬曲線五型（Fig.6）⑦變形分區圖五型（Fig.7）⑧分區範圍時間演化（Fig.8）⑨支撐反力增量+損傷比演化（Fig.9）⑩⑪參數研究（覆蓋深度、應力門檻）⑫應力路徑概念圖（Fig.12）。
- 表：文獻案例彙整（替前言扛文獻回顧）、施工紀錄、Sulem 式回歸參數、黏彈參數、室內試驗參數。
- 工藝重點：**Fig.3/6/7/8/9 全部沿用同一「五型」分版**（(a)~(e)對應 Type I~IIIB），監測→模擬→分區→演化→支撐載重一路平行對照；首圖(Fig.1)與尾圖(Fig.12)都是概念圖，形成「概念提出→概念收束」的閉環。

## (h) 對本研究（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）啟示

1. **「門檻面＋有效應力左移」正是我們的水位循環敘事**：本文 Fig.12 的 E1→W3 路徑（水壓上升→有效應力左移→跨越黏性邊界面→變形啟動）可直接移植——地下水位循環使襯砌裂縫「間歇性」開展/停止，可用同款「單一門檻參數當開關」的框架給出力學定義，且審稿人已見過此構式（同一團隊、同一期刊）。
2. **先分類、後模擬的敘事骨架**：監測資料先歸納成曲線型別（§3），再讓模型逐型重現（§4），五型分版貫穿 5 張圖——我們的裂縫開展歷時曲線也可先做型別分類（如：穩定型／水位敏感型／劣化累積型），讓 FDM-DEM 模擬逐型對照，整篇敘事自動有骨架。
3. **損傷比 Dm = M/Mcr 當支撐安全指標**：以最大彎矩/開裂彎矩的比值追蹤支撐安全裕度並劃分三類演化（持續增載型／補強受控型／破壞失控型）——對襯砌裂縫問題可平移為「襯砌損傷比」指標，把裂縫觀測與結構安全評估掛鉤，是 TUST 讀者喜歡的工程落地。
4. **「保留簡潔性」的防守性寫法**：貢獻句刻意與「加元件、改本構」的複雜化路線對比，主打 single parameter + unified framework——跨尺度 FDM-DEM 容易被質疑過度複雜，宜學此招：強調耦合介面的參數精簡與物理意義，並把限制一律包裝成 future work 問句收尾。

---
*筆記完成：2026-07-21，依本機手稿全文精讀。*
