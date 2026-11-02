"""マーチング・テトラヘドラ法による等値面のメッシュ化。

格子点に値を持つスカラー場 values (nx, ny, nz) から、値が iso になる面
（等値面）を三角形メッシュとして取り出す。値が iso より小さい側を内側とする
（距離関数なら、iso = 0 で形の表面になる）。

マーチング・キューブ法と同じく、格子の立方体を 1 個ずつ調べるが、各立方体を
6 個の四面体に分けて処理する。四面体の頂点は 4 個なので、内外の組み合わせは
2^4 = 16 通りしかなく、その表もプログラムで簡単に作れる。
"""

from __future__ import annotations

import numpy as np

from common import FloatArray, IntArray
from mesh import Mesh

# 立方体の 8 個の角。番号 c の角は、格子上で (c & 1, (c >> 1) & 1, (c >> 2) & 1) だけずれた位置にある。
CORNERS = np.array([[c & 1, (c >> 1) & 1, (c >> 2) & 1] for c in range(8)])

# 立方体を、対角線 0-7 を共有する 6 個の四面体に分ける。各四面体は、角 0 から角 7 へ
# x, y, z の軸を 1 本ずつたどる経路に当たる（軸をたどる順番が 3! = 6 通りある）。
TETRAHEDRA = np.array([
    [0, 1, 3, 7], [0, 1, 5, 7], [0, 2, 3, 7],
    [0, 2, 6, 7], [0, 4, 5, 7], [0, 4, 6, 7],
])


def tetra_cases() -> list[list[tuple[tuple[int, int], ...]]]:
    """四面体の 16 通りの内外の組み合わせごとに、作る三角形の一覧を返す。

    組み合わせの番号 code は、頂点 i が内側なら bit i を 1 にした値である。
    三角形は、頂点を置く辺を 3 本並べて表す。辺は (内側の頂点, 外側の頂点) の組で表す。
    """
    cases: list[list[tuple[tuple[int, int], ...]]] = []
    for code in range(16):
        inside = [i for i in range(4) if code >> i & 1]
        outside = [i for i in range(4) if not code >> i & 1]
        if len(inside) in (0, 4):
            cases.append([])  # すべて内側か、すべて外側: 面は通らない
        elif len(inside) == 1:
            # 1 頂点だけが内側: その頂点から出る 3 本の辺を結ぶ三角形 1 枚
            cases.append([tuple((inside[0], o) for o in outside)])
        elif len(inside) == 3:
            # 1 頂点だけが外側: 同じく三角形 1 枚
            cases.append([tuple((i, outside[0]) for i in inside)])
        else:
            # 2 対 2: 内外をまたぐ 4 本の辺が四角形を作るので、三角形 2 枚に分ける
            (a, b), (c, d) = inside, outside
            cases.append([((a, c), (a, d), (b, d)), ((a, c), (b, d), (b, c))])
    return cases


def marching_tetrahedra(values: FloatArray, points: FloatArray, iso: float = 0.0) -> Mesh:
    """格子点の値 values (nx, ny, nz) と座標 points (nx, ny, nz, 3) から等値面のメッシュを作る。"""
    nx, ny, nz = values.shape
    flat_values = values.ravel()
    flat_points = points.reshape(-1, 3)
    # すべての立方体について、角 0 の格子点の通し番号を求める。
    ix, iy, iz = np.meshgrid(np.arange(nx - 1), np.arange(ny - 1), np.arange(nz - 1), indexing="ij")
    base = ((ix * ny + iy) * nz + iz).ravel()
    corner_offset = (CORNERS[:, 0] * ny + CORNERS[:, 1]) * nz + CORNERS[:, 2]
    cases = tetra_cases()

    # 三角形の頂点を置く辺を、両端の格子点の番号 (内側, 外側) で表して集める。形は (三角形数, 3, 2)
    edge_list: list[IntArray] = []
    for tetra in TETRAHEDRA:
        ids = base[:, None] + corner_offset[tetra][None, :]  # 四面体の 4 頂点の格子点番号 (立方体数, 4)
        code = ((flat_values[ids] < iso) * (1 << np.arange(4))).sum(axis=1)
        for case, triangles in enumerate(cases):
            selected = ids[code == case]
            for triangle in triangles:
                edge_list.append(np.stack([selected[:, list(edge)] for edge in triangle], axis=1))
    if not edge_list:
        return Mesh(np.zeros((0, 3)), np.zeros((0, 3), dtype=np.int64))
    edges = np.concatenate(edge_list)

    # 同じ辺の上の頂点は 1 個にまとめる（隣の三角形と頂点を共有させ、つながったメッシュにする）。
    count = flat_values.size
    keys = np.minimum(edges[..., 0], edges[..., 1]) * count + np.maximum(edges[..., 0], edges[..., 1])
    unique_keys, inverse = np.unique(keys.ravel(), return_inverse=True)
    a = unique_keys // count
    b = unique_keys % count
    # 辺の両端の値から、値がちょうど iso になる位置を線形補間で求める。
    t = (iso - flat_values[a]) / (flat_values[b] - flat_values[a])
    vertices = flat_points[a] + t[:, None] * (flat_points[b] - flat_points[a])
    faces = inverse.reshape(-1, 3)

    # 三角形の表（頂点が反時計回りに見える側）が外側を向くように、裏返しのものは頂点の順番を入れ替える。
    p0, p1, p2 = (vertices[faces[:, k]] for k in range(3))
    normal = np.cross(p1 - p0, p2 - p0)
    outward = flat_points[edges[:, 0, 1]] - flat_points[edges[:, 0, 0]]  # 内側から外側への向き
    flip = np.sum(normal * outward, axis=1) < 0.0
    faces[flip] = faces[flip][:, [0, 2, 1]]
    return Mesh(vertices, faces)
