I have all the concrete data I need. The large model's box-boundary faces accumulate ~250-450 mm of displacement with a box differential of ~3-142 mm — this is what drives the small box. I now have the full verified recipe grounded in current Tunnel_TX geometry. Here is the synthesis.

---

# Alishan #46 Three-Scale Workflow — Recipe for Tunnel_TX (verified against current geometry)

This is the prior 260529 workflow re-expressed on the **current Tunnel_TX files** (`04_InitialBalance` = the three init balances; `05_One_Way_Simulation` = large->small staged drive; `03_CoupleModel` + `06_Two_Way_Simulation` = lining coupling). Current geometry differs from 260529 — coordinates and parameters below are the CURRENT ones, taken from the actual files.

Key current-geometry constants (from `04_InitialBalance/parameter.f3dat`):
- Large box: x∈[0,2000], y∈[−100,2000], z floor 800. K0=0.7, ν=0.25, per-layer E (L1 colluvium 0.5→L4 basement 7.0 GPa).
- Small box: **x∈[1250,1350], y∈[850,950], z∈[1700,1800]** (100³ m), 6 layers (L4 = WET sandshale, E=1.5 GPa, c=100 kPa, φ=30° — the weak driver).
- Coupled box: **x∈[1277,1317], y∈[860,910], z∈[1728,1768]** (40×50×40 m), PFC bonded lining.
- Creep: Burgers-Mohr, η_m=6.0e15, η_k=2.4e13 Pa·s, threshold ratio 0.6, fixed Δt=600 s.
- Water staging = **4 stages LOW–HIGH–LOW–HIGH, 30 days each (120 d)**; LOW plane z=1724, HIGH plane z=1807 (small); STL terrain-following planes (large).

---

## PART 1 — THE THREE INITIAL FORCE-BALANCE STATES (verify these FIRST)

All three: `model gravity 0 0 -9.81`, `nu=0.25`, **`model solve elastic`** (Wade rule — never let MC/creep settle the initial state, avoids spurious plastic zones / force-control divergence), compression negative, SI.

### 1A. LARGE init — `04_InitialBalance/run_large_init.f3dat` -> `Large_Initial.f3sav`
- **Material:** 4-layer Mohr-Coulomb, per-layer E/c/φ, `tension [ten_r]=1e5`.
- **Stress init:** `zone initialize-stresses ratio [K0]` with K0=0.7 (gravity + lateral ratio).
- **BCs (roller box + fixed floor):**
```
zone gridpoint fix velocity-x range position-x -1 1
zone gridpoint fix velocity-x range position-x 1999 2001
zone gridpoint fix velocity-y range position-y -101 -99
zone gridpoint fix velocity-y range position-y 1999 2001
zone gridpoint fix velocity   range position-z 799 801    ; floor fully fixed; top free
```
- **Solve:** `model solve elastic ratio-local 1e-3`. Top surface free.
- **Datum:** displacement NOT zeroed here (zeroing happens at stage-1 of the creep run). The init save is the in-situ datum.
- **Exports for next scale:** near-field zone stress x∈[1150,1450] y∈[750,1050] z∈[1600,1900] -> `large_stress_for_small.dat` (the IDW source).

**VERIFY (deliver to engineer):**
1. **Stress field:** `_stress_report` prints `szz[min,max]`. Check szz monotonic with depth, ≈ −ρgh (e.g. 2600·9.81·H), and σh/σv ≈ K0=0.7. CHK2 (after-init) vs CHK2 (after-solve) should be close (elastic solve only relaxes mesh discretization, not the field).
2. **Equilibrium:** `model solve elastic ratio-local 1e-3` actually REACHED 1e-3 (not cycle-capped). Report final unbalanced ratio.
3. **Plastic zone:** because MC + `solve elastic`, expect ZERO yielded zones — confirm `zone.state` plastic count = 0 (any yield at init means K0/strength mismatch).
4. **Velocity field:** post-solve max gp velocity ≈ 0 (quasi-static).
5. **BC check:** confirm the 5 fixed-face gp counts are nonzero and symmetric; top free.
6. **Export sanity:** `large_stress_for_small.dat` row count >0 and covers the small box footprint.

