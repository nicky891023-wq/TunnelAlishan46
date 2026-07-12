"""make_scale_zoom.py -- progressive-focus trio (07-12 v2, standard spec):
SAME y=885 cross-section of the three meshes, each panel framing the next model's
extent. Times New Roman English, large fonts, thesis-figure layer palettes,
coupled panel uses the CURRENT G4 recast ball ring (old fallen-ball dump retired).
Run from this assets folder:  python make_scale_zoom.py
"""
import numpy as np, pyvista as pv
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['axes.unicode_minus'] = False

pv.OFF_SCREEN = True
ROOT = r'C:\Users\Wade\Desktop\Tunnel_TX'
PAL_LARGE = {'layer1': '#e8d9a0', 'layer2': '#cdae6b',
             'layer3': '#a98c4b', 'layer4': '#7c6840'}
PAL_SMALL = {'layer1': '#efe0b0', 'layer2': '#dcc078', 'layer3': '#c1a15c',
             'layer4': '#a08349', 'layer5': '#82683c', 'layer6': '#655232',
             'lining': '#b8d4e8'}
ROCKC = '#d9cbb0'
BALLC = '#a86e3c'
Y = 885.0

def read_inp(path, nnode):
    nodes, elems, cur = {}, {}, None
    with open(path) as f:
        for line in f:
            ls = line.strip()
            if ls.startswith('*'):
                up = ls.upper()
                if up.startswith('*NODE'):
                    cur = ('N',)
                elif up.startswith('*ELEMENT'):
                    elems.setdefault(ls.split('=')[-1].strip(), [])
                    cur = ('E', ls.split('=')[-1].strip())
                else:
                    cur = None
            elif cur:
                t = [x for x in ls.replace(',', ' ').split() if x]
                if not t: continue
                if cur[0] == 'N':
                    nodes[int(t[0])] = [float(t[1]), float(t[2]), float(t[3])]
                else:
                    elems[cur[1]].append([int(x) for x in t[1:1+nnode]])
    ids = np.array(sorted(nodes))
    idmap = np.zeros(ids.max()+1, dtype=np.int64); idmap[ids] = np.arange(len(ids))
    pts = np.array([nodes[i] for i in ids])
    return pts, {g: idmap[np.array(v)] for g, v in elems.items() if v}

def grid_from(pts, groups, ct, nn):
    conn, cts, gid, names = [], [], [], sorted(groups)
    for k, g in enumerate(names):
        a = groups[g]
        conn.append(np.hstack([np.full((len(a),1), nn, dtype=np.int64), a]).ravel())
        cts.append(np.full(len(a), ct, dtype=np.uint8)); gid.append(np.full(len(a), k))
    gr = pv.UnstructuredGrid(np.concatenate(conn), np.concatenate(cts), pts)
    gr.cell_data['grp'] = np.concatenate(gid)
    return gr, names

def render_slice(grid, names, pal, box, xr, zr, fname, balls=None, lw=0.4,
                 edge='#9a9a9a'):
    sl = grid.slice(normal=[0,1,0], origin=(0, Y, 0))
    p = pv.Plotter(off_screen=True, window_size=(1100, 900))
    p.set_background('white')
    cols = [pal.get(n, '#999999') for n in names]
    p.add_mesh(sl, scalars='grp', cmap=cols, clim=(-0.5, len(names)-0.5),
               show_edges=True, edge_color=edge, line_width=lw,
               show_scalar_bar=False, ambient=0.9, diffuse=0.15)
    if balls is not None:
        p.add_mesh(pv.PolyData(balls), color=BALLC, point_size=3.2,
                   render_points_as_spheres=True)
    if box is not None:
        x0, x1, z0, z1 = box
        fr = pv.Box(bounds=(x0, x1, Y-0.5, Y-0.5, z0, z1)).extract_all_edges()
        p.add_mesh(fr, color='#c81e1e', line_width=6)
    cx, cz = (xr[0]+xr[1])/2, (zr[0]+zr[1])/2
    p.camera_position = [(cx, Y-200.0, cz), (cx, Y, cz), (0, 0, 1)]
    p.camera.parallel_projection = True
    p.camera.parallel_scale = (zr[1]-zr[0])/2 * 1.03
    p.screenshot(fname)
    print('slice ->', fname)

print('LARGE...')
pts, gr = read_inp(ROOT + r'\01_LargeModel\process\large_tet.inp', 4)
g, n = grid_from(pts, gr, pv.CellType.TETRA, 4)
render_slice(g, n, PAL_LARGE, (1250,1350,1700,1800), (450,2000), (800,2350),
             '_sz_large.png', lw=0.3)

print('SMALL...')
pts, gr = read_inp(ROOT + r'\02_SmallModel\process\small_conformal.inp', 4)
g, n = grid_from(pts, gr, pv.CellType.TETRA, 4)
render_slice(g, n, PAL_SMALL, (1277,1317,1728,1768), (1250,1350), (1700,1800),
             '_sz_small.png', lw=0.35, edge='#8a8a8a')

print('COUPLE...')
pts, gr = read_inp(ROOT + r'\03_CoupleModel\process\couple_hex.inp', 8)
g, n = grid_from(pts, gr, pv.CellType.HEXAHEDRON, 8)
# CURRENT ball ring: zero-gravity in-place recast (G4) -- no fallen balls
balls = np.loadtxt(ROOT + r'\05_One_Way_Simulation\process\ring3d_G4.txt', skiprows=1)
bsl = balls[np.abs(balls[:,1]-Y) < 0.35][:, :3]
g.cell_data['grp'] = np.zeros(g.n_cells, dtype=int)   # single equivalent material
render_slice(g, ['rock'], {'rock': ROCKC}, None, (1277,1317), (1728,1768),
             '_sz_couple.png', balls=bsl, lw=0.5, edge='#a99e86')

print('compose...')
imgs = [Image.open(f) for f in ['_sz_large.png','_sz_small.png','_sz_couple.png']]
fig, axes = plt.subplots(1, 3, figsize=(21, 7.2))
titles = ['Slope scale (2 km)\nsection y = 885 m; red frame = 100 m tunnel-scale box',
          'Tunnel scale (100 m)\nred frame = 40 m coupled box',
          'Coupled lining scale (40 m)\nsingle equivalent rock + bonded-ball lining']
for ax, im, t in zip(axes, imgs, titles):
    ax.imshow(im); ax.set_title(t, fontsize=19); ax.axis('off')
fig.text(0.352, 0.5, r'$\Longrightarrow$', fontsize=42, color='#B33535',
         ha='center', va='center')
fig.text(0.672, 0.5, r'$\Longrightarrow$', fontsize=42, color='#B33535',
         ha='center', va='center')
fig.text(0.352, 0.36, 'x20 focus', fontsize=17, color='#B33535', ha='center')
fig.text(0.672, 0.36, 'x2.5 focus', fontsize=17, color='#B33535', ha='center')
plt.tight_layout()
plt.savefig('scale_zoom.png', dpi=150, bbox_inches='tight')
print('scale_zoom.png done')
