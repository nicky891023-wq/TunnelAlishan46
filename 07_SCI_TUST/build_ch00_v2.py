#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_ch00_v2.py -- Chapter00 總綱 v2（56 篇精讀後全面重寫；文書規則落地）。

文書規則（Wade 07-22，IJRMMS 慣例）：
  * 段落末【重點：…】黃底黑字
  * 引用文獻藍字（author-year，如 (Chiu et al., 2017)）
  * 圖XX 紅字、表XX 綠字
行內標記語法：⟦B:藍字⟧ ⟦R:紅字⟧ ⟦G:綠字⟧；P(point=...) 產生段末黃底重點。
執行前自動備份既有 Chapter00 docx 至 _backup_YYMMDD/。
"""
import io
import shutil
import sys
import time
from pathlib import Path

import docx
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).parent
CH0 = ROOT / "Chapter00_總綱"
BLUE, RED, GREEN = (0x1F, 0x4E, 0xC8), (0xC0, 0x00, 0x00), (0x00, 0x80, 0x40)

bk = CH0 / f"_backup_{time.strftime('%y%m%d')}"
bk.mkdir(exist_ok=True)
for f in CH0.glob("*.docx"):
    shutil.copy2(f, bk / f.name)
print(f"backup -> {bk.name} ({len(list(bk.glob('*.docx')))} files)")


def new_doc():
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Times New Roman"
    st.font.size = Pt(12)
    st._element.rPr.rFonts.set(qn("w:eastAsia"), "標楷體")
    return d


def _run(p, text, size, bold=False, color=None, hl=False):
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(size)
    r.font.bold = bold
    if color:
        r.font.color.rgb = RGBColor(*color)
    if hl:
        r.font.highlight_color = WD_COLOR_INDEX.YELLOW
    rpr = r._r.get_or_add_rPr()
    rf = rpr.find(qn("w:rFonts"))
    if rf is None:
        from docx.oxml import OxmlElement
        rf = OxmlElement("w:rFonts")
        rpr.insert(0, rf)
    rf.set(qn("w:ascii"), "Times New Roman")
    rf.set(qn("w:hAnsi"), "Times New Roman")
    rf.set(qn("w:eastAsia"), "標楷體")
    return r


def rich(p, text, size=12, bold=False):
    """render ⟦B:…⟧/⟦R:…⟧/⟦G:…⟧ inline colour markup"""
    i = 0
    while i < len(text):
        j = text.find("⟦", i)
        if j < 0:
            _run(p, text[i:], size, bold)
            break
        if j > i:
            _run(p, text[i:j], size, bold)
        k = text.find("⟧", j)
        tag, body = text[j + 1], text[j + 3:k]
        col = {"B": BLUE, "R": RED, "G": GREEN}.get(tag)
        _run(p, body, size, bold, color=col)
        i = k + 1


def H(d, text, lv=1):
    p = d.add_paragraph()
    _run(p, text, 16 if lv == 1 else 14, bold=True)
    return p


def P(d, text, size=12, bold=False, indent=False, point=None):
    p = d.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Pt(18)
    rich(p, text, size, bold)
    if point:
        _run(p, "　", size)
        _run(p, f"【重點：{point}】", max(size - 1, 10), bold=False, color=(0, 0, 0), hl=True)
    return p


def DEC(d, text):
    p = d.add_paragraph()
    _run(p, "【⚖ 待裁決】", 12, bold=True, color=RED)
    rich(p, text, 12)
    return p


def TBL(d, header, rows, size=10.5):
    t = d.add_table(rows=1 + len(rows), cols=len(header))
    t.style = "Table Grid"
    for j, h in enumerate(header):
        c = t.rows[0].cells[j]
        c.text = ""
        _run(c.paragraphs[0], h, size + 0.5, bold=True)
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            c = t.rows[1 + i].cells[j]
            c.text = ""
            rich(c.paragraphs[0], str(v), size)
    return t


def save(d, name):
    d.save(CH0 / name)
    print("OK", name)


# ========================== 00 題目賣點材料 v3 ==========================
d = new_doc()
H(d, "文章題目、賣點、材料（框架首頁 v3，2026-07-22；56 篇精讀後重寫）")
P(d, "本版依全庫 56 篇逐篇精讀之數據重寫（統計見 refs/reading_notes/_SYN_title_anatomy.md）。"
     "文書規則自本版起落地：段落末黃底重點、引用文獻藍字、⟦R:圖XX⟧ 紅字、⟦G:表XX⟧ 綠字。",
  size=11, point="本頁=全文之錨；此頁不穩不動正文")

H(d, "一、題目（定版建議＝混血案；56 題解剖數據支撐）", 2)
P(d, "數據事實：我們的賽道（營運隧道病害×機制歸因）11/11 題目零方法詞；案例匿名化 30/31"
     "（“an operating tunnel” 式）；“under+水文驅動” 有同刊直接前例 ⟦B:(Sun et al., 2023)⟧；"
     "“crack evolution” 承接 ⟦B:(Chiu et al., 2017)⟧ 系譜（被引 94）。",
  point="賽道慣例：題目零方法詞、案例匿名、方法退居賣點層")
P(d, "首選（評分 22/25）：", bold=True)
P(d, "Lining crack evolution of an operating mountain railway tunnel under cyclic "
     "groundwater fluctuation: intermittent time-dependent deformation as the driving mechanism",
  indent=True, bold=True)
P(d, "營運山岳鐵路隧道襯砌裂縫在地下水位循環下之演化：以滯動依時變形為驅動機制", indent=True)
P(d, "主標繼承 ⟦B:(Chiu et al., 2017)⟧ 的「crack evolution of an operational tunnel」構式"
     "（續作訊號）；副標把 intermittent time-dependent deformation 佔位入題、跨刊承接前作"
     "⟦B:(Tsai et al., in review)⟧ 術語——一題同時鎖兩條團隊系譜。", indent=True, size=11,
  point="一題鎖雙系譜：2017 案例線＋前作理論線")
P(d, "備案 A（安全牌，若機制證據鏈不足以撐單因歸因）：Lining crack evolution of an operating "
     "mountain railway tunnel influenced by cyclic groundwater fluctuation", indent=True, size=11)
P(d, "備案 B（審稿疑慮時副標降級）：副標改 the role of intermittent time-dependent deformation"
     "（弱化為角色探討；不建議先自弱）。", indent=True, size=11)
DEC(d, "題目定版：首選混血案／備案 A？（N-B 淘汰：三連字複合詞、56 篇樣本零前例）")

H(d, "二、賣點（v2 重排：案例×機制＝故事主軸，方法＝差異化手段）", 2)
P(d, "賣點 1｜案例資產之唯一性：營運中文化資產鐵道隧道×十年病徵時序複合監測鏈"
     "（LiDAR 全斷面兩期、三期異狀展開圖、裂縫計持續緩剪紀錄、修復履歷、水位計年擺幅）。"
     "戰法＝⟦B:(Chiu et al., 2017)⟧ 的稀缺性反轉：長期裂縫時序紀錄極少見，n=1 翻成資料價值。",
  indent=True, point="故事主角是案例，不是模型")
P(d, "賣點 2｜機制主張＝滯動起閉的襯砌尺度延伸：前作 ⟦B:(Tsai et al., in review)⟧ 建立圍岩尺度"
     "滯動理論，本文推進到「水位相位控制襯砌損傷節律」：雨峰爆發 A_wet=7.0、退水凍結 "
     "A_frz=0.0046、濕窗貢獻 91% 損傷增量。", indent=True, point="機制詞已入題＝佔位")
P(d, "賣點 3｜方法特色一：三維工程地質模型錨定之跨尺度傳遞鏈（坡地→隧道→襯砌；340 m 鑽探"
     "＋室內試驗給參數出處；Kabsch 剛體扣除＋應變一致性檢核）。", indent=True,
  point="地質模型是出處不是背景")
P(d, "賣點 4｜方法特色二：BPM 離散襯砌之裂縫型態學（2.08M 鍵結、三軌分類環/斜/縱，與現地"
     "展開圖同座標對照）。最近前例 ⟦B:(Liu et al., 2023)⟧ 僅及材料缺陷單調載重、"
     "⟦B:(Zheng et al., 2024)⟧ 僅及潛變無水；水文循環驅動之離散襯砌損傷無人做過。",
  indent=True, point="離散襯砌×水循環＝文獻空格")
P(d, "賣點 5｜方法特色三＋工程收尾：D→E 損傷回饋初探（day-130 損傷達單向 2.83×，放討論章）"
     "＋「地下水位管理＝襯砌損傷管理」之維養含義（TUST maintenance 範疇甜蜜點）。",
  indent=True, point="回饋當討論不當主菜；工程含義收尾")
DEC(d, "賣點措辭與排序？（案例先行、方法置後之新排序是否符合你的直覺）")

H(d, "三、材料（5 項食材，不變）", 2)
for i, s in enumerate([
    "修正力學模式（門檻黏彈塑 Burgers-Mohr；s1 門檻掃描定準法）——引前作、只寫差異",
    "三維工程地質模型（坡地 4 層／隧道 6 層／互制模型；202411 附錄 11/12/13 鑽探試驗出處）",
    "真實案例資料（#46 隧道 1233 m、R=50 曲線：LiDAR 兩期、三期展開圖、裂縫計、修復履歷）",
    "單向弱耦合定版成果（05 v6：130 天、37,980 斷鍵、環199/斜19/縱3 m、外壓 946 kPa、推力 1,029 kN/m）",
    "雙向強耦合鏈（06 T5：26×5 天、D→E 回饋、107,479 斷鍵=2.83×）"], 1):
    P(d, f"材料 {i}：{s}", indent=True, size=11)
H(d, "四、討論要點（5 項，不變）", 2)
for s in ["雙向 vs 單向放大之分解（L0 對照鏈）", "門檻 T 的物理意義與定準敏感度",
          "水位擺幅情境論證（實測 ~30 m vs 模擬 100 m）", "f=0.25 縮尺與趨勢級解讀邊界",
          "水位管理＝損傷管理（滯動泵收尾）"]:
    P(d, "・" + s, indent=True, size=11)
save(d, "00_題目賣點材料.docx")

# ========================== 01 圖表總覽 v2 ==========================
d = new_doc()
H(d, "全文圖表總覽 v2（15 圖＋5 表；上限 16）")
P(d, "更新：依 ⟦B:(Zhang et al., 2025)⟧ 的文獻系譜時間軸戰法（Fig.1 終點紅字 This work、"
     "審稿人 10 秒看懂定位），建議 ⟦R:圖4⟧ 增加系譜面板：連續體潛變→非連續 DEM→水力耦合→"
     "跨尺度 FDM-DEM（This work）。", size=11, point="系譜圖＝前言的視覺化，強烈建議採用")
TBL(d, ["圖", "內容與故事", "素材／加工"], [
    ["⟦R:圖1⟧", "場址與案例綜覽（林鐵×曲線隧道×坡地）", "附圖95+96＋App5；新繪"],
    ["⟦R:圖2⟧", "#46 現地病徵時序（三期展開圖＋裂縫照片＋裂縫計）", "附圖93/97/100-102；重組英化"],
    ["⟦R:圖3⟧", "水文驅動（水位計年擺幅→W 面家族→情境）", "碩論表4-1＋擬合；⚖需主報告時序"],
    ["⟦R:圖4⟧", "跨尺度方法流程＋資料傳遞＋文獻系譜面板（This work）", "圖5-01 擴充＋新系譜面板"],
    ["⟦R:圖5⟧", "三尺度模型三面板", "圖5-02+03+04 合併"],
    ["⟦R:圖6⟧", "τ-p 門檻機制（濕季應力雲移入門檻帶）", "圖5-14 現成"],
    ["⟦R:圖7⟧", "門檻活化演化（乾衰減→雨爆發→退凍結）", "圖5-08+5-12 縮幀合併"],
    ["⟦R:圖8⟧", "近場排水暈", "圖5-11 現成"],
    ["⟦R:圖9⟧", "襯砌損傷史 A_wet/A_frz", "圖5-15 現成"],
    ["⟦R:圖10⟧", "襯砌外壓＋內力（946 kPa 帶＋1,029 kN/m 力偶）", "圖5-16+5-17 合併"],
    ["⟦R:圖11⟧", "裂縫發展與分類（與圖2 同座標展開）", "圖5-19 改造"],
    ["⟦R:圖12⟧", "三維裂縫演化（hero）", "圖5-20 現成"],
    ["⟦R:圖13⟧", "雙向耦合方法＋單雙向時間線", "FIG06-01 期刊化"],
    ["⟦R:圖14⟧", "D(s,y) 損傷圖演化", "FIG06-02 期刊化"],
    ["⟦R:圖15⟧", "滯動損傷泵概念圖（bookend）", "新繪 pptx"],
])
P(d, "")
TBL(d, ["表", "內容", "備註"], [
    ["⟦G:表1⟧", "文獻案例彙編（8 欄中性矩陣）", "不含 this study 行（前作教訓）"],
    ["⟦G:表2⟧", "三尺度模型組態與參數（含出處欄）", "回應 K0/參數來源問"],
    ["⟦G:表3⟧", "門檻與潛變參數（定準依據＋物理意義欄）", "回應門檻依據問"],
    ["⟦G:表4⟧", "現地調查監測資料彙整", "案例可信度（賣點 1 的證據表）"],
    ["⟦G:表5⟧", "單向 vs 雙向逐階段對照＋QA gates 摘要", "討論章"],
])
DEC(d, "圖4 系譜面板採不採？15 圖／5 表確認？")
save(d, "01_圖表總覽.docx")

# ========================== 02 參考文獻總集 v3 ==========================
d = new_doc()
H(d, "參考文獻總集（APA 7；v3＝56 篇全量＋閱讀狀態）")
P(d, "標記：★＝全文精讀（23 篇）；☆＝摘要級（33 篇，Elsevier 付費牆——補件優先序見 "
     "refs/ACCESS_LIST.md，⚖ 請以校園權限下載放入 Wade_TD_SCI/Reference/ 我即補讀）。"
     "TUST 31/56=55%（達標 ≥50%）；零 MDPI；全數 Crossref 逐 DOI 驗證。"
     "正文引用時一律 author-year 藍字，如 ⟦B:(Chiu et al., 2017)⟧、⟦B:(Fahimifar & Zareifard, 2009)⟧。",
  size=11, point="正式引用格式=Elsevier name-year；本檔為總庫、逐篇筆記在 refs/reading_notes/")
import json as _json
import re as _re
_acc = _json.loads((ROOT / "refs" / "_tools" / "_access_levels.json").read_text(encoding="utf-8"))
_master = (ROOT / "refs" / "REFS_MASTER.md").read_text(encoding="utf-8").splitlines()
_doi2id = {}
for _it in _json.loads((ROOT / "refs" / "_tools" / "_reading_list.json").read_text(encoding="utf-8")):
    _doi2id[_it["doi"].lower()] = _it["id"]
for _ln in _master:
    if _ln.startswith("## "):
        H(d, _ln[3:], 2)
    elif _ln.startswith("- ["):
        _m = _re.search(r"10\.[\d.]+/[^\s]+", _ln)
        _id = _doi2id.get((_m.group(0).rstrip(").") if _m else "").lower(), "")
        _star = "★" if _acc.get(_id, "").startswith("full") else "☆"
        _body = _re.sub(r"^- \[\w\](\s*\*\*\[TUST\]\*\*)?\s*", "", _ln)
        _tust = " [TUST]" if "**[TUST]**" in _ln else ""
        P(d, f"{_star}{_tust} {_body}", size=10, indent=True)
save(d, "02_參考文獻總集_APA.docx")

# ========================== 03 摘要與關鍵字 v2 ==========================
d = new_doc()
H(d, "摘要與關鍵字（v2；依新題目與缺口短版規則重寫）")
P(d, "規則：摘要第 2–3 句放缺口濃縮版（⟦B:(Wu et al., 2024)⟧「缺口說兩次」戰法）；"
     "結尾三分號結論式（前作格式）；不出現方法詞直到中段。", size=11)
P(d, "營運中山岳鐵路隧道之襯砌裂縫常與降雨及地下水活動高度相關，然其逐年演化之驅動機制"
     "尚缺乏定量解釋；既有研究多以穩態或單調水文情境處理地下水，且連續體模型無法顯式解析"
     "裂縫之萌生與擴展。本文以臺灣阿里山林業鐵路某曲線段營運隧道為對象，整合十年裂縫調查"
     "（雷射掃描兩期與三期展開圖）、裂縫計監測與水位觀測，建立三維工程地質模型錨定之跨尺度"
     "數值鏈——坡地尺度滲流、隧道尺度門檻滯動潛變、襯砌尺度鍵結顆粒離散開裂——重現水位"
     "年循環下襯砌損傷之時空發展，並以損傷—勁度回饋初探襯砌劣化之自增強效應。結果顯示："
     "雨峰窗口貢獻約九成之損傷增量，濕季損傷速率為初始乾季之 7.0 倍、退水後降至雨季之 0.5%，"
     "水位相位實質控制損傷節律；模擬裂縫呈帶狀分區且以環向為主導，與曲線異狀段現地展開圖"
     "對照一致【W1 統計回填】；考慮損傷回饋後 130 天累積損傷達單向分析之 2.83 倍，顯示襯砌"
     "劣化評估若忽略互制回饋將顯著低估。", point="缺口第2-3句＋三分號結論＋方法詞中段才出現")
H(d, "關鍵字（5–8；含題目佔位詞）", 2)
P(d, "EN: lining crack evolution; groundwater fluctuation; intermittent time-dependent "
     "deformation; operating tunnel; cross-scale simulation; tunnel maintenance")
P(d, "中：襯砌裂縫演化；地下水位循環；滯動依時變形；營運隧道；跨尺度模擬；隧道維養")
DEC(d, "摘要走向？「損傷泵」隱喻是否入摘要末句？")
save(d, "03_摘要與關鍵字.docx")

# ========================== 04 碩論濃縮對照表（沿用） ==========================
d = new_doc()
H(d, "碩論→期刊濃縮對照表（第一刀：解析解全砍；v2 補讀後註記）")
TBL(d, ["碩論內容", "期刊處置", "說明"], [
    ["Ch1 緒論", "濃縮入前言 P1/P5", "研究方法沿革刪"],
    ["Ch2 解析解相關", "【砍】", "僅 ⟦B:(Fahimifar & Zareifard, 2009)⟧ 留作討論章量級對照"],
    ["Ch2 潛變理論/模型系譜", "砍，引前作", "前言以 56 篇文獻庫重建；⟦R:圖4⟧ 系譜面板取代"],
    ["Ch3 案例（TT 版）", "濃縮入期刊 Ch3", "病徵分型＋監測時序保留（案例先行政治：⟦B:(Wang et al., 2023)⟧ 式獨立背景節）"],
    ["Ch4 多尺度地質模型", "期刊 3.3 一節＋⟦G:表2⟧", "建模過程刪、只留組態＋出處"],
    ["Ch5.1-5.2 方法", "期刊 Ch2", "假設條款前置法（⟦B:(Wu et al., 2024)⟧ 式引文護盾）"],
    ["Ch5.3-5.4 單向成果", "期刊 Ch4（21 圖→9 張）", "刪過程性圖；⚖ 圖5-10 驅動場驗證去留"],
    ["Ch5.5 侷限", "拆入討論＋結論限制", "包裝依 _SYN_packaging 十式"],
    ["Ch6 結論", "重寫（5 貢獻＋2 限制）", "不復述"],
    ["（碩論無）雙向耦合", "期刊 5.1 新寫", "初探定位"],
])
DEC(d, "續裁三候選：①坡地尺度篇幅②圖5-10 去留③QA 寫入深度")
save(d, "04_碩論濃縮對照表.docx")

# ========================== 05 寫作工藝手冊（新） ==========================
d = new_doc()
H(d, "寫作工藝手冊（56 篇精讀萃取；本檔即文書規則示範）")
P(d, "來源：refs/reading_notes/ 三份綜合報告（_SYN_title_anatomy／_SYN_intro_moves／"
     "_SYN_packaging），本手冊為落筆版摘要；細節與逐篇證據回查原檔。",
  size=11, point="這一頁是「怎麼寫」的作戰卡，寫作時貼在螢幕邊")

H(d, "一、題目工藝（56 題解剖）", 2)
P(d, "病害機制賽道 11/11 零方法詞；案例匿名化 30/31；「driven by」樣本零出現、"
     "「influenced by」僅 ⟦B:(Chiu et al., 2017)⟧ 一例、「under+情境」80%+ 為壓倒性構式；"
     "自創機制詞入題＝佔定義權（non-Darcy、pipeline-type karst 前例）。",
  point="題目零方法字＋under 構式＋機制詞佔位")

H(d, "二、前言五段骨架（B 型雙支線＋二階二分法收束）", 2)
P(d, "P1 現象共識＋案例鉤子：共識句（襯砌裂縫=營運隧道最常見病害）→場景收窄（山岳鐵路×"
     "多雨×服役 N 年）→硬數字鉤子 1-2 個→維修反覆失效句 ⟦B:(Wang et al., 2023)⟧→需求收尾。"
     "全段零方法詞。", indent=True, size=11, point="P1 禁方法詞；鉤子要帶數字")
P(d, "P2 支線 A（襯砌裂縫研究）→第一刀：一句一人動詞鏈 4-8 筆（⟦B:(Chiu et al., 2017)⟧"
     "⟦B:(Wang et al., 2024)⟧⟦B:(Chen et al., 2024)⟧⟦B:(Zhang et al., 2022)⟧…）→段尾缺口："
     "既有成果多靜態/單調載重，水文驅動的時間演化未被檢視。缺口寫成「實務失效/認識缺口」型，"
     "不寫方法缺口。", indent=True, size=11, point="第一刀砍在認識缺口，不砍方法")
P(d, "P3 支線 B（水×隧道依時）→第二刀：三軌回顧（解析 ⟦B:(Fahimifar & Zareifard, 2009)⟧／"
     "實驗 ⟦B:(Sun et al., 2023)⟧⟦B:(Li et al., 2021)⟧／案例 ⟦B:(Tarifard et al., 2022)⟧）→"
     "段尾雙短句：穩態假設×連續體極限。王牌證詞：⟦B:(Wang et al., 2023)⟧ 自陳水是 root cause "
     "但模型無水——同社群自指未解的落差。", indent=True, size=11,
  point="雙層下刀：情境缺口＋工具缺口分開砍")
P(d, "P4 方法系譜＋二階二分法收束：耦合已成熟（⟦B:(Zhou et al., 2024)⟧⟦B:(Bai et al., 2022)⟧"
     "⟦B:(Lisjak et al., 2015)⟧⟦B:(Yan et al., 2023)⟧）→「既有耦合研究聚焦開挖期圍岩；"
     "少數及襯砌者僅單調載重。同時滿足（i）水位循環載重（ii）襯砌裂縫顯式解析（iii）跨尺度"
     "互制之框架仍闕如」。搭配 ⟦R:圖4⟧ 系譜面板 This work 落點。", indent=True, size=11,
  point="三要素句框出唯一空格＝本文形狀")
P(d, "P5 貢獻宣告：To address this gap→案例錨定句（資料規格式：年數/期數/測點數）→方法鏈句→"
     "not only…but also 雙賣點句（機制揭示＋維養門檻）→機制鏈口號預告。不用 novel/first。",
  indent=True, size=11, point="not only…but also＝TUST 高頻貢獻句式")

H(d, "三、缺陷包裝（十式精選＋我方六弱點對策）", 2)
P(d, "樣本大發現：25 篇全文中僅 2 篇設獨立 limitations 節——主流是「就地消化」。",
  point="不設 limitations 專節是常態")
TBL(d, ["我方弱點", "包裝式", "落筆要領"], [
    ["f=0.25 縮尺", "A1 假設前置＋A4 趨勢級", "方法節前置宣告 trend-level＋標定敘事；引 ⟦B:(Barla et al., 2012)⟧ average-response 免責框"],
    ["100m 擺幅 vs 實測 30m", "A2 scope＋needs-based", "寫成「極端補注情境」適用域；引 ⟦B:(Tarifard et al., 2022)⟧ 營運期水位回升需求式"],
    ["單案例", "A6 稀缺反轉", "n=1 翻成十年複合監測鏈之資料價值（⟦B:(Chiu et al., 2017)⟧ 同招）"],
    ["素混凝土 BPM", "A2＋A3", "適用域=無筋/低配筋襯砌；配筋 BPM 入 future work 1:1 鏡像"],
    ["現地型態差異", "A9 誠實限定框", "對照層級=分區與帶狀分佈；地震/施工縫分量歸因外部化；⟦R:圖2⟧⟦R:圖11⟧ 同座標讓讀者自檢"],
    ["K0=0.7", "A1 引文護盾", "⟦G:表2⟧ 出處欄＋一句敏感度；202411 顧問審查回覆佐證"],
])
P(d, "紅線（反面教材）：①「自己說重要、自己不做」的水矛盾（⟦B:(Wang et al., 2023)⟧ 被我們"
     "當把柄的錯不可自犯）②路線圖承諾違約③方法缺口當主缺口會被問 so what④讓步句不展開、"
     "一行帶過即反轉。", point="簡化必須與前言主張自洽")

H(d, "四、文書規則（本檔示範中）", 2)
P(d, "①每段末【重點：…】黃底黑字；②引用一律 author-year 藍字如 ⟦B:(Chiu et al., 2017)⟧；"
     "③⟦R:圖XX⟧ 紅字；④⟦G:表XX⟧ 綠字；⑤圖領句起段（「⟦R:圖X⟧ 為…」）；⑥量化用倍率/區間；"
     "⑦段落 150–350 字一段一事；⑧綜合前述句收節。", point="與 IJRMMS 前作文書慣例完全對齊")
save(d, "05_寫作工藝手冊.docx")

print("CH00 v2 BUILT")
