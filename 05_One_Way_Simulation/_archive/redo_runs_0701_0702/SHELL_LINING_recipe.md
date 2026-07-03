I now have everything needed. I have the full picture: the actual project geometry, parameters, the proven threshold/creep recipe used in Tunnel_TX, the lining-softening experiments (which proved that load-controlled lining stress requires yielding, not just stiffness reduction), and Wade's source E-reduction pattern from Failure.f3dat / WadeCreepSupport.f3dat. Let me produce the precise implementation recipe.

# Alishan #46 SMALL Model — Shell-Lining + Threshold-Gated Burgers Creep + E-Reduction-on-Yield: Implementation Recipe

This synthesizes Wade's proven `Wade_TD_SCI` patterns (Failure.f3dat, WadeCreepSupport.f3dat, Chapter4/TYPE3A) with the *already-validated* Tunnel_TX small-model recipe (`small_4stage_standalone.f3dat`, `parameter.f3dat`, `prototype_small_creep.f3dat`, the two `test_lining_*` experiments). Everything below is grounded in those real files; coordinates/groups/parameters are the project's actual ones, not generic.

**Project context that drove the design (read before coding):**
- The current `02_SmallModel/Small_Model.f3dat` builds the 0.40 m lining as **solid zones** (`group 'lining'`, NR=3 radial cells, attached `by-face` to the rock cavity wall). Your task replaces those solid zones with a structural shell.
- Concrete caps from `parameter.f3dat`: `shot_fc = 41.2e6` (compression), `shot_ft = 4.12e6` (tension), `shot_E = 25e9`, `shot_v = 0.2`, `shot_t = 0.40`.
- Tunnel center in model coords ≈ (x=1299, z=1747); box x[1250,1350] y[850,950] z[1700,1800]; crown ≈ (1297,885,1752), springline ≈ (1303,885,1747).
- Two `test_lining_*` experiments already PROVED: reducing lining *stiffness* alone does NOT relieve over-support (stress is load-controlled, stayed 57→65 MPa). The lining must **yield/damage to cap stress and shed load to the rock**. That is exactly why the shell needs Wade's E-reduction-on-yield damage law, and why the cap target is the concrete strength (41.2/4.12 MPa), not Wade's old 100 MPa.

---

## STEP 0 — Starting state and what to restore

Build on the already-balanced state, not from scratch. The proven chain is: `Small_Model.f3sav` (build) → `Small_Initial.f3sav` (in-situ, IDW-mapped) → `small_ep` (burgers-mohr + creep configured). Because we are **swapping the lining representation**, the cleanest entry is to redo from `Small_Initial` so the shell is genuinely wished-in-place at the in-situ field. Restore and load parameters first:

```
model new
model restore '../04_InitialBalance/Small_Initial'
call '../04_InitialBalance/parameter.f3dat'
model largestrain off
model configure creep
fish automatic-create on
```

Reason (Wade rule, `parameter.f3dat` + `idw_map.f3dat`): the lining was initialized to the **same IDW in-situ field** as the rock (continuous interface, no internal force jump at t=0 — true wished-in-place). We preserve that principle for the shell.

---

## STEP 1 — Remove the solid lining zones (null) and create the structural shell

### 1a. Capture the lining/rock interface as a face group BEFORE nulling
Wade's shells are always created `by-face` on the internal rock↔opening surface (`Excavation.f3dat`: `zone face group 'support' internal range group 'rock' group 'excavation'`). The Tunnel_TX lining is its own zone group sitting in the outer ring, attached to the rock cavity wall. The shell must land on the **rock-side wall of the cavity** (the rock↔lining interface), so it represents support on the rock surface — *not* on the inner clearance face.

```
; Mark the rock<->lining internal interface as 'support' BEFORE deleting anything.
; (internal faces shared between the rock body and the lining ring)
zone face group 'support' slot 'sup' internal range group 'rock' slot 'mat' group 'lining' slot 'mat'
```

### 1b. Null the solid lining zones
```
zone cmodel assign null range group 'lining' slot 'mat'
```
Reason: `zone cmodel assign null` is Wade's standard removal (`Excavation.f3dat`). The 0.40 m solid ring becomes void; the inner clearance was already open. The rock cavity wall (now bounding void) carries the `'support'` face group from 1a.

