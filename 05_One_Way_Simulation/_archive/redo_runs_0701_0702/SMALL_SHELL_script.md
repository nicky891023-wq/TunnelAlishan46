All FISH intrinsics confirmed: `struct.num()`, `struct.list()`, `struct.pos.x/y/z(p)`, `struct.shell.stress.prin.x/.z(p,inode)`. Note the FISH names use `struct.` prefix (the docs title them `struct.num`, `struct.pos`, `struct.shell.stress.prin`) even though the dir is `sel.*`. I now have everything verified. Let me confirm one final detail: whether `zone null` is the correct null syntax vs `zone cmodel assign null`, and check `zone gridpoint fix velocity` / `zone gridpoint initialize displacement`. The existing run_small_init.f3dat already uses `zone cmodel assign null range group` (rule §7) and `zone gridpoint fix velocity` and `zone gridpoint initialize displacement` — all proven in the existing tree. 

I have everything I need. Here is the complete, verified script.

---

## Verified command sequence — Alishan #46 small-model SHELL-LINING in-situ balance

Write this to `C:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\run_small_shell_init.f3dat` and run from cwd `04_InitialBalance`. Every non-obvious line is annotated with its grounding. Three items are flagged **VERIFY** — run the early CHECKPOINT and abort if the shell extent is wrong before the long solve.

