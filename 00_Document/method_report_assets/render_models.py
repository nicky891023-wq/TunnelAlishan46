"""render_models.py -- GUI-style 360-degree orbit GIFs + hero PNGs of the three models.
Parses the ABAQUS .inp meshes (groups preserved) and the exported ball cloud, renders
with pyvista/VTK off-screen. Outputs into this assets folder:
  large_orbit.gif / large_hero.png     (4-layer tet slope model, full exterior)
  small_orbit.gif / small_hero.png     (6-layer + lining tet model, y<900 cutaway)
  couple_orbit.gif / couple_hero.png   (hex rock y<885 cutaway + PFC ball lining)
Run from this folder:  python render_models.py
"""
import numpy as np
import pyvista as pv

pv.OFF_SCREEN = True
ROOT = r'C:\Users\Wade\Desktop\Tunnel_TX'
N_FRAMES, STEP = 60, 6
WIN = (960, 720)

# FLAC-GUI-like categorical colors (consistent layer palette across models)
PAL = {
    'layer1': '#c8a165', 'layer2': '#7fbf6b', 'layer3': '#5b9bd5',
    'layer4': '#c96a6a', 'layer5': '#8f7bd5', 'layer6': '#4d4d6b',
    'lining': '#d94040', 'balls': '#d8c9a3',
}

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
                    name = ls.split('=')[-1].strip()
                    elems.setdefault(name, [])
                    cur = ('E', name)
                else:
                    cur = None
            elif cur:
                t = [x for x in ls.replace(',', ' ').split() if x]
                if not t:
                    continue
                if cur[0] == 'N':
                    nodes[int(t[0])] = [float(t[1]), float(t[2]), float(t[3])]
                else:
                    elems[cur[1]].append([int(x) for x in t[1:1 + nnode]])
    ids = np.array(sorted(nodes))
    idmap = np.zeros(ids.max() + 1, dtype=np.int64)
    idmap[ids] = np.arange(len(ids))
    pts = np.array([nodes[i] for i in ids])
    out = {g: idmap[np.array(v)] for g, v in elems.items() if v}
    return pts, out

def grid_from(pts, groups, celltype, nnode):
    conn, ctypes, gid, names = [], [], [], sorted(groups)
    for k, g in enumerate(names):
        arr = groups[g]
        conn.append(np.hstack([np.full((len(arr), 1), nnode, dtype=np.int64), arr]).ravel())
        ctypes.append(np.full(len(arr), celltype, dtype=np.uint8))
        gid.append(np.full(len(arr), k))
    grid = pv.UnstructuredGrid(np.concatenate(conn), np.concatenate(ctypes), pts)
    grid.cell_data['grp'] = np.concatenate(gid)
    return grid, names

def orbit(plotter, gif, hero, elev=18, cam=None):
    if cam is None:
        plotter.camera_position = 'iso'
        plotter.camera.elevation = elev
        plotter.camera.zoom(0.80)
    else:
        plotter.camera_position = cam
    plotter.screenshot(hero)
    plotter.open_gif(gif, fps=9)
    for _ in range(N_FRAMES):
        plotter.camera.azimuth = plotter.camera.azimuth + STEP
        plotter.write_frame()
    plotter.close()
    print('wrote', gif, '+', hero)

def add_grouped(plotter, grid, names, edges, opacity=1.0):
    surf = grid.extract_surface()
    cols = [PAL.get(n, '#999999') for n in names]
    plotter.add_mesh(surf, scalars='grp', cmap=cols, clim=(-0.5, len(names) - 0.5),
                     show_edges=edges, edge_color='#3a3a3a', line_width=0.5,
                     show_scalar_bar=False, opacity=opacity,
                     ambient=0.38, diffuse=0.75, specular=0.08)
    return cols

def legend(plotter, names, cols):
    plotter.add_legend(list(zip(names, cols)), bcolor='white', border=True,
                       size=(0.16, 0.028 * len(names)), loc='lower right')

# ---------------- 1. LARGE ----------------
print('LARGE: parsing...')
pts, gr = read_inp(ROOT + r'\01_LargeModel\process\large_tet.inp', 4)
grid, names = grid_from(pts, gr, pv.CellType.TETRA, 4)
print('  cells', grid.n_cells)
p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
cols = add_grouped(p, grid, names, edges=True)
legend(p, names, cols)
p.add_text('LARGE  slope-scale  511,988 tet / 4 layers', font_size=13, color='#222233')
orbit(p, 'large_orbit.gif', 'large_hero.png', elev=22)  # rendered OK earlier

# ---------------- 2. SMALL ----------------
print('SMALL: parsing...')
pts, gr = read_inp(ROOT + r'\02_SmallModel\process\small_conformal.inp', 4)
grid, names = grid_from(pts, gr, pv.CellType.TETRA, 4)
print('  cells', grid.n_cells)
cc = grid.cell_centers().points
mask = ~((cc[:, 1] > 900.0) & (cc[:, 0] > 1297.0))   # remove corner wedge -> 3/4 model,
half = grid.extract_cells(mask)                       # longitudinal cut through tunnel axis
def cut_cam(mesh, dist=1.75):
    b = np.array(mesh.bounds).reshape(3, 2)
    c = b.mean(1)
    diag = np.linalg.norm(b[:, 1] - b[:, 0])
    d = np.array([0.62, 1.15, 0.55]); d = d / np.linalg.norm(d)
    return [tuple(c + d * diag * dist), tuple(c), (0, 0, 1)]
p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
cols = add_grouped(p, half, names, edges=True)
legend(p, names, cols)
p.add_text('SMALL  tunnel-scale  1,433,466 tet / 6 layers + lining ring  (corner wedge removed)', font_size=13, color='#222233')
orbit(p, 'small_orbit.gif', 'small_hero.png', cam=cut_cam(half))

# ---------------- 3. COUPLED ----------------
print('COUPLE: parsing...')
pts, gr = read_inp(ROOT + r'\03_CoupleModel\process\couple_hex.inp', 8)
grid, names = grid_from(pts, gr, pv.CellType.HEXAHEDRON, 8)
print('  cells', grid.n_cells)
half = grid.clip(normal=[0, 1, 0], origin=(1297, 885, 1748))   # keep y<885
balls = np.loadtxt(ROOT + r'\04_InitialBalance\process\couple_solve\geom_balls.txt', skiprows=1)
b = balls[balls[:, 1] < 885.0]
sub = b[np.random.default_rng(1).choice(len(b), min(len(b), 170000), replace=False)]
cloud = pv.PolyData(sub[:, :3])
p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
surf = half.extract_surface()
p.add_mesh(surf, color='#9fb2c4', show_edges=True, edge_color='#42566b', line_width=0.5,
           ambient=0.38, diffuse=0.75, specular=0.08)
p.add_mesh(cloud, color=PAL['balls'], point_size=4.6, render_points_as_spheres=True)
legend(p, ['equivalent elastic rock (E_eq)', 'PFC lining balls'], ['#9fb2c4', PAL['balls']])
p.add_text('COUPLED  lining-scale  424,908 hex rock (single equivalent elastic) + 456,302 bonded balls', font_size=13, color='#222233')
orbit(p, 'couple_orbit.gif', 'couple_hero.png', cam=cut_cam(half, 1.8))
print('ALL DONE')
