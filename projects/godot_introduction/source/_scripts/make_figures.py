"""本文で使う図を matplotlib で描くスクリプト。conf.py からビルドのたびに呼び出す。"""

from __future__ import annotations

import math
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402
from matplotlib.figure import Figure  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

plt.rcParams["font.family"] = ["Meiryo", "Yu Gothic", "MS Gothic", "sans-serif"]
plt.rcParams["axes.unicode_minus"] = False

COLORS = ["#2a6fdb", "#e0663a", "#2a9d5c", "#9a4fd1"]


def _save(fig: Figure, path: Path) -> None:
    fig.tight_layout()
    fig.savefig(path, dpi=110)
    plt.close(fig)


def delta_comparison(path: Path) -> None:
    """delta を使う場合と使わない場合の移動距離の比較（第 8 章）。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    speed = 200.0
    for color, fps in zip(COLORS, [30, 60, 144]):
        times = [i / fps for i in range(fps * 2 + 1)]
        with_delta = [speed * t for t in times]
        without_delta = [speed / 60.0 * i for i in range(len(times))]
        axes[0].plot(times, with_delta, color=color, label=f"{fps} FPS")
        axes[1].plot(times, without_delta, color=color, label=f"{fps} FPS")
    axes[0].set_title("delta を使う（速さ × delta）")
    axes[1].set_title("delta を使わない（毎フレーム一定量）")
    for ax in axes:
        ax.set_xlabel("経過時間 [秒]")
        ax.grid(alpha=0.3)
        ax.legend()
    axes[0].set_ylabel("移動距離 [ピクセル]")
    _save(fig, path)


def fixed_timestep(path: Path) -> None:
    """描画フレームと物理フレームのタイミング（第 8 章）。"""
    fig, ax = plt.subplots(figsize=(9, 2.4))
    physics = [i / 60 for i in range(13)]
    render: list[float] = []
    t = 0.0
    intervals = [0.012, 0.025, 0.010, 0.030, 0.015, 0.020, 0.012, 0.028, 0.018, 0.016]
    for dt in intervals:
        t += dt
        render.append(t)
    ax.eventplot([physics, render], lineoffsets=[1, 0], linelengths=0.6, colors=[COLORS[0], COLORS[1]])
    ax.set_yticks([1, 0], ["_physics_process\n（60 回/秒で一定）", "_process\n（描画ごと、間隔は不定）"])
    ax.set_xlabel("時間 [秒]")
    ax.set_xlim(-0.005, 0.2)
    ax.grid(axis="x", alpha=0.3)
    _save(fig, path)


def _arrow(ax: Axes, start: tuple[float, float], end: tuple[float, float], color: str, label: str) -> None:
    ax.annotate("", xy=end, xytext=start, arrowprops={"arrowstyle": "->", "color": color, "lw": 2})
    ax.text((start[0] + end[0]) / 2, (start[1] + end[1]) / 2, label, color=color, fontsize=11,
            ha="center", va="bottom")


def coordinates(path: Path) -> None:
    """数学の座標系と Godot の 2D 座標系の比較（第 10 章）。"""
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    for ax in axes:
        ax.set_xlim(-0.5, 4)
        ax.set_aspect("equal")
        ax.axis("off")
    ax = axes[0]
    ax.set_ylim(-0.5, 4)
    _arrow(ax, (0, 0), (3.5, 0), "black", "")
    _arrow(ax, (0, 0), (0, 3.5), "black", "")
    ax.text(3.6, 0, "+X", va="center")
    ax.text(0, 3.6, "+Y", ha="center")
    ax.plot(2, 1.5, "o", color=COLORS[1])
    ax.text(2.1, 1.6, "(2, 1.5)")
    curve = {"arrowstyle": "->", "connectionstyle": "arc3,rad=0.3", "color": COLORS[0]}
    ax.annotate("", xy=(1.2, 0.9), xytext=(1.5, 0), arrowprops=curve)
    ax.text(1.6, 0.5, "正の角度", color=COLORS[0])
    ax.set_title("数学の座標系（Y は上向き）")
    ax = axes[1]
    ax.set_ylim(4, -0.5)
    _arrow(ax, (0, 0), (3.5, 0), "black", "")
    _arrow(ax, (0, 0), (0, 3.5), "black", "")
    ax.text(3.6, 0, "+X", va="center")
    ax.text(0, 3.75, "+Y", ha="center")
    ax.plot(2, 1.5, "o", color=COLORS[1])
    ax.text(2.1, 1.4, "(2, 1.5)")
    curve = {"arrowstyle": "->", "connectionstyle": "arc3,rad=-0.3", "color": COLORS[0]}
    ax.annotate("", xy=(1.2, 0.9), xytext=(1.5, 0), arrowprops=curve)
    ax.text(1.6, 0.6, "正の角度\n（時計回り）", color=COLORS[0])
    ax.text(-0.3, -0.25, "原点（画面の左上）", fontsize=9)
    ax.set_title("Godot の 2D 座標系（Y は下向き）")
    _save(fig, path)


def vector_operations(path: Path) -> None:
    """位置の差による方向ベクトルと正規化（第 10 章）。"""
    fig, ax = plt.subplots(figsize=(6, 4))
    a = (1.0, 1.0)
    b = (5.0, 3.5)
    ax.plot(*a, "o", color="black")
    ax.plot(*b, "o", color="black")
    ax.text(a[0] - 0.2, a[1] - 0.45, "自分の位置 A")
    ax.text(b[0] - 0.6, b[1] + 0.25, "目標の位置 B")
    _arrow(ax, a, b, COLORS[0], "")
    ax.text(3.4, 1.5, "B - A\n（A から B へのベクトル）", color=COLORS[0], fontsize=11)
    length = math.hypot(b[0] - a[0], b[1] - a[1])
    unit = (a[0] + (b[0] - a[0]) / length, a[1] + (b[1] - a[1]) / length)
    ax.annotate("", xy=unit, xytext=a, arrowprops={"arrowstyle": "->", "color": COLORS[1], "lw": 3})
    ax.text(unit[0] + 0.1, unit[1] - 0.45, "normalized()\n（長さ 1）", color=COLORS[1])
    ax.set_xlim(0, 6.5)
    ax.set_ylim(0, 4.5)
    ax.set_aspect("equal")
    ax.grid(alpha=0.3)
    _save(fig, path)


def jump_trajectory(path: Path) -> None:
    """重力とジャンプによる高さの変化（第 11 章）。"""
    gravity = 980.0
    jump_velocity = 500.0
    fig, ax = plt.subplots(figsize=(7, 3.6))
    # 高さ y = v0 t - g t² / 2（床に戻るまで）
    flight_time = 2 * jump_velocity / gravity
    times = [flight_time * i / 200 for i in range(201)]
    heights = [jump_velocity * t - gravity * t * t / 2 for t in times]
    ax.plot(times, heights, color=COLORS[0])
    peak = jump_velocity ** 2 / (2 * gravity)
    ax.axhline(peak, color=COLORS[1], ls="--")
    ax.text(0.02, peak + 4, f"最高点 約 {peak:.0f} ピクセル", color=COLORS[1])
    ax.set_xlabel("ジャンプしてからの時間 [秒]")
    ax.set_ylabel("床からの高さ [ピクセル]")
    ax.set_ylim(0, peak * 1.25)
    ax.grid(alpha=0.3)
    _save(fig, path)


def _ease_out(ease_in: Callable[[float], float]) -> Callable[[float], float]:
    return lambda t: 1.0 - ease_in(1.0 - t)


def _bounce_out(t: float) -> float:
    if t < 1 / 2.75:
        return 7.5625 * t * t
    if t < 2 / 2.75:
        t -= 1.5 / 2.75
        return 7.5625 * t * t + 0.75
    if t < 2.5 / 2.75:
        t -= 2.25 / 2.75
        return 7.5625 * t * t + 0.9375
    t -= 2.625 / 2.75
    return 7.5625 * t * t + 0.984375


def easing_curves(path: Path) -> None:
    """Tween の主なイージング（EASE_OUT）の比較（第 12 章）。"""
    back = 1.70158
    curves: list[tuple[str, Callable[[float], float]]] = [
        ("TRANS_LINEAR", lambda t: t),
        ("TRANS_SINE", lambda t: math.sin(t * math.pi / 2)),
        ("TRANS_BACK", _ease_out(lambda t: t * t * ((back + 1) * t - back))),
        ("TRANS_BOUNCE", _bounce_out),
    ]
    fig, axes = plt.subplots(1, 4, figsize=(10, 2.8), sharey=True)
    samples = [i / 200 for i in range(201)]
    for ax, color, (name, curve) in zip(axes, COLORS, curves):
        ax.plot(samples, [curve(t) for t in samples], color=color, lw=2)
        ax.set_title(name, fontsize=10)
        ax.set_xlabel("時間の割合")
        ax.grid(alpha=0.3)
    axes[0].set_ylabel("変化の割合")
    _save(fig, path)


def linear_to_db(path: Path) -> None:
    """音量の割合とデシベルの関係（第 14 章）。"""
    fig, ax = plt.subplots(figsize=(6, 3.4))
    ratios = [i / 200 for i in range(2, 201)]
    ax.plot(ratios, [20 * math.log10(r) for r in ratios], color=COLORS[0])
    ax.set_xlabel("音量の割合（linear）")
    ax.set_ylabel("デシベル [dB]")
    ax.axhline(-6.02, color=COLORS[1], ls="--")
    ax.text(0.55, -9.5, "割合 0.5 は約 -6 dB", color=COLORS[1])
    ax.grid(alpha=0.3)
    _save(fig, path)


def uv_coordinates(path: Path) -> None:
    """テクスチャの UV 座標と波打ちシェーダーのずれ量（第 16 章）。"""
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    ax = axes[0]
    ax.add_patch(Rectangle((0, 0), 1, 1, fill=False, lw=2))
    for (u, v) in [(0, 0), (1, 0), (0, 1), (1, 1), (0.5, 0.5)]:
        ax.plot(u, v, "o", color=COLORS[1])
        ax.text(u + 0.03, v + 0.06, f"({u:g}, {v:g})")
    ax.set_xlim(-0.15, 1.35)
    ax.set_ylim(1.2, -0.15)
    ax.set_aspect("equal")
    ax.set_xlabel("UV.x（右へ増える）")
    ax.set_ylabel("UV.y（下へ増える）")
    ax.set_title("画像の UV 座標")
    ax = axes[1]
    ys = [i / 200 for i in range(201)]
    for color, time in zip(COLORS, [0.0, 0.25, 0.5]):
        ax.plot([0.05 * math.sin(y * 12.0 + time * 4.0) for y in ys], ys, color=color, label=f"TIME = {time}")
    ax.set_ylim(1, 0)
    ax.set_xlabel("横方向のずれ量（UV 単位）")
    ax.set_ylabel("UV.y")
    ax.set_title("sin(UV.y × 12 + TIME × 4) × 0.05")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    _save(fig, path)


def editor_layout(path: Path) -> None:
    """Godot エディターの既定の画面構成の模式図（第 4 章）。"""
    fig, ax = plt.subplots(figsize=(10, 6))
    # (左, 下, 幅, 高さ, 番号, 名前, 塗りの色)
    areas: list[tuple[float, float, float, float, str, str, str]] = [
        (0, 92, 30, 8, "1", "メニュー", "#dddddd"),
        (30, 92, 40, 8, "2", "メイン画面の切り替え", "#dddddd"),
        (70, 92, 30, 8, "3", "実行ボタン", "#dddddd"),
        (0, 58, 20, 34, "4", "シーン\n（インポート）", "#cfe2ff"),
        (0, 26, 20, 32, "5", "ファイルシステム\n（履歴）", "#cfe2ff"),
        (20, 26, 58, 66, "6", "メイン画面\n（ビューポートや\nスクリプトエディター）", "#ffffff"),
        (78, 26, 22, 66, "7", "インスペクター\n（シグナル、グループ）", "#d4edda"),
        (0, 0, 100, 26, "8", "下部パネル\n出力／デバッガー／オーディオ／アニメーション／シェーダーエディター など", "#fff3cd"),
    ]
    for left, bottom, width, height, number, name, color in areas:
        ax.add_patch(Rectangle((left, bottom), width, height, facecolor=color, edgecolor="#555555", lw=1.5))
        ax.text(left + width / 2, bottom + height / 2, name, ha="center", va="center", fontsize=10)
        ax.text(left + 1.2, bottom + height - 1.2, number, ha="left", va="top", fontsize=12, color="#b00020")
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    _save(fig, path)


def main(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    editor_layout(output_dir / "editor_layout.png")
    delta_comparison(output_dir / "delta_comparison.png")
    fixed_timestep(output_dir / "fixed_timestep.png")
    coordinates(output_dir / "coordinates.png")
    vector_operations(output_dir / "vector_operations.png")
    jump_trajectory(output_dir / "jump_trajectory.png")
    easing_curves(output_dir / "easing_curves.png")
    linear_to_db(output_dir / "linear_to_db.png")
    uv_coordinates(output_dir / "uv_coordinates.png")


if __name__ == "__main__":
    main(Path(__file__).resolve().parent.parent / "_generated" / "figures")
