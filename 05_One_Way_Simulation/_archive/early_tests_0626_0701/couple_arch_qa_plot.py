"""couple_arch_qa_plot.py <prefix> -- Codex-spec visual pack for the BLUE-LINE arch deliverable.
Reads <prefix>_cracks.txt (x y z type diam age). Splits cracks by region:
  BLUE-LINE (load): y in mid-band [870,900] AND ang NOT in [250,320] (sidewalls+crown)
  FIXED-CORNER (artifact): y in [870,900] AND ang in [250,320]
  Y-END (artifact): y outside [870,900]
Produces <prefix>_archqa.png:
  (a) D-shape x-z cross-section, blue-line cracks (crimson) vs fixed-corner (gray) vs region guides
  (b) crack count by region (bar) -- counts must match the FULL-RESULT log line
  (c) circumferential sector histogram of MID-band cracks, blue-line bins highlighted vs corner band
Fixed axes/colors for cross-stage comparison. Tunnel axis (cx,cz)=(1297,1747.5)."""
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

CX, CZ = 1297.0, 1747.5
YMID = (870.0, 900.0)
CORNER = (250.0, 320.0)   # fixed-corner + bottom-gap band (excluded, Codex)

pfx = sys.argv[1] if len(sys.argv) > 1 else 'full_s4'
fn = f'{pfx}_cracks.txt'
try:
    d = np.loadtxt(fn, skiprows=1)
except Exception as e:
    print(f"cannot read {fn}: {e}")
    sys.exit(1)
if d.ndim == 1:
    d = d[None, :]
if len(d) == 0:
    print(f"{fn}: 0 cracks")
    sys.exit(0)

x, y, z, typ = d[:, 0], d[:, 1], d[:, 2], d[:, 3].astype(int)
ang = np.degrees(np.arctan2(z - CZ, x - CX)) % 360
inmid = (y >= YMID[0]) & (y <= YMID[1])
iscorner = (ang >= CORNER[0]) & (ang <= CORNER[1])
blue = inmid & ~iscorner       # blue-line deliverable
corner = inmid & iscorner      # fixed-corner artifact
yend = ~inmid                  # y-end artifact

print(f"{pfx}: total={len(d)}  BLUE-LINE(deliverable)={blue.sum()}  fixed-corner(excl)={corner.sum()}  y-end(excl)={yend.sum()}")

fig = plt.figure(figsize=(16, 5))

# (a) D-shape x-z cross-section
ax = fig.add_subplot(1, 3, 1)
ax.scatter(x[blue], z[blue], s=40, c='crimson', edgecolors='k', lw=0.4, label=f'BLUE-LINE cracks ({blue.sum()})', zorder=5)
ax.scatter(x[corner], z[corner], s=25, c='gray', alpha=0.5, label=f'fixed-corner (excl, {corner.sum()})', zorder=4)
th = np.linspace(0, 2 * np.pi, 200)
for r in (1.35, 4.7):
    ax.plot(CX + r * np.cos(th), CZ + r * np.sin(th), 'k--', lw=0.5, alpha=0.4)
# shade the excluded corner band
for a0 in np.radians(np.linspace(CORNER[0], CORNER[1], 30)):
    ax.plot([CX, CX + 6 * np.cos(a0)], [CZ, CZ + 6 * np.sin(a0)], color='gray', alpha=0.05, lw=2)
ax.plot(CX, CZ, 'k+', ms=10)
ax.annotate('crown', (CX, CZ + 5), ha='center', fontsize=8)
ax.annotate('R-wall', (CX + 5, CZ), va='center', fontsize=8)
ax.annotate('L-wall', (CX - 5, CZ), va='center', ha='right', fontsize=8)
ax.annotate('fixed corners\n(excluded)', (CX, CZ - 5.2), ha='center', fontsize=7, color='gray')
ax.set_xlabel('x'); ax.set_ylabel('z'); ax.set_aspect('equal')
ax.set_xlim(CX - 7, CX + 7); ax.set_ylim(CZ - 7, CZ + 7)
ax.set_title(f'{pfx}: MID blue-line arch cracks (x-z)'); ax.legend(fontsize=7, loc='upper right')

# (b) crack count by region
ax2 = fig.add_subplot(1, 3, 2)
cats = ['BLUE-LINE\n(deliverable)', 'fixed-corner\n(excl)', 'y-end\n(excl)']
vals = [blue.sum(), corner.sum(), yend.sum()]
cols = ['crimson', 'gray', 'lightgray']
ax2.bar(cats, vals, color=cols, edgecolor='k')
for i, v in enumerate(vals):
    ax2.annotate(str(v), (i, v), textcoords='offset points', xytext=(0, 4), ha='center', fontweight='bold')
ax2.set_ylabel('crack count'); ax2.set_title('crack count by region (artifacts excluded)')

# (c) MID-band sector histogram, corner band shaded
ax3 = fig.add_subplot(1, 3, 3)
bins = np.arange(0, 361, 15)
ax3.hist(ang[inmid], bins=bins, color='crimson', alpha=0.8)
ax3.axvspan(CORNER[0], CORNER[1], color='gray', alpha=0.3, label='fixed-corner band (excl)')
ax3.set_xlabel('circumferential angle (deg; 0=R-wall,90=crown,180=L-wall,270=bottom)')
ax3.set_ylabel('mid-band crack count'); ax3.set_xticks(np.arange(0, 361, 45))
ax3.set_title('mid-band crack angular distribution'); ax3.legend(fontsize=8)

plt.tight_layout()
out = f'{pfx}_archqa.png'
plt.savefig(out, dpi=115)
print(f"WROTE {out}")
