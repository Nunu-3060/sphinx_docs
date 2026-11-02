"""第 12 章「プロシージャルアニメーション」: 逆運動学 FABRIK（Aristidou と Lasenby、2011 年）。

関節の位置の列 joints（根元から先端へ）を、先端が目標 target に届くように動かす。
各ボーン（隣り合う関節の間）の長さは変えない。2 次元でも 3 次元でも同じコードで動く。

ボーンが 2 本だけの鎖には、余弦定理による解析解 two_bone_ik も用意する。

* fabrik_iterations.png: 後ろ向き・前向きの往復で鎖が目標に近づく様子
* fabrik_convergence.png: 反復回数と、先端と目標の距離の関係
"""

from __future__ import annotations

import math

import numpy as np

from common import FloatArray, output_dir, save_figure, setup_matplotlib


def bone_lengths(joints: FloatArray) -> FloatArray:
    """隣り合う関節の間の長さ (N - 1,)。"""
    result: FloatArray = np.linalg.norm(np.diff(joints, axis=0), axis=1)
    return result


def _place(anchor: FloatArray, toward: FloatArray, length: float) -> FloatArray:
    """anchor から toward の方向に length だけ離れた点。"""
    direction = toward - anchor
    distance = float(np.linalg.norm(direction))
    if distance < 1e-12:
        return anchor.copy()
    result: FloatArray = anchor + direction * (length / distance)
    return result


def backward_pass(joints: FloatArray, lengths: FloatArray, target: FloatArray) -> FloatArray:
    """後ろ向きの処理: 先端を目標に置き、先端から根元へ向かって長さを保つように引き寄せる。"""
    p = joints.copy()
    p[-1] = target
    for i in range(len(p) - 2, -1, -1):
        p[i] = _place(p[i + 1], p[i], float(lengths[i]))
    return p


def forward_pass(joints: FloatArray, lengths: FloatArray, root: FloatArray) -> FloatArray:
    """前向きの処理: 根元を元の位置に戻し、根元から先端へ向かって長さを保つように引き寄せる。"""
    p = joints.copy()
    p[0] = root
    for i in range(len(p) - 1):
        p[i + 1] = _place(p[i], p[i + 1], float(lengths[i]))
    return p


def fabrik(
    joints: FloatArray, target: FloatArray, tolerance: float = 1e-3, max_iterations: int = 20
) -> tuple[FloatArray, int]:
    """FABRIK で先端を target に近づけた関節の位置と、使った反復回数を返す。"""
    lengths = bone_lengths(joints)
    root = joints[0].copy()
    if np.linalg.norm(target - root) >= lengths.sum():
        # 届かない場合: 目標の方向へまっすぐ伸ばすのが最も近い姿勢である。
        p = joints.copy()
        for i in range(len(p) - 1):
            p[i + 1] = _place(p[i], target, float(lengths[i]))
        return p, 0
    p = joints.copy()
    for iteration in range(1, max_iterations + 1):
        p = forward_pass(backward_pass(p, lengths, target), lengths, root)
        if np.linalg.norm(p[-1] - target) < tolerance:
            return p, iteration
    return p, max_iterations


def two_bone_ik(root: FloatArray, target: FloatArray, upper: float, lower: float, bend: float = 1.0) -> FloatArray:
    """ボーンが 2 本の鎖（腰・膝・足など）を余弦定理で解き、根元・中間・先端の 3 点を返す（2 次元）。

    bend は中間の関節を曲げる向きで、根元から目標を見て左なら 1、右なら -1。
    届かない目標には、目標の方向へまっすぐ伸ばす。
    """
    offset = target - root
    distance = float(np.linalg.norm(offset))
    u = offset / max(distance, 1e-12)
    d = min(max(distance, abs(upper - lower) + 1e-9), upper + lower)
    along = (upper * upper - lower * lower + d * d) / (2.0 * d)  # 根元から、中間の関節の足までの距離
    height = math.sqrt(max(upper * upper - along * along, 0.0))
    normal = np.array([-u[1], u[0]]) * bend
    middle = root + u * along + normal * height
    return np.stack([root, middle, root + u * d])


def initial_chain(count: int = 4, length: float = 1.2, turn: float = -0.5) -> FloatArray:
    """根元を原点に置き、右へ伸びながら関節ごとに角度 turn [rad] ずつ曲がる鎖。"""
    angles = np.arange(count) * turn
    steps = np.stack([np.cos(angles), np.sin(angles)], axis=1) * length
    return np.vstack([np.zeros((1, 2)), np.cumsum(steps, axis=0)])


def draw_iterations(file_name: str) -> None:
    import matplotlib.pyplot as plt

    joints = initial_chain()
    lengths = bone_lengths(joints)
    root = joints[0].copy()
    target = np.array([-1.0, 2.0])
    after_backward = backward_pass(joints, lengths, target)
    after_forward = forward_pass(after_backward, lengths, root)
    second = forward_pass(backward_pass(after_forward, lengths, target), lengths, root)
    final, iterations = fabrik(joints, target)
    panels = [
        ("初期の姿勢", joints, None),
        ("1 回目: 後ろ向き", after_backward, joints),
        ("1 回目: 前向き", after_forward, after_backward),
        ("2 回目の後", second, after_forward),
        (f"収束（{iterations} 回）", final, None),
    ]
    figure, axes = plt.subplots(1, 5, figsize=(14, 3.2))
    for ax, (title, chain, previous) in zip(axes, panels):
        if previous is not None:
            ax.plot(previous[:, 0], previous[:, 1], "-o", color="#bbbbbb", ms=4, lw=1.5)
        ax.plot(chain[:, 0], chain[:, 1], "-o", color="#4c72b0", ms=5, lw=2.5)
        ax.plot(*root, "s", color="black", ms=8)
        ax.plot(*target, "*", color="#dd8452", ms=14)
        ax.set_title(title, fontsize=11)
        ax.set_xlim(-2.0, 4.0)
        ax.set_ylim(-3.2, 2.8)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def draw_convergence(file_name: str) -> None:
    import matplotlib.pyplot as plt

    figure, ax = plt.subplots(figsize=(6, 3.6))
    for target in [(-1.0, 2.0), (1.0, 2.5), (-2.0, 1.0), (0.5, 0.2)]:
        p = initial_chain()
        lengths = bone_lengths(p)
        root = p[0].copy()
        goal = np.array(target)
        errors = [float(np.linalg.norm(p[-1] - goal))]
        for _ in range(15):
            p = forward_pass(backward_pass(p, lengths, goal), lengths, root)
            errors.append(float(np.linalg.norm(p[-1] - goal)))
        # 誤差が 0 になると対数の軸に描けないので、倍精度の丸め誤差程度の値で下を切る。
        ax.semilogy(range(len(errors)), np.maximum(errors, 1e-16), "-o", ms=3, label=f"目標 {target}")
    ax.set_xlabel("反復回数")
    ax.set_ylabel("先端と目標の距離")
    ax.grid(alpha=0.3, which="both")
    ax.legend(fontsize=9)
    figure.tight_layout()
    save_figure(figure, output_dir(__file__) / file_name)


def main() -> None:
    setup_matplotlib()
    draw_iterations("fabrik_iterations.png")
    draw_convergence("fabrik_convergence.png")


if __name__ == "__main__":
    main()
