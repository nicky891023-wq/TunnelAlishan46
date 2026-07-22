# Sulem, Panet & Guenot (1987) — 寫作工藝精讀筆記

**書目**：Sulem, J., Panet, M., Guenot, A. (1987). An analytical solution for time-dependent displacements in a circular tunnel. *Int. J. Rock Mech. Min. Sci. & Geomech. Abstr.*, 24(3), 155–164. DOI: 10.1016/0148-9062(87)90523-7
**取得方式**：full-local（本機 PDF：`C:\Users\Wade\Desktop\Wade_TD_SCI\Reference\2020_2025\analyze\1987 依時解析解_ An analytical solution for time-dependent displacements in a circular tunnel.pdf`）
**性質**：純解析解＋方法論推廣＋單一實例驗證的「解法論文」經典範本（收稿 1986-01-28、修訂 1986-08-20）。

---

## (a) 題目解剖

> An Analytical Solution for Time-dependent Displacements in a Circular Tunnel

- **開頭元素＝方法產物**（An Analytical Solution），不是案例、不是現象。
- **有方法詞**：Analytical Solution（解法類型詞直接置頂）。
- **構式**：`An/A + [解法類型] + for + [物理量/行為]（time-dependent displacements）+ in + [幾何對象]（a circular tunnel）`。
- 三段式極簡：解法→對象量→幾何邊界；無地名、無「novel/new」等自誇詞、無機制詞（沒把 face advance 與 creep 分離這個核心賣點放進題目）。1980 年代解析解論文的標準題式：題目只承諾交付物，賣點留給摘要與內文。

## (b) 文章架構（節序與比重，全文 10 頁）

| 序 | 節名 | 頁數比重 | 角色 |
|---|---|---|---|
| 0 | Abstract＋Nomenclature | ~0.7 頁 | 摘要即路線圖（連「最後一章應用於實際隧道」都預告）；符號表前置整頁 |
| 1 | Introduction | ~0.4 頁 | 極短，3 段 |
| 2 | Determination of Displacements and Lining Pressure | ~5 頁（~50%） | 主推導：Assumptions → 無襯砌（彈性/破壞區）→ 襯砌安裝（分案）→ Summary of the results（公式總表） |
| 3 | The Convergence–Confinement Method for … Time-dependent Behaviour | ~1.5 頁（~15%) | 概念推廣：convergence surface 三維化 CCM |
| 4 | Illustrative Example | ~2 頁（~20%) | Quatre Chemins 試驗隧道；含 time-independent vs time-dependent 對照小節＋內嵌 mini-Conclusions |
| 5 | Conclusion | 2 段 | 極短收束 |
| 6 | References | 15 篇 | 半數為法系文獻（自引 4 篇構成方法系譜） |

- 特色一：推導節末尾放 **Summary of the results**——把散落各分案的公式重新整編成「使用手冊」，讀者可跳過推導直接取用。工程期刊解析解論文的貼心設計。
- 特色二：Illustrative Example 內部自帶 Conclusions 小節，先在案例層收束一次，再進全文 Conclusion——雙層收束。

## (c) 前言手法（3 段，第三段跨頁）

- **第 1 段（現象＋張力）**：從公認事實開場（襯砌壓力隨時間增加），立即拆出兩個混淆成因——岩體依時性質 vs 開挖面推進效應——並下斷語：兩效應「必須清楚分離」。**缺口 staging 不是「沒人做過」，而是「兩機制被混淆、需可分離的理論」**——機制分離型缺口。
- **第 2 段（文獻＝兩個具體先行者）**：只點名 Panet [1]（黏彈性收斂解）與 Sakurai [2]（支撐壓力閉合解）各一句。不做綜述式鋪陳，文獻回顧壓到最薄，只立「前人各解半題」的台階。
- **第 3 段（貢獻宣告）**：「In this paper, we present a closed form solution…」直接第一人稱宣告，並列三層貢獻：(i) 擴展到依時應力應變＋破壞行為；(ii) 與現地量測收斂律 [3]（同期姊妹作）一致；(iii) 使時間效應可納入 convergence–confinement method——順勢用兩句話向讀者補課 CCM 是什麼 [4–6]。
- 無 roadmap 段（摘要已代勞）。前言總長不到半頁——把版面全數讓給推導。

## (d) 結果敘事

- **推導型論文的「結果」＝關鍵方程式的物理判讀**。最高明的一手：式 (13)、(21) 直接在公式下方加底括號註記，把兩因子分別標為「僅依開挖面推進效應」與「僅依潛變效應」——用排版讓可分離性一眼可見。
- 隨後用一句明示主結論：「The major conclusion of this analysis is that…」位移可寫成兩函數之**乘積**——把數學結果升格為機制陳述，並立即勾回現地收斂律 [3,11,12] 佐證（理論↔量測互證）。
- **案例敘事採「對照劇」結構**：先做 time-independent 分析→量化結論（u∞=0.78 cm、Ps∞=0.46 MPa < pl，判定穩定）→再做 time-dependent 分析→判定襯砌將破壞→以現地事實裁決（實際每一斷面襯砌都在復挖時破壞；預測破壞收斂 7.5 mm vs 實測 6–9 mm）。傳統法「誤判安全」、新法「命中破壞」，一組數字定勝負。
- 圖領句形式如「The progressive closure has been first calculated … from equations (13) and (14) (Fig. 12)」——先說計算來源與內容，圖號括弧收尾；機制詮釋落在斜體強調：破壞不僅來自復挖，*也來自*依時性質與停工期間累積的收斂。