### 1c. Create the DKT-CSTH shell on that surface, E0=25 GPa, ν=0.2, t=0.40 m
Exact proven commands (Wade `Excavation.f3dat` lines 5–6 / `Failure.f3dat` lines 6–7), with the project's concrete properties:

```
[global Ec  = shot_E]     ; 25e9
[global nuc = shot_v]     ; 0.20
[global tc  = shot_t]     ; 0.40
struct shell create by-face element-type=dkt-csth range group 'support' slot 'sup'
struct shell property isotropic ([Ec], [nuc]) thickness [tc]
struct shell property density [shot_den]      ; 2400, so gravity/inertia on the shell is real
```

Reasons (from the SUPPORT digest, confirmed in the source files):
- **DKT-CSTH** = Discrete Kirchhoff Triangle + constant transverse shear. DKT removes shear-locking for thin plates; CSTH adds the transverse-shear compliance that is non-negligible for a 0.40 m lining at the horseshoe crown curvature. This element is what makes the M/N/V recovery valid later.
- **`by-face range group 'support'`** generates one shell element per internal cavity-wall face — geometry-exact to the rock surface, nodes coincident with the rock gridpoints, so load transfers without an interface element.
- t = 0.40 m here (NOT Wade's 0.30 m demo value) because that is the D7-decided Alishan lining thickness in `parameter.f3dat`.

### 1d. Link the shell nodes rigidly to the rock surface
Wade's `by-face` shells share gridpoints with the host zone faces automatically (no `struct link` needed when created by-face on a real zone surface). Verify the linkage exists rather than assuming:

```
fish define _shell_check
    local ns = 0
    local nl = 0
    loop foreach local s struct.list
        if struct.type(s) = 'shell' then
            ns = ns + 1
        end_if
    end_loop
    loop foreach local lk link.list
        nl = nl + 1
    end_loop
    io.out('SHELL_CHECK shells='+string(ns)+' links='+string(nl))
end
[_shell_check]
```
Reason (Wade lesson): created `by-face`, each shell node attaches to its underlying zone gridpoint via an auto link with full DOF — that is the load path from rock to lining. Confirm `links > 0`; if zero, the shell is floating and carries no load.

---

## STEP 2 — In-situ force balance with the shell wished-in-place

The shell was just installed onto an already-balanced rock field, but nulling the 0.40 m ring removed material stiffness/weight, so the system is no longer in equilibrium. Re-balance with the shell present (wished-in-place). Use Wade's **small-model solve discipline** — NOT `solve elastic`:

```
zone gridpoint initialize velocity 0 0 0
model solve ratio-average 1e-5 cycles 40000
```

Reasons (this is the single most important Tunnel_TX lesson, recorded inline in `prototype_small_creep.f3dat` line 36 and `large_creep_4stage.f3dat` line 76):
- The **LARGE** model re-equilibrates with `model solve elastic ratio-local 1e-3` (slope, far-field, elastic mode is fine there).
- The **SMALL/creep** model must re-equilibrate with the *full* `model solve ratio-average 1e-5` **in the burgers-mohr creep-mode stiffness**. Wade discovered that using `model solve elastic` on the small model causes a **stiffness-transition transient** when creep activates (elastic-mode stiffness ≠ burgers-mohr creep-mode stiffness) → spurious creep onset under low water. The fix was to re-equilibrate in the same constitutive stiffness the creep step will use. So here, with the shell installed, do the full `solve ratio-average`, not `solve elastic`.

Then zero the displacement datum once (this is the deformation clock start, `small_4stage_standalone.f3dat` line 76):

```
zone gridpoint initialize displacement 0 0 0
zone gridpoint initialize velocity 0 0 0
model save 'small_shell_insitu'
```

Sanity gate before proceeding — confirm the wished-in-place shell stress is *physical* (not the locked-in 57 MPa artifact the solid-ring experiments showed):

```
struct shell recover surface (0,1,0)
struct shell recover stress depth-factor 0
fish define _lin0
    local sc = 0.0
    local st = 0.0
    loop foreach local s struct.list
        if struct.type(s) = 'shell' then
            loop local k (0,3)
                local sp = struct.shell.stress.prin.x(s,k)   ; min principal (compression, signed)
                if -sp > sc then
                    sc = -sp                                 ; max compression magnitude
                end_if
                local spz = struct.shell.stress.prin.z(s,k)  ; max principal (tension, signed)
                if spz > st then
                    st = spz                                 ; max tension
                end_if
            end_loop
        end_if
    end_loop
    io.out('LIN0 insitu comp='+string(sc/1e6)+'MPa ten='+string(st/1e6)+'MPa (caps 41.2/4.12)')
end
[_lin0]
```

---

## STEP 3 — E-reduction-on-yield FISH for the shell (monotonic damage)

This is the heart of the request: adapt Wade's `shell_stress` (`WadeCreepSupport.f3dat` / `Failure.f3dat`) into a **two-cap, demand-based, monotonic-damage** law using the concrete strengths. Wade's original checked only compression against one cap (100/125 MPa) and reduced `E_new = E_old·(cap/σ)`. We generalize to **demand = max(σc/fc, σt/ft)** and add the requested stability safeguards (E floor 2.5 GPa, max 50% drop per event, monotonic).

```
; ---- shell damage parameters (concrete caps from parameter.f3dat) ----
[global sigCap_c = shot_fc]        ; 41.2e6  compression cap
[global sigCap_t = shot_ft]        ; 4.12e6  tension cap
[global E_floor  = 2.5e9]          ; never soften below 2.5 GPa (residual cracked-RC modulus)
[global drop_max = 0.5]            ; at most 50% E reduction in a single event (stability)
[global dmg_eps  = 0.01]           ; 1% over-cap tolerance before triggering (avoid chatter)

fish define shell_damage
    command
        struct shell recover surface (0,1,0)
        struct shell recover stress depth-factor 0
    endcommand
    local nred = 0
    loop foreach local s struct.list
        if struct.type(s) = 'shell' then
            ; --- gather extreme compression (sc) and extreme tension (st) over the 4 depth pts ---
            local sc = 0.0
            local st = 0.0
            loop local k (0,3)
                local smin = struct.shell.stress.prin.x(s,k)   ; min principal (most compressive, signed)
                if -smin > sc then
                    sc = -smin                                  ; compression magnitude (>=0)
                end_if
                local smax = struct.shell.stress.prin.z(s,k)   ; max principal (most tensile, signed)
                if smax > st then
                    st = smax                                   ; tension magnitude (>=0)
                end_if
            end_loop
            ; --- demand = worst of the two normalized caps ---
            local dem_c = sc / sigCap_c
            local dem_t = st / sigCap_t
            local dem = dem_c
            if dem_t > dem then
                dem = dem_t
            end_if
            ; --- trigger only if over cap by > eps ---
            if dem > (1.0 + dmg_eps) then
                local En = struct.shell.young(s)
                local En_target = En / dem                      ; Wade's proportional law: E_new = E_old*(cap/demand)
                ; safeguard 1: cap the per-event drop at drop_max (no more than 50% in one hit)
                local En_minstep = En * (1.0 - drop_max)
                if En_target < En_minstep then
                    En_target = En_minstep
                end_if
                ; safeguard 2: E floor
                if En_target < E_floor then
                    En_target = E_floor
                end_if
                ; safeguard 3: MONOTONIC -- only ever decrease
                if En_target < En then
                    struct.shell.young(s) = En_target
                    nred = nred + 1
                end_if
            end_if
        end_if
    end_loop
    global n_shell_red = nred
end
```

Design notes tied to Wade's proven choices and the project lessons:

- **Why `E_new = E_old / demand` (proportional)** — directly from `Failure.f3dat`/`WadeCreepSupport.f3dat` (`Et = En * (sigCap_out/sc)`). It is self-limiting: when σ rides back down to the cap, demand→1 and reduction stops. Generalized to `max(σc/fc, σt/ft)` so a tension crack at the crown intrados is detected as readily as compression crushing at the springline (the digest's whole point of "check both caps").
- **`recover stress depth-factor 0`** = outer-fiber stress (max bending extremum). Wade uses this exact recovery because tunnel linings fail in bending first; the 4-point depth loop (`k 0..3`) catches the worst fiber.
- **Monotonic (E only decreases)** — Wade's original was implicitly monotonic because σ only grows once exceeded; we make it *explicit* with the `if En_target < En` guard so a transient stress relief during creep re-equilibration can never *heal* the lining. This is the "monotonic damage" Wade requires.
- **E floor 2.5 GPa** — Wade's source had no floor (and his `Failure.f3dat` crash-recreate went to 15% = 3.75 GPa). The `test_lining_softE.f3dat` experiment used 6 GPa as "heavily cracked RC effective modulus." 2.5 GPa is a hard residual floor so the shell never goes to numerical zero stiffness (which would let the rock gridpoints fly → instability). It still provides residual confinement (mirrors `test_lining_softening.f3dat`'s residual-strength table `(0.005, 4.0e6)` keeping some support, no collapse).
- **Max 50%/event** — Wade's `Ereduce_ratio = 0.5` semantics, but applied as a per-event *floor on the step* rather than a fixed halving, so a wildly over-cap element can't drop to near-zero E in one callback and trigger a dynamic shock. Repeated callbacks then walk it down gradually.
- **eps tolerance 1%** — Wade's `eps = 0.01` exactly; prevents reduce/re-equilibrate chatter at the cap boundary.

### Callback timing — DO NOT use a per-cycle callback on this model
Wade's lab model used `fish callback add @shell_stress 12 interval 100`. **The Tunnel_TX small model is ~1.4M zones**, and the project already learned (inline comment, `prototype_small_creep.f3dat` lines 62–63) that a per-cycle single-thread FISH callback over 1.4M zones bottlenecks the multi-thread creep to ~1 core. The shell-only loop is cheap (few hundred elements), but to stay consistent and avoid recovering stress every 100 cycles, **call `shell_damage` at creep-segment boundaries** (the "update at creep-segment boundaries" the task asks for), exactly as Wade calls `@shell_failure` after each `model save` segment in `WadeCreepSupport.f3dat`'s `creep()` loop:

```
; called inside the per-stage day-stepping loop, at each dd-day segment boundary
```
(wired in Step 4). If you prefer the callback form for the shell only (cheap), it is safe:
```
fish callback add @shell_damage 12 interval 200   ; OPTIONAL; shell loop is small. Stage-boundary call preferred.
```
Reason for stage-12 if used: callback ID 12 fires post-cycle (after mechanical sub-step), so the recovered stress is the equilibrated state, matching Wade.

---

## STEP 4 — Integration with the staged large→small creep drive

The small model is **driven by the large model's per-stage cumulative displacement** as a velocity BC on the box faces — this is the squeezing source. The proven mechanics live in `couple_drive.f3dat` (the IDW-mapped per-stage cumulative disp, FIX driven gp velocity, sub-step ramp + calm). The four-stage water/creep cadence lives in `small_4stage_standalone.f3dat`. We fuse them: **box-face velocity BC drives the rock, threshold-gated burgers creep runs the time, shell_damage updates at each segment.**

### 4a. The driven boundary (from `couple_drive.f3dat`, lesson #69)
Load the large model's per-stage cumulative displacement targets onto the **box-face rock gridpoints only** (never interior, never the shell nodes), and FIX their velocity so the solver can't overwrite the imposed motion:

```
; gp.extra(g, stg) = cumulative displacement of this boundary gp at end of large-model stage `stg` (1..4)
; loaded from the large-model export via the IDW/boundary map (couple_bnd_disp.txt pattern)
[load_targets]                                   ; tags box-face gps group 'driven', fills gp.extra 1..4
zone gridpoint fix velocity range group 'driven' slot 'drive'
```
Reason: the box faces are the *only* place the large-model squeeze enters. The interior rock and the shell must remain free to respond. FIX the driven-gp velocity because an unfixed gp velocity is overwritten by the solver each cycle (lesson recorded in `couple_drive.f3dat` header).

### 4b. Per-stage drive: ramp the boundary to the stage target, then creep
Per stage `stg` (1..4): set each driven gp's velocity so it reaches `gp.extra(g,stg)` over the sub-stepped ramp (exact pattern from `couple_drive.f3dat run_stage`), `model calm` between sub-steps, then hold (vel→0) and run threshold-gated creep for that stage's days. The water plane toggles LOW/HIGH per stage exactly as `small_4stage_standalone.f3dat`.

```
fish define drive_and_creep(stg, nsub, ncyc_sub, d0, d1, dd)
    ; --- 1) compute per-gp increment to this stage's cumulative target ---
    loop foreach local g gp.list
        if gp.group(g,'drive') = 'driven' then
            gp.extra(g,5) = gp.extra(g, stg) - gp.disp(g)
        end_if
    end_loop
    local denom = float(nsub) * float(ncyc_sub) * mech.timestep
    ; --- 2) ramp the boundary in mechanical (no creep) sub-steps ---
    local j = 1
    loop while j <= nsub
        loop foreach local g2 gp.list
            if gp.group(g2,'drive') = 'driven' then
                gp.vel(g2) = gp.extra(g2,5) / denom
            end_if
        end_loop
        command
            model cycle [ncyc_sub]
            model calm
        endcommand
        j = j + 1
    end_loop
    ; --- 3) hold boundary, re-equilibrate rock in burgers-mohr stiffness ---
    loop foreach local g3 gp.list
        if gp.group(g3,'drive') = 'driven' then
            gp.vel(g3) = vector(0,0,0)
        end_if
    end_loop
    command
        model solve ratio-average 1e-5 cycles 40000
    endcommand
    [setKstrains]            ; re-set Kelvin strain to the NEW post-drive stress (CRITICAL, see pitfalls)
    do_threshold              ; gate creep on the new boundary-squeezed stress state
    [setKstrains]
    shell_damage              ; UPDATE shell E at the segment boundary, post-drive, pre-creep
    ; --- 4) creep this stage's days, refresh threshold + shell_damage each dd-day segment ---
    local d = d0 + dd
    command
        model creep active on
        model creep timestep fix [crp_dt]
    endcommand
    loop while d <= (d1 + 0.1)
        do_threshold                          ; per-increment threshold (multi-thread safe; NOT per-cycle)
        command
            model solve time-total [d*86400.0]
        endcommand
        shell_damage                          ; <-- E-reduction at the creep-segment boundary (Wade's @shell_failure timing)
        io.out('   stg'+string(stg)+' day='+string(d)+' active='+string(n_active)+' shell_reduced='+string(n_shell_red))
        d = d + dd
    endloop
    command
        model creep active off
        zone gridpoint initialize velocity 0 0 0
    endcommand
end
```

Stage cadence (LOW/HIGH water = the saturation toggle that drives effective-stress creep onset), mirroring `small_4stage_standalone.f3dat`, 4 stages × 30 days:

```
; STAGE 1 (drive to large s1, LOW water z1724, 0-30d) -- zero disp already done in Step 2
zone water plane origin (1297, 885, 1724) normal (0,0,1)
[drive_and_creep(1, 3, 100, 0.0, 30.0, 5.0)]
model save 'sm_s1'
; STAGE 2 (drive to large s2, HIGH water z1807, 30-60d, cumulative, NO disp zero)
zone water plane origin (1297, 885, 1807) normal (0,0,1)
[drive_and_creep(2, 3, 100, 30.0, 60.0, 5.0)]
model save 'sm_s2'
; STAGE 3 (large s3, LOW, 60-90d)
zone water plane origin (1297, 885, 1724) normal (0,0,1)
[drive_and_creep(3, 3, 100, 60.0, 90.0, 5.0)]
model save 'sm_s3'
; STAGE 4 (large s4, HIGH, 90-120d)
zone water plane origin (1297, 885, 1807) normal (0,0,1)
[drive_and_creep(4, 3, 100, 90.0, 120.0, 5.0)]
model save 'sm_s4'
```

### 4c. Hand off the ROCK-SIDE convergence to the coupled model (no double-counting)
This small model produces, per stage, the **rock-wall (cavity-surface) convergence** — the displacement of the rock gridpoints on the `'support'`/cavity surface. That convergence (NOT the shell internal forces) is what the coupled model consumes to drive its PFC-ball lining via `wz_outter`. Export the rock cavity-wall gridpoint cumulative displacement per stage in the same format `couple_drive.f3dat`'s `load_targets` reads:

```
fish define export_rock_conv(stg)
    local fp = 'small_rock_conv_s'+string(stg)+'.txt'
    local st = file.open(fp, 1, 1)
    local hdr = array.create(1)
    hdr(1) = 'gid dx dy dz'
    st = file.write(hdr,1)
    loop foreach local g gp.list
        ; cavity-wall rock gps: within ~5 m of tunnel axis, on the rock side
        local p = gp.pos(g)
        local rr = math.sqrt((comp.x(p)-1299.0)^2 + (comp.z(p)-1747.0)^2)
        if rr < 5.0 then
            local d = gp.disp(g)
            local ln = array.create(1)
            ln(1) = string(gp.id(g))+' '+string(comp.x(d))+' '+string(comp.y(d))+' '+string(comp.z(d))
            st = file.write(ln,1)
        end_if
    end_loop
    st = file.close
end
```

**No double-counting rule (the explicit task constraint):**
- The small model's **shell** carries the support reaction *for the small model's own equilibrium only* — it is the equivalent of the as-built RC lining, needed so the rock-side convergence is computed with realistic support stiffness/damage.
- The **coupled** model has its **own PFC-ball lining** (calibrated D7 micro-params in `parameter.f3dat`, confined by the rigid `w_inner`). It is driven by the small model's **rock-side convergence field**, NOT by the small shell's forces.
- Therefore: **export the rock cavity-wall gridpoint displacement; never export shell N/M/V to the coupled model.** The shell exists to make the small-model rock response correct; the PFC lining is the real lining in the coupled model. Feeding both would count the lining twice.

---

## STEP 5 — Pitfalls / reasons from Wade's experience to honor

1. **Small model: full `solve ratio-average`, NOT `solve elastic`.** (`prototype_small_creep.f3dat` line 36, the single biggest lesson.) `solve elastic` is the LARGE model's far-field tool. On the small/creep model it creates a stiffness-transition transient at creep activation → false creep onset under low water. Always re-equilibrate in the burgers-mohr creep-mode stiffness with `model solve ratio-average 1e-5`. This is also why Step 2's wished-in-place balance uses `solve ratio-average`.

2. **`setKstrains` after EVERY mechanical re-equilibration, before creep.** (Stamped all over `small_4stage_standalone.f3dat` and noted as "FLAC creep gotcha" in `prototype_small_creep.f3dat` line 96.) After any `model solve` that changes the stress (in-situ rebalance, water change, boundary drive), the Burgers **Kelvin strain** is stale relative to the new stress; without re-setting it you get a spurious creep transient on activation (a false trigger). Call `[setKstrains]` from `C:/Program Files/Itasca/Flac3d600/datafiles/Creep/SetKStrains.f3fis` after each re-eq and again after `do_threshold` flips viscosities.

3. **Threshold is called PER-INCREMENT, never as a per-cycle callback** on this 1.4M-zone model. (`prototype_small_creep.f3dat` lines 62–63.) A single-thread FISH over 1.4M zones every cycle bottlenecks multi-thread creep to ~1 core. The `do_threshold` is invoked once per dd-day segment inside `run_stage`. The **shell** loop is tiny, so calling `shell_damage` per segment (or a cheap `interval 200` callback) is fine — keep the *rock* threshold per-increment, never per-cycle.

4. **Use the corrected MC envelope for the threshold:** `q_th = threhold*(c*cos(phi) + p'*sin(phi))` (the form in `small_4stage_standalone.f3dat` line 39 and `large_creep_4stage.f3dat` line 48), NOT the old `tan` form. The earlier `ceff = thr*c; phieff = thr*tan(phi)` form (still present in `prototype_small_creep.f3dat` and Wade's lab `Failure.f3dat`) is `/cos(phi)` too high (~15.5% over-trigger). `threhold = 0.6` is the validated Alishan value (`parameter.f3dat` line 87); Wade's lab 0.4 was for his Chapter4 demo rock — do not import it.

5. **Lining stiffness reduction alone does NOT relieve over-support — it must damage/yield.** (Proven by `test_lining_softE.f3dat`: dropping E 25→6 GPa left stress at 57→still over.) The shell's E-reduction-on-yield law in Step 3 is the *correct* mechanism precisely because it caps stress at the concrete strength and sheds load to the rock, which is what `test_lining_softening.f3dat` demonstrated with strain-softening on the solid ring. Cap on **both** fc=41.2 MPa and ft=4.12 MPa — the intrados cracks in tension (4.12 cap) before the springline crushes in compression (41.2 cap), so a compression-only check (Wade's original) would miss the first failure mode.

6. **Monotonic damage + E floor are non-negotiable for stability.** Without the `if En_target < En` monotonic guard, a momentary creep-relaxation could "heal" the shell and oscillate. Without the 2.5 GPa floor and the 50%/event cap, an over-cap element can collapse to ~0 stiffness in one callback → the attached rock gridpoints get a dynamic kick → ratio blows up. These are the safeguards that adapt Wade's `Ereduce_ratio=0.5` and his crash-recreate-at-15% logic into a *stable in-place* damage law (no delete+recreate needed — Wade's in-place `struct.shell.young(s)=Et` preserves nodal DOF continuity and avoids remeshing shock).

