"""第 8 章「文法と成長による形状」: 空間植民アルゴリズム（Runions ら、2007 年）による樹木。

* colonization_steps.png: 成長の途中経過（灰色の点は残っている誘引点）
* colonization_params.png: 樹冠の形と、影響距離・消滅距離による違い
* colonization.mp4: 成長の様子の動画（ffmpeg がある場合）
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field

import numpy as np
from numpy.typing import NDArray
from scipy.spatial import cKDTree

from common import FloatArray, IntArray, output_dir, save_figure, setup_matplotlib

BoolArray = NDArray[np.bool_]
Shape = Callable[[FloatArray], BoolArray]


@dataclass
class Tree:
    """成長中の木。節点の位置と、それぞれの親の番号（根は -1）を持つ。"""

    nodes: list[FloatArray] = field(default_factory=list)
    parents: list[int] = field(default_factory=list)

    def add(self, position: FloatArray, parent: int) -> None:
        self.nodes.append(position)
        self.parents.append(parent)


def crown_points(count: int, inside: Shape, low: FloatArray, high: FloatArray, seed: int) -> FloatArray:
    """樹冠の範囲（inside が真を返す領域）に、誘引点を一様にばらまく（棄却法）。"""
    rng = np.random.default_rng(seed)
    points: list[FloatArray] = []
    while sum(len(p) for p in points) < count:
        candidates = rng.uniform(low, high, (count, 2))
        points.append(candidates[inside(candidates)])
    return np.concatenate(points)[:count]


def ellipse(center: tuple[float, float], radii: tuple[float, float]) -> Shape:
    """楕円の内側かどうかを返す関数。"""
    def inside(p: FloatArray) -> BoolArray:
        result: BoolArray = ((p[:, 0] - center[0]) / radii[0]) ** 2 + ((p[:, 1] - center[1]) / radii[1]) ** 2 <= 1
        return result
    return inside


def colonize(attractors: FloatArray, influence: float, kill: float, step: float, max_iterations: int = 200,
             history: list[tuple[int, int]] | None = None) -> Tree:
    """空間植民アルゴリズム。

    1. 各誘引点について、影響距離 influence 以内で最も近い節点を探す。
    2. 誘引点に引かれた節点は、引いている誘引点への単位ベクトルの平均の向きへ、step だけ伸びた
       新しい節点を作る。
    3. 新しい節点から消滅距離 kill 以内に入った誘引点を取り除く。
    誘引点が無くなるか、伸びる節点が無くなるまで繰り返す。history にリストを渡すと、
    各反復の後の (節点の数, 残った誘引点の数) を追加する。
    """
    tree = Tree()
    tree.add(np.array([0.0, 0.0]), -1)
    remaining = attractors.copy()
    # 幹: 最初の節点が誘引点の影響範囲に入るまで、まっすぐ上へ伸ばす。
    while len(remaining) and np.min(np.linalg.norm(remaining - tree.nodes[-1], axis=1)) > influence:
        tree.add(tree.nodes[-1] + np.array([0.0, step]), len(tree.nodes) - 1)
    for _ in range(max_iterations):
        if len(remaining) == 0:
            break
        nodes = np.array(tree.nodes)
        query = cKDTree(nodes).query(remaining, distance_upper_bound=influence)
        distance: FloatArray = np.asarray(query[0])
        nearest: IntArray = np.asarray(query[1])
        attracted = np.isfinite(distance)
        if not attracted.any():
            break
        directions = remaining[attracted] - nodes[nearest[attracted]]
        directions /= np.linalg.norm(directions, axis=1, keepdims=True)
        total = np.zeros_like(nodes)
        np.add.at(total, nearest[attracted], directions)
        grown = 0
        existing = cKDTree(nodes)
        for index in np.unique(nearest[attracted]):
            length = np.linalg.norm(total[index])
            if length < 1e-9:  # 反対向きの誘引点が釣り合うと伸びる向きが決まらない
                continue
            position = nodes[index] + step * total[index] / length
            # 前の反復と同じ所に節点を作り続ける（誘引点が消えずに残る）のを防ぐ。
            if existing.query(position)[0] < 0.5 * step:
                continue
            tree.add(position, int(index))
            grown += 1
        if grown == 0:
            break
        close = cKDTree(np.array(tree.nodes)).query(remaining, distance_upper_bound=kill)[0]
        remaining = remaining[~np.isfinite(close)]
        if history is not None:
            history.append((len(tree.nodes), len(remaining)))
    return tree


def branch_radii(tree: Tree, tip_radius: float = 0.02, exponent: float = 2.0) -> FloatArray:
    """枝の太さ。先端を tip_radius とし、親の太さを r^γ = Σ (子の r^γ) で決める（γ = exponent）。

    γ = 2 は、枝分かれの前後で断面積の合計が変わらないことを意味する。
    """
    count = len(tree.nodes)
    power = np.zeros(count)
    has_child = np.zeros(count, dtype=bool)
    parents = tree.parents
    for index in range(1, count):
        has_child[parents[index]] = True
    power[~has_child] = tip_radius ** exponent
    # 子は親より後に追加されるので、番号の大きい方から親へ足し込めばよい。
    for index in range(count - 1, 0, -1):
        power[parents[index]] += power[index]
    result: FloatArray = power ** (1.0 / exponent)
    return result


def draw_tree(ax: object, tree: Tree, count: int | None = None, scale: float = 60.0,
              attractors: FloatArray | None = None) -> None:
    """木を描く。count を与えると、最初の count 個の節点までの段階を描く。"""
    from matplotlib.collections import LineCollection

    n = len(tree.nodes) if count is None else count
    partial = Tree(tree.nodes[:n], tree.parents[:n])
    radii = branch_radii(partial)
    nodes = np.array(partial.nodes)
    segments = [(nodes[partial.parents[i]], nodes[i]) for i in range(1, n)]
    widths = scale * radii[1:]
    if attractors is not None and len(attractors):
        ax.scatter(attractors[:, 0], attractors[:, 1], s=2, color="#bbbbbb")  # type: ignore[attr-defined]
    ax.add_collection(LineCollection(segments, linewidths=widths, colors="#5a4030",  # type: ignore[attr-defined]
                                     capstyle="round"))
    ax.set_aspect("equal")  # type: ignore[attr-defined]
    ax.set_axis_off()  # type: ignore[attr-defined]


def remaining_attractors(attractors: FloatArray, nodes: FloatArray, kill: float) -> FloatArray:
    """節点の集合 nodes に対して、まだ取り除かれていない誘引点。"""
    distance = cKDTree(nodes).query(attractors, distance_upper_bound=kill)[0]
    result: FloatArray = attractors[~np.isfinite(distance)]
    return result


CROWN = ellipse((0.0, 6.5), (4.0, 3.0))
LOW = np.array([-4.0, 3.5])
HIGH = np.array([4.0, 9.5])


def draw_steps(file_name: str) -> None:
    import matplotlib.pyplot as plt

    attractors = crown_points(600, CROWN, LOW, HIGH, seed=1)
    history: list[tuple[int, int]] = []
    tree = colonize(attractors, influence=1.5, kill=0.3, step=0.15, history=history)
    stages = [history[int(len(history) * f)][0] for f in (0.1, 0.25, 0.5)] + [len(tree.nodes)]
    figure, axes = plt.subplots(1, 4, figsize=(12, 3.8))
    for ax, count in zip(axes, stages):
        nodes = np.array(tree.nodes[:count])
        draw_tree(ax, tree, count, attractors=remaining_attractors(attractors, nodes, 0.3))
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-0.2, 10)
        ax.set_title(f"節点 {count} 個", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_params(file_name: str) -> None:
    import matplotlib.pyplot as plt

    def cone(p: FloatArray) -> BoolArray:
        result: BoolArray = (p[:, 1] > 3.0) & (np.abs(p[:, 0]) < (9.5 - p[:, 1]) * 0.6)
        return result

    def two_lobes(p: FloatArray) -> BoolArray:
        result: BoolArray = ellipse((-2.2, 6.5), (2.0, 2.2))(p) | ellipse((2.2, 7.0), (2.0, 2.2))(p)
        return result

    cases = [
        ("楕円の樹冠", CROWN, 1.5, 0.3, 600),
        ("円錐の樹冠", cone, 1.5, 0.3, 600),
        ("2 つに分かれた樹冠", two_lobes, 1.5, 0.3, 600),
        ("影響距離 4.0（楕円）", CROWN, 4.0, 0.3, 600),
        ("消滅距離 0.8（楕円）", CROWN, 1.5, 0.8, 600),
        ("誘引点 150 個（楕円）", CROWN, 1.5, 0.3, 150),
    ]
    figure, axes = plt.subplots(1, 6, figsize=(13, 3.6))
    for ax, (title, shape, influence, kill, count) in zip(axes, cases):
        attractors = crown_points(count, shape, LOW, HIGH, seed=1)
        tree = colonize(attractors, influence=influence, kill=kill, step=0.15)
        draw_tree(ax, tree, scale=45.0)
        ax.set_xlim(-4.5, 4.5)
        ax.set_ylim(-0.2, 10)
        ax.set_title(title, fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def write_video(file_name: str) -> None:
    from video import VideoWriter, find_ffmpeg

    if find_ffmpeg() is None:
        print("ffmpeg が見つからないので動画を作らない")
        return
    import matplotlib.pyplot as plt

    attractors = crown_points(600, CROWN, LOW, HIGH, seed=1)
    history: list[tuple[int, int]] = []
    tree = colonize(attractors, influence=1.5, kill=0.3, step=0.15, history=history)
    counts = [count for count, _ in history]
    counts = [counts[0]] * 10 + counts + [counts[-1]] * 30
    figure = plt.figure(figsize=(3.6, 3.6), dpi=100)
    with VideoWriter(output_dir(__file__) / file_name, 360, 360, fps=30) as writer:
        for count in counts:
            figure.clear()
            ax = figure.add_axes((0.0, 0.0, 1.0, 1.0))
            nodes = np.array(tree.nodes[:count])
            draw_tree(ax, tree, count, attractors=remaining_attractors(attractors, nodes, 0.3))
            ax.set_xlim(-5.0, 5.0)
            ax.set_ylim(-0.2, 9.8)
            figure.canvas.draw()
            frame = np.asarray(figure.canvas.buffer_rgba())[:, :, :3]  # type: ignore[attr-defined]
            writer.write(np.ascontiguousarray(frame))
    plt.close(figure)


def main() -> None:
    setup_matplotlib()
    draw_steps("colonization_steps.png")
    draw_params("colonization_params.png")
    write_video("colonization.mp4")


if __name__ == "__main__":
    main()
