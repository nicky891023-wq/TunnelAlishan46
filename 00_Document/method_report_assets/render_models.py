"""render_models.py -- 360-degree orbit GIFs + hero PNGs of the three models (07-12 v3).
Standard spec (Wade): Times New Roman English text, LARGE fonts, thesis-figure layer
palettes, light-grey mesh edges on the large/small models, flat clip faces (no ragged
tets) on the small-model quarter cutaway, shell lining visible in the cutaway.
Outputs into this assets folder:
  large_orbit.gif / large_hero.png     (4-layer tet slope model, light-grey wireframe)
  small_orbit.gif / small_hero.png     (6-layer + annulus, flat quarter notch + shell)
  couple_orbit.gif / couple_hero.png   (hex rock y<885 cutaway + PFC ball lining)
Run from this folder:  python render_models.py
"""
import numpy as np
import pyvista as pv

pv.OFF_SCREEN = True
ROOT = r'C:\Users\Wade\Desktop\Tunnel_TX'
N_FRAMES, STEP = 60, 6
WIN = (1440, 1080)
FONT = 'times'
FS_TITLE = 20
FS_LEG = 17

# Thesis-figure layer palettes (= render_lg_model / render_sm_model / 圖5-04)
PAL_LARGE = {'layer1': '#e8d9a0', 'layer2': '#cdae6b',
             'layer3': '#a98c4b', 'layer4': '#7c6840'}
PAL_SMALL = {'layer1': '#efe0b0', 'layer2': '#dcc078', 'layer3': '#c1a15c',
             'layer4': '#a08349', 'layer5': '#82683c', 'layer6': '#655232',
             'lining': '#b8d4e8'}
LEG_NAME = {'lining': 'annulus (k x100)'}
BALLC = '#a86e3c'          # PFC lining balls, same as 圖5-04
ROCKC = '#d9cbb0'          # coupled equivalent elastic rock, same tint as 圖5-04 box
SHELLC = '#6f7c8b'         # shell lining in the small-model cutaway

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
        plotter.camera.zoom(0.85)
    else:
        plotter.camera_position = cam
    plotter.screenshot(hero)
    plotter.open_gif(gif, fps=9)
    for _ in range(N_FRAMES):
        plotter.camera.azimuth = plotter.camera.azimuth + STEP
        plotter.write_frame()
    plotter.close()
    print('wrote', gif, '+', hero)

def add_grouped(plotter, grid, names, edges, pal, opacity=1.0,
                edge_color='#8a8a8a', line_width=0.3):
    surf = grid.extract_surface()
    cols = [pal.get(n, '#999999') for n in names]
    plotter.add_mesh(surf, scalars='grp', cmap=cols, clim=(-0.5, len(names) - 0.5),
                     show_edges=edges, edge_color=edge_color, line_width=line_width,
                     show_scalar_bar=False, opacity=opacity,
                     ambient=0.45, diffuse=0.72, specular=0.06)
    return cols

def tnr_legend(plotter, names, cols):
    """Times-New-Roman legend: one coloured text line per entry, bottom-right stack."""
    for i, (n, c) in enumerate(zip(names[::-1], cols[::-1])):
        label = LEG_NAME.get(n, n)
        plotter.add_text(label, position=(WIN[0] - 300, 26 + 30 * i),
                         font_size=FS_LEG, color=c, font=FONT, shadow=False)

def title(plotter, text):
    plotter.add_text(text, position='upper_left', font_size=FS_TITLE,
                     color='#1a2433', font=FONT)

# ---------------- 1. LARGE ----------------
print('LARGE: parsing...')
pts, gr = read_inp(ROOT + r'\01_LargeModel\process\large_tet.inp', 4)
grid, names = grid_from(pts, gr, pv.CellType.TETRA, 4)
print('  cells', grid.n_cells)
p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
# light-grey wireframe (Wade 07-12): pale enough that the 1-px edges tint, not darken
cols = add_grouped(p, grid, names, edges=True, pal=PAL_LARGE,
                   edge_color='#c9c9c9', line_width=0.3)
