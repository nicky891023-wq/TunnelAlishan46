"""gen_large_geo_v3.py -- Alishan #46 LARGE model, NEW-geology (v3) mesh inputs.

Stage 1 of the large_tet rebuild (2026-06-13).  Geology = Wade's v2 logic
(qc_geo_v2.py / geo_surfaces_v2.npz):
  layer1 clv = DEM~F01, ONLY inside the F01 footprint
  layer2 ssh = top_rock~F02_Ssh   (top_rock = F01 in fp, DEM outside)
  layer3 bed = F02_Ssh~F03_bedrock-up
  layer4 base= F03~z=800
  clip rule (d): f01=min(F01,DEM); f02=min(F02_Ssh,top_rock); f03=min(F03,f02)

This script produces, on a UNIFORM 25 m grid (81 x 85):
  * TRUE clipped fields  dem / t1(=top_rock) / f02 / f03  -> cell labelling
  * FRAGMENT surfaces    s1z / s2z / s3z : equal to the true surfaces wherever
    the layer has >= G (12 m) of room; in pinch zones they DETACH and dive
    (distance-ramp, smoothed) to ~DIVE (36 m) artificial gaps -> mesh-healthy
    bands everywhere, NO slivers.  Labels use the true fields, so the
    artificial parts are geology-neutral (same trick as the proven
    build_large_tet.py rank blending, adapted to the new local-clv logic).
  * a 3D Structured size grid (large_size_v3.dat) for gmsh:
      size = min over surfaces of (near-size + 0.5*|dz|),  near-size =
             min(0.85*gap, sag-safe size), clipped [8,50]
      min with export-box term 17 + 0.35*dist(box x[1150,1450] y[750,1050]
             z[1600,1900])  -> <= 20 m in the export box
      far cap 50 m.
  * cross-check against geo_surfaces_v2.npz at common nodes (same sampler ->
    must agree exactly).

PINCH DECISIONS (recorded):
  - fragment-geometry minimum band G = 12 m ("撐開" applied to the FRAGMENT
    surfaces only); true layers thinner than ~half the local cell size merge
    into the neighbour by the centroid labelling ("合併"), thicker thin layers
    are kept, thickness-quantised at the local cell size.  No zero-volume or
    sliver bands can exist geometrically.
  - in pinch interiors the artificial surfaces dive to ~36 m gaps so the
    1.9 km^2 ssh-pinch / 0.88 km^2 bed-pinch interiors mesh at ~30-50 m.

Run with C:/Users/Wade/anaconda3/python.exe, serially (no parallel gmsh).
"""
from __future__ import annotations
import os, sys, json
import numpy as np
import scipy.ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from geo_sampler import Surf                     # exact STL sampler (fold-safe)

X0, X1, Y0, Y1, ZB = 0.0, 2000.0, -100.0, 2000.0, 800.0
DX = 25.0                                        # uniform sampling grid
G    = 12.0                                      # min fragment band gap (m)
DIVE = 36.0                                      # comfortable artificial gap (m)
SLOPE = 0.30                                     # dive ramp (m per m horiz.)
# export box (ANALYSIS_PIPELINE Step 2)
EBX = (1150.0, 1450.0); EBY = (750.0, 1050.0); EBZ = (1600.0, 1900.0)
SIZE_BOX, BOX_GROW = 12.0, 0.35                  # <=20 m EDGES in box (gmsh
                                                 # Delaunay edge overshoot ~1.3x)
SIZE_MIN, SIZE_FAR = 8.0, 50.0                   # global floor / far cap
VSLOPE = 0.5                                     # size growth away from surface
DZ_SIZE = 10.0                                   # size-grid vertical step

NPZ_OUT  = os.path.join(HERE, 'large_geo_v3.npz')
SIZE_OUT = os.path.join(HERE, 'large_size_v3.dat')


def sag_field(Z, h):
    """half second-difference = chord sag over one cell pair (m) at spacing h,
    max of x/y directions, dilated 1 cell for safety."""
    s = np.zeros_like(Z)
    s[1:-1, :] = np.abs(Z[2:, :] - 2*Z[1:-1, :] + Z[:-2, :]) / 2.0
    sy = np.zeros_like(Z)
    sy[:, 1:-1] = np.abs(Z[:, 2:] - 2*Z[:, 1:-1] + Z[:, :-2]) / 2.0
    s = np.maximum(s, sy)
    return ndi.maximum_filter(s, size=3)


