# 05 small-model 4-stage standalone: 120-day cumulative deformation history (flat-onset-flat-onset).
import re, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
lines = open('small_4stage.log', encoding='utf-8', errors='ignore').read().splitlines()
day=[]; dmax=[]; act=[]
for l in lines:
    m = re.search(r'S4creep day=([\d.]+) dmax=([\d.eE+-]+) m\s+\(active=(\d+)\)', l)
    if m:
        day.append(float(m.group(1))); dmax.append(float(m.group(2))*1000); act.append(int(m.group(3)))
day=np.array(day); dmax=np.array(dmax); act=np.array(act)
# stage active counts
eqs=[]
for l in lines:
    m=re.search(r'S4-S(\d)eq (\w+) active=(\d+)', l)
    if m: eqs.append((int(m.group(1)), m.group(2), int(m.group(3))))
print('stage active:', eqs)
print(f'cumulative dmax: day30={dmax[day==30][0] if 30 in day else "?"} day60={dmax[day==60][0] if 60 in day else "?"} '
      f'day90={dmax[day==90][0] if 90 in day else "?"} day120={dmax[day<=120][-1] if len(dmax) else "?"} mm')
fig, ax = plt.subplots(1, 2, figsize=(22, 8))
# (1) cumulative dmax vs day, shaded by water stage
ax[0].plot(day, dmax, 'o-', color='navy', lw=2, ms=5)
spans=[(0,30,'LOW','#cfe8ff'),(30,60,'HIGH','#ffd6d6'),(60,90,'LOW','#cfe8ff'),(90,120,'HIGH','#ffd6d6')]
for a,b,lab,col in spans:
    ax[0].axvspan(a,b,color=col,alpha=0.6)
    ax[0].text((a+b)/2, ax[0].get_ylim()[1]*0.05 if len(dmax) else 0.1, lab, ha='center', fontsize=10, color='gray')
ax[0].set_xlabel('day'); ax[0].set_ylabel('cumulative max creep displacement (mm)')
ax[0].set_title('(1) 120-day deformation history -- flat(low)/onset(high) x2  (blue=LOW dry, red=HIGH saturated)')
ax[0].grid(alpha=0.3)
# (2) active count per stage
if eqs:
    labs=[f'S{s}\n{w}' for s,w,n in eqs]; vals=[n for s,w,n in eqs]
    cols=['steelblue' if w=='LOW' else 'crimson' for s,w,n in eqs]
    bars=ax[1].bar(labs, vals, color=cols, width=0.6)
    for bbar,v in zip(bars,vals): ax[1].text(bbar.get_x()+bbar.get_width()/2, v, f'{v}\n({100*v/1098455:.0f}%)', ha='center', va='bottom', fontsize=9)
    ax[1].set_ylabel('creep-active rock zones'); ax[1].set_title('(2) active region per stage -- LOW small, HIGH expands (onset)')
    ax[1].grid(alpha=0.3, axis='y')
fig.suptitle('05 small-model 4-stage STANDALONE (120d, LOW-HIGH-LOW-HIGH) -- per-stage threshold + water density + 0.8', fontsize=13)
fig.tight_layout(); fig.savefig('s4_check.png', dpi=115)
print('saved s4_check.png')