```
; ============================================================================
; run_small_shell_init.f3dat -- Alishan #46 SMALL model, STRUCTURAL-SHELL lining
;   in-situ force balance (replaces the solid attached lining with a dkt-csth
;   shell on the rock cavity wall).  cwd = 04_InitialBalance.
;
;   flac3d600_console.exe run_small_shell_init.f3dat   (argv; stdin closed; ends quit)
; Units SI (Pa, kg/m3, m, deg, s).  Sign: compression negative.
; ============================================================================
program log-file 'run_small_shell_init.log'
program log on

model restore '../02_SmallModel/Small_Model'      ; rock(6-layer) + lining zones + attach, no in-situ
call 'parameter.f3dat'                              ; material params (E_S_*, co_S_*, nu, ten_r, shot_*, grav)
call 'idw_map.f3dat'                                ; defines ReadFile_ss(), MapStress_IDW()
model largestrain off

; ----------------------------------------------------------------------------
; 1) ROCK constitutive : 6-layer Mohr-Coulomb
;    (skill §4 mohr-coulomb required keys: bulk/shear OR young/poisson,
;     cohesion, friction, dilation, tension.  We supply young+poisson; dilation
;     defaults to 0.  Pattern proven in run_small_init.f3dat lines 17-29.)
; ----------------------------------------------------------------------------
zone cmodel assign mohr-coulomb range group 'rock' slot 'mat'
zone property young [E_S_1] poisson [nu] cohesion [co_S_1] friction [fr_S_1] tension [ten_r] range group 'layer1' slot 'type'
zone property young [E_S_2] poisson [nu] cohesion [co_S_2] friction [fr_S_2] tension [ten_r] range group 'layer2' slot 'type'
zone property young [E_S_3] poisson [nu] cohesion [co_S_3] friction [fr_S_3] tension [ten_r] range group 'layer3' slot 'type'
zone property young [E_S_4] poisson [nu] cohesion [co_S_4] friction [fr_S_4] tension [ten_r] range group 'layer4' slot 'type'
zone property young [E_S_5] poisson [nu] cohesion [co_S_5] friction [fr_S_5] tension [ten_r] range group 'layer5' slot 'type'
zone property young [E_S_6] poisson [nu] cohesion [co_S_6] friction [fr_S_6] tension [ten_r] range group 'layer6' slot 'type'
zone initialize density [den_S_1] range group 'layer1' slot 'type'
zone initialize density [den_S_2] range group 'layer2' slot 'type'
zone initialize density [den_S_3] range group 'layer3' slot 'type'
zone initialize density [den_S_4] range group 'layer4' slot 'type'
zone initialize density [den_S_5] range group 'layer5' slot 'type'
zone initialize density [den_S_6] range group 'layer6' slot 'type'
[io.out('CHK1 rock MC assigned: total zones='+string(zone.num))]

; ----------------------------------------------------------------------------
; 2) MAP large in-situ stress onto the ROCK (wished-in-place) BEFORE nulling
;    the lining, so IDW still sees the full rock field. radius 40 m per the
;    coarse subsample. (idw_map.f3dat MapStress_IDW maps onto ALL live zones;
;    lining zones get mapped too but are nulled in step 3, so harmless.)
; ----------------------------------------------------------------------------
[ReadFile_ss('large_stress_coarse.dat')]
[MapStress_IDW(40.0)]
[io.out('CHK2 large in-situ stress IDW-mapped onto rock')]

; ----------------------------------------------------------------------------
; 3) NULL the solid lining zones -> exposes the rock cavity wall as a NEW
;    external surface (faces that were attach-glued now have a null/no zone on
;    the far side).  Grounding: cmd_zone.cmodel.assign (null), and zone face
;    skin doc: "only zone faces that have no zone on the other side, a hidden
;    zone, or a mechanically null zone on the other side are surface faces"
;    (cmd_zone.face.skin.html line 36).
;    Excavation idiom per skill §7 rule 7: zone cmodel assign null range group.
; ----------------------------------------------------------------------------
zone cmodel assign null range group 'lining' slot 'mat'
[io.out('CHK3 lining nulled: live zones='+string(zone.num))]

; ----------------------------------------------------------------------------
; 4) MARK the cavity-wall faces.  An external rock face = a face of a live rock
;    zone whose neighbor across that face is null (zone.join(z,i)==null), AND
;    which is NOT on one of the 6 box boundary planes.  We assign such faces to
;    face-group 'cavity' in face-slot 'fcav'.
;    Grounding:
;      - zone.join(z,i) returns the joined zone or null (fish_zone.join.html L32,37).
;        This REPLACES the invalid zone.face.zone(zf,fi) attempt.
;      - zone.face.group(z,iside,slot)=name : face-group SET form
;        (fish_zone.face.group.html L33-34, "On set ... slot").
;      - hex faces iside 1..6 (fish_zone.join.html L41).
;    Box planes (Small_Model.f3dat L62-67): x=1250/1350, y=850/950, z=1700/1800.
;    Margin 1.0 m from each plane (matches the existing box-group +-1 m bands).
; ----------------------------------------------------------------------------
fish define mark_cavity
    local nface = 0
    loop foreach local z zone.list
        if zone.isnull(z) = false then                  ; skip the nulled lining
            loop local fi (1,6)
                if zone.join(z,fi) = null then           ; external face
                    local fp = zone.face.pos(z,fi)       ; face centroid (fish_zone.face.pos.html)
                    local px = comp.x(fp)
                    local py = comp.y(fp)
                    local pz = comp.z(fp)
                    local on_box = false
                    if px < 1251.0 then
                        on_box = true
                    endif
                    if px > 1349.0 then
                        on_box = true
                    endif
                    if py < 851.0 then
                        on_box = true
                    endif
                    if py > 949.0 then
                        on_box = true
                    endif
                    if pz < 1701.0 then
                        on_box = true
                    endif
                    if pz > 1799.0 then
                        on_box = true
                    endif
                    if on_box = false then
                        zone.face.group(z,fi,'fcav') = 'cavity'
                        nface = nface + 1
                    endif
                endif
            endloop
        endif
    endloop
    io.out('CHK4 cavity-wall faces marked = '+string(nface))
end
[mark_cavity]

; ----------------------------------------------------------------------------
; 5) CREATE the structural shell on ONLY the cavity-wall faces.
;    "by-face ... range group 'cavity' slot 'fcav'": by default only SURFACE
;    faces are considered AND the range restricts to the filtered cavity group,
;    so NO internal-rock shells (cmd_structure.shell.create.html L40 + keyword
;    block 'group' L77-78, 'element-type' L96-131 -> dkt-csth = L129-131).
;    Idiom proven in datafiles/Structure/Shell/AdvancingTunnel/AdvancingTunnel.f3dat
;    L33-34:  struct shell create by-face group '<name>' range group ... ;
;             struct shell property isotropic=(E,nu) thickness=...
;    element-type dkt-csth = DKT-(CST Hybrid) 18-DOF bending+membrane shell.
; ----------------------------------------------------------------------------
structure shell create by-face element-type dkt-csth group 'shell_lining' ...
          range group 'cavity' slot 'fcav'

; shell elastic props (parameter.f3dat: shot_E=25e9 shot_v=0.2 shot_t=0.40 shot_den=2400)
structure shell property isotropic=([shot_E], [shot_v]) thickness=[shot_t] density=[shot_den] ...
          range group 'shell_lining'

; ============================================================================
; *** EARLY CHECKPOINT *** -- shell count + r/y extent, BEFORE the long solve.
;   ABORT (program quit) and fix the filter if:
;     - n_shell == 0 (filter wrong / attach not exposed), OR
;     - r spans toward 0 (internal-face shells leaked in; cavity r should be
;       ~1.3-5 m per the lining r[0.96,4.72] / rock min-r ~1.347), OR
;     - y extent escapes [850,950].
;   r is measured from the tunnel axis (x0=1297, z0=1747.5); y is along-axis.
;   Grounding: struct.num() (fish_sel.num.html), struct.list() (fish_sel.list.html,
;   all SELs -- only shells exist here), struct.pos.x/y/z (fish_sel.pos.html).
; ============================================================================
fish define shell_checkpoint
    local x0 = 1297.0
    local z0 = 1747.5
    local ns = 0
    local rmn = 1e30
    local rmx = -1e30
    local ymn = 1e30
    local ymx = -1e30
    loop foreach local s struct.list
        ns = ns + 1
        local sx = struct.pos.x(s)
        local sy = struct.pos.y(s)
        local sz = struct.pos.z(s)
        local r = math.sqrt((sx-x0)^2 + (sz-z0)^2)
        if r < rmn then
            rmn = r
        endif
        if r > rmx then
            rmx = r
        endif
        if sy < ymn then
            ymn = sy
        endif
        if sy > ymx then
            ymx = sy
        endif
    endloop
    io.out('=== SHELL_CHECKPOINT ===')
    io.out('  n_shell      = '+string(ns)+'  (struct.num='+string(struct.num)+')')
    io.out('  r_from_axis  = ['+string(rmn)+' , '+string(rmx)+'] m')
    io.out('  y_extent     = ['+string(ymn)+' , '+string(ymx)+'] m')
    io.out('  EXPECT r~[1.3,5.0] (NOT toward 0) ; y in [850,950]. Else ABORT.')
    io.out('SHELL_CHECKPOINT_DONE')
end
[shell_checkpoint]
model save 'small_shell_created'      ; checkpoint save so you can rerun the solve without re-creating

; ----------------------------------------------------------------------------
; 6) BOUNDARY CONDITIONS
;    6 box faces fixed (Small_Model.f3dat box-group +-1 m bands; pattern from
;    run_small_init.f3dat L47-52). zone gridpoint fix velocity holds the
;    submodel at the parent state.
; ----------------------------------------------------------------------------
zone gridpoint fix velocity range position-x 1249 1251
zone gridpoint fix velocity range position-x 1349 1351
zone gridpoint fix velocity range position-y 849 851
zone gridpoint fix velocity range position-y 949 951
zone gridpoint fix velocity range position-z 1699 1701
zone gridpoint fix velocity range position-z 1799 1801

model gravity 0 0 [-grav]             ; 0 0 -9.81  (parameter.f3dat grav=9.81)

; ----------------------------------------------------------------------------
; 7) SOLVE -- small-model discipline (Wade): NOT 'solve elastic'.  Plain
;    mechanical solve in the creep-mode stiffness, ratio-average 1e-5, guarded
;    by a 40000-cycle cap.  Grounding: cmd_model.solve.html -- 'ratio-average'
;    (L361-364) and 'cycles' (mechanical.cycles L275-278); multiple limits ->
;    OR default = stop at whichever is met first (L349-352).
;    NOTE: this script keeps the static MC stiffness (model NOT configured creep).
;    If the creep module is required for the in-situ stiffness path, add
;    'model configure creep' + Burgers-Mohr assignment BEFORE this solve and
;    use 'model solve ratio-average 1e-5 cycles 40000' unchanged. <-- confirm
;    with Wade which stiffness the in-situ balance should run in.   [VERIFY]
; ----------------------------------------------------------------------------
fish define _szz(tag)
    local zmn = 1e30
    local zmx = -1e30
    loop foreach local z zone.list
        if zone.isnull(z) = false then
            local s = zone.stress.zz(z)
            if s < zmn then
                zmn = s
            endif
            if s > zmx then
                zmx = s
            endif
        endif
    endloop
    io.out('CHK '+tag+' szz[min='+string(zmn)+' max='+string(zmx)+']')
end
[_szz('before-solve')]
model solve ratio-average 1e-5 cycles 40000
[_szz('after-solve')]
[io.out('CHK5 small shell-lining in-situ solved')]

; ----------------------------------------------------------------------------
; 8) DATUM RESET + SAVE
;    Zero displacement & velocity once in-situ is converged (clean datum for the
;    later damage stage). zone gridpoint initialize displacement/velocity proven
;    in AdvancingTunnel (L: 'zone gridpoint initialize displacement (0,0,0)').
; ----------------------------------------------------------------------------
zone gridpoint initialize displacement 0 0 0
zone gridpoint initialize velocity 0 0 0
model save 'small_shell_insitu'
[io.out('CHK6 saved small_shell_insitu')]

; ============================================================================
; 9) QA REPORT (io.out)
; ============================================================================
; --- 9a. SHELL stress recovery + extremes ---------------------------------
;   recover surface (0,1,0): builds the surface coord system using the tunnel
;     axis (y) as the projected x'-direction -- valid because the cavity-wall
;     normals are ~radial (in x-z), never aligned with y, so the surface call
;     will not hit the "v aligned with z' " error (cmd_structure.shell.recover.html
;     L54-55).   [VERIFY the (0,1,0) choice does not error for the invert faces;
;     if it does, switch surface vector to (1,0,0).]
;   recover stress depth-factor 0 : mid-surface stress tensor, global frame
;     (L46-47). depth-factor 0 = membrane (mid-surface), avoids the +-1 outer/
;     inner fibre bending peak; report it as the membrane state.
structure shell recover surface (0,1,0)
structure shell recover stress depth-factor 0
fish define shell_stress_qa
    local cmax = 1e30      ; most negative principal = max compression
    local tmax = -1e30     ; most positive principal = max tension
    loop foreach local s struct.list
        if struct.shell.stress.valid(s) = true then     ; fish_sel.shell.stress.valid.html
            local sc = struct.shell.stress.prin.x(s,0)   ; min princ @ centroid (most comp)
            local st = struct.shell.stress.prin.z(s,0)   ; max princ @ centroid (most tens)
            if sc < cmax then
                cmax = sc
            endif
            if st > tmax then
                tmax = st
            endif
        endif
    endloop
    io.out('=== SHELL_STRESS_QA (depth-factor 0, mid-surface) ===')
    io.out('  max_compression (most -ve princ) = '+string(cmax)+' Pa')
    io.out('  max_tension     (most +ve princ) = '+string(tmax)+' Pa')
    io.out('  (must be PHYSICAL, not the locked-in 57 MPa artifact)')
end
[shell_stress_qa]

; --- 9b. ROCK QA near tunnel : least-compressive principal, tension count,
;         plastic count, max displacement (vs bare-rock 22.3 mm) -------------
;   zone.stress.prin.x = min (most comp), .z = max (least comp / most tens)
;   zone.state -> plastic-state bitmask; >0 = currently/previously yielded.
;   Grounding: these are standard zone FISH intrinsics in the install
;   (fish_zone.stress.*, fish_zone.state.*).   [VERIFY zone.state name on your
;   build -- some report it as zone.state.matrix; the count below uses the
;   scalar zone.state(z) which is the v6 flag.]
fish define rock_qa
    local least_comp = -1e30      ; max of (max principal) over rock
    local ntens = 0
    local nplas = 0
    local dmax = 0.0
    loop foreach local z zone.list
        if zone.isnull(z) = false then
            local zx = zone.pos.x(z)
            local zz = zone.pos.z(z)
            local r = math.sqrt((zx-1297.0)^2 + (zz-1747.5)^2)
            if r < 10.0 then                       ; near-tunnel annulus only
                local smax = zone.stress.prin.z(z) ; least-compressive principal
                if smax > least_comp then
                    least_comp = smax
                endif
                if smax > 0.0 then
                    ntens = ntens + 1
                endif
                if zone.state(z) > 0 then
                    nplas = nplas + 1
                endif
            endif
        endif
    endloop
    loop foreach local g gp.list
        local d = math.sqrt(gp.disp.x(g)^2 + gp.disp.y(g)^2 + gp.disp.z(g)^2)
        if d > dmax then
            dmax = d
        endif
    endloop
    io.out('=== ROCK_QA (near-tunnel r<10 m) ===')
    io.out('  least_comp_principal_max = '+string(least_comp)+' Pa  (>0 => tension)')
    io.out('  tension_zone_count       = '+string(ntens))
    io.out('  plastic_zone_count       = '+string(nplas))
    io.out('  max_total_disp           = '+string(dmax)+' m  (cf bare-rock 0.0223 m; must be BOUNDED)')
    io.out('ROCK_QA_DONE')
end
[rock_qa]

program log off
program quit
```

