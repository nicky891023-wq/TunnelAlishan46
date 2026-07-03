"""plot_slice.py <slice_file.txt> <out.png> [title]
Render a y-slice export (x z szz sxx syy prinz state dispmag velmag) as a multi-panel
contour/scatter figure for initial-force-balance QA: szz, least-compressive principal
(tension>0), plastic state, displacement magnitude, velocity magnitude.
"""
import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fn = sys.argv[1] if len(sys.argv) > 1 else 'slice_small_initial.txt'
out = sys.argv[2] if len(sys.argv) > 2 else 'qa_slice.png'
title = sys.argv[3] if len(sys.argv) > 3 else fn

d = np.loadtxt(fn, skiprows=1)
x, z = d[:, 0], d[:, 1]
szz, sxx, syy, prinz, state, dispmag, velmag = d[:, 2], d[:, 3], d[:, 4], d[:, 5], d[:, 6], d[:, 7], d[:, 8]

fig, axs = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle(title, fontsize=13)

def panel(ax, c, ttl, cmap='jet', clip=None):
    cc = c.copy()
    if clip:
        cc = np.clip(cc, clip[0], clip[1])
    s = ax.scatter(x, z, c=cc, s=4, cmap=cmap)
    ax.set_aspect('equal'); ax.set_title(ttl); ax.set_xlabel('x'); ax.set_ylabel('z')
    plt.colorbar(s, ax=ax, shrink=0.8)

panel(axs[0,0], szz/1e6, 'szz (MPa, comp<0)', 'jet')
panel(axs[0,1], sxx/1e6, 'sxx (MPa)', 'jet')
panel(axs[0,2], prinz/1e6, 'least-compressive principal (MPa, tension>0)', 'seismic',
      clip=(-0.2, 0.2))
# plastic state decode: FLAC3D bits 1=shear-n 2=tension-n 4=shear-p 8=tension-p
# (verified vs GUI: state 4=shear-p, 5=shear-n+shear-p, 12=shear-p+tension-p).
si = state.astype(int)
shear = ((si & 5) > 0)     # shear-now OR shear-past
tens = ((si & 10) > 0)     # tension-now OR tension-past
elas = ~(shear | tens)
ax = axs[1,0]
ax.scatter(x[elas], z[elas], s=3, c='lightgray', label='elastic')
ax.scatter(x[shear & ~tens], z[shear & ~tens], s=4, c='blue', label=f'shear ({int((shear&~tens).sum())})')
ax.scatter(x[tens], z[tens], s=6, c='red', label=f'tension ({int(tens.sum())})')
ax.set_aspect('equal'); ax.set_xlabel('x'); ax.set_ylabel('z')
ax.set_title('plastic: blue=shear(squeezing) red=tension(minimized)'); ax.legend(loc='upper right', fontsize=7)
panel(axs[1,1], dispmag, 'displacement mag (mm)', 'viridis')
panel(axs[1,2], np.log10(velmag + 1e-12), 'log10 velocity mag (m/s; ~equilibrium if low)', 'plasma')

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig(out, dpi=85)
print(f'saved {out}')
print(f'  n_zones={len(x)}  szz[{szz.min()/1e6:.2f},{szz.max()/1e6:.2f}]MPa  '
      f'max_tension(prinz)={prinz.max()/1e6:.3f}MPa  plastic={int((state!=0).sum())}/{len(x)}  '
      f'max_disp={dispmag.max():.2f}mm  max_vel={velmag.max():.2e}')
