"""本文の図を source/images に生成する。conf.py からビルドのたびに呼び出される。

シミュレーションの図は examples のサンプルコードの関数を import して計算するので、本文・コード・図の数値が一致する。
"""

from __future__ import annotations

import math
import os
import random
import sys
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon, Rectangle, Wedge  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / 'examples'
OUT = ROOT / 'source' / 'images'

os.environ.setdefault('PYGAME_HIDE_SUPPORT_PROMPT', '1')
sys.path.insert(0, str(EXAMPLES))

from pygame import Vector2  # noqa: E402

import curves  # noqa: E402
import easing  # noqa: E402
import integrators  # noqa: E402
import jump  # noqa: E402
import noise  # noqa: E402
import platformer  # noqa: E402
import random_tools  # noqa: E402
import rope  # noqa: E402
import spring  # noqa: E402

BLUE = '#3b75c4'
ORANGE = '#e8862a'
GREEN = '#3a9a5b'
RED = '#cc3d3d'
PURPLE = '#7d5ab5'
GRAY = '#888888'
LIGHT = '#dddddd'


def _select_font(candidates: list[str]) -> str:
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in installed:
            return name
    return 'sans-serif'


plt.rcParams.update({
    'font.family': _select_font(['Meiryo', 'Yu Gothic', 'Noto Sans JP']),
    'font.size': 10,
    'axes.grid': True,
    'grid.color': '#e6e6e6',
    'axes.axisbelow': True,
    'figure.dpi': 110,
    'savefig.dpi': 110,
    'savefig.bbox': 'tight',
    'axes.unicode_minus': False,
})

FIGURES: dict[str, Callable[[], None]] = {}


def figure(name: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
    def register(func: Callable[[], None]) -> Callable[[], None]:
        FIGURES[name] = func
        return func
    return register


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(OUT / name)
    plt.close(fig)


def arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], color: str = BLUE,
          label: str | None = None, label_offset: tuple[float, float] = (0, 0), width: float = 1.8,
          style: str = '-|>', linestyle: str = '-') -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle=style, mutation_scale=14, color=color, lw=width,
                                 linestyle=linestyle, shrinkA=0, shrinkB=0))
    if label:
        mx, my = (start[0] + end[0]) / 2 + label_offset[0], (start[1] + end[1]) / 2 + label_offset[1]
        ax.text(mx, my, label, color=color, ha='center', va='center', fontsize=11)


def plain(ax: Axes, xlim: tuple[float, float], ylim: tuple[float, float], grid: bool = True) -> None:
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.grid(grid)


# --- 第 2 章 ---

@figure('coords.png')
def fig_coords() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
    for ax, title, down in ((axes[0], '数学の座標系（y 軸が上向き）', False), (axes[1], '画面座標（y 軸が下向き）', True)):
        plain(ax, (-0.5, 6), (-0.5, 4.5))
        ax.set_title(title)
        arrow(ax, (0, 0), (5.5, 0), GRAY)
        arrow(ax, (0, 0), (0, 4.2), GRAY)
        ax.text(5.6, -0.3, 'x', fontsize=12)
        ax.text(-0.35, 4.1, 'y', fontsize=12)
        ax.plot([4], [3], 'o', color=ORANGE)
        ax.text(4.1, 3.15, '(4, 3)', fontsize=11)
        ax.text(0.1, 0.35 if down else -0.35, '原点（左上）' if down else '原点', fontsize=9)
        if down:
            ax.invert_yaxis()
            ax.text(0.2, 4.1, '下', fontsize=9, color=GRAY)
        ax.set_xticks(range(0, 6))
        ax.set_yticks(range(0, 5))
    save(fig, 'coords.png')


@figure('float_spacing.png')
def fig_float_spacing() -> None:
    import numpy as np
    xs = np.logspace(0, 9, 200)
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ax.loglog(xs, np.spacing(xs.astype(np.float32)), label='32 ビット浮動小数点数', color=ORANGE)
    ax.loglog(xs, np.spacing(xs), label='64 ビット浮動小数点数（Python の float）', color=BLUE)
    ax.axhline(1e-3, color=GRAY, ls='--', lw=1)
    ax.text(1.5, 1.6e-3, '1 mm（1 m を 1 とした場合）', color=GRAY, fontsize=9)
    ax.set_xlabel('値の大きさ（原点からの距離）')
    ax.set_ylabel('隣の表せる数との差')
    ax.legend(fontsize=9)
    save(fig, 'float_spacing.png')


# --- 第 3 章 ---

@figure('dt_compare.png')
def fig_dt_compare() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), sharey=True)
    colors = {30: RED, 60: BLUE, 144: GREEN}
    for fps, color in colors.items():
        t = [i / fps for i in range(fps + 1)]
        axes[0].plot(t, [4 * i for i in range(fps + 1)], color=color, label=f'{fps} FPS')
        axes[1].plot(t, [240 * ti for ti in t], color=color, label=f'{fps} FPS', lw=4 if fps == 30 else 1.5,
                     alpha=0.6 if fps == 30 else 1)
    axes[0].set_title('1 フレームに 4 ピクセル')
    axes[1].set_title('1 秒に 240 ピクセル（デルタタイムを掛ける）')
    for ax in axes:
        ax.set_xlabel('経過時間（秒）')
        ax.legend(fontsize=9)
    axes[0].set_ylabel('移動した距離（ピクセル）')
    save(fig, 'dt_compare.png')


@figure('interpolation.png')
def fig_interpolation() -> None:
    step = 1 / 15
    frame = 1 / 60
    fig, ax = plt.subplots(figsize=(7, 3.2))
    physics_t = [i * step for i in range(6)]
    ax.plot(physics_t, [300 * t for t in physics_t], 'o', color=ORANGE, ms=8, label='物理の更新（15 Hz）', zorder=3)
    frames = [i * frame for i in range(21)]
    latest = [300 * math.floor(t / step + 1e-9) * step for t in frames]
    interp = [300 * max(0.0, t - step) for t in frames]
    ax.step(frames, latest, where='post', color=ORANGE, alpha=0.6, label='最新の状態を描く（カクつく）')
    ax.plot(frames, interp, 's-', color=BLUE, ms=4, label='直前の 2 状態を補間して描く（1 ステップ遅れる）')
    ax.set_xlabel('時刻（秒）')
    ax.set_ylabel('描かれる位置')
    ax.legend(fontsize=9)
    save(fig, 'interpolation.png')


# --- 第 4 章 ---