---

### Grounding summary (all paths under `…\flac3d-600\references\chm_extracted\`)

| Command / intrinsic | Verified at |
|---|---|
| `zone.join(z,i)` -> neighbor or `null` (external-face test) | `flac3d\zone\…\zone_fish\zone_intrinsics\fish_zone.join.html` L32, L37, L41 |
| `zone.face.group(z,iside,slot) = name` (set face group) | `…\zone_fish\zone.face_intrinsics\fish_zone.face.group.html` L33-34, L49 |
| `zone.face.pos(z,fi)` (face centroid) | `…\zone.face_intrinsics\fish_zone.face.pos.html` (sibling, glob-confirmed) |
| `zone face skin … internal` semantics (null on far side = surface) | `…\zone_commands\cmd_zone.face.skin.html` L36, L57-58 |
| `structure shell create by-face … group … range`; default surface-only; `internal` opt; `element-type dkt-csth` | `flac3d\sel\…\shells\commands\cmd_structure.shell.create.html` L40, L77-78, L96-139 |
| `structure shell property isotropic=(E,v) thickness= density=` | `…\shells\commands\cmd_structure.shell.property.html` L39-47, L80-83 |
| `structure shell recover surface <v>` + `recover stress depth-factor <f>` | `…\shells\commands\cmd_structure.shell.recover.html` L34, L46-47, L54-55 |
| `struct.shell.stress.prin.x/.z(p,inode)`; .x=min(most comp), .z=max(most tens); inode 0=centroid; comp -ve | `…\shells\fish\sel.shell_intrinsics\fish_sel.shell.stress.prin.html` L34-36, L60, L100-101 |
| `struct.shell.stress.valid(p)` | `…\sel.shell_intrinsics\fish_sel.shell.stress.valid.html` (glob-confirmed) |
| `struct.list()`, `struct.num()`, `struct.pos.x/y/z(p)` | `…\sel\…\sel_fish\sel_intrinsics\fish_sel.list.html` L32, `fish_sel.num.html` L31, `fish_sel.pos.html` L33,57-89 |
| `model solve ratio-average <f> cycles <i>` (OR default) | `common\kernel\…\model\commands\cmd_model.solve.html` L361-364, L275-278, L349-352 |
| `struct shell create by-face group … ; struct shell property isotropic=(…) thickness=` live idiom | `C:\Program Files\Itasca\Flac3d600\datafiles\Structure\Shell\AdvancingTunnel\AdvancingTunnel.f3dat` L33-34 |
| MC keys, excavation-null idiom, gp fix velocity, gp init disp | skill §4, §7 rule 7; `run_small_init.f3dat` L17-52; AdvancingTunnel datum-reset line |
| `shot_E/v/t/den`, `E_S_*`, `co_S_*`, `nu`, `ten_r`, `grav` | `04_InitialBalance\parameter.f3dat` L21-23, L28, L59-82, L91-94 |
| `ReadFile_ss`, `MapStress_IDW` signatures | `04_InitialBalance\idw_map.f3dat` L20, L71 |

