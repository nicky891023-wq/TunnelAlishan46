"""build_couple_hex.py -- structured all-hex (C3D8) rock for the Tunnel_TX coupled model:
an O-grid TUBE whose INNER ring is sampled EXACTLY on the raw wallzone_outter.stl excavation
wall, welded gp-to-gp to a "picture-frame" background of 4 transfinite (Coons) patches that
bridge the tunnel-local core box out to the 40x40 domain.  Output couple_hex.inp.

======================================================================================
EXACT-STL BORE FIX (2026-06-24)  -- the user opened the GUI and rejected the old bore
======================================================================================
THE PROBLEM that was rejected: the rock EXCAVATION SURFACE (the O-grid inner ring) did NOT
follow the lining outer-wall STL.  The old ring was (a) too COARSE/blocky and (b) built on a
RESAMPLED/SMOOTHED azimuth-ray-cast loop sitting 0.07-0.11 m OFF the raw STL, so `wall-zone
create` (wrapping the rock bore faces to couple the PFC lining balls) left a GAP.

THE FIX -- the inner ring is now sampled DIRECTLY on the RAW triangulated STL:
  1. RAW PLANE-SECTION.  At each O-grid y-plane the raw wallzone_outter.stl triangles are
     intersected with that y-plane (`plane_segments`) and the resulting segments are chained
     into the EXACT cross-section polyline (`raw_arch`).  The STL is an OPEN horseshoe arch
     (the invert/floor is a free rim -- 183 boundary edges at z~1744-1746, confirmed), so the
     chained result is an OPEN polyline from the right invert corner, up over the crown, to the
     left invert corner.  The bore is closed by a straight INVERT CHORD between the two corners.
  2. ARC-LENGTH NODES ON THE RAW POLYGON.  The inner-ring nodes are placed at FIXED normalized
     arc-length fractions along this raw closed polygon (arch by arc length + a few interior
     floor-chord nodes) -- NO smoothing, NO averaging, NO spline, NO azimuth ray-cast.  Hence
       (a) every ARCH node lies EXACTLY on the raw STL (node-to-STL ~ 0, vs the old 0.07-0.11 m);
       (b) node i is the SAME normalized arc position at every y (fixed fractions, anchored at the
           stable right-invert corner) => identical node correspondence => ZERO TWIST;
       (c) arc length is robust at the SHARP invert corners (no star-shapedness needed, unlike the
           old azimuth ray-cast which the prompt flagged).
     Arc length is also far more efficient than azimuth: ~140 arch nodes already give a faceted
     bore within < 0.01 m face-chord error of the raw STL EVERYWHERE (arch, springline, walls,
     invert, and the two bottom corners).  N_RING below is the inner-ring node count.

ZERO-FOLD O-GRID (why the background had to become a picture frame):
  A uniform-arc-length horseshoe inner ring mapped RADIALLY to a uniform-rectangle core-box
  perimeter FOLDS (mixed-sign Jacobian) because the two node distributions are too dissimilar.
  The cure is to give the O-grid OUTER ring the SAME normalized arc-length parametrization as the
  inner ring: outer node i sits at the same arc fraction around the core RECTANGLE as inner node i
  on the STL (`core_perim`).  Co-monotonic arc length => radial lines never cross => 0 mixed-sign,
  aspect p99 ~ 5, min scaled-Jacobian ~ 0.5.  But that makes the core-box perimeter NON-UNIFORM,
  so the old single-rectangle conformal background can no longer weld to it.  The background is
  therefore 4 transfinite (Coons) PATCHES -- a "picture frame" -- each bridging one core-box edge
  (fine, non-uniform) to the matching 40x40 domain edge (coarse, uniform), the 4 patches sharing
  the diagonal SEAM nodes from each box corner to the matching domain corner.  This is a standard
  multiblock submapping; it welds gp-to-gp to the tube (0 duplicate nodes) and is all-hex.

KEPT from prior work:
  * ZERO TWIST (now by fixed arc-length fractions + a stable corner anchor).
  * UNIFORM-CLEARANCE CORE BOX (W,HT,HB ~ uniform 1.4-1.7 m off the bore) -- the invert
    cell-collapse fix; the arc-matched O-grid keeps aspect low with NO collapsed band.
  * ALL-HEX C3D8, geology LAYERS 2..6 (classified by centroid vs S02..S05), the 40x40 box
    (x[1277,1317] z[1728,1768] y[860,910]).

C3D8 node ordering is fixed so the trilinear signed Jacobian is POSITIVE at all 8 corners
(the all-negative flip [4,5,6,7,0,1,2,3] is applied where needed).  Output couple_hex.inp
(*NODE + per-layer *ELEMENT type=C3D8 ELSET=layer2..layer6, 1-based, orphan-free).

Run with C:/Users/Wade/anaconda3/python.exe (numpy + scipy).  Does NOT launch FLAC3D.
"""
import os, sys, struct
import numpy as np
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator

HERE  = os.path.dirname(os.path.abspath(__file__))
SMALL = os.path.join(os.path.dirname(os.path.dirname(HERE)), '02_SmallModel', 'input')
WALL  = os.path.join(HERE, '..', 'input', 'wallzone_outter.stl')   # OUTER tunnel wall (rock excavation surface)
WALLIN = os.path.join(HERE, '..', 'input', 'wall_inner.stl')       # INNER clearance surface (train clearance boundary)
INP   = os.path.join(HERE, 'couple_hex.inp')

# ----- HEX edges + trilinear shape derivatives ------------------------------------
HEX_EDGES = [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]
_NATc = np.array([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
                  [-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]], float)
def _dNc(c):
    xi, eta, ze = _NATc[c]; dd = np.empty((8, 3))
    dd[:, 0] = 0.125*_NATc[:, 0]*(1+eta*_NATc[:, 1])*(1+ze*_NATc[:, 2])
    dd[:, 1] = 0.125*_NATc[:, 1]*(1+xi*_NATc[:, 0])*(1+ze*_NATc[:, 2])
    dd[:, 2] = 0.125*_NATc[:, 2]*(1+xi*_NATc[:, 0])*(1+eta*_NATc[:, 1])
    return dd
_DNc = [_dNc(c) for c in range(8)]
HE = np.array(HEX_EDGES); DN = np.array(_DNc)

# ----- 40 x 40 domain --------------------------------------------------------------
BX0, BX1 = 1277.0, 1317.0          # domain x (tunnel center 1297 +- 20)
BZ0, BZ1 = 1728.0, 1768.0          # domain z (tunnel center 1748 +- 20)
Y0,  Y1  = 860.0,  910.0           # domain y
NG  = 25                           # S-surface sample grid (per axis)
EPS = 0.20                         # min surface separation (no inversion)

# tunnel-local O-grid core box (uniform ~1.7-2.0 m clearance off the worst-case +-3.0 m bore;
# a slightly larger box than before keeps the worst radial cell -- at the sharp left invert corner
# -- from skewing, lifting the tube min scaled-Jacobian from ~0.25 to ~0.34).
W, HT, HB = 4.8, 5.0, 4.8          # half-width / top / bottom
NRT  = 9                           # radial cells in the O-grid tube (wall -> core box)
GT   = 1.06                        # tube radial growth (toward the core box)

# ==================================================================================================
# CUBIC-CELL REBALANCE (2026-06-24) -- the user asked for the ROCK cells to be CLOSER TO CUBIC
# (aspect -> 1) while the bore STILL follows wallzone_outter.stl EXACTLY.  Cells were ~0.10 (circumf)
# x ~0.55 (axial DY) x ~0.17 (radial) => aspect ~6.  The cure is to EQUALISE the three local cell
# spacings (circumferential along the ring, axial along y, radial outward) instead of leaving the
# bore ring far denser than the y-sweep.  The four levers, and how each was chosen:
#
#  (1) N_RING / N_FLOOR -- inner-ring node count.  REDUCED 160 -> 116.  The bore->STL face error is
#      governed ONLY by the ARCH node count na = N_RING - N_FLOOR (the invert-chord nodes are off the
#      STL).  na=88 is a verified "sweet spot": every arch node lies exactly on the raw STL (node->STL
#      = 0.000 m) and the worst face-midpoint->STL is 0.0039 m (identical to the old na=146 mesh, and
#      well under the 0.02 m limit) -- the faceting happens to align with the sharp springline feature
#      at na=88.  na=88 gives ~0.167 m circumferential spacing (was ~0.10 m), matching the axial &
#      radial spacings below.  N_FLOOR was RAISED 14 -> 28 (decoupled from the arch: na stays 88):
#      the 28 invert-chord nodes feed the BOTTOM 40x40 domain edge of the picture frame, whose cell
#      was the single worst in the mesh (only 14 nodes over 40 m => 2.86 m wide => frame aspect ~6 at
#      the domain corner).  With 28 chord nodes the bottom domain edge is ~1.43 m, balanced with the
#      other three domain edges (~1.3-1.5 m), which is what actually collapsed the frame aspect.
#  (4) DY -- axial sweep step.  REFINED 0.55 -> 0.45 m so the axial cell ~ the 0.167 m-class in-plane
#      spacing near the tube and ~ the frame in-plane spacing in the far field.  0.45 m is the BALANCE
#      point: smaller DY makes the tube more cubic but re-elongates the coarse far-field frame cells
#      (single global DY cannot be both 0.17 m at the bore and 1.4 m at the domain corner); 0.45 m is
#      where tube and frame aspect cross (~3.3) and global aspect p99 is minimised.
#  (2)/(3) NRT/GT (tube radial) and NSEAM/GSEAM (frame radial) -- the tube radial spacing (~0.167 m
#      at NRT=9) already matched; NSEAM was set to 24 (graded growth 1.05) so the frame radial cell
#      grows smoothly from ~0.17 m at the box to the domain edge without an over-stretched ring.
#
# RESULT (verified): aspect median 3.02->1.84, p99 5.93->3.31, max 6.37->3.75; tube p99 6.23->3.31;
# min scaled-Jacobian 0.338->0.407; 364,000 -> 424,908 hexes (well under the 1.2 M ceiling); bore
# node->STL 0.000 m, face-mid->STL 0.0039 m; 0 mixed-sign, 0 duplicate, twist < 0.05 deg.  The
# residual p99~3.3 (vs the cubic ideal 1.0) is the irreducible far-field limit of a SINGLE global DY:
# the domain-corner frame cells are inherently coarse (1.4-1.6 m) so cannot be 0.45 m-cubic without a
# graded axial step (which the structured y-sweep does not provide).  Finer = more cells, same p99.
# ==================================================================================================
N_RING = 116                       # total inner-ring nodes (arch na=88 + invert-chord N_FLOOR)
N_FLOOR = 28                       # invert-chord nodes (also feeds the bottom 40x40 domain edge)

# picture-frame background: radial cells from each core-box edge out to the 40x40 domain edge.
# 2026-06-24 cubic rebalance: NSEAM 16 -> 24 graded with GSEAM 1.05 so the frame radial cell grows
# smoothly from ~0.17 m at the box to the domain edge, keeping the frame cells near-cubic out to the
# far field (with the N_FLOOR=28 fix above balancing the tangential domain-edge density).
NSEAM = 24                         # radial cells along each diagonal box-corner -> domain-corner seam
GSEAM = 1.05                       # seam radial growth (fine at the box, coarse at the domain)

DY  = 0.45                         # y sweep step (cubic rebalance: 0.55 -> 0.45, the tube/frame balance)
GAP = 0.6                          # min clamp gap (geology surface kept off the domain edge)