@figure('vector_add.png')
def fig_vector_add() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
    a, b = (3.0, 1.0), (1.0, 2.0)
    ax = axes[0]
    plain(ax, (-0.5, 4.8), (-0.5, 3.6))
    ax.set_title('足し算: a + b')
    arrow(ax, (0, 0), a, BLUE, 'a', (0.1, -0.3))
    arrow(ax, a, (a[0] + b[0], a[1] + b[1]), ORANGE, 'b', (0.3, 0))
    arrow(ax, (0, 0), b, ORANGE, None, linestyle='--', width=1)
    arrow(ax, b, (a[0] + b[0], a[1] + b[1]), BLUE, None, linestyle='--', width=1)
    arrow(ax, (0, 0), (a[0] + b[0], a[1] + b[1]), GREEN, 'a + b', (-0.4, 0.3))
    ax = axes[1]
    plain(ax, (-0.5, 4.8), (-0.5, 3.6))
    ax.set_title('引き算: b − a は a の先から b の先へ')
    arrow(ax, (0, 0), a, BLUE, 'a', (0.1, -0.3))
    arrow(ax, (0, 0), b, ORANGE, 'b', (-0.3, 0.1))
    arrow(ax, a, b, GREEN, 'b − a', (0.3, 0.4))
    ax.plot(*a, 'o', color=BLUE)
    ax.plot(*b, 'o', color=ORANGE)
    ax.text(a[0] + 0.1, a[1] - 0.35, '自分', fontsize=9)
    ax.text(b[0] - 0.2, b[1] + 0.2, '相手', fontsize=9)
    save(fig, 'vector_add.png')


@figure('diagonal.png')
def fig_diagonal() -> None:
    fig, ax = plt.subplots(figsize=(4, 4))
    plain(ax, (-1.6, 1.6), (-1.6, 1.6))
    ax.add_patch(Circle((0, 0), 1, fill=False, color=GRAY, ls='--'))
    ax.add_patch(Rectangle((-1, -1), 2, 2, fill=False, color=LIGHT))
    for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        arrow(ax, (0, 0), (dx, dy), BLUE, width=1.4)
    arrow(ax, (0, 0), (1, 1), RED, width=1.6)
    s = 1 / math.sqrt(2)
    arrow(ax, (0, 0), (s, s), GREEN, width=2)
    ax.text(0.2, 1.3, '(1, 1) 長さ √2 ≒ 1.41', color=RED, fontsize=9, ha='center')
    ax.text(0.75, 0.35, '正規化\n長さ 1', color=GREEN, fontsize=9)
    save(fig, 'diagonal.png')


@figure('dot_product.png')
def fig_dot_product() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8))
    ax = axes[0]
    plain(ax, (-0.5, 4.5), (-0.6, 3))
    ax.set_title('射影: a の b 方向の成分')
    a, b = (2.5, 2.0), (4.0, 0.0)
    arrow(ax, (0, 0), b, ORANGE, 'b', (0.6, -0.25))
    arrow(ax, (0, 0), a, BLUE, 'a', (-0.25, 0.15))
    ax.plot([a[0], a[0]], [0, a[1]], ':', color=GRAY)
    ax.plot([0, a[0]], [0, 0], color=GREEN, lw=4, alpha=0.6)
    ax.text(1.25, -0.35, '|a| cos θ', color=GREEN, ha='center')
    ax.add_patch(Wedge((0, 0), 0.7, 0, math.degrees(math.atan2(a[1], a[0])), fill=False, color=GRAY))
    ax.text(0.8, 0.25, 'θ', fontsize=11)
    ax = axes[1]
    plain(ax, (-3, 3), (-2.6, 2.6), grid=False)
    ax.set_title('向いている方向 f との内積の符号')
    ax.add_patch(Rectangle((0, -2.6), 3, 5.2, color=GREEN, alpha=0.12))
    ax.add_patch(Rectangle((-3, -2.6), 3, 5.2, color=RED, alpha=0.08))
    half = 35
    ax.add_patch(Wedge((0, 0), 2.4, -half, half, color=BLUE, alpha=0.25))
    arrow(ax, (0, 0), (1.2, 0), BLUE, None, width=2.4)
    ax.text(1.2, 0.25, 'f', color=BLUE, fontsize=12)
    ax.text(1.6, 1.9, '前方: f・d > 0', color=GREEN, fontsize=9)
    ax.text(-2.8, 1.9, '後方: f・d < 0', color=RED, fontsize=9)
    ax.text(1.3, -1.0, '視界:\n(f・d) / |d| ≥ cos 35°', color=BLUE, fontsize=9)
    ax.plot([0, 0], [-2.6, 2.6], color=GRAY, lw=1)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'dot_product.png')


@figure('cross_sign.png')
def fig_cross_sign() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6))
    for ax, down in ((axes[0], False), (axes[1], True)):
        plain(ax, (-2.2, 2.2), (-2.2, 2.2), grid=False)
        arrow(ax, (0, 0), (1.6, 0), BLUE, None, width=2.4)
        ax.text(1.65, 0.12, 'a', color=BLUE, fontsize=12)
        arrow(ax, (0, 0), (0.8, 1.4), GREEN, None)
        ax.text(0.85, 1.5, 'b', color=GREEN, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        if down:
            ax.invert_yaxis()
            ax.set_title('画面座標（y 軸が下向き）')
            ax.text(-2.0, 1.9, 'a × b > 0 なら b は a の右', fontsize=9, color=RED)
        else:
            ax.set_title('数学の座標系（y 軸が上向き）')
            ax.text(-2.0, -1.9, 'a × b > 0 なら b は a の左', fontsize=9, color=RED)
        ax.add_patch(Wedge((0, 0), 0.6, 0, 60, fill=False, color=GRAY))
    save(fig, 'cross_sign.png')


@figure('reflection.png')
def fig_reflection() -> None:
    fig, ax = plt.subplots(figsize=(6, 3.4))
    plain(ax, (-3.8, 3.8), (-0.6, 2.8), grid=False)
    ax.plot([-3, 3], [0, 0], color='black', lw=2)
    ax.add_patch(Rectangle((-3, -0.6), 6, 0.6, color=LIGHT))
    v = (2.0, -2.0)
    start = (-2.0, 2.0)
    arrow(ax, start, (0, 0), BLUE, 'v（入射）', (0.6, 0.4))
    arrow(ax, (0, 0), (2.0, 2.0), GREEN, 'r = v − 2(v・n)n', (1.5, -0.3))
    arrow(ax, (0, 0), (0, 1.2), GRAY, None)
    ax.text(0.1, 1.25, 'n（法線、長さ 1）', color=GRAY, fontsize=9)
    arrow(ax, (-2, 2), (-2, 0), ORANGE, None, linestyle='--', width=1.2)
    ax.text(-2.1, 0.9, '(v・n)n', color=ORANGE, fontsize=9, ha='right')
    ax.plot([-2, 0], [0, 0], color=PURPLE, lw=3, alpha=0.6)
    ax.text(-1.0, -0.35, '接線方向の成分（そのまま）', color=PURPLE, fontsize=9, ha='center')
    del v
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'reflection.png')