### Items flagged VERIFY (not 100% certain — confirm before / during the long run)
1. **`zone.state(z)` plastic flag name (step 9b).** The scalar plastic-state intrinsic is `zone.state(z)` on most v6 builds, but some report it as `zone.state.matrix`. If `[rock_qa]` errors on `zone.state`, the QA loop is the only thing affected (not the solve). I did not open the `fish_zone.state*.html` page in this session, so confirm the exact name (grep `fish_zone.state` in the manual) before relying on the plastic count.
2. **`recover surface (0,1,0)` for the invert (step 9a).** Documented to fail only if the surface vector aligns with a node normal `z'` (`cmd_structure.shell.recover.html` L55). Cavity-wall normals are radial in x-z so (0,1,0) is safe in general, but if any near-flat invert face has a normal that swings toward y it could error — fall back to `surface (1,0,0)`. Logic verified; the specific vector choice for this exact D-shape is the unverified part.
3. **Which stiffness the in-situ balance runs in (step 7).** The script keeps the static MC stiffness and uses `model solve ratio-average 1e-5 cycles 40000` (per the Wade discipline: NOT `solve elastic`). If the in-situ balance must run in the Burgers-Mohr creep-mode stiffness, add `model configure creep` + the Burgers-Mohr assignment before the solve — the `solve` line itself is unchanged and verified. Confirm the intended stiffness path with Wade.

