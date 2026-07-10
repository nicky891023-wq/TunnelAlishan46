#!/bin/bash
# closeout_chain2.sh -- 收尾鏈 v2（census 已完成；lg -> sm -> figs）
CS="C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe"
D04="C:/Users/Wade/Desktop/Tunnel_TX/04_InitialBalance/process/couple_solve"
D05="C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process"
ST="$D05/closeout_chain.status"
log(){ echo "[$(date '+%m-%d %H:%M:%S')] $*" >> "$ST"; }
waitm(){ local f="$1" m="$2" tmin="$3" i=0
  while [ $i -lt $((tmin*2)) ]; do
    grep -q "$m" "$f" 2>/dev/null && return 0
    grep -qE "Illegal geometry|\*\*\* An error|cannot use" "$f" 2>/dev/null && { log "FAIL-marker in $f"; return 1; }
    sleep 30; i=$((i+1))
  done; log "TIMEOUT waiting $m in $f"; return 1; }
log "chain v2 start: 1b large field export"
sleep 65
cd "$D05" && rm -f export_fields_lg_11.log
"$CS" export_fields_lg_11.f3dat < /dev/null > explg_stdout.txt 2>&1 &
waitm "$D05/export_fields_lg_11.log" "EXPF-DONE lg" 180 || { log "ABORT at lg export"; exit 1; }
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
