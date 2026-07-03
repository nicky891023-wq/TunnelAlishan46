# Full ball/wall geometry check: at y-slices (mouths 865/905 + mid 885), overlay
# balls vs wz_outter facets + count any ball OUTSIDE the bore (rock side) by radial test.
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
B = np.loadtxt('geom_balls.txt', skiprows=1)      # x y z r
W = np.loadtxt('geom_wzouter.txt', skiprows=1)    # x y z
cx, cz = 1297.0, 1747.0                             # tunnel center (x,z)
slices = [(864,866,'mouth y~865'),(884,886,'mid y~885'),(904,906,'mouth y~905')]
fig, ax = plt.subplots(1, 3, figsize=(24, 8))
for i,(y0,y1,lab) in enumerate(slices):
    bm = (B[:,1]>y0)&(B[:,1]<y1); wm = (W[:,1]>y0)&(W[:,1]<y1)
    bx,bz = B[bm,0], B[bm,2]; wx,wz = W[wm,0], W[wm,2]
    ax[i].scatter(wx,wz,c='red',s=10,label='wz_outter (rock face)',zorder=3)
    ax[i].scatter(bx,bz,c='royalblue',s=3,label='lining balls',zorder=2)
    # radial penetration test: ball outside the max bore radius at its angle bin
    nout=0
    if len(wx)>5 and len(bx)>0:
        wr = np.hypot(wx-cx, wz-cz); wa = np.degrees(np.arctan2(wz-cz, wx-cx))
        br = np.hypot(bx-cx, bz-cz); ba = np.degrees(np.arctan2(bz-cz, bx-cx))
        for j in range(len(bx)):
            sel = np.abs(((wa-ba[j]+180)%360)-180) < 6.0   # facets within 6 deg
            if sel.sum()>0 and br[j] > wr[sel].max()+0.02:  # 2cm tolerance
                nout+=1
                ax[i].scatter([bx[j]],[bz[j]],c='lime',s=25,zorder=5)
    ax[i].set_title(f'{lab}: balls={len(bx)} facets={len(wx)}  OUTSIDE(green)={nout}')
    ax[i].set_aspect('equal'); ax[i].set_xlabel('x'); ax[i].set_ylabel('z'); ax[i].legend(loc='lower center')
    print(f'{lab}: balls={len(bx)} facets={len(wx)} balls-outside-bore={nout}')
fig.suptitle('Couple_Initial ball/wall geometry check -- balls outside wz_outter (rock side)?', fontsize=13)
fig.tight_layout(); fig.savefig('geom_check.png', dpi=110)
print('saved geom_check.png')