fr = lambda n, g: np.concatenate([[0.0], np.cumsum(g**np.arange(n))]) / np.sum(g**np.arange(n))
FT = fr(NRT, GT)                   # tube radial node fractions (wall=0 .. core box=1)
FS = fr(NSEAM, GSEAM)              # seam radial node fractions (box=0 .. domain=1)


# ----- STL parsers (ASCII or binary) ----------------------------------------------
def stl_vertices(path):
    """Flat (3*ntri, 3) vertex array (used for the geology S0x.stl surfaces)."""
    d = open(path, 'rb').read()
    if d[:5] == b'solid' and b'facet' in d[:2000]:
        vs = []
        for ln in d.decode('latin-1').splitlines():
            ln = ln.strip()
            if ln.startswith('vertex'):
                p = ln.split(); vs.append((float(p[1]), float(p[2]), float(p[3])))
        return np.array(vs, float)
    n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d, dtype=np.uint8, count=n*50, offset=84).reshape(n, 50)
    return np.frombuffer(a[:, 12:48].tobytes(), dtype='<f4').reshape(n*3, 3).astype(float)


def stl_triangles(path):
    """(ntri, 3, 3) triangle array of the raw STL (used for exact y-plane sections of the bore)."""
    d = open(path, 'rb').read()
    if d[:5] == b'solid' and b'facet' in d[:2000]:
        vs = []
        for ln in d.decode('latin-1').splitlines():
            ln = ln.strip()
            if ln.startswith('vertex'):
                p = ln.split(); vs.append((float(p[1]), float(p[2]), float(p[3])))
        return np.array(vs, float).reshape(-1, 3, 3)
    n = struct.unpack('<I', d[80:84])[0]
    a = np.frombuffer(d, dtype=np.uint8, count=n*50, offset=84).reshape(n, 50)
    return np.frombuffer(a[:, 12:48].tobytes(), dtype='<f4').reshape(n, 3, 3).astype(float)


# ====================================================================================
#  RAW STL CROSS-SECTION  (exact y-plane intersection of the bore wall)
# ====================================================================================
def plane_segments(T, y):
    """Intersect the raw triangles T (ntri,3,3) with the plane y=const.  Each triangle that
    straddles the plane contributes ONE (x,z)->(x,z) segment.  Returns a list of (a,b) segments
    (a,b length-2 (x,z) arrays).  This is the EXACT raw cross-section of wallzone_outter.stl --
    no smoothing or resampling whatsoever."""
    yv = T[:, :, 1]
    sel = (yv.min(1) <= y) & (yv.max(1) >= y)
    segs = []
    for tri in T[sel]:
        d = tri[:, 1] - y
        pts = []
        for a, b in ((0, 1), (1, 2), (2, 0)):
            da, db = d[a], d[b]
            if (da < 0 and db > 0) or (da > 0 and db < 0):
                t = da / (da - db)
                p = tri[a] + t * (tri[b] - tri[a])
                pts.append((p[0], p[2]))
            elif da == 0:
                pts.append((tri[a, 0], tri[a, 2]))
        up = []
        for q in pts:
            if not any(abs(q[0]-u[0]) < 1e-9 and abs(q[1]-u[1]) < 1e-9 for u in up):
                up.append(q)
        if len(up) == 2:
            segs.append((np.array(up[0]), np.array(up[1])))
    return segs


def raw_arch(T, y, tol=1e-4):
    """Chain the raw plane-section segments at y into the EXACT ordered OPEN arch polyline.
    The bore STL is an open horseshoe (free invert rim), so the chained loop is an open path from
    one invert corner, up over the crown, to the other invert corner.  Oriented to START at the
    RIGHT (larger-x) invert corner and proceed CCW (up the right wall, over the crown, down the
    left wall to the left corner) so node 0 is an anatomically stable landmark at EVERY y."""
    import collections
    segs = plane_segments(T, y)
    def key(p): return (round(p[0]/tol), round(p[1]/tol))
    pts = {}; order = []
    def gid(p):
        k = key(p)
        if k not in pts:
            pts[k] = len(order); order.append(np.array(p))
        return pts[k]
    adj = collections.defaultdict(set)
    for a, b in segs:
        ia, ib = gid(a), gid(b)
        if ia != ib:
            adj[ia].add(ib); adj[ib].add(ia)
    deg1 = [i for i in adj if len(adj[i]) == 1]              # the two free invert corners
    start = deg1[0] if deg1 else next(iter(adj))
    if len(deg1) == 2 and order[deg1[1]][0] > order[deg1[0]][0]:
        start = deg1[1]                                      # start at the RIGHT corner (larger x)
    path = [start]; prev = -1; cur = start; seen = {start}
    while True:
        nxts = [n for n in adj[cur] if n != prev and n not in seen]
        if not nxts:
            break
        nxt = nxts[0]; path.append(nxt); seen.add(nxt); prev, cur = cur, nxt
    return np.array([order[i] for i in path])


def ring_centroid(P):
    """Polygon (shoelace) centroid of a closed loop P (P[-1] may or may not repeat P[0])."""
    Q = P if np.allclose(P[0], P[-1]) else np.vstack([P, P[:1]])
    x = Q[:, 0]; z = Q[:, 1]
    cr = x[:-1]*z[1:] - x[1:]*z[:-1]; A = cr.sum()/2.0
    cx = ((x[:-1]+x[1:])*cr).sum()/(6*A); cz = ((z[:-1]+z[1:])*cr).sum()/(6*A)
    return np.array([cx, cz])


def inner_ring(T, y):
    """Inner ring = N_RING nodes ON the raw closed bore polygon at FIXED normalized arc-length
    fractions (twist-free, exact on the STL).  Layout (node 0 = right invert corner, going CCW):
      - (N_RING - N_FLOOR) ARCH nodes by arc length along the raw arch (corner -> crown -> corner),
      - N_FLOOR interior nodes evenly along the straight INVERT CHORD (left corner -> right corner).
    Returns (ring (N_RING,2), frac (N_RING,) normalized arc-length of each node on the closed loop,
    is_floor (N_RING,) bool)."""
    na = N_RING - N_FLOOR
    arch = raw_arch(T, y)
    s = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(arch, axis=0), axis=1))])
    L = s[-1]
    fa = np.linspace(0.0, L, na)                             # arc length, includes both corners
    archN = np.column_stack([np.interp(fa, s, arch[:, 0]), np.interp(fa, s, arch[:, 1])])
    Lc, Rc = arch[-1], arch[0]                               # left / right invert corners
    tf = np.linspace(0.0, 1.0, N_FLOOR + 2)[1:-1]            # interior chord fractions
    floorN = Lc[None, :] + tf[:, None]*(Rc - Lc)[None, :]
    ring = np.vstack([archN, floorN])
    is_floor = np.array([False]*na + [True]*N_FLOOR)
    closed = np.vstack([ring, ring[:1]])
    cs = np.concatenate([[0.0], np.cumsum(np.linalg.norm(np.diff(closed, axis=0), axis=1))])
    frac = cs[:-1] / cs[-1]
    return ring, frac, is_floor


# O-grid OUTER-ring -> core-box edge assignment.  Each inner-ring node i is mapped to ONE of the 4
# core-box edges via a FIXED contiguous index split (computed once on the reference section in
# init_edge_split(); reused at every y).  Because the inner ring is twist-free (node i = the same
# anatomical location at all y), a fixed index split gives a CONSTANT per-edge node count across y
# (required for the structured sweep) AND a geometrically natural mapping (right-wall nodes -> right
# edge, crown -> top, left-wall -> left, invert chord -> bottom).  Within each edge the nodes are
# spread by the inner ring's own arc-length spacing on that segment, so inner & outer rings are
# co-monotonic in arc length and the radial O-grid never folds.
EDGE_SPLIT = None              # (i_top, i_left, i_bot) index boundaries; set by init_edge_split()


def init_edge_split(ring, frac):
    """Lock the inner-ring index boundaries that separate the right/top/left/bottom core-box edges,
    from the REFERENCE section, by which rectangle edge each node's radial direction points toward.
    Returns (i_top, i_left, i_bot): right edge = [0:i_top), top = [i_top:i_left),
    left = [i_left:i_bot), bottom(invert chord) = [i_bot:N_RING)."""
    global EDGE_SPLIT
    na = N_RING - N_FLOOR
    C = ring_centroid(ring)
    # the bottom edge is exactly the invert-chord (floor) nodes -> [na:N_RING)
    i_bot = na
    # split the arch by radial azimuth: nodes whose ray hits the right/top/left rectangle edge.
    # rectangle half-extents about the centroid:
    rel = ring[:na] - C
    # which edge does the ray (rel direction) hit on a W x (HT+HB) rectangle centred at C?
    # use the box actually centred at C (Cx +-W, Cz-HB..Cz+HT); param by ray-edge hit.
    ex = np.where(rel[:, 0] >= 0, W, -W); ez = np.where(rel[:, 1] >= 0, HT, -HB)
    tx = np.where(np.abs(rel[:, 0]) > 1e-9, ex/np.where(rel[:, 0] != 0, rel[:, 0], 1e-9), 1e18)
    tz = np.where(np.abs(rel[:, 1]) > 1e-9, ez/np.where(rel[:, 1] != 0, rel[:, 1], 1e-9), 1e18)
    hit_vertical = tx < tz                       # True -> hits a vertical edge (right/left)
    is_right = hit_vertical & (rel[:, 0] >= 0)
    is_left  = hit_vertical & (rel[:, 0] < 0)
    is_top   = (~hit_vertical) & (rel[:, 1] >= 0)
    # the ring goes right-wall(top? no) ... contiguous: right edge first, then top, then left.
    # find the first index that is 'top' and the first that is 'left' (contiguous regions).
    i_top = int(np.argmax(is_top)) if is_top.any() else na//3
    after = np.arange(na) >= i_top
    i_left = int(np.argmax(is_left & after)) if (is_left & after).any() else 2*na//3
    EDGE_SPLIT = (i_top, i_left, i_bot)
    return EDGE_SPLIT


def core_perim(C, frac):
    """O-grid OUTER ring = the core-box RECTANGLE.  Each inner-ring node i is placed on its assigned
    edge (per the locked EDGE_SPLIT) at the node's own normalized arc position WITHIN that edge's
    inner-ring segment (co-monotonic with the inner ring => no fold).  Rectangle CCW from bottom-
    RIGHT corner.  Returns (perim (N,2), edge index per node: 0=right,1=top,2=left,3=bottom)."""
    Cx, Cz = C
    BR = np.array([Cx+W, Cz-HB]); TR = np.array([Cx+W, Cz+HT])
    TL = np.array([Cx-W, Cz+HT]); BL = np.array([Cx-W, Cz-HB])
    i_top, i_left, i_bot = EDGE_SPLIT
    bounds = [(0, i_top, BR, TR), (i_top, i_left, TR, TL),
              (i_left, i_bot, TL, BL), (i_bot, N_RING, BL, BR)]
    out = np.zeros((N_RING, 2)); eidx = np.zeros(N_RING, int)
    # arc length of each inner-ring node measured along the closed loop (already = frac*L)
    for e, (lo, hi, A, Bp) in enumerate(bounds):
        f = frac[lo:hi]
        f0, f1 = f[0], (frac[hi] if hi < N_RING else 1.0)
        # normalized position of each node within this edge's arc span
        denom = (f1 - f0) if (f1 - f0) > 1e-12 else 1.0
        loc = (f - f0) / denom
        loc = np.clip(loc, 0.0, 1.0)
        out[lo:hi] = A[None, :] + loc[:, None]*(Bp - A)[None, :]
        eidx[lo:hi] = e
    return out, eidx


