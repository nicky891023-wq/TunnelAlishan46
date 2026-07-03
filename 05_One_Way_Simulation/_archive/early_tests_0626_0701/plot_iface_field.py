import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
CX, CZ = 1297.0, 1747.5
d = np.loadtxt('couple_interface_disp_s4.txt', skiprows=1)
x,y,z,dx,dy,dz = d[:,0],d[:,1],d[:,2],d[:,3],d[:,4],d[:,5]
# one y-slice near 885 for a clean cross-section quiver
m = (np.abs(y-885.0) < 2.0)
xs,zs,dxs,dzs = x[m],z[m],dx[m]*1000,dz[m]*1000  # mm
ang = np.degrees(np.arctan2(z-CZ, x-CX)) % 360
rx,rz = x-CX, z-CZ; rr=np.sqrt(rx*rx+rz*rz)
ri = -(dx*rx/rr + dz*rz/rr)*1000  # radial inward mm

fig = plt.figure(figsize=(15,5))
# (a) cross-section quiver
ax=fig.add_subplot(1,3,1)
sc=ax.scatter(xs,zs,c=(-(dxs*(xs-CX)+dzs*(zs-CZ))/np.sqrt((xs-CX)**2+(zs-CZ)**2)),
              s=12,cmap='RdBu_r',vmin=-2,vmax=2)
ax.quiver(xs,zs,dxs,dzs,angles='xy',scale_units='xy',scale=0.15,width=0.003,alpha=0.6)
th=np.linspace(0,2*np.pi,200); ax.plot(CX+4.7*np.cos(th),CZ+4.7*np.sin(th),'k--',lw=0.5)
ax.plot(CX,CZ,'k+',ms=12)
ax.annotate('crown(90)',(CX,CZ+5),ha='center',fontsize=8)
ax.annotate('R-wall(0)',(CX+5,CZ),fontsize=8); ax.annotate('L-wall(180)',(CX-5,CZ),ha='right',fontsize=8)
ax.annotate('bottom(270)',(CX,CZ-5.5),ha='center',fontsize=8)
ax.set_aspect('equal'); ax.set_xlim(CX-7,CX+7); ax.set_ylim(CZ-7,CZ+7)
ax.set_title('Interface disp field (y~885, vectors x15)\nblue=inward red=outward'); plt.colorbar(sc,ax=ax,label='radial inward mm')
# (b) polar radial-inward
ax2=fig.add_subplot(1,3,2,projection='polar')
abins=np.linspace(0,360,13); ac=(abins[:-1]+abins[1:])/2
means=[ri[(ang>=abins[i])&(ang<abins[i+1])].mean() if ((ang>=abins[i])&(ang<abins[i+1])).any() else 0 for i in range(12)]
ax2.plot(np.radians(ac),means,'o-',color='crimson')
ax2.plot(np.radians(np.linspace(0,360,100)),[0]*100,'k--',lw=0.5)
ax2.set_title('radial inward (mm) by angle\n(0=Rwall 90=crown 180=Lwall 270=bottom)',pad=20)
# (c) histogram of radial inward
ax3=fig.add_subplot(1,3,3)
ax3.hist(ri,bins=50,color='steelblue',edgecolor='k')
ax3.axvline(0,color='k',lw=1); ax3.axvline(ri.mean(),color='crimson',lw=2,label=f'mean={ri.mean():.3f}mm')
ax3.set_xlabel('radial inward (mm)'); ax3.set_ylabel('gp count'); ax3.legend()
ax3.set_title(f'interface gp radial-inward dist (n={len(ri)})')
plt.tight_layout(); plt.savefig('_provisional_figs/iface_field_s4.png',dpi=115)
print(f"WROTE iface_field_s4.png | n={len(d)} ymid_slice={m.sum()} | radial_inward mean={ri.mean():.3f} min={ri.min():.3f} max={ri.max():.3f} mm")
print(f"vertical closure proxy: crown(75-105deg) ri={ri[(ang>=75)&(ang<=105)].mean():.3f} + invert(255-285) ri={ri[(ang>=255)&(ang<=285)].mean():.3f}")
print(f"horizontal: Rwall(345-15) ri={ri[(ang>=345)|(ang<=15)].mean():.3f} + Lwall(165-195) ri={ri[(ang>=165)&(ang<=195)].mean():.3f}")