def main():
    xs = np.arange(X0, X1 + 0.1, DX)             # 81
    ys = np.arange(Y0, Y1 + 0.1, DX)             # 85
    Xg, Yg = np.meshgrid(xs, ys, indexing='ij')
    print(f"grid {len(xs)}x{len(ys)} @ {DX} m")

    # ---------------- sample + clip (EXACT qc_geo_v2 rule) ------------------
    # F01_fix01_edit.stl = closed colluvium BODY -> sample bottom face (clv
    # base); the others are single-valued heightfields (top sheet).
    S = {k: Surf(os.path.join(HERE, fn), sheet='bottom' if k == 'F01' else 'top')
         for k, fn in
         [('DEM', '../input/DEM.stl'), ('F01', '../input/F01.stl'),
          ('F02n', '../input/F02.stl'), ('F03n', '../input/F03.stl')]}
    dem, vdem = S['DEM'].sample(Xg, Yg)
    f01r, v01 = S['F01'].sample(Xg, Yg)
    f02r, v02 = S['F02n'].sample(Xg, Yg)
    f03r, v03 = S['F03n'].sample(Xg, Yg)
    assert vdem.all(), f"DEM holes: {(~vdem).sum()}"
    assert v02.all(),  f"F02_Ssh in-domain holes: {(~v02).sum()} (do NOT extrapolate)"
    assert v03.all(),  f"F03_bedrock-up in-domain holes: {(~v03).sum()}"
    f01c = np.where(v01, np.minimum(f01r, dem), np.nan)
    t1   = np.where(v01, f01c, dem)              # top_rock (true clv bottom)
    f02  = np.minimum(f02r, t1)
    f03  = np.minimum(f03r, f02)

    # ---------------- cross-check vs geo_surfaces_v2.npz --------------------
    d2 = np.load(os.path.join(HERE, '..', 'input', 'geo_surfaces_v2.npz'), allow_pickle=True)
    ix = np.searchsorted(xs, d2['xs']); iy = np.searchsorted(ys, d2['ys'])
    assert np.allclose(xs[ix], d2['xs']) and np.allclose(ys[iy], d2['ys'])
    for k, F in [('dem', dem), ('top_rock', t1), ('f02', f02), ('f03', f03)]:
        ref = d2[k]; new = F[np.ix_(ix, iy)]
        m = ~np.isnan(ref)
        dmax = np.nanmax(np.abs(new[m] - ref[m]))
        print(f"  cross-check vs v2 npz: {k:9s} max|dz| = {dmax:.6f} m")
        assert dmax < 1e-6, f"{k} disagrees with recon QC npz"
    m01_ref = d2['mask_f01']
    assert (v01[np.ix_(ix, iy)] == m01_ref).all(), "F01 footprint mask mismatch"

    # ---------------- layer thickness + pinch census -------------------------
    thk = {'clv': dem - t1, 'ssh': t1 - f02, 'bed': f02 - f03, 'base': f03 - ZB}
    cell = DX * DX
    dom = thk['clv'].size * cell
    print("\nTRUE clipped thickness (m) + pinch census (area km^2 / % domain):")
    for nm in ['clv', 'ssh', 'bed', 'base']:
        t = thk[nm]
        z0 = (t <= 1e-9).sum() * cell
        a2 = ((t > 1e-9) & (t < 2)).sum() * cell
        aG = ((t > 1e-9) & (t < G)).sum() * cell
        print(f"  {nm:4s} mean {t.mean():7.2f} min {t.min():7.2f} max {t.max():8.2f}"
              f" | zero {z0/1e6:6.3f} ({100*z0/dom:4.1f}%)"
              f" | 0<t<2m {a2/1e6:6.3f} ({100*a2/dom:4.1f}%)"
              f" | 0<t<G {aG/1e6:6.3f} ({100*aG/dom:4.1f}%)")

    # ---------------- fragment surfaces: exact-where-healthy + dive ---------
    D1t, D2t, D3t = dem - t1, dem - f02, dem - f03
    Dbot = dem - ZB

    def finish(d_exact_mask, d_raw, dmin_field):
        ds = ndi.gaussian_filter(d_raw, sigma=2.0)
        d = np.where(d_exact_mask, d_raw, ds)
        return np.maximum(d, dmin_field)

    # S1 (clv bottom / rock top)
    h1 = D1t >= G
    dist1 = ndi.distance_transform_edt(~h1, sampling=DX)
    cap1 = np.where(D2t >= 3*G, np.clip(0.5*D2t, G, DIVE),
            np.where(D3t >= 3*G, np.clip(D3t/3.0, G, DIVE),
                     np.clip(0.25*Dbot, G, DIVE)))
    d1 = np.where(h1, D1t, np.minimum(G + SLOPE*dist1, cap1))
    d1 = finish(h1, d1, np.full_like(d1, G))

    # S2 (ssh bottom)
    floor2 = d1 + G
    h2 = D2t >= floor2
    dist2 = ndi.distance_transform_edt(~h2, sampling=DX)
    cap2 = np.maximum(floor2,
                      np.minimum(0.5*(d1 + np.maximum(D3t, d1 + 2*G)),
                                 d1 + DIVE))
    d2v = np.where(h2, D2t, np.minimum(floor2 + SLOPE*dist2, cap2))
    d2v = finish(h2, d2v, floor2)

    # S3 (bed bottom)
    floor3 = d2v + G
    h3 = D3t >= floor3
    dist3 = ndi.distance_transform_edt(~h3, sampling=DX)
    cap3 = np.minimum(floor3 + DIVE, Dbot - 50.0)
    d3v = np.where(h3, D3t, np.minimum(floor3 + SLOPE*dist3, cap3))
    d3v = finish(h3, d3v, floor3)

    # strict cascade re-assert
    d1 = np.maximum(d1, G)
    d2v = np.maximum(d2v, d1 + G)
    d3v = np.maximum(d3v, d2v + G)
    assert (Dbot - d3v).min() > 50, "S3 too deep"
    s1z, s2z, s3z = dem - d1, dem - d2v, dem - d3v

    ex1 = h1 & (np.abs(d1 - D1t) < 1e-6)
    ex2 = h2 & (np.abs(d2v - D2t) < 1e-6)
    ex3 = h3 & (np.abs(d3v - D3t) < 1e-6)
    print("\nFRAGMENT surfaces: exact-conformal coverage (of domain area):")
    print(f"  S1 == true top_rock : {100*ex1.mean():5.1f}%   "
          f"(clv pinched/absent elsewhere -> artificial, geology-neutral)")
    print(f"  S2 == true f02      : {100*ex2.mean():5.1f}%")
    print(f"  S3 == true f03      : {100*ex3.mean():5.1f}%")
    in_fp_healthy = h1.sum()
    print(f"  [clv >= G inside fp: {in_fp_healthy*cell/1e6:.3f} km^2 -> exact clv base]")
    gaps = np.stack([d1, d2v - d1, d3v - d2v, Dbot - d3v])
    print(f"  fragment gap check: min DEM-S1 {gaps[0].min():.2f}  S1-S2 "
          f"{gaps[1].min():.2f}  S2-S3 {gaps[2].min():.2f}  S3-bot {gaps[3].min():.2f} (all >= {G})")

    # ---------------- 3D size grid ------------------------------------------
    surfs = [dem, s1z, s2z, s3z]
    gap_of = [d1, np.minimum(d1, d2v - d1), np.minimum(d2v - d1, d3v - d2v),
              np.minimum(d3v - d2v, Dbot - d3v)]
    near = []
    for Zs, gp in zip(surfs, gap_of):
        sg = np.maximum(sag_field(Zs, DX), 0.3)
        h_sag = DX * np.sqrt(0.35 * gp / sg)         # sag(h)=sg*(h/DX)^2 <=0.35*gap
        near.append(np.clip(np.minimum(0.85 * gp, h_sag), SIZE_MIN, SIZE_FAR))
    zs_lev = np.arange(ZB - 10.0, 2210.0 + 0.1, DZ_SIZE)
    nzl = len(zs_lev)
    print(f"\nsize grid {len(xs)}x{len(ys)}x{nzl} (dz={DZ_SIZE})")
    SZ = np.full((len(xs), len(ys), nzl), SIZE_FAR)
    for Zs, a in zip(surfs, near):
        dz = np.abs(zs_lev[None, None, :] - Zs[:, :, None])
        SZ = np.minimum(SZ, a[:, :, None] + VSLOPE * dz)
    # export-box term
    dxb = np.maximum(np.maximum(EBX[0] - Xg, Xg - EBX[1]), 0.0)
    dyb = np.maximum(np.maximum(EBY[0] - Yg, Yg - EBY[1]), 0.0)
    dzb = np.maximum(np.maximum(EBZ[0] - zs_lev[None, None, :],
                                zs_lev[None, None, :] - EBZ[1]), 0.0)
    dbox = np.sqrt(dxb[:, :, None]**2 + dyb[:, :, None]**2 + dzb**2)
    SZ = np.minimum(SZ, SIZE_BOX + BOX_GROW * dbox)
    SZ = np.clip(SZ, SIZE_MIN, SIZE_FAR)
    in_box = (dbox[:, :, :] == 0.0)
    print(f"  size in export box: min {SZ[in_box].min():.1f} max {SZ[in_box].max():.1f}"
          f"  | global min {SZ.min():.1f} max {SZ.max():.1f}")
    with open(SIZE_OUT, 'w') as f:
        f.write(f"{xs[0]} {ys[0]} {zs_lev[0]}\n{DX} {DX} {DZ_SIZE}\n"
                f"{len(xs)} {len(ys)} {nzl}\n")
        np.savetxt(f, SZ.reshape(-1, 1), fmt='%.3f')
    print(f"wrote {SIZE_OUT}")

    # ---------------- save npz ----------------------------------------------
    meta = dict(date='2026-06-13', grid=f'uniform {DX} m, indexing ij',
                G=G, DIVE=DIVE, slope=SLOPE,
                export_box=[EBX, EBY, EBZ], size=[SIZE_MIN, SIZE_BOX, SIZE_FAR],
                rule='s1/s2/s3 = true t1/f02/f03 where layer room >= G, '
                     'else detach+dive (geology-neutral; labels from true fields)',
                pinch='G=12 m min fragment band; true thickness < ~half cell '
                      'merges by centroid labelling; no geometric slivers')
    np.savez(NPZ_OUT, xs=xs, ys=ys, dem=dem,
             t1=t1, f02=f02, f03=f03, mask_f01=v01,
             s1z=s1z, s2z=s2z, s3z=s3z,
             ex1=ex1, ex2=ex2, ex3=ex3, zb=np.array(ZB),
             meta=np.array(json.dumps(meta)))
    print(f"wrote {NPZ_OUT}")


if __name__ == '__main__':
    main()
