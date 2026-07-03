"""gate0_plots.py -- Gate-0 Visual QA from gate0_dump.f3dat output.
Per Wade's spec: FIXED coords/colorscale/sampling; absolute field + stage increment +
unbalanced(ratio from logs) + boundary. Computes q=(s1-s3)/2, p'=(s1+s3)/2-pp,
q_th=0.6*(c*cos(phi)+p'*sin(phi)), q/qth. Outputs per-scale multi-panel PNGs + over-driving plot.
Usage: python gate0_plots.py <scale: small|large> ; expects z_<tag>_s{1..4}.txt, g_<tag>_s{1..4}.txt"""
import sys, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

THR = 0.6

def load_zone(fn):
    # xc yc zc s1 s3 pp coh phi layer creep  (layer is a string like 'layer4')
    rows = []
    with open(fn) as f:
        next(f)
        for ln in f:
            p = ln.split()
            if len(p) < 10: continue
            rows.append((float(p[0]),float(p[1]),float(p[2]),float(p[3]),float(p[4]),
                         float(p[5]),float(p[6]),float(p[7]), p[8], int(float(p[9]))))
    xc=np.array([r[0] for r in rows]); yc=np.array([r[1] for r in rows]); zc=np.array([r[2] for r in rows])
    s1=np.array([r[3] for r in rows]); s3=np.array([r[4] for r in rows]); pp=np.array([r[5] for r in rows])
    coh=np.array([r[6] for r in rows]); phi=np.array([r[7] for r in rows])
    lay=np.array([r[8] for r in rows]); cr=np.array([r[9] for r in rows])
    q=(s1-s3)/2.0; pm=(s1+s3)/2.0-pp
    qth=THR*(coh*np.cos(np.radians(phi))+pm*np.sin(np.radians(phi)))
    ratio=np.where(qth>1e-6, q/qth, 0.0)
    return dict(xc=xc,yc=yc,zc=zc,q=q,pm=pm,qth=qth,ratio=ratio,lay=lay,cr=cr,s1=s1,s3=s3,pp=pp)

def load_gp(fn):
    d=np.loadtxt(fn, skiprows=1)
    if d.ndim==1: d=d[None,:]
    x,y,z=d[:,0],d[:,1],d[:,2]; dmag=np.sqrt(d[:,3]**2+d[:,4]**2+d[:,5]**2)
    return x,y,z,dmag,d[:,5]

def main():
    scale = sys.argv[1] if len(sys.argv)>1 else 'small'
    tag = 's4' if scale=='small' else 'lg'
    yslice = (884,886) if scale=='small' else None  # small: tunnel x-z section @y885; large: project all
    Z=[load_zone(f'z_{tag}_s{n}.txt') for n in (1,2,3,4)]
    G=[load_gp(f'g_{tag}_s{n}.txt') for n in (1,2,3,4)]

    # ---- fixed color scales across stages ----
    rmax=max(np.percentile(z['ratio'],99) for z in Z); rmax=max(rmax,1.0)
    dmax=max(np.percentile(g[3],99.5) for g in G)

    # ---- panel: q/qth + active + disp per stage ----
    fig,ax=plt.subplots(3,4,figsize=(20,12))
    for i,(z,g) in enumerate(zip(Z,G)):
        if yslice: m=(z['yc']>=yslice[0])&(z['yc']<=yslice[1]); gm=(g[1]>=yslice[0])&(g[1]<=yslice[1])
        else: m=np.ones_like(z['xc'],bool); gm=np.ones_like(g[0],bool)
        # row0 q/qth ratio
        sc=ax[0,i].scatter(z['xc'][m],z['zc'][m],c=z['ratio'][m],s=4,cmap='hot_r',vmin=0,vmax=rmax)
        ax[0,i].set_title(f'{scale} S{i+1}  q/qth (>=1 active)'); ax[0,i].set_aspect('equal')
        if i==3: plt.colorbar(sc,ax=ax[0,i])
        # row1 active zones
        ax[1,i].scatter(z['xc'][m],z['zc'][m],c='lightgray',s=3)
        am=m&(z['cr']==1); ax[1,i].scatter(z['xc'][am],z['zc'][am],c='red',s=4)
        ax[1,i].set_title(f'S{i+1} creep-active n={int(z["cr"][m].sum())}'); ax[1,i].set_aspect('equal')
        # row2 disp magnitude
        sd=ax[2,i].scatter(g[0][gm],g[2][gm],c=g[3][gm],s=4,cmap='viridis',vmin=0,vmax=dmax)
        ax[2,i].set_title(f'S{i+1} |disp| max={g[3][gm].max()*1000:.2f}mm'); ax[2,i].set_aspect('equal')
        if i==3: plt.colorbar(sd,ax=ax[2,i])
    plt.tight_layout(); plt.savefig(f'gate0_{scale}_fields.png',dpi=110); plt.close()
    print(f'saved gate0_{scale}_fields.png (ratio vmax={rmax:.2f}, disp vmax={dmax*1000:.2f}mm)')

    # ---- active-by-layer table ----
    layers=sorted(set(Z[0]['lay']))
    print(f'\n{scale} creep-active count by layer:')
    print('layer  ' + '  '.join(f'S{n}' for n in (1,2,3,4)))
    for L in layers:
        cnts=[int(((z['lay']==L)&(z['cr']==1)).sum()) for z in Z]
        tot=int((Z[0]['lay']==L).sum())
        print(f'{L:8s} ' + '  '.join(f'{c}' for c in cnts) + f'   (of {tot})')

    # ---- dmax vs stage + field-rate reference ----
    dm=[g[3].max()*1000 for g in G]  # mm
    fig,ax=plt.subplots(figsize=(7,5))
    days=[30,60,90,120]
    ax.plot(days,dm,'o-',label=f'{scale} model dmax')
    # field slope rate 15-33 mm/yr -> over 120 d
    fr_lo=15/365*np.array(days); fr_hi=33/365*np.array(days)
    ax.fill_between(days,fr_lo,fr_hi,alpha=0.25,color='green',label='field rate 15-33 mm/yr')
    ax.set_xlabel('day'); ax.set_ylabel('dmax (mm)'); ax.set_yscale('log'); ax.legend(); ax.grid(True,alpha=0.3)
    ax.set_title(f'{scale}: model dmax vs field slope rate (over-driving check)')
    plt.tight_layout(); plt.savefig(f'gate0_{scale}_overdrive.png',dpi=110); plt.close()
    print(f'\nsaved gate0_{scale}_overdrive.png ; dmax(mm)/stage = {[round(x,3) for x in dm]}')
    print(f'field 120d window = {fr_lo[-1]:.1f}-{fr_hi[-1]:.1f} mm ; model/field ratio ~ {dm[-1]/fr_hi[-1]:.0f}-{dm[-1]/fr_lo[-1]:.0f}x')

if __name__=='__main__':
    main()
