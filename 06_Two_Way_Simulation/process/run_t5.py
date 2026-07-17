#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_t5.py -- 06 two-way T5 orchestrator (26 five-day ticks, staggered exchange).

Wade 07-12 directive: small/coupled two-way only (large model reused from 05 v6);
exchange every 5 days; forward = small boundary displacement -> coupled drive
(Kabsch residual x f=0.25 cumulative targets); feedback = coupled lining damage
D(s,y) -> small shell E = E0*(1-D) (>= 2.5 GPa), the mechanical realization of
"lining deformation -> rock reaction".

SOLAR §10 compliance: unique log per console run, atomic manifest
(planned->running->produced->committed), fail-closed (any gate red => chain stops,
report to Wade -- 鐵則: the runner monitors and reports, Wade decides).

Console iron rules built in: single console; >=65 s license gap; launch cwd =
06/process with bare filename; validate via the script's OWN log marker; power
plan must be never-sleep (external).

Usage (from 06/process):
    python run_t5.py smoke        # small-side unit tests (registry + identity E write)
    python run_t5.py stage0       # coupled stage-0 rebuild (REBAND+CONTROL-0+registry)
    python run_t5.py ticks [N]    # run ticks 1..N (default 26); resumes from manifest
    python run_t5.py status       # manifest summary
