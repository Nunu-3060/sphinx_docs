"""第 4 章「パターンとマテリアル」: 座標の分割による規則パターンの図を作る。

* repeat.png: floor と fract で平面をセルに分け、セルごとに図形を描く仕組み
* regular.png: 縞・チェッカー・レンガ・六角形タイル
"""

from __future__ import annotations

import math

import numpy as np

from color import hex_to_rgb
from common import FloatArray, grid, output_dir, setup_matplotlib
from prng import random2
from texture import mix, show_panels, smoothstep

SIZE = 256
AA = 0.03  # 境界をぼかす幅（セルの大きさに対する比）。ギザギザ（エイリアシング）を抑える


def stripes(x: FloatArray, y: FloatArray, angle: float, duty: float = 0.5) -> FloatArray:
    """角度 angle [ラジアン] の向きに並ぶ縞。duty は 1 周期のうち明るい部分の割合。"""
    u = x * math.cos(angle) + y * math.sin(angle)  # 縞に直交する向きの座標
    local = u - np.floor(u)  # fract
    return smoothstep(duty + AA, duty - AA, local) * smoothstep(0.0, AA, local)


def checker(x: FloatArray, y: FloatArray) -> FloatArray:
    """チェッカー（市松模様）。セルの番号 floor(x) + floor(y) の偶奇で塗り分ける。"""
    result: FloatArray = np.mod(np.floor(x) + np.floor(y), 2.0)
    return result


def bricks(x: FloatArray, y: FloatArray, ratio: float = 2.0, mortar: float = 0.06) -> tuple[FloatArray, FloatArray]:
    """レンガ積み。(目地を 0、レンガを 1 とする値, レンガごとの乱数) を返す。

    ratio はレンガの横と縦の比。奇数段は半個ずらす。mortar は目地の太さ（段の高さに対する比）。
    """
    row = np.floor(y)
    u = x / ratio + 0.5 * np.mod(row, 2.0)  # 奇数段を半個ずらす
    column = np.floor(u)
    # セル内の座標を、段の高さを 1 とする長さに直す。
    local_x = (u - column) * ratio
    local_y = y - row
    edge = np.minimum(np.minimum(local_x, ratio - local_x), np.minimum(local_y, 1.0 - local_y))
    brick = smoothstep(mortar * 0.5, mortar * 0.5 + AA * 4, edge)
    return brick, random2(column.astype(np.int64), row.astype(np.int64), seed=3)


def hex_cells(x: FloatArray, y: FloatArray) -> tuple[FloatArray, FloatArray, FloatArray, FloatArray]:
    """六角形のタイル。(中心からの x, y のずれ, 中心の x, y) を返す。

    ずれた 2 組の長方形の格子（間隔 1 × √3）を重ね、近いほうの中心を選ぶと六角形の領域になる。
    """
    size = np.array([1.0, math.sqrt(3.0)])
    half = size * 0.5
    ax = np.mod(x, size[0]) - half[0]
    ay = np.mod(y, size[1]) - half[1]
    bx = np.mod(x - half[0], size[0]) - half[0]
    by = np.mod(y - half[1], size[1]) - half[1]
    use_a = ax * ax + ay * ay < bx * bx + by * by
    gx = np.where(use_a, ax, bx)
    gy = np.where(use_a, ay, by)
    return gx, gy, x - gx, y - gy


def hex_edge_distance(gx: FloatArray, gy: FloatArray) -> FloatArray:
    """六角形（頂点が上下を向く）の中心からの距離。辺の上で 0.5 になる。"""
    ux = np.abs(gx)
    uy = np.abs(gy)
    return np.maximum(ux, ux * 0.5 + uy * math.sqrt(3.0) * 0.5)


def draw_repeat(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=4.0)
    cell_x = np.floor(x)
    cell_y = np.floor(y)
    local_x = x - cell_x
    local_y = y - cell_y
    ids = random2(cell_x.astype(np.int64), cell_y.astype(np.int64), seed=1)
    cells = np.stack([0.25 + 0.6 * ids, 0.25 + 0.6 * random2(cell_x.astype(np.int64), cell_y.astype(np.int64), 2),
                      np.full_like(ids, 0.75)], axis=-1)
    local = np.stack([local_x, local_y, np.zeros_like(local_x)], axis=-1)
    # セル内の座標で円を描く。半径をセルの乱数で変える。
    radius = 0.2 + 0.25 * ids
    distance = np.hypot(local_x - 0.5, local_y - 0.5)
    circles = smoothstep(radius + AA, radius - AA, distance)
    images = [np.stack([x / 4.0, y / 4.0, np.zeros_like(x)], axis=-1), cells, local, circles]
    titles = ["座標 (x, y) を 4 倍", "floor: セルの番号ごとの乱数", "fract: セル内の座標", "セル内の座標で円を描く"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def draw_regular(file_name: str) -> None:
    x, y = grid(SIZE, SIZE, scale=8.0)
    striped = stripes(x, y, angle=math.radians(30.0), duty=0.35)

    checked = checker(x, y)

    brick_x, brick_y = grid(SIZE, SIZE, scale=7.0)
    brick, brick_id = bricks(brick_x, brick_y)
    brick_color = mix(hex_to_rgb("#9c3d2b"), hex_to_rgb("#c8734f"), brick_id)
    brick_image = mix(np.array(hex_to_rgb("#d8d0c4")), brick_color, brick)

    hex_x, hex_y = grid(SIZE, SIZE, scale=6.0)
    gx, gy, cx, cy = hex_cells(hex_x, hex_y)
    # 中心の座標をハッシュに入れるため、整数にそろえる（中心は 0.5 刻みに並ぶ）。
    hex_id = random2(np.rint(cx * 2).astype(np.int64), np.rint(cy * 2 / math.sqrt(3.0)).astype(np.int64), seed=5)
    tile = smoothstep(0.47, 0.45, hex_edge_distance(gx, gy))
    hex_color = mix(hex_to_rgb("#2a6f97"), hex_to_rgb("#a9d6e5"), hex_id)
    hex_image = mix(np.array(hex_to_rgb("#f2f2f2")), hex_color, tile)

    images = [striped, checked, brick_image, hex_image]
    titles = ["縞（30 度、明るい部分 35 %）", "チェッカー", "レンガ", "六角形タイル"]
    show_panels(images, titles, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_repeat("repeat.png")
    draw_regular("regular.png")


if __name__ == "__main__":
    main()