# --- 第 5 章 ---

@figure('unit_circle.png')
def fig_unit_circle() -> None:
    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    plain(ax, (-1.4, 1.4), (-1.4, 1.4))
    ax.add_patch(Circle((0, 0), 1, fill=False, color=GRAY))
    theta = math.radians(40)
    p = (math.cos(theta), math.sin(theta))
    arrow(ax, (0, 0), p, BLUE, None)
    ax.plot([p[0], p[0]], [0, p[1]], color=ORANGE, lw=2)
    ax.plot([0, p[0]], [0, 0], color=GREEN, lw=2)
    ax.text(p[0] / 2, -0.12, 'cos θ', color=GREEN, ha='center')
    ax.text(p[0] + 0.05, p[1] / 2, 'sin θ', color=ORANGE)
    ax.text(p[0] + 0.05, p[1] + 0.07, '(cos θ, sin θ)', fontsize=9)
    ax.add_patch(Wedge((0, 0), 0.3, 0, 40, fill=False, color=GRAY))
    ax.text(0.33, 0.1, 'θ', fontsize=11)
    ax.text(0.9, -0.95, '半径 1', fontsize=9, color=GRAY)
    save(fig, 'unit_circle.png')


@figure('atan2.png')
def fig_atan2() -> None:
    fig, ax = plt.subplots(figsize=(6, 4.2))
    plain(ax, (-3.4, 3.4), (-2.0, 2.0))
    points = [(1.5, 1.0), (-1.5, 1.0), (-1.5, -1.0), (1.5, -1.0)]
    colors = [BLUE, GREEN, ORANGE, PURPLE]
    for (x, y), color in zip(points, colors):
        arrow(ax, (0, 0), (x, y), color, None)
        a2 = math.degrees(math.atan2(y, x))
        a1 = math.degrees(math.atan(y / x))
        ax.text(x + (0.1 if x > 0 else -0.1), y + (0.15 if y > 0 else -0.25),
                f'({x:g}, {y:g})\natan2: {a2:.0f}°\natan(y/x): {a1:.0f}°',
                fontsize=8, color=color, ha='left' if x > 0 else 'right')
    ax.set_title('atan(y/x) では、反対向きのベクトルが同じ角度になる', fontsize=10)
    save(fig, 'atan2.png')


@figure('rotation.png')
def fig_rotation() -> None:
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    plain(ax, (-1.3, 2.6), (-0.4, 2.4))
    theta = math.radians(35)
    c, s = math.cos(theta), math.sin(theta)
    p = (2.0, 0.6)
    q = (p[0] * c - p[1] * s, p[0] * s + p[1] * c)
    arrow(ax, (0, 0), (1, 0), GRAY, None, width=1)
    arrow(ax, (0, 0), (0, 1), GRAY, None, width=1)
    arrow(ax, (0, 0), (c, s), GREEN, None, width=1.4)
    arrow(ax, (0, 0), (-s, c), GREEN, None, width=1.4)
    ax.text(c + 0.03, s - 0.15, '(cos θ, sin θ)', color=GREEN, fontsize=8)
    ax.text(-s - 0.55, c + 0.07, '(−sin θ, cos θ)', color=GREEN, fontsize=8)
    ax.plot(*p, 'o', color=BLUE)
    ax.plot(*q, 'o', color=ORANGE)
    ax.text(p[0] + 0.05, p[1] - 0.2, '(x, y)', color=BLUE)
    ax.text(q[0] + 0.05, q[1] + 0.05, "(x', y')", color=ORANGE)
    ax.add_patch(Wedge((0, 0), 2.088, math.degrees(math.atan2(p[1], p[0])), math.degrees(math.atan2(q[1], q[0])),
                       fill=False, color=GRAY, ls='--'))
    ax.add_patch(Wedge((0, 0), 0.4, 0, 35, fill=False, color=GRAY))
    ax.text(0.42, 0.1, 'θ', fontsize=11)
    save(fig, 'rotation.png')


@figure('angle_wrap.png')
def fig_angle_wrap() -> None:
    fig, ax = plt.subplots(figsize=(4.4, 4.2))
    plain(ax, (-1.5, 1.5), (-1.4, 1.5), grid=False)
    ax.add_patch(Circle((0, 0), 1, fill=False, color=LIGHT))
    a, b = 170, -170
    for ang, color, label in ((a, BLUE, '今: 170°'), (b, ORANGE, '目標: −170°')):
        r = math.radians(ang)
        arrow(ax, (0, 0), (math.cos(r), math.sin(r)), color, None)
        dy = 0.12 if ang > 0 else -0.18
        ax.text(1.12 * math.cos(r) - 0.3, 1.12 * math.sin(r) + dy, label, color=color, fontsize=9)
    ax.add_patch(Arc((0, 0), 1.0, 1.0, theta1=-170, theta2=170, color=RED, ls='--'))
    ax.add_patch(Arc((0, 0), 1.6, 1.6, theta1=170, theta2=190, color=GREEN, lw=2.5))
    ax.text(-0.2, -0.75, '単純な差: −340°（遠回り）', color=RED, fontsize=9)
    ax.text(-1.45, 0.6, '最短: +20°', color=GREEN, fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'angle_wrap.png')


# --- 第 6 章 ---

ARROW_SHAPE = [(0, -0.25), (1.0, -0.25), (1.0, -0.5), (1.6, 0), (1.0, 0.5), (1.0, 0.25), (0, 0.25)]


def transform_points(points: list[tuple[float, float]], angle: float, tx: float, ty: float,
                     rotate_first: bool) -> list[tuple[float, float]]:
    c, s = math.cos(angle), math.sin(angle)
    result = []
    for x, y in points:
        if rotate_first:
            x, y = x * c - y * s, x * s + y * c
            x, y = x + tx, y + ty
        else:
            x, y = x + tx, y + ty
            x, y = x * c - y * s, x * s + y * c
        result.append((x, y))
    return result


@figure('transform_order.png')
def fig_transform_order() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.8))
    angle = math.radians(90)
    for ax, rotate_first, title in ((axes[0], True, 'T・R: 回転してから平行移動'),
                                    (axes[1], False, 'R・T: 平行移動してから回転')):
        plain(ax, (-4, 4.2), (-1, 5.2))
        ax.set_title(title)
        ax.add_patch(Polygon(ARROW_SHAPE, color=GRAY, alpha=0.4))
        ax.add_patch(Polygon(transform_points(ARROW_SHAPE, angle, 3, 0, rotate_first), color=ORANGE, alpha=0.8))
        ax.plot(0, 0, 'k+', ms=10)
    axes[0].text(2.2, 2.2, '原点が (3, 0) へ', fontsize=9)
    axes[1].text(-3.8, 2.0, '原点を中心に\n回り込む', fontsize=9)
    save(fig, 'transform_order.png')


