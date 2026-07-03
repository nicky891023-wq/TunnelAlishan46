**1. Overall Assessment**

CONDITIONALLY. `WORKFLOW_v1` is a useful scaffold, but it is not yet a sound executable workflow for the full study. I would block production execution until v2 fixes the physics gates, especially the small-model water-cycle interpretation, the threshold-definition mismatch, large-small handoff, coupled reference-frame handling, and the small-vs-coupled lining reaction definition.

**2. Section-By-Section Critique**

1. **Core Objective / Hypothesis**: The stated hypothesis is good, but current results do not yet support it. The small model is dominated by stage 1 LOW: active zones `597909 -> 430462 -> 105 -> 215727`, and displacement is already about `3.93 mm` by day 30. That is not a clean HIGH-water-onset story. The large model also has the largest displacement in stage 1 LOW and active counts decrease through stages. v2 must treat current outputs as provisional, not as hypothesis support.

2. **Three-Scale Architecture**: Small-to-coupled one-way submodeling is scientifically defensible only as a local mechanical transfer test. It is not yet proof of creep-driven cracking because the coupled rock has no internal creep source and only receives six-face displacement BCs. Large-to-small is weaker: [run_small_init.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/04_InitialBalance/run_small_init.f3dat:4) maps initial stress, but the small 4-stage run is not driven by large-model stage displacement or stress increments.

3. **Validated Recipes**: Partly valid, incomplete. The threshold recipe is internally inconsistent: [parameter.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/04_InitialBalance/parameter.f3dat:14) documents `0.6*(c*cos(phi)+p'*sin(phi))`, but large/small scripts implement `0.6*c + 0.6*p'*tan(phi)` at [large_creep_4stage.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/large_creep_4stage.f3dat:48) and [small_4stage_standalone.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/small_4stage_standalone.f3dat:39). Also the small script header says threshold `0.8` while code sets `0.6`.

4. **Water Modeling**: STL water for the large model is a good correction, and the horizontal-plane failure lesson is valid. But both water systems are instantaneous prescribed pore-pressure scenarios, not transient seepage. v2 must explicitly label this as drained/endmember cycling unless fluid diffusion is added.

5. **Stage A**: Claude’s “just re-solve Couple_Initial to 1e-4” is too optimistic. The residual `6.0954e-03` at cycle cap is real. Re-equilibration may itself break bonds or alter wall forces. Create `Couple_Initial_eq` only after Control-0 proves stationary bond state, wall forces, ball velocities, and energy.

6. **Stage B / Large Model**: Completed numerically, but not validated scientifically. `81 cm` large-slope dmax may be plausible or excessive; v2 needs displacement vectors, boundary constraint checks, stress-path plots, active-zone maps by layer, and field plausibility. The current active count trend does not clearly show HIGH water causing more creep.

7. **Stage C / Small Model**: The small model is the critical weak link. The `s1`-dominant displacement and `s3 active=105` can be physical only if explained by stress-path maps. Otherwise it suggests initial creep transient/saturation, not seasonal groundwater cycling. Require LOW-only, HIGH-only, no-creep, and spin-up/baseline controls.

8. **Stage D / Coupled Driver**: Not ready as written. `WORKFLOW_v1` says datum reset and zero-increment control, but [couple_drive.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/couple_drive.f3dat:11) restores and immediately tracks, then runs stage 1 at [couple_drive.f3dat](/C:/Users/Wade/Desktop/Tunnel_TX/05_One_Way_Simulation/couple_drive.f3dat:119). There is no datum reset, no Control-0 branch, no halt guard, no target-error abort, and `maxbvel` is sampled after `model calm`.

9. **Reference Frame**: Major missing gate. Stage 1 boundary motion has about `1.79 mm RMS`, with about `1.02 mm RMS` fitted rigid-body motion. If the outer rock is moved by that absolute field while `w_inner`, `w_860`, and `w_910` stay fixed, parent rigid translation/rotation becomes artificial lining squeeze. v2 must either move all walls with the fitted rigid component or drive only deformational residuals.

