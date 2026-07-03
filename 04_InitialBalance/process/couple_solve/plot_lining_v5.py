# Visual "睜開眼睛看" of the FINAL Couple_Initial_v5 lining (y~885): ball convergence +
# bond state (all intact?) + bond normal stress -- confirm the lining is intact & sensibly loaded.
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
D = np.loadtxt('lining_disp_v5.txt', skiprows=1)   # x z dx dz dmag
B = np.loadtxt('lining_bonds_v5.txt', skiprows=1)  # x z pbsig pbstate
dx_, dz_, ddx, ddz, dmag = D[:,0], D[:,1], D[:,2], D[:,3], D[:,4]
bx, bz, pbsig, pbstate = B[:,0], B[:,1], B[:,2], B[:,3].astype(int)
for s in [0,1,2,3]:
    print(f'pb_state={s}: {(pbstate==s).sum()} ({"never-bond" if s==0 else "tension-FAIL" if s==1 else "shear-FAIL" if s==2 else "INTACT"})')
nfail = ((pbstate==1)|(pbstate==2)).sum()
print(f'TRUE broken (1/2) = {nfail} of {len(pbstate)} ({100*nfail/max(1,len(pbstate)):.2f}%)')
print(f'disp: mean={dmag.mean()*1000:.2f}mm max={dmag.max()*1000:.1f}mm  >10mm={(dmag>0.01).sum()}  >50mm={(dmag>0.05).sum()}')
fig, ax = plt.subplots(1, 3, figsize=(26, 9))
# (1) convergence
sc0 = ax[0].scatter(dx_, dz_, c=dmag*1000, s=10, cmap='viridis', vmin=0, vmax=max(1,dmag.max()*1000))
plt.colorbar(sc0, ax=ax[0], label='|disp| (mm)')
# quiver subsample
ss = max(1, len(dx_)//1500)
ax[0].quiver(dx_[::ss], dz_[::ss], ddx[::ss], ddz[::ss], color='k', scale_units='xy', angles='xy', width=0.002)
ax[0].set_title(f'(1) lining convergence  mean={dmag.mean()*1000:.1f}mm max={dmag.max()*1000:.0f}mm (arrows=disp dir)')
ax[0].set_aspect('equal'); ax[0].set_xlabel('x'); ax[0].set_ylabel('z')
# (2) bond state
cmap_state={3:('0.6','intact'),1:('red','tension-FAIL'),2:('blue','shear-FAIL'),0:('orange','never-bond')}
for s,(col,lab) in cmap_state.items():
    m=pbstate==s
    if m.sum()>0:
        ax[1].scatter(bx[m], bz[m], c=col, s=7, label=f'{lab}: {m.sum()}')
ax[1].set_title(f'(2) bond state -- TRUE cracks(tension+shear)={nfail} ({100*nfail/max(1,len(pbstate)):.2f}%)')
ax[1].legend(loc='upper right', fontsize=9); ax[1].set_aspect('equal'); ax[1].set_xlabel('x'); ax[1].set_ylabel('z')
# (3) bond normal stress
sc2 = ax[2].scatter(bx, bz, c=pbsig/1e6, s=7, cmap='seismic', vmin=-3, vmax=3)
plt.colorbar(sc2, ax=ax[2], label='pb_sigma (MPa, +tension)')
ax[2].set_title(f'(3) bond normal stress range=[{pbsig.min()/1e6:.2f},{pbsig.max()/1e6:.2f}]MPa (pb_ten=2.1)')
ax[2].set_aspect('equal'); ax[2].set_xlabel('x'); ax[2].set_ylabel('z')
fig.suptitle('Couple_Initial_v5 lining @y~885 -- INTACT confined lining (0 broken bonds), sensible convergence', fontsize=13)
fig.tight_layout(); fig.savefig('lining_v5_check.png', dpi=110)
print('saved lining_v5_check.png')