@figure('parent_child.png')
def fig_parent_child() -> None:
    import transform2d
    fig, ax = plt.subplots(figsize=(5.4, 4.2))
    plain(ax, (-1, 6), (-0.5, 5))
    base = transform2d.Mat3.translation(0.5, 0.2) @ transform2d.Mat3.rotation(math.radians(50))
    lengths = (3.0, 2.2)
    angles = (0.0, math.radians(-70))
    parent = base
    parent_length = 0.0
    colors = (BLUE, GREEN)
    for i, (angle, length) in enumerate(zip(angles, lengths)):
        world = parent @ transform2d.Mat3.translation(parent_length, 0) @ transform2d.Mat3.rotation(angle)
        corners = [world.apply(x, y) for x, y in ((0, -0.15), (length, -0.15), (length, 0.15), (0, 0.15))]
        ax.add_patch(Polygon(corners, color=colors[i], alpha=0.6))
        o = world.apply(0, 0)
        for (vx, vy), color in (((0.9, 0), RED), ((0, 0.9), GREEN)):
            e = world.apply(vx, vy)
            arrow(ax, o, e, color, None, width=1.2)
        ax.text(o[0] - 0.5, o[1] + 0.1, ('親', '子')[i], fontsize=10)
        parent, parent_length = world, length
    ax.text(3.3, 0.3, '赤: 各部品のローカル x 軸\n緑: ローカル y 軸', fontsize=8)
    save(fig, 'parent_child.png')


@figure('perspective.png')
def fig_perspective() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    ax.set_xlim(-0.5, 7.2)
    ax.set_ylim(-0.4, 2.6)
    ax.set_aspect('equal')
    ax.grid(False)
    ax.plot(0, 0, 'o', color='black')
    ax.text(-0.1, -0.3, 'カメラ', fontsize=9)
    ax.plot([0, 6.3], [0, 0], color=GRAY, lw=1)
    ax.text(6.0, -0.3, 'z（奥行き）', fontsize=9)
    f = 2.0
    ax.plot([f, f], [-0.2, 2.4], color=BLUE, lw=2)
    ax.text(f + 0.05, 2.35, '投影面', color=BLUE, fontsize=9)
    for z, y, color in ((4.0, 1.6, ORANGE), (6.0, 1.6, GREEN)):
        ax.plot([z, z], [0, y], color=color, lw=3)
        ax.plot([0, z], [0, y], ':', color=color)
        ax.plot(f, f * y / z, 'o', color=color)
        ax.text(z + 0.05, y / 2, f'z = {z:g}', color=color, fontsize=9)
    ax.annotate("y' = f・y / z", (f, 0.8), (2.6, 2.2), fontsize=10, arrowprops={'arrowstyle': '->'})
    ax.text(0.8, -0.3, 'f', fontsize=10, color=BLUE)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'perspective.png')


# --- 第 7 章 ---

@figure('slerp.png')
def fig_slerp() -> None:
    fig, ax = plt.subplots(figsize=(5.4, 4))
    plain(ax, (-1.3, 1.3), (-0.2, 1.3))
    ax.add_patch(Wedge((0, 0), 1, 0, 180, fill=False, color=LIGHT))
    a, b = (1.0, 0.0), (math.cos(math.radians(150)), math.sin(math.radians(150)))
    ax.plot([a[0], b[0]], [a[1], b[1]], ':', color=GRAY)
    for i in range(9):
        t = i / 8
        lx, ly = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
        n = math.hypot(lx, ly)
        ax.plot([0, lx / n], [0, ly / n], color=ORANGE, lw=1, alpha=0.7)
        ang = math.radians(150 * t)
        ax.plot(math.cos(ang), math.sin(ang), 'o', color=BLUE, ms=5)
        ax.plot(lx / n, ly / n, 's', color=ORANGE, ms=4)
    ax.plot([], [], 'o', color=BLUE, label='slerp（角度が等間隔）')
    ax.plot([], [], 's', color=ORANGE, label='線形補間して正規化（中央が速い）')
    ax.legend(fontsize=8, loc='upper center', bbox_to_anchor=(0.5, -0.08))
    save(fig, 'slerp.png')


# --- 第 8 章 ---

@figure('easing_curves.png')
def fig_easing_curves() -> None:
    fig, ax = plt.subplots(figsize=(6, 4))
    ts = [i / 200 for i in range(201)]
    for (name, func), color in zip(easing.EASINGS.items(), (GRAY, BLUE, ORANGE, GREEN, PURPLE)):
        ax.plot(ts, [func(t) for t in ts], label=name, color=color)
    ax.set_xlabel('時間の割合 t')
    ax.set_ylabel('進み具合')
    ax.legend(fontsize=9)
    save(fig, 'easing_curves.png')


@figure('damp_fps.png')
def fig_damp_fps() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.4), sharey=True)
    for fps, color in ((20, RED), (60, BLUE), (144, GREEN)):
        t, naive, damped = [0.0], [0.0], [0.0]
        for i in range(fps):
            t.append((i + 1) / fps)
            naive.append(easing.lerp(naive[-1], 100, 0.1))
            damped.append(easing.damp(damped[-1], 100, 6.0, 1 / fps))
        axes[0].plot(t, naive, color=color, label=f'{fps} FPS')
        axes[1].plot(t, damped, color=color, label=f'{fps} FPS', lw=4 if fps == 20 else 1.5,
                     alpha=0.5 if fps == 20 else 1)
    axes[0].set_title('毎フレーム残りの 10 % 近づく')
    axes[1].set_title('damp（rate = 6）')
    for ax in axes:
        ax.set_xlabel('経過時間（秒）')
        ax.legend(fontsize=9)
    axes[0].set_ylabel('位置（目標は 100）')
    save(fig, 'damp_fps.png')


