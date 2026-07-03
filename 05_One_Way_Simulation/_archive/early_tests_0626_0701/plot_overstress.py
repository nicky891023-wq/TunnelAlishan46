# Where is the high-T_crit (creep-active) region in the small model? Upper over-stress or tunnel EDZ?
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = np.loadtxt('small_tcrit_y885.txt', skiprows=1)  # x z tcrit
x, z, tc = D[:,0], D[:,1], D[:,2]
act = tc >= 0.8
print(f'rock@y885={len(x)}  active(T>=0.8)={act.sum()} ({100*act.sum()/len(x):.1f}%)  Tmax={tc.max():.3f}')
r = np.sqrt((x-1299)**2+(z-1747)**2)
print(f'active within r<8m: {(act&(r<8)).sum()}  r>20m: {(act&(r>20)).sum()}')
print(f'active mean z = {z[act].mean():.0f} (tunnel z=1747)  active above z1755: {(act&(z>1755)).sum()} below z1740: {(act&(z<1740)).sum()}')
fig, ax = plt.subplots(1, 2, figsize=(22, 9))
sc = ax[0].scatter(x, z, c=tc, s=12, cmap='jet', vmin=0, vmax=max(0.9, tc.max()))
plt.colorbar(sc, ax=ax[0], label='T_crit = q/(c+p tanphi)')
ax[0].axhline(1747, color='k', ls='--', lw=0.8, alpha=0.5)
ax[0].scatter([1299],[1747], marker='+', s=300, c='magenta')
ax[0].set_title(f'(1) T_crit field @y885 (Tmax={tc.max():.2f}, cap=cos phi~0.866)')
ax[0].set_aspect('equal'); ax[0].set_xlabel('x'); ax[0].set_ylabel('z')
# active only
ax[1].scatter(x[~act], z[~act], c='0.85', s=8, label='inactive')
ax[1].scatter(x[act], z[act], c='red', s=12, label=f'ACTIVE T>=0.8 ({act.sum()})')
ax[1].scatter([1299],[1747], marker='+', s=300, c='blue', label='tunnel')
ax[1].set_title('(2) creep-ACTIVE region @y885 -- upper over-stress or tunnel EDZ?')
ax[1].set_aspect('equal'); ax[1].set_xlabel('x'); ax[1].set_ylabel('z'); ax[1].legend(fontsize=9)
fig.suptitle('small model in-situ T_crit (small_ep) -- is the creep-active region the tunnel or the mapped upper over-stress?', fontsize=12)
fig.tight_layout(); fig.savefig('overstress_check.png', dpi=110)
print('saved overstress_check.png')
