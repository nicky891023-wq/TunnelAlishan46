#!/bin/bash
# closeout_chain.sh -- HANDOFF_CURRENT.md STEP 1 自走鏈（Fable 07-08）
CS="C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe"
D04="C:/Users/Wade/Desktop/Tunnel_TX/04_InitialBalance/process/couple_solve"
D05="C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process"
ST="$D05/closeout_chain.status"
log(){ echo "[$(date '+%m-%d %H:%M:%S')] $*" >> "$ST"; }
waitm(){ local f="$1" m="$2" tmin="$3" i=0
  while [ $i -lt $((tmin*2)) ]; do
    grep -q "$m" "$f" 2>/dev/null && return 0
    grep -qE "Illegal geometry|\*\*\* An error" "$f" 2>/dev/null && { log "FAIL-marker in $f"; return 1; }
    sleep 30; i=$((i+1))
  done; log "TIMEOUT waiting $m in $f"; return 1; }

log "chain start; waiting for staged console to exit"
for i in $(seq 1 40); do
  n=$(powershell -NoProfile -Command "(Get-Process flac3d600_console -ErrorAction SilentlyContinue | Measure-Object).Count")
  [ "$n" = "0" ] && break; sleep 30
done
log "console clear; 1a bond census"
sleep 65
cd "$D04" && rm -f bond_census_G4.log
"$CS" bond_census_G4.f3dat < /dev/null > census_stdout.txt 2>&1 &
waitm "$D04/bond_census_G4.log" "CENSUS-DONE" 40 || { log "ABORT at census"; exit 1; }
log "census OK; 1b large field export"
sleep 65
cd "$D05" && rm -f export_fields_lg_11.log
"$CS" export_fields_lg_11.f3dat < /dev/null > explg_stdout.txt 2>&1 &
waitm "$D05/export_fields_lg_11.log" "EXPF-DONE lg" 150 || { log "ABORT at lg export"; exit 1; }
log "lg OK; 1c small field export"
sleep 65
rm -f export_fields_sm_11.log
"$CS" export_fields_sm_11.f3dat < /dev/null > expsm_stdout.txt 2>&1 &
waitm "$D05/export_fields_sm_11.log" "EXPF-DONE sm" 240 || { log "ABORT at sm export"; exit 1; }
log "sm OK; 1d figures"
sleep 10
cp "$D04/bond_census_G4.txt" "$D05/" 2>>"$ST"
cd "$D05" && python make_result_figs.py >> "$ST" 2>&1
log "ALL-DONE closeout chain complete -> 05/result/"
