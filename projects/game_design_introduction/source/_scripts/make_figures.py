"""本文で使う図を生成する。conf.py からビルドの開始時に呼び出される。

* 本文専用の図（フローチャンネル、成長曲線など）は、このスクリプトの中で matplotlib と Pillow を使って描く。
* サンプルコードの実行結果の図は、examples のスクリプトを --output などの引数付きで実行して作る。
  こうすることで、本文の図とサンプルを実行したときの結果が必ず一致する。

単独でも実行できる:
    python make_figures.py OUTPUT_DIR
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Polygon, Rectangle  # noqa: E402
from PIL import Image, ImageDraw  # noqa: E402

HERE = Path(__file__).resolve().parent
EXAMPLES = HERE.parent.parent / "examples"
DPI = 110

plt.rcParams["font.family"] = ["Yu Gothic", "Meiryo", "sans-serif"]


def save(fig: Figure, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)


def flow_channel(out: Path) -> None:
    """フローチャンネル（挑戦の難しさとプレイヤーの能力の関係）。"""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.add_patch(Polygon([(0, 0), (0, 0.25), (0.75, 1), (1, 1), (1, 0.75), (0.25, 0)], color="#9ad0a4", alpha=0.6))
    ax.text(0.66, 0.4, "フロー", ha="center", va="center", fontsize=14)
    ax.text(0.2, 0.8, "不安", ha="center", va="center", fontsize=14)
    ax.text(0.8, 0.2, "退屈", ha="center", va="center", fontsize=14)
    path_x = [0.05, 0.2, 0.25, 0.45, 0.5, 0.7, 0.75, 0.92]
    path_y = [0.05, 0.15, 0.3, 0.38, 0.55, 0.6, 0.78, 0.85]
    ax.plot(path_x, path_y, color="#3060c0", marker="o", linewidth=2, label="プレイヤーの体験の例")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel("プレイヤーの能力（スキル） →")
    ax.set_ylabel("挑戦の難しさ →")
    ax.legend(loc="lower right")
    save(fig, out)


def player_types(out: Path) -> None:
    """バートルのプレイヤータイプ（2 つの軸と 4 つのタイプ）。"""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    labels = [
        (-0.5, 0.5, "キラー\n他のプレイヤーに\n働きかける"),
        (0.5, 0.5, "アチーバー\n世界に\n働きかける"),
        (-0.5, -0.5, "ソーシャライザー\n他のプレイヤーと\n交流する"),
        (0.5, -0.5, "エクスプローラー\n世界と\n交流する"),
    ]
    for x, y, text in labels:
        ax.text(x, y, text, ha="center", va="center", fontsize=11, linespacing=1.6)
    ax.text(0.03, 1.0, "働きかける（acting）", ha="left", va="top")
    ax.text(0.03, -1.0, "交流する（interacting）", ha="left", va="bottom")
    ax.text(-1.0, 0.04, "プレイヤー", ha="left", va="bottom")
    ax.text(1.0, 0.04, "世界", ha="right", va="bottom")
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.axis("off")
    save(fig, out)


def growth_curves(out: Path) -> None:
    """次のレベルに必要な経験値の 3 つの式。"""
    levels = list(range(1, 31))
    curves: dict[str, list[float]] = {
        "線形: 100 L": [100 * lv for lv in levels],
        "多項式: 50 L²": [50 * lv ** 2 for lv in levels],
        "指数: 100 × 1.2^(L-1)": [100 * 1.2 ** (lv - 1) for lv in levels],
    }
    fig, ax = plt.subplots(figsize=(7, 4))
    for label, values in curves.items():
        ax.plot(levels, values, linewidth=2, label=label)
    ax.set_xlabel("現在のキャラクターのレベル L")
    ax.set_ylabel("次のレベルまでに必要な経験値")
    ax.set_title("成長曲線の比較")
    ax.grid(alpha=0.3)
    ax.legend()
    save(fig, out)


def intensity_curve(out: Path) -> None:
    """1 つのレベルの中での緊張度（強度）の推移。"""
    points = [(0, 0.1), (1, 0.35), (2, 0.2), (3, 0.55), (4, 0.3), (5, 0.25), (6, 0.7), (7, 0.4), (8, 0.95), (9, 0.15)]
    xs, ys = zip(*points)
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.plot(xs, ys, marker="o", linewidth=2, color="#c04040")
    notes = {1: "最初の戦闘", 2: "探索", 3: "新しい敵", 5: "休憩・セーブ", 6: "応用の戦闘", 8: "ボス", 9: "報酬"}
    valleys = {2, 5, 9}  # 谷の注釈は点の下に置く
    for x, note in notes.items():
        offset = (0, -16) if x in valleys else (0, 10)
        ax.annotate(note, (x, points[x][1]), textcoords="offset points", xytext=offset, ha="center", fontsize=9)
    ax.set_xticks(range(10))
    ax.set_xticklabels([f"区間 {i + 1}" for i in range(10)], fontsize=8)
    ax.set_ylim(-0.05, 1.1)
    ax.set_ylabel("緊張度")
    ax.set_title("レベル内の緊張と緩和")
    ax.grid(alpha=0.3)
    save(fig, out)


def blockout_metrics(out: Path) -> None:
    """ジャンプの性能（メトリクス）から足場の配置を決める例（横から見た図）。"""
    tile = 32
    # jump_feel.py の設定（初速 11、重力 0.5、落下時 1.8 倍、走る速さ 5）で地面から跳んだ軌跡を求める。
    vy, y, x = -11.0, 0.0, 0.0
    arc_x, arc_y = [0.0], [0.0]
    while True:
        vy = min(vy + (0.5 * 1.8 if vy > 0 else 0.5), 12.0)
        y += vy
        x += 5.0
        if y >= 0:
            break
        arc_x.append(x / tile)
        arc_y.append(-y / tile)
    arc_x.append(x / tile)
    arc_y.append(0.0)
    height = max(arc_y)

    fig, ax = plt.subplots(figsize=(8, 3.6))
    blocks = [(0, 0, 4, 1), (8, 0, 4, 1), (14, 2, 3, 1), (19, 4, 3, 1)]
    for bx, by, bw, bh in blocks:
        ax.add_patch(Rectangle((bx, by - 1), bw, bh, color="#8890a8"))
    ax.add_patch(Rectangle((3, 0), 0.75, 0.94, color="#5aa8f0"))
    ax.plot([3.4 + v for v in arc_x], arc_y, color="#f08030", linewidth=2, linestyle="--", label="最大ジャンプの軌跡")
    peak_x = 3.4 + arc_x[arc_y.index(height)]
    ax.annotate("", xy=(peak_x, height), xytext=(peak_x, 0), arrowprops={"arrowstyle": "<->"})
    ax.text(peak_x + 0.3, height / 2, f"高さ 約 {height:.1f} マス", ha="left", va="center", fontsize=9)
    ax.annotate("", xy=(3.4 + arc_x[-1], -1.6), xytext=(3.4, -1.6), arrowprops={"arrowstyle": "<->"})
    ax.text(3.4 + arc_x[-1] / 2, -1.5, f"幅 約 {arc_x[-1]:.1f} マス", ha="center", va="bottom", fontsize=9)
    ax.text(6, -0.5, "穴 4 マス", ha="center", va="center", fontsize=9)
    ax.text(15.5, 2.2, "段差 2 マス", ha="center", va="bottom", fontsize=9)
    ax.text(20.5, 4.2, "段差 2 マス", ha="center", va="bottom", fontsize=9)
    ax.set_xlim(0, 23)
    ax.set_ylim(-2, 6)
    ax.set_aspect("equal")
    ax.set_xticks(range(0, 24, 2))
    ax.set_yticks(range(-1, 7))
    ax.grid(alpha=0.3)
    ax.set_xlabel("横の位置（マス）")
    ax.set_ylabel("高さ（マス）")
    ax.legend(loc="upper left", fontsize=9)
    save(fig, out)


LEVEL_COLORS = {
    "#": (130, 136, 156),
    ".": (70, 74, 90),
}


def draw_level(level_path: Path, out: Path, cell: int = 28) -> None:
    """final_project のレベルファイルを、ゲーム画面に近い見た目で画像にする。"""
    rows = [line for line in level_path.read_text(encoding="utf-8").splitlines() if line and not line.startswith(";")]
    width, height = max(len(r) for r in rows), len(rows)
    image = Image.new("RGB", (width * cell, height * cell), LEVEL_COLORS["#"])
    pen = ImageDraw.Draw(image)
    for y, row in enumerate(rows):
        for x, char in enumerate(row):
            box = (x * cell, y * cell, (x + 1) * cell - 1, (y + 1) * cell - 1)
            pen.rectangle(box, fill=LEVEL_COLORS["#"] if char == "#" else LEVEL_COLORS["."])
            inner = (box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5)
            cx, cy = (box[0] + box[2]) // 2, (box[1] + box[3]) // 2
            if char == "@":
                pen.ellipse(inner, fill=(90, 170, 250))
            elif char == "*":
                pen.polygon([(cx, inner[1]), (inner[2], cy), (cx, inner[3]), (inner[0], cy)], fill=(250, 210, 70))
            elif char == "E":
                pen.rounded_rectangle((box[0] + 3, box[1] + 3, box[2] - 3, box[3] - 3), radius=4, fill=(80, 200, 120))
            elif char in "<>^v":
                pen.ellipse(inner, fill=(230, 80, 80))
                dx, dy = {"<": (-1, 0), ">": (1, 0), "^": (0, -1), "v": (0, 1)}[char]
                pen.line((cx, cy, cx + dx * cell // 2, cy + dy * cell // 2), fill=(240, 240, 240), width=3)
    image.save(out)


def run_example(script: str, *args: str, cwd: Path = EXAMPLES) -> None:
    """examples のスクリプトを実行する。標準出力は捨てる。"""
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    subprocess.run([sys.executable, script, *args], cwd=cwd, env=env, check=True, stdout=subprocess.DEVNULL)


def main(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    flow_channel(out_dir / "flow_channel.png")
    player_types(out_dir / "player_types.png")
    growth_curves(out_dir / "growth_curves.png")
    intensity_curve(out_dir / "intensity_curve.png")
    blockout_metrics(out_dir / "blockout_metrics.png")
    for level in sorted((EXAMPLES / "final_project" / "levels").glob("*.txt")):
        draw_level(level, out_dir / f"final_{level.stem}.png")

    run_example("resource_flow.py", "--output", str(out_dir / "resource_flow.png"))
    run_example("balance_simulation.py", "--output", str(out_dir / "balance_simulation.png"))
    run_example("difficulty_curve.py", "--output", str(out_dir / "difficulty_curve.png"))
    run_example("jump_feel.py", "--plot", str(out_dir / "jump_trajectory.png"))
    run_example("procgen_cave.py", "--method", "walk", "--seed", "5", "--output", str(out_dir / "procgen_walk.png"))
    run_example("procgen_cave.py", "--method", "cave", "--output", str(out_dir / "procgen_cave.png"))
    run_example("procgen_bsp.py", "--output", str(out_dir / "procgen_bsp.png"))
    run_example("playtest_heatmap.py", "--output", str(out_dir / "playtest_heatmap.png"))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent / "_generated")
