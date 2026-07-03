import numpy as np
import re
import sys

INP = r"C:/Users/Wade/Desktop/Tunnel_TX/02_SmallModel/small_conformal.inp"
CL  = r"C:/Users/Wade/Desktop/Tunnel_TX/02_SmallModel/centerline_model.csv"

# ---------------------------------------------------------------------------
# Pass 1: parse the .inp into a NODE block and per-ELSET ELEMENT blocks.
# We read the file once, splitting on the '*' section headers. Node lines and
# element connectivity lines are accumulated as raw text, then parsed in bulk
# with np.fromstring (vectorized) -- no per-tet python loop.
# ---------------------------------------------------------------------------
node_chunks = []          # list of raw text blocks for *NODE
elset_chunks = {}         # elset name -> list of raw text blocks
order = []                # preserve elset discovery order

mode = None               # None | 'node' | 'elem'
cur_elset = None

hdr_re = re.compile(r"ELSET\s*=\s*([^,\s]+)", re.IGNORECASE)

with open(INP, "r") as f:
    buf = []
    for line in f:
        if line[0] == "*":
            # flush current buffer into the active target before switching
            if buf:
                txt = "".join(buf)
                if mode == "node":
                    node_chunks.append(txt)
                elif mode == "elem":
                    elset_chunks[cur_elset].append(txt)
                buf = []
            up = line.upper()
            if up.startswith("*NODE"):
                mode = "node"
            elif up.startswith("*ELEMENT"):
                mode = "elem"
                m = hdr_re.search(line)
                cur_elset = m.group(1).strip() if m else "UNNAMED"
                if cur_elset not in elset_chunks:
                    elset_chunks[cur_elset] = []
                    order.append(cur_elset)
            else:
                # *Heading or any other -> ignore content
                mode = None
            continue
        if mode in ("node", "elem"):
            buf.append(line)
    if buf:
        txt = "".join(buf)
        if mode == "node":
            node_chunks.append(txt)
        elif mode == "elem":
            elset_chunks[cur_elset].append(txt)

# --- parse nodes: "id, x, y, z" -> (Nx4) float, vectorized ---
node_txt = "".join(node_chunks).replace(",", " ")
node_arr = np.fromstring(node_txt, sep=" ", dtype=np.float64).reshape(-1, 4)
node_ids = node_arr[:, 0].astype(np.int64)
node_xyz = node_arr[:, 1:4]

# map node id -> row index. ids appear 1-based & contiguous but don't assume.
max_id = int(node_ids.max())
id2row = np.full(max_id + 1, -1, dtype=np.int64)
id2row[node_ids] = np.arange(node_ids.shape[0], dtype=np.int64)

# --- parse elements per elset: "eid, n1,n2,n3,n4" -> (Mx5) int, vectorized ---
elset_conn = {}   # name -> (M,4) node-row indices
per_elset = {}
all_conn_list = []
all_elset_names = []
for name in order:
    txt = "".join(elset_chunks[name]).replace(",", " ")
    a = np.fromstring(txt, sep=" ", dtype=np.int64).reshape(-1, 5)
    conn_ids = a[:, 1:5]                 # 1-based node ids
    conn_rows = id2row[conn_ids]         # -> row indices into node_xyz
    elset_conn[name] = conn_rows
    per_elset[name] = int(conn_rows.shape[0])
    all_conn_list.append(conn_rows)
    all_elset_names.append((name, conn_rows.shape[0]))

conn = np.concatenate(all_conn_list, axis=0)   # (T,4) global, in elset order
total_tets = int(conn.shape[0])

# sanity: any unmapped node refs?
bad_ref = int(np.count_nonzero(conn < 0))

# ---------------------------------------------------------------------------
# Vectorized geometry: signed volume, edge lengths, aspect ratio.
# ---------------------------------------------------------------------------
p0 = node_xyz[conn[:, 0]]
p1 = node_xyz[conn[:, 1]]
p2 = node_xyz[conn[:, 2]]
p3 = node_xyz[conn[:, 3]]

e01 = p1 - p0
e02 = p2 - p0
e03 = p3 - p0
cross = np.cross(e02, e03)
signed_vol = np.einsum("ij,ij->i", e01, cross) / 6.0
abs_vol = np.abs(signed_vol)

negative_volume_tets = int(np.count_nonzero(signed_vol < 0.0))
degenerate_tets = int(np.count_nonzero(abs_vol < 1e-9))
min_abs_volume = float(abs_vol.min())

# all 6 edges
e12 = p2 - p1
e13 = p3 - p1
e23 = p3 - p2
edges_sq = np.stack([
    np.einsum("ij,ij->i", e01, e01),
    np.einsum("ij,ij->i", e02, e02),
    np.einsum("ij,ij->i", e03, e03),
    np.einsum("ij,ij->i", e12, e12),
    np.einsum("ij,ij->i", e13, e13),
    np.einsum("ij,ij->i", e23, e23),
], axis=1)
max_edge = np.sqrt(edges_sq.max(axis=1))

# aspect = max_edge^3 / (6*abs_vol). Guard zero volume.
safe_vol = np.where(abs_vol < 1e-300, 1e-300, abs_vol)
aspect = (max_edge ** 3) / (6.0 * safe_vol)
sliver_mask = aspect > 1000.0
sliver_tets = int(np.count_nonzero(sliver_mask))
worst_aspect_ratio = float(aspect.max())

