"""plot_convhist.py [logfile] -- parse small_driven.log for the y860-910 tunnel
convergence time-history (day, vclose, hclose) and plot vs physical day, marking the
4 water-level stages (LOW/HIGH) + the day-0 in-situ datum (curve starts non-zero).
NEGATIVE closure = closing (squeezing). Out: qa_convergence_history.png
"""
import re, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

log = sys.argv[1] if len(sys.argv) > 1 else 'small_driven.log'
txt = open(log, encoding='utf-8', errors='replace').read()

days, vcl, hcl = [], [], []
m0 = re.search(r'SD-CHK STAGE0 day=([\d.eE+-]+).*?vclose=([\d.eE+-]+)mm hclose=([\d.eE+-]+)', txt)
if m0:
    days.append(float(m0.group(1))); vcl.append(float(m0.group(2))); hcl.append(float(m0.group(3)))
for m in re.finditer(r'SD-creep stg(\d+) day=([\d.eE+-]+) vclose=([\d.eE+-]+)mm hclose=([\d.eE+-]+)mm', txt):
    days.append(float(m.group(2))); vcl.append(float(m.group(3))); hcl.append(float(m.group(4)))
stg_ends = []
for m in re.finditer(r'SD-CHK STAGE([1-4]) day=([\d.eE+-]+).*?vclose=([\d.eE+-]+)mm hclose=([\d.eE+-]+)', txt):
    stg_ends.append((int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4))))

if not days:
    print("No convergence points parsed yet from", log); sys.exit(0)

days = np.array(days); vcl = np.array(vcl); hcl = np.array(hcl)
order = np.argsort(days, kind='stable'); days, vcl, hcl = days[order], vcl[order], hcl[order]

fig, ax = plt.subplots(figsize=(12, 7))
for (a, b, col) in [(0,30,'#e8f0ff'), (30,60,'#ffe8e8'), (60,90,'#e8f0ff'), (90,120,'#ffe8e8')]:
    ax.axvspan(a, b, color=col, alpha=0.7)
ax.plot(days, vcl, 'o-', color='b', ms=4, label='vertical closure (crown-invert)')
ax.plot(days, hcl, 's-', color='r', ms=4, label='horizontal closure (springline)')
ax.axhline(0, color='k', lw=0.5)
for a in [30, 60, 90]:
    ax.axvline(a, color='gray', ls=':', lw=0.8)
ax.set_xlabel('physical day'); ax.set_ylabel('closure (mm; negative=closing/squeezing)')
ax.set_title('Alishan #46 small-model y860-910 tunnel convergence (large-driven, 4 water stages)\n'
             'LOW(blue)=slow creep  HIGH(red)=fast creep  |  day-0 = in-situ elasto-plastic (non-zero)')
ax.legend(loc='best'); ax.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('qa_convergence_history.png', dpi=95)
print('saved qa_convergence_history.png')
print(f'  points={len(days)}  day0 vclose={vcl[0]:.2f}mm hclose={hcl[0]:.2f}mm')
print(f'  final vclose={vcl[-1]:.2f}mm hclose={hcl[-1]:.2f}mm (negative=closing)')
for s, d, v, h in stg_ends:
    print(f'  STAGE{s} end day{d:.0f}: vclose={v:.2f}mm hclose={h:.2f}mm')
