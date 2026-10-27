"""本文で使う図を生成するスクリプト.

conf.py からビルド開始時に呼び出される. examples のサンプルコードを import して,
本文で説明している実装と同じコードで図を描く.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import numpy.typing as npt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.colors import ListedColormap  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402
from PIL import Image  # noqa: E402

import elementary_ca  # noqa: E402
import game_of_life  # noqa: E402
import langtons_ant  # noqa: E402
import lattice_gas_hpp  # noqa: E402
import traffic_nasch  # noqa: E402

plt.rcParams["font.family"] = ["BIZ UDPGothic", "Yu Gothic", "Meiryo", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

DPI = 120
CELL_COLOR = "#2b4c7e"
GRID_COLOR = "#999999"


def draw_cells(ax: Axes, cells: npt.NDArray[np.uint8], on: str = CELL_COLOR, off: str = "white") -> None:
    """0/1 の 2 次元配列をマス目として描く."""
    rows, cols = cells.shape
    for r in range(rows):
        for c in range(cols):
            color = on if cells[r, c] else off
            ax.add_patch(Rectangle((c, rows - 1 - r), 1, 1, facecolor=color, edgecolor=GRID_COLOR, linewidth=0.8))
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.axis("off")


def save(fig: Figure, out: Path, name: str) -> None:
    """図を PNG ファイルとして保存し, メモリを解放する."""
    fig.savefig(out / name, dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def neighborhoods(out: Path) -> None:
    """フォン・ノイマン近傍とムーア近傍."""
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.4))
    size = 5
    titles = ["フォン・ノイマン近傍 (r = 1)", "ムーア近傍 (r = 1)", "フォン・ノイマン近傍 (r = 2)"]
    for ax, title, kind in zip(axes, titles, ["vn1", "moore1", "vn2"]):
        for y in range(size):
            for x in range(size):
                dy, dx = y - 2, x - 2
                if kind == "vn1":
                    inside = abs(dy) + abs(dx) <= 1
                elif kind == "moore1":
                    inside = max(abs(dy), abs(dx)) <= 1
                else:
                    inside = abs(dy) + abs(dx) <= 2
                if dy == 0 and dx == 0:
                    color = "#d9534f"
                elif inside:
                    color = "#9cc3e6"
                else:
                    color = "white"
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor=color, edgecolor=GRID_COLOR))
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=12)
    save(fig, out, "neighborhoods.png")


def boundaries(out: Path) -> None:
    """1 次元の場合の境界条件 (周期・固定・反射) の模式図."""
    values = [1, 0, 1, 1, 0, 0, 1, 0]
    n = len(values)
    cases = [
        ("周期境界条件", values[-1], values[0]),
        ("固定境界条件 (外側を 0 に固定)", 0, 0),
        ("反射境界条件", values[0], values[-1]),
    ]
    fig, axes = plt.subplots(3, 1, figsize=(8, 4.2))
    for ax, (title, left_ghost, right_ghost) in zip(axes, cases):
        row = [left_ghost] + values + [right_ghost]
        for i, v in enumerate(row):
            ghost = i == 0 or i == n + 1
            face = ("#c9d6ea" if v else "#f2f2f2") if ghost else (CELL_COLOR if v else "white")
            ax.add_patch(Rectangle((i, 0), 1, 1, facecolor=face, edgecolor=GRID_COLOR,
                                   linestyle="--" if ghost else "-", linewidth=1.0))
            ax.text(i + 0.5, 0.5, str(v), ha="center", va="center", fontsize=11,
                    color="white" if (v and not ghost) else "black")
        ax.text(-0.3, 0.5, title, ha="right", va="center", fontsize=11)
        ax.set_xlim(-0.2, n + 2.2)
        ax.set_ylim(-0.2, 1.2)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.text(0.62, 0.0, "破線のセルは境界の外側に仮想的に置いたセル (ゴースト・セル) を表す", ha="center", fontsize=10)
    save(fig, out, "boundaries.png")


def rule_table_figure(out: Path, rule: int, name: str) -> None:
    """局所規則の表 (8 通りの近傍パターンと次の状態) を図にする."""
    table = elementary_ca.rule_table(rule)
    fig, axes = plt.subplots(1, 8, figsize=(10, 2.2))
    for ax, k in zip(axes, range(7, -1, -1)):
        bits = [(k >> 2) & 1, (k >> 1) & 1, k & 1]
        for i, b in enumerate(bits):
            ax.add_patch(Rectangle((i, 1.2), 1, 1, facecolor=CELL_COLOR if b else "white", edgecolor=GRID_COLOR))
        ax.add_patch(Rectangle((1, 0), 1, 1, facecolor=CELL_COLOR if table[k] else "white", edgecolor=GRID_COLOR))
        ax.text(1.5, -0.45, str(int(table[k])), ha="center", va="center", fontsize=13)
        ax.text(1.5, 2.65, f"{bits[0]}{bits[1]}{bits[2]}", ha="center", va="center", fontsize=11)
        ax.set_xlim(-0.1, 3.1)
        ax.set_ylim(-0.9, 2.9)
        ax.set_aspect("equal")
        ax.axis("off")
    fig.suptitle(f"ルール {rule} = {rule:08b} (2 進数)", fontsize=13, y=1.05)
    save(fig, out, name)


def eca_gallery(out: Path) -> None:
    """代表的な基本セル・オートマトンの時空図."""
    width, steps = 161, 80
    specs = [
        (30, elementary_ca.single_seed(width), "ルール 30 (単一セルから)"),
        (90, elementary_ca.single_seed(width), "ルール 90 (単一セルから)"),
        (110, elementary_ca.random_cells(width, seed=3), "ルール 110 (ランダムな初期配置)"),
        (184, elementary_ca.random_cells(width, density=0.4, seed=5), "ルール 184 (密度 0.4)"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(10, 6.2))
    for ax, (rule, init, title) in zip(axes.flat, specs):
        ax.imshow(elementary_ca.evolve(rule, init, steps), cmap="binary", interpolation="nearest")
        ax.set_title(title, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, out, "eca_gallery.png")


def wolfram_classes(out: Path) -> None:
    """ウルフラムの 4 クラスの例 (いずれもランダムな初期配置から)."""
    width, steps = 161, 100
    init = elementary_ca.random_cells(width, seed=11)
    specs = [(160, "クラス 1 (ルール 160)"), (108, "クラス 2 (ルール 108)"),
             (45, "クラス 3 (ルール 45)"), (110, "クラス 4 (ルール 110)")]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.4))
    for ax, (rule, title) in zip(axes, specs):
        ax.imshow(elementary_ca.evolve(rule, init, steps), cmap="binary", interpolation="nearest")
        ax.set_title(title, fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, out, "wolfram_classes.png")


def life_patterns(out: Path) -> None:
    """ライフゲームの代表的なパターン."""
    specs = [("block", "ブロック (静物)"), ("beehive", "ビーハイブ (静物)"), ("blinker", "ブリンカー (振動子, 周期 2)"),
             ("toad", "ヒキガエル (振動子, 周期 2)"), ("glider", "グライダー (宇宙船)"), ("lwss", "軽量級宇宙船 (LWSS)")]
    fig, axes = plt.subplots(1, 6, figsize=(13, 2.8))
    for ax, (key, title) in zip(axes, specs):
        grid = game_of_life.place(game_of_life.PATTERNS[key], (7, 7))
        draw_cells(ax, grid)
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    save(fig, out, "life_patterns.png")


def glider_evolution(out: Path) -> None:
    """グライダーの 4 世代分の変化."""
    grid = game_of_life.place(game_of_life.PATTERNS["glider"], (7, 7), top=1, left=1)
    fig, axes = plt.subplots(1, 5, figsize=(11, 2.6))
    for t, ax in enumerate(axes):
        draw_cells(ax, grid)
        ax.set_title(f"第 {t} 世代", fontsize=11)
        grid = game_of_life.step(grid)
    fig.tight_layout()
    save(fig, out, "glider_evolution.png")


def gosper_gun(out: Path) -> None:
    """グライダー銃の静止画とアニメーション (GIF)."""
    shape = (48, 64)
    grid = game_of_life.place(game_of_life.PATTERNS["gosper_gun"], shape, top=2, left=2)
    frames: list[Image.Image] = []
    scale = 6
    for t in range(150):
        if t % 2 == 0:
            pixels = np.where(grid == 1, 40, 250).astype(np.uint8)
            frame = Image.fromarray(pixels).resize((shape[1] * scale, shape[0] * scale), Image.Resampling.NEAREST)
            frames.append(frame.convert("P"))
        if t == 120:
            fig, ax = plt.subplots(figsize=(6.4, 4.8))
            ax.imshow(grid, cmap="binary", interpolation="nearest")
            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title("ゴスパーのグライダー銃 (第 120 世代)", fontsize=12)
            save(fig, out, "gosper_gun.png")
        # 右下に到達したグライダーが周期境界で回り込んで銃を壊さないように, 端の帯を消す.
        grid[-4:, :] = 0
        grid[:, -4:] = 0
        grid = game_of_life.step(grid)
    frames[0].save(out / "gosper_gun.gif", save_all=True, append_images=frames[1:], duration=80, loop=0)


def langtons_ant_figure(out: Path) -> None:
    """ラングトンのアリの軌跡."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    for ax, steps in zip(axes, [5000, 11000]):
        grid, ant = langtons_ant.run(100, steps)
        ax.imshow(grid, cmap="binary", interpolation="nearest")
        ax.plot(ant.col, ant.row, "r.", markersize=8)
        ax.set_title(f"{steps} ステップ後", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, out, "langtons_ant.png")