# ----- geology surfaces S02..S05 over the 40x40 box -------------------------------
def sample_surfaces():
    """S02..S05 sampled over the domain as 2-D grids; ordered S02 > S03 > S04 > S05 (no inversion).
    Linear interpolation with nearest-neighbour fallback outside the convex hull."""
    S = {k: stl_vertices(os.path.join(SMALL, k + '.stl')) for k in ['S02', 'S03', 'S04', 'S05']}
    lin = {k: LinearNDInterpolator(V[:, :2], V[:, 2]) for k, V in S.items()}
    nea = {k: NearestNDInterpolator(V[:, :2], V[:, 2]) for k, V in S.items()}
    xs = np.linspace(BX0, BX1, NG); ys = np.linspace(Y0, Y1, NG)
    Xg, Yg = np.meshgrid(xs, ys, indexing='ij')
    def s(k):
        z = lin[k](Xg, Yg); m = np.isnan(z)
        if m.any():
            z[m] = nea[k](Xg[m], Yg[m])
        return z
    Z = {k: s(k) for k in S}
    s2 = Z['S02']
    s3 = np.minimum(Z['S03'], s2 - EPS)
    s4 = np.minimum(Z['S04'], s3 - EPS)
    s5 = np.minimum(Z['S05'], s4 - EPS)
    return xs, ys, [s2, s3, s4, s5]


# ====================================================================================
#  TUNNEL AXIS (per-y bore-section centroid, straight from the raw STL)
# ====================================================================================
def tunnel_axis_from_stl(step=0.5, wall_path=WALL):
    """Per-y bore axis = the polygon centroid of the raw closed bore section at y.  axis_fn(y)
    returns (xc,zc); the diagnostic scan reports the (gentle) axis trend.  centerline_model.csv is
    NOT used.  ring_fn(y) returns the inner ring + its arc fractions + floor mask at y.

    wall_path selects which STL surface the ring is sampled on: wallzone_outter.stl (default) gives
    the ROCK excavation surface (rock O-grid inner ring); wall_inner.stl gives the CLEARANCE surface
    (--clearance variant, the train-clearance boundary the bore fill is sized to)."""
    T = stl_triangles(wall_path)
    ys = np.arange(Y0, Y1 + 1e-9, step)
    yk, xc, zc = [], [], []
    for y in ys:
        try:
            ring, _, _ = inner_ring(T, float(y))
        except Exception:
            continue
        c = ring_centroid(ring)
        yk.append(y); xc.append(c[0]); zc.append(c[1])
    yk = np.array(yk); xc = np.array(xc); zc = np.array(zc)
    axc = np.polyfit(yk, xc, 4); azc = np.polyfit(yk, zc, 4)

    def axis_fn(y):
        ring, _, _ = inner_ring(T, float(y))
        c = ring_centroid(ring); return float(c[0]), float(c[1])

    def ring_fn(y):
        return inner_ring(T, float(y))

    def section_raw(y):
        """raw arch polyline (open) at y, for the diagnostic / proof overlays."""
        return raw_arch(T, float(y))

    diag = {'yk': yk, 'xc': xc, 'zc': zc,
            'resx': xc - np.polyval(axc, yk), 'resz': zc - np.polyval(azc, yk),
            'section_raw': section_raw, 'segs': lambda y: plane_segments(T, float(y))}
    return axc, azc, axis_fn, ring_fn, diag


# ====================================================================================
#  PICTURE-FRAME BACKGROUND  (4 transfinite Coons patches around the core box)
# ====================================================================================
def coons(B, Tp, Lf, Rt):
    """Transfinite (bilinearly-blended Coons) structured patch from 4 boundary polylines:
       B,Tp : (ni,2) bottom / top edges (along u); Lf,Rt : (nj,2) left / right edges (along v).
    Corners must coincide (B[0]==Lf[0], B[-1]==Rt[0], Tp[0]==Lf[-1], Tp[-1]==Rt[-1]).
    Returns P (ni,nj,2).  Used to fill each picture-frame side from the (fine) core-box edge to the
    (coarse) domain edge, sharing the diagonal seam edges with the neighbouring patches."""
    ni = len(B); nj = len(Lf)
    u = np.linspace(0, 1, ni); v = np.linspace(0, 1, nj)
    U = u[:, None]; V = v[None, :]
    P = np.zeros((ni, nj, 2))
    for d in range(2):
        P[:, :, d] = ((1-V)*B[:, d][:, None] + V*Tp[:, d][:, None]
                      + (1-U)*Lf[:, d][None, :] + U*Rt[:, d][None, :]
                      - ((1-U)*(1-V)*B[0, d] + U*(1-V)*B[-1, d]
                         + (1-U)*V*Tp[0, d] + U*V*Tp[-1, d]))
    return P


def build_section(Cx, Cz, y, ring, frac, solid=False):
    """Build ONE cross-section: the O-grid tube (inner ring on the raw STL -> core box) plus the
    4 picture-frame background patches (core box -> 40x40 domain).  Returns a dict of structured
    (ni,nj,2) grids in global (x,z); weld_section() fuses them gp-to-gp.

    The core-box perimeter is taken at the inner ring's arc-length fractions (`core_perim`), so the
    O-grid never folds.  The same perimeter node positions form the inner edges of the 4 patches,
    so tube and background weld with no duplicate nodes.

    If solid=True, ALSO emit the butterfly bore-FILL patches ('core','p_right','p_top','p_left',
    'p_bot') whose OUTER edges coincide exactly with the inner-ring node positions -> they weld
    gp-to-gp to the tube's b=0 column (shared node IDs), filling the bore interior with hexes."""
    C = np.array([Cx, Cz])
    perim, eidx = core_perim(C, frac)

    out = {}
    # ---- O-grid TUBE: inner ring (on STL) -> core-box perimeter --------------------
    tube = np.empty((N_RING + 1, NRT + 1, 2))
    for r in range(NRT + 1):
        rr = (1 - FT[r])*ring + FT[r]*perim
        tube[:-1, r] = rr; tube[-1, r] = rr[0]
    out['tube'] = tube

    # ---- picture-frame: 4 transfinite patches around the core box -----------------
    BR = np.array([Cx+W, Cz-HB]); TR = np.array([Cx+W, Cz+HT])
    TL = np.array([Cx-W, Cz+HT]); BL = np.array([Cx-W, Cz-HB])
    dBR = np.array([BX1, BZ0]); dTR = np.array([BX1, BZ1])
    dTL = np.array([BX0, BZ1]); dBL = np.array([BX0, BZ0])

    # core-box edges taken DIRECTLY from the perimeter node slices (which already start exactly at
    # each box corner -- core_perim places loc=0 ON the corner) and closed by the NEXT edge's first
    # node (= the far corner).  This shares every box-edge node (corners included) with the O-grid
    # tube's outer ring, so tube and frame weld gp-to-gp with NO duplicate / collapsed corner cell.
    i_top, i_left, i_bot = EDGE_SPLIT
    e_right = np.vstack([perim[0:i_top],      perim[i_top:i_top+1]])    # BR .. TR
    e_top   = np.vstack([perim[i_top:i_left], perim[i_left:i_left+1]])  # TR .. TL
    e_left  = np.vstack([perim[i_left:i_bot], perim[i_bot:i_bot+1]])    # TL .. BL
    e_bot   = np.vstack([perim[i_bot:N_RING], perim[0:1]])             # BL .. BR (wrap)

    def seam(boxc, domc):                # diagonal seam box-corner -> domain-corner, graded
        return boxc[None, :] + FS[:, None]*(domc - boxc)[None, :]
    sBR = seam(BR, dBR); sTR = seam(TR, dTR); sTL = seam(TL, dTL); sBL = seam(BL, dBL)

    def dom_edge(d0, d1, n):             # domain edge, n nodes (matches the box-edge node count)
        return np.column_stack([np.linspace(d0[0], d1[0], n), np.linspace(d0[1], d1[1], n)])

    # each patch: inner edge = box edge (along u), outer edge = domain edge, sides = the 2 seams.
    out['fr_right'] = coons(e_right, dom_edge(dBR, dTR, len(e_right)), sBR, sTR)
    out['fr_top']   = coons(e_top,   dom_edge(dTR, dTL, len(e_top)),   sTR, sTL)
    out['fr_left']  = coons(e_left,  dom_edge(dTL, dBL, len(e_left)),  sTL, sBL)
    out['fr_bot']   = coons(e_bot,   dom_edge(dBL, dBR, len(e_bot)),   sBL, sBR)

    if solid:
        out.update(build_fill(C, ring, frac))   # butterfly fill of the bore interior (group 'excav')
    return out


# ====================================================================================
#  SOLID-BORE FILL  (2026-06-24)  -- butterfly core that FILLS the bore interior
# ====================================================================================
# For a convergence-confinement initial balance the excavation region must be NULLABLE hex
# zones (so `zone relax excavate` releases the in-situ stress gradually).  The bore interior
# (the region INSIDE the 116-node O-grid inner ring) is therefore FILLED with a structured
# all-hex butterfly: a small central core block + 4 transition (Coons) "petals" that bridge
# the 4 ring arcs (right/top/left/bottom, the SAME EDGE_SPLIT used for the core box) inward to
# the 4 edges of the central core block.  This is the picture-frame mirrored INWARD.
#
# The fill nodes on the bore boundary ARE the inner-ring node positions ring[i] (placed at the
# IDENTICAL rounded (x,z) the tube's b=0 column uses), so weld_section() fuses them to the rock
# O-grid inner ring gp-to-gp: shared node IDs, no duplicate/coincident separate nodes -> a true
# weld.  A butterfly core (not a radial fan to a single center) avoids the collapsed-center
# zero-volume degeneracy.  All petals + core are structured (ni,nj,2) grids -> all-hex C3D8.
#
# CORE SIZE: the central block half-extents are a fraction of the RING's OWN half-extents about
# its centroid C (NOT the rock core-box W/HT/HB, which is ~2x larger than the bore and would push
# the core block almost onto the ring, folding the petals).  Sizing off the ring keeps a generous,
# uniform petal band all the way round (incl. the sharp invert corners) so no petal cell inverts.
CORE_FRAC = 0.55                   # core block half-extent as a fraction of the ring half-extent
NSEAM_FILL = 6                     # radial (transverse) cells along each petal seam (core -> ring)

# FILL junctions: a 4-way split of the closed 116-node ring into arcs (right,top,left,bottom).
# These weld to the core-block corners.  Unlike the rock EDGE_SPLIT they are chosen so OPPOSITE
# petals carry EQUAL node counts (right==left, top==bottom) -- the central core block is then a
# single valid structured rectangle (a structured grid REQUIRES opposite edges to share a node
# count).  Every ring node is shared with the rock either way, so the choice of junctions does not
# affect the weld; it only balances the petals.  Set once on the reference section.
FILL_JUNC = None                   # (j0,j1,j2,j3) ring indices = BR, TR, TL, BL corners


