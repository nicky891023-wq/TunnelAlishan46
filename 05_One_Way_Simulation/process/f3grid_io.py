#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
f3grid_io.py -- parse FLAC3D `zone export` .f3grid (ASCII) into a pyvista UnstructuredGrid,
with .vtu caching (parse once, reload fast). Zones keyed by original FLAC3D ids so per-stage
field dumps (id state pp visc / id ux uy uz) can be attached as cell/point data.

f3grid format (FLAC3D 6.00):
  G  <gid> <x> <y> <z>
  Z  T4 <zid> <g1> <g2> <g3> <g4>        (tet; B8/W6/P5/H8 etc. for other shapes)
  ZGROUP "name" SLOT "slot"  \n  <zid list lines>
"""
from pathlib import Path
import numpy as np
import pyvista as pv
import vtk

CELLTYPE = {
    "T4": (vtk.VTK_TETRA, 4),
    "B8": (vtk.VTK_HEXAHEDRON, 8),
    "W6": (vtk.VTK_WEDGE, 6),
    "P5": (vtk.VTK_PYRAMID, 5),
}


def parse_f3grid(path):
    """returns (points Nx3, gid2idx dict, cells list[(vtktype, [gp idx...])], zids array,
    groups: {slot: {zid: groupname}})"""
    pts, gids = [], []
    cells, zids = [], []
    groups = {}
    cur_group = None
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if not line:
                continue
            c0 = line[0]
            if c0 == "G":
                p = line.split()
                gids.append(int(p[1])); pts.append((float(p[2]), float(p[3]), float(p[4])))
            elif c0 == "Z" and line[1] == " ":
                p = line.split()
                typ = p[1]
                if typ in CELLTYPE:
                    zids.append(int(p[2]))
                    cells.append((typ, [int(x) for x in p[3:3 + CELLTYPE[typ][1]]]))
                cur_group = None
            elif line.startswith("ZGROUP"):
                p = line.split('"')
                name, slot = p[1], p[3] if len(p) > 3 else "default"
                groups.setdefault(slot, {})
                cur_group = (slot, name)
            elif c0 in " 0123456789" and cur_group is not None and line.strip():
                slot, name = cur_group
                for tok in line.split():
                    groups[slot][int(tok)] = name
            elif c0 == "*":
                if "FACES" in line:      # stop before faces section (not needed)
                    break
                cur_group = None
    pts = np.asarray(pts)
    gid2idx = {g: i for i, g in enumerate(gids)}
    return pts, gid2idx, cells, np.asarray(zids), groups


def to_unstructured(path, cache=True):
    """f3grid -> pyvista UnstructuredGrid with cell data 'zid' (+ 'layer' int from slot '1').
    Caches to <path>.vtu."""
    path = Path(path)
    vtu = path.with_suffix(".vtu")
    if cache and vtu.exists() and vtu.stat().st_mtime > path.stat().st_mtime:
        return pv.read(str(vtu))
    pts, gid2idx, cells, zids, groups = parse_f3grid(path)
    n = len(cells)
    conn, types, offs = [], np.empty(n, np.uint8), []
    for typ, gps in cells:
        idx = [gid2idx[g] for g in gps]
        conn.append([len(idx)] + idx)
    types[:] = [CELLTYPE[t][0] for t, _ in cells]
    conn = np.concatenate(conn).astype(np.int64)
    grid = pv.UnstructuredGrid(conn, types, pts)
    grid.cell_data["zid"] = zids
    # layer name -> int code from slot '1' (layer1..layerN); keep mapping in field data
    slot = groups.get("1", {})
    names = sorted(set(slot.values()))
    code = {nm: i + 1 for i, nm in enumerate(names)}
    lay = np.array([code.get(slot.get(int(z), ""), 0) for z in zids], np.int32)
    grid.cell_data["layer"] = lay
    grid.field_data["layer_names"] = np.array(names)
    if cache:
        grid.save(str(vtu))
    return grid


def attach_zone_fields(grid, zf_path):
    """attach id-keyed zone dump (id state pp visc) as cell data arrays state/pp/visc."""
    d = np.loadtxt(zf_path, skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    rows = id2row[grid.cell_data["zid"]]
    assert (rows >= 0).all(), "zone id mismatch between f3grid and field dump"
    grid.cell_data["state"] = d[rows, 1]
    grid.cell_data["pp"] = d[rows, 2]
    grid.cell_data["visc"] = d[rows, 3]
    # threshold ACTIVE = creep zone (visc>0) currently flowing (visc < 1e50)
    v = d[rows, 3]
    grid.cell_data["active"] = ((v > 0) & (v < 1e50)).astype(np.int8)
    return grid


def attach_gp_disp(grid, gf_path, gid_order=None):
    """attach gridpoint displacement (id ux uy uz) as point data 'disp' (Nx3).
    Requires the same gid ordering used to build points; rebuild mapping from f3grid if given."""
    d = np.loadtxt(gf_path, skiprows=1)
    id2row = np.full(int(d[:, 0].max()) + 1, -1, np.int64)
    id2row[d[:, 0].astype(np.int64)] = np.arange(len(d))
    if gid_order is None:
        raise ValueError("pass gid_order (original G ids in point order)")
    rows = id2row[gid_order]
    assert (rows >= 0).all()
    grid.point_data["disp"] = d[rows, 1:4]
    grid.point_data["umag"] = np.linalg.norm(d[rows, 1:4], axis=1)
    return grid


def gid_order_of(path):
    """original G-id sequence (point order) of an f3grid file."""
    gids = []
    with open(path, "r", errors="ignore") as f:
        for line in f:
            if line.startswith("G "):
                gids.append(int(line.split()[1]))
            elif line.startswith("* ZONES"):
                break
    return np.asarray(gids, np.int64)
