#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_s1_reruns.py -- generate stage-1-only rerun scripts from the staged originals
(Wade 07-10: s1 threshold raise; later stages keep existing saves).
Usage: python gen_s1_reruns.py <T1>
Creates large_s1_rerun.f3dat + small_s1_rerun.f3dat (head of the staged file verbatim,
crp_threshold overridden AFTER the parameter call, stage-1 block + save + quit).
"""
import sys
from pathlib import Path

T1 = sys.argv[1] if len(sys.argv) > 1 else "0.95"
HERE = Path(__file__).parent

def gen(src, dst, log, stage1_lines, done_tag):
    s = (HERE / src).read_text(encoding="utf-8", errors="ignore")
    lines = s.split("\n")
    # head = everything before the first stage-1 invocation
    cut = next(i for i, l in enumerate(lines) if l.strip().startswith("[crp_stage(1,"))
    head = lines[:cut]
    out = []
    for l in head:
        if "program log-file" in l:
            out.append(f"program log-file '{log}'")
            continue
        out.append(l)
        if "parameter.f3dat" in l and "call" in l:
            out.append(f"[global crp_threshold = {T1}]   ; S1 RERUN OVERRIDE (Wade 07-10)")
            out.append(f"[io.out('S1RERUN threshold override T={T1}')]")
    out += stage1_lines
    out += [f"[io.out('{done_tag} T1={T1}')]", "program log off", "program quit", ""]
    (HERE / dst).write_text("\n".join(out), encoding="utf-8")
    print("generated", dst, f"(head {cut} lines, T1={T1})")

gen("large_staged.f3dat", "large_s1_rerun.f3dat", "large_s1_rerun.log",
    ["[crp_stage(1,'W-110',30.0)]",
     "[export_box_disp('lg_disp_s01.txt')]",
     "model save '../output/lgs_01'"],
    "LG-S1-RERUN-DONE")

gen("small_staged_v2.f3dat", "small_s1_rerun.f3dat", "small_s1_rerun.log",
    ["[crp_stage(1,'W-110','lg_disp_resid_s01.txt',30.0)]",
     "model save '../output/ss_01'"],
    "SM-S1-RERUN-DONE")