def init_fill_junctions(ring):
    """Pick 4 ring-index junctions (j0,j1,j2,j3) so the 4 petals have EQUAL opposite node counts.
    Start from the rock EDGE_SPLIT (geometrically right/top/left/bottom corners), then nudge the
    top/bottom boundary so the top and bottom arcs carry the same number of edges (right==left is
    already balanced by construction).  Returns FILL_JUNC."""
    global FILL_JUNC
    it, il, ib = EDGE_SPLIT
    j0, j1, j2, j3 = 0, it, il, ib
    E = N_RING                                   # total edges around the closed loop
    # edges per arc: e_r=j1-j0, e_t=j2-j1, e_l=j3-j2, e_b=E-j3
    e_r = j1 - j0; e_l = j3 - j2
    # keep right==left: set both to their average (move j3 so e_l == e_r), then top==bottom follows
    a = (e_r + e_l) // 2                         # right & left edge count
    b = (E - 2 * a) // 2                         # top & bottom edge count (a+a+b+b = E)
    # rebuild contiguous junctions from j0=0 with edge counts (a, b, a, b)
    rem = E - 2 * (a + b)                        # any rounding remainder -> dump into bottom arc
    j0 = 0; j1 = j0 + a; j2 = j1 + b; j3 = j2 + a
    # bottom arc = E - j3 edges = b + rem  (closes the loop); a,b chosen so this stays positive
    FILL_JUNC = (j0, j1, j2, j3)
    return FILL_JUNC


def build_fill(C, ring, frac):
    """Butterfly fill of the bore interior bounded by the 116-node inner `ring` (closed loop, the
    SAME node positions as the O-grid tube b=0 column).  Returns a dict of structured (ni,nj,2)
    grids whose OUTER edges coincide exactly with ring[j] so weld_section() welds them to the rock.

    Layout (uses the balanced FILL_JUNC right/top/left/bottom arcs):
      * a central CORE block -- a rectangle centred at C, well inside the ring;
      * 4 PETAL patches, each a Coons patch from one ring arc (outer) to one core-block edge
        (inner), the petals sharing diagonal SEAM edges from each ring arc-junction node to the
        matching core-block corner.  Petals + core tile the whole interior with NO gap/overlap and
        NO collapsed center (the butterfly avoids the radial-fan zero-volume degeneracy)."""
    Cx, Cz = C
    j0, j1, j2, j3 = FILL_JUNC
    # core-block u/v cell counts = the (balanced) arc node counts minus 1
    ncu = (j1 - j0)            # right/left arcs have this many edges -> core block v-edges
    ncv = (j2 - j1)            # top/bottom arcs -> core block u-edges
    # core block half-extents from the RING's OWN extent about C (per-quadrant, so the core stays
    # centred inside an asymmetric horseshoe and every petal keeps a comfortable band).
    rx_p = ring[:, 0].max() - Cx; rx_m = Cx - ring[:, 0].min()
    rz_p = ring[:, 1].max() - Cz; rz_m = Cz - ring[:, 1].min()
    cwp = CORE_FRAC * rx_p; cwm = CORE_FRAC * rx_m
    czp = CORE_FRAC * rz_p; czm = CORE_FRAC * rz_m
    # central core-block corners (CCW from bottom-right), centred at the section centroid C:
    bBR = np.array([Cx + cwp, Cz - czm]); bTR = np.array([Cx + cwp, Cz + czp])
    bTL = np.array([Cx - cwm, Cz + czp]); bBL = np.array([Cx - cwm, Cz - czm])

    def edge(A, B, n):
        return np.column_stack([np.linspace(A[0], B[0], n), np.linspace(A[1], B[1], n)])

    out = {}
    # ---- central CORE block: structured rectangle (Coons of its 4 straight edges) -------------
    # u runs bottom->top edges length (ncv+1); v runs left->right edges length (ncu+1)
    eb = edge(bBL, bBR, ncv + 1); et = edge(bTL, bTR, ncv + 1)
    elf = edge(bBL, bTL, ncu + 1); ert = edge(bBR, bTR, ncu + 1)
    out['core'] = coons(eb, et, elf, ert)

    # ---- ring arcs (outer edge of each petal), oriented to match the core edge direction --------
    a_right = np.vstack([ring[j0:j1], ring[j1:j1 + 1]])      # BR .. TR   (ncu edges)
    a_top   = np.vstack([ring[j1:j2], ring[j2:j2 + 1]])      # TR .. TL   (ncv edges)
    a_left  = np.vstack([ring[j2:j3], ring[j3:j3 + 1]])      # TL .. BL   (ncu edges)
    a_bot   = np.vstack([ring[j3:N_RING], ring[0:1]])        # BL .. BR (wrap, ncb edges)

    # diagonal seams: core-block corner -> ring arc-junction node (graded linearly, NSEAM_FILL cells)
    def seam(corner, ringnode):
        t = np.linspace(0.0, 1.0, NSEAM_FILL + 1)
        return corner[None, :] + t[:, None] * (ringnode - corner)[None, :]

    # petal: u-edges = (core-block edge, ring arc) [equal node counts]; v-edges = the 2 seams.
    # right petal bridges core RIGHT edge (bBR->bTR, ncu+1 nodes) to ring right arc (ncu+1 nodes).
    out['p_right'] = coons(edge(bBR, bTR, len(a_right)), a_right,
                           seam(bBR, ring[j0]), seam(bTR, ring[j1]))
    out['p_top']   = coons(edge(bTR, bTL, len(a_top)),   a_top,
                           seam(bTR, ring[j1]), seam(bTL, ring[j2]))
    out['p_left']  = coons(edge(bTL, bBL, len(a_left)),  a_left,
                           seam(bTL, ring[j2]), seam(bBL, ring[j3]))
    out['p_bot']   = coons(edge(bBL, bBR, len(a_bot)),   a_bot,
                           seam(bBL, ring[j3]), seam(bBR, ring[j0]))
    return out


def weld_section(P):
    """Fuse all patches into one node list + quad list, gp-to-gp by rounded (x,z).
    Returns (src, quads, quad_patch): src[i]=(owning-patch,a,b) of section node i; quads = welded
    quads (node-index 4-tuples); quad_patch[k] = the patch name that GENERATED quad k (used to
    classify rock vs the solid-bore fill, since a fill quad may reference ring nodes already owned
    by the 'tube' patch)."""
    idx = {}; src = []; quads = []; quad_patch = []
    def add(name, a, b, xz):
        k = (round(xz[0]*1e4), round(xz[1]*1e4))
        if k not in idx:
            idx[k] = len(src); src.append((name, a, b))
        return idx[k]
    for name in P:
        G = P[name]; ni, nj = G.shape[:2]
        ID = [[add(name, a, b, G[a, b]) for b in range(nj)] for a in range(ni)]
        for a in range(ni - 1):
            for b in range(nj - 1):
                quads.append((ID[a][b], ID[a+1][b], ID[a+1][b+1], ID[a][b+1]))
                quad_patch.append(name)
    return src, quads, quad_patch


# ====================================================================================
#  RENDER:  couple_bore_vs_stl.png  (O-grid inner ring overlaid on the RAW STL section)
# ====================================================================================
def render_bore_vs_stl(inner_xz, Yv, adiag):
    """REQUIRED PROOF couple_bore_vs_stl.png: at y=865,885,905 overlay the O-grid inner ring (a
    connected polyline through the inner nodes) on the RAW wallzone_outter.stl cross-section.
    Top row = the full horseshoe; bottom row = a zoom on the invert + the two bottom corners.
    The ring must visually coincide with the STL with no coarseness / gap."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

    yts = (865.0, 885.0, 905.0)
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    for col, yt in enumerate(yts):
        j = int(np.argmin(np.abs(Yv - yt)))
        ring = np.vstack([inner_xz[:, j, :], inner_xz[:1, j, :]])     # closed inner-ring polyline
        segs = adiag['segs'](float(Yv[j]))                            # raw STL segments
        lc = [np.array([a, b]) for a, b in segs]

        for row, (title, zoom) in enumerate([('full horseshoe', None),
                                             ('invert + bottom corners', True)]):
            ax = axes[row, col]
            ax.add_collection(LineCollection(lc, colors='0.55', linewidths=4.0))
            ax.plot([], [], '-', color='0.55', lw=4, label='raw wallzone_outter.stl')
            ax.plot(ring[:, 0], ring[:, 1], '-', color='C3', lw=1.3, label='O-grid inner ring')
            ax.plot(inner_xz[:, j, 0], inner_xz[:, j, 1], '.', color='C0', ms=4)
            ax.set_aspect('equal'); ax.grid(alpha=0.3)
            ax.set_xlabel('x'); ax.set_ylabel('z')
            allp = np.vstack([np.vstack(lc), ring])
            if zoom:
                # zoom on the invert band: bottom ~1.8 m and full width of the section
                zlo = allp[:, 1].min(); ax.set_ylim(zlo - 0.3, zlo + 2.2)
                ax.set_xlim(allp[:, 0].min() - 0.4, allp[:, 0].max() + 0.4)
                ax.set_title(f'y = {Yv[j]:.1f}  --  {title}')
            else:
                ax.set_xlim(allp[:, 0].min() - 0.6, allp[:, 0].max() + 0.6)
                ax.set_ylim(allp[:, 1].min() - 0.6, allp[:, 1].max() + 0.6)
                ax.set_title(f'y = {Yv[j]:.1f}  --  {title}')
            if col == 0 and row == 0:
                ax.legend(loc='lower center', fontsize=9)
    fig.suptitle('couple_hex O-grid inner ring (excavation surface) vs RAW wallzone_outter.stl '
                 '-- exact, no gap, no coarseness', fontsize=13)
    fig.tight_layout()
    f = os.path.join(HERE, 'couple_bore_vs_stl.png')
    fig.savefig(f, dpi=120); plt.close(fig)
    print(f"wrote {f}")
    return f


def render_notwist(inner_xz, axis_xz, Yv):
    """Longitudinal twist proof couple_hex_notwist_long.png: crown + two spring inner-ring nodes
    vs y -- twist-free => smooth, non-oscillating curves (azimuth especially)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    crown = int(np.argmax(inner_xz[:, :, 1].mean(1)))
    iL = int(np.argmin(inner_xz[:, :, 0].mean(1)))
    iR = int(np.argmax(inner_xz[:, :, 0].mean(1)))
    rel = inner_xz - axis_xz[None, :, :]
    fig, axs = plt.subplots(3, 1, figsize=(11, 10), sharex=True)
    names = [('crown node', crown, 'C2'), ('spring node L', iL, 'C0'), ('spring node R', iR, 'C3')]
    for nm, ni, cc in names:
        axs[0].plot(Yv, inner_xz[ni, :, 0], '-', color=cc, label=nm)
    axs[0].plot(Yv, axis_xz[:, 0], '--', color='0.5', label='axis xc(y)')
    axs[0].set_ylabel('x'); axs[0].legend(fontsize=8, ncol=2); axs[0].grid(alpha=0.3)
    axs[0].set_title('Inner-ring crown + two spring nodes vs y (smooth = NO twist)')
    for nm, ni, cc in names:
        axs[1].plot(Yv, inner_xz[ni, :, 1], '-', color=cc, label=nm)
    axs[1].plot(Yv, axis_xz[:, 1], '--', color='0.5', label='axis zc(y)')
    axs[1].set_ylabel('z'); axs[1].legend(fontsize=8, ncol=2); axs[1].grid(alpha=0.3)
    for nm, ni, cc in names:
        a = np.degrees(np.unwrap(np.arctan2(rel[ni, :, 1], rel[ni, :, 0])))
        axs[2].plot(Yv, a, '-', color=cc, label=nm)
    axs[2].set_ylabel('node azimuth [deg]'); axs[2].set_xlabel('y')
    axs[2].legend(fontsize=8, ncol=3); axs[2].grid(alpha=0.3)
    fig.tight_layout()
    f = os.path.join(HERE, 'couple_hex_notwist_long.png')
    fig.savefig(f, dpi=110); plt.close(fig)
    print(f"wrote {f}")


