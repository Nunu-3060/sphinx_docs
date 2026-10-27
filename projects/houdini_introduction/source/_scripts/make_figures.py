"""本文の図を matplotlib で描き、PNG で保存する。

conf.py からビルドのたびに実行される。単独で実行するときは、保存先の
ディレクトリを引数で渡す。

    python make_figures.py ../_static/figures
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle  # noqa: E402
from mpl_toolkits.mplot3d import Axes3D  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "MS Gothic", "sans-serif"]
plt.rcParams["font.size"] = 11
plt.rcParams["axes.unicode_minus"] = False

# 座標軸の色。Houdini のビューポートと同じく X を赤、Y を緑、Z を青にする。
AXIS_COLORS = {"X": "#d62728", "Y": "#2ca02c", "Z": "#1f77b4"}
POINT_COLOR = "#d62728"
PRIM_COLOR = "#9ecae1"
EDGE_COLOR = "#333333"


def box_faces(center: tuple[float, float, float],
              size: tuple[float, float, float]) -> list[list[tuple[float, float, float]]]:
    """中心と大きさを指定した直方体の 6 つの面を、頂点のリストで返す。"""
    cx, cy, cz = center
    hx, hy, hz = size[0] / 2, size[1] / 2, size[2] / 2
    corners = [(cx + sx * hx, cy + sy * hy, cz + sz * hz)
               for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    # corners の番号: (sx, sy, sz) を 2 進数とみなした値（-1 を 0、1 を 1）
    faces = [(0, 1, 3, 2), (4, 5, 7, 6), (0, 1, 5, 4), (2, 3, 7, 6), (0, 2, 6, 4), (1, 3, 7, 5)]
    return [[corners[i] for i in face] for face in faces]


def to_plot(points: list[tuple[float, float, float]]) -> list[tuple[float, float, float]]:
    """Houdini の座標（Y が上）を matplotlib の 3D 座標（Z が上）に並べ替える。"""
    return [(x, z, y) for x, y, z in points]


def setup_3d(ax: Axes3D, limits: tuple[float, float, float], elev: float = 22, azim: float = -60) -> None:
    """3D の軸の範囲と視点を設定し、目盛りを消す。"""
    lx, ly, lz = limits
    ax.set_xlim(-lx, lx)
    ax.set_ylim(-lz, lz)
    ax.set_zlim(0, ly)
    ax.set_box_aspect((2 * lx, 2 * lz, ly))
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()


def arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], color: str = "black",
          width: float = 1.5) -> None:
    """2D の図に矢印を描く。"""
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14, color=color, lw=width))


# ---------------------------------------------------------------------------
# 画面と基本操作
# ---------------------------------------------------------------------------


def fig_ui_layout() -> Figure:
    """Houdini のメインウィンドウの構成を模式的に描く。"""
    fig, ax = plt.subplots(figsize=(9, 5.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 62)
    ax.set_axis_off()

    def pane(x: float, y: float, w: float, h: float, label: str, color: str, size: int = 11,
             rotation: float = 0) -> None:
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, edgecolor=EDGE_COLOR, lw=1.2))
        ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=size, rotation=rotation)

    pane(0, 58, 100, 4, "(1) メインメニュー", "#e0e0e0", 10)
    pane(0, 52, 100, 6, "(2) シェルフ", "#fde0c5")
    pane(0, 6, 4, 46, "(4) ツールボックス", "#e7d4f0", 9, rotation=90)
    pane(4, 48, 54, 4, "(5) オペレーションツールバー", "#e7d4f0", 9)
    pane(4, 6, 50, 42, "(3) シーンビュー\n（3D ビューポート）", "#d4e8f7", 13)
    pane(54, 6, 4, 42, "(6) 表示オプション", "#e7d4f0", 9, rotation=90)
    pane(58, 31, 42, 21, "(7) パラメーターエディター", "#fff3b0", 12)
    pane(58, 6, 42, 25, "(8) ネットワークエディター", "#d8f0d0", 12)
    pane(0, 2, 100, 4, "(9) プレイバー（タイムライン）", "#e0e0e0", 10)
    pane(0, 0, 100, 2, "", "#cccccc")
    ax.text(50, -1.6, "(10) ステータスライン", ha="center", va="top", fontsize=9)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# 3DCG の基礎知識
# ---------------------------------------------------------------------------


def fig_coordinate_system() -> Figure:
    """Houdini の座標系（Y が上の右手系）を描く。"""
    fig = plt.figure(figsize=(5, 4.2))
    ax: Axes3D = fig.add_subplot(projection="3d")
    origin = np.zeros(3)
    # Houdini の (x, y, z) を matplotlib の (x, z, y) に対応させる。
    axes = {"X": (1.0, 0.0, 0.0), "Y": (0.0, 1.0, 0.0), "Z": (0.0, 0.0, 1.0)}
    for name, (x, y, z) in axes.items():
        ax.quiver(*origin, x, z, y, color=AXIS_COLORS[name], arrow_length_ratio=0.12, lw=2.5)
        ax.text(x * 1.15, z * 1.15, y * 1.15, f"+{name}", color=AXIS_COLORS[name], fontsize=14,
                ha="center", va="center")
    # 地面（XZ 平面）のグリッド
    for t in np.linspace(-1, 1, 5):
        ax.plot([t, t], [-1, 1], [0, 0], color="#bbbbbb", lw=0.8)
        ax.plot([-1, 1], [t, t], [0, 0], color="#bbbbbb", lw=0.8)
    ax.text(-1.0, -1.0, 0.0, "地面（XZ 平面）", color="#777777", fontsize=10)
    ax.set_xlim(-1, 1.2)
    ax.set_ylim(-1, 1.2)
    ax.set_zlim(0, 1.2)
    ax.set_box_aspect((2.2, 2.2, 1.2))
    ax.view_init(elev=20, azim=-55)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def fig_normals() -> Figure:
    """面の法線とポイントの法線の違いを、円柱の断面で描く。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    n = 8
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False) + np.pi / n
    pts = np.stack([np.cos(angles), np.sin(angles)], axis=1)
    titles = ["面の法線（角張って見える）", "ポイントの法線（滑らかに見える）"]
    for ax, title in zip(axes, titles):
        ax.add_patch(Polygon(pts, closed=True, facecolor=PRIM_COLOR, edgecolor=EDGE_COLOR, lw=1.5))
        ax.scatter(pts[:, 0], pts[:, 1], color=POINT_COLOR, zorder=3, s=18)
        ax.set_title(title, fontsize=12)
        ax.set_aspect("equal")
        ax.set_xlim(-1.8, 1.8)
        ax.set_ylim(-1.8, 1.8)
        ax.set_axis_off()
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        mid = (a + b) / 2
        normal = mid / np.linalg.norm(mid)
        arrow(axes[0], tuple(mid), tuple(mid + normal * 0.6), color="#e6550d")
    for p in pts:
        normal = p / np.linalg.norm(p)
        arrow(axes[1], tuple(p), tuple(p + normal * 0.6), color="#e6550d")
    fig.tight_layout()
    return fig