tnr_legend(p, names, cols)
title(p, 'LARGE - slope scale: 511,988 tet zones / 4 layers')
orbit(p, 'large_orbit.gif', 'large_hero.png', elev=22)

# ---------------- 2. SMALL ----------------
print('SMALL: parsing...')
pts, gr = read_inp(ROOT + r'\02_SmallModel\process\small_conformal.inp', 4)
grid, names = grid_from(pts, gr, pv.CellType.TETRA, 4)
print('  cells', grid.n_cells)
# quarter notch removed with FLAT clip faces (Wade: 切出面、不要稜稜角角)
b = grid.bounds
notch = grid.clip_box(bounds=(1298.0, b[1], 898.0, b[3], b[4], b[5]), invert=True)
notch.cell_data['grp'] = notch.cell_data['grp'].astype(np.int64)
# shell lining ring, shown inside the exposed bore (y > clip start only where visible)
sh = np.loadtxt(ROOT + r'\05_One_Way_Simulation\process\sm_shells.txt', skiprows=1)
tris = sh[:, 1:10].reshape(-1, 3, 3)
shell_poly = pv.PolyData(tris.reshape(-1, 3),
                         np.hstack([np.full((len(tris), 1), 3),
                                    np.arange(len(tris) * 3).reshape(-1, 3)]).astype(np.int64))

def cut_cam(mesh, dist=1.75):
    bb = np.array(mesh.bounds).reshape(3, 2)
    c = bb.mean(1)
    diag = np.linalg.norm(bb[:, 1] - bb[:, 0])
    d = np.array([0.62, 1.15, 0.55]); d = d / np.linalg.norm(d)
    return [tuple(c + d * diag * dist), tuple(c), (0, 0, 1)]

p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
cols = add_grouped(p, notch, names, edges=True, pal=PAL_SMALL,
                   edge_color='#c2c2c2', line_width=0.3)
p.add_mesh(shell_poly, color=SHELLC, smooth_shading=True,
           ambient=0.5, diffuse=0.7, specular=0.15)
tnr_legend(p, names + ['shell lining'], cols + [SHELLC])
title(p, 'SMALL - tunnel scale: 1,433,466 tet zones / 6 layers + annulus + shell lining')
orbit(p, 'small_orbit.gif', 'small_hero.png', cam=cut_cam(notch))

# ---------------- 3. COUPLED ----------------
print('COUPLE: parsing...')
pts, gr = read_inp(ROOT + r'\03_CoupleModel\process\couple_hex.inp', 8)
grid, names = grid_from(pts, gr, pv.CellType.HEXAHEDRON, 8)
print('  cells', grid.n_cells)
half = grid.clip(normal=[0, 1, 0], origin=(1297, 885, 1748))   # keep y<885
balls = np.loadtxt(ROOT + r'\05_One_Way_Simulation\process\ring3d_G4.txt', skiprows=1)
b2 = balls[balls[:, 1] < 885.0]
sub = b2[np.random.default_rng(1).choice(len(b2), min(len(b2), 170000), replace=False)]
cloud = pv.PolyData(sub[:, :3])
p = pv.Plotter(off_screen=True, window_size=WIN)
p.set_background('white')
surf = half.extract_surface()
p.add_mesh(surf, color=ROCKC, show_edges=True, edge_color='#a99e86', line_width=0.4,
           ambient=0.45, diffuse=0.72, specular=0.06)
p.add_mesh(cloud, color=BALLC, point_size=4.6, render_points_as_spheres=True)
tnr_legend(p, ['E_eq elastic rock', 'PFC lining balls'], [ROCKC, BALLC])
title(p, 'COUPLED - lining scale: 424,908 hex zones (E_eq) + 456,163 bonded balls')
orbit(p, 'couple_orbit.gif', 'couple_hero.png', cam=cut_cam(half, 1.8))
print('ALL DONE')