def render_cells(coords, H, ta):
    """Render the ACTUAL O-grid hex cell outlines at the y=885 cut, zoomed on the tunnel."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    XR, ZR = (1290.0, 1306.0), (1741.0, 1754.0)
    yt = 885.0
    P = coords[H]
    cy = P[:, :, 1].mean(1); cx = P[:, :, 0].mean(1); cz = P[:, :, 2].mean(1)
    m = (np.abs(cy - yt) < 0.5) & (cx >= XR[0]) & (cx <= XR[1]) & (cz >= ZR[0]) & (cz <= ZR[1])
    polys = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in P[m]]
    fig, ax = plt.subplots(figsize=(9, 7.5))
    ax.add_collection(PolyCollection(polys, facecolors='none', edgecolors='#1f4fbf', linewidths=0.5))
    ax.set_xlim(*XR); ax.set_ylim(*ZR); ax.set_aspect('equal')
    ax.set_xlabel('x'); ax.set_ylabel('z'); ax.grid(alpha=0.25)
    ax.set_title(f'couple_hex O-grid cells @ y={yt:.0f}  tube aspect p99={np.percentile(ta,99):.2f} '
                 f'max={ta.max():.2f}')
    fig.tight_layout()
    fc = os.path.join(HERE, 'couple_hex_cells.png')
    fig.savefig(fc, dpi=140); plt.close(fig)
    print(f"wrote {fc}")


def render_outer_density(coords, H, sj, asp):
    """REQUIRED couple_outer_density.png: the FULL 40x40 cross-section at y=885 drawn as the ACTUAL
    hex cell outlines, so the doubled OUTER (picture-frame) radial density is visible all the way to
    the domain edge.  Left = full domain (every cell out to x[1277,1317] z[1728,1768]); right = a
    zoom on the tunnel + core box so the O-grid tube is still legible.  Compare-ready against the
    previous (NSEAM=8) mesh."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    yt = 885.0
    P = coords[H]
    cy = P[:, :, 1].mean(1)
    m = np.abs(cy - yt) < 0.5
    polys = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in P[m]]
    fig, (axF, axZ) = plt.subplots(1, 2, figsize=(17, 8.2))
    for ax, (x0, x1), (z0, z1), title in [
            (axF, (BX0, BX1), (BZ0, BZ1), 'FULL 40x40 section -- outer picture-frame radial density'),
            (axZ, (1287.0, 1308.0), (1739.0, 1758.0), 'zoom: O-grid tube + core box')]:
        ax.add_collection(PolyCollection(polys, facecolors='none',
                                         edgecolors='#1f4fbf', linewidths=0.35))
        ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_aspect('equal')
        ax.set_xlabel('x'); ax.set_ylabel('z'); ax.grid(alpha=0.25)
        ax.set_title(title, fontsize=11)
    fig.suptitle(f'couple_hex @ y={yt:.0f}  --  outer picture-frame radial cells NSEAM={NSEAM} '
                 f'(graded, growth {GSEAM:.3f})   aspect p99={np.percentile(asp,99):.2f} '
                 f'max={asp.max():.2f}   min scaled-J={sj.min():.3f}', fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fc = os.path.join(HERE, 'couple_outer_density.png')
    fig.savefig(fc, dpi=140); plt.close(fig)
    print(f"wrote {fc}")
    return fc


def render_cubic_cells(coords, H, asp):
    """REQUIRED couple_cubic_cells.png (the cubic-rebalance proof): the FULL y=885 cross-section drawn
    as the ACTUAL hex cell outlines, each cell SHADED by its 3-D aspect ratio (blue~1 cubic -> red
    elongated) so the more-cubic rock cells are visible, PLUS an aspect-ratio histogram of every hex
    in the mesh with the median / p99 / max marked.  Top-left = full 40x40 domain; top-right = zoom on
    the O-grid tube + core box (where the bore follows wallzone_outter.stl); bottom = the histogram."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    yt = 885.0
    P = coords[H]
    cy = P[:, :, 1].mean(1)
    msec = np.abs(cy - yt) < 0.5
    polys = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in P[msec]]
    asec = asp[msec]
    # color scale: 1 (cubic) .. 4 (elongated); clamp so the cubic majority is legible
    vmin, vmax = 1.0, 4.0
    fig = plt.figure(figsize=(17, 12))
    gs = fig.add_gridspec(2, 2, height_ratios=[2.1, 1.0])
    axF = fig.add_subplot(gs[0, 0]); axZ = fig.add_subplot(gs[0, 1])
    axH = fig.add_subplot(gs[1, :])
    for ax, (x0, x1), (z0, z1), title in [
            (axF, (BX0, BX1), (BZ0, BZ1), 'FULL 40x40 section -- cells shaded by aspect ratio'),
            (axZ, (1288.0, 1307.0), (1740.0, 1757.0),
             'zoom: O-grid tube on wallzone_outter.stl + core box')]:
        pc = PolyCollection(polys, array=asec, cmap='turbo', edgecolors='0.3', linewidths=0.25)
        pc.set_clim(vmin, vmax)
        ax.add_collection(pc)
        ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_aspect('equal')
        ax.set_xlabel('x'); ax.set_ylabel('z'); ax.grid(alpha=0.2)
        ax.set_title(title, fontsize=11)
    cb = fig.colorbar(pc, ax=[axF, axZ], fraction=0.025, pad=0.02)
    cb.set_label('cell aspect ratio  (1 = cubic)')
    # ---- aspect histogram (ALL hexes) ----------------------------------------------
    med, p99, mx = np.median(asp), np.percentile(asp, 99), asp.max()
    axH.hist(asp, bins=np.linspace(1.0, max(4.0, mx), 80), color='#1f77b4', alpha=0.85)
    for v, c, lab in [(med, 'C2', f'median {med:.2f}'), (p99, 'C1', f'p99 {p99:.2f}'),
                      (mx, 'C3', f'max {mx:.2f}')]:
        axH.axvline(v, color=c, lw=2, label=lab)
    axH.axvline(1.0, color='0.4', lw=1.2, ls='--', label='cubic = 1.0')
    axH.set_xlabel('hex aspect ratio (longest edge / shortest edge)')
    axH.set_ylabel('number of hexes'); axH.legend(); axH.grid(alpha=0.25)
    axH.set_title(f'aspect-ratio distribution of all {len(asp):,} hexes '
                  f'(N_RING={N_RING}, N_FLOOR={N_FLOOR}, NRT={NRT}, NSEAM={NSEAM}, DY={DY})')
    fig.suptitle('couple_hex CUBIC-REBALANCE @ y=885 -- rock cells driven toward cubic while the '
                 'bore stays exactly on wallzone_outter.stl', fontsize=13)
    fc = os.path.join(HERE, 'couple_cubic_cells.png')
    fig.savefig(fc, dpi=140); plt.close(fig)
    print(f"wrote {fc}")
    return fc


def render_solid_section(coords, H, excavmask, ringloop_xz):
    """REQUIRED couple_solid_section.png: the y=885 cross-section drawn as the ACTUAL hex cell
    outlines, ROCK (blue) vs EXCAV bore-fill (orange) coloured differently, with the welded bore
    inner ring (the rock/excav interface) overdrawn in red -- proving the bore is now SOLID and the
    interface welds (shared nodes, no gap).  Left = zoom on tunnel + core box; right = full 40x40."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection
    yt = 885.0
    P = coords[H]
    cy = P[:, :, 1].mean(1)
    msec = np.abs(cy - yt) < 0.5
    polys = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in P[msec]]
    isex = excavmask[msec]
    face = np.where(isex, '#ff8c1a', '#bcd2ff')      # excav=orange, rock=light blue
    fig, (axZ, axF) = plt.subplots(1, 2, figsize=(17, 8.2))
    for ax, (x0, x1), (z0, z1), title in [
            (axZ, (1290.0, 1306.0), (1741.0, 1755.0),
             'zoom: bore now SOLID -- rock (blue) | excav fill (orange) | welded interface (red)'),
            (axF, (BX0, BX1), (BZ0, BZ1), 'FULL 40x40 section -- rock vs excav')]:
        ax.add_collection(PolyCollection(polys, facecolors=face, edgecolors='0.25', linewidths=0.3))
        ax.plot(ringloop_xz[:, 0], ringloop_xz[:, 1], '-', color='red', lw=1.4,
                label='bore inner ring = rock/excav weld (shared nodes)')
        ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_aspect('equal')
        ax.set_xlabel('x'); ax.set_ylabel('z'); ax.grid(alpha=0.25)
        ax.set_title(title, fontsize=11)
    axZ.legend(loc='lower center', fontsize=9)
    nex = int(excavmask[msec].sum()); nrk = int((~excavmask[msec]).sum())
    fig.suptitle(f'couple_hex_solid @ y={yt:.0f}  --  bore interior FILLED with welded hex (excav).  '
                 f'section: {nrk} rock + {nex} excav cells', fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fc = os.path.join(HERE, 'couple_solid_section.png')
    fig.savefig(fc, dpi=140); plt.close(fig)
    print(f"wrote {fc}")
    return fc


def render_clearance_section(rock_coords, rock_hex_xz, clr_coords, clr_H, wallin_seg, wallout_seg):
    """REQUIRED couple_clearance_section.png: the y=885 cross-section showing the THREE concentric
    regions of the convergence-confinement initial-balance mesh:
      * the ROCK O-grid (blue cell outlines) whose INNER ring lies on wallzone_outter.stl,
      * the EMPTY RING between wallzone_outter.stl (rock inner ring) and wall_inner.stl -- the gap
        the PFC lining balls will occupy (filled in FLAC at run time, NOT here),
      * the CLEARANCE 'excav' fill (orange cell outlines) whose OUTER ring lies on wall_inner.stl.
    The two STL section polylines are overdrawn (grey = wallzone_outter, red = wall_inner) so the
    empty ball ring between them is unmistakable.  Left = zoom on the tunnel; right = full 40x40."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.collections import PolyCollection, LineCollection
    fig, (axZ, axF) = plt.subplots(1, 2, figsize=(17, 8.2))
    rock_polys = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in rock_hex_xz]
    clr_polys  = [(0.5*(h[:4] + h[4:]))[:, [0, 2]] for h in clr_coords[clr_H]]
    lc_out = [np.array([a, b]) for a, b in wallout_seg]
    lc_in  = [np.array([a, b]) for a, b in wallin_seg]
    for ax, (x0, x1), (z0, z1), title in [
            (axZ, (1290.0, 1305.0), (1741.0, 1754.0),
             'zoom: rock (blue) | EMPTY ring for balls | clearance excav fill (orange)'),
            (axF, (BX0, BX1), (BZ0, BZ1), 'FULL 40x40 section -- rock + empty ring + clearance')]:
        ax.add_collection(PolyCollection(rock_polys, facecolors='#bcd2ff', edgecolors='#3a63c0',
                                         linewidths=0.30))
        ax.add_collection(PolyCollection(clr_polys, facecolors='#ff8c1a', edgecolors='#7a3d00',
                                         linewidths=0.30))
        ax.add_collection(LineCollection(lc_out, colors='0.25', linewidths=1.6))
        ax.add_collection(LineCollection(lc_in,  colors='red',  linewidths=1.6))
        ax.plot([], [], '-', color='0.25', lw=1.6, label='wallzone_outter.stl (rock inner ring)')
        ax.plot([], [], '-', color='red',  lw=1.6, label='wall_inner.stl (clearance outer ring)')
        ax.plot([], [], 's', color='#bcd2ff', mec='#3a63c0', label='rock O-grid')
        ax.plot([], [], 's', color='#ff8c1a', mec='#7a3d00', label='clearance excav fill')
        ax.set_xlim(x0, x1); ax.set_ylim(z0, z1); ax.set_aspect('equal')
        ax.set_xlabel('x'); ax.set_ylabel('z'); ax.grid(alpha=0.25)
        ax.set_title(title, fontsize=11)
    axZ.legend(loc='lower center', fontsize=8, ncol=2)
    fig.suptitle('couple_hex_clearance @ y=885  --  rock O-grid + EMPTY ball ring (gap between '
                 'wallzone_outter.stl and wall_inner.stl) + clearance excav fill', fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fc = os.path.join(HERE, 'couple_clearance_section.png')
    fig.savefig(fc, dpi=140); plt.close(fig)
    print(f"wrote {fc}")
    return fc


def main_clearance():
    """couple_hex_clearance.inp = the rock O-grid (COPIED byte-identically from couple_hex.inp, the
    bore-hole version, groups layer2..layer6) PLUS a SEPARATE set of zones that butterfly-FILL the
    CLEARANCE region INSIDE wall_inner.stl (ELSET 'excav', slot 'type'), for a convergence-confinement
    initial balance.

    The clearance fill is built with the SAME arc-length / butterfly machinery as the --solid bore
    fill, but sized to wall_inner.stl (the inner clearance surface) instead of wallzone_outter.stl
    (the rock excavation surface).  The RING between wall_inner and wallzone_outter is left EMPTY (no
    zones -- that gap is for the PFC lining balls).  The clearance zones therefore do NOT share node
    IDs with the rock: clearance node IDs are OFFSET above the rock's max ID (a disjoint range), and
    the rock *NODE/*ELEMENT lines are written byte-for-byte from couple_hex.inp so the rock part is
    unchanged.  Does NOT launch FLAC3D."""
    out_inp = os.path.join(HERE, 'couple_hex_clearance.inp')

    # ---- 1. READ couple_hex.inp -> the rock part stays byte-identical ----------------
    # split into: header lines, rock *NODE lines, rock *ELEMENT blocks (verbatim); parse rock node
    # coords + max rock node ID so the clearance node IDs can be offset above it (disjoint range).
    head_lines, node_lines, elem_lines = [], [], []
    rock_xyz = []; rock_max_id = 0
    mode = None
    with open(INP) as f:
        for ln in f:
            s = ln.rstrip('\n')
            if s.startswith('*NODE'):
                mode = 'node'; head_lines.append(s); continue
            if s.startswith('*ELEMENT'):
                mode = 'elem'; elem_lines.append(s); continue
            if s.startswith('*'):
                mode = 'head'; head_lines.append(s); continue
            if mode == 'node':
                node_lines.append(s)
                p = s.split(',')
                nid = int(p[0]); rock_max_id = max(rock_max_id, nid)
                rock_xyz.append((float(p[1]), float(p[2]), float(p[3])))
            elif mode == 'elem':
                elem_lines.append(s)
            else:
                head_lines.append(s)
    rock_xyz = np.asarray(rock_xyz)
    print(f"couple_hex.inp READ byte-identically: {len(node_lines)} rock nodes (max id {rock_max_id}), "
          f"{sum(1 for s in elem_lines if not s.startswith('*'))} rock elements")

    # ---- 2. BUILD the clearance butterfly fill on wall_inner.stl ---------------------
    Ti = stl_triangles(WALLIN)
    Yv = np.linspace(Y0, Y1, int(round((Y1 - Y0)/DY)) + 1); NY = len(Yv)   # SAME y-planes as the rock
    r0, f0, _ = inner_ring(Ti, 885.0)
    init_edge_split(r0, f0)                    # lock the 4-way ring split (twist-free; reference y)
    init_fill_junctions(r0)                    # balanced butterfly junctions (right==left, top==bot)
    print(f"clearance ring @885: {len(r0)} nodes (arch {N_RING-N_FLOOR} + invert chord {N_FLOOR})  "
          f"width {np.ptp(r0[:,0]):.2f}  height {np.ptp(r0[:,1]):.2f}  on wall_inner.stl")
    print(f"FILL junctions (balanced petals) ring indices: {FILL_JUNC}  "
          f"core block {FILL_JUNC[1]-FILL_JUNC[0]}x{FILL_JUNC[2]-FILL_JUNC[1]} cells")

    rings = []; fracs = []
    for y in Yv:
        rg, fa, _ = inner_ring(Ti, float(y)); rings.append(rg); fracs.append(fa)
    CxCz = np.array([ring_centroid(rg) for rg in rings]); Cx, Cz = CxCz[:, 0], CxCz[:, 1]

    jm = NY // 2
    P0 = build_fill(np.array([Cx[jm], Cz[jm]]), rings[jm], fracs[jm])     # ONLY core + 4 petals
    src, quads, _ = weld_section(P0); NS = len(src)
    coords = np.empty((NS*NY, 3))
    for j in range(NY):
        P = build_fill(np.array([Cx[j], Cz[j]]), rings[j], fracs[j])
        for s, (n, a, b) in enumerate(src):
            xz = P[n][a, b]; coords[s*NY+j] = (xz[0], Yv[j], xz[1])

    hexes = []
    for (q0, q1, q2, q3) in quads:
        for j in range(NY-1):
            hexes.append((q0*NY+j, q1*NY+j, q2*NY+j, q3*NY+j,
                          q0*NY+j+1, q1*NY+j+1, q2*NY+j+1, q3*NY+j+1))
    H = np.array(hexes)
    d = np.linalg.det(np.einsum('cia,mib->mcab', DN, coords[H], optimize=True))
    allneg = d.max(1) < 0; H[allneg] = H[allneg][:, [4, 5, 6, 7, 0, 1, 2, 3]]
    Pc = coords[H]
    d = np.linalg.det(np.einsum('cia,mib->mcab', DN, Pc, optimize=True))
    nbad = int(((d.min(1) <= 0) & (d.max(1) > 0)).sum())
    ex_zero = int((np.abs(d).max(1) <= 1e-12).sum())
    el = np.linalg.norm(Pc[:, HE[:, 0]] - Pc[:, HE[:, 1]], axis=2)
    asp = el.max(1) / np.maximum(el.min(1), 1e-12)
    J = np.einsum('cia,mib->mcab', DN, Pc, optimize=True)
    sj = (np.linalg.det(J) / np.maximum(np.linalg.norm(J, axis=3).prod(2), 1e-12)).min(1)

    used = np.unique(H)
    remap = -np.ones(len(coords), np.int64); remap[used] = np.arange(len(used)); cc = coords[used]
    key = np.round(cc / 1e-4).astype(np.int64)
    ndup = len(cc) - len(np.unique(key, axis=0))           # duplicate coincident WITHIN clearance

    # ---- 3. WRITE couple_hex_clearance.inp -------------------------------------------
    # rock *NODE + *ELEMENT lines verbatim, then clearance *NODE (IDs OFFSET above rock_max_id) and
    # one *ELEMENT ELSET=excav block (1-based node refs into the OFFSET clearance range).
    OFF = rock_max_id                                       # clearance node id = OFF + (remap index + 1)
    with open(out_inp, 'w') as f:
        f.write('*Heading\n couple_hex_clearance (rock O-grid COPIED byte-identically from '
                'couple_hex.inp [layer2..6, inner ring on wallzone_outter.stl] PLUS a SEPARATE '
                'butterfly clearance fill INSIDE wall_inner.stl in ELSET excav (slot \'type\', '
                'nullable); the ring between wall_inner and wallzone_outter is left EMPTY for the PFC '
                'lining balls; clearance node IDs are offset above the rock max id -- disjoint, no '
                'shared node IDs with the rock)\n*NODE\n')
        # rock nodes verbatim
        f.write('\n'.join(node_lines)); f.write('\n')
        # clearance nodes (offset IDs)
        for i, p in enumerate(cc, 1):
            f.write(f'{OFF + i}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        # rock element blocks verbatim
        f.write('\n'.join(elem_lines)); f.write('\n')
        # clearance excav element block (continue element ids after the rock's last)
        rock_nelem = sum(1 for s in elem_lines if not s.startswith('*'))
        eid = rock_nelem + 1
        f.write('*ELEMENT, type=C3D8, ELSET=excav\n')
        for c in H:
            f.write(f'{eid}, ' + ', '.join(str(OFF + int(remap[n]) + 1) for n in c) + '\n'); eid += 1

    # ---- 4. VERIFY -------------------------------------------------------------------
    # 4a. rock<->clearance min distance (the ring gap; floor invert is shared geometry -> coincident)
    from scipy.spatial import cKDTree
    rtree = cKDTree(rock_xyz)
    dd, _ = rtree.query(cc, k=1)
    coincident = int((dd < 1e-4).sum())
    arch_gap = float(dd[dd >= 1e-4].min())
    coincident_z = cc[dd < 1e-4][:, 2]

    # 4b. clearance OUTER ring (arch) -> wall_inner.stl, and ring-gap radius vs wallzone_outter
    def pt_segs_dist(p, segs):
        best = 1e18
        for a, b in segs:
            ab = b - a; ap = p - a
            t = np.clip((ap @ ab)/max(ab @ ab, 1e-12), 0, 1)
            best = min(best, float(np.linalg.norm(ap - t*ab)))
        return best
    worst_n = 0.0; worst_ny = None
    To = stl_triangles(WALL)
    gap_lines = []
    for j in range(NY):
        segs = plane_segments(Ti, float(Yv[j]))
        if not segs:
            continue
        rg, fa, isf = inner_ring(Ti, float(Yv[j]))
        dn = np.array([pt_segs_dist(p, segs) for p in rg[~isf]])
        if dn.max() > worst_n:
            worst_n = dn.max(); worst_ny = float(Yv[j])
    for y in (865.0, 885.0, 905.0):
        ri, _, _ = inner_ring(Ti, float(y)); Cy = ring_centroid(ri)
        rmax = np.linalg.norm(ri - Cy, axis=1).max()
        ao = raw_arch(To, float(y)); romax = np.linalg.norm(ao - Cy, axis=1).max()
        gap_lines.append((y, rmax, romax, romax - rmax))

    # ---- 5. RENDER couple_clearance_section.png --------------------------------------
    rock_xyz_arr = rock_xyz
    # rock hexes at the y=885 cut, reconstructed from the rock *ELEMENT lines (for outline drawing)
    rid2pos = {}
    for s in node_lines:
        p = s.split(','); rid2pos[int(p[0])] = (float(p[1]), float(p[2]), float(p[3]))
    yt = 885.0
    rock_hex_xz = []
    for s in elem_lines:
        if s.startswith('*'):
            continue
        ids = [int(t) for t in s.split(',')[1:]]
        hx = np.array([rid2pos[i] for i in ids])
        if abs(hx[:, 1].mean() - yt) < 0.5:
            rock_hex_xz.append(hx)
    rock_hex_xz = np.array(rock_hex_xz)
    cy = coords[H][:, :, 1].mean(1); msec = np.abs(cy - yt) < 0.5
    wallin_seg = plane_segments(Ti, yt); wallout_seg = plane_segments(To, yt)
    render_clearance_section(rock_xyz_arr, rock_hex_xz, coords, H[msec], wallin_seg, wallout_seg)

    # ---- 6. REPORT -------------------------------------------------------------------
    exbb_lo = cc.min(0); exbb_hi = cc.max(0)
    rock_nelem = sum(1 for s in elem_lines if not s.startswith('*'))
    pct = lambda v, p: float(np.percentile(v, p))
    print(f"\n=== couple_hex_clearance INTEGRITY ===")
    print(f"rock zones (layer2..6, UNCHANGED) : {rock_nelem}")
    print(f"clearance 'excav' zones           : {len(H)}   (slot 'type', nullable)")
    print(f"total nodes : {len(node_lines)} rock + {len(cc)} clearance = {len(node_lines)+len(cc)}")
    print(f"total hexes : {rock_nelem} rock + {len(H)} clearance = {rock_nelem+len(H)}")
    print(f"clearance bbox : x[{exbb_lo[0]:.3f},{exbb_hi[0]:.3f}] y[{exbb_lo[1]:.3f},{exbb_hi[1]:.3f}] "
          f"z[{exbb_lo[2]:.3f},{exbb_hi[2]:.3f}]")
    print(f"clearance all-hex C3D8 : YES   ({'8 nodes/elem' })")
    print(f"clearance mixed-sign Jacobian : {nbad}   (MUST be 0)")
    print(f"clearance zero/neg-volume     : {ex_zero}   (MUST be 0)")
    print(f"clearance min scaled-Jacobian : {sj.min():.4f}")
    print(f"clearance aspect: median {np.median(asp):.2f}  p99 {pct(asp,99):.2f}  max {asp.max():.2f}")
    print(f"duplicate coincident nodes WITHIN clearance : {ndup}   (MUST be 0)")
    print(f"--- clearance OUTER ring on wall_inner.stl ---")
    print(f"max clearance OUTER-ring(arch) node -> wall_inner.stl : {worst_n:.5f} m at y={worst_ny:.1f}  "
          f"({'PASS (<0.02)' if worst_n < 0.02 else 'FAIL'})")
    print(f"--- RING GAP for the balls (clearance must NOT reach wallzone_outter) ---")
    for (y, rmax, romax, gap) in gap_lines:
        print(f"  y={y:.0f}: max clearance node R={rmax:.3f}  wallzone_outter R={romax:.3f}  "
              f"gap={gap:.3f} m  ({'GAP OK' if rmax < romax else 'NO GAP -- FAIL'})")
    print(f"--- rock<->clearance node coincidence (disjoint node IDs either way) ---")
    print(f"min distance any clearance node -> any rock node : {dd.min():.6f} m")
    print(f"  {coincident} clearance nodes coincide (<1e-4) with a rock node -- these are the INVERT "
          f"FLOOR-CHORD nodes (z {coincident_z.min():.3f}..{coincident_z.max():.3f}); wall_inner.stl and "
          f"wallzone_outter.stl SHARE the invert floor rim, so the fill floor sits on the rock floor.")
    print(f"  min distance among NON-coincident (ARCH) clearance nodes -> rock : {arch_gap:.5f} m  "
          f"-- this is the EMPTY ARCH RING gap for the balls (>0 confirms the gap, NOT a weld).")
    print(f"  NOTE: clearance node IDs are OFFSET above the rock max id ({rock_max_id}); the rock and "
          f"clearance share NO node IDs (disjoint range) even at the coincident floor.")
    fsz = os.path.getsize(out_inp)
    print(f"\ninp size {fsz/1e6:.2f} MB")
    print(f"wrote {out_inp}")


def main(solid=False):
    """solid=False -> couple_hex.inp (rock only, bore is a hole; the original deliverable, unchanged).
    solid=True  -> couple_hex_solid.inp = the SAME rock PLUS the butterfly-filled bore interior
    welded gp-to-gp into group 'excav' (slot 'type'), for `zone relax excavate` initial balance."""
    out_inp = os.path.join(HERE, 'couple_hex_solid.inp') if solid else INP
    xs_s, ys_s, surfs = sample_surfaces()
    from scipy.interpolate import RegularGridInterpolator
    S = [RegularGridInterpolator((xs_s, ys_s), s, bounds_error=False, fill_value=None) for s in surfs]
    axc, azc, axis_fn, ring_fn, adiag = tunnel_axis_from_stl()
    r0, f0, _ = ring_fn(885.0)
    init_edge_split(r0, f0)                          # lock the core-box edge index split (no twist)
    if solid:
        init_fill_junctions(r0)                      # balanced butterfly junctions (right==left, top==bot)
        print(f"FILL junctions (balanced petals) ring indices: {FILL_JUNC}  "
              f"arc edges r/t/l/b = {FILL_JUNC[1]-FILL_JUNC[0]}/{FILL_JUNC[2]-FILL_JUNC[1]}/"
              f"{FILL_JUNC[3]-FILL_JUNC[2]}/{N_RING-FILL_JUNC[3]}  core block "
              f"{FILL_JUNC[1]-FILL_JUNC[0]}x{FILL_JUNC[2]-FILL_JUNC[1]} cells")
    print(f"core-box edge split (inner-ring indices): right[0:{EDGE_SPLIT[0]}] "
          f"top[{EDGE_SPLIT[0]}:{EDGE_SPLIT[1]}] left[{EDGE_SPLIT[1]}:{EDGE_SPLIT[2]}] "
          f"bottom[{EDGE_SPLIT[2]}:{N_RING}]")
    print(f"AXIS from wallzone_outter.stl: {len(adiag['yk'])} y-stations "
          f"(deg-4 trend resid x|max {np.abs(adiag['resx']).max():.3f} "
          f"z|max {np.abs(adiag['resz']).max():.3f} m; SWEEP uses the EXACT per-y centroid)")
    print(f"inner ring @885: {len(r0)} nodes (arch {N_RING-N_FLOOR} + invert chord {N_FLOOR})  "
          f"width {np.ptp(r0[:,0]):.2f}  height {np.ptp(r0[:,1]):.2f}")

    Yv = np.linspace(Y0, Y1, int(round((Y1-Y0)/DY))+1); NY = len(Yv)
    rings = []; fracs = []
    for y in Yv:
        rg, fa, _ = ring_fn(y); rings.append(rg); fracs.append(fa)
    CxCz = np.array([ring_centroid(rg) for rg in rings])
    Cx, Cz = CxCz[:, 0], CxCz[:, 1]

    FILL_PATCHES = {'core', 'p_right', 'p_top', 'p_left', 'p_bot'}
    jm = NY // 2
    P0 = build_section(Cx[jm], Cz[jm], Yv[jm], rings[jm], fracs[jm], solid=solid)
    src, quads, quad_patch = weld_section(P0); NS = len(src)
    coords = np.empty((NS*NY, 3))
    for j in range(NY):
        P = build_section(Cx[j], Cz[j], Yv[j], rings[j], fracs[j], solid=solid)
        for s, (n, a, b) in enumerate(src):
            xz = P[n][a, b]; coords[s*NY+j] = (xz[0], Yv[j], xz[1])

    # tube-hex mask: a swept hex is an O-grid TUBE cell iff all 4 base section-nodes are 'tube'.
    # excav-hex mask: a swept hex is a bore-FILL cell iff its generating section quad came from a
    # fill patch (core/petal).  Provenance is tracked per quad because a fill quad on the ring uses
    # ring nodes already owned by the 'tube' patch -- so a node-tag test would misclassify them.
    is_tube_node = np.array([n == 'tube' for (n, a, b) in src])
    hexes = []; tubemask = []; excavmask = []
    for qk, (q0, q1, q2, q3) in enumerate(quads):
        t = bool(is_tube_node[q0] and is_tube_node[q1] and is_tube_node[q2] and is_tube_node[q3])
        e = quad_patch[qk] in FILL_PATCHES
        for j in range(NY-1):
            hexes.append((q0*NY+j, q1*NY+j, q2*NY+j, q3*NY+j,
                          q0*NY+j+1, q1*NY+j+1, q2*NY+j+1, q3*NY+j+1))
            tubemask.append(t); excavmask.append(e)
    H = np.array(hexes); tubemask = np.array(tubemask); excavmask = np.array(excavmask)
    d = np.linalg.det(np.einsum('cia,mib->mcab', DN, coords[H], optimize=True))
    allneg = d.max(1) < 0; H[allneg] = H[allneg][:, [4, 5, 6, 7, 0, 1, 2, 3]]
    Pc = coords[H]
    d = np.linalg.det(np.einsum('cia,mib->mcab', DN, Pc, optimize=True))
    nbad = int(((d.min(1) <= 0) & (d.max(1) > 0)).sum())
    el = np.linalg.norm(Pc[:, HE[:, 0]] - Pc[:, HE[:, 1]], axis=2)
    asp = el.max(1) / np.maximum(el.min(1), 1e-12)
    J = np.einsum('cia,mib->mcab', DN, Pc, optimize=True)
    sj = (np.linalg.det(J) / np.maximum(np.linalg.norm(J, axis=3).prod(2), 1e-12)).min(1)

    # ---- classify each hex into layer2..layer6 by centroid vs S02..S05 (ROCK only) -
    # the bore-FILL hexes (excavmask) are NOT geology -- they go to group 'excav' (slot 'type'),
    # not into any layer (slot 'mat'), so the rock layer counts stay IDENTICAL to couple_hex.inp.
    cent = Pc.mean(1); cz = cent[:, 2]
    s2c = S[0](cent[:, :2]); s3c = S[1](cent[:, :2])
    s4c = S[2](cent[:, :2]); s5c = S[3](cent[:, :2])
    lay = np.full(len(H), 6, int)
    lay[cz >= s5c] = 5; lay[cz >= s4c] = 4; lay[cz >= s3c] = 3; lay[cz >= s2c] = 2

    used = np.unique(H)
    remap = -np.ones(len(coords), np.int64); remap[used] = np.arange(len(used)); cc = coords[used]
    order = {}
    for k, (c, Ln) in enumerate(zip(H, lay)):
        grp = 'excav' if excavmask[k] else f'layer{Ln}'
        order.setdefault(grp, []).append(c)

    # ABAQUS .inp ELSETs map 1:1 to FLAC3D zone groups on import.  Rock ELSETs layer2..6 carry the
    # geology (slot 'mat'); the 'excav' ELSET carries the nullable bore fill (slot 'type').  The
    # FLAC3D-side `zone import ... use-given-id` then `zone group 'excav' slot 'type'` /
    # `zone group 'layerN' slot 'mat'` reproduces the two slots; the ELSET names alone weld the mesh.
    with open(out_inp, 'w') as f:
        if solid:
            f.write('*Heading\n couple_hex_solid (rock O-grid on wallzone_outter.stl + picture-frame '
                    'background; bore interior FILLED with butterfly hexes welded gp-to-gp into ELSET '
                    "excav (slot 'type', nullable for zone relax excavate); layers slot 'mat')\n*NODE\n")
        else:
            f.write('*Heading\n couple_hex (O-grid bore EXACT on wallzone_outter.stl + picture-frame '
                    'background, conformal S02..S05 by centroid, gp-to-gp)\n*NODE\n')
        for i, p in enumerate(cc, 1):
            f.write(f'{i}, {p[0]:.6f}, {p[1]:.6f}, {p[2]:.6f}\n')
        eid = 1
        for Ln in sorted(order):
            f.write(f'*ELEMENT, type=C3D8, ELSET={Ln}\n')
            for c in order[Ln]:
                f.write(f'{eid}, ' + ', '.join(str(int(remap[n])+1) for n in c) + '\n'); eid += 1

    key = np.round(cc / 1e-4).astype(np.int64)
    ndup = len(cc) - len(np.unique(key, axis=0))

    # ---- inner-ring node table: (x,z) of every O-grid inner ring node at every y ------
    tube_inner_s = [s for s, (n, a, b) in enumerate(src) if n == 'tube' and b == 0]
    NR = len(tube_inner_s)
    inner_xz = np.empty((NR, NY, 2))
    for ii, s in enumerate(tube_inner_s):
        block = coords[s*NY:(s+1)*NY]
        inner_xz[ii, :, 0] = block[:, 0]; inner_xz[ii, :, 1] = block[:, 2]
    axis_xz = np.column_stack([Cx, Cz])

    # ---- ACCEPTANCE 1: NO TWIST (per-node azimuth drift along y) -------------------
    rel = inner_xz - axis_xz[None, :, :]
    azi = np.arctan2(rel[:, :, 1], rel[:, :, 0])
    dazi = np.angle(np.exp(1j*np.diff(azi, axis=1)))
    azi_drift_deg = float(np.degrees(np.abs(dazi).max()))
    worst_node = int(np.unravel_index(np.abs(dazi).argmax(), dazi.shape)[0])
    print(f"\n=== ACCEPTANCE 1 -- NO TWIST (per-node azimuth drift along y) ===")
    print(f"max per-node azimuth change between consecutive y-planes: {azi_drift_deg:.4f} deg "
          f"(node {worst_node})   ({'PASS (<1 deg)' if azi_drift_deg < 1.0 else 'FAIL'})")

    # ---- ACCEPTANCE 2: inner ring (excavation surface) vs RAW wallzone_outter.stl --
    def pt_segs_dist(p, segs):
        best = 1e18
        for a, b in segs:
            ab = b - a; ap = p - a
            t = np.clip((ap @ ab)/max(ab @ ab, 1e-12), 0, 1)
            best = min(best, float(np.linalg.norm(ap - t*ab)))
        return best
    # floor classification: a ring node is on the invert chord (no STL beneath) -- excluded from
    # the node/face-to-STL metric, which is meaningful only where the lining wall STL exists (arch).
    print(f"\n=== ACCEPTANCE 2 -- inner ring (arch) vs RAW wallzone_outter.stl (worst over ALL y) ===")
    worst_n = 0.0; worst_ny = None; worst_f = 0.0; worst_fy = None
    for j in range(NY):
        segs = adiag['segs'](float(Yv[j]))
        if not segs:
            continue
        ring = inner_xz[:, j, :]
        rg, fa, isf = ring_fn(float(Yv[j]))               # is_floor mask (same node order)
        dn = np.array([pt_segs_dist(p, segs) for p in ring])
        if dn[~isf].max() > worst_n:
            worst_n = dn[~isf].max(); worst_ny = float(Yv[j])
        Rc = np.vstack([ring, ring[:1]])
        mids = 0.5*(Rc[:-1] + Rc[1:])
        archface = (~isf) & (~np.roll(isf, -1))
        dm = np.array([pt_segs_dist(m, segs) for m in mids])
        if dm[archface].max() > worst_f:
            worst_f = dm[archface].max(); worst_fy = float(Yv[j])
    print(f"max inner-NODE -> raw-STL distance over all {NY} y: {worst_n:.5f} m at y={worst_ny:.1f}  "
          f"({'PASS (<0.01)' if worst_n < 0.01 else 'FAIL'})")
    print(f"max inner-FACE-midpoint -> raw-STL distance over all faces: {worst_f:.5f} m at "
          f"y={worst_fy:.1f}  ({'PASS (<0.02)' if worst_f < 0.02 else 'FAIL'})")

    # ---- ACCEPTANCE 3: O-GRID TUBE CELL QUALITY ------------------------------------
    pct = lambda v, p: float(np.percentile(v, p))
    ta = asp[tubemask]; tsj = sj[tubemask]
    tube_nbad = int(((d.min(1) <= 0) & (d.max(1) > 0) & tubemask).sum())
    print(f"\n=== ACCEPTANCE 3 -- O-GRID TUBE CELL QUALITY ({int(tubemask.sum())} tube hexes) ===")
    print(f"tube aspect  median {np.median(ta):.2f}  p90 {pct(ta,90):.2f}  p99 {pct(ta,99):.2f}  "
          f"max {ta.max():.2f}   (cubic target p99<3.5 {'PASS' if pct(ta,99) < 3.5 else 'FAIL'}  "
          f"max<5 {'PASS' if ta.max() < 5 else 'FAIL'})")
    print(f"tube min scaled Jacobian {tsj.min():.4f}   "
          f"({'PASS (>0.18)' if tsj.min() > 0.18 else 'FAIL'})")
    print(f"tube mixed-sign Jacobian hexes: {tube_nbad}   ({'PASS' if tube_nbad == 0 else 'FAIL'})")

    # ---- ACCEPTANCE 4: RENDER ------------------------------------------------------
    render_bore_vs_stl(inner_xz, Yv, adiag)
    render_notwist(inner_xz, axis_xz, Yv)
    render_cells(coords, H, ta)
    render_outer_density(coords, H, sj, asp)
    render_cubic_cells(coords, H, asp)

    # ===============================================================================
    #  SOLID-BORE INTEGRITY (only when solid=True): excav fill + rock/excav weld
    # ===============================================================================
    if solid:
        nex = int(excavmask.sum()); nrk = int((~excavmask).sum())
        ex_orphan = 0                                   # checked below against the global orphan test
        # bbox of the excav fill
        exc_used = np.unique(H[excavmask])
        exbb_lo = coords[exc_used].min(0); exbb_hi = coords[exc_used].max(0)
        # excav cell integrity (subset of the global metrics)
        ex_nbad = int(((d.min(1) <= 0) & (d.max(1) > 0) & excavmask).sum())
        ex_zero = int((np.abs(np.linalg.det(np.einsum('cia,mib->mcab', DN, Pc[excavmask],
                       optimize=True))).max(1) <= 1e-12).sum()) if nex else 0
        ex_sj = sj[excavmask]

        # ----- WELD CHECK: the bore inner ring is the shared rock/excav interface ----
        # interface section nodes = the 'tube' b=0 column (the inner ring).  Both a rock TUBE hex
        # and an excav PETAL hex reference these SAME welded node IDs -> a true weld (shared IDs).
        # We (1) confirm each interface node is referenced by BOTH a rock hex and an excav hex, and
        # (2) report the min distance between DISTINCT node IDs on/near the interface (must be >> 0;
        # a value ~0 would mean two separate coincident nodes = a non-weld).
        iface_s = [s for s, (n, a, b) in enumerate(src) if n == 'tube' and b == 0]   # NR section nodes
        iface_gids = np.array([s*NY + j for s in iface_s for j in range(NY)])        # global node IDs
        iface_set = set(int(g) for g in iface_gids)
        rock_nodes = set(int(x) for x in np.unique(H[~excavmask]))
        exc_nodes  = set(int(x) for x in np.unique(H[excavmask]))
        shared = iface_set & rock_nodes & exc_nodes
        shared_remapped = sorted(int(remap[g]) + 1 for g in shared if remap[g] >= 0)
        # min distance between distinct interface node positions (after the global remap/dedup):
        ifc_xyz = coords[sorted(iface_set)]
        from scipy.spatial import cKDTree
        tree = cKDTree(ifc_xyz)
        dd, _ = tree.query(ifc_xyz, k=2)
        min_iface_gap = float(dd[:, 1].min())            # nearest DISTINCT interface node
        # global orphan check: every node in cc must be used by >=1 hex (true by remap construction)
        orphan = int((np.bincount(H.ravel(), minlength=len(coords))[used] == 0).sum())

        ringloop_xz = np.vstack([inner_xz[:, jm, :], inner_xz[:1, jm, :]])
        render_solid_section(coords, H, excavmask, ringloop_xz)

        print(f"\n=== SOLID-BORE INTEGRITY ===")
        print(f"rock hexes  : {nrk}")
        print(f"excav hexes : {nex}   (group 'excav', slot 'type')")
        print(f"total hexes : {len(H)}  = rock {nrk} + excav {nex}  "
              f"({'OK' if nrk+nex == len(H) else 'MISMATCH'})")
        print(f"excav bbox  : x[{exbb_lo[0]:.2f},{exbb_hi[0]:.2f}] "
              f"y[{exbb_lo[1]:.2f},{exbb_hi[1]:.2f}] z[{exbb_lo[2]:.2f},{exbb_hi[2]:.2f}]")
        print(f"excav mixed-sign Jacobian : {ex_nbad}   (MUST be 0)")
        print(f"excav zero/neg-volume     : {ex_zero}   (MUST be 0)")
        print(f"excav min scaled-Jacobian : {ex_sj.min():.4f}")
        print(f"--- rock/excav WELD ---")
        print(f"interface (bore inner-ring) section nodes: {len(iface_s)}  x NY {NY} = "
              f"{len(iface_set)} global gps")
        print(f"interface gps shared by BOTH a rock hex AND an excav hex: {len(shared)}  "
              f"({'WELD OK -- shared IDs' if len(shared) == len(iface_set) else 'PARTIAL'})")
        print(f"min distance between DISTINCT interface node positions: {min_iface_gap:.6f} m  "
              f"(a true weld shares IDs; this is the spacing between NEIGHBOURING interface gps, "
              f"NOT a duplicate pair -- duplicate coincident nodes anywhere = {ndup})")
        print(f"orphan nodes (unused) : {orphan}   (MUST be 0)")

    # ---- report --------------------------------------------------------------------
    fsz = os.path.getsize(out_inp)
    tag = 'couple_hex_solid' if solid else 'couple_hex'
    print(f"\n=== {tag} ===")
    print(f"inner-ring nodes per section: {NR}   (arch {N_RING-N_FLOOR} + invert chord {N_FLOOR})  "
          f"[cubic rebalance: was 160=146+14]")
    print(f"y sweep: DY={DY}  NY={NY}  [cubic rebalance: was DY=0.55, NY=92]")
    print(f"outer/peripheral radial cells (core box -> 40x40 edge): NSEAM={NSEAM}  "
          f"seam growth {GSEAM}")
    print(f"total hex {len(H)}   nodes {len(cc)}   (NS {NS} section nodes, NY {NY} y-planes)")
    cnt = {k: len(v) for k, v in sorted(order.items())}
    print(f"per-group: {cnt}")
    print(f"mixed-sign Jacobian hexes: {nbad}   (MUST be 0)")
    print(f"duplicate coincident node positions: {ndup}   (MUST be 0)")
    print(f"aspect ratio (all cells)  median {np.median(asp):.2f}  p90 {pct(asp,90):.2f}  "
          f"p99 {pct(asp,99):.2f}  max {asp.max():.2f}")
    print(f"min scaled Jacobian over all hexes: {sj.min():.4f}  (p01 {pct(sj,1):.3f})")
    print(f"inp size {fsz/1e6:.2f} MB")
    print(f"wrote {out_inp}")


if __name__ == '__main__':
    if '--clearance' in sys.argv:
        # couple_hex_clearance.inp: rock O-grid (byte-identical) + butterfly clearance fill inside
        # wall_inner.stl (ELSET excav), empty ring between for the balls.  Disjoint clearance node IDs.
        main_clearance()
    else:
        solid = ('--solid' in sys.argv)
        main(solid=solid)
