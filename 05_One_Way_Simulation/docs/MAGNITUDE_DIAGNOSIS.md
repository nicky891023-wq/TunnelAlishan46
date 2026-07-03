Surface above the tunnel (x~1250-1346) ranges z=1534 to 2186m; tunnel crown ~z1797. So overburden is roughly z_surface(~1900-2000 typical over the tunnel) minus z_crown(1797) ≈ **100-200m** of cover, but the zone-stress data at the tunnel shows only sig1~0.3-1.7 MPa. That low stress is consistent with ~100-150m cover at the shallower end but the actual measured stresses are the ground truth and they're low. 

I have fully verified the load-bearing numbers. The key correction to the input briefs: the in-situ stress at the tunnel is **sub-MPa to ~1.7 MPa (not 5-12 MPa)**, and the eta-sensitivity test PROVES creep viscosity is not the bottleneck. This reframes the diagnosis. Let me compose the decision-ready synthesis.

---

# ALISHAN #46 SMALL-MODEL SQUEEZING — MAGNITUDE DIAGNOSIS & PLAN

I verified every load-bearing number against the project files (`parameter.f3dat`, `small_driven.log`, `small_drive_residual.txt`, `diag_etam.log`, `diag_zone_y885.txt`, `small_tcrit_y885.txt`, `large_slope_surface.txt`). Two of the three input briefs over-estimated the in-situ stress (assumed 5-12 MPa). The actual measured tunnel-horizon stress is far lower, and there is an already-run eta sensitivity test that settles the creep question. This sharpens the diagnosis considerably.

## 0. GROUND-TRUTH CORRECTIONS (verified, not assumed)

- **In-situ stress at the tunnel is SUB-MPa to ~1.7 MPa, NOT 5-12 MPa.** `diag_zone_y885.txt` zones at crown elevation (z~1745-1797) show sig1 ≈ 0.34-1.7 MPa, sig3 ≈ 0.11-0.7 MPa. The earlier "σv≈6 MPa / 12.5 MPa" estimates in the briefs are wrong by ~5-10x. The surface over the tunnel (x 1250-1346) is z≈1534-2186m vs crown z≈1797m, so cover is only ~100-200m on the high side and near-zero on the daylighting side — a shallow, partly-daylighting slope toe, not a deep tunnel.
- **The eta_m sensitivity test was ALREADY RUN and is decisive** (`diag_etam.log`): dropping eta_m 300x from 6e15 to **2e13 Pa·s** produced essentially **no extra creep** — vclose stayed at −1.57 / −1.56 / −1.61 mm over a 30-day HIGH-water stage (it even relaxed slightly). This is the single most important experiment in the project and it **rules out creep viscosity as the bottleneck.**
- All other brief numbers confirmed: E_S_4=1.5 GPa, c=100 kPa/φ=30°; eta_m=6e15, eta_k=2.4e13, threshold=0.6, crp_dt=600s; shell E=25 GPa, t=0.40 m, ft=4.12/fc=41.2 MPa; convergence day0 vclose −2.14/hclose −1.75 → S3-END −2.44/−3.00 mm; shellMaxT rode to 46.2 MPa (force-controlled, not capped); residuals at box faces 5-26 mm.

## 1. DIAGNOSIS — ranked contributors to the 40-60x gap

The gap is **NOT one dominant factor**; it is a chain in which the *driving energy never reaches the tunnel*. Ranked by leverage:

| Rank | Contributor | Verified number | Why it limits magnitude |
|---|---|---|---|
| **1** | **Low driving stress + sub-threshold creep** | tunnel sig1 0.3-1.7 MPa; deviatoric q≈(sig1−sig3)/2 ≈ 0.3-0.5 MPa; q_th≈0.6·(0.087+pmean·0.5)≈0.45-0.6 MPa; **tcrit field 0.35-0.61, mostly < 0.6** (`small_tcrit_y885.txt`) | Most near-tunnel zones never cross the creep threshold, so creep can't run regardless of eta. Even where it runs, q is tiny so ε̇=q/η is tiny. This is the true bottleneck. |
| **2** | **Shell over-support** | bare rock 22.3 mm → shelled 5.2 mm in-situ (4.3x suppression); E_shell/E_rock = 25/1.5 = 16.7x | Real, but it only caps the *elastic/plastic* response to ~5 mm. It is the gating factor for the "instant" part, not the creep part. |
| **3** | **Large-model drive residual is small** | deformational residual at box faces 5-26 mm over the 100 m box (`small_drive_residual.txt`) → gradient ~0.2 mm/m → ~2 mm over a 10 m tunnel span | The slope creep is ~99% rigid translation; only this small distortion strains the small box. Modest, but it IS what produced the +0.3-0.8 mm/stage seen. |
| **4 (NOT a cause)** | **Creep viscosity eta_m** | 6e15 → 2e13 (300x softer) changed vclose by ~0 (`diag_etam.log`) | Lowering eta does nothing here because the creep engine is starved by Factors 1+3. Tuning eta is both cheating AND ineffective. |

