"""couple_evolution_plot.py -- parse couple_full4.log for per-stage mid-tunnel deliverables and plot
the stage evolution (Codex Q3 deliverable: per-stage mid crack count + reaction + convergence).
Reads FULL-RESULT-s{n}, MID-WALL full_s{n}, MID-CONV full_s{n}. End-band counts shown separately
(boundary-affected, excluded from interpretation). Output couple_evolution.png."""
import re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

LOG = 'couple_full4.log'
try:
    txt = open(LOG, errors='ignore').read()
except Exception as e:
    print(f"cannot read {LOG}: {e}")
    raise SystemExit

stages, mid_cr, end_cr, wz_tot, wi = [], [], [], [], []
midwall_sum, midwall_abs, conv_mean, conv_max = {}, {}, {}, {}

for m in re.finditer(r'FULL-RESULT-s(\d+) abort=\d+ MID_cracks=(\d+) end_cracks\(excl\)=(\d+) wz_total=([-\d.eE]+)MN w_inner=([-\d.eE]+)MN', txt):
    s = int(m.group(1)); stages.append(s)
    mid_cr.append(int(m.group(2))); end_cr.append(int(m.group(3)))
    wz_tot.append(float(m.group(4))); wi.append(float(m.group(5)))
for m in re.finditer(r'MID-WALL full_s(\d+) y\[[\d.]+,[\d.]+\] bf_couple_n=\d+ sum_normal=([-\d.eE]+)MN abs_normal=([-\d.eE]+)MN', txt):
    s = int(m.group(1)); midwall_sum[s] = float(m.group(2)); midwall_abs[s] = float(m.group(3))
for m in re.finditer(r'MID-CONV full_s(\d+) lining_balls=\d+ radial_inward_mean=([-\d.eE]+)mm max=([-\d.eE]+)mm', txt):
    s = int(m.group(1)); conv_mean[s] = float(m.group(2)); conv_max[s] = float(m.group(3))

if not stages:
    print("no FULL-RESULT stages parsed yet (run still in progress?)")
    raise SystemExit

print(f"stages parsed: {stages}")
for i, s in enumerate(stages):
    print(f"  s{s}: mid_cracks={mid_cr[i]} end(excl)={end_cr[i]} wz_total={wz_tot[i]}MN "
          f"mid_react_abs={midwall_abs.get(s,'?')}MN conv_mean={conv_mean.get(s,'?')}mm conv_max={conv_max.get(s,'?')}mm")

fig, ax = plt.subplots(1, 3, figsize=(16, 4.5))
xs = stages

# (a) mid crack count vs stage (deliverable) on OWN axis; end band on twin axis (excluded)
ax[0].plot(xs, mid_cr, 'o-', color='crimson', lw=2.5, ms=9, label='MID (y870-900) DELIVERABLE')
for xi, yi in zip(xs, mid_cr):
    ax[0].annotate(str(yi), (xi, yi), textcoords='offset points', xytext=(0, 8), ha='center', color='crimson', fontweight='bold')
ax[0].set_xlabel('stage'); ax[0].set_ylabel('MID crack count', color='crimson'); ax[0].set_xticks(xs)
ax[0].set_ylim(-0.5, max(mid_cr) + 2); ax[0].tick_params(axis='y', labelcolor='crimson')
axb = ax[0].twinx()
axb.plot(xs, end_cr, 's--', color='gray', lw=1, alpha=0.5, label='end-band (EXCLUDED, artifact)')
axb.set_ylabel('end-band count (excluded)', color='gray'); axb.tick_params(axis='y', labelcolor='gray')
ax[0].set_title('mid-tunnel lining crack onset by stage (invert tension)')
ax[0].legend(loc='upper left', fontsize=8); axb.legend(loc='lower right', fontsize=7)

# (b) mid reaction (abs sum) + total wz (contaminated, dashed)
mr = [midwall_abs.get(s, np.nan) for s in xs]
ax[1].plot(xs, mr, 'o-', color='navy', lw=2, label='MID coupling |normal| sum')
ax[1].plot(xs, wz_tot, 's--', color='gray', lw=1, alpha=0.6, label='wz_total (end-contaminated)')
ax[1].set_xlabel('stage'); ax[1].set_ylabel('reaction (MN)'); ax[1].set_xticks(xs)
ax[1].set_title('mid-tunnel lining reaction by stage'); ax[1].legend(fontsize=8)

# (c) mid convergence vs stage
cm = [conv_mean.get(s, np.nan) for s in xs]
cx = [conv_max.get(s, np.nan) for s in xs]
ax[2].plot(xs, cm, 'o-', color='green', lw=2, label='radial-inward mean')
ax[2].plot(xs, cx, '^-', color='darkgreen', lw=1, label='radial-inward max')
ax[2].set_xlabel('stage'); ax[2].set_ylabel('convergence (mm)'); ax[2].set_xticks(xs)
ax[2].set_title('mid-tunnel lining convergence by stage'); ax[2].legend(fontsize=8)

plt.tight_layout()
plt.savefig('couple_evolution.png', dpi=110)
print("WROTE couple_evolution.png")