# ---------------------------------------------------------------------------
# Duplicate coincident nodes: round xyz to 5 decimals, find buckets > 1.
# ---------------------------------------------------------------------------
xyz_r = np.round(node_xyz, 5)
# lexsort to group identical rows, vectorized
uniq, inv, counts = np.unique(xyz_r, axis=0, return_inverse=True, return_counts=True)
inv = inv.ravel()
dup_bucket_mask = counts[inv] > 1
duplicate_coincident_nodes = int(np.count_nonzero(dup_bucket_mask))
n_dup_buckets = int(np.count_nonzero(counts > 1))

# ---------------------------------------------------------------------------
# Lining geometry vs centerline.
# ---------------------------------------------------------------------------
cl = np.loadtxt(CL, delimiter=",", skiprows=1)
cl_x, cl_y, cl_z = cl[:, 0], cl[:, 1], cl[:, 2]
# fit y -> x and y -> z, deg 4
cx = np.polyfit(cl_y, cl_x, 4)
cz = np.polyfit(cl_y, cl_z, 4)

lining_name = None
for nm in order:
    if nm.lower() == "lining":
        lining_name = nm
        break

lining_tets = per_elset.get(lining_name, 0) if lining_name else 0

lining_mean_thickness_m = float("nan")
lining_y_gaps = "none"
lining_min_r = lining_max_r = float("nan")
if lining_name and lining_tets > 0:
    lc = elset_conn[lining_name]
    cen = (node_xyz[lc[:, 0]] + node_xyz[lc[:, 1]] +
           node_xyz[lc[:, 2]] + node_xyz[lc[:, 3]]) / 4.0
    cy = cen[:, 1]
    cl_x_at = np.polyval(cx, cy)
    cl_z_at = np.polyval(cz, cy)
    dx = cen[:, 0] - cl_x_at
    dz = cen[:, 2] - cl_z_at
    radial = np.sqrt(dx * dx + dz * dz)
    p5, p95 = np.percentile(radial, [5, 95])
    lining_mean_thickness_m = float(p95 - p5)
    lining_min_r = float(radial.min())
    lining_max_r = float(radial.max())

    # 2 m bins over [850, 950]
    bin_edges = np.arange(850.0, 950.0 + 1e-6, 2.0)
    hist, _ = np.histogram(cy, bins=bin_edges)
    empty = np.where(hist == 0)[0]
    if empty.size == 0:
        lining_y_gaps = "none"
    else:
        gaps = ["[%.0f,%.0f)" % (bin_edges[i], bin_edges[i + 1]) for i in empty]
        lining_y_gaps = ", ".join(gaps)

# ---------------------------------------------------------------------------
# Decisions.
# ---------------------------------------------------------------------------
solve_ready = not (degenerate_tets > 0 or duplicate_coincident_nodes > 0)
creep_ready = not (sliver_tets > 0.01 * total_tets)

# worst examples (small argpartition, not a python loop over all tets)
def worst_idx(arr, k=3, largest=True):
    if largest:
        idx = np.argpartition(-arr, k)[:k]
        return idx[np.argsort(-arr[idx])]
    else:
        idx = np.argpartition(arr, k)[:k]
        return idx[np.argsort(arr[idx])]

wa = worst_idx(aspect, 3, True)
wv = worst_idx(abs_vol, 3, False)

# which elset each global tet belongs to (for reporting)
elset_bounds = np.cumsum([0] + [per_elset[n] for n in order])
def elset_of(gi):
    for j, n in enumerate(order):
        if elset_bounds[j] <= gi < elset_bounds[j + 1]:
            return n
    return "?"

print("=== MESH VERIFICATION ===")
print("total_tets:", total_tets)
print("bad_node_refs:", bad_ref)
print("per_elset:", {n: per_elset[n] for n in order})
print("negative_volume_tets:", negative_volume_tets,
      "(%.4f%%)" % (100.0 * negative_volume_tets / total_tets))
print("degenerate_tets:", degenerate_tets)
print("min_abs_volume: %.6e" % min_abs_volume)
print("sliver_tets:", sliver_tets,
      "(%.4f%%)" % (100.0 * sliver_tets / total_tets))
print("worst_aspect_ratio: %.4f" % worst_aspect_ratio)
print("duplicate_coincident_nodes:", duplicate_coincident_nodes,
      "in", n_dup_buckets, "buckets")
print("total_nodes:", node_ids.shape[0])
print("lining_tets:", lining_tets)
print("lining radial r: min=%.4f max=%.4f" % (lining_min_r, lining_max_r))
print("lining_mean_thickness_m (p95-p5): %.6f" % lining_mean_thickness_m)
print("lining_y_gaps:", lining_y_gaps)
print("solve_ready:", solve_ready)
print("creep_ready:", creep_ready)

print("\n--- worst aspect examples (global tet idx) ---")
for gi in wa:
    print("  gi=%d elset=%s aspect=%.2f abs_vol=%.4e max_edge=%.4f" %
          (gi, elset_of(gi), aspect[gi], abs_vol[gi], max_edge[gi]))
print("--- smallest abs_vol examples ---")
for gi in wv:
    print("  gi=%d elset=%s abs_vol=%.6e aspect=%.2f" %
          (gi, elset_of(gi), abs_vol[gi], aspect[gi]))

# sliver distribution per elset
print("\n--- sliver per elset ---")
for j, n in enumerate(order):
    lo, hi = elset_bounds[j], elset_bounds[j + 1]
    sc = int(np.count_nonzero(sliver_mask[lo:hi]))
    print("  %s: %d slivers / %d (%.3f%%)" %
          (n, sc, per_elset[n], 100.0 * sc / max(per_elset[n], 1)))
