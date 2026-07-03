"""small_idw.py -- IDW-map the LARGE model's per-stage CUMULATIVE displacement
(lg_bc_s1..s4.txt, 'x y z dx dy dz', from extract_large_bc.f3dat) onto the SMALL
model's box-face gridpoints (small_bnd.txt, 'id x y z', from export_small_bnd.f3dat)
-> small_drive.txt ('id d1x..d4z' per-stage CUMULATIVE displacement keyed by gp.id).

small_driven.f3dat reads small_drive.txt, gp.find(id), tags each box-face gp
'driven' and stores its 4 per-stage cumulative targets in gp.extra(g,1..4); the
driven gps are velocity-fixed and ramped to gp.extra(g,stg) each stage.

DECISION (Wade rule #2 + IDW-pipeline brief): write the FULL cumulative
displacement (NOT the rigid-body residual). For an axis-aligned box submodel the
boundary condition IS the parent's full cumulative deformation field -- that is
where the ~10-20 cm tunnel squeeze comes from. Rigid subtraction is only for the
COUPLED curved lining interface (couple_idw.py, prevents rotation-only cracking).
The small model's in-situ stress is already embedded in Small_Initial; the full
IDW box-face displacement adds the large model's cumulative slope-creep squeeze
on top. The rigid decomposition is still REPORTED + written (small_drive_residual.txt)
as a diagnostic, mirroring couple_idw.py, but is NOT used to drive.

k=8 nearest IDW, 1/d^2 weighting -- identical kernel to couple_idw.py.
Run with C:/Users/Wade/anaconda3/python.exe (numpy [+ scipy optional]). cwd = 05.
"""
import numpy as np
try:
    from scipy.spatial import cKDTree
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False


def load_bc(fn):
    """lg_bc_sN.txt: 'x y z dx dy dz' per row, 1 header line (extract_large_bc.f3dat:12)."""
    d = np.loadtxt(fn, skiprows=1)
    return d[:, :3], d[:, 3:6]


# --- large-model per-stage CUMULATIVE displacement fields (4 stages) ---
print("Loading large-model per-stage cumulative displacement (lg_bc_s1..s4.txt)...")
P, D1 = load_bc('lg_bc_s1.txt')
_, D2 = load_bc('lg_bc_s2.txt')
_, D3 = load_bc('lg_bc_s3.txt')
_, D4 = load_bc('lg_bc_s4.txt')
print(f"  large box-region source gps: {len(P)}")

# --- small-model box-face target gridpoints (id x y z) ---
print("Loading small-model box-face gridpoints (small_bnd.txt)...")
bnd = np.loadtxt('small_bnd.txt', skiprows=1)
if bnd.ndim == 1:
    bnd = bnd[None, :]
ids = bnd[:, 0].astype(np.int64)
Q = bnd[:, 1:4]
print(f"  small box-face target gps: {len(ids)}")

# --- k=8 nearest-neighbour IDW, 1/d^2 (couple_idw.py:29-49 kernel) ---
k = 8
if HAVE_SCIPY:
    print("Building cKDTree on large-model source points...")
    tree = cKDTree(P)
    dist, idx = tree.query(Q, k=k)
else:
    print("scipy unavailable -> brute-force kNN")
    idx = np.zeros((len(Q), k), dtype=np.int64)
    dist = np.zeros((len(Q), k))
    for i, q in enumerate(Q):
        d2 = ((P - q) ** 2).sum(axis=1)
        nn = np.argpartition(d2, k)[:k]
        idx[i] = nn
        dist[i] = np.sqrt(d2[nn])

eps = 1e-9
w = 1.0 / (dist ** 2 + eps)
wsum = w.sum(axis=1, keepdims=True)


def idw(D):
    vals = D[idx]                       # (Nbnd, k, 3)
    return (w[:, :, None] * vals).sum(axis=1) / wsum


print("IDW interpolating the 4 cumulative stage fields onto the box faces...")
T = [idw(D1), idw(D2), idw(D3), idw(D4)]


