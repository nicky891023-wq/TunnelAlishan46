"""make_resid.py -- per-stage rigid-body removal (Kabsch/least-squares) for lg_disp_sNN.txt.

For each stage file (x y z dx dy dz, cumulative displacement of the small-model box
region exported by large_staged.f3dat), fit the best rigid motion
    u_rigid(r) = t + omega x (r - rc)
by linear least squares over all points, subtract it, and write
lg_disp_resid_sNN.txt with the same 6-column format. The residual (deformational)
field is what drives the small model (rigid translation/rotation produces zero
strain, hence zero tunnel squeezing -- see COUPLING_METHOD_PROPOSAL.md D3).

GATE G3 (strain consistency): the mean strain tensor over the box computed from the
full field and from the residual field must match (rigid removal is strain-neutral).
Both are computed from the same least-squares displacement-gradient fit and printed;
per-stage max component difference is asserted < 1e-9.
"""
import glob
import numpy as np

def fit_rigid(X, U):
    rc = X.mean(axis=0)
    R = X - rc
    n = len(X)
    A = np.zeros((3 * n, 6))
    for i, (rx, ry, rz) in enumerate(R):
        A[3*i:3*i+3, 0:3] = np.eye(3)
        A[3*i:3*i+3, 3:6] = np.array([[0.0, rz, -ry],
                                      [-rz, 0.0, rx],
                                      [ry, -rx, 0.0]])
    sol, *_ = np.linalg.lstsq(A, U.reshape(-1), rcond=None)
    t, om = sol[:3], sol[3:]
    Urig = t + np.cross(np.broadcast_to(om, R.shape), R)
    return U - Urig, t, om

def mean_strain(X, U):
    """Least-squares uniform displacement-gradient fit -> symmetric strain."""
    rc = X.mean(axis=0)
    R = X - rc
    G = np.zeros((3, 3))
    M = np.linalg.pinv(R.T @ R)
    for j in range(3):
        G[j] = M @ (R.T @ (U[:, j] - U[:, j].mean()))
    return 0.5 * (G + G.T)

files = sorted(glob.glob('lg_disp_s??.txt'))
assert files, 'no lg_disp_sNN.txt found (run from 05_One_Way_Simulation)'
print(f'{"stage":8s} {"full med/max (mm)":>20s} {"resid med/max (mm)":>20s} {"rigid frac":>10s} {"strain gate":>12s}')
for f in files:
    d = np.loadtxt(f, skiprows=1)
    X, U = d[:, 0:3], d[:, 3:6]
    resid, t, om = fit_rigid(X, U)
    e_full = mean_strain(X, U)
    e_res = mean_strain(X, resid)
    gate = np.abs(e_full - e_res).max()
    assert gate < 1e-9, f'{f}: strain-consistency gate FAILED ({gate:.2e})'
    mf = np.linalg.norm(U, axis=1) * 1000
    mr = np.linalg.norm(resid, axis=1) * 1000
    out = f.replace('lg_disp_s', 'lg_disp_resid_s')
    with open(out, 'w') as fh:
        fh.write('x y z dx dy dz  # rigid-removed deformational residual\n')
        for (x, y, z), (ux, uy, uz) in zip(X, resid):
            fh.write(f'{x:.8e} {y:.8e} {z:.8e} {ux:.8e} {uy:.8e} {uz:.8e}\n')
    rigid_frac = 1.0 - np.sqrt((mr**2).mean()) / max(np.sqrt((mf**2).mean()), 1e-30)
    print(f'{f[9:12]:8s} {np.median(mf):8.2f}/{mf.max():8.2f} {np.median(mr):8.2f}/{mr.max():8.2f} '
          f'{rigid_frac:10.3f} {gate:12.2e}  -> {out}')
print('\nall stages OK (strain gate passed); residual files written.')