## (e) 貢獻凸顯

- **位置**：摘要（is developed / is proposed 被動句式）→ 前言第 3 段（we present…主動宣告）→ **推導中段的 major conclusion 句**（最重的一筆放在論文正中央，不留到結論）→ 案例 mini-Conclusions（It is interesting to point out that…以反差句凸顯）→ 全文 Conclusion 首句重申「explicit solution … offers the advantage of simple calculation」。
- **措辭風格**：不用 novel/first；賣點靠「simple calculation」「closed form」「can be predicted」等實用詞，以及 time-independent 分析誤判的對照來自證價值。

## (f) 缺陷包裝

- **前置 Assumptions 小節**：三條編號假設（圓形斷面/深埋/均質等向；平面應變＋虛擬支撐壓力模擬面效應；可分離潛變律）把限制轉譯為「適用範圍」，並各附引文背書——可分離假設引 [9] 的文獻回顧稱對多數岩石可接受；線性 g(σ) 則以「for the sake of simplicity」帶過，同時誠實註明非線性律會使應力場依賴潛變參數（標出簡化的代價後即前行）。
- **推廣節的誠實＋補救**：坦承若破壞區發展，最終平衡依賴應力路徑、無法免除逐步計算——隨即給出工程解方：以「無破壞區」假設求壓力下界，下界即不穩才需完整計算。缺陷立刻變成實用判別流程。
- **結論的讓步子句**：「although valid for simple tunnel geometry and field stress conditions」一行帶過，緊接「can give a reasonable estimate」收正。**全文無獨立 Limitations 節**。
- Future work 以工程應用面貌出現（延後支撐時機、改變勁度以避免破壞；預測何時須補強）——說成能力延伸而非研究不足。

## (g) 圖表數與類型

- **圖 13 幅、表 0 張**，全為線繪圖，無照片：
  - 概念示意 9 幅（Fig.1 虛擬支撐壓力/座標、Fig.2 潛變試驗、Fig.3 破壞區、Fig.4 函數示意、Fig.5 收斂曲面 3D、Fig.6–7 收斂面投影、Fig.8–9 CCM 線圖）；
  - 參數率定曲線 1 幅（Fig.10：λ(x) 與 f(t)——模型輸入完全透明化）；
  - 分析結果 2 幅（Fig.11 vs Fig.12 傳統/依時 CCM 對照，同軸同格式方便互比）；
  - 時程驗證 1 幅（Fig.13 Quatre Chemins 收斂與支撐壓力時程，標註停工/復挖/破壞事件）。
- 概念圖佔 7 成：對「提出新方法框架」的論文，示意圖就是論證主體；材料參數以行文列出（E, ν, σc, φ…），不設表。

## (h) 對本研究（營運山岳鐵路隧道襯砌裂縫 × 地下水位循環 × 跨尺度 FDM-DEM）啟示

1. **把全文押在一句可分離性陳述上**：Sulem 的骨幹是「位移＝面效應函數 × 時間效應函數」這一句，並用公式底註＋major conclusion 句雙重打光。我們可鍛造對應命題——例如「襯砌裂縫響應＝結構傳遞函數 ×地下水位循環荷載歷程」或 FDM-DEM 尺度可分離性——在推導/模擬結果中段就明示，不留到結論。
2. **「傳統法誤判、新法命中、現地裁決」的對照劇**：以定水位（或不考慮循環）分析 vs 水位循環分析平行呈現（如其 Fig.11/12 同格式對圖），並以營運隧道實測裂縫行為當裁判——這是說服工程期刊審者「非考慮循環不可」最省力的敘事。
3. **Assumptions 前置＋結論讓步子句、免設 Limitations 節**：跨尺度耦合必然帶簡化（2D 等效、DEM 接觸律、水位歷程理想化），照此法在方法節開頭列編號假設並逐條引文背書，計算代價誠實標註後即前行；TUST 雖現代審稿多要 limitations，仍可學其「缺陷→適用範圍→補救流程（如下界判別）」的轉譯術。
4. **公式總表（Summary of the results）與率定曲線圖**：若我們給出解析或半解析裂縫-水位關係，節末附使用手冊式公式總表；FDM-DEM 率定參數比照其 Fig.10 以曲線圖全裸公開——這兩件小事對「可被工程師取用」的口碑貢獻極大，也是 TUST 讀者群的偏好。

---
*小註：原文頁 159 方程編號有排版誤植（(28) 出現兩次，前者應為 (26)）——引用其式時以 (24)(26)(27)(28) 的邏輯序核對。*