# --- rigid-body decomposition (DIAGNOSTIC only; couple_idw.py:55-72 verbatim) ---
def rigid_decompose(Q, D):
    rc = Q.mean(axis=0)
    r = Q - rc
    t = D.mean(axis=0)                       # best-fit translation = mean disp
    Dp = D - t
    A = np.zeros((3, 3))
    b = np.zeros(3)
    for ri, di in zip(r, Dp):
        K = np.array([[0, ri[2], -ri[1]],    # K @ omega == omega x ri
                      [-ri[2], 0, ri[0]],
                      [ri[1], -ri[0], 0]])
        A += K @ K.T                         # K^T K
        b -= K @ di                          # K^T di (K skew => K.T = -K)
    omega = np.linalg.lstsq(A, b, rcond=None)[0]
    rigid = t + np.cross(np.broadcast_to(omega, r.shape), r)
    resid = D - rigid
    return resid, t, omega, rigid


print("\n--- DIAGNOSTIC: rigid-body decomposition (reported, NOT used to drive) ---")
Tr = []
for nm, Ti in zip(['s1', 's2', 's3', 's4'], T):
    resid, t, omega, rigid = rigid_decompose(Q, Ti)
    Tr.append(resid)
    magT = np.sqrt((Ti ** 2).sum(1))
    magR = np.sqrt((resid ** 2).sum(1))
    magRig = np.sqrt((rigid ** 2).sum(1))
    print(f"  {nm}: |t|={np.linalg.norm(t)*1000:.3f}mm |omega|={np.linalg.norm(omega):.3e}rad "
          f"| total RMS={np.sqrt((magT**2).mean())*1000:.3f} "
          f"rigid RMS={np.sqrt((magRig**2).mean())*1000:.3f} "
          f"residual RMS={np.sqrt((magR**2).mean())*1000:.3f} mm  "
          f"(rigid frac={np.sqrt((magRig**2).mean())/np.sqrt((magT**2).mean()):.2f})")

# --- PRIMARY OUTPUT: FULL cumulative displacement (drives small_driven.f3dat) ---
print("\nWriting small_drive.txt (FULL cumulative per-stage IDW field)...")
out = np.column_stack([ids] + T)
with open('small_drive.txt', 'w') as f:
    f.write('id d1x d1y d1z d2x d2y d2z d3x d3y d3z d4x d4y d4z   # FULL cumulative displacement (no rigid subtraction)\n')
    for row in out:
        f.write(f"{int(row[0])} " + " ".join(f"{v:.8e}" for v in row[1:]) + "\n")

# --- REFERENCE OUTPUT: deformational residual (rigid subtracted; NOT for driving) ---
outr = np.column_stack([ids] + Tr)
with open('small_drive_residual.txt', 'w') as f:
    f.write('id r1x r1y r1z r2x r2y r2z r3x r3y r3z r4x r4y r4z   # DEFORMATIONAL residual (rigid subtracted, reference only)\n')
    for row in outr:
        f.write(f"{int(row[0])} " + " ".join(f"{v:.8e}" for v in row[1:]) + "\n")

print(f"WROTE small_drive.txt (FULL, primary) + small_drive_residual.txt (reference): {len(ids)} gps x 4 stages")

# --- summaries: full magnitude + per-stage increments (what each ramp applies) ---
print("\n--- FULL box-face displacement magnitude per stage (drives small model) ---")
for nm, Ti in zip(['s1', 's2', 's3', 's4'], T):
    mag = np.sqrt((Ti ** 2).sum(axis=1))
    print(f"  {nm}: min={mag.min()*1000:.3f} mm  max={mag.max()*1000:.3f} mm  mean={mag.mean()*1000:.3f} mm")

print("\n--- cumulative-to-cumulative increments (per-stage drive ramp) ---")
inc1 = np.sqrt((T[0] ** 2).sum(axis=1))
print(f"  insitu->s1: max={inc1.max()*1000:.3f} mm  mean={inc1.mean()*1000:.3f} mm")
for i in range(1, 4):
    dinc = T[i] - T[i - 1]
    m = np.sqrt((dinc ** 2).sum(axis=1))
    print(f"  s{i}->s{i+1}: max={m.max()*1000:.3f} mm  mean={m.mean()*1000:.3f} mm")

print("\n[END small_idw.py]")
