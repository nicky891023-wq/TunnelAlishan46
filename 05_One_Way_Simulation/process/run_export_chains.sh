#!/bin/bash
# run_export_chains.sh -- sequence the 3 FLAC3D export chains (single console, 90s license buffer)
cd "C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/process"
FLAC="C:/Program Files/Itasca/FLAC3D600/exe64/flac3d600_console.exe"
echo "[runner] LG chain start $(date +%H:%M:%S)"
"$FLAC" lg_chain.f3dat
echo "[runner] LG chain exit=$? $(date +%H:%M:%S)"
sleep 90
echo "[runner] SM chain start $(date +%H:%M:%S)"
"$FLAC" sm_chain.f3dat
echo "[runner] SM chain exit=$? $(date +%H:%M:%S)"
sleep 90
echo "[runner] CP chain start $(date +%H:%M:%S)"
"$FLAC" cp_chain.f3dat
echo "[runner] CP chain exit=$? $(date +%H:%M:%S)"
echo "[runner] ALL-CHAINS-DONE"