def fig_winding() -> Figure:
    """ポイントの並び順と面の表裏の関係を描く。"""
    fig, ax = plt.subplots(figsize=(4.6, 4.2))
    square = np.array([[0, 2], [2, 2], [2, 0], [0, 0]], dtype=float)
    ax.add_patch(Polygon(square, closed=True, facecolor=PRIM_COLOR, edgecolor=EDGE_COLOR, lw=1.5))
    for i, (x, y) in enumerate(square):
        ax.scatter([x], [y], color=POINT_COLOR, zorder=3, s=30)
        ax.text(x + (-0.18 if x == 0 else 0.18), y + (0.18 if y == 2 else -0.18), str(i),
                ha="center", va="center", fontsize=13)
    for i in range(4):
        a = square[i] * 0.7 + np.array([0.3, 0.3])
        b = square[(i + 1) % 4] * 0.7 + np.array([0.3, 0.3])
        arrow(ax, tuple(a + (b - a) * 0.15), tuple(a + (b - a) * 0.85), color="#555555", width=1.2)
    # 手前向きの法線を表す記号（丸の中に点）
    ax.add_patch(Circle((1.0, 1.0), 0.16, facecolor="white", edgecolor="#e6550d", lw=2))
    ax.scatter([1.0], [1.0], color="#e6550d", s=20, zorder=4)
    ax.text(1.0, -0.65, "0 → 1 → 2 → 3 の順に時計回り\n→ 法線は手前（見ている人の方）を向く",
            ha="center", va="center", fontsize=10)
    ax.set_aspect("equal")
    ax.set_xlim(-0.6, 2.6)
    ax.set_ylim(-1.1, 2.6)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def checker_colors(u: np.ndarray, v: np.ndarray, n: int = 6) -> np.ndarray:
    """UV 座標から市松模様の色（RGBA）を作る。"""
    cells = (np.floor(u * n) + np.floor(v * n)) % 2
    light = np.array([0.95, 0.85, 0.55, 1.0])
    dark = np.array([0.25, 0.45, 0.7, 1.0])
    result: np.ndarray = np.where(cells[..., None] == 0, light, dark)
    return result


