#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_final60.py -- 自 88 篇工作庫產出正式參考清單（TUST 全留 39 ＋ 非 TUST 精選 21）。

非 TUST 精選原則（依序）：
  1. 角色不可替代（原典／血緣錨／模板／子類唯一來源）
  2. 已完成全文精讀者優先
  3. 被引次數與相關性
輸出：REFS_FINAL60.md（正式清單）＋ READING_GAP.md（尚未全文者與取得方式）
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = Path(__file__).parent.parent

KEEP_NONTUST = {
    "Barla_2012":    "1A｜擠壓依時案例經典（監測反分析）",
    "Sulei_2022":    "1B｜排水系統劣化→襯砌開裂案例（1B 僅有非 TUST 來源）",
    "Tarifard_2022": "1B｜潛變＋水對襯砌載重之長期反分析（1B 僅有非 TUST 來源）",
    "WangTT_2010":   "1C｜★血緣錨：襯砌裂縫型態分類原典，§4.3 語彙來源",
    "Sulem_1987":    "2A｜依時收斂解析原典（系譜句起點）",
    "Tsai_inreview": "2B｜★前作：門檻黏彈塑模式（本文理論母體）",
    "Yan_2020":      "2B｜水—岩作用改良本構（連接驅動與機制）",
    "Li_2021":       "2B｜飽和—失水循環潛變劣化本構（水循環之本構依據）",
    "Guo_2021":      "4A｜隱式曲面＋marching tetrahedra 由鑽孔建模（技術程序）",
    "Parry_2014":    "4B｜★IAEG Commission 25：工程地質模型之制度性定義（區域／場址尺度）",
    "Liu_2020":      "4C｜地層界面不確定性（本文離散化之誠實陳述依據）",
    "Vazaios_2019":  "5B｜FDEM 隧道 EDZ 最高引（驗證階梯三級跳）",
    "Potyondy_2004": "5C｜★BPM 原典（5C 無 TUST 來源）",
    "Cho_2007":      "5C｜拉壓比缺陷之量化（四步論證鏈第一步）",
    "Wu_2016":       "5C｜flat-joint 對三內在問題之修正（第二步）",
    "Nitka_2018":    "5C｜混凝土 DEM×μCT 標定（第四步：混凝土依據）",
    "Cai_2004":      "5C｜裂縫起始／損傷應力門檻（σ_ci 標定目標）",
    "Yoon_2007":     "5C｜DOE 微參數標定與敏感度排序",
    "Wang_2023":     "6B｜圍岩潛變→襯砌漸進破壞案例",
    "Liu_2023":      "6B｜DEM 襯砌材料缺陷漸進破壞（最近似本文離散襯砌）",
    "Zheng_2024":    "6B｜★模板論文：潛變作用下襯砌損傷演化",
}