### 1B. SMALL init — `04_InitialBalance/run_small_init.f3dat` -> `Small_Initial.f3sav`
- **Material:** 6-layer MC rock (`slot 'mat'='rock'`, `slot 'type'='layer1..6'`) + **elastic lining continuum** (D7: E=25 GPa, ν=0.2) wished-in-place sharing rock nodes (conformal — no attach, no t=0 interface jump).
- **Stress init = SUBMODELING:** read parent stress, IDW-map onto ALL zones (rock+lining):
```
[ReadFile_ss('large_stress_coarse.dat')]
[MapStress_IDW(40.0)]        ; 1/d^2 weight, radius 40 m, coarse-subsampled parent field
```
- **BCs:** all 6 box faces fully fixed (submodel held at parent state — conformal Route C, full-face fix is safe):
```
zone gridpoint fix velocity range position-x 1249 1251 / 1349 1351
zone gridpoint fix velocity range position-y 849 851  / 949 951
zone gridpoint fix velocity range position-z 1699 1701 / 1799 1801
```
- **Solve:** `model solve elastic ratio-local 1e-3 cycles 8000` (cycle-guard so interface imbalance can't run unbounded).
- **Export:** focus-region (x[1268,1306] y[855,915] z[1738,1758]) rock stress -> `small_stress_for_coupled.dat`.

**VERIFY:**
1. **Stress continuity:** mapped szz at small box should match `Large_Initial` szz at the same coords (IDW fidelity) — compare `_srep` before-solve (just-mapped) vs after-solve; the elastic solve should barely move it (Δszz small) → confirms the mapped field was already near-equilibrium.
2. **Interface (lining↔rock):** because lining is wished-in-place at the same in-situ stress, the t=0 internal force jump across the lining/rock interface ≈ 0. Verify lining zones carry the same σ as adjacent rock.
3. **Plastic zone = 0**, max velocity ≈ 0, ratio reached 1e-3 (NOT capped at 8000).
4. **BC check:** 6 faces each have nonzero fixed-gp count.

### 1C. COUPLED init — `04_InitialBalance/couple_solve/` -> `Couple_Initial.f3sav`
(Built by `03_CoupleModel/build_Couple_mb3.f3dat`; init/servo in `couple_solve/couple_servo_v5.f3dat`.)
- **Geometry:** 40×50×40 box x[1277,1317] y[860,910] z[1728,1768]; structured-hex rock (layers 2–6); **PFC bonded lining** (linearpbond, pb_ten=2.1 MPa, pb_coh=23 MPa, see `parameter.f3dat` pfc_* block); `wz_outter` wall-zone coupling (rock↔balls); `w_inner` rigid inner backstop + `w_860/910` end plates. **Zero fixed balls** (lining held by wz_outter outside + w_inner inside).
- **Stress init:** rock IDW-mapped from `small_stress_for_coupled.dat`; lining bonded in place.
- **Solve:** servo to equilibrium (PFC `model solve ratio-average`-style); balls settle into the in-situ rock.

**VERIFY (use `couple_solve/verify_*` + `verify_couple_render.f3dat`):**
1. **wz_outter in-situ contact force** (`verify_wzforce_v5.f3dat` / `wzf_report`): report |Fc| and components — this is the baseline lining confinement (must be a sane MN-scale, not 0, not runaway).
2. **w_inner load** (`couple_recon`): if w_inner carries large net force the ring is being crushed by the backstop — flag it.
3. **Bond inventory:** total bonds, 0 broken at init (`fracture_track.fis` -> crack_num=0).
4. **Ball velocity ≈ 0** after settle; **ball radius range** (for later Ncyc sizing: per-cycle move ≤ 1e-3·r_ball).
5. **Lining stress** (`verify_lining_v5.f3dat`): hoop/radial baseline.
6. Visual: render + Read self-check against trusted `cb_control0` geometry baseline (Wade rule: never break correct geometry).

---

## PART 2 — THE LARGE -> SMALL DRIVE MECHANISM (the heart of the workflow)

There are two coupled facts: **(a)** the large model is run as its own staged slope-creep, exporting a per-stage displacement field; **(b)** that field drives the small box faces as a **velocity BC**, and the tunnel convergence is measured **relative to a tunnel-interior datum** so the curve includes elasto-plastic + creep and does NOT start at 0.

### 2A. Large staged slope-creep — `05_One_Way_Simulation/large_creep_4stage.f3dat` -> `lg_s1..s4.f3sav`
Restore `Large_Initial`, `model configure creep`, assign **Burgers-Mohr** per layer with G_m=G_k=elastic G(E,ν), bulk=K(E,ν), η_m/η_k from parameter — so instantaneous response == static MC (no spurious softening). Per stage:
```
zone water set 'watertable_lower'        ; (or _higher)  -- terrain-following STL plane
model calm
model solve elastic ratio-local 1e-3 cycles 30000     ; WATER STEADY-STATE re-eq (elastic, Wade rule)
[setKstrains]      ; init Kelvin strains from current stress (no inherited strain)
[do_threshold]     ; gate creep ON/OFF per zone
[setKstrains]
zone gridpoint initialize displacement 0 0 0    ; *** ZERO ONCE, stage 1 only -> slope-creep clock start ***
zone gridpoint initialize velocity 0 0 0
model creep active on
model creep timestep fix 600
[run_stage(0,30,10)]                     ; model solve time-total [day*86400]
model creep active off
model save 'lg_s1'
```
Stages 2–4 repeat but **do NOT re-zero displacement** (only velocity) → displacement is **cumulative** across the 4 stages. Threshold + setKstrains re-run after each water change.

### 2B. The threshold gate (identical FISH in large/small/coupled) — corrected MC envelope
```
q_th = 0.6 * ( c*cos(phi) + p'*sin(phi) )      ; p' = (s1+s3)/2 - pore  ;  q = (s1-s3)/2
if q >= q_th -> viscosity-maxwell=eta_m, viscosity-kelvin=eta_k, group 'CreepActive'
else         -> viscosity-*=1e100 (inert),                         group 'CreepOff'
```
**LESSON BAKED IN:** the envelope is `c·cos φ + p'·sin φ` (sin/cos form). The earlier `tan φ` (=/cos) form was ~15.5% too high — do NOT regress. High water → high pore pressure → lower p' → ... but the WET layer's low strength means more zones cross threshold when saturated → creep activates → "high-water creeping" trend. Re-evaluated each stage at equilibrium (and can be put on a callback `interval 100` during a stage for dynamic on/off).

### 2C. The DRIVE BC: large per-stage disp -> small box faces (velocity-controlled IDW)
The large model's box-boundary gridpoints (faces x=1250/1350, y=850/950, z=1700/1800) accumulate displacement each stage. **Verified magnitudes from `lg_s4` (`diag_large_bnd.f3dat`):** face means −282/−248 mm (x), +317/+314 mm (y), −74/−215 mm (z) → **box differential closure ≈ 34 mm (x), 3 mm (y), 142 mm (z)**. That differential is the squeeze fed to the small box.

Mechanism (the proven `ApplyVel_IDW` pattern, current incarnation = `couple_export_bnd` + `couple_drive` for the coupled box; the SAME pattern applies to the small box):
1. **Export** large per-stage gp displacement near the small footprint -> `*_disp.dat` (id x y z ux uy uz), one file per stage.
2. **Identify small box-boundary gps** (the 6 outer faces) → mark group `'driven'`.
3. **Per stage, IDW-interpolate** the large displacement onto each driven gp (1/d² weight, radius ~40–100 m; fallback nearest-neighbour). target = interpolated cumulative disp at that stage.
4. **Velocity = (target − current_disp)/stage_time**, applied + **FIXED** so the solver does not overwrite it:
```
gp.vel(g) = (target_u - gp.disp(g)) / creep_time      ; reach target over the stage
gp.fix velocity range group 'driven'                  ; boundary gps fixed-velocity
; internal gps FREE -> respond to in-situ stress + creep naturally
```
Internal small-model zones run their own threshold-gated Burgers creep; only the 6 faces are kinematically driven by the large model.

### 2D. Datum / zeroing so the convergence curve is NOT zero at start
- After the small init (1B), displacements are at the in-situ datum. At small **stage-1 equilibrium**, displacement is zeroed **once** (`zone gridpoint initialize displacement 0 0 0`) — this defines the deformation clock start AFTER the elasto-plastic excavation response is already in the section.
- **Crucial:** the convergence is reported as a **relative** quantity between fixed datum points inside the tunnel, e.g. (current geometry datum points from `small_4stage_standalone.f3dat`):
```
zone history name 'crown_dz' displacement-z position (1297, 885, 1752)   ; crown
zone history name 'side_dx'  displacement-x position (1303, 885, 1747)   ; springline
```
Crown−invert and springline closure are differences of these → the curve carries the elasto-plastic excavation closure + creep, so it does NOT start flat at 0; each water-HIGH stage adds a creep ramp on top.
- Stages 2–4: zero VELOCITY only, never displacement → cumulative.

### 2E. Per-stage water steady-state + creep (small) — `small_4stage_standalone.f3dat` is the validated template
Each stage: set water plane → `model calm` → `model solve ratio-average 1e-5 cycles 40000` (water/mechanical steady-state) → `setKstrains` → `do_threshold` → `setKstrains` → zero vel → `model creep active on` / `timestep fix 600` / `run_stage` (`model solve time-total [day*86400]`) → save. The standalone uses fixed faces; the **driven** version replaces the fixed faces with the 2C velocity-IDW BC on group `'driven'`.

---

## PART 3 — SMALL -> COUPLED DRIVE (for later; design in `docs/THREAD_C_REBUILD_DESIGN.md`)

- **Transfer quantity:** small-model per-stage cavity displacement with **rigid-body removed** (robust Kabsch best-fit on interior gps, residual = P1 − R·P0 − t, outlier cap ~0.10 m) → `cavdef_<stage>.txt`. Only NET convergence drives the lining, not bulk translation.
- **Apply (current = `couple_drive.f3dat`):** drive ONLY the **outer rock** boundary gps of the coupled box (group `'driven'`, 28304 gps from `couple_bnd_disp.txt`), NEVER the balls (lesson #69 — direct ball displacement-control over-cracks). Lining force-shares through `wz_outter`.
```
zone gridpoint fix velocity range group 'driven'
gp.vel(g) = (gp.extra(g,stage) - gp.disp(g)) / (nsub*ncyc_sub*mech.timestep)   ; ramp to target
model cycle [ncyc_sub] ; model calm        ; sub-step ramp + calm
... then hold vel=0, model solve ratio-average 1e-4 cycles [cap]   ; settle/equilibrate
```
- **Settings:** `model mechanical timestep scale`, `model largestrain on`, `ball attribute damp 0.8`, sub-step ramp so per-cycle wall move ≪ ball radius (avoids tet inversion).
- **Creep/settle alternation** (260529 pattern, for the two-way version): during FLAC creep soften ball-facet (emod 1e3) + fix balls; during settle restore ball-facet (emod 1e10) + free balls + `model solve ratio-average`.
- **Outputs:** crack count/positions per stage (`fracture_track.fis` / dump bond-broken `'linear'` contacts), `wz_outter` reaction force (lining external force), lining internal forces; save `cb_*` per stage. Stages share cracks (no reset between stages).
- **Open items (per design doc):** rock simplified to single equivalent elastic (compliance-matched to reproduce small-model y860-910 local closure); release `w_inner`; minimal anti-drift constraint; pilot small/fast first.

---

## PART 4 — TRENDS THE WORKFLOW PRODUCES (acceptance signatures)

- **LARGE (slope creep, meter-scale):** cumulative dmax reaches **~1.6 m at day 120** (verified `lg_s4`: dmax=1.63 m; box-face disp 250–450 mm). Monotonic accumulation, steeper in HIGH-water stages (more zones cross threshold), near-flat in LOW. This is the regional 邊坡潛移 that supplies the boundary squeeze.
- **SMALL (tunnel squeezing, ~cm-to-10cm scale when driven):** convergence curve has the **flat-onset-flat-onset** shape over LOW–HIGH–LOW–HIGH: nearly flat during LOW (q < threshold, creep off), creep ramp during HIGH (WET layer crosses threshold, creep on). Cumulative closure, NOT starting at 0 (carries excavation elasto-plastic closure). (Note: the FIXED-face standalone `s4` gives only ~4.4 mm because its faces are clamped — the box differential ~34–142 mm from the large model is what produces the 10 cm-scale squeeze once the 2C velocity-IDW drive replaces the fixed faces. This is exactly the large->small coupling step the engineer wants next.)
- **COUPLED (lining):** progressive bond breakage / crack count rising during HIGH-water creep, relative stabilization during LOW; `wz_outter` reaction force rises with water, lining hoop stress concentrates at springline/crown per the closure asymmetry; cracks accumulate across stages (no inter-stage reset). 260529 reference reached thousands of cracks over the cycle.

---

## EXECUTION ORDER (current files)

1. `04_InitialBalance/run_large_init.f3dat` -> verify 1A -> `Large_Initial`
2. `04_InitialBalance/run_small_init.f3dat` -> verify 1B -> `Small_Initial`
3. `04_InitialBalance/couple_solve/couple_servo_v5.f3dat` (+ `verify_*`) -> verify 1C -> `Couple_Initial`
4. `05_One_Way_Simulation/large_creep_4stage.f3dat` -> `lg_s1..s4` (run diag_large_bnd to confirm box differential)
5. Export large per-stage box-face disp; apply 2C velocity-IDW drive to small box faces (extend `small_4stage_standalone.f3dat`: swap fixed faces for group `'driven'` + IDW velocity) -> driven small `s4`
6. (later) small residual `cavdef_*` -> `05/couple_drive.f3dat` / `06_Two_Way_Simulation` lining.

Relevant absolute paths:
- `c:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\parameter.f3dat` (all params)
- `c:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\run_large_init.f3dat`, `run_small_init.f3dat`, `idw_map.f3dat`
- `c:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\large_creep_4stage.f3dat`, `small_4stage_standalone.f3dat`, `diag_large_bnd.f3dat`, `couple_export_bnd.f3dat`, `couple_drive.f3dat`
- `c:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\docs\THREAD_C_REBUILD_DESIGN.md`
- `c:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\couple_solve\couple_servo_v5.f3dat`, `verify_lining_v5.f3dat`, `verify_wzforce_v5.f3dat`

CAVEAT: I did not find a current-geometry file that already wires the large->small velocity-IDW drive on the SMALL box (only the coupled-box version `couple_export_bnd`/`couple_drive` exists; the small run is currently the fixed-face standalone). Building that small-box driven version (step 5) is the concrete next implementation task, following the 2C pattern exactly.