def margolus(out: Path) -> None:
    """マーゴラス近傍 (ブロックの区切り方を時刻ごとに交互にずらす)."""
    fig, axes = plt.subplots(1, 2, figsize=(8, 4))
    size = 6
    for ax, offset, title in zip(axes, [0, 1], ["偶数時刻の区切り方", "奇数時刻の区切り方"]):
        for y in range(size):
            for x in range(size):
                ax.add_patch(Rectangle((x, y), 1, 1, facecolor="white", edgecolor="#cccccc"))
        for by in range(-1, size, 2):
            for bx in range(-1, size, 2):
                block = Rectangle((bx + offset, by + offset), 2, 2, fill=False, edgecolor="#d9534f", linewidth=2.2)
                ax.add_patch(block)
        ax.set_xlim(0, size)
        ax.set_ylim(0, size)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(title, fontsize=12)
    save(fig, out, "margolus.png")


def lambda_rule(rng: np.random.Generator, k: int, n: int, lam: float) -> npt.NDArray[np.int64]:
    """ラングトンの λ パラメータを持つランダムな局所規則を作る.

    各近傍パターンについて, 確率 1 - λ で静止状態 0 を, 確率 λ でそれ以外の状態を一様に選ぶ.
    すべてのセルが 0 の近傍は必ず 0 に移す (静止条件).
    """
    size = k ** n
    table = np.where(rng.random(size) < lam, rng.integers(1, k, size), 0).astype(np.int64)
    table[0] = 0
    return table