@figure('bezier.png')
def fig_bezier() -> None:
    fig, ax = plt.subplots(figsize=(6, 3.8))
    p = [Vector2(0, 0), Vector2(1, 2.5), Vector2(4, 2.5), Vector2(5, 0)]
    plain(ax, (-0.5, 5.5), (-0.4, 2.9))
    pts = [curves.cubic_bezier(*p, i / 100) for i in range(101)]
    ax.plot([q.x for q in pts], [q.y for q in pts], color=BLUE, lw=2.5)
    ax.plot([q.x for q in p], [q.y for q in p], 'o--', color=GRAY)
    for i, q in enumerate(p):
        ax.text(q.x + 0.08, q.y + 0.1, f'P{i}', fontsize=10)
    t = 0.4
    a, b, c = (curves.lerp_point(p[i], p[i + 1], t) for i in range(3))
    d, e = curves.lerp_point(a, b, t), curves.lerp_point(b, c, t)
    f = curves.lerp_point(d, e, t)
    ax.plot([a.x, b.x, c.x], [a.y, b.y, c.y], 'o-', color=ORANGE, ms=5)
    ax.plot([d.x, e.x], [d.y, e.y], 'o-', color=GREEN, ms=5)
    ax.plot(f.x, f.y, 'o', color=RED, ms=8)
    ax.text(f.x + 0.1, f.y - 0.3, 'B(0.4)', color=RED)
    save(fig, 'bezier.png')


@figure('catmull_rom.png')
def fig_catmull_rom() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.6))
    points = [Vector2(p) for p in curves.WAYPOINTS]
    curve = curves.closed_spline(points)
    n = len(points)
    table = curves.ArcLengthTable(curve, n, curves.TABLE_SAMPLES)
    outline = [curve(n * i / 300) for i in range(301)]
    for ax, title in ((axes[0], 'u を等間隔に取る'), (axes[1], '弧長を等間隔に取る')):
        ax.plot([q.x for q in outline], [q.y for q in outline], color=LIGHT, lw=2)
        ax.plot([q.x for q in points], [q.y for q in points], 'o', color='black', ms=5)
        ax.set_title(title)
        ax.set_aspect('equal')
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks([])
    samples = 48
    uniform_u = [curve(n * i / samples) for i in range(samples)]
    uniform_s = [curve(table.u_at(table.total * i / samples)) for i in range(samples)]
    axes[0].plot([q.x for q in uniform_u], [q.y for q in uniform_u], '.', color=ORANGE, ms=7)
    axes[1].plot([q.x for q in uniform_s], [q.y for q in uniform_s], '.', color=BLUE, ms=7)
    save(fig, 'catmull_rom.png')


# --- 第 9 章 ---

@figure('circle_points.png')
def fig_circle_points() -> None:
    rng = random.Random(4)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.6))
    naive = []
    for _ in range(1500):
        a = rng.uniform(0, math.tau)
        r = rng.random()
        naive.append((r * math.cos(a), r * math.sin(a)))
    good = [random_tools.random_point_in_circle(rng, 1.0) for _ in range(1500)]
    for ax, pts, title, color in ((axes[0], naive, '半径を一様乱数にした場合（中心に偏る）', ORANGE),
                                  (axes[1], good, '半径を √(一様乱数) にした場合', BLUE)):
        plain(ax, (-1.1, 1.1), (-1.1, 1.1), grid=False)
        ax.add_patch(Circle((0, 0), 1, fill=False, color=GRAY))
        ax.plot([p[0] for p in pts], [p[1] for p in pts], '.', ms=2, color=color)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, 'circle_points.png')


@figure('gacha.png')
def fig_gacha() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.6))
    ns = list(range(0, 501))
    for p, color in ((0.01, BLUE), (0.03, ORANGE)):
        ax.plot(ns, [random_tools.probability_at_least_once(p, n) * 100 for n in ns], color=color,
                label=f'当たる確率 {p * 100:.0f} %')
    for target in (50, 90):
        ax.axhline(target, color=GRAY, ls='--', lw=1)
    n50 = random_tools.tries_needed(0.01, 0.5)
    n90 = random_tools.tries_needed(0.01, 0.9)
    ax.plot([n50, n90], [50, 90], 'o', color=BLUE)
    ax.text(n50 + 8, 45, f'{n50} 回', color=BLUE)
    ax.text(n90 + 8, 85, f'{n90} 回', color=BLUE)
    ax.set_xlabel('抽選の回数')
    ax.set_ylabel('少なくとも 1 回当たる確率（%）')
    ax.legend(fontsize=9, loc='lower right')
    save(fig, 'gacha.png')


@figure('noise.png')
def fig_noise() -> None:
    rng = random.Random(0)
    xs = [i / 50 for i in range(501)]
    fig, axes = plt.subplots(4, 1, figsize=(7, 6.4), sharex=True)
    axes[0].plot(xs, [rng.uniform(-1, 1) for _ in xs], color=GRAY, lw=0.8)
    axes[0].set_title('一様乱数をそのまま並べたもの', fontsize=9)
    axes[1].plot(xs, [noise.value_noise(x) for x in xs], color=ORANGE)
    axes[1].plot(range(11), [noise.value_noise(float(i)) for i in range(11)], 'o', color=ORANGE, ms=4)
    axes[1].set_title('バリューノイズ（格子点の値を滑らかに補間）', fontsize=9)
    axes[2].plot(xs, [noise.perlin_noise(x) for x in xs], color=BLUE)
    axes[2].plot(range(11), [0] * 11, 'o', color=BLUE, ms=4)
    axes[2].set_title('パーリンノイズ（格子点で 0、傾きが乱数）', fontsize=9)
    axes[3].plot(xs, [noise.fractal_noise(x, 5) for x in xs], color=GREEN)
    axes[3].set_title('フラクタルノイズ（パーリンノイズを 5 オクターブ重ねたもの）', fontsize=9)
    for ax in axes:
        ax.set_ylim(-1.1, 1.1)
    axes[3].set_xlabel('x')
    fig.tight_layout()
    save(fig, 'noise.png')


# --- 第 10 章 ---

def simulate_jump(variable_release: float | None, fall_scale: float) -> tuple[list[float], list[float]]:
    """jump.py の定数でジャンプの高さの時間変化を計算する（地面からの高さ、上向きを正）。"""
    dt = 1 / 240
    g, v0 = jump.GRAVITY, jump.JUMP_SPEED
    t, y, v = 0.0, 0.0, v0
    ts, ys = [0.0], [0.0]
    while True:
        if variable_release is not None and t >= variable_release:
            v = min(v, v0 * jump.JUMP_CUT_SCALE)
        gravity = g * (fall_scale if v < 0 else 1.0)
        y += v * dt - 0.5 * gravity * dt * dt
        v -= gravity * dt
        t += dt
        if y < 0:
            break
        ts.append(t)
        ys.append(y)
    return ts, ys