10. **E1/E2/E3 Consistency Checks**: Good idea, underdefined. `wz_outter` net force alone is insufficient because contact forces cancel. E1 must compare distributions: normal/shear traction, force magnitude sums, resultants, moments, sectors, and axial slices. E2 must compare full circumferential convergence, not one point. E3 cannot be claimed until large-stage boundary effects are actually transferred or explicitly excluded.

11. **Visual QA**: Direction is good, but needs quantitative gates. Add fixed-scale plots for `q/qth`, pore pressure, effective stress, creep strain increment, boundary target error, IDW nearest distance, rigid/residual displacement, bond utilization, fracture mode, energy, and process-specific convergence.

**3. Verdicts On Section 8 Open Decisions**

1. **Couple_Initial residual**: Use option A only with audit. Do not simply re-solve and trust it. Run baseline bond-state/utilization, Control-0, wall-force drift, pre-calm velocity, kinetic/strain energy, and process-ratio checks. If any bond breaks or forces drift materially, the baseline is not valid.

2. **`w_inner` rigid sensitivity**: Mandatory. Rigid `w_inner` may be kept for a diagnostic case, but not as validation. A free-inner-face or compliant/contact-interface control is required. Also, even rigid walls must follow parent rigid-body motion if absolute parent displacement is used.

3. **`s1`-dominant increments**: Red flag. It may indicate real rapid primary creep, but it currently undermines the seasonal HIGH-water crack narrative. Require LOW-only baseline subtraction, creep spin-up, `q/qth` maps, active-zone maps inside the coupled box, and stage-wise convergence at tunnel wall before cracking interpretation.

4. **Small lining reaction extraction**: Use virtual interface traction integration. Identify outer lining faces adjacent to rock, compute `F = -sigma_lining · n * A` per face with a documented normal direction, decompose into normal/shear, and sum by axial slice and circumferential sector. Compare increments, not only absolute net force, against coupled `wz_outter` contact-force distributions.

**4. Missing Elements**

- Large-to-small stage handoff: displacement/stress increments from `lg_s1..s4` to the small boundary, or an explicit statement that large and small are parallel scenario models.
- Threshold-definition freeze: choose `tan` criterion or MC `sin/cos` criterion, then rerun or sensitivity-check.
- Active-source audit inside the coupled domain: if small-model creep-active zones are inside the coupled box, boundary-only transfer is not enough.
- Rigid-body/residual decomposition and wall-motion handling.
- Small-model interface reaction extractor with sign, unit, length normalization, and equilibrium check.
- Baseline controls: LOW-only, HIGH-only, no-creep, no-water-change, no-damage coupled transfer, rigid-body-only coupled run.
- Mesh and stress-path gates: zone quality, lining thickness, boundary distance, K0 sensitivity, pore-pressure sign, effective-stress sanity.
- Sensitivity/uncertainty: threshold, viscosity, water level, lining stiffness, PFC bond strength, timestep/ramp rate, IDW `k`.
- Field anchoring: groundwater levels, tunnel convergence, crack locations/timing. If unavailable, label the result as scenario analysis, not calibrated prediction.

**5. Prioritized Changes For WORKFLOW_v2**

1. Freeze definitions first: units, sign, threshold equation, water interpretation, datum convention, and acceptance tolerances.
2. Reclassify existing large/small results as provisional until threshold and water-cycle controls pass.
3. Add Stage 0 controls: LOW-only, HIGH-only, no-creep, and creep spin-up or baseline subtraction.
4. Add large-small handoff QA or explicitly narrow the claim to “same-scenario multi-scale,” not true three-scale coupling.
5. Rewrite coupled Stage D: mapping QA, rigid-body correction, datum reset, target-error abort, Control-0, no-damage transfer, then very short stage-1 ramp.
6. Replace `wz_now` as the main E1 metric with full contact-force/traction distributions and moments.
7. Make free/compliant `w_inner` sensitivity mandatory before interpreting crack patterns as field lining damage.
8. Require post-stage review packets with fixed plots plus numeric tables before any long run.

No files were written.
