"""第 11 章: 衝突判定の関数集。

座標は画面座標（y 軸が下向き）を想定しているが、どの関数も座標軸の向きにはよらずに使える。
接触の情報は「法線（1 つ目の図形から 2 つ目の図形へ向かう単位ベクトル）」と「めり込みの深さ」の組で返す。

collision_demo.py、balls_demo.py、platformer.py から import して使う。
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from pygame import Vector2

Contact = tuple[Vector2, float]  # (法線, めり込みの深さ)
EPSILON = 1e-9


@dataclass(frozen=True)
class AABB:
    """軸に平行な長方形（Axis-Aligned Bounding Box）。"""

    left: float
    top: float
    right: float
    bottom: float

    @staticmethod
    def from_center(cx: float, cy: float, width: float, height: float) -> AABB:
        return AABB(cx - width / 2, cy - height / 2, cx + width / 2, cy + height / 2)

    @property
    def center(self) -> Vector2:
        return Vector2((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    @property
    def half_size(self) -> Vector2:
        return Vector2((self.right - self.left) / 2, (self.bottom - self.top) / 2)


# --- 点・円・長方形 ---

def point_in_aabb(p: Vector2, box: AABB) -> bool:
    return box.left <= p.x <= box.right and box.top <= p.y <= box.bottom


def circles_overlap(c1: Vector2, r1: float, c2: Vector2, r2: float) -> bool:
    """2 つの円が重なっているか。平方根を避けるため、距離の 2 乗で比べる。"""
    return c1.distance_squared_to(c2) < (r1 + r2) ** 2


def circle_circle_contact(c1: Vector2, r1: float, c2: Vector2, r2: float) -> Contact | None:
    """2 つの円の接触情報。重なっていなければ None。"""
    offset = c2 - c1
    distance = offset.length()
    if distance >= r1 + r2:
        return None
    normal = offset / distance if distance > EPSILON else Vector2(1, 0)  # 中心が一致したら向きは決められない
    return normal, r1 + r2 - distance


def aabbs_overlap(a: AABB, b: AABB) -> bool:
    """x 方向と y 方向の両方で区間が重なっていれば、長方形どうしが重なっている。"""
    return a.left < b.right and b.left < a.right and a.top < b.bottom and b.top < a.bottom


def aabb_contact(a: AABB, b: AABB) -> Contact | None:
    """2 つの長方形の接触情報。めり込みが浅い方の軸を押し戻す向きとする。"""
    overlap_x = min(a.right, b.right) - max(a.left, b.left)
    overlap_y = min(a.bottom, b.bottom) - max(a.top, b.top)
    if overlap_x <= 0 or overlap_y <= 0:
        return None
    d = b.center - a.center
    if overlap_x < overlap_y:
        return Vector2(1 if d.x >= 0 else -1, 0), overlap_x
    return Vector2(0, 1 if d.y >= 0 else -1), overlap_y


def closest_point_on_aabb(p: Vector2, box: AABB) -> Vector2:
    """長方形の上（内部を含む）で、点 p に最も近い点。各成分を範囲に収めるだけで求まる。"""
    return Vector2(min(max(p.x, box.left), box.right), min(max(p.y, box.top), box.bottom))


def circle_aabb_contact(center: Vector2, radius: float, box: AABB) -> Contact | None:
    """長方形から円への接触情報（法線は長方形から円へ向かう）。"""
    closest = closest_point_on_aabb(center, box)
    offset = center - closest
    distance_sq = offset.length_squared()
    if distance_sq > EPSILON:
        if distance_sq >= radius * radius:
            return None
        distance = math.sqrt(distance_sq)
        return offset / distance, radius - distance
    # 円の中心が長方形の内部にある: 最も近い辺から外へ押し出す
    c, h = box.center, box.half_size
    dx = h.x - abs(center.x - c.x)
    dy = h.y - abs(center.y - c.y)
    if dx < dy:
        return Vector2(1 if center.x >= c.x else -1, 0), dx + radius
    return Vector2(0, 1 if center.y >= c.y else -1), dy + radius


def closest_point_on_segment(p: Vector2, a: Vector2, b: Vector2) -> Vector2:
    """線分 ab の上で、点 p に最も近い点。"""
    ab = b - a
    length_sq = ab.length_squared()
    if length_sq < EPSILON:
        return Vector2(a)
    t = max(0.0, min(1.0, (p - a).dot(ab) / length_sq))  # p を直線 ab に射影した位置の割合
    return a + ab * t


# --- レイ（半直線）と線分 ---

def ray_circle(origin: Vector2, direction: Vector2, center: Vector2, radius: float) -> float | None:
    """点 origin + t * direction（t >= 0）が初めて円に触れる t。当たらなければ None。

    |origin + t d - center|^2 = r^2 を t の 2 次方程式として解く。
    direction の長さが 1 なら t は距離になり、移動量なら t = 1 が移動の終点になる。
    """
    m = origin - center
    a = direction.dot(direction)
    b = m.dot(direction)
    c = m.dot(m) - radius * radius
    if c <= 0:
        return 0.0  # 始点がすでに円の中にある
    discriminant = b * b - a * c
    if b > 0 or discriminant < 0:
        return None  # 円から遠ざかっている、または直線が円を通らない
    return (-b - math.sqrt(discriminant)) / a


def ray_aabb(origin: Vector2, direction: Vector2, box: AABB) -> float | None:
    """点 origin + t * direction（t >= 0）が初めて長方形に触れる t（スラブ法）。当たらなければ None。"""
    t_enter, t_exit = 0.0, math.inf
    for o, d, lo, hi in ((origin.x, direction.x, box.left, box.right), (origin.y, direction.y, box.top, box.bottom)):
        if abs(d) < EPSILON:
            if o < lo or o > hi:
                return None  # この軸に平行で、範囲の外を通る
            continue
        t1, t2 = (lo - o) / d, (hi - o) / d
        t_enter = max(t_enter, min(t1, t2))  # すべての軸で範囲に入った時刻
        t_exit = min(t_exit, max(t1, t2))  # どれか 1 つの軸で範囲から出た時刻
        if t_enter > t_exit:
            return None
    return t_enter


def sweep_circle_circle(p: Vector2, motion: Vector2, r: float, q: Vector2, rq: float) -> float | None:
    """半径 r の円が p から p + motion まで動くとき、静止した円（中心 q、半径 rq）に初めて触れる割合（0～1）。

    動く円を点に縮め、止まっている円の半径を r + rq に広げれば、レイと円の判定になる。
    """
    t = ray_circle(p, motion, q, r + rq)
    if t is None or t > 1:
        return None
    return t


# --- 凸多角形（分離軸定理） ---

def polygon_axes(polygon: list[Vector2]) -> list[Vector2]:
    """多角形の各辺の法線（単位ベクトル）。"""
    axes = []
    for i, a in enumerate(polygon):
        edge = polygon[(i + 1) % len(polygon)] - a
        axes.append(Vector2(-edge.y, edge.x).normalize())
    return axes


def project_polygon(polygon: list[Vector2], axis: Vector2) -> tuple[float, float]:
    """多角形を軸に射影したときの区間（最小値, 最大値）。"""
    values = [p.dot(axis) for p in polygon]
    return min(values), max(values)


def polygon_contact(a: list[Vector2], b: list[Vector2]) -> Contact | None:
    """2 つの凸多角形の接触情報（分離軸定理）。どれか 1 つの軸で影が離れていれば、重なっていない。"""
    best_depth = math.inf
    best_axis = Vector2()
    for axis in polygon_axes(a) + polygon_axes(b):
        min_a, max_a = project_polygon(a, axis)
        min_b, max_b = project_polygon(b, axis)
        depth = min(max_a, max_b) - max(min_a, min_b)
        if depth <= 0:
            return None  # 分離軸が見つかった
        if depth < best_depth:
            best_depth, best_axis = depth, axis
    center_a = sum(a, Vector2()) / len(a)
    center_b = sum(b, Vector2()) / len(b)
    if best_axis.dot(center_b - center_a) < 0:
        best_axis = -best_axis  # a から b へ向かう向きにそろえる
    return best_axis, best_depth


# --- タイルマップ ---

def tiles_overlapping(box: AABB, tile_size: float) -> tuple[range, range]:
    """長方形が重なっているタイルの列番号と行番号の範囲。右端・下端ちょうどのタイルは含めない。"""
    first_col = math.floor(box.left / tile_size)
    last_col = math.ceil(box.right / tile_size) - 1
    first_row = math.floor(box.top / tile_size)
    last_row = math.ceil(box.bottom / tile_size) - 1
    return range(first_col, last_col + 1), range(first_row, last_row + 1)
