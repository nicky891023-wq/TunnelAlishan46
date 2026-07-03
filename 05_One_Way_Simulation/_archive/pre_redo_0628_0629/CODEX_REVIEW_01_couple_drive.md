# CODEX REVIEW #01 — couple_drive SMOKE

- Decision: **BLOCKED**
- Scope: review only; no model was run and no existing file was modified.
- Next allowed action: prepare `REVIEW_PACKET_01R_couple_drive.md`. Do **not** start the proposed stage-1 SMOKE yet.

## What passed

1. Driving the coupled model through the outer FLAC rock boundary, rather than directly prescribing PFC-ball motion, is the correct direction for a nested mechanical submodel.
2. `model mechanical timestep scale`, density-scaled quasistatic cycling, damping, and velocity-controlled loading all have FLAC3D/PFC 6 precedents in:
   - `C:\Program Files\Itasca\Flac3d600\datafiles\ExampleApplications\PunchIndentation\PunchIndentation.f3dat`
   - `C:\Program Files\Itasca\Flac3d600\datafiles\ExampleApplications\SleevedTriaxialTest\SleevedTriaxialTest.f3dat`
3. All four `bc_s*.txt` files contain 140,694 rows and have byte-identical coordinate sequences. The production Python assumption that rows correspond between stages therefore passes for these files.
4. `couple_bnd.txt` contains 28,304 unique boundary gridpoints. The six-face split is:
   - xmin/xmax: 3,584 each
   - ymin/ymax: 7,888 each
   - zmin/zmax: 3,248 / 3,024
5. IDW source coverage is finite but relatively coarse:
   - nearest source distance: median 0.865 m, p95 1.809 m, max 3.204 m
   - eighth-neighbour distance: median 2.511 m, p95 3.789 m, max 4.894 m
6. The actual maximum stage-1 imposed movement per ramp cycle is approximately `3.909 mm / 300 = 13.0 µm`, not 6.5 µm. It remains below the proposed `1e-3*rmin = 36 µm` numerical guard.

## Blocking findings

### B1. Control-0 is proposed but not implemented

`couple_drive.f3dat` immediately runs stage 1. There is no independent zero-increment branch.

This is mandatory because `Couple_Initial` was saved at a final ratio-average of about `6.1e-3`, after reaching the 8,000-cycle cap rather than the requested `1e-4`. Changing timestep mode and ball damping from 0.7 to 0.8 may cause additional relaxation and bond breaks without any applied parent displacement.

Required:

1. Restore `Couple_Initial`.
2. Record global intact/tension-broken/shear-broken ball-ball bonds and utilization before cycling.
3. Run the same timestep scaling, damping, calm schedule, cycle count, and terminal solve with zero boundary increment.
4. Record new bond-break events, process-specific convergence, ball velocity before calm, wall/contact load distributions, and displacement drift.
5. Branch stage 1 from the accepted equilibrated control baseline, not from a separately evolving unbalanced state.

Acceptance is not simply “approximately zero cracks.” Any cracks must be spatially and mechanically explained. A stable baseline must also show stationary displacement, contact force, and energy.

### B2. Parent rigid-body motion is being converted into false lining squeeze

The mapped stage-1 boundary field contains a fitted rigid component:

- translation: approximately `(-0.368, +0.001, -0.244) mm`
- rotation: approximately `(-1.69e-5, -4.19e-5, +1.42e-5) rad`
- rigid-component RMS: about 1.025 mm
- total boundary-displacement RMS: about 1.792 mm

The rock boundary is driven by this absolute field while `w_inner`, `w_860`, and `w_910` remain fixed in global space. Harmless parent translation/rotation will therefore become relative rock–wall displacement and can generate artificial compression, shear, and end cracking.

Required: either

- move all rigid PFC walls consistently with the fitted parent rigid-body component while applying the deformational residual to the outer rock boundary; or
- remove the common rigid-body component from the complete parent field before driving, with a documented physical interpretation.

Keeping `w_inner` rigid in shape does not require keeping it fixed against parent rigid-body translation/rotation.

### B3. The two fixed end walls conflict with the dominant driven faces

The y=860 and y=910 faces contain 15,776 of the 28,304 driven gridpoints. The adjacent PFC end walls remain fixed while the rock end faces receive nonzero x/y/z displacement. This can create artificial axial shear and cracks at the model ends.

Required:

- apply the consistent rigid component to `w_860` and `w_910`;
- separately quantify the deformational relative motion at both ends;
- exclude an end-effect buffer from the physical crack interpretation;
- report cracks by axial position, not only total count.

### B4. `maxbvel` is sampled after `model calm`

The official `model calm` definition sets all linear and rotational velocities to zero. In the current loop:

```text
model cycle ...
model calm
io.out(... maxbvel ...)
```

the reported `maxbvel` cannot diagnose the preceding instability.

Required: capture maximum ball velocity and kinetic energy before `model calm`, preferably as solve histories or maxima accumulated during the substep.

### B5. The “crack breaker” does not exist in the script

The packet promises interruption when cracking reaches the thousand level, but the script only checks after a complete 100-cycle substep and never halts. A fracture avalanche could continue through all 100 cycles.

Required:

- implement a verified `fish-halt`/callback stop or use very short checkpointed ramps;
- first increments should be 1–5–20 cycles or equivalent, with a save/check after each;
- define stopping criteria using crack-rate, kinetic energy, ball velocity, and bond-energy release—not an unsupported absolute count alone.

### B6. Baseline bond state and failure margin are not established globally

Existing checks only demonstrated zero broken bonds near y≈885. The driver resets the DFN counter, but that does not restore already broken contacts.

Required before Control-0:

- global ball-ball counts for `pb_state = 0,1,2,3`;
- tensile and shear utilization percentiles and maxima;
- spatial maps of near-critical bonds;
- separation of material ball-ball bonds from wall-zone coupling bonds;
- baseline crack/bond state by axial segment.

### B7. The fracture tracker contains an inherited bounds bug

`fracture_track.fis` assigns:

```text
global zmin = domain.min.z()
global zmin = domain.min.z()
```

`zmax` is never assigned. Correct and parse-test the tracker before relying on fracture relocation. Also ensure the callback is restricted to ball-ball material bonds so a future ball-facet bond event cannot be processed as two balls.

### B8. The parse check did not validate gridpoint mapping

`parse_check2.f3dat` uses `model new`; consequently its own log reports:

```text
driven=0 miss=28304
```

It validated syntax and text parsing only. It did not prove that restored `Couple_Initial` resolves all gridpoint IDs.

Required: in the real driver, abort before cycling unless:

```text
ndriven == 28304
nmiss == 0
```

Also check that all driven gridpoints are on the intended exterior faces and that no wall-zone/cavity gridpoints are accidentally grouped.

### B9. Net wall force is not a valid interface-load measure

The reported 1.88 MN (`wz_outter`) and 1.38 MN (`w_inner`) are net vector resultants. Symmetric or opposing contact forces can cancel, so these values do not demonstrate force-sharing magnitude.

Required outputs:

- sum of contact-force magnitudes;
- normal and shear contact-force distributions;
- resultant force and moment about the tunnel centre;
- circumferential sectors and axial segments;
- boundary work/energy during loading.

Do not use `wz_now` alone as proof that the lining is carrying the transferred load.

### B10. Near-tunnel response has not been validated against the Small model

The coupled rock contains no corresponding water/creep field in this driver. Prescribing only the six outer faces produces the coupled model’s own elastic boundary-value response; it does not automatically reproduce the Small model’s local cavity-wall displacement or effective-stress path.

Before interpreting any PFC fracture:

1. Extract the Small-model rock/lining-interface displacement at locations corresponding to `wz_outter`.
2. Run a no-damage or bonded-elastic coupled transfer check.
3. Compare radial/tangential/axial displacement around the full circumference and along y.
4. Define an acceptance tolerance before viewing the result.

If the cavity response is not reproduced, increasing the driven-band thickness is only one possible remedy; local pore-pressure/creep loading or direct residual-field transfer may be required.

### B11. Current stage-1 input is not a validated groundwater-onset event

The source is the standalone Small run:

- stage 1 LOW already has 597,909 creep-active zones;
- the global maximum displacement is not tunnel convergence;
- Large-model displacement is not propagated into this Small run;
- stage increments are dominated by LOW stage 1.

The proposed SMOKE may be used only as a software/integration loading test. It cannot be described as validation of the study’s groundwater-rise → creep → cracking mechanism.

### B12. The statement “PFC balls are not in ratio-average” is incorrect

Previous coupled logs show `model solve ratio-average` reporting mechanical Zone, Ball, Clump, and Structure processes. Report process-specific ratios and termination reason. Reaching a cycle cap is not convergence.

## `w_inner` ruling

For a diagnostic SMOKE, `w_inner` may remain geometrically rigid only under all of these conditions:

1. it receives the same parent rigid-body motion as the surrounding submodel reference frame;
2. its relative confinement is explicitly labelled an artificial inner backstop;
3. crack results are not interpreted as field-predicted lining cracks;
4. a later free-inner-face or compliant/contact-interface sensitivity case is mandatory.

There is currently no defensible universal “reasonable crack count versus shatter” threshold. Classification must use crack-rate, spatial localization, fragment formation, energy release, and comparison with Control-0.

## Required pre-run Visual QA

Submit before the revised SMOKE:

1. all six driven faces coloured by stage-1 `dx`, `dy`, `dz`, magnitude, and nearest-source distance;
2. edge/corner continuity and IDW sensitivity (`k=4,8,16` or another justified comparison);
3. parent source versus mapped target profiles at y=860, 885, and 910;
4. rigid-body versus deformational displacement decomposition;
5. driven boundary, `wz_outter`, `w_inner`, `w_860`, and `w_910` in one geometry plot;
6. baseline bond-utilization and bond-state maps.

## Revised execution sequence required

1. Mapping/geometry QA without model cycling.
2. Baseline global bond and convergence audit.
3. Independent Control-0 from `Couple_Initial`.
4. Review Control-0 results.
5. Create/identify an accepted equilibrated baseline.
6. Very-short stage-1 ramp with implemented halt guards.
7. Review mechanics and Visual QA before any 1,500-cycle terminal solve.

## Resubmission

Claude should create `REVIEW_PACKET_01R_couple_drive.md` that answers B1–B12 with exact file/line references and proposed stop thresholds. The current `couple_drive.f3dat` is not approved for execution.