"""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(r"C:/Users/Wade/Desktop/Tunnel_TX")
P06 = ROOT / "06_Two_Way_Simulation" / "process"
OUT = ROOT / "06_Two_Way_Simulation" / "output" / "t5"
CONSOLE = r"C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe"
PY = sys.executable
GAP = 65
LG = "../../05_One_Way_Simulation/process/"

STAGES = {
    1: ("W-110", "lg_disp_resid_s01.txt", 30.0), 2: ("W-90", "lg_disp_resid_s02.txt", 5.0),
    3: ("W-70", "lg_disp_resid_s03.txt", 5.0),   4: ("W-50", "lg_disp_resid_s04.txt", 5.0),
    5: ("W-30", "lg_disp_resid_s05.txt", 5.0),   6: ("W-10", "lg_disp_resid_s06.txt", 30.0),
    7: ("W-30", "lg_disp_resid_s07.txt", 5.0),   8: ("W-50", "lg_disp_resid_s08.txt", 5.0),
    9: ("W-70", "lg_disp_resid_s09.txt", 5.0),   10: ("W-90", "lg_disp_resid_s10.txt", 5.0),
    11: ("W-110", "lg_disp_resid_s11.txt", 30.0),
}
STAGE_OF_TICK = [1, 1, 1, 1, 1, 1, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 7, 8, 9, 10,
                 11, 11, 11, 11, 11, 11]
PROLOGUE = {1, 7, 8, 9, 10, 11, 17, 18, 19, 20, 21}
KEEP_SAVES = {1, 6, 10, 11, 16, 20, 21, 26}      # + t00 (never touched) + latest 2
CRACK_INC_STOP = 30000                            # v6 in-flight rule (shatter guard)


def ts():
    return time.strftime("%m-%d %H:%M:%S")


def say(msg):
    print(f"[{ts()}] {msg}", flush=True)


# ------------------------------ manifest ------------------------------
MANIFEST = OUT / "manifest.json"


def mload():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"meta": {}, "stage0": {}, "ticks": {}}


def msave(m):
    tmp = MANIFEST.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(m, indent=1, ensure_ascii=False), encoding="utf-8")
    tmp.replace(MANIFEST)


# ------------------------------ console runner ------------------------------
def flac_alive():
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq flac3d600_console.exe", "/FO", "CSV"],
                       capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if "flac3d600_console" in l]
    if not lines:
        return None
    parts = lines[0].split('","')
    return parts[4].strip('" ') if len(parts) > 4 else "?"


def last_interesting(txt):
    for ln in reversed(txt.splitlines()):
        if any(k in ln for k in ("SS06-HIST", "CS-CHK", "SS06-EAPPLY", "SSv2-stg",
                                 "CS-REBAND", "CS-CONTROL0", "CEB-BND", "CS-read",
                                 "SS06-SHELLREG", "CS06-REGDUMP")):
            return ln.strip()
    return "(no marker line yet)"


def run_console(bare, log_name, marker, timeout_h, stale_min=60):
    """stale_min: kill only if the log stops growing for this long. The PFC coupled
    model runs quiet cycle blocks up to ~70 min (3000 cyc @ ~1.35 s/cyc) with NO log
    flush -- 45 min killed a healthy stage-0 on 07-14. Small-model runs print HIST
    every 1.25-day chunk, so 60 min is generous there."""
    log = P06 / log_name
    if log.exists():
        log.unlink()
    say(f"LAUNCH {bare}  (wait {GAP}s license gap; marker '{marker}'; "
        f"timeout {timeout_h}h; stale-kill {stale_min}min)")
    time.sleep(GAP)
    proc = subprocess.Popen([CONSOLE, bare], cwd=str(P06), stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    t0 = time.time()
    last_hb = t0
    last_size = -1
    last_change = t0
    while time.time() - t0 < timeout_h * 3600:
        txt = log.read_text(errors="ignore") if log.exists() else ""
        if marker in txt:
            try:
                proc.wait(timeout=900)
            except subprocess.TimeoutExpired:
                proc.kill()
            say(f"DONE {bare} in {(time.time()-t0)/60:.1f} min")
            return True, txt
        if "*** An error" in txt or "Illegal geometry" in txt:
            proc.kill()
            say(f"FAIL {bare}: FLAC error in log")
            return False, txt
        if len(txt) != last_size:
            last_size = len(txt)
            last_change = time.time()
        elif time.time() - last_change > stale_min * 60:
            proc.kill()
            say(f"FAIL {bare}: log stale >{stale_min} min (hung console?)")
            return False, txt
        if proc.poll() is not None:
            time.sleep(10)
            txt = log.read_text(errors="ignore") if log.exists() else ""
            ok = marker in txt
            say(f"{'DONE' if ok else 'FAIL'} {bare}: console exited "
                f"({'marker found' if ok else 'no marker'})")
            return ok, txt
        if time.time() - last_hb > 600:
            last_hb = time.time()
            say(f"HB {bare} {(time.time()-t0)/60:.0f}min log={last_size/1024:.0f}kB "
                f"mem={flac_alive()} | {last_interesting(txt)}")
        time.sleep(20)
    proc.kill()
    say(f"FAIL {bare}: timeout {timeout_h}h")
    return False, txt


def run_py(args):
    r = subprocess.run([PY] + args, cwd=str(P06), capture_output=True, text=True)
    out = (r.stdout or "") + (r.stderr or "")
    for ln in out.strip().splitlines():
        say(f"  py> {ln}")
    return r.returncode == 0, out


def maybe_done(log_name, marker, sav):
    """Mid-tick resume: if a previous attempt's OWN log has the end marker and the
    save exists, reuse that run instead of re-launching the console (a tick that
    failed at the coupled/python stage must not redo its finished small stage)."""
    log = P06 / log_name
    if log.exists() and sav.exists():
        txt = log.read_text(errors="ignore")
        if marker in txt:
            return txt
    return None


# ------------------------------ script generators ------------------------------
def gen_small(t):
    s = STAGE_OF_TICK[t - 1]
    wt, drv, days = STAGES[s]
    pro = t in PROLOGUE
    L = [f"; ss06_t{t:02d}.f3dat -- GENERATED by run_t5.py "
         f"(tick {t}/26, stage {s}, {'PROLOGUE' if pro else 'mid-stage'}, wt={wt})",
         f"program log-file 'ss06_t{t:02d}.log'",
         "program log on"]
    if t == 1:
        L.append("model restore '../../04_InitialBalance/output/Small_Initial'")
    else:
        L.append(f"model restore '../output/t5/ss06_t{t-1:02d}'")
    L.append("call '../../04_InitialBalance/parameter.f3dat'")
    if s == 1:
        L.append("[global crp_threshold = 1.00]   ; s1 baseline threshold T=1.0 (07-11 ruling)")
    L.append("call 'C:/Program Files/Itasca/Flac3d600/datafiles/Creep/SetKStrains.f3fis'")
    if t == 1:
        L.append("model configure creep")
    L += ["model largestrain off",
          "fish automatic-create on",
          f"[global cum_days = {5.0*(t-1):.2f}]",
          "[global abort_flag = 0]",
          "call 'ss06_kernel.f3dat'",
          "call 'exp06_body.f3dat'"]
    if t == 1:
        L.append("call 'ss06_t1_init.f3dat'")
    if t >= 2:
        L.append(f"[apply_shellE('shellE_t{t-1:02d}.txt')]   ; D->E feedback (5-day lag)")
    if pro:
        L.append(f"[crp_prologue({s},'{wt}','{LG}{drv}',{days})]")
    L += [f"[crp_tick({s}, 5.0)]",
          f"[exp_bnd('cpl_bnd_t{t:02d}.txt')]",
          f"[exp_wall('cpl_wall_t{t:02d}.txt')]",
          f"model save '../output/t5/ss06_t{t:02d}'",
          f"[io.out('SS06-TICK-DONE t{t:02d} cum='+string(cum_days))]",
          "program log off",
          "program quit"]
    (P06 / f"ss06_t{t:02d}.f3dat").write_text("\n".join(L) + "\n", encoding="utf-8")


def gen_coupled(t):
    prev = "cs06_t00" if t == 1 else f"cs06_t{t-1:02d}"
    L = [f"; cs06_t{t:02d}.f3dat -- GENERATED by run_t5.py (tick {t}/26, parent {prev})",
         f"program log-file 'cs06_t{t:02d}.log'",
         "program log on",
         "program load module 'pfc'",
         "program load module 'wallzone'",
         f"model restore '../output/t5/{prev}'",
         "model largestrain on",
         "model mechanical timestep scale",
         "fish automatic-create on",
         "call 'track_reattach.fis'",
         "call 'couple_qa_v2.fis'",
         "call 'cs06_kernel.f3dat'",
         f"[cs_stage({t},'cpl_resid_t{t:02d}.txt')]",
         f"model save '../output/t5/cs06_t{t:02d}'",
         f"[io.out('CS06-TICK-DONE t{t:02d}')]",
         "program log off",
         "program quit"]
    (P06 / f"cs06_t{t:02d}.f3dat").write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------ gates ------------------------------
def gate_small(t, txt, m):
    g = {"ok": True, "why": []}
    hist = re.findall(r"SS06-HIST stg=(\d+) day=([\d.]+) vclose=([-\d.eE+]+) "
                      r"hclose=([-\d.eE+]+) dmax=([-\d.eE+]+) active=(\d+)", txt)
    if not hist:
        g["ok"] = False
        g["why"].append("no SS06-HIST lines")
        return g
    day = float(hist[-1][1])
    g.update(day=day, vclose=float(hist[-1][2]), hclose=float(hist[-1][3]),
             dmax=float(hist[-1][4]), active=int(hist[-1][5]))
    if abs(day - 5.0 * t) > 1e-3:
        g["ok"] = False
        g["why"].append(f"creep clock {day} != {5.0*t}")
    # NOTE all gate patterns must NOT match the FISH-definition echo lines
    # ("Def>  io.out('SS06-ABORT...')") that FLAC prints when call'ing the kernel --
    # match the EXECUTED output (line start / digits), never bare substrings.
    if re.search(r"^SS06-ABORT", txt, re.M):
        g["ok"] = False
        g["why"].append("kinematic abort in small model")
    if g["dmax"] > 0.2:
        g["ok"] = False
        g["why"].append(f"dmax {g['dmax']}")
    mb = re.search(rf"CEB-BND cpl_bnd_t{t:02d}\.txt n=(\d+)", txt)
    if not mb or int(mb.group(1)) < 9000:
        g["ok"] = False
        g["why"].append("boundary export missing/short")
    else:
        g["bnd_n"] = int(mb.group(1))
    if t >= 2:
        me = re.search(r"SS06-EAPPLY \S+ n_ewrite=(\d+) n_echange=(\d+)", txt)
        nshell = m["meta"].get("nshell", 0)
        if not me or int(me.group(1)) != nshell:
            g["ok"] = False
            g["why"].append(f"shell E writes {me.group(1) if me else 'none'} != {nshell}")
        else:
            g["ewrite"], g["echange"] = int(me.group(1)), int(me.group(2))
    if t in PROLOGUE:
        if not re.search(r"creep start: active=\d+", txt):
            g["ok"] = False
            g["why"].append("prologue did not reach creep start")
    return g


def gate_coupled(t, txt, m):
    g = {"ok": True, "why": []}
    mc = re.search(rf"CS-CHK stg{t} cracks_t=(\d+) cracks_s=(\d+) "
                   r"ball_dmax=([-\d.eE+]+) gp_dmax=([-\d.eE+]+)", txt)
    if not re.search(r"^CS06-TRACK-REATTACH ok", txt, re.M):
        g["ok"] = False
        g["why"].append("crack callback NOT re-attached (silent undercount risk)")
    if not mc:
        g["ok"] = False
        g["why"].append("no CS-CHK line")
        return g
    cum = int(mc.group(1)) + int(mc.group(2))
    g.update(cracks_t=int(mc.group(1)), cracks_s=int(mc.group(2)), cracks_cum=cum,
             ball_dmax=float(mc.group(3)), gp_dmax=float(mc.group(4)))
    prev_cum = (m["stage0"].get("control0_cracks", 0) if t == 1
                else m["ticks"][f"{t-1:02d}"]["coupled"]["cracks_cum"])
    inc = cum - prev_cum
    g["cracks_inc"] = inc
    if inc < 0:
        g["ok"] = False
        g["why"].append(f"crack count decreased ({inc}) -- DFN lost through restore?")
    if inc >= CRACK_INC_STOP:
        g["ok"] = False
        g["why"].append(f"crack increment {inc} >= {CRACK_INC_STOP} (v6 shatter rule; "
                        "Wade decides on DRIVE_SCALE)")
    if not (1e-7 < g["gp_dmax"] < 0.05):
        g["ok"] = False
        g["why"].append(f"gp_dmax {g['gp_dmax']} outside (1e-7, 0.05) -- frozen rock "
                        "or runaway")
    # ball.disp is CUMULATIVE from the stage-0 datum; v6-accepted trajectory reached
    # 0.069 by s3 and plateaued at 0.074 by s11 (spalled-ball drift into the cavity,
    # Wade-approved). Gate at 2x the v6 ceiling to catch genuine shatter only.
    if g["ball_dmax"] > 0.15:
        g["ok"] = False
        g["why"].append(f"ball_dmax {g['ball_dmax']} > 0.15 (2x v6 ceiling 0.074)")
    return g


# ------------------------------ phases ------------------------------
def smoke():
    m = mload()
    a = ["; ss06_smoke_a.f3dat -- GENERATED: registry + export smoke (read-only)",
         "program log-file 'ss06_smoke_a.log'",
         "program log on",
         "model restore '../../04_InitialBalance/output/Small_Initial'",
         "call '../../04_InitialBalance/parameter.f3dat'",
         "fish automatic-create on",
         "call 'ss06_kernel.f3dat'",
         "call 'exp06_body.f3dat'",
         "[exp_shellreg('shell_registry.txt')]",
         "[exp_bnd('cpl_bnd_smoke.txt')]",
         "[io.out('SS06-SMOKEA-DONE')]",
         "program log off",
         "program quit"]
    (P06 / "ss06_smoke_a.f3dat").write_text("\n".join(a) + "\n", encoding="utf-8")
    ok, txt = run_console("ss06_smoke_a.f3dat", "ss06_smoke_a.log", "SS06-SMOKEA-DONE", 1.5)
    mr = re.search(r"SS06-SHELLREG \S+ n=(\d+)", txt)
    mb = re.search(r"CEB-BND cpl_bnd_smoke\.txt n=(\d+)", txt)
    if not (ok and mr and int(mr.group(1)) > 0 and mb and int(mb.group(1)) >= 9000):
        say("SMOKE-A FAILED -- inspect ss06_smoke_a.log (struct.pos intrinsic? kernel load?)")
        return False
    nshell, bnd_n = int(mr.group(1)), int(mb.group(1))
    say(f"SMOKE-A OK nshell={nshell} bnd_n={bnd_n}")

    ok, out = run_py(["make_shellE.py", "--identity"])
    if not ok:
        return False

    b = ["; ss06_smoke_b.f3dat -- GENERATED: identity shell-E write + stability check",
         "program log-file 'ss06_smoke_b.log'",
         "program log on",
         "model restore '../../04_InitialBalance/output/Small_Initial'",
         "call '../../04_InitialBalance/parameter.f3dat'",
         "fish automatic-create on",
         "call 'ss06_kernel.f3dat'",
         "[apply_shellE('shellE_identity.txt')]",
         "model cycle 50",
         "[io.out('SS06-SMOKEB dmax='+string(dmax_all))]",
         "[io.out('SS06-SMOKEB-DONE')]",
         "program log off",
         "program quit"]
    (P06 / "ss06_smoke_b.f3dat").write_text("\n".join(b) + "\n", encoding="utf-8")
    ok, txt = run_console("ss06_smoke_b.f3dat", "ss06_smoke_b.log", "SS06-SMOKEB-DONE", 1.5)
    me = re.search(r"SS06-EAPPLY \S+ n_ewrite=(\d+) n_echange=(\d+)", txt)
    md = re.search(r"SS06-SMOKEB dmax=([-\d.eE+]+)", txt)
    if not (ok and me and md):
        say("SMOKE-B FAILED -- inspect ss06_smoke_b.log")
        return False
    ew, ec, dm = int(me.group(1)), int(me.group(2)), float(md.group(1))
    if ew != nshell or ec != 0 or dm > 1e-3:
        say(f"SMOKE-B GATE FAIL: n_ewrite={ew}/{nshell} n_echange={ec} (want 0) dmax={dm}")
        return False
    say(f"SMOKE-B OK identity write {ew}/{nshell}, zero changes, dmax={dm:.2e}")
    m["meta"].update(nshell=nshell, smoke_bnd_n=bnd_n, smoke_done=ts())
    msave(m)
    return True


def stage0():
    m = mload()
    resume = (OUT / "cs06_reband.f3sav").exists() and not (OUT / "cs06_t00.f3sav").exists()
    if resume:
        say("STAGE0 resume mode: cs06_reband.f3sav found -- skipping the anneal")
        ok, txt = run_console("cs06_stage0b_resume.f3dat", "cs06_stage0b.log",
                              "CS06-STAGE0-DONE", 6.0, stale_min=150)
    else:
        # v6 calibration: conditioning+CONTROL-0 ~3-4 h @ ~1.35 s/cyc; quiet <=70 min
        ok, txt = run_console("cs06_stage0.f3dat", "cs06_stage0.log", "CS06-STAGE0-DONE",
                              12.0, stale_min=150)
    if not ok:
        say("STAGE0 FAILED -- inspect the stage0 log; DO NOT proceed (report Wade)")
        return False
    g = {}
    ma = re.search(r"CS-REBAND-A anchored\(new band\)=(\d+)", txt)
    mq = re.search(r"CS-REBAND-QUIET ball_dmax over 1500cyc = ([-\d.eE+]+)", txt)
    if resume and not ma:          # anneal evidence lives in the earlier log
        old = P06 / "cs06_stage0.log"
        if old.exists():
            ot = old.read_text(errors="ignore")
            ma = re.search(r"CS-REBAND-A anchored\(new band\)=(\d+)", ot)
            mq = mq or re.search(r"CS-REBAND-QUIET ball_dmax over 1500cyc = ([-\d.eE+]+)", ot)
    mg = re.search(r"CS-CONTROL0 GATE: cracks=(\d+) .*ball_drift=([-\d.eE+]+)", txt)
    mrg = re.search(r"CS06-REGDUMP \S+ breakable=(\d+) anchored=(\d+)", txt)
    if not (mg and mrg) or (not ma and not resume):
        say("STAGE0 FAIL: missing gate lines (REBAND-A / CONTROL0 / REGDUMP)")
        return False
    g["resume"] = resume
    g["anchored_band"] = int(ma.group(1)) if ma else None
    g["quiet_dmax"] = float(mq.group(1)) if mq else None
    g["control0_cracks"] = int(mg.group(1))
    g["control0_drift"] = float(mg.group(2))
    g["reg_breakable"] = int(mrg.group(1))
    g["reg_anchored"] = int(mrg.group(2))
    sav = OUT / "cs06_t00.f3sav"
    if not sav.exists() or sav.stat().st_size < 3e9:
        say("STAGE0 FAIL: cs06_t00.f3sav missing/short")
        return False
    hard_fail = []
    if g["control0_cracks"] > 200:
        hard_fail.append(f"control0 cracks {g['control0_cracks']} > 200")
    if g["control0_drift"] > 0.01:
        hard_fail.append(f"control0 drift {g['control0_drift']} > 0.01")
    if not (1.6e6 < g["reg_breakable"] < 2.4e6):
        hard_fail.append(f"registry breakable {g['reg_breakable']} outside 1.6M-2.4M")
    g["hard_fail"] = hard_fail
    m["stage0"] = {"state": "failed" if hard_fail else "committed", "ts": ts(), **g}
    msave(m)
    for fn in ("cs_control0_cracks.txt", "cs06_t00_pmap.txt", "cs06_t00_cwall.txt",
               "cpl_bond_registry.txt"):
        if (P06 / fn).exists():
            shutil.copy2(P06 / fn, OUT / fn)
    if hard_fail:
        say("STAGE0 HARD FAIL: " + "; ".join(hard_fail) + " -- STOP, report Wade")
        return False
    say(f"STAGE0 COMMITTED: anchored={g['anchored_band']} quiet={g['quiet_dmax']} "
        f"control0={g['control0_cracks']}cr/{g['control0_drift']:.4f}m "
        f"(v6 baseline 28cr/0.0031m) registry={g['reg_breakable']} breakable")
    return True


def do_tick(t, m):
    key = f"{t:02d}"
    if m["ticks"].get(key, {}).get("state") == "committed":
        say(f"tick {key} already committed -- skip")
        return True
    stage = STAGE_OF_TICK[t - 1]
    say(f"=== TICK {key}/26 (stage {stage}{', PROLOGUE' if t in PROLOGUE else ''}) ===")
    m["ticks"][key] = {"state": "running", "stage": stage, "start": ts()}
    msave(m)

    # -- 1. small model: 5 days creep (+ prologue) + boundary export --
    txt = maybe_done(f"ss06_t{key}.log", f"SS06-TICK-DONE t{key}",
                     OUT / f"ss06_t{key}.f3sav")
    if txt is not None:
        say(f"tick {key} small stage already done (log marker + save verified) -- reuse")
        ok = True
    else:
        gen_small(t)
        ok, txt = run_console(f"ss06_t{key}.f3dat", f"ss06_t{key}.log",
                              f"SS06-TICK-DONE t{key}", 4.0)
    g1 = gate_small(t, txt, m) if ok else {"ok": False, "why": ["no marker"]}
    m["ticks"][key]["small"] = g1
    msave(m)
    if not g1["ok"]:
        m["ticks"][key]["state"] = "failed_small"
        msave(m)
        say(f"TICK {key} SMALL FAIL: {g1['why']} -- CHAIN STOPPED (report Wade)")
        return False

    # -- 2. Kabsch rigid removal + strain gate --
    ok, out = run_py(["make_cpl_resid06.py", key])
    mres = re.search(r"RESID06-OK t\d+ n=(\d+).*resid_max=([\d.]+)mm.*gate=([\deE.+-]+)",
                     out)
    m["ticks"][key]["resid"] = {"ok": ok, "line": out.strip().splitlines()[-1] if out else ""}
    msave(m)
    if not ok or not mres:
        m["ticks"][key]["state"] = "failed_resid"
        msave(m)
        say(f"TICK {key} RESID FAIL -- CHAIN STOPPED")
        return False

    # -- 3. coupled model: drive to cumulative targets --
    txt2 = maybe_done(f"cs06_t{key}.log", f"CS06-TICK-DONE t{key}",
                      OUT / f"cs06_t{key}.f3sav")
    if txt2 is not None:
        say(f"tick {key} coupled stage already done (log marker + save verified) -- reuse")
        ok = True
    else:
        gen_coupled(t)
        # v6 calibration: coupled stage recipe ~1.5-1.8 h; settle quiet <=55 min
        ok, txt2 = run_console(f"cs06_t{key}.f3dat", f"cs06_t{key}.log",
                               f"CS06-TICK-DONE t{key}", 5.0, stale_min=120)
    g2 = gate_coupled(t, txt2, m) if ok else {"ok": False, "why": ["no marker"]}
    m["ticks"][key]["coupled"] = g2
    msave(m)
    if not g2["ok"]:
        m["ticks"][key]["state"] = "failed_coupled"
        msave(m)
        say(f"TICK {key} COUPLED FAIL: {g2['why']} -- CHAIN STOPPED (report Wade)")
        return False

    # -- 4. damage map + shell E table (feedback for tick t+1) --
    ok, out = run_py(["make_damage_map_v2.py", str(t)])
    if not ok:
        m["ticks"][key]["state"] = "failed_damage"
        msave(m)
        say(f"TICK {key} DAMAGE-MAP FAIL -- CHAIN STOPPED")
        return False
    m["ticks"][key]["damage"] = out.strip().splitlines()[-1]
    ok, out = run_py(["make_shellE.py", str(t)])
    if not ok:
        m["ticks"][key]["state"] = "failed_shellE"
        msave(m)
        say(f"TICK {key} SHELL-E FAIL -- CHAIN STOPPED")
        return False
    m["ticks"][key]["shellE"] = out.strip().splitlines()[-1]

    # -- 5. artifacts -> output/t5, retention, commit --
    arts = [f"cpl_bnd_t{key}.txt", f"cpl_resid_t{key}.txt", f"cpl_wall_t{key}.txt",
            f"dmg_map_t{key}.txt", f"shellE_t{key}.txt"]
    for fn in arts:
        if (P06 / fn).exists():
            shutil.copy2(P06 / fn, OUT / fn)
    for p in P06.glob(f"cs_s{t}_*.txt"):
        shutil.copy2(p, OUT / p.name.replace(f"cs_s{t}_", f"cs06_t{key}_"))
    k = t - 2
    if k >= 1 and k not in KEEP_SAVES:
        for fn in (f"ss06_t{k:02d}.f3sav", f"cs06_t{k:02d}.f3sav"):
            f = OUT / fn
            if f.exists():
                f.unlink()
                say(f"retention: deleted {fn} (regenerable; keep-set {sorted(KEEP_SAVES)})")
    m["ticks"][key]["state"] = "committed"
    m["ticks"][key]["end"] = ts()
    msave(m)
    say(f"TICK {key} COMMITTED: day={g1['day']:.1f} vclose={g1['vclose']:.3f}mm "
        f"active={g1['active']} | cracks_cum={g2['cracks_cum']} (+{g2['cracks_inc']}) "
        f"gp_dmax={g2['gp_dmax']:.2e} | {m['ticks'][key]['damage']}")
    return True


def status():
    m = mload()
    say(f"meta: {m['meta']}")
    s0 = m.get("stage0", {})
    say(f"stage0: {s0.get('state', 'not run')} control0={s0.get('control0_cracks')}cr "
        f"registry={s0.get('reg_breakable')}")
    for key in sorted(m["ticks"]):
        e = m["ticks"][key]
        c = e.get("coupled", {})
        say(f"t{key}: {e['state']:14s} stage{e['stage']:2d} "
            f"cracks={c.get('cracks_cum', '-')}(+{c.get('cracks_inc', '-')}) "
            f"{e.get('damage', '')}")


def main():
    if not Path(CONSOLE).exists():
        say(f"FATAL: console not found at {CONSOLE}")
        return 1
    cmd = sys.argv[1] if len(sys.argv) > 1 else "ticks"
    if cmd == "smoke":
        return 0 if smoke() else 1
    if cmd == "stage0":
        return 0 if stage0() else 1
    if cmd == "status":
        status()
        return 0
    if cmd == "ticks":
        upto = int(sys.argv[2]) if len(sys.argv) > 2 else 26
        m = mload()
        if "nshell" not in m["meta"]:
            say("FATAL: run 'smoke' first (need nshell + registry)")
            return 1
        if m.get("stage0", {}).get("state") != "committed":
            say("FATAL: stage0 not committed")
            return 1
        for t in range(1, upto + 1):
            m = mload()
            if not do_tick(t, m):
                say(f"CHAIN STOPPED at tick {t} -- see manifest + logs; Wade decides")
                return 1
        say(f"CHAIN OK through tick {upto} " +
            ("-- T5 26-tick two-way chain COMPLETE" if upto == 26 else "(partial run)"))
        return 0
    say(f"unknown command {cmd}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
