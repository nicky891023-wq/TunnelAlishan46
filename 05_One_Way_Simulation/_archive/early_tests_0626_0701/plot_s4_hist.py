import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
# parse s4_history.txt (Step, Zdis=crown_dz, Xdis=side_dx, n_act); skip 2 header rows
rows=[]
with open('s4_history.txt') as f:
    for ln in f:
        p=ln.split()
        if len(p)>=4:
            try:
                rows.append([float(p[0]),float(p[1]),float(p[2]),float(p[3])])
            except: pass
d=np.array(rows)
step,cz,sx,nact = d[:,0],d[:,1]*1000,d[:,2]*1000,d[:,3]  # mm
idx=np.arange(len(d))
# segment by nactive level -> stages (662k S1, 656k S2, 5k S3, 443k S4)
fig,ax=plt.subplots(1,2,figsize=(15,5))
ax[0].plot(idx,cz,'b.-',ms=3,label='crown_dz (mm)')
ax[0].plot(idx,sx,'r.-',ms=3,label='side_dx (mm)')
ax[0].axhline(0,color='k',lw=0.5)
# mark stage boundaries by nactive change
chg=np.where(np.abs(np.diff(nact))>1000)[0]
for c in chg:
    ax[0].axvline(c,color='gray',ls='--',lw=1)
ax[0].set_xlabel('history record index (sequential)'); ax[0].set_ylabel('displacement (mm)')
ax[0].set_title('small-model tunnel-point disp history (crown_dz, side_dx)\ndashed=stage boundary (nactive change)'); ax[0].legend()
ax[1].plot(idx,nact/1000,'g.-',ms=3); ax[1].set_xlabel('index'); ax[1].set_ylabel('n_active creep zones (x1000)')
ax[1].set_title('creep-active zone count (stage marker)')
plt.tight_layout(); plt.savefig('_provisional_figs/s4_history_check.png',dpi=110)
print(f"rows={len(d)} | crown_dz range[{cz.min():.4f},{cz.max():.4f}]mm | side_dx range[{sx.min():.4f},{sx.max():.4f}]mm")
print(f"nactive unique levels: {sorted(set(np.round(nact/1000).astype(int)))}")
print(f"stage-boundary indices (nactive jumps): {chg.tolist()}")
print(f"final crown_dz={cz[-1]:.4f}mm side_dx={sx[-1]:.4f}mm")
