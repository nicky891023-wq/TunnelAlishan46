# Diagnose Small_Initial stability (Wade's priority): unbalanced force field (+direction),
# velocity, stress, plastic zone, lining -- find the divergence root cause @y~885.
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
G = np.loadtxt('diag_gp_y885.txt', skiprows=1)   # x z funb fx fz vel
Z = np.loadtxt('diag_zone_y885.txt', skiprows=1) # x z sig1 sig3 state islin
gx, gz, funb, ffx, ffz, gvel = G[:,0],G[:,1],G[:,2],G[:,3],G[:,4],G[:,5]
zx, zz, sig1, sig3, state, islin = Z[:,0],Z[:,1],Z[:,2],Z[:,3],Z[:,4].astype(int),Z[:,5].astype(int)
print(f'gp@y885={len(gx)} funb: mean={funb.mean():.2e} max={funb.max():.2e}N  vel max={gvel.max():.2e}m/s')
print(f'zone@y885={len(zx)} plastic(state>0)={ (state>0).sum() } ({100*(state>0).sum()/len(zx):.1f}%)  lining={ (islin==1).sum() }')
print(f'sig1(max-principal,compression+) range=[{sig1.min()/1e6:.2f},{sig1.max()/1e6:.2f}]MPa  sig3=[{sig3.min()/1e6:.2f},{sig3.max()/1e6:.2f}]MPa')
fig, ax = plt.subplots(2, 3, figsize=(26, 15))
# (1) unbalanced force magnitude + direction
sc=ax[0,0].scatter(gx,gz,c=np.log10(funb+1e-12),s=10,cmap='hot_r'); plt.colorbar(sc,ax=ax[0,0],label='log10|unbal force| (N)')
ss=max(1,len(gx)//1200); ax[0,0].quiver(gx[::ss],gz[::ss],ffx[::ss],ffz[::ss],color='cyan',scale_units='xy',width=0.002)
ax[0,0].set_title(f'(1) UNBALANCED FORCE max={funb.max():.1e}N (arrows=dir)'); ax[0,0].set_aspect('equal')
# (2) velocity
sc=ax[0,1].scatter(gx,gz,c=np.log10(gvel+1e-15),s=10,cmap='hot_r'); plt.colorbar(sc,ax=ax[0,1],label='log10|vel| (m/s)')
ax[0,1].set_title(f'(2) VELOCITY max={gvel.max():.1e}m/s (eq~0)'); ax[0,1].set_aspect('equal')
# (3) plastic zone + lining
el=state==0; pl=state>0
ax[0,2].scatter(zx[el],zz[el],c='0.8',s=8,label=f'elastic {el.sum()}')
ax[0,2].scatter(zx[pl],zz[pl],c='red',s=8,label=f'PLASTIC {pl.sum()} ({100*pl.sum()/len(zx):.0f}%)')
lin=islin==1
ax[0,2].scatter(zx[lin],zz[lin],facecolor='none',edgecolor='lime',s=20,label=f'lining {lin.sum()}')
ax[0,2].set_title('(3) PLASTIC zone (red) + lining (green)'); ax[0,2].legend(fontsize=8); ax[0,2].set_aspect('equal')
# (4) sig1 (max principal, compression+)
sc=ax[1,0].scatter(zx,zz,c=sig1/1e6,s=10,cmap='jet'); plt.colorbar(sc,ax=ax[1,0],label='sig1 MPa(comp+)')
ax[1,0].set_title('(4) sig1 (most compressive principal)'); ax[1,0].set_aspect('equal')
# (5) sig3
sc=ax[1,1].scatter(zx,zz,c=sig3/1e6,s=10,cmap='jet'); plt.colorbar(sc,ax=ax[1,1],label='sig3 MPa')
ax[1,1].set_title('(5) sig3 (least compressive principal)'); ax[1,1].set_aspect('equal')
# (6) deviatoric q = (sig1-sig3)/2
q=(sig1-sig3)/2
sc=ax[1,2].scatter(zx,zz,c=q/1e6,s=10,cmap='viridis'); plt.colorbar(sc,ax=ax[1,2],label='q=(s1-s3)/2 MPa')
ax[1,2].set_title('(6) deviatoric q'); ax[1,2].set_aspect('equal')
for a in ax.flat: a.set_xlabel('x'); a.set_ylabel('z')
fig.suptitle('Small_Initial diagnostics @y~885 -- root-cause search for the creep divergence', fontsize=15)
fig.tight_layout(); fig.savefig('diag_small_check.png', dpi=105)
print('saved diag_small_check.png')