@figure('jump_arc.png')
def fig_jump_arc() -> None:
    fig, ax = plt.subplots(figsize=(6.6, 3.6))
    cases = ((None, 1.0, GRAY, '重力が一定（放物線）'),
             (None, jump.FALL_GRAVITY_SCALE, BLUE, f'下降中の重力を {jump.FALL_GRAVITY_SCALE:g} 倍'),
             (0.08, jump.FALL_GRAVITY_SCALE, ORANGE, '0.08 秒でボタンを離した場合'))
    for release, scale, color, label in cases:
        ts, ys = simulate_jump(release, scale)
        ax.plot(ts, ys, color=color, label=label)
    ax.axhline(jump.JUMP_HEIGHT, color=GREEN, ls='--', lw=1)
    ax.axvline(jump.TIME_TO_APEX, color=GREEN, ls=':', lw=1)
    ax.text(0.01, jump.JUMP_HEIGHT + 3, f'h = {jump.JUMP_HEIGHT:g} px', color=GREEN, fontsize=9)
    ax.text(jump.TIME_TO_APEX + 0.01, 5, f'T = {jump.TIME_TO_APEX:g} 秒', color=GREEN, fontsize=9)
    ax.set_xlabel('時間（秒）')
    ax.set_ylabel('高さ（ピクセル）')
    ax.set_ylim(-5, 150)
    ax.legend(fontsize=9, loc='upper right')
    save(fig, 'jump_arc.png')


@figure('run_velocity.png')
def fig_run_velocity() -> None:
    dt = 1 / 240
    t, v = 0.0, 0.0
    ts, vs = [0.0], [0.0]
    while t < 0.6:
        move = 1.0 if t < 0.35 else 0.0
        accel = jump.GROUND_ACCEL if move else jump.GROUND_DECEL
        v = jump.approach(v, move * jump.RUN_SPEED, accel * dt)
        t += dt
        ts.append(t)
        vs.append(v)
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(ts, vs, color=BLUE)
    ax.axvspan(0, 0.35, color=GREEN, alpha=0.08)
    ax.text(0.02, 20, '右キーを押している', fontsize=9, color=GREEN)
    ax.set_xlabel('時間（秒）')
    ax.set_ylabel('横方向の速度（px/s）')
    save(fig, 'run_velocity.png')


@figure('integrators.png')
def fig_integrators() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.4))
    colors = {'オイラー法': RED, '半陰的オイラー法': ORANGE, '速度ベルレ法': BLUE}
    dt = 1 / 20
    exact_t = [i / 200 for i in range(601)]
    axes[0].plot(exact_t, [math.cos(integrators.OMEGA * t) for t in exact_t], color=LIGHT, lw=5, label='正確な解')
    for name, stepper in integrators.STEPPERS.items():
        hist = integrators.simulate(stepper, integrators.spring_acceleration, 1.0, 0.0, dt, 3.0)
        axes[0].plot([h[0] for h in hist], [h[1] for h in hist], '.-', ms=3, lw=1, color=colors[name], label=name)
    axes[0].set_ylim(-3, 3)
    axes[0].set_title('ばねの単振動の位置（dt = 1/20 秒）')
    axes[0].set_xlabel('時間（秒）')
    axes[0].legend(fontsize=8, loc='lower left')
    e0 = integrators.spring_energy(1.0, 0.0)
    for name, stepper in integrators.STEPPERS.items():
        hist = integrators.simulate(stepper, integrators.spring_acceleration, 1.0, 0.0, 1 / 60, 10.0)
        axes[1].plot([h[0] for h in hist], [integrators.spring_energy(h[1], h[2]) / e0 for h in hist],
                     color=colors[name], label=name)
    axes[1].set_yscale('log')
    axes[1].set_title('エネルギー（最初を 1 とする、dt = 1/60 秒）')
    axes[1].set_xlabel('時間（秒）')
    axes[1].legend(fontsize=8)
    save(fig, 'integrators.png')


# --- 第 11 章 ---

@figure('overlap_tests.png')
def fig_overlap_tests() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    ax = axes[0]
    plain(ax, (-0.5, 5), (-0.5, 3.5), grid=False)
    ax.set_title('円と円: 中心間の距離 < r₁ + r₂', fontsize=9)
    ax.add_patch(Circle((1.2, 1.5), 1.1, fill=False, color=BLUE, lw=2))
    ax.add_patch(Circle((3.3, 1.7), 0.9, fill=False, color=ORANGE, lw=2))
    ax.plot([1.2, 3.3], [1.5, 1.7], 'k:', lw=1)
    ax.plot([1.2, 3.3], [1.5, 1.7], 'ko', ms=3)
    ax.text(2.2, 1.85, 'd', fontsize=11)
    ax = axes[1]
    plain(ax, (-0.5, 5), (-0.5, 3.5), grid=False)
    ax.set_title('長方形どうし: x と y の区間が両方重なる', fontsize=9)
    ax.add_patch(Rectangle((0.5, 0.8), 2.2, 1.6, fill=False, color=BLUE, lw=2))
    ax.add_patch(Rectangle((2.0, 1.6), 2.2, 1.4, fill=False, color=ORANGE, lw=2))
    ax.plot([0.5, 2.7], [0.1, 0.1], color=BLUE, lw=4, alpha=0.6)
    ax.plot([2.0, 4.2], [0.25, 0.25], color=ORANGE, lw=4, alpha=0.6)
    ax.plot([-0.2, -0.2], [0.8, 2.4], color=BLUE, lw=4, alpha=0.6)
    ax.plot([-0.05, -0.05], [1.6, 3.0], color=ORANGE, lw=4, alpha=0.6)
    ax = axes[2]
    plain(ax, (-0.5, 5), (-0.5, 3.5), grid=False)
    ax.set_title('円と長方形: 長方形上の最も近い点', fontsize=9)
    ax.add_patch(Rectangle((0.5, 0.5), 2.4, 1.6, fill=False, color=BLUE, lw=2))
    cx, cy = 3.7, 2.7
    ax.add_patch(Circle((cx, cy), 1.0, fill=False, color=ORANGE, lw=2))
    px, py = min(max(cx, 0.5), 2.9), min(max(cy, 0.5), 2.1)
    ax.plot([cx, px], [cy, py], 'k:', lw=1)
    ax.plot(px, py, 'o', color=RED)
    ax.plot(cx, cy, 'ko', ms=3)
    ax.text(px - 1.3, py + 0.2, '最も近い点', color=RED, fontsize=9)
    for a in axes:
        a.set_xticks([])
        a.set_yticks([])
    save(fig, 'overlap_tests.png')


