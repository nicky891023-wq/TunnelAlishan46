# Visual "睜開眼睛看" of the flat-then-onset: per-stage creep dmax vs day.
# Full fix = per-stage threshold (stability) + zone water density (pp) + threshold 0.8.
import re, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
lines = open('track_e.log', encoding='utf-8', errors='ignore').read().splitlines()
s1d=[]; s1v=[]; s2d=[]; s2v=[]
for l in lines:
    m = re.search(r'TEcreep day=([\d.]+) dmax=([\d.eE+-]+)', l)
    if m:
        d=float(m.group(1)); v=float(m.group(2))*1000
        if d<=30: s1d.append(d); s1v.append(v)
        else: s2d.append(d); s2v.append(v)
# prepend the stage starts at 0 (disp was zeroed at each re-eq)
s1d=[0]+s1d; s1v=[0]+s1v
s2d=[30]+s2d; s2v=[0]+s2v
fig, ax = plt.subplots(1, 2, figsize=(20, 8))
# (1) per-stage creep (each from its own zero)
ax[0].plot(s1d, s1v, 'o-', color='steelblue', lw=2.5, ms=7, label=f'STAGE1 LOW water (dry tunnel)\nactive=214247 (20%)  ->  {s1v[-1]:.2f}mm/30d')
ax[0].plot(s2d, s2v, 's-', color='crimson', lw=2.5, ms=7, label=f'STAGE2 HIGH water (saturated)\nactive=492727 (45%)  ->  {s2v[-1]:.2f}mm/30d')
ax[0].axvline(30, color='gray', ls='--', alpha=0.6)
ax[0].annotate('water table rises\nz1724 -> z1807\n(disp re-zeroed)', xy=(30, 1.5), xytext=(18, 2.6),
               arrowprops=dict(arrowstyle='->', color='gray'), fontsize=10, color='gray')
ax[0].set_xlabel('day'); ax[0].set_ylabel('max creep displacement (mm)')
ax[0].set_title('(1) Per-stage creep -- FLAT (low) then ONSET (high)', fontsize=13)
ax[0].legend(loc='upper left', fontsize=10); ax[0].grid(alpha=0.3)
# (2) creep RATE bar
rates=[s1v[-1]/30, s2v[-1]/30]
bars=ax[1].bar(['LOW water\n(0-30d)','HIGH water\n(30-60d)'], rates, color=['steelblue','crimson'], width=0.5)
for b,r in zip(bars,rates):
    ax[1].text(b.get_x()+b.get_width()/2, r+0.002, f'{r:.3f}\nmm/day', ha='center', fontsize=11)
ax[1].set_ylabel('creep rate (mm/day)')
ax[1].set_title(f'(2) Creep RATE -- onset = {rates[1]/rates[0]:.1f}x faster at high water', fontsize=13)
ax[1].grid(alpha=0.3, axis='y')
fig.suptitle('05 small-model threshold creep VALIDATED -- per-stage + water density + threshold 0.8\n'
             'low water dry tunnel = small flat creep; high water saturated = onset (eff. stress drops, near-yield region 2.3x)', fontsize=13)
fig.tight_layout(); fig.savefig('te_onset_check.png', dpi=115)
print('saved te_onset_check.png')
print(f'LOW: {s1v[-1]:.2f}mm/30d ({rates[0]:.3f}mm/d)  HIGH: {s2v[-1]:.2f}mm/30d ({rates[1]:.3f}mm/d)  onset={rates[1]/rates[0]:.1f}x')