**Bottom line:** the model is producing ~3 mm because that is genuinely what this stress/geometry/support system delivers in 120 days. The gap is dominated by **insufficient driving stress reaching a sub-threshold creep field**, not by an over-stiff dashpot.

## 2. IS 10-20 cm PHYSICALLY REASONABLE HERE?

**Honest answer: NOT at the current in-situ stress and 120-day window. 10-20 cm is the wrong target for *this* model state.**

- Squeezing magnitude scales with the strength ratio σcm/p0 and with time. The literature 10-20 cm cases (Wang 2003 New Kuanyin: ~180-280 mm) have **p0 ≈ 5-10 MPa over 240+ days with σcm/p0 ≈ 0.3-0.5**. Here the *measured* p0 at the tunnel is **0.3-1.7 MPa**. With UCS_rockmass even as low as 2-5 MPa, σcm/p0 ≳ 1.5-3 → that is **non-squeezing / light-squeezing territory** (Hoek-Marinos NS-LS, <0.25-0.5% strain). 3 mm on a ~10 m opening is 0.03% — exactly what a non-squeezing low-stress section should give.
- **The dominant mechanism that COULD give 10-20 cm here is slope-drive, not in-situ creep** — but only if the drive delivered cm-scale distortion to the box, which it currently does not (5-26 mm residual, mostly rigid).

So either (a) Wade's 10-20 cm expectation is set by a deeper / higher-stress section than the one being modeled, or (b) the drive coupling is under-transmitting. Both are physical questions, not knobs to turn.

**Physically-justified ways the target becomes reachable (none are cheating):**
1. **Higher in-situ stress** — if the real tunnel section sits under 300-500 m cover (p0 5-12 MPa) instead of the 100-200 m the current mesh represents, σcm/p0 drops into the squeezing range and both plastic yield and creep engage. This must come from the *geology/section selection*, verified against the centerline, not from inflating K0.
2. **Longer time** — creep is time-dependent; cm-scale creep needs years, not 120 days, even with engaged creep. The 4×30-day window is too short for a creep-dominated 10-20 cm.
3. **Larger transmitted drive** — if the large→small coupling delivered the *true* slope distortion (not 99%-rigid-removed residual of 5-26 mm but cm-scale boundary movement), the tunnel could close 10-20 cm by kinematic forcing.

## 3. ACTIONABLE PLAN (ordered by correctness, then no-cheating)

**(i) Fix the working shell E-reduction so the cracked lining genuinely softens (correctness fix, NOT a magnitude trick).**
The current shell damage is "record-only / force-controlled" — it counts cracked shells but E never actually drops on the next solve, so the lining keeps its full 25 GPa restraint while reporting 46 MPa (11x over ft). That is physically wrong: a lining cracked 11x past tension capacity cannot still carry full stiffness. Make it a real isotropic E-reduction via the command path (FISH `struct.shell.young` alone does NOT propagate; you must apply `structure shell property isotropic (Enew,nu) range ...`). Per-shell grouping by FISH intrinsic doesn't exist; use command grouping `structure shell group <name> slot <s> range ...` or apply `range id <id-list>` built in FISH. Floor at residual cracked-RC modulus ~2.5-5 GPa. **Expected effect: convergence rises from ~5 mm toward bare-rock ~22 mm as cracking propagates — i.e. up to ~2-4x, reaching ~10-20 mm, still short of 100-200 mm but physically honest.**

**(ii) Reconsider E0=25 GPa for an *equivalent* lining — this is likely the most defensible single change.**
Wade WANTS it to crack. A 0.40 m, 25 GPa intact-RC shell that is supposed to crack should be modeled with an *effective* modulus reflecting its cracked/jointed state. Cracked-RC effective modulus from literature is **3-8 GPa** (vs 25 GPa intact). Setting E0 ≈ 5 GPa as the *equivalent lining* property is **physical justification, not tuning to a target**: it represents a segmental/cracked liner, not a monolithic elastic plate. This drops E_shell/E_rock from 16.7x to ~3x and lets convergence approach bare-rock + creep. Combined with (i), expect **~10-20 mm**.

**(iii) Creep eta: DO NOT change it. Document why.**
The `diag_etam.log` experiment proves eta is not the lever (300x softer → ~0 effect). eta_m=6e15 is Wade's literature-grounded estimate and is fine. The creep deficit is upstream (sub-threshold stress), so any eta change would be both cheating and useless. Flag this experiment to Wade as the proof.

