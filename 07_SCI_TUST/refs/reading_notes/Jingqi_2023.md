# Jia Jingqi et al. (2023) — 精讀筆記【access = abstract-only（實為 metadata-only）】

- **書目**：Jia Jingqi; Chen Yun; Luo Hao; Ma Guowei (2023). *Seepage stability analysis of a deep-buried tunnel in fractured rocks based on a non-Darcy hydro-mechanical coupled method*. **Tunnelling and Underground Space Technology**, 142, 105393. DOI: 10.1016/j.tust.2023.105393（2023-12 出版）
- **取得情形**：本機 PDF 無（Wade_TD_SCI/Reference 全樹比對無此篇；`Ma 2023.pdf` 為 Ma Gaoyu C&G 論文，非本篇）。OpenAlex `oa_status=closed`、無 `best_oa_location.pdf_url`；Crossref／OpenAlex／Semantic Scholar 三個 API 皆**未存摘要文字**。依省額度規則不爬 landing page、不試其他來源。以下 (b)–(g) 凡標【未驗證】者為無全文之誠實留白，禁止當成事實引用。
- **可驗證外部訊號**：cited_by = 33（OpenAlex，2026-07 查）；參考文獻 82 篇；OpenAlex 概念標籤：Geotechnical engineering / Permeability / Rock mass classification / Groundwater / Darcy's law。本專案 `_gap_collection_raw.json` 已收錄（axis=L4，is_tust=true）。

## (a) 題目解剖（可全額分析——題目本身即證據）
> Seepage stability analysis of a deep-buried tunnel in fractured rocks based on a non-Darcy hydro-mechanical coupled method

- **開頭元素**：以「現象＋分析行為」起手（*Seepage stability analysis*）——不是案例名、不是方法名。問題導向先行。
- **案例呈現**：不具名通用對象「a deep-buried tunnel in fractured rocks」，用兩個限定詞（埋深 deep-buried＋地質 fractured rocks）畫定適用範圍，取代具體工程名。
- **方法詞**：有，且置於句尾從句 —— *based on a non-Darcy hydro-mechanical coupled method*。**創新形容詞（non-Darcy）內嵌在方法從句裡**，一詞同時標出「打破什麼預設（Darcy 假設）」與「賣什麼（HM 耦合）」。
- **構式模板**：`[現象/問題] analysis of [對象＋限定詞] based on a [創新詞] [耦合類型] method`；約 19 個英文詞，三段式：問題→對象→方法。
- **點評**：TUST 接受題目不出現具體案例名；「based on a … method」是 TUST 常見的方法掛尾式，創新賣點靠方法從句內的一個非常規假設詞（non-Darcy）承載。

## (b) 文章架構【未驗證——無全文】
- 節序與比重無法確認。僅可由 82 篇引文與 TUST 慣例**推測**（標註為推測）：Introduction → 非達西滲流/HM 耦合理論 → 數值方法與驗證 → 深埋隧道案例分析 → 參數討論 → Conclusions。此推測不得引用為該文事實。

## (c) 前言手法【未驗證——無全文】
- 段數、各段角色、缺口 staging、貢獻句式皆需全文方能萃取。唯一可靠線索：題目與概念標籤顯示其缺口敘事軸線大概率為「傳統滲流分析採 Darcy 線性假設，裂隙岩體高速流下失效 → 需 non-Darcy HM 耦合」——此為由題目反推的**框架推測**，非逐段驗證。

## (d) 結果敘事【未驗證——無全文】
- 圖領句、量化方式、機制詮釋無法萃取。

## (e) 貢獻凸顯【未驗證——無全文】
- 位置與措辭無法萃取。可驗證的間接訊號：兩年 33 次被引，顯示其「non-Darcy＋HM 耦合」賣點在 TUST 讀者群確實被當成方法貢獻引用（本專案即以 L4 軸引用其「裂隙流耦合公式選型」）。

## (f) 缺陷包裝【未驗證——無全文】
- limitations 位置與淡化策略無法萃取。

## (g) 圖表數與類型【未驗證——無全文】
- 無法計數。

## (h) 對我們的啟示（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）
1. **題目模板可直接移植**：`[問題] of [對象＋限定詞] based on a [創新詞] [耦合] method`。我們的對應寫法示例：*Cracking behaviour of the lining of an operating mountain railway tunnel under cyclic groundwater fluctuation based on a cross-scale FDM-DEM hydro-mechanical coupled method*——「cross-scale」佔據該文「non-Darcy」的創新形容詞槽位，一詞承載「打破單尺度連續體假設」的賣點。
2. **缺口敘事同構**：該文以「打破 Darcy 線性假設」立缺口；我們可同構地以「打破穩態地下水位假設」立缺口（水位循環升降 vs. 恆定水頭），把「循環」做成我們的 non-Darcy 級關鍵詞。
3. **案例可匿名**：TUST 題目不必出現隧道名；用「operating mountain railway tunnel」之類限定詞畫範圍即可，正文再揭示案例——降低題目長度與資訊密度負擔。
4. **引用定位**：本篇在我們稿中的角色已定（L4 方法段：裂隙流 HM 耦合選型背書）。其 non-Darcy 角度與我們的水位循環角度**互補不競爭**，屬低風險必引；被引 33 次亦證明 fractured-rock HM 滲流是 TUST 熱區，我們的選題落在活水域。

---
*筆記狀態：metadata-only。若日後經機構訂閱取得全文，應回填 (b)–(g) 並將 access 升級為 full-subscription。*