def main():
    acc = json.loads((HERE / "_tools/_access_levels.json").read_text(encoding="utf-8"))
    rl = json.loads((HERE / "_tools/_reading_list.json").read_text(encoding="utf-8"))
    doi2id = {it["doi"].lower(): it["id"] for it in rl}
    meta = {it["id"]: it for it in rl}

    cur_g = cur_s = None
    picked, dropped = [], []
    for ln in (HERE / "REFS_MASTER.md").read_text(encoding="utf-8").splitlines():
        if ln.startswith("## "):
            cur_g = ln[3:].split("（")[0]
        elif ln.startswith("### "):
            cur_s = ln[4:].split("（")[0]
        elif ln.startswith("- ["):
            m = re.search(r"10\.[\d./()\w-]+", ln)
            doi = (m.group(0).rstrip(").") if m else "").lower()
            _id = doi2id.get(doi, "Tsai_inreview" if "in review" in ln else "?")
            tust = "[TUST]" in ln or "Tunnelling and Underground" in ln
            body = re.sub(r"^- \[\w\](\s*\*\*\[TUST\]\*\*)?\s*", "", ln)
            rec = dict(g=cur_g, sub=cur_s, id=_id, tust=tust, body=body,
                       full=acc.get(_id, "?").startswith("full"),
                       cite=int(cm.group(1)) if (cm := re.search(r"被引 (\d+)", ln)) else 0)
            (picked if (tust or _id in KEEP_NONTUST) else dropped).append(rec)

    n = len(picked)
    nt = sum(1 for r in picked if r["tust"])
    nf = sum(1 for r in picked if r["full"])
    out = ["# REFS_FINAL60｜正式參考清單（自 88 篇工作庫精選）", "",
           f"> **{n} 篇；TUST {nt} 篇（{100*nt/n:.0f}%）；已全文精讀 {nf} 篇（{100*nf/n:.0f}%）**",
           "> 原則：TUST 全留；非 TUST 依「角色不可替代 → 已全文 → 被引×相關性」精選。",
           "> ✔＝已全文精讀；○＝尚未全文（清單見 READING_GAP.md）。", ""]
    order, seen = [], set()
    for r in picked:
        if r["sub"] not in seen:
            seen.add(r["sub"]); order.append((r["g"], r["sub"]))
    lastg = None
    for g, s in order:
        if g != lastg:
            out += [f"## {g}", ""]; lastg = g
        lst = sorted([r for r in picked if r["sub"] == s], key=lambda x: -x["cite"])
        out += [f"### {s}（{len(lst)} 篇，TUST {sum(1 for r in lst if r['tust'])}）", ""]
        for r in lst:
            mark = "✔" if r["full"] else "○"
            tag = " **[TUST]**" if r["tust"] else ""
            note = f"　※{KEEP_NONTUST[r['id']]}" if r["id"] in KEEP_NONTUST else ""
            out.append(f"- {mark}{tag} {r['body']}{note}")
        out.append("")
    (HERE / "REFS_FINAL60.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    gap = [r for r in picked if not r["full"]]
    need = max(0, int(-(-n * 8 // 10)) - nf)
    PDF_ONHAND = {"Fahimifar_2010"}
    g2 = ["# READING_GAP｜正式清單中尚未全文精讀者", "",
          f"> 正式清單 {n} 篇，已全文 {nf} 篇（{100*nf/n:.0f}%）。",
          f"> 達 80%（{-(-n*8//10)} 篇）尚需再讀 **{need}** 篇；下列 {len(gap)} 篇全讀則達 100%。", "",
          "## A. 本機已有 PDF，可立即精讀", ""]
    for r in sorted(gap, key=lambda x: -x["cite"]):
        if r["id"] in PDF_ONHAND:
            g2.append(f"- {r['id']}（被引 {r['cite']}｜{r['sub']}）— Wade_TD_SCI/Reference/2020_2025/analyze/")
    g2 += ["", "## B. 需下載 PDF（⚖ 請置入 References/PDF/）", ""]
    for r in sorted(gap, key=lambda x: -x["cite"]):
        if r["id"] not in PDF_ONHAND:
            it = meta.get(r["id"], {})
            g2.append(f"- **{r['id']}**（被引 {r['cite']}｜{r['sub']}）"
                      f" https://doi.org/{it.get('doi','?')}")
    (HERE / "READING_GAP.md").write_text("\n".join(g2) + "\n", encoding="utf-8")

    print(f"正式清單 {n} 篇｜TUST {nt}（{100*nt/n:.0f}%）｜已全文 {nf}（{100*nf/n:.0f}%）")
    print(f"未入選 {len(dropped)} 篇（留在工作庫 REFS_MASTER）")
    print(f"達 80% 尚需再讀 {need} 篇；未讀清單共 {len(gap)} 篇 → READING_GAP.md\n")
    for g, s in order:
        lst = [r for r in picked if r["sub"] == s]
        print(f"  {s:22s} {len(lst):2d} 篇（TUST {sum(1 for r in lst if r['tust'])}"
              f"｜已讀 {sum(1 for r in lst if r['full'])}）")


if __name__ == "__main__":
    main()
