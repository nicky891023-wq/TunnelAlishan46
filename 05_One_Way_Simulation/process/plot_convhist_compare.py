"""plot_convhist_compare.py -- overlay TWO small_driven runs' y860-910 tunnel
convergence histories (uniform threshold 0.6 vs per-stage 0.6/0.4/0.3/0.1) to show
how progressively lowering the creep threshold turns the LOW-water stages (S3) from
FROZEN into contributing and the 2nd HIGH-water stage (S4) from shakedown into a
real creep contributor. NEGATIVE closure = closing (squeezing).
Usage: plot_convhist_compare.py <run1.log> <run2.log> [out.png]
"""
import re, sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

f1 = sys.argv[1] if len(sys.argv) > 1 else 'sd_run1_uniform06.log'
f2 = sys.argv[2] if len(sys.argv) > 2 else 'sd_run2_thresh.log'
out = sys.argv[3] if len(sys.argv) > 3 else 'qa_convergence_compare.png'


def parse(log):
    txt = open(log, encoding='utf-8', errors='replace').read()
    days, vcl, hcl = [], [], []
    m0 = re.search(r'SD-CHK STAGE0 day=([\d.eE+-]+).*?vclose=([\d.eE+-]+)mm hclose=([\d.eE+-]+)', txt)
    if m0:
        days.append(float(m0.group(1))); vcl.append(float(m0.group(2))); hcl.append(float(m0.group(3)))
    for m in re.finditer(r'SD-creep stg(\d+) day=([\d.eE+-]+) vclose=([\d.eE+-]+)mm hclose=([\d.eE+-]+)mm', txt):
        days.append(float(m.group(2))); vcl.append(float(m.group(3))); hcl.append(float(m.group(4)))
    d = np.array(days); v = np.array(vcl); h = np.array(hcl)
    o = np.argsort(d, kind='stable')
    return d[o], v[o], h[o]


d1, v1, h1 = parse(f1)
d2, v2, h2 = parse(f2)

fig, ax = plt.subplots(figsize=(13, 7.5))
for (a, b, col) in [(0, 30, '#e8f0ff'), (30, 60, '#ffe8e8'), (60, 90, '#e8f0ff'), (90, 120, '#ffe8e8')]:
    ax.axvspan(a, b, color=col, alpha=0.7)
for a in [30, 60, 90]:
    ax.axvline(a, color='gray', ls=':', lw=0.8)
ax.axhline(0, color='k', lw=0.5)

# uniform 0.6 (dashed, lighter)
ax.plot(d1, v1, 'o--', color='#5aa0ff', ms=4, lw=1.4, label='vert closure — uniform 0.6')
ax.plot(d1, h1, 's--', color='#ff8a8a', ms=4, lw=1.4, label='horiz closure — uniform 0.6')
# per-stage 0.6/0.4/0.3/0.1 (solid, bold)
ax.plot(d2, v2, 'o-', color='b', ms=5, lw=2.2, label='vert closure — 0.6/0.4/0.3/0.1')
ax.plot(d2, h2, 's-', color='r', ms=5, lw=2.2, label='horiz closure — 0.6/0.4/0.3/0.1')

# stage threshold annotations
for x, t in [(15, 'S1\nθ=0.6'), (45, 'S2\nθ=0.4'), (75, 'S3\nθ=0.3'), (105, 'S4\nθ=0.1')]:
    ax.text(x, 0.4, t, ha='center', va='top', fontsize=9, color='#333')

ax.set_xlabel('physical day')
ax.set_ylabel('closure (mm; negative = closing / squeezing)')
ax.set_title('Alishan #46 small-model tunnel convergence — per-stage threshold 0.6/0.4/0.3/0.1 (solid) vs uniform 0.6 (dashed)\n'
             'LOW water = blue band, HIGH water = red band | lowering θ each stage keeps S3/S4 creeping instead of freezing')
ax.legend(loc='lower left', fontsize=9)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(out, dpi=95)
print(f'saved {out}')


def stg_end(d, v, h, day):
    i = np.argmin(np.abs(d - day))
    return v[i], h[i]


print(f'\n{"stage":<10}{"uniform 0.6 (v/h mm)":<26}{"0.6/0.4/0.3/0.1 (v/h mm)":<28}')
for day, lbl in [(0, 'in-situ'), (30, 'S1 end'), (60, 'S2 end'), (90, 'S3 end'), (120, 'S4 end')]:
    a = stg_end(d1, v1, h1, day); b = stg_end(d2, v2, h2, day)
    print(f'  day{day:<6}{a[0]:>7.2f}/{a[1]:>7.2f}          {b[0]:>7.2f}/{b[1]:>7.2f}')
