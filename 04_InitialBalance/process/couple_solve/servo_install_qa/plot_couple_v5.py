# Verify the FINAL Couple_Initial_v5 in-situ + excavation stress (y~885): max principal +
# szz, confirm (a) clean far-field (no box artifact, smooth physical slope), (b) a PHYSICAL
# near-tunnel concentration that developed from the excavation (not imposed).
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
S = np.loadtxt('couple_v5_y885.txt', skiprows=1)   # x z sxx syy szz sxy sxz syz
x, z = S[:,0], S[:,1]
sxx, syy, szz, sxy, sxz, syz = S[:,2], S[:,3], S[:,4], S[:,5], S[:,6], S[:,7]
n = len(x); maxp = np.zeros(n); minp = np.zeros(n)
for i in range(n):
    T = np.array([[sxx[i],sxy[i],sxz[i]],[sxy[i],syy[i],syz[i]],[sxz[i],syz[i],szz[i]]])
    ev = np.linalg.eigvalsh(T); maxp[i]=ev.max(); minp[i]=ev.min()
cx, cz = 1297.0, 1747.0
oldbox = (1277.0,1305.0,1739.0,1757.0)
fig, ax = plt.subplots(1, 3, figsize=(26, 9))
for i,(val,lab,cm,vlim) in enumerate([
        (maxp/1e6,'MAX PRINCIPAL (MPa) -- what Wade flagged before','jet',None),
        (szz/1e6,'szz vertical (MPa)','jet',None),
        (minp/1e6,'MIN PRINCIPAL = most compressive (MPa) -- near-tunnel concentration','jet',None)]):
    sc = ax[i].scatter(x, z, c=val, s=14, cmap=cm)
    plt.colorbar(sc, ax=ax[i], label=lab)
    ax[i].add_patch(Rectangle((oldbox[0],oldbox[2]), oldbox[1]-oldbox[0], oldbox[3]-oldbox[2], fill=False, edgecolor='red', linewidth=2, ls='--', label='OLD overlay box (should be INVISIBLE)'))
    ax[i].scatter([cx],[cz], c='k', marker='+', s=150, linewidth=2)
    ax[i].set_title(lab); ax[i].set_aspect('equal'); ax[i].set_xlabel('x'); ax[i].set_ylabel('z'); ax[i].legend(loc='upper right', fontsize=7)
fig.suptitle('Couple_Initial_v5 FINAL stress @y~885 -- clean far-field (no box) + physical near-tunnel concentration', fontsize=13)
fig.tight_layout(); fig.savefig('couple_v5_check.png', dpi=110)
left=(x<cx); right=(x>cx)
print(f'rock zones @y885 = {n}')
print(f'MAX-PRINCIPAL mean L={maxp[left].mean()/1e6:.3f} R={maxp[right].mean()/1e6:.3f} asym={abs(maxp[left].mean()-maxp[right].mean())/1e6:.3f}MPa')
print(f'szz mean L={szz[left].mean()/1e6:.3f} R={szz[right].mean()/1e6:.3f}')
print(f'min-principal (most compressive): range [{minp.min()/1e6:.2f},{minp.max()/1e6:.2f}]MPa (near-tunnel = most negative)')
band=(z>oldbox[2])&(z<oldbox[3]); ji=band&(x>1302)&(x<1305); jo=band&(x>1305)&(x<1308)
if ji.sum()>0 and jo.sum()>0:
    print(f'OLD box-edge szz jump @x~1305: in={szz[ji].mean()/1e6:.3f} out={szz[jo].mean()/1e6:.3f} JUMP={abs(szz[ji].mean()-szz[jo].mean())/1e6:.3f}MPa (smooth = box gone)')
print('saved couple_v5_check.png')
