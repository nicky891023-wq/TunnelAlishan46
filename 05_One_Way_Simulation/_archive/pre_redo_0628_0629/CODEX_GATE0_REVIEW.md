GATE-0: PASS WITH CONDITIONS

1. GEOMETRY: PASS. The y=885 dumps are valid thin slices: small `x=1250-1350, z=1700-1800`, large `x≈0-1983, z≈811-1966`. Small active zones are physically centered on layer 4 plus tunnel-adjacent EDZ. Large zones are shallow/slope-surface dominated but span layers 2-4, so do not describe large as a single layer-4 mechanism.

2. STRESS PATH / MECHANISM: PASS. Source FISH now uses `q_th = 0.6*(c*cos(phi)+p'*sin(phi))`, with FLAC3D compressive-negative stresses flipped to positive. Dump checks show `s1 >= s3`, positive `p'`, positive `q_th`; no sign/unit red flag. Water rise lowers `p'` and increases active threshold exceedance. Important caveat: final dump `q/qth` is post-creep stress state, while `creep=1` is the saved pre-creep gate flag; do not expect exact one-to-one matching in plots.

3. DEFORMATION LOCATION: PASS WITH CONDITION. Small deformation is mm-scale and tunnel/weak-band localized, but the plotted/global `dmax` is not always exactly at the lining. Phase 1 must extract lining/crown/side reactions from tunnel-wall or lining reference points, not use global `dmax` as “tunnel convergence.” Large max displacement is shallow slope motion, m-scale, consistent with the stated over-driven regional scenario.

4. FAILURE / ACTIVE ZONE: PASS WITH CONDITION. Small layer 4 dominance is physically plausible for wet weak sandshale at `c=100 kPa`, but it is also a sensitivity flag: full-model layer 4 is nearly fully active early, then strongly modulated by drainage/stress history. Report it as “threshold-sensitive weak-layer creep,” not as a calibrated failure prediction. Run threshold/cohesion sensitivity before any design-level claim.

5. LARGE OVER-DRIVING: PASS WITH CONDITION. I agree large can proceed only as a clearly labeled non-calibrated regional-context/endmember scenario. It must not be used as a quantitative field-rate prediction. If Phase 2 applies large-model displacement/stress output as calibrated boundary forcing, then recalibrate or scale `eta/threshold` first; otherwise proceed with explicit “endmember” labeling.

6. SMALL MODEL READINESS: PASS. The small model is sound enough for Phase 1 lining-reaction extraction and Phase 2 coupled-drive setup, subject to item 3: tunnel-specific metrics must be extracted directly, and large-model forcing must be treated per item 5.

7. VISUAL-QA CAVEATS: CONDITIONS BEFORE PHASE 1/2: fix audit labels/comments in HIGH-only/LOW-only scripts/log summaries so stage labels match actual water planes; add a note/table that `creep` flags are pre-creep threshold gates while `q/qth` fields are post-stage dumps. DEFER: interpolation/contours, polished stress-path plots, rigid/residual checks, and unbalanced/ratio plots can move to their relevant Phase 1/2 verification packages.
