"""couple_idw.py -- IDW-map the small model's per-stage cumulative disp (bc_s1..4.txt) onto the
coupled model's outer boundary gridpoints (couple_bnd.txt) -> couple_bnd_disp.txt keyed by gp.id.
Run B (FLAC3D) reads couple_bnd_disp.txt, gp.find(id), drives each boundary gp to insitu+disp per
stage, solves equilibrium -> lining force-shares & cracks. k=8 nearest IDW (1/d^2)."""
import numpy as np
try:
    from scipy.spatial import cKDTree
    HAVE_SCIPY = True
except Exception:
    HAVE_SCIPY = False

def load_bc(fn):
    d = np.loadtxt(fn, skiprows=1)
    return d[:, :3], d[:, 3:6]

P, D1 = load_bc('bc_s1.txt')
_, D2 = load_bc('bc_s2.txt')
_, D3 = load_bc('bc_s3.txt')
_, D4 = load_bc('bc_s4.txt')
print(f"bc points: {len(P)}")

bnd = np.loadtxt('couple_bnd.txt', skiprows=1)
if bnd.ndim == 1:
    bnd = bnd[None, :]
ids = bnd[:, 0].astype(np.int64)
Q = bnd[:, 1:4]
print(f"boundary gps: {len(ids)}")

k = 8
if HAVE_SCIPY:
    tree = cKDTree(P)
    dist, idx = tree.query(Q, k=k)
else:  # brute force fallback
    print("scipy unavailable -> brute force kNN")
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

T = [idw(D1), idw(D2), idw(D3), idw(D4)]

# ---- rigid-body decomposition (Gate-0/Codex A(c)): subtract best-fit translation+rotation,
#      drive only the DEFORMATIONAL residual; report rigid magnitude. d ~ t + omega x (r-rc) ----
def rigid_decompose(Q, D):
    rc = Q.mean(axis=0)
    r = Q - rc
    t = D.mean(axis=0)                       # best-fit translation = mean disp
    Dp = D - t
    # solve omega (3) minimizing |Dp - omega x r|^2 ; build normal equations A omega = b
    A = np.zeros((3, 3)); b = np.zeros(3)
    for ri, di in zip(r, Dp):
        K = np.array([[0, ri[2], -ri[1]],    # K = -[ri]_x (negative skew): K @ omega == omega x ri directly
                      [-ri[2], 0, ri[0]],
                      [ri[1], -ri[0], 0]])
        # model Dp ~ K omega; normal eqns (K^T K) omega = K^T Dp.  K skew => K.T = -K.
        A += K @ K.T               # == K^T K
        b -= K @ di                # == K^T di (since K.T=-K); DO NOT flip to += (reintroduces wrong-omega bug)
    omega = np.linalg.lstsq(A, b, rcond=None)[0]
    rigid = t + np.cross(np.broadcast_to(omega, r.shape), r)
    resid = D - rigid
    return resid, t, omega, rigid

Tr = []
print("\n--- rigid-body decomposition (drive deformational residual) ---")
for nm, Ti in zip(['s1','s2','s3','s4'], T):
    resid, t, omega, rigid = rigid_decompose(Q, Ti)
    Tr.append(resid)
    magT = np.sqrt((Ti**2).sum(1)); magR = np.sqrt((resid**2).sum(1)); magRig = np.sqrt((rigid**2).sum(1))
    print(f"  {nm}: |t|={np.linalg.norm(t)*1000:.3f}mm |omega|={np.linalg.norm(omega):.3e}rad "
          f"| total RMS={np.sqrt((magT**2).mean())*1000:.3f} rigid RMS={np.sqrt((magRig**2).mean())*1000:.3f} "
          f"residual RMS={np.sqrt((magR**2).mean())*1000:.3f} mm  (rigid frac={np.sqrt((magRig**2).mean())/np.sqrt((magT**2).mean()):.2f})")

# drive the RESIDUAL (deformational). also keep the full field for reference.
out = np.column_stack([ids] + Tr)
with open('couple_bnd_disp.txt', 'w') as f:
    f.write('id d1x d1y d1z d2x d2y d2z d3x d3y d3z d4x d4y d4z   # DEFORMATIONAL RESIDUAL (rigid subtracted)\n')
    for row in out:
        f.write(f"{int(row[0])} " + " ".join(f"{v:.8e}" for v in row[1:]) + "\n")
outf = np.column_stack([ids] + T)
with open('couple_bnd_disp_full.txt', 'w') as f:
    f.write('id d1x..d4z  # FULL IDW field (rigid+deformational, reference)\n')
    for row in outf:
        f.write(f"{int(row[0])} " + " ".join(f"{v:.8e}" for v in row[1:]) + "\n")

print(f"\nWROTE couple_bnd_disp.txt (residual, drives coupled) + couple_bnd_disp_full.txt (ref): {len(ids)} gps")
for nm, Ti in zip(['s1', 's2', 's3', 's4'], T):
    mag = np.sqrt((Ti ** 2).sum(axis=1))
    print(f"  {nm}: boundary disp mag (mm) min={mag.min()*1000:.3f} max={mag.max()*1000:.3f} mean={mag.mean()*1000:.3f}")
# stage-to-stage increment magnitude (what actually drives each stage)
for i in range(1, 4):
    dinc = T[i] - T[i-1]
    m = np.sqrt((dinc**2).sum(axis=1))
    print(f"  incr s{i}->s{i+1}: mag (mm) max={m.max()*1000:.3f} mean={m.mean()*1000:.3f}")
inc1 = np.sqrt((T[0]**2).sum(axis=1))
print(f"  incr insitu->s1: mag (mm) max={inc1.max()*1000:.3f} mean={inc1.mean()*1000:.3f}")
