Verdict: **PROCEED WITH CONDITIONS**.

Do **not** run current `couple_drive.f3dat` as-is. The Phase 2 concept is acceptable, but the executable package still needs pre-run fixes/gates.

**Phase 1 Reaction Consensus**
Pick **(c): virtual cut matched to the coupled wall geometry**, which is basically option (a) done correctly.

Use a virtual cylindrical/actual `wz_outter`-matched surface, not the `lining` group. Integrate:

`traction = sigma · n`, with compression-positive radial pressure `p_r = -(sigma · n) · n`

Report:

- signed radial resultant `∫ p_r dA`
- contact-load magnitude proxy `∫ |p_r| dA` or sector sums
- net vector `|∫ traction dA|`
- circumferential and axial sectors

Option (b), mean radial stress times wall area, is only a sanity scalar. It is not enough because the field is anisotropic and net vectors cancel.

The small “lining” structure is **not a build red flag for the small model’s current role** because `run_small_init.f3dat` explicitly defines a wished-in-place, node-sharing elastic continuum lining. But it **is a red flag for interpreting Phase 1 as physical liner reaction**. With 335,011 zones spanning the core/plug volume, no void, no interface, and initial stresses already above nominal shotcrete strength, the small model can provide tunnel displacement/stress fields. It cannot provide a defensible thin-liner force/crack result. That must come from the coupled PFC model.

**Phase 2 Corrections**
The sequence is right:

1. rigid-body residual drive
2. Control-0 zero-increment gate
3. no-damage transfer
4. SMOKE first
5. rigid `w_inner` main case
6. free-inner sensitivity case

But fix these before execution:

- `couple_idw.py` has a rigid-rotation sign bug. Current `b += K @ di` returns `omega` with the wrong sign. Use `b -= K @ di` or solve with `-b`, then regenerate `couple_bnd_disp.txt`.
- The existing `couple_bnd_disp.txt` appears stale/full-field, not verified residual output.
- Print residual displacement/increment stats, not full-field stats.
- Add hard abort if `ndriven != 28304` or `nmiss != 0`.
- Add Control-0 and no-damage branches before damage SMOKE.
- Move `maxbvel` sampling before `model calm`; current log samples after calm.
- Add an actual crack breaker; current script only logs cracks.

**Control-0 Pass Criterion**
Pass only if all are true:

- `ndriven = 28304`, `nmiss = 0`
- zero target produces `Δcrack = 0` new ball-ball bond breaks
- final target/drift error: RMS ≤ `0.01 mm`, max ≤ `0.05 mm`
- `wz_outter` and `w_inner` force drift ≤ `2%`
- pre-calm max ball velocity decreases and ends below 10% of the Stage-1 per-cycle imposed displacement rate
- final ratio does not worsen from `6.1e-3`; clean pass preferred at `≤1e-3`

If Control-0 cracks at all, Stage-1 damage interpretation is blocked.

**Crack Breaker**
For first damage SMOKE, change from `3 × 100` to **`30 × 10` cycles** so the breaker can act early.

Abort/save/inspect if:

- `Δcrack_sub > 50` in any 10-cycle substep
- cumulative Stage-1 cracks exceed `200`
- crack rate accelerates for two consecutive substeps
- cracks localize at end-wall buffers only

If Claude insists on 100-cycle substeps, use `Δcrack_sub > 250`, but I do not approve that for first damage SMOKE.

**w_inner**
Run both:

- rigid `w_inner` = Wade main case, labelled confined/backstop condition
- free-inner = mandatory sensitivity before interpreting crack pattern

If rigid/free crack count, mode, or location differs materially, report the coupled result as a boundary-condition bracket, not a single predicted lining crack pattern.
