"""couple_qa_plot.py <prefix> -- Visual QA crack-pattern plots for a coupled stage.
Reads <prefix>_cracks.txt (x y z type diam age; type 1=tension 2=shear) written by
couple_qa_funcs.fis dump_cracks. Produces <prefix>_crack_pattern.png:
  (a) 3D scatter (tension red / shear blue),
  (b) y~885 cross-section slice in x-z plane with tunnel centre + nominal wall circle,
  (c) circumferential sector histogram (12 x 30deg).
Fixed axes/colors so stages are visually comparable (Wade Visual-QA rule)."""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa

CX, CZ = 1297.0, 1747.5      # tunnel axis (x,z); axis along y
R_NOM = 4.7                  # nominal wall radius (wz_outter mean-ish)
YSLICE, YBAND = 885.0, 2.0   # cross-section slice

pfx = sys.argv[1] if len(sys.argv) > 1 else 'sm_s1'
fn = f'{pfx}_cracks.txt'
try:
    d = np.loadtxt(fn, skiprows=1)
except Exception as e:
    print(f"cannot read {fn}: {e}")
    sys.exit(1)
if d.ndim == 1:
    d = d[None, :]
if len(d) == 0:
    print(f"{fn}: 0 cracks (no plot)")
    sys.exit(0)

x, y, z, typ = d[:, 0], d[:, 1], d[:, 2], d[:, 3].astype(int)
ten = typ == 1
sh = typ == 2
print(f"{pfx}: {len(d)} cracks  tension={ten.sum()} shear={sh.sum()}")

fig = plt.figure(figsize=(16, 5))

# (a) 3D scatter
ax = fig.add_subplot(1, 3, 1, projection='3d')
ax.scatter(x[ten], y[ten], z[ten], c='red', s=6, alpha=0.5, label=f'tension ({ten.sum()})')
ax.scatter(x[sh], y[sh], z[sh], c='blue', s=6, alpha=0.5, label=f'shear ({sh.sum()})')
ax.set_xlabel('x'); ax.set_ylabel('y'); ax.set_zlabel('z')
ax.set_title(f'{pfx} cracks 3D (n={len(d)})'); ax.legend(loc='upper right', fontsize=8)

# (b) y~885 slice
ax2 = fig.add_subplot(1, 3, 2)
msk = np.abs(y - YSLICE) <= YBAND
ax2.scatter(x[msk & ten], z[msk & ten], c='red', s=14, alpha=0.6, label='tension')
ax2.scatter(x[msk & sh], z[msk & sh], c='blue', s=14, alpha=0.6, label='shear')
th = np.linspace(0, 2 * np.pi, 100)
ax2.plot(CX + R_NOM * np.cos(th), CZ + R_NOM * np.sin(th), 'k--', lw=0.8, label=f'r={R_NOM}m')
ax2.plot(CX, CZ, 'k+', ms=10)
ax2.set_xlabel('x'); ax2.set_ylabel('z'); ax2.set_aspect('equal')
ax2.set_xlim(CX - 7, CX + 7); ax2.set_ylim(CZ - 7, CZ + 7)
ax2.set_title(f'y={YSLICE}±{YBAND} slice (n={msk.sum()})'); ax2.legend(fontsize=8)

# (c) sector histogram
ax3 = fig.add_subplot(1, 3, 3)
ang = np.degrees(np.arctan2(z - CZ, x - CX)) % 360
bins = np.arange(0, 361, 30)
ax3.hist([ang[ten], ang[sh]], bins=bins, stacked=True, color=['red', 'blue'],
         label=['tension', 'shear'])
ax3.set_xlabel('circumferential angle (deg, 0=+x/springline)')
ax3.set_ylabel('crack count'); ax3.set_xticks(bins)
ax3.set_title('sector distribution (30deg bins)'); ax3.legend(fontsize=8)

plt.tight_layout()
out = f'{pfx}_crack_pattern.png'
plt.savefig(out, dpi=110)
print(f"WROTE {out}")