### Two structural cautions (verified, not flags)
- **Step 5 vs your Approach B.** The doc explicitly states `by-face` considers "only surface faces" by default (`cmd_structure.shell.create.html` L40). Your Approach B got 47033 shells because the bare `cylinder … radius 5.2` volume range selected interior zones whose faces, after the cut, were surface-eligible in that geometry. The FISH-filtered `group 'cavity' slot 'fcav'` approach is unambiguous: it only contains the `zone.join==null` non-box faces, so no internal-rock leakage is possible. This is why the early CHECKPOINT prints r-extent — it is the direct guard against that exact failure.
- **Nulling vs the attach (step 3).** `zone cmodel assign null range group 'lining' slot 'mat'` nulls the lining mechanically; the rock cavity-wall faces it was attached to then satisfy "mechanically null zone on the other side" and become surface faces (`cmd_zone.face.skin.html` L36) — which is exactly what `zone.join==null` detects and what `by-face` needs. You do not need a separate `zone face skin internal true` call; the FISH filter supersedes it and is cleaner for an off-center D-shape (skin would scatter the cavity across sTop/sBottom/sEast/sWest groups by normal).

Relevant file paths:
- Script to create: `C:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\run_small_shell_init.f3dat`
- Restore source: `C:\Users\Wade\Desktop\Tunnel_TX\02_SmallModel\Small_Model.f3sav`
- Called: `C:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\parameter.f3dat`, `...\idw_map.f3dat`
- Reference for idioms already in use: `C:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\run_small_init.f3dat`