@figure('sat.png')
def fig_sat() -> None:
    fig, ax = plt.subplots(figsize=(6, 4.2))
    plain(ax, (-1, 7.5), (-3.2, 4.4), grid=False)
    a = [(0.5, 0.5), (2.5, 0.2), (3.0, 2.0), (1.0, 2.6)]
    b = [(3.8, 1.6), (5.6, 2.2), (4.6, 3.8)]
    ax.add_patch(Polygon(a, fill=False, color=BLUE, lw=2))
    ax.add_patch(Polygon(b, fill=False, color=ORANGE, lw=2))
    edge = (b[0][0] - b[2][0], b[0][1] - b[2][1])
    n = (-edge[1], edge[0])
    ln = math.hypot(*n)
    axis = (n[0] / ln, n[1] / ln)
    origin = (-0.5, -0.2)
    ax.plot([origin[0] - axis[0] * 1, origin[0] + axis[0] * 7.5], [origin[1] - axis[1] * 1, origin[1] + axis[1] * 7.5],
            color=GRAY, lw=1)

    def proj(points: list[tuple[float, float]]) -> tuple[float, float]:
        values = [(p[0] - origin[0]) * axis[0] + (p[1] - origin[1]) * axis[1] for p in points]
        return min(values), max(values)

    for poly, color, off in ((a, BLUE, 0.0), (b, ORANGE, 0.0)):
        lo, hi = proj(poly)
        ax.plot([origin[0] + axis[0] * lo, origin[0] + axis[0] * hi], [origin[1] + axis[1] * lo + off,
                                                                       origin[1] + axis[1] * hi + off],
                color=color, lw=6, alpha=0.6)
        for p in poly:
            t = (p[0] - origin[0]) * axis[0] + (p[1] - origin[1]) * axis[1]
            ax.plot([p[0], origin[0] + axis[0] * t], [p[1], origin[1] + axis[1] * t], ':', color=color, lw=0.8)
    ax.text(3.6, -2.9, '分離軸（影が離れている）', fontsize=9, color=GRAY)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'sat.png')


@figure('ray_slab.png')
def fig_ray_slab() -> None:
    fig, ax = plt.subplots(figsize=(6, 3.8))
    plain(ax, (-0.5, 7), (-0.5, 4.5), grid=False)
    left, right, bottom, top = 3.0, 5.0, 1.5, 3.0
    ax.add_patch(Rectangle((left, bottom), right - left, top - bottom, color=BLUE, alpha=0.3))
    ax.axvspan(left, right, color=ORANGE, alpha=0.08)
    ax.axhspan(bottom, top, color=GREEN, alpha=0.08)
    o, d = (0.0, 0.3), (1.0, 0.45)
    ts = [(left - o[0]) / d[0], (right - o[0]) / d[0], (bottom - o[1]) / d[1], (top - o[1]) / d[1]]
    end = 6.8
    ax.plot([o[0], o[0] + d[0] * end], [o[1], o[1] + d[1] * end], color='black', lw=1.5)
    labels = ('x 方向に入る', 'x 方向から出る', 'y 方向に入る', 'y 方向から出る')
    colors = (ORANGE, ORANGE, GREEN, GREEN)
    for t, label, color in zip(ts, labels, colors):
        p = (o[0] + d[0] * t, o[1] + d[1] * t)
        ax.plot(*p, 'o', color=color)
        dx, dy = (0.1, -0.35) if color == ORANGE else (-1.6, 0.15)
        ax.text(p[0] + dx, p[1] + dy, label, fontsize=8, color=color)
    t_enter = max(min(ts[0], ts[1]), min(ts[2], ts[3]))
    t_exit = min(max(ts[0], ts[1]), max(ts[2], ts[3]))
    for t in (t_enter, t_exit):
        ax.plot(o[0] + d[0] * t, o[1] + d[1] * t, 'o', color=RED, ms=10, fillstyle='none', mew=2)
    ax.text(0.1, 4.0, '入る時刻の最大 ≤ 出る時刻の最小 なら当たる', fontsize=9, color=RED)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'ray_slab.png')


@figure('tunneling.png')
def fig_tunneling() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 2.6))
    for ax, swept in ((axes[0], False), (axes[1], True)):
        plain(ax, (-0.5, 10.5), (-1.2, 1.4), grid=False)
        ax.add_patch(Rectangle((4.6, -1.0), 0.4, 2.2, color=GRAY))
        for i, x in enumerate((1.0, 8.0)):
            ax.add_patch(Circle((x, 0), 0.4, color=BLUE, alpha=0.5 + 0.4 * i))
            ax.text(x, -0.85, ('前のステップ', '次のステップ')[i], ha='center', fontsize=8)
        if swept:
            ax.add_patch(Rectangle((1.0, -0.4), 7.0, 0.8, color=ORANGE, alpha=0.25))
            ax.add_patch(Circle((4.2, 0), 0.4, fill=False, color=RED, lw=2))
            ax.set_title('移動の経路全体で判定すると、衝突の時刻を求められる', fontsize=9)
        else:
            ax.set_title('離散的な判定: どちらの位置でも壁と重ならない', fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, 'tunneling.png')


@figure('grid.png')
def fig_grid() -> None:
    rng = random.Random(3)
    fig, ax = plt.subplots(figsize=(5, 5))
    plain(ax, (0, 8), (-0.8, 8), grid=False)
    for i in range(9):
        ax.plot([i, i], [0, 8], color=LIGHT, lw=1)
        ax.plot([0, 8], [i, i], color=LIGHT, lw=1)
    for _ in range(28):
        x, y, r = rng.uniform(0.3, 7.7), rng.uniform(0.3, 7.7), rng.uniform(0.15, 0.4)
        ax.add_patch(Circle((x, y), r, color=GRAY, alpha=0.6))
    ax.add_patch(Rectangle((3, 3), 2, 2, color=ORANGE, alpha=0.25))
    ax.add_patch(Circle((4.1, 3.8), 0.45, color=BLUE))
    ax.text(4.0, -0.5, '自分が重なるマス（橙）にいる物とだけ調べる', ha='center', fontsize=9, color=ORANGE)
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'grid.png')


# --- 第 12 章 ---

@figure('normal_tangent.png')
def fig_normal_tangent() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.4))
    for ax, e, title in ((axes[0], None, '衝突前の速度を分解する'), (axes[1], 0.5, '衝突後（反発係数 e = 0.5、摩擦なし）')):
        plain(ax, (-2.5, 3.0), (-1.6, 2.4), grid=False)
        ax.plot([-2.5, 3.0], [0, 0], color='black', lw=2)
        ax.add_patch(Rectangle((-2.5, -1.6), 5.5, 1.6, color=LIGHT))
        arrow(ax, (0, 0), (0, 0.9), GRAY, None, width=1)
        ax.text(0.1, 0.9, 'n', color=GRAY)
        if e is None:
            arrow(ax, (-1.6, 1.8), (0, 0), BLUE, None)
            ax.text(-1.2, 1.0, 'v', color=BLUE, fontsize=12)
            arrow(ax, (-1.6, 1.8), (-1.6, 0), ORANGE, None, linestyle='--', width=1.2)
            ax.text(-2.4, 0.8, '法線方向\nv・n', color=ORANGE, fontsize=8)
            arrow(ax, (-1.6, 0.03), (0, 0.03), GREEN, None, width=1.2)
            ax.text(-1.3, -0.4, '接線方向', color=GREEN, fontsize=8)
        else:
            arrow(ax, (0, 0), (1.6, 0.9), BLUE, None)
            ax.text(1.65, 0.95, "v'", color=BLUE, fontsize=12)
            arrow(ax, (1.6, 0), (1.6, 0.9), ORANGE, None, linestyle='--', width=1.2)
            ax.text(1.7, 0.35, '−e (v・n)', color=ORANGE, fontsize=8)
            arrow(ax, (0, 0.03), (1.6, 0.03), GREEN, None, width=1.2)
            ax.text(0.4, -0.4, '接線方向は変わらない', color=GREEN, fontsize=8)
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    save(fig, 'normal_tangent.png')


