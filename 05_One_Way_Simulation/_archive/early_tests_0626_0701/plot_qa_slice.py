import sys, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
pfx = sys.argv[1] if len(sys.argv)>1 else 'large'
fn = f'qa_{pfx}_slice.txt'
rows=[]
with open(fn) as f:
    next(f)  # header
    for ln in f:
        p=ln.split()
        if len(p)>=5:
            try: rows.append([float(p[0]),float(p[1]),float(p[2]),float(p[3]),float(p[4])])
            except: pass
d=np.array(rows)
x,z,szz,sxx,state = d[:,0],d[:,1],d[:,2],d[:,3],d[:,4]
k0 = np.where(szz!=0, sxx/szz, 0)
fig,ax=plt.subplots(1,4,figsize=(22,6))
for a,val,ttl,cm in [(ax[0],szz/1e6,'szz (MPa, compression neg)','RdBu'),
                      (ax[1],sxx/1e6,'sxx (MPa)','RdBu'),
                      (ax[2],k0,'sxx/szz (K0, expect ~0.7)','viridis'),
                      (ax[3],state,'plastic state (0=elastic)','Reds')]:
    sc=a.scatter(x,z,c=val,s=6,cmap=cm)
    a.set_xlabel('x'); a.set_ylabel('z'); a.set_aspect('equal'); a.set_title(f'{pfx}: {ttl}')
    plt.colorbar(sc,ax=a)
    if 'K0' in ttl: sc.set_clim(0,1.5)
    if 'state' in ttl: sc.set_clim(0,1)
plt.tight_layout(); out=f'_provisional_figs/qa_{pfx}_initial.png'
plt.savefig(out,dpi=100)
print(f"WROTE {out} | n={len(d)} szz[{szz.min()/1e6:.2f},{szz.max()/1e6:.2f}]MPa K0_med={np.median(k0):.3f} plastic={int((state!=0).sum())}")