def lambda_figure(out: Path) -> None:
    """λ パラメータを変えたときの振る舞いの変化 (K = 4, 近傍の半径 2)."""
    k, radius = 4, 2
    n = 2 * radius + 1
    width, steps = 160, 120
    lams = [0.10, 0.25, 0.40, 0.65]
    fig, axes = plt.subplots(1, 4, figsize=(12, 3.8))
    cmap = ListedColormap(["white", "#2b4c7e", "#d9534f", "#5cb85c"])
    for ax, lam in zip(axes, lams):
        rng = np.random.default_rng(7)
        table = lambda_rule(rng, k, n, lam)
        cells = rng.integers(0, k, width)
        cells[: width // 4] = 0
        cells[-width // 4:] = 0
        history = np.zeros((steps, width), dtype=np.int64)
        for t in range(steps):
            history[t] = cells
            index = np.zeros(width, dtype=np.int64)
            for offset in range(-radius, radius + 1):
                index = index * k + np.roll(cells, -offset)
            cells = table[index]
        ax.imshow(history, cmap=cmap, vmin=0, vmax=k - 1, interpolation="nearest")
        ax.set_title(f"λ = {lam:.2f}", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, out, "lambda.png")


def traffic_figures(out: Path) -> None:
    """ナーゲル・シュレッケンベルク・モデルの時空図と基本図."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    for ax, density in zip(axes, [0.1, 0.3]):
        history = traffic_nasch.simulate(200, density, 5, 0.25, 200, seed=2)
        ax.imshow(history != traffic_nasch.EMPTY, cmap="binary", interpolation="nearest", aspect="auto")
        ax.set_title(f"密度 {density}", fontsize=12)
        ax.set_xlabel("位置 (セル)")
        ax.set_ylabel("時刻 (ステップ)")
    fig.tight_layout()
    save(fig, out, "nasch_spacetime.png")

    fig, ax = plt.subplots(figsize=(6, 4.2))
    densities = np.linspace(0.02, 0.9, 30)
    for p, marker in [(0.0, "s-"), (0.25, "o-"), (0.5, "^-")]:
        flows = [traffic_nasch.mean_flow(400, float(rho), 5, p, transient=300, measure=300, seed=1)
                 for rho in densities]
        ax.plot(densities, flows, marker, markersize=4, label=f"p = {p}")
    ax.set_xlabel("密度 ρ")
    ax.set_ylabel("流量 q")
    ax.set_title("基本図 (v_max = 5)", fontsize=12)
    ax.legend()
    ax.grid(alpha=0.3)
    save(fig, out, "nasch_diagram.png")


def hpp_figure(out: Path) -> None:
    """HPP 格子ガスで密度の高い領域から波が広がる様子."""
    size, block = 256, 4
    state = lattice_gas_hpp.initial_state(size, background=0.2, bump=0.7, radius=size // 16, seed=1)
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.9))
    t = 0
    for ax, target in zip(axes, [0, 30, 60]):
        while t < target:
            state = lattice_gas_hpp.step(state)
            t += 1
        ax.imshow(lattice_gas_hpp.coarse_density(state, block), cmap="viridis", vmin=0.4, vmax=1.6,
                  interpolation="nearest")
        ax.set_title(f"{target} ステップ後", fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.tight_layout()
    save(fig, out, "hpp.png")


def hpp_rules(out: Path) -> None:
    """HPP モデルの衝突規則."""
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.2))
    arrows = {"E": (1, 0), "W": (-1, 0), "N": (0, 1), "S": (0, -1)}

    def node(ax: Axes, cx: float, dirs: str, incoming: bool) -> None:
        ax.plot(cx, 0, "ko", markersize=6)
        for d in dirs:
            dx, dy = arrows[d]
            outer = (cx + 0.9 * dx, 0.9 * dy)
            # 衝突前は粒子がノードへ向かってくる様子, 衝突後はノードから出ていく様子を描く.
            head, tail = ((cx + 0.15 * dx, 0.15 * dy), outer) if incoming else (outer, (cx, 0))
            ax.annotate("", xy=head, xytext=tail, arrowprops={"arrowstyle": "-|>", "color": CELL_COLOR, "lw": 2})

    for ax, (before, after) in zip(axes, [("EW", "NS"), ("NS", "EW")]):
        node(ax, 0, before, incoming=True)
        ax.annotate("", xy=(2.3, 0), xytext=(1.5, 0), arrowprops={"arrowstyle": "->", "lw": 1.5})
        node(ax, 3.8, after, incoming=False)
        ax.set_xlim(-1.3, 5.1)
        ax.set_ylim(-1.3, 1.3)
        ax.set_aspect("equal")
        ax.axis("off")
    axes[0].set_title("東西方向の 2 粒子 → 南北方向へ", fontsize=11)
    axes[1].set_title("南北方向の 2 粒子 → 東西方向へ", fontsize=11)
    save(fig, out, "hpp_rules.png")


def generate(out: Path) -> None:
    """すべての図を out に出力する."""
    out.mkdir(parents=True, exist_ok=True)
    neighborhoods(out)
    boundaries(out)
    rule_table_figure(out, 30, "rule30_table.png")
    eca_gallery(out)
    wolfram_classes(out)
    life_patterns(out)
    glider_evolution(out)
    gosper_gun(out)
    langtons_ant_figure(out)
    margolus(out)
    lambda_figure(out)
    traffic_figures(out)
    hpp_figure(out)
    hpp_rules(out)


if __name__ == "__main__":
    import sys

    generate(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "_generated")