@figure('restitution.png')
def fig_restitution() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.2))
    for e, color in ((1.0, GRAY), (0.8, BLUE), (0.5, ORANGE)):
        y, v, t = 2.0, 0.0, 0.0
        ts, ys = [0.0], [y]
        dt = 1 / 1000
        while t < 4:
            v -= 9.8 * dt
            y += v * dt
            if y < 0:
                y, v = -y * e, -v * e
            t += dt
            ts.append(t)
            ys.append(y)
        ax.plot(ts, ys, color=color, label=f'e = {e:g}')
    ax.set_xlabel('時間（秒）')
    ax.set_ylabel('高さ（m）')
    ax.legend(fontsize=9)
    save(fig, 'restitution.png')


@figure('axis_separation.png')
def fig_axis_separation() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(9.6, 3.2))
    titles = ('1. x 方向だけ動かす', '2. x 方向のめり込みを戻す', '3. y 方向に動かして戻す')
    for ax, title in zip(axes, titles):
        plain(ax, (0, 4), (0, 3), grid=False)
        ax.invert_yaxis()
        for c, r in ((2, 2), (3, 2), (3, 1)):
            ax.add_patch(Rectangle((c, r), 1, 1, color='#4a5f8a'))
        ax.set_title(title, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    start = (1.0, 0.9)
    size = (0.8, 0.95)
    ax = axes[0]
    ax.add_patch(Rectangle(start, *size, fill=False, color=GRAY, ls='--'))
    ax.add_patch(Rectangle((start[0] + 1.6, start[1]), *size, color=ORANGE, alpha=0.6))
    arrow(ax, (start[0] + 0.4, start[1] + 0.45), (start[0] + 2.0, start[1] + 0.45), BLUE, None)
    ax = axes[1]
    ax.add_patch(Rectangle((3 - size[0], start[1]), *size, color=ORANGE, alpha=0.6))
    arrow(ax, (3.3, 1.35), (2.75, 1.35), RED, None)
    ax.text(1.9, 0.6, '壁の左端に合わせる', fontsize=8, color=RED)
    ax = axes[2]
    ax.add_patch(Rectangle((3 - size[0], start[1]), *size, fill=False, color=GRAY, ls='--'))
    ax.add_patch(Rectangle((3 - size[0], 2 - size[1]), *size, color=ORANGE, alpha=0.6))
    ax.text(1.0, 0.6, '床の上に合わせ、着地とする', fontsize=8, color=RED)
    save(fig, 'axis_separation.png')


# --- 第 13 章 ---

@figure('spring_response.png')
def fig_spring_response() -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    dt = 1 / 240
    for ratio, color in zip(spring.DAMPING_RATIOS, (RED, GREEN, BLUE)):
        k, c = spring.spring_coefficients(spring.FREQUENCY, ratio)
        x, v = Vector2(0, 0), Vector2(0, 0)
        ts, xs = [0.0], [0.0]
        for i in range(round(1.5 / dt)):
            x, v = spring.spring_step(x, v, Vector2(1, 0), k, c, dt)
            ts.append((i + 1) * dt)
            xs.append(x.x)
        ax.plot(ts, xs, color=color, label=f'減衰比 {ratio:g}')
    ax.axhline(1, color=GRAY, ls='--', lw=1)
    ax.set_xlabel('時間（秒）')
    ax.set_ylabel('位置（目標は 1）')
    ax.legend(fontsize=9)
    save(fig, 'spring_response.png')


@figure('rope_frames.png')
def fig_rope_frames() -> None:
    points, sticks = rope.make_rope()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_aspect('equal')
    ax.set_xlim(30, 620)
    ax.set_ylim(370, 50)
    shots = {0, 10, 20, 35, 60}
    colors = iter((LIGHT, '#bbbbbb', '#999999', '#666666', BLUE))
    for frame in range(61):
        if frame in shots:
            ax.plot([p.position.x for p in points], [p.position.y for p in points], '.-', color=next(colors), ms=3,
                    label=f'{frame} ステップ後')
        rope.verlet_step(points, rope.STEP)
        for _ in range(rope.ITERATIONS):
            for stick in sticks:
                rope.satisfy(stick)
    ax.plot(points[0].position.x, points[0].position.y, 'o', color=RED)
    ax.legend(fontsize=8, loc='upper left', bbox_to_anchor=(1.02, 1))
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, 'rope_frames.png')


# --- 第 15 章 ---

@figure('level_map.png')
def fig_level_map() -> None:
    """platformer.py のマップ全体を Pillow で描く。"""
    tile = 12
    rows = platformer.LEVEL
    image = Image.new('RGB', (len(rows[0]) * tile, len(rows) * tile), (24, 28, 44))
    draw = ImageDraw.Draw(image)
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            x, y = c * tile, r * tile
            if ch == '#':
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(70, 90, 130), outline=(50, 64, 96))
            elif ch == '^':
                draw.polygon([(x + 1, y + tile - 1), (x + tile / 2, y + 2), (x + tile - 2, y + tile - 1)],
                             fill=(220, 220, 230))
            elif ch == 'C':
                draw.ellipse((x + 3, y + 3, x + tile - 4, y + tile - 4), fill=(250, 210, 70))
            elif ch == 'G':
                draw.line((x + 3, y, x + 3, y + tile), fill=(230, 230, 230), width=2)
                draw.polygon([(x + 4, y), (x + tile - 1, y + 3), (x + 4, y + 6)], fill=(90, 230, 120))
            elif ch == 'P':
                draw.rectangle((x + 3, y + 1, x + tile - 4, y + tile - 1), fill=(240, 240, 240))
    image = image.resize((image.width * 2, image.height * 2), Image.Resampling.NEAREST)
    image.save(OUT / 'level_map.png')


def main(only_missing: bool = False) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, func in FIGURES.items():
        if only_missing and (OUT / name).exists():
            continue
        func()


if __name__ == '__main__':
    main()
