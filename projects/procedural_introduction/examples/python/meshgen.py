"""手続きでメッシュを作る関数（第 6 章）。

* 格子の三角形分割（parametric_surface）と、それを使った基本形状（平面・円柱・球）
* 回転体（lathe）と、断面を曲線に沿って動かすスイープ（sweep）
* 曲線に沿った座標系（フレネ標構と回転最小化標構）
* Catmull-Rom スプライン、ハイトマップからの格子メッシュ
* 三角形ごとに色を指定して描く関数と、スムーズシェーディングの簡易表示

座標系は matplotlib に合わせて z 軸を上にとる。三角形は外側から見て反時計回りに並べる。
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import numpy as np

from common import FloatArray, IntArray
from mesh import Mesh, shade


def grid_faces(rows: int, columns: int, wrap: bool = False) -> IntArray:
    """rows × columns 個の頂点を並べた格子を三角形に分ける。

    頂点 (行 j, 列 i) の番号は j * columns + i とする。格子の 1 マス（四角形）を 2 枚の
    三角形に分け、列方向を u、行方向を v としたとき、u 方向 × v 方向の向きを表とする。
    wrap が真なら、最後の列と最初の列をつなぐ（円柱の側面のように閉じる）。
    """
    cell_columns = columns if wrap else columns - 1
    j, i = np.meshgrid(np.arange(rows - 1), np.arange(cell_columns), indexing="ij")
    i1 = (i + 1) % columns
    a = j * columns + i
    b = j * columns + i1
    c = (j + 1) * columns + i1
    d = (j + 1) * columns + i
    first = np.stack([a, b, c], axis=-1).reshape(-1, 3)
    second = np.stack([a, c, d], axis=-1).reshape(-1, 3)
    return np.concatenate([first, second]).astype(np.int64)


def remove_degenerate(mesh: Mesh, epsilon: float = 1e-12) -> Mesh:
    """面積がほぼ 0 の三角形（球の極などで頂点が重なったもの）を取り除く。"""
    a, b, c = (mesh.vertices[mesh.faces[:, k]] for k in range(3))
    area = np.linalg.norm(np.cross(b - a, c - a), axis=1)
    return Mesh(mesh.vertices, mesh.faces[area > epsilon], mesh.uvs)


def parametric_surface(points: FloatArray, wrap: bool = False) -> Mesh:
    """(行, 列, 3) に並べた点の格子から、三角形メッシュを作る。

    wrap が偽なら、頂点ごとに UV（列方向 u、行方向 v、どちらも 0〜1）を付ける。
    閉じた形でも UV が必要な場合は、wrap を偽にして最初と最後の列に同じ位置の点を置く
    （UV の継ぎ目では、位置が同じでも UV が違う頂点を 2 つ持つ必要がある）。
    """
    rows, columns = points.shape[:2]
    faces = grid_faces(rows, columns, wrap)
    uvs = None
    if not wrap:
        u, v = np.meshgrid(np.linspace(0.0, 1.0, columns), np.linspace(0.0, 1.0, rows))
        uvs = np.stack([u, v], axis=-1).reshape(-1, 2)
    return remove_degenerate(Mesh(points.reshape(-1, 3).astype(np.float64), faces, uvs))


def combine(meshes: Sequence[Mesh]) -> Mesh:
    """複数のメッシュを 1 つにまとめる。すべてが UV を持つときは UV も連結する。"""
    offsets = np.cumsum([0] + [len(mesh.vertices) for mesh in meshes[:-1]])
    vertices = np.concatenate([mesh.vertices for mesh in meshes])
    faces = np.concatenate([mesh.faces + offset for mesh, offset in zip(meshes, offsets)])
    uv_list = [mesh.uvs for mesh in meshes]
    uvs = np.concatenate([uv for uv in uv_list if uv is not None]) if all(uv is not None for uv in uv_list) else None
    return Mesh(vertices, faces, uvs)


def plane(width: float, depth: float, columns: int, rows: int) -> Mesh:
    """xy 平面上の、columns × rows 個の頂点を持つ格子（中心が原点）。"""
    x, y = np.meshgrid(np.linspace(-width / 2, width / 2, columns), np.linspace(-depth / 2, depth / 2, rows))
    return parametric_surface(np.stack([x, y, np.zeros_like(x)], axis=-1))


def disk(radius: float, height: float, segments: int, up: bool) -> Mesh:
    """高さ height にある円板。中心の頂点から扇形に三角形を張る。up が真なら上向き。"""
    angle = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    rim = np.stack([radius * np.cos(angle), radius * np.sin(angle), np.full(segments, height)], axis=-1)
    vertices = np.concatenate([[[0.0, 0.0, height]], rim])
    i = np.arange(segments)
    faces = np.stack([np.zeros(segments, dtype=np.int64), 1 + i, 1 + (i + 1) % segments], axis=-1)
    if not up:
        faces = faces[:, ::-1]
    uvs = 0.5 + 0.5 * vertices[:, :2] / radius
    return Mesh(vertices, faces.astype(np.int64), uvs)


def cylinder(radius: float, height: float, segments: int, rings: int = 2, caps: bool = True) -> Mesh:
    """z 軸に沿った円柱。側面は segments × rings の格子、caps が真なら上下にふたを付ける。"""
    angle = np.linspace(0.0, 2.0 * np.pi, segments + 1)  # 継ぎ目の列を重複させて UV を付ける
    z = np.linspace(0.0, height, rings)
    a, zz = np.meshgrid(angle, z)
    side = parametric_surface(np.stack([radius * np.cos(a), radius * np.sin(a), zz], axis=-1))
    if not caps:
        return side
    return combine([side, disk(radius, 0.0, segments, up=False), disk(radius, height, segments, up=True)])


def uv_sphere(radius: float, segments: int, rings: int, wrap: bool = False) -> Mesh:
    """経度 segments 分割、緯度 rings 分割の球（UV 球）。

    wrap が偽なら経度 0 と 360 度の列を重複させて UV を付け、真なら列を共有して閉じる。
    """
    if wrap:
        longitude = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    else:
        longitude = np.linspace(0.0, 2.0 * np.pi, segments + 1)
    latitude = np.linspace(-np.pi / 2, np.pi / 2, rings + 1)
    lon, lat = np.meshgrid(longitude, latitude)
    points = radius * np.stack([np.cos(lat) * np.cos(lon), np.cos(lat) * np.sin(lon), np.sin(lat)], axis=-1)
    if wrap:
        # 極の頂点を 1 つにまとめないと、極の周りの法線の平均が乱れる。
        mesh = parametric_surface(points[1:-1], wrap=True)
        count = len(mesh.vertices)
        south, north = count, count + 1
        i = np.arange(segments)
        bottom = np.stack([np.full(segments, south), (i + 1) % segments, i], axis=-1)
        top_row = (rings - 2) * segments
        top = np.stack([np.full(segments, north), top_row + i, top_row + (i + 1) % segments], axis=-1)
        vertices = np.concatenate([mesh.vertices, [[0.0, 0.0, -radius], [0.0, 0.0, radius]]])
        return Mesh(vertices, np.concatenate([mesh.faces, bottom, top]).astype(np.int64))
    return parametric_surface(points)


def lathe(radius: FloatArray, height: FloatArray, segments: int) -> Mesh:
    """断面の曲線（半径 radius と高さ height の組）を z 軸の周りに 1 周回した回転体。"""
    angle = np.linspace(0.0, 2.0 * np.pi, segments + 1)
    a, r = np.meshgrid(angle, radius)
    _, z = np.meshgrid(angle, height)
    return parametric_surface(np.stack([r * np.cos(a), r * np.sin(a), z], axis=-1))


def _normalize_rows(vectors: FloatArray) -> FloatArray:
    lengths = np.linalg.norm(vectors, axis=-1, keepdims=True)
    result: FloatArray = vectors / np.maximum(lengths, 1e-12)
    return result


def tangents(points: FloatArray) -> FloatArray:
    """折れ線の各点での単位接線ベクトル（前後の点の差から求める）。"""
    return _normalize_rows(np.gradient(points, axis=0))


def frenet_frames(points: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray]:
    """フレネ標構（接線 T、主法線 N、従法線 B）。N は曲がる向き（T の変化の向き）。

    曲率が 0 に近い所で N が定まらず、変曲点では N が急に反転する。
    """
    t = tangents(points)
    n = _normalize_rows(np.gradient(t, axis=0))
    b = np.cross(t, n)
    return t, n, b


def rotation_minimizing_frames(
    points: FloatArray, initial_normal: Sequence[float] | None = None
) -> tuple[FloatArray, FloatArray, FloatArray]:
    """回転最小化標構（平行移動による標構）を、二重反射法（Wang ら、2008 年）で求める。

    前の点の法線を、接線を前の接線から今の接線へ移す最小の回転で運ぶ。ねじれが生じないので、
    パイプや道路の断面が曲線の途中で急に回らない。
    """
    t = tangents(points)
    count = len(points)
    n = np.zeros_like(points)
    if initial_normal is None:
        # 最初の接線と平行でない軸を選び、接線に垂直な成分を初期の法線にする。
        axis = np.array([0.0, 0.0, 1.0]) if abs(t[0, 2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    else:
        axis = np.asarray(initial_normal, dtype=np.float64)
    n[0] = _normalize_rows(axis - np.dot(axis, t[0]) * t[0])
    for k in range(count - 1):
        # 1 回目の反射: 点 k と k+1 を結ぶ線分の垂直二等分面で反射する。
        v1 = points[k + 1] - points[k]
        c1 = float(np.dot(v1, v1))
        if c1 < 1e-20:
            n[k + 1] = n[k]
            continue
        n_l = n[k] - (2.0 / c1) * np.dot(v1, n[k]) * v1
        t_l = t[k] - (2.0 / c1) * np.dot(v1, t[k]) * v1
        # 2 回目の反射: 反射後の接線を目標の接線に重ねる面で反射する。
        v2 = t[k + 1] - t_l
        c2 = float(np.dot(v2, v2))
        n[k + 1] = n_l if c2 < 1e-20 else n_l - (2.0 / c2) * np.dot(v2, n_l) * v2
    n = _normalize_rows(n)
    b = np.cross(t, n)
    return t, n, b


def sweep(points: FloatArray, normals: FloatArray, binormals: FloatArray, section: FloatArray,
          scale: FloatArray | None = None) -> Mesh:
    """断面 section（(K, 2) の 2 次元座標）を、曲線 points に沿って動かした面（スイープ）。

    各点で、断面の x 座標を法線 N の向きに、y 座標を従法線 B の向きに置く。
    scale を与えると、点ごとに断面の大きさを変えられる（先細りの枝など）。
    閉じた断面にしたい場合は、section の最後に最初の点を重ねて置く。
    """
    factor = np.ones(len(points)) if scale is None else scale
    sx = section[None, :, 0] * factor[:, None]
    sy = section[None, :, 1] * factor[:, None]
    grid = points[:, None, :] + sx[..., None] * normals[:, None, :] + sy[..., None] * binormals[:, None, :]
    return parametric_surface(grid)


def circle_section(radius: float, segments: int) -> FloatArray:
    """スイープ用の円の断面（最後の点は最初の点と重なる）。"""
    angle = np.linspace(0.0, 2.0 * np.pi, segments + 1)
    return np.stack([radius * np.cos(angle), radius * np.sin(angle)], axis=-1)


def catmull_rom(control: FloatArray, samples: int) -> FloatArray:
    """制御点をすべて通る Catmull-Rom スプライン。区間ごとに samples 個の点を返す。

    端の区間は、最初と最後の制御点を複製して補う。
    """
    p = np.concatenate([control[:1], control, control[-1:]])
    t = np.linspace(0.0, 1.0, samples, endpoint=False)[:, None]
    pieces = []
    for k in range(len(control) - 1):
        p0, p1, p2, p3 = p[k], p[k + 1], p[k + 2], p[k + 3]
        pieces.append(0.5 * (2.0 * p1 + (p2 - p0) * t + (2.0 * p0 - 5.0 * p1 + 4.0 * p2 - p3) * t ** 2
                             + (3.0 * p1 - p0 - 3.0 * p2 + p3) * t ** 3))
    pieces.append(control[-1:])
    return np.concatenate(pieces)


def heightfield(heights: FloatArray, spacing: float = 1.0, origin: Sequence[float] = (0.0, 0.0)) -> Mesh:
    """ハイトマップ heights[行 y, 列 x] から、格子状の地形メッシュを作る。"""
    rows, columns = heights.shape
    x, y = np.meshgrid(origin[0] + np.arange(columns) * spacing, origin[1] + np.arange(rows) * spacing)
    return parametric_surface(np.stack([x, y, heights], axis=-1))


def frame_cylinder(start: Sequence[float] | FloatArray, end: Sequence[float] | FloatArray, radius_start: float,
                   radius_end: float, segments: int = 8) -> Mesh:
    """点 start から end へ伸びる、ふたの無い円錐台（枝 1 本分）。"""
    p0 = np.asarray(start, dtype=np.float64)
    p1 = np.asarray(end, dtype=np.float64)
    axis = p1 - p0
    axis /= max(float(np.linalg.norm(axis)), 1e-12)
    helper = np.array([0.0, 0.0, 1.0]) if abs(axis[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(axis, helper)
    u /= np.linalg.norm(u)
    v = np.cross(axis, u)
    angle = np.linspace(0.0, 2.0 * np.pi, segments, endpoint=False)
    ring = np.cos(angle)[:, None] * u + np.sin(angle)[:, None] * v
    vertices = np.concatenate([p0 + radius_start * ring, p1 + radius_end * ring])
    # u × v = axis なので、角度の増える向きを列、軸の向きを行にすると外向きになる。
    return Mesh(vertices, grid_faces(2, segments, wrap=True))


def draw_faces(ax: Any, mesh: Mesh, facecolors: FloatArray, edgecolor: str | None = None,
               linewidth: float = 0.2) -> None:
    """三角形ごとの色 facecolors（(M, 3)）をそのまま使って、3D の軸にメッシュを描く。"""
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    collection = Poly3DCollection(
        mesh.vertices[mesh.faces], facecolors=facecolors,
        edgecolors=edgecolor if edgecolor else facecolors, linewidths=linewidth,
    )
    ax.add_collection3d(collection)


def subdivide_smooth(mesh: Mesh, normals: FloatArray, level: int) -> tuple[Mesh, FloatArray]:
    """各三角形を level × level 個の小さな三角形に分け、頂点の法線を重心座標で補間する。

    形は元の平らな三角形のままで、法線だけが滑らかに変わる。スムーズシェーディング
    （頂点の法線を面の内部で補間して陰影を付ける方法）を、面ごとにしか色を塗れない
    matplotlib で近似的に表示するために使う。戻り値は小さな三角形のメッシュとその法線。
    """
    # 1 枚の三角形の中に置く点の重心座標 (w0, w1, w2)
    pairs = [(i, j) for j in range(level + 1) for i in range(level + 1 - j)]
    index = {pair: k for k, pair in enumerate(pairs)}
    bary = np.array([[1.0 - (i + j) / level, i / level, j / level] for i, j in pairs])
    small = []
    for j in range(level):
        for i in range(level - j):
            small.append((index[(i, j)], index[(i + 1, j)], index[(i, j + 1)]))
            if i + j + 1 < level:
                small.append((index[(i + 1, j)], index[(i + 1, j + 1)], index[(i, j + 1)]))
    local = np.array(small)
    corners = mesh.vertices[mesh.faces]  # (M, 3, 3)
    corner_normals = normals[mesh.faces]
    points = np.einsum("pk,mkd->mpd", bary, corners)  # (M, P, 3)
    point_normals = np.einsum("pk,mkd->mpd", bary, corner_normals)
    offsets = (np.arange(len(mesh.faces)) * len(pairs))[:, None, None]
    faces = (local[None, :, :] + offsets).reshape(-1, 3)
    vertices = points.reshape(-1, 3)
    sub_normals = _normalize_rows(point_normals.reshape(-1, 3))
    face_normals = _normalize_rows(sub_normals[faces].mean(axis=1))
    return Mesh(vertices, faces.astype(np.int64)), face_normals


def shaded_colors(normals: FloatArray, base: Sequence[float] | FloatArray) -> FloatArray:
    """法線から陰影を付けた色（mesh.shade と同じ光源）。base は 1 色でも面ごとの色でもよい。"""
    colors = np.asarray(base, dtype=np.float64)
    if colors.ndim == 1:
        return shade(normals, colors)
    result: FloatArray = shade(normals, (1.0, 1.0, 1.0)) * colors
    return result