**(iv) In-situ stress / depth check — the highest-leverage *correctness* question.**
The measured 0.3-1.7 MPa tunnel stress is the real reason squeezing is light. Two checks, both physical:
   - Verify the modeled section against `tunnel46-2m.csv` centerline: is this the deep section Wade expects 10-20 cm at, or a shallow toe? If the design squeezing section is under 300-500 m cover, the small box must be cut from that location, raising p0 to 5-12 MPa.
   - Re-examine the in-situ initialization: `codex_insitu.txt`/`codex_insitu2.txt` flag that the K0=0.7 + terrain solve produced tension-capping and 425 mm settlement, i.e. the initial stress field is itself unsettled. A clean gravity-compatible no-tension in-situ (per the codex recipe) may yield a higher, cleaner confinement at the tunnel.

## 4. CONCRETE RECOMMENDATION — tonight vs Wade's morning decision

**Re-run tonight (cheap, correctness-driven, no target-chasing):**
1. **Equivalent-lining E sweep**: re-run the staged `small_driven` with shell E0 = 5 GPa (cracked-RC effective modulus, literature-justified) AND the *working* (command-based) E-reduction-on-yield from §3(i). Report new vclose/hclose per stage + bare-rock-with-shell-softened max_disp. Expected ~10-20 mm — this tells us how much of the gap is shell over-support honestly closable. Cost: same as the existing run.
2. **In-situ stress audit**: dump sig1/sig3/pmean and the tcrit field at the tunnel for the *current* state (you already have `diag_zone_y885.txt`/`small_tcrit_y885.txt` — just confirm the fraction of near-tunnel zones with tcrit≥0.6). This quantifies "how starved is the creep engine" in one number for Wade.

**Flag for Wade's morning decision (these are scope/physics calls, NOT mine to make):**
- **A. The big one: is the modeled section the right (deep enough) one?** Measured p0 at the tunnel is 0.3-1.7 MPa → σcm/p0 puts this in light/non-squeezing. 10-20 cm needs p0≈5-12 MPa (≈300-500 m cover). Decision: re-cut the small box from a deeper centerline station, or accept that *this* section is genuinely low-squeeze. **This single decision likely accounts for most of the 40-60x gap.**
- **B. Equivalent lining E0**: confirm modeling the liner with cracked-RC effective E (~3-8 GPa) instead of intact 25 GPa. Defensible as "it cracks," but it's a constitutive interpretation Wade should bless.
- **C. Time window**: 120 days cannot produce creep-dominated 10-20 cm. If 10-20 cm is meant to be a long-term (multi-year) state, the run horizon must extend; if it's a construction-stage number, it's drive/stress-dominated, reinforcing decision A.
- **D. eta**: present the `diag_etam` 300x-no-effect result as proof that eta stays at 6e15 — no action, just confirmation we won't cheat there.

**Do NOT do (cheating):** lower eta to hit the target (proven ineffective anyway), inflate K0 beyond geological justification, lower c/φ, or switch off Burgers-Mohr. The honest path to 10-20 cm runs through *correct in-situ stress (depth), a physically-cracked lining, and adequate time/drive* — not through softening the dashpot.

**Honest one-liner for Wade:** "At the stress this section actually carries (sub-MPa to 1.7 MPa, ~100-200 m cover), 3 mm is the physically-correct answer — it's light-squeezing ground. 10-20 cm requires the deeper, higher-stress design section (5-12 MPa) and/or longer time; the eta test proves creep viscosity is not the missing 50x. Tonight I'll quantify the honestly-closable part via a cracked-lining (E≈5 GPa) re-run; the section-depth call is yours."

Verified source files (all absolute):
- `C:\Users\Wade\Desktop\Tunnel_TX\04_InitialBalance\parameter.f3dat` (all material/creep/lining params)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\small_driven.log` (staged convergence + shell stress)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\diag_etam.log` (eta_m=2e13 sensitivity — decisive null result)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\diag_zone_y885.txt` (tunnel-horizon stress 0.3-1.7 MPa)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\small_tcrit_y885.txt` (creep threshold field 0.35-0.61, mostly sub-0.6)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\small_drive_residual.txt` (box-face deformational residual 5-26 mm)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\diag_thresh.f3dat` (threshold formula: q=(s1−s3)/2 vs q_th=thr·(c·cosφ+pmean·sinφ))
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\large_slope_surface.txt` (surface z 1534-2186 over tunnel crown z~1797 → ~100-200 m cover)
- `C:\Users\Wade\Desktop\Tunnel_TX\05_One_Way_Simulation\codex_insitu.txt`, `codex_insitu2.txt` (in-situ tension/settlement concerns supporting the depth/stress re-audit)