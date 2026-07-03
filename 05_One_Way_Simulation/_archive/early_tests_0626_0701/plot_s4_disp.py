# Where is the 5.28mm dmax? (tunnel ~0.1mm but global dmax 5.28mm). Plot y~885 disp slice.
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = np.loadtxt('s4_disp_y885.txt', skiprows=1)  # x z dmag dz
x, z, dmag, dz = D[:,0], D[:,1], D[:,2]*1000, D[:,3]*1000  # mm
print(f'gp@y885={len(x)}  dmag: max={dmag.max():.3f}mm at idx  x[{x.min():.0f},{x.max():.0f}] z[{z.min():.0f},{z.max():.0f}]')
im = np.argmax(dmag)
print(f'MAX disp at (x={x[im]:.1f}, z={z[im]:.1f}) = {dmag[im]:.3f}mm   tunnel center ~(1299,1747)')
# near-tunnel disp
import numpy as _np
r = _np.sqrt((x-1299)**2+(z-1747)**2)
print(f'disp within r<8m of tunnel: max={dmag[r<8].max():.3f}mm mean={dmag[r<8].mean():.3f}mm')
print(f'disp at r>20m (far/boundary): max={dmag[r>20].max():.3f}mm')
fig, ax = plt.subplots(1, 2, figsize=(22, 9))
sc0 = ax[0].scatter(x, z, c=dmag, s=10, cmap='hot_r', vmin=0, vmax=dmag.max())
plt.colorbar(sc0, ax=ax[0], label='|disp| (mm)')
ax[0].scatter([1299],[1747], marker='+', s=300, c='cyan', label='tunnel center')
ax[0].plot(x[im], z[im], 'co', ms=12, mfc='none', label=f'MAX {dmag[im]:.2f}mm')
ax[0].set_title(f'(1) |disp| @y885 -- max={dmag.max():.2f}mm; is it the tunnel or elsewhere?')
ax[0].set_aspect('equal'); ax[0].set_xlabel('x'); ax[0].set_ylabel('z'); ax[0].legend(fontsize=9)
sc1 = ax[1].scatter(x, z, c=dz, s=10, cmap='seismic', vmin=-dmag.max(), vmax=dmag.max())
plt.colorbar(sc1, ax=ax[1], label='disp_z (mm, +up/-down)')
ax[1].scatter([1299],[1747], marker='+', s=300, c='lime')
ax[1].set_title('(2) vertical disp_z @y885'); ax[1].set_aspect('equal'); ax[1].set_xlabel('x'); ax[1].set_ylabel('z')
fig.suptitle('05 standalone day120 displacement field @y~885 -- locating the 5.28mm dmax vs the ~0.1mm tunnel', fontsize=13)
fig.tight_layout(); fig.savefig('s4_disp_check.png', dpi=110)
print('saved s4_disp_check.png')
