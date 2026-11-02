"""第 8 章「文法と成長による形状」: L-system とタートルグラフィックス。

* lsystem_steps.png: 書き換えを繰り返すと植物の形が育っていく様子
* lsystem_plants.png: 規則と角度の異なる 6 種類の 2 次元の植物
* lsystem_stochastic.png: 確率的 L-system でシードだけを変えた植物
* lsystem_tree3d.png: 3 次元のタートルで作った木（枝を円錐台のメッシュにした）
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib
from mesh import Mesh
from meshgen import combine, draw_faces, frame_cylinder, shaded_colors, uv_sphere

# 規則の右辺。文字列なら決定的な規則、(確率, 文字列) の列なら確率的な規則。
Rule = str | Sequence[tuple[float, str]]


def rewrite(axiom: str, rules: Mapping[str, Rule], iterations: int, seed: int = 0) -> str:
    """L-system の書き換え。各世代で、すべての文字を同時に規則の右辺に置き換える。

    規則の無い文字（+ - [ ] など）はそのまま残す。確率的な規則は、乱数で右辺を 1 つ選ぶ。
    """
    rng = np.random.default_rng(seed)
    text = axiom
    for _ in range(iterations):
        pieces = []
        for symbol in text:
            rule = rules.get(symbol)
            if rule is None:
                pieces.append(symbol)
            elif isinstance(rule, str):
                pieces.append(rule)
            else:
                weights = np.array([weight for weight, _ in rule])
                choice = int(rng.choice(len(rule), p=weights / weights.sum()))
                pieces.append(rule[choice][1])
        text = "".join(pieces)
    return text


def turtle2d(text: str, angle: float, step: float = 1.0, heading: float = 90.0) -> tuple[FloatArray, FloatArray]:
    """2 次元のタートルグラフィックス。文字列を命令として読み、亀が描いた線分を返す。

    F: 前に進んで線を引く、f: 線を引かずに進む、+: 左に angle 度回る、-: 右に回る、
    [: 今の状態（位置と向き）をスタックに積む、]: スタックから状態を戻す。ほかの文字は無視する。
    戻り値は線分の両端 (N, 2, 2) と、各線分の入れ子の深さ（枝の太さに使う）。
    """
    x, y, direction = 0.0, 0.0, heading
    stack: list[tuple[float, float, float]] = []
    segments: list[tuple[tuple[float, float], tuple[float, float]]] = []
    depths: list[int] = []
    for symbol in text:
        if symbol in "Ff":
            nx = x + step * math.cos(math.radians(direction))
            ny = y + step * math.sin(math.radians(direction))
            if symbol == "F":
                segments.append(((x, y), (nx, ny)))
                depths.append(len(stack))
            x, y = nx, ny
        elif symbol == "+":
            direction += angle
        elif symbol == "-":
            direction -= angle
        elif symbol == "[":
            stack.append((x, y, direction))
        elif symbol == "]":
            x, y, direction = stack.pop()
    return np.array(segments, dtype=np.float64), np.array(depths, dtype=np.float64)


@dataclass
class Plant:
    """2 次元の植物の L-system（Prusinkiewicz と Lindenmayer の本の図 1.24 の例）。"""

    name: str
    axiom: str
    rules: dict[str, Rule]
    angle: float
    iterations: int


PLANTS = [
    Plant("(a) F→F[+F]F[-F]F", "F", {"F": "F[+F]F[-F]F"}, 25.7, 5),
    Plant("(b) F→F[+F]F[-F][F]", "F", {"F": "F[+F]F[-F][F]"}, 20.0, 5),
    Plant("(c) F→FF-[-F+F+F]+[+F-F-F]", "F", {"F": "FF-[-F+F+F]+[+F-F-F]"}, 22.5, 4),
    Plant("(d) X→F[+X]F[-X]+X", "X", {"X": "F[+X]F[-X]+X", "F": "FF"}, 20.0, 7),
    Plant("(e) X→F[+X][-X]FX", "X", {"X": "F[+X][-X]FX", "F": "FF"}, 25.7, 7),
    Plant("(f) X→F-[[X]+X]+F[+FX]-X", "X", {"X": "F-[[X]+X]+F[+FX]-X", "F": "FF"}, 22.5, 5),
]


def draw_segments(ax: object, segments: FloatArray, depths: FloatArray, color: str = "#3b5e2b",
                  base_width: float = 1.6) -> None:
    """線分を、入れ子が深い（先の）枝ほど細く描く。"""
    from matplotlib.collections import LineCollection

    widths = base_width * 0.75 ** depths
    collection = LineCollection(list(segments), linewidths=widths, colors=color, capstyle="round")
    ax.add_collection(collection)  # type: ignore[attr-defined]
    points = segments.reshape(-1, 2)
    low = points.min(axis=0)
    high = points.max(axis=0)
    margin = 0.03 * float((high - low).max())
    ax.set_xlim(low[0] - margin, high[0] + margin)  # type: ignore[attr-defined]
    ax.set_ylim(low[1] - margin, high[1] + margin)  # type: ignore[attr-defined]
    ax.set_aspect("equal")  # type: ignore[attr-defined]
    ax.set_axis_off()  # type: ignore[attr-defined]


def draw_steps(file_name: str) -> None:
    import matplotlib.pyplot as plt

    plant = PLANTS[0]
    figure, axes = plt.subplots(1, 5, figsize=(12, 3.6))
    for n, ax in enumerate(axes):
        text = rewrite(plant.axiom, plant.rules, n)
        segments, depths = turtle2d(text, plant.angle)
        draw_segments(ax, segments, depths)
        ax.set_title(f"{n} 世代（F が {text.count('F')} 個）", fontsize=10)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_plants(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 6, figsize=(13, 4.2))
    for ax, plant in zip(axes, PLANTS):
        text = rewrite(plant.axiom, plant.rules, plant.iterations)
        segments, depths = turtle2d(text, plant.angle)
        draw_segments(ax, segments, depths, base_width=1.0)
        ax.set_title(f"{plant.name}\n{plant.angle}°、{plant.iterations} 世代", fontsize=8)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


STOCHASTIC_RULES: dict[str, Rule] = {"F": [(0.33, "F[+F]F[-F]F"), (0.33, "F[+F]F"), (0.34, "F[-F]F")]}


def draw_stochastic(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(1, 6, figsize=(12, 3.6))
    for seed, ax in enumerate(axes):
        text = rewrite("F", STOCHASTIC_RULES, 5, seed=seed)
        segments, depths = turtle2d(text, 25.7)
        draw_segments(ax, segments, depths)
        ax.set_title(f"シード {seed}", fontsize=10)
    # 高さをそろえて大きさの違いが分かるようにする。
    top = max(ax.get_ylim()[1] for ax in axes)
    for ax in axes:
        ax.set_ylim(-1, top)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def rotate(vector: FloatArray, axis: FloatArray, degrees: float) -> FloatArray:
    """vector を単位ベクトル axis の周りに degrees 度回す（ロドリゲスの回転公式）。"""
    t = math.radians(degrees)
    result: FloatArray = (vector * math.cos(t) + np.cross(axis, vector) * math.sin(t)
                          + axis * np.dot(axis, vector) * (1.0 - math.cos(t)))
    return result


@dataclass
class Branch:
    """3 次元のタートルが描いた枝 1 本。"""

    start: FloatArray
    end: FloatArray
    radius: float


def turtle3d(text: str, angle: float, roll: float, length: float = 1.0, radius: float = 0.12,
             length_scale: float = 0.8, radius_scale: float = 0.65,
             jitter: float = 0.0, seed: int = 0) -> tuple[list[Branch], list[FloatArray]]:
    """3 次元のタートル。向き H（前）、L（左）、U（上）の 3 本のベクトルで姿勢を持つ。

    F: 前に進んで枝を作る、+ -: U の周りに回る（左右）、& ^: L の周りに回る（下・上を向く）、
    / \\: H の周りに回る（ひねる）、!: 以降の枝の長さと太さを縮める、[ ]: 状態の保存と復帰、
    A: 枝先（葉を付ける位置として記録する）。jitter を与えると、回転角に乱数のばらつきを加える。
    """
    rng = np.random.default_rng(seed)
    position = np.zeros(3)
    heading = np.array([0.0, 0.0, 1.0])
    left = np.array([-1.0, 0.0, 0.0])
    up = np.cross(heading, left)
    size = (length, radius)
    stack: list[tuple[FloatArray, FloatArray, FloatArray, FloatArray, tuple[float, float]]] = []
    branches: list[Branch] = []
    tips: list[FloatArray] = []

    def turn(degrees: float) -> float:
        return degrees + jitter * float(rng.normal())

    for symbol in text:
        if symbol == "F":
            end = position + heading * size[0]
            branches.append(Branch(position, end, size[1]))
            position = end
        elif symbol in "+-":
            a = turn(angle if symbol == "+" else -angle)
            heading, left = rotate(heading, up, a), rotate(left, up, a)
        elif symbol in "&^":
            a = turn(angle if symbol == "&" else -angle)
            heading, up = rotate(heading, left, a), rotate(up, left, a)
        elif symbol in "/\\":
            a = turn(roll if symbol == "/" else -roll)
            left, up = rotate(left, heading, a), rotate(up, heading, a)
        elif symbol == "!":
            size = (size[0] * length_scale, size[1] * radius_scale)
        elif symbol == "[":
            stack.append((position, heading, left, up, size))
        elif symbol == "]":
            position, heading, left, up, size = stack.pop()
        elif symbol == "A":
            tips.append(position)
    return branches, tips


TREE_AXIOM = "FFA"
TREE_RULES: dict[str, Rule] = {"A": "![&FA]/[&FA]/[&FA]"}


def tree_mesh(seed: int, iterations: int = 5, jitter: float = 8.0) -> tuple[Mesh, Mesh]:
    """3 次元の木の幹と枝のメッシュ、葉のメッシュを返す。"""
    text = rewrite(TREE_AXIOM, TREE_RULES, iterations)
    branches, tips = turtle3d(text, angle=32.0, roll=120.0, jitter=jitter, seed=seed)
    # 枝の先端を根元の 0.8 倍の太さにして、先細りに見せる。
    wood = combine([frame_cylinder(b.start, b.end, b.radius, b.radius * 0.8, segments=6) for b in branches])
    leaf = uv_sphere(0.18, 5, 3)
    leaves = combine([leaf.transformed(offset=tuple(tip)) for tip in tips])
    return wood, leaves


def draw_tree3d(file_name: str) -> None:
    import matplotlib.pyplot as plt

    from mesh import fit_view

    figure = plt.figure(figsize=(12, 4.6))
    settings = [(0, 0.0, "角度のばらつき 0°"), (1, 8.0, "ばらつき 8°（シード 1）"), (2, 8.0, "ばらつき 8°（シード 2）")]
    for k, (seed, jitter, title) in enumerate(settings):
        wood, leaves = tree_mesh(seed, jitter=jitter)
        ax = figure.add_subplot(1, 3, k + 1, projection="3d")
        both = combine([wood, leaves])
        colors = np.concatenate([np.tile([0.45, 0.32, 0.22], (len(wood.faces), 1)),
                                 np.tile([0.40, 0.65, 0.30], (len(leaves.faces), 1))])
        draw_faces(ax, both, shaded_colors(both.face_normals(), colors), linewidth=0.1)
        fit_view(ax, [both], elev=10.0)
        ax.set_box_aspect((1.0, 1.0, 1.0), zoom=1.3)
        ax.set_title(f"{title}、枝 {len(wood.faces) // 12} 本", fontsize=10)
    figure.subplots_adjust(wspace=0.0, left=0.0, right=1.0)
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_steps("lsystem_steps.png")
    draw_plants("lsystem_plants.png")
    draw_stochastic("lsystem_stochastic.png")
    draw_tree3d("lsystem_tree3d.png")


if __name__ == "__main__":
    main()