7. **Drive only the box-face rock gridpoints; FIX their velocity; never drive the shell or interior.** (`couple_drive.f3dat` lesson #69 + the FIX rule.) The squeeze enters through the boundary only. An unfixed driven-gp velocity is overwritten each cycle by the solver — the imposed motion would silently vanish. Ramp with `model cycle` + `model calm` sub-steps (mechanical, creep off) before holding and running creep, so the boundary motion doesn't shock the creep integration.

8. **Cumulative displacement, zeroed exactly once** (after Stage-1 in-situ re-eq, Step 2). Stages 2–4 do NOT re-zero displacement — that is what produces the flat-onset-flat-onset deformation history across the 120-day record. (`small_4stage_standalone.f3dat` lines 76 vs 93/109/125: disp zeroed only in S1, velocity zeroed every stage.)

9. **Hand-off boundary is the rock-side convergence, not shell forces** (Step 4c). The coupled model's PFC lining is the real lining there; the small shell is only the small-model's support so its rock convergence is realistic. Export rock cavity-wall gp displacement, never shell N/M/V — that is the no-double-counting guarantee.

10. **`model configure creep` and `model largestrain off`** for the small model (`prototype_small_creep.f3dat` lines 12–13). Note the **coupled** model runs `largestrain on` + `mechanical timestep scale` (`couple_drive.f3dat` lines 13–14) — different mode; do not copy the coupled solver settings into the small model.

---

## Key file references (all absolute)
- Proven E-reduction source: `C:\Users\Wade\Desktop\Wade_TD_SCI\FLAC\code\CreepSupport\CreepFISH\WadeCreepSupport.f3dat` (`shell_stress`, `shell_failure`); `C:\Users\Wade\Desktop\Wade_TD_SCI\FLAC\Chapter4\TYPE3A\Failure.f3dat` (delete+recreate-at-15% variant).
- Shell create/property pattern: `C:\Users\Wade\Desktop\Wade_TD_SCI\FLAC\Chapter4\TYPE3A\Excavation.f3dat`.
- Project parameters (caps, eta, threshold, lining): `c:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\parameter.f3dat`.
- Validated small-model threshold/creep recipe: `c:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\small_4stage_standalone.f3dat`; solve-mode lesson in `prototype_small_creep.f3dat`.
- Lining-must-yield proof: `c:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\test_lining_softE.f3dat` (stiffness alone fails) and `test_lining_softening.f3dat` (yielding works).
- Boundary velocity-BC drive + no-double-count handoff: `c:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\couple_drive.f3dat`; large-model source of per-stage disp: `large_creep_4stage.f3dat`; mapping: `c:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\idw_map.f3dat`.
- Current solid-lining build to be replaced: `c:\Users\Wade\Desktop\Tunnel_TX\02_SmallModel\Small_Model.f3dat`.

**One open item to confirm with Wade before a long run** (per the project rule to verify before long files): whether the box-face driven-gp displacement targets (`gp.extra 1..4`) for the small model are already exported from `large_creep_4stage` in the small-model gridpoint-id space, or still need the `idw_map`/boundary-export step that `couple_drive.f3dat` consumes (`couple_bnd_disp.txt`, expects 28304 driven gps). If that boundary export doesn't yet exist for the *standalone small* model (it currently exists for the *coupled* model), Step 4a needs that export produced first.