def fig_uv() -> Figure:
    """UV 座標で、2 次元の画像を 3 次元の面に貼る様子を描く。"""
    fig = plt.figure(figsize=(9, 4.2))
    ax1 = fig.add_subplot(1, 2, 1)
    res = 60
    u, v = np.meshgrid(np.linspace(0, 1, res), np.linspace(0, 1, res))
    ax1.imshow(checker_colors(u, v), origin="lower", extent=(0, 1, 0, 1))
    ax1.set_xlabel("u")
    ax1.set_ylabel("v")
    ax1.set_title("UV 空間の画像（テクスチャ）", fontsize=12)
    ax1.set_xticks([0, 0.5, 1])
    ax1.set_yticks([0, 0.5, 1])

    ax2: Axes3D = fig.add_subplot(1, 2, 2, projection="3d")
    theta = u * np.pi * 1.2 - np.pi * 0.6
    x = np.sin(theta)
    z = np.cos(theta)
    y = v * 1.5
    ax2.plot_surface(x, z, y, facecolors=checker_colors(u, v), rstride=1, cstride=1,
                     linewidth=0, antialiased=False, shade=False)
    ax2.set_title("曲面に貼った結果", fontsize=12)
    ax2.set_box_aspect((2, 1.2, 1.5))
    ax2.view_init(elev=15, azim=-90)
    ax2.set_axis_off()
    fig.tight_layout()
    return fig


