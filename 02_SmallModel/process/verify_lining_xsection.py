"""Plot a y~900 cross-section of small_conformal.inp coloured by group, to confirm
the lining ring follows the outer+inner design profile cleanly (no saw-tooth)."""
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

INP = 'small_conformal.inp'
nodes = {}
elsets = {}
cur = None
mode = None
with open(INP) as f:
    for ln in f:
        s = ln.strip()
        if s.startswith('*NODE'):
            mode = 'n'; continue
        if s.startswith('*ELEMENT'):
            mode = 'e'; cur = s.split('ELSET=')[1].strip(); elsets[cur] = []; continue
        if s.startswith('*'):
            mode = None; continue
        if not s:
            continue
        p = s.split(',')
        if mode == 'n':
            nodes[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
        elif mode == 'e':
            elsets[cur].append([int(x) for x in p[1:5]])

nid = np.array(sorted(nodes))
xyz = np.array([nodes[i] for i in nid])
idx = {int(t): k for k, t in enumerate(nid)}

YC = 900.0
fig, ax = plt.subplots(figsize=(9, 9))
colors = {'lining': 'red', 'layer1': '#bbb', 'layer2': '#aaa', 'layer3': '#999',
          'layer4': '#888', 'layer5': '#777', 'layer6': '#666'}
for name, tets in elsets.items():
    if not tets:
        continue
    tt = np.array(tets)
    c = xyz[[ [idx[n] for n in row] for row in tt ]].mean(axis=1)
    m = np.abs(c[:, 1] - YC) < 0.6
    if m.sum() == 0:
        continue
    ax.scatter(c[m, 0], c[m, 2], s=6 if name == 'lining' else 3,
               c=colors.get(name, 'k'), label=f'{name} ({m.sum()})',
               alpha=0.9 if name == 'lining' else 0.35, linewidths=0)
ax.set_aspect('equal'); ax.set_xlabel('x'); ax.set_ylabel('z')
ax.set_title(f'small_conformal.inp  cross-section y={YC}+-0.6  (lining=red)')
ax.legend(loc='upper right', fontsize=7)
# zoom on the tunnel
ax.set_xlim(1293, 1303); ax.set_ylim(1742, 1753)
plt.tight_layout(); plt.savefig('lining_xsection.png', dpi=110)
print('wrote lining_xsection.png')
# numeric: lining radial spread at this slice (should be ~0.40 m ring)
allc = []
for name in ['lining']:
    tt = np.array(elsets[name])
    c = xyz[[ [idx[n] for n in row] for row in tt ]].mean(axis=1)
    m = np.abs(c[:, 1] - YC) < 0.6
    allc = c[m]
cx, cz = 1297.0, 1747.5
r = np.hypot(allc[:, 0] - cx, allc[:, 2] - cz)
print(f'lining centroids near y=900: {len(allc)}  radial(to ~axis) min={r.min():.2f} max={r.max():.2f}')
