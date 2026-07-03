"""plot_large_init.py -- render-verify Large_Initial y~900 slice: szz, sxx, pore-pressure.
Physical checks: szz/sxx increase (more compressive) with depth; pp hydrostatic below
the W-110 water table, ~0 above. Out: qa_large_init.png"""
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.loadtxt('slice_large_init.txt', skiprows=1)
x, z, szz, sxx, pp = d[:,0], d[:,1], d[:,2], d[:,3], d[:,4]
fig, axs = plt.subplots(1, 3, figsize=(19, 6.5))
fig.suptitle('Large_Initial (260529-method: fluid W-110 steady-state -> solve elastic) | y~900 slice', fontsize=12)
for ax, c, ttl, cmap in [(axs[0], szz/1e6, 'szz (MPa, comp<0)', 'jet'),
                          (axs[1], sxx/1e6, 'sxx (MPa, comp<0)', 'jet'),
                          (axs[2], pp/1e6, 'pore pressure (MPa)', 'viridis')]:
    s = ax.scatter(x, z, c=c, s=3, cmap=cmap)
    ax.set_aspect('equal'); ax.set_title(ttl); ax.set_xlabel('x'); ax.set_ylabel('z')
    plt.colorbar(s, ax=ax, shrink=0.8)
plt.tight_layout(rect=[0,0,1,0.96]); plt.savefig('qa_large_init.png', dpi=90)
print('saved qa_large_init.png')
print(f'  n={len(x)} z[{z.min():.0f},{z.max():.0f}]  szz[{szz.min()/1e6:.2f},{szz.max()/1e6:.2f}]MPa'
      f'  sxx[{sxx.min()/1e6:.2f},{sxx.max()/1e6:.2f}]MPa  pp[{pp.min()/1e6:.2f},{pp.max()/1e6:.2f}]MPa')
# quick physical check: mean szz in top third vs bottom third
zt = np.percentile(z, 66); zb = np.percentile(z, 33)
print(f'  szz mean: top(z>{zt:.0f})={szz[z>zt].mean()/1e6:.2f}MPa  bottom(z<{zb:.0f})={szz[z<zb].mean()/1e6:.2f}MPa (bottom should be more negative)')
print(f'  pp mean: top={pp[z>zt].mean()/1e6:.2f}MPa  bottom={pp[z<zb].mean()/1e6:.2f}MPa (bottom higher)')
