#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
merge_260712.py -- 依老師版合稿（07-12）：TT 初稿8 為基底 → 260712_TX碩論_Wade.docx
步驟（冪等，整檔重建）：
  1 複製 TT 原檔
  2 摘要換老師五段版（摘要.docx）＋關鍵字
  3 Ch5 文字回填 v6 定量（雙門檻/黏滯係數/損傷/外壓/推力/變形/裂縫）
  4 換圖 17 張（TT 編號 ↔ result/ v6 圖；同時清該繪圖之 srcRect 裁切、修正長寬）
  5 圖5-21 掛專屬新圖、插入 圖5-22 三維演化＋內文引用
  6 英文摘要改寫對齊
之後由 Word COM 更新欄位。非換圖之既有裁切(srcRect)一律不動。
"""
import copy
import io
import shutil
import sys
import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from PIL import Image

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = "TTW/260711 碩論_營運中隧道結構受地下水位變化引致圍岩依時變形影響(初稿8)_TT.docx"
DST = "260712_TX碩論_Wade.docx"
R = "result/"
EMU_W = 5270000

shutil.copyfile(SRC, DST)
d = docx.Document(DST)
P = d.paragraphs

def set_text(par, text, en=False):
    for r in list(par.runs):
        r._r.getparent().remove(r._r)
    r = par.add_run(text)
    r.font.name = "Times New Roman"
    rpr = r._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    rf.set(qn("w:ascii"), "Times New Roman")
    rf.set(qn("w:hAnsi"), "Times New Roman")
    if not en:
        rf.set(qn("w:eastAsia"), "標楷體")

# ---------- 2 摘要 ----------
A = docx.Document("TTW/摘要.docx")
abs_all = [p.text.strip() for p in A.paragraphs if p.text.strip()]
kw = [t for t in abs_all if t.startswith("關鍵字")][0]
body = [t for t in abs_all if not t.startswith("關鍵字")]
i27 = [i for i, p in enumerate(P) if p.text.strip() == "摘要"][0] + 1
set_text(P[i27], body[0])
set_text(P[i27 + 1], body[1])
anchor = P[i27 + 1]._p
for t in body[2:]:
    newp = copy.deepcopy(P[i27 + 1]._p)
    anchor.addnext(newp)
    anchor = newp
    set_text(Paragraph(newp, P[i27 + 1]._parent), t)
for p in d.paragraphs:
    if p.text.strip().startswith("關鍵字"):
        set_text(p, kw)
        break
print("step2 abstract ok")

# ---------- 3 文字回填 ----------
def find(key):
    for i, p in enumerate(d.paragraphs):
        if key in p.text:
            return i
    return -1

edits = []
i = find("所有模型統一選用應力門檻閥值T=0.8")
edits.append((i,
 "依時變形參數方面，為了模擬出岩體依時變形啟動範圍於高水位階段增廣、於低水位階段大幅縮減之現象，"
 "水位變化各階段（階段2至11）統一選用應力門檻閥值T=0.8；首階段（初始低水位）另經門檻掃描"
 "（T=0.80至1.00）比較後採T=1.0，以建立乾淨之初始基準，避免初始應力平衡之殘餘擾動誇大低水位期"
 "之依時變形範圍。Maxwell黏滯係數ηm=1.2×10^15 Pa·s，Kelvin黏滯係數ηk=2.4×10^13 Pa·s。"))
i = find("全域統一採用門檻閥值=0.8")
t = d.paragraphs[i].text.replace(
 "全域統一採用門檻閥值=0.8與Maxwell、Kelvin黏滯係數 =1.2×10^15 Pa·s、=2.4×10^13 Pa·s",
 "全域統一採用門檻閥值T=0.8（首階段T=1.0，見5.1節）與Maxwell、Kelvin黏滯係數ηm=1.2×10^15 Pa·s、ηk=2.4×10^13 Pa·s")
edits.append((i, t))
i = find("尖峰38,793條")
edits.append((i,
 "水位變化各階段襯砌損傷演化以PFC模型鍵結斷裂累積情形表示如圖 5-16。扣除首階段之初始基準"
 "（2,751條）後，新增斷鍵數(ΔN)於最高水位(階段6)時達尖峰14,570條，水位循環全程之累積斷鍵密度"
 "約1.70%（含初始基準為1.83%）；升水至最高水位時窗（階段2至6）之斷鍵合計占水位循環總損傷之91%，"
 "顯示大多數微裂隙生成時間集中於水位逐漸升高至最高點的階段，水位降低後新生裂隙數量大減"
 "（末段低水位30天僅新增88條）。若以濕期（階段2至6）平均日斷鍵速率與初始低水位期比較，"
 "比值約7.0；退水後末段低水位期速率僅為濕期平均之0.5%，呈現濕期加速、退水後近乎凍結之滯動特徵"
 "（圖中A_wet、A_frz即此二比值）。"))
i = find("最大約1,832 kPa")
t = d.paragraphs[i].text
t = t.replace("水位最低(階段1及11)及最高(階段時的受壓狀況", "水位最低(階段1及11)及最高(階段6)時的受壓狀況")
t = t.replace("最大約1,832 kPa", "最大約946 kPa")
edits.append((i, t))
i = find("環向內力最大的位置發生在隧道西側拱肩")
t = d.paragraphs[i].text
t = t.replace("顯示環向內力最大的位置發生在隧道西側拱肩，隨水位上升增加、水位下降後不恢復",
 "顯示環向內力最大的位置發生在隧道西側拱肩，最高水位與末段低水位皆約1,030 kN/m（初始低水位同部位約260 kN/m），隨水位上升增加、水位下降後不恢復")
t = t.replace("剖面有向西傾斜之變形，且兩側有內擠",
 "剖面有向西傾斜之變形，且兩側有內擠（最高水位時兩側腰部內擠之區域平均值各約0.15 mm，末段低水位幾乎與其重合）")
edits.append((i, t))
i = find("其中環向裂縫總長度最長")
t = d.paragraphs[i].text
t = t.replace("其中環向裂縫總長度最長，集中於東側腰部，累積總裂縫長度隨水位上升增加",
 "其中環向裂縫總長度最長（末階段環向約199 m，遠大於斜向19 m與縱向3 m；裁除模型兩端各2 m之端部影響帶統計），集中於東側腰部；累積總裂縫長度由初期約6 m於最高水位增至201 m、末階段為221 m，增長集中於水位上升時窗、退水後顯著趨緩")
edits.append((i, t))
for i, t in edits:
    assert i >= 0
    set_text(d.paragraphs[i], t)
print("step3 refill ok:", len(edits))

# ---------- 4 換圖 ----------
P = d.paragraphs
SWAPS = {
 430: ([429], "rId69", R + "圖5-05_物理量傳遞示意.png"),
 439: ([438], "rId70", R + "圖5-02_邊坡尺度模型網格與地下水位面.png"),
 441: ([440], "rId71", R + "圖5-06_邊坡尺度水壓分布.png"),
 449: ([448], "rId72", R + "圖5-03_隧道圍岩擾動尺度模型網格與襯砌.png"),
 451: ([450], "rId73", R + "圖5-11_隧道近場水壓洩降.png"),
 459: ([458], "rId74", R + "圖5-04_圍岩襯砌互制尺度模型.png"),
 486: ([485], "rId79", R + "圖5-08_邊坡尺度塑性區與門檻演化.png"),
 488: ([487], "rId80", R + "圖5-09_邊坡變形歷線.png"),
 495: ([494], "rId81", R + "圖5-10_映射驅動場.png"),
 497: ([496], "rId82", R + "圖5-14_隧道周圍有效應力分布與門檻判定.png"),
 501: ([498, 499, 500], "rId83", R + "圖5-12_隧道圍岩塑性區與門檻演化.png"),
 503: ([502], "rId84", R + "圖5-13_隧道收斂曲線.png"),
 513: ([512], "rId85", R + "圖5-15_襯砌損傷演化歷程.png"),
 515: ([514], "rId86", R + "圖5-16_襯砌外壓展開圖.png"),
 517: ([516], "rId87", R + "圖5-17_襯砌內力分布.png"),
 519: ([518], "rId88", R + "圖5-18_襯砌變形.png"),
 521: ([520], "rId89", R + "圖5-19_襯砌裂縫發展與分類.png"),
}

def fix_drawing(dr, cx, cy):
    for sr in list(dr.iter(qn("a:srcRect"))):
        sr.getparent().remove(sr)
    for ext in dr.iter(qn("wp:extent")):
        ext.set("cx", str(cx)); ext.set("cy", str(cy))
    for ext in dr.iter(qn("a:ext")):
        if ext.getparent().tag == qn("a:xfrm"):
            ext.set("cx", str(cx)); ext.set("cy", str(cy))

rels = d.part.rels
for cap, (imps, rid, png) in SWAPS.items():
    w, h = Image.open(png).size
    cy = int(EMU_W * h / w)
    rels[rid].target_part._blob = open(png, "rb").read()
    first = True
    for ip in imps:
        draws = list(P[ip]._p.iter(qn("w:drawing")))
        for k, dr in enumerate(draws):
            if first and k == 0:
                fix_drawing(dr, EMU_W, cy)
            else:
                dr.getparent().remove(dr)
        first = False
print("step4 swaps ok:", len(SWAPS))

# ---------- 5 圖5-21 專屬圖 + 圖5-22 ----------
png = R + "圖5-21_襯砌裂縫長度累積.png"
w, h = Image.open(png).size
rid21, _ = d.part.get_or_add_image(png)
dr21 = list(P[522]._p.iter(qn("w:drawing")))
assert dr21, "5-21 drawing missing"
for b in dr21[0].iter(qn("a:blip")):
    b.set(qn("r:embed"), rid21)
fix_drawing(dr21[0], EMU_W, int(EMU_W * h / w))
png2 = R + "圖5-20_襯砌裂縫三維演化.png"
w2, h2 = Image.open(png2).size
rid22, _ = d.part.get_or_add_image(png2)
imgp = copy.deepcopy(P[522]._p)
P[523]._p.addnext(imgp)
for b in imgp.iter(qn("a:blip")):
    b.set(qn("r:embed"), rid22)
for dr in imgp.iter(qn("w:drawing")):
    fix_drawing(dr, EMU_W, int(EMU_W * h2 / w2))
capp = copy.deepcopy(P[523]._p)
imgp.addnext(capp)
set_text(Paragraph(capp, P[523]._parent), "圖 5-22 隧道襯砌裂縫三維演化圖(四代表階段)")
for p in d.paragraphs:
    if "襯砌裂縫展開圖、剖面及各階段長度統計如圖 5-20至圖 5-21" in p.text:
        set_text(p, p.text.replace("如圖 5-20至圖 5-21",
                 "如圖 5-20至圖 5-21（三維視角之四階段演化詳圖 5-22）", 1))
        break
print("step5 fig5-21/5-22 ok")

# ---------- 6 英文摘要 ----------
EN = [
 "During long-term operation, tunnels may be affected by rainfall infiltration, groundwater-level fluctuations, geological structures, and the creep characteristics of the surrounding rock, so that a tunnel structure that has apparently stabilized deforms again, leading to lining cracking, spalling, or support deterioration. Existing studies on tunnel time-dependent deformation focus mostly on the excavation stage or the early post-construction period; how repeated groundwater-level changes during operation modify the effective-stress state of the surrounding rock and further damage the tunnel structure has not been fully discussed. This study therefore takes a mountain railway tunnel in Taiwan as a case to investigate groundwater-level-induced time-dependent deformation of the surrounding rock and its influence on an in-service tunnel structure.",
 "A modified Burgers model with a stress-threshold concept is adopted to establish, on the basis of effective stress and seepage, a conceptual model for the influence of groundwater-level fluctuations on tunnel time-dependent deformation. When the groundwater level rises, pore pressure and seepage forces alter the effective-stress distribution around the tunnel, bringing part of the surrounding rock close to or beyond the time-dependent deformation threshold and thereby initiating or accelerating long-term deformation; when the groundwater level falls, the activated region shrinks and the deformation rate slows down.",
 "For the case tunnel, this study integrates existing literature, borehole data, groundwater monitoring, electrical resistivity surveys, terrain interpretation, and tunnel-face images to build a three-dimensional engineering geological model spanning the regional-geology, slope-investigation, and tunnel scales, clarifying the spatial relations among tunnel anomalies, crack distribution, strata, weak zones, and groundwater conditions.",
 "To overcome the scale gap between slope-scale hydrogeological processes and local lining damage, a cross-scale numerical simulation framework is established. A slope-scale FLAC3D model first simulates the effective-stress changes and time-dependent slope deformation caused by groundwater-level fluctuations, and transfers the deformation rates to the boundary of the tunnel-scale model. The tunnel-scale model further incorporates excavation, lining, and near-wall pressure drawdown to analyse the stress state, threshold-activated region, and convergence behaviour of the surrounding rock. Finally, a coupled FLAC3D-PFC rock-lining interaction model transfers the rock deformation to the bonded-particle lining to simulate lining compression, damage generation, and crack development.",
 "The results show that groundwater-level fluctuations change the effective stress at the slope scale and, through time-dependent deformation of the surrounding rock, influence the local tunnel response. The slope-scale model exhibits slow deformation at low water levels, accelerated deformation at high levels, and deceleration after drawdown. The rock-lining interaction model reproduces the main characteristics of lining cracking under compression: cracks are dominantly circumferential with subordinate oblique ones and concentrate in the anomalous curved section, in good agreement with field observations. Overall, this study establishes an analysis workflow from groundwater-level change through rock time-dependent deformation to lining damage, and demonstrates that a three-dimensional engineering geological model combined with cross-scale numerical simulation is an effective tool for assessing the long-term deformation mechanism and maintenance strategies of in-service tunnels.",
]
KW = ("Keywords: Lining anomaly, Groundwater-level change, Time-dependent deformation, "
      "3D engineering geological model, Modified Burgers model, Cross-scale numerical simulation")
Pn = d.paragraphs
ei = [i for i, p in enumerate(Pn) if p.text.strip() == "ABSTRACT"][0]
en, kwi = [], None
for i in range(ei + 1, ei + 12):
    t = Pn[i].text.strip()
    if t.startswith("Keywords"):
        kwi = i
        break
    if t:
        en.append(i)
n = min(len(en), len(EN))
for k in range(n):
    set_text(Pn[en[k]], EN[k], en=True)
anchor = Pn[en[-1]]._p
for t in EN[n:]:
    newp = copy.deepcopy(Pn[en[-1]]._p)
    anchor.addnext(newp)
    anchor = newp
    set_text(Paragraph(newp, Pn[en[-1]]._parent), t, en=True)
set_text(Pn[kwi], KW, en=True)
print("step6 EN abstract ok")

d.save(DST)
print("MERGED SAVED:", DST)
