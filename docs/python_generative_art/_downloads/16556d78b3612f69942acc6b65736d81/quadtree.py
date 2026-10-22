"""点を登録する四分木と、それを使った範囲探索。

四分木は、正方形の領域を 4 つの小さな正方形に分けることを繰り返す
木構造である。ここでは、1 つの正方形に入る点の数が上限
（``capacity``）を超えたときだけ、その正方形を 4 分割する。こうすると、
点の密な場所ほど細かく、疎な場所ほど粗く分割される。

ある円の中にある点を探すときは、円と重ならない正方形をその下の
子孫ごと調べずに済ませられるため、点の密度に偏りがあっても、調べる
点の数を抑えられる。
"""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

from neighbor_search import noise_weighted_points


class QuadTree:
    """正方形の領域 1 つを表す四分木のノード。

    分割されていないノード（葉）は、領域内の点の番号を ``indices`` に
    持つ。分割されたノードは、点を持たず、4 つの子ノードを
    ``children`` に持つ。
    """

    def __init__(
        self,
        x0: float,
        y0: float,
        size: float,
        capacity: int = 4,
        max_depth: int = 12,
        depth: int = 0,
    ) -> None:
        self.x0: float = x0  # 左上の x 座標
        self.y0: float = y0  # 左上の y 座標
        self.size: float = size  # 1 辺の長さ
        self.capacity: int = capacity
        self.max_depth: int = max_depth
        self.depth: int = depth
        self.indices: list[int] = []
        self.children: list[QuadTree] = []

    def insert(self, index: int, points: np.ndarray) -> None:
        """番号 ``index`` の点 ``points[index]`` を登録する。

        点は、この領域の中にあるものとする。
        """
        if self.children:
            self._child_for(points[index]).insert(index, points)
            return

        self.indices.append(index)
        # 上限を超えたら 4 分割し、持っていた点を子ノードへ配り直す。
        # 同じ位置に点が重なっていると分割しても減らないため、深さにも
        # 上限を設ける。
        if len(self.indices) > self.capacity and self.depth < self.max_depth:
            half: float = self.size / 2
            self.children = [
                QuadTree(
                    self.x0 + dx * half,
                    self.y0 + dy * half,
                    half,
                    self.capacity,
                    self.max_depth,
                    self.depth + 1,
                )
                for dy in (0, 1)
                for dx in (0, 1)
            ]
            for i in self.indices:
                self._child_for(points[i]).insert(i, points)
            self.indices = []

    def _child_for(self, point: np.ndarray) -> QuadTree:
        """点 ``point`` が入る子ノードを返す。"""
        half: float = self.size / 2
        dx: int = 1 if point[0] >= self.x0 + half else 0
        dy: int = 1 if point[1] >= self.y0 + half else 0
        return self.children[dy * 2 + dx]

    def intersects_circle(self, cx: float, cy: float, radius: float) -> bool:
        """この正方形が、中心 (cx, cy)・半径 ``radius`` の円と重なるか。

        円の中心にもっとも近い正方形内の点を求め、そこまでの距離が
        半径以下かどうかで判定する。
        """
        nearest_x: float = min(max(cx, self.x0), self.x0 + self.size)
        nearest_y: float = min(max(cy, self.y0), self.y0 + self.size)
        return (nearest_x - cx) ** 2 + (nearest_y - cy) ** 2 <= radius**2

    def query_circle(
        self,
        cx: float,
        cy: float,
        radius: float,
        points: np.ndarray,
        visited: list[QuadTree] | None = None,
    ) -> list[int]:
        """円の中にある点の番号を返す。

        円と重ならないノードは、その子孫ごと調べずに飛ばす。
        ``visited`` にリストを渡すと、調べたノードがそこに追加される
        （図示用）。
        """
        if not self.intersects_circle(cx, cy, radius):
            return []
        if visited is not None:
            visited.append(self)
        if self.children:
            found: list[int] = []
            for child in self.children:
                found += child.query_circle(cx, cy, radius, points, visited)
            return found
        return [
            i
            for i in self.indices
            if (points[i, 0] - cx) ** 2 + (points[i, 1] - cy) ** 2 < radius**2
        ]

    def leaves(self) -> list[QuadTree]:
        """全ての葉ノードを返す。"""
        if not self.children:
            return [self]
        result: list[QuadTree] = []
        for child in self.children:
            result += child.leaves()
        return result


def build_quadtree(points: np.ndarray, size: float, capacity: int) -> QuadTree:
    """1 辺 ``size`` の正方形を根とする四分木を作り、全ての点を登録する。"""
    root: QuadTree = QuadTree(0.0, 0.0, size, capacity)
    for i in range(len(points)):
        root.insert(i, points)
    return root


def render_quadtree(
    root: QuadTree,
    points: np.ndarray,
    query: tuple[float, float, float],
    size: int,
) -> Image.Image:
    """四分木の葉の正方形と点を描き、範囲探索の様子を重ねる。

    探索で調べた葉を薄く塗り、探索の円と、見つかった点を強調する。
    """
    image: Image.Image = Image.new("RGB", (size, size), (14, 18, 32))
    draw: ImageDraw.ImageDraw = ImageDraw.Draw(image)
    cx, cy, radius = query

    visited: list[QuadTree] = []
    found: set[int] = set(root.query_circle(cx, cy, radius, points, visited))

    # 探索で調べた葉を薄く塗る。
    for node in visited:
        if not node.children:
            draw.rectangle(
                [node.x0, node.y0, node.x0 + node.size, node.y0 + node.size],
                fill=(40, 60, 90),
            )
    # 全ての葉の正方形の輪郭。
    for leaf in root.leaves():
        draw.rectangle(
            [leaf.x0, leaf.y0, leaf.x0 + leaf.size, leaf.y0 + leaf.size],
            outline=(70, 90, 130),
        )
    # 点。見つかった点は明るい色で少し大きく描く。
    for i, (x, y) in enumerate(points):
        if i in found:
            draw.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 140, 90))
        else:
            draw.rectangle([x - 1, y - 1, x, y], fill=(240, 200, 120))
    draw.ellipse(
        [cx - radius, cy - radius, cx + radius, cy + radius],
        outline=(255, 140, 90),
        width=2,
    )
    return image


def main() -> None:
    size: int = 800
    rng: np.random.Generator = np.random.default_rng(seed=0)
    points: np.ndarray = noise_weighted_points(4000, size, rng)
    root: QuadTree = build_quadtree(points, float(size), capacity=4)

    # 範囲探索の結果が、全ての点を調べた場合と一致することを確かめる。
    query: tuple[float, float, float] = (300.0, 360.0, 90.0)
    cx, cy, radius = query
    visited: list[QuadTree] = []
    by_tree: list[int] = root.query_circle(cx, cy, radius, points, visited)
    by_brute: np.ndarray = np.flatnonzero(
        (points[:, 0] - cx) ** 2 + (points[:, 1] - cy) ** 2 < radius**2
    )
    checked: int = sum(len(node.indices) for node in visited)
    print(
        f"leaves: {len(root.leaves())}, found: {len(by_tree)}, "
        f"points checked: {checked} / {len(points)}, "
        f"same result: {sorted(by_tree) == by_brute.tolist()}"
    )

    render_quadtree(root, points, query, size).save("quadtree_points.png")


if __name__ == "__main__":
    main()
