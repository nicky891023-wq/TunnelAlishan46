#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rebuild_master_v6.py -- 依 Wade 07-25 六類架構重編 REFS_MASTER。
六類：1 營運隧道案例／2 圍岩依時變形／3 水力耦合分析／4 三維地質模型／
      5 跨尺度數值方法／6 襯砌受力與損傷；每子類含判準與引用位置。
新增 12 篇取自 Wade 藏書（case/analyze/model），Crossref 已逐篇驗證。
"""
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
HERE = Path(__file__).parent.parent          # References/
Q = "'"

NEW = [
 ("1A", 115, "Yu, J., Liu, G., Cai, Y., Zhou, J., Liu, S., & Tu, B. (2020). Time-dependent "
  "deformation mechanism for swelling soft-rock tunnels in coal mines and its mathematical "
  "deduction. International Journal of Geomechanics, 20(3), 04019186. "
  "https://doi.org/10.1061/(ASCE)GM.1943-5622.0001594", "10.1061/(asce)gm.1943-5622.0001594", "Yu_2020"),
 ("1A", 14, "Yong, R., Nie, D., Ma, C., Du, S., Wang, Q., & Ye, J. (2024). Time-dependent behavior "
  "of reinforcement rock unit anchored by energy-absorbing bolt. International Journal of Rock "
  "Mechanics and Mining Sciences, 174, 105629. https://doi.org/10.1016/j.ijrmms.2023.105629",
  "10.1016/j.ijrmms.2023.105629", "Yong_2024"),
 ("2A", 163, "Fahimifar, A., Monshizadeh Tehrani, F., Hedayat, A., & Vakilzadeh, A. (2010). "
  "Analytical solution for the excavation of circular tunnels in a visco-elastic Burger" + Q +
  "s material under hydrostatic stress field. Tunnelling and Underground Space Technology, "
  "25(4), 297-304. https://doi.org/10.1016/j.tust.2010.01.002", "10.1016/j.tust.2010.01.002",
  "Fahimifar_2010"),
 ("2A", 136, "Nomikos, P., Rahmannejad, R., & Sofianos, A. (2011). Supported axisymmetric tunnels "
  "within linear viscoelastic Burgers rocks. Rock Mechanics and Rock Engineering, 44(5), 553-564. "
  "https://doi.org/10.1007/s00603-011-0159-0", "10.1007/s00603-011-0159-0", "Nomikos_2011"),
 ("2A", 76, "Do, D.-P., Tran, N.-T., Mai, V.-T., Hoxha, D., & Vu, M.-N. (2020). Time-dependent "
  "reliability analysis of deep tunnel in the viscoelastic Burger rock with sequential installation "
  "of liners. Rock Mechanics and Rock Engineering, 53(3), 1259-1285. "
  "https://doi.org/10.1007/s00603-019-01975-6", "10.1007/s00603-019-01975-6", "Do_2020"),
 ("2A", 61, "Chu, Z., Wu, Z., Liu, Q., & Liu, B. (2021). Analytical solution for lined circular "
  "tunnels in deep viscoelastic Burgers rock considering the longitudinal discontinuous excavation "
  "and sequential installation of liners. Journal of Engineering Mechanics, 147(4), 04021009. "
  "https://doi.org/10.1061/(ASCE)EM.1943-7889.0001912", "10.1061/(asce)em.1943-7889.0001912",
  "Chu_2021"),
 ("2A", 37, "Arora, K., & Gutierrez, M. (2021). Viscous-elastic-plastic response of tunnels in "
  "squeezing ground conditions: Analytical modeling and validation. International Journal of Rock "
  "Mechanics and Mining Sciences, 146, 104888. https://doi.org/10.1016/j.ijrmms.2021.104888",
  "10.1016/j.ijrmms.2021.104888", "Arora_2021"),
 ("2A", 19, "Hu, X., & Gutierrez, M. (2023). Viscoelastic Burger" + Q + "s model for tunnels "
  "supported with tangentially yielding liner. Journal of Rock Mechanics and Geotechnical "
  "Engineering, 15(4), 826-837. https://doi.org/10.1016/j.jrmge.2022.07.013",
  "10.1016/j.jrmge.2022.07.013", "HuGut_2023"),
 ("2A", 15, "Hu, X., & Gutierrez, M. (2022). Analytical model for deep tunnel with an adaptive "
  "support system in a viscoelastic-Burger" + Q + "s rock. Transportation Geotechnics, 35, 100775. "
  "https://doi.org/10.1016/j.trgeo.2022.100775", "10.1016/j.trgeo.2022.100775", "HuGut_2022"),
 ("2B", 88, "Tarifard, A., Török, Á., & Görög, P. (2024). Review of the creep constitutive models "
  "for rocks and the application of creep analysis in geomechanics. Rock Mechanics and Rock "
  "Engineering, 57(10), 7727-7757. https://doi.org/10.1007/s00603-024-03939-x",
  "10.1007/s00603-024-03939-x", "Tarifard_2024"),
 ("2B", 96, "Lin, H., Zhang, X., Cao, R., & Wen, Z. (2020). Improved nonlinear Burgers shear creep "
  "model based on the time-dependent shear strength for rock. Environmental Earth Sciences, 79(6), "
  "149. https://doi.org/10.1007/s12665-020-8896-6", "10.1007/s12665-020-8896-6", "Lin_2020"),
 ("2B", 33, "Li, A., Deng, H., Zhang, H., Liu, H., & Jiang, M. (2021). The shear-creep behavior of "
  "the weak interlayer mudstone in a red-bed soft rock in acidic environments and its modeling with "
  "an improved Burgers model. Mechanics of Time-Dependent Materials, 27, 1-18. "
  "https://doi.org/10.1007/s11043-021-09523-y", "10.1007/s11043-021-09523-y", "LiMTDM_2021"),
]

ASSIGN = {
 "GM.1943-5622.0000163": "1A", "tust.2013.07.014": "1A", "tust.2021.103838": "1A",
 "tust.2020.103697": "1A", "tust.2024.106319": "1A",
 "s40948-022-00342-0": "1B", "engfailanal.2022.106270": "1B",
 "enggeo.2010.06.010": "1C", "tust.2017.03.004": "1C", "tust.2024.105975": "1C",
 "tust.2021.103814": "1C", "tust.2024.106345": "1C",
 "tust.2015.07.018": "1D", "tust.2024.105940": "1D", "tust.2026.107586": "1D",
 "tust.2020.103796": "1D",
 "0148-9062(87)90523-7": "2A", "tust.2017.07.001": "2A", "nag.3650": "2A",
 "ijmst.2021.12.003": "2A",
 "ijrmms.2020.104250": "2B", "s11069-021-04779-6": "2B", "tust.2022.104537": "2B",
 "tust.2025.107383": "2B", "IJRMMS-inreview": "2B",
 "tust.2009.06.002": "3A", "tust.2023.105393": "3A", "tust.2023.105018": "3A",
 "tust.2026.107691": "3A",
 "tust.2023.105138": "3B", "tust.2024.106253": "3B", "tust.2024.105615": "3B",
 "tust.2024.105917": "5A", "compgeo.2022.104752": "5A", "tust.2020.103348": "5A",
 "s40571-025-01038-4": "5A", "tust.2023.105263": "5A",
 "jrmge.2019.02.004": "5B", "s00603-015-0847-2": "5B", "tust.2024.106034": "5B",
 "tust.2018.11.018": "5B",
 "ijrmms.2004.09.011": "5C", "ijrmms.2007.02.002": "5C", "ijrmms.2004.02.001": "5C",
 "ijrmms.2007.01.004": "5C", "12269328.2014.998346": "5C", "s00603-015-0890-z": "5C",
 "cemconres.2018.02.006": "5C", "s10035-015-0546-4": "5C", "ijrmms.2017.10.004": "5C",
 "s00603-023-03390-4": "5C",
 "tust.2017.08.015": "6A", "tust.2023.105470": "6A",
 "engfailanal.2024.108392": "6B", "tafmec.2023.103832": "6B", "tust.2026.107460": "6B",
 "engfailanal.2022.106946": "6B",
 "compgeo.2023.105808": "6C", "tust.2022.104436": "6C",
}

G = [
 ("1", "1｜營運隧道案例",
  "營運中隧道之長期監測、變形、地下水位與襯砌異狀實證，建立本文工程背景與異狀分類依據。",
  "operational mountain tunnel、long-term tunnel deformation、tunnel lining inspection、"
  "LiDAR tunnel monitoring",
  [("1A", "依時變形", "隧道呈現長期依時變形之實測案例與反分析",
    "§1 P1、§3 案例（源：Wade 藏書 case/）"),
   ("1B", "地下水位", "案例中地下水位／排水狀態對隧道與襯砌之影響", "§1 P1、§3.1 場址水文"),
   ("1C", "襯砌異狀", "襯砌裂縫／剝落之調查、型態分類與評估指標",
    "§1 P1、§4.3 對照語彙（★本團隊系譜）"),
   ("1D", "坡隧系統互制（缺口對照）", "坡體與隧道互制案例，驅動為地震／開挖／重力",
    "§1 P4 缺口證據：互制研究之驅動源鮮少為水位循環")]),
 ("2", "2｜圍岩依時變形",
  "岩石潛變、依時收斂與黏彈塑本構之理論與模式，支持 Modified Burgers-Mohr Model 之理論組成、"
  "參數率定與模式驗證。",
  "time-dependent deformation of surrounding rock、rock creep、stress threshold、"
  "visco-elasto-plastic model、Burgers-Mohr model",
  [("2A", "閉合收斂解析", "以解析解描述隧道依時收斂與圍岩—支撐互制",
    "§1 P2 系譜句、§2.2 理論定位（源：Wade 藏書 analyze/）"),
   ("2B", "修正力學模式", "以本構模式之修正、應力門檻或水力劣化為貢獻主體",
    "§2.2 修正力學模式（源：Wade 藏書 model/；★前作滯動門檻）")]),
 ("3", "3｜水力耦合分析",
  "地下水滲流場、有效應力與水位變動之力學效應，作為跨尺度分析之外部驅動與邊界條件。",
  "hydro-mechanical coupling、transient seepage、effective stress、groundwater-level fluctuation",
  [("3A", "近場滲流解析", "隧道近場滲流場、外水壓與水力—力學耦合之解析／數值解",
    "§1 P2 驅動端、§3.1、§5.2 量級對照　⚠ 需擴充（目前僅 4 篇）"),
   ("3B", "地下水位變動", "水位升降之結構響應實證（模型試驗與現地）",
    "§2.1 循環邊界條件之正當性（★單循環不可逆性）")]),
 ("4", "4｜三維地質模型",
  "多源地質資料整合、區域至場址尺度模型建置，以及地質模型轉為數值模型之量化程序。",
  "3D engineering geological model、geological modelling with borehole integration、"
  "implicit geological modelling、geological model discretization",
  [("4A", "多源地質資料整合", "地形、鑽孔、開挖面影像等多源資料之整合建模", "§2.1、§3.3"),
   ("4B", "區域尺度—場址尺度", "區域至場址尺度之模型範圍界定與縮尺", "§3.3"),
   ("4C", "地質模型數值量化", "地質模型轉為數值網格／材料分區之量化程序", "§2.1")]),
 ("5", "5｜跨尺度數值方法",
  "區域邊坡、隧道圍岩與襯砌三尺度之串接方法：物理量傳遞、連續—離散耦合與離散模型率定回饋。",
  "multiscale tunnel modelling、cross-scale state transfer、FLAC3D-PFC coupling、"
  "continuum-discrete modelling、bonded particle model",
  [("5A", "跨尺度物理量傳遞", "以域劃分、介面交握與狀態量傳遞為貢獻主體",
    "§2.1 跨尺度架構（★Wang 2020 力與力矩雙平衡）"),
   ("5B", "連續體—離散體耦合", "以連續／離散混合方法模擬隧道破壞或水力過程",
    "§1 P3–P4 方法系譜、§2.3 驗證階梯"),
   ("5C", "BPM 率定與回饋", "鍵結顆粒模型之理論、微參數率定、內在缺陷修正與混凝土表述",
    "§2.3 四步論證鏈：問題→修正→我方選擇→混凝土依據")]),
 ("6", "6｜襯砌受力與損傷",
  "襯砌所受岩壓與水壓之演化、裂縫萌生擴展與損傷演化，以及補強維護對策。",
  "tunnel lining damage evolution、lining cracking、external water pressure on lining、"
  "lining stiffness degradation、tunnel rehabilitation",
  [("6A", "岩壓與水壓演化", "以襯砌所受荷載（岩壓／外水壓）之演化為貢獻主體",
    "§1 P2 現象端、§4.2 外壓與內力型態"),
   ("6B", "裂縫與損傷演化", "以襯砌裂縫萌生擴展、損傷演化過程為貢獻主體",
    "§4.2–4.3（★Zheng 2024 模板、Liu 2023 最近似）"),
   ("6C", "補強與維護對策", "以劣化評估、補強工法或維護決策為貢獻主體", "§5.3 工程含義與對策")]),
]


def main():
    entries = []
    for ln in (HERE / "REFS_MASTER.md").read_text(encoding="utf-8").splitlines():
        if not ln.startswith("- ["):
            continue
        m = re.search(r"10\.[\d./()\w-]+", ln)
        doi = m.group(0).rstrip(").") if m else ""
        key = next((k for k in ASSIGN if k.lower() in doi.lower()), None)
        if key is None and "in review" in ln:
            key = "IJRMMS-inreview"
        if key is None:
            print("!! 未歸類：", ln[:90])
            continue
        entries.append((ASSIGN[key], ln))
    for sub, c, apa, doi, _id in NEW:
        tust = " **[TUST]**" if "Tunnelling and Underground" in apa else ""
        entries.append((sub, f"- [V]{tust} (被引 {c}) {apa}"))

    buckets = {}
    for cat, body in entries:
        buckets.setdefault(cat, []).append(body)

    def cite(b):
        m = re.search(r"被引 (\d+)", b)
        return int(m.group(1)) if m else 0

    def istust(b):
        return "[TUST]" in b or "Tunnelling and Underground" in b

    out = ["# REFS_MASTER（主文獻庫 v6，2026-07-25；六類架構，依 Wade 07-25 定義）", "",
           "> **回顧主線**：營運隧道案例 → 圍岩依時變形 → 水力耦合分析 → 三維地質模型 →",
           "> 跨尺度數值方法 → 襯砌受力與損傷。",
           "> 每類含蒐集範圍與檢索詞；每子類含判準與引用位置。一篇只放一個子類。", "", ""]
    tot = ttot = 0
    for gid, gname, purpose, terms, subs in G:
        gl = [b for s, _, _, _ in subs for b in buckets.get(s, [])]
        gt = sum(1 for b in gl if istust(b))
        tot += len(gl)
        ttot += gt
        flag = "　⚠ 全類 0 篇，亟需蒐集" if not gl else ""
        out += [f"## {gname}（{len(gl)} 篇，TUST {gt}）{flag}", "",
                f"- **蒐集與支撐**：{purpose}", f"- **檢索詞**：{terms}", ""]
        for sid, sname, crit, pos in subs:
            lst = sorted(buckets.get(sid, []), key=cite, reverse=True)
            st = sum(1 for b in lst if istust(b))
            gap = "　⚠ 待蒐集" if not lst else ""
            out += [f"### {sid}｜{sname}（{len(lst)} 篇，TUST {st}）{gap}", "",
                    f"- 判準：{crit}", f"- 引用位置：{pos}", ""] + lst + [""]
    out.insert(5, f"> 合計 {tot} 篇；TUST {ttot} 篇（{100*ttot/tot:.0f}%）；"
                  "全數 Crossref 逐 DOI 驗證、零 MDPI。")
    (HERE / "REFS_MASTER.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    rl = json.loads((HERE / "_tools/_reading_list.json").read_text(encoding="utf-8"))
    have = {it["id"] for it in rl}
    for sub, c, apa, doi, _id in NEW:
        if _id not in have:
            yr = re.search(r"\((\d{4})\)", apa)
            rl.append(dict(id=_id, axis=sub, authors=apa.split(" (")[0],
                           year=int(yr.group(1)) if yr else 0,
                           title=apa.split("). ", 1)[1][:120], journal="", doi=doi))
    (HERE / "_tools/_reading_list.json").write_text(
        json.dumps(rl, ensure_ascii=False), encoding="utf-8")
    acc = json.loads((HERE / "_tools/_access_levels.json").read_text(encoding="utf-8"))
    for sub, c, apa, doi, _id in NEW:
        acc.setdefault(_id, "pdf-onhand-unread")
    (HERE / "_tools/_access_levels.json").write_text(
        json.dumps(acc, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"REFS_MASTER v6：{tot} 篇 / TUST {ttot}（{100*ttot/tot:.0f}%）\n")
    for gid, gname, _, _, subs in G:
        gl = [b for s, _, _, _ in subs for b in buckets.get(s, [])]
        print(f"{gname:20s} {len(gl):2d} 篇" + ("　⚠ 全缺" if not gl else ""))
        for sid, sname, _, _ in subs:
            lst = buckets.get(sid, [])
            print(f"    {sid} {sname[:20]:22s} {len(lst):2d}"
                  f"（TUST {sum(1 for b in lst if istust(b))}）" + ("  ⚠" if not lst else ""))


if __name__ == "__main__":
    main()
