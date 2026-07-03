"""make_scale_zoom.py -- slide-12 trio: SAME y=885 cross-section of the three meshes,
progressive focusing (large -> small -> coupled), each panel framing the next model's
extent. Pure mesh rendering (pyvista slices, parallel projection) -- no FLAC needed.
Run from this assets folder."""
import numpy as np, pyvista as pv
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

pv.OFF_SCREEN = True
ROOT = r'C:\Users\Wade\Desktop\Tunnel_TX'
PAL = {'layer1':'#c8a165','layer2':'#7fbf6b','layer3':'#5b9bd5','layer4':'#c96a6a',
       'layer5':'#8f7bd5','layer6':'#4d4d6b','lining':'#d21f1f'}
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

def render_slice(grid, names, box, xr, zr, fname, balls=None, lw=0.5):
    sl = grid.slice(normal=[0,1,0], origin=(0, Y, 0))
    p = pv.Plotter(off_screen=True, window_size=(1100, 900))
    p.set_background('white')
    cols = [PAL.get(n, '#999999') for n in names]
    p.add_mesh(sl, scalars='grp', cmap=cols, clim=(-0.5, len(names)-0.5),
               show_edges=True, edge_color='#33404f', line_width=lw,
               show_scalar_bar=False, ambient=0.9, diffuse=0.15)
    if balls is not None:
        p.add_mesh(pv.PolyData(balls), color='#8a5a2a', point_size=3.0,
                   render_points_as_spheres=True)
    if box is not None:
        x0, x1, z0, z1 = box
        fr = pv.Box(bounds=(x0, x1, Y-0.5, Y-0.5, z0, z1)).extract_all_edges()
        p.add_mesh(fr, color='red', line_width=6)
    cx, cz = (xr[0]+xr[1])/2, (zr[0]+zr[1])/2
    p.camera_position = [(cx, Y-200.0, cz), (cx, Y, cz), (0, 0, 1)]
    p.camera.parallel_projection = True
    p.camera.parallel_scale = (zr[1]-zr[0])/2 * 1.03
    p.screenshot(fname)
    print('slice ->', fname)

print('LARGE...')
pts, gr = read_inp(ROOT + r'\01_LargeModel\process\large_tet.inp', 4)
g, n = grid_from(pts, gr, pv.CellType.TETRA, 4)
render_slice(g, n, (1250,1350,1700,1800), (450,2000), (800,2350), '_sz_large.png', lw=0.35)

print('SMALL...')
pts, gr = read_inp(ROOT + r'\02_SmallModel\process\small_conformal.inp', 4)
g, n = grid_from(pts, gr, pv.CellType.TETRA, 4)
render_slice(g, n, (1277,1317,1728,1768), (1250,1350), (1700,1800), '_sz_small.png', lw=0.4)

print('COUPLE...')
pts, gr = read_inp(ROOT + r'\03_CoupleModel\process\couple_hex.inp', 8)
g, n = grid_from(pts, gr, pv.CellType.HEXAHEDRON, 8)
balls = np.loadtxt(ROOT + r'\04_InitialBalance\process\couple_solve\geom_balls.txt', skiprows=1)
bsl = balls[np.abs(balls[:,1]-Y) < 0.35][:, :3]
gs, ns = g, n
# single-material look (final ruling): one color
gs.cell_data['grp'] = np.zeros(gs.n_cells, dtype=int)
render_slice(gs, ['rock'], None, (1277,1317), (1728,1768), '_sz_couple.png', balls=bsl, lw=0.6)

print('compose...')
imgs = [Image.open(f) for f in ['_sz_large.png','_sz_small.png','_sz_couple.png']]
fig, axes = plt.subplots(1, 3, figsize=(19.2, 6.4))
titles = ['大模｜邊坡尺度（2 km）\ny=885 剖面，紅框＝小模 100 m 箱',
          '小模｜隧道圍岩尺度（100 m）\n紅框＝耦合模 40 m 箱',
          '耦合模｜襯砌尺度（40 m）\n單一等效材料＋球體襯砌']
for ax, im, t in zip(axes, imgs, titles):
    ax.imshow(im); ax.set_title(t, fontsize=13); ax.axis('off')
fig.text(0.352, 0.5, '➜', fontsize=34, color='#B33535', ha='center', va='center')
fig.text(0.672, 0.5, '➜', fontsize=34, color='#B33535', ha='center', va='center')
fig.text(0.352, 0.40, '×20 聚焦', fontsize=12, color='#B33535', ha='center')
fig.text(0.672, 0.40, '×2.5 聚焦', fontsize=12, color='#B33535', ha='center')
plt.tight_layout()
plt.savefig('scale_zoom.png', dpi=135, bbox_inches='tight')
print('scale_zoom.png done')
