#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run_twoway.py -- 06 雙向強耦合總指揮（骨架 v1，2026-07-07 Fable）
⚠ 尚不可執行：等 05 完成＋METHOD_TWO_WAY.md §7 checklist 全勾再啟用。

設計要點（console 鐵則全部內建）：
  * 一次只跑一個 FLAC3D console；兩次啟動間隔 >= LICENSE_GAP 秒
  * cd 到腳本所在目錄、傳裸檔名（位置參數不可含斜線）
  * 驗證 = 腳本自身 log 的 marker 行 + 產物檔存在（絕不用 flac3d.log）
  * manifest.json 簿記每一步 → 任何中斷可斷點續跑
  * L1 交錯式為主線；L2 Picard 只對 WET_STAGES 啟用
"""
import json, subprocess, time, shutil
from pathlib import Path

ROOT      = Path(r"C:/Users/Wade/Desktop/Tunnel_TX")
P06       = ROOT / "06_Two_Way_Simulation"
CONSOLE   = r"C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe"
LICENSE_GAP = 65          # 秒，console 接 console 的授權緩衝（鐵則）
N_STAGES  = 11
WET_STAGES = [5, 6, 7]    # L2 Picard 只做濕峰段
MAX_ITER  = 3
OMEGA     = 0.5           # Picard 欠鬆弛
TOL_U     = 0.05          # 洞壁位移收斂判準（相對變化）
TOL_CRACK = 0.10          # 裂縫增量收斂判準

def load_manifest():
    f = P06 / "output" / "manifest.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {"done": []}

def save_manifest(m):
    (P06 / "output" / "manifest.json").write_text(
        json.dumps(m, indent=2, ensure_ascii=False), encoding="utf-8")

def run_console(script_dir: Path, bare_name: str, done_marker: str, log_name: str,
                timeout_h: float = 6.0) -> bool:
    """啟動 console 跑 bare_name，輪詢自身 log 出現 done_marker 或超時。"""
    time.sleep(LICENSE_GAP)
    proc = subprocess.Popen([CONSOLE, bare_name], cwd=str(script_dir),
                            stdin=subprocess.DEVNULL,
                            stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    log = script_dir / log_name
    t0 = time.time()
    while time.time() - t0 < timeout_h * 3600:
        if log.exists():
            txt = log.read_text(errors="ignore")
            if done_marker in txt:
                proc.wait(timeout=300)
                return True
            if "Illegal geometry" in txt or "*** An error" in txt:
                proc.kill()
                return False
        if proc.poll() is not None:          # console 已退出
            txt = log.read_text(errors="ignore") if log.exists() else ""
            return done_marker in txt
        time.sleep(30)
    proc.kill()
    return False

def small_stage(k: int, it: int, dmg_map: Path | None) -> bool:
    """跑小模第 k 階段（殼 E 依 dmg_map 折減；None=未損傷 E0）。TODO: 生成
    small_stage_dmg.f3dat 的參數側檔（stage、restore 名、dmg 檔名），呼叫 console。"""
    raise NotImplementedError("等 05 完成後實作（用 small_staged_v2 單階段化）")

def export_drive(k: int, it: int) -> Path:
    """ss_k' → exp_body 模式匯出 → make_cpl_resid.py → 回傳 cpl_resid 路徑。"""
    raise NotImplementedError

def coupled_stage(k: int, it: int, resid: Path) -> Path:
    """跑耦合模第 k 階段（G4 系配方），回傳 dmg_map 路徑（make_damage_map.py）。"""
    raise NotImplementedError

def relax_damage(prev: Path | None, new: Path, out: Path):
    """D̂ = D̂_prev + OMEGA*(D_new − D̂_prev)，逐扇區。prev=None 時直接複製。"""
    raise NotImplementedError

def converged(k: int, it: int) -> bool:
    """比較迭代 it 與 it-1 的洞壁位移欄位（cwall）與裂縫數：TOL_U / TOL_CRACK。"""
    raise NotImplementedError

def main():
    m = load_manifest()
    dmg_prev: Path | None = None                    # L1: 上一階段的損傷圖
    for k in range(1, N_STAGES + 1):
        iters = MAX_ITER if k in WET_STAGES else 1  # L2 只在濕峰
        dmg_hat = dmg_prev
        for it in range(1, iters + 1):
            tag = f"s{k:02d}_i{it}"
            if tag in m["done"]:
                continue                            # 斷點續跑
            assert small_stage(k, it, dmg_hat), f"small stage {tag} failed"
            resid = export_drive(k, it)
            dmg_new = coupled_stage(k, it, resid)
            out = P06 / "output" / f"dmg_hat_{tag}.txt"
            relax_damage(dmg_hat, dmg_new, out)
            dmg_hat = out
            m["done"].append(tag); save_manifest(m)
            if it > 1 and converged(k, it):
                break
        dmg_prev = dmg_hat                          # 餵給下一階段（L1 滯後）
    print("TWOWAY-DONE")

if __name__ == "__main__":
    main()
