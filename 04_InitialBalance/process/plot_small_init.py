"""plot_small_init.py -- render-verify Small_Initial y~885 slice: szz, sxx, pore-pressure,
plastic state (blue=shear red=tension). 260529-method: null lining -> fluid W-110 ->
bare relax 1e-4 -> elastic dkt-csth shell -> solve 1e-5. Out: qa_small_init.png"""
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
d = np.loadtxt('slice_small_init.txt', skiprows=1)
x, z, szz, sxx, pp, state = d[:,0], d[:,1], d[:,2], d[:,3], d[:,4], d[:,5].astype(int)
fig, axs = plt.subplots(2, 2, figsize=(14, 12))
fig.suptitle('Small_Initial (260529-method: null lining -> fluid W-110 -> bare relax 1e-4 -> shell -> solve 1e-5) | y~885', fontsize=11)
def panel(ax, c, ttl, cmap, clip=None):
    cc = np.clip(c, *clip) if clip else c
    s = ax.scatter(x, z, c=cc, s=5, cmap=cmap); ax.set_aspect('equal')
    ax.set_title(ttl); ax.set_xlabel('x'); ax.set_ylabel('z'); plt.colorbar(s, ax=ax, shrink=0.8)
panel(axs[0,0], szz/1e6, 'szz (MPa, comp<0)', 'jet')
panel(axs[0,1], sxx/1e6, 'sxx (MPa, comp<0)', 'jet')
panel(axs[1,0], pp/1e6, 'pore pressure (MPa)', 'viridis')
# plastic state: bit1=shear-n bit2=tension-n bit4=shear-p bit8=tension-p; shear=&5 tension=&10
shear = (state & 5) > 0; tens = (state & 10) > 0; elas = ~(shear | tens)
ax = axs[1,1]
ax.scatter(x[elas], z[elas], s=4, c='lightgray', label='elastic')
ax.scatter(x[shear & ~tens], z[shear & ~tens], s=5, c='blue', label=f'shear ({int((shear&~tens).sum())})')
ax.scatter(x[tens], z[tens], s=7, c='red', label=f'tension ({int(tens.sum())})')
ax.set_aspect('equal'); ax.set_title('plastic state around bore (blue=shear red=tension)')
ax.set_xlabel('x'); ax.set_ylabel('z'); ax.legend(loc='upper right', fontsize=8)
plt.tight_layout(rect=[0,0,1,0.97]); plt.savefig('qa_small_init.png', dpi=90)
print('saved qa_small_init.png')
print(f'  n={len(x)} szz[{szz.min()/1e6:.2f},{szz.max()/1e6:.2f}]MPa sxx[{sxx.min()/1e6:.2f},{sxx.max()/1e6:.2f}]MPa'
      f' pp[{pp.min()/1e6:.3f},{pp.max()/1e6:.3f}]MPa')
print(f'  plastic: shear={int((shear&~tens).sum())} tension={int(tens.sum())} elastic={int(elas.sum())} / {len(x)}')
