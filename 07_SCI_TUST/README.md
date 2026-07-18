# 07_SCI_TUST — 期刊論文作業區（目標：Tunnelling and Underground Space Technology）

> 2026-07-17 開設（Wade 指令）。後續論文架構討論與逐步撰寫都在本資料夾進行。

## 現況

- **企劃書 v0**：`PAPER_PLAN_20260716.md`（原以 IJRMMS 為標竿撰寫；投稿目標現定為
  **TUST（Elsevier）**——標竿解剖的 6 節架構/圖表經濟/段落微結構大體通用，
  投稿格式與審稿口味待依 TUST 校準）
- 素材來源：
  - 單向定版成果＝05/RUN_STATUS.md＋00_Document/result（圖5-01~5-21、表5-1~5-5）
  - 雙向定版成果＝06/result（FIG06-01~07＋T06_*）＋06/output/t5/manifest.json
  - 論文中文敘事＝00_Document/260712_TX碩論_Wade.docx（TT 定稿基底，v6 數字）
  - 寫作規範＝00_Document/WRITING_BRIEF.md＋05/process/thesis_style.py

## 待辦（⚖=Wade 裁決）

1. ⚖ 定位拍板：一篇三層貢獻（跨尺度鏈＋雙向回饋＋水位=損傷泵）或拆兩篇
2. ⚖ L0 關回饋 26-tick 對照鏈（~2.5 天算力）——放大係數分解的分母，企劃 P0
3. TUST 投稿規格調查（字數/圖數/格式/近年同主題文章的架構與審稿重點）
4. 架構討論 → 逐節大綱 → 圖表定版 → 英文初稿 → 內審（Codex）→ 投稿包

## 資料夾結構（07-18 起，Word 審閱制——Wade 於 Word 中批改決策）

```
07_SCI_TUST/
  Chapter00_總綱/       00 題目賣點材料｜01 圖表總覽｜02 參考文獻總集APA｜
                        03 摘要關鍵字｜04 碩論濃縮對照表（解析解已砍）
  Chapter01_前言/       子節架構/ 段落核心/ Figure/ Table/ Reference/（各一 docx）
  Chapter02_研究方法/   同上
  Chapter03_研究案例/   同上
  Chapter04_數值模擬/   同上（單向成果；雙向在 Ch05）
  Chapter05_討論/       同上（5.1 雙向、5.2 參數物理意義、5.3 工程含義）
  Chapter06_結論/       同上（5 貢獻＋2 限制；無圖表文獻）
  build_review_docs.py  審閱文件產生器（冪等；依 Wade 批改迭代重建）
  01_ARCHITECTURE.md    內部主控索引（docx 為審閱正本）
  PAPER_PLAN_20260716.md 企劃書 v0（歷史檔）
  refs/REFS_SEED_VERIFIED.md 文獻種子（36 篇、TUST 61%）
```

審閱流程：Wade 在 docx 上批改（LibreOffice/Word 皆可）→ 告知 Fable →
更新 build_review_docs.py 內容 → 重建 → 下一輪。