def fig_transform_order() -> Figure:
    """変換の順序で結果が変わることを、2 次元の四角形で描く。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 4.2))
    square = np.array([[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5]])
    angle = np.radians(45)
    rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    move = np.array([2.0, 0.0])
    cases = [
        ("回転してから移動", (square @ rot.T) + move),
        ("移動してから回転", (square + move) @ rot.T),
    ]
    for ax, (title, result) in zip(axes, cases):
        ax.add_patch(Polygon(square, closed=True, facecolor="#dddddd", edgecolor="#888888", lw=1, ls="--"))
        ax.add_patch(Polygon(result, closed=True, facecolor=PRIM_COLOR, edgecolor=EDGE_COLOR, lw=1.5))
        ax.axhline(0, color="#bbbbbb", lw=0.8)
        ax.axvline(0, color="#bbbbbb", lw=0.8)
        ax.scatter([0], [0], color="black", s=12)
        ax.text(0.08, -0.25, "原点", fontsize=9)
        ax.set_title(title, fontsize=12)
        ax.set_aspect("equal")
        ax.set_xlim(-1, 3)
        ax.set_ylim(-1, 2.6)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("同じ 2 つの変換（原点まわりに 45 度回転、X 方向に 2 移動）を逆の順序で適用する", fontsize=11)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# はじめてのモデリング
# ---------------------------------------------------------------------------

# examples/build_table.py と同じ寸法
TOP_SIZE = (1.2, 0.04, 0.7)
TABLE_HEIGHT = 0.72
LEG_SIZE = 0.05
LEG_INSET = 0.08


def fig_table() -> Figure:
    """机の完成形を、部品ごとに色分けして描く。"""
    fig = plt.figure(figsize=(6.4, 4.6))
    ax: Axes3D = fig.add_subplot(projection="3d")
    top_w, top_t, top_d = TOP_SIZE
    leg_h = TABLE_HEIGHT - top_t
    top = box_faces((0, leg_h + top_t / 2, 0), TOP_SIZE)
    ax.add_collection3d(Poly3DCollection([to_plot(f) for f in top], facecolor="#c49a6c",
                                         edgecolor="#5a4632", lw=0.6, alpha=0.95))
    px, pz = top_w / 2 - LEG_INSET, top_d / 2 - LEG_INSET
    for sx in (-1, 1):
        for sz in (-1, 1):
            leg = box_faces((sx * px, leg_h / 2, sz * pz), (LEG_SIZE, leg_h, LEG_SIZE))
            ax.add_collection3d(Poly3DCollection([to_plot(f) for f in leg], facecolor="#8c6d4f",
                                                 edgecolor="#4a3a2a", lw=0.6))
            ax.scatter([sx * px], [sz * pz], [0], color=POINT_COLOR, s=30, depthshade=False)
    # 脚の位置を決めるグリッド
    grid = [(-px, 0.0, -pz), (px, 0.0, -pz), (px, 0.0, pz), (-px, 0.0, pz)]
    gx, gy, gz = zip(*to_plot(grid + [grid[0]]))
    ax.plot(gx, gy, gz, color=POINT_COLOR, lw=1, ls="--")
    ax.text(0, -pz - 0.25, 0, "Grid（2 x 2 のポイント）", color=POINT_COLOR, fontsize=10, ha="center")
    ax.set_title("天板: Box → Transform → PolyBevel → Boolean\n脚: Box → Copy to Points（Grid のポイントへ）",
                 fontsize=10)
    setup_3d(ax, (0.7, 0.85, 0.45), elev=18, azim=-58)
    fig.subplots_adjust(left=0, right=1, bottom=-0.08, top=0.86)
    return fig


# ---------------------------------------------------------------------------
# パラメーターとエクスプレッション
# ---------------------------------------------------------------------------


def fig_bounce() -> Figure:
    """build_expressions.py のボールの高さと回転角を、フレームごとにグラフにする。"""
    frames = np.arange(1, 121)
    height = 0.5 + np.abs(np.sin(np.radians(frames * 6))) * 2
    angle = (frames - 1) / (120 - 1) * 360
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    axes[0].plot(frames, height, color="#1f77b4")
    axes[0].set_title('bounce の Translate Y\nch("../ball/radx") + abs(sin($F * 6)) * 2', fontsize=10)
    axes[1].plot(frames, angle, color="#d62728")
    axes[1].scatter([1, 120], [0, 360], color="#d62728", zorder=3)
    axes[1].set_title("spin の Rotate Y\n（1 と 120 フレームにキーフレーム、linear()）", fontsize=10)
    for ax, label in zip(axes, ["高さ（m）", "角度（度）"]):
        ax.set_xlabel("フレーム")
        ax.set_ylabel(label)
        ax.grid(alpha=0.3)
        ax.set_xlim(1, 120)
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# ジオメトリとアトリビュート
# ---------------------------------------------------------------------------


def fig_mesh_elements() -> Figure:
    """ポイント、バーテックス、プリミティブ、ディテールの関係を描く。"""
    fig, ax = plt.subplots(figsize=(8, 4.6))
    pts = np.array([[0, 0], [2, 0], [4, 0], [0, 2], [2, 2], [4, 2]], dtype=float)
    prims = [[3, 4, 1, 0], [4, 5, 2, 1]]   # 上から見て時計回り
    ax.add_patch(Rectangle((-1.0, -1.0), 6.0, 4.0, facecolor="none", edgecolor="#888888", lw=1.2,
                           ls="--"))
    ax.text(-0.9, 2.75, "ディテール（ジオメトリ全体）", fontsize=10, color="#555555")
    vertex_number = 0
    for prim_number, prim in enumerate(prims):
        poly = pts[prim]
        ax.add_patch(Polygon(poly, closed=True, facecolor=PRIM_COLOR, edgecolor=EDGE_COLOR, lw=1.5))
        center = poly.mean(axis=0)
        ax.text(center[0], center[1], f"プリミティブ {prim_number}", ha="center", va="center",
                fontsize=11, color="#08519c")
        for point_index in prim:
            # バーテックスは、プリミティブの角に少し内側にずらして描く。
            pos = pts[point_index] + (center - pts[point_index]) * 0.3
            ax.scatter([pos[0]], [pos[1]], marker="s", color="#31a354", s=26, zorder=3)
            ax.text(pos[0], pos[1] + (-0.3 if pos[1] > 1 else 0.18), f"v{vertex_number}", ha="center",
                    fontsize=9, color="#31a354")
            vertex_number += 1
    for i, (x, y) in enumerate(pts):
        ax.scatter([x], [y], color=POINT_COLOR, s=45, zorder=4)
        ax.text(x, y + (0.25 if y > 1 else -0.35), f"ポイント {i}", ha="center", fontsize=9,
                color=POINT_COLOR)
    ax.scatter([], [], color=POINT_COLOR, s=45, label="ポイント（位置を持つ）")
    ax.scatter([], [], marker="s", color="#31a354", s=26, label="バーテックス（プリミティブの角）")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=9, frameon=False)
    ax.set_aspect("equal")
    ax.set_xlim(-1.2, 5.2)
    ax.set_ylim(-1.7, 3.1)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# プロシージャルモデリングの実践
# ---------------------------------------------------------------------------


def fig_stairs() -> Figure:
    """階段のポイントと、そこにコピーする箱の関係を横から見た図で描く。"""
    fig, ax = plt.subplots(figsize=(8, 4.4))
    count, rise, run = 5, 0.18, 0.28
    for i in range(count):
        h = rise * (i + 1)
        z = run * (i + 0.5)
        ax.add_patch(Rectangle((z - run / 2, 0), run, h, facecolor=PRIM_COLOR, edgecolor=EDGE_COLOR, lw=1.2))
        ax.scatter([z], [h / 2], color=POINT_COLOR, s=30, zorder=3)
        ax.text(z, h / 2 - 0.07, f"{i}", ha="center", va="top", fontsize=9, color=POINT_COLOR)
    # 最後の段の寸法を示す。
    z_last = run * (count - 0.5)
    h_last = rise * count
    ax.annotate("", xy=(z_last + run / 2 + 0.06, 0), xytext=(z_last + run / 2 + 0.06, h_last),
                arrowprops={"arrowstyle": "<->"})
    ax.text(z_last + run / 2 + 0.09, h_last / 2, "高さ = step_height x (i + 1)", va="center", fontsize=9)
    ax.annotate("", xy=(z_last - run / 2, h_last + 0.05), xytext=(z_last + run / 2, h_last + 0.05),
                arrowprops={"arrowstyle": "<->"})
    ax.text(z_last, h_last + 0.08, "step_depth", ha="center", fontsize=9)
    ax.text(0.0, h_last + 0.12, "赤い点: Wrangle が作るポイント（番号 i）\n"
            "箱: Copy to Points で各ポイントにコピーした Box", fontsize=9, va="bottom")
    ax.set_xlabel("Z（奥行き方向、m）")
    ax.set_ylabel("Y（高さ、m）")
    ax.set_aspect("equal")
    ax.set_xlim(-0.1, 2.1)
    ax.set_ylim(0, 1.25)
    ax.grid(alpha=0.25)
    fig.tight_layout()
    return fig


def fig_city_lots() -> Figure:
    """グリッドのマスを区画にし、区画ごとに高さを決める流れを上から見た図で描く。"""
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.8))
    n = 5
    rng = np.random.default_rng(3)
    heights = rng.uniform(6, 60, size=(n, n))
    empty = rng.uniform(size=(n, n)) < 0.2
    titles = ["(1) Grid のマス", "(2) PolyExtrude で縮めた区画", "(3) 区画ごとの高さ（空き地あり）"]
    cmap = plt.get_cmap("Blues")
    for k, (ax, title) in enumerate(zip(axes, titles)):
        for i in range(n):
            for j in range(n):
                inset = 0.0 if k == 0 else 0.15
                if k == 2 and empty[i, j]:
                    ax.add_patch(Rectangle((j, i), 1, 1, facecolor="none", edgecolor="#cccccc", lw=0.8))
                    continue
                color = PRIM_COLOR if k < 2 else cmap(0.3 + 0.7 * heights[i, j] / 60)
                ax.add_patch(Rectangle((j + inset, i + inset), 1 - 2 * inset, 1 - 2 * inset,
                                       facecolor=color, edgecolor=EDGE_COLOR, lw=0.8))
                if k == 2:
                    ax.text(j + 0.5, i + 0.5, f"{heights[i, j]:.0f}", ha="center", va="center", fontsize=8)
        ax.set_title(title, fontsize=11)
        ax.set_aspect("equal")
        ax.set_xlim(-0.1, n + 0.1)
        ax.set_ylim(-0.1, n + 0.1)
        ax.set_axis_off()
    fig.text(0.5, 0.02, "（数字は高さ（m）の例。実際の値は Seed などのパラメーターで変わる）", ha="center",
             fontsize=9)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    return fig


FIGURES: dict[str, Callable[[], Figure]] = {
    "ui_layout.png": fig_ui_layout,
    "coordinate_system.png": fig_coordinate_system,
    "normals.png": fig_normals,
    "winding.png": fig_winding,
    "uv.png": fig_uv,
    "transform_order.png": fig_transform_order,
    "table.png": fig_table,
    "bounce.png": fig_bounce,
    "mesh_elements.png": fig_mesh_elements,
    "stairs.png": fig_stairs,
    "city_lots.png": fig_city_lots,
}


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, make in FIGURES.items():
        fig = make()
        fig.savefig(output_dir / name, dpi=110, facecolor="white")
        plt.close(fig)
        print(f"saved {name}")


if __name__ == "__main__":
    main()
