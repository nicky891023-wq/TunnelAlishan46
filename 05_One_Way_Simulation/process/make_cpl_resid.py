"""make_cpl_resid.py -- rigid-body removal for the small->coupled drive (Phase C).

Same Kabsch/least-squares logic + strain-consistency gate as make_resid.py, applied
to cpl_bnd_sNN.txt (couple-box boundary bands exported from ss_NN). Rigid motion of
the 40 m couple box does zero work on the lining (bonded inside, moves with the box);
only the deformational residual loads it. Run from 05/process/.
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
        A[3*i:3*i+3, 3:6] = np.array([[0.0, rz, -ry], [-rz, 0.0, rx], [ry, -rx, 0.0]])
    sol, *_ = np.linalg.lstsq(A, U.reshape(-1), rcond=None)
    t, om = sol[:3], sol[3:]
    return U - (t + np.cross(np.broadcast_to(om, R.shape), R))

def mean_strain(X, U):
    rc = X.mean(axis=0)
    R = X - rc
    G = np.zeros((3, 3))
    M = np.linalg.pinv(R.T @ R)
    for j in range(3):
        G[j] = M @ (R.T @ (U[:, j] - U[:, j].mean()))
    return 0.5 * (G + G.T)

files = sorted(glob.glob('cpl_bnd_s??.txt'))
assert files, 'no cpl_bnd_sNN.txt found (run from 05/process)'
print(f'{"stage":8s} {"full med/max (mm)":>20s} {"resid med/max (mm)":>20s} {"strain gate":>12s}')
for f in files:
    d = np.loadtxt(f, skiprows=1)
    X, U = d[:, 0:3], d[:, 3:6]
    resid = fit_rigid(X, U)
    gate = np.abs(mean_strain(X, U) - mean_strain(X, resid)).max()
    assert gate < 1e-9, f'{f}: strain gate FAILED ({gate:.2e})'
    mf = np.linalg.norm(U, axis=1) * 1000
    mr = np.linalg.norm(resid, axis=1) * 1000
    out = f.replace('cpl_bnd_s', 'cpl_resid_s')
    with open(out, 'w') as fh:
        fh.write('x y z dx dy dz  # rigid-removed residual (small->coupled)\n')
        for (x, y, z), (ux, uy, uz) in zip(X, resid):
            fh.write(f'{x:.8e} {y:.8e} {z:.8e} {ux:.8e} {uy:.8e} {uz:.8e}\n')
    print(f'{f[9:12]:8s} {np.median(mf):8.2f}/{mf.max():8.2f} {np.median(mr):8.2f}/{mr.max():8.2f} {gate:12.2e} -> {out}')
print('\nall stages OK.')
