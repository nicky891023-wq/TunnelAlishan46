"""gate0_trends.py -- extract per-stage dmax + creep-active from all Phase-0 run logs into a
trend table + plots. Large: LG-S{N}done dmax=, LG-S{N}eq active=. Small: S4-S{N}done dmax=,
S4-S{N}eq active=. (controls reuse the same stage tags; the log file distinguishes them.)"""
import re, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt

RUNS = {
 'large': {'baseline':'large_creep_4stage.log','HIGH-only':'large_HIGHonly.log',
           'LOW-only':'large_LOWonly.log','no-creep':'large_nocreep.log'},
 'small': {'baseline':'small_4stage.log','HIGH-only':'small_HIGHonly.log',
           'LOW-only':'small_LOWonly.log','no-creep':'small_nocreep.log'},
}
TAG = {'large':'LG','small':'S4'}

def parse(scale, fn):
    dmax={}; act={}
    try: txt=open(fn,errors='ignore').read()
    except FileNotFoundError: return None,None
    t=TAG[scale]
    for n in (1,2,3,4):
        m=re.findall(rf'{t}-S{n}done.*?dmax=([0-9.eE+-]+)', txt)
        if m: dmax[n]=float(m[-1])
        a=re.findall(rf'{t}-S{n}eq.*?active=([0-9]+)', txt)
        if a: act[n]=int(a[-1])
    if 4 not in dmax:   # stage-4 dmax lives in the per-run DONE line (LG-DONE/LGH-DONE/S4-DONE/...)
        alld=re.findall(r'dmax=([0-9.eE+-]+)', txt)
        if alld: dmax[4]=float(alld[-1])
    return dmax,act

print("=== Phase-0 trend table (dmax per stage; mm for small, m for large) ===")
for scale in ('large','small'):
    unit=1000.0 if scale=='small' else 1.0; us='mm' if scale=='small' else 'm'
    print(f"\n[{scale}]  dmax({us}) by stage  (S1 LOW, S2 HIGH, S3 LOW, S4 HIGH)")
    print(f"{'case':12s}  S1     S2     S3     S4    | increments")
    fig,ax=plt.subplots(1,2,figsize=(13,5))
    for case,fn in RUNS[scale].items():
        dm,ac=parse(scale,fn)
        if not dm: print(f"{case:12s}  (no/partial log: {fn})"); continue
        vals=[dm.get(n,float('nan'))*unit for n in (1,2,3,4)]
        inc=[vals[0]]+[vals[i]-vals[i-1] for i in range(1,4)]
        print(f"{case:12s}  "+" ".join(f"{v:6.3f}" for v in vals)+"  | "+" ".join(f"{x:+.3f}" for x in inc))
        days=[30,60,90,120]
        ax[0].plot(days,vals,'o-',label=case)
        ax[1].bar([d+ (list(RUNS[scale]).index(case)-1.5)*6 for d in days], inc, width=6, label=case)
    # field rate band (large only meaningful but show on both)
    if scale=='large':
        d=np.array([30,60,90,120]); ax[0].fill_between(d,15/365*d,33/365*d,alpha=.2,color='g',label='field 15-33mm/yr')
    ax[0].set_title(f'{scale} cumulative dmax'); ax[0].set_xlabel('day'); ax[0].set_ylabel(us); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
    ax[1].set_title(f'{scale} per-stage increment (water effect)'); ax[1].set_xlabel('day'); ax[1].set_ylabel(us); ax[1].legend(fontsize=8); ax[1].grid(alpha=.3)
    plt.tight_layout(); plt.savefig(f'gate0_{scale}_trends.png',dpi=110); plt.close()
    print(f"  -> saved gate0_{scale}_trends.png")
    # active-by-stage
    print(f"  active zones by stage:")
    for case,fn in RUNS[scale].items():
        dm,ac=parse(scale,fn)
        if ac: print(f"    {case:12s}  "+" ".join(f"S{n}={ac.get(n,'?')}" for n in (1,2,3,4)))
